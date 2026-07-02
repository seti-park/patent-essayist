---
name: figure-prep
description: >
  Layer-1 patent-figure cleaner (Phase 0 of the patent-essay pipeline). Takes RAW patent
  drawings (PDF-page screenshots/exports in input/figures-raw/), decides per figure — by
  looking at it — whether to rotate the body upright and where the USPTO/WO header/footer
  band ends, then runs a deterministic pixel pipeline (edge trim → density tight-crop →
  uniform 10% margin) and writes cleaned, consistently named input/figures/fig-NN.png at
  300 DPI plus a figure-manifest. Use when a run provides raw figures, or when asked to
  clean/normalize patent drawings.
argument-hint: "[raw dir] [out dir]  (defaults: input/figures-raw → input/figures)"
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
---

# figure-prep — Layer-1 figure cleaning (Phase 0)

Turn raw patent drawings into the pipeline's input contract: `input/figures/fig-NN.png`,
header-free, body-tight, uniform margins, 300 DPI grayscale. Vision decides the semantics
(rotation, header band); `scripts/process_figures.py` does every pixel deterministically.

Ported from `seti-park/patent-essay-pipeline` `patent-figures-clean` v2.1, plus a rotation
step that repo deliberately lacked (its side-header cases were handled by cropping the band;
here a sideways-printed BODY may additionally be rotated upright).

## Inputs / outputs

- In: `input/figures-raw/*.{png,jpg,jpeg}` — one file per figure, **sub-figures pre-split
  by the user** (this skill does not split panels). Filenames must end in the figure number
  (+ optional panel letters) before the extension: `fig-01.png`, `Fig-3A.jpg`,
  `12636684-7.png`.
- Out: `input/figures/fig-NN.png` (zero-padded, letters uppercased),
  `input/figures/figure-manifest.md`, `input/figures/trim-decisions.json` (the audit trail),
  and — with `--index` — a `figures-index.txt` (one figure number per line, the gates' format).

## Steps

1. **Deps check**: `python3 -c "import PIL, numpy"` — if missing,
   `pip install pillow numpy` (no other dependencies; no OCR, no PDF tooling — inputs are
   already rasterized).
2. **List** the raw files; **view each with the Read tool** (batch several Reads per
   response). Screenshots of PDF pages are fine.
3. **Decide per figure** — rotation (only if the figure BODY reads sideways) and
   header/footer/side-band trim fractions — per `references/header-detection.md`. When
   uncertain: no rotation, `null` trim (the tight-crop absorbs small stray ink; over-trim
   risks the body).
4. **Write** `input/figures/trim-decisions.json` mapping each input filename to its spec.
5. **Run**:

   ```
   python .claude/skills/figure-prep/scripts/process_figures.py \
     input/figures-raw input/figures \
     --trim-decisions input/figures/trim-decisions.json \
     --index handoff/01-design/figures-index.txt   # when running inside a pipeline run
   ```

6. **Verify** — Read 2-3 outputs: header gone, "FIG. N" caption preserved, body intact,
   margins visually equal on all four sides; check `figure-manifest.md`'s Cropped/Pad
   columns for outliers (a near-zero pad or a wildly asymmetric crop means a wrong trim
   fraction — fix the JSON entry and re-run; re-runs overwrite). Rename any
   `unknown-NN.png` by hand.

## Pixel pipeline (deterministic — `references/pixel-crop-spec.md`)

rotate (cw, optional) → fractional edge trim → `tight_crop` (ink threshold 200, ≥2 ink px
per row/col, 1 px edge shave) → `pad` (margin = 10% of the longer side, all four sides) →
save grayscale PNG, 300 DPI, optimized. Alpha is flattened onto white at load (transparent
PNGs otherwise read as solid ink and skew the crop).

## Contract with the orchestrator

`patent-essay` runs this as **Phase 0** whenever `input/figures-raw/` has files and treats
`input/figures/` as its cleaned input afterwards. Standalone use (any raw dir → any out dir)
is also fine.
