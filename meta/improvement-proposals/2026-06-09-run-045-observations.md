---
proposal_id: 2026-06-09-run-045-observations
created: 2026-06-09T00:00:00Z
status: watch
lever: reference-edit
goal: "1"
root_cause_stage: compose
root_cause_artifact: essay-en-composer/references/citation-format.md
recurrence_count: 2
confidence: low
triggering_findings:
  - essay_id: 045-spacex-user-terminal-edge-autonomy, iter: 1, pattern_tag: claim-accuracy-paraphrase
  - essay_id: 045-spacex-user-terminal-edge-autonomy, iter: 1, pattern_tag: claim-accuracy-paraphrase
---

## Problem (WATCH — not yet actionable)

Essay 045 produced two pass-3 medium findings of the same class (`claim-accuracy-paraphrase`),
both in Compose: a non-quoted paraphrase that subtly misstated the *relationship* between
correctly-cited facts.

- §1 framed the outage and the patent as the *same* failure mode (they are the same *kind*:
  latency `[0005]` vs unavailability).
- §4 inverted the patent's detection *hierarchy* (called the 10 Hz ping primary; `[0094]`
  makes the protocol counters primary).

Both were resolved in iteration 2. The verbatim quotes themselves were always exact — the drift
was in surrounding paraphrase that asserts ordering/scope the source does not.

## Why WATCH, not recommended-apply

This is 2 instances in a single essay — below the cross-essay recurrence threshold (3). One
essay is not enough signal to edit a reference. If a second essay shows the same class, promote
to `recommended-apply`.

## Candidate change (if it recurs)

`reference-edit` to `essay-en-composer/references/citation-format.md`: add a rule that when a
paraphrase asserts an *ordering, hierarchy, primacy, or same/different* relationship between
cited facts, the composer must re-check the source's own stated ordering/scope before writing
it (verbatim quotes alone do not guarantee the paraphrase's relational claim is faithful).

## Note — gate improvements already applied this run (audit trail)

Run 045 also surfaced two real gate gaps, fixed directly (human-applied, with tests + green
`meta/regression.py`), since they were unambiguous and mechanically safe — not held as
proposals:
1. Sub-figure letter tokens (1A/1B/5B) in `gate_figure_use` + `gate_anchors` (commits
   5c2249a / fed6acf).
2. `gate_figure_use` scoping the selected set to the "## Selected figures" section + stripping
   HTML comments (commit 5c2249a).

These validate the `gate-promotion` lever end-to-end: a real patent exercised the gates, the
gaps were caught, fixed, and regression-guarded.
