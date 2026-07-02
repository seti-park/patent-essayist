# Figures Rationale (Compose placements)

> **Post-acceptance update (human-post-accept, after archiving/meta-loop/push):** SETI asked
> for FIGS. 2-7 to get the same `image-plus-caption` treatment FIG. 1 already had, rather than
> the `caption-only-italic` rendering "folded into body prose" recorded below (which this file
> itself flagged, at the time, as "a deliberate deviation from the caption-only-italic
> default"). All six now have an actual `![FIG. N: ...](figures/fig-0N.png)` embed followed by
> an italic caption paragraph, at the same body locations already chosen below (placement
> unchanged; only the rendering mode changed, from folded-into-prose to image-plus-caption).
> Each caption reuses this file's already-drafted caption text (updated where the self-audit
> corrected it, i.e. FIG. 3's six-line description). The per-figure sections below are kept as
> the historical record of the original placement decision and are otherwise still accurate;
> only their "Rendering" and "Caption (as written)" fields no longer describe the current
> output. See `handoff/03-edit/revision-notes.md` for the delta record.

All 7 figure numbers Phase 1 selected are placed. No pair broken; no figure dropped. This
records Compose's actual placement, which matches Phase 1's `figure-rationale.md` plan with
one refinement: FIG. 4-7 (the flowchart set) is split across two sections instead of stacked
in one, so the adversarial-defense (false-positive) beat gets its own paragraph rather than
trailing the mechanism section as an afterthought.

## FIG. 1 — header (fig-01AB.png + fig-01C.png as one cognitive unit)

- **Placement**: header
- **Rendering**: image-plus-caption (fig-01AB.png embedded; fig-01C.png's content folded into
  the same detailed caption rather than embedded separately, since the caption_role is
  `header_composite` and the two files together are one figure number)
- **caption_role**: header_composite
- **Caption (as written)**: detailed header caption walking FIG. 1A (robot 100 + sensor 102 +
  navigation system 106, fanning into wall tracking / material recognition / cliff detection /
  SLAM), FIG. 1B (IMU 112 + controller 108 + ToF sensor 102 + memory 109), and FIG. 1C (the 8x8
  zone array 114, region of interest 116, first/second/third row 118/120/122, spatial
  separation 124).
- **Bare-token compliance**: a bare "FIG. 1" token appears in the caption itself ("FIG. 1
  makes the geometry itself visible...") is NOT relied on here — see the mechanical gotcha
  compliance note below; the header caption uses "FIG. 1A" / "FIG. 1B" / "FIG. 1C" only, so the
  bare tokens live in body prose (§3, §5), not in this caption.
- **Decision note**: chosen as the top visual hook per Phase 1's plan, unchanged. Establishes
  the single-sensor-multi-function fact and the exact row geometry before the mechanism section
  needs it.

## FIG. 2 — body, after §4 opening (fig-02AB.png + fig-02CD.png as one cognitive unit)

- **Placement**: body-section-4-after-[0046]
- **Rendering**: caption-only-italic (no image embed; both files represent one figure number
  and are described together in prose rather than as two separate caption blocks)
- **caption_role**: body_figure_carries_unique_info
- **Caption (as written)**: folded into body prose rather than a standalone italic caption
  line — "FIG. 2 draws exactly this sequence, the robot's own beam grazing the edge, then
  slipping past it into empty air, across the four distances the essay has been narrating
  stage by stage." This is a deliberate deviation from the caption-only-italic default: the
  four-stage sequence is described in the sentence itself because the analogy section's prose
  already needs to narrate the sequence, and a separate italic caption line would repeat it.
- **Decision note**: placed in §4 (the analogy section) rather than §3 (core-claim), since the
  progressive four-stage approach is the visual backbone of the "one row suddenly reads
  farther" analogy, not the abstract claim statement. This refines Phase 1's figure-rationale.md
  slightly (which associated FIG. 2 with both 3-core-claim and 4-analogy) by giving it a single
  home in the analogy section, where it does the most narrative work.
- **Bare-token compliance**: bare "FIG. 2" token present in this sentence.

## FIG. 3 — body, in §4 (analogy), immediately after FIG. 2

- **Placement**: body-section-4-after-FIG.2
- **Rendering**: caption-only-italic (folded into prose, same treatment as FIG. 2, for the
  same reason: the six-line graph's behavior is the sentence's subject, not a caption
  underneath an embedded image)
- **caption_role**: body_figure_carries_unique_info
- **Caption (as written)**: "FIG. 3's graph is the same event turned into six lines: three
  median-distance lines and three peak-intensity lines, sitting flat and evenly spaced while
  the floor holds, then the peak-intensity lines dropping through the ambient rate one after
  another, then all six lines jumping together the instant the sensor loses the near floor and
  starts reading the far one."
- **Decision note**: per Phase 1's figure-rationale.md, this is "the single best visual for the
  core mechanism" — placed directly after FIG. 2 so the reader sees the schematic event (FIG.
  2) and its instrument readout (FIG. 3) back to back, then the inline-bold thesis anchor
  ("One row suddenly reading much farther...") lands immediately after both.

## FIG. 4 — body, in §5 (three-range check), first of the flowchart set

- **Placement**: body-after-section-5-open
- **Rendering**: caption-only-italic (folded into prose)
- **caption_role**: body_figure_prose_covers_fully
- **Caption (as written)**: "FIG. 4 restates the whole method in three blocks: sense while
  moving [0086], compare the rows and detect an approaching edge, then change the robot's
  propulsion before it reaches that edge."
- **Decision note**: opens the adversarial-defense section (a change in floor material could
  weaken a signal too) with the claim restated as a diagram, then FIGS. 5-7 answer the
  skepticism one range at a time.

## FIG. 5 — body, in §5, long-range test

- **Placement**: body-section-5-after-FIG.4
- **Rendering**: caption-only-italic (folded into prose)
- **caption_role**: body_figure_prose_covers_fully
- **Caption (as written)**: "FIG. 5 makes the long-range test literal. A peak intensity is only
  treated as a cliff signal if it falls below a stated multiple of the measured ambient light
  level, not an arbitrary drop..."
- **Decision note**: grounds the false-positive concern (dark floor vs. real edge) in the
  ambient-relative threshold, per Phase 1's rationale that this figure "reinforces that a
  change in floor material, not a cliff, could produce a similar reading" is exactly the
  concern being pre-empted.

## FIG. 6 — body, in §5, medium-range test

- **Placement**: body-section-5-after-FIG.5
- **Rendering**: caption-only-italic (folded into prose)
- **caption_role**: body_figure_prose_covers_fully
- **Caption (as written)**: "FIG. 6 runs the equivalent check for the medium-range convergence
  test..."
- **Decision note**: kept deliberately brief (one clause) since FIG. 5 already established the
  pattern (a fixed test, not a vague impression) and FIG. 6 is the second instance of the same
  pattern applied to the other metric (median distance vs. peak intensity).

## FIG. 7 — body, in §5, short-range test, closing the section

- **Placement**: body-section-5-after-FIG.6
- **Rendering**: caption-only-italic (folded into prose)
- **caption_role**: body_figure_prose_covers_fully
- **Caption (as written)**: "...and FIG. 7 covers the simplest of the three, whether the ground
  has been lost entirely."
- **Decision note**: closes the three-figure sequence on the most intuitively graspable test,
  matching Phase 1's rationale that "the ground is just gone" pairs naturally with the
  analogy section's framing, even though it is placed in the adversarial-defense section
  rather than immediately beside the analogy.

## Mechanical gotcha compliance (figure-selection.md / phase2-handoff-notes.md §d)

Bare "FIG. 1" and bare "FIG. 2" tokens are both present in body prose, independent of the
lettered captions used elsewhere:

- Bare "FIG. 1": appears at the end of §3 ("FIG. 1 makes the geometry itself visible, before
  any of these three stages even begins.") — three occurrences total in the draft (header
  intro line, prose sentence in §3, and the header caption text itself uses "FIG. 1" as a
  label in the section title too).
- Bare "FIG. 2": appears at the start of the FIG. 2 description in §4 ("FIG. 2 draws exactly
  this sequence...").

Verified against the live (unfixed) `gate_figure_use.py` regex
(`\bfig(?:ure|\.|-)?\s*0*(\d+)\b`) by running the gate script directly against the draft:
all 7 figure numbers register as used, zero orphans, zero off-plan figures.
