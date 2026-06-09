---
name: patent-essay
description: >
  Orchestrator / entry point for the patent-essay system. Given an English patent (+
  cleaned figures), runs Phase 1 Design → Phase 2 Compose → Phase 3 Edit, automating the
  hand-off between stages on disk and running the Compose↔Edit quality loop until the
  draft clears the deterministic gates and the editorial assessment (or max iterations),
  then runs pipeline-retro to grow the system. Use when asked to turn a patent into a
  finished English essay end to end.
argument-hint: "[patent path | text | number]  [--threshold pass|revise-recommended] [--max-iter N] [--mode essay|wire]"
allowed-tools: Read, Write, Edit, Grep, Glob, Bash, Task, WebFetch, WebSearch
---

# Patent Essay — Orchestrator

Drive the three-phase pipeline and the Compose↔Edit quality loop, then the meta-loop. The
patent to process is named in `$ARGUMENTS` (a path under `input/`, raw text, or a patent
number/URL).

This orchestrator owns the **loop policy**; each phase's domain work lives in its own skill.
Stages pass data through **handoff directories on disk**, not chat copy-paste. The four
north-star goals and the goal→check matrix live in `_shared/references/scoring-rubric.md`.

## Inputs (provided per run)

- `input/patent.md` — the English patent (or whatever path `$ARGUMENTS` names).
- `input/figures/fig-NN.png` — pre-cleaned figures (Layer-1 cleaning is out of scope).
- `input/essay-context.md` — optional extra framing/context for the run.

## Parameters

- `--threshold pass|revise-recommended` — minimum editorial `overall_assessment` the loop
  accepts. **Default: `pass`** (clean). `revise-recommended` accepts medium-only findings for
  faster turnaround; it may never be relaxed to `revise-required`. See `scoring-rubric.md`.
- `--max-iter N` — max Compose↔Edit revision rounds. **Default: 4.**
- `--mode essay|wire` — deliverable mode. **Default: essay.**
- `--audience deep|investor` — reader altitude. **Default: `deep`** (patent-fidelity: inline
  `[xxxx]` anchors + reference numbers, full mechanism walkthrough, ~2000+ words). `investor`
  is the accessible altitude for the investor/analyst reader: stake-first, mechanism
  compressed, body under the word ceiling with **no inline anchors / reference numbers**, but
  it **keeps** scannable subheadings, the `# Sources` block, and figures (plain captions). The
  P1 thesis frame, P2 mode, P3 reader profile, and the `gate_readability` gate all shift with
  it. Grounding rigor is unchanged underneath (anchors live in `thesis-trace.md`). See
  `_shared/references/scoring-rubric.md` §"Audience altitude".

## Pipeline

Pass `--audience` to every phase. On `investor` it changes the thesis frame (P1), the
compose mode (P2), the editorial reader profile (P3), and activates `gate_readability`.

### Phase 1 — Design  (skill: `thesis-architect`, voice-off)
Invoke `thesis-architect` on the patent **with the audience**. It writes the design hand-off
to `handoff/01-design/` (invention-summary, thesis-spine, thesis-candidates, figure-selection,
figure-rationale, fact-check-log, search-log, phase2-handoff-notes). Also write a plain
`handoff/01-design/figures-index.txt` (one figure token per line, from the cleaned
`input/figures/`) for the gates. On `investor`, the spine favors a forward-capability / market
hook and declares a `reader_stake`; figure-selection picks fewer figures by "helps a
non-expert understand" (see `thesis-architect/references/hook-patterns.md`).

**Thesis selection (auto):** read `thesis-candidates.md` and auto-pick the recommended /
single-spine candidate. Surface the candidate list in one short line so the user can
override; if `$ARGUMENTS` names a specific thesis, use that. Confirm the choice is locked in
`thesis-spine.md`.

### Phase 2 — Compose  (skill: `essay-en-composer`, voice-on)
Invoke `essay-en-composer` **with the audience**. It reads `handoff/01-design/` (it does
**not** read the raw patent) and writes `handoff/02-compose/` (essay-draft, publication,
figures-rationale, thesis-trace). It calls `voice-canon-lookup` internally per section. On
`investor` it uses the accessible blueprint (stake-first, mechanism compressed, word ceiling,
no inline anchors/reference numbers in the body — anchors recorded in `thesis-trace.md`, plain
figure captions); see `essay-en-composer/references/mode-spec.md`.

### Phase 3 — Edit  (skill: `editorial-review`, voice-fenced)
Invoke `editorial-review` **with the audience**. It reads `handoff/02-compose/` + Phase-1
cross-check anchors, runs the 6-pass review (including the pass-3 coverage sub-check for
goal 2), and writes `handoff/03-edit/edit-log.md` with an `overall_assessment`. It does
**not** load `voice-profile` / `caption-roles`. On `investor`, pass-5 judges against the
investor reader profile and verifies grounding via `thesis-trace.md` (the body has no inline
anchors); pass-2 runs the load-bearing audit.

### Deterministic gates (mechanical, run every round before trusting the edit-log)

```
python .claude/skills/_shared/scripts/run_gates.py \
  --draft handoff/02-compose/essay-draft.md \
  --invention-summary handoff/01-design/invention-summary.md \
  --figures handoff/01-design/figures-index.txt \
  --figure-selection handoff/01-design/figure-selection.md \
  --mode <essay|wire> --audience <deep|investor> --json
```

Any gate **fail** (exit code 1) — including `FIGUSE-001` (orphan figure), and on `investor`
the readability `READAB-001/002` — is a hard fail regardless of the edit-log.

## Quality loop (inner, auto)

Round result combines the two layers:

- **gates** = pass/fail from `run_gates.py`.
- **assessment** = `overall_assessment` from `edit-log.md` (`pass` / `revise-recommended` /
  `revise-required`).

```
PASS  ⇔  gates all pass
         AND  assessment is acceptable per --threshold
         AND  grounding hard-gate not breached (no pass-3 high/critical, no gate_anchors fail)
         AND  goal-2 hard-gate not breached (no FIGUSE-001, no pass-3 coverage high)
         AND  goal-3 hard-gate not breached (investor only: no READAB-001/READAB-002)
```

While the round is **FAIL** and `iterations < max-iter`:
1. Feed the `edit-log.md` findings (+ failing gate `check_id`s) back to `essay-en-composer` in
   **revision mode** — it revises `handoff/02-compose/` in place.
2. Re-run the gates and re-invoke `editorial-review`.
3. Increment the counter.

Stop on PASS, or at `max-iter`. On stop, promote the accepted draft to
`handoff/03-edit/essay-final.md`.

Each phase's heavy work runs in its own forked context; keep only the structured hand-off
summaries in the main thread to stay within budget.

## Archive + meta-loop (after the inner loop)

1. **Archive** the run to `runs/<essay-id>/` (append `-investor` to the id for the investor
   altitude so a deep and an investor run of the same patent archive side by side): copy
   `edit-log.md`, the final `run_gates.py --json` output as `gate-result.json`, and write
   `score-history.md`.
2. **Meta-loop (skill: `pipeline-retro`, propose-only):** invoke `pipeline-retro` with the
   run's `edit-log.md` + `gate-result.json`. It normalizes findings into
   `meta/findings-ledger.jsonl` (keyed by goal + owner artifact via the matrix), and when a
   root-cause class recurs it writes an evidence-backed proposal to
   `meta/improvement-proposals/`. It **never** edits a skill — surface only the top proposal
   (if any) to the user in one line.

## Output

- The **final essay** (`handoff/03-edit/essay-final.md`, clean prose).
- A **SCORE HISTORY** table: iteration → `overall_assessment` → gate result (failing
  `check_id`s) → PASS/FAIL → one-line note.
- One line on any new `pipeline-retro` proposal awaiting human review.
- If it never cleared the bar: ship the **best round**, state the remaining findings.

## Optional: wrap with `/goal` as an outer safety net

The orchestrator's own loop already enforces the bar; `/goal` only adds an auto-resume
backstop if a run is interrupted before passing:

```
/goal the patent-essay SCORE HISTORY shows a final draft that passes all gates with overall_assessment == pass
```
