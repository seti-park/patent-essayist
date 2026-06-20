# Invention Summary

## Metadata

- **Patent ID**: US 2026/0006802 A1
- **Title**: High Bandwidth Flash Memory Containing a Stack of Bonded Logic and Memory Die Assemblies and Methods for Forming the Same
- **Filing date**: 2024-08-21
- **Publication date**: 2026-01-01
- **Priority date**: 2024-06-28 (US provisional 63/665,731)
- **Application no.**: 18/811,118
- **Family ID**: 98222603
- **Inventors**: Mitsuteru Mushiga (Kuwana, JP), Masaaki Higashitani (Cupertino, CA)
- **Classification**: H10B80/00; H01L25/065 (H01L25/0657); H01L25/18; H01L24/08; H01L24/80; H01L25/50; H01L23/00
- **Assignee / Applicant**: SanDisk Technologies, Inc. (Milpitas, CA)
- **Legal status**: Published application — NOT granted. Claims may narrow in prosecution. Frame all rights as *sought*, not held.

## 발명 명칭 / 기술분야

A flash-memory packaging architecture that gives every NAND (or NOR) memory die its own bonded, dedicated memory-controller die, stacks those memory-plus-controller assemblies on top of one another, and runs power and signal vertically through the whole stack with through-substrate vias and arrays of bonding pads. Technical field: semiconductor devices, specifically a "high bandwidth flash" (HBF) memory built from a stack of bonded logic-and-memory die assemblies and the methods for forming it `[0001]`. The applicant frames this as the NAND analogue of the DRAM-plus-logic stacks the industry already builds.

## 종래 문제 / 과제

The background the patent itself states is minimal: flash memory means NAND and NOR devices, conventionally formed by depositing memory layers over a driver circuit on a single silicon wafer `[0002]`. That monolithic, single-wafer framing is the implicit baseline the rest of the disclosure works against: a memory array and its control logic share one process flow, which couples their fabrication and caps how much capacity and bandwidth one die can deliver. The disclosure's own stated motivations — increased bandwidth and capacity `[0055]`, low manufacturing cost `[0056]`, and shorter control paths / reduced control-signal delay `[0188]` — define the problems by what the architecture is said to improve.

**Quotable spans:**
- `[0002]`: "Flash memory devices include NAND and NOR memory devices. Such memory devices may be formed by sequentially depositing memory device layers over a driver circuit located on a silicon wafer."
- `[0188]`: "the relatively long electrically conductive paths between the system level logic die 3000 and the dedicated memory-controller die 700 may be used for system level control commands rather than for control of each memory cell, which reduces control signal delay"

## 청구항 분석 — 4-layer core mechanism

### Layer 1 — What (one sentence)

A semiconductor structure made of a vertical stack of bonded assemblies, where each assembly is one memory die (a 3D NAND/NOR array with vertical semiconductor channels) bonded to its own dedicated memory-controller die, and every neighboring pair of assemblies is bonded through arrays of bonding structures so that electrically conductive paths run vertically from the bottom of the bottommost assembly to the top of the topmost assembly `[0174]`.

### Layer 2 — How (mechanism)

1. Fabricate a memory die (900) — a 3D NAND/NOR array: alternating insulating/conductive layers (32/46), vertical semiconductor channels (60) and memory stack structures (55), through-stack via structures (486), and front bonding structures (198) `[0110]`, `[0113]`.
2. Separately fabricate a memory-controller die (700) on its own wafer — a memory controller circuit (720) that controls *that* memory die's array, plus through-substrate vias (716) and mirror-image front bonding structures (798) `[0114]`, `[0115]`, `[0121]`.
3. Bond one memory die (900) to one memory-controller die (700) — pad-to-pad, metal-to-metal (copper-to-copper), optionally with dielectric-to-dielectric hybrid bonding — to form a unit bonded assembly (1000). Bonding can be wafer-to-wafer, die-to-wafer, or die-to-die `[0122]`, `[0125]`.
4. Stack and bond multiple unit assemblies (1000) to each other through paired arrays of bonding structures, using metal-to-metal OR solder-mediated bonding, by chip-to-chip (assembly-to-assembly) OR wafer-to-wafer bonding to reduce cost `[0055]`, `[0056]`.
5. The vertical stack of two or more assemblies is the high bandwidth flash memory stack (2000); conductive paths extend vertically through the whole stack (planes HP1 → HP2 → HP3) via the TSVs and bonding-pad arrays `[0153]`, `[0174]`, `[0179]`.
6. Optionally bond the stack to a system-level logic die (3000), an interposer (4000), and a packaging substrate (5000); because each memory die already has a dedicated controller, the system logic die handles system-level commands rather than per-cell control `[0158]`, `[0159]`, `[0188]`.

**Key components**: memory die 900, memory-controller die 700, memory controller circuit 720, unit bonded assembly 1000, through-stack via structure 486, through-substrate via (TSV) structure 716, memory-die front bonding structures 198, controller-die front bonding structures 798, memory-die/controller-die backside bonding structures 128/728, solder material portions 25, high bandwidth flash memory stack 2000, system level logic die 3000, interposer 4000, packaging substrate 5000.

### Layer 3 — Why novel

- **Relative to prior art**: The patent's own background only recites the monolithic single-wafer flash baseline (array deposited over a driver circuit on one wafer) `[0002]`. The disclosed move is to split the array and its controller onto separate, separately optimized dies, bond them one-to-one into an assembly, and then stack assemblies with bottom-to-top vertical interconnect — replacing one big die with a stack of bonded specialist pairs.
- **Industry practice contrast** (external — needs verification): structurally this is the move high-bandwidth memory (HBM) made for DRAM-plus-logic — vertically stacked dies wired with TSVs — applied to NAND flash. The patent names the result "high bandwidth flash." (The HBM parallel is industry context, not stated in the patent, and is flagged in fact-check-log.md.)

### Layer 4 — Innovation angles

- **packaging-grammar-moat**: the breadth of the independent *structure* claim — it reads on essentially any stack of (dedicated-controller + memory) bonded assemblies with bottom-to-top vertical paths, regardless of the exotic process details.
  - Evidence paragraphs: `[0174]`, `[0003]`, `[0055]`
  - Quote anchor refs: `q-0174-1`, `q-0174-2`, `q-0055-2`
- **dedicated-per-die-controller**: every memory die carries its own controller, so the system logic die is freed from per-cell control — the architectural choice that distinguishes the claim from a single shared controller.
  - Evidence paragraphs: `[0188]`, `[0055]`, `[0159]`
  - Quote anchor refs: `q-0188-1`, `q-0188-2`, `q-0055-1`
- **manufacturing-optionality**: separate NAND and CMOS wafers, then chip-to-chip OR wafer-to-wafer bonding, metal-to-metal OR solder — defensibility living in process optionality and cost rather than one exotic step.
  - Evidence paragraphs: `[0056]`, `[0171]`, `[0176]`
  - Quote anchor refs: `q-0056-1`, `q-0056-2`, `q-0176-1`
- **claim-exposure-risk** (counter-angle, feeds adversarial defense): the short method claim (15) is bond-bond-stack and is the kind of broad independent claim most exposed to prior-art narrowing; the obvious design-arounds (monolithic stacking; one shared controller) are namable.
  - Evidence paragraphs: `[0004]`, `[0188]`
  - Quote anchor refs: `q-0004-1`, `q-0188-1`

## Reference number table

| Number | Label | Paragraphs | Figures |
|---|---|---|---|
| 9 | Carrier substrate | `[0057]`, `[0127]` | FIG. 1, FIG. 17, FIG. 21 |
| 32 / 46 | Insulating layers / electrically conductive layers (alternating stack) | `[0062]`, `[0100]`, `[0113]` | FIG. 17, FIG. 21 |
| 54 / 55 | Memory material layer / memory stack structure | `[0083]`, `[0113]` | FIG. 17, FIG. 21 |
| 60 | Vertical semiconductor channel | `[0082]`, `[0174]` | FIG. 17, FIG. 21 |
| 486 | Through-stack via structure | `[0104]`, `[0113]`, `[0184]` | FIG. 17, FIG. 21 |
| 198 | Memory-die front bonding structures | `[0111]`, `[0122]`, `[0178]` | FIG. 17, FIG. 20, FIG. 21 |
| 900 | Memory die | `[0112]`, `[0113]`, `[0174]` | FIG. 17, FIG. 21, FIG. 33 |
| 700 | Memory-controller die | `[0120]`, `[0121]`, `[0174]` | FIG. 20, FIG. 21, FIG. 33 |
| 709 | Logic-die / controller-die semiconductor substrate | `[0114]`, `[0175]` | FIG. 20, FIG. 21, FIG. 33 |
| 716 | Through-substrate via (TSV) structure | `[0118]`, `[0175]`, `[0186]` | FIG. 20, FIG. 21, FIG. 33 |
| 720 | Memory controller circuit | `[0114]`, `[0115]`, `[0174]` | FIG. 20, FIG. 21 |
| 798 | Controller-die front bonding structures | `[0120]`, `[0122]`, `[0178]` | FIG. 20, FIG. 21 |
| 1000 | Unit bonded assembly | `[0122]`, `[0165]`, `[0174]` | FIG. 21, FIG. 33 |
| 128 / 728 | Memory-die / controller-die backside bonding structures | `[0132]`, `[0141]`, `[0180]` | FIG. 21, FIG. 33 |
| 25 | Solder material portions | `[0143]`, `[0153]`, `[0182]` | FIG. 33 |
| 2000 | High bandwidth flash memory stack | `[0153]`, `[0157]`, `[0174]` | FIG. 33, FIG. 36A, FIG. 36B |
| 3000 | System level logic die | `[0158]`, `[0159]`, `[0188]` | FIG. 36A, FIG. 36B |
| 4000 | Interposer | `[0158]`, `[0162]` | FIG. 36A, FIG. 36B |
| 5000 | Packaging substrate | `[0158]`, `[0162]` | FIG. 36A, FIG. 36B |

## Figure relationships

| Figure | Paired with | Relationship | Notes |
|---|---|---|---|
| FIG. 17 | FIG. 20 | conceptual "two halves" pair (finished memory die + finished controller die) | each is a standalone cross-section; together they are the two dies that bond into FIG. 21 |
| FIG. 21 | (builds on 17 + 20) | composition figure — the unit bonded assembly = memory die (900, top) bonded to controller die (700, bottom) | the "atom" of the invention |
| FIG. 32 | FIG. 33 | sibling stack figures | FIG. 32 = vertical stack of two assemblies; FIG. 33 = vertical stack of three assemblies (solder-bonded); same family, different assembly count |
| FIG. 36A | FIG. 36B | same-page sub-figure pair (paragraph `[0041]`, `[0158]`) | 36A = HBF stack on logic die on interposer on substrate (vertical tower); 36B = HBF stack and logic die side-by-side on the interposer |
| FIG. 1 | (standalone) | early in-process memory-die cross-section (carrier substrate, stepped alternating stack) | manufacturing-stage, not a finished product |

> Note: FIG. 32/33 captions in the specification describe "two" and "three" bonded assemblies respectively `[0149]`, `[0150]`. These counts describe the specific illustrated embodiments only. The claims recite "a plurality of stacked bonded assemblies" with NO numeric stack count — do not generalize two/three into a claimed quantity.

## Quote anchor table

| Quote ID | Paragraph | Verbatim text | Significance |
|---|---|---|---|
| q-0002-1 | `[0002]` | "Flash memory devices include NAND and NOR memory devices. Such memory devices may be formed by sequentially depositing memory device layers over a driver circuit located on a silicon wafer." | prior-art-contrast |
| q-0003-1 | `[0003]` | "a semiconductor structure comprises a plurality stacked bonded assemblies" | claim-supporting |
| q-0004-1 | `[0004]` | "a method of forming a semiconductor includes bonding a first memory die to a first memory-controller die to form a first bonded assembly, bonding second memory die to a second memory-controller die to form a second bonded assembly, and bonding the first bonded assembly to the second bonded assembly to form a memory stack" | claim-supporting |
| q-0055-1 | `[0055]` | "The logic dies may comprise memory-controller dies which control the respective memory die that is bonded to the respective memory-controller die in the same bonded assembly." | mechanism-critical |
| q-0055-2 | `[0055]` | "The bonded assemblies may then be stacked and bonded to each other using TSVs and bonding pads on opposing sides of each bonded assembly." | mechanism-critical |
| q-0055-3 | `[0055]` | "The stack of bonded assemblies provide increased bandwidth and memory capacity." | claim-supporting |
| q-0055-4 | `[0055]` | "The memory dies may comprise flash memory dies, such as flash memory dies containing three-dimensional NAND or NOR memory devices." | mechanism-critical |
| q-0056-1 | `[0056]` | "The bonded assemblies may be bonded to each other in a stack using chip to chip (i.e., assembly to assembly) bonding or wafer-to-wafer bonding to reduce production costs." | mechanism-critical |
| q-0056-2 | `[0056]` | "The stack of multiple bonded assemblies of the embodiments of the present disclosure provides a high bandwidth bonded flash memory chip array at a low manufacturing cost." | claim-supporting |
| q-0056-3 | `[0056]` | "A metal-to-metal bonding or a solder-mediated bonding may be employed to bond vertically neighboring pairs of bonded assemblies." | mechanism-critical |
| q-0115-1 | `[0115]` | "The memory controller circuit 720 is configured to control operation of the memory array within the memory die 900." | mechanism-critical |
| q-0122-1 | `[0122]` | "The bonding between mating pairs of a respective memory die 900 and a respective memory-controller die 700 may be performed employing a wafer-to-wafer bonding process" | mechanism-critical |
| q-0153-1 | `[0153]` | "Each vertical stack of two or more bonded assemblies 1000 constitutes a high bandwidth flash memory stack 2000." | claim-supporting |
| q-0159-1 | `[0159]` | "The system level logic die 3000, if present, controls the operation of the memory-controller dies 700 in each bonded assembly 1000 of the high bandwidth flash memory stack 2000." | mechanism-critical |
| q-0171-1 | `[0171]` | "The metal-to-metal bonding may comprise wafer to wafer bonding, die to wafer bonding or die to die bonding." | mechanism-critical |
| q-0172-1 | `[0172]` | "No solder material is present between any vertically neighboring pair of a memory die 900 and a memory-controller die 700 within the entirety of the high bandwidth flash memory stack 2000." | mechanism-critical |
| q-0174-1 | `[0174]` | "a semiconductor structure (2000, 3000, 4000) comprises a plurality of stacked bonded assemblies 1000" | claim-supporting |
| q-0174-2 | `[0174]` | "Each vertically neighboring pair of bonded assemblies 1000 of the plurality of bonded assemblies 1000 is bonded to each other through a respective pair of arrays of bonding structures (198, 798) such that electrically conductive paths vertically extend from a first horizontal plane HP1 including a bottom surface of a bottommost bonded assembly 1000 of the plurality of bonded assemblies 1000 at least to a second horizontal plane HP2 including a bottom surface of a topmost bonded assembly 1000 of the plurality of bonded assemblies 1000." | claim-supporting |
| q-0176-1 | `[0176]` | "Therefore, the chips can be stacked using micro-bumps or by direct metal-to-metal bonding to form the flash memory stack 2000 using a lower cost, simplified method." | claim-supporting |
| q-0188-1 | `[0188]` | "Each bonded assembly 1000 chip includes a dedicated memory-controller die 700, and the system level logic die 3000 is not required to directly control the operation of each memory cell in each of the memory dies 900." | mechanism-critical |
| q-0188-2 | `[0188]` | "the relatively long electrically conductive paths between the system level logic die 3000 and the dedicated memory-controller die 700 may be used for system level control commands rather than for control of each memory cell, which reduces control signal delay" | mechanism-critical |

> Verbatim discipline note: stored text is post-allowed-normalization (markdown `**bold**` reference-number markers stripped; e.g. patent's `**700**` is stored as `700`). Phase 3 Edit Pass 3 applies the same bold-strip / NBSP / smart-quote normalization to both sides before string-matching, so these are exact matches against `input/patent.md`.

## Timeline

- **Priority (provisional) date**: 2024-06-28 (US 63/665,731)
- **Filing date (non-provisional)**: 2024-08-21
- **Publication date**: 2026-01-01
- **Examination period**: not applicable — published application, not yet granted. Time from filing to publication ≈ 498 days (2024-08-21 → 2026-01-01).
- **Prior-art chronology**: No prior-art references are cited in the body of `input/patent.md` (the source is the US specification + claims; no examiner search report / cited-references list is present in the provided text). Cited-reference analysis therefore cannot be grounded from this source — see Prior-art section below. Any competitor/prior-art comparison is EXTERNAL (fact-check-log.md).

## Prior-art references + differentiation

- **No in-text prior-art citations.** `input/patent.md` contains no cited-reference list and no `[XXXX]`-anchored prior-art discussion beyond the one-sentence background at `[0002]` (monolithic single-wafer NAND/NOR). The Axis-4 baseline must therefore be sourced externally (the HBM / CMOS-bonded-array / die-to-die-bonding industry baseline) and is logged in fact-check-log.md as needs-verification.
- **Internal baseline (patent-anchored)**: the monolithic, single-wafer flash construction at `[0002]` — "memory device layers over a driver circuit located on a silicon wafer" — is the one baseline the patent itself states, and the dedicated-controller + stacked-bonded architecture is the differentiation.

## 유리한 효과 + 정량 데이터

The disclosure states three advantages: (1) increased bandwidth and memory capacity from stacking bonded assemblies `[0055]`; (2) low manufacturing cost, enabled by wafer-to-wafer or chip-to-chip bonding and by stacking via micro-bumps or direct metal-to-metal bonding `[0056]`, `[0176]`; and (3) reduced control-signal delay, because each memory die has a dedicated controller and the long paths to the system logic die carry only system-level commands `[0188]`.

**Quotable spans:**
- `[0055]`: "The stack of bonded assemblies provide increased bandwidth and memory capacity."
- `[0056]`: "The stack of multiple bonded assemblies of the embodiments of the present disclosure provides a high bandwidth bonded flash memory chip array at a low manufacturing cost."
- `[0188]`: "Each bonded assembly 1000 chip includes a dedicated memory-controller die 700, and the system level logic die 3000 is not required to directly control the operation of each memory cell in each of the memory dies 900."

| Metric | Value | Paragraph |
|---|---|---|
| Word-line / layer repetitions per memory die (alternating-stack levels) | 8 to 1,024 (example 32 to 256) — embodiment range, NOT a stack-of-assemblies count | `[0063]` |
| Number of stacked bonded assemblies | NOT claimed / NOT specified (illustrated embodiments show two and three; claim recites only "a plurality") | `[0149]`, `[0150]`, `[0174]` |
| Bandwidth / capacity gain | Qualitative ("increased"); no number disclosed | `[0055]` |
| Manufacturing cost | Qualitative ("low" / "lower cost"); no number disclosed | `[0056]`, `[0176]` |
| Control-signal delay | Qualitative ("reduces"); no number disclosed | `[0188]` |

> Guardrail note: the patent discloses NO quantitative bandwidth figure, NO stack-of-assemblies count, and NO bonding pitch. The only numeric ranges are layer/word-line counts and process dimensions. Do not invent stack counts or bandwidth numbers in the essay.

## Claims structure (independent vs dependent)

- **Claim 1 — independent STRUCTURE claim** (`[0174]` is its description-side restatement): a plurality of stacked bonded assemblies, each = memory die (3D array + vertical channels) + memory-controller die (controller circuit controlling that array), neighbors bonded through paired bonding-structure arrays with bottom-to-top vertical conductive paths. This is the broad claim; breadth is the strength, unexamined status is the risk.
- **Claims 2–14 — dependent on claim 1** (structure): add TSVs as part of the conductive paths (2), bottom/top bonding structures (3), the alternating memory/controller orientation (4), front bonding structures + metal-to-metal bonding (5, 6), paths to top plane HP3 (7), backside dielectric + bonding structures (8), backside metal-to-metal (9) or solder (10, 11) inter-assembly bonding, NAND/NOR memory-die internals (12), controller-die internals incl. TSVs (13), and the optional system-level logic die via solder or interposer (14).
- **Claim 15 — independent METHOD claim** (`[0004]` is its summary restatement): bond memory die to controller die (×2 assemblies), then bond the two assemblies into a stack. Short bond-bond-stack claim — the most prior-art-exposed independent claim.
- **Claims 16–20 — dependent on claim 15** (method): wafer-level fabricate-then-dice (16), form TSVs in controllers (17), NAND/NOR + metal-to-metal die bonding + bottom-to-top paths + bottom/top bonding structures (18), inter-assembly bonding by solder after dicing (19) OR by metal-to-metal bonding (20).
