---
name: thesis-architect
description: >
  Phase 1 (Design) of the patent-essay pipeline. Analyze an English patent, research
  context, and derive falsifiable thesis candidates from the gap between conventional
  wisdom and the patent's evidence. Voice-off. Writes the design hand-off that Phase 2
  (essay-en-composer) consumes. Use when given a patent and asked to design the essay's
  angle, or as step 1 of the orchestrator.
argument-hint: "[patent path | text | number]"
context: fork
agent: general-purpose
allowed-tools: Read, Write, Grep, Glob, WebFetch, WebSearch
---

# Thesis Architect — Phase 1 (Design)

Turn an English patent (+ cleaned figures) into a defensible essay **thesis** plus the
grounding, figure plan, and fact-check seed the composer needs. This phase is
**voice-off**: it does not load `voice-profile` or `deliverable-voice-rules`, and it
makes no prose-voice decisions. It owns *framing*, not *voice*.

## Inputs

- The patent named in `$ARGUMENTS` (path under `input/`, raw text, or number/URL).
- `input/figures/fig-NN.png` — cleaned figures.
- `input/essay-context.md` (optional) — extra framing.

## References this phase may load

- `_shared/references/working-dialogue-voice.md` — how to talk to the user (dialogue, not
  deliverable).
- `_shared/references/writing-textbook.md` — argument/thesis structure rules.
- It must **not** load the deliverable-voice canon (fencing).

## Procedure (PI-derived; replace with the ported skill body)

1. **Ingest** the patent and extract an **invention summary**: independent + key
   dependent claims, the stated problem, the disclosed mechanism, notable figures and
   quantitative results. Record **Quotable spans** with `[dddd]` paragraph anchors — these
   anchors are the *only* source of truth the composer is allowed to cite.
2. **Research context** (web search): the conventional wisdom / prior-art baseline the
   patent pushes against. Log every source in `search-log.md`.
3. **Derive thesis candidates** (2–4): each is a non-obvious, falsifiable claim living in
   the gap between conventional wisdom and the patent's evidence. Anchor each to specific
   claims/figures/`[dddd]` spans.
4. **Ground each candidate** on 4 axes (evidence, novelty, stakes, defensibility), apply
   the **hook gate** (is there a real tension to open on?), and run an **adversarial
   defense** pass (what's the strongest objection, does the thesis survive?).
5. **Map figures** to the thesis and seed the **fact-check log** (claims that Phase 3
   must verify verbatim against the patent).

<!-- PORTED PROMPT: replace the Procedure above with the user's existing Phase-1 Design
     skill body (thesis-architect). Keep the output contract below intact so Phase 2 and
     Phase 3 keep parsing the hand-off. -->

## Output contract — write these 8 files to `handoff/01-design/`

| File | Contents |
|------|----------|
| `invention-summary.md` | Plain-language summary + **Quotable spans** with `[dddd]` anchors (the composer's only citable source). |
| `thesis-spine.md` | The locked thesis (one sentence) + its supporting sub-claim spine. |
| `thesis-candidates.md` | The 2–4 candidates; one marked `RECOMMENDED` with a one-line rationale. |
| `search-log.md` | Every research source (title, URL, what it establishes). |
| `figure-selection.md` | The figures to use, by number (one usable figure number per line is fine for the gate parser). |
| `figure-rationale.md` | Why each selected figure earns its place; ties to the thesis. |
| `fact-check-log.md` | Claims Phase 3 must verify verbatim against the patent. |
| `phase2-handoff-notes.md` | The composer's entry point: what to argue, in what order, with which anchors/figures. |

Do not invent claim numbers, figures, results, or `[dddd]` anchors. If the source is
incomplete, say so in `invention-summary.md`.
