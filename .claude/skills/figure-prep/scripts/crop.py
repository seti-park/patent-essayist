#!/usr/bin/env python3
"""Pixel primitives for figure-prep: load / tight_crop / pad.

Ported from seti-park/patent-essay-pipeline `patent-figures-clean` v2.1 (the minimal
used surface — the v1 heuristic header detector was dead code there and is not ported;
header/edge decisions are made by vision and arrive as trim fractions, see
process_figures.py).

Requires Pillow + numpy (`pip install pillow numpy`). Everything here is deterministic;
no model involvement.
"""

from dataclasses import dataclass

import numpy as np
from PIL import Image


@dataclass(frozen=True)
class CropConfig:
    # A grayscale value below this counts as ink.
    ink_threshold: int = 200
    # A row/column needs at least this many ink pixels to count (kills scan speckle).
    min_ink_density: int = 2
    # Shrink the bbox by this many pixels per side after cropping (kills a continuous
    # 1-px frame line, e.g. a browser-screenshot border, that density alone can't tell
    # from content).
    edge_shave_px: int = 1
    # Uniform margin = round(max(h, w) * pad_fraction) on all four sides. Using the
    # LONGER side as the single baseline gives portrait and landscape figures the same
    # absolute margin, so a mixed set frames consistently.
    pad_fraction: float = 0.10


def load(path):
    """Open an image as a grayscale uint8 array, flattening alpha onto WHITE.

    Patent figures exported with transparency often store RGB(0,0,0) under
    transparent pixels; a naive .convert("L") turns those into ink and corrupts the
    bounding box (asymmetric padding). Compositing onto white first fixes that.
    """
    im = Image.open(path)
    has_alpha = (
        im.mode in ("RGBA", "LA")
        or (im.mode == "P" and "transparency" in im.info)
    )
    if has_alpha:
        rgba = im.convert("RGBA")
        bg = Image.new("RGBA", rgba.size, (255, 255, 255, 255))
        im = Image.alpha_composite(bg, rgba)
    return np.asarray(im.convert("L"), dtype=np.uint8)


def tight_crop(arr, cfg):
    """Density-based bounding-box crop with speckle + frame-line defenses."""
    mask = arr < cfg.ink_threshold
    rows = np.where(mask.sum(axis=1) >= cfg.min_ink_density)[0]
    cols = np.where(mask.sum(axis=0) >= cfg.min_ink_density)[0]
    if rows.size == 0 or cols.size == 0:
        return arr  # all-white safeguard
    r0, r1 = int(rows[0]), int(rows[-1]) + 1
    c0, c1 = int(cols[0]), int(cols[-1]) + 1
    s = cfg.edge_shave_px
    if s > 0 and (r1 - r0) > 2 * s and (c1 - c0) > 2 * s:
        r0, r1, c0, c1 = r0 + s, r1 - s, c0 + s, c1 - s
    return arr[r0:r1, c0:c1]


def pad(arr, cfg):
    """Uniform symmetric white border around the cropped figure."""
    h, w = arr.shape
    margin = int(round(max(h, w) * cfg.pad_fraction))
    out = np.full((h + 2 * margin, w + 2 * margin), 255, dtype=np.uint8)
    out[margin:margin + h, margin:margin + w] = arr
    return out
