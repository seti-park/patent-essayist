#!/usr/bin/env python3
"""Shared helpers for the patent-essay gate scripts.

Kept deliberately tiny: each gate stays runnable standalone (same-directory
import, stdlib only). Only logic that must not drift between gates lives here:
quote masking (gate_emdash and gate_banned must agree on what "quoted" means)
and the figures-file parser (run_gates and gate_anchors must agree on format).
"""

import re


class QuoteMasker:
    """Mask the contents of double-quoted spans, keeping the quote chars.

    Quoted text is exempt from the em-dash and banned-terms gates (verbatim
    source quotes). Straight quotes (") toggle the state; typographic quotes
    open (U+201C) / close (U+201D) it explicitly. The state carries across
    lines so a quote that wraps a line boundary stays masked; callers must
    call reset() at paragraph boundaries (blank lines, fences, blockquotes)
    so an unbalanced quote can never mask more than one paragraph.
    """

    def __init__(self):
        self.in_quote = False

    def reset(self):
        self.in_quote = False

    def mask(self, line):
        out = []
        for ch in line:
            if ch == '"':
                out.append(ch)
                self.in_quote = not self.in_quote
            elif ch == "“":  # opening typographic quote
                out.append(ch)
                self.in_quote = True
            elif ch == "”":  # closing typographic quote
                out.append(ch)
                self.in_quote = False
            elif self.in_quote:
                out.append(" ")
            else:
                out.append(ch)
        return "".join(out)


def parse_figures_file(path):
    """Parse a figures file: integers, one per line or comma/space separated.

    Raises ValueError naming the file, line and offending token instead of
    surfacing a bare int() traceback: the file is written fresh by the
    orchestrator each run, so format drift must produce an actionable message.
    """
    nums = []
    with open(path, "r", encoding="utf-8") as fh:
        for lineno, raw in enumerate(fh, start=1):
            for tok in re.split(r"[,\s]+", raw.strip()):
                if not tok:
                    continue
                try:
                    nums.append(int(tok))
                except ValueError:
                    raise ValueError(
                        "figures file %s line %d: %r is not an integer "
                        "(expected one figure number per line, e.g. '3')"
                        % (path, lineno, tok))
    return nums
