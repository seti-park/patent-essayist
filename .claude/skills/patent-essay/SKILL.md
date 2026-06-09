---
name: patent-essay
description: >
  Orchestrator / entry point for the patent-essay system. Given an English patent, runs
  the full pipeline — analyze → derive hypothesis → structure → write → evaluate — and
  loops write↔evaluate until the rubric score clears the threshold or max iterations.
  Use when asked to turn a patent into a finished English essay end to end.
argument-hint: "[patent text | file path | number]  [--threshold N] [--max-iter N]"
allowed-tools: Read, Write, Grep, Glob, Task, WebFetch, WebSearch
---

# Patent Essay — Orchestrator

Drive the full pipeline and the quality loop. The patent to process is in `$ARGUMENTS`.

## Parameters (defaults from the rubric)

- `--threshold N` — pass score on 0–100. **Default: 85.**
- `--max-iter N` — max write↔evaluate revision rounds. **Default: 4.**

## Pipeline

1. **Analyze** — invoke the `patent-analyze` skill on the patent. Capture its output and
   the RECOMMENDED HYPOTHESIS. If the user named a different hypothesis in `$ARGUMENTS`,
   use that instead.
2. **Structure** — invoke `essay-structure` with the chosen hypothesis to get the
   outline.
3. **Write** — invoke `essay-write` with the outline to get the first draft.
4. **Evaluate** — invoke `essay-evaluate` on the draft. Parse `FINAL SCORE` and the
   PASS/FAIL line.
5. **Loop** — while the result is FAIL and iterations < `--max-iter`:
   - invoke `essay-write` in **revision mode**, passing the evaluator's REVISION ACTIONS;
   - re-invoke `essay-evaluate` on the new draft;
   - increment the iteration counter.
6. **Stop** when PASS, or when `--max-iter` is reached.

Each step's heavy work runs in its own context (the analyze/evaluate skills fork); keep
only their structured outputs in the main thread to stay within budget.

## Output

- The **final essay** (clean prose).
- A **SCORE HISTORY** table: iteration → FINAL SCORE → PASS/FAIL → one-line note.
- If it never cleared the threshold: ship the **best-scoring** draft and state the
  remaining gap plus the unaddressed REVISION ACTIONS.

## Optional: wrap with `/goal` as an outer safety net

For extra assurance the user can run, around this orchestrator:

```
/goal the patent-essay SCORE HISTORY shows a final draft with FINAL SCORE >= 85 and PASS
```

The orchestrator's own loop already enforces the threshold; `/goal` only adds an
automatic-resume backstop if a run is interrupted before passing.

<!-- The four stage prompts live in the patent-analyze / essay-structure / essay-write /
     essay-evaluate skills. Port the user's existing prompts there; this orchestrator just
     wires them together and owns the loop policy. -->
