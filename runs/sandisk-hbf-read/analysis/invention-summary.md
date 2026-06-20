# Invention Summary

Two related SanDisk applications, treated as one symmetric pair. Shorthand **'885** =
US20250322885A1 (Always-On Bit Lines); **'143** = US20250279143A1 (Discharge-Free Read).

## Metadata

- **Patent ID**: US 2025/0322885 A1 ('885) · US 2025/0279143 A1 ('143)
- **Title**: "A High Bandwidth Memory Device With Always On Bit Lines" ('885) · "Discharge-Free Read Operations for High Bandwidth Nonvolatile Memory Devices" ('143)
- **Filing date**: 2024-04-15 ('885) · 2024-05-30 ('143, claiming US provisional 63/561,196 filed 2024-03-04)
- **Publication date**: 2025-10-16 ('885) · 2025-09-04 ('143)
- **Inventors**: Xiang Yang, Wei Cao, Deepanshu Dutta ('885) · Wei Cao, Xiang Yang, Jiahui Yuan, Deepanshu Dutta, Richard New ('143)
- **Classification**: CPC G11C16/26 (read), G11C16/24 ('885) · G11C16/26, G11C16/08, G11C16/102 ('143)
- **Assignee**: SanDisk Technologies LLC
- **Status**: US published applications (NOT granted)

## 발명 명칭 / 기술분야

Two read-path techniques for NAND flash built to serve as High Bandwidth Flash (HBF) — a
non-volatile alternative to HBM for AI workloads that read enormous, static data sets (model
weights) over and over. Both attack the same overhead: the voltages a NAND array raises to read
a cell, and then *lowers again*, between every read. Field: non-volatile memory read techniques
for performance ('885 [0001]; '143 [0002]).

## 종래 문제 / 과제

Conventional NAND charges the bit lines and biases the word lines for each read, then discharges
them, then does it all again for the next read. For workloads that re-read the same data at very
high rates, that setup/recovery time caps throughput and burns power. HBM (volatile DRAM) is fast
but expensive; NAND is cheap but conventionally too slow and too power-hungry to substitute.

**Quotable spans:**
- `[0004]` ('885): "in some machine learning applications, large language models that include a terabyte (or more) of data must be stored in memory and retrieved at a very high data rate. Accordingly, such applications require very high bandwidth and low power."
- `[0005]` ('885): "Non-volatile memory (e.g., NAND) is significantly less expensive than DRAM, but the bandwidth of conventional NAND memory devices is too low, and the power consumption of conventional NAND memory devices is too high to provide a viable alternative to HBM devices."
- `[0047]` ('143): "a "non-discharging read" mode or technique is implemented in which a plurality of unselected word lines in a memory block remain biased at a read pass voltage VREAD and are not discharged between successive read operations. By not discharging the unselected word lines, the time between read operations can be reduced, thereby improving read performance and read bandwidth."

## 청구항 분석 — 4-layer core mechanism

### Layer 1 — What (one sentence)

A NAND read array reaches HBM-class read throughput by holding its access voltages *up* between
consecutive reads instead of ramping them back down — bit lines (columns) in '885, unselected
word lines (rows) in '143 — eliminating the per-read recharge/recovery time.

### Layer 2 — How (mechanism)

1. Prepare a plane/block of NAND cells reachable by a shared set of bit lines (columns) and word lines (rows). (`[0006]` '885; `[0146]` '143)
2. **'885 (column axis):** perform a read on a first block while the bit lines are held at a first voltage greater than 0 V (VBL ≈ 0.2 V). (`[0006]`, `[0147]`)
3. Without ramping the bit lines down, perform the next block's read with the bit lines still at that voltage; repeat indefinitely. Only the per-block select/word-line voltages move. (`[0148]`, `[0151]`)
4. **'143 (row axis):** keep the unselected word lines biased at read-pass VREAD and do **not** discharge them during *or between* successive reads. (`[0007]`, `[0162]`, `[0178]`)
5. **'143 (adaptive trigger):** start in a normal discharging mode; after detecting a predetermined number of reads within a predetermined interval, switch into the non-discharging mode. (`[0181]`, `[0182]`)

**Key components**: bit lines BLs (VBL), word lines (selected WLn at read reference SLCR / V_CGR; unselected WL_U at read-pass VREAD), select gates (SGD), the plane/block, control circuitry; system: a processor/GPU plus plural HBF packages.

### Layer 3 — Why novel

- **Relative to prior art / industry practice**: conventional reads fully discharge and recharge the array between operations ('885 FIG. 9 baseline). The claims keep one electrode axis energized across reads, trading a fully-settled idle state for speed. Holding the bit lines at VBL keeps them within 25%, never below ~0.15 V. (`[0147]`)
- **Effect tied to the target**: both filings frame the gain as HBF read bandwidth for AI/LLM inference, not generic NAND. (`[0004]`, `[0047]`, `[0179]`)

### Layer 4 — Innovation angles

- **two-axis-symmetry**: column-hold ('885) and row-hold ('143) are the same idea applied to the two electrode axes of the array; together they cover both.
  - Evidence paragraphs: `[0006]`, `[0147]` ('885); `[0007]`, `[0047]` ('143)
  - Quote anchor refs: q-0147-1, q-0047-1
- **delete-the-recovery-tax**: the novelty is an omission — not ramping down — so the gain is time and power saved, not a new cell. (best hook for technical-impossibility)
  - Evidence paragraphs: `[0005]`, `[0147]`, `[0148]`
  - Quote anchor refs: q-0005-1, q-0148-1
- **adaptive-non-discharging**: the device senses a read burst and switches modes, so the speed mode is triggered by workload, not always-on blindly. (sophistication / moat depth)
  - Evidence paragraphs: `[0181]`, `[0182]` ('143)
  - Quote anchor refs: q-0181-1
- **built-for-inference-systems**: claims reach to systems of a processor + four-or-more HBF packages — memory designed around an accelerator. ('885 claims 14/19; '143 claim 13)
  - Evidence paragraphs: `[0011]` ('885), `[0019]` ('143)
  - Quote anchor refs: q-0019-1

## Reference number table

| Number | Label | Paragraphs | Figures (essay-local) |
|---|---|---|---|
| — | Bit lines BLs / VBL (column axis) | `[0147]`, `[0148]` ('885) | Figure 2, Figure 3, Figure 4 |
| — | Unselected word lines WL_U / read-pass VREAD (row axis) | `[0146]`, `[0162]`, `[0178]` ('143) | Figure 2, Figure 5 |
| — | Selected word line WLn / read reference (SLCR, V_CGR) | `[0146]`, `[0150]` ('143) | Figure 2, Figure 5 |
| 900/904 | HBF packages around a processor/GPU | `[0019]` ('143) | Figure 1 |
| 1000 | Adaptive non-discharging mode flow | `[0181]`, `[0182]` ('143) | Figure 6 |

## Figure relationships

| Figure (essay-local) | Paired with | Relationship | Source |
|---|---|---|---|
| Figure 3 | Figure 4 | progressive sequence (before / after, column axis) | '885 FIG. 9 / FIG. 10 |
| Figure 4 | Figure 5 | parallel pair (column-hold vs row-hold) | '885 FIG. 10 / '143 FIG. 8A |
| Figure 1 | (standalone) | orientation (HBF system) | '143 FIG. 9 |
| Figure 6 | (standalone) | mechanism (adaptive trigger) | '143 FIG. 10 |

## Quote anchor table

| Quote ID | Paragraph | Verbatim text | Significance |
|---|---|---|---|
| q-0005-1 | `[0005]` ('885) | "the bandwidth of conventional NAND memory devices is too low, and the power consumption of conventional NAND memory devices is too high to provide a viable alternative to HBM devices" | prior-art-contrast |
| q-0004-1 | `[0004]` ('885) | "large language models that include a terabyte (or more) of data must be stored in memory and retrieved at a very high data rate" | mechanism-critical |
| q-0006-1 | `[0006]` ('885) | "without ramping the plurality of bit lines down from the elevated voltage, the method continues with the step of performing a second read operation on a second memory block" | claim-supporting |
| q-0147-1 | `[0147]` ('885) | "the times required to discharge and ramp-up the bit lines are eliminated, thereby improving read performance (reducing tRead)" | mechanism-critical |
| q-0147-2 | `[0147]` ('885) | "VBL is set at approximately 0.2 V, and the voltages of the bit lines BLs never fall by more than 25% from VBL during or between read operations" | quantitative |
| q-0148-1 | `[0148]` ('885) | "the bit lines can be considered to be "always on."" | claim-supporting |
| q-0047-1 | `[0047]` ('143) | "a "non-discharging read" mode or technique is implemented in which a plurality of unselected word lines in a memory block remain biased at a read pass voltage VREAD and are not discharged between successive read operations" | claim-supporting |
| q-0007-1 | `[0007]` ('143) | "The unselected word lines are not discharged and remain biased to the read pass voltage during and between the first read operation and the second read operation." | claim-supporting |
| q-0179-1 | `[0179]` ('143) | "By increasing the read performance (reducing read time tR), the bandwidth of the HBF memory device is increased." | mechanism-critical |
| q-0019-1 | `[0019]` ('143) | "a plurality of high bandwidth flash packages in electrical communication with the processing unit" | claim-supporting |
| q-0181-1 | `[0181]` ('143) | "it is detected that a predetermined number of reads" ... "the memory device switches operation to the non-discharging read operating mode" | mechanism-critical |

## Timeline

- **'885**: filed 2024-04-15, published 2025-10-16 (examination period ~ 549 days to publication; not granted).
- **'143**: provisional 2024-03-04, filed 2024-05-30, published 2025-09-04 (not granted).
- **Prior-art chronology**: full cited-reference list not extracted from the published bodies in this run; the filings frame their baseline against conventional discharging reads ('885 FIG. 9). External forward-citation chain is handled as a fenced external fact (see fact-check-log).

## Prior-art references + differentiation

- The filings differentiate against the conventional read cycle (discharge + recharge of the array between reads), shown as the '885 FIG. 9 baseline and described at `[0147]`-`[0148]`. The claimed advance is the omission of that ramp-down.

## 유리한 효과 + 정량 데이터

Eliminating the per-read ramp reduces read time and so raises read bandwidth at lower power; the
gain is framed for HBF / AI inference. No percentage bandwidth figure is given by either filing.

**Quotable spans:**
- `[0147]` ('885): "the times required to discharge and ramp-up the bit lines are eliminated, thereby improving read performance (reducing tRead)."
- `[0148]` ('885): "there is only a brief settling time (for example, less than 1 microseconds) to let the bit lines BLs settle back at VBL"
- `[0179]` ('143): "By increasing the read performance (reducing read time tR), the bandwidth of the HBF memory device is increased."

| Metric | Value | Paragraph |
|---|---|---|
| Bit-line hold voltage VBL ('885 embodiment) | ≈ 0.2 V | `[0147]` |
| Bit-line droop limit between reads | ≤ 25% (not below ~0.15 V) | `[0147]` |
| Inter-read bit-line settling ('885 FIG. 10) | < 1 µs | `[0148]` |
| System scale (claimed) | ≥ 4 HBF devices/packages per processor | `[0011]` ('885), `[0019]` ('143) |
| Quantified bandwidth gain | not disclosed | — |
