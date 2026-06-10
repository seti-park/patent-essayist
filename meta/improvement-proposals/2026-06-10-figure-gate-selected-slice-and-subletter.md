# Proposal: figure-use gate — selected-only slice invocation + sub-letter parsing

- **Date:** 2026-06-10
- **Triggering run:** `001-google-quantum-control` (iter 1) — ledger records with
  `pattern_tag: figure-gate-context-mismatch` and `figure-subletter-parse-gap`
- **Recurrence count:** 1 each (first run) — **below** RECUR_THRESHOLD=3
- **Signal:** `watch` — but both defects are **deterministic**, not stochastic: they will
  reproduce on every run whose figure-selection records a sheet map (the Phase-1 template
  now does) and on every patent with sub-lettered figures (FIG. 3A…3K here). Treat as a
  recommended-apply candidate at the maintainer's discretion despite the count.
- **Goal threatened:** 2 (figures + spec sufficiency) — the gate guarding goal 2 produced
  10 false FIGUSE-001 failures, and its parser cannot see sub-lettered references at all.
- **Confidence:** high (reproduced both ways in the run: full file → 10 false orphans;
  `## Selected figures`-only slice → all gates pass; `FIG. 3A` verified non-matching
  against `FIG_RE`, `fig-16.jpg` verified matching as figure 16).

## Evidence

1. Documented invocation (`patent-essay/SKILL.md` → `--figure-selection
   handoff/01-design/figure-selection.md`) fed the gate the full file, whose 17-row
   sheet↔FIG mapping table mentions `fig-01…fig-17`; `gate_figure_use` parsed every
   number as "selected" and failed figures 2,3,6,7,10,11,12,13,14,17 as orphans —
   none of which Phase 1 selected. Archived in
   `runs/001-google-quantum-control/score-history.md`.
2. The orchestrator worked around it mid-run by slicing the `## Selected figures`
   section to `figure-selection-gate.md`; gates then passed with zero findings.
3. `FIG_RE = r"\bfig(?:ure|\.|-)?\s*0*(\d+)\b"` — `"FIG. 3A"` does not match (no word
   boundary between `3` and `A`); `"fig-16.jpg"` matches as figure 16 (sheet-file token
   pollutes the used/selected sets).

## Lever

**(b) gate strengthening** (`gate_figure_use.py`) + **(a) reference/procedure edit**
(`patent-essay/SKILL.md` invocation + `handoff-template/01-design/figure-selection.md`).

## Exact diff (apply after `python meta/regression.py` is green)

### 1. `gate_figure_use.py` — parse sub-letters; key the used-set on textual FIG refs

```diff
-# Matches "fig-07", "FIG. 7", "Figure 7", "Fig 7".
-FIG_RE = re.compile(r"\bfig(?:ure|\.|-)?\s*0*(\d+)\b", re.IGNORECASE)
+# Matches "fig-07", "FIG. 7", "Figure 7", "Fig 7", and sub-lettered forms
+# "FIG. 3A" / "FIGS. 3B-3D" (letter suffix ignored: 3A -> 3).
+FIG_RE = re.compile(r"\bfig(?:ures|ure|s|\.|-)?\s*0*(\d+)(?:[A-Za-z](?:-\d*[A-Za-z])?)?\b",
+                    re.IGNORECASE)
```

Optionally (stricter): for the DRAFT side, count only `FIG(S)./Figure` textual forms and
ignore `fig-NN` file tokens (image paths), so sheet filenames cannot satisfy a figure
reference. Decide when applying; add a fixture either way.

### 2. `patent-essay/SKILL.md` — make the slice the documented invocation

```diff
-  --figure-selection handoff/01-design/figure-selection.md --json
+  --figure-selection handoff/01-design/figure-selection-gate.md --json
+
+(Before the first gate run, extract the `## Selected figures` section of
+`figure-selection.md` to `figure-selection-gate.md` — the gate's "selected" set is
+exactly the figures the essay must use, not the sheet-mapping documentation.)
```

### 3. `handoff-template/01-design/figure-selection.md` — add a note

Mark the `## Selected figures` section as the machine-read region (the gate consumes
only this section via the orchestrator slice); sheet↔FIG mapping stays documentation.

### 4. `meta/attribution-table.md` — add routing rows (new classes)

```
| `figure-gate-context-mismatch` | gate FIGUSE-001 (false) | 2 | design | patent-essay invocation + figure-selection template | reference-edit |
| `figure-subletter-parse-gap`   | gate FIGUSE/FIGREF      | 2 | gate   | gate_figure_use.py FIG_RE | gate-promotion |
| `claim-adequacy-overreach`     | pass-3                  | 1 | compose | citation-format.md | reference-edit |
| `sources-entry-fidelity`       | pass-6 6C               | 4a | compose | x-articles-format-en.md | reference-edit |
```

## Regression protection

Add a fixture `meta/fixtures/figure-subletter/`: draft referencing "FIG. 3A" with
figure-selection slice selecting FIG. 3 → expect no FIGUSE-001 after the regex change
(and FIGUSE-001 present before it, demonstrating the gap).

## Status

`watch` (count 1). Apply manually after `python meta/regression.py` passes; flip the two
triggering ledger records to `resolved` with a new appended record citing this file.
