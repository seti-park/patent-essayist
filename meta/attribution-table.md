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

## Recurrence ledger summary (auto-maintained by pipeline-retro)

`pipeline-retro` keeps a running count per class here so a human can see system health at a
glance. Counts are derived from `meta/findings-ledger.jsonl`; do not hand-edit the counts.

| pattern_tag | open | watch | proposed | resolved | escalated | patches applied |
|---|---|---|---|---|---|---|
| `mobile-paragraph-wall` † | 0 | 0 | 4 | 0 | 0 | 0 |
| `external-fact-universalization` † | 0 | 0 | 3 | 0 | 0 | 0 |
| `fence-canon-verification-gap` † | 0 | 0 | 3 | 0 | 0 | 0 |
| `claim-scope-misattribution` † | 0 | 0 | 2 | 0 | 0 | 0 |
| `figure-token-regex-blindspot` † | 0 | 0 | 2 | 0 | 0 | 0 |
| `redundancy-bloat` | 0 | 5 | 0 | 0 | 0 | 0 |
| `paraphrase-hedge-compression` † | 0 | 2 | 0 | 0 | 0 | 0 |
| `revision-induced-band-break` † | 0 | 2 | 0 | 0 | 0 | 0 |
| `sources-entry-template-drift` † | 0 | 2 | 0 | 0 | 0 | 0 |
| `banned-pattern-recurring` | 0 | 1 | 0 | 0 | 0 | 0 |
| `quote-notation-gap` † | 0 | 1 | 0 | 0 | 0 | 0 |
| `source-pointer-style-drift` † | 0 | 1 | 0 | 0 | 0 | 0 |
| `figure-panel-context-bleed` † | 0 | 1 | 0 | 0 | 0 | 0 |
| `legal-posture-language-slip` † | 0 | 1 | 0 | 0 | 0 | 0 |
| `jargon-gloss-gap` † | 0 | 1 | 0 | 0 | 0 | 0 |
| `fact-introduced-beyond-spans` | 0 | 1 | 0 | 0 | 0 | 0 |
| `quoted-title-emdash-policy-gap` † | 0 | 1 | 0 | 0 | 0 | 0 |

Counts derived from the ledger as of run `2026-06-11-us20260158546a1-both-and-steel` (second
recorded run; cross-run recurrence is now measurable). A class with a proposal on file shows
all its records under `proposed` (the proposal file under `meta/improvement-proposals/` lists
the triggering finding ids and is the append-only audit reference).

Cross-essay recurrence (present in 2/2 essays): `claim-scope-misattribution` (HIGH +
grounding hard-gate breach both runs — most damaging class in the system),
`mobile-paragraph-wall` (medium walls both runs, gate-invisible to sentence-counting
STRUCT-001), `external-fact-universalization`, `fence-canon-verification-gap` (escalated
low → medium; run-2 resolution field-tested the interrogative-🤔-host fix),
`redundancy-bloat`, `revision-induced-band-break`, `paraphrase-hedge-compression`, and
`figure-token-regex-blindspot` (latent; avoided by trap-3 convention both runs — counted as
recurring mitigation cost, not failure).

RECUR_THRESHOLD=3 reached by record count: `external-fact-universalization`,
`fence-canon-verification-gap`, `mobile-paragraph-wall` (proposals on file,
recommended-apply) and `redundancy-bloat` (deliberately HELD at `watch`: all five records
low-severity, heterogeneous sub-mechanisms — anchor doubling, caption echo, layering
awareness, two intensifier tics — no single mechanical rule covers them and the class has
never cost a loop iteration). 5 proposals on file as of 2026-06-11; see
`meta/improvement-proposals/2026-06-11-*.md`. Do not hand-edit the counts.
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
