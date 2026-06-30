# Thesis Trace

## Spine source

- **Spine**: handoff/01-design/thesis-spine.md
- **One-line spine**: The VL53L9CX recovers distance from photon statistics, a per-zone histogram streamed bin by bin where the peak is the distance, and the hero patent (US 2026/0140238 A1) is what makes that processing lean enough to run on-chip, on a fingernail-sized, battery-friendly module.
- **Q7 hook**: technical-impossibility (you cannot start a stopwatch on a few photons travelling at light speed; distance comes from a histogram of arrival times instead).
- **Mode / posture used**: walkthrough / measured.
- **Series role**: Part 1 (Mechanism) of a planned 3-part series; general curious audience, high-school to undergraduate; the patent is the protagonist.

## Section → spine mapping

The five sections preserve the locked 5-layer structure, in order. Section headers are written as claims so a header-only skim reconstructs the mechanism (light is too fast to time -> the claim is one sentence about bins -> a histogram read one bar at a time -> lean math is why it fits on a fingernail -> the grammar the rest of the story is written in).

### 1 — "Light Is Too Fast to Time, So the Sensor Counts Photons Instead"  (Layer 1: Problem)
- **Spine element carried**: Q7 hook (technical-impossibility) + problem framing; gloss dToF / iToF / SPAD / TDC on first use; distance from photon statistics, not a timed beam.
- **voice_canon_reference**: `opening-reader-experience-llm-date` (concrete try-it-yourself scene -> problem essence -> the sensor's answer).
- **paragraph_anchors_used**: `[0004]`, `[0003]` (hero). Support patent material (photon-count bins, the TDC) is glossed in prose; the SPAD/TDC definitions name the parts without a bare support anchor, per house style.
- **external_facts_used**: [] (3.3 ns/m is a physical constant, derivable, not an external claim).
- **word_target / word_actual**: 270 / 268.

### 2 — "The Patent's Claim Is One Sentence About Bins"  (Layer 2: Core claim, verbatim)
- **Spine element carried**: land the hero representative claim; quote the hero VERBATIM anchor as a block quote + attribution line; unpack "bin by bin" in plain words.
- **voice_canon_reference**: `inline-bold-thesis-anchor-photon-in-8bit-optimization` (turning-point reframing; applied at the close of the section to set up the mechanism payoff).
- **paragraph_anchors_used**: `[0015]` (hero) + hero VERBATIM anchor block quote ("processes time-of-flight measurement data using sequential bin-by-bin histogram processing", attributed US 2026/0140238 A1, Abstract and claim 1).
- **external_facts_used**: [].
- **word_target / word_actual**: 160 / 156.

### 3 — "A Histogram Read One Bar at a Time"  (Layer 3: Mechanism by analogy)
- **Spine element carried**: build the histogram picture; DEFINE the callback vocabulary in-line (histogram, zone/multizone, peak = distance); the hero's streaming / single-pass / minimal-memory move; the SUPPORT patent as the underlying principle; cluster one-liner; optional same-engineer thread.
- **voice_canon_reference**: `inline-bold-thesis-anchor-photon-in-8bit-optimization` (the bold "the peak is marked as it streams past" anchor is the single load-bearing bold sentence of the piece).
- **paragraph_anchors_used**: `[0042]`, `[0069]`, `[0016]` (hero). Support VERBATIM anchor block quote ("each bin of the histogram representing a photon count corresponding to a distance from a light-ranging system", attributed US 2023/0296739 B2, paragraph [0003]); support `[0004]` single-pass principle named in prose. (The `[0003]` token in this section is the support-patent attribution line, explicitly named so no reader is misled about which patent it points to.)
- **external_facts_used**: [] inside the filing; the five cluster filings (US 2021/0302550, US 2020/0400792, US 2018/0253404, US 2024/0353538, US 2019/0109977) are named in one sentence and listed under Sources / Patents.
- **word_target / word_actual**: 560 / 575.

### 4 — "Lean Math Is Why the Whole Sensor Fits on a Fingernail"  (Layer 4: Product connection)
- **Spine element carried**: lean on-chip processing is what lets a fingernail-sized all-in-one module run 2,268 zones (54x42) at up to 100 fps over 5 cm to 9 m on a battery-friendly budget, feeding depth / IR / confidence to edge AI; ~35x over the prior <=64-zone generation; ST's qualified "first ... in ST's portfolio"; not the absolute first dToF.
- **voice_canon_reference**: `inline-bold-thesis-anchor-photon-in-8bit-optimization` (reframe: leanness is the enabler, not a limitation — applied as plain prose, no extra bold to keep bold restrained).
- **paragraph_anchors_used**: `[0013]`, `[0042]` (hero — memory prohibitive for compact devices, streaming memory reduction). Power kept qualitative from the patent's own language; no milliwatt figure.
- **external_facts_used**: F1 (2,268 zones / 2.3K / ~35x), F2 (54x42 FoV / 5 cm-9 m / up to 100 fps), F3 (on-chip processing / flood illumination / all-in-one), F5 (edge-AI feed) — all attributed to STMicroelectronics in prose and listed under Sources. NON-assertable datasheet figures (940 nm, BSI stacked, dual-VCSEL+BCD, ~150 mW, package size, ~1% TNR) deliberately omitted.
- **word_target / word_actual**: 260 / 261.

### 5 — "The Grammar the Rest of the Story Is Written In"  (Layer 5: Why it matters)
- **Spine element carried**: this histogram / zone / peak grammar is what the rest of the series stands on; one-sentence seam into Part 2 (sunlight and glass create fake peaks that pollute the histogram; next: learning to trust the distance).
- **voice_canon_reference**: `closing-open-question-finger-cable-next-essay` (series-anchor close: recap, then a single clean hand-off sentence to the next part; the sanctioned closing emoji omitted to hold the measured, general-audience register).
- **paragraph_anchors_used**: [] (synthesis + seam; no new patent claim).
- **external_facts_used**: [] (the production-timeline / sunlight-glass setup is framed as the next chapter, not asserted as a dated fact here).
- **word_target / word_actual**: 140 / 138.

## Coverage check

- All five layers carried in order: Problem -> §1, Core-claim-verbatim -> §2, Mechanism-by-analogy -> §3, Product-connection -> §4, Why-it-matters + seam -> §5.
- Both VERBATIM anchors are block-quoted with an attribution line: hero (US 2026/0140238 A1, Abstract and claim 1) in §2; support (US 2023/0296739 B2, paragraph [0003]) in §3.
- Callback vocabulary defined once, in §3: **histogram**, **zone** (multizone), peak = distance; dToF / iToF / SPAD / TDC glossed on first use in §1.
- Every inline `[dddd]` token used (`[0003] [0004] [0013] [0015] [0016] [0042] [0069]`) is in the invention-summary allow-list; hero facts carry inline anchors, support material is named in prose with its patent number.
- Mechanism / product channels kept distinct: streaming / single-pass / minimal-memory credited to the patent; zone / fps / range / power numbers credited to ST as external facts.
- Body ~1,418 words; deterministic gates pass with zero fail findings (remaining warnings are LONGSENT artifacts from the gate's cross-paragraph sentence joiner plus the brief-mandated single-sentence cluster line).
- No figures referenced; no em dashes; no Latin abbreviations; no exclamation marks; no banned terms; no reader-instruction / meta phrasings.
