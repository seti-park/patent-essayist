#!/usr/bin/env python3
"""Investor-edition 5:2 header: dual ticker chips, company logo strip, and a
whiteboard "analyst slide" (patent figure -> gigacast underbody -> rocket + ?)
presented by Gyeongtae. Companion to make_header_mascot.py; same brand tokens.

  python tools/make_header_investor.py \
      --title "Print It or Keep It Hard" \
      --patent "US 2026/0158546 A1 . PENDING . INVESTOR EDITION" \
      --figure input/figures/fig-02C.png \
      --out runs/<essay-id>/header-investor.png

Logos: tools/assets/logos/*.svg (simple-icons, CC0), rendered monochrome ink,
editorial reference to the companies discussed.
"""
import argparse
import io
import math
import os
import sys

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from make_header import (ACCENT, F_MONO, F_MONO_B, INK, INK_SOFT, PAPER,
                         H, W, decorate, fit_title)
from make_header_mascot import TEXT_X, TEXT_W, draw_easel, paste_mascot

LOGO_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "assets", "logos")
CAST_TINT = (240, 213, 206)
NAVY_CHIP = (44, 53, 67)


def arrow(d, p0, p1):
    d.line([p0, p1], fill=ACCENT, width=10)
    ang = math.atan2(p1[1] - p0[1], p1[0] - p0[0])
    for da in (2.6, -2.6):
        d.line([p1, (p1[0] - 26 * math.cos(ang + da),
                     p1[1] - 26 * math.sin(ang + da))], fill=ACCENT, width=10)


def draw_underbody(d, x, y, w, h):
    """Top-view skateboard platform; front/rear casting zones tinted."""
    for wx in (x + 26, x + w - 82):
        for wy in (y - 16, y + h - 10):
            d.rounded_rectangle((wx, wy, wx + 56, wy + 26), radius=10, fill=INK)
    d.rounded_rectangle((x, y, x + w, y + h), radius=34, fill=(255, 255, 255),
                        outline=INK, width=6)
    d.rounded_rectangle((x + 10, y + 10, x + int(w * 0.30), y + h - 10),
                        radius=22, fill=CAST_TINT, outline=ACCENT, width=4)
    d.rounded_rectangle((x + int(w * 0.70), y + 10, x + w - 10, y + h - 10),
                        radius=22, fill=CAST_TINT, outline=ACCENT, width=4)
    for i in range(1, 4):
        lx = x + int(w * 0.30) + int(w * 0.40) * i // 4
        d.line((lx, y + 18, lx, y + h - 18), fill=(180, 170, 148), width=4)


def draw_rocket(d, x, y, h):
    w = int(h * 0.40)
    cx = x + w // 2
    nose = int(h * 0.30)
    body_bot = y + int(h * 0.82)
    pts = [(x, y + nose), (cx, y), (x + w, y + nose), (x + w, body_bot),
           (x, body_bot)]
    d.polygon(pts, fill=(255, 255, 255))
    d.line(pts + [pts[0]], fill=INK, width=6, joint="curve")
    d.polygon([(x, y + nose), (cx, y), (x + w, y + nose)], fill=CAST_TINT)
    d.line([(x, y + nose), (cx, y), (x + w, y + nose)], fill=INK, width=6,
           joint="curve")
    for fx, dx in ((x, -int(w * 0.45)), (x + w, int(w * 0.45))):
        d.polygon([(fx, body_bot), (fx + dx, y + h), (fx, y + int(h * 0.6))],
                  fill=INK)
    d.ellipse((cx - 14, y + nose + 18, cx + 14, y + nose + 46), fill=PAPER,
              outline=INK, width=5)


def board_slide(canvas, d, figure):
    from PIL import ImageChops
    from make_header import crop_drawing
    x0, y0, x1, y1 = 1566, 200, 2010, 830     # left half of the board face
    fig = crop_drawing(figure)
    k = min((x1 - x0) / fig.width, (y1 - y0) / fig.height)
    fig = fig.resize((int(fig.width * k), int(fig.height * k)), Image.LANCZOS)
    fx = x0 + (x1 - x0 - fig.width) // 2
    fy = y0 + (y1 - y0 - fig.height) // 2
    region = canvas.crop((fx, fy, fx + fig.width, fy + fig.height))
    canvas.paste(ImageChops.multiply(region, fig.convert("RGB")), (fx, fy))
    ub_x, ub_y, ub_w, ub_h = 2078, 268, 300, 124
    draw_underbody(d, ub_x, ub_y, ub_w, ub_h)
    draw_rocket(d, 2160, 500, 190)
    f_q = ImageFont.truetype(F_MONO_B, 84)
    d.text((2280, 540), "?", font=f_q, fill=ACCENT)
    arrow(d, (2008, 430), (2066, 340))
    arrow(d, (2008, 520), (2138, 570))
    f_lab = ImageFont.truetype(F_MONO, 30)
    d.text((ub_x + 62, ub_y + ub_h + 26), "gigacasting", font=f_lab,
           fill=INK_SOFT)
    d.text((2138, 716), "aerospace", font=f_lab, fill=INK_SOFT)


def logo_strip(canvas, d, y):
    import cairosvg
    x = TEXT_X
    f = ImageFont.truetype(F_MONO_B, 40)
    for name, label in (("tesla", "TESLA"), ("spacex", "SPACEX")):
        png = cairosvg.svg2png(url=os.path.join(LOGO_DIR, name + ".svg"),
                               output_width=54, output_height=54)
        ic = Image.open(io.BytesIO(png)).convert("RGBA")
        tint = Image.new("RGBA", ic.size, INK + (255,))
        tint.putalpha(ic.getchannel("A"))
        canvas.paste(tint, (x, y), tint)
        d.text((x + 70, y + 8), label, font=f, fill=INK)
        x += 70 + int(d.textlength(label, font=f)) + 64


def text_block(canvas, d, tickers, title, patent, series):
    y = 225
    f_tick = ImageFont.truetype(F_MONO_B, 64)
    x = TEXT_X
    for ticker, color in zip(tickers, (ACCENT, NAVY_CHIP)):
        tw = int(d.textlength(ticker, font=f_tick))
        d.rounded_rectangle((x, y, x + tw + 64, y + 108), radius=16, fill=color)
        d.text((x + 32, y + 22), ticker, font=f_tick, fill=PAPER)
        x += tw + 64 + 24
    y += 108 + 52
    f_title, lines = fit_title(d, title, TEXT_W, max_lines=2, start=170)
    for ln in lines:
        d.text((TEXT_X, y), ln, font=f_title, fill=INK)
        y += int(f_title.size * 1.12)
    y += 30
    d.text((TEXT_X, y), patent, font=ImageFont.truetype(F_MONO, 42),
           fill=INK_SOFT)
    logo_strip(canvas, d, y + 76)
    d.text((TEXT_X, y + 170), " ".join(series.upper()),
           font=ImageFont.truetype(F_MONO_B, 40), fill=INK_SOFT)


def main():
    ap = argparse.ArgumentParser(description="Investor 5:2 essay header")
    ap.add_argument("--tickers", default="$TSLA,$SPCX")
    ap.add_argument("--title", required=True)
    ap.add_argument("--patent", required=True)
    ap.add_argument("--figure", required=True,
                    help="patent figure for the board (left panel)")
    ap.add_argument("--series", default="SETI . PATENT ESSAYIST")
    ap.add_argument("--style", choices=["comic", "flat"], default="comic")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    canvas = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(canvas)
    decorate(d)
    draw_easel(canvas, d)
    board_slide(canvas, d, args.figure)
    paste_mascot(canvas, args.style)
    d = ImageDraw.Draw(canvas)
    text_block(canvas, d, args.tickers.split(","), args.title, args.patent,
               args.series)
    canvas.save(args.out, optimize=True)
    print(args.out, canvas.size)


if __name__ == "__main__":
    main()
