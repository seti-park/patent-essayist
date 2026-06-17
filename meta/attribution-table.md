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
| `sources-entry-template-drift` | pass-6 6D (author form / bibliographic template; gate-invisible) | 4a | compose | x-articles-format-en.md (Sources per-item citation format) | reference-edit |
| `lead-conclusion-weak` | pass-6 6A/6B | 4a | design/compose | thesis-spine arc / section-blueprint closing_directive | reference-edit |
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
| `sources-entry-template-drift` | 0 | 0 | 3 | 0 | 0 | 0 |
| `banned-pattern-recurring` | 0 | 1 | 0 | 1 | 0 | 0 |
| `reader-engagement-break` | 0 | 0 | 0 | 2 | 0 | 0 |
| `quote-notation-gap` † | 0 | 1 | 0 | 0 | 0 | 0 |
| `source-pointer-style-drift` † | 0 | 1 | 0 | 0 | 0 | 0 |
| `figure-panel-context-bleed` † | 0 | 1 | 0 | 0 | 0 | 0 |
| `legal-posture-language-slip` † | 0 | 1 | 0 | 0 | 0 | 0 |
| `jargon-gloss-gap` † | 0 | 1 | 0 | 0 | 0 | 0 |
| `fact-introduced-beyond-spans` | 0 | 1 | 0 | 0 | 0 | 0 |
| `quoted-title-emdash-policy-gap` † | 0 | 1 | 0 | 0 | 0 | 0 |

Counts derived from the ledger as of run `045-sandisk-hbf-flash-training` (third recorded run;
a single clean run — iter-1 revise-recommended → iter-2 pass — with both mediums resolved
in-loop, so it adds mostly resolved/empty-pass records and one newly-threshold class). A class
with a proposal on file shows all its records under `proposed` (the proposal file under
`meta/improvement-proposals/` lists the triggering finding ids and is the append-only audit
reference). Records resolved inside the inner loop are counted under `resolved`.

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
recommended-apply); `sources-entry-template-drift` (newly reached at run 045: 2 watch from
run 2 + run-045's Pass-6D "Hu, et al." → "Hu, Edward J., et al." correction → proposal on
file `meta/improvement-proposals/2026-06-17-sources-author-form-rule.md`, recommended-apply,
confidence medium — root cause is x-articles-format-en.md line 58 itself stating the wrong
"First, et al." form; gate-invisible, corrected by Pass 6 in 2 of the last 3 essays); and
`redundancy-bloat` (deliberately HELD at `watch`: all five records low-severity, heterogeneous
sub-mechanisms — anchor doubling, caption echo, layering awareness, two intensifier tics — no
single mechanical rule covers them and the class has never cost a loop iteration). Below
threshold and HELD at `watch`: `reader-engagement-break` (2 records, both run 045, both
resolved in-loop — the §4 means-plus-function gloss medium + a low secondary-jargon variant;
adjoins run-2 `jargon-gloss-gap` at 1, both gloss-at-first-use of the most load-bearing term;
watch the combined gloss-discipline class) and `banned-pattern-recurring` (2: run-1 contrast-
pair cluster + run-045 semicolon-joined-clauses, both judged defensible, resolved). 6 proposals
on file as of 2026-06-17 (5 from 2026-06-11 + this run's `2026-06-17-sources-author-form-rule`).
Do not hand-edit the counts.
† = new finding class with no row in the main table above; adding the missing rows is itself
a small reference-edit proposal per this table's header (human decision, still pending from
run 1). `sources-entry-template-drift` lost its † at run 045 — a mapping row was added under
the `sources-*` block (citation author-form, 6D), per this table header's allowance to add a
row when a new finding class reaches the table.
