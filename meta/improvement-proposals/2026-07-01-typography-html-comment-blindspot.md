---
proposal_id: 2026-07-01-typography-html-comment-blindspot
created: 2026-07-01T00:00:00Z
status: watch
lever: gate-promotion
goal: "4b"
root_cause_stage: gate
root_cause_artifact: _shared/scripts/gate_typography.py (EXCLAIM_RE = re.compile(r"!(?!\[)") exempts markdown image syntax "![" but not HTML comments "<!--")
recurrence_count: 1
confidence: high
triggering_findings:
  - essay_id: 001-st-histogram-mechanism, iter: 1, pattern_tag: typography-html-comment-blindspot
---

## Problem

`gate_typography.py`'s `EXCLAIM-001` check (a **hard-fail**) scans every line of the draft for
a bare `!` not immediately followed by `[` (the one exemption already carved out, for Markdown
image syntax `![alt](src)`). It has no equivalent exemption for HTML comments (`<!-- ... -->`),
which the pipeline uses routinely as internal process annotations — e.g. this run's own
`handoff/01-design/figure-selection.md` closes with:

```
<!-- No revision note: figure selection matched the spine's pre-planned 2-problem /
     3-core-claim / 4-analogy sections without requiring a spine update (Step 9 confirmed
     rather than revised Step 8's plan). -->
```

Any HTML comment opens with `<!--` — a literal `!` immediately followed by `-`, not `[`. Round
1 of essay `001-st-histogram-mechanism`'s draft carried an internal `<!-- ... -->` annotation
(the composer's own revision-tracking convention, structurally identical to the one shown
above), and `EXCLAIM_RE` fired `EXCLAIM-001` on the comment's opening `!` — a false hard-fail
on content that is not body prose at all, mirroring exactly how `![` is already recognized as
"not really an exclamation mark." This blocked round 1's typography gate until the stray
comment was deleted (a content-layer workaround the essay's own `score-history.md` logs as a
gate-script bug, not a genuine defect fix — see its "Gate-script findings for pipeline-retro"
section, item 2).

This is a **distinct mechanism** from the two related-but-different classes already on file:

- `figuse-selection-scope-overread` (`2026-06-24-figuse-selection-scope.md`) — a *selected-set*
  parsing bug in `gate_figure_use.py`, unrelated file, unrelated check.
- `figure-token-regex-blindspot` (`2026-06-11-figure-token-panel-suffix.md`) — a figure-number
  regex missing lettered-panel suffixes like "FIG. 4B", also in `gate_figure_use.py`.

This one is a **non-prose-construct exemption gap** in `gate_typography.py`'s `EXCLAIM_RE`
specifically. Confirmed no existing attribution-table row or proposal file covers it
(`typography-html-comment-blindspot` does not appear anywhere in `meta/attribution-table.md` or
`meta/improvement-proposals/` prior to this filing).

Mechanically verified against the current `gate_typography.py` (2026-07-01):

```python
>>> EXCLAIM_RE = re.compile(r"!(?!\[)")
>>> EXCLAIM_RE.findall("<!-- No revision note: ... -->")
['!']          # false fire — the comment is not prose
>>> EXCLAIM_RE.findall("![figure one](fig-01.png)")
[]             # correctly exempt already
```

Single occurrence so far (`recurrence_count: 1`), filed at `watch` per the promotion rules —
but the mechanism is mechanically safe, fully verified, ships with a regression test, and the
pipeline's own handoff templates and design-phase artifacts use HTML comments as a matter of
routine convention (see `figure-selection.md`'s own trailing comment above, and
`handoff-template/03-edit/revision-notes.md`'s `## delta` convention notes), so this will keep
recurring on any future draft that legitimately carries an internal HTML-comment annotation —
the exact diff + test are included for early human application (same posture as the sibling
`figuse-selection-scope-overread` proposal when it was first filed at `watch`).

## Proposed change (exact diff)

**File 1: `.claude/skills/_shared/scripts/gate_typography.py`**

Strip HTML comments from the draft text once, before the existing per-line scan begins — the
same "this construct is not prose, don't scan it" treatment the gate already gives fenced code
blocks (`FENCE_RE` / `in_fence` state) and blockquote lines (`raw.lstrip().startswith(">")`).
This is more robust than extending `EXCLAIM_RE` with a `(?!--)` lookahead: a lookahead only
protects the exact `!--` two-character sequence and would still leave a *coincidental* `!`
immediately followed by `--` elsewhere in real prose (e.g. "Wait--no!--this changes
everything") mis-exempted, and it does nothing for other checks that should also ignore
comment content (LATIN-001, EMOJI-001, CAPS-001, LONGSENT-001 could all false-fire on a
sufficiently detailed internal comment). Stripping the comment text outright — before any
check runs, not just `EXCLAIM-001` — closes the whole class at once and handles multi-line
`<!-- ... -->` blocks correctly (`re.DOTALL`).

```diff
 GATE_ID = "typography"
 LONG_SENTENCE_WORDS = 35          # warn threshold; editorial target is ~15-25
 ALLOWED_EMOJI = {"\U0001F914"}    # 🤔 — sanctioned at a closing-open-question
 
 FENCE_RE = re.compile(r"^\s*(```|~~~)")
+# HTML comments (<!-- ... -->) are process annotations, not prose — same treatment as
+# fenced code blocks and blockquotes. Strip them before any check runs so EXCLAIM-001
+# (and every other check here) never scans a comment's contents.
+# (ledger: typography-html-comment-blindspot, run 001-st-histogram-mechanism)
+HTML_COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)
 
 LATIN_PATTERNS = [
```

```diff
 def check(draft_text: str, context: dict) -> dict:
     findings = []
     in_fence = False
     prose_lines = []
 
+    # Strip HTML comments globally first (they can span multiple lines) so no check
+    # below ever scans a comment's contents as if it were body prose.
+    draft_text = HTML_COMMENT_RE.sub("", draft_text or "")
+
     for lineno, raw in enumerate(draft_text.splitlines(), start=1):
         if FENCE_RE.match(raw):
             in_fence = not in_fence
             continue
```

**File 2: `.claude/skills/_shared/scripts/test_gates.py`** — add to `TestTypography`, placed
after `test_code_fence_exempt` (the class's existing "exempt this construct" test), mirroring
its style:

```diff
     def test_code_fence_exempt(self):
         r = gate_typography.check("```\nx = 1  # e.g. this!\n```\n", {})
         self.assertTrue(r["passed"], r["findings"])
+
+    def test_html_comment_exclaim_exempt(self):
+        # An HTML comment's opening "<!--" is not a body-prose exclamation mark.
+        draft = (
+            "Some prose here that is fine.\n\n"
+            "<!-- internal note: revision applied, see round 1! -->\n\n"
+            "More prose after the comment.\n"
+        )
+        r = gate_typography.check(draft, {})
+        self.assertTrue(r["passed"], r["findings"])
+        self.assertFalse(_has(r, "EXCLAIM-001"))
+
+    def test_html_comment_does_not_mask_real_exclamation(self):
+        # A genuine exclamation mark in body prose must still fail, even when an
+        # HTML comment appears elsewhere in the same draft.
+        draft = "This is amazing!\n<!-- a harmless internal note -->\n"
+        r = gate_typography.check(draft, {})
+        self.assertFalse(r["passed"])
+        self.assertTrue(_has(r, "EXCLAIM-001"))
+
+    def test_multiline_html_comment_stripped(self):
+        # HTML comments spanning multiple lines must be fully removed, not just the
+        # opening line.
+        draft = (
+            "Prose before.\n"
+            "<!-- a multi-line\n"
+            "     comment block\n"
+            "     with an ! inside -->\n"
+            "Prose after.\n"
+        )
+        r = gate_typography.check(draft, {})
+        self.assertTrue(r["passed"], r["findings"])
+        self.assertFalse(_has(r, "EXCLAIM-001"))
```

## Why this lever

- The defect lives in the gate script's text-scanning scope (`root_cause_stage: gate`); no
  reference edit changes how `EXCLAIM_RE` reads the draft. Stripping non-prose constructs
  before scanning is the same category of fix `_mask_quoted_spans` and the fence/blockquote
  handling already use elsewhere in this exact file — a strict extension of an established
  pattern, not a new mechanism.
- **Mechanically safe.** Verified 2026-07-01 against the live gate: the fix eliminates the
  false `EXCLAIM-001` on HTML-comment content, still correctly fails on a genuine exclamation
  mark in body prose even when a comment is present elsewhere in the same draft, and correctly
  handles multi-line comment blocks (`re.DOTALL`).
- Not a reference-edit: "delete the stray comment" is exactly the per-draft mitigation cost
  this should retire — an internal process annotation (a convention the pipeline's own
  templates use, e.g. `figure-selection.md`'s trailing `<!-- No revision note: ... -->`) should
  not have to be scrubbed from a draft just to clear a hygiene gate that was never meant to
  read it as prose.
- `watch`, not `recommended-apply`: first occurrence (`recurrence_count: 1` <
  `RECUR_THRESHOLD` 3). The fix, diff, and tests are filed now (rather than waiting) because
  the failure mode is mechanically proven, the fix is a strict, low-risk refinement (comments
  are never prose; nothing that currently passes can start failing), and the underlying
  convention — internal HTML-comment annotations in handoff artifacts — is routine enough in
  this pipeline that a second occurrence is likely before three are needed to force the
  question.

## Regression expectation

Run `python meta/regression.py` before applying. Expected after applying:

- `python .claude/skills/_shared/scripts/test_gates.py`: all existing `TestTypography` cases
  pass unchanged (no HTML comments in their fixtures, so stripping is a no-op for them) + 3 new
  cases pass (`test_html_comment_exclaim_exempt`,
  `test_html_comment_does_not_mask_real_exclamation`, `test_multiline_html_comment_stripped`).
- `python meta/regression.py`: `clean-baseline` and `figure-orphan` fixtures unaffected (neither
  contains an HTML comment; behavior identical before/after).
- Observable success criterion next run: a draft carrying a legitimate internal
  `<!-- ... -->` annotation clears `EXCLAIM-001` (and every other typography check) without
  requiring the comment to be deleted first; a real exclamation mark in body prose still
  hard-fails regardless of whether a comment appears elsewhere in the draft.
