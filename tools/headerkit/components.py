"""HeaderKit reusable draw components.

Every component takes a Pillow ImageDraw / Image, a Theme, and a Grid, and draws
using ONLY theme/grid token values — no hardcoded colors or sizes.
See tools/headerkit/CONTRACT.md section 2.
"""

from PIL import Image, ImageDraw, ImageFont

from .tokens import (
    W, H, Theme, Grid,
    F_TITLE, F_MONO, F_MONO_B,
    TITLE_MAX, TITLE_MIN, EYEBROW, META,
    hex_to_rgb,
)


# ---------------------------------------------------------------------------
# internal font cache
# ---------------------------------------------------------------------------
_FONT_CACHE = {}


def _font(path, size):
    key = (path, size)
    f = _FONT_CACHE.get(key)
    if f is None:
        f = ImageFont.truetype(path, size)
        _FONT_CACHE[key] = f
    return f


def _text_w(d, text, font):
    return d.textlength(text, font=font)


def _line_h(font):
    asc, desc = font.getmetrics()
    return asc + desc


# ---------------------------------------------------------------------------
# text utilities (single canonical source)
# ---------------------------------------------------------------------------
def wrap_to_width(d, text, font, max_w) -> list:
    """Greedy word-wrap `text` so each line fits within max_w pixels."""
    words = text.split()
    if not words:
        return []
    lines = []
    cur = words[0]
    for word in words[1:]:
        trial = f"{cur} {word}"
        if _text_w(d, trial, font) <= max_w:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    lines.append(cur)
    return lines


def fit_title(d, text, max_w, *, max_lines, start, floor):
    """Find the largest title font (from `start` down to `floor`) for which `text`
    wraps to at most `max_lines` lines within max_w. Returns (font, lines)."""
    size = start
    last = None
    while size >= floor:
        font = _font(F_TITLE, size)
        lines = wrap_to_width(d, text, font, max_w)
        last = (font, lines)
        if len(lines) <= max_lines:
            return font, lines
        size -= 4
    # Floor reached and still too many lines: clamp to max_lines.
    font, lines = last
    if len(lines) > max_lines:
        lines = lines[:max_lines]
    return font, lines


# ---------------------------------------------------------------------------
# canvas + background
# ---------------------------------------------------------------------------
def canvas(theme: Theme, size=(W, H)):
    """New RGB canvas filled with the vertical bg_top->bg_bottom soft gradient.

    Returns (Image, ImageDraw)."""
    width, height = size
    img = Image.new("RGB", (width, height))
    top = hex_to_rgb(theme.bg_top)
    bottom = hex_to_rgb(theme.bg_bottom)
    grad = Image.new("RGB", (1, height))
    gd = grad.load()
    denom = max(height - 1, 1)
    for y in range(height):
        t = y / denom
        gd[0, y] = (
            round(top[0] + (bottom[0] - top[0]) * t),
            round(top[1] + (bottom[1] - top[1]) * t),
            round(top[2] + (bottom[2] - top[2]) * t),
        )
    img.paste(grad.resize((width, height)))
    d = ImageDraw.Draw(img)
    return img, d


def dot_grid(d, theme, grid) -> None:
    """Faint token-colored dot grid across the canvas."""
    color = hex_to_rgb(theme.grid)
    step = grid.margin
    radius = 3
    # Use the draw object's image bounds.
    width, height = d.im.size
    y = step
    while y < height:
        x = step
        while x < width:
            d.ellipse((x - radius, y - radius, x + radius, y + radius), fill=color)
            x += step
        y += step


# ---------------------------------------------------------------------------
# scrim panel
# ---------------------------------------------------------------------------
def scrim_panel(canvas, theme, box, *, feather=0) -> None:
    """Composite the soft RGBA scrim panel onto `canvas` so dark text stays
    legible over a bright illustration.

    feather == 0 : a rounded card (the standalone-panel default).
    feather >  0 : a flush wash whose right edge fades to transparent over the
                   last `feather` px, so the panel melts into the illustration
                   instead of reading as a hard-edged card. Anchor the box flush
                   to the canvas edges for a seamless soft wash."""
    x0, y0, x1, y1 = box
    w = max(int(x1 - x0), 1)
    h = max(int(y1 - y0), 1)
    r, g, b = theme.scrim[0], theme.scrim[1], theme.scrim[2]
    a = theme.scrim[3]
    if feather and feather > 0:
        panel = Image.new("RGBA", (w, h), (r, g, b, 255))
        ramp = Image.new("L", (w, 1))
        px = ramp.load()
        f = min(int(feather), w)
        solid = w - f
        for x in range(w):
            if x < solid:
                px[x, 0] = a
            else:
                i = x - solid
                px[x, 0] = int(a * (1 - i / max(f - 1, 1)))
        panel.putalpha(ramp.resize((w, h)))
    else:
        panel = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        pd = ImageDraw.Draw(panel)
        radius = min(w, h) // 12 or 1
        pd.rounded_rectangle((0, 0, w - 1, h - 1), radius=radius,
                             fill=(r, g, b, a))
    base = canvas.convert("RGBA")
    base.alpha_composite(panel, dest=(int(x0), int(y0)))
    canvas.paste(base.convert("RGB"))


# ---------------------------------------------------------------------------
# eyebrow chip
# ---------------------------------------------------------------------------
def eyebrow_chip(d, xy, text, theme, *, fill=None) -> int:
    """Small rounded mono-caps chip (patent no. / status). Returns chip bottom y."""
    x, y = xy
    font = _font(F_MONO_B, EYEBROW)
    label = text.upper()
    pad_x = EYEBROW // 2
    pad_y = EYEBROW // 4
    tw = _text_w(d, label, font)
    th = _line_h(font)
    chip_fill = hex_to_rgb(fill) if fill is not None else hex_to_rgb(theme.accent)
    x1 = x + tw + 2 * pad_x
    y1 = y + th + 2 * pad_y
    radius = (y1 - y) // 2
    d.rounded_rectangle((x, y, x1, y1), radius=radius, fill=chip_fill)
    # paper-colored text = the bright bg_top, for contrast on the soft accent chip
    d.text((x + pad_x, y + pad_y), label, font=font, fill=hex_to_rgb(theme.bg_top))
    return int(y1)


# ---------------------------------------------------------------------------
# title block
# ---------------------------------------------------------------------------
def title_block(d, text, theme, grid, *, top, max_lines=3) -> int:
    """Autosized (TITLE_MAX->TITLE_MIN), wrapped title in theme.ink.
    Draws at grid.text_x, wraps to grid.text_w. Returns bottom y."""
    font, lines = fit_title(
        d, text, grid.text_w,
        max_lines=max_lines, start=TITLE_MAX, floor=TITLE_MIN,
    )
    ink = hex_to_rgb(theme.ink)
    line_h = int(_line_h(font) * 1.06)
    y = int(top)
    for line in lines:
        d.text((grid.text_x, y), line, font=font, fill=ink)
        y += line_h
    return y


# ---------------------------------------------------------------------------
# meta line + series tag
# ---------------------------------------------------------------------------
def meta_line(d, xy, text, theme) -> None:
    """Mono ink_soft secondary line (subtitle / one-line thesis)."""
    font = _font(F_MONO, META)
    d.text(xy, text, font=font, fill=hex_to_rgb(theme.ink_soft))


def series_tag(d, xy, text, theme, *, default="SETI . PATENT ESSAYIST") -> None:
    """Letterspaced mono-caps series tag in ink_soft."""
    label = (text or default).upper()
    spaced = " ".join(list(label))
    font = _font(F_MONO_B, META)
    d.text(xy, spaced, font=font, fill=hex_to_rgb(theme.ink_soft))
