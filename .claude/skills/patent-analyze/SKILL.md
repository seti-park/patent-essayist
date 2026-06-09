---
name: patent-analyze
description: >
  Step 1 of the patent-essay pipeline. Analyze an English patent and derive
  hypothesis/thesis candidates for an essay. Use when given a patent (text, file path,
  or number) and asked to analyze it or extract essay angles.
argument-hint: "[patent text | file path]"
context: fork
agent: general-purpose
allowed-tools: Read, Grep, Glob, WebFetch, WebSearch
---

# Patent Analyze

Analyze the English patent provided in `$ARGUMENTS` (raw text, a file path to read, or a
patent number/URL to fetch) and produce a structured analysis plus essay hypotheses.

## Procedure

1. **Ingest** the patent. If `$ARGUMENTS` is a path, Read it. If it's a number/URL,
   fetch it. If it's raw text, use it directly.
2. **Extract** the technical core:
   - Independent claims (what is actually protected) and key dependent claims.
   - The problem the patent says it solves; the disclosed solution/mechanism.
   - Notable figures, embodiments, and any quantitative results.
   - Stated or implied prior-art tension and novelty.
3. **Derive hypotheses.** Propose 2–4 distinct, non-obvious, falsifiable thesis
   candidates an essay could argue (technical significance, competitive/market angle,
   limitation/risk angle). Each must be anchored to specific claims/figures.

<!-- PORTED PROMPT: replace the Procedure above with the user's existing ANALYSIS prompt.
     Keep the Output contract section below intact so downstream skills still parse it. -->

## Output contract (downstream `essay-structure` depends on this)

Return exactly these sections:

- **PATENT SUMMARY** — 3–5 sentences, plain language.
- **CORE CLAIMS** — bulleted list, each with claim number + one-line gist.
- **NOVELTY & PRIOR-ART TENSION** — what's new and against what.
- **HYPOTHESIS CANDIDATES** — numbered list; for each: the thesis sentence, the angle
  type, and the specific patent evidence (claim #/figure) it rests on.
- **RECOMMENDED HYPOTHESIS** — pick one with a one-line rationale (the orchestrator or
  user may override).

Do not invent claim numbers, figures, or results. If the source is incomplete, say so.
