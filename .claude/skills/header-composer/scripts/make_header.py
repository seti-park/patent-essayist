#!/usr/bin/env python3
"""Deterministic 5:2 X-Article header renderer for the patent-essay pipeline.

Renders a header PNG from a JSON spec (see handoff-template/04-promote/
header-spec.json). Two variants of the house light-editorial system:

  - "editorial": serif statement left, real patent figure (ink on paper) right,
    badge + kicker + bottom index strip.            (the V4 system)
  - "numbers":  struck old value -> giant new value, flat ink + orange.
                                                    (the V5 system)

Design system: references/design-system.md (cream paper / ink black / single
warm-orange accent / Fraunces + Space Grotesk + IBM Plex Mono / flat, no glow).

Deterministic: same spec + same assets => identical PNG (no noise, no RNG).

Requires Pillow (the only non-stdlib dependency in this repo, isolated to this
publication-asset stage — never imported by the gate layer):

    pip install pillow

Usage:
    python make_header.py --spec header-spec.json --out header.png
"""

import argparse
import json
import os
import sys

try:
    from PIL import Image, ImageDraw, ImageFont, ImageOps
except ImportError:
    sys.stderr.write("ERROR: Pillow is required: pip install pillow\n")
    sys.exit(2)

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, "..", "assets", "fonts")

W, H = 2000, 800  # 5:2

# ---------------------------------------------------------------------------
# Palette (design-system.md)
# ---------------------------------------------------------------------------
CREAM = (247, 243, 234)
INK = (20, 22, 27)
ACCENT = (228, 87, 46)       # warm editorial orange
PAPER_DIM = (185, 177, 160)  # dimmed ink for the "old" value
GRAY_TXT = (110, 103, 87)    # mono microcopy
TICK = (201, 194, 180)       # corner furniture
ARROW = (120, 113, 98)


def sg(size, wght=700):
    f = ImageFont.truetype(os.path.join(FONTS, "SpaceGrotesk.ttf"), size)
    f.set_variation_by_axes([wght])
    return f


def fraunces(size, wght=620, opsz=144):
    f = ImageFont.truetype(os.path.join(FONTS, "Fraunces.ttf"), size)
    f.set_variation_by_axes([opsz, wght, 0, 0])  # axes: opsz, wght, SOFT, WONK
    return f


def plex(size):
    return ImageFont.truetype(os.path.join(FONTS, "IBMPlexMono-Medium.ttf"), size)


def plex_sb(size):
    return ImageFont.truetype(os.path.join(FONTS, "IBMPlexMono-SemiBold.ttf"), size)


# ---------------------------------------------------------------------------
# Drawing helpers
# ---------------------------------------------------------------------------
def base():
    return Image.new("RGBA", (W, H), CREAM + (255,))


def corner_ticks(d):
    for (x, y) in [(56, 56), (W - 56, 56), (56, H - 56), (W - 56, H - 56)]:
        d.line([(x - 12, y), (x + 12, y)], fill=TICK, width=3)
        d.line([(x, y - 12), (x, y + 12)], fill=TICK, width=3)


def spaced(d, xy, text, font, fill, sp=0):
    """Letterspaced text; returns the x cursor after the last glyph."""
    x, y = xy
    for ch in text:
        d.text((x, y), ch, font=font, fill=fill)
        x += d.textlength(ch, font=font) + sp
    return x


def spaced_w(d, text, font, sp):
    return sum(d.textlength(c, font=font) + sp for c in text) - (sp if text else 0)


def kicker(d, xy, text, color=ACCENT, size=26, sp=6, bullet=True):
    x, y = xy
    if bullet:
        d.rectangle([x, y + 8, x + 12, y + 20], fill=ACCENT)
        x += 30
    spaced(d, (x, y), text, plex(size), color, sp)


def badge(d, xy, text, size=27, pad=(20, 10)):
    """Filled accent badge; returns bottom y."""
    x, y = xy
    f = plex_sb(size)
    tw = spaced_w(d, text, f, 5)
    bb = f.getbbox("Ag")
    th = bb[3] - bb[1]
    d.rectangle([x, y, x + tw + pad[0] * 2, y + th + pad[1] * 2], fill=ACCENT)
    spaced(d, (x + pad[0], y + pad[1] - bb[1] + 2), text, f, (255, 252, 247), 5)
    return y + th + pad[1] * 2


def index_strip(d, y, items, size=24, sp=6):
    """Centered bottom strip: ITEM • ITEM • ITEM with accent dots."""
    f = plex(size)
    total, seg = 0, []
    for i, it in enumerate(items):
        seg.append(("t", it))
        total += spaced_w(d, it, f, sp)
        if i < len(items) - 1:
            seg.append(("d", None))
            total += 46
    x = (W - total) // 2
    for kind, val in seg:
        if kind == "t":
            x = spaced(d, (x, y), val, f, GRAY_TXT, sp)
        else:
            d.ellipse([x + 18, y + 14, x + 28, y + 24], fill=ACCENT)
            x += 46


def staircase(d, x0, x1, yb, segs, color, width):
    """FIG.9-style stepped waveform: segs = [(frac_start, frac_end, dy), ...]."""
    pts = [(x0, yb)]
    for fs, fe, dy in segs:
        xs, xe = x0 + (x1 - x0) * fs, x0 + (x1 - x0) * fe
        pts += [(xs, yb), (xs, yb - dy), (xe, yb - dy), (xe, yb)]
    pts.append((x1, yb))
    d.line(pts, fill=color, width=width, joint="curve")


def figure_ink(path):
    """Patent drawing -> ink-on-transparent layer (keeps the authentic look)."""
    fig = Image.open(path).convert("L")
    fig = ImageOps.autocontrast(fig)
    inv = ImageOps.invert(fig).point(lambda p: 0 if p < 55 else min(255, int(p * 1.5)))
    inv = inv.crop(inv.getbbox())
    return inv


def fit_lines(d, lines, font_fn, base_size, max_w, min_size=72):
    """Shrink the headline font until every line fits max_w. Returns (font, size)."""
    size = base_size
    while size > min_size:
        f = font_fn(size)
        if all(d.textlength("".join(s["text"] for s in ln), font=f) <= max_w
               for ln in lines) :
            return f, size
        size -= 4
    return font_fn(min_size), min_size


# ---------------------------------------------------------------------------
# Variants
# ---------------------------------------------------------------------------
def render_editorial(spec):
    img = base()
    d = ImageDraw.Draw(img)
    corner_ticks(d)
    kicker(d, (92, 72), spec["kicker"])
    by = badge(d, (92, 140), spec["badge"]) if spec.get("badge") else 140

    # figure (right) first, so the headline knows its zone
    inv = figure_ink(spec["figure"]["file"])
    max_fw, max_fh = spec["figure"].get("max", [860, 560])
    sc = min(max_fw / inv.width, max_fh / inv.height)
    inv = inv.resize((int(inv.width * sc), int(inv.height * sc)), Image.LANCZOS)
    lay = Image.new("RGBA", inv.size, INK + (0,))
    lay.putalpha(inv.point(lambda p: int(p * 0.94)))
    fx, fy = W - 92 - inv.width, spec["figure"].get("top", 96)
    img.alpha_composite(lay, (fx, fy))
    d = ImageDraw.Draw(img)
    if spec["figure"].get("caption"):
        cy = fy + inv.height + 18
        d.rectangle([fx + 4, cy + 8, fx + 16, cy + 20], fill=ACCENT)
        spaced(d, (fx + 30, cy), spec["figure"]["caption"], plex(24), GRAY_TXT, 5)

    # headline (left), auto-fit to the space left of the figure
    max_w = fx - 88 - 48
    f_h, size = fit_lines(d, spec["headline"], lambda s: fraunces(s), spec.get("headline_size", 128), max_w)
    leading = int(size * 1.125)
    y = by + 34
    for ln in spec["headline"]:
        x = 88
        for segm in ln:
            color = ACCENT if segm.get("color") == "accent" else INK
            d.text((x, y), segm["text"], font=f_h, fill=color)
            x += d.textlength(segm["text"], font=f_h)
        y += leading

    if spec.get("strip"):
        index_strip(d, 732, spec["strip"])
    return img


def render_numbers(spec):
    img = base()
    d = ImageDraw.Draw(img)
    corner_ticks(d)
    kicker(d, (92, 72), spec["kicker"])
    if spec.get("kicker_right"):
        t = spec["kicker_right"]
        tw = spaced_w(d, t, plex(26), 6)
        spaced(d, (W - 92 - tw, 72), t, plex(26), GRAY_TXT, 6)

    BASE = 460
    f_old = sg(195, 640)
    old = spec["old_value"]
    d.text((140, BASE), old, font=f_old, fill=PAPER_DIM, anchor="ls")
    bb = d.textbbox((140, BASE), old, font=f_old, anchor="ls")
    sx0, sx1 = bb[0] - 26, bb[2] + 26
    sy0, sy1 = (bb[1] + bb[3]) // 2 + 26, (bb[1] + bb[3]) // 2 - 18
    d.line([(sx0, sy0), (sx1, sy1)], fill=ACCENT, width=14)
    for cx, cy in [(sx0, sy0), (sx1, sy1)]:
        d.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=ACCENT)

    ay = BASE - 78
    ax0 = bb[2] + 70
    d.line([(ax0, ay), (ax0 + 195, ay)], fill=ARROW, width=6)
    d.line([(ax0 + 160, ay - 30), (ax0 + 198, ay), (ax0 + 160, ay + 30)],
           fill=ARROW, width=6, joint="curve")

    f9 = sg(470, 700)
    nx = ax0 + 320
    d.text((nx, BASE + 10), spec["new_value"], font=f9, fill=INK, anchor="ls")
    bb9 = d.textbbox((nx, BASE + 10), spec["new_value"], font=f9, anchor="ls")

    CAPY = BASE + 86
    spaced(d, (bb[0] + 6, CAPY), spec["old_caption"], plex(28), GRAY_TXT, 6)
    c2 = spec["new_caption"]
    c2w = spaced_w(d, c2, plex(28), 6)
    cx = (bb9[0] + bb9[2]) // 2 - c2w // 2
    spaced(d, (min(max(cx, bb9[0] - 240), W - 92 - c2w), CAPY), c2, plex(28), ACCENT, 6)

    staircase(d, 92, 1908, 724,
              [(0.16, 0.24, 40), (0.40, 0.50, 62), (0.70, 0.76, 92)], ACCENT, 5)
    return img


VARIANTS = {"editorial": render_editorial, "numbers": render_numbers}


def main(argv=None):
    p = argparse.ArgumentParser(description="Render a 5:2 X-Article header from a JSON spec.")
    p.add_argument("--spec", required=True, help="path to header-spec.json")
    p.add_argument("--out", required=True, help="output PNG path")
    args = p.parse_args(argv)

    with open(args.spec, "r", encoding="utf-8") as fh:
        spec = json.load(fh)
    variant = spec.get("variant", "editorial")
    if variant not in VARIANTS:
        sys.stderr.write("ERROR: unknown variant %r (use: %s)\n" % (variant, ", ".join(VARIANTS)))
        return 2

    # Input problems (missing figure file, bad spec field) exit 2 with an
    # actionable message, never a bare traceback — same policy as the gates.
    try:
        img = VARIANTS[variant](spec)
    except (OSError, KeyError, ValueError, TypeError) as exc:
        sys.stderr.write("ERROR: spec/asset problem (%s): %s\n"
                         % (exc.__class__.__name__, exc))
        return 2
    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    img.convert("RGB").save(args.out)
    print("wrote %s (%dx%d, variant=%s)" % (args.out, W, H, variant))
    return 0


if __name__ == "__main__":
    sys.exit(main())
