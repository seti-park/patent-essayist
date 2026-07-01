# Phase 2 Handoff Notes

## (a) Audience reframe decision

Audience is set by `essay-context.md`, not reframed by Phase 1: general tech-curious reader, roughly high-school-to-early-undergrad literacy, visual- and analogy-driven, oriented around "why this matters" rather than a specialist/investor audience. This is Article 1 of a 3-part series (this article = "the eye *works*" / mechanism); Articles 2–3 are out of scope for this run but will reuse this article's vocabulary and hero patent as continuity — so definitions must be written to be **reusable**, not article-1-specific throwaway phrasing.

No further reframe applied. The technical-impossibility Q7 hook (locked in `thesis-spine.md`) IS the audience-appropriate entry point essay-context.md already specifies (§"Recommended structure" layers 1–2) — Phase 1 executed the brief's framing rather than replacing it, per this run's explicit instructions.

**Mandatory vocabulary contract** (series-wide, callback contract — Articles 2/3 will NOT redefine these): this essay must explicitly define **histogram** (bar chart of photon arrival times for one zone), **zone / multi-zone** (grid the field of view is divided into, each cell = its own distance reading), and **peak = distance** (the histogram's tallest bin marks the round-trip time, hence distance). Also unpack **dToF**, **SPAD**, and **TDC** in plain language on first use. Write these definitions generically enough to still read naturally when Article 2 (robustness) and Article 3 (SLAM bridge) reference them without re-explaining.

## (b) Citation priority mapping

| Quotable span | Primary section | Role |
|---|---|---|
| Abstract q-abstract-1 ("sequential bin-by-bin histogram processing") | 3-core-claim | the verbatim anchor essay-context.md names explicitly — quote exactly, no paraphrase, this is the load-bearing claim quote |
| `[0013]` (memory banks prohibitive) | 2-problem → 4-analogy bridge | problem framing — sets up why "hold the whole histogram in memory" is the thing to avoid |
| `[0041]` ("operates without dedicated RAM") | 4-analogy | effect anchor — the plain-language payoff of the mechanism |
| `[0080]` ("processed one bin at a time... state machine that maintains minimal internal buffers") | 3-core-claim → 4-analogy | mechanism-critical — the sentence the "read each bar the instant it arrives" analogy is built from |
| `[0101]`/`[0103]` (256 bytes → 19 bytes) | 4-analogy or 5-product-stakes | quantitative payoff — a concrete, small, intuitive number for a general reader (unlike the more abstract bin-count/buffer-depth figures) |
| aux-patent anchor ("each bin of the histogram representing a photon count corresponding to a distance from a light-ranging system") | 2-problem (principle scaffold beat) | ONE supporting appearance only — establishes "sweep left to right, the peak that rises then falls is the distance" as the baseline principle before the hero's efficient implementation. Do not reuse elsewhere; do not expand. |
| VL53L9CX product facts (2,268 zones, 100 fps, on-chip) | 5-product-stakes | Axis 4 payoff — makes the "why does this matter" landing concrete and current |

## (c) Framing trace (rejected candidates)

- Candidate 2 ("The engineer's fingerprint across two ST patents") rejected: Axis 4 (the inter-patent baseline-difference this candidate's own thesis needed) only 1/4 anchored — the auxiliary patent's filing date could not be independently verified this session (see `search-log.md` query 6), and essay-context.md forbids inventing any detail about the auxiliary patent beyond its one pre-cleared quote. Making the two-patent pairing the *spine* also directly conflicts with essay-context.md's design-intent constraint that the auxiliary patent get one supporting beat only, never compete with the hero for attention. **Phase 2 must NOT** restructure the essay around a "first he patented the principle, then the engine" narrative arc — the inventor-overlap (Andreas Assmann on both patents) may appear as a light, optional aside near the principle-scaffold beat (§2), exactly as essay-context.md allows ("not a forced device"), but must not become the essay's organizing device.

## (d) Traps to avoid

- **Auxiliary patent discipline (hard constraint)**: quote ONLY "each bin of the histogram representing a photon count corresponding to a distance from a light-ranging system" from US 2023/0296739. Do not invent, paraphrase-as-quote, or attribute any other sentence, paragraph number, or claim detail to it. One appearance, in the principle-scaffold beat (§2), not a parallel deep-dive.
- **Cluster-patent discipline (hard constraint)**: the five cluster patents listed in essay-context.md (US 2021/0302550, US 2020/0400792, US 2018/0253404, US 2024/0353538, US 2019/0109977) get one-line mentions at most, as a single breadth-signaling aside — never a verbatim quote, never individual deep-dives. Do not let this list sprawl into a survey.
- **No purple-depth-map figure**: the hook's "purple depth-map demo" is a conceptual/prose-only reference — there is no image asset for it (only 7 numbered figures exist: FIG. 1–7). Do not cite it as a numbered figure, do not invent a caption for it. Describe it in prose in §1, then transition into the real FIG. 1 diagram.
- **FIG. 3–7 are excluded on purpose, not orphaned**: do not reopen the figure-selection decision to add FIG. 4 or FIG. 6 back in for "more visual variety" — their circuit-diagram density exceeds this audience's floor. Their structural content (crosstalk compactness, dual peak-finding, median-phase interpolation) may be referenced in prose from `invention-summary.md` Layer 2 without needing the image.
- **Don't let the patent become the product**: per the adversarial defense's mitigation, state the VL53L9CX connection as "the kind of engineering that makes a chip like this possible," timing-consistent (filing 2024-11-19, product announced 2026-06-22 — about 19 months later) but not a proven one-to-one implementation identity. STMicroelectronics does not publish a patent-to-silicon mapping — the essay's product/stakes section (§5) must concede this explicitly (the steelman beat locked in `thesis-spine.md`) before making the timing-consistency argument, not skip past it.
- **Anti-overclaim guards from essay-context.md** (carry forward verbatim as drafting constraints):
  - Do NOT say the system "directly measures the speed of light" or "times light directly" — it measures photon-arrival statistics via a histogram, not a literal stopwatch on a photon.
  - Do NOT confuse this with iToF (indirect, phase-based ToF) — this is **direct** (d)ToF.
  - "First" claims only in ST's own qualified phrasing — "first direct Time-of-Flight (dToF) 3D LiDAR all-in-one module **in ST's portfolio**" (qualifier intact) — never an unqualified "world's first" or "first multi-zone dToF sensor" (multi-zone dToF already existed in VL53L5/L8CX; the jump here is resolution + flood illumination, not the category).
  - SLAM/robotics framing is Article 3's territory — if it comes up at all in the closing gesture, keep ST's role as supplying senses/inputs, not "solving" navigation.
  - Keep the ~150 mW power figure's fps qualifier hedged (see `fact-check-log.md` vl53l9cx-power-draw note) — this session's independent search corroborated "~150 mW typical" but did not re-confirm the "(at 30 fps)" qualifier specifically.
  - Keep "~35x" as an approximation (2,268 / 64 ≈ 35.4), not an ST-stated figure.
- **Em-dash discipline**: em dash is banned in essay body prose (deliverable voice rule); patent verbatim quotes preserve their original em dashes if present (patent-quote verbatim discipline is a separate rule from body-prose style — see `quote-anchor-conventions.md`).
- **Verbatim discipline reminder**: every `[xxxx]`-cited quote must string-match `invention-summary.md`'s Quotable spans / Quote anchor table exactly (post-allowed-normalization only) — Phase 3 Edit Pass 3 verifies this mechanically.

## (e) Open questions for Phase 2 (awaiting SETI)

None blocking — this run is fully autonomous (strict-execution mode per essay-context.md) with no live checkpoint. Two non-blocking notes for Phase 2's judgment:

- The inventor-overlap aside (Andreas Assmann on both hero and auxiliary patent) is optional per essay-context.md ("a light... thread is fine as an optional connective touch, not a forced device"). Phase 2 may include or omit it in §2 at compose-time discretion; if included, keep it to one sentence.
- Whether to state the `[0101]`/`[0103]` "256 bytes → 19 bytes" figure in the 4-analogy section or hold it for the 5-product-stakes payoff is a compose-time pacing call — both are pre-approved locations per the citation priority mapping above; default to 4-analogy (it's a mechanism-scale number, not a product-scale number) unless the draft's pacing needs a stronger number to close §5.

<!-- No feedback-loop cascade this run: this file was written once, after all upstream
     Phase 1 steps stabilized (no >2 revisions of any single file triggered by this step). -->
