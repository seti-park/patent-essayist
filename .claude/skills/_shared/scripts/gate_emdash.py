#!/usr/bin/env python3
"""Em-dash / en-dash gate for the patent-essay pipeline.

DRAFT FORMAT ASSUMPTIONS (shared across all gates; documented here in full):
  - The draft is Markdown text.
  - "Quoted text" means anything inside double quotes (straight "..." or
    typographic “...”) OR a Markdown blockquote line starting with ">".
    A quoted span may wrap a line boundary within a paragraph (the masking
    state resets at blank lines / fences / blockquotes, so an unbalanced
    quote can never hide more than one paragraph). Em-dashes inside quoted
    text are ALLOWED (they are verbatim source quotes); em-dashes anywhere
    else are violations.
  - Citation anchors are inline tokens matching \\[(\\d{4})\\], e.g. [0123].
  - Figure refs are "Figure N" / "Fig. N" / "Fig N" (case-insensitive), N an int.
  - A "Sources block" is a Markdown section whose header matches
    ^#{1,6}\\s+Sources\\s*$ near the end of the document.

IMPORTANT: the real handoff data formats come from an upstream system and are
still TBD. These scripts use the documented, pragmatic formats above and are
written to be easily retargeted (constants up top, tolerant parsers).

This gate:
  EMDASH-001 (fail): any em-dash U+2014 outside quoted text and outside fenced
                     code blocks.
  EMDASH-002 (warn): an en-dash U+2013 used as a sentence connector (i.e. with
                     surrounding whitespace, like " – ").
"""

import argparse
import re
import sys

import gate_common

# ---------------------------------------------------------------------------
# Tunable constants
# ---------------------------------------------------------------------------
GATE_ID = "emdash"
EM_DASH = "—"          # — true em-dash
EN_DASH = "–"          # – en-dash
FENCE_RE = re.compile(r"^\s*(```|~~~)")          # fenced code block delimiter
# En-dash "used as connector" = whitespace on at least one side (warn only).
EN_DASH_CONNECTOR_RE = re.compile(r"(?:\s–)|(?:–\s)")


def check(draft_text: str, context: dict) -> dict:
    findings = []
    in_fence = False
    # Quote masking is shared with gate_banned (gate_common.QuoteMasker) so the
    # two gates can never disagree on what counts as quoted text. State carries
    # across lines within a paragraph; reset at blank lines/fences/blockquotes.
    masker = gate_common.QuoteMasker()

    for lineno, raw in enumerate(draft_text.splitlines(), start=1):
        if FENCE_RE.match(raw):
            in_fence = not in_fence
            masker.reset()
            continue
        if in_fence:
            continue
        if not raw.strip():
            masker.reset()
            continue
        # Blockquote lines are entirely quoted text -> em-dashes allowed.
        if raw.lstrip().startswith(">"):
            masker.reset()
            continue

        scan = masker.mask(raw)

        # EMDASH-001: em-dash outside quotes/code.
        for m in re.finditer(re.escape(EM_DASH), scan):
            col = m.start() + 1
            findings.append({
                "check_id": "EMDASH-001",
                "severity": "fail",
                "message": "em-dash (U+2014) used outside quoted text",
                "location": "line %d, col %d" % (lineno, col),
            })

        # EMDASH-002: en-dash as a sentence connector (warn).
        for m in EN_DASH_CONNECTOR_RE.finditer(scan):
            col = m.start() + 1
            findings.append({
                "check_id": "EMDASH-002",
                "severity": "warn",
                "message": "en-dash (U+2013) used as a sentence connector",
                "location": "line %d, col %d" % (lineno, col),
            })

    passed = not any(f["severity"] == "fail" for f in findings)
    return {"gate": GATE_ID, "passed": passed, "findings": findings}


def _report(result: dict) -> None:
    status = "PASS" if result["passed"] else "FAIL"
    print("[%s] gate=%s" % (status, result["gate"]))
    for f in result["findings"]:
        print("  %-5s %-12s %s  (%s)" % (
            f["severity"].upper(), f["check_id"], f["message"], f["location"]))
    if not result["findings"]:
        print("  (no findings)")


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="Em-dash gate (%s)" % GATE_ID)
    p.add_argument("draft", help="path to the draft Markdown file")
    args = p.parse_args(argv)
    with open(args.draft, "r", encoding="utf-8") as fh:
        text = fh.read()
    result = check(text, {})
    _report(result)
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
