"""Unit tests for the HeaderKit foundation (tokens + components + render).

Runs under pytest:  python -m pytest tools/headerkit/tests/test_library.py -q
Or stand-alone:     python tools/headerkit/tests/test_library.py
"""

import os
import sys

# Make the repo root importable when run stand-alone (so `tools.headerkit` resolves).
_REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)

from PIL import Image  # noqa: E402

import tools.headerkit as hk  # noqa: E402
from tools.headerkit import (  # noqa: E402
    W, H, RATIO, THEMES, DEFAULT_THEME, GRID, TITLE_MIN, TITLE_MAX,
    Theme, brightness, is_soft,
    canvas, dot_grid, scrim_panel, eyebrow_chip, title_block,
    meta_line, series_tag, wrap_to_width, fit_title,
    svg_to_image, paste_illustration,
)

THEME = THEMES[DEFAULT_THEME]


# ---------------------------------------------------------------------------
# tokens
# ---------------------------------------------------------------------------
def test_ratio_is_5_2():
    assert RATIO == (5, 2)
    assert W / H == 2.5


def test_default_theme_present():
    assert DEFAULT_THEME == "aurora"
    assert "aurora" in THEMES
    assert isinstance(THEME, Theme)


def test_brightness_accepts_hex_and_tuple():
    assert abs(brightness((255, 255, 255)) - 255.0) < 1e-3
    assert brightness((0, 0, 0)) == 0.0
    assert abs(brightness("#FFFFFF") - 255.0) < 1e-3
    # hex and tuple agree
    assert abs(brightness("#2E3A46") - brightness((0x2E, 0x3A, 0x46))) < 1e-6


def test_is_soft_aurora():
    assert is_soft(THEME) is True


def test_ink_is_only_dark_token():
    # ink dark
    assert brightness(THEME.ink) < 150
    # every other color token bright
    for tok in (THEME.bg_top, THEME.bg_bottom,
                THEME.accent, THEME.accent2, THEME.accent3):
        assert brightness(tok) >= 150


def test_is_soft_false_when_a_fill_is_dark():
    bad = Theme(
        name="bad",
        bg_top=(10, 10, 10), bg_bottom=THEME.bg_bottom,
        ink=THEME.ink, ink_soft=THEME.ink_soft,
        accent=THEME.accent, accent2=THEME.accent2, accent3=THEME.accent3,
        scrim=THEME.scrim, grid=THEME.grid,
    )
    assert is_soft(bad) is False


# ---------------------------------------------------------------------------
# components
# ---------------------------------------------------------------------------
def test_canvas_size_and_type():
    img, d = canvas(THEME)
    assert isinstance(img, Image.Image)
    assert img.mode == "RGB"
    assert img.size == (3000, 1200)
    assert d is not None


def test_canvas_gradient_top_to_bottom():
    img, _ = canvas(THEME)
    top_px = img.getpixel((W // 2, 1))
    bot_px = img.getpixel((W // 2, H - 2))
    # top row near bg_top, bottom row near bg_bottom
    assert abs(top_px[0] - THEME.bg_top[0]) <= 3
    assert abs(bot_px[2] - THEME.bg_bottom[2]) <= 3
    assert top_px != bot_px


def test_wrap_to_width_wraps():
    _, d = canvas(THEME)
    from tools.headerkit.tokens import F_TITLE
    from PIL import ImageFont
    font = ImageFont.truetype(F_TITLE, TITLE_MAX)
    long = "word " * 40
    lines = wrap_to_width(d, long.strip(), font, GRID.text_w)
    assert len(lines) > 1
    assert wrap_to_width(d, "", font, GRID.text_w) == []


def test_fit_title_respects_max_lines():
    _, d = canvas(THEME)
    long = ("Adaptive Multi-Modal Latent Diffusion for Real-Time "
            "Autonomous Vehicular Perception Systems")
    font, lines = fit_title(d, long, GRID.text_w,
                            max_lines=3, start=TITLE_MAX, floor=TITLE_MIN)
    assert len(lines) <= 3
    assert TITLE_MIN <= font.size <= TITLE_MAX


def test_title_block_returns_y_in_canvas_and_wraps():
    img, d = canvas(THEME)
    long = ("A Very Long Patent Essay Title That Must Wrap Across Several "
            "Lines To Fit The Left Text Column Width Of The Header Canvas")
    bottom = title_block(d, long, THEME, GRID, top=200, max_lines=3)
    assert isinstance(bottom, int)
    assert 200 < bottom <= H


def test_eyebrow_chip_returns_int_bottom_y():
    _, d = canvas(THEME)
    y = eyebrow_chip(d, (GRID.text_x, 150), "US 12,345,678 . GRANTED", THEME)
    assert isinstance(y, int)
    assert y > 150


def test_scrim_panel_no_raise():
    img, _ = canvas(THEME)
    scrim_panel(img, THEME, GRID.scrim_box)
    assert img.size == (W, H)


def test_dot_grid_no_raise():
    img, d = canvas(THEME)
    dot_grid(d, THEME, GRID)
    assert img.size == (W, H)


def test_meta_and_series_no_raise():
    _, d = canvas(THEME)
    meta_line(d, (GRID.text_x, 900), "one-line thesis goes here", THEME)
    series_tag(d, (GRID.text_x, 1000), "SETI . PATENT ESSAYIST", THEME)


# ---------------------------------------------------------------------------
# render
# ---------------------------------------------------------------------------
def test_svg_to_image_renders_to_size():
    svg = ('<svg xmlns="http://www.w3.org/2000/svg" width="10" height="10">'
           '<rect width="10" height="10" fill="#F2A98C"/></svg>')
    img = svg_to_image(svg, 64, 48)
    assert isinstance(img, Image.Image)
    assert img.mode == "RGBA"
    assert img.size == (64, 48)


def test_paste_illustration_full_bleed_and_boxed():
    base, _ = canvas(THEME)
    illo = Image.new("RGBA", (300, 300), (159, 194, 221, 255))
    paste_illustration(base, illo)            # full-bleed
    assert base.size == (W, H)
    base2, _ = canvas(THEME)
    paste_illustration(base2, illo, box=(100, 100, 700, 700))   # boxed
    assert base2.size == (W, H)


# ---------------------------------------------------------------------------
# integration: nothing raises on the aurora theme
# ---------------------------------------------------------------------------
def test_full_compose_no_raise_on_aurora():
    img, d = canvas(THEME)
    dot_grid(d, THEME, GRID)
    scrim_panel(img, THEME, GRID.scrim_box)
    d2 = _redraw(img)
    yb = eyebrow_chip(d2, (GRID.text_x, GRID.scrim_box[1] + 40),
                      "US 12,000,000 . GRANTED", THEME)
    yt = title_block(d2, "How A Soft Lens Reframes Patent Search",
                     THEME, GRID, top=yb + 40, max_lines=3)
    meta_line(d2, (GRID.text_x, yt + 30), "one-line thesis", THEME)
    series_tag(d2, (GRID.text_x, GRID.scrim_box[3] - 80), None, THEME)
    assert img.size == (W, H)
    assert hk.is_soft(THEME)


def _redraw(img):
    from PIL import ImageDraw
    return ImageDraw.Draw(img)


if __name__ == "__main__":
    import traceback
    fns = [v for k, v in sorted(globals().items())
           if k.startswith("test_") and callable(v)]
    failed = 0
    for fn in fns:
        try:
            fn()
            print(f"PASS {fn.__name__}")
        except Exception:
            failed += 1
            print(f"FAIL {fn.__name__}")
            traceback.print_exc()
    print(f"\n{len(fns) - failed}/{len(fns)} passed")
    sys.exit(1 if failed else 0)
