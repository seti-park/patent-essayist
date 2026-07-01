# Figure Selection

## Selected figures

| Figure | File | Thesis point (spine element / section) | caption_role |
|---|---|---|---|
| FIG. 1 | fig-01.png | System architecture overview — VCSEL, SPAD arrays, and the histogram processing circuit as one signal path (2-problem → 3-core-claim transition) | header_composite |
| FIG. 2 | fig-02.png | Histogram processing circuit exploded view — correlator, phase/bin computation, range/rate calculators as the "read each bar the instant it arrives" mechanism (4-analogy) | body_figure_carries_unique_info |

## Not selected (and why)

Only 7 figure assets exist (`input/figures/fig-01.png` … `fig-07.png`), matching the patent's own FIG. 1–7. Per essay-context.md: "Not every figure needs use — select for audience accessibility, but do not orphan any figure you do select." FIG. 3–7 are excluded, not orphaned, for these reasons:

- **FIG. 3** (crosstalk calibration flowchart): circuit/calibration-math detail (LUT coefficients, leaky integrators, 10000:1 dynamic range) that is below this article's audience floor (general tech-curious, high-school-to-early-undergrad) and outside the mechanism this article owns (peak = distance). Crosstalk mitigation is a real but secondary capability — mentioning it in prose (if at all) does not require its own figure.
- **FIG. 4** (correlator circuit detail — AMB/Filter/Crosstalk MAC, closest-target, strongest-maximum): this is the correct *structural* content for the 4-analogy beat, but at implementation-diagram density (11 sub-blocks, signal names like CORR_AMB/CORR_HIST/CORR_XTALK) it would overwhelm the target reader. FIG. 2's coarser exploded view carries the same "your zone's bar chart gets read as it streams" idea at the right resolution; FIG. 4's content is folded into FIG. 2's rationale and can be referenced in prose without its own image.
- **FIG. 5** (bin-serial processing flowchart): a process view of the FIG. 4 correlator circuit already excluded above — redundant with FIG. 2 for this audience's purposes.
- **FIG. 6** (phase/bin computation circuit detail): same density problem as FIG. 4, for the median-phase/zero-crossing sub-mechanism, which is deeper implementation detail than this article's "peak = distance" definition needs.
- **FIG. 7** (on-the-fly median estimation flowchart): a process view of the FIG. 6 circuit already excluded above.

This is a deliberate audience-accessibility selection, not a coverage gap: the patent's full mechanism (crosstalk removal, dual closest/strongest peak-finding, median-phase interpolation) is still summarized in prose in `invention-summary.md` Layer 2 and can be referenced narratively in the essay without requiring FIG. 3–7 as image assets. FIG. 1 and FIG. 2 alone carry the system-level story this article needs (per essay-context.md: "FIG. 1 and FIG. 2 are the strongest header candidates given the mechanism thesis").

## Paired-figure relationships (acknowledged)

Per `invention-summary.md` §"Figure relationships": this patent has no same-page sub-figure pairs (no "FIG. NA/NB" labels appear). The relevant structure is a hierarchy, not a pair:

| Figure(s) | Relationship | Treatment in selection |
|---|---|---|
| FIG. 1 | standalone (system level) | selected as header composite |
| FIG. 2 | exploded view of FIG. 1's block 114; zoom source for FIG. 4 and FIG. 6 | selected as body figure |
| FIG. 4, FIG. 6 | detail-zooms of two of FIG. 2's sub-blocks | NOT selected — density exceeds audience floor; content folded into FIG. 2's rationale narratively |
| FIG. 3 | standalone flowchart (crosstalk calibration) | NOT selected — secondary capability, below mechanism-thesis floor |
| FIG. 5, FIG. 7 | process views of FIG. 4 / FIG. 6 respectively | NOT selected — redundant with already-excluded structural figures |

No pair is being broken (there are no pairs in this patent) — this is a hierarchy-level selection (system + one exploded view, stopping before the two further detail-zooms), acknowledged and intentional. Flagged in `phase2-handoff-notes.md` so Phase 2 does not reopen the FIG. 3–7 exclusion.

## Header / body assignment

- **Header**: FIG. 1 (system architecture composite — the reader's first look at "what's actually in this tiny sensor," anchoring the technical-impossibility hook's resolution)
- **Body**: FIG. 2 (histogram processing circuit — carries the bin-serial-streaming mechanism visually for the analogy section)

<!-- No revision note: figure selection matched the spine's pre-planned 2-problem /
     3-core-claim / 4-analogy sections without requiring a spine update (Step 9 confirmed
     rather than revised Step 8's plan). -->
