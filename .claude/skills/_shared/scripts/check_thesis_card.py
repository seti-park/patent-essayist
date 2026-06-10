#!/usr/bin/env python3
"""Thesis-card conformance check for the patent-essay pipeline (P1, pre-compose).

Runs on handoff/01-design/thesis-spine.md RIGHT AFTER Phase 1 and BEFORE Phase 2
-- the cheapest point to kill a weak thesis. It is a STANDALONE script, not part
of run_gates.py: run_gates runs on the Phase-2 draft, which is too late for this
purpose.

The design move is the same as gate_arc: the unverifiable judgment ("is this
thesis interesting?") is decomposed so its verifiable half becomes a declaration
plus a conformance check. "Interesting = distance between a REAL prevailing view
(통념) and the patent evidence" -- and the REALITY of the 통념 is mechanically
checkable: the spine's `## Consensus evidence` section must carry live external
citations proving someone actually holds that view. A 통념 nobody holds is a
strawman, and overturning it is not a thesis.

MEASUREMENT DISCIPLINE (anti-Goodhart): every check is an elimination FILTER,
never a score. The non-mechanical half (how decisively the evidence overturns
the consensus) is handled by the pairwise tournament in thesis-candidates.md and
the pre-compose SETI checkpoint -- relative judgment and human authority, no
absolute scoring. See _shared/references/scoring-rubric.md.

Checks:
  TCARD-000 (warn): spine file empty, or `## Consensus evidence` section absent
            (legacy spine predating the schema -- consensus checks skipped; the
            orchestrator treats this as fail-equivalent on NEW runs).
  TCARD-001 (fail): `## Selected thesis` absent or empty.
  TCARD-002 (fail): a 4-axis section is absent/empty, or Axes 1-3 lack a patent
            anchor (`[dddd]` or a claim reference). Axis 4 (baseline) is external
            by design and only needs content.
  TCARD-003 (fail): `## Consensus evidence` present but carries ZERO external
            citations (URL heuristic). The strawman filter.
  TCARD-004 (warn): only ONE consensus citation (>=2 is clean).
  TCARD-005 (warn): Adversarial defense's Residual risk carries no falsifiability
            (no `none` / `Acknowledged` / `Acceptance` / falsifier language).
  TCARD-006 (fail): `## Arc budget` absent, or its shares sum outside 90-110%.
            Reuses gate_arc.parse_arc_budget -- single parser, no duplication.
  TCARD-007 (warn): a budget role appears nowhere in the spine's
            `## Spine -> section trace` table (coverage heuristic).
"""

import argparse
import json
import re
import sys

import gate_arc

GATE_ID = "thesis_card"

HTML_COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)
H2_RE = re.compile(r"^##\s+(.*\S)\s*$")
ANCHOR_RE = re.compile(r"\[\d{4}\]")
CLAIM_RE = re.compile(r"(청구항\s*\d+|claims?\s+\d+|\bclaim\s*\d+)", re.IGNORECASE)
URL_RE = re.compile(r"https?://\S+|www\.\S+", re.IGNORECASE)
AXIS_RE = re.compile(r"^###\s+Axis\s+(\d)\b", re.IGNORECASE)
FALSIFIABILITY_RE = re.compile(
    r"residual risk[^\n]*\n?.*?(none|acknowledged|acceptance|falsif)",
    re.IGNORECASE | re.DOTALL)

SUM_LOW, SUM_HIGH = 90.0, 110.0


def _sections(text):
    """Return {h2-title-lowercased: body} with HTML comments stripped first,
    so template placeholder text inside comments never satisfies a check."""
    text = HTML_COMMENT_RE.sub("", text or "")
    out, title, buf = {}, None, []
    for line in text.splitlines():
        m = H2_RE.match(line)
        if m:
            if title is not None:
                out[title] = "\n".join(buf)
            title = m.group(1).strip().lower()
            buf = []
        elif title is not None:
            buf.append(line)
    if title is not None:
        out[title] = "\n".join(buf)
    return out


def _find_section(sections, prefix):
    """First section whose title starts with prefix (titles carry suffixes like
    '(통념 실재 검증)' or arrows)."""
    for title, body in sections.items():
        if title.startswith(prefix):
            return body
    return None


def _axes(grounding_body):
    """Return {axis_number: body} from the 4-axis grounding section."""
    if grounding_body is None:
        return {}
    axes, cur, buf = {}, None, []
    for line in grounding_body.splitlines():
        m = AXIS_RE.match(line)
        if m:
            if cur is not None:
                axes[cur] = "\n".join(buf)
            cur = int(m.group(1))
            buf = []
        elif cur is not None:
            buf.append(line)
    if cur is not None:
        axes[cur] = "\n".join(buf)
    return axes


def check(spine_text: str, context: dict = None) -> dict:
    findings = []

    def add(check_id, severity, message, location):
        findings.append({"check_id": check_id, "severity": severity,
                         "message": message, "location": location})

    if not (spine_text or "").strip():
        add("TCARD-000", "warn",
            "thesis-spine is empty/absent; thesis-card check skipped", "(file)")
        return {"gate": GATE_ID, "passed": True, "findings": findings}

    sections = _sections(spine_text)

    # TCARD-001: selected thesis present + non-empty.
    thesis = _find_section(sections, "selected thesis")
    if thesis is None or not thesis.strip():
        add("TCARD-001", "fail",
            "`## Selected thesis` absent or empty", "spine")

    # TCARD-002: 4-axis grounding -- all axes present; Axes 1-3 anchored.
    grounding = _find_section(sections, "4-axis grounding")
    axes = _axes(grounding)
    for n in (1, 2, 3, 4):
        body = (axes.get(n) or "").strip()
        if not body:
            add("TCARD-002", "fail",
                "Axis %d section absent or empty" % n, "spine `## 4-axis grounding`")
        elif n <= 3 and not (ANCHOR_RE.search(body) or CLAIM_RE.search(body)):
            add("TCARD-002", "fail",
                "Axis %d carries no patent anchor ([dddd] or claim reference)" % n,
                "spine `## 4-axis grounding`")

    # TCARD-000/003/004: consensus evidence (the strawman filter).
    consensus = _find_section(sections, "consensus evidence")
    if consensus is None:
        add("TCARD-000", "warn",
            "no `## Consensus evidence` section (legacy spine schema); "
            "consensus-reality check skipped -- fail-equivalent on new runs",
            "spine")
    else:
        citations = sum(1 for line in consensus.splitlines() if URL_RE.search(line))
        if citations == 0:
            add("TCARD-003", "fail",
                "consensus evidence carries zero external citations -- "
                "an uncited 통념 is a potential strawman", "spine `## Consensus evidence`")
        elif citations == 1:
            add("TCARD-004", "warn",
                "only one consensus citation (>=2 is clean)", "spine `## Consensus evidence`")

    # TCARD-005: falsifiability in the adversarial defense's residual risk.
    defense = _find_section(sections, "adversarial defense")
    if defense is None or not FALSIFIABILITY_RE.search(defense):
        add("TCARD-005", "warn",
            "Residual risk carries no falsifiability "
            "(none/Acknowledged/Acceptance/falsifier)", "spine `## Adversarial defense`")

    # TCARD-006: arc budget present + sane sum (reuse gate_arc's parser).
    budget = gate_arc.parse_arc_budget(spine_text)
    if not budget:
        add("TCARD-006", "fail",
            "`## Arc budget` absent or unparseable", "spine")
    else:
        total = sum(b["pct"] for b in budget.values())
        if not (SUM_LOW <= total <= SUM_HIGH):
            add("TCARD-006", "fail",
                "arc budget sums to %.1f%% (expected %.0f-%.0f%%)"
                % (total, SUM_LOW, SUM_HIGH), "spine `## Arc budget`")

    # TCARD-007: every budget role should surface in the spine -> section trace.
    trace = _find_section(sections, "spine")  # "spine → section trace" / "spine -> ..."
    if budget and trace:
        trace_lower = trace.lower()
        for role in budget:
            if role not in trace_lower:
                add("TCARD-007", "warn",
                    "budget role %r appears nowhere in the spine->section trace" % role,
                    "spine `## Spine → section trace`")

    passed = not any(f["severity"] == "fail" for f in findings)
    return {"gate": GATE_ID, "passed": passed, "findings": findings}


def _report(result):
    status = "PASS" if result["passed"] else "FAIL"
    print("[%s] gate=%s" % (status, result["gate"]))
    for f in result["findings"]:
        print("  %-5s %-10s %s  (%s)" % (
            f["severity"].upper(), f["check_id"], f["message"], f["location"]))
    if not result["findings"]:
        print("  (no findings)")


def main(argv=None) -> int:
    p = argparse.ArgumentParser(
        description="Thesis-card conformance check (P1, pre-compose)")
    p.add_argument("--thesis-spine", required=True,
                   help="path to handoff/01-design/thesis-spine.md")
    p.add_argument("--json", action="store_true", help="JSON output")
    args = p.parse_args(argv)
    try:
        with open(args.thesis_spine, "r", encoding="utf-8") as fh:
            spine_text = fh.read()
    except OSError:
        spine_text = ""
    result = check(spine_text, {})
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        _report(result)
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
