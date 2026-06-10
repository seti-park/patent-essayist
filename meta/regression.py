#!/usr/bin/env python3
"""Regression guard for pipeline-retro improvement proposals.

A proposal from `pipeline-retro` (under meta/improvement-proposals/) changes a skill,
reference, gate, or canon. Before a human applies it, run this to confirm nothing regresses:

  1. the deterministic gate test suite still passes
     (_shared/scripts/test_gates.py), and
  2. every fixture under meta/fixtures/ still produces its expected gate verdict
     (and, where declared, no longer exhibits the previously-recurring defect check_id).

A proposal that breaks (1) or worsens any fixture in (2) must be rejected.

Each fixture is a directory meta/fixtures/<name>/ containing:
  - expect.json     : {"gate_pass": true|false,                             # optional (needs draft.md)
                       "tcard_pass": true|false,                            # optional (needs thesis-spine.md;
                                                                            #  runs check_thesis_card.py)
                       "audience": "deep"|"investor",                       # optional (default deep)
                       "must_not_contain_check_ids": ["FIGUSE-001", ...],   # optional
                       "must_contain_check_ids": ["SOURCES-002", ...]}      # optional
  - draft.md        : the essay draft to run gates over (optional for
                      thesis-card-only fixtures)
  - invention-summary.md   (optional context)
  - figures-index.txt      (optional, ints one per line)
  - figure-selection.md    (optional)

Usage:
  python meta/regression.py            # run gate tests + all fixtures
  python meta/regression.py --fixtures-only
Exit code 0 iff everything passes.
"""

import argparse
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
SCRIPTS = os.path.join(REPO, ".claude", "skills", "_shared", "scripts")
FIXTURES = os.path.join(HERE, "fixtures")

sys.path.insert(0, SCRIPTS)


def _expected_assessment(severities):
    """severity list -> overall_assessment, per the editorial severity model
    (shared by editorial-review and prepublish-verify). Low/none never escalate."""
    s = set(severities)
    if "critical" in s or "high" in s:
        return "revise-required"
    if "medium" in s:
        return "revise-recommended"
    return "pass"


def _check_verification_log(path):
    """Validate the severity->assessment invariant on a verification-log.md.

    Stdlib-only (the project is stdlib): pull the declared `overall_assessment`
    and the per-finding `severity:` lines from the fenced YAML and confirm they
    agree with the shared severity model. Returns True on pass.
    """
    text = _load(path)
    decl = re.search(r"^\s*overall_assessment:\s*([a-z-]+)\s*$", text, re.MULTILINE)
    if not decl:
        print("  FAIL %s: no overall_assessment declared" % path)
        return False
    severities = re.findall(r"^\s*severity:\s*(critical|high|medium|low)\s*$",
                            text, re.MULTILINE)
    expected = _expected_assessment(severities)
    got = decl.group(1)
    if got != expected:
        print("  FAIL %s: overall_assessment=%s but severities %s imply %s"
              % (os.path.relpath(path, REPO), got, severities or "[]", expected))
        return False
    print("  ok   %s (assessment=%s)" % (os.path.relpath(path, REPO), got))
    return True


def _check_verification_logs():
    """Run the invariant over the template + any fixture verification-log.md files."""
    print("== verification-log consistency ==")
    paths = []
    tmpl = os.path.join(REPO, "handoff-template", "03-edit", "verification-log.md")
    if os.path.exists(tmpl):
        paths.append(tmpl)
    if os.path.isdir(FIXTURES):
        for d in sorted(os.listdir(FIXTURES)):
            vlog = os.path.join(FIXTURES, d, "verification-log.md")
            if os.path.exists(vlog):
                paths.append(vlog)
    if not paths:
        print("  (no verification-log.md found)")
        return True
    return all(_check_verification_log(p) for p in paths)


def _run_gate_tests():
    """Run the gate unittest suite as a subprocess. Return True on success."""
    test_path = os.path.join(SCRIPTS, "test_gates.py")
    print("== gate test suite ==")
    rc = subprocess.call([sys.executable, test_path])
    return rc == 0


def _load(path):
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read()


def _run_fixture(name):
    """Run gates (and/or the thesis-card check) over one fixture; compare to
    expect.json. Return True on pass."""
    import run_gates  # imported here so a broken edit surfaces as a clear failure

    fdir = os.path.join(FIXTURES, name)
    expect = json.loads(_load(os.path.join(fdir, "expect.json")))

    ctx = {"mode": "essay", "audience": expect.get("audience", "deep")}
    inv = os.path.join(fdir, "invention-summary.md")
    if os.path.exists(inv):
        ctx["invention_summary_text"] = _load(inv)
    figs = os.path.join(fdir, "figures-index.txt")
    if os.path.exists(figs):
        ctx["figures_index"] = [t.upper() for t in _load(figs).split()]
    sel = os.path.join(fdir, "figure-selection.md")
    if os.path.exists(sel):
        ctx["figure_selection_text"] = _load(sel)
    spine = os.path.join(fdir, "thesis-spine.md")
    if os.path.exists(spine):
        ctx["thesis_spine_text"] = _load(spine)
    trace = os.path.join(fdir, "thesis-trace.md")
    if os.path.exists(trace):
        ctx["thesis_trace_text"] = _load(trace)

    seen = set()
    ok = True

    draft_path = os.path.join(fdir, "draft.md")
    if os.path.exists(draft_path):
        overall, results = run_gates.run_all(_load(draft_path), ctx)
        seen |= {f["check_id"] for r in results for f in r["findings"]}
        if "gate_pass" in expect and overall != expect["gate_pass"]:
            print("  FAIL %s: gate_pass expected %s, got %s" % (name, expect["gate_pass"], overall))
            ok = False

    # thesis-card check (P1 pre-compose, standalone): opt in via expect.tcard_pass.
    if "tcard_pass" in expect:
        import check_thesis_card
        tres = check_thesis_card.check(ctx.get("thesis_spine_text", ""))
        seen |= {f["check_id"] for f in tres["findings"]}
        if tres["passed"] != expect["tcard_pass"]:
            print("  FAIL %s: tcard_pass expected %s, got %s"
                  % (name, expect["tcard_pass"], tres["passed"]))
            ok = False
    for cid in expect.get("must_not_contain_check_ids", []):
        if cid in seen:
            print("  FAIL %s: regressed -- %s present (must not contain)" % (name, cid))
            ok = False
    for cid in expect.get("must_contain_check_ids", []):
        if cid not in seen:
            print("  FAIL %s: expected %s not detected" % (name, cid))
            ok = False
    if ok:
        print("  ok   %s" % name)
    return ok


def main(argv=None):
    p = argparse.ArgumentParser(description="pipeline-retro regression guard")
    p.add_argument("--fixtures-only", action="store_true")
    args = p.parse_args(argv)

    all_ok = True
    if not args.fixtures_only:
        all_ok = _run_gate_tests() and all_ok

    print("== fixtures ==")
    if not os.path.isdir(FIXTURES):
        print("  (no fixtures directory)")
    else:
        names = sorted(
            d for d in os.listdir(FIXTURES)
            if os.path.isdir(os.path.join(FIXTURES, d))
        )
        if not names:
            print("  (no fixtures yet)")
        for name in names:
            all_ok = _run_fixture(name) and all_ok

    all_ok = _check_verification_logs() and all_ok

    print("\nREGRESSION: %s" % ("PASS" if all_ok else "FAIL"))
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
