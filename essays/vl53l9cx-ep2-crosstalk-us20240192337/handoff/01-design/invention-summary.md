# Invention Summary

## Metadata

- **Patent ID**: US 2024-0192337 B2 (granted)
- **Title**: Cross-talk rejecting convolution peak finding
- **Filing date**: 2022-12-12
- **Application number**: 18/064412
- **Publication date**: <unknown — not stated on the provided cover page; only filing date and application number are given>
- **Inventors**: Andreas Assmann
- **Classification**: <unknown — not stated on the provided cover page>
- **Assignee**: STMicroelectronics N.V.

## 발명 명칭 / 기술분야

Reader-ready framing: a method (and the on-chip circuit that runs it) for telling a real object
apart from the sensor's own reflection off its protective cover glass, inside the raw histogram
a time-of-flight sensor produces — without needing a separate processor or a factory-tuned
correction step. Technical field, per the patent's own opening line: "time-of-flight (ToF)
imagers, and, in particular embodiments, to ToF imagers with peaking finding circuits for
rejecting cross-talk and improving range of detection." `[0001]`

## 종래 문제 / 과제

A time-of-flight sensor fires a laser pulse and times how long the reflection takes to return;
that timing data arrives as a histogram — a per-distance bin count of returned photons — and the
real target shows up as a peak in that histogram `[0032]`. The sensor sits behind a protective
window (a cover glass), and that window reflects part of the outgoing pulse straight back into
the detector array before the pulse ever leaves the housing `[0029]`. Because the window is only
millimeters from the detector, that reflection lands in the very first few histogram bins — the
"near zero distance" region — masquerading as a target sitting almost on top of the sensor
`[0029]`. Two established ways of turning the histogram into a target's distance each fail against
this problem in a different way: a matched filter (MF) gets long range but is highly vulnerable to
being fooled by the cross-talk peak `[0056]`, while a zero-crossing filter (ZCF) can be made robust
against cross-talk but loses signal-to-noise and therefore range `[0055]`. Compounding this, the
conventional way of extracting any information from the histogram at all is "computationally
intensive," typically pushed to an off-chip processor on a separate silicon die `[0004]`, `[0027]` —
which is itself costly, slow, and power-hungry `[0027]`, `[0028]`.

**Quotable spans:**
- `[0029]`: "The cross-talk signal in the histogram, if not processed properly, may be incorrectly detected as a close target."
- `[0029]`: "The window reflects a portion of the transmitted light signal 104 back to the SPAD array 101, this phenomenon is referred to as cross-talk (may also be referred to as cover glass reflection, or housing reflection), and the reflected light signal by the window is referred to as a cross-talk signal."
- `[0056]`: "The MF based target detection described above can achieve long detection range. However, the MF based target detection is very sensitive to cross-talk."
- `[0027]`: "Such off-chip computation is not only costly (e.g., due to the number of IC devices needed), but also increases input/output (I/O) complexity of the ToF imager, requires large amounts of memory, and incurs time delay for data transfer, due to the large amount of histogram data to be transferred between the ToF imager and the off-chip processing module."

## 청구항 분석 — 4-layer core mechanism

### Layer 1 — What (one sentence)

The chip filters its own raw histogram two ways at once — a zero-crossing filter that stays
level-headed near the sensor and a matched filter that reaches out to long range — then uses a
weighted-sum test on the zero-crossing filter's output to throw out any near-sensor peak that
looks like the cover-glass's own reflection, before it ever gets reported as a target.

### Layer 2 — How (mechanism)

1. Filter the histogram with a zero-crossing filter (ZCF) to produce a ZCF output signal, and
   separately filter it with a matched filter (MF) to produce an MF output signal. `[0030]`,
   claim 1, claim 6
2. Find the zero-crossing points in the ZCF output signal; each pair of zero-crossing points
   brackets one positive pulse region — a candidate target. `[0042]`, claim 1
3. Assign a weight coefficient to every histogram bin: negative for bins before a "reference
   zero-point" (the bin distance matching the cover-glass window), positive for bins after it.
   `[0054]`, `[0060]`, claim 3, claim 4
4. For each positive pulse region, multiply the ZCF output values by their bins' weight
   coefficients and sum the result — the weighted sum. `[0049]`-`[0050]`, claim 2
5. Find the maximum peak inside each pulse region, then classify that peak as a first type
   (potentially a real target) or a second type (cross-talk or noise) by comparing the weighted
   sum against a positive and a negative threshold. `[0052]`, claim 5
6. Validate the surviving first-type peaks by confidence level (e.g., signal-to-noise ratio)
   and collect them into a list of ZCF targets; separately find the strongest MF target (subject
   to its own switch-over distance and confidence check). `[0053]`, `[0057]`-`[0058]`, claim 8
7. A decision module compares the strongest ZCF target and the strongest MF target and reports
   the stronger one as the overall strongest target, while combining both lists into one list of
   targets in the histogram. `[0063]`-`[0064]`, claim 12

**Key components**: SPAD array (101 / 401), light source / emitter (103 / 403), zero-crossing
filter — ZCF (301 in FIG. 4 concept; 811 in FIG. 10 flow), matched filter — MF (303 in FIG. 4
concept; 803 in FIG. 10 flow), weight-coefficient generator (809), peak finding circuit (407 /
421), decision module / switch-over criteria (821), depth map memory (409).

### Layer 3 — Why novel

- **Relative to prior art**: The patent frames conventional histogram processing as
  computationally heavy, iterative, and normally off-chip `[0004]`, `[0027]`, `[0028]` — the
  disclosure's own point of departure rather than a differentiation from a single named
  competitor patent (no external prior-art patent number is cited in the body; see "Prior-art
  references" below for the one related-application citation that does appear). Within that
  framing, the specific novelty is combining a weighted-sum classification step with a
  parallel-running MF/ZCF switch-over, so cross-talk rejection and long range are no longer a
  forced trade-off between the two filter types.
- **Industry practice contrast**: Standard practice, per the patent's own account, is to pick
  one detection approach and accept its failure mode — MF for range (vulnerable to cross-talk)
  or ZCF for cross-talk robustness (short range) — or to push the classification work off-chip
  entirely. The claimed architecture runs both filters in parallel on-chip and lets a per-region
  weighted-sum test do the classification that neither filter alone can do, integrated directly
  into the SPAD array's own IC device. `[0069]`, `[0071]`-`[0072]`

### Layer 4 — Innovation angles

- **weighted-zero-crossing-rejection**: the weight-coefficient trick — negative before the
  cover-glass reference point, positive after — is what turns a symmetric-looking pulse region
  into a classifiable "is this cross-talk" signal.
  - Evidence paragraphs: `[0054]`, `[0060]`
  - Quote anchor refs: q-0054-1, q-0060-1
- **dual-filter-switchover**: running ZCF (short-range-safe) and MF (long-range-capable) in
  parallel and letting a decision module pick the stronger validated target closes the gap that
  neither filter closes alone.
  - Evidence paragraphs: `[0056]`, `[0076]`
  - Quote anchor refs: q-0056-1, q-0076-1
- **on-chip-integration**: the entire peak-finding circuit — MF, ZCF, weighting, classification,
  decision module — sits on the same IC device as the SPAD array, eliminating the off-chip
  processor the specification frames as the conventional approach.
  - Evidence paragraphs: `[0027]`, `[0069]`
  - Quote anchor refs: q-0027-1, q-0069-1
- **calibration-free-reference-point** (secondary/deepening angle): the "reference zero-point"
  is the histogram bin matching the known SPAD-to-window distance, computed once and reused
  (`[0060]`: "the processing of blocks 807 and 809 may be performed only once, and the resulting
  weight coefficients may be saved for future use"). Caution: the patent's own word for
  establishing this value is itself "a calibration of the bin distance" `[0033]` — do not frame
  this angle as the patent itself saying "no calibration." The specification does not state
  whether that one-time determination happens per-unit or per product design, so "not a per-unit
  factory trim" is NOT a patent-supported claim; that specific framing belongs to ST's external
  "calibration-free" marketing language (fact-check-log.md), not to the specification, and must
  be attributed there, not blended into the patent's own technical description. This is also the
  mechanism the supporting patent later makes adaptive over time.
  - Evidence paragraphs: `[0033]`, `[0060]`
  - Quote anchor refs: q-0033-1, q-0033-2, q-0060-1

## Reference number table

| Number | Label | Paragraphs | Figures |
|---|---|---|---|
| 100 | ToF imager | `[0026]`, `[0031]` | FIG. 1 |
| 101 | SPAD array | `[0026]`, `[0029]` | FIG. 1 |
| 103 | Light source / emitter (VCSEL) | `[0026]`, `[0029]` | FIG. 1 |
| 104 | Light signal (outgoing) | `[0026]`, `[0029]` | FIG. 1 |
| 105 | Object / target | `[0026]` | FIG. 1 |
| 106 | Reflected light signal | `[0026]`, `[0029]` | FIG. 1 |
| 107 | Time-to-digital converter (TDC) | `[0026]` | FIG. 1 |
| 109 | Histogram | `[0026]` | FIG. 1 |
| 201 | Cross-talk peak in histogram | `[0032]`, `[0033]` | FIG. 2, FIG. 3 |
| 203 | Real-target peak in histogram | `[0032]`, `[0033]` | FIG. 2, FIG. 3 |
| 301 | ZCF (curve) | `[0034]`, `[0037]` | FIG. 4 |
| 303 | MF (curve) | `[0034]`, `[0038]` | FIG. 4 |
| 500 | ZCF (longer variant) | `[0039]` | FIG. 5 |
| 501 | Rising edge region | `[0039]` | FIG. 5 |
| 503 | Accumulation region | `[0039]` | FIG. 5 |
| 505 | Falling edge region | `[0039]` | FIG. 5 |
| 601 | ZCF output signal | `[0041]`, `[0042]` | FIG. 6, FIG. 9 |
| 601W | Weighted ZCF output signal | `[0048]`, `[0049]` | FIG. 9 |
| 603 | MF output signal | `[0041]` | FIG. 6 |
| 611 | Maximum peak, 1st ZCF pulse region (cross-talk candidate) | `[0042]`, `[0043]` | FIG. 6, FIG. 9 |
| 613 | Maximum peak, 2nd ZCF pulse region (real-target candidate) | `[0042]`, `[0043]` | FIG. 6, FIG. 9 |
| 701 / 703 / 705 | Weight-coefficient curve sets (2-segment linear / 4-segment linear / non-linear) | `[0044]`-`[0047]` | FIG. 7, FIG. 8 |
| 710 | Zoomed area of FIG. 7 shown in FIG. 8 | `[0047]` | FIG. 7 |
| 800 | Adaptive target detection method | `[0057]` | FIG. 10 |
| 801-825 | Adaptive detection method blocks | `[0057]`-`[0064]` | FIG. 10 |
| 400 | IC device (peak finding on separate block from SPAD array) | `[0069]` | FIG. 13 |
| 401 | SPAD array (IC device) | `[0069]`, `[0071]` | FIG. 13, FIG. 14 |
| 403 | Light source (IC device) | `[0069]` | FIG. 13, FIG. 14 |
| 405 | Memory module (histogram storage) | `[0069]` | FIG. 13 |
| 407 | Peak finding circuit (IC device 400) | `[0069]`, `[0070]` | FIG. 13 |
| 409 | Depth map memory | `[0069]`, `[0070]` | FIG. 13, FIG. 14 |
| 400A | IC device (peak finding integrated at pixel level) | `[0070]` | FIG. 14 |
| 408 | I/O circuit (IC device 400A) | `[0070]` | FIG. 14 |
| 411 | SPADs (pixel-level detail) | `[0071]` | FIG. 14 |
| 413 | TDCs (pixel-level detail) | `[0071]` | FIG. 14 |
| 415 | Histogram memory (pixel-level detail) | `[0071]` | FIG. 14 |
| 417 | MF/ZCF (pixel-level detail) | `[0071]` | FIG. 14 |
| 419 | Filter response memory (pixel-level detail) | `[0071]` | FIG. 14 |
| 421 | Peak finding circuit (pixel-level detail) | `[0071]` | FIG. 14 |
| 423 | I/O circuit (pixel-level detail) | `[0071]` | FIG. 14 |
| 1010-1060 | Claim-level method blocks | `[0075]` | FIG. 15 |

## Figure relationships

| Figure | Paired with | Relationship | Page (if known) |
|---|---|---|---|
| FIG. 2 | FIG. 3 | same histogram, re-plotted — FIG. 2 is bin-number x-axis (raw), FIG. 3 is the same data recalibrated to distance and shifted so the cross-talk peak (201) sits at the "reference zero-point" | `[0031]`-`[0033]` |
| FIG. 4 | FIG. 5 | ZCF variant pair — FIG. 4 shows a shorter ZCF alongside the MF for direct shape comparison; FIG. 5 shows a longer ZCF variant with labeled sub-regions (rising edge / accumulation / falling edge) | `[0034]`, `[0039]`-`[0040]` |
| FIG. 6 | FIG. 9 | progressive sequence — FIG. 6 shows the raw ZCF and MF output overlaid on the (recalibrated) histogram; FIG. 9 zooms into the ZCF output's near-zero region and adds the weighted curve (601W) that performs the actual classification | `[0041]`-`[0043]`, `[0048]`-`[0052]` |
| FIG. 7 | FIG. 8 | same-page sub-figure pair — FIG. 7 shows three weight-coefficient curve families across the full bin range; FIG. 8 is a zoomed inset of the same three curves around the reference zero-point (area 710 in FIG. 7) | `[0044]`-`[0047]` |
| FIG. 11 | FIG. 12 | progressive sequence (before / after) — FIG. 11 shows adaptive-method performance with no cross-talk present; FIG. 12 shows the identical experiment with cross-talk present, so the pair is the load-bearing before/after comparison for the entire cross-talk-rejection claim | `[0066]`-`[0068]` |
| FIG. 13 | FIG. 14 | same-page sub-figure pair (architecture variants) — FIG. 13 shows peak-finding integrated once per IC device (405/407 outside the SPAD array); FIG. 14 shows peak-finding pushed down to per-pixel granularity within the SPAD array | `[0069]`-`[0072]` |
| FIG. 1 | (standalone) | establishes the ToF imager architecture and the raw histogram output | `[0026]` |
| FIG. 10 | (standalone) | full adaptive-detection method flow chart; references components/values introduced across FIGs. 1-9 but is not itself a sub-figure of any single other figure | `[0057]`-`[0065]` |
| FIG. 15 | (standalone) | claim-1-level method flow chart — the minimal method, distinct from FIG. 10's fuller adaptive-detection flow | `[0074]`-`[0075]` |

## Quote anchor table

| Quote ID | Paragraph | Verbatim text | Significance |
|---|---|---|---|
| q-0029-1 | `[0029]` | "The cross-talk signal in the histogram, if not processed properly, may be incorrectly detected as a close target." | claim-supporting |
| q-0029-2 | `[0029]` | "The window reflects a portion of the transmitted light signal 104 back to the SPAD array 101, this phenomenon is referred to as cross-talk (may also be referred to as cover glass reflection, or housing reflection), and the reflected light signal by the window is referred to as a cross-talk signal." | mechanism-critical |
| q-0027-1 | `[0027]` | "Such off-chip computation is not only costly (e.g., due to the number of IC devices needed), but also increases input/output (I/O) complexity of the ToF imager, requires large amounts of memory, and incurs time delay for data transfer, due to the large amount of histogram data to be transferred between the ToF imager and the off-chip processing module." | prior-art-contrast |
| q-0056-1 | `[0056]` | "The MF based target detection described above can achieve long detection range. However, the MF based target detection is very sensitive to cross-talk." | mechanism-critical |
| q-0055-1 | `[0055]` | "while the ZCF output signal can be used to detect close target with improved robustness against cross-talk, ZCF based target detection may not perform well for far-away target" | mechanism-critical |
| q-0054-1 | `[0054]` | "by assigning negative values to weight coefficients of histogram bins at distance closer than the distance D, the weighted sum calculation described above penalizes values of the positive pulse region before the distance D, because these values are mostly likely caused by cross-talk" | mechanism-critical |
| q-0060-1 | `[0060]` | "the histogram bin having a distance equal to the distance between the SPAD array 101 and the window of the assembly housing is identified, and its location is used as the reference zero-point" | mechanism-critical |
| q-0033-1 | `[0033]` | "the zero point on the x-axis of the histogram in FIG. 3 is also referred to as the reference zero-point" | mechanism-critical |
| q-0033-2 | `[0033]` | "a calibration of the bin distance" | mechanism-critical |
| q-0069-1 | `[0069]` | "the peaking finding circuit 407 performs on-chip processing of the histogram data from the SPAD array 401, which significantly reduces the chip complexity related to I/O transfer of histogram data to an off-chip processing module, and reduces the processing delay related to off-chip processing" | claim-supporting |
| q-0076-1 | `[0076]` | "the disclosed ZCF based target detection method can reject false target caused by cross-talk, thus achieving robustness against cross-talk" | quantitative/effect |
| q-0076-2 | `[0076]` | "the disclosed adaptive detection method enjoys benefit from both the ZCF based detection and MF based detection, thereby achieving robustness against cross-talk while still maintaining long detection range" | quantitative/effect |
| q-0067-1 | `[0067]` | "when no cross-talk is present, the ZCF based detection is effective for close range detection, but was unable to correctly detect target at long range due to the SNR attenuation" | prior-art-contrast |
| q-0068-1 | `[0068]` | "when cross-talk is present, the MF based target detection, due to its sensitivity to cross-talk, locks on to the false target generated by cross-talk, and was unable to detect target correctly at close range" | quantitative/effect |
| q-0068-2 | `[0068]` | "the adaptive detection method, by switching between MF based detection and ZCF based detection (e.g., choosing the ZCF based detection at close range and the MF based detection at long range if appropriate), was able to achieve correct target detection for a range comparable to that of the MF based target detection method" | quantitative/effect |

## Timeline

- **Filing date**: 2022-12-12
- **Publication date**: <unknown — not stated on the provided cover page>
- **Grant status**: Granted (B2 designation on cover page)
- **Examination period**: <unknown — grant date not stated on the provided cover page>
- **Prior-art chronology**: The specification does not cite any external prior-art patent numbers
  in its Background of the Invention. The only related-application citation in the body is to
  the same assignee's own concurrently-filed differential-correlator-filter application:
  | Citation | Relationship | Paragraph |
  |---|---|---|
  | U.S. patent application Ser. No. 17/858,421, "Differential Correlator Filter for Efficient ToF Peak Finding" | Incorporated by reference; same assignee, ZCF/DCF design detail | `[0037]` |

## Prior-art references + differentiation

- **U.S. patent application Ser. No. 17/858,421** ("Differential Correlator Filter for Efficient
  ToF Peak Finding", cited at `[0037]`): incorporated by reference for ZCF/DCF (differential
  correlator filter) design and application detail. This is a companion filing, not an
  adversarial prior-art citation — the patent does not frame it as something this invention
  improves upon, only as background detail on the ZCF's own filter design that is "not discussed
  here" in this specification.
  <!-- Note: no adversarial/third-party prior art is cited by number in the specification body.
       The patent instead frames its own novelty against unnamed "conventional" practice
       (off-chip processing, single-filter-type detection) described in [0004], [0027]-[0028],
       [0055]-[0056]. This is the source for Axis 4 (baseline-difference) — see
       thesis-spine.md, where the baseline-difference anchor draws on context research
       (industry-wide cover-glass cross-talk as a named, recurring problem across ST's own
       product line, not a single rival patent) rather than a named competitor's patent. -->

## 유리한 효과 + 정량 데이터

The claimed method and circuit reject a cross-talk-caused false target while preserving long
detection range and keeping all of the processing on the same IC device as the SPAD array —
trading away the pure-ZCF and pure-MF failure modes without needing an off-chip processor. The
patent's own performance data is comparative (curve-based, FIGS. 11-12) rather than a single
pinned percentage or millisecond figure: with no cross-talk, plain ZCF detection is accurate at
close range but fails at long range, while the adaptive method matches MF's long range without
losing that close-range integrity `[0067]`; with cross-talk present, plain MF detection "locks
on" to the false target and fails at close range, while the adaptive method still achieves
"correct target detection for a range comparable to that of the MF based target detection
method" `[0068]`.

**Quotable spans:**
- `[0076]`: "the disclosed ZCF based target detection method can reject false target caused by cross-talk, thus achieving robustness against cross-talk"
- `[0068]`: "the adaptive detection method, by switching between MF based detection and ZCF based detection (e.g., choosing the ZCF based detection at close range and the MF based detection at long range if appropriate), was able to achieve correct target detection for a range comparable to that of the MF based target detection method"

| Metric | Value | Paragraph |
|---|---|---|
| Histogram size (example) | ~128 bins | `[0031]` |
| Detection range, no cross-talk (comparative, FIG. 11) | adaptive method ≈ MF-only method's range, exceeding ZCF-only range | `[0066]`-`[0067]` |
| Detection range, with cross-talk (comparative, FIG. 12) | adaptive method rejects the false close-range target and still ≈ MF-only method's range; plain MF fails at close range | `[0068]` |
| Detection range plotted (FIGS. 11-12 axes) | 0-2000+ mm depth axis | FIG. 11, FIG. 12 (visual scale only — not a claimed spec number) |

<!--
  No single pinned percentage-improvement or millisecond-lead number exists in this patent's
  own text (contrast with the Tesla RCM template's "~70ms" / "<0.1%" figures) — the patent's
  own evidence is comparative-curve-based (FIGS. 11/12), not a single quantitative headline
  metric. This is itself an accurate finding, not a gap to force-fill: Axis 3 (effect anchor)
  in thesis-spine.md draws on this comparative framing plus the qualitative q-0076-1 /
  q-0068-2 language rather than inventing a number the patent does not state.
-->

> Revision note — triggered by [post-acceptance self-audit, skeptical-pro-subject-reader +
> impatient-investor reviewers] [2026-07-01]: two grounding corrections applied after the essay
> was already promoted to essay-final.md. (1) The "종래 문제" section's `[0003]` anchor for "a
> real target shows up as a peak in that histogram" was wrong — paragraph [0003] only covers SPAD
> avalanche-photodiode mechanics and never mentions peaks or targets; corrected to `[0032]`, which
> is the paragraph that actually introduces peak 201 (cross-talk) and peak 203 (real target).
> (2) The calibration-free-reference-point innovation angle asserted "not a per-unit factory
> trim" as if the patent said so; the patent's own word for this exact mechanism is "a calibration
> of the bin distance" [0033], and the spec does not state whether the one-time determination is
> per-unit or per-design. Reworded to attribute "calibration-free" to ST's external marketing
> language only, added q-0033-2 as the verbatim "calibration" anchor so a future recompose from
> this file cannot reintroduce the same overreach. Both corrections propagated to
> handoff/02-compose/essay-draft.md, publication.md, and handoff/03-edit/essay-final.md.
