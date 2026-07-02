# Header detection + rotation — the vision decision spec

The semantic calls Claude makes while viewing each raw figure (Read tool), one JSON entry per
file. Two questions, in order:

1. **Orientation** — does the figure BODY read sideways (printed landscape on a portrait
   sheet)? If yes, decide the clockwise rotation (90 / 180 / 270) that brings it upright.
2. **Header** — is there a USPTO/WO patent-page metadata band? If yes, at what fraction of
   the (post-rotation) image does it end?

These are the only vision-dependent steps. The figure-body bbox is then found by
pixel-density `tight_crop` and the margin by a fixed ratio (deterministic — see
`pixel-crop-spec.md`).

## What counts as a header

The metadata band at the edge of a raw patent application/grant PDF page. Any one pattern is
sufficient:

- "Patent Application Publication" (USPTO published apps)
- "U.S. Patent" (USPTO granted patents)
- "Sheet N of M" / "Sheet N"
- "US YYYY/XXXXXXXX A1" or a similar publication-number string
- A date in publication format ("Nov. 7, 2024", "May 26, 2026")
- WO/EP equivalents ("WO 2026/...", "EP X XXX XXX")

The header is typically a single horizontal band at the very top, separated from the figure
body by a thin white gap.

## What does NOT count as a header

- Figure captions ("FIG. 1", "Figure 1") — part of the figure body; ALWAYS preserved.
- Reference numerals inside the figure ("172 CMD Load").
- Page numbers within the drawing (a "200" near a flowchart).
- Section dividers inside the figure body.

## Rotation decision

- The rotation target is the FIGURE BODY reading upright (captions horizontal, flow-chart
  text readable left-to-right). The sheet's own orientation does not matter.
- USPTO landscape sheets usually print the metadata band rotated 90° along the RIGHT margin
  (thin vertical band of small rotated text in the right ~5-10% of width). Two valid
  treatments:
  - body already upright, only the side band present → no rotate; `{"right": 0.10}`.
  - body itself sideways → `"rotate": 90` or `270` (whichever brings the body upright;
    check which way the caption text tips), then express trims in the POST-rotation frame
    (the side band will have become a top or bottom band).
- `180` is for upside-down scans only (rare).
- When in doubt, do not rotate — native orientation is the default (the source pipeline
  never rotated at all; rotation exists here for the sideways-body case only).

## How to derive the trim fraction

Identify where the header band ends, in normalized 0-1 (top-left origin, post-rotation
frame). Be **generous** — include a ~1-2% buffer past the header text so `tight_crop` does
not catch trailing pixels. Example: band spans 0.03-0.07 → return `0.10`.

## Output format — `trim-decisions.json`

Map each input filename to one of:

- `null` — pre-cleaned, nothing to do
- `<float 0-1>` — shorthand for top-only trim
- `{"rotate": 90|180|270, "top": x, "right": y, "bottom": z, "left": w}` — any subset;
  `rotate` is clockwise and applied FIRST; trim fractions refer to the rotated image

```json
{
  "fig-01.png": null,
  "fig-02.png": 0.12,
  "fig-08.png": {"right": 0.10},
  "fig-09.png": {"rotate": 90, "top": 0.08},
  "fig-10.png": {"top": 0.06, "bottom": 0.04}
}
```

## Footer (bottom edge)

WIPO/PCT sheets sometimes carry "SUBSTITUTE SHEET (RULE 26)" or a page number at the bottom
→ `{"bottom": 0.05}`.

## Edge cases + conservatism

- **Header text mixed with the figure** (no clear separation): rare; best-judgment trim, or
  `null` and re-process with a manual trim after inspection.
- **Tiny band** (bare page number, <1% height): usually `null` — `tight_crop` absorbs it.
- Err toward **smaller trim**: `tight_crop` is robust to small stray ink; over-trimming can
  cut the figure body. A clearly pre-cleaned image is always `null`.
