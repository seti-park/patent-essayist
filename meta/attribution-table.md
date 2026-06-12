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
| `redundancy-bloat` | 0 | 6 | 0 | 0 | 0 | 0 |
| `mobile-paragraph-wall` † | 0 | 0 | 5 | 0 | 0 | 0 |
| `external-fact-universalization` † | 0 | 0 | 4 | 0 | 0 | 0 |
| `fence-canon-verification-gap` † | 0 | 0 | 4 | 0 | 0 | 0 |
| `sources-entry-template-drift` † | 0 | 0 | 4 | 0 | 0 | 0 |
| `claim-scope-misattribution` † | 0 | 0 | 3 | 0 | 0 | 0 |
| `paraphrase-hedge-compression` † | 0 | 0 | 3 | 0 | 0 | 0 |
| `figure-token-regex-blindspot` † | 0 | 0 | 2 | 0 | 0 | 0 |
| `revision-induced-band-break` † | 0 | 2 | 0 | 0 | 0 | 0 |
| `banned-pattern-recurring` | 0 | 2 | 0 | 0 | 0 | 0 |
| `quote-notation-gap` † | 0 | 2 | 0 | 0 | 0 | 0 |
| `source-pointer-style-drift` † | 0 | 1 | 0 | 0 | 0 | 0 |
| `figure-panel-context-bleed` † | 0 | 1 | 0 | 0 | 0 | 0 |
| `legal-posture-language-slip` † | 0 | 1 | 0 | 0 | 0 | 0 |
| `jargon-gloss-gap` † | 0 | 1 | 0 | 0 | 0 | 0 |
| `fact-introduced-beyond-spans` | 0 | 1 | 0 | 0 | 0 | 0 |
| `quoted-title-emdash-policy-gap` † | 0 | 1 | 0 | 0 | 0 | 0 |
| `claim-anchor-mechanism-gap` † | 0 | 1 | 0 | 0 | 0 | 0 |
| `title-conclusion-stance-mismatch` † | 0 | 1 | 0 | 0 | 0 | 0 |
| `caption-voice-rule-bypass` † | 0 | 1 | 0 | 0 | 0 | 0 |
| `gate-selection-scope-overharvest` † | 0 | 0 | 0 | 1 | 0 | 1 |

Counts derived from the ledger as of run `tesla-washer-pump-two-wire-moat` (third recorded
run). A class with a proposal on file shows all its records under `proposed` (the proposal
file under `meta/improvement-proposals/` lists the triggering finding ids and is the
append-only audit reference).

Cross-essay recurrence (present in 3/3 essays): `claim-scope-misattribution` (HIGH in two of
three runs, grounding hard-gate breach class, one loop iteration cost per run — still the most
damaging class in the system; run 3 added the spec-to-claims direction, EL-01),
`mobile-paragraph-wall` (5th record), `external-fact-universalization` (4th),
`fence-canon-verification-gap` (4th; the interrogative-🤔-host fix field-tested again in run-3
round 2), `paraphrase-hedge-compression` (3rd — threshold reached run 3), `redundancy-bloat`
(6th). 2/3 essays: `sources-entry-template-drift` (but 4 records, two of them in run 3 where
the EL-03 fix itself introduced R2-01 — template root cause confirmed), `quote-notation-gap`,
`banned-pattern-recurring` (now two distinct density clusters: contrast pairs, triads).

RECUR_THRESHOLD=3 reached by record count: `external-fact-universalization`,
`fence-canon-verification-gap`, `mobile-paragraph-wall` (2026-06-11 proposals,
recommended-apply, still pending human application — patches applied remains 0, so run-3
recurrence of these classes is expected, not evidence of an ineffective patch);
newly at/over threshold in run 3: `sources-entry-template-drift` and
`paraphrase-hedge-compression` (new recommended-apply proposals 2026-06-12) and
`claim-scope-misattribution` (promotion proposal 2026-06-12 lifts the 2026-06-11 lock-map
proposal from watch to recommended-apply). `redundancy-bloat` remains deliberately HELD at
`watch` (six low-severity records, heterogeneous sub-mechanisms, never cost a loop
iteration). One run-3 gate defect, `gate-selection-scope-overharvest` (FIGUSE-001 false fail
on the template-schema Not-selected table), was fixed mid-run by the orchestrator (commit
a980562, tests + regression pass) — recorded as `resolved` with 1 patch applied; a watch
proposal adds the missing `meta/fixtures/` lock. 9 proposals on file as of 2026-06-12; see
`meta/improvement-proposals/2026-06-1*.md`. Do not hand-edit the counts.
† = new finding class with no row in the main table above; adding the missing rows is itself
a small reference-edit proposal per this table's header (human decision, still pending since
run 1; four more † classes added in run 3).
