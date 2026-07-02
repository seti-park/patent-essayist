# Essay context — US 2024-0192337 B2 (VL53L9CX series, Article 2 of 3 — "Robustness")

Framing brief for the patent-essay pipeline. Read by Phase 1 (thesis grounding + context
research) and carried through Phase 2/3. Source: series brief + this-episode brief supplied by
the author (translated/condensed into English here; nothing in this file should be treated as
patent text — only `input/patent.md` is the primary source for quotes and anchors).

## Series identity and this episode's place

This essay is **Article 2 of a 3-part series** on STMicroelectronics' VL53L9CX dToF 3D LiDAR
module, written for X Articles (long-form). Channel identity: patent-analysis-based
storytelling — the patent itself is the protagonist, not the company. Audience: general readers
between high-school and early-undergraduate level — visual, analogy-driven, oriented around "why
this matters," not patent-prosecution mechanics.

Series arc (one throughline across all 3 articles): **the eye works → the eye can be trusted →
that eye becomes the robot's spatial behavior (toward SLAM).**

| # | Theme | Hero patent | One-line |
|---|---|---|---|
| 1 | Mechanism | US2026-0140238 | How the chip pulls distance out of a streamed photon histogram |
| **2** | **Robustness (this essay)** | **US2024-0192337** | **The cleverness that filters fake targets out of sunlight and glass** |
| 3 | The Bridge | US2023-0356397 | That eye keeps a robot from stepping off a ledge → SLAM |

**This episode's role.** Article 1 establishes the histogram (a per-distance count of returned
laser photons) as the sensor's raw material. Article 2 does not introduce a new raw material —
it reveals that the histogram from Article 1 arrives *contaminated*, and this patent is the
cleaning step. Include one short reminder of what a histogram is, for readers new to the series,
without re-teaching Article 1 in full. Reuse Article 1's own vocabulary for "histogram" — do not
rename it or introduce a competing metaphor for the same concept.

**One-line thesis anchor for this piece:** the cleverness that filters out fake targets even
through sunlight, cover glass, and clutter. Frame the pair as: *Article 1 = reading the
histogram; Article 2 = cleaning the histogram.*

## Hero patent (the spine of this essay)

**US 2024-0192337 B2** — "Cross-talk rejecting convolution peak finding." Filed 2022-12-12.
Inventor: Andreas Assmann. Assignee: STMicroelectronics N.V. Full specification and claims are
in `input/patent.md` (this is the only patent in this run with full source text — treat it as
the primary and only fully-verifiable source of quotes).

- **Verified verbatim anchor (quote exactly, no paraphrase):** "The cross-talk signal in the
  histogram, if not processed properly, may be incorrectly detected as a close target." (`[0029]`)
- **Claim hook:** the cover glass over the sensor reflects part of the outgoing laser pulse
  straight back into the SPAD array. That reflection lands in the histogram as a spurious peak at
  nearly zero distance — a "ghost target" parked right in front of the sensor. The patent's fix:
  a zero-crossing filter (ZCF) plus a set of per-bin weight coefficients that are *negative* for
  the near-sensor bins and positive further out, so the weighted sum for a near-in pulse region
  lands on the wrong side of a threshold and gets classified as cross-talk/noise rather than a
  real target — while a second filter (the matched filter, MF) runs in parallel so a genuine
  far-away target is not thrown out along with the ghost.
- **Problem → solution, one line each:** Problem — cover-glass cross-talk fabricates a false
  near-target inside the histogram. Solution — classify and reject it mathematically, inside the
  same on-chip histogram processing, using weighted zero-crossing pulse regions, with no off-chip
  step required.
- **Product connection (use explicitly, this is the episode's strongest beat):** ST's own public
  marketing for VL53L9CX states that on-chip histogram processing and algorithmic compensation
  remove cover-glass cross-talk and veiling glare (see Product facts below — verify current
  wording via Phase 1 context research and log to `fact-check-log.md`, tiered by source). This
  patent is the concrete mechanism behind that marketing claim — say so plainly: this is "the
  actual patent behind that line in the press release."

## Supporting patent (same beat, deepen only — do not promote to co-hero)

**US 2025-0012901** — "Rising edge adaptive cross-talk correction." Filed 2023-07-07. Inventor:
Andreas Assmann. **Its full specification is not included in this run's uploads** — only the
anchor below was pre-verified by the author against the source. Treat it as a lightly-sourced
secondary reference: quote only the verified anchor verbatim, do not invent additional claim
language or mechanism detail beyond what is given here.

- **Verified verbatim anchor:** "automatically adjusts the amount of cross-talk signal to be
  removed based on the current condition of the cover glass (e.g., scratch, smudge, dirt)"
- **Role:** deepens the same cross-talk beat into reality that changes over time — a scratch, a
  smudge, dust accumulating on the cover glass — i.e., not a fixed factory correction but a live,
  adaptive one. Use only to extend the hero's beat one step further; do not give it its own
  section arc or equal weight to the hero.

## Cluster patents (mention in one line total, no depth — breadth only)

US 2022-0187431 (fingerprint/smudge dynamic correction) · US 2026-0036684 (wraparound: a distant
mirror-like reflector reading as falsely close) · US 2025-0008232 (separating overlapping clutter
targets) · US 2022-0308173 (display/LED flicker stabilization) · US 2024-0426985 (factory
calibration). No source text is available for any of these — do not quote them, do not describe
their mechanisms beyond the one-line gloss above. Purpose: show that robustness has more than one
adversary and ST holds a patent against each — one sentence, not a section.

## Recommended structure (a suggestion Phase 1/2 may adapt, not a rigid template)

1. Hook — why doesn't a ToF sensor get fooled by its own cover glass, or by sunlight?
2. Problem — the cover glass reflects the laser back into the sensor; a ghost wall appears at
   near-zero distance in the histogram.
3. Core claim — land on the verbatim anchor above.
4. Analogy (seed, adapt freely) — like catching your own reflection in a window and learning to
   look past it: the chip recognizes "that peak is my own reflection" and subtracts it, rather
   than mistaking it for something standing right in front of the sensor.
5. Product/meaning — calibration-free operation across varied cover-glass conditions is what
   makes this a shippable, reliable product rather than a lab demonstration.

## Hard requirements (design-intent checks this piece must hold to)

- Hero stays singular: US2024-0192337. The supporting patent appears only as the "adaptive /
  changes over time" extension of the same beat — never split into a second thesis or given a
  parallel section.
- Explicit callback to Article 1's histogram concept, framed as "this is the same histogram — now
  we are cleaning it," reusing Article 1's own vocabulary (no renaming, no competing metaphor).
- Explicitly connect the mechanism to ST's public marketing language about on-chip cross-talk /
  veiling-glare compensation — name plainly that this patent is the substance behind that claim.
- All quoted spans must be verbatim against `input/patent.md` — no paraphrase inside quotation
  marks. Anything quoted from the supporting patent is limited to the one pre-verified anchor
  above.
- No exaggeration: never claim this is the "first" cross-talk-rejection method in the field, and
  never claim STM "solves" cross-talk outright — the claim is that this is STM's specific,
  patented way of doing it. Reserve "first" language for ST's own qualified phrasing about the
  *module* ("first ... in ST's portfolio"), not about this individual patent's technique.

## Caution / nuance to acknowledge (briefly — one clause, not a detour)

- "Cross-talk = cover-glass reflection" is the core analogy for this piece, but the patent's own
  language allows cross-talk to include internal optical leakage too — acknowledge in passing,
  don't build a section on it.
- Veiling glare (light bleed/scatter) belongs to the same correction family in ST's marketing copy
  but is not this patent's own subject — mention it only in the product-connection beat; do not
  analyze it as though this patent covered it.
- Inventor Andreas Assmann is the same inventor as Article 1's hero patent — a legitimate,
  optional "one engineer's throughline" thread across the series if it fits naturally. Do not
  force it in.

## Product facts (VL53L9CX / STEVAL-VL53L9) relevant to this episode

Direct dToF (direct Time-of-Flight) 3D LiDAR all-in-one module; STEVAL-VL53L9 is the evaluation
board; volume production begins early July 2026 (announced 2026-06-22). 2,268 zones (54×42) —
roughly 35x the zone count of the prior VL53L5/L8CX generation (≤64 zones). FoV 54×42°, range
5cm-9m, up to 100fps, accuracy ~1% (TNR — cross-check before quoting a hard number). BSI-stack
SPAD array; 2x VCSEL emitters + BCD driver, 940nm invisible light, Class-1; dual-scan flood
illumination (replaces dot-scan, removing dead zones and improving small-object/edge detection
and motion artifacts). Metasurface optical element (MOE) + physical IR filter. On-chip SoC
performs histogram processing + algorithmic compensation to remove cover-glass cross-talk and
veiling glare — calibration-free. Outputs: depth (3D), 2D IR (active/inactive), reflectance,
confidence — AI-ready for MCU edge AI. First ToF sensor interface with MIPI/I3C (plus I2C).
~150mW at 30fps (cross-check before quoting). Package 12.8×6.1×4.6mm (cross-check before
quoting). Applications include robotics, drones, humanoids, and edge AI.

**ST's own marketing language (reported by the author as verbatim from ST's public press
release / blog, as verified 2026-06-30 — re-verify current wording via Phase 1 context research
before quoting, and log source + tier to `fact-check-log.md`):** "VL53L9 is the first direct
Time-of-Flight (dToF) 3D LiDAR all-in-one module in ST's portfolio." This is a *qualified* first
("in ST's portfolio") — multi-zone dToF already existed via VL53L5/L8; the leap here is
resolution + flood illumination, not the invention of multi-zone dToF itself. Do not state or
imply an unqualified "first."

Items flagged by the author as still needing independent datasheet cross-check (do not present
as settled fact without verification, and prefer to hedge or omit if unverifiable): 940nm
wavelength, BSI "stack" structure detail, VCSEL count + BCD driver detail, ~150mW power figure,
12.8×6.1×4.6mm package size, ~1% (TNR) accuracy figure.

## Figures available

FIG. 1-15, pre-cleaned, in `input/figures/`. Notable: FIG. 2/3 show the histogram with the
cross-talk peak and the real target peak (FIG. 3 recalibrated to the cover-glass "reference
zero-point"); FIG. 4/5 show the ZCF and MF filter shapes; FIG. 6 shows the two filters' output
signals overlaid on the histogram, with the ghost and real pulse regions marked; FIG. 7/8/9 show
the weight-coefficient curves and the weighted-sum computation that performs the actual
rejection; FIG. 10 is the full adaptive-detection flow chart; FIG. 11/12 show measured
performance with and without cross-talk present; FIG. 13/14 show the on-chip integrated-circuit
placement of the peak-finding circuit; FIG. 15 is the claim-level method flow chart.
