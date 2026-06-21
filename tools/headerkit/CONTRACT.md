# HeaderKit — design-system contract (frozen interface)

The patent-essay **header design system**. One library, one source of truth for
tokens, components, and the AI-illustration engine. Every essay header is composed
from this kit — **no module outside `tools/headerkit/` may draw a header primitive
directly** (enforced by `gate_header`).

Output: a **5:2** bright/soft header image that, combined with the title, implies the
essay's content. Canonical raster: **3000 x 1200 PNG** (X Articles cover).

This file is the FROZEN contract. Parallel work builds against the names/signatures
below; integration reconciles against this file. Do not change a signature here
without updating every consumer.

---

## Package layout

```
tools/headerkit/
  __init__.py            re-exports public API (build_header, THEMES, ...)
  tokens.py              [Agent A] design tokens: themes, type scale, layout grid
  components.py          [Agent A] reusable draw components (canvas, title, chip, scrim, series)
  render.py              [Agent A] SVG->PNG + PNG helpers (cairosvg wrapper)
  illustration.py        [Agent B] AI-illustration engine (thesis -> SVG illustration)
  illustration_grammar.md[Agent B] the visual grammar / prompt contract for illustrations
  header.py              [INTEGRATOR] composer + CLI: illustration + title -> 5:2 header
  README.md              [Agent C] design-system documentation (replaces old header-style.md)
  CONTRACT.md            this file
  tests/                 unit tests (test_library.py [A], test_illustration.py [B], test_gate via C)
  fixtures/              sample IllustrationSpec inputs for validation
.claude/skills/header-review/   [Agent C] end-of-pipeline design review skill
_shared/scripts/gate_header.py  [Agent C] lint gate: no-bypass + 5:2 + token compliance
```

---

## 1. Tokens — `tokens.py`  (Agent A owns)

```python
RATIO   = (5, 2)
W, H    = 3000, 1200            # canonical render size; W/H == 2.5 exactly

@dataclass(frozen=True)
class Theme:
    name: str
    bg_top: tuple      # gradient field top color (RGB)
    bg_bottom: tuple   # gradient field bottom color (RGB)
    ink: str           # title ink (hex, soft navy)
    ink_soft: str      # meta/subtitle ink (hex)
    accent: str        # primary soft accent (hex)
    accent2: str       # secondary soft accent (hex)
    accent3: str       # tertiary soft accent (hex)
    scrim: tuple       # RGBA light panel behind text (legibility over illustration)
    grid: str          # faint dot grid (hex)

# PRIMARY theme — bright & soft ("aurora"). This is the default and the deliverable.
THEMES = {
  "aurora": Theme(
     name="aurora",
     bg_top=(253, 246, 239),     # #FDF6EF soft peach-cream  (BRIGHT)
     bg_bottom=(238, 243, 248),  # #EEF3F8 soft sky          (SOFT)
     ink="#2E3A46", ink_soft="#6B7682",
     accent="#F2A98C",           # soft coral
     accent2="#9FC2DD",          # soft sky
     accent3="#BfDcC8",          # soft mint
     scrim=(251, 248, 243, 200), # ~0.78 alpha light panel
     grid="#ECE6DC",
  ),
}
DEFAULT_THEME = "aurora"

# Type scale (Liberation; present at /usr/share/fonts/truetype/liberation)
FONT_DIR  = "/usr/share/fonts/truetype/liberation"
F_TITLE   = f"{FONT_DIR}/LiberationSans-Bold.ttf"
F_MONO    = f"{FONT_DIR}/LiberationMono-Regular.ttf"
F_MONO_B  = f"{FONT_DIR}/LiberationMono-Bold.ttf"
TITLE_MAX, TITLE_MIN = 188, 104   # autosize bounds
EYEBROW, META = 46, 42            # mono sizes

@dataclass(frozen=True)
class Grid:                        # layout for the 5:2 canvas
    margin: int = 130
    text_x: int = 130
    text_w: int = 1500            # left text column width (title wraps to this)
    scrim_box: tuple = (90, 150, 1640, 1050)   # x0,y0,x1,y1 light panel behind text
GRID = Grid()

def brightness(rgb) -> float:        # 0..255 perceived luminance (for review/tests)
def is_soft(theme: Theme) -> bool:   # True if palette stays in the bright/soft band
```

**Bright/soft definition (testable):** every `bg_*`, `accent*` token has perceived
luminance >= 150 (bright) and pairwise contrast of adjacent fills <= 4.5:1 (soft, no
harsh edges). `ink` is the only low-luminance token (title legibility). `is_soft()`
encodes this and the review skill + tests assert it.

---

## 2. Components — `components.py`  (Agent A owns)

All components take a Pillow `ImageDraw.Draw` and/or `Image`, a `Theme`, and a `Grid`.
They never hardcode colors — only token values.

```python
def canvas(theme: Theme, size=(W, H)) -> tuple[Image, ImageDraw]:
    """New RGB canvas filled with the vertical bg_top->bg_bottom soft gradient."""

def dot_grid(d, theme, grid) -> None
    """Faint token-colored dot grid across the canvas."""

def scrim_panel(canvas, theme, box) -> None
    """Composite the soft RGBA scrim rounded panel so text stays legible over art."""

def eyebrow_chip(d, xy, text, theme, *, fill=None) -> int
    """Small rounded mono-caps chip (patent no. / status). Returns chip bottom y."""

def title_block(d, text, theme, grid, *, top, max_lines=3) -> int
    """Autosized (TITLE_MAX->TITLE_MIN), wrapped title in theme.ink. Returns bottom y."""

def meta_line(d, xy, text, theme) -> None
    """Mono ink_soft secondary line (subtitle / one-line thesis)."""

def series_tag(d, xy, text, theme, *, default='SETI . PATENT ESSAYIST') -> None
    """Letterspaced mono-caps series tag in ink_soft."""

# text utilities (single source; previously duplicated 3x in the old scripts)
def wrap_to_width(d, text, font, max_w) -> list[str]
def fit_title(d, text, max_w, *, max_lines, start, floor) -> tuple[font, list[str]]
```

---

## 3. Render util — `render.py`  (Agent A owns)

```python
def svg_to_image(svg: str, width: int, height: int) -> Image   # cairosvg -> RGBA PIL
def paste_illustration(canvas, illo: Image, box=None) -> None   # full-bleed or boxed
```

---

## 4. Illustration engine — `illustration.py`  (Agent B owns)

The "AI-generated illustration" component. Bespoke per-essay conceptual art derived
from the thesis, rendered in the theme's bright/soft palette, so that **illustration +
title together imply the essay's content**.

```python
@dataclass
class IllustrationSpec:
    title: str
    thesis: str               # one-line essay thesis / what the illustration must imply
    keywords: list[str]       # 3-6 concept anchors pulled from the essay
    theme_name: str = "aurora"
    seed: int | None = None   # derived from title if None (determinism)

def generate_illustration_svg(spec: IllustrationSpec, *, backend="procedural") -> str:
    """Return a complete SVG (viewBox 0 0 1500 1200, the illustration zone of a 5:2
    header) using ONLY theme palette tokens.
      backend='procedural' : deterministic soft composition seeded from spec
                             (gradient field + soft conceptual forms keyed to keywords).
                             MUST be deterministic -> used by tests/CI/gate.
      backend='llm'        : LLM-authored bespoke SVG (insert via render_with_llm hook);
                             falls back to 'procedural' if no LLM artifact is supplied.
      backend='image-api'  : documented adapter seam (credential-gated; raises
                             NotImplementedError with a clear message if no key)."""

def render_illustration(spec, out_png, *, width=1500, height=1200, backend="procedural") -> str:
    """Render the SVG to PNG; returns out_png path."""
```

**Grammar (see `illustration_grammar.md`):** soft layered shapes — a luminous
gradient field (bg_top->bg_bottom), 2-4 large soft-edged forms in accent/accent2/
accent3 at low opacity, and lightweight conceptual glyph(s) abstracted from keywords
(e.g. a lens/eye, a timeline, a shield). Bright, airy, no hard black, no photoreal.
The illustration must read as *about something* (the thesis), not decoration.

---

## 5. Composer + CLI — `header.py`  (INTEGRATOR owns)

```python
def build_header(*, title, thesis, badge, series="SETI . PATENT ESSAYIST",
                 theme_name="aurora", backend="procedural",
                 keywords=None, out, size=(W,H)) -> str:
    """Full-bleed soft illustration (illustration.py) + dot grid + scrim panel +
    eyebrow chip + title block + meta(thesis) + series tag -> 5:2 PNG at `out`.
    Asserts out image is exactly 5:2. Returns out path."""

# CLI:
#   python -m tools.headerkit.header --title "..." --thesis "..." \
#       --badge "US ... . GRANTED" --backend procedural --out runs/<id>/header.png
```

---

## 6. Lint gate — `_shared/scripts/gate_header.py`  (Agent C owns)

`check_id`s, all hard unless noted:
- `gate_header_ratio`  — every PNG under `runs/**/header*.png` is exactly 5:2 (W/H==2.5).
- `gate_header_bypass` — no file outside `tools/headerkit/{components,render}.py` and
  `illustration.py` calls `ImageDraw.Draw(`, `Image.new(`, or hardcodes a hex color in
  a header context. Header CLIs/templates must route through headerkit.
- `gate_header_tokens` — header source imports palette from `tokens` (no stray hex).
Mirror the run-pattern of the existing `_shared/scripts/run_gates.py` (stdlib only,
returns pass/fail + check_ids, has a `test_gate_header.py`).

---

## 7. Review skill — `.claude/skills/header-review/`  (Agent C owns)

End-of-pipeline design-system review (mirror the editorial-review skill's shape:
SKILL.md + references/, structured YAML findings, NOT auto-fix). Passes:
1. **Format** — 5:2 ratio + 3000x1200 + file present (delegates to `gate_header_ratio`).
2. **Bright/soft tone** — palette within the soft band (`is_soft`), no harsh contrast,
   brightness >= threshold. 
3. **Legibility** — title contrast over the scrim/illustration is sufficient to read.
4. **Content coherence** — does illustration + title together imply the thesis?
   (the goal: "implicating the contents of essay when combined with the title").
5. **No-bypass** — routed through headerkit (delegates to `gate_header_bypass`).
Severity model: pass / revise-recommended / revise-required (match scoring-rubric).

---

## Status board (integrator updates)

- [x] Discard old header scripts + style doc
- [x] Freeze contract
- [x] Agent A — tokens + components + render + test_library (18/18 green)
- [x] Agent B — illustration engine + grammar + test_illustration (19/19 green)
- [x] Agent C — header-review skill + gate_header + README (gate tests green)
- [x] Integrator — header.py composer + scrim feather + pipeline wiring (P4) + reconcile
- [x] Validation — rendered runs/sample-essay/header.png (3000x1200, 5:2), visual + gate + review pass
- [x] Bug fixes during integration: gate_header repo-root depth (../../.. -> ../../../..)
      + test-file bypass exemption (regression-tested)
- [x] Commit + push

### Revision r2 — viral-X lessons (see docs/lessons/header-viral-lessons.md)

Token/composition values below evolved from the original spec (signatures unchanged):
- `ink` #2E3A46 -> **#1B232E** (near-black; high-contrast headline read at a glance);
  `ink_soft` #6B7682 -> **#5A6573**.
- Type: `TITLE_MAX,MIN` 188/104 -> **208/124** (headline-dominant); added **`F_SANS`**
  + **`SUBTITLE=56`** and a `subtitle_block` component (clear sans subtitle, not mono).
- Composition: text top-anchored, headline-first; **brand/series tag OFF by default**
  (`build_header(series="")`), opt back in via `series=` / `--series`.
