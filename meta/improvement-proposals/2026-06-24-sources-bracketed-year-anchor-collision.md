---
proposal_id: 2026-06-24-sources-bracketed-year-anchor-collision
created: 2026-06-24T00:00:00Z
status: watch
lever: reference-edit
goal: "1"
root_cause_stage: compose
root_cause_artifact: essay-en-composer/references/x-articles-format-en.md (no policy: render years/dates in # Sources as "(YYYY)", never "[YYYY]") — with a gate-side hardening option in _shared/scripts/gate_anchors.py
recurrence_count: 1
confidence: high
triggering_findings:
  - essay_id: 029-agility-torso-protrusion, iter: 1, pattern_tag: sources-bracketed-year-anchor-collision
---

## Problem

A literal bracketed 4-digit year (or any bracketed digit-run) inside a `# Sources` entry title
**collides with the `[dddd]` citation-anchor format** that `gate_anchors.py` scans across the
*whole* draft, including the Sources block.

- This run (`029-agility-torso-protrusion`, Compose-time near-miss): a Sources entry title
  carried "[2026]" (the Robozaps title). `[2026]` is a well-formed 4-digit token, so it is read
  as a citation anchor; it is not in the invention-summary anchor set, so it would trip
  **`ANCHOR-001`** (chain, hard fail). A non-4-digit bracketed stamp — e.g. an arXiv-style year
  "[26308]" or a short "[26]" — would instead trip **`ANCHOR-002`** (format, hard fail). The
  composer self-corrected to "(2026)" before the gate ran, so the failure never materialized.

Verified mechanically against the current gate (2026-06-24): `gate_anchors.py` matches
`ANCHOR_ANY_DIGITS_RE = re.compile(r"\[(\d+)\]")` and `ANCHOR_RE = re.compile(r"\[(\d{4})\]")`
over every line of the draft with **no `# Sources` block exclusion** — so any bracketed digit
token anywhere below `# Sources` is treated as a citation anchor.

The `# Sources` block is the one region of the draft where bracketed digit tokens are
legitimately *not* anchors (they are years, volumes, arXiv stamps inside human-readable
titles). The collision is mechanically decidable and novel.

**Not a duplicate.** Distinct from the three relevant existing classes:
- `figure-token-regex-blindspot` / proposal `2026-06-11-figure-token-panel-suffix` — that is
  `FIG_RE`/`FIGREF_RE` and *figure* tokens ("FIG. 4B"); different regex, different token class.
- `sources-entry-template-drift` / run-2 F12 — author/title *bibliographic* form; no gate.
- `quoted-title-emdash-policy-gap` — em-dashes in quoted titles vs `gate_emdash`; different
  gate, different character.

Single occurrence (a self-corrected near-miss), so below RECUR_THRESHOLD(3) → files at
`watch`, with the full diff ready, exactly as `2026-06-11-figure-token-panel-suffix` did for a
latent mechanical gate blindspot. A second bracketed-token-in-Sources patent (or one actual
spurious `ANCHOR-001`/`ANCHOR-002` fail) promotes this.

## Proposed change (exact diff)

Two cheap, mechanically-safe options. **Option A (compose-side, primary) is sufficient on its
own**; Option B (gate-side) is a defense-in-depth backstop and is the part that ships with a
test. Apply A, or A+B; B alone would let a bracketed token survive into the published title.

### Option A — `reference-edit` (compose-side; primary)

**File: `.claude/skills/essay-en-composer/references/x-articles-format-en.md`** — add to the
inline-quote / Sources conventions a years-and-dates rule. Insert after the attribution-form
line (the "em-dash 회피" convention, around the `### Inline quote conventions` block):

```diff
 Attribution form — em-dash 회피. Patent paragraph attribution 은 paragraph anchor `[xxxx]`
 form 사용. Multi-source attribution 은 separate line 의 comma-separated metadata.
+
+Years and dates in `# Sources` entries (and any source title) render as `(YYYY)`, never
+bracketed `[YYYY]`. A bracketed 4-digit token is the citation-anchor format and is scanned
+across the whole draft including the Sources block, so a title like "Robozaps [2026]" is read
+as a (chain-invalid) anchor `[2026]` and hard-fails `gate_anchors` (`ANCHOR-001`; a non-4-digit
+stamp such as an arXiv "[26308]" fails `ANCHOR-002`). Use parentheses for any year, volume, or
+arXiv year-stamp that would otherwise sit in brackets.
```

### Option B — gate-side hardening (defense-in-depth; ships with the test)

**File: `.claude/skills/_shared/scripts/gate_anchors.py`** — exclude the `# Sources` block from
anchor scanning, reusing the block-boundary logic already present in `gate_sources.py` (h1
`# Sources` to next h1/EOF). Add the boundary helper and apply it in the two anchor scans:

```diff
 GATE_ID = "anchors"
 ANCHOR_RE = re.compile(r"\[(\d{4})\]")                 # [0123]
 ANCHOR_ANY_DIGITS_RE = re.compile(r"\[(\d+)\]")
 FIGREF_RE = re.compile(r"\bfig(?:ure|\.)?\s*(\d+)\b", re.IGNORECASE)  # Figure 3 / Fig. 3 / Fig 3
+SOURCES_HEADER_RE = re.compile(r"^#\s+Sources\s*$")    # h1 "# Sources" (mirrors gate_sources)
+H1_RE = re.compile(r"^#\s+\S")
+
+
+def _sources_line_span(lines):
+    """1-based [start, end) line span of the `# Sources` block, or None.
+    Bracketed digit tokens inside source titles (years, volumes, arXiv stamps)
+    are NOT citation anchors; the block is excluded from anchor scanning."""
+    start = None
+    for i, line in enumerate(lines):
+        if SOURCES_HEADER_RE.match(line):
+            start = i + 1            # block body begins after the header line
+            break
+    if start is None:
+        return None
+    end = len(lines)
+    for j in range(start, len(lines)):
+        if H1_RE.match(lines[j]):
+            end = j
+            break
+    return (start + 1, end + 1)      # 1-based, end exclusive
```

Apply it in the `ANCHOR-002` format scan and the `_find_anchors` chain scan so lines inside the
Sources span are skipped:

```diff
 def check(draft_text: str, context: dict) -> dict:
     findings = []
     context = context or {}
+    lines = draft_text.splitlines()
+    src_span = _sources_line_span(lines)            # exclude # Sources block from anchor scans

     # --- ANCHOR format (4-digit zero-padded) ---------------------------------
     for lineno, raw in enumerate(draft_text.splitlines(), start=1):
+        if src_span and src_span[0] <= lineno < src_span[1]:
+            continue
         for m in ANCHOR_ANY_DIGITS_RE.finditer(raw):
```

```diff
 def _find_anchors(text):
     """Return an ordered list of (anchor_token, lineno) for each [dddd] hit."""
     hits = []
+    lines = (text or "").splitlines()
+    src_span = _sources_line_span(lines)
     for lineno, raw in enumerate((text or "").splitlines(), start=1):
+        if src_span and src_span[0] <= lineno < src_span[1]:
+            continue
         for m in ANCHOR_RE.finditer(raw):
             hits.append((m.group(1), lineno))
     return hits
```

**File: `.claude/skills/_shared/scripts/test_gates.py`** — add to `TestAnchors`:

```diff
     def test_figref_in_index_passes(self):
         draft = "Fig. 2 and Figure 3 are referenced.\n"
         ctx = {"invention_summary_text": "", "figures_index": [1, 2, 3]}
         r = gate_anchors.check(draft, ctx)
         self.assertTrue(r["passed"], r["findings"])
+
+    def test_bracketed_year_in_sources_not_an_anchor(self):
+        # A bracketed year inside a # Sources title must NOT be read as a citation
+        # anchor (neither ANCHOR-001 chain nor ANCHOR-002 format).
+        draft = (
+            'Body cites [0042].\n\n'
+            '# Sources\n'
+            '## News & media\n'
+            '- Robozaps [2026]. "Apptronik update". URL\n'
+            '- arXiv stamp [26308] in a paper title.\n'
+        )
+        ctx = {"invention_summary_text": "anchor [0042] here", "figures_index": [1]}
+        r = gate_anchors.check(draft, ctx)
+        self.assertTrue(r["passed"], r["findings"])
+        self.assertFalse(_has(r, "ANCHOR-001"))
+        self.assertFalse(_has(r, "ANCHOR-002"))
+
+    def test_bracketed_anchor_in_body_still_checked(self):
+        # The exclusion is scoped to the Sources block; body anchors still gated.
+        draft = 'Body cites [2026].\n\n# Sources\n- An entry.\n'
+        ctx = {"invention_summary_text": "only [0042]", "figures_index": [1]}
+        r = gate_anchors.check(draft, ctx)
+        self.assertFalse(r["passed"])
+        self.assertTrue(_has(r, "ANCHOR-001"))
```

Accepted limit (verified): the exclusion is scoped strictly to the `# Sources` h1 block; body
anchors and figure refs are unchanged. The change is a strict *narrowing* of where anchors are
scanned — it can only remove false fails inside Sources, never add a match elsewhere; re-running
over both fixtures and the archived `runs/*/essay-final.md` yields identical body-anchor sets
(their Sources blocks contain no bracketed digit tokens, so nothing changes).

## Why this lever

- **Option A is the cheapest durable fix at the root**: the defect is a compose-stage rendering
  choice (bracketing a year), and `x-articles-format-en.md` is where Sources formatting is
  specified. Stating "(YYYY) never [YYYY]" prevents the token from ever entering the Sources
  block, which also keeps the *published* title clean — a gate-only fix would silence the gate
  but leave "[2026]" in the reader-facing title.
- **Option B is gate-side and decidable** (the Sources block is mechanically locatable; the
  boundary logic is already proven in `gate_sources.py`), so it is a safe defense-in-depth
  backstop and the natural place to add the regression test. It is filed alongside A rather than
  instead of it.
- **Not rubric/voice:** purely a goal-1 accuracy/mechanics surface; no voice fence implicated
  (no `voice-profile`/canon exposure).
- `watch`, not `recommended-apply`: a single self-corrected near-miss is below the bar; the diff
  is ready so a human can apply early, or wait for a second bracketed-token-in-Sources patent.

## Regression expectation

- Option A alone: documentation-only. `python .claude/skills/_shared/scripts/test_gates.py` and
  `python meta/regression.py` unchanged green (no script/fixture touched).
- Option B (if applied): `python .claude/skills/_shared/scripts/test_gates.py` — all existing
  cases pass unchanged (the exclusion only narrows Sources-block scanning) + the 2 new cases
  pass. `python meta/regression.py` — `clean-baseline` still `gate_pass: true` with no
  ANCHOR-001/002; `figure-orphan` still fails on `FIGUSE-001` only. (Both fixtures' Sources
  blocks, if any, contain no bracketed digit tokens, so verdicts are identical.)
