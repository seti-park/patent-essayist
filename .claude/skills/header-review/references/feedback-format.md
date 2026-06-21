# Feedback format

Referenced by header-review SKILL.md. Defines the structured feedback YAML
output. Deliberately parallel to `editorial-review/references/feedback-format.md`
and `_shared/references/scoring-rubric.md` so the header review and the essay
review speak the same severity language.

## Schema

```yaml
review_id: <essay-id>-header-review-<n>
header_source: runs/<essay-id>/header.png
title_reviewed: "<essay title shown on the header>"
thesis_reviewed: "<one-line thesis the header must imply>"
theme_reviewed: aurora
review_timestamp: <ISO-8601>
overall_assessment: pass | revise-recommended | revise-required

findings:
  - pass: <pass-name>
    location: <image region or pass scope>
    severity: critical | high | medium | low
    finding: "<what was observed>"
    recommendation: "<what to re-render>"
    gate_check_id: <optional: HEADER-RATIO-001 / HEADER-BYPASS-001 / ... for delegated passes>
```

## Pass names

- `format`            (pass 1 — delegates to gate_header_ratio)
- `bright-soft-tone`  (pass 2)
- `legibility`        (pass 3)
- `content-coherence` (pass 4)
- `no-bypass`         (pass 5 — delegates to gate_header_bypass + gate_header_tokens)

## Required fields per finding

- `pass` (which pass detected it)
- `location` (image region, e.g. "title block", "illustration center glyph", or the pass scope for delegated passes)
- `severity` (critical / high / medium / low)
- `finding` (specific observation)
- `recommendation` (what to re-render — must be actionable through `build_header`)

## Optional fields

- `gate_check_id`: for delegated passes (1, 5), the originating `gate_header` `check_id`.
- `quote`: the title text, when a finding concerns title/legibility.

## Severity criteria

### critical (publication-blocking, reserved)

- Header file missing or corrupt where a deliverable is required.
- Title illegible to the point the essay cannot be identified from its cover.

### high (publication-blocking)

- Any `gate_header` fail: non-5:2 ratio, bypass primitive, stray hex / missing
  token import (delegated passes 1 + 5 — always high, see hard-gate override).
- Theme out of the bright/soft band (`is_soft()` False), or a dark illustration
  mass dominating the frame (pass 2).
- Title contrast insufficient over its column, or title clipped/truncated (pass 3).
- Title and illustration imply two different essays, or the image misreads the
  thesis (pass 4).

### medium (quality concern)

- Localized dark form / harsh edge / photoreal patch in the illustration (pass 2).
- Glyph crowding the text column; title clamped to floor into a dense wall (pass 3).
- Illustration is generic decoration with no concept glyph; glyph weakly tied to
  a keyword (pass 4).
- 5:2 but well below the canonical 3000x1200 raster (pass 1).

### low (polish)

- Faint meta/series line; minor airiness nit (pass 2/3).
- Glyph mildly redundant with the title (pass 4).

## Overall assessment rules

| Has critical? | Has high? | Has medium? | Assessment |
|---|---|---|---|
| Yes | (any) | (any) | revise-required |
| No | Yes | (any) | revise-required |
| No | No | Yes | revise-recommended |
| No | No | No | pass |

Low findings do not affect the assessment.

### Hard-gate override

Any `gate_header` fail on pass 1 (`HEADER-RATIO-001`) or pass 5
(`HEADER-BYPASS-001`, `HEADER-TOKENS-001/002`) forces `overall_assessment:
revise-required`, regardless of the visual findings. A mechanical defect in the
deliverable is non-negotiable — this mirrors how a `gate_anchors`/`gate_emdash`
fail is an automatic FAIL for the essay loop in `scoring-rubric.md`.

## Empty pass handling

If a pass produces no findings, emit it anyway with an explicit `"no findings"`
and a `scoped_to` describing what was reviewed (proves the pass ran). For the
delegated passes, put the gate confirmation in `scoped_to`:

```yaml
- pass: format
  finding: "no findings"
  scoped_to: "gate_header_ratio PASS — runs/044/header.png is 3000x1200, ratio 2.5"

- pass: bright-soft-tone
  finding: "no findings"
  scoped_to: "is_soft(aurora) True; rendered field reads light, no dark masses"
```

Empty-pass output without an explicit `"no findings"` annotation is invalid.

## Example output

```yaml
review_id: 044-tesla-rcm-header-review-1
header_source: runs/044-tesla-rcm/header.png
title_reviewed: "How Tesla Vision Vindicated the Rotational Crash Model"
thesis_reviewed: "Vision-fusion cuts airbag-deploy latency below the accelerometer baseline"
theme_reviewed: aurora
review_timestamp: 2026-06-21T12:00:00Z
overall_assessment: revise-recommended

findings:
  - pass: format
    finding: "no findings"
    scoped_to: "gate_header_ratio PASS — 3000x1200, ratio 2.5"

  - pass: bright-soft-tone
    location: illustration right third
    severity: low
    finding: |
      Soft accent forms sit in band; one coral form is slightly heavier than its
      neighbors but stays above the brightness floor.
    recommendation: |
      Optional. Drop that form's opacity a notch for a more even airy field.

  - pass: legibility
    finding: "no findings"
    scoped_to: "ink (#2E3A46) over scrim panel reads cleanly; title wrapped to 2 lines at ~150px"

  - pass: content-coherence
    location: illustration center glyph
    severity: medium
    finding: |
      Illustration shows a generic gradient field with soft blobs; no glyph
      abstracts the sensor-fusion / latency concept. Title carries the meaning;
      the image is decoration, not implication.
    recommendation: |
      Re-run build_header with keywords anchored to the mechanism, e.g.
      keywords=["vision", "fusion", "timeline", "airbag", "milliseconds"].

  - pass: no-bypass
    finding: "no findings"
    scoped_to: "gate_header_bypass + gate_header_tokens PASS — routed through headerkit, no stray hex"
```

## Notes

- Severity is the most consequential field. Review carefully.
- Recommendations must be re-render-able through `build_header` — this skill does
  not draw or edit headers.
- Every pass must appear in output, even empty ones (failure-mode mitigation
  against review inertia, same rule as editorial-review).
- Auto-fix is NOT this skill's responsibility. The caller decides what to
  re-render.
