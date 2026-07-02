# Thesis Trace

## Spine source

- **Spine**: handoff/01-design/thesis-spine.md
- **One-line spine**: The same row-of-zones histogram comparison that reads a floor as a bar
  chart across a few rows of photon counts is the mechanism this patent reuses to turn one bad
  reading into a robot's decision to stop before it falls, the moment a trustworthy depth map
  becomes robot behavior.
- **Q7 hook**: technical-impossibility (a single distance reading cannot be a decision; the
  patent's resolution is that it is never one reading, it is several rows compared against
  each other)

## Section → spine mapping

### 1-hook — "A Robot Vacuum Reads the Floor Before It Falls"
- **Spine element carried**: Q7 technical-impossibility hook; widens from robot-vacuum framing
  toward the general question, per phase2-handoff-notes.md (a) audience reframe and
  essay-context.md's recommended structure step 1.
- **voice_canon_reference**: `opening-industry-norm-reversal-xray-tesla` (structure: standard
  industry placement stated, "for decades" temporal authority, one-sentence reversal — adapted
  here to "most cliff sensors... for decades... this patent's sensor sits on the front instead")
- **paragraph_anchors_used**: `[0004]`, `[0018]`
- **external_facts_used**: []
- **word_target / word_actual**: 150 / 158

### 2-problem — "A Depth Map Is a Photograph, Not a Warning"
- **Spine element carried**: Axis 2 problem anchor — a depth map is a static snapshot; what
  makes a snapshot become action?
- **voice_canon_reference**: (connective prose; no dedicated voice-canon lookup needed for this
  short transitional section per mode-spec.md's non-mandatory-per-section reading — the
  epistemic-hierarchy tone rules from voice-profile.md apply throughout regardless)
- **paragraph_anchors_used**: `[0018]`
- **external_facts_used**: []
- **word_target / word_actual**: 130 / 121

### 3-core-claim — "The Sensor Compares Rows Against Each Other, Not One Reading"
- **Spine element carried**: Axis 1 claims anchor (verbatim Claim 1 callback, required
  unparaphrased, cited by claim name with no `[dddd]` bracket — see self-audit correction note
  below) + the histogram/multi-zone callback (reconstructed inline per thesis-spine.md's
  adversarial-defense mitigation, framed as "the callback this series has been building
  toward" rather than presupposing prior articles) + three-range mechanism + quantified ranges.
- **voice_canon_reference**: `inline-bold-thesis-anchor-etherloop-steady-state` (X-not-Y
  reframing anchor structure, applied as "The controller is not reading one bar chart. It is
  watching three bar charts drift apart.")
- **paragraph_anchors_used**: `[0035]`, `[0036]`, `[0043]`, `[0050]`, `[0051]`, `[0054]`,
  `[0083]` (plus Claim 1, cited by name, no bracket — see self-audit correction note below)
- **external_facts_used**: []
- **word_target / word_actual**: 320 / 367 (+15%, within ±20% tolerance; the section carries
  the essay's single heaviest citation load and the verbatim-anchor discipline requirement, so
  the wider allowance is intentional per execution-boundary.md's word-target flexibility)

### 4-analogy — "One Row Reading Farther Means the Floor Is Gone There"
- **Spine element carried**: Row-by-row "reading the floor a row at a time" analogy — one row
  suddenly reading farther means the floor is gone there.
- **voice_canon_reference**: `inline-bold-thesis-anchor-taillight-hidden-skin` (two-short-
  sentence parallel reveal structure, applied as "One row suddenly reading much farther than
  the fixed geometry allows is not a data anomaly. It is the floor announcing that it is gone
  there.")
- **paragraph_anchors_used**: `[0045]`, `[0046]`
- **external_facts_used**: []
- **word_target / word_actual**: 180 / 187

### 5-adversarial-defense — "The Three-Range Check Runs a Fixed Test, Not a Vague Impression"
- **Spine element carried**: not a distinct spine element on its own — this section was split
  out of the original 5-layer plan's "meaning/horizon" bucket to give FIGS. 4-7 (the flowchart
  set) and the false-positive concern (floor material vs. real edge) their own beat, rather
  than compressing them into the closing section. This is a Compose-stage structural
  refinement, not a spine deviation: no claim outside the spine is introduced, and the content
  (three-range mechanism's robustness) was already licensed under 3-core-claim's citation
  priority mapping in phase2-handoff-notes.md (b).
- **voice_canon_reference**: (connective/explanatory; mechanism-detail section, epistemic-
  hierarchy tone throughout)
- **paragraph_anchors_used**: `[0082]`, `[0086]`
- **external_facts_used**: []
- **word_target / word_actual**: 130 / 152 (word count predates the self-audit's FIG. 6/7
  accuracy split, logged in revision-notes.md; the split added a paragraph break but no new
  citation)

### 6-meaning-horizon — "The Same Trick Still Runs Under 35 Times More Zones"
- **Spine element carried**: Axis 3 effect anchor (speed/path-optimization payoff) + Axis 4
  baseline-difference (VL53L9CX 2,268-zone / ~35x jump) + secondary patent generalization +
  SLAM horizon gesture (fenced, never "STM solves SLAM") + steelman beat (concede the
  narrow-trick objection at full strength before refining past it, per thesis-spine.md's
  adversarial defense).
- **voice_canon_reference**: `closing-aphoristic-landing-redundancy-steady-state` (negation +
  reframing structure, applied as "STM is not solving SLAM here. It is building one of the
  senses, and a reflex, a SLAM stack needs if it is going to trust the ground under it." —
  wording softened in the self-audit, see revision-notes.md `closing-scope-overreach` delta;
  structure unchanged), `closing-forward-watching-event-etherloop-next-iteration`
  (forward-pointer + open-question close structure)
- **paragraph_anchors_used**: `[0019]`, `[0026]`, `[0036]`
- **external_facts_used**: `st-vl53l9cx-press-release-2026`, `st-vl53l9cx-blog-2026`,
  `secondary-patent-us2022-0184815`, `horizon-cluster-patents-2026`
- **word_target / word_actual**: 260 / 397 (+53% over target — see note below)

**Word-target deviation note (6-meaning-horizon):** this section runs well past the ±20%
tolerance stated in section-blueprint.md. Reasoning for not splitting it further: the section
carries five distinct, individually-required obligations locked by Phase 1 — (1) the effect
anchor, (2) the baseline-difference anchor with its "qualified first" overclaim guard, (3) the
secondary-patent generalization kept deliberately brief so it does not compete with the hero,
(4) the horizon-cluster patents cited as a line/clause each (five of them), and (5) the
steelman concession that must not be skipped. Compressing all five into 260 words risked
turning the steelman beat and the overclaim guard into throwaway clauses, which
phase2-handoff-notes.md (d) explicitly warns against ("do not let this concession get lost or
skipped"). This is flagged here for Phase 3 Edit's awareness rather than silently absorbed;
if Edit's pass-2 (redundancy/compression) finds compressible material, the horizon-cluster
patent list (currently one clause each, five clauses) is the most compressible candidate,
since essay-context.md itself specifies "never expanded into a full case."

**IMU/GNSS caution compliance**: `imu-gnss-caution-us2019-0033466` (US2019-0033466) was
available in fact-check-log.md but is NOT cited anywhere in the draft. Phase 1's caution was
that IF it appears in the horizon paragraph, it must not be treated like the hero or secondary
patent; Compose's judgment call was to omit it entirely rather than include it with a caveat,
since the five horizon-cluster patents already fill that gesture-only role and a sixth caveated
citation risked diluting rather than reinforcing the "these are far-horizon, one-clause-each"
framing.

## Coverage check

- All 4 axes carried: Axis 1 (claims) -> §3, Axis 2 (problem) -> §2, Axis 3 (effect) -> §6,
  Axis 4 (baseline-difference) -> §6.
- Q7 hook (technical-impossibility) carried in §1 and resolved across §3-4.
- Steelman beat (narrow-trick concession) present in §6, stated before the refine-past move,
  per thesis-spine.md's adversarial-defense requirement.
- Verbatim anchor "comparing a statistical distribution of the reflected signals received at a
  plurality of different rows of zones" appears unparaphrased in §3, sourced from Claim 1 as
  granted (cited by claim name, not a `[dddd]` bracket — corrected in the post-acceptance
  self-audit; the quote originally carried an incorrect `[0005]` specification-paragraph tag
  and was missing the claim's own "identifying a convergence..." limitation, see
  revision-notes.md `claim-vs-spec-citation-conflation` delta).
- No out-of-spine claims introduced. The 5-layer plan became 6 sections (the flowchart/
  adversarial-defense material was split out of the horizon section into its own §5) — this is
  a section-count adjustment, not a spine deviation, since section-blueprint.md's "typical
  structure: 4-7 sections... adjust per essay character" explicitly allows this, and every
  spine element still lands in exactly one section.
- Every `[xxxx]` used traces to an invention-summary Quotable span / Quote anchor (verified
  programmatically against invention-summary.md — 16 anchors, zero mismatches).
- Every external fact used traces to a fact-check-log.md Fact ID and appears in `# Sources`.
- No "pending confirmation" fact (940nm, package dimensions, power draw, ~1% accuracy) is
  asserted anywhere in the draft.
- No unqualified "first" claim; ST's "first... in ST's portfolio" phrasing is preserved and
  explicitly flagged in-text as a qualified first.
- "Cliff" is used throughout as drop-off/stair-edge, never a geological cliff.
