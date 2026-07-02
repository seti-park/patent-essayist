---
proposal_id: 2026-07-02-section-blueprint-paragraph-word-band
created: 2026-07-02T00:00:00Z
status: recommended-apply
lever: reference-edit
goal: "3"
root_cause_stage: compose
root_cause_artifact: essay-en-composer/references/section-blueprint.md (word_target is per-SECTION only; no per-paragraph band, so walls are drafted and the loop pays to remove them)
recurrence_count: 12
confidence: high
triggering_findings:
  - essay_id: 2026-07-01-us20230356397b2-cliff-histogram-bridge, iter: 1, pattern_tag: mobile-paragraph-wall (recurred iters 1→2→3→4 within one inner loop — 3 avoidable rounds)
  - essay_id: 001-st-histogram-mechanism, iter: 1, pattern_tag: mobile-paragraph-wall (9 dense paragraphs in round 1)
  - essay_id: 2026-06-27-us12560948b2-safe-stop-e2e, iter: 1, pattern_tag: mobile-paragraph-wall
  - essay_id: 2026-06-10-us12636684b1-deleted-dome, iter: 1, pattern_tag: mobile-paragraph-wall
  - essay_id: 2026-06-11-us20260158546a1-both-and-steel, iter: 1, pattern_tag: mobile-paragraph-wall
---

## Problem

`mobile-paragraph-wall` is the system's most expensive craft class: 12 ledger records across
6 of the recorded runs, including 4 recurrences *within one essay's inner loop*
(cliff-histogram-bridge, iters 1→4 — 3 full Compose↔Edit rounds spent re-splitting
paragraphs). The detection side is now fully mechanical (STRUCT-005 word warn + STRUCT-001
aligned to Pass 2C, both applied 2026-07-02), but detection still means the wall was DRAFTED
and a loop round pays to remove it. The 2026-06-11 word-wall proposal explicitly deferred
this compose-side companion ("a paragraph word band in section-blueprint.md ... is the
natural follow-up"); the cliff run's within-loop recurrence is the evidence it was waiting
for.

## Proposed change (exact diff)

**File: `.claude/skills/essay-en-composer/references/section-blueprint.md`** — extend the
`word_target` field spec (currently "`word_target` — integer. Composer writes within ±20%."):

```diff
 - `word_target` — integer. Composer writes within ±20%.
+- **Paragraph band (joint, draft-time)** — every body paragraph stays within BOTH bands:
+  3–7 sentences AND ≤ 110 words (the mechanical mirrors: STRUCT-001 warns at ≥ 8 sentences,
+  STRUCT-005 at > 110 words ≈ 8 mobile lines; editorial Pass 2C flags ≥ 8 sentences high).
+  Draft TO the band — do not draft walls for the loop to split (mobile-paragraph-wall has
+  cost 3 full revision rounds in a single essay). One idea per paragraph: if a paragraph
+  needs a second idea to justify its length, it is two paragraphs.
+- **Recount after structural edits** — any split/merge during drafting or revision can push
+  a NEIGHBOR paragraph across the band (revision-induced-band-break); re-count every
+  paragraph in a touched section before handing off.
```

## Why this lever

- The gate half of this class is done; what remains is procedural — the composer has a
  per-section budget but no per-paragraph rule, so the band exists only in Edit's head. A
  reference-edit puts the band where drafting happens.
- Zero false-positive risk: the band restates thresholds already enforced downstream
  (STRUCT-001/005, Pass 2C); nothing that currently passes becomes non-compliant.
- Complements `2026-07-02-composer-revision-mode-discipline.md` (its re-scan rule and this
  recount rule are the same discipline at revision time vs draft time).

## Regression expectation

Documentation-only. `test_gates.py` + `meta/regression.py` unchanged green. Success
criterion: next run's iter-1 draft produces zero STRUCT-005 warns and zero pass-5
mobile-wall findings — the class stops costing rounds because walls stop being drafted.
