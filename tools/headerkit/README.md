# HeaderKit — the patent-essay header design system

HeaderKit is the design system for **essay header images** in the patent-essay
pipeline. One library, one source of truth for tokens, components, and the
AI-illustration engine. Every essay header is composed from this kit — **no
module outside `tools/headerkit/` may draw a header primitive directly**
(enforced by the `gate_header` lint gate).

> **Deliverable:** a **5:2**, **bright + soft** header image (canonical
> **3000 x 1200 PNG**, the X-Articles cover size) whose AI-generated illustration
> and title **together imply the essay's content**.

The frozen interface for everything below is `tools/headerkit/CONTRACT.md`. This
README is the human-facing tour; the CONTRACT is the authority. (This file
replaces the deleted one-off `tools/header-style.md`.)

---

## What it is (and what changed)

Headers used to be one-off scripts — each essay had its own bespoke drawing code
that hardcoded colors and sizes and could drift off-ratio or off-brand without
anything catching it. HeaderKit replaces that with a real design system:

- **Tokens** define the palette, type scale, and layout grid once.
- **Components** are reusable draw primitives that read *only* tokens.
- **An illustration engine** turns the essay's thesis + keywords into bespoke,
  on-theme conceptual art.
- **A composer + CLI** (`header.py`) assembles illustration + title into the 5:2
  PNG and asserts the ratio.
- **A lint gate** (`gate_header`) fails any code that bypasses the library or any
  output that isn't 5:2 / token-sourced.
- **A review skill** (`header-review`) runs at the end of the pipeline and judges
  whether the rendered header is bright/soft, legible, and actually *about* the
  essay.

---

## Package map

```
tools/headerkit/
  __init__.py             public API re-exports (tokens + components + render utils)
  tokens.py               design tokens: themes, type scale, layout grid, is_soft()
  components.py           reusable draw components (canvas, title, chip, scrim, grid, series)
  render.py               SVG->PNG + illustration compositing (cairosvg + Pillow)
  illustration.py         AI-illustration engine (thesis -> on-theme SVG)
  illustration_grammar.md the visual grammar / prompt contract for illustrations
  header.py               composer + CLI: illustration + title -> 5:2 header   [integrator]
  README.md               this file
  CONTRACT.md             the frozen interface (authority)
  tests/                  test_library.py, test_illustration.py
  fixtures/               sample IllustrationSpec inputs

.claude/skills/header-review/        end-of-pipeline design review skill
.claude/skills/_shared/scripts/gate_header.py   lint gate: no-bypass + 5:2 + token compliance
```

Public API (import from the package, never reach for raw Pillow):

```python
from tools.headerkit import (
    THEMES, DEFAULT_THEME, is_soft, brightness,    # tokens
    canvas, dot_grid, scrim_panel, eyebrow_chip,   # components
    title_block, meta_line, series_tag,
    svg_to_image, paste_illustration,              # render
)
```

---

## Token themes — `tokens.py`

The canvas is **5:2** (`RATIO = (5, 2)`, `W, H = 3000, 1200`, so `W/H == 2.5`
exactly). All styling values live in `tokens.py`; nothing else hardcodes a color
or size.

### `aurora` — bright & soft (the default and the deliverable)

| Token | Value | Role |
|---|---|---|
| `bg_top` | `#FDF6EF` soft peach-cream | gradient field top (bright) |
| `bg_bottom` | `#EEF3F8` soft sky | gradient field bottom (soft) |
| `ink` | `#1B232E` near-black navy | title ink — high contrast for at-a-glance reading (the only dark token) |
| `ink_soft` | `#5A6573` | subtitle / meta ink |
| `accent` | `#F2A98C` soft coral | primary accent |
| `accent2` | `#9FC2DD` soft sky | secondary accent |
| `accent3` | `#BFDCC8` soft mint | tertiary accent |
| `scrim` | `rgba(251,248,243,200)` | light panel behind text (legibility) |
| `grid` | `#ECE6DC` | faint dot grid |

**Type scale:** Liberation fonts (`/usr/share/fonts/truetype/liberation`); the
headline is dominant — title autosizes `TITLE_MAX=208 → TITLE_MIN=124` (bold),
the subtitle is a clear sans (`F_SANS`, `SUBTITLE=56`) so the key sentence reads
at a glance, mono eyebrow chip at 46.
**Layout:** `Grid` — 130px margin, a left text column, and a scrim box behind it.
The header carries **no brand tag by default** (the author's handle carries the
brand on X); pass `series=` / `--series` to opt the tag back in.

### Bright/soft, made testable

"Bright/soft" is not a vibe — it is `is_soft(theme)`:

- **bright:** every `bg_*` and `accent*` token has perceived luminance **>= 150**;
- **soft:** `ink` is the **only** low-luminance token.

```python
from tools.headerkit import THEMES, is_soft, brightness
assert is_soft(THEMES["aurora"])
brightness("#FDF6EF")   # ~246  (bright)
brightness("#1B232E")   # ~34   (the dark title ink — high contrast)
```

Both the tests and the `header-review` skill assert this band, so a new theme
that drifts dark or harsh is caught mechanically.

---

## How the AI-illustration backend works — `illustration.py`

The illustration is the "AI-generated" half of the deliverable: bespoke
per-essay conceptual art derived from the thesis, in the theme's bright/soft
palette, so **illustration + title together imply the content**. It is driven by
an `IllustrationSpec`:

```python
from tools.headerkit.illustration import IllustrationSpec, generate_illustration_svg

spec = IllustrationSpec(
    title="How Tesla Vision Vindicated the Rotational Crash Model",
    thesis="Vision-fusion cuts airbag-deploy latency below the accelerometer baseline",
    keywords=["vision", "fusion", "timeline", "airbag", "milliseconds"],
    theme_name="aurora",
    seed=None,        # derived deterministically from the title if None
)
svg = generate_illustration_svg(spec, backend="procedural")
```

It returns a complete SVG (viewBox `0 0 1500 1200`, the illustration zone of the
5:2 header) using **only theme palette tokens**. The **visual grammar** (see
`illustration_grammar.md`): a luminous `bg_top→bg_bottom` gradient field, 2-4
large soft-edged accent forms at low opacity, and lightweight **conceptual
glyph(s)** abstracted from the keywords (lens, clock/timeline, shield, layers,
waveform, network, battery, flow, orbit). Bright, airy, no hard black, no
photoreal — the image must read as *about something*, not decoration.

Three backends, one contract:

- **`procedural`** (default) — deterministic soft composition seeded from the
  spec. Because it is deterministic, this is the backend used by tests, CI, and
  the gate.
- **`llm`** — LLM-authored bespoke SVG via the `LLM_SVG_PROVIDER` hook (or a
  per-spec override). **Falls back to `procedural`** if no LLM artifact is
  supplied, so it never breaks a build.
- **`image-api`** — a documented, credential-gated adapter seam. Raises
  `NotImplementedError` with a clear message when no API key is configured.

`render_illustration(spec, out_png, backend=...)` rasterizes the SVG to PNG via
`render.svg_to_image` (cairosvg → Pillow).

---

## How to generate a header — `header.py` (CLI)

The composer assembles the full-bleed illustration + dot grid + feathered scrim
panel + eyebrow chip + dominant title block + clear sans subtitle (thesis) into
the 5:2 PNG, and **asserts the output is exactly 5:2** before returning the path.
The text block is top-anchored and headline-first; no brand tag is drawn unless
`series=` is passed.

```python
from tools.headerkit.header import build_header

build_header(
    title="How Tesla Vision Vindicated the Rotational Crash Model",
    thesis="Vision-fusion cuts airbag-deploy latency below the accelerometer baseline",
    badge="US 11,123,456 B2 . GRANTED",
    # series="SETI . PATENT ESSAYIST",  # optional; off by default (no brand watermark)
    theme_name="aurora",
    backend="procedural",
    keywords=["vision", "fusion", "timeline", "airbag", "milliseconds"],
    out="runs/044-tesla-rcm/header.png",
)
```

CLI:

```
python -m tools.headerkit.header \
    --title  "How Tesla Vision Vindicated the Rotational Crash Model" \
    --thesis "Vision-fusion cuts airbag-deploy latency below the accelerometer baseline" \
    --badge  "US 11,123,456 B2 . GRANTED" \
    --backend procedural \
    --out runs/044-tesla-rcm/header.png
```

> `header.py` is owned by the integrator; if it is not present yet in your
> checkout, compose directly from the public API (`canvas` → `paste_illustration`
> → `scrim_panel` → `eyebrow_chip` → `title_block` → `meta_line` → `series_tag`),
> still using only tokens and components.

---

## The lint gate — `gate_header.py`

`_shared/scripts/gate_header.py` is the deterministic guardrail. Stdlib only
(Pillow is optional, used only for the ratio check), same run-pattern as the
essay text gates (`run_gates.py`): each check returns pass/fail + `check_id`s and
`main()` exits nonzero on any hard fail.

```
python .claude/skills/_shared/scripts/gate_header.py
python .claude/skills/_shared/scripts/test_gate_header.py   # the paired test suite
```

Checks (all hard; `*-000` are informational notes so an empty/partial repo
passes):

| `check_id` | Fails when |
|---|---|
| `HEADER-RATIO-001` | a `runs/**/header*.png` is not exactly 5:2 (2.5), or is unopenable |
| `HEADER-BYPASS-001` | `ImageDraw.Draw(` / `Image.new(` is used **outside** the headerkit draw allowlist (`components.py`, `render.py`, `illustration.py`) |
| `HEADER-TOKENS-001` | a header source carries a raw `#RRGGBB` literal instead of a token |
| `HEADER-TOKENS-002` | a drawing header source does not import palette from `tokens` |

`tokens.py` and `illustration.py` are allowlisted for hex literals (they
legitimately define / emit token hex into SVG).

---

## The review skill — `header-review`

`.claude/skills/header-review/` is the end-of-pipeline **design review** — the
visual sibling of `editorial-review`. It runs on a generated `header.png` plus
the essay's title + thesis and emits structured YAML findings (NOT auto-fix).
Five passes:

1. **Format** — 5:2 + 3000x1200 + present (delegates to `gate_header_ratio`).
2. **Bright/soft tone** — palette in the soft band (`is_soft`), no harsh contrast.
3. **Legibility** — title reads cleanly over the scrim / illustration.
4. **Content coherence** — do illustration + title together imply the thesis?
5. **No-bypass** — routed through HeaderKit (delegates to `gate_header_bypass`).

Severity model matches `_shared/references/scoring-rubric.md`: per-finding
`critical / high / medium / low`, rolled into one `overall_assessment`
(`pass / revise-recommended / revise-required`). Any `gate_header` fail (pass 1
or 5) hard-forces `revise-required`. A human applies findings by re-running
`build_header`.

---

## Invariants (don't break these)

- Output is **always 5:2** (`W/H == 2.5`); `build_header` asserts it.
- **No color or size is hardcoded** outside `tokens.py`; everything reads tokens.
- **No header primitive is drawn outside `tools/headerkit/`** — `gate_header`
  enforces it.
- The **`procedural` illustration backend is deterministic** (tests/CI/gate rely
  on it).
- Changing a signature means updating `CONTRACT.md` and every consumer.
