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

## Recurrence ledger summary (auto-maintained by pipeline-retro)

`pipeline-retro` keeps a running count per class here so a human can see system health at a
glance. Counts are derived from `meta/findings-ledger.jsonl`; do not hand-edit the counts.

| pattern_tag | open | watch | proposed | resolved | escalated | patches applied |
|---|---|---|---|---|---|---|
| `redundancy-bloat` | 0 | 8 | 0 | 0 | 0 | 0 |
| `mobile-paragraph-wall` † | 0 | 8 | 2 | 0 | 0 | 0 |
| `external-fact-universalization` † | 0 | 0 | 3 | 0 | 0 | 0 |
| `fence-canon-verification-gap` † | 0 | 0 | 3 | 0 | 0 | 0 |
| `claim-scope-misattribution` † | 0 | 0 | 2 | 0 | 0 | 0 |
| `figure-token-regex-blindspot` † | 0 | 0 | 2 | 0 | 0 | 0 |
| `paraphrase-hedge-compression` † | 0 | 2 | 0 | 0 | 0 | 0 |
| `revision-induced-band-break` † | 0 | 2 | 0 | 0 | 0 | 0 |
| `sources-entry-template-drift` † | 0 | 6 | 0 | 0 | 0 | 0 |
| `banned-pattern-recurring` | 0 | 1 | 0 | 0 | 0 | 0 |
| `quote-notation-gap` † | 0 | 1 | 0 | 0 | 0 | 0 |
| `claim-vs-spec-citation-conflation` † | 0 | 0 | 2 | 0 | 0 | 0 |
| `figuse-selection-scope-overread` † | 0 | 0 | 1 | 0 | 0 | 0 |
| `source-tier-hedge-posture` † | 0 | 1 | 0 | 0 | 0 | 0 |
| `rule-of-three-warn` † | 0 | 1 | 0 | 0 | 0 | 0 |
| `source-pointer-style-drift` † | 0 | 1 | 0 | 0 | 0 | 0 |
| `figure-panel-context-bleed` † | 0 | 1 | 0 | 0 | 0 | 0 |
| `legal-posture-language-slip` † | 0 | 1 | 0 | 0 | 0 | 0 |
| `jargon-gloss-gap` † | 0 | 1 | 0 | 0 | 0 | 0 |
| `fact-introduced-beyond-spans` | 0 | 1 | 0 | 0 | 0 | 0 |
| `quoted-title-emdash-policy-gap` † | 0 | 1 | 0 | 0 | 0 | 0 |
| `thesis-restatement-redundancy` | 0 | 3 | 0 | 0 | 0 | 0 |
| `anchor-malformed` | 0 | 2 | 0 | 0 | 0 | 0 |
| `paraphrase-substantive-change` | 0 | 2 | 0 | 0 | 0 | 0 |
| `closing-scope-overreach` † | 0 | 1 | 0 | 0 | 0 | 0 |
| `quote-fidelity-gap` † | 0 | 1 | 0 | 0 | 0 | 0 |
| `figure-mechanism-oversimplification` † | 0 | 1 | 0 | 0 | 0 | 0 |

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

### Update — run `2026-07-01-us20230356397b2-cliff-histogram-bridge`

Row counts above (`redundancy-bloat` 8, `mobile-paragraph-wall` 8 watch + 2 proposed,
`sources-entry-template-drift` 6, `claim-vs-spec-citation-conflation` moved to 2 under
`proposed` now that a proposal file exists for the class, plus new rows
`thesis-restatement-redundancy` 3, `anchor-malformed` 2, `paraphrase-substantive-change` 2,
`closing-scope-overreach` 1, `quote-fidelity-gap` 1, `figure-mechanism-oversimplification` 1)
reflect this run's 13 inner-loop records + its pre-existing 5 self-post-accept records, added by
`pipeline-retro`. Only rows this run's records touch were recomputed from the full ledger; other
rows above (e.g. `claim-scope-misattribution`, `external-fact-universalization`) were not
touched by this run and were left at their prior values, which are already known to lag the
ledger by several intervening runs (`2026-06-26-*`, `2026-06-27-*`) not yet reconciled here — a
full-table recount is a separate, larger task than this run's retro warrants.

**`claim-vs-spec-citation-conflation` is now at 2 total occurrences** (run
`045-agility-638-last-mile-moat` iter 1, `inner-loop`/editorial + this run,
`self-post-accept`/self-audit) — below `RECUR_THRESHOLD` (3). Held at `watch`, not promoted.
See `meta/improvement-proposals/2026-07-01-claim-vs-spec-citation-conflation-watch.md` for the
explicit watch record and the applied-in-advance recommendation (run 045's own logged
recommendation already states the fix; both occurrences self-corrected without needing it
applied, but a 3rd occurrence should auto-promote).

**Within-run recurrence signal:** this run's `mobile-paragraph-wall` recurred 4 times *within
its own inner loop* (iter 1→2→3→4) before resolving at the iteration cap — see the "Within-run
recurrence" section above. This does not change the cross-run recurrence count differently than
a normal 4-record addition would, but it is additional, sharper evidence for the already-on-file
`2026-06-11-gate-structure-word-wall.md` proposal (`recommended-apply`): the gate gap is now
shown to cost iterations within a single essay, not just to recur across essays.
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

## Within-run recurrence — a distinct signal from cross-run recurrence

`2026-07-01-us20230356397b2-cliff-histogram-bridge` recurred `mobile-paragraph-wall` 4 times
*within its own inner loop* (iter 1 -> 2 -> 3 -> 4, shrinking magnitude each round, only
resolving at the iteration cap). This is the same `pattern_tag` as the existing cross-run
`mobile-paragraph-wall` class (see the main table row above and the recurrence ledger below —
counted together, not double-tracked under a second tag), but the *within-one-essay* shape of
the recurrence is itself a signal distinct from cross-essay recurrence: a single essay needing
3 revision rounds to clear one finding class, even though it converged before the cap, means the
mechanical gate gap (`gate_structure.py` counts sentences, not words) cost this run 3 full
Compose<->Edit iterations it should not have needed. This sharpens (does not replace) the
existing `mobile-paragraph-wall` proposal record: the word-count gate gap is not just a
gate-invisibility problem across essays, it is now demonstrated to be an iteration-cost problem
within a single essay. See `meta/improvement-proposals/2026-06-11-gate-structure-word-wall.md`
(already `recommended-apply`) — this run is additional evidence for that same on-file proposal,
not a new class or a new proposal.
