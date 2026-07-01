# Figure Rationale

## FIG. 1 — ToF imager architecture + histogram

- **Purpose**: Shows the SPAD array (101), light source/VCSEL (103), TDCs (107), and the
  resulting histogram (109) as one system — the same architecture and the same "histogram"
  concept Article 1 established, redrawn here as the shared starting point for this essay.
- **Intended effect**: Grounds the reader immediately in familiar territory before the essay
  complicates it — "you already know this diagram, you already know what a histogram is; here
  is what we're about to discover is wrong with it." Functions as the explicit visual anchor for
  the required Article 1 histogram callback. (caption_role: header_composite — detailed caption
  naming the SPAD array, emitter, and histogram output.)

## FIG. 3 — The ghost and the real target, recalibrated

- **Purpose**: Shows the histogram with two peaks — 201 (cross-talk, sitting at the recalibrated
  "reference zero-point," essentially distance zero) and 203 (the real target, further out) —
  supporting `[0029]`'s and `[0033]`'s anchors on cross-talk and the reference zero-point.
- **Intended effect**: Makes the "ghost parked right in front of the sensor" claim visually
  concrete — the reader sees the tall, sharp near-zero peak and the shorter, real-target peak
  side by side, before any explanation of how the chip tells them apart. This is the essay's
  single most load-bearing "problem" image. (caption_role: body_figure_carries_unique_info —
  medium caption naming both peaks and what the recalibrated zero point represents.)

## FIG. 6 — Both filters see the same ghost

- **Purpose**: Shows the ZCF output (601) and MF output (603) overlaid on the same
  (recalibrated) histogram, with maximum peaks 611 (cross-talk candidate) and 613 (real-target
  candidate) marked in both filter outputs — establishing that both filter types "see" the same
  two candidate peaks before classification happens.
- **Intended effect**: Sets up the steelman beat's premise — neither filter type inherently
  knows which peak is real; both just find local maxima. Prepares the reader for FIG. 9's
  payoff, where the classification actually happens. (caption_role:
  body_figure_carries_unique_info — medium caption identifying the ZCF/MF curves and the two
  labeled peaks.)

## FIG. 9 — The ghost test itself

- **Purpose**: Shows the weighted ZCF curve (601W) alongside the raw ZCF curve (601), with the
  positive/negative classification thresholds (P_thresh, N_thresh) marked — this is the actual
  computation that decides peak 611 is cross-talk and peak 613 is a real target, grounded in
  `[0052]`'s classification rule and `[0049]`-`[0050]`'s weighted-sum computation.
- **Intended effect**: This is the payoff figure for the mechanism section — the reader watches
  the same two candidate peaks from FIG. 6 get pulled apart by the weighting, with one now
  sitting outside the threshold band and one inside it. Directly supports the "how does the chip
  tell them apart without an outside reference" hook resolution. (caption_role:
  body_figure_carries_unique_info — medium caption naming the weighted curve and the threshold
  lines.)

## FIG. 10 — The whole system, in one flow chart

- **Purpose**: Shows the complete adaptive-detection method — MF path (803, 805), ZCF path
  (811, 815, 817, 818, 819), weight-coefficient generation (807, 809), and the switch-over
  decision module (821) that produces the strongest target (823) and the combined target list
  (825) — the single figure that shows both filters and the classification/switch-over as one
  integrated system.
- **Intended effect**: Directly supports the steelman beat — this is the figure that shows the
  claimed *combination* (not either filter alone) is the actual system, visually answering "isn't
  this just switching between two known filters" by showing the weighting and classification
  steps sitting between the raw ZCF output and the final decision, not just a simple either/or
  switch. (caption_role: body_figure_carries_unique_info — medium-to-long caption walking the
  reader through the MF branch, the ZCF+weighting branch, and the switch-over decision.)

## FIG. 12 — The payoff, cross-talk present

- **Purpose**: Shows the adaptive method's measured performance when cross-talk is present —
  plain MF detection (903, 913) "locks on" to the false target and fails at close range, plain
  ZCF (901, 911) rejects the ghost but loses long range, and the adaptive/hybrid method (905,
  915) tracks the ideal detection line (907) across the full range — grounded in `[0068]`'s
  verbatim performance description.
- **Intended effect**: This is the effect-section payoff — the reader sees, in one chart, the
  exact failure modes described in the steelman beat (MF fooled at close range; ZCF blind at
  long range) and the adaptive method avoiding both. The "before" case (FIG. 11, no cross-talk)
  is described in prose rather than shown, to keep the single figure focused on the cross-talk
  scenario the whole essay is about. (caption_role: body_figure_carries_unique_info — medium
  caption naming the three detection curves and what each one fails at.)

## FIG. 13 — On the same chip

- **Purpose**: Shows the IC device (400) with the SPAD array (401), light source (403), memory
  module (405), peak finding circuit (407), and depth map memory (409) all on one die —
  supporting `[0069]`'s anchor that the peak-finding circuit performs on-chip processing,
  eliminating the off-chip processor the specification frames as the conventional approach.
- **Intended effect**: Grounds the product-meaning closer — this is not a lab technique running
  on an external computer, it is a block sitting on the same chip as the sensor itself, which is
  what makes "calibration-free, single-component module" (the product claim) plausible rather
  than aspirational. (caption_role: body_figure_prose_covers_fully — short identifier-only
  caption, since the prose in 6-product-meaning carries the on-chip-integration point in full.)

<!--
  > Revision note — triggered by [step 9, figure mapping] [2026-07-01]: FIG. 6 was initially
  drafted with a purpose statement that overlapped heavily with FIG. 9's (both described as
  "showing the classification"). Revised so FIG. 6's purpose is scoped to "both filters see the
  same ghost, before classification" and FIG. 9's purpose is scoped to "the classification
  itself" — avoiding a redundant pair of figure rationales that would otherwise blur the
  mechanism section's own problem-then-test structure.
-->
