# Scoring Rubric — Phase 3 Edit + Quality Loop

Defines how the orchestrator decides PASS/FAIL for the Compose↔Edit loop. Two layers,
by design:

1. **Deterministic gates** (mechanical, hard pass/fail) — `_shared/scripts/run_gates.py`.
2. **Qualitative editorial assessment** — `editorial-review`'s 6-pass review, expressed as a
   **severity model** (`overall_assessment`), not an arbitrary 0–100 number. This mirrors the
   real `editorial-review/references/feedback-format.md` so the loop and the editor speak the
   same language.

## North-star goals → checks (acceptance traceability matrix)

The system exists to satisfy four goals. They are first-class acceptance criteria, and every
gate/pass below is here because it defends one of them. The meta-loop (`pipeline-retro`) uses
the **owner** column to attribute a recurring finding back to the stage/artifact that should
have prevented it.

| Goal | Deterministic gate | Editorial pass | Upstream owner (P1/P2 artifact) |
|------|--------------------|----------------|---------------------------------|
| **1. Catch the patent's core accurately** | `gate_anchors` (ANCHOR-001/002 anchor-chain + format) | pass-3 claim-adequacy / paraphrase, pass-4 logic | invention-summary 4-layer + Quotable spans, 4-axis grounding, thesis-spine |
| **2. Use figures + spec sufficiently** | **`gate_figure_use`** (FIGUSE-001 orphan) + `gate_anchors` (FIGREF-001) | **pass-3 coverage sub-check** (core-mechanism layer / Quotable span left uncovered) | figure-selection / figure-rationale, invention-summary Quotable spans |
| **3. Easy for the reader to understand** | `gate_structure` (warn) + **`gate_readability` (enforced on `investor`)** | pass-5 reader-perspective (audience-conditional profile) | audience altitude + mode/posture calibration |
| **4a. Well-structured** | `gate_structure` | pass-6 lead/conclusion + format | section-blueprint, x-articles-format-en, thesis arc |
| **4b. Natural (not AI-tell)** | `gate_banned`, `gate_emdash` | pass-1 voice + anti-ai | voice-on drafting + anti-ai canon + strip-pipeline |

When `pipeline-retro` records a finding, it tags it with the goal it threatens and the owner
artifact, so improvement proposals target the true root cause rather than the symptom.

## Audience altitude (`--audience deep|investor`)

Audience is a first-class pipeline dimension that changes the deliverable's altitude, not just
its surface. Two values:

- **`deep` (default)** — the patent-fidelity altitude: inline `[xxxx]` anchors + reference
  numbers on the surface, full mechanism walkthrough, ~2000+ words. Backward-compatible; all
  existing behavior and gates are unchanged. `gate_readability` is inert.
- **`investor`** — the accessible altitude for SETI's actual X readers (investors / analysts).
  The accessible-format contract: **keep** scannable subheadings, the `# Sources` 5-label
  block, and figures (plain captions, no reference numbers); **drop** inline `[xxxx]` /
  reference numbers from the reader-facing body and compress to a stake-first, so-what-led
  piece under the word ceiling. Grounding rigor is unchanged underneath — anchor↔claim
  traceability moves to `handoff/02-compose/thesis-trace.md`, where editorial pass-3 verifies
  it; it just does not surface to the reader. Audience can also flip the P1 thesis frame (an
  `investor` spine favors a forward-capability / market hook, with a `reader_stake` field).

This promotes **goal 3 from warn-only to enforced** for `investor`: `gate_readability`'s
`READAB-001` (length ceiling) and `READAB-002` (no inline anchors in body) are hard fails, and
pass-5 judges against the declared investor reader profile (see
`editorial-review/references/pass-5-reader-perspective.md`).

## Layer 1 — Deterministic gates (hard, mechanical)

Run `run_gates.py` over `handoff/02-compose/essay-draft.md`, passing the Phase-1 hand-off so
the chain/figure/orphan checks resolve. **Any `fail`-severity finding fails the round
outright**, regardless of the editorial assessment. Warnings never fail the round; they feed
the editorial passes and the revision actions.

| Gate | Hard `check_id`s (fail) | Warn `check_id`s | Defends goal |
|------|-------------------------|------------------|--------------|
| `emdash`     | `EMDASH-001` | `EMDASH-002` | 4b |
| `anchors`    | `ANCHOR-001`, `ANCHOR-002`, `FIGREF-001` | `ANCHOR-000`, `FIGREF-000` | 1, 2 |
| `sources`    | `SOURCES-001/002/003` | `SOURCES-004` | 4a |
| `banned`     | `BANNED-001` | — | 4b |
| `structure`  | (none — all warn) | `STRUCT-001..004` | 3, 4a |
| `figure_use` | `FIGUSE-001` (orphan figure) | `FIGUSE-000`, `FIGUSE-002` | 2 |
| `readability`| `READAB-001` (length), `READAB-002` (inline anchor in body) — **`investor` audience only** | `READAB-000` (skipped on `deep`), `READAB-003` | 3 |

Invocation (orchestrator):

```
python _shared/scripts/run_gates.py \
  --draft handoff/02-compose/essay-draft.md \
  --invention-summary handoff/01-design/invention-summary.md \
  --figures handoff/01-design/figures-index.txt \
  --figure-selection handoff/01-design/figure-selection.md --json
```

## Layer 2 — Editorial assessment (severity model)

`editorial-review` runs the 6 passes and emits one `overall_assessment` from this enum,
computed from the worst-severity finding present (see `editorial-review/references/feedback-format.md`):

| Has critical? | Has high? | Has medium? | `overall_assessment` |
|---|---|---|---|
| Yes | (any) | (any) | `revise-required` |
| No  | Yes  | (any) | `revise-required` |
| No  | No   | Yes   | `revise-recommended` |
| No  | No   | No    | `pass` |

`low` findings never change the assessment. The posture lens (aggressive / measured /
conservative) can shift a finding's severity; `severity_under_default_posture` keeps that
transparent.

### Coverage sub-check (goal 2, pass-3)

Beyond verbatim/paraphrase checks, pass-3 runs a **coverage sub-check**: walk the
`invention-summary.md` 4-layer core mechanism and the high-priority Quotable spans, and
confirm each core-mechanism layer is addressed somewhere in the draft. A core-mechanism layer
or a spine-critical Quotable span left entirely uncovered is a `high` finding ("specification
under-use"). This is the qualitative complement to the mechanical `gate_figure_use`: gates
catch unused *figures*, the coverage sub-check catches unused *specification*.

## PASS / FAIL (orchestrator loop policy)

```
PASS  ⇔  Layer-1 gates all pass (no fail-severity finding, including FIGUSE-001)
         AND  editorial overall_assessment is acceptable per threshold
         AND  grounding hard-gate not breached
```

- **Threshold (default): `pass`.** The loop accepts only a clean `pass`. `--threshold` may
  relax this to `revise-recommended` (accept medium-only findings) for faster turnaround; it
  may never relax to `revise-required`.
- **Grounding hard-gate:** any `high`/`critical` finding in pass-3 (claim adequacy / fact /
  paraphrase) or any `gate_anchors` fail is an automatic FAIL even if you relaxed the
  threshold — never ship weak or invented grounding (goal 1).
- **Goal-2 hard-gate:** any `FIGUSE-001` (orphan figure) or pass-3 coverage `high` finding is
  an automatic FAIL — figures and spec must actually be used.
- **Goal-3 hard-gate (`investor` audience only):** any `READAB-001` (over the word ceiling) or
  `READAB-002` (inline anchor on the reader-facing surface) is an automatic FAIL — the
  accessible piece must stay finishable and free of patent-ese. Inert for `deep`.
- **Max revision iterations: 4** (`--max-iter`). On FAIL, the orchestrator feeds the
  `findings` back into `essay-en-composer` (revision mode) and re-scores. If still failing at
  the cap, it returns the best round with the remaining findings and the score history.

## Loop ↔ retro hand-off

After the inner loop terminates (PASS or cap), the orchestrator hands the final `edit-log.md`
+ gate result + score history to `pipeline-retro`, which normalizes findings into
`meta/findings-ledger.jsonl` keyed by the goal + owner from the matrix above. See the
`pipeline-retro` skill for the propose-only meta-loop.
