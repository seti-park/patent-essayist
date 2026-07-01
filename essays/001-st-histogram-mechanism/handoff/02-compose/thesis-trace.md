# Thesis Trace

## Spine source

- **Spine**: handoff/01-design/thesis-spine.md
- **One-line spine**: STMicroelectronics' ultra-lean histogram patent solves a doubled impossibility — you can't time light with a stopwatch, and you can't process thousands of those photon-count histograms per frame if you have to hold each one fully in memory — by streaming every histogram through dedicated hardware one bin at a time.
- **Q7 hook**: technical-impossibility

## Section → spine mapping

### 1-hook — "Statistics Replaces the Stopwatch"
- **Spine element carried**: Q7 technical-impossibility hook — depth-camera framing (conceptual "purple depth-map demo" rendered in prose, no figure asset) → "how does this get a distance number?"
- **voice_canon_reference**: `opening-reader-experience-llm-date`
- **paragraph_anchors_used**: `[0001]` (technical-field framing only)
- **external_facts_used**: [] (the light-speed figure, ~1 m / ~3.3 ns, is a physical constant stated directly in prose, not a fact-check-log external claim)
- **word_target / word_actual**: 130 / 159

### 2-problem — "Light Is Too Fast to Time, So the Chip Counts Instead"
- **Spine element carried**: first half of the doubled impossibility — statistics (histogram) replaces a literal stopwatch; principle-scaffold beat from the auxiliary patent
- **voice_canon_reference**: `opening-industry-norm-reversal-xray-tesla` (structural echo — "the fix the industry settled on" norm-naming beat, not a full norm-reversal open since this section is mid-essay)
- **paragraph_anchors_used**: [] (dToF/SPAD/TDC definitions are conceptual unpacking, not paragraph-anchored; the auxiliary-patent quote is attributed by patent number in prose, not a `[XXXX]` anchor, per its own non-numbered-paragraph sourcing) — **revision v2 attempted-then-reverted**: edit-log.md's pass-3 low-severity finding asked for a `[0004]` inline anchor on the SPAD/histogram-generation sentence. `[0004]`'s content was verified verbatim against `input/patent.md` directly (paragraph [0004] does support the sentence), and thesis-spine.md's spine→section trace table already designates `[0004]` as this section's primary anchor. However, `[0004]` has **zero occurrences anywhere in `handoff/01-design/invention-summary.md`** (confirmed by direct grep — not in Quotable spans, not in the Quote anchor table) and `gate_anchors.py`'s ANCHOR-001 check hard-fails any `[dddd]` token not present in that file's raw text, with no carve-out for paraphrase-form citations. Per citation-format.md, `invention-summary.md` is the sole source-of-truth Phase 2 is allowed to cite from ("Phase 2 never re-extracts from patent.md"), so adding the anchor was reverted rather than shipping a draft that hard-fails its own deterministic gate. This is a genuine spine-to-invention-summary coverage gap, not a compose-stage error — flagged for Phase 1 to backfill (add a `[0004]` Quotable span to invention-summary.md) and as a meta-loop candidate finding.
- **external_facts_used**: `aux-patent-anchor-only` (one supporting appearance only, per phase2-handoff-notes.md hard constraint)
- **word_target / word_actual**: 190 / 273 (unchanged from v1 — the `[0004]` addition was reverted)

### 3-core-claim — "The Claim Itself Says Bin by Bin, Not All at Once"
- **Spine element carried**: Axis 1 claims anchor, verbatim — sequential bin-by-bin histogram streaming
- **voice_canon_reference**: `inline-bold-thesis-anchor-etherloop-steady-state` (reframing-form inline bold anchor at section turning point)
- **paragraph_anchors_used**: `[0054]`, `[0055]`, `[0069]`, `[0080]` (Claim 1 quoted verbatim in prose; abstract `q-abstract-1` quoted in prose, unbracketed — no 4-digit paragraph number exists for the Abstract in invention-summary.md's Quote anchor table)
- **external_facts_used**: []
- **word_target / word_actual**: 220 / 391 (revision v2: paragraph splits added header-adjacent whitespace only, no content added)

### 4-analogy — "Every Zone Gets Its Own Bar Chart, Read as It Streams"
- **Spine element carried**: Axis 2 problem anchor + Axis 3 effect anchor — every zone's own bar chart; chip reads each bar as it arrives instead of holding the whole chart
- **voice_canon_reference**: `inline-bold-thesis-anchor-photon-in-8bit-optimization` (reframing-form inline bold anchor, "not fully assembled... consumed one bin at a time" turn)
- **paragraph_anchors_used**: `[0054]` (naive-approach callback), `[0101]`, `[0103]`, `[0043]`
- **external_facts_used**: []
- **word_target / word_actual**: 260 / 427 (revision v2: includes the explicit zone=cell bridge insertion, "give every cell in that grid, every zone, its own histogram" (comma-set-off, not em-dash-set-off, per gate_emdash's no-em-dash-outside-quotes rule), closing the pass-5 vocabulary-callback-contract finding)

### 5-product-stakes — "ST Will Not Say Which Patent Built the VL53L9CX, but the Dates Line Up"
- **Spine element carried**: Axis 4 baseline-difference + adversarial mitigation + steelman beat (locked in thesis-spine.md — conceded at full strength before the timing-consistency argument)
- **voice_canon_reference**: `closing-aphoristic-landing-xray-signal` (structural pattern: "X was not Y. It was always Z." reframing landing) + `closing-open-question` category (🤔 close)
- **paragraph_anchors_used**: [] (this section is entirely product/company facts + the steelman/mitigation argument; no new patent claims introduced beyond what §3/§4 already anchored)
- **external_facts_used**: `vl53l9cx-2268-zones`, `vl53l9cx-fov-fps-range`, `vl53l9cx-onchip-processing`, `vl53l9cx-first-in-portfolio`, `vl53l9cx-mass-production-date`, `vl53l5l8cx-64-zone-baseline`, `hero-patent-filing-date`
- **word_target / word_actual**: 240 / 350

## Coverage check

- All 4 axes carried: Axis 1 (claims) → §3, Axis 2 (problem) → §2/§4, Axis 3 (effect) → §4, Axis 4 (baseline-difference) → §5.
- Adversarial defense mitigation + residual risk ("Acknowledged") + steelman beat all land in §5, per thesis-spine.md's explicit instruction that Phase 2 must draft this beat, not omit it — the sentence "STMicroelectronics does not publish which patent maps to which line of silicon, and this patent never names the VL53L9CX" concedes the strongest objection at full strength before the timing-consistency argument follows.
- No out-of-spine claims introduced. The five cluster patents (US 2021/0302550, US 2020/0400792, US 2018/0253404, US 2024/0353538, US 2019/0109977) were NOT used in this draft — the mechanism narrative did not need a breadth-signaling aside to land, and phase2-handoff-notes.md permits omitting rather than forcing it in. The inventor-overlap aside (Andreas Assmann on both hero and auxiliary patent) was also omitted at compose-time discretion (phase2-handoff-notes.md marks both as optional, non-blocking).
- Every `[XXXX]` used (`[0001]`, `[0043]`, `[0054]`, `[0055]`, `[0069]`, `[0080]`, `[0101]`, `[0103]`) traces to an invention-summary.md Quotable span or Quote anchor table row; verified by direct string-match script against invention-summary.md source text (8/8 quote+anchor pairs verbatim-matched).
- **Revision v2 — `[0004]` anchor NOT added (attempted, reverted)**: edit-log.md's pass-3 low-severity finding asked for a `[0004]` inline anchor on §2's SPAD/histogram-generation sentence. `[0004]`'s content was verified verbatim against `input/patent.md` directly and thesis-spine.md's spine→section trace table designates `[0004]` as this section's primary anchor, so the citation was drafted in. `python .claude/skills/_shared/scripts/run_gates.py` then hard-failed it: ANCHOR-001, "citation anchor [0004] not present in invention-summary" — `[0004]` has zero occurrences anywhere in `handoff/01-design/invention-summary.md` (confirmed by direct grep), and citation-format.md establishes that file as Phase 2's sole citable source-of-truth ("Phase 2 never re-extracts from patent.md"). The citation was reverted rather than ship a draft that fails its own deterministic gate. Genuine spine-to-invention-summary coverage gap, not a compose-stage error — flagged for Phase 1 to backfill (add a `[0004]` Quotable span to invention-summary.md) and as a meta-loop candidate finding.
- The abstract quote ("processes time-of-flight measurement data using sequential bin-by-bin histogram processing") and the auxiliary-patent quote ("each bin of the histogram representing a photon count corresponding to a distance from a light-ranging system") are both quoted verbatim in prose but carry no `[XXXX]` bracket, because neither source assigns them a 4-digit paragraph number (Abstract is unnumbered in invention-summary.md; the auxiliary patent's only pre-cleared anchor is likewise unnumbered per fact-check-log.md). Both string-match their source documents exactly.
- Every external fact used traces to a fact-check-log.md Fact ID and appears in `# Sources`.
- Vocabulary contract fulfilled: histogram, zone/multi-zone, and peak=distance are all explicitly defined in this essay (§1/§2/§4), reusable for Article 2/3 callback per essay-context.md. dToF, SPAD, and TDC are unpacked in plain language on first use in §2.
- Anti-overclaim guards from essay-context.md all held: no "times light directly" phrasing (§1 explicitly frames the resolution as counting, not timing); dToF vs iToF distinction stated explicitly (§2); the "first...in ST's portfolio" qualifier kept intact (§5); SLAM/robotics framing was not introduced (out of scope for Article 1, correctly omitted); the ~35x and ~150 mW hedges were respected (~35x stated as "not a precise figure ST states outright but a straightforward ratio"; the ~150 mW figure was not used in this draft at all, avoiding the fps-qualifier risk entirely).
