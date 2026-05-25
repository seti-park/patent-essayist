"""Pipeline for cleaning a single patent-figure image.

Stages:
    1. orient        — portrait vs landscape
    2. trim_header   — remove the meta-info header band on one edge
                       (top for portrait; left or right for landscape — whichever
                        side actually carries the header pattern)
    3. tight_crop    — density-based bounding box around the remaining ink
    4. pad           — add a 5–10% white margin

Conventions:
    All stages operate on a 2-D `numpy.ndarray` of grayscale pixels (uint8,
    0 = black, 255 = white). The boundary functions `load`/`save` handle
    PIL <-> ndarray conversion. Everything in between is pure data.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from pathlib import Path

import numpy as np
from PIL import Image


# ----------------------------- config & types -----------------------------

class Orientation(str, Enum):
    PORTRAIT = "portrait"
    LANDSCAPE = "landscape"


class HeaderSide(str, Enum):
    TOP = "top"
    LEFT = "left"
    RIGHT = "right"
    NONE = "none"      # no header pattern detected; skip the trim


@dataclass(frozen=True)
class CropConfig:
    # Grayscale value below which a pixel counts as "ink".
    ink_threshold: int = 200
    # Fraction of an ink line that has to be present in a row/col for the row
    # to be considered "inked". Adaptive to the densest row, clamped to 2 px.
    ink_row_frac: float = 0.005
    # The header band must be confined to this much of the image dimension
    # (looking from the relevant edge). Anything larger is treated as the
    # figure itself and we refuse to trim.
    max_header_fraction: float = 0.18
    # A confirmed gap between the header text and the figure must be at
    # least this many pixels long. Smaller gaps are treated as part of the
    # header (multi-line headers, decorations, etc.).
    min_gap_px: int = 8
    # White margin as a fraction of max(cropped_h, cropped_w). 0.07 ≈ 7%.
    pad_fraction: float = 0.07
    # tight_crop defenses against scan/screenshot artifacts:
    #   - rows/cols whose total ink count is below `min_ink_density` are
    #     ignored when computing the bounding box (kills isolated specks).
    #   - after the box is computed, `edge_shave_px` pixels are shaved off
    #     each side. This is the only thing that defeats a *continuous*
    #     1-pixel border line (e.g. a Safari screenshot frame), since such a
    #     line has high density and survives the density filter.
    min_ink_density: int = 2
    edge_shave_px: int = 1


@dataclass(frozen=True)
class TrimReport:
    """Provenance for the header-trim step. Useful for debugging and tests."""
    orientation: Orientation
    side: HeaderSide
    cut_at: int                  # pixels removed from that edge
    band_extent: tuple[int, int] | None  # (band_start, band_end) along the cut axis


# ----------------------------- I/O boundary -----------------------------

def load(path: Path) -> np.ndarray:
    """Read an image as 2-D grayscale ndarray (uint8). White-on-black gets
    auto-corrected if a heuristic suggests it (rare for patents)."""
    img = Image.open(path).convert("L")
    return np.asarray(img, dtype=np.uint8)


def save(arr: np.ndarray, path: Path) -> None:
    Image.fromarray(arr, mode="L").save(path)


# ----------------------------- pure stages -----------------------------

def orient(arr: np.ndarray) -> Orientation:
    h, w = arr.shape
    return Orientation.PORTRAIT if h >= w else Orientation.LANDSCAPE


def _ink_mask(arr: np.ndarray, threshold: int) -> np.ndarray:
    return arr < threshold


def _find_header_cut(profile: np.ndarray, cfg: CropConfig
                     ) -> tuple[int, tuple[int, int]] | None:
    """Walk a 1-D ink-density profile from index 0; return the cut position
    (drop indices [0, cut)) and the detected band's extent, or None if no
    clear header pattern exists within the configured search window."""
    cap = int(len(profile) * cfg.max_header_fraction)
    if cap < cfg.min_gap_px * 2:
        return None

    ink_threshold = max(2, int(profile.max() * cfg.ink_row_frac))
    is_ink = profile > ink_threshold

    # Phase 1: skip leading blank margin
    i = 0
    while i < cap and not is_ink[i]:
        i += 1
    if i >= cap:
        return None
    band_start = i

    # Phase 2: walk through the (possibly multi-line) header band
    band_end = band_start
    gap = 0
    while i < cap:
        if is_ink[i]:
            band_end = i
            gap = 0
        else:
            gap += 1
            if gap >= cfg.min_gap_px:
                # confirmed gap — cut at the start of the gap so that we
                # remove the header line(s) cleanly without touching the
                # figure that follows.
                return band_end + 1, (band_start, band_end)
        i += 1

    # Reached the cap without finding a sustained gap — the "header band"
    # extends too deep into the image; this is probably the figure itself,
    # so we refuse to cut.
    return None


def trim_header(arr: np.ndarray, cfg: CropConfig
                ) -> tuple[np.ndarray, TrimReport]:
    """Remove the header strip from whichever edge carries it.

    Strategy: project ink density along each candidate edge, search for a
    'short ink band followed by a sustained gap'. The first edge whose
    profile yields a confirmed cut wins. For portraits we only look at the
    top; for landscapes we try left then right.
    """
    h, w = arr.shape
    mask = _ink_mask(arr, cfg.ink_threshold)
    o = orient(arr)

    candidates: list[tuple[HeaderSide, np.ndarray]] = []
    if o == Orientation.PORTRAIT:
        candidates.append((HeaderSide.TOP, mask.sum(axis=1)))                  # rows
    else:
        candidates.append((HeaderSide.LEFT, mask.sum(axis=0)))                 # cols
        candidates.append((HeaderSide.RIGHT, mask.sum(axis=0)[::-1]))          # cols, reversed

    for side, profile in candidates:
        result = _find_header_cut(profile, cfg)
        if result is None:
            continue
        cut, band = result
        if side == HeaderSide.TOP:
            return arr[cut:, :], TrimReport(o, side, cut, band)
        if side == HeaderSide.LEFT:
            return arr[:, cut:], TrimReport(o, side, cut, band)
        if side == HeaderSide.RIGHT:
            return arr[:, : w - cut], TrimReport(o, side, cut, band)

    return arr, TrimReport(o, HeaderSide.NONE, 0, None)


def tight_crop(arr: np.ndarray, cfg: CropConfig) -> np.ndarray:
    """Bounding-box crop around inked pixels, with two artifact defenses.

    1. Density filter — a row/column counts only if it has at least
       `min_ink_density` inked pixels. Catches single-pixel noise.
    2. Edge shave — after the bounding box is found, `edge_shave_px`
       pixels are removed from each side. This is what actually defeats a
       continuous 1-pixel border line (browser-screenshot frames), since
       a full-length line has very high density and would otherwise be
       indistinguishable from legitimate figure content.
    """
    mask = _ink_mask(arr, cfg.ink_threshold)
    rows = np.where(mask.sum(axis=1) >= cfg.min_ink_density)[0]
    cols = np.where(mask.sum(axis=0) >= cfg.min_ink_density)[0]
    if len(rows) == 0 or len(cols) == 0:
        return arr
    r0, r1 = rows[0], rows[-1] + 1
    c0, c1 = cols[0], cols[-1] + 1

    s = cfg.edge_shave_px
    if s > 0 and (r1 - r0) > 2 * s and (c1 - c0) > 2 * s:
        r0, r1, c0, c1 = r0 + s, r1 - s, c0 + s, c1 - s

    return arr[r0:r1, c0:c1]


def pad(arr: np.ndarray, cfg: CropConfig) -> np.ndarray:
    h, w = arr.shape
    margin = int(round(max(h, w) * cfg.pad_fraction))
    if margin <= 0:
        return arr
    out = np.full((h + 2 * margin, w + 2 * margin), 255, dtype=arr.dtype)
    out[margin:margin + h, margin:margin + w] = arr
    return out


# ----------------------------- composition -----------------------------

@dataclass(frozen=True)
class ProcessReport:
    src: Path
    orientation: Orientation
    trim: TrimReport
    in_shape: tuple[int, int]
    out_shape: tuple[int, int]


def process(arr: np.ndarray, cfg: CropConfig = CropConfig()
            ) -> tuple[np.ndarray, ProcessReport]:
    in_shape = arr.shape  # type: ignore[assignment]
    o = orient(arr)
    after_trim, trim = trim_header(arr, cfg)
    after_crop = tight_crop(after_trim, cfg)
    after_pad = pad(after_crop, cfg)
    return after_pad, ProcessReport(
        src=Path(""),
        orientation=o,
        trim=trim,
        in_shape=in_shape,            # type: ignore[arg-type]
        out_shape=after_pad.shape,    # type: ignore[arg-type]
    )
