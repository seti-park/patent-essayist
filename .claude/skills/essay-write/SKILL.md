---
name: essay-write
description: >
  Step 3 of the patent-essay pipeline. Write (or revise) a natural English essay from an
  outline, applying the style guide and the vendored humanizer pass. Use after
  essay-structure, or when given an outline (and optional revision feedback) to draft.
argument-hint: "[outline] [+ optional revision feedback]"
allowed-tools: Read, Write, Grep, Glob
---

# Essay Write

Draft a natural-sounding English patent essay from the outline, then strip AI tells.

## Inputs

- The `essay-structure` outline.
- (Revision mode) The prioritized revision actions from `essay-evaluate`. If present,
  revise the existing draft to address them rather than starting from scratch.

## Procedure

1. **Read the style guide:** `.claude/skills/_shared/references/style-guide.md`. Write to
   its voice/sentence/word-choice/formatting rules.
2. **Draft** the essay section by section from the outline. Anchor every claim to the
   patent specifics named in the outline. Never invent claim numbers/figures/results.
3. **Humanize.** Apply the vendored humanizer skill at
   `.claude/skills/_shared/vendor/humanizer/SKILL.md` (Read it and follow its
   detect→rewrite passes) over the draft to remove residual AI tells while preserving
   meaning and patent accuracy.
4. **Revision mode:** address each evaluator action explicitly; keep what already scored
   well; don't regress grounding or accuracy.

<!-- PORTED PROMPT: replace the Procedure above with the user's existing WRITING prompt.
     Keep the humanize step (3) and the Output contract so the loop still works. -->

## Output contract (downstream `essay-evaluate` depends on this)

- The full essay as clean prose (no outline scaffolding, no meta commentary).
- A one-line **CHANGELOG** at the very end listing, in revision mode, which evaluator
  actions were addressed (omit on the first draft).
