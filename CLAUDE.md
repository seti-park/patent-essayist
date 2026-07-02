# Patent Essay System (Claude Code / web)

A skill-based pipeline that turns an **English patent** (+ its drawings — raw PDF-page
exports are fine) into a finished **English essay** for X Articles. An optional **Phase 0**
(`figure-prep`) cleans raw drawings into the input contract (header cut → rotate if the body
reads sideways → tight-crop → uniform margins → `fig-NN.png`); three phases — **Design →
Compose → Edit** — then pass data through on-disk hand-off directories, and an orchestrator
runs the Compose↔Edit quality loop until the draft clears the deterministic gates and the
editorial assessment. After each essay a second, slower **meta-loop** (`pipeline-retro`)
proposes improvements to the system itself.

This is a conversion of a system originally run as separate claude.ai Projects. The real
skill bodies have been ported into `.claude/skills/`; the originals are preserved verbatim in
`docs/source-prompts/` as the reference baseline. The conversion adds: **automated stage
hand-off**, **real deterministic gate scripts aligned to the editorial rules**, an
**automatic inner quality loop**, and a **propose-only self-improvement meta-loop**.

## North-star goals (acceptance criteria)

Every gate and editorial pass exists to defend one of four goals. The full goal→check
traceability matrix is in `_shared/references/scoring-rubric.md`:

1. **Catch the patent's core accurately** — anchor chain, invention-summary, grounding.
2. **Use figures + specification sufficiently** — `gate_figure_use` (orphan figures) +
   editorial pass-3 coverage sub-check.
3. **Easy for the reader to understand** — structure gate + pass-5 reader perspective.
4. **Well-structured (4a) and natural (4b)** — sources/format + lead/conclusion; banned/em-dash
   + voice-on drafting.

## How to run

```
/patent-essay <patent path | text | number>  [--threshold pass|revise-recommended] [--max-iter 4] [--mode essay|wire]
```

Inputs live under `input/`: `patent.md`, figures (either pre-cleaned `figures/fig-NN.png`,
or RAW drawings in `figures-raw/` — Phase 0 `figure-prep` cleans, renames, and indexes them
automatically; needs `pip install pillow numpy`), and optional `essay-context.md`. The
orchestrator runs Phase 0 when raw figures are present, then all three phases plus the loop,
archives the run to `essays/<essay-id>/`, runs the meta-loop, and returns the final essay
(`handoff/03-edit/essay-final.md`) plus a score history. Optional outer backstop:

```
/goal the patent-essay SCORE HISTORY shows a final draft that passes all gates with overall_assessment == pass
```

Individual phases can be run standalone: `/figure-prep`, `/thesis-architect`, `/essay-en-composer`,
`/editorial-review`, `/pipeline-retro` (`/voice-canon-lookup` is an internal Phase-2 helper).

## Architecture

```
.claude/skills/
  patent-essay/        orchestrator: P0→P1→P2→P3 inner loop + per-essay pipeline-retro (entry point)
  figure-prep/         P0 Figure prep — raw drawings → header cut / rotate-if-sideways /
                       tight-crop / uniform 10% margin → input/figures/fig-NN.png + manifest
                       (vision decides per-figure trim+rotation; scripts/ do the pixels —
                       ported from patent-essay-pipeline patent-figures-clean v2.1)
  thesis-architect/    P1 Design  — patent → thesis + 4-axis grounding + figure plan (voice-off)
  essay-en-composer/   P2 Compose — design hand-off → blueprint → draft → strip (voice-on)
  voice-canon-lookup/  P2 internal helper — voice-canon corpus (index.yaml + 33 entries)
  editorial-review/    P3 Edit    — 7-pass severity review (voice-fenced; pass-7 adversarial reader)
  pipeline-retro/      meta-loop  — findings → ledger → propose-only improvement proposals
  _shared/
    references/        shared canon: deliverable-voice-rules · anti-ai-writing (vendored absorbed) ·
                       caption-roles · working-dialogue-voice · scoring-rubric (severity + matrix)
                       (each ported skill also carries its own references/: voice-profile +
                        voice-canon live under voice-canon-lookup/; x-articles-format-en,
                        section-blueprint, mode-spec, etc. under essay-en-composer/)
    scripts/           11 deterministic gate scripts (Python stdlib) + banned_terms.txt + tests
    vendor/            blader/humanizer + harshaneel/ai-check — REFERENCE ONLY, absorbed into
                       anti-ai-writing.md, NOT run in the loop — see vendor/README.md
handoff/          01-design 02-compose 03-edit       runtime stage artifacts (gitignored)
handoff-template/ 01-design 02-compose 03-edit       full-schema templates the skills reference
runs/    <essay-id>/  edit-log.md · gate-result.json · score-history.md   (per-run archive)
meta/
  findings-ledger.jsonl      append-only normalized findings (keyed by goal + owner artifact)
  attribution-table.md       finding-class → goal + owner stage/artifact + lever (retro's brain)
  improvement-proposals/     propose-only proposals (evidence + exact diff); applied by a human
  fixtures/ + regression.py  regression guard run before any proposal is applied
input/    patent.md · figures-raw/ (raw drops) · figures/ (cleaned) · essay-context.md
docs/source-prompts/  original claude.ai skills (5: 01-design 02-compose 03-edit 04-promote)
```

Data flows by **output contracts**: each phase's `SKILL.md` defines the exact files it writes
to its `handoff/<phase>/` directory, and the next phase reads them — no chat copy-paste. The
`handoff-template/` tree holds the full-schema templates the skills point at.

## Voice fencing (by which references each phase loads)

The original system enforced this by physically separate Projects; here it is enforced by
which references each phase loads:

- **Design (voice-off):** thesis-architect's own references only (invention-summary-schema,
  4-axis-grounding, hook-patterns, …) — no deliverable-voice canon.
- **Compose (voice-on):** full voice stack — `voice-canon-lookup` (voice-profile + 33-entry
  canon), `deliverable-voice-rules`, `anti-ai-writing`, the composer's `x-articles-format-en`,
  `caption-roles`.
- **Edit (voice-fenced):** `deliverable-voice-rules` + `anti-ai-writing` only — **not**
  voice-profile or caption-roles, to prevent editor voice drift. The meta-loop preserves this
  fence: a Phase-3 voice finding routes to anti-ai/deliverable-voice or a Phase-2 voice-canon
  admission, never back to voice-profile.

## Loop control (three tiers)

- **Inner loop (orchestrator, auto):** deterministic gates (hard pass/fail) + editorial
  **severity model** (`overall_assessment`: pass / revise-recommended / revise-required),
  threshold (default `pass`), grounding + goal-2 hard-gates, max iterations (default 4). On
  FAIL it feeds the edit findings back into Compose (revision mode) and re-scores.
- **Self-audit (orchestrator, auto, post-acceptance):** after the inner loop passes, ≥2
  fresh-context adversarial reviewers (the `pass-7-adversarial-reader` checklist + grounding
  spot-checks, separate forked contexts, multi-vote) catch the blind-spots a `pass` survives.
  Applied autonomously and logged via the revision-delta channel as `origin: self-post-accept`;
  loops until dry. It can only ADD findings, never relax the bar. Acceptance set in
  `_shared/references/scoring-rubric.md` (Layer 3), enforceable as a `/goal`.
- **Meta-loop (`pipeline-retro`, propose-only):** after each essay, normalizes findings into
  `meta/findings-ledger.jsonl`, attributes recurring root causes to the owning stage/artifact,
  and writes evidence-backed improvement proposals. It **never edits a skill** — a human
  applies proposals after `meta/regression.py` passes. It also normalizes the **revision-delta
  channel** — `handoff/03-edit/revision-notes.md` (post-acceptance human edits) via
  `meta/normalize_revision_notes.py`, tagged `origin: human-post-accept` — so the editorial
  blind-spots a human catches AFTER the loop says pass feed the ledger too (the half the
  gates/passes don't yet score, and the engine that keeps the self-check criteria growing).
- **`/goal` (optional outer net):** auto-resume backstop if a run is interrupted.

## Deterministic gates

`_shared/scripts/run_gates.py` runs eleven mechanical checks and returns pass/fail + `check_id`s:
`gate_emdash`, `gate_anchors` (`[dddd]` 4-digit format + chain + figure refs), `gate_sources`
(`# Sources` h1, 5-label enum, all-or-nothing subgrouping), `gate_banned` (anti-AI banned
list), `gate_structure` (warn-only heuristics), `gate_figure_use` (orphan selected figure —
goal 2), plus four **run-045 self-check gates** — `gate_meta` (reader-instruction /
essay-self-reference posturing; hard-fail), `gate_stub` (stub section vs siblings), `gate_cashtag`
(bare ticker → `$`cashtag), `gate_dupe` (gross verbatim repetition; warn) — the mechanical half
of the editorial blind-spots a human used to catch by hand in post-acceptance revision (see
`meta/improvement-proposals/2026-06-26-human-revision-blindspots.md`; judgment complement =
editorial **pass-7** adversarial reader). A further gate, `gate_typography`, adds the GOV.UK-base
hygiene layer — Latin abbreviations and exclamation marks hard-fail; emoji, all-caps runs,
non-descriptive link text, and run-on sentences warn — the mechanical subset of the govuk-derived
`deliverable-voice-rules`. Run `python .claude/skills/_shared/scripts/test_gates.py`
for the suite, or `python meta/regression.py` for tests + fixtures.

## Customization

- **Tune behavior** in `_shared/references/` (scoring-rubric threshold + matrix,
  anti-ai-writing, deliverable-voice-rules) and each skill's own `references/`. The banned-term
  list is mirrored to `_shared/scripts/banned_terms.txt` for mechanical enforcement. The
composition/hygiene canon (`deliverable-voice-rules` + `anti-ai-writing`) is based on the
**govuk-style** plain-English standard, adapted with patent-domain exceptions: claim language,
terms of art, part numbers, and verbatim quotes keep their exact wording (reading-level and
plain-word swaps apply only to the connective prose).
- **Grow the canon** via the meta-loop: `pipeline-retro` proposes reference edits, gate
  promotions, voice-canon admissions, and rubric tuning — applied by a human after regression.
- **Reference the originals:** `docs/source-prompts/<phase>/<skill>/` holds the verbatim
  claude.ai skills (incl. Phase-4 `promo-composer`, out of scope for this conversion but
  preserved for a future port). Keep each phase's **output contract** intact when porting.
- **Vendored AI-tell skills** under `_shared/vendor/` are reference-only (absorbed into
  `anti-ai-writing.md`); they are not run in the loop.

## Note

The legacy static HTML files (`index.html`, `1.html`–`3.html`) are unrelated leftovers and
are not part of this system.
