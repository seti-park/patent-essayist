# Figure source map (essay-local numbering)

Two patents share most architecture drawings, and the deterministic gates parse figure
references as **integers**. To avoid figure-number collisions across the two documents, the
run uses a single **essay-local** numbering (Figure 1..6). Each maps to one source drawing
below. **Caption rule for this run:** in the essay, cite a figure's source by *patent
shorthand + paragraph anchor* (e.g. "the '885 application, [0148]"), **never** by writing the
source "FIG. N" token — a literal `FIG. 10` in the prose would be read by the anchor gate as a
reference to essay-figure 10, which does not exist. The only `Figure N` tokens allowed in the
draft are the essay-local numbers 1-6.

Shorthand: **'885** = US20250322885A1 (Always-On Bit Lines). **'143** = US20250279143A1
(Discharge-Free Read).

| Essay | File | Source | Shows | Key anchors | Suggested role |
|---|---|---|---|---|---|
| **Figure 1** | fig-01.png | '143 FIG. 9 | A central GPU ringed by eight HBF (High Bandwidth Flash) packages — the system HBF is built to sit in. | `[0019]`, `[0073]` ('143) | orientation |
| **Figure 2** | fig-02.png | '143 FIG. 6 | One NAND string during sensing: bit line on top (VBL), the selected word line at the read reference (SLCR), the *unselected* word lines held at read-pass VREAD, source line at 0 V. Establishes column (bit line) vs row (word line). | `[0146]` ('143) | mechanism |
| **Figure 3** | fig-03.png | '885 FIG. 9 | Conventional read timing across three blocks. The bit-line trace (BLs) visibly **discharges and recharges** between every block read (labeled BL DISCHARGE / BL RECHARGE). The cost being removed. | `[0148]` ('885, as the FIG. 9 baseline) | contrast |
| **Figure 4** | fig-04.png | '885 FIG. 10 | Always-on timing. Bit lines stay **flat at VBL≈0.2 V** across all three reads; only a tiny settling blip per read ("NO BL DISCHARGE/RECHARGE, ONLY BL SETTLING TIME"). The column-axis fix. | `[0147]`, `[0148]` ('885) | evidence |
| **Figure 5** | fig-05.png | '143 FIG. 8A | Discharge-free timing. Across two successive reads the **unselected word lines (WL_U) hold flat at VREAD** and never discharge; only the selected line and bit line move. The row-axis counterpart to Figure 4. | `[0162]`, `[0168]`, `[0178]` ('143) | evidence |
| **Figure 6** | fig-06.png | '143 FIG. 10 | Adaptive-trigger flowchart: run normal reads → **detect that N reads occurred within time T** → switch into the non-discharging mode → keep word lines up between reads. The mode is triggered by a read burst, not always on. | `[0181]`, `[0182]` ('143) | mechanism |

## Verified cite-safe numbers (from the filings' own specifications)

- '885 [0147]: bit lines held at **VBL ≈ 0.2 V**, never falling by more than **25%** (i.e. not
  below ~0.15 V) during or between reads; holding them eliminates the discharge + recharge time
  and reduces tRead. Bit lines held "indefinitely" even with no pending read.
- '885 [0148] / FIG. 10: between reads there is only a brief settling time, **"less than 1
  microsecond,"** vs the full discharge/recharge of FIG. 9; bit lines "can be considered to be
  'always on.'" '885 FIG. 10 labels VBL≈0.2 V and VSG≈5 V.
- '143 [0047], [0156], [0179]: a **"non-discharging read"** mode keeps unselected word lines at
  read-pass **VREAD** and does not discharge them between reads, reducing read time tR and so
  increasing HBF bandwidth.
- '143 [0181]-[0182] / FIG. 10: device starts in a normal (discharging) mode and **switches**
  to non-discharging after detecting a predetermined read count N within an interval T.
- '143 FIG. 6 labels its own embodiment VBL = 1.2 V — a **different** number from '885's 0.2 V.
  Do NOT conflate the two patents' example voltages.
