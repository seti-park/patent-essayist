# Passes 2 + 3 — Bright/soft tone & Legibility

These are the **visual judgment** passes. They cannot be fully mechanized — they
read the rendered PNG — but they are anchored to the testable definitions in
`tools/headerkit/tokens.py` so findings stay objective.

## Pass 2 — Bright/soft tone

The deliverable is a **bright AND soft** header. "Bright/soft" is not a vibe; it
is the `is_soft(theme)` definition (CONTRACT.md section 1, `tokens.py`):

- **Bright:** every `bg_top`, `bg_bottom`, `accent`, `accent2`, `accent3` token
  has perceived luminance **>= 150** (on 0..255). The whole field reads light.
- **Soft:** the only low-luminance (dark) token is `ink` (the title). No harsh
  edges; adjacent fills stay close in luminance (no jarring contrast jumps).

### Sub-check 2A — token band (objective)

Confirm the theme used passes `is_soft()`:

```python
from tools.headerkit.tokens import THEMES, is_soft, brightness
assert is_soft(THEMES["aurora"])
```

If a non-default theme was used and `is_soft()` is False, that is a `high`
finding — the palette left the bright/soft band by construction.

### Sub-check 2B — rendered tone (visual)

The token check guarantees the *palette* is bright/soft, but the **illustration**
(`illustration.py`) composes shapes over the field and can still land too dark or
too harsh in pixels. Read the actual PNG:

- **No hard black.** Largest illustration forms should be soft accents at low
  opacity, not heavy dark masses. A dark illustration block = `medium` (`high` if
  it dominates the frame).
- **No harsh edges.** Soft-edged, layered forms — not hard geometric cuts with
  high local contrast. Photoreal or high-contrast clip-art = `medium`.
- **Airy.** Negative space reads light; the header feels open, not crowded.

A useful spot check: sample a few illustration regions and confirm perceived
`brightness(pixel) >= 150` away from the title; isolated dark glyph strokes are
fine, dark *fields* are not.

## Pass 3 — Legibility

The title (`theme.ink`, soft navy) must read cleanly. The composer puts a soft
RGBA **scrim panel** (`tokens.GRID.scrim_box`, `components.scrim_panel`) behind
the text column exactly so dark text stays legible over the bright illustration.
Check that this is working:

- **Ink-vs-background contrast in the text column.** `ink` (#1B232E,
  brightness ~56) over the scrim (light, ~248) is high contrast — good. If the
  illustration bled a dark form *under* the title and the scrim didn't fully
  cover it, contrast drops → `high` (title is the one thing that must read).
- **Title not colliding with a busy region.** The title block lives in the left
  column (`GRID.text_x`, `text_w=1500`); the illustration zone is to its right.
  If a glyph crowds into the text column, flag `medium`.
- **Autosize sanity.** `fit_title` shrinks `TITLE_MAX=208 → TITLE_MIN=124` and
  clamps to `max_lines`. A very long title clamped to the floor and still
  wrapping to a dense wall is hard to read → `medium`; a title truncated/clipped
  is `high`.
- **Meta + series legible too**, but at lower stakes (`ink_soft`); a faint meta
  line is `low`.

## Cross-pass: tone ↔ legibility

A single defect — an illustration form that landed too dark behind the text — can
trip **both** pass 2 (out of the soft band) and pass 3 (kills title contrast).
When both fire on the same region, file one `high` finding and note it spans both
passes; the fix (re-render with a lighter illustration / wider scrim) resolves
both. Prefer the legibility framing in the recommendation, since unreadable title
is the more severe failure.

## Severity quick-reference

| Observation | severity |
|---|---|
| Theme fails `is_soft()` (palette out of band) | high |
| Dark illustration mass dominating the frame | high |
| Title contrast insufficient over its column | high |
| Title clipped / truncated | high |
| Localized dark form, harsh edge, photoreal patch | medium |
| Glyph crowding the text column | medium |
| Title clamped to floor into a dense wall | medium |
| Faint meta/series line; minor airiness nit | low |
