"""Propose an improved skill description from eval findings."""

from __future__ import annotations

from .dataset import Example
from .evaluate import RubricReport, TriggerReport, run_trigger_eval, score_rubric
from .heuristics import extract_negatives, extract_triggers, tokenize, _STOPWORDS
from .llm import LLMClient
from .skills import Skill

_IMPROVE_SCHEMA = {
    "type": "object",
    "properties": {
        "improved_description": {"type": "string"},
        "rationale": {"type": "string"},
        "changes": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["improved_description", "rationale", "changes"],
    "additionalProperties": False,
}

# Common descriptive words that are too generic to be safe routing triggers.
# The offline miner drops these so it doesn't promote "fast"/"expert"/etc. into
# the description (which would over-fire the router). The LLM path doesn't use
# this — it writes clean prose directly.
_COMMON_WORDS = {
    "fast", "dense", "expert", "tone", "short", "full", "deep", "new", "core",
    "real", "good", "nice", "best", "give", "make", "want", "quick", "voice",
    "investors", "investor", "company", "patent", "filing", "this", "into",
    "summary", "summarize", "analyze", "analysis", "write", "draft",
}

_IMPROVE_SYSTEM = (
    "You improve a skill-routing DESCRIPTION (the frontmatter field a dispatcher "
    "reads to decide when to load a skill). Rewrite it so it fires on the prompts "
    "it should and stays quiet on the ones it shouldn't, and scores higher on "
    "clarity, trigger coverage, and scope boundaries.\n\n"
    "HARD CONSTRAINTS:\n"
    "- Preserve the skill's actual meaning and persona. Do NOT broaden it into a "
    "different skill.\n"
    "- Keep every out-of-scope ('NOT ...') boundary the original states.\n"
    "- Keep it a single dense paragraph; do not bloat it.\n"
    "- Only add triggers that are genuinely consistent with the skill's job."
)


def _offline_candidates(report: TriggerReport, skill: Skill) -> tuple[list[str], list[str]]:
    """Mine missing trigger terms (from FNs) and scope terms (from FPs)."""
    triggers = extract_triggers(skill.description)
    negatives = extract_negatives(skill.description)

    pos_add: dict[str, int] = {}
    neg_add: dict[str, int] = {}

    fn_prompts = [r["prompt"] for r in report.results if r["kind"] == "FN"]
    fp_prompts = [r["prompt"] for r in report.results if r["kind"] == "FP"]

    # Exclusion corpus = every prompt labelled should-not-trigger. A mined term is
    # rejected if it appears anywhere in here (substring, so Korean particle
    # agglutination — e.g. 특허 inside 특허에 — can't slip a false positive in).
    neg_text = " ".join(r["prompt"].lower() for r in report.results if not r["expected"])

    def salient(tok: str) -> bool:
        t = tok.lower()
        if t in _STOPWORDS or t in _COMMON_WORDS or any(t in trg for trg in triggers):
            return False
        if t in neg_text:  # would over-fire on a should-not-trigger prompt
            return False
        is_hangul = bool(__import__("re").fullmatch(r"[가-힣]+", tok))
        if is_hangul:
            return len(t) >= 2
        # Prefer distinctive English vocabulary: compounds, or longer-than-common.
        return "-" in t or len(t) >= 6

    for p in fn_prompts:
        for tok in tokenize(p):
            t = tok.lower()
            if salient(tok):
                pos_add[t] = pos_add.get(t, 0) + 1

    for p in fp_prompts:
        for tok in tokenize(p):
            t = tok.lower()
            if t in _STOPWORDS or len(t) < 4 or any(t in n for n in negatives):
                continue
            neg_add[t] = neg_add.get(t, 0) + 1

    pos = [w for w, _ in sorted(pos_add.items(), key=lambda kv: (-kv[1], kv[0]))][:8]
    neg = [w for w, _ in sorted(neg_add.items(), key=lambda kv: (-kv[1], kv[0]))][:6]
    return pos, neg


def propose_improved_description(
    client: LLMClient,
    skill: Skill,
    dataset: list[Example],
    trigger_report: TriggerReport | None = None,
    rubric_report: RubricReport | None = None,
) -> dict:
    """Return {improved_description, rationale, changes, mode}."""
    if trigger_report is None:
        trigger_report = run_trigger_eval(client, skill, dataset)
    if rubric_report is None:
        rubric_report = score_rubric(client, skill)

    if client.online:
        failures = trigger_report.failures
        fail_lines = "\n".join(
            f"- [{f['kind']}] expected_invoke={f['expected']} but predicted={f['predicted']}: {f['prompt']}"
            for f in failures
        ) or "(none — all trigger cases already correct)"
        weak = "\n".join(
            f"- {c['name']}: {c['score']}/{c['max']} — {c['comment']}" for c in rubric_report.criteria
        )
        user = (
            f"SKILL NAME: {skill.name}\n"
            f"CURRENT DESCRIPTION:\n{skill.description}\n\n"
            f"TRIGGER-EVAL FAILURES (router judged the description, these are wrong):\n{fail_lines}\n\n"
            f"RUBRIC BREAKDOWN:\n{weak}\n\n"
            "Rewrite the description to fix the failures and raise the weak rubric "
            "criteria, honouring the hard constraints. Return JSON."
        )
        try:
            out = client.complete_json(_IMPROVE_SYSTEM, user, _IMPROVE_SCHEMA, effort="high")
            return {
                "improved_description": " ".join(str(out["improved_description"]).split()),
                "rationale": str(out.get("rationale", "")),
                "changes": [str(c) for c in out.get("changes", [])],
                "mode": "online",
            }
        except Exception as exc:
            client.online = False
            client.reason = f"API call failed, fell back to heuristic: {exc}"

    # Offline: extend the description with mined trigger / scope terms.
    pos, neg = _offline_candidates(trigger_report, skill)
    improved = skill.description.rstrip()
    changes: list[str] = []
    if pos:
        improved += " Also triggers when the user asks for: " + ", ".join(pos) + "."
        changes.append(f"Added {len(pos)} trigger term(s) mined from missed prompts: {pos}")
    if neg:
        improved += " Does not apply to: " + ", ".join(neg) + "."
        changes.append(f"Added {len(neg)} out-of-scope term(s) mined from false-positive prompts: {neg}")
    if not changes:
        changes.append("No misclassified examples to learn from; description left unchanged.")
    return {
        "improved_description": " ".join(improved.split()),
        "rationale": "Heuristic improvement: learned trigger/scope vocabulary from misclassified examples.",
        "changes": changes,
        "mode": "offline",
    }
