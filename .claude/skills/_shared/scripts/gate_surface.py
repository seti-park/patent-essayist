#!/usr/bin/env python3
"""Surface / feed-context gate for the patent-essay pipeline.

The 2026-07-04 reader-first overhaul (docs/architecture/reader-first-overhaul.md,
row T9) added an energy contract that binds the SURFACE of the essay -- the
title, the cover caption, and the lead's opening sentences -- the part a reader
sees in a feed or card before ever opening the piece. These are the mechanical
half of that contract. They never touch body accuracy, and (like
gate_structure.py) every check here is WARN severity by design: a title that
reads well in isolation can still sit on a bad essay, and vice versa, so this
is a nudge, not a blocker.

DRAFT FORMAT ASSUMPTIONS (see gate_emdash.py for the full shared list): the
draft is Markdown, with an optional leading YAML frontmatter block delimited by
`---` lines; the title is the first `#` (H1) line; a cover image is a
`![alt](src)` line; a cover caption is a standalone italic `*...*` line. "Body"
begins after that structural matter (frontmatter, title, cover image, cover
caption) and after any `##` section header.

Checks (all warn):
  SURF-001: the H1 title exceeds TITLE_MAX_CHARS (markdown '#' and a trailing
            period stripped before counting) -- a feed card truncates a long
            title, so the whole hook must fit inside the limit.
  SURF-002: the first body sentence is qualifier-led (reuses gate_hedge's
            qualifier-led-verdict lexicon/detector). The lead's job is the
            hook, not a pre-hedged verdict; the call belongs at the END of the
            lead, per the hook-first lead directive (T5), not its first word.
  SURF-003: the cover caption carries more than SURF003_MAX_NUMERALS distinct
            reference-numeral tokens -- a caption dense with part numbers reads
            as a parts diagram, not an invitation, in a feed preview.
  SURF-004: a defensive-open lexicon hit (status / lien / rejection language)
            lands in the first two body sentences -- discovery must come
            before insurance; stacking disclaimers ahead of the hook is the
            report-genre failure (verdict-insurance-first) this overhaul
            targets.
"""

import argparse
import os
import re
import sys

# Allow running both as a script and as a module (mirrors run_gates.py).
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import gate_hedge  # reuse its qualifier-led-verdict lexicon for SURF-002

# ---------------------------------------------------------------------------
# Tunable constants
# ---------------------------------------------------------------------------
GATE_ID = "surface"

TITLE_MAX_CHARS = 70        # SURF-001
SURF003_MAX_NUMERALS = 6    # SURF-003

HEADING_RE = re.compile(r"^#{1,6}\s+")
H1_RE = re.compile(r"^#\s+(.*)$")
SECTION_H2_RE = re.compile(r"^##\s+\S")
IMAGE_RE = re.compile(r"^!\[")
# A standalone italic line: single leading '*' (not '**bold**'), closing '*'.
CAPTION_RE = re.compile(r"^\*(?!\*).*\*\s*$")
BLOCKQUOTE_RE = re.compile(r"^>")
SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+")
NUMERAL_TOKEN_RE = re.compile(r"\b\d{3,4}[A-Za-z]?\b")

# SURF-002: identical detector gate_hedge uses for a qualifier-led verdict
# ("a qualified yes", "the cautious no", ...), applied here to the lead's
# first sentence instead of the verdict section.
QUALIFIER_LED_RE = gate_hedge.QUALIFIER_LED_RE

# SURF-004: status / insurance lexicon. Case-insensitive substring match.
DEFENSIVE_OPEN_TERMS = [
    "pending application",
    "not an asset",
    "final rejection",
    "loan collateral",
    "security interest",
    "no claim has been",
    "not a patent",
    "abandoned",
]


def _mask_quoted_spans(text):
    """Blank out double-quoted span contents (keep the quote chars).

    Same approach as the other gates (gate_emdash.py, gate_hedge.py): text
    inside "..." is verbatim source and exempt from these checks.
    """
    out, in_q = [], False
    for ch in text:
        if ch == '"':
            out.append(ch)
            in_q = not in_q
        elif in_q:
            out.append(" ")
        else:
            out.append(ch)
    return "".join(out)


def _strip_frontmatter(draft_text):
    """Return the draft's lines with a leading YAML frontmatter block removed."""
    lines = draft_text.splitlines()
    if lines and lines[0].strip() == "---":
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                return lines[i + 1:]
    return lines


def _title_line(draft_text):
    """Return the H1 title's text (markdown '#' stripped), or None."""
    for raw in _strip_frontmatter(draft_text):
        line = raw.strip()
        if not line:
            continue
        m = H1_RE.match(line)
        return m.group(1).strip() if m else None
    return None


def _cover_caption(draft_text):
    """First standalone italic caption line that appears before the first ## section."""
    lines = _strip_frontmatter(draft_text)
    limit = len(lines)
    for i, raw in enumerate(lines):
        if SECTION_H2_RE.match(raw.strip()):
            limit = i
            break
    for raw in lines[:limit]:
        line = raw.strip()
        if CAPTION_RE.match(line):
            return line
    return None


def _body_paragraphs(draft_text):
    """Body prose paragraphs: headers, images, captions, blockquotes excluded."""
    paragraphs = []
    buf = []
    for raw in _strip_frontmatter(draft_text):
        line = raw.strip()
        structural = (not line or HEADING_RE.match(line) or IMAGE_RE.match(line)
                      or CAPTION_RE.match(line) or BLOCKQUOTE_RE.match(line))
        if structural:
            if buf:
                paragraphs.append(" ".join(buf))
                buf = []
            continue
        buf.append(line)
    if buf:
        paragraphs.append(" ".join(buf))
    return paragraphs


def _first_body_sentences(draft_text, n):
    """First n sentences of body prose, in document order across paragraphs."""
    sentences = []
    for para in _body_paragraphs(draft_text):
        for s in SENTENCE_SPLIT_RE.split(para):
            if s.strip():
                sentences.append(s.strip())
            if len(sentences) >= n:
                return sentences
    return sentences


def check(draft_text: str, context: dict) -> dict:
    findings = []

    # SURF-001: H1 title length.
    title = _title_line(draft_text)
    if title:
        stripped = title.rstrip()
        if stripped.endswith("."):
            stripped = stripped[:-1]
        n = len(stripped)
        if n > TITLE_MAX_CHARS:
            findings.append({
                "check_id": "SURF-001",
                "severity": "warn",
                "message": "H1 title is %d characters (max %d); a feed card truncates it"
                           % (n, TITLE_MAX_CHARS),
                "location": "title line",
            })

    # SURF-002: qualifier-led first body sentence.
    first = _first_body_sentences(draft_text, 1)
    if first:
        scan = _mask_quoted_spans(first[0])
        m = QUALIFIER_LED_RE.search(scan)
        if m:
            findings.append({
                "check_id": "SURF-002",
                "severity": "warn",
                "message": "first body sentence is qualifier-led (\"%s\"); the hook "
                           "comes first, the call lands at the end of the lead"
                           % m.group(0),
                "location": "first body sentence",
            })

    # SURF-003: cover-caption reference-numeral density.
    caption = _cover_caption(draft_text)
    if caption:
        tokens = set(NUMERAL_TOKEN_RE.findall(caption))
        if len(tokens) > SURF003_MAX_NUMERALS:
            findings.append({
                "check_id": "SURF-003",
                "severity": "warn",
                "message": "cover caption carries %d distinct reference-numeral tokens "
                           "(max %d): %s" % (len(tokens), SURF003_MAX_NUMERALS,
                                             ", ".join(sorted(tokens))),
                "location": "cover caption",
            })

    # SURF-004: defensive-open lexicon in the first two body sentences.
    first_two = _first_body_sentences(draft_text, 2)
    if first_two:
        scan = _mask_quoted_spans(" ".join(first_two)).lower()
        hits = [term for term in DEFENSIVE_OPEN_TERMS if term in scan]
        if hits:
            findings.append({
                "check_id": "SURF-004",
                "severity": "warn",
                "message": "defensive-open lexicon in the first two body sentences: %s"
                           % ", ".join(hits),
                "location": "first two body sentences",
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
    p = argparse.ArgumentParser(description="Surface gate (%s)" % GATE_ID)
    p.add_argument("draft", help="path to the draft Markdown file")
    args = p.parse_args(argv)
    with open(args.draft, "r", encoding="utf-8") as fh:
        text = fh.read()
    result = check(text, {})
    _report(result)
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
