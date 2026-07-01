# Attribution table — finding class → goal + owner stage/artifact + lever

The meta-loop's brain. `pipeline-retro` reads this to route each normalized finding to the
*stage and artifact that should have prevented it*, tag it with the north-star goal it
threatens, and pick the default improvement lever. Human-editable: when a new finding class
appears that isn't covered, add a row (that itself is a small reference-edit proposal).

Voice fencing is encoded here on purpose: Phase-3 voice findings route to
`anti-ai-writing.md` / `deliverable-voice-rules.md` or a Phase-2 voice-canon admission — never
to re-exposing `voice-profile.md` in Phase 3.

| Finding class (pattern_tag) | Source signal | Goal | Owner stage | Owner artifact | Default lever |
|---|---|---|---|---|---|
| `anchor-missing` | gate ANCHOR-001 / pass-3 | 1 | design | thesis-architect invention-summary / quote-anchor-conventions | reference-edit |
| `anchor-malformed` | gate ANCHOR-002 | 1 | compose | essay-en-composer/citation-format.md | reference-edit |
| `paraphrase-accidental-drift` | pass-3 3C | 1 | compose | essay-en-composer/citation-format.md | reference-edit |
| `paraphrase-substantive-change` | pass-3 3C | 1 | compose | execution-boundary.md (Plan⊥Execute) | reference-edit |
| `fact-introduced-beyond-spans` | pass-3 3A | 1 | compose | execution-boundary.md | reference-edit |
| `correlation-causation-drift` | pass-3 3D / pass-4 | 1 | compose | causal-reasoning awareness in section-blueprint | reference-edit |
| `figure-orphan` | gate FIGUSE-001 | 2 | compose | essay-en-composer/figure-rendering.md | reference-edit |
| `figure-offplan` | gate FIGUSE-002 | 2 | design/compose | figure-selection.md ↔ figures-rationale.md sync | reference-edit |
| `spec-undercoverage` | pass-3 coverage sub-check | 2 | design | invention-summary 4-layer / phase2-handoff-notes citation priority | reference-edit |
| `sources-enum-violation` | gate SOURCES-002 / pass-6 6C | 4a | compose | x-articles-format-en.md | reference-edit (or gate-promotion) |
| `sources-subgroup-violation` | gate SOURCES-003 / pass-6 6C | 4a | compose | x-articles-format-en.md | reference-edit |
| `lead-conclusion-weak` | pass-6 6A/6B | 4a | design/compose | thesis-spine arc / section-blueprint closing_directive | reference-edit |
| `conclusion-over-hedge` | SETI catch / pass-6 6G | 4a | design + edit | thesis-spine closing posture + pass-6-lead-conclusion-format.md | reference-edit (or rubric-tuning: posture) |
| `paragraph-eight-sentence-slip` | gate STRUCT-001 vs pass-2C | 3 / 4a | gate | gate_structure.py threshold (>8 vs >=8) | gate-strengthen |
| `publication-hard-wrap` | publish render | 4a | compose | x-articles-format-en.md + strip-pipeline.md | reference-edit + pipeline |
| `figure-cover-undervalued` | SETI catch / design | 2 | design | invention-summary-schema Figure relationships + SKILL Step 9 | reference-edit |
| `figure-composition-tooling-gap` | cover build | 2 / 4a | tooling | tools/ (no figure-sequence helper) | new-tool |
| `section-thesis-misalignment` | pass-4 | 4a | design | thesis-spine spine→section trace | reference-edit |
| `reader-engagement-break` | pass-5 | 3 | compose | mode-spec posture / section-blueprint | rubric-tuning (posture) |
| `redundancy-bloat` | pass-2 | 3 | compose | section-blueprint word_target | reference-edit |
| `banned-word` | gate BANNED-001 / pass-1 1B | 4b | canon | anti-ai-writing.md → banned_terms.txt | gate-promotion |
| `banned-pattern-recurring` | pass-1 1B (judged) | 4b | canon | anti-ai-writing.md | gate-promotion (if mechanically safe) |
| `em-dash` | gate EMDASH-001 / pass-6 6E | 4b | compose | strip-pipeline.md | reference-edit |
| `voice-canon-cadence-drift` | pass-1 1A | 4b | compose | voice-canon entry (weak/missing) | voice-canon-admission |
| `voice-canon-structural-miss` | pass-1 1A | 4b | compose | voice-canon entry + section-blueprint | voice-canon-admission |
| `meta-reader-instruction` | gate META-001 / pass-1 / pass-7 | 4b | canon | anti-ai-writing.md → gate_meta | gate-promotion (done run 045) |
| `lead-thesis-deferral` | pass-6 6A / pass-7 / human-revision | 4a | design/compose | thesis-spine arc / section-blueprint lead block | reference-edit |
| `nonclaim-section-header` | pass-6 / pass-7 / human-revision | 4a | compose | section-blueprint header / x-articles-format-en | reference-edit |
| `jargon-overdepth` | pass-5 / pass-7 / human-revision | 3 | compose | deliverable-voice-rules.md | reference-edit |
| `steelman-absent` | pass-4 / pass-7 / human-revision | 1 | design | thesis-spine adversarial-defense → phase2-handoff-notes | reference-edit |
| `section-stub-imbalance` | gate STUB-001 / pass-5 / pass-7 | 4a | compose | section-blueprint word_target balance | reference-edit |
| `thesis-restatement-redundancy` | pass-2 / pass-7 | 3 | compose | section-blueprint (sub-mechanism of redundancy-bloat) | rubric-tuning |
| `revision-induced-duplication` | gate DUPE-001 / pass-2 | 4b | compose | essay-en-composer revision-mode re-scan | rubric-tuning |
| `venue-ticker-convention` | gate CASH-001 / pass-6 | 4a | compose | x-articles-format-en.md | reference-edit (done run 045) |
| `typography-html-comment-blindspot` | gate EXCLAIM-001 | 4b | gate | _shared/scripts/gate_typography.py (EXCLAIM_RE has no HTML-comment exemption) | gate-promotion (proposal on file 2026-07-01) |
| `header-title-near-duplicate` | pass-1 1A | 4b | compose | essay-en-composer/references/section-blueprint.md (no rule against H1/first-`##` sharing a sentence frame) | reference-edit |

## Recurrence ledger summary (auto-maintained by pipeline-retro)

`pipeline-retro` keeps a running count per class here so a human can see system health at a
glance. Counts are derived from `meta/findings-ledger.jsonl`; do not hand-edit the counts.

| pattern_tag | open | watch | proposed | resolved | escalated | patches applied |
|---|---|---|---|---|---|---|
| `redundancy-bloat` | 0 | 7 | 0 | 0 | 0 | 0 |
| `mobile-paragraph-wall` † | 0 | 6 | 2 | 0 | 0 | 0 |
| `external-fact-universalization` † | 0 | 0 | 3 | 0 | 0 | 0 |
| `fence-canon-verification-gap` † | 0 | 0 | 3 | 0 | 0 | 0 |
| `claim-scope-misattribution` † | 0 | 0 | 2 | 0 | 0 | 0 |
| `figure-token-regex-blindspot` † | 0 | 0 | 2 | 0 | 0 | 0 |
| `paraphrase-hedge-compression` † | 0 | 2 | 0 | 0 | 0 | 0 |
| `revision-induced-band-break` † | 0 | 2 | 0 | 0 | 0 | 0 |
| `sources-entry-template-drift` † | 0 | 2 | 0 | 0 | 0 | 0 |
| `banned-pattern-recurring` | 0 | 1 | 0 | 0 | 0 | 0 |
| `quote-notation-gap` † | 0 | 1 | 0 | 0 | 0 | 0 |
| `claim-vs-spec-citation-conflation` † | 0 | 1 | 0 | 0 | 0 | 0 |
| `figuse-selection-scope-overread` † | 0 | 0 | 4 | 0 | 0 | 0 |
| `source-tier-hedge-posture` † | 0 | 1 | 0 | 0 | 0 | 0 |
| `rule-of-three-warn` † | 0 | 1 | 0 | 0 | 0 | 0 |
| `source-pointer-style-drift` † | 0 | 1 | 0 | 0 | 0 | 0 |
| `figure-panel-context-bleed` † | 0 | 1 | 0 | 0 | 0 | 0 |
| `legal-posture-language-slip` † | 0 | 1 | 0 | 0 | 0 | 0 |
| `jargon-gloss-gap` † | 0 | 2 | 0 | 0 | 0 | 0 |
| `fact-introduced-beyond-spans` | 0 | 1 | 0 | 0 | 0 | 0 |
| `quoted-title-emdash-policy-gap` † | 0 | 1 | 0 | 0 | 0 | 0 |
| `spec-undercoverage` | 0 | 1 | 0 | 0 | 0 | 0 |
| `typography-html-comment-blindspot` (new 2026-07-01) | 0 | 0 | 1 | 0 | 0 | 0 |
| `header-title-near-duplicate` (new 2026-07-01) | 0 | 1 | 0 | 0 | 0 | 0 |

Rows above updated 2026-07-01 for run `001-st-histogram-mechanism`'s contributions only
(`redundancy-bloat`, `mobile-paragraph-wall`, `figuse-selection-scope-overread`,
`jargon-gloss-gap`, `spec-undercoverage`, and the 2 new rows). Every other row in this table
still reflects its state as of run `045-agility-638-last-mile-moat` and has not been
re-tallied against the several runs recorded in the ledger between 045 and this run (e.g.
`2026-06-26-*`, `2026-06-27-*` datasets already visible in `findings-ledger.jsonl`) — this
summary table has drifted out of sync with the ledger for those rows and a full re-tally
across the whole ledger is recommended next time a human is doing table maintenance, not
just an incremental per-run update. Flagged here rather than silently corrected in full,
since a blanket re-tally is a larger edit than this run's scope justifies.

Counts derived from the ledger as of run `045-agility-638-last-mile-moat` (third recorded
run). A class with a proposal on file shows its triggering records under `proposed` (the
proposal file under `meta/improvement-proposals/` lists the triggering finding ids and is the
append-only audit reference).

Cross-essay recurrence (present in 2+/3 essays): `claim-scope-misattribution` (HIGH +
grounding hard-gate breach in runs 1–2 — most damaging class in the system; **did NOT recur in
run 045**, whose grounding/claim pass was clean — the run-045 claim issue was a *citation
notation* mislabel, a different class, see below), `mobile-paragraph-wall` (walls in runs 1–2,
edge-of-band only in run 045), `external-fact-universalization`, `fence-canon-verification-gap`
(escalated low → medium; run-2 resolution field-tested the interrogative-🤔-host fix, no
recurrence in run 045), `redundancy-bloat` (now 3/3 — sanctioned-repetition-layering awareness
again in run 045), `revision-induced-band-break`, `paraphrase-hedge-compression`, and
`figure-token-regex-blindspot` (latent; avoided by convention all runs — recurring mitigation
cost, not failure).

New first-seen classes in run 045 (all `watch`/`proposed`, count 1): **`claim-vs-spec-citation-conflation`**
(the iter-1 MEDIUM — three verbatim CLAIM quotes carried a `[0144]` *spec-paragraph* bracket;
quote TEXT byte-exact, only the attribution LABEL wrong; distinct from `claim-scope-misattribution`,
which is claim *semantics*, and from `quote-notation-gap`, which was a missing "(emphasis added)";
resolved iter-2 by attributing claim quotes by claim in prose + correcting thesis-trace upstream),
**`figuse-selection-scope-overread`** (proposal on file — `gate_figure_use` reads the whole
selection file, so figures in the "Reviewed but NOT selected" section false-count as selected;
one dropped-figure-from-prose away from a spurious goal-2 hard FAIL), `source-tier-hedge-posture`
(a tier-4 source on a hedged non-load-bearing forward pointer — within bounds), and
`rule-of-three-warn` (STRUCT-004 on a factual customer triad — warn-only, behaving as designed).

RECUR_THRESHOLD=3 reached by record count: `external-fact-universalization`,
`fence-canon-verification-gap`, `mobile-paragraph-wall` (proposals on file,
recommended-apply) and `redundancy-bloat` (now at 6, still deliberately HELD at `watch`:
heterogeneous sub-mechanisms — anchor doubling, caption echo, sanctioned-layering awareness,
intensifier tics — no single mechanical rule covers them and the class has never cost a loop
iteration). 6 proposals on file as of 2026-06-24 (5 from `2026-06-11-*.md` + the new
`2026-06-24-figuse-selection-scope.md`). Do not hand-edit the counts.
† = new finding class with no row in the main table above; adding the missing rows is itself
a small reference-edit proposal per this table's header (human decision, still pending from
run 1).

## Self-audit channel — first dataset (origin: self-post-accept)

Run `2026-06-26-us12560948b2-investor-selfaudit` is the first dataset for a third finding
**origin**, alongside `inner-loop` (a pass should have caught it) and `human-post-accept` (only a
human caught it): **`self-post-accept`** — the self-audit loop caught it *adversarially, with no
human in the loop*, after the inner loop returned `pass` and all ten gates were green. Captured
via the same `## delta` channel (`meta/normalize_revision_notes.py --origin self-post-accept`).
This is the empirical answer to "can `/goal` self-check without a human": 15 findings caught and
resolved across three autonomous rounds, convergence verified by a third blind fresh-context pair
that traced two residual off-by-one anchors back to the Phase-1 invention-summary and fixed them at
the source.

Routing for the classes that channel surfaced (added so the ledger records resolve; mirrors the
levers already used for their cousins):

| Finding class (pattern_tag) | Source signal | Goal | Owner stage | Owner artifact | Default lever |
|---|---|---|---|---|---|
| `claim-scope-misattribution` | pass-7 G1 / fresh-context | 1 | design | thesis-architect invention-summary claim-scope map (locked/open/pinned) | reference-edit |
| `legal-posture-language-slip` | pass-7 / fresh-context | 1 | compose | deliverable-voice-rules.md legal register + fact-check-log | reference-edit |
| `prosecution-record-overstatement` | pass-7 G1 / fresh-context | 1 | compose | fact-check-log prosecution-record discipline | reference-edit |
| `figure-caption-scope-deferral` | pass-7 / fresh-context | 2 | compose | caption-roles.md scope-first ordering | reference-edit |
| `anchor-incomplete` | pass-7 G2 / fresh-context | 1 | compose | essay-en-composer/citation-format.md range anchors for multi-paragraph spans | reference-edit |
| `anchor-offbyone` | pass-7 G2 / fresh-context | 1 | design | thesis-architect invention-summary Quotable-spans paragraph labeling | reference-edit (fix at source) |

`nonclaim-section-header`, `lead-thesis-deferral`, `steelman-absent`, `meta-reader-instruction`,
`venue-ticker-convention`, and `revision-induced-duplication` are the run-045 human-revision
classes, now field-tested by the autonomous pass too (caught by `gate_dupe` / pass-7 without a
human). Their rows live with the run-045 dataset. See
`meta/improvement-proposals/2026-06-26-self-audit-origin-and-goal-acceptance.md`.

## Run `001-st-histogram-mechanism` (2026-07-01)

US 2026/0140238 A1, Article 1 of 3 in the STM VL53L9CX series. 3 inner-loop rounds (iter 1
revise-recommended → iter 2 revise-recommended → iter 3 pass), then a dry self-audit round
(0 applied edits — nothing cleared the multi-vote bar).

**`figuse-selection-scope-overread` promoted `watch` → `recommended-apply`** (recurrence_count
1 → 2): this run is the second occurrence the sibling proposal
(`2026-06-24-figuse-selection-scope.md`) predicted verbatim — a `## Selected figures` /
`## Not selected (and why)` sectioned selection file where the dropped figures (FIG. 3-7) are
not echoed in prose, producing 5 real `FIGUSE-001` false fails in every one of the run's 3
rounds (15 false fails total). The orchestrator manually adjudicated goal 2 as clear each
round (the real `## Selected figures` set — FIG. 1, FIG. 2 — has zero orphans). See the
proposal file's 2026-07-01 update block for the full re-verification.

**New class `typography-html-comment-blindspot`** (watch, count 1): `gate_typography.py`'s
`EXCLAIM_RE` exempts Markdown image syntax `![` but not HTML comments `<!--`, so an internal
`<!-- ... -->` process annotation in the draft false-fires `EXCLAIM-001` (hard-fail) on the
comment's opening `!`. Fired in round 1; worked around by deleting the stray comment (a
content-layer fix, not a gate fix). Distinct from `figuse-selection-scope-overread` (different
file, different check) and `figure-token-regex-blindspot` (lettered-panel suffixes, same gate
script but a different regex). Proposal: `2026-07-01-typography-html-comment-blindspot.md`.

**New class `header-title-near-duplicate`** (watch, count 1): the H1 and the first `##`
section header shared the same "[subject] Cannot Time a [X] With a Stopwatch" sentence frame
— a near-verbatim restatement rather than an escalation from title-hook to lead-hook. Resolved
in round 2 (H1 states the paradox, first `##` now states the resolution). Single occurrence;
no proposal filed yet, watching for recurrence. Distinct from `voice-canon-cadence-drift`
(cadence matching against canon exemplars) and from pass-7 check 2 header-as-claim (whether
headers reconstruct the argument on a skim, not whether two adjacent headers duplicate each
other).

**Recurring, matches existing rows (no new class):** `mobile-paragraph-wall` (9 dense
paragraphs in round 1, 1 residual in round 2 — same class as the on-file
`recommended-apply` `2026-06-11-gate-structure-word-wall.md`, now recurrence 8 by record
count); `redundancy-bloat` (the "full histogram" motif recurrence, explicitly judged
sanctioned-layering not filler — same heterogeneous-mechanism class deliberately held at
`watch`, now recurrence 7); `spec-undercoverage` (a `[0004]` spine-trace anchor promised in
`thesis-spine.md` but with no matching Quote-anchor entry in `invention-summary.md` — a
Phase-1 backfill item, logged not papered over, matches this row's existing owner artifact);
`jargon-gloss-gap` (the series-vocabulary "zone = cell" equivalence gap, resolved round 2 —
same mechanism as the existing row, with a series-continuity wrinkle noted in the ledger
record).

**Self-audit calibration data point (does not fit the ledger schema cleanly, flagged for
human judgment):** one self-audit reviewer raised a HIGH-severity claim-scope grounding
finding that did **not** survive the orchestrator's own independent verification against
`input/patent.md` (the reviewer conflated two distinct senses of "full histogram processing
capabilities" in the patent's own vocabulary). Correctly not applied (reviewers split 1-1, no
majority; the orchestrator's direct check refuted rather than confirmed it). Logged as
`self-audit-reviewer-false-positive` (`root_cause_stage: self-audit-process`, not a
design/compose/gate/canon stage) — this is reviewer-precision calibration data, not an essay
defect, and the existing schema's "stage that should have prevented it" framing does not map
cleanly onto "a reviewer's own false-positive rate." Single data point; not a proposal trigger
on its own. Worth tracking as its own dimension if a recurring pattern of claim-scope
false-positives (as opposed to the channel's several *true*-positive catches, e.g.
`anchor-offbyone`, `claim-scope-misattribution` elsewhere in this table) emerges across future
self-audit runs.
