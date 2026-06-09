#!/usr/bin/env python3
"""Figure-use gate for the patent-essay pipeline (north-star goal 2 support).

Goal 2 -- "the essay must make sufficient use of the patent's figures and
specification" -- has a deterministic component: every figure the Phase 1 Design
selected (`handoff/01-design/figure-selection.md`) must actually be referenced
in the composed draft. A selected-but-unused figure is an ORPHAN and fails.

The reverse is also flagged: a figure the draft references that the design never
selected means the composer pulled in an off-plan figure (warn -- the figure may
be legitimate but the selection record is now out of sync).

This complements gate_anchors' FIGREF-001 (which checks refs against the set of
AVAILABLE figures); this gate checks refs against the set of SELECTED figures and
checks for orphans in the other direction.

Context keys consumed:
  - figure_selection_text (str, optional): text of figure-selection.md. The
    figure numbers found here form the "selected" set.

Figure numbers are parsed from any of: "fig-07", "FIG. 7", "Figure 7", "Fig 7"
(case-insensitive), N an integer.

Checks:
  FIGUSE-000 (warn): no figure-selection provided -- check skipped.
  FIGUSE-001 (fail): a SELECTED figure is never referenced in the draft (orphan).
  FIGUSE-002 (warn): a figure REFERENCED in the draft is not in the selection.
"""

import argparse
import re
import sys

# ---------------------------------------------------------------------------
# Tunable constants
# ---------------------------------------------------------------------------
GATE_ID = "figure_use"
# Matches "fig-07", "FIG. 7", "Figure 7", "Fig 7", and sub-figures with a letter
# suffix: "fig-01A", "FIG. 1A", "Figure 5B". The identity is number+letter, so
# 1A and 1B are distinct figures.
FIG_RE = re.compile(r"\bfig(?:ure|\.|-)?\s*0*(\d+)([A-Za-z]?)\b", re.IGNORECASE)


SELECTED_HEADING_RE = re.compile(r"^#{1,6}\s+selected figures\b", re.IGNORECASE)
ANY_HEADING_RE = re.compile(r"^#{1,6}\s+\S")


HTML_COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)


def _figure_tokens(text):
    """Return the set of figure tokens mentioned in text (e.g. {'1A', '2'}).

    HTML comments are stripped first: a figure named only inside a `<!-- ... -->`
    annotation (e.g. "FIG. 1B ... NOT selected") is commentary, not a selection
    or a reference, and must not be counted.
    """
    body = HTML_COMMENT_RE.sub("", text or "")
    return {m.group(1) + m.group(2).upper() for m in FIG_RE.finditer(body)}


def _selected_section(text):
    """Return only the '## Selected figures' section of a figure-selection doc.

    figure-selection.md lists the chosen figures under a 'Selected figures'
    heading, then discusses dropped/paired figures in later sections. The
    selected set must come from the Selected-figures section only -- otherwise a
    figure merely mentioned as 'dropped' would be counted as selected and flagged
    as an orphan. If no such heading exists (bare-list fixtures), return the whole
    text for backward compatibility.
    """
    lines = (text or "").splitlines()
    start = None
    for i, line in enumerate(lines):
        if SELECTED_HEADING_RE.match(line):
            start = i + 1
            break
    if start is None:
        return text or ""
    end = len(lines)
    for j in range(start, len(lines)):
        if ANY_HEADING_RE.match(lines[j]):
            end = j
            break
    return "\n".join(lines[start:end])


def check(draft_text: str, context: dict) -> dict:
    findings = []
    context = context or {}

    selection_text = context.get("figure_selection_text")
    if selection_text is None:
        findings.append({
            "check_id": "FIGUSE-000",
            "severity": "warn",
            "message": "no figure-selection provided, figure-use check skipped",
            "location": "(global)",
        })
        return {"gate": GATE_ID, "passed": True, "findings": findings}

    selected = _figure_tokens(_selected_section(selection_text))
    used = _figure_tokens(draft_text)

    # FIGUSE-001: selected but never used (orphan).
    for tok in sorted(selected - used):
        findings.append({
            "check_id": "FIGUSE-001",
            "severity": "fail",
            "message": "selected figure %s is never referenced in the draft (orphan)" % tok,
            "location": "figure-selection",
        })

    # FIGUSE-002: used but not selected (off-plan figure).
    for tok in sorted(used - selected):
        findings.append({
            "check_id": "FIGUSE-002",
            "severity": "warn",
            "message": "draft references figure %s, which is not in figure-selection" % tok,
            "location": "draft",
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
    p = argparse.ArgumentParser(description="Figure-use gate (%s)" % GATE_ID)
    p.add_argument("draft", help="path to the draft Markdown file")
    p.add_argument("--figure-selection", help="path to figure-selection.md")
    args = p.parse_args(argv)
    with open(args.draft, "r", encoding="utf-8") as fh:
        text = fh.read()
    ctx = {}
    if args.figure_selection:
        with open(args.figure_selection, "r", encoding="utf-8") as fh:
            ctx["figure_selection_text"] = fh.read()
    result = check(text, ctx)
    _report(result)
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
