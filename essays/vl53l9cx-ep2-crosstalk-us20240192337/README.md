# The chip that ignores its own reflection — US 2024-0192337 B2 (VL53L9CX series, Article 2 of 3)

A general-audience patent-analysis essay on STMicroelectronics' "Cross-talk rejecting
convolution peak finding" (US 2024-0192337 B2), produced through the full `patent-essay`
pipeline (Phase 1 Design → Phase 2 Compose → Phase 3 Edit loop → post-acceptance self-audit →
meta-loop). This is **Article 2 of a 3-part series** on STM's VL53L9CX dToF 3D LiDAR module:
Article 1 covers the histogram mechanism (US2026-0140238), this essay covers robustness against
cover-glass cross-talk, and Article 3 (US2023-0356397) will carry the throughline to SLAM /
robot behavior.

## Final deliverable

- `essay-final.md` — the clean, reader-facing article (publication form: frontmatter stripped,
  `# Sources` kept). ~2,400 words of body. Title: "The Chip Learns to Ignore Its Own Reflection
  in the Glass."

## How it was produced (artifacts)

| Stage | Files |
|---|---|
| Phase 1 Design (`thesis-architect`, voice-off) | `handoff/01-design/`: invention-summary, thesis-spine (Q7 hook: `technical-impossibility`), thesis-candidates, fact-check-log, figure-selection, figure-rationale, phase2-handoff-notes, search-log, figures-index |
| Phase 2 Compose (`essay-en-composer`, voice-on, strict-execution + measured) | `handoff/02-compose/`: essay-draft, publication, thesis-trace, figures-rationale |
| Phase 3 Edit (`editorial-review`, voice-fenced, 2 rounds) | `handoff/03-edit/`: edit-log (final, iteration 2 — `pass`), edit-log-iter1 (iteration 1 — `revise-required`, preserved for the record), essay-final, gate-result.json, score-history, revision-notes (self-audit deltas) |
| Run evidence (top level) | `edit-log.md`, `score-history.md`, `gate-result.json`, `essay-context.md`, `revision-notes.md`, `revision-notes.ledger.jsonl` (this essay's slice of `meta/findings-ledger.jsonl`) |
| Figures | `figures/`: fig-01 (header), fig-03, fig-06, fig-09, fig-10, fig-12, fig-13 — the 7 figures `figure-selection.md` actually selected, out of 15 available |

## Result

- **Inner loop**: 2 iterations (cap 4). Iteration 1 returned `revise-required` (missing `##
  Patents` in Sources — high; one over-long 3-idea paragraph — medium; 2 low/optional notes).
  Iteration 2, after Compose applied the fixes, returned a clean `pass`. Deterministic gates:
  all 11 PASS on the final round.
- **Post-acceptance self-audit** (2 independent fresh-context reviewer rounds — impatient
  investor + skeptical pro-subject reader personas — against `essay-final.md` and the raw
  patent, no exposure to the design process): round 1 caught and fixed 2 real grounding issues a
  passing review had missed (a citation anchored to the wrong paragraph; an inference —"not a
  per-unit factory trim" — presented as patent fact when the patent's own word for that
  mechanism is "calibration"). Round 2 independently confirmed **dry** (no new findings).
  Full detail: `revision-notes.md`.
- **Meta-loop** (`pipeline-retro`, propose-only): normalized this run into
  `meta/findings-ledger.jsonl`; one recurring class (`sources-entry-template-drift`, now at 4
  occurrences across 3 essays) crossed the promotion threshold and produced
  `meta/improvement-proposals/2026-07-01-sources-entry-field-completeness.md`
  (`recommended-apply`, awaiting human review + regression).
- **Infrastructure side-effect**: this run also found and fixed a real bug in
  `_shared/scripts/gate_figure_use.py` (false-positive orphan-figure findings from
  rejection-rationale text) — see `meta/improvement-proposals/2026-06-24-figuse-selection-scope.md`
  for the full reconciliation against the proposal that was already on file for it.

## The thesis in one line

Article 1 taught the histogram (a per-distance count of returned laser photons) as this
sensor's raw material; this patent's contribution is that the histogram arrives contaminated by
the sensor's own reflection off its cover glass, and its specific fix (a weighted zero-crossing
classification pinned to a fixed, geometry-derived reference point, combined with a matched-filter
switch-over) is the concrete mechanism behind ST's own "on-chip cross-talk / veiling-glare
compensation" marketing claim for VL53L9CX.

## Reproduce the validation

```
python .claude/skills/_shared/scripts/run_gates.py \
  --draft essays/vl53l9cx-ep2-crosstalk-us20240192337/essay-final.md \
  --invention-summary essays/vl53l9cx-ep2-crosstalk-us20240192337/handoff/01-design/invention-summary.md \
  --figures essays/vl53l9cx-ep2-crosstalk-us20240192337/handoff/01-design/figures-index.txt \
  --figure-selection essays/vl53l9cx-ep2-crosstalk-us20240192337/handoff/01-design/figure-selection.md
```

## Scope note

A general-audience technical read of one patent in a hero-plus-cluster set; the supporting
patent (US 2025-0012901) and five cluster patents are acknowledged at the depth `essay-context.md`
specifies (one paragraph and one sentence respectively) and are not independently fact-checked
against their own full specifications, which were not part of this run's uploads.
