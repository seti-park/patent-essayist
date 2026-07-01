# Figures Rationale (Compose placements)

Actual placement decisions as executed in `essay-draft.md`. Selection set matches
`handoff/01-design/figure-selection.md`'s "Selected figures" table exactly (FIG. 1, 3, 6, 9,
10, 12, 13); no figure outside that table was added, and none of the six figures that table's
own rejection notes discuss (FIG. 2, 7, 8, 11, 14, 15) were reopened, per
`phase2-handoff-notes.md`'s instruction that those pair-breaks are intentional and closed.

## FIG. 1 — header

- **Placement**: header
- **Rendering**: image-plus-caption
- **caption_role**: header_composite
- **Caption (as written)**: detailed header caption naming the VCSEL emitter (103), SPAD array
  (101), TDCs (107), and the histogram (109) output, framed explicitly as "the same architecture
  Article 1 introduced" — the required Article 1 histogram callback anchor.
- **Decision note**: matches figure-selection.md's stated purpose exactly (shared-vocabulary
  anchor with Article 1, grounding the reader before the essay complicates the picture).

## FIG. 3 — body, in §2-problem, after `[0029]`

- **Placement**: body-section-2-after-[0029]
- **Rendering**: caption-only-italic
- **caption_role**: body_figure_carries_unique_info
- **Caption (as written)**: `*FIG. 3: the histogram recalibrated so the cover-glass reflection
  sits at the "reference zero-point." Peak 201 is the ghost; peak 203 is the real target
  further down the range. Nothing about the shape of either peak announces which one is
  which.*`
- **Decision note**: the essay's single most load-bearing "problem" image, per
  figure-rationale.md's intent — placed immediately after the `[0029]` cross-talk quote so the
  reader sees the two peaks (201 cross-talk, 203 real target) right as the concept is named.
  FIG. 2 (the same histogram before recalibration) was deliberately not placed alongside it —
  this is the intentional pair-break figure-selection.md documents, not an oversight.

## FIG. 6 — body, in §3-mechanism, before the classification step

- **Placement**: body-section-3-after-structural-setup
- **Rendering**: caption-only-italic
- **caption_role**: body_figure_carries_unique_info
- **Caption (as written)**: `*FIG. 6: the matched filter (603) and zero-crossing filter (601)
  outputs overlaid on the histogram. Both filters flag the same two candidate peaks, 611 near
  zero and 613 further out. Neither filter alone can tell which one is real.*`
- **Decision note**: placed to set up the classification problem before FIG. 9 resolves it,
  exactly as figure-rationale.md intended ("both filters see the same ghost, before
  classification"). Kept intact with FIG. 9 as the one progressive-sequence pair not broken.

## FIG. 9 — body, in §3-mechanism, at the classification payoff

- **Placement**: body-section-3-after-[0052]
- **Rendering**: caption-only-italic
- **caption_role**: body_figure_carries_unique_info
- **Caption (as written)**: `*FIG. 9: the weighted ZCF curve (601W) against the P_thresh /
  N_thresh classification band. The near-zero peak lands below N_thresh and is discarded as
  cross-talk; the real target clears P_thresh and survives as a validated candidate.*`
- **Decision note**: the payoff figure for the mechanism section, placed right after the
  weighted-sum mechanism is explained in prose, directly resolving the Q7 hook
  ("how does the chip tell them apart without an outside reference"). Body prose stays
  numeral-light per phase2-handoff-notes.md §(e) default; the caption alone carries 611, 613,
  601W, P_thresh/N_thresh.

## FIG. 10 — body, in §4-steelman, at the combination reveal

- **Placement**: body-section-4-after-combination-claim
- **Rendering**: caption-only-italic
- **caption_role**: body_figure_carries_unique_info
- **Caption (as written)**: `*FIG. 10: the full adaptive-detection flow. Histogram (801) into
  weight-coefficient generation (807, 809) and the ZCF/MF paths (811, 803) in parallel; target
  classification (817) and the switch-over criteria (821) sit between the raw filter outputs
  and the final valid-target list (825), the combination this patent claims.*`
- **Decision note**: placed at the exact point the steelman beat identifies the specific claimed
  combination as the answer to "isn't this just switching between two known filters" — matches
  figure-rationale.md's stated intent precisely.

## FIG. 12 — body, in §5-effect, at the comparative payoff

- **Placement**: body-section-5-after-[0068]
- **Rendering**: caption-only-italic
- **caption_role**: body_figure_carries_unique_info
- **Caption (as written)**: `*FIG. 12: measured performance with cross-talk present. Plain MF
  (903) locks onto the false near-zero target; plain ZCF (901) rejects the ghost but loses range
  beyond about a meter; the adaptive method (905) tracks the true depth line (907) across the
  full measured range.*`
- **Decision note**: the "before" case (FIG. 11, no cross-talk) is carried entirely in prose via
  the `[0067]` anchor, exactly as figure-selection.md specifies — this is the intentional
  pair-break, keeping the single visual budget on the cross-talk-present scenario the whole
  essay is about.

## FIG. 13 — body, in §6-product-meaning, at the on-chip claim

- **Placement**: body-section-6-after-[0069]
- **Rendering**: caption-only-italic
- **caption_role**: body_figure_prose_covers_fully
- **Caption (as written)**: `*FIG. 13: the peak-finding circuit (407) on the same IC device (400)
  as the SPAD array (401) and emitter (403), with the resulting depth map (409) staying
  on-chip.*`
- **Decision note**: short identifier-only caption per `body_figure_prose_covers_fully` (the
  surrounding prose already carries the on-chip-integration analytical content in full, matching
  figure-rationale.md's stated caption_role exactly).

## Figures reviewed and NOT placed (intentional, per figure-selection.md)

- **FIG. 2** — paired precursor to FIG. 3; dropped, FIG. 3 alone carries the load-bearing
  recalibrated "reference zero-point" concept.
- **FIG. 7 / FIG. 8** — weight-coefficient curve families; concept carried instead by FIG. 9's
  weighted-ZCF curve applied to real signal data (more legible for the target audience).
- **FIG. 11** — paired precursor to FIG. 12 (no-cross-talk baseline); carried in prose via
  `[0067]` instead of a second figure, to keep the single payoff figure on the cross-talk-present
  case.
- **FIG. 14** — pixel-level integration variant; FIG. 13's block-level diagram already carries
  the "no off-chip processor" point for this essay's needs.
- **FIG. 15** — claim-1-level flow chart; FIG. 10's fuller adaptive-detection flow chart already
  covers the same ground plus the MF/switch-over context FIG. 15 omits.

## Known gate/artifact note (flagged for the orchestrator)

`_shared/scripts/gate_figure_use.py` parses `figure-selection.md` for any `FIG. N` /
`Figure N` string to build its "selected" set. Because figure-selection.md's own
"Paired-figure relationships (acknowledged)" table and rejection HTML-comment legitimately
discuss FIG. 2, 7, 8, 11, 14, 15 by number (to document why they were NOT selected), the gate's
regex cannot distinguish "selected in the main table" from "named in the rejection rationale,"
and misreads all six as orphaned selections. This draft's figure usage is verified correct
against figure-selection.md's actual "Selected figures" table (the authoritative list); the six
FIGUSE-001 findings this produces are a gate-parsing limitation on the upstream artifact's own
documentation style, not a composition gap. Recommend a future gate fix (e.g., parse only the
"Selected figures" table's own rows, or bound the scan to a fenced/delimited section) rather
than adding the rejected figures back into the draft.
