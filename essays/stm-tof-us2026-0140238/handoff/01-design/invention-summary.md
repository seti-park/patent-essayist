# Invention Summary

## Metadata

- **Patent ID**: US 2026/0140238 A1 (published application)
- **Title**: Ultra-Lean Time-of-Flight Histogram Processing
- **Filing date**: 2024-11-19 (appl. 18/952,453)
- **Publication date**: 2026 (US 2026/0140238 A1)
- **Inventors**: Donald Baxter, Pascal Mellot, Stuart McLeod, Andreas Assmann
- **Classification**: time-of-flight sensor technology / direct-ToF histogram processing (cover page does not enumerate CPC in the supplied text)
- **Assignee**: STMicroelectronics International N.V.

Support patent (principle only): **US 2023/0296739 B2**, "Methods and devices for identifying
peaks in histograms", filed 2022-03-17 (appl. 17/697,784), inventor Andreas Aßmann, assignee
STMicroelectronics Research & Development Ltd. Andreas Assmann / Aßmann is a co-inventor on both
filings — an optional one-line "same engineer" thread (2022 principle, then the 2024 on-chip
implementation).

## 발명 명칭 / 기술분야

Reader-ready framing: a way to pull distance out of a stream of returning photons while holding
almost nothing in memory — the histogram is walked one bin at a time, the peak is found on the
fly, and the result is computed without ever storing the whole picture, so the work fits on a
tiny battery-powered chip. 기술분야: direct time-of-flight (dToF) sensor signal processing, in
particular ultra-lean on-chip histogram processing for compact, power-constrained devices.

## 종래 문제 / 과제

Light is far too fast to time directly (about 3.3 nanoseconds per metre, one-way) and a single
return is only a handful of photons, so a dToF sensor does not start a stopwatch — it builds a
histogram of photon arrival times and recovers distance from where the photons pile up [0004].
The cost of that approach is memory: conventional ToF systems hold the full histogram, often
several copies, in substantial RAM, which becomes prohibitive in battery-powered or compact
devices [0013]. The patent targets exactly that gap — keep full-histogram processing quality, but
do it without the memory and logic that normally make it impossible to run on-chip [0013][0014].

**Quotable spans:**
- `[0013]`: "conventional time-of-flight systems rely on substantial memory resources to store and process histogram data"
- `[0013]`: "the use of large memory banks becomes prohibitive in applications where power consumption, cost, and size can be critical factors, such as in battery-powered devices or compact mobile electronics"
- `[0004]`: "These systems generate histograms of photon arrival times, which are processed to determine distance information."
- `[0003]`: "Direct ToF systems measure the actual time of light travel, while indirect ToF systems measure phase shifts in modulated light signals."

## 청구항 분석 — 4-layer core mechanism

### Layer 1 — What (one sentence)

A time-of-flight sensor system (light emitter + detector array + histogram processing circuit)
that processes the photon-arrival histogram one bin at a time, in a single streaming pass, doing
its corrections and peak-finding on the fly so it never has to store the whole histogram — which
is what lets full-quality dToF processing run on a tiny, low-power chip [0015][0042][0069].

### Layer 2 — How (mechanism)

1. A light emitter (in the described embodiment a VCSEL, 102) sends short pulses toward the
   target; a detector array (a SPAD array, 106) detects the returning photons [0008][0045][0047].
2. Photon arrivals are sorted by time-of-flight into bins; each bin counts photons at one time
   delay, so the histogram is a distribution of arrival times — and a peak marks a target's
   distance [0004][0114] (claim 9).
3. Instead of accumulating and storing the full histogram, a sequencer presents each bin to the
   hardware one at a time; the circuit processes that bin and asks for the next — bin-serial /
   streaming processing [0042][0080].
4. During that single pass the circuit applies its work "on the fly": crosstalk removal, ambient
   estimation, correlation (matched filter), and peak detection — closest target and strongest
   (highest-SNR) peak [0015][0017] (claim 10).
5. Only a small state is kept — a short buffer of the most-recently-processed bins (for example a
   five-element buffer for zero-crossing detection) — so memory stays tiny [0016][0113] (claim 11).
6. The histogram is iterated serially, computing outputs in a single pass without modifying the
   histogram, which is what collapses the memory and logic footprint [0069].

**Key components**: light emitter / VCSEL (102); return SPAD array (106); histogram processing
circuit (114 / 200); correlator circuit (202 / 400) with ambient, filter, and crosstalk MAC
circuits; phase/bin computation circuit (204 / 600); MCU-as-sequencer (116); small register and
buffer storage in place of dedicated RAM [0041][0043].

### Layer 3 — Why novel

- **Relative to prior art**: conventional dToF either pushes the full histogram off-chip (raising
  I/O complexity and memory cost) or runs on-chip with a large MCU and multiple data sweeps; both
  carry a heavy memory and power burden [0013][0054][0055]. The claimed architecture keeps full
  histogram processing on-chip but in a single streaming pass with minimal memory [0042][0069].
- **Industry practice contrast**: the usual answer to histogram processing is a general-purpose
  microcontroller or DSP with ample RAM holding multiple copies of the data [0007][0013]; the
  patent replaces that with discrete hardware circuits, shared MAC units, and a sequencer, aiming
  at an extremely low gate/logic count [0038].

### Layer 4 — Innovation angles

- **angle-bin-serial-streaming** (the spine): the histogram is processed one bin at a time in a
  single pass, never stored whole, with operations applied on the fly.
  - Evidence paragraphs: `[0015]`, `[0042]`, `[0069]`
  - Quote anchor refs: q-0042-1, q-0069-1
- **angle-memory-collapse**: full-histogram quality without the RAM — the memory footprint is the
  thing that previously kept this off a battery-powered chip.
  - Evidence paragraphs: `[0013]`, `[0042]`, `[0041]`
  - Quote anchor refs: q-0013-1, q-0042-1
- **angle-peak-equals-distance**: a peak in the photon-arrival histogram is a target's distance;
  the circuit finds the closest and strongest peaks on the fly.
  - Evidence paragraphs: `[0004]`, `[0006]`
  - Quote anchor refs: q-0004-1, q-0006-1

## Reference number table

| Number | Label | Paragraphs | Figures |
|---|---|---|---|
| 100 | ToF sensor system | `[0045]` | FIG. 1 |
| 102 | VCSEL (light emitter) | `[0045]`, `[0047]` | FIG. 1 |
| 104 | VCSEL driver | `[0045]`, `[0047]` | FIG. 1 |
| 106 | Return SPAD array (detector) | `[0045]`, `[0047]` | FIG. 1 |
| 108 | Reference SPAD array | `[0045]`, `[0047]` | FIG. 1 |
| 110 / 112 | First / second OR tree | `[0048]` | FIG. 1 |
| 114 / 200 | Histogram processing circuit | `[0049]`, `[0066]` | FIG. 1, 2 |
| 116 | MCU (sequencer) | `[0050]`, `[0043]` | FIG. 1 |
| 202 / 400 | Correlator circuit | `[0066]`, `[0104]` | FIG. 2, 4 |
| 204 / 600 | Phase/bin computation circuit | `[0066]`, `[0173]` | FIG. 2, 6 |
| 402 / 404 / 406 | Ambient / filter / crosstalk MAC | `[0104]`, `[0125]` | FIG. 4 |
| 408 / 410 | Closest target / strongest maximum circuit | `[0104]`, `[0137]` | FIG. 4 |

> Note: figures are listed for completeness of the reference map only. No figures are selected or
> referenced in this article (no cleaned assets this run) — see figure-selection.md.

## Figure relationships

No figures are used in this article. The table below records the source filing's figure structure
for reference only; none of these are referenced in the draft.

| Figure | Paired with | Relationship | Notes |
|---|---|---|---|
| FIG. 1 | (standalone) | system block diagram | the whole sensor; not used in the essay |
| FIG. 2 | FIG. 4, FIG. 6 | top-level circuit ↔ its sub-circuits | not used in the essay |
| FIG. 5 | (standalone) | bin-serial processing flowchart | not used in the essay |
| FIG. 7 | (standalone) | on-the-fly median estimation flowchart | not used in the essay |

## Quote anchor table

Hero patent (US 2026/0140238 A1) unless marked. Verbatim text matches the source exactly
(markdown-bold strip and smart-quote → straight-quote normalizations applied per
quote-anchor-conventions.md).

| Quote ID | Paragraph | Verbatim text | Significance |
|---|---|---|---|
| q-0002-1 | `[0002]` | "ToF systems measure the time light travels from an emitter to an object and back to a sensor, enabling distance measurements and three-dimensional environment mapping." | mechanism-critical |
| q-0003-1 | `[0003]` | "Direct ToF systems measure the actual time of light travel, while indirect ToF systems measure phase shifts in modulated light signals." | mechanism-critical |
| q-0004-1 | `[0004]` | "These systems generate histograms of photon arrival times, which are processed to determine distance information." | mechanism-critical |
| q-0006-1 | `[0006]` | "It involves analyzing collected photon timing data to extract distance information." | mechanism-critical |
| q-0008-1 | `[0008]` | "The time difference between the emission and detection of light pulses is used to calculate the distance to the reflecting object." | mechanism-critical |
| q-0008-2 | `[0008]` | "ToF systems may include a vertical-cavity surface-emitting laser (VCSEL) as a light source, emitting short light pulses." | mechanism-critical |
| q-0013-1 | `[0013]` | "conventional time-of-flight systems rely on substantial memory resources to store and process histogram data" | prior-art-contrast |
| q-0013-2 | `[0013]` | "the use of large memory banks becomes prohibitive in applications where power consumption, cost, and size can be critical factors, such as in battery-powered devices or compact mobile electronics" | prior-art-contrast |
| q-0014-1 | `[0014]` | "ultra-lean histogram processing architectures for time-of-flight sensors" | claim-supporting |
| q-0015-1 | `[0015]` | "process measurement data from the detector array using a sequential bin-by-bin histogram processing, and apply, during the sequential bin-by-bin histogram processing, one or more on-the-fly operations" | claim-supporting |
| q-0042-1 | `[0042]` | "Instead of storing full histograms or multiple copies of processed data, the system employs a bin-serial processing approach. The method allows for the processing of histogram data in a streaming fashion, significantly reducing memory requirements." | mechanism-critical |
| q-0069-1 | `[0069]` | "the histogram processing circuit 200 is advantageously configured to iterate the histogram by serially computing relevant outputs in a single pass" | mechanism-critical |
| q-ABS-1 | Abstract | "processes time-of-flight measurement data using sequential bin-by-bin histogram processing" | claim-supporting (VERBATIM ANCHOR) |
| q-CLM1-1 | claim 1 | "process measurement data from the detector array using a sequential bin-by-bin histogram processing" | claim-supporting (representative claim) |
| q-CLM9-1 | claim 9 | "a value in each bin representing a number of photons detected at the corresponding time delay, wherein the histogram data represents a distribution of photon arrival times from the reflected light pulses" | claim-supporting |
| q-CLM11-1 | claim 11 | "maintaining a state of a predetermined number of most recently processed bins, and generating output data for each bin before proceeding to a subsequent bin" | claim-supporting |
| q-SUP-0002-1 | support `[0002]` | "A photon-count histogram may be generated that group photon-detection events into time ranges referred to as bins." | mechanism-critical (support patent) |
| q-SUP-0003-1 | support `[0003]` | "each bin of the histogram representing a photon count corresponding to a distance from a light-ranging system" | claim-supporting (support VERBATIM ANCHOR) |
| q-SUP-0004-1 | support `[0004]` | "A single-pass method for identifying peaks in a time of flight histogram" | claim-supporting (support patent) |
| q-SUP-0005-1 | support `[0005]` | "a time to digital converter in communication with the optical receiver and configured to output times of flight of photons detected by the optical receiver" | mechanism-critical (support patent) |

## Quotable anchors (gate_anchors allow-list)

This is the allow-list the deterministic `gate_anchors` check enforces: every `[dddd]` token a
draft cites must appear here. Each is a verified real paragraph of the stated source. Be generous
in the draft only within this set; do not cite a paragraph that is not listed.

**Hero patent (US 2026/0140238 A1) anchors:**
- `[0002]` — ToF measures the time light travels emitter → object → sensor, for distance and 3D mapping.
- `[0003]` — direct ToF measures actual travel time; indirect ToF measures phase shift (dToF vs iToF contrast).
- `[0004]` — SPADs detect individual photons; the system builds histograms of photon arrival times, processed for distance.
- `[0006]` — histogram processing analyzes photon timing data to extract distance (noise reduction, peak detection, phase calc).
- `[0008]` — a VCSEL emits short pulses, a SPAD array detects the return, the emit-to-detect time difference gives distance.
- `[0013]` — conventional ToF holds the full histogram, often multiple copies, in substantial RAM; prohibitive for battery / compact devices.
- `[0014]` — the invention is an ultra-lean histogram-processing architecture for ToF sensors.
- `[0015]` — first aspect: process measurement data via sequential bin-by-bin histogram processing, applying on-the-fly operations.
- `[0016]` — method aspect: sequentially process individual bins, maintain a state of the most-recently-processed bins, emit output per bin (claim-11 content).
- `[0042]` — instead of storing full histograms, a bin-serial / streaming approach significantly reduces memory.
- `[0069]` — iterate the histogram serially, computing outputs in a single pass, without modifying the histogram.

Representative-claim content (also recorded so claim citations resolve; cite the patent in prose
for claim language, with inline `[dddd]` only where the same wording appears at a recorded
paragraph — claim 1 ↔ `[0015]`, claim 9 ↔ `[0004]`/`[0016]`, claim 11 ↔ `[0016]`):
- **claim 1** (representative): a ToF sensor system — light emitter + detector array + histogram
  processing circuit — that receives ToF measurement data and "process[es] measurement data from
  the detector array using a sequential bin-by-bin histogram processing", applying "one or more
  on-the-fly operations" during that processing. (Same wording appears verbatim at `[0015]`.)
- **claim 9**: the histogram data is a plurality of bins, each bin a time delay, each value a
  photon count, "wherein the histogram data represents a distribution of photon arrival times from
  the reflected light pulses." (Same wording at `[0004]` for the arrival-times point, and the
  full bin/value phrasing recurs at `[0016]`-adjacent description and `[0236]`.)
- **claim 11**: a method — emit, detect, receive ToF data, "processing the time-of-flight
  measurement data using sequential bin-by-bin histogram processing, wherein the sequential
  bin-by-bin histogram processing comprises sequentially processing individual bins of a
  histogram, maintaining a state of a predetermined number of most recently processed bins, and
  generating output data for each bin before proceeding to a subsequent bin". (Same wording
  verbatim at `[0016]`.)

**Supporting patent (US 2023/0296739) anchors:**
- support `[0002]` — LiDAR/ToF determines distance from photon travel time; a photon-count
  histogram groups photon-detection events into time-range bins; peaks identify objects at distances.
- support `[0003]` — the single-pass method: ordered bin-by-bin comparison against an adaptive
  threshold, "each bin of the histogram representing a photon count corresponding to a distance
  from a light-ranging system"; mark a peak between the rising-above and falling-below bins.
- support `[0004]` — "A single-pass method for identifying peaks in a time of flight histogram":
  enable peak tracking on rising above threshold, mark the peak when it falls back below.
- support `[0005]` — a light-ranging system: optical source, optical receiver, a time-to-digital
  converter (TDC) outputting times of flight, and a processor storing them in a ToF histogram.

> Citation note for Phase 2: support-patent paragraphs are recorded in this allow-list so a `[dddd]`
> token resolves if used, but per house style the support patent should be named in prose
> ("US 2023/0296739 ... [0003]") rather than carried by a bare inline anchor. Inline `[dddd]`
> anchors are best reserved for hero-patent facts. Note the support patent shares the [0002]-[0006]
> range with the hero patent; the gate only checks the 4-digit token, so it cannot tell them apart —
> attribute correctly in prose so a reader is never misled about which patent a number points to.

## VERBATIM anchors (quote exactly — do not paraphrase)

Both confirmed as exact substrings of their sources.

- **Hero** (Abstract; representative claim 1): `processes time-of-flight measurement data using
  sequential bin-by-bin histogram processing` — source: hero Abstract (line 20) and claim 1.
  Attribution line for Phase 2: name US 2026/0140238 A1, Abstract / claim 1.
- **Support** (paragraph [0003]): `each bin of the histogram representing a photon count
  corresponding to a distance from a light-ranging system` — source: support `[0003]` (and
  recurring at support `[0005]`, `[0111]`, `[0115]`). Attribution line for Phase 2: name
  US 2023/0296739 B2, paragraph [0003].

## Claim-scope note (what claim 1 requires vs. optional detail)

Phase 2 must not over-credit the claim. The representative claim is deliberately broad.

| Layer | Content |
|---|---|
| **Locked (independent claim 1 requires)** | Only three things: (a) a light emitter that emits pulses toward a target; (b) a detector array that detects the reflected pulses; (c) a histogram processing circuit that receives the ToF measurement data, **processes it using sequential bin-by-bin histogram processing**, and **applies one or more on-the-fly operations** during that processing. That is the whole independent claim. |
| **Open (dependent claims / description add; claim 1 does NOT require)** | The correlator with ambient/filter/crosstalk MAC circuits and bin-serial processing (claim 2); closest-target + strongest-maximum (highest-SNR) circuits (claim 3); the phase/bin computation circuit with ambient-pad, zero-pad, filter MAC, and positive-zero-crossing detection (claim 4); median-phase interpolation (claim 5); crosstalk histogram via interpolation + adaptive update (claim 6); sliding window (claim 7); the explicit "full histogram processing while maintaining low power for battery-powered devices" framing (claim 8); the bins-as-distribution-of-arrival-times detail (claim 9); the specific on-the-fly operations "removing crosstalk ... tracking and finding a first peak ... tracking and finding a largest peak" (claim 10); the method form with "maintaining a state of a predetermined number of most recently processed bins" (claim 11). |
| **Pinned (illustrative example values, not claim limits)** | Crosstalk description "19 bytes" vs conventional "256 bytes" [0101][0103]; "five-element" buffer [0113]; range modes "2.4 m / 4.8 m / 9.6 m" [0107]; bit widths (24-bit bins, 10/11-bit coefficients) [0111][0121]. All are "e.g." embodiment numbers in the description, not limitations the independent claim states. Treat as illustration, attribute to the paragraph, do not present as guaranteed specs. |

**Scope-discipline note**: "single pass", "streaming", "minimal memory", and "on-chip / low
power" are the patent's described advantages and the embodiment framing [0042][0069][0044]; claim
1 itself requires only "sequential bin-by-bin histogram processing" + "on-the-fly operations". The
essay can and should explain the streaming/single-pass mechanism (it is the real content), but
should attribute the leanness to the architecture and the patent's own qualitative language, not
imply the bare independent claim recites memory or power numbers.

## Timeline

- **Hero filing date**: 2024-11-19
- **Hero publication**: 2026 (US 2026/0140238 A1)
- **Support filing date**: 2022-03-17 (US 2023/0296739 B2)
- **Same-inventor thread**: Andreas Assmann / Aßmann appears on both — the 2022 single-pass
  peak-finding principle (support) and the 2024 ultra-lean on-chip implementation (hero).
- **Incorporated-by-reference family** (hero, for context only — not cited in the essay):
  18/348,600 (crosstalk), 18/342,965 (pile-up), 18/176,163 (closest target), 18/304,589 (rising
  edge) [0071][0072][0138][0202].

## Prior-art references + differentiation

- **Conventional off-chip dToF** (described, hero `[0054]`-`[0056]`): full histogram processing on
  a powerful off-chip MCU — increases I/O complexity, needs large memory, slows computation. The
  hero keeps processing on-chip in a single streaming pass.
- **Conventional on-chip dToF with a large MCU** (hero `[0055]`-`[0056]`): a large MCU in the
  sensor package consumes significant power and silicon area, with standby draw and longer run
  times. The hero replaces it with discrete hardware circuits + a sequencer at low gate count
  `[0038]`.
- **Multi-sweep peak detection** (support `[0025]`-`[0026]`): known peak detection sweeps the
  histogram multiple times (crosstalk, pulse segmentation, pulse fitting), burdening a LiDAR
  system; the support patent's single-pass method finds peaks in one iteration, the principle the
  hero carries on-chip.

## 유리한 효과 + 정량 데이터

The streaming, bin-serial design keeps full-histogram processing quality while collapsing the
memory and logic footprint, so the work fits on a low-power, compact sensor SoC — the patent
frames this qualitatively (minimal memory, low gate/logic count, battery-powered devices) rather
than committing the independent claim to a power number [0042][0044][0069]. Use the patent's own
qualitative language for "low power"; do not pin a milliwatt figure (see fact-check-log.md).

**Quotable spans:**
- `[0042]`: "Instead of storing full histograms or multiple copies of processed data, the system employs a bin-serial processing approach. The method allows for the processing of histogram data in a streaming fashion, significantly reducing memory requirements."
- `[0069]`: "the histogram processing circuit 200 is advantageously configured to iterate the histogram by serially computing relevant outputs in a single pass"

| Metric | Value | Paragraph | Status |
|---|---|---|---|
| Crosstalk description size (example) | "19 bytes" vs conventional "256 bytes" | `[0101]`, `[0103]` | pinned example — attribute, do not generalize |
| Recent-bins state buffer (example) | "five-element" | `[0113]` | pinned example |
| Range modes (example) | 2.4 m / 4.8 m / 9.6 m | `[0107]` | pinned example |

> Product-level numbers (2,268 zones, 54x42 FoV, 5 cm-9 m, up to 100 fps, ~35x leap, July 2026
> production) are NOT patent facts — they come from ST primary sources and live in fact-check-log.md.
> The NON-assertable datasheet figures (940 nm, BSI stacked, dual-VCSEL+BCD, ~150 mW, package
> dimensions, ~1% TNR) must not be stated at all. See fact-check-log.md.
