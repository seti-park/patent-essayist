# Scoring Rubric — Phase 3 Edit + Quality Loop

> **Status: SCAFFOLD.** Defines how Phase 3 (`editorial-review`) scores a draft and how the
> orchestrator decides PASS/FAIL for the Compose↔Edit loop. Two layers: a **deterministic
> gate** (mechanical, hard pass/fail) and a **qualitative editorial score** (0–100). Tune
> weights, threshold, and the banned/structure constants to taste.

## Layer 1 — Deterministic gates (hard, mechanical)

Run `_shared/scripts/run_gates.py` over `handoff/02-compose/essay-draft.md`. It returns a
machine pass/fail plus `check_id`s. **Any `fail`-severity finding fails the round outright**,
regardless of the qualitative score:

| Gate | Hard `check_id`s | Meaning |
|------|------------------|---------|
| `emdash`   | `EMDASH-001` | em-dash outside quotes |
| `anchors`  | `ANCHOR-001`, `FIGREF-001` | `[dddd]` / figure ref doesn't resolve to the Phase-1 hand-off |
| `sources`  | `SOURCES-001/002/003` | missing or malformed Sources block |
| `banned`   | `BANNED-001` | banned AI-tell term/construction outside quotes |
| `structure`| (`STRUCT-00x` are **warn** only) | heuristic structure smells |

Warnings do not fail the round; they feed the qualitative score and the revision actions.

## Layer 2 — Qualitative editorial score (0–100)

The 6-pass review scores these dimensions:

| # | Dimension | Weight | Full marks |
|---|-----------|--------|-----------|
| 1 | **Thesis adherence** | 25 | Every section traces to `thesis-spine.md`. |
| 2 | **Grounding / anchor-chain** | 25 | All claims anchored to Phase-1 `[dddd]`/figures; nothing invented. |
| 3 | **Verbatim fact-check** | 15 | `fact-check-log.md` claims match `input/patent.md` word-for-word. |
| 4 | **Voice compliance** | 15 | Matches `deliverable-voice-rules.md` + `anti-ai-writing.md` (NOT voice-profile). |
| 5 | **Structure / format** | 10 | Conforms to `x-article-format.md`. |
| 6 | **So-what / close** | 10 | Specific, falsifiable takeaway. |

Editorial score = weighted sum (max 100). The optional vendored `ai-check` may feed
dimension 4 as a secondary cross-check; it is not the source of truth.

## PASS / FAIL (orchestrator loop policy)

```
PASS  ⇔  Layer-1 gates all pass
         AND  editorial score >= threshold
         AND  grounding hard-gate not breached
```

- **Pass threshold: 85** (default; `--threshold` overrides).
- **Grounding hard-gate:** dimension 2 < 18/25 is an automatic FAIL — never ship weak or
  invented grounding, even if the total clears the threshold.
- **Max revision iterations: 4** (`--max-iter`). If still failing after the cap, return the
  best round with the remaining gap and the unaddressed revision actions.

## Required Phase-3 output

`editorial-review` writes `handoff/03-edit/edit-log.md` (YAML; schema in that skill),
including `gates`, the six `passes`, `score`, `grounding_gate`, `verdict`, and
`revision_actions` (only when FAIL). The orchestrator parses `verdict` + gate result to
drive the loop and feeds `revision_actions` back into `essay-en-composer`.
