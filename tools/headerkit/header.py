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
from .render import svg_to_image, paste_illustration
from .illustration import IllustrationSpec, generate_illustration_svg, VIEW_W, VIEW_H

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
    out: str,
    size=(W, H),
    grid_overlay: bool = True,
) -> str:
    """Compose a 5:2 bright/soft essay header and save it to ``out``.

    Layers (bottom -> top): base soft gradient, AI illustration in the right
    zone (native 1500x1200, no distortion), a faint dot grid, a soft scrim panel
    over the left text column, then the eyebrow chip, title, one-line thesis, and
    series tag. Asserts the output is exactly 5:2. Returns ``out``.
    """
    theme = THEMES.get(theme_name, THEMES[DEFAULT_THEME])
    width, height = size
    # Composition grid: text column kept narrow enough to sit over the solid part
    # of the feathered scrim; scrim anchored flush to the left/top/bottom edges.
    scrim_right = int(width * 0.60)
    grid = Grid(margin=130, text_x=130, text_w=1320,
                scrim_box=(0, 0, scrim_right, height))
    scrim_feather = int(width * 0.11)

    img, d = canvas(theme, size)

    # --- AI illustration: native aspect into the right zone (no stretching) ---
    spec = IllustrationSpec(
        title=title,
        thesis=thesis,
        keywords=list(keywords) if keywords else _auto_keywords(title, thesis),
        theme_name=theme_name,
    )
    svg = generate_illustration_svg(spec, backend=backend)
    zone_w = min(VIEW_W, width)               # illustration zone width
    illo = svg_to_image(svg, zone_w, height)
    paste_illustration(img, illo, box=(width - zone_w, 0, width, height))

    # --- faint engineering dot grid (soft texture) ---
    if grid_overlay:
        dot_grid(d, theme, grid)

    # --- soft feathered scrim wash (melts into the art; softens the seam) ---
    scrim_panel(img, theme, grid.scrim_box, feather=scrim_feather)

    # --- text stack: top-anchored, headline-dominant, no brand watermark ---
    # Viral X covers read at a glance: a big bold high-contrast headline up top,
    # a clear subtitle under it, and NO brand tag on the image (the author's
    # handle carries the brand). Series tag renders only when explicitly asked.
    y = grid.margin + 40
    if badge:
        y = eyebrow_chip(d, (grid.text_x, y), badge, theme) + 56
    y = title_block(d, title, theme, grid, top=y, max_lines=2) + 30
    subtitle_block(d, thesis, theme, grid, top=y, max_lines=2)
    if series:
        series_tag(d, (grid.text_x, height - grid.margin - 44), series, theme)

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
    ap.add_argument("--no-grid", action="store_true", help="drop the dot-grid texture")
    ap.add_argument("--out", required=True)
    args = ap.parse_args(argv)

    keywords = [k.strip() for k in args.keywords.split(",") if k.strip()] or None
    out = build_header(
        title=args.title, thesis=args.thesis, badge=args.badge, series=args.series,
        theme_name=args.theme_name, backend=args.backend, keywords=keywords,
        out=args.out, grid_overlay=not args.no_grid,
    )
    from PIL import Image
    print(out, Image.open(out).size)
    return out


if __name__ == "__main__":
    main()
