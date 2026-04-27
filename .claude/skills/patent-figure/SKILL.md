---
name: patent-figure
description: Clean up a patent-office figure image by removing the meta-info header band, tight-cropping to the actual drawing content, and adding a small white margin. Invoke when the user shares a patent figure (PNG/JPEG) and asks to crop it, remove the "U.S. Patent / Sheet N of M / publication number" header, tidy up a patent drawing, prepare a patent figure for embedding, or uses Korean phrasings like "특허 도면 정리/크롭/헤더 제거".
---

# Patent Figure Cleanup

A 4-stage pure pipeline that turns a raw patent-office figure image into a
content-only image suitable for slides, papers, and RAG corpora.

```
load → orient → trim_header → tight_crop → pad → save
```

Validated on real USPTO portrait + landscape sheets across multiple
resolutions (1500–3500 px). Single default config handles them all; tune
only on regression.

## When to invoke

The user supplies a patent figure image and wants any combination of:
- the meta-info header line removed (e.g. `U.S. Patent  Date  Sheet 1 of 7  US 12,345,678 B2`)
- excess whitespace trimmed
- the drawing tight-cropped with a clean white margin

Inputs may be PNG or JPEG. Both portrait and landscape (header rotated
90° on left or right) are supported automatically.

## How to run

The skill ships with two files:
- `crop.py` — pure stage functions (`load`, `orient`, `trim_header`, `tight_crop`, `pad`, `process`)
- `crop_figure.py` — thin CLI wrapper

### Step 1 — make sure dependencies are present

Only Pillow + numpy are required. If a project venv is available use it;
otherwise install briefly into the active interpreter:

```bash
python -c "import PIL, numpy" 2>/dev/null || pip install --quiet pillow numpy
```

### Step 2 — run on a single image

```bash
python /path/to/.claude/skills/patent-figure/crop_figure.py <input> [<output>]
```

If `<output>` is omitted, the result is written next to the input as
`<stem>.cropped.png`. Output is always PNG (lossless) regardless of the
input format.

The script prints a short report:
```
input        : foo.png  shape=(2163, 1530)
orientation  : portrait
header trim  : side=top  cut=259px  band=(223, 258)
output       : foo.cropped.png  shape=(1933, 1275)
```

### Step 3 — run on a folder

```bash
SKILL=/path/to/.claude/skills/patent-figure
mkdir -p out
for f in in/*.{png,jpg,jpeg,JPG,JPEG}; do
  [ -e "$f" ] || continue
  python "$SKILL/crop_figure.py" "$f" "out/$(basename "${f%.*}").png"
done
```

### Programmatic use

```python
import sys
from pathlib import Path
sys.path.insert(0, "/path/to/.claude/skills/patent-figure")

from crop import CropConfig, load, process, save

arr = load(Path("input.png"))
out, report = process(arr, CropConfig())   # tweak CropConfig for edge cases
save(out, Path("output.png"))
print(report)   # orientation, side, cut_at, in/out shapes
```

## Tunable parameters (`CropConfig`)

All defaults work for USPTO sheets. Adjust only when a new layout misbehaves.

| field | default | bump up when… | bump down when… |
|---|---|---|---|
| `ink_threshold` | 200 | grayscale watermark bleeds in | extremely faint scans miss text |
| `max_header_fraction` | 0.18 | header occupies > 18% of the edge | aggressive crops eat into figure |
| `min_gap_px` | 8 | header is multi-line and the gap is large | high-res scans need more sensitivity |
| `pad_fraction` | 0.07 | want roomier slide layout (≤ 0.10) | want tighter inserts (≥ 0.05) |
| `ink_row_frac` | 0.005 | dense figures cause false ink runs | sparse figures lose thin lines |

## Algorithm at a glance

1. **orient** — `PORTRAIT` if `h ≥ w`, else `LANDSCAPE`.
2. **trim_header** — project ink density along the candidate edge(s):
   - portrait → top only
   - landscape → left, then right (first edge with a confirmed pattern wins)
   The pattern is: *short ink band → sustained blank gap*. If no such
   pattern is found within `max_header_fraction`, the trim is silently
   skipped (`side=NONE`) — safe fallback.
3. **tight_crop** — bounding box of all remaining ink pixels.
4. **pad** — add a `pad_fraction × max(h, w)` white border on all sides.

## Known limits

- Header expected on top (portrait) or short edges (landscape). 180°-rotated
  pages with the meta-info on the bottom are NOT auto-handled — rotate the
  image first.
- All-image scans without an ink-based header layer (e.g., a watermark
  embedded in the figure) need `ink_threshold` tuning.
- Output is grayscale (PIL `L` mode). Convert to RGB downstream if needed.

## Returning to the user

After running, briefly report: orientation, trim side, pixels cut,
in/out shapes. If the cropped image is small or the trim was skipped
(`side=NONE`), flag it so the user can verify the image matches the
expected patent layout before using it downstream.
