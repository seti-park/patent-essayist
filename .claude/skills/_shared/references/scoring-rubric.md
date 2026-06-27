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
| **3. Easy for the reader to understand** | `gate_structure`, `gate_stub`, `gate_meta` (warn-only smells) | pass-5 reader-perspective + **pass-7 adversarial reader** | mode/posture calibration, section-blueprint lead-altitude |
| **4a. Well-structured** | `gate_structure`, `gate_stub`, `gate_cashtag` | pass-6 lead/conclusion + format (BLUF + header-as-claim) | section-blueprint, x-articles-format-en, thesis arc |
| **4b. Natural (not AI-tell)** | `gate_banned`, `gate_emdash`, `gate_meta`, `gate_dupe` | pass-1 voice + anti-ai | voice-on drafting + anti-ai canon + strip-pipeline |

When `pipeline-retro` records a finding, it tags it with the goal it threatens and the owner
artifact, so improvement proposals target the true root cause rather than the symptom.

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
| `meta`       | `META-001` (reader-instruction / self-reference) | `META-002` | 4b, 3 |
| `stub`       | (none — all warn) | `STUB-001` (section stub) | 4a, 3 |
| `cashtag`    | (none — all warn) | `CASH-001` (bare ticker) | 4a |
| `dupe`       | (none — all warn) | `DUPE-001` (verbatim repeat) | 4b, 3 |

The last four are the **run-045 self-check gates** — the mechanical half of the editorial
blind-spots a human used to catch by hand in post-acceptance revision (see
`meta/improvement-proposals/2026-06-26-human-revision-blindspots.md`). `gate_meta` hard-fails;
the rest warn. Their judgment complement is **pass-7** (below).

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

### Adversarial reader-pass (pass-7, goal 3/4a)

A fresh-context pass that does NOT trust the draft (the judgment complement of the self-check
gates). It simulates the target reader (the impatient investor) and a skeptical pro-subject
reader, and hunts — decomposed yes/no with a quoted span per check, multi-vote for fuzzy items
— for: BLUF lead-altitude (does para 1 state the verdict?), header-as-claim, an unrebutted
strongest counter (steelman absent), reader-instruction / self-reference meta, jargon deep-dive
past the insight, stub-section rhythm, and the core verdict restated in > 3 sections. See
`editorial-review/references/pass-7-adversarial-reader.md`. Findings feed the severity model
like any other pass.

### Richer goal strings (`/goal` as quality driver)

`/goal` can drive the loop to self-enforce more than "gates pass + assessment == pass": pass it
the acceptance criteria as falsifiable, evidence-forced checks and the orchestrator self-audits
each iteration. Example: `/goal the final passes all gates AND a fresh-eyes adversarial
reader-pass returns no unresolved high findings (para-1 states the verdict; headers are claims;
the strongest counter is rebutted; no reader-instruction meta; jargon as signposts; no stub
section)`. As criteria get mechanized into gates, reliance on the judge shrinks.

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
- **Max revision iterations: 4** (`--max-iter`). On FAIL, the orchestrator feeds the
  `findings` back into `essay-en-composer` (revision mode) and re-scores. If still failing at
  the cap, it returns the best round with the remaining findings and the score history.

## Layer 3 — Post-acceptance self-audit (autonomous)

The inner loop and gates can return `pass` and still leave the editorial + grounding blind-spots a
fresh reader catches. Layer 3 is a **post-acceptance** stage the orchestrator runs after the inner
loop passes (`--self-audit on`, default): ≥2 reviewers in **separate forked contexts** run the
`editorial-review/references/pass-7-adversarial-reader.md` checklist + grounding spot-checks, and
their multi-voted findings are applied autonomously and logged via the revision-delta channel.

Reliability comes from HOW, not just WHAT — the mechanisms the inner loop cannot apply to itself:
fresh context (no commitment to the draft), decomposed evidence-forced checks (quoted span or
`ABSENT`), persona diversity + multi-vote, fix-at-source for upstream causes, and loop-until-dry.
It can only **raise** the bar — never relax a gate or a pass, and the grounding + goal-2 hard-gates
hold every round.

**Acceptance set (enforceable as a `/goal`):**

```
the patent-essay run is self-audited: after the inner loop returns pass with all gates green, a
fresh-context adversarial pass (>=2 reviewers, pass-7 personas, separate context) returns no
unresolved high or medium finding, the grounding hard-gate holds, and a second blind pass confirms
convergence; applied deltas are logged via revision-notes.md (origin: self-post-accept).
```

## Loop ↔ retro hand-off

After the inner loop terminates (PASS or cap) and the post-acceptance self-audit (Layer 3) runs,
the orchestrator hands the final `edit-log.md` + gate result + score history + the self-audit's
`revision-notes.md` to `pipeline-retro`, which normalizes findings into
`meta/findings-ledger.jsonl` keyed by the goal + owner from the matrix above. Self-audit deltas
carry `origin: self-post-accept` (vs the inner loop's `inner-loop` and the human channel's
`human-post-accept`), so recurrence is scored over the dimension no pass yet gates. See the
`pipeline-retro` skill for the propose-only meta-loop.
