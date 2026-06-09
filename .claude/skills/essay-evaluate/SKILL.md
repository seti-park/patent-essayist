---
name: essay-evaluate
description: >
  Step 4 of the patent-essay pipeline. Score an essay draft against the rubric and the
  AI-tell (ai-check) detector, returning a 0–100 score, pass/fail vs threshold, and
  prioritized revision actions. Use after essay-write to grade a draft.
argument-hint: "[essay draft] (uses outline + analysis as reference)"
context: fork
agent: general-purpose
allowed-tools: Read, Grep, Glob
---

# Essay Evaluate

Grade the essay draft and decide whether it passes the quality threshold.

## Inputs

- The `essay-write` draft (from `$ARGUMENTS` or the latest draft).
- For reference: the `essay-structure` outline and `patent-analyze` output (to verify
  thesis adherence and grounding accuracy).

## Procedure

1. **Read the rubric:** `.claude/skills/_shared/references/scoring-rubric.md`. Score each
   of the five dimensions and compute the subtotal.
2. **Run AI-tell detection:** apply the vendored `ai-check` skill at
   `.claude/skills/_shared/vendor/ai-check/SKILL.md` (Read it, follow its nine-signal
   forensic scoring) to get the OVERALL SCORE on 0–27 and verdict. Map it to the penalty
   per the rubric.
3. **Verify grounding accuracy** against the analysis: flag any claim number, figure, or
   result not supported by the patent (this can trigger the grounding hard-gate).
4. **Decide** PASS/FAIL against the threshold and the grounding hard-gate.

<!-- PORTED PROMPT: replace the Procedure above with the user's existing EVALUATION
     prompt. Keep steps 2 (ai-check) and the Output contract so the orchestrator loop
     can parse the score and actions. -->

## Output contract (the orchestrator parses this to drive the loop)

Return, in this exact order:
1. **DIMENSION SCORES** — the five rubric dimensions with score + one-line justification.
2. **AI-TELL** — ai-check OVERALL SCORE `NN/27`, verdict, and the penalty applied.
3. **FINAL SCORE: NN / 100** followed by **PASS** or
   **FAIL (below threshold | grounding gate)**.
4. **REVISION ACTIONS** — top 3 concrete, prioritized fixes (only when FAIL). These are
   fed verbatim into the next `essay-write` revision pass.
