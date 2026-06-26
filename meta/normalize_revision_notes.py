#!/usr/bin/env python3
"""Normalize a revision-notes.md into findings-ledger.jsonl records.

The **revision-delta capture channel**. Post-acceptance human edits (the delta from the
edit-log-applied draft to the published final) are logged as `## delta` blocks in
`handoff/03-edit/revision-notes.md` (schema: `handoff-template/03-edit/revision-notes.md`).
This deterministic normalizer turns each block into a ledger record tagged
`origin: human-post-accept` / `source: human-revision`, so `pipeline-retro` can score
recurrence over the editorial blind-spots a human catches AFTER the loop says "pass" — the
half the gates/passes don't yet see. See
`meta/improvement-proposals/2026-06-26-human-revision-blindspots.md`.

`origin` distinguishes "the loop missed it" (`inner-loop`, the default for gate/editorial
records) from "the loop never had a chance to see it" (`human-post-accept`). Both are useful;
they motivate different fixes (tune a pass vs. extend coverage).

Usage:
  python meta/normalize_revision_notes.py --notes handoff/03-edit/revision-notes.md \
      --essay-id 045-agility-638-last-mile-moat [--timestamp 2026-06-26T00:00:00Z]
  python meta/normalize_revision_notes.py --notes NOTES.md --essay-id ID --append meta/findings-ledger.jsonl
  python meta/normalize_revision_notes.py --selftest
"""

import argparse
import json
import re
import sys
from datetime import datetime, timezone

# class (pattern_tag) -> (goal, root_cause_stage, root_cause_artifact). Mirrors the
# human-revision rows in meta/attribution-table.md. Unknown classes fall through to a
# flag so a new attribution-table row gets proposed.
CLASS_MAP = {
    "lead-thesis-deferral": ("4a", "compose", "section-blueprint lead block / thesis-spine arc"),
    "nonclaim-section-header": ("4a", "compose", "section-blueprint header / x-articles-format-en"),
    "meta-reader-instruction": ("4b", "canon", "anti-ai-writing.md -> gate_meta"),
    "jargon-overdepth": ("3", "compose", "deliverable-voice-rules.md"),
    "steelman-absent": ("1", "design", "thesis-spine adversarial-defense -> phase2-handoff-notes"),
    "section-stub-imbalance": ("4a", "compose", "section-blueprint word_target balance"),
    "thesis-restatement-redundancy": ("3", "compose", "section-blueprint (redundancy-bloat sub-mechanism)"),
    "revision-induced-duplication": ("4b", "compose", "essay-en-composer revision-mode re-scan"),
    "venue-ticker-convention": ("4a", "compose", "x-articles-format-en.md"),
}
_KEYS = ("class", "round", "before", "after", "rationale", "goal")
_KV_RE = re.compile(r"\s*([A-Za-z_]+)\s*:\s*(.*)$")


def parse_notes(text):
    """Parse `## delta` blocks into a list of dicts (each must carry `class`)."""
    deltas, cur = [], None
    for raw in text.splitlines():
        stripped = raw.strip()
        if stripped.lower() == "## delta":
            if cur is not None:
                deltas.append(cur)
            cur = {}
            continue
        if cur is None:
            continue
        if stripped.startswith("#"):          # any other heading closes the block
            deltas.append(cur)
            cur = None
            continue
        m = _KV_RE.match(raw)
        if m and m.group(1).lower() in _KEYS:
            cur[m.group(1).lower()] = m.group(2).strip()
    if cur is not None:
        deltas.append(cur)
    return [d for d in deltas if d.get("class")]


def to_record(d, essay_id, ts):
    cls = d["class"]
    if cls in CLASS_MAP:
        goal, stage, artifact = CLASS_MAP[cls]
    else:
        goal = d.get("goal", "?")
        stage, artifact = "edit", "(unmapped class -- add a meta/attribution-table.md row)"
    if d.get("goal"):
        goal = d["goal"]
    rnd = d.get("round", "").strip()
    finding = "post-accept revision%s: %r -> %r. %s" % (
        (" (" + rnd + ")") if rnd else "",
        d.get("before", "").strip(),
        d.get("after", "").strip(),
        d.get("rationale", "").strip(),
    )
    return {
        "essay_id": essay_id,
        "iter": None,
        "run_timestamp": ts,
        "source": "human-revision",
        "origin": "human-post-accept",
        "pass": None,
        "check_id": None,
        "severity": "warn",
        "goal": goal,
        "root_cause_stage": stage,
        "root_cause_artifact": artifact,
        "pattern_tag": cls,
        "finding": finding,
        "recommendation": "captured via the revision-delta channel; owner artifact + lever per attribution-table.",
        "status": "watch",
    }


def normalize(text, essay_id, ts):
    return [to_record(d, essay_id, ts) for d in parse_notes(text)]


_SELFTEST_NOTES = """# Revision notes — test
## delta
class: meta-reader-instruction
round: v2.2
before: Read it the way an examiner would.
after: removed
rationale: stage direction, not insight.

## delta
class: brand-new-unmapped-class
before: x
after: y
rationale: z

# Sources
- not a delta
"""


def _selftest():
    recs = normalize(_SELFTEST_NOTES, "test-essay", "2026-01-01T00:00:00Z")
    assert len(recs) == 2, "expected 2 deltas, got %d" % len(recs)
    a = recs[0]
    assert a["pattern_tag"] == "meta-reader-instruction"
    assert a["origin"] == "human-post-accept" and a["source"] == "human-revision"
    assert a["goal"] == "4b" and a["root_cause_stage"] == "canon"
    assert "Read it the way an examiner would" in a["finding"]
    b = recs[1]
    assert "unmapped" in b["root_cause_artifact"], "unknown class must flag for a new row"
    # every record must be valid JSON round-trip
    for r in recs:
        json.loads(json.dumps(r))
    print("selftest OK: %d records, schema + class-map + unknown-flag verified" % len(recs))
    return 0


def main(argv=None):
    p = argparse.ArgumentParser(description="Normalize revision-notes.md -> ledger records.")
    p.add_argument("--notes", help="path to revision-notes.md")
    p.add_argument("--essay-id", default="unknown-essay")
    p.add_argument("--timestamp", help="ISO-8601; default = now (UTC)")
    p.add_argument("--append", help="ledger path to append JSONL records to")
    p.add_argument("--selftest", action="store_true")
    args = p.parse_args(argv)

    if args.selftest:
        return _selftest()
    if not args.notes:
        p.error("--notes is required (or use --selftest)")

    ts = args.timestamp or datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    with open(args.notes, "r", encoding="utf-8") as fh:
        recs = normalize(fh.read(), args.essay_id, ts)

    lines = [json.dumps(r, ensure_ascii=False) for r in recs]
    if args.append:
        with open(args.append, "a", encoding="utf-8") as fh:
            for line in lines:
                fh.write(line + "\n")
        print("appended %d human-post-accept records to %s" % (len(lines), args.append))
    else:
        for line in lines:
            print(line)
    return 0


if __name__ == "__main__":
    sys.exit(main())
