"""HeaderKit design tokens — themes, type scale, layout grid.

Single source of truth for every styling value used to compose a header.
No module that draws a header may hardcode a color or size; it reads from here.
See tools/headerkit/CONTRACT.md section 1.
"""

from dataclasses import dataclass

# ---------------------------------------------------------------------------
# Canvas geometry
# ---------------------------------------------------------------------------
RATIO = (5, 2)
W, H = 3000, 1200            # canonical render size; W/H == 2.5 exactly


# ---------------------------------------------------------------------------
# Theme
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class Theme:
    name: str
    bg_top: tuple       # gradient field top color (RGB)
    bg_bottom: tuple    # gradient field bottom color (RGB)
    ink: str            # title ink (hex, soft navy)
    ink_soft: str       # meta/subtitle ink (hex)
    accent: str         # primary soft accent (hex)
    accent2: str        # secondary soft accent (hex)
    accent3: str        # tertiary soft accent (hex)
    scrim: tuple        # RGBA light panel behind text (legibility over illustration)
    grid: str           # faint dot grid (hex)


# PRIMARY theme — bright & soft ("aurora"). Default and the deliverable.
THEMES = {
    "aurora": Theme(
        name="aurora",
        bg_top=(253, 246, 239),      # #FDF6EF soft peach-cream  (BRIGHT)
        bg_bottom=(238, 243, 248),   # #EEF3F8 soft sky          (SOFT)
        ink="#2E3A46", ink_soft="#6B7682",
        accent="#F2A98C",            # soft coral
        accent2="#9FC2DD",           # soft sky
        accent3="#BfDcC8",           # soft mint
        scrim=(251, 248, 243, 200),  # ~0.78 alpha light panel
        grid="#ECE6DC",
    ),
}
DEFAULT_THEME = "aurora"


# ---------------------------------------------------------------------------
# Type scale (Liberation; present at /usr/share/fonts/truetype/liberation)
# ---------------------------------------------------------------------------
FONT_DIR = "/usr/share/fonts/truetype/liberation"
F_TITLE = f"{FONT_DIR}/LiberationSans-Bold.ttf"
F_MONO = f"{FONT_DIR}/LiberationMono-Regular.ttf"
F_MONO_B = f"{FONT_DIR}/LiberationMono-Bold.ttf"
TITLE_MAX, TITLE_MIN = 188, 104    # autosize bounds
EYEBROW, META = 46, 42             # mono sizes


# ---------------------------------------------------------------------------
# Layout grid
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class Grid:                          # layout for the 5:2 canvas
    margin: int = 130
    text_x: int = 130
    text_w: int = 1500              # left text column width (title wraps to this)
    scrim_box: tuple = (90, 150, 1640, 1050)   # x0,y0,x1,y1 light panel behind text


GRID = Grid()


# ---------------------------------------------------------------------------
# Color helpers
# ---------------------------------------------------------------------------
def hex_to_rgb(value) -> tuple:
    """Accept '#RRGGBB' / 'RRGGBB' (case-insensitive) or an (R,G,B[,A]) tuple."""
    if isinstance(value, (tuple, list)):
        return tuple(int(c) for c in value[:3])
    s = value.strip().lstrip("#")
    if len(s) == 3:                 # short form #abc
        s = "".join(ch * 2 for ch in s)
    if len(s) not in (6, 8):
        raise ValueError(f"not a hex color: {value!r}")
    return tuple(int(s[i:i + 2], 16) for i in (0, 2, 4))


def brightness(rgb) -> float:
    """0..255 perceived luminance (0.2126R + 0.7152G + 0.0722B).

    Accepts a hex string or an (R,G,B[,A]) tuple.
    """
    r, g, b = hex_to_rgb(rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def is_soft(theme: Theme) -> bool:
    """True if the palette stays in the bright/soft band.

    Bright/soft definition (testable): every bg_* and accent* token has perceived
    luminance >= 150 (bright), and `ink` is the only low-luminance (dark) token.
    """
    bright_tokens = (
        theme.bg_top,
        theme.bg_bottom,
        theme.accent,
        theme.accent2,
        theme.accent3,
    )
    if not all(brightness(t) >= 150 for t in bright_tokens):
        return False
    # ink must be the single dark token.
    return brightness(theme.ink) < 150
