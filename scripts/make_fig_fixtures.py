"""Render a few synthetic patent-figure images that exercise the crop
pipeline end-to-end.

Each fixture has a known structure:
    - portrait_simple : a USPTO-style header line at the top, a generous
                        gap, then a rectangular figure occupying the lower
                        ~60% of the canvas.
    - portrait_off_center: figure shifted to one side; tight_crop should
                        recenter the bounding box.
    - landscape_left  : same as portrait_simple but rotated 90° clockwise
                        (header now on the LEFT edge).
    - no_header       : a figure-only image without any header band; the
                        pipeline should detect 'none' and skip the trim.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "figures_in"
OUT.mkdir(parents=True, exist_ok=True)


def _font(size: int) -> ImageFont.ImageFont:
    # Fall back to default bitmap font if no TTF is available; the actual
    # glyph shapes don't matter — we only need an ink band of plausible
    # height.
    try:
        return ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", size)
    except OSError:
        return ImageFont.load_default()


def _draw_header(draw: ImageDraw.ImageDraw, w: int, top: int) -> None:
    f = _font(28)
    draw.text((int(w * 0.05), top), "U.S. Patent", font=f, fill=0)
    draw.text((int(w * 0.30), top), "Jan. 13, 2026", font=f, fill=0)
    draw.text((int(w * 0.55), top), "Sheet 1 of 7", font=f, fill=0)
    draw.text((int(w * 0.80), top), "US 12,523,817 B2", font=f, fill=0)


def _draw_figure(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int]) -> None:
    """Fill in a figure-like shape inside `box` so tight_crop has a target."""
    x0, y0, x1, y1 = box
    # Outer frame
    draw.rectangle(box, outline=0, width=3)
    # A few inner shapes
    cx = (x0 + x1) // 2
    cy = (y0 + y1) // 2
    draw.line((x0 + 20, cy, x1 - 20, cy), fill=0, width=2)
    draw.ellipse((cx - 60, cy - 60, cx + 60, cy + 60), outline=0, width=2)
    draw.rectangle((x0 + 30, y0 + 30, x0 + 120, y0 + 90), outline=0, width=2)
    f = _font(20)
    draw.text((cx - 40, y1 - 30), "Fig. 1", font=f, fill=0)


def make_portrait_simple() -> Path:
    w, h = 1200, 1500
    img = Image.new("L", (w, h), 255)
    d = ImageDraw.Draw(img)
    _draw_header(d, w, top=80)
    _draw_figure(d, (200, 350, 1000, 1300))
    p = OUT / "portrait_simple.png"
    img.save(p)
    return p


def make_portrait_off_center() -> Path:
    w, h = 1200, 1500
    img = Image.new("L", (w, h), 255)
    d = ImageDraw.Draw(img)
    _draw_header(d, w, top=80)
    _draw_figure(d, (520, 400, 1140, 950))   # right-shifted
    p = OUT / "portrait_off_center.png"
    img.save(p)
    return p


def make_landscape_left() -> Path:
    src = Image.open(make_portrait_simple()).rotate(90, expand=True)  # → header on LEFT
    p = OUT / "landscape_left.png"
    src.save(p)
    return p


def make_no_header() -> Path:
    w, h = 1200, 900
    img = Image.new("L", (w, h), 255)
    d = ImageDraw.Draw(img)
    _draw_figure(d, (150, 150, 1050, 750))
    p = OUT / "no_header.png"
    img.save(p)
    return p


def main() -> None:
    for fn in (make_portrait_simple,
               make_portrait_off_center,
               make_landscape_left,
               make_no_header):
        path = fn()
        arr = np.asarray(Image.open(path))
        print(f"  built {path.name:30s} shape={arr.shape}")


if __name__ == "__main__":
    main()
