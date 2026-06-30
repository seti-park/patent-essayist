---
proposal_id: 2026-06-30-compose-grounding-precision-guards
created: 2026-06-30T00:00:00Z
status: watch
lever: reference-edit
goal: "1"
root_cause_stage: compose
root_cause_artifact: essay-en-composer/references/citation-format.md + essay-en-composer/references/section-blueprint.md
recurrence_count: 2   # two strong first-seen mechanism-level grounding-precision classes this run; family (goal-1 grounding) is 10+ across the ledger
confidence: medium
triggering_findings:
  - essay_id: 002-vl53l9cx-crosstalk-robustness, iter: post-accept, pattern_tag: mechanism-gloss-contradicts-quote, origin: self-post-accept
  - essay_id: 002-vl53l9cx-crosstalk-robustness, iter: post-accept, pattern_tag: cross-patent-mechanism-conflation, origin: self-post-accept
  - essay_id: 002-vl53l9cx-crosstalk-robustness, iter: post-accept, pattern_tag: caveat-not-grounded-in-source, origin: self-post-accept
  - essay_id: 002-vl53l9cx-crosstalk-robustness, iter: post-accept, pattern_tag: marketing-line-overbinding, origin: self-post-accept
family_evidence:   # the goal-1 grounding-precision super-class these are mechanism-level cousins of
  - pattern_tag: claim-scope-misattribution (6 records, runs 2026-06-10/11/24/26/27, 045 — most damaging class in the system)
  - pattern_tag: claim-vs-spec-citation-conflation (run 045, citation-format.md owner)
  - pattern_tag: prosecution-record-overstatement (self-audit channel)
  - pattern_tag: external-fact-universalization (3 records)
---

## Problem

The 002 self-audit (origin: `self-post-accept`) caught four grounding-precision defects that
the inner-loop `pass` survived with all gates green and only `low` editorial findings. They are
all the same family — **the connective gloss drifts from, or over-binds, the very source it
sits next to** — and that family (goal 1, accurate capture) is the most recurring and most
damaging in the ledger (`claim-scope-misattribution` x6, `claim-vs-spec-citation-conflation`,
`prosecution-record-overstatement`, `external-fact-universalization` x3).

Two of the four are genuinely new failure *shapes* worth hardening against:

1. **`mechanism-gloss-contradicts-quote`** — the compose draft glossed [0052]'s band
   classification as a sign rule ("negative score -> ghost"), one sentence before quoting
   [0052], which makes a *strongly negative* sum the FIRST type. The gloss contradicted the
   anchor it cited. This is distinct from paraphrase drift (the *quote* was byte-exact); the
   surrounding prose restated the quoted rule in a simpler-but-wrong logical form (band ->
   sign).

2. **`cross-patent-mechanism-conflation`** — with a hero + support patent sharing a beat, the
   draft's "It Subtracts..." header/body attributed the SUPPORT patent's scale-and-subtract
   mechanism to the HERO, which only classifies-and-rejects. A mechanism verb migrated across
   patents.

The other two (`caveat-not-grounded-in-source` — a "package leakage counts as cross-talk"
caveat [0029] does not support; `marketing-line-overbinding` — a multi-patent ST line bound to
the single hero) are the same root reflex (asserting grounding the source does not give) and
are recorded as supporting evidence.

These are blind-spots the inner loop cannot see by construction: the *anchor* is valid and
byte-exact, so `gate_anchors` and pass-3's string match pass; the defect is in the *logical
relationship* between gloss and anchor, which only an adversarial reader rereads against the
raw spec. They warrant a composer-side guard so fewer reach the self-audit.

## Proposed change (exact diff)

Two reference-edits in Phase-2 Compose. Both are procedural rules with no mechanical false-positive
surface, so reference-edit (not gate-promotion) is correct.

### A. `essay-en-composer/references/citation-format.md` — gloss-must-match-anchor logical form

Add under "## What does NOT need citation" (new subsection):

```markdown
## The gloss must restate the anchor in the same logical form

When a sentence quotes or cites an `[xxxx]` anchor, the surrounding gloss must restate the
anchored rule in the SAME logical form — do not simplify a threshold / band / multi-step rule
into a sign or binary.

- If the anchor states a **band** ("first type if WS > Pthresh OR < Nthresh; second type if
  between"), the gloss says "outside a band" / "inside a band" — NOT "negative -> ghost".
  (002: a strongly negative sum is the FIRST type, so the sign gloss contradicted the [0052]
  quote one sentence later.)
- If the anchor states a **threshold**, name the threshold, not "high/low".
- If the anchor is a **multi-step** procedure, the gloss must not collapse it to one step.
- Self-check: read the gloss and the quoted anchor back to back. If a reader who believed the
  gloss would mis-predict the quoted rule on any input, the gloss is wrong — rewrite it, do not
  re-quote.

A caveat or aside that asserts patent grounding ("the patent counts X as Y too") must cite the
span that says so. If no span says it, drop the grounding claim or attribute it to its real
source. (002: a "package leakage counts as cross-talk" caveat was not in [0029], which says
"cover glass reflection, or housing reflection".)
```

### B. `essay-en-composer/references/section-blueprint.md` — hero-vs-support verb attribution

Add to the "## Lead altitude, section headers, and balance" bullet list (after "No stub
sections."):

```markdown
- **Reserve mechanism verbs to the patent that performs them.** When the hero and a support
  patent share a beat, name which patent each mechanism verb belongs to; do not let a support
  patent's verb migrate onto the hero (or vice versa) in a header or body sentence. (002: the
  hero CLASSIFIES-AND-REJECTS second-type peaks; literal scale-and-SUBTRACT is the support
  patent — the "It Subtracts..." header imported the support mechanism onto the hero.)
- **A multi-patent external line binds to the family, not the single hero.** When a marketing /
  press line spans the whole filing family, attribute it to "one of the patents" / the family,
  not "the patent behind that line". (002: ST's compensation line spans hero classify-and-reject
  AND support scale-and-subtract.)
```

## Why this lever

- **reference-edit, not gate-promotion.** All four defects are *semantic relationships* between
  prose and a valid anchor — there is no literal/regex that flags "band restated as sign" or "a
  support verb on the hero" without unacceptable false positives. The composer is the stage that
  writes the gloss and chooses the verb; citation-format.md and section-blueprint.md already own
  exactly these decisions (citation-format owns quote/anchor discipline; section-blueprint owns
  headers and the run-045 hand-revision defaults). This extends the run-045 precedent.
- **Why not edit a gate.** `gate_anchors` already passes here (anchors valid, quotes byte-exact)
  — the defect is invisible to it by construction. Promoting to a gate would be a false-confidence
  patch.
- **Why now / why one proposal.** Each new class is count-1 (individually `watch`), so this is a
  `watch` proposal, not `recommended-apply`. But the *family* (goal-1 grounding-precision) is the
  ledger's most recurrent and damaging, and the gloss-contradicts-quote shape is novel and high-
  severity (a self-contradiction). Bundling the two composer guards (A + B) under one goal-1
  proposal mirrors how the run-045 hand-revision defaults were bundled. A human can apply A and B
  independently.

## Regression expectation

- `python meta/regression.py` and `python .claude/skills/_shared/scripts/test_gates.py` must
  stay green — this proposal touches only two `references/*.md` (no gate script, no
  `banned_terms.txt`), so no gate test should change.
- Reference-only edits have no fixture under `meta/fixtures/` to flip; the regression guard's job
  here is to confirm no gate behavior moved. If a future run records a third grounding-precision
  mechanism class, promote this proposal to `recommended-apply` and add a `meta/fixtures/` case
  pairing a band-anchor with a sign-gloss draft (must be flagged by pass-3/pass-7 after the edit).
