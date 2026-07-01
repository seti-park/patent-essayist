# Figure Rationale

## FIG. 1 — Time-of-flight sensor system block diagram

- **Purpose**: Shows the VCSEL (102) / VCSEL driver (104) emitting light, the return SPAD array (106) and reference SPAD array (108) catching photons, the two OR trees (110, 112) combining them, and everything funneling into the histogram processing circuit (114) — alongside the MCU (116), I/O interface (118), power management (120), and OTP memory (122) that round out the whole sensor package. All of this in one diagram, at a scale a general reader can parse without prior chip-design knowledge.
- **Intended effect**: This is the reader's first concrete look at "what's actually inside a sensor this small" — it resolves the hook's implicit question (how does a tiny chip do this?) by showing that the whole light-emit / photon-catch / histogram-crunch pipeline lives on one small block diagram, not a rack of external processing hardware. It primes the reader for the "this is lean by design, not by accident" thesis before the mechanism section unpacks *how* the histogram block stays lean. (caption_role: header_composite — detailed caption walking through VCSEL → SPAD arrays → histogram processing circuit as one path.)

## FIG. 2 — Histogram processing circuit block diagram

- **Purpose**: Opens up block 114 from FIG. 1 into its working parts — the correlator circuit (202), phase/bin computation circuit (204), range calculation circuit (206), rate calculation circuit (208), and crosstalk histogram generator (218) — showing the reference/return histogram and crosstalk histogram flowing in, and a median range flowing out. This is the diagram that carries the "bar chart in, distance out" idea structurally.
- **Intended effect**: Makes the essay's core analogy (every zone gets its own bar chart; the chip reads each bar as it streams past, instead of holding the whole chart in memory) visually concrete rather than purely verbal. The reader sees discrete circuit blocks doing discrete jobs on the histogram data — which supports the claim that this is a hardware pipeline built for streaming, not a general-purpose processor churning through stored data. Because this figure carries real information load (five labeled sub-blocks, a clear data flow), the caption should be a medium-length, information-bearing caption naming what flows where — not just an identifier. (caption_role: body_figure_carries_unique_info.)

## Figures reviewed but not selected — brief rationale carried forward

Per `figure-selection.md`, FIG. 3–7 were reviewed against the paired-figure/hierarchy table in `invention-summary.md` and excluded for audience-accessibility reasons (implementation-diagram density above this article's floor), not orphaned. Their structural content (crosstalk calibration compactness, dual closest/strongest peak-finding, median-phase zero-crossing interpolation) remains available for prose reference from `invention-summary.md` Layer 2 without requiring their own image assets. See `figure-selection.md` "Not selected (and why)" for the per-figure reasoning; not repeated here to avoid duplication drift between the two files.

<!-- No revision note this run. -->
