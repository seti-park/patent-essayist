# Figure Selection

## Selected figures

| Figure | File | Thesis point (spine element / section) | caption_role |
|---|---|---|---|
| FIG. 1 | fig-01.png | ToF imager architecture + raw histogram output — establishes the shared vocabulary with Article 1 (2-problem) | header_composite |
| FIG. 3 | fig-03.png | The cross-talk peak and real-target peak in the histogram, recalibrated to the reference zero-point — the "ghost in the histogram" (2-problem) | body_figure_carries_unique_info |
| FIG. 6 | fig-06.png | ZCF and MF output signals overlaid on the histogram, showing both candidate peaks (611, 613) — sets up the classification problem (3-mechanism) | body_figure_carries_unique_info |
| FIG. 9 | fig-09.png | The weighted-ZCF curve (601W) and the P_thresh/N_thresh classification thresholds — the actual "ghost test" computation (3-mechanism) | body_figure_carries_unique_info |
| FIG. 10 | fig-10.png | Full adaptive-detection flow chart — MF path, ZCF path, weighting, classification, switch-over decision, as one system (3-mechanism / 4-steelman) | body_figure_carries_unique_info |
| FIG. 12 | fig-12.png | Adaptive-method performance WITH cross-talk present — the payoff half of the before/after pair (5-effect) | body_figure_carries_unique_info |
| FIG. 13 | fig-13.png | On-chip IC placement — peak-finding circuit integrated on the same die as the SPAD array (6-product-meaning) | body_figure_prose_covers_fully |

<!-- FIG. 2 was reviewed as the paired precursor to FIG. 3 (same histogram, bin-number x-axis
     rather than distance/reference-zero-point) but NOT selected: FIG. 3 is the recalibrated,
     load-bearing version that carries the "reference zero-point" concept the mechanism section
     needs, and showing both would repeat the same two peaks without adding reader value. This
     pair-break is intentional and is flagged in phase2-handoff-notes.md so Phase 2 does not
     reopen it.

     FIG. 11 was reviewed as the paired precursor to FIG. 12 (same experiment, no cross-talk
     present) but NOT selected on its own: the essay's argument is about cross-talk rejection,
     so the "no cross-talk" baseline case is described in prose (drawing on invention-summary.md
     [0066]-[0067] verbatim anchors) rather than rendered as a second figure, keeping the visual
     budget on the cross-talk-present payoff (FIG. 12) where the thesis's claim actually lands.
     This pair-break is also flagged in phase2-handoff-notes.md.

     FIGS. 7/8 (weight-coefficient curve families) were reviewed and NOT selected: the underlying
     concept (negative weights before the reference zero-point, positive after) is carried by
     FIG. 9's weighted-ZCF curve, which shows the concept already applied to actual signal data
     rather than as an abstract coefficient plot — more legible for the target general-audience
     reader per essay-context.md. FIGS. 4/5 (raw ZCF/MF filter shapes in isolation) were reviewed
     and NOT selected for the same reason: FIG. 6 shows the same filters' actual OUTPUT on real
     histogram data, which is the more reader-useful and less abstract figure. FIG. 14 (pixel-level
     integration variant) was reviewed and NOT selected: FIG. 13's block-level on-chip diagram
     already carries the "no off-chip processor needed" point; FIG. 14 is a deeper architectural
     variant not needed for this essay's thesis. FIG. 15 (claim-1-level flow chart) was reviewed
     and NOT selected: FIG. 10's fuller adaptive-detection flow chart already carries the same
     ZCF-classification steps plus the MF/switch-over context FIG. 15 omits, so FIG. 10 alone
     covers the ground for this essay's needs without duplicating a near-identical flow chart. -->

## Paired-figure relationships (acknowledged)

<!-- Mirrors invention-summary.md §"Figure relationships" for the pairs touched by this
     selection. -->
| Figure(s) | Relationship | Treatment in selection |
|---|---|---|
| FIG. 2 + FIG. 3 | same histogram, re-plotted (raw bin-number axis vs recalibrated distance/reference-zero-point axis) | FIG. 3 selected, FIG. 2 dropped — pair-break is intentional (flagged in phase2-handoff-notes.md); FIG. 3 alone carries the load-bearing "reference zero-point" concept |
| FIG. 6 + FIG. 9 | progressive sequence (FIG. 6 = raw filter outputs overlaid on histogram; FIG. 9 = zoomed-in weighted classification) | Both selected — this is the one pair kept intact, since FIG. 6 sets up the two candidate peaks and FIG. 9 shows the actual test that tells them apart; splitting this pair would break the "here's the problem, here's the test" narrative |
| FIG. 7 + FIG. 8 | same-page sub-figure pair (full-range weight curves + zoomed inset) | NOT selected — the underlying weight-coefficient concept is carried by FIG. 9's weighted-ZCF curve applied to real data instead |
| FIG. 11 + FIG. 12 | progressive sequence (before / after — no cross-talk vs cross-talk present) | FIG. 12 selected, FIG. 11 dropped — pair-break is intentional (flagged in phase2-handoff-notes.md); the "before" (no cross-talk) case is carried in prose, keeping the single payoff figure on the cross-talk-present case the thesis is actually about |
| FIG. 13 + FIG. 14 | same-page sub-figure pair (architecture variants — block-level vs pixel-level integration) | FIG. 13 selected, FIG. 14 dropped — pair-break is intentional (flagged in phase2-handoff-notes.md); FIG. 13's block-level diagram is sufficient for the "on-chip, no off-chip processor" point |
| FIG. 1 | standalone | selected as header composite — shared vocabulary anchor with Article 1 |
| FIG. 10 | standalone | selected — the one whole-system flow chart, not itself paired with another figure |

## Header / body assignment

- **Header**: FIG. 1 (ToF imager architecture + histogram — the explicit visual callback to
  Article 1's own established vocabulary, before the essay complicates it)
- **Body**: FIG. 3, FIG. 6, FIG. 9, FIG. 10, FIG. 12, FIG. 13

<!--
  > Revision note — triggered by [step 9, figure mapping] [2026-07-01]: initial figure-mapping
  pass considered selecting FIG. 2 alongside FIG. 3 for a "before/after recalibration" beat, but
  this was dropped in favor of FIG. 3 alone once thesis-spine.md's section trace confirmed
  2-problem does not need the recalibration mechanic itself (that belongs to the reference-
  zero-point concept in 3-mechanism, already carried by FIG. 9) — only the ghost-vs-real-peak
  visual. No cascading revision to thesis-spine.md was needed.
-->
