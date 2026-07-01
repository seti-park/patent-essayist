# Phase 2 Handoff Notes

<!-- essay_id: vl53l9cx-ep2-crosstalk-us20240192337 -->

## (a) Audience reframe decision

Audience held exactly at essay-context.md's default: general readers, high-school to
early-undergraduate level, visual and analogy-driven, oriented around "why this matters" rather
than patent-prosecution mechanics. No reframe. This is Article 2 of 3 in the VL53L9CX series;
readers are assumed to have read (or be able to quickly recall) Article 1's histogram concept,
but the essay must still work for a reader encountering the series here — one short, concrete
reminder of what a histogram is, reusing Article 1's own vocabulary, without re-teaching Article
1 in full (essay-context.md requirement, carried directly into 1-hook).

## (b) Citation priority mapping

| Quotable span / anchor | Primary section | Role |
|---|---|---|
| `[0029]` (both spans — cross-talk definition + "incorrectly detected as a close target") | 2-problem | problem anchor, used first — the essay's core "ghost in the histogram" claim |
| Claim 1 (ZCF → pulse regions → weighted sum → classify → ZCF target list) | 3-mechanism | claims anchor — the backbone of the mechanism section |
| `[0060]` (reference zero-point = SPAD-to-window distance) | 3-mechanism | resolves the Q7 hook — how classification works with no external reference |
| `[0054]` (negative weights penalize the near-sensor region) | 3-mechanism | mechanism support — the "why negative weights near the sensor" explanation |
| `[0055]` / `[0056]` (ZCF loses range / MF is very sensitive to cross-talk) | 4-steelman | sets up the objection at full strength — reserve for the concede half of the steelman beat, do not spend early |
| `[0076]` (q-0076-1, q-0076-2 — ZCF rejects cross-talk / adaptive method gets benefit of both) | 4-steelman, then 5-effect | the refine half of the steelman beat, then reused as the effect-anchor synthesis — do not exhaust in 4-steelman alone |
| `[0067]` (no-cross-talk comparative) | 5-effect | prose-only "before" case (FIG. 11 is not rendered as a figure — see figure-selection.md) |
| `[0068]` (q-0068-1, q-0068-2 — cross-talk-present comparative) | 5-effect | quantitative/comparative payoff, paired with FIG. 12 |
| `[0069]` (on-chip processing reduces I/O complexity) | 6-product-meaning | claims anchor for "no off-chip processor needed," paired with FIG. 13 |
| fact-check-log: `st-onchip-crosstalk-veiling-glare-2026` | 6-product-meaning | the explicit tie to ST's on-chip cross-talk/veiling-glare marketing claim — essay-context.md's strongest required beat; state plainly this patent is "the actual patent behind that line" |
| fact-check-log: `st-vl53l9-first-in-portfolio-2026` | 6-product-meaning (optional) | only usable in its qualified form — "first...in ST's portfolio" — never as an unqualified first; may be omitted if it crowds the section |
| fact-check-log: `vl53l9cx-calibration-free-2026` | 6-product-meaning | secondary beat folded in from rejected Candidate 2 — calibration-free operation as the product-level consequence, not the lead problem |
| Supporting-patent anchor — "automatically adjusts the amount of cross-talk signal to be removed based on the current condition of the cover glass (e.g., scratch, smudge, dirt)" (US 2025-0012901) | 6-product-meaning | deepens the same beat into "changes over time" — do NOT give it its own section arc or equal weight to the hero; one paragraph, same beat |
| Cluster patents (US 2022-0187431, US 2026-0036684, US 2025-0008232, US 2022-0308173, US 2024-0426985) | 6-product-meaning (one sentence) | one-line, no depth, no quotes — "ST holds a patent against each" gloss only |

## (c) Framing trace (rejected candidates)

- Candidate 2 ("the zero-point trick" / calibration-free framing) rejected: its problem anchor
  is only 3/4-strength on its own terms — the patent's own Background of the Invention states
  the problem as cross-talk/false-target detection (`[0029]`), not calibration cost;
  "calibration-free" is a real downstream product consequence, not the specification's own
  stated problem. Using it as the lead would invert the patent's own cause-and-effect and drops
  essay-context.md's required explicit histogram/Article-1 callback. Phase 2 must NOT open the
  essay on "why does every sensor need a calibration step" — that is a secondary beat inside
  6-product-meaning, not the entry-point problem.

## (d) Traps to avoid

- Do not claim STM "solves" cross-talk outright, and do not claim this is the "first"
  cross-talk-rejection method in the field (essay-context.md hard requirement). Reserve "first"
  language strictly for ST's own qualified phrasing about the *module*
  ("first...in ST's portfolio") — never about this patent's technique.
- Do not flatten the mechanism into "the chip switches between two filters" without the
  steelman beat's concede-then-refine treatment — a critical reader's strongest objection is
  precisely that framing (see thesis-spine.md Adversarial defense); the essay must state that
  objection at full strength, then show the specific claimed weighting-plus-switch-over
  combination as the actual novel contribution, not either filter type alone.
- Do not present the FIG. 11/12 comparison, or any patent-derived number, as a single pinned
  percentage or millisecond figure — this patent's own evidence is comparative/curve-based, not
  a headline metric like "~70ms." Do not invent one.
- Do not quote the ~1% (TNR) accuracy figure, the exact wording of the 940nm/150mW/package-size
  specs, or any other essay-context.md-flagged product number as a hard, unhedged fact beyond
  what fact-check-log.md actually supports. The ~1% accuracy figure specifically could not be
  verified this run — omit it rather than assert it (see fact-check-log.md Notes).
- Do not build a section around veiling glare — it belongs to the same ST marketing-copy
  correction family but is NOT this patent's own subject; mention only in passing inside
  6-product-meaning, one clause, not a detour (essay-context.md caution).
- Do not build a section around "cross-talk = cover-glass reflection" as the ONLY form of
  cross-talk — the patent's own `[0029]` language defines cross-talk more generally (any window
  reflection back into the array) before specifically naming cover-glass reflection as the case
  discussed; acknowledge in one clause that internal optical leakage is also cross-talk per the
  patent's definition, do not build a section on it (essay-context.md caution).
- Do not give the supporting patent (US 2025-0012901) its own section arc, its own hook, or
  equal narrative weight to the hero — one paragraph inside 6-product-meaning, quoting only the
  single pre-verified anchor given, no invented mechanism detail.
- Do not rename "histogram" or introduce a competing metaphor for it — reuse Article 1's own
  term exactly, per essay-context.md's explicit instruction.
- Em-dash is banned in essay body prose (deliverable voice, enforced by `gate_emdash`); patent
  verbatim quotes keep their own em-dashes if any exist in the source (none of the anchors
  selected here contain one, so this should not arise, but stay alert if Phase 2 pulls any
  additional anchor not listed here).
- All `[dddd]` anchors used in the essay must trace to a Quotable span or Quote anchor table row
  in `invention-summary.md` — if Phase 2 needs a paragraph not covered here, return to Phase 1
  for extraction rather than re-touching `input/patent.md` directly (patent.md is not in Phase 2
  Knowledge per the pipeline's contract).

## (e) Open questions for Phase 2 (awaiting SETI)

- Whether to name the specific reference numerals (611, 613, 601W, P_thresh/N_thresh) in body
  prose when discussing FIG. 9, or keep the prose numeral-free and let the caption carry them.
  Default: keep body prose numeral-light (reader-friendly), let captions carry the numerals —
  consistent with essay-context.md's audience level.
- Whether the Andreas Assmann "same inventor as Article 1" thread is worth one sentence in
  1-hook or 7-closing. essay-context.md marks this as optional and says "do not force it in."
  Default: leave it out unless a natural opening presents itself in the lead's drafting; do not
  manufacture a beat for it.
- Whether to surface the qualified "first...in ST's portfolio" product fact at all in
  6-product-meaning, given essay-context.md's caution that it's easy to misstate. Default:
  include it once, in its fully qualified form, only if it strengthens the closing without
  requiring extra hedging language that would slow the section down; omit if it does not fit
  cleanly.
- Title pattern: the technical-impossibility hook (FIG. 9's "ghost test") supports either a
  direct-question title or a declarative-reversal title. SETI/Compose to pick at compose time;
  no default lock here.
