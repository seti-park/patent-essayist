# Pixel pipeline spec (deterministic half)

Everything after the vision decisions is fixed arithmetic in `scripts/crop.py` +
`scripts/process_figures.py`. Parameters (in `CropConfig`, chosen and validated upstream in
patent-essay-pipeline on the US12636684B1 / US20240370522A1 batches):

| Parameter | Value | Meaning |
|---|---|---|
| `ink_threshold` | 200 | grayscale < 200 counts as ink |
| `min_ink_density` | 2 | a row/column needs ≥2 ink px to count (kills scan speckle) |
| `edge_shave_px` | 1 | shrink the bbox 1 px per side (kills a continuous 1-px frame line) |
| `pad_fraction` | 0.10 | margin = round(max(h, w) × 0.10) on all four sides |
| dpi | 300 | written into the PNG `pHYs` metadata |
| mode | `L` | grayscale — USPTO/WO drawings are B&W; color is out of scope |

Step order per figure:

1. **load** — PIL open; if the image has alpha (RGBA/LA/palette-transparency), composite
   onto WHITE before `.convert("L")`. Transparent pixels often store RGB(0,0,0); a naive
   grayscale convert turns them into ink and corrupts the bbox → asymmetric padding.
2. **rotate** — `rotate` degrees clockwise from the trim spec, if present (sideways-printed
   figure body only; native orientation is the default).
3. **edge trim** — slice off `int(dimension × fraction)` per named side, in the
   post-rotation frame. Pure array slicing; no heuristics.
4. **tight_crop** — bbox over rows/cols having ≥ `min_ink_density` ink pixels, then shave
   `edge_shave_px`; an all-white image is returned unchanged.
5. **pad** — paste onto a white canvas with a uniform margin of `pad_fraction` of the
   LONGER side. Using one baseline (not per-axis) gives portrait and landscape figures the
   same absolute margin, so a mixed set frames consistently.
6. **save** — `fig-<label>.png`, grayscale, `dpi=(300, 300)`, `optimize=True`.

Label derivation: trailing `digits[+letters]` before the input extension; digits
zero-padded to 2, letters uppercased (`fig-2.png → fig-02.png`, `fig-03a.jpg → fig-03A.png`,
`12636684-7.png → fig-07.png`); otherwise `unknown-NN.png`. `--index` additionally writes
the distinct figure NUMBERS, sorted, one per line — the `figures-index.txt` format
`run_gates.py --figures` consumes.

Quality signal (from the source repo's symmetry check): after processing, per-side ink
margins should match within ~1% of the dimension (top≈bottom, left≈right). A visibly
asymmetric result means a wrong trim fraction or missed alpha — fix the JSON, re-run.
