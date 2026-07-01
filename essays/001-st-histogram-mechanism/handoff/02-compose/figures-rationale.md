# Figures Rationale (Compose placements)

## FIG. 1 — header

- **Placement**: header
- **Rendering**: image-plus-caption
- **caption_role**: header_composite
- **Caption (as written)**: "FIG. 1: the ToF sensor system (100). The VCSEL (102) and VCSEL driver (104) emit the light pulse; the return SPAD array (106) and reference SPAD array (108) catch photons and feed two OR trees (110, 112) that combine per-SPAD signals into the reference and return histograms. Everything funnels into the histogram processing circuit (114), alongside the MCU (116), I/O interface (118), power management (120), and OTP memory (122) that round out the package."
- **Decision note**: matches Phase 1's figure-selection.md assignment (FIG. 1 = header, system-level composite) exactly — no placement deviation. Detailed caption per `figure-rendering.md`'s `header_composite` role (walks the full signal path, connects to the "what's actually inside a sensor this small" resolution of the §1 hook). Verified visually against the actual asset (`input/figures/fig-01.png`): all reference numbers named in the caption (102, 104, 106, 108, 110, 112, 114, 116, 118, 120, 122) are present and correctly labeled in the image.

## FIG. 2 — body, in §4 (analogy)

- **Placement**: body-after-section-4 (placed at the "Every Zone Gets Its Own Bar Chart" analogy section, where the bin-serial mechanism becomes visually concrete)
- **Rendering**: caption-only-italic
- **caption_role**: body_figure_carries_unique_info
- **Caption (as written)**: "FIG. 2: the histogram processing circuit, exploded. Reference/return histogram, crosstalk histogram, and window-start/end signals flow into the correlator (202) and phase/bin computation (204) circuits; range calculation (206) and rate calculation (208) turn the running bin-by-bin answer into median range and per-SPAD rate."
- **Decision note**: matches Phase 1's figure-selection.md assignment (FIG. 2 = body, `body_figure_carries_unique_info`) exactly. Medium-length caption (15-30 words target per `figure-rendering.md`) naming the actual data flow (five labeled sub-blocks: correlator 202, phase/bin computation 204, range calculation 206, rate calculation 208, crosstalk generator 218 — the caption covers 202/204/206/208 directly and folds 218's crosstalk-histogram output into the "crosstalk histogram... flow in" clause) rather than a short identifier-only caption, because the figure carries real information load the surrounding prose does not fully restate. Verified visually against the actual asset (`input/figures/fig-02.png`): all block labels and reference numbers named in the caption (202, 204, 206, 208, plus the ref/return histogram, crosstalk histogram, and window-start/end input labels, and the median-range output label) are present and correctly positioned in the image.

## Figures reviewed but not selected — no change from Phase 1

FIG. 3-7 remain excluded per Phase 1's figure-selection.md (audience-accessibility density reasons, not orphans). Compose did not reopen this exclusion, per phase2-handoff-notes.md's explicit instruction. No revision note.

## figures_locked confirmation

Per `_shared/references/caption-roles.md`, the figure set is now locked for this run: 2 figures used (FIG. 1 header, FIG. 2 body), both matching Phase 1's locked selection with zero placement deviation. `gate_figure_use.py` orphan-check against `figure-selection.md`'s actual **Selected figures** table (top of that file, listing only FIG. 1 and FIG. 2) confirms no orphans among the truly selected set — the gate's raw CLI output flags FIG. 3-7 as "orphans" only because it pattern-matches figure-number mentions anywhere in `figure-selection.md`'s prose, including the "Not selected (and why)" narrative section that discusses FIG. 3-7 specifically to explain their exclusion. This is a known false-positive mode of the current gate script (it does not distinguish the file's "Selected figures" table from its "Not selected" narrative section); flagged here for Phase 3 Edit's attention and as a candidate finding for the meta-loop (`pipeline-retro`) to route toward a `gate_figure_use.py` parsing fix.
