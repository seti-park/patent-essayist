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
| `sources-category-omitted` † | pass-6 6C | 4a | compose | x-articles-format-en.md (Sources category checklist — no explicit "every analyzed patent must appear under a category" completeness rule) | reference-edit |

## Recurrence ledger summary (auto-maintained by pipeline-retro)

`pipeline-retro` keeps a running count per class here so a human can see system health at a
glance. Counts are derived from `meta/findings-ledger.jsonl`; do not hand-edit the counts.

| pattern_tag | open | watch | proposed | resolved | escalated | patches applied |
|---|---|---|---|---|---|---|
| `redundancy-bloat` | 0 | 9 | 0 | 0 | 0 | 0 |
| `mobile-paragraph-wall` † | 0 | 1 | 4 | 0 | 0 | 0 |
| `external-fact-universalization` † | 0 | 0 | 3 | 0 | 0 | 0 |
| `fence-canon-verification-gap` † | 0 | 0 | 3 | 0 | 0 | 0 |
| `claim-scope-misattribution` † | 0 | 0 | 2 | 0 | 0 | 0 |
| `figure-token-regex-blindspot` † | 0 | 0 | 2 | 0 | 0 | 0 |
| `paraphrase-hedge-compression` † | 0 | 2 | 0 | 0 | 0 | 0 |
| `revision-induced-band-break` † | 0 | 2 | 0 | 0 | 0 | 0 |
| `sources-entry-template-drift` † | 0 | 0 | 4 | 0 | 0 | 0 |
| `banned-pattern-recurring` | 0 | 1 | 0 | 0 | 0 | 0 |
| `quote-notation-gap` † | 0 | 1 | 0 | 0 | 0 | 0 |
| `claim-vs-spec-citation-conflation` † | 0 | 1 | 0 | 0 | 0 | 0 |
| `figuse-selection-scope-overread` † | 0 | 0 | 0 | 0 | 0 | 1 |
| `source-tier-hedge-posture` † | 0 | 1 | 0 | 0 | 0 | 0 |
| `rule-of-three-warn` † | 0 | 1 | 0 | 0 | 0 | 0 |
| `source-pointer-style-drift` † | 0 | 1 | 0 | 0 | 0 | 0 |
| `figure-panel-context-bleed` † | 0 | 1 | 0 | 0 | 0 | 0 |
| `legal-posture-language-slip` † | 0 | 1 | 0 | 0 | 0 | 0 |
| `jargon-gloss-gap` † | 0 | 1 | 0 | 0 | 0 | 0 |
| `fact-introduced-beyond-spans` | 0 | 1 | 0 | 0 | 0 | 0 |
| `quoted-title-emdash-policy-gap` † | 0 | 1 | 0 | 0 | 0 | 0 |
| `meta-reader-instruction` | 0 | 3 | 0 | 0 | 0 | 1 |
| `sources-category-omitted` † | 0 | 1 | 0 | 0 | 0 | 0 |

Counts derived from the ledger as of run `vl53l9cx-ep2-crosstalk-us20240192337` (sixth recorded
run, following `045-agility-638-last-mile-moat`, `2026-06-26-us12560948b2-investor-selfaudit`,
and `2026-06-27-us12560948b2-safe-stop-e2e`). A class with a proposal on file shows its
triggering records under `proposed` (the proposal file under `meta/improvement-proposals/` lists
the triggering finding ids and is the append-only audit reference).

**Staleness note (2026-07-01):** the two intervening runs (`...-investor-selfaudit` and
`...-safe-stop-e2e`) added self-audit and inner-loop records for several classes — notably
`claim-scope-misattribution`, `legal-posture-language-slip`, and the `mobile-paragraph-wall` /
`proposed` split — whose numeric rows above were not refreshed at the time (this pipeline-retro
pass corrected only the rows its own new records directly touch: `redundancy-bloat` and
`sources-entry-template-drift`, plus the two brand-new tags). A full recount pass across all six
runs is still owed; flagging here rather than silently rewriting rows this run has no fresh
evidence for.

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

New first-seen class in `vl53l9cx-ep2-crosstalk-us20240192337` (2026-07-01, inner-loop iter-1
HIGH — the sole driver of that iteration's `revise-required`): **`sources-category-omitted`** —
the `# Sources` block carried only `## Official statements` and `## Technical specs`
subheadings; neither analyzed patent (subject US 2024-0192337 B2, supporting US 2025-0012901)
appeared under a `## Patents` category at all, despite both being cited in-body. Distinct from
the table's two existing Sources-structure classes: `sources-enum-violation` is a *wrong label*
(an ad-hoc category name outside the 5-item enum) and `sources-subgroup-violation` is
*inconsistent subgrouping* (some sources categorized, others not, once `##` is in use) — this is
a *whole required category silently absent* despite in-body use, which neither existing check
tests for. First occurrence, count 1, filed `watch`; needs the human-added attribution-table row
above (marked †) confirmed/refined once a second instance appears. Resolved iter-2 (`## Patents`
added, ordered first, both patents in 6-field format).

This run's `redundancy-bloat` instance (iter-1 MEDIUM, §6 3-idea paragraph) is a **new
sub-mechanism**, not a repeat of a prior flavor: each of the three stacked ideas individually
honored its own word-budget instruction, but the paragraph-level combination pushed past the
single-idea earn threshold — a *budget-per-idea vs. budget-per-paragraph* gap, distinct from the
class's previously observed flavors (word-level doubling, header/body echo, sanctioned
cross-section layering, intensifier tics). Still folded into the umbrella `redundancy-bloat` tag
per the class's existing heterogeneous-sub-mechanisms handling (see below), not split out, since
it is a single low-frequency instance of yet another sub-mechanism rather than a stable new
pattern on its own.

This run's `sources-entry-template-drift` instance (iter-2 LOW — "filed" used instead of the
spec's "priority" label; hero-patent publication date omitted with no placeholder) is the 4th
occurrence of the class and crosses `RECUR_THRESHOLD`. Unlike the prior three occurrences (all
`watch`, no proposal on file), this run's evidence — combined with the prior three — supports a
`recommended-apply` reference-edit: see
`meta/improvement-proposals/2026-07-01-sources-entry-field-completeness.md` (fixes both the
Patents field-4/5 label-locking and unstated-field placeholder convention, and the adjacent
Papers author/venue-unstated convention that drove the first two occurrences).

This run's `meta-reader-instruction` instance (iter-1 LOW, FIG. 1 caption "this essay starts
from...") is the 3rd ledger occurrence of the tag but **does not** warrant a new proposal: unlike
the prior two occurrences (both confirmed violations that were removed), this one was judged
*borderline* and ultimately ruled an exempted functional-scope-disclaimer, not a violation —
`gate_meta` (already gate-promoted in run 045, see the main table above) correctly did not fire.
This is the mechanism working as designed at the judgment layer, complementing rather than
exposing a gap in the mechanical gate; no action proposed.

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
