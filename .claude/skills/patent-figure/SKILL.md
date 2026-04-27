---
name: patent-figure
description: Clean up patent-office figure images and (optionally) assemble multiple figures into a 5:2 publication header (3890x1556). Layer 1 — remove the meta-info header band, tight-crop, pad. Layer 2 — detect each "Fig. N" label, normalise figures by label height, compose horizontally, fit to canvas. Invoke when the user shares one or more patent figures (PNG/JPEG) and asks to crop, remove the "U.S. Patent / Sheet N of M / publication number" header, tidy a patent drawing, build a 5:2 essay header from several figures, or uses Korean phrasings like "특허 도면 정리/크롭/헤더 제거" or "특허 도면 헤더 만들기".
---

# Patent Figure Cleanup + Header Assembly

Two-layer pipeline:

```
Layer 1 (crop.py)        load -> orient -> trim_header -> tight_crop -> pad
Layer 2 (assemble.py)    [layer1] -> find_label_bbox -> normalize_by_label
                                  -> compose_horizontal -> fit_to_canvas
```

Validated on real USPTO portrait + landscape sheets across multiple
resolutions (1500–3500 px). Single default config handles them all; tune
only on regression. Layer 2 raises `LabelDetectionError` when a label
cannot be found — there is no silent fallback.

## When to invoke

The user supplies one or more patent figure images and wants either:

- **Layer 1 only** — clean a single image (header trim + tight crop + pad).
  Phrasings: "crop this patent figure", "remove header", "특허 도면 정리".
- **Layer 1 + 2** — produce a 5:2 publication header from 1–4 figures.
  Phrasings: "build a header image from these figures", "essay header
  만들어줘", "5:2 헤더 조립".

## How to run

The skill ships four files in this folder:

| file | purpose |
|---|---|
| `crop.py`         | Layer 1 pure stages |
| `assemble.py`     | Layer 2 pure stages |
| `crop_figure.py`  | CLI: clean a single figure |
| `build_header.py` | CLI: clean N figures + assemble header |

### Step 1 — make sure dependencies are present

```bash
python -c "import PIL, numpy" 2>/dev/null || pip install --quiet pillow numpy
```

### Step 2 — Layer 1: clean a single figure

```bash
python /path/to/.claude/skills/patent-figure/crop_figure.py <input> [<output>]
```

Output is always PNG (lossless) regardless of input format. Reports:
```
input        : foo.png  shape=(2163, 1530)
orientation  : portrait
header trim  : side=top  cut=259px  band=(223, 258)
output       : foo.cropped.png  shape=(1933, 1275)
```

### Step 3 — Layer 1 + 2: assemble a 5:2 header

```bash
python /path/to/.claude/skills/patent-figure/build_header.py \
    out_header.png  fig1.png  fig2.png  [fig3.png  [fig4.png]]
```

Each input is cleaned via Layer 1, then Layer 2 detects each "Fig. N"
label, scales figures so all label heights match the median, composes them
left-to-right with a 120 px gutter and centre alignment, and fits the
strip onto the 3890×1556 canvas with 220 px side margin. Reports:
```
  cleaned  IMG_2362.png  -> shape=(1757, 1217)
  cleaned  IMG_2363.png  -> shape=(1922, 1272)
  cleaned  IMG_2364.png  -> shape=(1928, 1263)

label heights      : [44, 44, 43]
target label height: 44
canvas             : 3890x1556
output             : out_header.png
```

### Programmatic use

```python
import sys
from pathlib import Path
sys.path.insert(0, "/path/to/.claude/skills/patent-figure")

from crop import CropConfig, load, process, save
from assemble import AssembleConfig, build_header

# Layer 1
arr = load(Path("input.png"))
cleaned, _ = process(arr, CropConfig())

# Layer 2 (single figure -> just label detection)
from assemble import find_label_bbox
bbox = find_label_bbox(cleaned, AssembleConfig(), source="input.png")

# Layer 1 + 2 (multi-figure header)
figs = [process(load(p), CropConfig())[0] for p in [Path("a.png"), Path("b.png")]]
header, report = build_header(figs, AssembleConfig(),
                              sources=["a.png", "b.png"])
save(header, Path("header.png"))
```

## Failure policy

`assemble.find_label_bbox` raises `LabelDetectionError` (subclass of
`ValueError`) on any of these conditions, with a message that names the
source image, the parameter values used, and the specific reason:

- empty search region
- no ink rows in the search region
- no inked columns in the candidate band
- no column cluster wide enough to be text
- detected vspan or hspan outside the configured ranges

When this happens, **do not retry with a fallback height** — investigate
the failure (e.g. by inspecting the cleaned image around the label band)
and either fix the input, adjust `AssembleConfig` for that layout, or
reject the document. Silent fallbacks have caused aspect-ratio bugs to
slip into published headers; that is the reason for the hard-fail rule.

## Tunable parameters

### `CropConfig` (Layer 1)

| field | default | bump up when… | bump down when… |
|---|---|---|---|
| `ink_threshold` | 200 | grayscale watermark bleeds in | very faint scans miss text |
| `max_header_fraction` | 0.18 | header > 18% of edge | aggressive crops eat figure |
| `min_gap_px` | 8 | multi-line headers w/ wide gaps | high-res scans need sensitivity |
| `pad_fraction` | 0.07 | want roomier slide layout (≤0.10) | tighter inserts (≥0.05) |
| `min_ink_density` | 2 | speckled scans cause false ink rows | sparse figures lose thin lines |
| `edge_shave_px` | 1 | thicker browser frames | every pixel of content matters |

### `AssembleConfig` (Layer 2)

| field | default | meaning |
|---|---|---|
| `label_search_frac` | 0.30 | fraction of cleaned-image height scanned for the bottom label |
| `label_row_gap_px` | 20 | initial row-grouping gap |
| `label_refine_row_gap_px` | 8 | refinement gap; isolates the label from a section indicator like "b-b" sitting one line above |
| `label_min_col_density` | 2 | min ink count per column inside the label band |
| `label_max_inter_glyph_gap_px` | 50 | larger than a "Fig." → "1c" space; smaller → label gets split |
| `label_min_text_cluster_px` | 50 | min cluster width; below → discarded as artifact |
| `label_vspan_range` | (40, 200) | sanity range for label height in pixels |
| `label_hspan_range` | (50, 600) | sanity range for label width |
| `figure_gutter_px` | 120 | gap between figures in the strip |
| `canvas_size_px` | (3890, 1556) | 5:2 publication canvas |
| `canvas_side_pad_px` | 220 | minimum side margin on the canvas |

## Algorithm at a glance — Layer 2 label detection

1. Scan the bottom `label_search_frac` of the cleaned image for inked rows.
2. Group rows with gaps < `label_row_gap_px`. Pick the bottom-most group.
3. Always re-segment that group with `label_refine_row_gap_px` and pick the
   bottom-most sub-group. This handles two cases uniformly: figure body
   merged into the label band, and a section indicator like "b-b" sitting
   one line above the label.
4. Inside the resulting band, build clusters of inked columns separated by
   gaps ≥ `label_max_inter_glyph_gap_px`. Discard clusters narrower than
   `label_min_text_cluster_px` — this is what kills single-column
   scan-border artifacts even when those columns are ink-dense.
5. Pick the widest remaining cluster as the text bbox.
6. Sanity-check vspan and hspan against the configured ranges — raise on
   any mismatch.

## Returning to the user

After Layer 1 alone, briefly report orientation, trim side, pixels cut,
in/out shapes. After a header build, report per-figure label heights, the
target label height used for normalisation, and the canvas size. If any
detection raised, surface the full error message including the source
image and params — never paper over it.
