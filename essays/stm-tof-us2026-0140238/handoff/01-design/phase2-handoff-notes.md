# Phase 2 handoff notes

Concise notes for the composer. Voice-ON phase. Target ~1,000-1,300 words of body, lighter and
friendlier than a specialist piece. Audience: general curious readers, high-school to
undergraduate. Posture: measured / accurate-but-friendly. The patent is the protagonist; this is
the **Mechanism** article (Part 1 of a 3-part series), NOT an investor/moat piece.

## (a) Audience reframe decision

This is the English X-Articles long-form version of a piece first drafted in Korean. Keep the
design intent (5-layer Mechanism); render finished English. No reframe of the angle — Mechanism is
locked by the brief. Do not reframe toward diligence/moat.

## (b) The 5-layer plan (which anchors anchor which layer)

1. **Problem** — light too fast to time directly (~3.3 ns/m one-way), a return is only a few
   photons, so distance comes from photon statistics (a histogram), not a stopwatch. Gloss dToF,
   iToF, SPAD, TDC on first use. Anchors: hero `[0003]` (dToF vs iToF), `[0004]` (histogram of
   arrival times); support `[0002]` (bins from photon-detection events), support `[0005]` (TDC);
   hero `[0008]` (VCSEL + SPAD + time difference = distance).
2. **Core claim, quoted verbatim** — land the hero representative claim as a blockquote + attribution.
   Anchors: hero VERBATIM ANCHOR + `[0015]`; the support VERBATIM ANCHOR + support `[0003]` as the
   underlying principle (named in prose).
3. **Mechanism, by analogy** — histogram streamed one bin at a time, peak found on the fly, almost
   no memory held. DEFINE the callback vocabulary here. Anchors: hero `[0042]` (streaming, minimal
   memory), `[0069]` (single pass), `[0016]` (maintain state of recent bins = claim 11); support
   `[0004]` (single-pass peak finding, named in prose).
4. **Product connection** — lean on-chip processing is what lets a fingernail-sized module run
   2,268 zones (54x42) at up to 100 fps in a battery-friendly budget. Anchors: hero `[0013]`,
   `[0042]` + ST facts F1-F5 (fact-check-log.md, attributed to ST).
5. **Why it matters** — this is the grammar the whole series is built on; one-sentence seam into
   Part 2 (sunlight/glass make fake peaks). Synthesis; no new anchors required.

## (c) The two VERBATIM quotes + attribution lines

Quote both EXACTLY as blockquotes, each followed by an attribution line naming the patent
(and paragraph/claim), as in the reference deliverable. These are the only two verbatim quotes the
piece needs.

- **Hero** (Layer 2): `processes time-of-flight measurement data using sequential bin-by-bin
  histogram processing`
  - Attribution: US 2026/0140238 A1, "Ultra-Lean Time-of-Flight Histogram Processing"
    (Abstract; representative claim 1). Inline anchor `[0015]` may accompany the claim-1 wording.
- **Support** (Layer 2 or 3, as the underlying principle): `each bin of the histogram representing
  a photon count corresponding to a distance from a light-ranging system`
  - Attribution: US 2023/0296739 B2, "Methods and devices for identifying peaks in histograms"
    (paragraph [0003]). Name the patent in prose; this is support material.

## (d) Cluster one-liner (content for one sentence only)

A string of adjacent ST filings each cover one step of the pipeline — a TDC building the histogram
bins (US 2021/0302550), summing several SPAD outputs into a bin (US 2020/0400792), extracting
distance from a histogram (US 2018/0253404), sharpening distance with rising-edge super-resolution
(US 2024/0353538), and assembling the 2,268-zone array (US 2019/0109977). ONE sentence only; the
hero stays the focus. (These go in Sources under Patents if cited.)

## (e) Optional inventor thread (one sentence, optional)

Andreas Assmann (spelled Aßmann on the 2022 filing) is a co-inventor on both patents: the 2022
single-pass peak-finding principle (support) and the 2024 ultra-lean on-chip implementation (hero).
Usable as a single "same engineer: the principle, then the on-chip landing" sentence if it earns
its place. Not the spine; at most one sentence.

## (f) Claim-scope traps Phase 2 must avoid

- Claim 1 (representative) requires ONLY: light emitter + detector array + a histogram processing
  circuit that does "sequential bin-by-bin histogram processing" with "on-the-fly operations".
  Do NOT present the correlator, MAC circuits, SNR/closest/strongest peak-finding, crosstalk byte
  counts, or the phase/bin circuit as required by claim 1 — they are dependent/description (Open).
- The "19 bytes vs 256 bytes", "five-element buffer", and range-mode numbers are pinned example
  values (`[0101]`/`[0103]`/`[0113]`/`[0107]`), not claim limits or product specs. Attribute, do
  not generalize.
- Credit the *mechanism* (streaming, single pass, minimal memory) to the patent; credit the
  *product numbers* (zones, fps, power) to ST as external facts. Keep the two channels distinct.

## (g) Anti-exaggeration (hard — repeat of brief)

- Do NOT say the sensor "measures the speed of light directly" — it recovers distance from photon
  statistics (a histogram).
- "First" only as ST's qualified "first dToF 3D LiDAR all-in-one module in ST's portfolio"; NOT the
  absolute first dToF (VL53L5/L8 existed). The leap is resolution + flood illumination.
- Do NOT claim STM "solves SLAM"; the sensor supplies sense/legs, navigation is Part 3.
- Keep power qualitative (`[0013]`, `[0042]`); no milliwatt number.
- Do NOT assert any NON-assertable datasheet figure (940 nm, BSI stacked, dual-VCSEL+BCD, ~150 mW,
  package size, ~1% TNR). "A small infrared laser" is the safe phrasing for the light source.

## (h) Gate constraints (the draft is gate-checked before edit)

- **No figure references** of any kind ("Fig. 3" / "Figure 3") and no embedded images — figures-
  index is empty; a figure ref hard-fails. The mechanism is prose-only.
- **Inline anchors**: 4-digit form only, e.g. `[0042]`. EVERY `[dddd]` token used must be in the
  invention-summary allow-list (`[0002] [0003] [0004] [0006] [0008] [0013] [0014] [0015] [0016]
  [0042] [0069]` for the hero, plus support `[0002] [0003] [0004] [0005]`). Do not invent anchors.
  Attach inline anchors to hero-patent facts; name the patent in prose for support-patent material.
  (Caution: support and hero both have [0002]-[0006]; the gate cannot tell them apart, so attribute
  in prose so the reader is never misled about which patent a number points to.)
- **Each verbatim quote** = a blockquote followed by an attribution line naming the patent (and
  paragraph/claim).
- **No em dashes.** **No Latin abbreviations** (write "for example", "that is", "and so on").
  **No exclamation marks.** **No banned AI words.** **No reader-instruction / essay-self-reference
  phrasings** ("in this article", "let's look", "as we will see") — open straight into the material.
- **Sources**: a single `# Sources` h1 at the end; entries subgrouped under the 5-label enum
  (Patents, Papers, Official statements, News & media, Technical specs); all-or-nothing subgrouping.
  - Patents: hero US 2026/0140238 A1, support US 2023/0296739 B2, plus the five cluster filings (if
    cited).
  - Official statements: ST newsroom press release (VL53L9, p4783); ST blog (blog.st.com/vl53l9).
  - Technical specs: ST databrief DB5805 (Rev 2) — FoV/range/fps/interface framing only.
- **Length**: ~1,000-1,300 words of body.

## (i) Open questions for Phase 2

- None blocking. Posture is measured; the angle is Mechanism. If the inventor thread or cluster
  sentence crowds the mechanism, cut it — the hero mechanism is the priority. Keep exactly the two
  verbatim quotes.
