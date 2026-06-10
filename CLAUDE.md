# Patent Essay System (Claude Code / web)

A skill-based pipeline that turns an **English patent** (+ cleaned figures) into a finished
**English essay** for X Articles. Three phases — **Design → Compose → Edit** — pass data
through on-disk hand-off directories, and an orchestrator runs the Compose↔Edit quality loop
until the draft clears the deterministic gates and the editorial assessment. After each essay
a second, slower **meta-loop** (`pipeline-retro`) proposes improvements to the system itself.

This is a conversion of a system originally run as separate claude.ai Projects. The real
skill bodies have been ported into `.claude/skills/` and adapted to this runtime (claude.ai
Project-era assumptions replaced with repo paths; loop-round behavior defined in
`essay-en-composer/references/revision-mode.md`); the originals are preserved verbatim in
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
/patent-essay <patent path | text | number>  [--threshold pass|revise-recommended] [--max-iter 4]
```

The standard input is **one zip archive** (chat upload or under `input/`) holding the
specification md + a `figures/` directory of drawings; the orchestrator extracts it to
`input/patent.md` + `input/figures/fig-NN.<ext>` before Phase 1. The decomposed form
(`patent.md`, `figures/fig-NN.png`, optional `essay-context.md` under `input/`) is
accepted as-is. The orchestrator runs all three phases plus the loop, archives the run to
`runs/<essay-id>/` (committed — the archive is the meta-loop's evidence chain), runs the
meta-loop, and returns the final essay
(`handoff/03-edit/essay-final.md`) plus a score history, then renders the 5:2 X-Article
header (`header-composer`, Phase 4-lite) to `handoff/04-promote/header.png`. Optional
outer backstop:

```
/goal the patent-essay SCORE HISTORY shows a final draft that passes all gates with overall_assessment == pass
```

Individual phases can be run standalone: `/thesis-architect`, `/essay-en-composer`,
`/editorial-review`, `/pipeline-retro` (`/voice-canon-lookup` is an internal Phase-2 helper).

## Architecture

```
.claude/skills/
  patent-essay/        orchestrator: P1→P2→P3 inner loop + per-essay pipeline-retro (entry point)
  thesis-architect/    P1 Design  — patent → thesis + 4-axis grounding + figure plan (voice-off)
  essay-en-composer/   P2 Compose — design hand-off → blueprint → draft → strip (voice-on)
  voice-canon-lookup/  P2 internal helper — voice-canon corpus (index.yaml + 33 entries)
  editorial-review/    P3 Edit    — 6-pass severity review (voice-fenced)
  header-composer/     P4-lite Promote — essay → header-spec.json → deterministic 5:2 header
                       (scripts/make_header.py + vendored OFL fonts + design-system.md;
                        the repo's only non-stdlib dep, Pillow, lives here — never in gates)
  pipeline-retro/      meta-loop  — findings → ledger → propose-only improvement proposals
  _shared/
    references/        shared canon: deliverable-voice-rules · anti-ai-writing (vendored absorbed) ·
                       caption-roles · working-dialogue-voice · scoring-rubric (severity + matrix)
                       (each ported skill also carries its own references/: voice-profile +
                        voice-canon live under voice-canon-lookup/; x-articles-format-en,
                        section-blueprint, mode-spec, etc. under essay-en-composer/)
    scripts/           6 deterministic gate scripts (Python stdlib) + banned_terms.txt + tests
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
input/    patent.md · figures/ · essay-context.md
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

## Loop control (two tiers)

- **Inner loop (orchestrator, auto):** deterministic gates (hard pass/fail) + editorial
  **severity model** (`overall_assessment`: pass / revise-recommended / revise-required),
  threshold (default `pass`), grounding + goal-2 hard-gates, max iterations (default 4). On
  FAIL it feeds the edit findings back into Compose (revision mode) and re-scores.
- **Meta-loop (`pipeline-retro`, propose-only):** after each essay, normalizes findings into
  `meta/findings-ledger.jsonl`, attributes recurring root causes to the owning stage/artifact,
  and writes evidence-backed improvement proposals. It **never edits a skill** — a human
  applies proposals after `meta/regression.py` passes.
- **`/goal` (optional outer net):** auto-resume backstop if a run is interrupted.

## Deterministic gates

`_shared/scripts/run_gates.py` runs six mechanical checks and returns pass/fail + `check_id`s:
`gate_emdash`, `gate_anchors` (`[dddd]` 4-digit format + chain + figure refs), `gate_sources`
(`# Sources` h1, 5-label enum, all-or-nothing subgrouping), `gate_banned` (anti-AI banned
list), `gate_structure` (warn-only heuristics), `gate_figure_use` (orphan selected figure —
goal 2). Run `python .claude/skills/_shared/scripts/test_gates.py` for the suite, or
`python meta/regression.py` for tests + fixtures.

## Customization

- **Tune behavior** in `_shared/references/` (scoring-rubric threshold + matrix,
  anti-ai-writing, deliverable-voice-rules) and each skill's own `references/`. The banned-term
  list is mirrored to `_shared/scripts/banned_terms.txt` for mechanical enforcement.
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
