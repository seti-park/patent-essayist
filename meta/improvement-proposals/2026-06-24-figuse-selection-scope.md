---
proposal_id: 2026-06-24-figuse-selection-scope
created: 2026-06-24T00:00:00Z
updated: 2026-07-01T00:00:00Z
status: recommended-apply
lever: gate-promotion
goal: "2"
root_cause_stage: gate
root_cause_artifact: _shared/scripts/gate_figure_use.py (_figure_numbers reads the entire figure-selection.md, not just the selected-figure section)
recurrence_count: 2
confidence: high
triggering_findings:
  - essay_id: 045-agility-638-last-mile-moat, iter: 0, pattern_tag: figuse-selection-scope-overread
  - essay_id: 001-st-histogram-mechanism, iter: 1, pattern_tag: figuse-selection-scope-overread
  - essay_id: 001-st-histogram-mechanism, iter: 2, pattern_tag: figuse-selection-scope-overread
  - essay_id: 001-st-histogram-mechanism, iter: 3, pattern_tag: figuse-selection-scope-overread
---

## Problem

`gate_figure_use` builds its **selected** set by regex-scanning the *entire* text of
`figure-selection.md`. But the Phase-1 figure-selection format (see
`handoff/01-design/figure-selection.md` and the `figure-orphan`-free handoff template) carries
three sections:

- `## Selected figures` — the figures actually chosen,
- `## Reviewed but NOT selected (with reason)` — figures deliberately **dropped**,
- `## Figure relationships (acknowledged)` — pair/sequence notes that **name the dropped
  figures again**.

Because `_figure_numbers(selection_text)` reads all of it, every figure mentioned *anywhere* in
the file — including the explicitly-dropped ones — is treated as "selected." For run 045 this
makes `selected = {1, 2, 3, 4, 5}` when only **FIG. 1 / 4 / 5** are selected (FIG. 2 and FIG. 3
are in the "Reviewed but NOT selected" table). The dropped figures then become `FIGUSE-001`
**orphans** unless the prose mentions them anyway.

This run did **not** fail only by luck: the draft happens to reference FIG. 2 and FIG. 3 in
prose (thesis-trace coverage note), so `used` covered them. A clean drop of the dropped figures
from prose — the legitimate authoring intent for a figure the design chose **not** to use —
would have spuriously **hard-FAILED goal 2** on figures 2 and 3.

Mechanically verified against the current `gate_figure_use.py` (2026-06-24):

```
whole-file parse  -> selected = {1, 2, 3, 4, 5}   (current, buggy)
section-scoped     -> selected = {1, 4, 5}          (correct)
```

This is a **distinct mechanism** from the existing `figure-token-regex-blindspot` class
(`2026-06-11-figure-token-panel-suffix.md`), which is about lettered-panel tokens like
"FIG. 4B". This one is a **selected-set scope over-read** of the selection *file*.

## Update 2026-07-01 — second occurrence, promoted to `recommended-apply`

Run `001-st-histogram-mechanism` (US 2026/0140238 A1) is exactly the second occurrence this
proposal's original text predicted: "A second selection file with a 'Reviewed but NOT
selected' section whose dropped figures are not echoed in prose... promotes this to
`recommended-apply`." Its `handoff/01-design/figure-selection.md` carries a `## Selected
figures` table (FIG. 1, FIG. 2 only) followed by a `## Not selected (and why)` section that
names FIG. 3-7 by number to document deliberate exclusion (crosstalk/correlator/phase-circuit
detail below the audience floor). The essay draft never mentions FIG. 3-7 in prose — a clean,
legitimate drop, exactly the case run 045 got lucky on. `gate_figure_use.py` fired real
`FIGUSE-001` fails for figures 3, 4, 5, 6, and 7 in **every one of that run's 3 rounds**
(iter 1, 2, 3 — the defect is stable across drafts, confirming it is a parse-scope bug, not
content-dependent). The orchestrator manually adjudicated the goal-2 hard-gate as clear for
that run's PASS determination (verified the real `## Selected figures` set — FIG. 1, FIG. 2 —
has zero orphans), but this is exactly the "adjudicate around it every run" mitigation cost
this proposal exists to retire.

Re-verified against the current `gate_figure_use.py` source (2026-07-01, unchanged since
2026-06-24): the diff below still applies verbatim.

`recurrence_count` 1 → 2, `status` `watch` → `recommended-apply` per this proposal's own
stated promotion rule. Mechanically safe, fully verified twice now, and has produced two real
false `FIGUSE-001` batches (5 figures × 3 rounds in run 001 alone) rather than a single latent
near-miss — the exact diff + test below are ready for direct human application.

## Proposed change (exact diff)

**File 1: `.claude/skills/_shared/scripts/gate_figure_use.py`**

Add a section-scoping helper and use it for the **selected** set only. The `used` set still
scans the whole draft (unchanged). When the `## Selected figures` heading is absent (legacy /
bare-list inputs, e.g. the fixtures and the `test_gates.py` `SELECTION` constant), it falls
back to whole-text parsing — so the change is a **strict refinement** with full backward
compatibility.

```diff
 GATE_ID = "figure_use"
 # Matches "fig-07", "FIG. 7", "Figure 7", "Fig 7".
 FIG_RE = re.compile(r"\bfig(?:ure|\.|-)?\s*0*(\d+)\b", re.IGNORECASE)
+# The selected set must come ONLY from the "## Selected figures" section, not from
+# the "## Reviewed but NOT selected" / "## Figure relationships" sections that also
+# name the dropped figures (ledger: figuse-selection-scope-overread, run 045).
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
+    # "Reviewed but NOT selected" / "Figure relationships" sections name dropped
+    # figures and must not be counted as selected (else they false-orphan).
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
  edit fixes how the script reads the file. Section-scoping is the minimal mechanical fix.
- **Mechanically safe / strict refinement.** Verified 2026-06-24:
  - run 045 live file: `{1,2,3,4,5}` → `{1,4,5}` (the bug, fixed);
  - handoff template: `{1,2}` → `{1,2}` (unchanged — its dropped figures sit in HTML comments /
    a later section, already excluded);
  - both fixtures + the `test_gates.py` `SELECTION` constant: **identical** both ways (no
    `## Selected figures` heading → whole-text fallback), so `figure-orphan` still emits
    `FIGUSE-001` and all 32 existing gate tests stay green.
- Not a reference-edit: the "mention dropped figures in prose anyway" workaround is exactly the
  per-run mitigation cost this should retire — a figure the design **dropped** should be allowed
  to be absent from prose without a spurious goal-2 hard fail.
- `recommended-apply` (updated 2026-07-01, was `watch`): the promotion trigger this proposal
  itself specified — "a second selection file with a 'Reviewed but NOT selected' section whose
  dropped figures are not echoed in prose" — fired for real in run `001-st-histogram-mechanism`
  (15 real `FIGUSE-001` false fails: 5 figures × 3 rounds). Below `RECUR_THRESHOLD` by strict
  essay-count (2 essays), but the per-run defect count and 100% reproduction rate across both
  triggering runs make this a high-confidence mechanical fix ready for direct application; not
  gated further on hitting essay-count 3.

## Regression expectation

Run `python meta/regression.py` before applying. Expected after applying:

- `python .claude/skills/_shared/scripts/test_gates.py`: all existing cases pass unchanged
  (whole-text fallback preserves the no-heading inputs) + 2 new `TestFigureUse` cases pass.
- `python meta/regression.py`:
  - `figure-orphan` fixture still emits `FIGUSE-001` (its bare-list selection has no
    `## Selected figures` heading → whole-text fallback → selected `{1,2,3}` as today;
    `must_contain_check_ids` intact);
  - `clean-baseline` still passes with no FIGUSE/FIGREF findings.
- Observable success criterion next run: a `figure-selection.md` that drops a figure can omit
  that figure from prose without a spurious `FIGUSE-001`; a genuine orphan inside
  `## Selected figures` still fails.
