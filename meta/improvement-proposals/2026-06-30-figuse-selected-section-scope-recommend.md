---
proposal_id: 2026-06-30-figuse-selected-section-scope-recommend
created: 2026-06-30T00:00:00Z
status: recommended-apply
lever: gate-promotion
goal: "2"
root_cause_stage: gate
root_cause_artifact: _shared/scripts/gate_figure_use.py (FIG_RE / _figure_numbers scans the ENTIRE figure-selection.md to build the "selected" set, not just the "## Selected figures" section)
recurrence_count: 2
confidence: high
supersedes: 2026-06-24-figuse-selection-scope
triggering_findings:
  - essay_id: 045-agility-638-last-mile-moat, iter: 0, pattern_tag: figuse-selection-scope-overread
  - essay_id: 046-stm-cliff-bridge-from-seeing-to-doing, iter: 0, pattern_tag: figuse-selection-scope-overread
---

## Problem

`gate_figure_use` (north-star goal 2) builds its **selected** set by regex-scanning the
*entire* text of `figure-selection.md` with `FIG_RE`. But the Phase-1 figure-selection format
carries more than the selected list:

- `## Selected figures` — the figures actually chosen,
- `## Reviewed but NOT selected (with reason)` — figures deliberately **dropped**,
- `## Paired-figure relationships (acknowledged)` / `## Figure relationships` — pair/sequence
  notes that **name the dropped (or all) figures again** for documentation,
- explanatory prose.

Because `_figure_numbers(selection_text)` reads all of it, every figure mentioned *anywhere* in
the file — including explicitly-dropped or merely-discussed figures — is treated as "selected,"
and any such figure absent from the draft becomes a spurious `FIGUSE-001` orphan **hard FAIL**
on goal 2.

This is now a **confirmed, recurring** gate bug across two runs:

- **Run 045** (`045-agility-638-last-mile-moat`): the file selects FIG. 1/4/5 but the whole-file
  parse yields `selected = {1,2,3,4,5}` because FIG. 2/3 sit in the "Reviewed but NOT selected"
  table. It did **not** fail only because the draft happened to reference FIG. 2/3 in prose.

- **Run 046** (`046-stm-cliff-bridge-from-seeing-to-doing`, this run): a **text-only** essay —
  `input/figures/` is empty, the `## Selected figures` table is `(none)`, **zero figures
  selected**. Yet `figure-selection.md` documents the patent's drawings in a
  `## Paired-figure relationships (acknowledged)` table and surrounding prose. The gate passed
  **only because the Phase-1 author defensively wrote every figure reference in WORDS** ("the
  robot/architecture group", "four-panel approach sequence") instead of literal `FIG. N` tokens,
  and added an explicit warning note in the file itself:

  > `gate_figure_use` parses every `FIG. N`/`Figure N` token in this document as a *selected*
  > figure, so the reference-only rows below describe the patent drawings in words to avoid a
  > spurious orphan FAIL. ... (Flagged for the meta-loop: the gate should parse only the
  > "Selected figures" table.)

  That author-side workaround **is** the recurring per-run mitigation cost this proposal retires.
  A Phase-1 author should be free to write a relationships table naturally ("FIG. 4A–4D
  progressive sequence") on a text-only essay without tripping a goal-2 hard FAIL on figures that
  were never selected.

Mechanically verified against the current `gate_figure_use.py` (2026-06-30) on the run-046 live
file and a realistic natural-token variant of it:

```
run-046 live file (defensive wording)   whole-file -> []   section-scoped -> []      (both pass)
run-046 with natural "FIG. 1" / "FIG. 4A-4D"
  in the relationships table             whole-file -> {1}  (SPURIOUS orphan FAIL)
                                         section-scoped -> [] (correct: zero selected)
handoff-template/01-design/figure-selection.md
                                         whole-file -> {1,2}  section-scoped -> {1,2}  (unchanged)
test_gates.py SELECTION constant (no heading)
                                         whole-file == section-scoped (fallback, unchanged)
```

This is a **distinct mechanism** from `figure-token-regex-blindspot`
(`2026-06-11-figure-token-panel-suffix.md`, lettered-panel tokens like "FIG. 4B"). This one is a
**selected-set scope over-read** of the selection *file*.

This proposal **supersedes** `2026-06-24-figuse-selection-scope.md` (filed `watch`, count 1).
The second confirmed occurrence (run 046) reaches the second-occurrence promotion bar and
upgrades the on-file `watch` proposal to **`recommended-apply`**: the failure is mechanically
verified, mechanically safe, has now appeared in two consecutive runs, and on each run sits one
natural figure token away from a spurious goal-2 hard FAIL.

## Proposed change (exact diff)

**File 1: `.claude/skills/_shared/scripts/gate_figure_use.py`**

Add a section-scoping helper and use it for the **selected** set only. The `used` set still scans
the whole draft (unchanged). When the `## Selected figures` heading is absent (legacy / bare-list
inputs — the fixtures and the `test_gates.py` `SELECTION` constant), it falls back to whole-text
parsing, so the change is a **strict refinement** with full backward compatibility.

```diff
 GATE_ID = "figure_use"
 # Matches "fig-07", "FIG. 7", "Figure 7", "Fig 7".
 FIG_RE = re.compile(r"\bfig(?:ure|\.|-)?\s*0*(\d+)\b", re.IGNORECASE)
+# The selected set must come ONLY from the "## Selected figures" section, not from
+# the "## Reviewed but NOT selected" / "## (Paired-)figure relationships" sections
+# that also name the dropped (or merely-discussed) figures (ledger:
+# figuse-selection-scope-overread, runs 045 + 046).
+_SEL_HEADING_RE = re.compile(r"^##\s+Selected figures\s*$", re.IGNORECASE | re.MULTILINE)
+_NEXT_H2_RE = re.compile(r"^##\s+", re.MULTILINE)
+
+
+def _selected_region(text):
+    """Return the substring holding the selected-figure rows: from the
+    '## Selected figures' heading up to the next '## ' heading. If that heading
+    is absent (legacy / bare-list selection text), return the whole text so the
+    behavior is unchanged for inputs that have no sectioning."""
+    if not text:
+        return text or ""
+    m = _SEL_HEADING_RE.search(text)
+    if not m:
+        return text
+    start = m.end()
+    nxt = _NEXT_H2_RE.search(text, start)
+    return text[start:nxt.start()] if nxt else text[start:]
 
 
 def _figure_numbers(text):
     """Return the set of figure numbers mentioned in text."""
     return {int(m.group(1)) for m in FIG_RE.finditer(text or "")}
```

```diff
-    selected = _figure_numbers(selection_text)
+    # Only the "## Selected figures" section defines the selected set; the
+    # "Reviewed but NOT selected" / "(Paired-)figure relationships" sections name
+    # dropped or merely-discussed figures and must not be counted as selected
+    # (else they false-orphan -- ledger figuse-selection-scope-overread, runs 045+046).
+    selected = _figure_numbers(_selected_region(selection_text))
     used = _figure_numbers(draft_text)
```

**File 2: `.claude/skills/_shared/scripts/test_gates.py`** — add to `TestFigureUse`:

```diff
     def test_no_selection_skips(self):
         r = gate_figure_use.check("Figure 1.\n", {})
         self.assertTrue(r["passed"])
         self.assertTrue(_has(r, "FIGUSE-000"))
+
+    def test_dropped_figures_in_reviewed_section_not_orphaned(self):
+        # Figures named only in "Reviewed but NOT selected" / "Figure relationships"
+        # are NOT selected and must not false-orphan when absent from the draft.
+        selection = (
+            "# Figure Selection\n\n"
+            "## Selected figures\n"
+            "| FIG. 1 | fig-01.png | header |\n"
+            "| FIG. 4 | fig-04.png | body |\n"
+            "| FIG. 5 | fig-05.png | body |\n\n"
+            "## Reviewed but NOT selected (with reason)\n"
+            "| FIG. 2 | fig-02.png | redundant with FIG. 1 |\n"
+            "| FIG. 3 | fig-03.png | covered by FIG. 5 + prose |\n"
+        )
+        draft = "FIG. 1 anchors it. FIG. 4 shows the legs. FIG. 5 the deployment.\n"
+        r = gate_figure_use.check(draft, {"figure_selection_text": selection})
+        self.assertTrue(r["passed"], r["findings"])
+        self.assertFalse(_has(r, "FIGUSE-001"))
+
+    def test_text_only_relationships_section_not_orphaned(self):
+        # Text-only essay (zero selected): figures named in a "## Paired-figure
+        # relationships" section must NOT false-count as selected (run 046).
+        selection = (
+            "# Figure Selection\n\n"
+            "## Selected figures\n"
+            "| (none) | (none) | text-only essay |\n\n"
+            "## Paired-figure relationships (acknowledged)\n"
+            "| FIG. 1 robot group | same-set | NOT selected |\n"
+            "| FIG. 4 approach sequence | progressive | NOT selected |\n"
+        )
+        draft = "The essay is text-only and references no figures.\n"
+        r = gate_figure_use.check(draft, {"figure_selection_text": selection})
+        self.assertTrue(r["passed"], r["findings"])
+        self.assertFalse(_has(r, "FIGUSE-001"))
+
+    def test_orphan_still_fails_within_selected_section(self):
+        # A genuine orphan inside "## Selected figures" must still FAIL.
+        selection = (
+            "## Selected figures\n"
+            "| FIG. 1 | header |\n| FIG. 4 | body |\n| FIG. 5 | body |\n\n"
+            "## Reviewed but NOT selected\n| FIG. 2 | dropped |\n"
+        )
+        draft = "Only FIG. 1 and FIG. 4 appear.\n"   # FIG. 5 is a true orphan
+        r = gate_figure_use.check(draft, {"figure_selection_text": selection})
+        self.assertFalse(r["passed"])
+        self.assertTrue(_has(r, "FIGUSE-001"))
```

## Why this lever

- The defect lives in the gate script's parse scope (`root_cause_stage: gate`); no reference
  edit changes how the script reads the file. Section-scoping is the minimal mechanical fix.
- **Mechanically safe / strict refinement.** Verified 2026-06-30:
  - run-046 live file: `[]` → `[]` (still passes; the defensive wording is now unnecessary);
  - run-046 with natural figure tokens in its relationships table: `{1}` spurious FAIL → `[]`
    correct (**the bug, fixed**);
  - run-045 live file: `{1,2,3,4,5}` → `{1,4,5}` (the bug, fixed);
  - handoff template: `{1,2}` → `{1,2}` (unchanged);
  - the `test_gates.py` `SELECTION` constant and `meta/fixtures/` selections have **no**
    `## Selected figures` heading → whole-text fallback → identical behavior, so `figure-orphan`
    still emits `FIGUSE-001` and all 60 existing gate tests stay green.
- Not a reference-edit: the "describe dropped/discussed figures in words, or echo them in prose"
  workaround is exactly the per-run mitigation cost this should retire. A figure the design
  **dropped** (or a text-only essay with **zero** figures) should be allowed to omit figure
  references without a spurious goal-2 hard FAIL.

## Regression expectation

Run `python meta/regression.py` before applying. Expected after applying:

- `python .claude/skills/_shared/scripts/test_gates.py`: all 60 existing cases pass unchanged
  (whole-text fallback preserves the no-heading inputs) + the 3 new `TestFigureUse` cases pass.
- `python meta/regression.py`:
  - `figure-orphan` fixture still emits `FIGUSE-001` (its bare-list selection has no
    `## Selected figures` heading → whole-text fallback → selected set as today;
    `must_contain_check_ids` intact);
  - `clean-baseline` still passes with no FIGUSE/FIGREF findings.
- Observable success criterion next run: a `figure-selection.md` that drops a figure (or selects
  none, text-only) can name those figures naturally in a `## Reviewed but NOT selected` /
  `## Paired-figure relationships` section without a spurious `FIGUSE-001`; a genuine orphan
  inside `## Selected figures` still fails.

On apply, flip the run-045 + run-046 `figuse-selection-scope-overread` ledger records to
`resolved` (append a new record referencing this proposal id) and update the recurrence summary
in `meta/attribution-table.md` (`figuse-selection-scope-overread`: proposed → resolved, patches
applied +1).
