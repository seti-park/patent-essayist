"""Trigger-accuracy and rubric evaluation of a skill description."""

from __future__ import annotations

from dataclasses import dataclass, field

from .dataset import Example
from .heuristics import extract_negatives, extract_triggers, heuristic_predict
from .llm import LLMClient
from .skills import Skill

# --------------------------------------------------------------------------- #
# Trigger accuracy
# --------------------------------------------------------------------------- #

_TRIGGER_SCHEMA = {
    "type": "object",
    "properties": {
        "should_invoke": {"type": "boolean"},
        "confidence": {"type": "number"},
        "reason": {"type": "string"},
    },
    "required": ["should_invoke", "confidence", "reason"],
    "additionalProperties": False,
}

_ROUTER_SYSTEM = (
    "You are a skill router. You are given ONE skill's name and description, and "
    "a user prompt. Decide solely from the description whether this skill should "
    "be invoked to handle the prompt. Judge only what the description claims to "
    "cover, including any scope exclusions it states. Do not use outside knowledge "
    "of what the skill might do."
)


def judge_trigger(client: LLMClient, skill: Skill, prompt: str) -> dict:
    """Return {should_invoke, confidence, reason}."""
    if client.online:
        user = (
            f"SKILL NAME: {skill.name}\n"
            f"SKILL DESCRIPTION:\n{skill.description}\n\n"
            f"USER PROMPT:\n{prompt}\n\n"
            "Should this skill be invoked? Respond as JSON."
        )
        try:
            out = client.complete_json(
                _ROUTER_SYSTEM, user, _TRIGGER_SCHEMA, effort="low", thinking=False, max_tokens=1024
            )
            return {
                "should_invoke": bool(out["should_invoke"]),
                "confidence": float(out.get("confidence", 0.5)),
                "reason": str(out.get("reason", "")),
            }
        except Exception as exc:  # fall through to heuristic on any API failure
            client.online = False
            client.reason = f"API call failed, fell back to heuristic: {exc}"

    triggers = extract_triggers(skill.description)
    negatives = extract_negatives(skill.description)
    decision, conf, reason = heuristic_predict(triggers, negatives, prompt)
    return {"should_invoke": decision, "confidence": conf, "reason": reason}


@dataclass
class TriggerReport:
    mode: str
    results: list[dict] = field(default_factory=list)
    tp: int = 0
    fp: int = 0
    tn: int = 0
    fn: int = 0

    @property
    def total(self) -> int:
        return self.tp + self.fp + self.tn + self.fn

    @property
    def accuracy(self) -> float:
        return (self.tp + self.tn) / self.total if self.total else 0.0

    @property
    def precision(self) -> float:
        denom = self.tp + self.fp
        return self.tp / denom if denom else 0.0

    @property
    def recall(self) -> float:
        denom = self.tp + self.fn
        return self.tp / denom if denom else 0.0

    @property
    def f1(self) -> float:
        p, r = self.precision, self.recall
        return 2 * p * r / (p + r) if (p + r) else 0.0

    @property
    def failures(self) -> list[dict]:
        return [r for r in self.results if not r["correct"]]

    def to_dict(self) -> dict:
        return {
            "mode": self.mode,
            "counts": {"tp": self.tp, "fp": self.fp, "tn": self.tn, "fn": self.fn},
            "metrics": {
                "accuracy": round(self.accuracy, 4),
                "precision": round(self.precision, 4),
                "recall": round(self.recall, 4),
                "f1": round(self.f1, 4),
            },
            "results": self.results,
        }


def run_trigger_eval(client: LLMClient, skill: Skill, dataset: list[Example]) -> TriggerReport:
    report = TriggerReport(mode=client.mode)
    for ex in dataset:
        out = judge_trigger(client, skill, ex.prompt)
        predicted = out["should_invoke"]
        correct = predicted == ex.should_trigger
        if ex.should_trigger and predicted:
            kind = "TP"
            report.tp += 1
        elif ex.should_trigger and not predicted:
            kind = "FN"
            report.fn += 1
        elif not ex.should_trigger and predicted:
            kind = "FP"
            report.fp += 1
        else:
            kind = "TN"
            report.tn += 1
        report.results.append(
            {
                "id": ex.id,
                "prompt": ex.prompt,
                "expected": ex.should_trigger,
                "predicted": predicted,
                "correct": correct,
                "kind": kind,
                "confidence": round(float(out["confidence"]), 3),
                "reason": out["reason"],
            }
        )
    # mode may have flipped to offline mid-run if the API failed
    report.mode = client.mode
    return report


# --------------------------------------------------------------------------- #
# Rubric score
# --------------------------------------------------------------------------- #

_RUBRIC_CRITERIA = [
    ("trigger_coverage", 30, "Lists concrete situations/keywords that should invoke the skill."),
    ("scope_boundaries", 20, "States what is OUT of scope so the skill does not over-fire."),
    ("purpose_clarity", 20, "Makes the skill's job and output unambiguous."),
    ("concrete_examples", 15, "Gives concrete example phrasings rather than only abstractions."),
    ("conciseness", 15, "Dense and scannable, not padded or bloated."),
]

_RUBRIC_SCHEMA = {
    "type": "object",
    "properties": {
        "criteria": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "score": {"type": "integer"},
                    "max": {"type": "integer"},
                    "comment": {"type": "string"},
                },
                "required": ["name", "score", "max", "comment"],
                "additionalProperties": False,
            },
        },
        "summary": {"type": "string"},
    },
    "required": ["criteria", "summary"],
    "additionalProperties": False,
}

_RUBRIC_SYSTEM = (
    "You grade the quality of a skill-routing DESCRIPTION (the frontmatter field "
    "a dispatcher reads to decide when to load the skill). Score each criterion "
    "from 0 to its max. A good description is trigger-rich, states its scope "
    "boundaries, is unambiguous about its job, gives concrete example phrasings, "
    "and stays concise. Be a tough but fair grader."
)


@dataclass
class RubricReport:
    mode: str
    criteria: list[dict]
    summary: str

    @property
    def overall(self) -> int:
        return sum(int(c["score"]) for c in self.criteria)

    @property
    def max_total(self) -> int:
        return sum(int(c["max"]) for c in self.criteria)

    def to_dict(self) -> dict:
        return {
            "mode": self.mode,
            "overall": self.overall,
            "max_total": self.max_total,
            "criteria": self.criteria,
            "summary": self.summary,
        }


def _heuristic_rubric(skill: Skill) -> RubricReport:
    desc = skill.description
    triggers = extract_triggers(desc)
    negatives = extract_negatives(desc)
    length = len(desc)
    has_examples = ("," in desc and ("such as" in desc.lower() or "asks for" in desc.lower() or len(triggers) >= 3))

    criteria = []

    cov = min(30, 5 * len(triggers))
    criteria.append({
        "name": "trigger_coverage", "score": cov, "max": 30,
        "comment": f"{len(triggers)} distinct trigger term(s) detected: {sorted(triggers)}",
    })

    scope = 20 if negatives else 4
    criteria.append({
        "name": "scope_boundaries", "score": scope, "max": 20,
        "comment": (f"explicit out-of-scope markers: {sorted(negatives)}" if negatives
                    else "no 'NOT ...' scope boundary stated"),
    })

    has_use_when = bool(__import__("re").search(r"\buse\s+wh(en|enever)\b", desc, __import__("re").I))
    purpose = 20 if (has_use_when and length > 120) else (12 if length > 80 else 6)
    criteria.append({
        "name": "purpose_clarity", "score": purpose, "max": 20,
        "comment": ("states job and an explicit 'Use when/whenever' clause"
                    if has_use_when else "purpose stated but no explicit trigger clause"),
    })

    examples = 15 if has_examples else 5
    criteria.append({
        "name": "concrete_examples", "score": examples, "max": 15,
        "comment": "enumerates concrete example phrasings" if has_examples
                   else "few/no concrete example phrasings",
    })

    if length < 80:
        conc, cnote = 6, f"too thin ({length} chars) — likely under-specified"
    elif length <= 650:
        conc, cnote = 15, f"good density ({length} chars)"
    elif length <= 950:
        conc, cnote = 11, f"slightly long ({length} chars)"
    else:
        conc, cnote = 6, f"bloated ({length} chars) — trim"
    criteria.append({"name": "conciseness", "score": conc, "max": 15, "comment": cnote})

    overall = sum(c["score"] for c in criteria)
    summary = (
        f"Heuristic rubric: {overall}/100. "
        + ("Strong trigger coverage. " if cov >= 20 else "Trigger coverage is thin. ")
        + ("Scope boundary present. " if negatives else "Add an out-of-scope boundary. ")
    )
    return RubricReport(mode="offline", criteria=criteria, summary=summary)


def score_rubric(client: LLMClient, skill: Skill) -> RubricReport:
    if client.online:
        criteria_spec = "\n".join(f"- {n} (max {m}): {d}" for n, m, d in _RUBRIC_CRITERIA)
        user = (
            f"SKILL NAME: {skill.name}\n"
            f"DESCRIPTION:\n{skill.description}\n\n"
            f"Grade against these criteria:\n{criteria_spec}\n\n"
            "Return JSON with one entry per criterion (name, score, max, comment) "
            "and a short summary."
        )
        try:
            out = client.complete_json(_RUBRIC_SYSTEM, user, _RUBRIC_SCHEMA, effort="high")
            return RubricReport(mode="online", criteria=out["criteria"], summary=out.get("summary", ""))
        except Exception as exc:
            client.online = False
            client.reason = f"API call failed, fell back to heuristic: {exc}"

    return _heuristic_rubric(skill)
