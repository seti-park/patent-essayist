"""Layer 2 — patent-figure header assembly.

Pipeline:
    find_label_bbox  ->  label_height  ->  normalize_by_label
                     ->  compose_horizontal  ->  fit_to_canvas

The first stage (label detection) is the gate: every downstream stage
depends on having a correct text bbox for the "Fig. N" label. Detection
failures must `raise LabelDetectionError` — never fall back to a heuristic
height. Silent fallbacks have caused aspect-ratio bugs to slip into
published artifacts before, which is the reason for the hard-fail rule.

All stages are pure on `numpy.ndarray`s plus a frozen `AssembleConfig`.
I/O happens only at `load_figures` and `save`.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
from PIL import Image


# ----------------------------- config -----------------------------

@dataclass(frozen=True)
class AssembleConfig:
    # ---- label detection ----------------------------------------------------
    # Fraction of cleaned-image height to scan for the bottom label. Layer 1
    # adds pad_fraction (~0.07) of white margin on each side; the label sits
    # in the bottom of the *content*, which after padding lands at roughly
    # y/H ≈ 1 - 0.07 - small_offset ≈ 0.85–0.92. 0.30 leaves an 8% buffer.
    label_search_frac: float = 0.30

    # A pixel counts as "ink" for label scanning if its grayscale value is
    # below this threshold (matches Layer 1's default).
    ink_threshold: int = 200

    # Rows are grouped into label-band candidates; gaps below this many
    # consecutive blank rows keep the group merged. Keeps multi-line labels
    # ("FIG. 5\nb-b") together.
    label_row_gap_px: int = 20

    # Refinement gap used only when the initial grouping returns a group
    # taller than `label_vspan_range` upper bound. The bottom-most group is
    # re-segmented with this tighter gap to peel the actual label off the
    # figure body. Must be smaller than `label_row_gap_px`.
    label_refine_row_gap_px: int = 8

    # Cluster-aware horizontal extent (Fix B):
    #   1. compute column density inside the candidate group
    #   2. find contiguous "ink columns" separated by gaps below
    #      `label_max_inter_glyph_gap_px`
    #   3. drop clusters narrower than `label_min_text_cluster_px` (this is
    #      what discards single-column scan-border artifacts even when the
    #      column is ink-dense)
    #   4. pick the widest remaining cluster as the text bbox
    label_min_col_density: int = 2
    # Must exceed the widest space character at the smallest expected
    # label size. For ~40px-tall "Fig. 1c" labels the space is ~30px, so 50
    # gives a safe margin without bleeding into the next figure on the page.
    label_max_inter_glyph_gap_px: int = 50
    label_min_text_cluster_px: int = 50

    # Sanity ranges for a real "Fig. N" label. If detection produces a bbox
    # outside these, we raise — the caller has either fed in a non-USPTO
    # layout or the cleanup output is broken.
    label_vspan_range: tuple[int, int] = (40, 200)
    label_hspan_range: tuple[int, int] = (50, 600)

    # ---- header assembly ----------------------------------------------------
    figure_gutter_px: int = 120                       # horizontal gap between figures
    canvas_size_px: tuple[int, int] = (3890, 1556)    # 5:2 (W, H)
    canvas_side_pad_px: int = 220                     # left/right safe margin


# ----------------------------- types -----------------------------

@dataclass(frozen=True)
class LabelBBox:
    """Bounding box of the detected 'Fig. N' label in image coordinates."""
    x1: int
    y1: int
    x2: int  # exclusive
    y2: int  # exclusive

    @property
    def vspan(self) -> int:
        return self.y2 - self.y1

    @property
    def hspan(self) -> int:
        return self.x2 - self.x1

    @property
    def y_start_frac(self) -> float | None:  # filled in by caller
        return None  # not stored here; caller computes against image height


class LabelDetectionError(ValueError):
    """Label detection failed. Always carries enough context to debug from
    a production log without re-running on the original image."""


# ----------------------------- internal helpers -----------------------------

def _ink_mask(arr: np.ndarray, threshold: int) -> np.ndarray:
    return arr < threshold


def _row_groups(row_has_ink: np.ndarray, max_gap: int) -> list[tuple[int, int]]:
    """Walk a 1-D boolean array and return [(start, end_inclusive), ...] for
    every contiguous run, where blank gaps shorter than `max_gap` keep
    neighbouring runs merged into a single group."""
    n = len(row_has_ink)
    groups: list[tuple[int, int]] = []
    i = 0
    while i < n:
        if not row_has_ink[i]:
            i += 1
            continue
        start = i
        end = i
        while i < n:
            if row_has_ink[i]:
                end = i
                i += 1
            else:
                # peek ahead: keep merging if the gap is short
                j = i
                while j < n and not row_has_ink[j]:
                    j += 1
                if j - i < max_gap and j < n:
                    i = j
                else:
                    break
        groups.append((start, end))
    return groups


def _column_clusters(is_ink_col: np.ndarray, max_gap: int
                     ) -> list[tuple[int, int]]:
    """Same shape as `_row_groups` but for columns. Returned ranges are
    inclusive."""
    return _row_groups(is_ink_col, max_gap)


# ----------------------------- pure stages -----------------------------

def find_label_bbox(arr: np.ndarray, cfg: AssembleConfig,
                    *, source: str | None = None) -> LabelBBox:
    """Locate the bottom-most "Fig. N" label and return its tight bbox.

    Algorithm (cluster-aware horizontal extent):
        1. scan the bottom `label_search_frac` of the image
        2. group ink rows into bands (gap < `label_row_gap_px` keeps merged)
        3. take the bottom-most band — that is the label
        4. inside that band, identify ink columns and group them into
           text clusters (gap < `label_max_inter_glyph_gap_px`)
        5. discard clusters narrower than `label_min_text_cluster_px`
           (this is how single-column scan-border artifacts get dropped
           even when the column is ink-dense)
        6. pick the widest remaining cluster as the text bbox
        7. sanity-check vspan / hspan against `label_*_range`

    Raises:
        LabelDetectionError — at every failure mode, with a message that
        names the source image, the search params used, and the reason.
    """
    src = source or "<ndarray>"
    h, w = arr.shape

    # 1. search region
    y_offset = int(h * (1 - cfg.label_search_frac))
    region = arr[y_offset:]
    if region.size == 0:
        raise LabelDetectionError(
            f"label detection failed: {src}\n"
            f"  reason=empty_search_region  search_frac={cfg.label_search_frac}  "
            f"image_h={h}")

    mask = _ink_mask(region, cfg.ink_threshold)
    row_has_ink = mask.any(axis=1)

    # 2. row groups
    groups = _row_groups(row_has_ink, cfg.label_row_gap_px)
    if not groups:
        raise LabelDetectionError(
            f"label detection failed: {src}\n"
            f"  reason=no_ink_rows  search_frac={cfg.label_search_frac}  "
            f"region_h={region.shape[0]}")

    # 3. bottom-most group is the label candidate
    g_start_local, g_end_local = groups[-1]

    # 3b. Refinement pass: always re-segment the candidate band with a
    # tighter gap and pick the bottom-most sub-group. This handles two
    # cases uniformly:
    #   - the figure body got merged in (initial vspan way over the upper
    #     bound) — the bottom-most sub-group is the label proper.
    #   - a small section indicator like "b-b" sits one line above the
    #     label (initial vspan looks plausible but contains both) — the
    #     bottom-most sub-group is again just the label.
    # If no further split is possible the sub-group equals the input and
    # nothing changes.
    sub_mask = row_has_ink[g_start_local: g_end_local + 1]
    sub_groups = _row_groups(sub_mask, cfg.label_refine_row_gap_px)
    if not sub_groups:
        raise LabelDetectionError(
            f"label detection failed: {src}\n"
            f"  reason=refinement_empty  initial_band="
            f"y[{y_offset + g_start_local}:{y_offset + g_end_local + 1}]  "
            f"refine_gap={cfg.label_refine_row_gap_px}")
    sb_start, sb_end = sub_groups[-1]
    refined_start = g_start_local + sb_start
    refined_end = g_start_local + sb_end
    g_start_local, g_end_local = refined_start, refined_end

    g_start = y_offset + g_start_local
    g_end = y_offset + g_end_local                       # inclusive

    # 4. column clusters within the group
    band = arr[g_start: g_end + 1]
    col_density = (band < cfg.ink_threshold).sum(axis=0)
    is_ink_col = col_density >= cfg.label_min_col_density
    if not is_ink_col.any():
        raise LabelDetectionError(
            f"label detection failed: {src}\n"
            f"  reason=no_ink_cols_in_band  band_y=[{g_start}:{g_end + 1}]  "
            f"min_col_density={cfg.label_min_col_density}")

    clusters = _column_clusters(is_ink_col, cfg.label_max_inter_glyph_gap_px)

    # 5. filter out narrow clusters (single-column artifacts, stray dots)
    wide = [(c0, c1) for (c0, c1) in clusters
            if (c1 - c0 + 1) >= cfg.label_min_text_cluster_px]
    if not wide:
        widths = [c1 - c0 + 1 for c0, c1 in clusters]
        raise LabelDetectionError(
            f"label detection failed: {src}\n"
            f"  reason=no_wide_cluster  band_y=[{g_start}:{g_end + 1}]  "
            f"cluster_widths={widths}  min_required={cfg.label_min_text_cluster_px}")

    # 6. widest cluster
    c0, c1 = max(wide, key=lambda c: c[1] - c[0])
    bbox = LabelBBox(x1=int(c0), y1=int(g_start),
                     x2=int(c1) + 1, y2=int(g_end) + 1)

    # 7. sanity check
    vlo, vhi = cfg.label_vspan_range
    hlo, hhi = cfg.label_hspan_range
    if not (vlo <= bbox.vspan <= vhi):
        raise LabelDetectionError(
            f"label detection failed: {src}\n"
            f"  reason=vspan_out_of_range  vspan={bbox.vspan}  "
            f"expected=[{vlo},{vhi}]  bbox={bbox}")
    if not (hlo <= bbox.hspan <= hhi):
        raise LabelDetectionError(
            f"label detection failed: {src}\n"
            f"  reason=hspan_out_of_range  hspan={bbox.hspan}  "
            f"expected=[{hlo},{hhi}]  bbox={bbox}")

    return bbox


def label_height(arr: np.ndarray, cfg: AssembleConfig,
                 *, source: str | None = None) -> int:
    """Convenience: vertical pixel span of the detected label.
    Raises `LabelDetectionError` on failure (same contract as
    `find_label_bbox`)."""
    return find_label_bbox(arr, cfg, source=source).vspan


# ----------------------------- normalisation -----------------------------

def normalize_by_label(figs: list[np.ndarray], cfg: AssembleConfig,
                       *, sources: list[str] | None = None,
                       target_label_height: int | None = None
                       ) -> list[np.ndarray]:
    """Resize each figure so that all "Fig. N" labels end up the same pixel
    height. `target_label_height` defaults to the median across inputs; pass
    a value to lock the output scale.

    Uses `Image.LANCZOS` resampling. Output is grayscale uint8.
    """
    if not figs:
        return []
    sources = sources or [f"<fig {i}>" for i in range(len(figs))]
    if len(sources) != len(figs):
        raise ValueError(f"sources length {len(sources)} != figs length {len(figs)}")

    heights = [label_height(arr, cfg, source=src)
               for arr, src in zip(figs, sources)]
    target = target_label_height if target_label_height is not None \
        else int(np.median(heights))

    resized: list[np.ndarray] = []
    for arr, lh, src in zip(figs, heights, sources):
        scale = target / lh
        new_w = max(1, int(round(arr.shape[1] * scale)))
        new_h = max(1, int(round(arr.shape[0] * scale)))
        img = Image.fromarray(arr, mode="L").resize((new_w, new_h),
                                                    resample=Image.LANCZOS)
        resized.append(np.asarray(img, dtype=np.uint8))
    return resized


# ----------------------------- composition -----------------------------

def compose_horizontal(figs: list[np.ndarray], cfg: AssembleConfig
                       ) -> np.ndarray:
    """Stack figures left-to-right, separated by `figure_gutter_px` of
    white space, vertically centre-aligned. Output canvas height is the
    tallest figure, and width is the sum of figure widths plus gutters."""
    if not figs:
        raise ValueError("compose_horizontal: no figures")
    H = max(a.shape[0] for a in figs)
    W = sum(a.shape[1] for a in figs) + cfg.figure_gutter_px * (len(figs) - 1)
    canvas = np.full((H, W), 255, dtype=np.uint8)
    x = 0
    for a in figs:
        h, w = a.shape
        y = (H - h) // 2
        canvas[y: y + h, x: x + w] = a
        x += w + cfg.figure_gutter_px
    return canvas


def fit_to_canvas(arr: np.ndarray, cfg: AssembleConfig) -> np.ndarray:
    """Place the composed strip onto a fixed `canvas_size_px` background
    while preserving aspect ratio (no crop). Side padding is enforced as a
    minimum; the figure shrinks further if necessary."""
    cw, ch = cfg.canvas_size_px           # spec is (W, H)
    pad = cfg.canvas_side_pad_px
    avail_w = cw - 2 * pad
    avail_h = ch - 2 * pad
    if avail_w <= 0 or avail_h <= 0:
        raise ValueError(
            f"fit_to_canvas: padding {pad}px leaves no room in "
            f"{cw}x{ch} canvas")

    h, w = arr.shape
    scale = min(avail_w / w, avail_h / h)
    new_w = max(1, int(round(w * scale)))
    new_h = max(1, int(round(h * scale)))
    resized = np.asarray(
        Image.fromarray(arr, mode="L").resize((new_w, new_h),
                                              resample=Image.LANCZOS),
        dtype=np.uint8,
    )

    canvas = np.full((ch, cw), 255, dtype=np.uint8)
    x = (cw - new_w) // 2
    y = (ch - new_h) // 2
    canvas[y: y + new_h, x: x + new_w] = resized
    return canvas


# ----------------------------- top-level -----------------------------

@dataclass(frozen=True)
class HeaderReport:
    sources: tuple[str, ...]
    label_heights_px: tuple[int, ...]
    target_label_height_px: int
    canvas_size_px: tuple[int, int]


def build_header(figs: list[np.ndarray], cfg: AssembleConfig,
                 *, sources: list[str] | None = None,
                 target_label_height: int | None = None
                 ) -> tuple[np.ndarray, HeaderReport]:
    """End-to-end: detect labels, normalise, compose, fit. Raises
    `LabelDetectionError` if any input fails detection — by design, no
    silent fallback."""
    if not 1 <= len(figs) <= 4:
        raise ValueError(
            f"build_header: expected 1–4 figures, got {len(figs)}")
    sources = sources or [f"<fig {i}>" for i in range(len(figs))]

    heights = [label_height(arr, cfg, source=src)
               for arr, src in zip(figs, sources)]
    target = target_label_height if target_label_height is not None \
        else int(np.median(heights))

    normed = normalize_by_label(figs, cfg, sources=sources,
                                target_label_height=target)
    strip = compose_horizontal(normed, cfg)
    canvas = fit_to_canvas(strip, cfg)
    return canvas, HeaderReport(
        sources=tuple(sources),
        label_heights_px=tuple(heights),
        target_label_height_px=target,
        canvas_size_px=cfg.canvas_size_px,
    )


# ----------------------------- I/O boundary -----------------------------

def load_figure(path: Path) -> np.ndarray:
    img = Image.open(path).convert("L")
    return np.asarray(img, dtype=np.uint8)


def save(arr: np.ndarray, path: Path) -> None:
    Image.fromarray(arr, mode="L").save(path)
