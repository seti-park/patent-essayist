# A Depth Sensor That Cannot Time a Single Photon With a Stopwatch — US 2026/0140238 A1 (formal pipeline run)

Article 1 of 3 ("Mechanism") in the STM VL53L9CX patent-analysis series. Hero patent:
US 2026/0140238 A1, "Ultra-Lean Time-of-Flight Histogram Processing" (STMicroelectronics).
Full three-phase pipeline run (Design → Compose → Edit) plus post-acceptance self-audit and
the `pipeline-retro` meta-loop.

## Final deliverable

- `essay-final.md` — the accepted essay (identical to `essay-final-selfaudit.md`: the
  post-acceptance self-audit ran one round and applied zero edits — see Result below).
- `figures/fig-01.png` … `fig-07.png` — the patent's own figures; the essay uses FIG. 1 and
  FIG. 2 only (see Scope note).

## How it was produced (artifacts)

| Stage | Files |
|---|---|
| Phase 1 Design (`thesis-architect`) | `handoff/01-design/`: invention-summary, thesis-candidates, thesis-spine, figure-selection, figure-rationale, fact-check-log, search-log, phase2-handoff-notes, figures-index.txt |
| Phase 2 Compose (`essay-en-composer`) | `handoff/02-compose/`: essay-draft (final, draft_version 3), figures-rationale, thesis-trace, publication |
| Phase 3 Edit (`editorial-review`) | `handoff/03-edit/`: edit-log (round 3, final `pass`), edit-log-round1 / edit-log-round2 (superseded rounds, kept for the audit trail), essay-final, revision-notes (self-audit) |
| Run evidence (top level) | `edit-log.md`, `gate-result.json`, `score-history.md`, `revision-notes.md` |
| Series framing | `essay-context.md` — the English framing brief synthesized from the series' Korean storytelling briefs |

## Result

- **Deterministic gates: pass, with one adjudicated gate-script false positive.** All 10 gates
  clean every round except `figure_use`, which fired `FIGUSE-001` on figures 3-7 in every
  round. Verified against `gate_figure_use.py`'s source: the gate regex-scans the *entire*
  `figure-selection.md` file for figure mentions, including its "Not selected (and why)"
  section, which legitimately discusses FIG. 3-7 by number to explain their exclusion. The
  actual `## Selected figures` table lists only FIG. 1 and FIG. 2, and both are referenced in
  the essay — no real orphan. See `score-history.md` for the full writeup; this is now filed as
  a `recommended-apply` proposal in `meta/improvement-proposals/2026-06-24-figuse-selection-scope.md`
  (a second, real-world occurrence of a previously-`watch`-status class).
- **Editorial loop: 3 rounds, terminated at `pass`.** Round 1 `revise-recommended` (4 medium, 3
  low — H1/H2 header echo, paragraph density in §3-§4, missing zone=cell definition, missing
  `[0004]` anchor). Round 2 `revise-recommended` (1 medium remaining — one fused 149-word §5
  paragraph). Round 3 `pass` (0 high/critical/medium; 1 low, a logged Phase-1 backfill gap).
- **Post-acceptance self-audit: 1 round, dry.** Two independent fresh-context reviewers (no
  exposure to the design/compose process) ran the pass-7 adversarial checklist plus grounding
  spot-checks. No finding cleared the multi-vote bar. Notably, one reviewer raised a
  high-severity claim-scope objection (that "Claim 1... never holds that full copy" conflicts
  with dependent claim 8's "full histogram processing capabilities") that did **not** survive
  the orchestrator's own independent verification against the patent text — claim 8's phrase is
  used throughout the spec (e.g. `[0044]`) as the functional outcome the memory-lean bin-serial
  method *achieves*, not a competing memory model. See `revision-notes.md` for the full
  reasoning trail.

## The thesis in one line

STMicroelectronics' bin-serial histogram-processing circuit resolves a doubled impossibility —
you cannot time one photon with a stopwatch, and you cannot hold thousands of full photon-count
histograms in memory per frame — by streaming every histogram through dedicated hardware one
bin at a time, which is what a chip like the VL53L9CX needs to exist at 2,268 zones.

## Reproduce the validation

```
python .claude/skills/_shared/scripts/run_gates.py \
  --draft essays/001-st-histogram-mechanism/handoff/02-compose/essay-draft.md \
  --invention-summary essays/001-st-histogram-mechanism/handoff/01-design/invention-summary.md \
  --figures essays/001-st-histogram-mechanism/handoff/01-design/figures-index.txt \
  --figure-selection essays/001-st-histogram-mechanism/handoff/01-design/figure-selection.md \
  --mode essay --json
```

Expect the same adjudicated `figure_use` false positive described above (fails on FIG. 3-7);
every other gate should return clean.

## Scope note

- This is Article 1 of a planned 3-part series; Articles 2 (hero US 2024/0192337) and 3 (hero
  US 2023/0356397) are out of scope for this run. This essay owns the series' shared vocabulary
  (histogram / zone / peak=distance) for later articles to call back to without redefinition.
- The auxiliary patent (US 2023/0296739) and five cluster patents named in `essay-context.md`
  had no full text available this run — only one pre-cleared verbatim anchor exists for the
  auxiliary patent, and it is the only fact attributed to it anywhere in the essay.
- Some VL53L9CX product specs (940nm wavelength, BSI-stacked SPAD structure, VCSEL count,
  ~150mW power, package dimensions, ~1% accuracy) were corroborated only via search-snippet
  cross-checks during Phase 1's web research, not a direct fetch of ST's datasheet (ST's
  primary datasheet domain blocks automated access) — see `handoff/01-design/fact-check-log.md`
  for the full tiering. None of these hedged specs are load-bearing in the final essay text.
