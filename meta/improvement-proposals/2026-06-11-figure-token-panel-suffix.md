---
proposal_id: 2026-06-11-figure-token-panel-suffix
created: 2026-06-11T16:30:00Z
updated: 2026-06-20T17:40:00Z
status: recommended-apply
lever: gate-promotion
goal: "2"
root_cause_stage: gate
root_cause_artifact: _shared/scripts/gate_figure_use.py (FIG_RE + free-text derivation of the SELECTED set) + _shared/scripts/gate_anchors.py FIGREF_RE
recurrence_count: 3
confidence: high
triggering_findings:
  - essay_id: 2026-06-10-us12636684b1-deleted-dome, iter: 0, pattern_tag: figure-token-regex-blindspot
  - essay_id: 2026-06-11-us20260158546a1-both-and-steel, iter: 0, pattern_tag: figure-token-regex-blindspot
  - essay_id: 2026-06-20-us12430274b2-processor-on-nand-moat, iter: 0, pattern_tag: figure-token-regex-blindspot
---

> **2026-06-20 refresh (run `274-processor-on-nand-moat`).** Recurrence reached
> **3 of 3 runs** → promoted `watch` → **recommended-apply**. This run surfaced a
> **second, distinct variant** that the original panel-suffix regex fix does **not**
> address (and would, if anything, *worsen*): a **de-selection-prose** mention. See the
> new Part B below; the original lettered-panel fix is retained as Part A.

## Problem

`gate_figure_use`/`gate_anchors` derive figure sets by **regex-scanning free-text `FIG. N`
tokens** over whole handoff documents. Two distinct ways that breaks have now each surfaced:

**Variant A — lettered-panel token (runs 1 & 2).** A panel-suffixed token like "FIG. 4B" is
invisible to both regexes (`FIG_RE`, `FIGREF_RE`): the trailing letter removes the `\b` word
boundary after the digits (`\d+` cannot end at a digit→letter position), so a draft whose
only reference to figure 4 is "FIG. 4B" is **falsely orphaned** (spurious `FIGUSE-001` hard
fail, goal-2 hard-gate) and the token also escapes `FIGREF-001` off-index checking. Verified
mechanically (2026-06-11). Both runs spent a `phase2-handoff-notes` trap slot (run 2: trap 3,
across **16 lettered panel assets**) mandating the parseable form "FIG. N (panel X)" and
banning "FIG. 2A"-style sole references; the round-2 edit-log re-verified "no letter-suffixed
FIG tokens" by hand. Avoidance-by-convention worked, but taxed every run.

**Variant B — de-selection-prose mention (run 3, NEW; the failure actually fired).**
`gate_figure_use.check` computes the **SELECTED set** as
`selected = _figure_numbers(selection_text)` (line 61) — i.e. *every* `FIG. N` token anywhere
in `figure-selection.md`, **including the prose that explains which figures were NOT
selected** and the paired-figure / alternative-embodiment rows. In run 3 the
`## Selected figures` table held exactly {12, 14, 15, 16}, but the "NOT selected" note and the
alternative-embodiment row named the de-selected figures in `FIG. N` form, so the gate read
figures **1, 17, 20 as selected** and **spuriously orphaned them** (FIGUSE-001 on three
deliberately-excluded figures). The composer worked around it at Step 9 by **de-tokenizing** —
spelling out "figure one"/"figure twenty" and de-tokenizing the alternative row — so the
parsed set matched the table. Recorded verbatim in `handoff/01-design/figure-selection.md`
(Step-9 reconciliation note, 2026-06-20).

**Why Variant B is not covered by the Variant-A fix.** The panel-letter regex widening
(Part A) makes `FIG_RE` match *more* free-text tokens, not fewer — applied alone it would make
Variant B **worse** (it would also start matching "FIG. 17B"-style de-selection mentions). The
root cause of Variant B is upstream of the regex: the SELECTED set must come from a
**structured field/row**, not a free-text scan of a document that legitimately *names*
de-selected figures in prose. Part B fixes that; Part A stays valid for the *referenced-side*
scan of the draft (which has no analogous "de-referenced" prose).

Recurrence is now **3 of 3 runs** (count 3 = RECUR_THRESHOLD), two distinct mechanisms, and
run 3 actually *fired* the failure (three spurious FIGUSE-001 before the de-tokenization
workaround) rather than merely paying mitigation cost → promoted to **recommended-apply**.
The two parts share the one owner script and the one root pathology (figure sets derived from
free text); a human may apply Part A and Part B independently.

## Proposed change (exact diff)

### Part A — accept a panel-letter suffix in both figure-token regexes (Variant A)

**File 1: `.claude/skills/_shared/scripts/gate_figure_use.py`**

```diff
 GATE_ID = "figure_use"
-# Matches "fig-07", "FIG. 7", "Figure 7", "Fig 7".
-FIG_RE = re.compile(r"\bfig(?:ure|\.|-)?\s*0*(\d+)\b", re.IGNORECASE)
+# Matches "fig-07", "FIG. 7", "Figure 7", "Fig 7", and panel-suffixed "FIG. 7C".
+# The optional single panel letter is needed because a trailing letter removes the
+# \b word boundary after the digits, making "FIG. 4B" invisible and falsely
+# orphaning figure 4 (ledger: figure-token-regex-blindspot, 2/2 runs).
+FIG_RE = re.compile(r"\bfig(?:ure|\.|-)?\s*0*(\d+)[a-z]?\b", re.IGNORECASE)
```

**File 2: `.claude/skills/_shared/scripts/gate_anchors.py`**

```diff
-FIGREF_RE = re.compile(r"\bfig(?:ure|\.)?\s*(\d+)\b", re.IGNORECASE)  # Figure 3 / Fig. 3 / Fig 3
+FIGREF_RE = re.compile(r"\bfig(?:ure|\.)?\s*(\d+)[a-z]?\b", re.IGNORECASE)  # Figure 3 / Fig. 3 / Fig 3 / FIG. 3B
```

**File 3: `.claude/skills/_shared/scripts/test_gates.py`**

```diff
     def test_no_selection_skips(self):
         r = gate_figure_use.check("Figure 1.\n", {})
         self.assertTrue(r["passed"])
         self.assertTrue(_has(r, "FIGUSE-000"))
+
+    def test_lettered_panel_token_counts_for_figure(self):
+        # "FIG. 3B" must count as a reference to figure 3 (no false orphan).
+        draft = "Figure 1, Fig. 2, and FIG. 3B all appear.\n"
+        r = gate_figure_use.check(draft, {"figure_selection_text": self.SELECTION})
+        self.assertTrue(r["passed"], r["findings"])
+        self.assertFalse(_has(r, "FIGUSE-001"))
```

and in `TestAnchors`:

```diff
     def test_figref_in_index_passes(self):
         draft = "Fig. 2 and Figure 3 are referenced.\n"
         ctx = {"invention_summary_text": "", "figures_index": [1, 2, 3]}
         r = gate_anchors.check(draft, ctx)
         self.assertTrue(r["passed"], r["findings"])
+
+    def test_lettered_figref_not_in_index_fails(self):
+        # Panel-suffixed off-index token must no longer escape FIGREF-001.
+        draft = "FIG. 7C shows the gear.\n"
+        ctx = {"invention_summary_text": "", "figures_index": [1, 2, 3]}
+        r = gate_anchors.check(draft, ctx)
+        self.assertFalse(r["passed"])
+        self.assertTrue(_has(r, "FIGREF-001"))
```

Known, accepted limits (verified): plural ranges ("FIGS. 3A-5") and multi-letter panels
("FIG. 4AB") still don't match — the handoff-notes guidance that quoted spans don't count as
the composer's own reference stays valid. The change is a strict superset of current
matches: re-running both regexes over all `meta/fixtures/` files and both archived
`runs/*/essay-final.md` yields identical figure sets (checked 2026-06-11).

### Part B — derive the SELECTED set from the structured table, not free-text prose (Variant B)

The SELECTED set must be parsed from the `## Selected figures` table rows of
`figure-selection.md`, so that "NOT selected" prose, paired-figure rows, and
alternative-embodiment rows can name figures without inflating the selected set. The
referenced-side scan of the *draft* is left as a free-text scan (a draft has no analogous
"de-referenced" prose); only the *selection* side changes.

**File 4: `.claude/skills/_shared/scripts/gate_figure_use.py`** — replace the whole-text
selection scan with a structured-table parse, falling back to the free-text scan only when no
table is found (back-compat for any caller that passes a bare list):

```diff
 GATE_ID = "figure_use"
-# Matches "fig-07", "FIG. 7", "Figure 7", "Fig 7".
-FIG_RE = re.compile(r"\bfig(?:ure|\.|-)?\s*0*(\d+)\b", re.IGNORECASE)
+# Matches "fig-07", "FIG. 7", "Figure 7", "Fig 7", and panel-suffixed "FIG. 7C" (Part A).
+FIG_RE = re.compile(r"\bfig(?:ure|\.|-)?\s*0*(\d+)[a-z]?\b", re.IGNORECASE)
+# A markdown table row whose first cell names a figure: "| FIG. 14 | ... |".
+# Used to read the SELECTED set from the `## Selected figures` table ONLY, so that
+# de-selection prose and alternative-embodiment rows cannot inflate it (Variant B).
+SELECTED_ROW_RE = re.compile(r"^\s*\|\s*fig(?:ure|\.|-)?\s*0*(\d+)[a-z]?\b",
+                             re.IGNORECASE | re.MULTILINE)
+
+
+def _selected_numbers(selection_text):
+    """SELECTED set = figure numbers in the rows of the `## Selected figures` table.
+
+    Falls back to a whole-text token scan only if no such section/rows are found, so
+    existing fixtures and any bare-text callers keep working. Slicing to the section
+    means the 'NOT selected' note and the alternative-embodiment rows (which legitimately
+    NAME de-selected figures) no longer leak into the selected set (ledger:
+    figure-token-regex-blindspot Variant B, run 274-processor-on-nand-moat).
+    """
+    text = selection_text or ""
+    m = re.search(r"^#{1,6}\s*Selected figures\b", text, re.IGNORECASE | re.MULTILINE)
+    if m:
+        # From the heading to the next heading of the same-or-higher level (or EOF).
+        rest = text[m.end():]
+        nxt = re.search(r"^#{1,6}\s", rest, re.MULTILINE)
+        section = rest[: nxt.start()] if nxt else rest
+        nums = {int(x.group(1)) for x in SELECTED_ROW_RE.finditer(section)}
+        if nums:
+            return nums
+    # Fallback: legacy whole-text scan.
+    return {int(x.group(1)) for x in FIG_RE.finditer(text)}
```

```diff
-    selected = _figure_numbers(selection_text)
+    selected = _selected_numbers(selection_text)
     used = _figure_numbers(draft_text)
```

**File 5: `.claude/skills/_shared/scripts/test_gates.py`** — add to `TestFigureUse`:

```diff
+    def test_deselection_prose_does_not_inflate_selected(self):
+        # The "NOT selected" prose names figures 1, 17, 20; they must NOT be treated
+        # as selected, so referencing only the table's figures must NOT orphan them.
+        selection = (
+            "## Selected figures\n"
+            "| Figure | File |\n|---|---|\n"
+            "| FIG. 14 | f |\n| FIG. 15 | f |\n"
+            "\nNOT selected: FIG. 1 (flowchart) and FIG. 20 (block diagram); "
+            "alternative embodiments FIG. 17 are out of scope.\n"
+        )
+        draft = "FIG. 14 and FIG. 15 carry the thesis.\n"
+        r = gate_figure_use.check(draft, {"figure_selection_text": selection})
+        self.assertTrue(r["passed"], r["findings"])
+        self.assertFalse(_has(r, "FIGUSE-001"))
+
+    def test_orphan_still_caught_from_table(self):
+        # A figure in the SELECTED table but absent from the draft is still an orphan.
+        selection = ("## Selected figures\n| Figure |\n|---|\n"
+                     "| FIG. 14 |\n| FIG. 15 |\n")
+        draft = "Only FIG. 14 appears.\n"
+        r = gate_figure_use.check(draft, {"figure_selection_text": selection})
+        self.assertFalse(r["passed"])
+        self.assertTrue(_has(r, "FIGUSE-001"))  # figure 15 orphaned
```

The fallback preserves every current fixture: the `figure-orphan` and `clean-baseline`
selection inputs that are bare token text (no `## Selected figures` table) keep using the
whole-text scan and produce identical sets — verify before applying.

## Why this lever

- The defect lives in the gate script itself (`root_cause_stage: gate`); no reference edit can
  fix a regex or a derivation rule. Part A is mechanically safe (strict superset; the `fig`
  prefix still gates it, so no new match on "config 9"-style words). Part B is a tightening
  with a legacy fallback, so it cannot regress a bare-text caller.
- If applied, the per-run trap burden shrinks from load-bearing to stylistic: "FIG. N
  (panel X)" remains the *recommended* reader-facing convention, but a slipped "FIG. 7C"
  warns/fails correctly (Part A); and a designer may explain de-selection in normal `FIG. N`
  prose without spuriously orphaning excluded figures (Part B) — removing the Step-9
  de-tokenization workaround run 3 had to perform.
- Promoted to recommended-apply: recurrence 3/3 runs, and run 3 fired the actual failure
  (three spurious FIGUSE-001). Part B is the higher-priority half (it caused the real
  misfire); Part A remains valid and cheap. Apply both; they are independent edits.
- Not a reference-edit: keeping the "spell out de-selected numbers" convention in
  `figure-selection.md` (the current workaround) is a per-run tax that one forgotten token
  re-triggers — a structural parse removes the tax permanently.

## Regression expectation

- `python .claude/skills/_shared/scripts/test_gates.py`: all existing cases pass unchanged
  (Part A superset property; Part B fallback preserves bare-text inputs) + the 4 new cases
  pass (2 Part A, 2 Part B).
- `python meta/regression.py`: `figure-orphan` fixture must still emit `FIGUSE-001`
  (its selection input is bare token text → fallback path → identical set; its draft has no
  lettered tokens for the orphaned figure); `clean-baseline` must still pass with no
  FIGUSE/FIGREF findings. **Confirmed green at the pre-application baseline 2026-06-20**
  (`REGRESSION: PASS`, 32/32 gate tests, both fixtures ok).
- Success criterion for the next lettered-panel or multi-row-selection patent: zero spurious
  FIGUSE-001, and no Step-9 de-tokenization or trap-slot mitigation needed.
