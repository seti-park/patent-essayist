#!/usr/bin/env python3
"""Arc-budget / structure-conformance gate for the patent-essay pipeline.

This gate enforces the "move the judgment earlier" design: per-section LENGTH and
STRUCTURE are DECIDED once in Phase 1 (the spine's `## Arc budget` declares each
arc role's share of the essay), and Phase 3 only runs a DETERMINISTIC conformance
check against that declaration. The arc is declared PER ESSAY (not a global
template), so the gate checks "does the draft conform to the arc THIS spine
declared", never "does it match a fixed shape" -- forcing a fixed shape would be
exactly the Goodhart failure this system avoids.

MEASUREMENT DISCIPLINE (anti-Goodhart): every check here is WARN severity and is
an elimination FILTER (a tolerance band), never a score to optimize. Section word
shares are recomputed from the DRAFT, not trusted from a self-reported field. See
_shared/references/scoring-rubric.md "Measurement discipline".

Context keys consumed:
  - thesis_spine_text (str): the spine markdown; its `## Arc budget` section is
    parsed for role -> (pct, once). ABSENT => gate self-skips (backward compatible).
  - thesis_trace_text (str): the trace markdown; each `### <section>` block's
    `arc_role` gives the ordered role per essay section.

Checks (all warn):
  ARC-000: no arc budget provided -- gate skipped (pass). Backward compatible.
  ARC-001: a role's actual body-word share deviates > TOLERANCE (relative) from
           its declared budget share.
  ARC-002: mapping incompleteness -- a trace role absent from the budget, a budget
           role absent from the trace, or draft section count != trace section count.
  ARC-003: a role the budget marks `once` maps to != 1 essay section.
  ARC-004: the budget percentages do not sum to ~100 (malformed declaration).
"""

import argparse
import re
import sys

# ---------------------------------------------------------------------------
# Tunable constants
# ---------------------------------------------------------------------------
GATE_ID = "arc"
TOLERANCE = 0.15           # ARC-001 relative band on a role's budgeted share
SUM_TOLERANCE_PP = 2.0     # ARC-004 allowed drift of the budget sum from 100 (pp)

SOURCES_HEADER_RE = re.compile(r"^#\s+Sources\s*$")
HTML_COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)
FENCE_RE = re.compile(r"^\s*(```|~~~)")
IMAGE_RE = re.compile(r"!\[[^\]]*\]\([^)]*\)")
H2_RE = re.compile(r"^##\s+\S")
H1_RE = re.compile(r"^#\s+\S")
ARCBUDGET_HEADER_RE = re.compile(r"^##\s+Arc budget\s*$", re.IGNORECASE)
ANY_H2_RE = re.compile(r"^##\s+")
# Budget — bullet form: "- lead: 10%" with optional "(once)".
BUDGET_LINE_RE = re.compile(
    r"^\s*[-*]\s*([A-Za-z][\w /()-]*?)\s*:\s*(\d+(?:\.\d+)?)\s*%\s*(\(once\))?",
    re.IGNORECASE)
# Budget — table row: "| turn (reversal) | 25 | once |".
BUDGET_ROW_RE = re.compile(
    r"^\s*\|\s*([A-Za-z][\w /()-]*?)\s*\|\s*(\d+(?:\.\d+)?)\s*%?\s*\|\s*(once)?\s*\|",
    re.IGNORECASE)
TRACE_SECTION_RE = re.compile(r"^#{3,4}\s+\S")
TRACE_ARCROLE_RE = re.compile(r"arc_role\W+([A-Za-z][\w /()-]*)", re.IGNORECASE)


def _norm_role(role):
    """Normalize a role label for matching: lowercase first token-ish word.
    'turn(reversal)' / 'turn (reversal)' / 'Turn' all normalize to 'turn'."""
    role = role.strip().lower()
    m = re.match(r"[a-z]+", role)
    return m.group(0) if m else role


def parse_arc_budget(spine_text):
    """Return {role: {'pct': float, 'once': bool}} from the spine's
    `## Arc budget` section, or {} if absent."""
    if not spine_text:
        return {}
    lines = spine_text.splitlines()
    start = None
    for i, line in enumerate(lines):
        if ARCBUDGET_HEADER_RE.match(line):
            start = i + 1
            break
    if start is None:
        return {}
    budget = {}
    for line in lines[start:]:
        if ANY_H2_RE.match(line) or H1_RE.match(line):
            break
        m = BUDGET_LINE_RE.match(line) or BUDGET_ROW_RE.match(line)
        if not m:
            continue
        role_raw = m.group(1).strip()
        # skip a table header row ("Role" / "Budget %")
        if _norm_role(role_raw) in ("role", "budget"):
            continue
        role = _norm_role(role_raw)
        budget[role] = {"pct": float(m.group(2)), "once": bool(m.group(3))}
    return budget


def parse_arc_trace(trace_text):
    """Return the ordered list of arc roles, one per `###`/`####` trace section."""
    if not trace_text:
        return []
    roles = []
    cur_has_role = None
    for line in trace_text.splitlines():
        if TRACE_SECTION_RE.match(line):
            if cur_has_role is not None:
                roles.append(cur_has_role)
            cur_has_role = ""          # opened a section, role unknown yet
            continue
        if cur_has_role is not None and not cur_has_role:
            m = TRACE_ARCROLE_RE.search(line)
            if m:
                cur_has_role = _norm_role(m.group(1))
    if cur_has_role is not None:
        roles.append(cur_has_role)
    # drop sections that never declared a role (empty string)
    return [r for r in roles if r]


def _body_lines(draft_text):
    """Body before `# Sources`, HTML comments + fenced code + image lines removed."""
    lines = draft_text.splitlines()
    end = len(lines)
    for i, line in enumerate(lines):
        if SOURCES_HEADER_RE.match(line):
            end = i
            break
    body = "\n".join(lines[:end])
    body = HTML_COMMENT_RE.sub("", body)
    out, in_fence = [], False
    for raw in body.splitlines():
        if FENCE_RE.match(raw):
            in_fence = not in_fence
            continue
        if not in_fence:
            out.append(raw)
    return out


def _word_count(text):
    return len(re.findall(r"\S+", IMAGE_RE.sub("", text)))


def draft_section_words(draft_text):
    """Word count per essay section, in order. Section boundaries are `##` (h2)
    headers; the body before the first `##` is the lead section. A title-only
    h1 line is not counted as a section start."""
    lines = _body_lines(draft_text)
    sections = []          # list of word counts
    buf = []

    def flush():
        if buf:
            sections.append(_word_count("\n".join(buf)))

    seen_h2 = False
    for raw in lines:
        if H2_RE.match(raw):
            flush()
            buf.clear()
            seen_h2 = True
            continue
        buf.append(raw)
    flush()
    # If there was a leading h1 title + lead before the first h2, the first
    # accumulated block is the lead. If no h2 at all, the whole body is 1 section.
    return [w for w in sections if w > 0] if seen_h2 else ([_word_count("\n".join(lines))]
                                                           if lines else [])


def check(draft_text: str, context: dict) -> dict:
    context = context or {}
    findings = []
    budget = parse_arc_budget(context.get("thesis_spine_text", ""))

    if not budget:
        findings.append({
            "check_id": "ARC-000",
            "severity": "warn",
            "message": "no `## Arc budget` declared in the spine; arc gate skipped",
            "location": "(global)",
        })
        return {"gate": GATE_ID, "passed": True, "findings": findings}

    # ARC-004: budget must sum to ~100.
    total_pct = sum(b["pct"] for b in budget.values())
    if abs(total_pct - 100.0) > SUM_TOLERANCE_PP:
        findings.append({
            "check_id": "ARC-004",
            "severity": "warn",
            "message": "arc budget sums to %.1f%% (expected ~100%%)" % total_pct,
            "location": "spine `## Arc budget`",
        })

    trace_roles = parse_arc_trace(context.get("thesis_trace_text", ""))
    section_words = draft_section_words(draft_text)

    # ARC-002: mapping completeness between budget, trace roles, and draft sections.
    budget_roles = set(budget)
    trace_role_set = set(trace_roles)
    for r in trace_role_set - budget_roles:
        findings.append({
            "check_id": "ARC-002",
            "severity": "warn",
            "message": "trace arc_role %r is not in the spine arc budget" % r,
            "location": "thesis-trace",
        })
    for r in budget_roles - trace_role_set:
        findings.append({
            "check_id": "ARC-002",
            "severity": "warn",
            "message": "budget role %r is carried by no trace section" % r,
            "location": "spine `## Arc budget`",
        })

    aligned = len(trace_roles) == len(section_words) and len(trace_roles) > 0
    if not aligned:
        findings.append({
            "check_id": "ARC-002",
            "severity": "warn",
            "message": "draft has %d sections but trace declares %d arc roles "
                       "(cannot map shares reliably)" % (len(section_words), len(trace_roles)),
            "location": "(document)",
        })

    # ARC-003: `once` roles must map to exactly one section.
    role_counts = {}
    for r in trace_roles:
        role_counts[r] = role_counts.get(r, 0) + 1
    for role, b in budget.items():
        if b["once"] and role_counts.get(role, 0) != 1:
            findings.append({
                "check_id": "ARC-003",
                "severity": "warn",
                "message": "role %r is marked `once` but maps to %d sections"
                           % (role, role_counts.get(role, 0)),
                "location": "thesis-trace",
            })

    # ARC-001: actual body-word share per role vs declared budget (only when the
    # draft sections and trace roles align one-to-one).
    if aligned:
        total_words = sum(section_words) or 1
        actual_by_role = {}
        for role, w in zip(trace_roles, section_words):
            actual_by_role[role] = actual_by_role.get(role, 0) + w
        for role, b in budget.items():
            target = b["pct"]
            actual_share = actual_by_role.get(role, 0) * 100.0 / total_words
            if target > 0 and abs(actual_share - target) / target > TOLERANCE:
                findings.append({
                    "check_id": "ARC-001",
                    "severity": "warn",
                    "message": "role %r is %.0f%% of the body, budget %.0f%% "
                               "(outside +/-%.0f%%)" % (role, actual_share, target, TOLERANCE * 100),
                    "location": "(body)",
                })

    passed = not any(f["severity"] == "fail" for f in findings)
    return {"gate": GATE_ID, "passed": passed, "findings": findings}


def _report(result):
    status = "PASS" if result["passed"] else "FAIL"
    print("[%s] gate=%s" % (status, result["gate"]))
    for f in result["findings"]:
        print("  %-5s %-12s %s  (%s)" % (
            f["severity"].upper(), f["check_id"], f["message"], f["location"]))
    if not result["findings"]:
        print("  (no findings)")


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="Arc-budget gate (%s)" % GATE_ID)
    p.add_argument("draft", help="path to the draft Markdown file")
    p.add_argument("--thesis-spine", help="path to thesis-spine.md (arc budget)")
    p.add_argument("--thesis-trace", help="path to thesis-trace.md (arc roles)")
    args = p.parse_args(argv)
    with open(args.draft, "r", encoding="utf-8") as fh:
        text = fh.read()
    ctx = {}
    if args.thesis_spine:
        with open(args.thesis_spine, "r", encoding="utf-8") as fh:
            ctx["thesis_spine_text"] = fh.read()
    if args.thesis_trace:
        with open(args.thesis_trace, "r", encoding="utf-8") as fh:
            ctx["thesis_trace_text"] = fh.read()
    result = check(text, ctx)
    _report(result)
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
