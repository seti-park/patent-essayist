---
proposal_id: 2026-06-12-figuse-selection-scope-fixture
created: 2026-06-12T05:00:00Z
status: watch
lever: gate-promotion
goal: "2"
root_cause_stage: gate
root_cause_artifact: meta/fixtures/ (regression-guard coverage for gate_figure_use selected-set scoping)
recurrence_count: 1
confidence: high
triggering_findings:
  - essay_id: tesla-washer-pump-two-wire-moat, iter: 0, pattern_tag: gate-selection-scope-overharvest  # FIGUSE-001 false fail on not-selected FIG. 4/5
---

## Problem

In run `tesla-washer-pump-two-wire-moat`, `gate_figure_use` false-failed (FIGUSE-001) on FIG. 4
and FIG. 5 because it harvested figure numbers from the whole `figure-selection.md`, including
the `## Not selected` table that the handoff template schema *requires*. The gate code fix is
**already applied and committed** (a980562: harvesting scoped to `## Selected figures` with
free-form fallback, plus `test_gates.py` template-schema cases) — **this proposal does not
re-fix the gate.**

The residual gap is in the regression guard: both fixtures under `meta/fixtures/`
(`clean-baseline`, `figure-orphan`) use *free-form list* selection files, so the fixture layer —
the check `meta/regression.py` runs before any proposal is applied, whose documented contract
includes "no longer exhibits the previously-recurring defect check_id" — cannot detect a
re-regression of this class if a future gate edit reverts or breaks the scoping. The unit tests
cover it today, but fixtures are the artifact-shaped guard and the declared home for
defect-class locks (`must_not_contain_check_ids`).

## Proposed change (exact diff)

New fixture directory `meta/fixtures/template-schema-selection/` (no existing file modified):

`expect.json`
```json
{"gate_pass": true, "must_not_contain_check_ids": ["FIGUSE-001"]}
```

`figure-selection.md`
```markdown
# Figure Selection

## Selected figures

| Figure | File | Thesis point | caption_role |
|---|---|---|---|
| FIG. 1 | fig-01.jpg | mechanism overview | header_composite |
| FIG. 2 | fig-02.jpg | deleted part made visible | body_figure_carries_unique_info |

## Not selected

| Figure | File | Reason |
|---|---|---|
| FIG. 4 | fig-04.jpg | flowchart restating claim language; adds nothing |
| FIG. 5 | fig-05.jpg | generic architecture boilerplate |
```

`figures-index.txt`
```
1
2
4
5
```

`draft.md` — a minimal gate-clean draft (copy `meta/fixtures/clean-baseline/draft.md` and ensure
the body references FIG. 1 and FIG. 2 only — FIG. 4 / FIG. 5 must appear nowhere in prose, so the
fixture passes only if the gate correctly ignores the Not-selected table).

`invention-summary.md` — copy from `clean-baseline` (context only).

## Why this lever

Gate-promotion (strengthening the guard around a gate) is the matching lever; the proposal-format
rule "must ship with a test" is satisfied — the fixture *is* the test, in the layer that gates
proposal application. Reference-edit fixes nothing here (no skill misbehaved) and the defect was
mechanical with a known reproduction, so a fixture is exact and false-positive-free. `watch`
status per the promotion rules: single occurrence, and the defect itself is already resolved —
this only locks the resolution in.

## Regression expectation

`python meta/regression.py` must pass with the new fixture on current HEAD (the fixed gate
ignores the Not-selected table, so `gate_pass: true` and no FIGUSE-001). To validate the fixture
bites: temporarily reverting a980562's `gate_figure_use.py` hunk must make exactly this fixture
fail with FIGUSE-001 while `clean-baseline` and `figure-orphan` keep their verdicts.
