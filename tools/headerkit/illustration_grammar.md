# HeaderKit illustration grammar — the cross-backend prompt contract

This is the **visual grammar** for the AI-illustration engine (`illustration.py`,
Agent B). It defines what a HeaderKit illustration *is*, independent of the backend
that draws it, so the same illustration *intent* can be produced procedurally, by an
LLM, or by an external image API. Any backend that follows this grammar produces a
drop-in illustration for the 5:2 header composer (`header.py`).

Output is always a **standalone SVG**, `viewBox="0 0 1500 1200"`, the illustration
zone of a 5:2 header. It carries no title text — the composer overlays title/meta on
top. The illustration's job: **combined with the title, imply the essay's content.**

---

## 1. Palette — tokens only, bright + soft

Colors come **only** from the active theme (`tokens.THEMES[theme_name]`, default
`aurora`). No raw hex authored by hand, no pure black, no photoreal shading.

| Token        | aurora value | Role in the illustration                          |
|--------------|--------------|---------------------------------------------------|
| `bg_top`     | `#fdf6ef`    | gradient field, top stop (bright peach-cream)      |
| `bg_bottom`  | `#eef3f8`    | gradient field, bottom stop (soft sky)             |
| `accent`     | `#f2a98c`    | soft coral — blobs + glyph strokes                 |
| `accent2`    | `#9fc2dd`    | soft sky — blobs + glyph strokes                   |
| `accent3`    | `#bfdcc8`    | soft mint — blobs + glyph strokes                  |
| `ink`        | `#2e3a46`    | NOT used by the illustration (title ink only)      |

**Brightness/softness rules (testable):**

- Every fill/stroke is a `bg_*` or `accent*` token (all luminance >= 150 — bright).
- No `#000`, `#000000`, or hand-authored dark fill anywhere.
- Large forms sit at **low opacity (0.18-0.40)** and are **gaussian-blurred** so edges
  stay airy and luminous — no hard edges between adjacent fills.
- Glyph strokes are thin (4-7px in viewBox units) at moderate opacity (0.45-0.7).
- The result reads as soft conceptual art, not a flat diagram and not noise.

---

## 2. Layer model (three layers, back to front)

1. **Gradient field** — a single `<rect>` filling the viewBox with a `<linearGradient>`
   from `bg_top` (top) to `bg_bottom` (bottom). A small seed-derived diagonal tilt
   keeps each field subtly unique while staying soft. This is the luminous ground.

2. **Soft accent forms** — **2-4** large blobs/ellipses in `accent`/`accent2`/`accent3`
   at opacity 0.18-0.40, each behind a `feGaussianBlur` filter (`stdDeviation` ~34-60).
   Positions, sizes, count, and circle-vs-ellipse are seeded. These give the image its
   depth and color mood without any hard shape.

3. **Conceptual glyph(s)** — **1-3** lightweight, thin-stroke glyphs abstracted from the
   keywords (see §3). These are what make the illustration read as *about something*.
   They are drawn as accent strokes (not filled silhouettes) so they stay airy.

---

## 3. Glyph vocabulary (keyword -> concept)

Glyphs are selected by case-insensitive **substring** match of the spec's `keywords`
against a fixed vocabulary. Selection is deterministic: keywords are normalized and
sorted, the vocabulary order below is the tie-break preference, and the chosen list is
de-duplicated and capped at 3 (the seed rotates which subset shows when more match).

| Glyph id   | Trigger substrings (any)                                               | Reads as            |
|------------|-----------------------------------------------------------------------|---------------------|
| `lens`     | vision, camera, lens, eye, see, optic, image, view, detect            | a lens / eye ring   |
| `clock`    | time, latency, ms, before, predict, speed, fast, delay, realtime      | a clock / timing    |
| `shield`   | safe, airbag, shield, protect, secure, guard, defen, crash            | a soft shield       |
| `layers`   | print, 3d, layer, stack, deposit, additive, weave, fabric             | stacked layers      |
| `waveform` | signal, wave, sound, audio, rf, radio, frequency, pulse, sensor       | a waveform          |
| `network`  | network, node, graph, mesh, connect, link, neural, model, data        | a node graph        |
| `battery`  | battery, energy, power, charge, cell, volt, current                   | a battery / bolt    |
| `flow`     | flow, fluid, valve, pump, thermal, heat, cool, pressure               | a flow arrow        |
| `orbit`    | *(default — used when no keyword matches)*                            | a soft orbit / node |

To extend the vocabulary, add a `(glyph_id, {triggers})` entry to `_GLYPH_VOCAB` and a
matching renderer in `_GLYPH_RENDERERS`. Keep renderers stroke-based and palette-only.

---

## 4. Determinism

The procedural backend is **byte-deterministic**: same `IllustrationSpec` -> identical
SVG string. This is what tests/CI/the gate rely on. Rules the backend obeys:

- All randomness flows through one `random.Random(seed)`.
- `seed` is taken from `spec.seed`, or derived from `spec.title` via SHA-256 if `None`.
- No wall-clock time, no PID, no unordered `set`/`dict` iteration leaks into output.
  Any keyword-derived choice is sorted before use.
- Floats are formatted at fixed precision (`%.1f` / rounded opacities).

---

## 5. Backends

### `procedural` (default; tests/CI/gate)
Deterministic soft composition seeded from the spec, following §1-4. No network, no
credentials. This is the reference implementation of the grammar.

### `llm` (LLM-authored bespoke SVG)
For a hand- or LLM-crafted illustration that still obeys §1-3. The engine resolves an
SVG from, in order:

1. `spec.llm_svg` — a complete SVG **string**, or a **callable** `fn(spec) -> str|None`.
2. The module-level hook `illustration.LLM_SVG_PROVIDER` — a callable `fn(spec) -> str|None`.

If neither yields a non-empty SVG, the engine logs a one-line note and falls back to
the `procedural` backend (annotated with an SVG comment). **How to supply one:**

```python
from tools.headerkit import illustration as illo

# Option A — per-spec string (e.g. an LLM was asked to author the SVG):
spec = illo.IllustrationSpec(title="...", thesis="...", keywords=[...],
                             llm_svg=svg_string_from_llm)
svg = illo.generate_illustration_svg(spec, backend="llm")

# Option B — a module-level provider used for every 'llm' render:
def my_provider(spec):
    prompt = build_prompt(spec)          # see the prompt contract below
    return call_llm(prompt)              # must return a complete SVG string or None
illo.LLM_SVG_PROVIDER = my_provider
```

**Prompt contract for an LLM provider** — instruct the model to return *only* a
complete SVG with `viewBox="0 0 1500 1200"`, using *only* the active theme's token hex
values (§1), following the three-layer model (§2) and choosing glyphs that imply the
thesis (§3): a luminous `bg_top -> bg_bottom` gradient field, 2-4 large soft blurred
accent forms at 0.18-0.40 opacity, and 1-3 thin-stroke conceptual glyphs. Bright, airy,
no hard black, no photoreal. The returned SVG is used verbatim.

### `image-api` (credential-gated seam)
A documented adapter seam for an external image-generation API. It is **not wired up**.
`generate_illustration_svg(spec, backend="image-api")` raises `NotImplementedError`
naming the env var it would need: **`HEADERKIT_IMAGE_API_KEY`**. To implement, set that
env var and fill in `illustration._image_api_svg` so it calls the API and returns a
palette-compliant SVG (or rasterizes + traces to SVG). The seam exists so the engine's
public surface already accounts for a credentialed backend without shipping one.

---

## 6. Public API (frozen — see CONTRACT.md §4)

```python
@dataclass
class IllustrationSpec:
    title: str
    thesis: str
    keywords: list[str]
    theme_name: str = "aurora"
    seed: int | None = None        # derived from title via SHA-256 if None
    llm_svg: object | None = None  # str or callable(spec)->str|None, for backend='llm'

def generate_illustration_svg(spec, *, backend="procedural") -> str
def render_illustration(spec, out_png, *, width=1500, height=1200, backend="procedural") -> str
```
