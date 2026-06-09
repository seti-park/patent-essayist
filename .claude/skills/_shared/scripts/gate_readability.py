#!/usr/bin/env python3
"""Readability / accessible-altitude gate for the patent-essay pipeline.

This gate enforces the ACCESSIBLE-FORMAT CONTRACT of the `investor` audience
altitude (north-star goal 3 — easy for the reader). It is audience-aware and
does nothing for the default `deep` audience, so it is harmless to register
unconditionally in run_gates.py.

Audience contract (investor):
  - the body (everything before the `# Sources` block) must stay under a word
    ceiling, so the piece is finishable;
  - the body must carry NO inline patent anchors (`[dddd]`) or patent-ese — the
    grounding traceability lives in handoff/02-compose/thesis-trace.md and the
    `# Sources` block, not on the reader-facing surface.

Context keys consumed:
  - audience (str): "deep" (default) or "investor". Only "investor" activates
    the hard checks.

Checks:
  READAB-000 (warn): audience is not "investor" -- gate skipped (pass).
  READAB-001 (fail, investor): body word count exceeds MAX_BODY_WORDS.
  READAB-002 (fail, investor): an inline `[dddd]` patent anchor appears in the
                               body (accessible contract forbids surface anchors).
  READAB-003 (warn, investor): readability heuristics -- long mean sentence
                               length, or a very long sentence, or high
                               undefined-acronym density.
"""

import argparse
import re
import sys

# ---------------------------------------------------------------------------
# Tunable constants
# ---------------------------------------------------------------------------
GATE_ID = "readability"
MAX_BODY_WORDS = 1100            # READAB-001 ceiling (investor)
MEAN_SENTENCE_WORDS_WARN = 30    # READAB-003 mean sentence length
LONG_SENTENCE_WORDS = 50         # READAB-003 single long sentence
ACRONYM_PER_100_WORDS_WARN = 4   # READAB-003 acronym density

SOURCES_HEADER_RE = re.compile(r"^#\s+Sources\s*$")
HTML_COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)
FENCE_RE = re.compile(r"^\s*(```|~~~)")
ANCHOR_RE = re.compile(r"\[\d{4}\]")
IMAGE_RE = re.compile(r"!\[[^\]]*\]\([^)]*\)")
# All-caps acronym of 2+ letters (UT, POP, LEO, SAT), not at sentence start only.
ACRONYM_RE = re.compile(r"\b[A-Z]{2,}\b")
SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+")


def _body_text(draft_text):
    """Return the reader-facing body: everything before the `# Sources` h1,
    with HTML comments and fenced code blocks removed."""
    lines = draft_text.splitlines()
    end = len(lines)
    for i, line in enumerate(lines):
        if SOURCES_HEADER_RE.match(line):
            end = i
            break
    body = "\n".join(lines[:end])
    body = HTML_COMMENT_RE.sub("", body)
    # drop fenced code blocks
    out, in_fence = [], False
    for raw in body.splitlines():
        if FENCE_RE.match(raw):
            in_fence = not in_fence
            continue
        if not in_fence:
            out.append(raw)
    return "\n".join(out)


def _word_count(text):
    # Drop image markdown (the alt text / path are not "reading" words).
    text = IMAGE_RE.sub("", text)
    return len(re.findall(r"\S+", text))


def check(draft_text: str, context: dict) -> dict:
    context = context or {}
    audience = context.get("audience", "deep")
    findings = []

    if audience != "investor":
        findings.append({
            "check_id": "READAB-000",
            "severity": "warn",
            "message": "audience is %r, readability gate skipped" % audience,
            "location": "(global)",
        })
        return {"gate": GATE_ID, "passed": True, "findings": findings}

    body = _body_text(draft_text)

    # READAB-001: body word ceiling
    n_words = _word_count(body)
    if n_words > MAX_BODY_WORDS:
        findings.append({
            "check_id": "READAB-001",
            "severity": "fail",
            "message": "body is %d words, over the investor ceiling of %d"
                       % (n_words, MAX_BODY_WORDS),
            "location": "(body)",
        })

    # READAB-002: inline patent anchors in the reader-facing body
    for lineno, raw in enumerate(body.splitlines(), start=1):
        for m in ANCHOR_RE.finditer(raw):
            findings.append({
                "check_id": "READAB-002",
                "severity": "fail",
                "message": "inline patent anchor %s in body (investor surface "
                           "must carry no [dddd] anchors)" % m.group(0),
                "location": "body line %d" % lineno,
            })

    # READAB-003: readability heuristics (warn)
    plain = IMAGE_RE.sub("", body)
    sentences = [s for s in SENTENCE_SPLIT_RE.split(plain) if s.strip()]
    if sentences:
        lengths = [len(re.findall(r"\S+", s)) for s in sentences]
        mean_len = sum(lengths) / float(len(lengths))
        if mean_len > MEAN_SENTENCE_WORDS_WARN:
            findings.append({
                "check_id": "READAB-003",
                "severity": "warn",
                "message": "mean sentence length %.1f words (>%d): consider shorter sentences"
                           % (mean_len, MEAN_SENTENCE_WORDS_WARN),
                "location": "(body)",
            })
        longest = max(lengths)
        if longest > LONG_SENTENCE_WORDS:
            findings.append({
                "check_id": "READAB-003",
                "severity": "warn",
                "message": "a sentence runs %d words (>%d)" % (longest, LONG_SENTENCE_WORDS),
                "location": "(body)",
            })
    if n_words >= 100:
        n_acro = len(ACRONYM_RE.findall(plain))
        per_100 = n_acro * 100.0 / n_words
        if per_100 > ACRONYM_PER_100_WORDS_WARN:
            findings.append({
                "check_id": "READAB-003",
                "severity": "warn",
                "message": "acronym density %.1f per 100 words (>%d): spell out for a lay reader"
                           % (per_100, ACRONYM_PER_100_WORDS_WARN),
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
    p = argparse.ArgumentParser(description="Readability gate (%s)" % GATE_ID)
    p.add_argument("draft", help="path to the draft Markdown file")
    p.add_argument("--audience", choices=["deep", "investor"], default="investor",
                   help="audience altitude (default: investor for standalone use)")
    args = p.parse_args(argv)
    with open(args.draft, "r", encoding="utf-8") as fh:
        text = fh.read()
    result = check(text, {"audience": args.audience})
    _report(result)
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
