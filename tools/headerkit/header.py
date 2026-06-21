"""HeaderKit composer + CLI — illustration + title -> 5:2 essay header.

The integration keystone of the HeaderKit design system: it composes the
AI-illustration engine (illustration.py) and the reusable components
(components.py) into a single bright/soft 5:2 header so that the illustration,
combined with the title, implies the essay's content (CONTRACT.md section 5).

Routes everything through the library — this module never calls a raw drawing
primitive (Image.new / ImageDraw.Draw), so it passes gate_header_bypass.

CLI:
    python -m tools.headerkit.header \
        --title "Filed Before It Was Announced" \
        --thesis "Tesla's 70 ms predictive-airbag patent was on file months before the reveal" \
        --badge "US 2026/0125022 A1 . PENDING" \
        --keywords vision,airbag,70ms,before,sensor \
        --backend procedural \
        --out runs/<essay-id>/header.png
"""

from __future__ import annotations

import argparse
import re

from .tokens import (
    W, H, THEMES, DEFAULT_THEME, Grid,
)
from .components import (
    canvas, dot_grid, scrim_panel,
    eyebrow_chip, title_block, subtitle_block, series_tag,
)
from .render import svg_to_image, paste_illustration, load_cover
from .illustration import IllustrationSpec, generate_illustration_svg

DEFAULT_SERIES = "SETI . PATENT ESSAYIST"

# Stopwords for auto keyword extraction (only used when --keywords is omitted).
_STOP = {
    "the", "a", "an", "and", "or", "but", "of", "to", "in", "on", "for", "it",
    "is", "was", "were", "be", "been", "by", "with", "as", "at", "that", "this",
    "from", "its", "it's", "before", "after", "than", "then", "into", "over",
    "when", "while", "how", "why", "what", "which", "who", "you", "your",
}


def _auto_keywords(title: str, thesis: str, *, limit: int = 6) -> list:
    """Derive concept anchors from title+thesis when none are supplied.

    Deterministic: first-seen order over lowercased word tokens, stopwords and
    short tokens dropped. Kept simple — explicit --keywords always wins.
    """
    seen = []
    for word in re.findall(r"[A-Za-z0-9']+", f"{title} {thesis}".lower()):
        if len(word) < 3 or word in _STOP:
            continue
        if word not in seen:
            seen.append(word)
        if len(seen) >= limit:
            break
    return seen


def build_header(
    *,
    title: str,
    thesis: str = "",
    badge: str = "",
    series: str = "",
    theme_name: str = "aurora",
    backend: str = "procedural",
    keywords=None,
    image: str = None,
    out: str,
    scale: float = 2.0,
    size=None,
    grid_overlay: bool = False,
) -> str:
    """Compose a 5:2 bright/soft essay header and save it to ``out``.

    Rendered at ``scale``x the 3000x1200 reference (default 2x = 6000x2400) so
    the text stays crisp when the image is zoomed; the illustration is vector
    (SVG) and rasterizes sharp at any size. Pass ``size`` to override the pixel
    dimensions directly (must be 5:2); otherwise size = (W, H) * scale.

    Layers (bottom -> top): base soft gradient, AI illustration in the right
    half (vector, no distortion), optional dot grid (off by default), a feathered
    soft scrim over the left text column, then the eyebrow chip, dominant title,
    clear subtitle, and (only if requested) a series tag. Asserts the output is
    exactly 5:2. Returns ``out``.
    """
    theme = THEMES.get(theme_name, THEMES[DEFAULT_THEME])
    if size is not None:
        width, height = size
        scale = width / float(W)
    else:
        width, height = int(round(W * scale)), int(round(H * scale))

    def s(v):
        return int(round(v * scale))

    # Geometry scales with the canvas so the design is identical at any resolution.
    # Text column sits over the solid part of the feathered scrim; scrim is flush
    # to the left/top/bottom edges and fades out on the right into the art.
    grid = Grid(margin=s(130), text_x=s(130), text_w=s(1320),
                scrim_box=(0, 0, s(1800), height))
    scrim_feather = s(330)

    img, d = canvas(theme, (width, height))

    # --- art layer in the right half of the canvas (5:2 -> half-width is
    #     1.25:1, matching the 1500x1200 viewBox, so no distortion) ---
    zone_w = width // 2
    zone_box = (width - zone_w, 0, width, height)
    if image:
        # A supplied or AI-generated raster used as the illustration (richer than
        # the procedural SVG). Cover-fit into the art zone; the header still lays
        # crisp, scalable title/badge text over the clean left column.
        illo = load_cover(image, (zone_w, height))
    else:
        spec = IllustrationSpec(
            title=title,
            thesis=thesis,
            keywords=list(keywords) if keywords else _auto_keywords(title, thesis),
            theme_name=theme_name,
        )
        svg = generate_illustration_svg(spec, backend=backend)
        illo = svg_to_image(svg, zone_w, height)   # vector -> crisp at any size
    paste_illustration(img, illo, box=zone_box)

    # --- optional faint dot grid (off by default; reads as noise over the soft field) ---
    if grid_overlay:
        dot_grid(d, theme, grid)

    # --- soft feathered scrim wash (melts into the art; softens the seam) ---
    scrim_panel(img, theme, grid.scrim_box, feather=scrim_feather)

    # --- text stack: top-anchored, headline-dominant, no brand watermark ---
    # Viral X covers read at a glance: a big bold high-contrast headline up top,
    # a clear subtitle under it, and NO brand tag on the image (the author's
    # handle carries the brand). Series tag renders only when explicitly asked.
    y = grid.margin + s(40)
    if badge:
        y = eyebrow_chip(d, (grid.text_x, y), badge, theme, scale=scale) + s(56)
    y = title_block(d, title, theme, grid, top=y, max_lines=2, scale=scale) + s(30)
    subtitle_block(d, thesis, theme, grid, top=y, max_lines=2, scale=scale)
    if series:
        series_tag(d, (grid.text_x, height - grid.margin - s(44)), series, theme, scale=scale)

    ratio = width / height
    if abs(ratio - 2.5) > 1e-6:
        raise ValueError(f"header is not 5:2 (got {width}x{height}, ratio {ratio:.4f})")
    img.save(out)
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description="Compose a 5:2 bright/soft essay header.")
    ap.add_argument("--title", required=True, help="essay hook title (short)")
    ap.add_argument("--thesis", default="", help="one-line thesis / subtitle")
    ap.add_argument("--badge", default="", help="e.g. 'US 2026/0125022 A1 . PENDING'")
    ap.add_argument("--series", default="",
                    help="brand tag on the image (default off; the author handle carries the brand)")
    ap.add_argument("--theme", default=DEFAULT_THEME, dest="theme_name")
    ap.add_argument("--backend", default="procedural",
                    choices=["procedural", "llm", "image-api"])
    ap.add_argument("--keywords", default="",
                    help="comma-separated concept anchors (else auto from title+thesis)")
    ap.add_argument("--image", default=None,
                    help="use a supplied/AI-generated raster as the art layer (cover-fit into "
                         "the right zone) instead of the generated SVG illustration")
    ap.add_argument("--grid", action="store_true", help="add the faint dot-grid texture (off by default)")
    ap.add_argument("--scale", type=float, default=2.0,
                    help="render scale over the 3000x1200 reference (default 2.0 = 6000x2400; "
                         "raise for crisper zoom)")
    ap.add_argument("--out", required=True)
    args = ap.parse_args(argv)

    keywords = [k.strip() for k in args.keywords.split(",") if k.strip()] or None
    out = build_header(
        title=args.title, thesis=args.thesis, badge=args.badge, series=args.series,
        theme_name=args.theme_name, backend=args.backend, keywords=keywords,
        image=args.image, out=args.out, scale=args.scale, grid_overlay=args.grid,
    )
    from PIL import Image
    print(out, Image.open(out).size)
    return out


if __name__ == "__main__":
    main()
