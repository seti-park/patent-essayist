# Patent Essay System (Claude Code / web)

A skill-based pipeline that turns an **English patent** (+ cleaned figures) into a finished
**English essay** for X Articles. Three phases — **Design → Compose → Edit** — pass data
through on-disk hand-off directories, and an orchestrator runs the Compose↔Edit quality
loop until the draft clears the deterministic gates and the editorial threshold.

This is a conversion of a system originally run as four separate claude.ai Projects. The
originals are the reference baseline (preserved in `docs/source-prompts/`); the conversion
adds three improvements: **automated stage hand-off**, **real deterministic gate scripts**,
and an **automatic quality loop**.

## How to run

```
/patent-essay <patent path | text | number>  [--threshold 85] [--max-iter 4] [--mode essay|wire]
```

Inputs live under `input/`: `patent.md`, `figures/fig-NN.png` (pre-cleaned), and optional
`essay-context.md`. The orchestrator runs all three phases plus the loop and returns the
final essay (`handoff/03-edit/essay-final.md`) plus a score history. Optional outer
backstop:

```
/goal the patent-essay SCORE HISTORY shows a final draft that passes all gates with score >= 85
```

Individual phases can be run standalone: `/thesis-architect`, `/essay-en-composer`,
`/editorial-review` (`/voice-canon-lookup` is an internal Phase-2 helper).

## Architecture

```
.claude/skills/
  patent-essay/        orchestrator: P1→P2→P3 + Compose↔Edit auto loop (entry point)
  thesis-architect/    P1 Design  — patent → thesis + grounding + figure plan (voice-off, forked)
  essay-en-composer/   P2 Compose — design hand-off → blueprint → draft → strip (voice-on)
  voice-canon-lookup/  P2 internal helper (per-section voice lookup)
  editorial-review/    P3 Edit    — 6-pass review + gate scripts → edit-log (voice-fenced, forked)
  _shared/
    references/        canon: voice-profile · deliverable-voice-rules · anti-ai-writing ·
                       x-article-format · caption-roles · working-dialogue-voice ·
                       writing-textbook · scoring-rubric
    scripts/           deterministic gate scripts (Python, stdlib) + tests
    vendor/            optional ai-check (humanizer demoted) — see vendor/README.md
handoff/  01-design/  02-compose/  03-edit/    runtime stage artifacts (gitignored)
input/    patent.md · figures/ · essay-context.md
docs/source-prompts/  original claude.ai Project assets (reference)
```

Data flows by **output contracts**: each phase's `SKILL.md` defines the exact files it
writes to its `handoff/<phase>/` directory, and the next phase reads them — no chat
copy-paste.

## Voice fencing (by which references each phase loads)

The original system enforced this by physically separate Projects; here it is enforced by
which `_shared/references/` files each phase loads:

- **Design (voice-off):** writing-textbook only — no deliverable-voice canon.
- **Compose (voice-on):** full voice stack (voice-profile, deliverable-voice, anti-ai,
  x-article-format, caption-roles).
- **Edit (voice-fenced):** deliverable-voice-rules + anti-ai-writing only — **not**
  voice-profile or caption-roles, to prevent editor voice drift.

## Loop control

Two layers, by design:
- **Orchestrator (core):** deterministic gates (hard pass/fail, real scripts) + qualitative
  editorial score, threshold (default 85), grounding hard-gate, and max iterations
  (default 4). On FAIL it feeds the edit findings back into Compose and re-scores.
- **`/goal` (optional outer net):** auto-resume backstop if a run is interrupted before
  passing. Not required for normal runs.

## Deterministic gates

`_shared/scripts/run_gates.py` runs five mechanical checks over the draft and returns
pass/fail + `check_id`s: `gate_emdash` (em-dash outside quotes), `gate_anchors`
(`[dddd]`/figure refs resolve to the Phase-1 hand-off), `gate_sources` (Sources block),
`gate_banned` (anti-AI banned terms), `gate_structure` (heuristic warnings). Run
`python .claude/skills/_shared/scripts/test_gates.py` for the test suite.

## Customization

- **Tune behavior** in `_shared/references/` — voice canon, structure rules, rubric weights,
  threshold, grounding hard-gate. The banned-term list is mirrored to
  `_shared/scripts/banned_terms.txt` for mechanical enforcement.
- **Port the originals:** each phase `SKILL.md` has a `<!-- PORTED PROMPT -->` marker for
  dropping the original skill body; Knowledge files map to `_shared/references/`. Keep each
  phase's **output contract** intact so the hand-off keeps parsing.
- **Swap the AI-tell cross-check:** replace files under `_shared/vendor/` (optional only).

## Note

The legacy static HTML files (`index.html`, `1.html`–`3.html`) are unrelated leftovers and
are not part of this system.
