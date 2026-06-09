---
name: essay-en-composer
description: >
  Phase 2 (Compose) of the patent-essay pipeline. Read the Phase-1 design hand-off and
  compose a natural English essay (X Articles format): section blueprint → figure plan →
  voiced drafting → strip pipeline. Voice-on. Also runs in revision mode from Phase-3
  edit findings. Use after thesis-architect, or as step 2 of the orchestrator.
argument-hint: "[optional: revision mode + edit-log findings]"
allowed-tools: Read, Write, Edit, Grep, Glob, Task
---

# Essay EN Composer — Phase 2 (Compose)

Compose the English essay from the design hand-off. This phase is **voice-on**: it owns
*voice*, not *framing* (Phase 1) and not *editorial* decisions (Phase 3). It never reads
the raw patent — `handoff/01-design/invention-summary.md` **Quotable spans** (the `[dddd]`
anchors) are the only citable source of truth.

## Inputs

- `handoff/01-design/` — 7 files (everything except `search-log.md`):
  `phase2-handoff-notes.md` is the entry point; `invention-summary.md`,
  `thesis-spine.md`, `figure-selection.md`, `figure-rationale.md`, `fact-check-log.md`,
  `thesis-candidates.md`.
- `input/figures/fig-NN.png` — cleaned figures.
- **Revision mode:** `handoff/03-edit/edit-log.md` findings (+ failing gate `check_id`s).
  Address each finding; keep what already scored well; do not regress grounding.

## References this phase loads (full voice stack — voice-on)

- `_shared/references/working-dialogue-voice.md`
- `_shared/references/deliverable-voice-rules.md`
- `_shared/references/anti-ai-writing.md`
- `_shared/references/voice-profile.md`
- `_shared/references/x-article-format.md`
- `_shared/references/caption-roles.md`

## Procedure (PI-derived; replace with the ported skill body)

1. **Read `phase2-handoff-notes.md`** — the composer's marching orders from Phase 1.
2. **Section blueprint** — plan sections per `x-article-format.md`; every section traces
   to `thesis-spine.md`.
3. **Figure plan** — assign each selected figure a `caption_role` (one of the 4 roles in
   `caption-roles.md`) and lock figure placement (`figures_locked`).
4. **Draft section by section** — for each section, call `voice-canon-lookup` to pull the
   exact voice rule for the move you're making, then write. Cite only `[dddd]` anchors
   from `invention-summary.md`; never quote the raw patent.
5. **Strip pipeline** — run the draft through the anti-AI strip (per `anti-ai-writing.md`)
   to produce the clean publication copy. The deterministic gate scripts are the
   mechanical backstop for this step; aim to pass them before hand-off.
6. **Revision mode** — apply each `edit-log.md` finding explicitly and note it in
   `thesis-trace.md`.

<!-- PORTED PROMPT: replace the Procedure above with the user's existing Phase-2 Compose
     skill body (essay-en-composer + voice-canon-lookup). Keep the output contract intact
     so Phase 3 and the gates keep parsing. -->

## Output contract — write these 4 files to `handoff/02-compose/`

| File | Contents |
|------|----------|
| `essay-draft.md` | The working draft (pre-strip), with `[dddd]` citations and figure refs inline. The gates run against this file. |
| `publication.md` | The clean, stripped publication copy (no scaffolding/meta). |
| `figures-rationale.md` | Each figure's `caption_role`, placement, and why it earns its spot. |
| `thesis-trace.md` | Section → sub-claim → anchors/figures used; in revision mode, which edit findings were addressed. |

Every section must trace to the thesis. Do not introduce facts or anchors that are not in
the Phase-1 hand-off.
