#!/usr/bin/env python3
"""Run-completeness checker: did the Compose↔Edit loop actually run?

The inner loop's historical escape hatches were all "the model said so": a
round-1 `pass` graded by the same context that composed, findings applied
without verification, promotion at the cap without a trace. This script makes
the loop's SHAPE mechanically checkable. The orchestrator must run it (and it
must pass) before archiving a run; the /goal acceptance string can require it.

Artifact contract (written by the orchestrator each round N = 1..K):
  handoff/03-edit/edit-log.round-N.md          review round N (feedback-format.md;
                                               findings carry finding_id rN-F<k>)
  handoff/03-edit/gate-result.round-N.json     run_gates.py --json output for round N
  handoff/02-compose/revision-response.round-N.md   composer dispositions for round N
                                               (required for every round FOLLOWED by
                                               another round)
  handoff/03-edit/essay-final.md               promotion target (acceptance only)
  handoff/03-edit/score-history.md             must contain "CAP HIT" if promoted at cap
  handoff/03-edit/revision-notes.md            self-audit deltas (essay mode)

Checks:
  RUN-001 (fail): round artifacts missing or non-contiguous (edit-log/gate-result
                  for rounds 1..K; revision-response for rounds 1..K-1).
  RUN-002 (fail): an edit-log has no parsable overall_assessment, or a gate
                  result JSON is unreadable.
  RUN-003 (fail): a medium/high/critical finding in round N has no disposition
                  block in revision-response.round-N.md, or a failing gate
                  check_id has none (rounds followed by another round only).
  RUN-004 (fail): a medium+ finding_id from round N-1 is never mentioned in
                  round N's edit-log (silently dropped instead of ruled on).
  RUN-005 (fail): essay-final.md exists but the acceptance rule is not met:
                  the LAST TWO rounds must both be clean (assessment acceptable
                  per --threshold AND gates passed) — a round-1 pass is a
                  hypothesis, not a verdict, until a fresh review confirms it —
                  UNLESS score-history.md declares "CAP HIT" (explicit
                  ship-best-round decision, surfaced to the user).
  RUN-006 (warn): promoted via CAP HIT (informational — unresolved findings ship).
  RUN-007 (fail): --self-audit on and essay-final.md exists, but
                  revision-notes.md is missing or has neither a "## delta"
                  block nor an explicit no-findings statement.
  RUN-000 (warn): informational skips.

Usage:
  check_run.py [--handoff handoff] [--threshold pass|revise-recommended]
               [--self-audit on|off] [--json]
Exit code 0 iff no fail-severity finding.
"""

import argparse
import glob
import json
import os
import re
import sys

ASSESS_RE = re.compile(r"^\s*overall_assessment:\s*(\S+)", re.M)
FINDING_ID_RE = re.compile(r"^\s*-\s*finding_id:\s*(r\d+-F\d+)", re.M)
SEVERITY_RE = re.compile(r"^\s*severity:\s*(\S+)", re.M)
CAP_HIT_RE = re.compile(r"\bCAP\s+HIT\b", re.I)
DELTA_RE = re.compile(r"^##\s+delta\b", re.M | re.I)
NO_FINDINGS_RE = re.compile(r"self-audit[^\n]*no[^\n]*finding", re.I)

ACCEPTABLE = {
    "pass": {"pass"},
    "revise-recommended": {"pass", "revise-recommended"},
}


def _read(path):
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read()


def _findings_with_severity(edit_log_text):
    """Return list of (finding_id, severity) from an edit-log.

    Tolerant block parser: a finding_id line opens a block; the first severity
    line before the next finding_id (or EOF) is its severity.
    """
    out = []
    pending = None
    for line in edit_log_text.splitlines():
        m = re.match(r"^\s*-\s*finding_id:\s*(r\d+-F\d+)", line)
        if m:
            if pending is not None:
                out.append((pending, "unspecified"))
            pending = m.group(1)
            continue
        if pending is not None:
            s = re.match(r"^\s*severity:\s*(\S+)", line)
            if s:
                out.append((pending, s.group(1).strip()))
                pending = None
    if pending is not None:
        out.append((pending, "unspecified"))
    return out


def check(handoff_dir, threshold="pass", self_audit="on"):
    findings = []
    edit_dir = os.path.join(handoff_dir, "03-edit")
    compose_dir = os.path.join(handoff_dir, "02-compose")

    def add(check_id, severity, message, location):
        findings.append({"check_id": check_id, "severity": severity,
                         "message": message, "location": location})

    # --- discover rounds --------------------------------------------------
    logs = glob.glob(os.path.join(edit_dir, "edit-log.round-*.md"))
    rounds = sorted(int(m.group(1)) for p in logs
                    for m in [re.search(r"edit-log\.round-(\d+)\.md$", p)] if m)
    if not rounds:
        add("RUN-001", "fail",
            "no edit-log.round-N.md artifacts found — the loop left no trace",
            edit_dir)
        return _result(findings)
    K = max(rounds)
    if rounds != list(range(1, K + 1)):
        add("RUN-001", "fail",
            "rounds are non-contiguous: found %s (expected 1..%d)" % (rounds, K),
            edit_dir)

    # --- per-round artifacts + parses -------------------------------------
    assessments = {}
    gates_passed = {}
    round_findings = {}
    for n in range(1, K + 1):
        log_path = os.path.join(edit_dir, "edit-log.round-%d.md" % n)
        gate_path = os.path.join(edit_dir, "gate-result.round-%d.json" % n)
        if not os.path.exists(log_path):
            continue  # RUN-001 already covers gaps
        text = _read(log_path)
        m = ASSESS_RE.search(text)
        if not m:
            add("RUN-002", "fail",
                "edit-log.round-%d.md has no parsable overall_assessment" % n, log_path)
        else:
            assessments[n] = m.group(1).strip()
        round_findings[n] = _findings_with_severity(text)

        if not os.path.exists(gate_path):
            add("RUN-001", "fail", "gate-result.round-%d.json missing" % n, edit_dir)
        else:
            try:
                gates_passed[n] = bool(json.loads(_read(gate_path)).get("passed"))
            except (ValueError, OSError) as e:
                add("RUN-002", "fail",
                    "gate-result.round-%d.json unreadable: %s" % (n, e), gate_path)

        # response required for every round followed by another round
        if n < K:
            resp_path = os.path.join(compose_dir, "revision-response.round-%d.md" % n)
            if not os.path.exists(resp_path):
                add("RUN-001", "fail",
                    "revision-response.round-%d.md missing (round %d was revised "
                    "without a disposition trace)" % (n, n), compose_dir)
            else:
                resp = _read(resp_path)
                for fid, sev in round_findings.get(n, []):
                    if sev in ("medium", "high", "critical", "unspecified") and fid not in resp:
                        add("RUN-003", "fail",
                            "finding %s (%s) has no disposition in "
                            "revision-response.round-%d.md" % (fid, sev, n), resp_path)
                gate_json = gates_passed.get(n)
                if gate_json is False:
                    try:
                        gate_data = json.loads(_read(os.path.join(
                            edit_dir, "gate-result.round-%d.json" % n)))
                        failing = {f["check_id"] for g in gate_data.get("gates", [])
                                   for f in g.get("findings", [])
                                   if f.get("severity") == "fail"}
                    except (ValueError, OSError):
                        failing = set()
                    for cid in sorted(failing):
                        if cid not in resp:
                            add("RUN-003", "fail",
                                "failing gate %s has no disposition in "
                                "revision-response.round-%d.md" % (cid, n), resp_path)

        # carried-id rule: every medium+ id from round n-1 must appear in round n's log
        if n > 1:
            prev = round_findings.get(n - 1, [])
            for fid, sev in prev:
                if sev in ("medium", "high", "critical", "unspecified") and fid not in text:
                    add("RUN-004", "fail",
                        "finding %s (round %d, %s) is never ruled on in round %d's "
                        "edit-log (silently dropped)" % (fid, n - 1, sev, n), log_path)

    # --- acceptance rule ----------------------------------------------------
    final_path = os.path.join(edit_dir, "essay-final.md")
    if os.path.exists(final_path):
        ok = ACCEPTABLE.get(threshold, {"pass"})

        def clean(n):
            return assessments.get(n) in ok and gates_passed.get(n) is True

        double_clean = K >= 2 and clean(K) and clean(K - 1)
        score_path = os.path.join(edit_dir, "score-history.md")
        cap_hit = os.path.exists(score_path) and bool(CAP_HIT_RE.search(_read(score_path)))
        if not double_clean and not cap_hit:
            add("RUN-005", "fail",
                "essay-final.md promoted without double-clean acceptance (last two "
                "rounds clean) and without an explicit CAP HIT in score-history.md — "
                "a single self-graded pass is not acceptance (K=%d, assessments=%s, "
                "gates=%s)" % (K, assessments, gates_passed), final_path)
        elif cap_hit and not double_clean:
            add("RUN-006", "warn",
                "promoted via CAP HIT — unresolved findings ship; surface them to the user",
                score_path)

        if self_audit == "on":
            notes_path = os.path.join(edit_dir, "revision-notes.md")
            if not os.path.exists(notes_path):
                add("RUN-007", "fail",
                    "self-audit is on but revision-notes.md is missing (no evidence "
                    "the post-acceptance audit ran)", edit_dir)
            else:
                notes = _read(notes_path)
                if not DELTA_RE.search(notes) and not NO_FINDINGS_RE.search(notes):
                    add("RUN-007", "fail",
                        "revision-notes.md has neither a '## delta' block nor an "
                        "explicit 'self-audit: no unresolved findings' statement",
                        notes_path)
    else:
        add("RUN-000", "warn",
            "essay-final.md not present — acceptance checks skipped (run in progress?)",
            edit_dir)

    return _result(findings)


def _result(findings):
    passed = not any(f["severity"] == "fail" for f in findings)
    return {"gate": "check_run", "passed": passed, "findings": findings}


def _report(result):
    status = "PASS" if result["passed"] else "FAIL"
    print("[%s] %s" % (status, result["gate"]))
    for f in result["findings"]:
        print("  %-5s %-8s %s  (%s)" % (
            f["severity"].upper(), f["check_id"], f["message"], f["location"]))
    if not result["findings"]:
        print("  (no findings)")


def main(argv=None):
    p = argparse.ArgumentParser(description="Loop run-completeness checker")
    p.add_argument("--handoff", default="handoff", help="handoff directory (default: handoff)")
    p.add_argument("--threshold", choices=["pass", "revise-recommended"], default="pass")
    p.add_argument("--self-audit", choices=["on", "off"], default="on")
    p.add_argument("--json", action="store_true")
    args = p.parse_args(argv)

    result = check(args.handoff, args.threshold, args.self_audit)
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        _report(result)
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
