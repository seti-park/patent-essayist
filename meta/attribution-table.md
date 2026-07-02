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
| `typography-html-comment-blindspot` | gate EXCLAIM-001 | 4b | gate | _shared/scripts/gate_typography.py (EXCLAIM_RE has no HTML-comment exemption) | gate-promotion (applied 2026-07-02) |
| `header-title-near-duplicate` | pass-1 1A | 4b | compose | essay-en-composer/references/section-blueprint.md (no rule against H1/first-`##` sharing a sentence frame) | reference-edit |
| `sources-category-omitted` † | pass-6 6C | 4a | compose | x-articles-format-en.md (Sources category checklist — no explicit "every analyzed patent must appear under a category" completeness rule) | reference-edit |

## Recurrence ledger summary (derived — do not hand-edit)

The table between the markers below is GENERATED from `meta/findings-ledger.jsonl` plus the
proposal frontmatter by `python meta/tally_ledger.py --write`. It replaces the hand-maintained
per-run recount that repeatedly drifted (each 2026-07-01 run independently flagged "a full
re-tally is owed") and that guaranteed merge conflicts between parallel sessions.
`meta/regression.py` fails while the block is stale, so merging a run branch or applying a
proposal forces a regeneration. Class-STATE judgment (hold-at-watch decisions, promotion
rationale, applied-fix narratives) lives in the proposal files and `meta/run-notes/`, not here.

<!-- tally:begin — generated by `python meta/tally_ledger.py --write`; do not hand-edit -->

| pattern_tag | records | essays | gate | editorial | self-audit | human-rev | retro | proposals |
|---|---|---|---|---|---|---|---|---|
| `mobile-paragraph-wall` | 12 | 6 |  | 12 |  |  |  | `2026-06-11-gate-structure-word-wall` (applied) |
| `redundancy-bloat` | 10 | 6 |  | 10 |  |  |  | — |
| `sources-entry-template-drift` | 8 | 4 |  | 7 |  | 1 |  | `2026-07-01-sources-entry-field-completeness` (applied) |
| `external-fact-universalization` | 5 | 3 |  | 3 | 2 |  |  | `2026-06-11-external-fact-scope-discipline` (applied) |
| `claim-scope-misattribution` | 4 | 4 |  | 3 | 1 |  |  | `2026-06-11-claim-scope-lock-map` (watch) |
| `figuse-selection-scope-overread` | 4 | 2 | 4 |  |  |  |  | `2026-06-24-figuse-selection-scope` (applied) |
| `anchor-offbyone` | 3 | 2 |  |  | 3 |  |  | — |
| `fence-canon-verification-gap` | 3 | 2 |  | 3 |  |  |  | `2026-06-11-emoji-host-fence-decidable` (applied) |
| `figure-token-regex-blindspot` | 3 | 3 | 2 |  |  |  | 1 | `2026-06-11-figure-token-panel-suffix` (watch) |
| `meta-reader-instruction` | 3 | 3 |  | 1 | 1 | 1 |  | — |
| `revision-induced-duplication` | 3 | 2 |  |  | 2 | 1 |  | — |
| `thesis-restatement-redundancy` | 3 | 3 |  | 1 | 1 | 1 |  | — |
| `anchor-incomplete` | 2 | 1 |  |  | 2 |  |  | — |
| `anchor-malformed` | 2 | 1 |  | 2 |  |  |  | — |
| `claim-vs-spec-citation-conflation` | 2 | 2 |  | 1 | 1 |  |  | `2026-07-01-claim-vs-spec-citation-conflation-watch` (applied) |
| `jargon-gloss-gap` | 2 | 2 |  | 2 |  |  |  | — |
| `lead-thesis-deferral` | 2 | 2 |  |  | 1 | 1 |  | — |
| `legal-posture-language-slip` | 2 | 2 |  | 1 | 1 |  |  | — |
| `nonclaim-section-header` | 2 | 2 |  |  | 1 | 1 |  | — |
| `paragraph-eight-sentence-slip` | 2 | 2 |  | 1 |  |  | 1 | `2026-06-26-gate-structure-sentence-band-align` (applied) |
| `paraphrase-hedge-compression` | 2 | 2 |  | 2 |  |  |  | — |
| `paraphrase-substantive-change` | 2 | 1 |  | 1 | 1 |  |  | — |
| `revision-induced-band-break` | 2 | 2 |  | 2 |  |  |  | — |
| `steelman-absent` | 2 | 2 |  |  | 1 | 1 |  | — |
| `venue-ticker-convention` | 2 | 2 |  |  | 1 | 1 |  | — |
| `banned-pattern-recurring` | 1 | 1 |  | 1 |  |  |  | — |
| `closing-scope-overreach` | 1 | 1 |  |  | 1 |  |  | — |
| `conclusion-over-hedge` | 1 | 1 |  | 1 |  |  |  | `2026-06-24-conclusion-over-hedge-check` (watch) |
| `fact-introduced-beyond-spans` | 1 | 1 |  | 1 |  |  |  | — |
| `figure-caption-scope-deferral` | 1 | 1 |  |  | 1 |  |  | — |
| `figure-composition-tooling-gap` | 1 | 1 |  |  |  |  | 1 | — |
| `figure-cover-undervalued` | 1 | 1 |  |  |  |  | 1 | `2026-06-26-figure-selection-cover-and-phase` (watch) |
| `figure-mechanism-oversimplification` | 1 | 1 |  |  | 1 |  |  | — |
| `figure-panel-context-bleed` | 1 | 1 |  | 1 |  |  |  | — |
| `figure-rendering-mode-inconsistency` | 1 | 1 |  |  |  | 1 |  | — |
| `gate-clean-run` | 1 | 1 |  | 1 |  |  |  | — |
| `header-title-near-duplicate` | 1 | 1 |  | 1 |  |  |  | — |
| `jargon-overdepth` | 1 | 1 |  |  |  | 1 |  | — |
| `prosecution-record-overstatement` | 1 | 1 |  |  | 1 |  |  | — |
| `publication-hard-wrap` | 1 | 1 |  |  |  |  | 1 | `2026-06-26-publication-line-wrap` (applied) |
| `quote-fidelity-gap` | 1 | 1 |  |  | 1 |  |  | — |
| `quote-notation-gap` | 1 | 1 |  | 1 |  |  |  | — |
| `quoted-title-emdash-policy-gap` | 1 | 1 |  | 1 |  |  |  | — |
| `rule-of-three-warn` | 1 | 1 | 1 |  |  |  |  | — |
| `section-stub-imbalance` | 1 | 1 |  |  |  | 1 |  | — |
| `self-audit-reviewer-false-positive` | 1 | 1 |  |  | 1 |  |  | — |
| `source-pointer-style-drift` | 1 | 1 |  | 1 |  |  |  | — |
| `source-tier-hedge-posture` | 1 | 1 |  | 1 |  |  |  | — |
| `sources-category-omitted` | 1 | 1 |  | 1 |  |  |  | — |
| `spec-undercoverage` | 1 | 1 |  | 1 |  |  |  | — |
| `typography-html-comment-blindspot` | 1 | 1 | 1 |  |  |  |  | `2026-07-01-typography-html-comment-blindspot` (applied) |

Derived from 139 ledger records (113 tagged + 26 untagged coverage/no-finding records) across 10 runs, and 15 proposal files. Do not hand-edit: regenerate with `python meta/tally_ledger.py --write`; `meta/regression.py` fails while this block is stale. Proposal statuses come from each proposal file's frontmatter (`watch` / `recommended-apply` / `applied` / `escalated`).
<!-- tally:end -->

## Per-run retro notes

Run-scoped narrative (what each run surfaced, judgment calls, promotion updates) is written to
`meta/run-notes/<essay-id>.md` — one file per run, so parallel Claude Code sessions never
conflict on this shared file. This table keeps only durable class knowledge: the routing
tables and the derived tally.

## Historical dataset notes (through the 2026-07-01 runs)

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
**`figuse-selection-scope-overread`** (proposal `2026-06-24-figuse-selection-scope.md` — status
now `applied`: the predicted failure fired for real on `vl53l9cx-ep2-crosstalk-us20240192337`
(6 spurious `FIGUSE-001`), and the fix applied there turned out to need a superset of the
original diff — HTML-comment stripping, not just section-scoping, since the template's own
rejected-figure rationale lives in an HTML comment rather than a separate heading; see the
proposal file's 2026-07-01 update for the full comparison), `source-tier-hedge-posture`
(a tier-4 source on a hedged non-load-bearing forward pointer — within bounds), and
`rule-of-three-warn` (STRUCT-004 on a factual customer triad — warn-only, behaving as designed).

RECUR_THRESHOLD=3 reached by record count: `external-fact-universalization`,
`fence-canon-verification-gap`, `mobile-paragraph-wall` (proposals on file,
recommended-apply), `sources-entry-template-drift` (now at 4, **new** `recommended-apply`
proposal as of 2026-07-01 — see above), `meta-reader-instruction` (now at 3, no new proposal —
already gate-promoted, this run's instance is a correctly-behaving judgment-layer complement,
not a gap), and `redundancy-bloat` (now at 9, still deliberately HELD at `watch`: heterogeneous
sub-mechanisms — anchor doubling, caption echo, sanctioned-layering awareness, intensifier tics,
and now budget-per-idea-vs-per-paragraph stacking — no single mechanical rule covers them and
the class has never cost a loop iteration). 7 proposals on file as of 2026-07-01 (5 from
`2026-06-11-*.md` + `2026-06-24-figuse-selection-scope.md` +
`2026-07-01-sources-entry-field-completeness.md`). Do not hand-edit the counts.

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

## Self-audit channel — second dataset (run `2026-07-01-us20230356397b2-cliff-histogram-bridge`)

Three new first-seen classes surfaced by this essay's self-audit (`origin: self-post-accept`),
added here per this table's header rule (a new finding class gets a row when first seen):

| Finding class (pattern_tag) | Source signal | Goal | Owner stage | Owner artifact | Default lever |
|---|---|---|---|---|---|
| `closing-scope-overreach` | pass-7 / fresh-context self-audit | 1 | design | thesis-spine adversarial-defense steelman-refine scope (closing-paragraph proportionality) | reference-edit |
| `quote-fidelity-gap` | pass-3 / fresh-context self-audit (live-source check) | 1 | design | fact-check-log / essay-context.md external-quote transcription discipline | reference-edit |
| `figure-mechanism-oversimplification` | pass-3 coverage / fresh-context self-audit | 2 | compose | caption-roles.md + essay-en-composer figure-description fidelity (multi-signal mechanisms) | reference-edit |

Notes on routing judgment: `closing-scope-overreach` is distinct from `conclusion-over-hedge`
(that is under-claiming/hedging; this is a closing sentence implying a broader architectural
dependency than the patent supports — tentatively routed to goal 1 grounding-proportionality per
the reviewer's own framing in the ledger record, not goal 4a format). `quote-fidelity-gap` is
distinct from `paraphrase-accidental-drift` and `paraphrase-substantive-change` (those are
patent-source paraphrase drift; this is an external, non-patent verbatim quote — a blog-post
title — losing a word somewhere upstream of Phase 2, traced to essay-context.md's own
transcription). `figure-mechanism-oversimplification` is distinct from `figure-orphan` /
`figure-offplan` (those are gate-visible use/selection mismatches; this is a judgment-level
fidelity gap where a correctly-used, correctly-selected figure's underlying mechanism is
described with an incorrect generalization across its sub-signals).
