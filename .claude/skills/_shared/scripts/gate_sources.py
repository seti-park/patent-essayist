#!/usr/bin/env python3
"""Sources-block gate for the patent-essay pipeline.

DRAFT FORMAT ASSUMPTIONS (see gate_emdash.py for the full shared list):
  - A "Sources block" is a Markdown section whose header matches
    ^#{1,6}\\s+Sources\\s*$ near the end of the document. The block runs from
    that header to the next same-or-higher-level header or end of document.

IMPORTANT: this Sources-entry format is provisional; real upstream formats are
TBD. The parser below is deliberately tolerant and heavily commented so it can
be retargeted once the upstream canon lands.

Entry / category parsing (tolerant):
  An "entry" is a top-level list item line (starting with '-', '*' or '1.').
  An entry's category is taken from, in order of preference:
    1. a bold lead-in  "**Category:**"  -> category = text before the colon
    2. a leading       "- Category — ..."  (en/em dash or hyphen as separator)
  The extracted category string is matched case-insensitively against
  ALLOWED_CATEGORIES.

Sub-group headings: a Markdown header *inside* the Sources block (deeper than
the Sources header) is treated as a sub-group heading.

Checks:
  SOURCES-001 (fail): no Sources block found.
  SOURCES-002 (fail): an entry's category is not in ALLOWED_CATEGORIES.
  SOURCES-003 (fail): a "Patent" entry lacks PATENT_CITATION_FIELDS
                      comma/pipe-separated citation fields.
  SOURCES-004 (warn): mixed subgrouping — some entries under a sub-group
                      heading and some not (all-or-nothing expected).
"""

import argparse
import re
import sys

# ---------------------------------------------------------------------------
# Tunable constants
# ---------------------------------------------------------------------------
GATE_ID = "sources"
ALLOWED_CATEGORIES = ["Patent", "Academic", "News/Media", "Official/Standards", "Other"]
# Expected number of comma/pipe-separated citation fields in a Patent entry,
# e.g. "US1234567B2 | Assignee | Title | Filed 2019 | Granted 2021 | [0042]".
PATENT_CITATION_FIELDS = 6

SOURCES_HEADER_RE = re.compile(r"^(#{1,6})\s+Sources\s*$")
ANY_HEADER_RE = re.compile(r"^(#{1,6})\s+(.*\S)\s*$")
LIST_ITEM_RE = re.compile(r"^\s*(?:[-*]|\d+\.)\s+(.*)$")
BOLD_LEADIN_RE = re.compile(r"^\*\*([^*]+?):\*\*")               # **Category:** ...
DASH_LEADIN_RE = re.compile(r"^([^—–-]+?)\s*[—–-]\s+")            # Category — ...

# Lowercased lookup so matching is case-insensitive but messages keep canon.
_ALLOWED_LOWER = {c.lower(): c for c in ALLOWED_CATEGORIES}


def _find_sources_block(lines):
    """Return (header_level, start_idx, end_idx) for the Sources block.

    start_idx/end_idx are line indices bounding the entries (header excluded).
    Returns None if no Sources header found. If several, the last one wins
    (Sources blocks live "near the end of the doc").
    """
    found = None
    for i, line in enumerate(lines):
        m = SOURCES_HEADER_RE.match(line)
        if m:
            found = (len(m.group(1)), i)
    if not found:
        return None
    level, start = found
    end = len(lines)
    for j in range(start + 1, len(lines)):
        hm = ANY_HEADER_RE.match(lines[j])
        if hm and len(hm.group(1)) <= level:
            end = j
            break
    return (level, start + 1, end)


def _extract_category(entry_text):
    """Return (category_or_None, raw_token) from a list-item body."""
    bm = BOLD_LEADIN_RE.match(entry_text)
    if bm:
        return bm.group(1).strip(), bm.group(0)
    dm = DASH_LEADIN_RE.match(entry_text)
    if dm:
        return dm.group(1).strip(), dm.group(0)
    return None, ""


def _count_citation_fields(entry_text):
    """Count comma/pipe-separated fields in the entry body (after lead-in)."""
    # Strip a bold or dash lead-in if present, count the remainder's fields.
    body = entry_text
    bm = BOLD_LEADIN_RE.match(body)
    if bm:
        body = body[bm.end():]
    else:
        dm = DASH_LEADIN_RE.match(body)
        if dm:
            body = body[dm.end():]
    body = body.strip()
    if not body:
        return 0
    parts = [p for p in re.split(r"[|,]", body) if p.strip()]
    return len(parts)


def check(draft_text: str, context: dict) -> dict:
    findings = []
    lines = draft_text.splitlines()

    block = _find_sources_block(lines)
    if block is None:
        findings.append({
            "check_id": "SOURCES-001",
            "severity": "fail",
            "message": "no Sources block found",
            "location": "(global)",
        })
        return {"gate": GATE_ID, "passed": False, "findings": findings}

    level, start, end = block

    # Walk the block: track sub-group headings and entries, noting for each
    # entry whether it falls under a sub-group heading.
    current_subgroup = None
    entries = []  # list of (lineno, body, under_subgroup_bool)
    for idx in range(start, end):
        raw = lines[idx]
        hm = ANY_HEADER_RE.match(raw)
        if hm and len(hm.group(1)) > level:
            current_subgroup = hm.group(2)
            continue
        lm = LIST_ITEM_RE.match(raw)
        if lm:
            entries.append((idx + 1, lm.group(1).strip(), current_subgroup is not None))

    # SOURCES-002 / SOURCES-003
    for lineno, body, _under in entries:
        category, _tok = _extract_category(body)
        if category is None or category.lower() not in _ALLOWED_LOWER:
            shown = category if category else "(none)"
            findings.append({
                "check_id": "SOURCES-002",
                "severity": "fail",
                "message": "source category %r not in allowed set %s" % (shown, ALLOWED_CATEGORIES),
                "location": "line %d" % lineno,
            })
            continue  # category unknown -> skip patent-field check for this entry
        canon = _ALLOWED_LOWER[category.lower()]
        if canon == "Patent":
            n = _count_citation_fields(body)
            if n != PATENT_CITATION_FIELDS:
                findings.append({
                    "check_id": "SOURCES-003",
                    "severity": "fail",
                    "message": "Patent entry has %d citation fields, expected %d" % (n, PATENT_CITATION_FIELDS),
                    "location": "line %d" % lineno,
                })

    # SOURCES-004: all-or-nothing subgrouping
    if entries:
        under = sum(1 for _l, _b, u in entries if u)
        if 0 < under < len(entries):
            findings.append({
                "check_id": "SOURCES-004",
                "severity": "warn",
                "message": "mixed subgrouping: %d of %d entries under sub-group headings (expected all or none)" % (under, len(entries)),
                "location": "Sources block (line %d-%d)" % (start, end),
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
    p = argparse.ArgumentParser(description="Sources gate (%s)" % GATE_ID)
    p.add_argument("draft", help="path to the draft Markdown file")
    args = p.parse_args(argv)
    with open(args.draft, "r", encoding="utf-8") as fh:
        text = fh.read()
    result = check(text, {})
    _report(result)
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
