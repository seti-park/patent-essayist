---
proposal_id: 2026-06-20-figure-selection-parse-scope
created: 2026-06-20T17:40:00Z
status: recommended-apply
lever: gate-promotion
goal: "2"
root_cause_stage: gate
root_cause_artifact: _shared/scripts/gate_figure_use.py (selected-set parse scope)
recurrence_count: 3
confidence: high
triggering_findings:
  - essay_id: 2026-06-10-us12636684b1-deleted-dome, iter: 0, pattern_tag: figure-token-regex-blindspot
  - essay_id: 2026-06-11-us20260158546a1-both-and-steel, iter: 0, pattern_tag: figure-token-regex-blindspot
  - essay_id: 2026-06-20-hbf-nand-hbm-lane, iter: 0, pattern_tag: figure-selection-parse-scope
related_proposal: 2026-06-11-figure-token-panel-suffix
---

## Problem

`gate_figure_use.check()` builds the *selected* figure set by running `_figure_numbers()`
over the **entire** text of `handoff/01-design/figure-selection.md`:

```python
selected = _figure_numbers(selection_text)   # whole file
```

But the Phase-1 `figure-selection.md` template (`handoff-template/01-design/figure-selection.md`)
deliberately enumerates **rejected** figures *inside the same file* — a
`## Paired-figure relationships (acknowledged)` table plus HTML comments that name the dropped
figures so Phase 2 does not reopen the decision. Every `FIG. N` token in those rejected rows is
swept into `selected`, so a figure the design explicitly **dropped** is then required to appear
in the draft and falsely orphans (`FIGUSE-001`, a goal-2 hard fail) when it correctly does not.

**This run (`2026-06-20-hbf-nand-hbm-lane`) is the first time the class produced an actual
OVERALL gate FAIL** (the prior two runs were latent token-shape costs). The genuine selected
set was `{1, 5, 8, 10}`, referenced exactly by the draft; the file's `## Paired-figure
relationships` block listed FIG. 2 / 3 / 4 / 6 / 7 / 9 as NOT selected. Reproduced mechanically
against the run's selection file (2026-06-20):

```
CURRENT gate (whole-file parse): selected = {1,2,3,4,5,6,7,8,9,10}
  -> FIGUSE-001 false orphans = [2, 3, 4, 6, 7, 9]   (OVERALL gate FAIL)
FIXED gate  (## Selected figures section only): selected = {1, 5, 8, 10}
  -> FIGUSE-001 orphans = []                          (correct — matches the draft)
```

The orchestrator had to **normalize the input by hand before the loop could be trusted**
(relocate the rejected-figure rationale into `figure-rationale.md`, which no gate consumes, and
strip the selection file down to selected numbers) — selection decision unchanged, gates then
green. That hand-normalization is exactly the kind of per-run tax a deterministic gate is
supposed to remove.

### Relationship to `2026-06-11-figure-token-panel-suffix` (do not duplicate)

Same owner script (`gate_figure_use.py`), same goal (2), same broad class (the figure-selection
gate input-contract), but a **different mechanism**, and they **interact** — so this is a
tightly-scoped complement, not a re-file:

| | `figure-token-panel-suffix` (on file, `watch`) | this proposal (`figure-selection-parse-scope`) |
|---|---|---|
| Defect | lettered token `FIG. 4B` is **invisible** to `FIG_RE` (lost `\b`) | **all** tokens in the *rejected* region are **visible** and miscounted as selected |
| Direction | false **negative** (figure 4 silently orphaned / off-index) | false **positive** (rejected figures demanded → spurious orphan + OVERALL FAIL) |
| Fired in a run? | no — latent, avoided by the `FIG. N (panel X)` convention (2/2 runs) | **yes — OVERALL gate FAIL this run** |

**Interaction (important for apply order):** the panel-suffix proposal widens `FIG_RE` to match
`FIG. 4B`. On the template as written, the rejected figures happen to be lettered (`FIG. 4B`,
`FIG. 7A/7B/7C`), so today's narrow regex *accidentally* hides some of them from the selected
set. Applying the regex widening **without** this scope fix would make the parse-scope defect
**worse** — newly-matched rejected lettered figures would also leak into `selected`. The two
should land together, scope-fix first.

Recurrence: the figure-selection gate input-contract class now appears in **3 of 3 recorded
runs** (run-1 latent, run-2 latent, this run an actual FAIL). `recurrence_count = 3 =
RECUR_THRESHOLD`, and unlike the panel-suffix variant the failure has now actually fired →
`recommended-apply`.

## Proposed change (exact diff)

**File 1: `.claude/skills/_shared/scripts/gate_figure_use.py`**

Add a scoped extractor for the selected set, and have `check()` use it. The selected set is read
only from the `## Selected figures` section (up to the next `##` header or EOF); if that header
is absent the function falls back to the whole text, preserving every current caller and the
`figure-orphan` fixture (which has no section headers).

```diff
 GATE_ID = "figure_use"
 # Matches "fig-07", "FIG. 7", "Figure 7", "Fig 7".
 FIG_RE = re.compile(r"\bfig(?:ure|\.|-)?\s*0*(\d+)\b", re.IGNORECASE)
+# The "## Selected figures" section of figure-selection.md, up to the next "##"
+# header or end of file. The Phase-1 template also enumerates REJECTED figures
+# lower in the same file (a "## Paired-figure relationships" table + comments);
+# those tokens must NOT be read as selected (ledger: figure-selection-parse-scope,
+# 2026-06-20 OVERALL FAIL). Absent the header, fall back to the whole text.
+SELECTED_SECTION_RE = re.compile(
+    r"(?ims)^[ \t]*##[ \t]+selected\s+figures[ \t]*$(.*?)(?=^[ \t]*##[ \t]|\Z)"
+)
+
+
+def _selected_section(text):
+    """Return only the '## Selected figures' section, or the whole text if absent."""
+    m = SELECTED_SECTION_RE.search(text or "")
+    return m.group(1) if m else (text or "")


 def _figure_numbers(text):
     """Return the set of figure numbers mentioned in text."""
     return {int(m.group(1)) for m in FIG_RE.finditer(text or "")}
```

```diff
-    selected = _figure_numbers(selection_text)
+    # Only the "## Selected figures" section names the selected set; rejected figures
+    # enumerated elsewhere in the file must not be swept in (figure-selection-parse-scope).
+    selected = _figure_numbers(_selected_section(selection_text))
     used = _figure_numbers(draft_text)
```

Also update the module docstring's "Context keys consumed" note:

```diff
 Context keys consumed:
   - figure_selection_text (str, optional): text of figure-selection.md. The
-    figure numbers found here form the "selected" set.
+    figure numbers found in its "## Selected figures" section form the "selected"
+    set (the file may also enumerate REJECTED figures lower down — those are
+    ignored; absent the header, the whole text is used as a fallback).
```

**File 2: `.claude/skills/_shared/scripts/test_gates.py`** — add to `TestFigureUse`:

```diff
     def test_no_selection_skips(self):
         r = gate_figure_use.check("Figure 1.\n", {})
         self.assertTrue(r["passed"])
         self.assertTrue(_has(r, "FIGUSE-000"))
+
+    def test_rejected_figures_section_not_counted_as_selected(self):
+        # Only "## Selected figures" names the selected set; a "## Paired-figure
+        # relationships" block listing rejected figures must not orphan them.
+        selection = (
+            "# Figure Selection\n\n"
+            "## Selected figures\n"
+            "| FIG. 1 | header |\n| FIG. 5 | body |\n\n"
+            "## Paired-figure relationships (acknowledged)\n"
+            "| FIG. 2 / FIG. 3 | NOT selected |\n| FIG. 4 | NOT selected |\n"
+        )
+        draft = "Figure 1 and Fig. 5 are discussed.\n"  # only the selected set
+        r = gate_figure_use.check(draft, {"figure_selection_text": selection})
+        self.assertTrue(r["passed"], r["findings"])
+        self.assertFalse(_has(r, "FIGUSE-001"))
+
+    def test_selection_without_header_falls_back_to_whole_text(self):
+        # Headerless selection (e.g. the figure-orphan fixture form) is unchanged.
+        selection = "fig-01 lead. FIG. 2 mechanism. Figure 3 closes.\n"
+        draft = "Figure 1 and Fig. 2 are discussed.\n"  # 3 selected but unused
+        r = gate_figure_use.check(draft, {"figure_selection_text": selection})
+        self.assertFalse(r["passed"])
+        self.assertTrue(_has(r, "FIGUSE-001"))
```

**File 3: new regression fixture `meta/fixtures/figure-selection-rejected-block/`** — locks the
exact run-2026-06-20 shape so the defect cannot silently return.

`meta/fixtures/figure-selection-rejected-block/expect.json`:

```json
{ "gate_pass": true, "must_not_contain_check_ids": ["FIGUSE-001"] }
```

`meta/fixtures/figure-selection-rejected-block/figure-selection.md`:

```markdown
# Figure Selection

## Selected figures
| Figure | File | Thesis point | caption_role |
|---|---|---|---|
| FIG. 1 | fig-01.png | architecture | header_composite |
| FIG. 5 | fig-05.png | bandwidth recipe | body_figure_carries_unique_info |
| FIG. 8 | fig-08.png | voltage scheme | body_figure_carries_unique_info |
| FIG. 10 | fig-10.png | package assembly | body_figure_carries_unique_info |

## Paired-figure relationships (acknowledged)
| Figure(s) | Relationship | Treatment in selection |
|---|---|---|
| FIG. 2 / FIG. 3 | architecture detail pair | NOT selected (prose covers fully) |
| FIG. 4 | block-erase detail | NOT selected |
| FIG. 6 | latency sub-figure | NOT selected |
| FIG. 7 | voltage-table variant | NOT selected |
| FIG. 9 | redundancy diagram | NOT selected |
```

`meta/fixtures/figure-selection-rejected-block/draft.md` (references only the selected set,
plus a minimal well-formed Sources block so unrelated gates stay green):

```markdown
# How Cheap, Slow NAND Reaches HBM's Lane

The architecture is in Figure 1. The bandwidth recipe is in FIG. 5. The voltage
scheme is in FIG. 8, and the package assembly to 1.1 TB/s is in FIG. 10. See [0005]
for the problem framing.

# Sources
- US2025/0259685A1, SanDisk Technologies LLC, High Bandwidth Nonvolatile Memory Devices, published 2025-08-14
```

(Include `figures-index.txt` with `1 5 8 10` if the harness also exercises `gate_anchors`
FIGREF on this fixture; optional, since the proposal targets `figure_use`.)

## Why this lever

- The defect is in the gate **script itself** (`root_cause_stage: gate`) — a parse-scope bug, not
  a procedure gap — so no reference edit reaches it. It is mechanically safe: the change only
  *narrows* what is read, and is a strict no-op whenever the `## Selected figures` header is
  absent (verified: the `figure-orphan` fixture is headerless and keeps emitting `FIGUSE-001`).
- It removes a real per-run hand-normalization tax and closes a path to a **spurious OVERALL
  FAIL**, which is the worst failure mode for a deterministic gate (it falsely blocks a clean
  draft). The fix keeps the template's deliberate "record the rejected figures in-file" design
  (good for Phase-2 traceability) compatible with the gate.
- A cheaper `reference-edit` (e.g. "tell Phase 1 to never name rejected figures in
  `figure-selection.md`") was considered and rejected: it fights the template's own design,
  depends on author discipline every run (the same fragility the panel-suffix convention already
  shows), and does nothing for the lettered-token interaction. Fixing the parser is the durable
  level.
- One lever per proposal: the `FIG_RE` panel-letter widening stays in its own file
  (`2026-06-11-figure-token-panel-suffix`); this proposal's interaction note records that the
  scope fix should land first / together so the widening cannot leak rejected lettered figures.

## Regression expectation

- `python .claude/skills/_shared/scripts/test_gates.py`: all existing `TestFigureUse` cases pass
  unchanged (the `SELECTION` constant is headerless → fallback path, identical behavior) + the 2
  new cases pass.
- `python meta/regression.py`:
  - `figure-orphan` fixture (headerless): still `gate_pass: false`, still emits `FIGUSE-001`
    (fallback path unchanged).
  - `clean-baseline` fixture: unchanged (no figure-selection context).
  - new `figure-selection-rejected-block` fixture: `gate_pass: true`, **no** `FIGUSE-001`
    (this is the previously-recurring defect, now proven absent).
- Success criterion for the next run with an in-file rejected-figure block: `gate_figure_use`
  passes on first run with **no hand-normalization** of `figure-selection.md`.
