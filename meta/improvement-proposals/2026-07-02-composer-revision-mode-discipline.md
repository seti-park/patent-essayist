---
proposal_id: 2026-07-02-composer-revision-mode-discipline
created: 2026-07-02T00:00:00Z
status: applied (2026-07-02, user-sponsored, regression-gated)
lever: reference-edit
goal: "4b"
root_cause_stage: compose
root_cause_artifact: essay-en-composer/SKILL.md (no revision-mode contract — the word "revision" does not appear in it, yet the orchestrator invokes the skill "in revision mode" every loop round)
recurrence_count: 5
confidence: high
triggering_findings:
  - essay_id: 045-agility-638-last-mile-moat, iter: v2.1, pattern_tag: revision-induced-duplication
  - essay_id: 045-agility-638-last-mile-moat, iter: v2.3, pattern_tag: revision-induced-duplication
  - essay_id: 2026-06-10-us12636684b1-deleted-dome, iter: 2, pattern_tag: revision-induced-band-break
  - essay_id: 2026-06-11-us20260158546a1-both-and-steel, iter: 2, pattern_tag: revision-induced-band-break
  - essay_id: (audience feedback, multi-iteration published outputs), pattern_tag: conclusion-over-hedge — reader-reported over-conservative register on heavily-looped essays (SETI, 2026-07-02)
---

> **Update 2026-07-02 — applied verbatim** (the "Revision mode (loop rounds ≥ 2)" section
> inserted into `essay-en-composer/SKILL.md` between "Process (7 steps)" and "Plan ⊥ Execute
> boundary", exactly as filed), same-day, on SETI's go-ahead following the reader-feedback
> discussion. Success criteria to watch on the next multi-round run are in the Regression
> expectation below.

## Problem

The orchestrator's quality loop says: "Feed the `edit-log.md` findings back to
`essay-en-composer` in **revision mode** — it revises `handoff/02-compose/` in place." But
`essay-en-composer/SKILL.md` defines no revision mode at all. Every loop round after the first
is therefore an UNCONSTRAINED rewrite opportunity: the composer may touch any sentence, flagged
or not, and there is no rule saying what must survive a revision byte-identical.

Three observed failure channels flow through this hole:

1. **Revision introduces new defects.** `revision-induced-duplication` (3 ledger records, 2
   essays): a round-1 steelman fix produced a 5-gram echo of the verdict section, caught only
   by `gate_dupe` on re-run; a round-2 rewrite left a near-verbatim within-section echo.
   `revision-induced-band-break` (2 records): splitting one over-long paragraph pushed a
   neighbor to exactly 8 sentences, invisible to the then-gate, caught by manual re-count.
2. **Iteration cost.** `2026-07-01-us20230356397b2-cliff-histogram-bridge` spent 3 of its 4
   inner-loop rounds re-fixing `mobile-paragraph-wall` — each revision pass reshaped prose
   broadly enough to keep re-triggering the class ("shrinking magnitude each round").
3. **Register drift (the invisible channel).** Reader feedback (2026-07-02, via SETI):
   heavily-looped essays read "too safe / dispute-avoidant" for investment-diligence readers.
   Passes 3/4 push claims down every round; with no rule freezing UNFLAGGED prose, each
   revision round may quietly re-hedge sentences no finding named. Nothing currently measures
   or forbids this (companion instrumentation:
   `2026-07-02-posture-softening-ledger-tag.md`).

## Proposed change (exact diff)

**File: `.claude/skills/essay-en-composer/SKILL.md`** — add a new section immediately after
"## Process (7 steps)":

```markdown
## Revision mode (loop rounds ≥ 2)

When invoked with edit-log findings / failing gate check_ids (the orchestrator's revision
step), the composer is a SURGEON, not a re-drafter:

- **Touch only named spans.** Edit exactly the spans a finding or failing check names, plus
  the minimal surrounding wording a fix forces. Every unflagged sentence survives the round
  byte-identical.
- **No new hedges on unflagged prose.** Never add qualifiers, soften verbs, demote definite
  articles, or downgrade the declared closing posture on sentences no finding named. The
  loop's Pass 3/4 findings push claims down where evidence demands it; revision mode must not
  amplify that into register-wide drift (reader-reported failure mode on multi-iteration
  essays). Grounding fixes state exactly what the finding requires — no prophylactic hedging
  around them.
- **Re-scan the blast radius.** After editing, re-check the touched section(s) for
  (a) self-echo against the rest of the essay (the `gate_dupe` classes:
  revision-induced-duplication) and (b) the paragraph band — a split or merge can push a
  NEIGHBOR paragraph over the sentence/word band (revision-induced-band-break); re-count
  every paragraph in any structurally edited section.
- **Log the delta.** End the revision with a one-line-per-edit list (span → finding id) so
  Edit and the self-audit can verify nothing outside the findings moved.
```

## Why this lever

- The gap is a missing procedural contract in the exact file the orchestrator invokes; a
  reference-edit lands the rule where the behavior happens. Not gate-promotion: "did an
  unflagged sentence get softer" is not mechanically decidable (the companion ledger-tag
  proposal makes it *observable* instead).
- The surgical-scope rule mirrors the discipline the self-audit layer already enforces on
  itself ("surgical-fix scope", split/taste findings not forced in) — this extends the same
  brake to the inner loop, where most rounds happen.
- Directly reduces the iteration bill: rounds that only touch named spans cannot re-trigger
  unrelated classes, so `--max-iter` budget goes to real findings.

## Regression expectation

Documentation-only. `python .claude/skills/_shared/scripts/test_gates.py`,
`python meta/regression.py` unchanged green. Success criteria on the next multi-round run:
zero `revision-induced-*` findings; unflagged prose diff between iter N and iter 1 is empty
(spot-checkable from the logged delta); no new hedges outside finding spans.
