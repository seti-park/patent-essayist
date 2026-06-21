"""HeaderKit AI-illustration engine — thesis -> bright/soft conceptual SVG.

Agent B component of the HeaderKit design system (see CONTRACT.md section 4 and
illustration_grammar.md). Turns an essay thesis into a bespoke, conceptual SVG
illustration rendered in the theme's bright/soft pastel palette so that
*illustration + title together imply the essay's content*.

Three backends, one contract:

  procedural : deterministic soft composition seeded from the spec. Used by
               tests/CI/gate. Same spec -> byte-identical SVG. Palette tokens only.
  llm        : LLM-authored bespoke SVG injected via the ``LLM_SVG_PROVIDER`` hook
               (or a per-spec attribute); falls back to procedural if none supplied.
  image-api  : documented credential-gated adapter seam. Raises NotImplementedError
               naming the env var it would need.

The visual grammar (palette use, layer model, glyph vocabulary, brightness/softness
rules, and how a human/LLM supplies a bespoke SVG) is documented in
``illustration_grammar.md`` — that file is the cross-backend "prompt contract".
"""

from __future__ import annotations

import hashlib
import logging
import math
import os
import random
from dataclasses import dataclass, field
from typing import Callable, Optional

from . import tokens

log = logging.getLogger(__name__)

# ViewBox of the illustration zone (the right/full conceptual portion of a 5:2 header).
VIEW_W, VIEW_H = 1500, 1200

# Optional module-level hook for the 'llm' backend. A human/agent may assign a
# callable here that takes an IllustrationSpec and returns a complete SVG string
# (or None to defer to procedural). See illustration_grammar.md.
LLM_SVG_PROVIDER: Optional[Callable[["IllustrationSpec"], Optional[str]]] = None

# Env var that the credential-gated image-API backend would require.
IMAGE_API_KEY_ENV = "HEADERKIT_IMAGE_API_KEY"


# ---------------------------------------------------------------------------
# Spec
# ---------------------------------------------------------------------------
@dataclass
class IllustrationSpec:
    """Inputs that fully determine an illustration (see CONTRACT.md section 4)."""

    title: str
    thesis: str                       # one-line essay thesis the illustration must imply
    keywords: list = field(default_factory=list)  # 3-6 concept anchors
    theme_name: str = "aurora"
    seed: Optional[int] = None        # derived from title if None (determinism)
    # Optional per-spec LLM SVG override for the 'llm' backend (takes precedence
    # over the module-level LLM_SVG_PROVIDER). May be a string or a callable.
    llm_svg: Optional[object] = None

    def resolved_seed(self) -> int:
        """Deterministic seed: explicit seed, else derived from the title via SHA-256."""
        if self.seed is not None:
            return int(self.seed)
        digest = hashlib.sha256(self.title.encode("utf-8")).hexdigest()
        return int(digest[:16], 16)


# ---------------------------------------------------------------------------
# Glyph vocabulary — keyword -> conceptual glyph
# ---------------------------------------------------------------------------
# Each entry: (glyph_id, set-of-trigger-substrings). Matching is substring-based,
# case-insensitive, over the keyword tokens. Order here is the deterministic
# preference order when several glyphs match.
_GLYPH_VOCAB = [
    ("lens",     {"vision", "camera", "lens", "eye", "see", "optic", "image", "view", "detect"}),
    ("clock",    {"time", "latency", "ms", "before", "predict", "speed", "fast", "delay", "realtime"}),
    ("shield",   {"safe", "airbag", "shield", "protect", "secure", "guard", "defen", "crash"}),
    ("layers",   {"print", "3d", "layer", "stack", "deposit", "additive", "weave", "fabric"}),
    ("waveform", {"signal", "wave", "sound", "audio", "rf", "radio", "frequency", "pulse", "sensor"}),
    ("network",  {"network", "node", "graph", "mesh", "connect", "link", "neural", "model", "data"}),
    ("battery",  {"battery", "energy", "power", "charge", "cell", "volt", "current"}),
    ("flow",     {"flow", "fluid", "valve", "pump", "thermal", "heat", "cool", "pressure"}),
]

# Fallback glyph when no keyword matches: a soft orbit/node motif.
_DEFAULT_GLYPH = "orbit"


def _select_glyphs(keywords, rng, max_glyphs=3):
    """Pick 1..max_glyphs conceptual glyphs deterministically from keywords.

    Deterministic: keywords are normalized + sorted, vocabulary order is fixed,
    no set iteration leaks into output. Returns a sorted, de-duplicated list.
    """
    norm = sorted({str(k).strip().lower() for k in keywords if str(k).strip()})
    chosen = []
    for glyph_id, triggers in _GLYPH_VOCAB:        # fixed vocab order
        for kw in norm:                            # sorted keyword order
            if any(t in kw for t in sorted(triggers)):
                chosen.append(glyph_id)
                break
    if not chosen:
        chosen = [_DEFAULT_GLYPH]
    # Cap to max_glyphs; if we have more matches than allowed, keep a stable subset
    # but let the seed rotate which ones appear so distinct theses vary.
    if len(chosen) > max_glyphs:
        start = rng.randrange(len(chosen))
        rotated = chosen[start:] + chosen[:start]
        chosen = sorted(set(rotated[:max_glyphs]))
    return chosen


# ---------------------------------------------------------------------------
# Color helpers (palette tokens only)
# ---------------------------------------------------------------------------
def _hex(theme_color: str) -> str:
    """Normalize a token hex string to lowercase '#rrggbb' for byte-stable output."""
    r, g, b = tokens.hex_to_rgb(theme_color)
    return f"#{r:02x}{g:02x}{b:02x}"


def _rgb_str(rgb) -> str:
    r, g, b = tokens.hex_to_rgb(rgb)
    return f"#{r:02x}{g:02x}{b:02x}"


# ---------------------------------------------------------------------------
# Glyph renderers — each returns SVG markup, drawn as thin/soft accent strokes
# ---------------------------------------------------------------------------
def _g(*children) -> str:
    return "".join(children)


def _glyph_lens(cx, cy, r, stroke):
    return _g(
        f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="none" '
        f'stroke="{stroke}" stroke-width="6" opacity="0.7"/>',
        f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r*0.55:.1f}" fill="none" '
        f'stroke="{stroke}" stroke-width="6" opacity="0.55"/>',
        f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r*0.16:.1f}" fill="{stroke}" '
        f'opacity="0.5"/>',
    )


def _glyph_clock(cx, cy, r, stroke):
    ticks = []
    for i in range(12):
        a = math.pi * 2 * i / 12
        x1 = cx + math.cos(a) * r
        y1 = cy + math.sin(a) * r
        x2 = cx + math.cos(a) * (r * 0.86)
        y2 = cy + math.sin(a) * (r * 0.86)
        ticks.append(
            f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
            f'stroke="{stroke}" stroke-width="5" opacity="0.55"/>'
        )
    return _g(
        f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="none" '
        f'stroke="{stroke}" stroke-width="6" opacity="0.7"/>',
        *ticks,
        f'<line x1="{cx:.1f}" y1="{cy:.1f}" x2="{cx:.1f}" y2="{cy-r*0.62:.1f}" '
        f'stroke="{stroke}" stroke-width="7" stroke-linecap="round" opacity="0.7"/>',
        f'<line x1="{cx:.1f}" y1="{cy:.1f}" x2="{cx+r*0.45:.1f}" y2="{cy+r*0.12:.1f}" '
        f'stroke="{stroke}" stroke-width="7" stroke-linecap="round" opacity="0.7"/>',
    )


def _glyph_shield(cx, cy, r, stroke):
    top = cy - r
    w = r * 0.82
    bot = cy + r * 1.15
    path = (
        f"M {cx-w:.1f} {top+r*0.18:.1f} "
        f"L {cx:.1f} {top:.1f} "
        f"L {cx+w:.1f} {top+r*0.18:.1f} "
        f"L {cx+w:.1f} {cy+r*0.2:.1f} "
        f"Q {cx+w:.1f} {bot-r*0.2:.1f} {cx:.1f} {bot:.1f} "
        f"Q {cx-w:.1f} {bot-r*0.2:.1f} {cx-w:.1f} {cy+r*0.2:.1f} Z"
    )
    return _g(
        f'<path d="{path}" fill="none" stroke="{stroke}" stroke-width="6" '
        f'stroke-linejoin="round" opacity="0.7"/>',
        f'<path d="M {cx-r*0.32:.1f} {cy+r*0.05:.1f} l {r*0.22:.1f} {r*0.28:.1f} '
        f'l {r*0.5:.1f} {-r*0.6:.1f}" fill="none" stroke="{stroke}" '
        f'stroke-width="7" stroke-linecap="round" stroke-linejoin="round" '
        f'opacity="0.6"/>',
    )


def _glyph_layers(cx, cy, r, stroke):
    parts = []
    for i, dy in enumerate((-r * 0.55, 0.0, r * 0.55)):
        y = cy + dy
        op = 0.7 - i * 0.12
        parts.append(
            f'<path d="M {cx-r:.1f} {y:.1f} L {cx:.1f} {y-r*0.32:.1f} '
            f'L {cx+r:.1f} {y:.1f} L {cx:.1f} {y+r*0.32:.1f} Z" '
            f'fill="none" stroke="{stroke}" stroke-width="6" '
            f'stroke-linejoin="round" opacity="{op:.2f}"/>'
        )
    return _g(*parts)


def _glyph_waveform(cx, cy, r, stroke):
    pts = []
    n = 24
    for i in range(n + 1):
        x = cx - r + (2 * r) * i / n
        amp = r * 0.5 * math.sin(i / n * math.pi * 4)
        env = math.sin(i / n * math.pi)        # taper ends
        y = cy + amp * env
        pts.append(f"{x:.1f},{y:.1f}")
    return _g(
        f'<polyline points="{" ".join(pts)}" fill="none" stroke="{stroke}" '
        f'stroke-width="6" stroke-linecap="round" stroke-linejoin="round" '
        f'opacity="0.7"/>'
    )


def _glyph_network(cx, cy, r, stroke):
    nodes = []
    for i in range(6):
        a = math.pi * 2 * i / 6
        nodes.append((cx + math.cos(a) * r, cy + math.sin(a) * r))
    nodes.append((cx, cy))
    edges = []
    center = nodes[-1]
    for nx, ny in nodes[:-1]:
        edges.append(
            f'<line x1="{center[0]:.1f}" y1="{center[1]:.1f}" '
            f'x2="{nx:.1f}" y2="{ny:.1f}" stroke="{stroke}" '
            f'stroke-width="4" opacity="0.45"/>'
        )
    dots = [
        f'<circle cx="{nx:.1f}" cy="{ny:.1f}" r="{r*0.12:.1f}" '
        f'fill="{stroke}" opacity="0.6"/>'
        for nx, ny in nodes
    ]
    return _g(*edges, *dots)


def _glyph_battery(cx, cy, r, stroke):
    w, h = r * 1.4, r * 0.9
    x0, y0 = cx - w / 2, cy - h / 2
    return _g(
        f'<rect x="{x0:.1f}" y="{y0:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{r*0.12:.1f}" '
        f'fill="none" stroke="{stroke}" stroke-width="6" opacity="0.7"/>',
        f'<rect x="{x0+w:.1f}" y="{cy-h*0.18:.1f}" width="{r*0.16:.1f}" height="{h*0.36:.1f}" '
        f'rx="{r*0.05:.1f}" fill="{stroke}" opacity="0.6"/>',
        f'<path d="M {cx-r*0.1:.1f} {y0+h*0.18:.1f} L {cx-r*0.32:.1f} {cy:.1f} '
        f'L {cx+r*0.02:.1f} {cy:.1f} L {cx-r*0.18:.1f} {y0+h*0.85:.1f}" '
        f'fill="none" stroke="{stroke}" stroke-width="6" stroke-linejoin="round" '
        f'opacity="0.65"/>',
    )


def _glyph_flow(cx, cy, r, stroke):
    pts = []
    n = 28
    for i in range(n + 1):
        t = i / n
        x = cx - r + (2 * r) * t
        y = cy + r * 0.45 * math.sin(t * math.pi * 2)
        pts.append(f"{x:.1f},{y:.1f}")
    arrow_x = cx + r
    arrow_y = cy
    return _g(
        f'<polyline points="{" ".join(pts)}" fill="none" stroke="{stroke}" '
        f'stroke-width="6" stroke-linecap="round" opacity="0.65"/>',
        f'<path d="M {arrow_x-r*0.18:.1f} {arrow_y-r*0.14:.1f} '
        f'L {arrow_x:.1f} {arrow_y:.1f} L {arrow_x-r*0.18:.1f} {arrow_y+r*0.14:.1f}" '
        f'fill="none" stroke="{stroke}" stroke-width="6" stroke-linecap="round" '
        f'stroke-linejoin="round" opacity="0.65"/>',
    )


def _glyph_orbit(cx, cy, r, stroke):
    return _g(
        f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{r:.1f}" ry="{r*0.46:.1f}" '
        f'fill="none" stroke="{stroke}" stroke-width="5" opacity="0.55"/>',
        f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{r*0.46:.1f}" ry="{r:.1f}" '
        f'fill="none" stroke="{stroke}" stroke-width="5" opacity="0.5"/>',
        f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r*0.16:.1f}" fill="{stroke}" opacity="0.6"/>',
        f'<circle cx="{cx+r:.1f}" cy="{cy:.1f}" r="{r*0.09:.1f}" fill="{stroke}" opacity="0.55"/>',
    )


_GLYPH_RENDERERS = {
    "lens": _glyph_lens,
    "clock": _glyph_clock,
    "shield": _glyph_shield,
    "layers": _glyph_layers,
    "waveform": _glyph_waveform,
    "network": _glyph_network,
    "battery": _glyph_battery,
    "flow": _glyph_flow,
    "orbit": _glyph_orbit,
}


# ---------------------------------------------------------------------------
# Procedural backend
# ---------------------------------------------------------------------------
def _procedural_svg(spec: IllustrationSpec) -> str:
    theme = tokens.THEMES.get(spec.theme_name, tokens.THEMES[tokens.DEFAULT_THEME])
    rng = random.Random(spec.resolved_seed())

    bg_top = _rgb_str(theme.bg_top)
    bg_bottom = _rgb_str(theme.bg_bottom)
    accents = [_hex(theme.accent), _hex(theme.accent2), _hex(theme.accent3)]

    # --- defs: gradient field + soft blur -------------------------------
    # Slight, seed-derived diagonal tilt keeps each field subtly unique but soft.
    angle = rng.uniform(0.0, 18.0)
    x2 = 50 + math.sin(math.radians(angle)) * 40
    defs = _g(
        f'<linearGradient id="field" x1="50%" y1="0%" x2="{x2:.1f}%" y2="100%">'
        f'<stop offset="0%" stop-color="{bg_top}"/>'
        f'<stop offset="100%" stop-color="{bg_bottom}"/>'
        f'</linearGradient>',
        '<filter id="soft" x="-40%" y="-40%" width="180%" height="180%">'
        '<feGaussianBlur stdDeviation="60"/></filter>',
        '<filter id="soft2" x="-40%" y="-40%" width="180%" height="180%">'
        '<feGaussianBlur stdDeviation="34"/></filter>',
    )

    # --- layer 1: luminous gradient field -------------------------------
    layer_field = (
        f'<rect x="0" y="0" width="{VIEW_W}" height="{VIEW_H}" fill="url(#field)"/>'
    )

    # --- layer 2: 2-4 large soft-edged accent blobs/arcs ----------------
    n_blobs = rng.randint(2, 4)
    blobs = []
    for i in range(n_blobs):
        color = accents[i % len(accents)]
        cx = rng.uniform(VIEW_W * 0.28, VIEW_W * 0.92)
        cy = rng.uniform(VIEW_H * 0.12, VIEW_H * 0.9)
        rad = rng.uniform(VIEW_W * 0.14, VIEW_W * 0.3)
        opacity = round(rng.uniform(0.18, 0.4), 3)
        flt = "soft" if i % 2 == 0 else "soft2"
        if rng.random() < 0.4:
            # soft arc/ellipse for variety
            rx = rad
            ry = rad * rng.uniform(0.55, 0.95)
            blobs.append(
                f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" '
                f'fill="{color}" opacity="{opacity}" filter="url(#{flt})"/>'
            )
        else:
            blobs.append(
                f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{rad:.1f}" '
                f'fill="{color}" opacity="{opacity}" filter="url(#{flt})"/>'
            )
    layer_blobs = _g(*blobs)

    # --- layer 3: lightweight conceptual glyphs -------------------------
    glyph_ids = _select_glyphs(spec.keywords, rng, max_glyphs=3)
    glyph_markup = []
    # Lay glyphs along a gentle arc in the central-right of the zone.
    n = len(glyph_ids)
    for i, gid in enumerate(glyph_ids):
        # deterministic placement
        frac = (i + 1) / (n + 1)
        gx = VIEW_W * (0.42 + 0.42 * frac)
        gy = VIEW_H * (0.34 + 0.34 * (i % 2))
        gr = rng.uniform(120, 170) if n == 1 else rng.uniform(95, 135)
        stroke = accents[(i + 1) % len(accents)]
        renderer = _GLYPH_RENDERERS.get(gid, _glyph_orbit)
        glyph_markup.append(
            f'<g transform="translate(0,0)">{renderer(gx, gy, gr, stroke)}</g>'
        )
    layer_glyphs = _g(*glyph_markup)

    body = _g(
        f"<defs>{defs}</defs>",
        f'<g id="field-layer">{layer_field}</g>',
        f'<g id="blob-layer">{layer_blobs}</g>',
        f'<g id="glyph-layer">{layer_glyphs}</g>',
    )

    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'viewBox="0 0 {VIEW_W} {VIEW_H}" '
        f'width="{VIEW_W}" height="{VIEW_H}">'
        f"{body}"
        f"</svg>"
    )
    return svg


# ---------------------------------------------------------------------------
# LLM backend
# ---------------------------------------------------------------------------
def _llm_svg(spec: IllustrationSpec) -> str:
    """Use an LLM-authored bespoke SVG if one is supplied; else fall back.

    Resolution order (first non-None wins):
      1. spec.llm_svg (string, or callable(spec) -> str|None)
      2. module-level LLM_SVG_PROVIDER callable
    Falls back to the deterministic procedural backend if neither yields an SVG.
    See illustration_grammar.md for the SVG the provider must return.
    """
    candidate = spec.llm_svg
    if callable(candidate):
        candidate = candidate(spec)
    if isinstance(candidate, str) and candidate.strip():
        return candidate

    if LLM_SVG_PROVIDER is not None:
        produced = LLM_SVG_PROVIDER(spec)
        if isinstance(produced, str) and produced.strip():
            return produced

    log.info(
        "illustration: backend='llm' but no LLM SVG supplied; "
        "falling back to procedural backend."
    )
    fallback = _procedural_svg(spec)
    # Embed a one-line note as an SVG comment for traceability.
    note = "<!-- llm backend: no SVG supplied, fell back to procedural -->"
    return fallback.replace("<svg ", note + "<svg ", 1)


# ---------------------------------------------------------------------------
# image-api backend (documented credential-gated seam)
# ---------------------------------------------------------------------------
def _image_api_svg(spec: IllustrationSpec) -> str:
    if not os.environ.get(IMAGE_API_KEY_ENV):
        raise NotImplementedError(
            "image-api backend is a documented adapter seam and is not wired up. "
            f"It requires the {IMAGE_API_KEY_ENV} environment variable (an external "
            "image-generation API key) plus an adapter that returns palette-compliant "
            "SVG. Set the key and implement the adapter, or use backend='procedural' "
            "or backend='llm'. See illustration_grammar.md (Image-API seam)."
        )
    raise NotImplementedError(
        f"{IMAGE_API_KEY_ENV} is set, but no image-API adapter is implemented yet. "
        "Implement the adapter in illustration._image_api_svg to honor the credential. "
        "See illustration_grammar.md (Image-API seam)."
    )


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------
_BACKENDS = {
    "procedural": _procedural_svg,
    "llm": _llm_svg,
    "image-api": _image_api_svg,
}


def generate_illustration_svg(spec: IllustrationSpec, *, backend: str = "procedural") -> str:
    """Return a complete SVG (viewBox 0 0 1500 1200) for the spec, palette tokens only.

    See CONTRACT.md section 4 for backend semantics.
    """
    if backend not in _BACKENDS:
        raise ValueError(
            f"unknown backend {backend!r}; choose from {sorted(_BACKENDS)}"
        )
    return _BACKENDS[backend](spec)


def _rasterize(svg: str, width: int, height: int):
    """SVG -> RGBA PIL image. Prefer render.svg_to_image; fall back to cairosvg."""
    try:
        from .render import svg_to_image  # type: ignore
    except Exception:
        svg_to_image = None
    if svg_to_image is not None:
        return svg_to_image(svg, width, height)

    # Local fallback so tests don't depend on render.py landing first.
    import io

    import cairosvg
    from PIL import Image

    png_bytes = cairosvg.svg2png(
        bytestring=svg.encode("utf-8"),
        output_width=width,
        output_height=height,
    )
    return Image.open(io.BytesIO(png_bytes)).convert("RGBA")


def render_illustration(
    spec: IllustrationSpec,
    out_png: str,
    *,
    width: int = VIEW_W,
    height: int = VIEW_H,
    backend: str = "procedural",
) -> str:
    """Render the illustration SVG to a PNG at ``out_png``; return ``out_png``."""
    svg = generate_illustration_svg(spec, backend=backend)
    img = _rasterize(svg, width, height)
    img.save(out_png)
    return out_png
