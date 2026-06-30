# STM VL53L9CX dToF LiDAR — Article 1 "Mechanism" (formal pipeline run)

A general-audience, patent-as-protagonist storytelling article on STMicroelectronics'
ultra-lean time-of-flight histogram patent **US 2026/0140238 A1** ("Ultra-Lean Time-of-Flight
Histogram Processing"), produced through the full `patent-essay` pipeline (Phase 1 Design →
Phase 2 Compose → Phase 3 Edit loop → post-acceptance self-audit → archive).

This is the **English article version** of a piece first drafted in Korean. It is Part 1 of a
planned 3-part series on the VL53L9CX (Mechanism → Robustness → The Bridge). The series angle
(the patent is the protagonist; audience high-school to undergraduate) was preserved, not
reframed.

## Final deliverable

- `essay-final.md` — the clean, reader-facing article. ~1,382 words of body. Five-layer
  structure: problem → verbatim claim → mechanism by analogy → product connection → why it
  matters. Defines the series' callback vocabulary (histogram, zone/multizone, peak = distance).

## How it was produced (artifacts)

| Stage | Files |
|---|---|
| Phase 1 Design (`thesis-architect`, voice-off) | `handoff/01-design/`: invention-summary (+ `[dddd]` anchor allow-list, claim-scope note), thesis-spine, thesis-candidates, figure-selection (none this run), figure-rationale, fact-check-log, phase2-handoff-notes, search-log, figures-index (empty) |
| Phase 2 Compose (`essay-en-composer`, voice-on) | `handoff/02-compose/`: essay-draft, publication, thesis-trace, figures-rationale |
| Phase 3 Edit (`editorial-review`, voice-fenced) | `handoff/03-edit/`: edit-log (7-pass), essay-final, gate-result.json, score-history, revision-notes (self-audit) |
| Run evidence (top level) | `edit-log.md`, `score-history.md`, `gate-result.json`, `revision-notes.md`, `essay-context.md` |
| Figures | none — no cleaned figure assets were available; the mechanism is carried entirely in prose |

## Result

- Deterministic gates: all 11 PASS, 0 fail (warn-only LONGSENT, all tokenizer joiner artifacts
  or one ~45-word spec-list sentence). FIGREF/FIGUSE skipped, no figures this run.
- Editorial loop: revise-recommended on iteration 1 (two medium readability findings), **PASS on
  iteration 2** after a surgical revision (cap 4). See `score-history.md`.
- Post-acceptance self-audit (2 fresh-context adversarial reviewers): two verifiable grounding
  corrections applied (block-quote attribution; an on-chip anchor re-pointed to `[0043]`), logged
  in `revision-notes.md` and normalized to the ledger with `origin: self-post-accept`. Grounding
  hard-gate held throughout.

## The thesis in one line

The VL53L9CX recovers distance from photon statistics: a per-zone histogram streamed one bin at a
time, where the peak is the distance, and US 2026/0140238 is what makes that processing lean
enough to run on the sensor's own chip.

## Anchors quoted verbatim

- Hero, US 2026/0140238 A1 (Abstract): "processes time-of-flight measurement data using sequential
  bin-by-bin histogram processing".
- Support, US 2023/0296739 B2 ([0003]): "each bin of the histogram representing a photon count
  corresponding to a distance from a light-ranging system".

## Reproduce the validation

```
python .claude/skills/_shared/scripts/run_gates.py \
  --draft essays/stm-tof-us2026-0140238/essay-final.md \
  --invention-summary essays/stm-tof-us2026-0140238/handoff/01-design/invention-summary.md \
  --figures essays/stm-tof-us2026-0140238/handoff/01-design/figures-index.txt \
  --figure-selection essays/stm-tof-us2026-0140238/handoff/01-design/figure-selection.md
```

## Scope note

A technical-storytelling read for a general audience, not a legal opinion on claim validity or
scope. Product facts (2,268 zones, 54x42 degrees, 5 cm to 9 m, up to 100 fps, on-chip processing,
flood illumination) are ST's, attributed in the text and external to the patent. Datasheet-only
figures pending independent cross-check (940 nm, BSI stack, dual-VCSEL+BCD, ~150 mW, package size,
~1% accuracy) are deliberately not asserted.
