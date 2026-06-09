# Patent Essay System (Claude Code / web)

A skill-based pipeline that turns an **English patent** (+ cleaned figures) into a finished
**English essay** for X Articles. Three phases — **Design → Compose → Edit** — pass data
through on-disk hand-off directories, and an orchestrator runs the Compose↔Edit quality loop
until the draft clears the deterministic gates and the editorial assessment. A final
**pre-publish verification gate** (`prepublish-verify`) then runs once — an independent red-team
+ live source-resolution by a fresh reviewer — before the essay is archived/published. After each
essay a second, slower **meta-loop** (`pipeline-retro`) proposes improvements to the system itself.

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
/patent-essay <patent path | text | number>  [--threshold pass|revise-recommended] [--max-iter 4] [--mode essay|wire] [--audience deep|investor] [--verify auto|off]
```

Inputs live under `input/`: `patent.md`, `figures/fig-NN.png` (pre-cleaned), and optional
`essay-context.md`. The orchestrator runs all three phases plus the loop, archives the run to
`runs/<essay-id>/`, runs the meta-loop, and returns the final essay
(`handoff/03-edit/essay-final.md`) plus a score history. Optional outer backstop:

```
/goal the patent-essay SCORE HISTORY shows a final draft that passes all gates with overall_assessment == pass
```

Individual phases can be run standalone: `/thesis-architect`, `/essay-en-composer`,
`/editorial-review`, `/prepublish-verify`, `/pipeline-retro` (`/voice-canon-lookup` is an
internal Phase-2 helper).

## Audience altitude (`--audience deep|investor`)

A first-class dimension threaded through every phase. **`deep` (default)** is the
patent-fidelity altitude (inline `[xxxx]` anchors + reference numbers, full mechanism
walkthrough, ~2000+ words) — fully backward-compatible. **`investor`** is the accessible
altitude for the investor/analyst reader: stake-first, mechanism compressed, body under a word
ceiling with **no inline anchors / reference numbers**, but it **keeps** scannable subheadings,
the `# Sources` block, and figures (plain captions). Audience shifts the P1 thesis frame
(investor favors a forward-capability / market hook + a `reader_stake`), the P2 compose mode,
the P3 reader profile, and activates the `gate_readability` gate (goal 3 enforced:
`READAB-001` length ceiling, `READAB-002` no body anchors). Grounding rigor is unchanged —
anchor↔claim traceability moves to `handoff/02-compose/thesis-trace.md` (verified by pass-3),
it just does not surface to the reader. See `_shared/references/scoring-rubric.md`.

## Architecture

```
.claude/skills/
  patent-essay/        orchestrator: P1→P2→P3 inner loop → prepublish-verify → pipeline-retro (entry point)
  thesis-architect/    P1 Design  — patent → thesis + 4-axis grounding + figure plan (voice-off)
  essay-en-composer/   P2 Compose — design hand-off → blueprint → draft → strip (voice-on)
  voice-canon-lookup/  P2 internal helper — voice-canon corpus (index.yaml + 33 entries)
  editorial-review/    P3 Edit    — 6-pass severity review (voice-fenced)
  prepublish-verify/   verify     — independent red-team + live source-resolution at the publish threshold
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
runs/    <essay-id>/  edit-log.md · gate-result.json · verification-log.md · score-history.md   (per-run archive)
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
- **Verify (voice-fenced + full patent):** `prepublish-verify` keeps the same voice fence as Edit
  (no voice-profile/caption-roles) but, unlike Edit, **loads the full patent** — it needs it to
  catch invented numbers and mechanism misstatements. Its voice judgment is limited to
  `anti-ai-writing` (raise-then-disavow / insinuation) + `deliverable-voice-rules`.

## Loop control (two tiers + a publish gate)

- **Inner loop (orchestrator, auto):** deterministic gates (hard pass/fail) + editorial
  **severity model** (`overall_assessment`: pass / revise-recommended / revise-required),
  threshold (default `pass`), grounding + goal-2 hard-gates, max iterations (default 4). On
  FAIL it feeds the edit findings back into Compose (revision mode) and re-scores.
- **Pre-publish verification gate (`prepublish-verify`, after the inner loop, `--verify auto`):**
  an **independent** reviewer (not the editor that just passed the draft) runs once at the
  publication threshold — a red-team close-read against the full patent + a **live** source
  re-resolution — reusing the same severity model. low → surgical fix / surface; medium+ → one
  more Compose↔Edit round then re-verify (+1 cap). This is where the authoritative live external
  check lives (moved off the per-round editorial Pass-3, which now only flags candidates).
- **Meta-loop (`pipeline-retro`, propose-only):** after each essay, normalizes findings into
  `meta/findings-ledger.jsonl`, attributes recurring root causes to the owning stage/artifact,
  and writes evidence-backed improvement proposals. It **never edits a skill** — a human
  applies proposals after `meta/regression.py` passes.
- **`/goal` (optional outer net):** auto-resume backstop if a run is interrupted.

## Deterministic gates

`_shared/scripts/run_gates.py` runs seven mechanical checks and returns pass/fail + `check_id`s:
`gate_emdash`, `gate_anchors` (`[dddd]` 4-digit format + chain + figure refs), `gate_sources`
(`# Sources` h1, 5-label enum, all-or-nothing subgrouping, **plus `SOURCES-005`: leaked
tool-call / harness XML tags are a hard fail**), `gate_banned` (anti-AI banned
list), `gate_structure` (warn-only heuristics), `gate_figure_use` (orphan selected figure —
goal 2), and `gate_readability` (accessible-altitude contract — goal 3, `--audience investor`
only; inert on `deep`). Run `python .claude/skills/_shared/scripts/test_gates.py` for the
suite, or `python meta/regression.py` for tests + fixtures.

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
