---
proposal_id: 2026-06-09-bold-marker-normalization
created: 2026-06-09T01:00:00Z
status: watch
lever: reference-edit
goal: "1"
root_cause_stage: design
root_cause_artifact: thesis-architect/references/quote-anchor-conventions.md
recurrence_count: 1
confidence: medium
triggering_findings:
  - essay_id: 045-spacex-user-terminal-edge-autonomy, iter: 1, pattern_tag: verbatim-normalization-artifact
---

## Problem (WATCH)

The production run of US 12,647,863 B1 produced one Pass-3 medium: the invention-summary
captured a Quotable span containing a no-space join — "gateway terminals 104and no satellites"
— which originates from the patent.md's `**104**and` bold reference-number marker (the bold
strip removes the marker and glues the number to the following word). The composer quoted the
span verbatim, and Pass-3 flagged the whitespace mismatch against the patent. It was resolved
by converting that clause to a paraphrase.

This is the same family as the deliberately-preserved "deterioriation" patent typo: an
ingestion artifact riding into a verbatim Quotable span. It is **structural, not essay-specific**
— any patent whose source markdown uses `**NNN**word` bold reference numbers can produce it.

## Why WATCH, not recommended-apply

Only one observed instance (one patent). The fix touches Phase-1 extraction discipline, which is
higher blast radius than a one-essay symptom warrants. Confirm on a second bold-marker patent
before applying.

## Candidate change (if it recurs)

`reference-edit` to `thesis-architect/references/quote-anchor-conventions.md`: add a normalization
rule for Quotable span extraction —
1. When a reference-number marker (`**NNN**`) is glued to an adjacent word, normalize to
   `NNN word` (single space) in the stored verbatim_text; OR
2. Flag any Quotable span that contains a `digit+letter` or `letter+digit` join with no
   intervening space as **paraphrase-only**, so Phase 2 cites the anchor without a verbatim quote.

Option 1 is cleaner (keeps the span quotable) but must be applied identically in Phase-3
verification so both sides normalize the same way. Option 2 is safer (never quotes the artifact)
at the cost of one fewer verbatim quote. Recommend option 2 unless a verbatim quote of that exact
span is load-bearing.

## Note

This is the production run's only medium; the dry-run's mediums were a different class
(claim-accuracy-paraphrase). No class has yet reached the cross-essay recurrence threshold (3),
so no proposal is `recommended-apply` this cycle.
