# Invention Summary

## Metadata

- **Patent ID**: US 2026/0140238 A1
- **Title**: Ultra-Lean Time-of-Flight Histogram Processing
- **Filing date**: 2024-11-19
- **Publication date**: <unknown — cover sheet in patent.md does not list a separate publication date; 공개번호 US2026-0140238A1 implies a 2026 publication consistent with the application number series>
- **Inventors**: Donald Baxter, Pascal Mellot, Stuart McLeod, Andreas Assmann
- **Classification**: <unknown — CPC codes not present in the supplied patent.md text>
- **Assignee**: STMicroelectronics International N.V.
- **Application number**: 18/952453

## 발명 명칭 / 기술분야

A time-of-flight sensor architecture that finds the distance to a target by streaming its photon-count histogram through dedicated hardware one bin at a time, instead of holding the whole histogram in memory — a design lean enough to run the full processing pipeline on-chip, inside the sensor package. Technical field: time-of-flight (ToF) sensor technology, specifically ultra-lean histogram-processing architectures for direct ToF (dToF) sensors used in mobile devices, robotics, automotive, and other power/size-constrained applications `[0001]`.

## 종래 문제 / 과제

Conventional direct-ToF systems build a full histogram of photon arrival times and then hand it to a general-purpose microcontroller or DSP for processing — crosstalk estimation, pulse segmentation, phase estimation — which means holding multiple copies of the histogram in memory at once `[0013]`, `[0054]`. That approach requires a large, power-hungry MCU inside the sensor package: bigger silicon area, higher idle/standby draw, longer runtimes at a given clock frequency, and larger module cost and size `[0055]`, `[0056]`. Those costs make full on-chip histogram processing hard to justify in compact, battery-powered devices such as phones, wearables, or autonomous ranging gadgets `[0056]`, `[0057]`.

**Quotable spans:**
- `[0013]`: "the use of large memory banks becomes prohibitive in applications where power consumption, cost, and size can be critical factors, such as in battery-powered devices or compact mobile electronics"
- `[0041]`: "The disclosed system operates without dedicated RAM, relying on a small selection of registers and buffers for temporary data storage."
- `[0054]`: "Conventional solutions for time-of-flight (ToF) sensor histogram processing typically involve utilizing full histogram processing with a powerful off-chip microcontroller unit (MCU)."
- `[0055]`: "On-chip processing presents several drawbacks, such as necessitating a large MCU in the sensor package, which consumes significant power and increases read-out complexity."

## 청구항 분석 — 4-layer core mechanism

### Layer 1 — What (one sentence)

A time-of-flight sensor system's histogram processing circuit takes in raw photon-arrival-time data and processes it using sequential bin-by-bin histogram processing, applying on-the-fly operations (like crosstalk removal and peak-finding) as each bin streams through, rather than storing and processing the full histogram at once (claim 1).

### Layer 2 — How (mechanism)

1. The VCSEL (102) emits light pulses at a target; the return SPAD array (106) and reference SPAD array (108) detect reflected and reference photons `[0045]`, `[0047]`.
2. The OR trees (110, 112) combine per-SPAD signals into one stream each for the histogram processing circuit (114) `[0048]`.
3. The histogram processing circuit (114/200) receives the reference/return histogram and a crosstalk histogram, and processes both **one bin at a time** — a firmware/sequencer presents each bin in turn, the hardware processes it, and only then does the next bin arrive `[0079]`, `[0080]`.
4. Inside that circuit, the correlator circuit (202/400) runs three parallel MAC (multiply-accumulate) paths — ambient (402), filter/main-correlation (404), crosstalk (406) — each bin-serial, each keeping only a small buffer (e.g. five elements deep) of recent history instead of the whole histogram `[0113]`, `[0125]`.
5. A hardware accelerator (412) computes signal-to-noise ratio (SNR) per bin on the fly from those three MAC outputs, feeding a closest-target circuit (408) and a strongest-maximum circuit (410) that each track a running "best so far" as the bins go by `[0128]`–`[0141]`.
6. The phase/bin computation circuit (204/600) applies filter coefficients to the histogram in the same bin-serial fashion and watches for a positive zero crossing in the filtered output — the point where the filtered signal flips from negative to positive marks the pulse's median location `[0189]`, `[0197]`–`[0199]`.
7. Firmware (610) interpolates the current and previous filter values around that zero crossing to compute a sub-bin-precision median phase, which the range calculation circuit (206) converts to a distance using calibration/gain data `[0201]`, `[0077]`. If no zero crossing is found (e.g. merged targets), a fallback derivative-based estimate substitutes `[0204]`–`[0211]`.

**Key components**: VCSEL (102), VCSEL driver (104), return SPAD array (106), reference SPAD array (108), OR trees (110, 112), histogram processing circuit (114/200), MCU (116), correlator circuit (202/400) with ambient MAC (402) / filter MAC (404) / crosstalk MAC (406) / closest target circuit (408) / strongest maximum circuit (410) / hardware accelerator (412), phase/bin computation circuit (204/600) with ambient pad (602) / zero-pad (604) / filter MAC (606) / positive zero crossing detection circuit (608) / firmware (610), range calculation circuit (206), rate calculation circuit (208), crosstalk histogram generator circuit (218).

### Layer 3 — Why novel

- **Relative to prior art**: Prior direct-ToF designs process the histogram as a full array held in memory, using general-purpose compute for crosstalk removal, segmentation, and phase estimation `[0054]`. This patent instead discretizes each processing stage into dedicated hardware circuits that consume the histogram serially, one bin at a time, with only small fixed buffers — never a full copy of the histogram in RAM `[0041]`, `[0069]`.
- **Industry practice contrast**: Standard practice accepts a "big MCU in the package" cost as the price of on-chip full-histogram processing `[0055]`, `[0056]`; this architecture's own MCU is reduced to a sequencer role with limited local register storage, eliminating the need for a separate memory system altogether `[0043]`.

### Layer 4 — Innovation angles

- **bin-serial-streaming**: the histogram is never fully materialized in memory — it is consumed bin-by-bin through a state machine with minimal internal buffers, which is the enabling move for on-chip, ultra-low-power full histogram processing
  - Evidence paragraphs: `[0041]`, `[0042]`, `[0069]`, `[0080]`
  - Quote anchor refs: `q-0041-1`, `q-0080-1`
- **compact-crosstalk-representation**: crosstalk calibration data is compressed from a ~256-byte full-shape description down to ~19 bytes via a lookup-table + leaky-integrator hybrid, then regenerated and subtracted on the fly per bin
  - Evidence paragraphs: `[0070]`, `[0101]`, `[0103]`
  - Quote anchor refs: `q-0101-1`, `q-0103-1`
- **on-the-fly-dual-peak-finding**: the correlator simultaneously tracks the closest target and the strongest (highest-SNR) target as it streams through the histogram once, without a second pass
  - Evidence paragraphs: `[0035]`, `[0128]`, `[0139]`–`[0141]`
  - Quote anchor refs: `q-0035-1`, `q-0139-1`
- **mcu-as-sequencer**: the system's MCU is demoted from a compute-heavy processor to a bin sequencer with register-only local storage, removing the separate memory subsystem entirely
  - Evidence paragraphs: `[0043]`
  - Quote anchor refs: `q-0043-1`

## Reference number table

| Number | Label | Paragraphs | Figures |
|---|---|---|---|
| 100 | ToF sensor system | `[0045]`–`[0053]` | FIG. 1 |
| 102 | VCSEL | `[0045]`, `[0047]` | FIG. 1 |
| 104 | VCSEL driver | `[0045]`, `[0047]` | FIG. 1 |
| 106 | Return SPAD array | `[0045]`, `[0047]` | FIG. 1 |
| 108 | Reference SPAD array | `[0045]`, `[0047]` | FIG. 1 |
| 110 | First OR tree | `[0045]`, `[0048]` | FIG. 1 |
| 112 | Second OR tree | `[0045]`, `[0048]` | FIG. 1 |
| 114 | Histogram processing circuit | `[0045]`, `[0049]`, `[0061]`–`[0065]` | FIG. 1 |
| 116 | MCU | `[0045]`, `[0050]` | FIG. 1 |
| 118 | I/O interface | `[0045]`, `[0051]` | FIG. 1 |
| 120 | Power management circuit | `[0045]`, `[0051]` | FIG. 1 |
| 122 | OTP memory | `[0045]`, `[0052]` | FIG. 1 |
| 200 | Histogram processing circuit (detail) | `[0066]`–`[0069]` | FIG. 2 |
| 202 | Correlator circuit | `[0066]`, `[0072]`–`[0075]` | FIG. 2, FIG. 4 |
| 204 | Phase/bin computation circuit | `[0066]`, `[0076]` | FIG. 2, FIG. 6 |
| 206 | Range calculation circuit | `[0066]`, `[0077]` | FIG. 2 |
| 208 | Rate calculation circuit | `[0066]`, `[0078]` | FIG. 2 |
| 218 | Crosstalk histogram generator circuit | `[0066]`, `[0070]` | FIG. 2 |
| 300 | Crosstalk calibration data method | `[0083]`–`[0103]` | FIG. 3 |
| 302–312 | Crosstalk calibration steps | `[0084]`–`[0100]` | FIG. 3 |
| 400 | Correlator circuit (detail) | `[0104]`–`[0148]` | FIG. 4 |
| 402 | Ambient MAC circuit | `[0104]`, `[0125]`–`[0127]` | FIG. 4 |
| 404 | Filter MAC circuit | `[0104]`, `[0125]`, `[0128]` | FIG. 4 |
| 406 | Crosstalk MAC circuit | `[0104]`, `[0125]`, `[0132]` | FIG. 4 |
| 408 | Closest target circuit | `[0104]`, `[0137]`, `[0138]` | FIG. 4 |
| 410 | Strongest maximum circuit | `[0104]`, `[0139]`–`[0142]` | FIG. 4 |
| 412 | Hardware accelerator | `[0129]`–`[0136]` | FIG. 4 |
| 432 | Ambient pad circuit | `[0118]` | FIG. 4 |
| 434 | Zero-pad circuit | `[0118]` | FIG. 4 |
| 500 | Bin-serial processing method | `[0149]`–`[0172]` | FIG. 5 |
| 502–510 | Method 500 steps | `[0150]`–`[0170]` | FIG. 5 |
| 600 | Phase/bin computation circuit (detail) | `[0173]`–`[0211]` | FIG. 6 |
| 602 | Ambient pad circuit (phase/bin) | `[0173]`, `[0187]` | FIG. 6 |
| 604 | Zero-pad circuit (phase/bin) | `[0173]`, `[0187]` | FIG. 6 |
| 606 | Filter MAC circuit (phase/bin) | `[0173]`, `[0189]`–`[0195]` | FIG. 6 |
| 608 | Positive zero crossing detection circuit | `[0173]`, `[0196]`–`[0200]` | FIG. 6 |
| 610 | Firmware | `[0173]`, `[0177]`–`[0179]`, `[0201]` | FIG. 6 |
| 700 | On-the-fly median estimation method | `[0212]`–`[0227]` | FIG. 7 |
| 702–712 | Method 700 steps | `[0213]`–`[0226]` | FIG. 7 |

## Figure relationships

| Figure | Paired with | Relationship | Page (if known) |
|---|---|---|---|
| FIG. 1 | (standalone) | System-level block diagram — establishes the whole sensor's parts | `[0023]`, `[0045]` |
| FIG. 2 | FIG. 4, FIG. 6 (zoom targets) | FIG. 2 is the mid-level exploded view of block 114 from FIG. 1; FIG. 4 and FIG. 6 are further detail-zooms of two of FIG. 2's sub-blocks (correlator 202, phase/bin 204) | `[0024]`, `[0066]` |
| FIG. 3 | (standalone flowchart) | Method for generating crosstalk calibration data — supports FIG. 2's crosstalk generator (218) but stands alone as a process | `[0025]`, `[0083]` |
| FIG. 4 | FIG. 2 (zoom source) | Detail block diagram of correlator circuit (202) introduced in FIG. 2 | `[0026]`, `[0104]` |
| FIG. 5 | FIG. 4 (implementing circuit) | Flowchart of the bin-serial method implemented using the FIG. 4 correlator circuit — a process view of the same mechanism FIG. 4 shows structurally | `[0027]`, `[0149]` |
| FIG. 6 | FIG. 2 (zoom source) | Detail block diagram of phase/bin computation circuit (204) introduced in FIG. 2 | `[0028]`, `[0173]` |
| FIG. 7 | FIG. 6 (implementing circuit) | Flowchart of the on-the-fly median estimation method implemented using the FIG. 6 circuit — a process view of the same mechanism FIG. 6 shows structurally | `[0029]`, `[0212]` |

No same-page sub-figure pairs (no "FIG. NA/NB" labels in this patent — all seven figures are independently numbered). The relationship that matters for selection is the **system → sub-block → detail-zoom** hierarchy: FIG. 1 (system) → FIG. 2 (histogram-circuit exploded view) → FIG. 4 / FIG. 6 (further detail on two of FIG. 2's blocks), plus two flowcharts (FIG. 5, FIG. 7) that are process views of the FIG. 4 / FIG. 6 circuits respectively, and one standalone calibration flowchart (FIG. 3).

## Quote anchor table

| Quote ID | Paragraph | Verbatim text | Significance |
|---|---|---|---|
| q-abstract-1 | Abstract | "processes time-of-flight measurement data using sequential bin-by-bin histogram processing" | claim-supporting |
| q-0013-1 | `[0013]` | "the use of large memory banks becomes prohibitive in applications where power consumption, cost, and size can be critical factors, such as in battery-powered devices or compact mobile electronics" | prior-art-contrast |
| q-0041-1 | `[0041]` | "The disclosed system operates without dedicated RAM, relying on a small selection of registers and buffers for temporary data storage." | mechanism-critical |
| q-0043-1 | `[0043]` | "the system's microcontroller unit (MCU) functions primarily as a sequencer, with limited local storage in the form of registers" | mechanism-critical |
| q-0054-1 | `[0054]` | "Conventional solutions for time-of-flight (ToF) sensor histogram processing typically involve utilizing full histogram processing with a powerful off-chip microcontroller unit (MCU)." | prior-art-contrast |
| q-0055-1 | `[0055]` | "On-chip processing presents several drawbacks, such as necessitating a large MCU in the sensor package, which consumes significant power and increases read-out complexity." | prior-art-contrast |
| q-0069-1 | `[0069]` | "Rather than processing the full reference/return histogram input as an entire array in memory, the histogram processing circuit 200 is advantageously configured to iterate the histogram by serially computing relevant outputs in a single pass." | mechanism-critical |
| q-0080-1 | `[0080]` | "The histogram data is processed one bin at a time using the bin-serial processing method." | mechanism-critical |
| q-0080-2 | `[0080]` | "The approach creates a state machine that maintains minimal internal buffers, significantly reducing memory requirements compared to traditional approaches that process entire histograms simultaneously." | mechanism-critical |
| q-0035-1 | `[0035]` | "the current implementation of the custom peak finder outputs the strongest and closest target outputs from full histogram data" | mechanism-critical |
| q-0139-1 | `[0139]` | "The strongest maximum circuit 410 identifies the peak with the highest SNR and stores its location and SNR value." | mechanism-critical |
| q-0101-1 | `[0101]` | "Conventional approaches typically require storing 128 or 144 bins of 16-bit data, resulting in a memory footprint of approximately 256 bytes. However, the proposed implementation reduces the required storage to, for example, 19 bytes." | quantitative |
| q-0103-1 | `[0103]` | "The substantial reduction in memory usage from, for example, 256 bytes to 19 bytes represents a significant optimization for the memory-constrained system" | quantitative |
| q-0107-1 | `[0107]` | "Correlator circuit 400 is compatible with multiple pulse/bin widths (i.e., timing options) to enable short range (2.4 meters (m)), medium range (e.g., 4.8 m), and long range (e.g., 9.6 m) operations." | quantitative |
| q-0236-1 | `[0236]` | "the histogram data including: a plurality of bins, each bin corresponding to a time delay; and a value in each bin representing a number of photons detected at the corresponding time delay, wherein the histogram data represents a distribution of photon arrival times from the reflected light pulses" | claim-supporting |

## Timeline

- **Filing date**: 2024-11-19
- **Publication date**: <unknown — patent.md cover sheet does not give a separate publication date field; the publication number US2026-0140238A1 implies 2026>
- **Examination period**: <not computable — publication date not stated in the supplied text>
- **Prior-art chronology**: The patent's specification does not cite external prior-art publications with their own filing/publication dates (no "cited at [XXXX]" numbered prior-art references appear in the Background section). It does, however, incorporate three of the assignee's own co-pending/earlier applications by reference for specific sub-techniques (see next section) — same-assignee continuations of technique, not adversarial prior art.

## Prior-art references + differentiation

The patent's Background of the Invention (`[0001]`–`[0013]`) describes conventional direct-ToF histogram processing generically (general-purpose MCU/DSP-based, full-histogram-in-memory) rather than citing specific numbered prior-art patents to differentiate against. The differentiation axis is therefore **industry-practice contrast**, not citation-by-citation contrast: `[0054]`–`[0058]` state the conventional approach's costs (large MCU, higher standby power, larger silicon area, higher module cost) as the baseline this architecture improves on.

Separately, the specification incorporates three same-assignee (STMicroelectronics) prior applications by reference for specific component techniques — these are not adversarial prior art but internal cross-references establishing that certain sub-techniques (crosstalk correction, pile-up mitigation, closest-target detection, rising-edge phase focus) were separately filed and are reused here as building blocks:
- **U.S. patent application Ser. No. 18/348,600** (cited at `[0071]`): adaptive crosstalk estimator / low-cost crosstalk shape storage and approximation technique — feeds the crosstalk histogram generator circuit (218).
- **U.S. patent application Ser. No. 18/342,965** (cited at `[0072]`): pile-up mitigation technique used by the correlator circuit's closest-edge-finding algorithm.
- **U.S. patent application Ser. No. 18/176,163** (cited at `[0138]`): closest-detected-target determination approach used by the closest target circuit (408).
- **U.S. patent application Ser. No. 18/304,589** (cited at `[0202]`): rising-edge phase-calculation focus used by the phase/bin computation circuit.

None of these four internal cross-references is independently verified against source text this session (their content here is only as characterized by the hero patent's own `[0071]`/`[0072]`/`[0138]`/`[0202]` paraphrase) — do not attribute further detail to them beyond what the hero patent itself states.

## 유리한 효과 + 정량 데이터

The bin-serial, on-the-fly architecture cuts the memory and MCU footprint of full histogram processing enough to run entirely on-chip within a battery-powered device's power budget, while retaining full histogram capability (crosstalk removal, dual closest/strongest peak-finding, multi-range-mode operation) rather than trading capability away for the power savings `[0044]`, `[0059]`, `[0060]`.

**Quotable spans:**
- `[0044]`: "the system achieves full histogram processing capabilities comparable to more resource-intensive solutions while maintaining ultra-low power consumption suitable for integration into battery-powered devices"
- `[0059]`: "ToF sensor system 100 can detect and process multiple targets, adapting to various environmental conditions, including ambient light interference. It can operate in different ranging modes, adapting to close, medium, or long-range applications while maintaining consistent memory requirements."
- `[0107]`: "Correlator circuit 400 is compatible with multiple pulse/bin widths (i.e., timing options) to enable short range (2.4 meters (m)), medium range (e.g., 4.8 m), and long range (e.g., 9.6 m) operations."
- `[0101]`: "Conventional approaches typically require storing 128 or 144 bins of 16-bit data, resulting in a memory footprint of approximately 256 bytes. However, the proposed implementation reduces the required storage to, for example, 19 bytes."

| Metric | Value | Paragraph |
|---|---|---|
| Crosstalk calibration data footprint (proposed vs. conventional) | ~19 bytes (vs. ~256 bytes conventional) | `[0101]`, `[0103]` |
| Crosstalk shape dynamic range | 10000:1 (14-bit) | `[0085]`, `[0102]` |
| Range-mode operating distances (example) | short 2.4 m / medium 4.8 m / long 9.6 m | `[0107]` |
| Reference/return histogram bin count (example) | 32 or 128 bins | `[0114]` |
| Crosstalk event histogram bin count (example) | 64 bins | `[0115]` |
| Histogram bin data width (example) | 24-bit unsigned | `[0114]`, `[0116]` |
| Filter coefficient bit-width (example) | 11-bit, signed 1.10 fixed-point | `[0108]` |
| MAC buffer depth (example) | 5-element deep | `[0113]`, `[0125]` |

Note: these are the patent's own illustrative example values ("e.g.," / "for example") for its embodiments, not marketed product specs — kept distinct from the VL53L9CX product figures in `fact-check-log.md`.

> Revision note — triggered by [step 2, context research] 2026-07-01: no changes required to this file from Step 2 findings. Context research (VL53L9CX product specs, VL53L5/L8CX baseline) is entirely external-fact material and lives in `fact-check-log.md` / `search-log.md`, not here — the patent-anchored content above was stable through Steps 2–9.
