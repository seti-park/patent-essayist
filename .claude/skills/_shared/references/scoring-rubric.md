# Scoring Rubric — Patent Essay Evaluation

> **Status: SCAFFOLD.** Starter rubric. Tune weights and threshold to taste.
> `essay-evaluate` produces a numeric score from this rubric and combines it with the
> AI-tell score from the vendored `ai-check` skill.

## Composite score (0–100)

The final score is a weighted sum of five rubric dimensions, then adjusted by the
AI-tell penalty.

| # | Dimension | Weight | What earns full marks |
|---|-----------|--------|-----------------------|
| 1 | **Thesis & hypothesis** | 25 | One clear, non-obvious, falsifiable hypothesis derived from the patent; stated up front. |
| 2 | **Grounding in the patent** | 25 | Every major claim anchored to specific claims/figures/passages; no invented facts. |
| 3 | **Argument structure** | 20 | Follows `writing-textbook.md`; sections advance the thesis in logical order; honest counterpoint present. |
| 4 | **Prose quality & voice** | 15 | Matches `style-guide.md`; varied rhythm; concrete; readable. |
| 5 | **Insight / so-what** | 15 | Specific, consequential takeaway; not generic. |

Subtotal = sum of the five (max 100).

## AI-tell penalty (from `ai-check`)

Run `_shared/vendor/ai-check/SKILL.md`. It returns an OVERALL SCORE on 0–27 (higher =
more AI-like). Convert to a penalty:

| ai-check 0–27 | Penalty (subtract from subtotal) |
|---------------|----------------------------------|
| 0–3   | 0  |
| 4–6   | 5  |
| 7–10  | 12 |
| 11–15 | 20 |
| 16+   | 30 |

**Final score = clamp(Subtotal − Penalty, 0, 100).**

## Threshold & loop policy (defaults — orchestrator may override)

- **Pass threshold: 85.**
- **Hard gate:** regardless of total, dimension 2 (Grounding) < 18/25 is an automatic
  fail — never ship an essay with weak/invented patent grounding.
- **Max revision iterations: 4.** If still < threshold after 4, return the best draft so
  far with a clear note on the remaining gap.

## Required evaluator output

`essay-evaluate` must return, in this order:
1. Per-dimension scores (1–5) with one-line justification each.
2. ai-check OVERALL SCORE (0–27) + verdict + the penalty applied.
3. **FINAL SCORE: NN / 100** and **PASS** or **FAIL (below threshold | grounding gate)**.
4. Top 3 prioritized, concrete revision actions (only if FAIL) — these feed the next
   `essay-write` revision pass.
