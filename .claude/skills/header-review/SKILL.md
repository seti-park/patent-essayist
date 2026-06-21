---
name: header-review
description: "End-of-pipeline design-system review on a generated essay header. Five passes (format ratio, bright/soft tone, title legibility, content coherence, no-bypass routing) over a 5:2 header PNG plus the essay title + thesis. Structured YAML feedback — NOT auto-fix. Passes 1 and 5 delegate to gate_header's deterministic checks; passes 2-4 are visual/editorial judgment. Use when a header.png lands at the end of a patent-essay run. NOT for: drawing or fixing the header (route through tools/headerkit/), text-essay review (Phase 3 editorial-review), token authoring (tools/headerkit/tokens.py)."
---

# header-review

The HeaderKit design system's end-of-pipeline review. Five passes. Structured feedback YAML output. The visual sibling of `editorial-review`: same shape, same severity model, same NOT-auto-fix posture — but it reviews the **header image**, not the essay prose.

```
runs/<essay-id>/header.png            (the generated 5:2 header)
    + the essay title + one-line thesis (what the header must imply)
    + handoff/02-compose/publication.md  (title/thesis source, if present)
    + tools/headerkit/CONTRACT.md         (the frozen spec being reviewed against)
    + deterministic checks: _shared/scripts/gate_header.py
    → 5 passes
    → runs/<essay-id>/header-review.md (structured YAML feedback)
    → human revises (re-runs build_header) → final header.png
```

## Output role

2nd redundancy on the deliverable header. The composer (`tools/headerkit/header.py`) is the 1st instance — it asserts 5:2 and routes every primitive through the library. This skill is the qualitative check the composer cannot make: *does the picture actually read as bright, legible, and about the essay?* A `build_header` call can produce a perfectly 5:2, perfectly token-compliant header that still fails to imply the thesis. That gap is what this review exists to catch.

- Findings supply input for the human's revise decision. NOT auto-fix.
- This skill never draws or edits a header. Revision means re-running `build_header` with a different illustration spec / title / theme.
- Conflict resolution: a human visual judgment overrides skill output.

## Two-layer model (mirrors the scoring rubric)

Like the essay loop, header review is two layers:

1. **Deterministic gate** (mechanical, hard pass/fail) — `_shared/scripts/gate_header.py`. Passes 1 and 5 of this skill *delegate* to it. If `gate_header` emits any `fail`-severity finding (`HEADER-RATIO-001`, `HEADER-BYPASS-001`, `HEADER-TOKENS-001/002`), the corresponding pass is automatically `revise-required` — no visual judgment can override a mechanical fail.
2. **Qualitative design assessment** — passes 2-4 (tone, legibility, coherence), expressed as a `severity` per finding and rolled into one `overall_assessment`.

## When to invoke

After the integrator's `header.py` composes `runs/<essay-id>/header.png` at the end of a patent-essay run, with the essay's final title + thesis in hand. Mandatory on every shipped header. No skip option — a header is the first thing a reader sees, so a header that misreads the essay is a publication-grade defect.

## Five passes (locked order)

1. **Format** — file present, 5:2 ratio, high-resolution master (default 6000x2400, scalable). **Delegates to `gate_header_ratio`** (`HEADER-RATIO-001`). A non-5:2 or unopenable PNG is `revise-required`. See `references/format-and-bypass.md`.
2. **Bright/soft tone** — the palette stays in the bright/soft band: every `bg_*`/`accent*` token brightness >= 150 and `ink` is the only dark token (the `is_soft(theme)` definition, CONTRACT.md section 1). Visually: airy, no hard black, no harsh edges, no photoreal. Read the rendered image for harsh contrast the token check can't see (e.g. an illustration form that landed too dark). See `references/tone-and-legibility.md`.
3. **Legibility** — the title (theme `ink`) reads cleanly over the scrim panel and illustration. Sufficient ink-vs-background contrast in the text column; title not colliding with a busy illustration region; autosize didn't clamp the title into an unreadable wall. See `references/tone-and-legibility.md`.
4. **Content coherence** — *does illustration + title together imply the thesis?* The north-star: "implicating the contents of the essay when combined with the title." Check that the illustration's conceptual glyphs/forms are abstracted from the essay's actual concepts (not generic decoration), and that title + image point at the same idea rather than two different ones. See `references/content-coherence.md`.
5. **No-bypass** — the header was composed through HeaderKit, not hand-drawn. **Delegates to `gate_header_bypass`** + `gate_header_tokens` (`HEADER-BYPASS-001`, `HEADER-TOKENS-001/002`). Any out-of-library primitive or stray hex is `revise-required`. See `references/format-and-bypass.md`.

Tone (pass 2) and legibility (pass 3) are a recurring cross-pass pair: a too-dark illustration form threatens both the soft band and title contrast. See `references/tone-and-legibility.md`.

## Severity model

Per-finding `severity`: `critical | high | medium | low`. One `overall_assessment` from `pass | revise-recommended | revise-required`, computed from the worst finding present (identical table to `_shared/references/scoring-rubric.md` and `editorial-review`):

| Has critical? | Has high? | Has medium? | `overall_assessment` |
|---|---|---|---|
| Yes | (any) | (any) | `revise-required` |
| No | Yes | (any) | `revise-required` |
| No | No | Yes | `revise-recommended` |
| No | No | No | `pass` |

`low` findings never change the assessment. **Hard-gate override:** any `gate_header` fail (pass 1 or pass 5) forces `revise-required` regardless of the visual findings — a mechanical defect in the deliverable is non-negotiable, exactly as `gate_anchors`/`gate_emdash` fails are for the essay. See `references/feedback-format.md` for the full severity criteria and schema.

## Output format

Structured YAML feedback. See `references/feedback-format.md` for the full schema.

Minimal example:

```yaml
review_id: <essay-id>-header-review-1
header_source: runs/<essay-id>/header.png
title_reviewed: "<essay title>"
thesis_reviewed: "<one-line thesis>"
overall_assessment: revise-recommended

findings:
  - pass: content-coherence
    location: illustration left-of-center glyph
    severity: medium
    finding: |
      The illustration reads as a generic gradient field; no glyph abstracts the
      essay's core concept (a latency-reducing sensor-fusion path). Title carries
      all the meaning; image is decoration, not implication.
    recommendation: |
      Re-run build_header with keywords that anchor the illustration to the
      mechanism (e.g. ["sensor", "fusion", "latency", "path"]).

  - pass: format
    finding: "no findings"
    scoped_to: "gate_header_ratio: 6000x2400, ratio 2.5 exact"
```

Feedback gets written to `runs/<essay-id>/header-review.md`. A human applies findings by re-running `build_header`.

## Pre/post conditions

Pre:
- `runs/<essay-id>/header.png` present (the composed header).
- Essay title + one-line thesis available (from `handoff/02-compose/publication.md` or supplied directly).
- `gate_header.py` runnable from `_shared/scripts/`.
- `tools/headerkit/CONTRACT.md` + `tokens.py` accessible (for the `is_soft` band + canonical size).

Post:
- `runs/<essay-id>/header-review.md` emitted with one entry per finding, every pass represented (empty passes annotated `"no findings"`).
- Each finding has a specific location (image region or pass) + severity + recommendation.
- `overall_assessment` set per the severity table, with the hard-gate override applied.
- Auto-fix NOT performed (a human decides what to re-render).

## Coupling

- ← `tools/headerkit/header.py` (`runs/<id>/header.png` input)
- ← `_shared/scripts/gate_header.py` (passes 1 + 5 delegate to it)
- ← `handoff/02-compose/publication.md` (title + thesis being implied)
- → human (returns feedback to re-run `build_header` → final header)

## Out of scope

- Drawing or fixing the header (route through `tools/headerkit/`; this is review only).
- Authoring tokens or themes (`tools/headerkit/tokens.py`, Agent A).
- Text-essay review (Phase 3 `editorial-review`).
- Illustration-engine internals (`tools/headerkit/illustration.py`, Agent B) — review judges the *output*, not the algorithm.

## References

- `references/format-and-bypass.md` — passes 1 + 5; how they delegate to `gate_header` and map its `check_id`s to severities.
- `references/tone-and-legibility.md` — passes 2 + 3; the `is_soft` bright/soft band, contrast heuristics, title-over-scrim legibility, the tone↔legibility cross-pass.
- `references/content-coherence.md` — pass 4; the implication test (illustration + title ⇒ thesis), decoration-vs-implication calls.
- `references/feedback-format.md` — output YAML schema + severity criteria + overall-assessment rules + hard-gate override.
