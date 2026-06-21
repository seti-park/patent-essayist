"""HeaderKit render utilities — SVG->PNG and illustration compositing.

See tools/headerkit/CONTRACT.md section 3.
"""

import io

import cairosvg
from PIL import Image


def svg_to_image(svg: str, width: int, height: int) -> Image.Image:
    """Rasterize an SVG string to a PIL RGBA image at the requested size."""
    png_bytes = cairosvg.svg2png(
        bytestring=svg.encode("utf-8"),
        output_width=width,
        output_height=height,
    )
    return Image.open(io.BytesIO(png_bytes)).convert("RGBA")


def load_cover(path: str, size) -> Image.Image:
    """Load an image file and cover-fit it (scale to fill + center-crop, no
    distortion) to ``size`` = (width, height). Used to place a supplied or
    AI-generated raster illustration into the header's art zone."""
    w, h = int(size[0]), int(size[1])
    im = Image.open(path).convert("RGBA")
    scale = max(w / im.width, h / im.height)
    nw, nh = max(round(im.width * scale), w), max(round(im.height * scale), h)
    im = im.resize((nw, nh), Image.LANCZOS)
    left, top = (nw - w) // 2, (nh - h) // 2
    return im.crop((left, top, left + w, top + h))


def paste_illustration(canvas, illo: Image.Image, box=None) -> None:
    """Alpha-composite an illustration onto `canvas`.

    If `box` is None the illustration is scaled full-bleed to the canvas size;
    otherwise it is scaled into box (x0, y0, x1, y1) and composited there.
    """
    illo = illo.convert("RGBA")
    base = canvas.convert("RGBA")
    if box is None:
        if illo.size != base.size:
            illo = illo.resize(base.size)
        base.alpha_composite(illo)
    else:
        x0, y0, x1, y1 = (int(v) for v in box)
        w = max(x1 - x0, 1)
        h = max(y1 - y0, 1)
        if illo.size != (w, h):
            illo = illo.resize((w, h))
        base.alpha_composite(illo, dest=(x0, y0))
    canvas.paste(base.convert("RGB"))
