# Patent Essay System (Claude Code / web)

A skill-based pipeline that turns an **English patent** into a finished **English essay**:
analyze the patent and derive a hypothesis, structure an article from writing-textbook
rules, write it in a natural voice, then score it against a rubric and loop until it
clears a quality threshold.

## How to run

From a Claude Code session in this repo:

```
/patent-essay <patent text | file path | patent number>  [--threshold 85] [--max-iter 4]
```

The orchestrator runs the whole pipeline and the write↔evaluate loop, then returns the
final essay plus a score history. Optional outer backstop:

```
/goal the patent-essay SCORE HISTORY shows a final draft with FINAL SCORE >= 85 and PASS
```

Individual stages can also be run standalone: `/patent-analyze`, `/essay-structure`,
`/essay-write`, `/essay-evaluate`.

## Architecture

```
.claude/skills/
  patent-essay/      orchestrator + loop policy (entry point)
  patent-analyze/    1. patent → analysis + hypothesis candidates   (forked context)
  essay-structure/   2. hypothesis → English article outline
  essay-write/       3. outline → natural draft (+ humanizer pass)
  essay-evaluate/    4. draft → 0–100 score + AI-tell + actions       (forked context)
  _shared/
    references/      writing-textbook.md · style-guide.md · scoring-rubric.md
    vendor/          third-party humanizer + ai-check skills (MIT, see vendor/README.md)
```

Data flows by **output contracts**: each stage's SKILL.md defines the exact output the
next stage parses. The orchestrator reads `essay-evaluate`'s `FINAL SCORE` / `PASS|FAIL`
to decide whether to loop, feeding the `REVISION ACTIONS` back into `essay-write`.

## Loop control

Two layers, by design:
- **Orchestrator (core):** precise numeric rubric scoring, threshold, and max iterations
  — deterministic and reproducible.
- **`/goal` (optional outer net):** auto-resume backstop if a run is interrupted before
  passing. Not required for normal runs.

## Customization

- **Tune behavior** in `_shared/references/` — the writing rules, voice, rubric weights,
  threshold (default 85), and grounding hard-gate live there, not in code.
- **Port existing prompts:** each stage SKILL.md has a `<!-- PORTED PROMPT: ... -->`
  marker showing exactly where to drop your existing analysis/structure/writing/
  evaluation prompts. Keep each stage's **Output contract** intact so the pipeline keeps
  parsing.
- **Swap the humanizer:** replace files under `_shared/vendor/` and update the references
  in `essay-write` / `essay-evaluate`.

## Note

The legacy static HTML files (`index.html`, `1.html`–`3.html`) are unrelated leftovers
and are not part of this system.
