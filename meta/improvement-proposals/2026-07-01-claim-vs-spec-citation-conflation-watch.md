---
proposal_id: 2026-07-01-claim-vs-spec-citation-conflation-watch
created: 2026-07-01T11:00:00Z
status: watch
lever: reference-edit
goal: "1"
root_cause_stage: compose
root_cause_artifact: essay-en-composer/references/citation-format.md (claim-language vs spec-paragraph attribution convention) + thesis-architect invention-summary Quote-anchor table (claim-sourced vs spec-sourced marking)
recurrence_count: 2
confidence: medium
triggering_findings:
  - essay_id: 045-agility-638-last-mile-moat, iter: 1, pattern_tag: claim-vs-spec-citation-conflation
  - essay_id: 2026-07-01-us20230356397b2-cliff-histogram-bridge, iter: null (self-post-accept, round 1), pattern_tag: claim-vs-spec-citation-conflation
---

## Problem

The same defect shape has now occurred in **2 of roughly 6-7 recorded essay runs**: verbatim
**claim** language is cited or paraphrased as if it came from a specification paragraph, either
by carrying a `[dddd]` spec-paragraph bracket on claim text (run 045) or by asserting a
paragraph "quotes Claim 1 exactly as filed" when the quoted text is actually the specification
summary paragraph, missing the claim's own limitation (this run). Both times the quote TEXT
integrity was never at risk (byte-exact where quoted) — only the **attribution label**
(claim-sourced vs spec-sourced) was wrong, and both times the mislabel was invisible to every
deterministic gate (`gate_anchors` only checks that a `[dddd]` bracket is well-formed and
in-index; it cannot know whether the adjacent prose's claim-number assertion matches the
anchor's actual source layer).

- **Run 045** (`045-agility-638-last-mile-moat`, iter 1, `inner-loop`/editorial, MEDIUM): three
  verbatim CLAIM quotes (q-clm1-1, q-clm1-2, q-clm17-1) carried a `[0144]` spec-paragraph
  bracket. Caught by pass-3 paraphrase-mutation-judgment. Resolved iter 2 by removing the
  brackets and attributing the quotes by claim number in prose.
- **This run** (`2026-07-01-us20230356397b2-cliff-histogram-bridge`, `self-post-accept`, round
  1): the essay's central "quote Claim 1 exactly as filed" sentence was actually the
  specification-summary paragraph `[0005]`, missing Claim 1's own disjunctive
  "identifying a convergence..." limitation; a second, redundant reference to that exact phrase
  was also cited to `[0005]`, which does not contain it. Caught independently by two fresh-context
  self-audit reviewers approaching from different angles (one checking the phrase against
  `[0005]`, the other checking claim 1 as granted against the quoted text). Not caught by the
  inner loop's own pass-3 in this run — this occurrence surfaced only in the post-acceptance
  self-audit layer, one layer later than run 045's occurrence.

**Recurrence count is 2, below `RECUR_THRESHOLD` (3).** Per the promotion rules in
`references/proposal-format.md`, this stays at `status: watch` — it does **not** auto-promote to
`recommended-apply` on this run. This proposal exists so the exact fix is on file and a human
can apply it early (the class is goal-1 grounding-adjacent and has now cost one inner-loop
iteration and one self-audit round across two different essays), or so a third occurrence
auto-promotes this file without re-deriving the diagnosis from scratch.

Confidence is `medium` rather than `high` (contrast
`2026-06-11-claim-scope-lock-map.md`, filed at `high` on a 2/2 cross-essay HIGH grounding
breach): both occurrences of this class self-corrected without cost to the run's overall
`pass` outcome, and the second occurrence was caught by the self-audit layer rather than the
inner loop, so the loop-cost signal is milder than a repeated HIGH.

## Proposed change (exact diff)

Carried forward, largely verbatim, from run 045's own logged `recommendation` in
`meta/findings-ledger.jsonl` (essay_id `045-agility-638-last-mile-moat`, pattern_tag
`claim-vs-spec-citation-conflation`) — that occurrence already correctly diagnosed the fix; this
proposal packages it as an applyable diff now that a second, independent occurrence corroborates
the diagnosis.

**File 1: `.claude/skills/essay-en-composer/references/citation-format.md`** — add an explicit
claim-vs-spec attribution rule (exact insertion point depends on the file's current section
structure; insert as a new subsection near the existing anchor-format rules):

```markdown
### Claim language vs specification-paragraph attribution

Verbatim **claim** language (independent or dependent claim text) is attributed by claim number
in prose — "Claim 1 states...", "claim 17 covers..." — **never** by a `[dddd]`
specification-paragraph bracket. `[dddd]` brackets are reserved for specification paragraphs.

Before citing any quote as claim language, verify the quoted text actually appears in the named
claim (not the specification's summary/background paragraph describing the same limitation in
different words, and not the Abstract). A specification paragraph that restates a claim
limitation in its own words is a paraphrase of the claim, not the claim itself, and must not be
quoted as if it were the granted claim text.

If the invention-summary's Quote-anchor table marks a span as spec-sourced, do not upgrade it to
"the claim, quoted exactly as filed" in composed prose even if the wording is similar to the
claim; either quote the claim itself (re-extracting it from the patent's claims section) or keep
the spec-paragraph attribution and description-level framing.
```

**File 2: `.claude/skills/thesis-architect/references/invention-summary-schema.md`** (or the
file governing the Quote-anchor table's column spec) — add a `Source layer` column to the
Quote-anchor / Quotable-spans table:

```markdown
| Quote id | Text | Anchor | Source layer (claim / spec) |
|---|---|---|---|
| q-clm1-1 | "..." | claim 1 | claim |
| q-0005-1 | "..." | [0005] | spec |
```

Rule: every Quotable span must be marked `claim` or `spec` at extraction time, when the patent
text is in hand and the distinction is cheapest to get right. Compose must carry this marking
into `thesis-trace.md`'s anchor map unchanged; a `claim`-marked span may never acquire a `[dddd]`
bracket downstream, and a `spec`-marked span may never be narrated as "the claim... exactly as
filed" downstream.

## Why this lever

- The defect is a **procedural gap at the citation-convention level**, not a mechanically
  detectable pattern (a gate cannot know, from a `[dddd]` bracket alone, whether the adjacent
  prose's claim-number assertion is true — that requires reading the claim and the paragraph and
  comparing). `reference-edit` is the correct lever; `gate-promotion` is not viable without a
  high false-positive/false-negative rate.
- Fixing it at the **source** (marking claim-vs-spec at Phase-1 extraction time, in
  `invention-summary.md`) is cheaper than relying on Phase-2/Phase-3 catching the mislabel after
  the fact — this mirrors the fix pattern already used for `anchor-offbyone` (fixed upstream in
  the Quotable-spans table so a recompose cannot reintroduce it) and
  `claim-scope-misattribution`'s locked/open/pinned map.
- Not `voice-canon-admission` or `rubric-tuning`: this is not a voice or calibration issue, it is
  a factual-attribution discipline gap.

## Regression expectation

Documentation-only change (two Markdown reference files; no script, no banned list, no fixture
input touched). After applying:

- `python .claude/skills/_shared/scripts/test_gates.py` — all tests pass, unchanged (no gate
  reads either file).
- `python meta/regression.py` — all fixtures produce identical verdicts.
- Observable success criterion for future runs: `invention-summary.md`'s Quote-anchor table
  carries a `Source layer` column for every Quotable span; `thesis-trace.md` inherits it
  unchanged; zero further `claim-vs-spec-citation-conflation` findings at any origin
  (`inner-loop` or `self-post-accept`). A third occurrence, if it happens before this proposal is
  applied, should auto-promote this file's `status` to `recommended-apply` rather than opening a
  fresh proposal.
