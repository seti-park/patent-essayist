"""HeaderKit — design-system foundation for patent-essay headers.

Public API re-exports: tokens, components, render utilities. Compose any header
from these tokens and components without reaching for raw Pillow.
See tools/headerkit/CONTRACT.md.
"""

from .tokens import (
    RATIO, W, H,
    Theme, THEMES, DEFAULT_THEME,
    Grid, GRID,
    FONT_DIR, F_TITLE, F_SANS, F_MONO, F_MONO_B,
    TITLE_MAX, TITLE_MIN, EYEBROW, META, SUBTITLE,
    brightness, is_soft, hex_to_rgb,
)
from .components import (
    canvas, dot_grid, scrim_panel,
    eyebrow_chip, title_block, subtitle_block, meta_line, series_tag,
    wrap_to_width, fit_title,
)
from .render import svg_to_image, paste_illustration
from .illustration import (
    IllustrationSpec, generate_illustration_svg, render_illustration,
)
from .header import build_header

__all__ = [
    # tokens
    "RATIO", "W", "H",
    "Theme", "THEMES", "DEFAULT_THEME",
    "Grid", "GRID",
    "FONT_DIR", "F_TITLE", "F_SANS", "F_MONO", "F_MONO_B",
    "TITLE_MAX", "TITLE_MIN", "EYEBROW", "META", "SUBTITLE",
    "brightness", "is_soft", "hex_to_rgb",
    # components
    "canvas", "dot_grid", "scrim_panel",
    "eyebrow_chip", "title_block", "subtitle_block", "meta_line", "series_tag",
    "wrap_to_width", "fit_title",
    # render
    "svg_to_image", "paste_illustration",
    # illustration engine
    "IllustrationSpec", "generate_illustration_svg", "render_illustration",
    # composer
    "build_header",
]
