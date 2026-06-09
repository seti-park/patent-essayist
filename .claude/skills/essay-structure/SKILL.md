---
name: essay-structure
description: >
  Step 2 of the patent-essay pipeline. Build an English article outline from a chosen
  hypothesis + patent analysis, following the writing-textbook structure rules. Use after
  patent-analyze, or when given an analysis and asked to outline the essay.
argument-hint: "[chosen hypothesis] (uses prior patent-analyze output)"
allowed-tools: Read, Grep, Glob
---

# Essay Structure

Turn a chosen hypothesis + patent analysis into a concrete English article outline.

## Inputs

- The `patent-analyze` output (PATENT SUMMARY, CORE CLAIMS, HYPOTHESIS CANDIDATES).
- The selected hypothesis from `$ARGUMENTS` (default: the RECOMMENDED HYPOTHESIS).

## Procedure

1. **Read the structure rules:** `.claude/skills/_shared/references/writing-textbook.md`.
   Follow its required structure and structural rules; reject its listed anti-patterns.
2. **Lock the thesis** = the chosen hypothesis, phrased as one sentence.
3. **Plan sections.** For each body section, specify: the sub-claim it argues, the
   specific patent evidence (claim #/figure/passage) it uses, and the implication.
4. **Sequence** sections by logical dependency, not patent layout. Add the
   counterpoint/limits section and the so-what close.

<!-- PORTED PROMPT: replace the Procedure above with the user's existing STRUCTURE prompt.
     Keep the Output contract intact so essay-write can consume it. -->

## Output contract (downstream `essay-write` depends on this)

A nested outline:

- **THESIS** — one sentence.
- **HOOK** — one line describing the opening tension/stakes.
- **GROUNDING** — what plain-language patent facts this section establishes.
- **BODY SECTIONS** — for each: `Header → sub-claim → evidence (claim#/figure) →
  implication`.
- **COUNTERPOINT** — the honest limit/risk to address.
- **CLOSE** — the specific, falsifiable takeaway.
- **TARGET LENGTH** — words (default 600–1,100).

Every body section must trace to the thesis. If one doesn't, cut it and note why.
