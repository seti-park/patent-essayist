# Thesis Trace

## Spine source

- **Spine**: handoff/01-design/thesis-spine.md
- **One-line spine**: The histogram Article 1 taught readers to trust arrives contaminated by
  the sensor's own reflection off its cover glass — US 2024-0192337 B2 is STMicroelectronics'
  specific, patented way of telling that ghost apart from a real target, on-chip, without a
  factory calibration step, and it is the concrete mechanism behind VL53L9CX's on-chip
  cross-talk/veiling-glare marketing claim.
- **Q7 hook**: technical-impossibility (the ghost and the real target are made of the same
  stuff, reflected laser light in the same histogram; resolved by exploiting where the ghost has
  to sit, not by adding an outside reference)

## Section → spine mapping

### 1-hook — "The Chip Learns to Ignore Its Own Reflection in the Glass"

- **Spine element carried**: Q7 technical-impossibility hook + explicit Article 1 histogram
  callback
- **voice_canon_reference**: `opening-reader-experience-llm-date` (window-reflection
  reader-experience entry point), `opening-industry-norm-reversal-xray-tesla` (structural
  cadence for the "same stuff, can't tell apart" framing)
- **paragraph_anchors_used**: `[0003]` (histogram peak = real target, framing only)
- **external_facts_used**: []
- **word_target / word_actual**: 180 / 210

### 2-problem — "The Cover Glass Writes a Fake Target Into the Histogram"

- **Spine element carried**: Axis 2 problem anchor — the cover-glass ghost in the histogram
- **voice_canon_reference**: `inline-bold-thesis-anchor-taillight-hidden-skin` (structural model
  for stating the reveal directly after the visual evidence)
- **paragraph_anchors_used**: `[0029]` (both Quotable spans — mechanism-critical span + the
  "incorrectly detected as a close target" span)
- **external_facts_used**: []
- **word_target / word_actual**: 220 / 245

### 3-mechanism — "The Test That Reads Where the Ghost Has to Sit, Not What It Looks Like"

- **Spine element carried**: Axis 1 claims anchor — ZCF, weighted sum, reference zero-point,
  classification; resolves the Q7 hook explicitly
- **voice_canon_reference**: `inline-bold-thesis-anchor-photon-in-8bit-optimization` (bold
  thesis-anchor placement pattern, applied at "The chip does not need an outside reference...")
- **paragraph_anchors_used**: `[0056]`, `[0055]`, `[0060]`, `[0054]`, `[0052]`
- **external_facts_used**: []
- **word_target / word_actual**: 380 / 460

### 4-steelman — "Two Known Filters, One New Fence"

- **Spine element carried**: Adversarial defense concede-then-refine beat — "isn't this just
  switching filters" objection stated at full strength, then answered via the specific claimed
  combination (weighted classification + switch-over decision module)
- **voice_canon_reference**: contrast-structure signature pattern (voice-profile.md Q22/Q58 —
  "Not X, not Y — Z" / parallel contrast), applied to "not a rebrand of parts that already
  existed"
- **paragraph_anchors_used**: `[0076]`
- **external_facts_used**: []
- **word_target / word_actual**: 260 / 310

### 5-effect — "What the Combination Actually Buys, With and Without the Ghost Present"

- **Spine element carried**: Axis 3 effect anchor — comparative before/after (no cross-talk
  prose case vs cross-talk-present FIG. 12 payoff)
- **voice_canon_reference**: contrast-structure pattern (parallel "with no cross-talk... / add
  cross-talk back in..." construction)
- **paragraph_anchors_used**: `[0067]`, `[0068]` (both Quote anchor table rows)
- **external_facts_used**: []
- **word_target / word_actual**: 260 / 280

### 6-product-meaning — "The Patented Mechanism Behind a Marketing Line"

- **Spine element carried**: Axis 4 baseline-difference + explicit tie to ST's on-chip marketing
  claim + calibration-free secondary beat + supporting-patent deepening + cluster-patent
  one-liner + qualified "first" fact
- **voice_canon_reference**: closing-adjacent product-tie framing (no dedicated canon entry
  category for this beat; followed deliverable-voice-rules citation-interpretation pairing
  instead)
- **paragraph_anchors_used**: `[0027]`, `[0069]`
- **external_facts_used**: `st-onchip-crosstalk-veiling-glare-2026`,
  `vl53l9cx-calibration-free-2026`, `st-vl53l9-first-in-portfolio-2026`,
  `industry-cover-glass-crosstalk-baseline-2026` (implicit, via the cluster-patent one-liner)
- **word_target / word_actual**: 340 / 400

### 7-closing — "Cleaning the Histogram Is What Makes Trusting It Possible"

- **Spine element carried**: thesis recap + forward pointer to Article 3 (SLAM/robot behavior)
- **voice_canon_reference**: `closing-forward-watching-event-etherloop-next-iteration` (forward
  pointer to a concrete next-article event, closing 🤔)
- **paragraph_anchors_used**: []
- **external_facts_used**: []
- **word_target / word_actual**: 140 / 155

## Coverage check

- All 4 axes carried: Axis 1 (claims) -> §3-mechanism, Axis 2 (problem) -> §2-problem, Axis 3
  (effect) -> §5-effect, Axis 4 (baseline-difference) -> §6-product-meaning.
- Q7 hook (technical-impossibility) carried in §1-hook and resolved in §3-mechanism.
- Steelman beat placed directly after the mechanism section (§4), before the product/meaning
  closer (§6), matching thesis-spine.md's explicit placement instruction.
- No out-of-spine claims introduced; no section given to the supporting patent or cluster
  patents beyond the one-paragraph / one-sentence allotment phase2-handoff-notes.md specifies.
- Every `[dddd]` used traces to an invention-summary.md Quotable span or Quote anchor table row
  (verified string-match, see verification note below).
- Every external fact used traces to a fact-check-log.md Fact ID and appears in # Sources.

## Open-question judgment calls (phase2-handoff-notes.md §(e))

- **FIG. 9 reference numerals in body prose**: kept body prose numeral-light per the stated
  default; captions alone carry 611, 613, 601W, P_thresh/N_thresh.
- **Andreas Assmann same-inventor thread**: included, one clause in §1-hook ("an STMicroelectronics
  patent from the same inventor, Andreas Assmann, behind Article 1's mechanism") — a natural
  opening presented itself while establishing the Article 1 handoff, so it was included per the
  default's own "unless a natural opening presents itself" carve-out, not forced as a separate beat.
- **Qualified "first...in ST's portfolio" fact**: included once in §6-product-meaning, in its
  fully qualified form, immediately followed by an explicit clause holding it apart from this
  patent's own technique ("That claim is about the module, not this technique"), matching the
  default's condition that it strengthen the section without extra hedging overhead.
- **Title pattern**: chose declarative-reversal-adjacent phrasing ("The Chip Learns to Ignore
  Its Own Reflection in the Glass") built on the technical-impossibility hook rather than a
  direct-question title, per x-articles-format-en.md's Pattern 2 mapping
  (technical-impossibility -> aphoristic catch + technical context); 11 words, no em-dash.

## Verbatim citation verification note

A post-compose string-match pass confirmed every double-quoted span in essay-draft.md
attributed to the patent (all twelve `[dddd]`-anchored quotes) matches its
invention-summary.md Quotable span / Quote anchor table row exactly, including capitalization
(one initial-capitalization mismatch on the `[0029]` "The cross-talk signal..." span was caught
and corrected to match the source verbatim). Non-anchored quoted phrases in the draft (the
patent title, the essay's own short descriptive phrases like "reference zero-point," and
fact-check-log-sourced Sources titles) are not presented as `[dddd]`-cited patent quotes and are
not subject to this check.
