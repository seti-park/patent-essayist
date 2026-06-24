---
proposal_id: 2026-06-24-figure-selection-scope-bleed
created: 2026-06-24T19:00:00Z
status: watch
lever: gate-promotion
goal: "2"
root_cause_stage: gate
root_cause_artifact: _shared/scripts/gate_figure_use.py (_figure_numbers scans the whole figure-selection.md) + _shared/scripts/run_gates.py build_context (reads the entire file into figure_selection_text)
recurrence_count: 1
confidence: high
triggering_findings:
  - essay_id: 045-agility-cycloid-vertical-integration, iter: 0, pattern_tag: figure-selection-scope-bleed
---

## Problem

`gate_figure_use` derives its **selected-figure set** by scanning *every* `FIG. N` /
`fig-NN` token in the whole `handoff/01-design/figure-selection.md` file. The orchestrator
passes the file via `run_gates.py --figure-selection`, `build_context` reads the entire file
into `figure_selection_text`, and `gate_figure_use._figure_numbers(selection_text)` regexes
the lot. But `thesis-architect`'s `figure-selection.md` does not contain only selected
figures: it also carries a **`## Paired-figure relationships`** table and **cut-figure
commentary** that name figures explicitly marked *NOT selected* / *dropped*.

Worked example, straight from `handoff-template/01-design/figure-selection.md`: the
`## Selected figures` table lists {1, 2, 4} (FIG. 4A → 4), but the file also says
"FIG. 7A / 7B / 7C ... NOT selected" and "FIG. 4B ... dropped". `_figure_numbers` over the
whole file returns **{1, 2, 4, 7}** — figure 7 is pulled into the "selected" set purely from
the line that says it was *rejected*. A draft that correctly omits figure 7 is then flagged
`FIGUSE-001` (selected-but-unused **orphan**) — a **goal-2 HARD fail**, fired by a
contract mismatch, not by anything wrong with the essay. Verified mechanically against
`gate_figure_use.py` + `run_gates.py` + the Phase-1 template (2026-06-24).

**This is a distinct defect from `2026-06-11-figure-token-panel-suffix`**, and must not be
deduped into it:

| | panel-suffix proposal | this proposal |
|---|---|---|
| token affected | `FIG. 4B` (lettered) | any `FIG. N` in a non-selected section |
| direction | **under**-count (token invisible → orphan of the *referenced* fig) | **over**-count (cut figure counted as selected → orphan of the *cut* fig) |
| fix surface | regex word-boundary (`[a-z]?`) | input scope (which part of the file feeds the selected set) |

Applying the panel-suffix regex fix does **not** address this; if anything it widens the
bleed (more cut-figure tokens would match).

Recurrence determination, per the run-1 framing reused throughout this ledger ("candidate
gate-strengthening **if it recurs**"): run 045 is the **first explicit articulation** of this
scope-bleed class (count 1 → `watch`). The *failure* did not fire in run 045 only because
Phase 2 spent effort spelling out every cut-figure mention so the gate happened to parse
exactly the survivor set {1, 3, 7, 10, 18}, and the survivor-vs-cut sets did not collide.
That is avoidance-by-convention — the same per-run mitigation tax already on record for the
panel-suffix class — and it sits one un-rewritten cut-figure token away from a spurious hard
FAIL. The full diff + test are filed now (gate changes must ship with tests) so a human can
apply early; a second essay where a cut figure's number is absent from the survivor set, or
one actual spurious `FIGUSE-001`, promotes this to `recommended-apply`.

## Proposed change (exact diff)

Scope the selected-set parse to the `## Selected figures` section only. Tokens that appear
in the paired-figure table or cut-figure commentary no longer count as selected. The reverse
direction (`used - selected` → FIGUSE-002 off-plan warn) is unaffected.

**File 1: `.claude/skills/_shared/scripts/gate_figure_use.py`**

```diff
 GATE_ID = "figure_use"
 # Matches "fig-07", "FIG. 7", "Figure 7", "Fig 7".
 FIG_RE = re.compile(r"\bfig(?:ure|\.|-)?\s*0*(\d+)\b", re.IGNORECASE)
+# The SELECTED set must come only from the "## Selected figures" section of
+# figure-selection.md; the file also carries a "## Paired-figure relationships"
+# table and cut-figure commentary that NAME non-selected figures. Scanning the
+# whole file pulls cut figures into the selected set and spuriously orphans them
+# (ledger: figure-selection-scope-bleed, run 045). Section header is matched
+# case-insensitively; the section runs until the next "## " heading or EOF.
+SELECTED_HEADING_RE = re.compile(
+    r"^\s*##\s+selected\s+figures\b.*?(?=^\s*##\s+|\Z)",
+    re.IGNORECASE | re.MULTILINE | re.DOTALL,
+)
+
+
+def _selected_section(text):
+    """Return the body of the '## Selected figures' section, or the whole text
+    if no such heading exists (back-compat with the flat test fixture)."""
+    if text is None:
+        return ""
+    m = SELECTED_HEADING_RE.search(text)
+    return m.group(0) if m else text
```

and scope the selected-set parse in `check`:

```diff
-    selected = _figure_numbers(selection_text)
+    # Only figures named under "## Selected figures" are selected; cut-figure
+    # commentary and the paired-figure table elsewhere in the file are excluded.
+    selected = _figure_numbers(_selected_section(selection_text))
     used = _figure_numbers(draft_text)
```

Also extend the module docstring's FIGUSE-001 note:

```diff
-  FIGUSE-001 (fail): a SELECTED figure is never referenced in the draft (orphan).
+  FIGUSE-001 (fail): a SELECTED figure is never referenced in the draft (orphan).
+    "Selected" = figures named under the "## Selected figures" heading only;
+    figures named in the paired-figure table / cut-figure notes do not count.
```

**File 2: `.claude/skills/_shared/scripts/test_gates.py`** — add to `TestFigureUse`
(realistic multi-section selection that names a cut figure):

```diff
     def test_no_selection_skips(self):
         r = gate_figure_use.check("Figure 1.\n", {})
         self.assertTrue(r["passed"])
         self.assertTrue(_has(r, "FIGUSE-000"))
+
+    # Realistic figure-selection.md: a "## Selected figures" table plus a
+    # "## Paired-figure relationships" section that NAMES a cut figure (7).
+    SELECTION_WITH_CUTS = (
+        "# Figure Selection\n\n"
+        "## Selected figures\n"
+        "| FIG. 1 | fig-01.png | lead | header_composite |\n"
+        "| FIG. 2 | fig-02.png | mechanism | body_figure_carries_unique_info |\n\n"
+        "## Paired-figure relationships (acknowledged)\n"
+        "| FIG. 7A / 7B / 7C | progressive sequence | NOT selected |\n"
+    )
+
+    def test_cut_figure_not_counted_as_selected(self):
+        # Draft uses only the two truly-selected figures; figure 7 is named
+        # ONLY in the cut-figure section and must NOT orphan the draft.
+        draft = "Figure 1 and Fig. 2 are discussed.\n"
+        r = gate_figure_use.check(
+            draft, {"figure_selection_text": self.SELECTION_WITH_CUTS})
+        self.assertTrue(r["passed"], r["findings"])
+        self.assertFalse(_has(r, "FIGUSE-001"))
+
+    def test_selected_section_orphan_still_fails(self):
+        # A figure truly in "## Selected figures" but unused still orphans.
+        draft = "Figure 1 only.\n"  # FIG. 2 selected but unused
+        r = gate_figure_use.check(
+            draft, {"figure_selection_text": self.SELECTION_WITH_CUTS})
+        self.assertFalse(r["passed"])
+        self.assertTrue(_has(r, "FIGUSE-001"))
```

Back-compat: when no `## Selected figures` heading is present (e.g. the existing flat
`SELECTION` one-liner fixture), `_selected_section` returns the whole text, so every current
test passes unchanged. The change is a strict *narrowing* of the selected set on real Phase-1
files and a no-op on heading-less input.

### Alternative lever (noted, not chosen here)
A `reference-edit` to `thesis-architect` could instead emit a fenced machine-readable
selected list (e.g. a ```selected-figures\n1,3,7,10,18\n``` block) that the gate consumes by
preference. That is cleaner long-term but touches a skill body + the gate + the handoff
contract (three artifacts, two stages) and would force every existing `figure-selection.md`
to be regenerated. The section-scope fix above is self-contained in the gate, backward
compatible, and ships today; the machine-readable-list option is the right follow-up if a
*third* figure-selection contract finding appears.

## Why this lever

- The defect lives in the gate's own input handling (`root_cause_stage: gate`); no reference
  or prose edit can stop a regex from reading the wrong span of a file. Gate-promotion (here,
  gate-*correction* shipped with tests) is the matching lever.
- Mechanically safe: the fix only *removes* figures that were never selected from the
  selected set, so it can only ever turn a spurious FAIL into a PASS or leave behavior
  identical — it cannot introduce a new false orphan. The `## Selected figures` heading is a
  fixed element of the `thesis-architect` Step-9 schema (`handoff-template/01-design/
  figure-selection.md`), so the anchor is reliable.
- `watch`, not `recommended-apply`: count is 1 for this distinct class and the failure has
  never actually fired in a run. The diff + tests are filed so a human can apply early
  (same posture as `2026-06-11-figure-token-panel-suffix`).

## Regression expectation

- `python .claude/skills/_shared/scripts/test_gates.py`: all existing cases pass unchanged
  (the flat `SELECTION` fixture has no `## Selected figures` heading → `_selected_section`
  returns it whole → identical results) + the 2 new `TestFigureUse` cases pass.
- `python meta/regression.py`: `figure-orphan` fixture must still emit `FIGUSE-001`
  (its selection's orphaned figure is in the selected section, so narrowing does not hide
  it); `clean-baseline` must still pass with no FIGUSE finding. If any fixture's
  `figure-selection` input lacks a `## Selected figures` heading, behavior is unchanged by
  the back-compat fallback.
- Success criterion: a future run whose `figure-selection.md` names cut figures no longer
  needs Phase 2 to spell out cut-figure mentions to avoid a spurious orphan; FIGUSE-001 fires
  only on a genuinely selected-but-unused figure.
