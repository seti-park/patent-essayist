---
proposal_id: 2026-06-11-external-fact-scope-discipline
created: 2026-06-11T16:30:00Z
updated: 2026-06-20T17:40:00Z
status: recommended-apply
lever: reference-edit
goal: "1"
root_cause_stage: compose
root_cause_artifact: essay-en-composer/references/execution-boundary.md (external-fact scope discipline)
recurrence_count: 4
confidence: high
triggering_findings:
  - essay_id: 2026-06-10-us12636684b1-deleted-dome, iter: 1, pattern_tag: external-fact-universalization
  - essay_id: 2026-06-10-us12636684b1-deleted-dome, iter: 2, pattern_tag: external-fact-universalization
  - essay_id: 2026-06-11-us20260158546a1-both-and-steel, iter: 1, pattern_tag: external-fact-universalization
  - essay_id: 2026-06-20-us12430274b2-processor-on-nand-moat, iter: 1, pattern_tag: uncited-external-claim
---

> **2026-06-20 refresh (run `274-processor-on-nand-moat`).** A fourth record, and the
> **most severe instance to date**: a `high` Pass-3B finding (sole driver of the round-1
> revise-required) where §4 asserted the patent "belongs to a family with related pending
> cases" — an external claim with **no fact-check-log Fact ID and no `# Sources` entry**.
> This is the **strongest form** of the class: not over-broadening a *logged* fact (the
> three prior `external-fact-universalization` records) but asserting an **unlogged**
> external fact outright. The proposed diff already covers it (the "Is the fact in
> facts_locked? → If no, stop" line), so this run **corroborates** the existing fix and
> lifts confidence `medium` → `high`. Tagged `uncited-external-claim` in the ledger to keep
> the sub-mechanism distinct; same root artifact and same lever.

## Problem

Prose makes an **external (non-patent) factual claim the fact-check-log does not support** —
either by over-broadening a *logged* fact, or (run 3) by asserting an *unlogged* one. 4 ledger
records, 3 distinct instances, **3 of 3 essays** (goal 1, accuracy):

- Run 1 (medium → low residue): "the industry sprays its covers" universalized from the
  dlhBowles nozzle facts, whose logged scope also covers spraying a bare lens; the verified
  invariant was non-contact cleaning, not cover-as-universal. Editor recommendation,
  verbatim: *"Tie external-fact prose scope to the fact-check-log entry's literal scope;
  assert a universal only when the log states one."*
- Run 2 (medium, F2): EOS maraging steel "sold for exactly this kind of work" stretched the
  logged fact (`eos-ms1-18ni300-aging`: "typical applications **include** injection-molding
  tools and inserts") into a universal fit. Fixed by naming the logged scope explicitly.
- **Run 3 (HIGH, Pass-3B, `uncited-external-claim`):** §4 asserted the patent "belongs to a
  family with related pending cases", load-bearing for the moat-**strength** argument — with
  **no fact-check-log Fact ID and no `# Sources` entry**. The sister cases (US 18/608,695,
  US 18/933,962) came from `essay-context.md` and were never pulled/verified (per
  `phase2-handoff-notes` "Sister cases"). This is the same root pathology — *prose claims
  more than the log supports* — at its limit: zero logged scope. It also dragged a Pass-4
  causal inference (family-depth → durable moat) onto an unverified premise. Resolved by
  **removing** the assertion and re-grounding strength on the patent's own two independent
  claims (a patent-internal fact). This was the sole driver of the round-1 `revise-required`.

`execution-boundary.md` already locks **which** facts may be used (`facts_locked`) but says
nothing about the **scope** of prose built on them, nor does it spell out that a claim with no
`facts_locked` entry *and* no `# Sources` entry is a hard stop — the recurring gap is prose
asserting more than the log supports, which no gate can see.

Record count 4 ≥ RECUR_THRESHOLD, cross-essay 3/3, now reaching `high` → `recommended-apply`,
confidence lifted to `high` (3 distinct instances, the latest a grounding hard-gate breach).

## Proposed change (exact diff)

**File: `.claude/skills/essay-en-composer/references/execution-boundary.md`** — extend the
"Quick reference" per-sentence checklist:

```diff
 Before composing each sentence:
 - Is this a factual claim? → Cite [^fact-id] from facts_locked
 - Is the fact in facts_locked? → If no, stop. Gap detected.
+- Is it an EXTERNAL (non-patent) fact? → Two checks:
+  (1) Existence: the claim must trace to a fact-check-log Fact ID AND appear in `# Sources`.
+      A claim with neither is a hard stop — never assert the existence/status of an external
+      thing (a patent family, a pending sister case, a product, a competitor) from
+      essay-context.md or background knowledge that was not pulled and logged this run; if it
+      is load-bearing, either log+source it or re-ground the point on patent-internal facts.
+  (2) Scope: prose scope must not exceed the logged entry's literal scope. Assert a universal
+      ("the industry…", "sold for exactly this…") only when the log entry states one; if the
+      log says "include"/"typical"/"can also", name the logged scope explicitly instead of
+      universalizing it. Titles and closing aphorisms may compress a scoped fact only when
+      the precise scoped statement appears in nearby body prose (deliberate-compression
+      allowance, on the record).
 - Is this transition/interpretation prose? → No citation needed, but no new facts either
```

## Why this lever

- Root cause is a compose-stage procedural gap, and `execution-boundary.md` is the artifact
  the composer is required to check sentence-by-sentence — the rule lands exactly where the
  failure happens. All three editors' fixes were applications of this same checklist.
- Not gate-promotion: both checks require reading the log — existence ("is there a Fact ID?")
  and scope semantics ("include" vs "is"); a regex would be all false positives.
- The title/aphorism allowance clause encodes run-1's iter-2 adjudication (compression
  backed by precise nearby prose was accepted as deliberate), so the rule doesn't outlaw a
  pattern the editor already sanctioned. The run-3 existence check is the more important half:
  the over-broadening sub-mechanism cost only mediums, but the unlogged-existence
  sub-mechanism cost a `high` and a full revision round.
- **CASCADE note:** this class has **0 patches applied** (it has only ever been proposed). The
  4 records pre-date any fix, so this is not an ineffective-patch situation. The cascade clock
  starts only if a *distinct* instance recurs **after** this diff is applied — at which point
  reconsider whether the gap is procedural (reference) or needs a Phase-1 fact-pull policy.

## Regression expectation

Documentation-only change. `python .claude/skills/_shared/scripts/test_gates.py` and
`python meta/regression.py` unchanged green (no script or fixture touched) — **confirmed at
the 2026-06-20 baseline** (`REGRESSION: PASS`). Success criterion: zero pass-3 external-fact
existence-or-scope findings in the next run; a distinct instance *after applying* would start
the `ineffective-patch` / CASCADE_CAP clock for this class.
