---
name: patent-essay
description: >
  Orchestrator / entry point for the patent-essay system. Given an English patent (+
  cleaned figures), runs Phase 1 Design → Phase 2 Compose → Phase 3 Edit, automating the
  hand-off between stages on disk and running the Compose↔Edit quality loop until the
  draft clears the deterministic gates and the editorial threshold (or max iterations).
  Use when asked to turn a patent into a finished English essay end to end.
argument-hint: "[patent path | text | number]  [--threshold N] [--max-iter N] [--mode essay|wire]"
allowed-tools: Read, Write, Edit, Grep, Glob, Bash, Task, WebFetch, WebSearch
---

# Patent Essay — Orchestrator

Drive the three-phase pipeline and the Compose↔Edit quality loop. The patent to process
is named in `$ARGUMENTS` (a path under `input/`, raw text, or a patent number/URL).

This orchestrator owns the **loop policy**; each phase's domain work lives in its own
skill. Stages pass data through **handoff directories on disk**, not chat copy-paste.

## Inputs (provided per run)

- `input/patent.md` — the English patent (or whatever path `$ARGUMENTS` names).
- `input/figures/fig-NN.png` — pre-cleaned figures (Layer-1 figure cleaning is out of
  scope; assume figures arrive cleaned).
- `input/essay-context.md` — optional extra framing/context for the run.

## Parameters (defaults from the rubric)

- `--threshold N` — editorial pass score on 0–100. **Default: 85.** (See
  `_shared/references/scoring-rubric.md`.)
- `--max-iter N` — max Compose↔Edit revision rounds. **Default: 4.**
- `--mode essay|wire` — deliverable mode. **Default: essay.**

## Pipeline

### Phase 1 — Design  (skill: `thesis-architect`)
Invoke `thesis-architect` on the patent. It writes the design hand-off to
`handoff/01-design/` (8 files; see that skill's output contract). It is **voice-off**.

**Thesis selection (auto):** read `handoff/01-design/thesis-candidates.md` and auto-pick
the `RECOMMENDED` candidate. Surface the candidate list to the user in one short line so
they can override; if `$ARGUMENTS` names a specific thesis, use that. Record the chosen
thesis id into `handoff/01-design/thesis-spine.md` if not already locked.

### Phase 2 — Compose  (skill: `essay-en-composer`)
Invoke `essay-en-composer`. It reads `handoff/01-design/` (it does **not** read the raw
patent) and writes `handoff/02-compose/` (4 files). It is **voice-on** and calls
`voice-canon-lookup` internally per section.

### Phase 3 — Edit  (skill: `editorial-review`)
Invoke `editorial-review`. It reads `handoff/02-compose/` plus Phase-1 cross-check
anchors, runs the 6-pass editorial review, and writes `handoff/03-edit/edit-log.md`. It
is **voice-fenced** (no `voice-profile`/`caption-roles`).

### Deterministic gates (mechanical, before trusting any editorial score)
Run the real gate scripts and parse their result:

```
python .claude/skills/_shared/scripts/run_gates.py \
  --draft handoff/02-compose/essay-draft.md \
  --invention-summary handoff/01-design/invention-summary.md \
  --figures handoff/01-design/figure-selection.md \
  --mode <essay|wire> --json
```

Any gate **fail** (exit code 1) is a hard fail regardless of the editorial score.

## Quality loop (auto)

Compute the round result:

- **score** = editorial qualitative score (0–100) from `edit-log.md`.
- **gates** = pass/fail from `run_gates.py`.

```
PASS  ⇔  gates all pass  AND  score >= threshold  AND  no grounding hard-gate breach
```

While the round is **FAIL** and `iterations < max-iter`:
1. Feed the `edit-log.md` findings (and any gate `check_id`s) back to `essay-en-composer`
   in **revision mode** — it revises `handoff/02-compose/` in place.
2. Re-run the deterministic gates and re-invoke `editorial-review`.
3. Increment the counter.

Stop on PASS, or when `max-iter` is reached. On stop, promote the accepted draft to
`handoff/03-edit/essay-final.md`.

Each phase's heavy work runs in its own context (the analyze/edit skills fork); keep only
the structured hand-off summaries in the main thread to stay within budget.

## Output

- The **final essay** (`handoff/03-edit/essay-final.md`, clean prose).
- A **SCORE HISTORY** table: iteration → editorial score → gate result (with failing
  `check_id`s) → PASS/FAIL → one-line note.
- If it never cleared the bar: ship the **best round** and state the remaining gap plus
  the unaddressed findings.

## Optional: wrap with `/goal` as an outer safety net

The orchestrator's own loop already enforces the bar; `/goal` only adds an auto-resume
backstop if a run is interrupted before passing:

```
/goal the patent-essay SCORE HISTORY shows a final draft that passes all gates with score >= 85
```

<!-- The four phase prompts live in thesis-architect / essay-en-composer /
     voice-canon-lookup / editorial-review. Port the user's existing skill bodies there;
     this orchestrator only wires them together, automates the on-disk hand-off, and owns
     the loop + gate policy. -->
