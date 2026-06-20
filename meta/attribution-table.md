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

| pattern_tag | total records | essays | worst severity | proposal status | patches applied |
|---|---|---|---|---|---|
| `mobile-paragraph-wall` † | 8 | 3 | high | recommended-apply (`gate-structure-word-wall`) | 0 |
| `redundancy-bloat` | 7 | 3 | low | none — HELD at watch (heterogeneous) | 0 |
| `figure-token-regex-blindspot` † | 3 | 3 | warn (fired×3 in run 3) | recommended-apply (`figure-token-panel-suffix`) | 0 |
| `external-fact-universalization` † (+`uncited-external-claim`) | 3 (+2) | 3 | high | recommended-apply (`external-fact-scope-discipline`) | 0 |
| `banned-pattern-recurring` | 3 | 2 | low | none — HELD at watch (heterogeneous) | 0 |
| `fence-canon-verification-gap` † | 3 | 2 | medium | recommended-apply (`emoji-host-fence-decidable`) | 0 |
| `revision-induced-band-break` † | 3 | 3 | low | watch (`paragraph-length-joint-spec`, HELD) | 0 |
| `claim-scope-misattribution` † | 2 | 2 | high | watch (`claim-scope-lock-map`) | 0 |
| `uncited-external-claim` † | 2 | 1 | high | rolled into `external-fact-scope-discipline` | 0 |
| `correlation-causation-drift` | 2 | 1 | medium | none (dependency of `uncited-external-claim`) | 0 |
| `paraphrase-hedge-compression` † | 2 | 2 | low | none (watch) | 0 |
| `sources-entry-template-drift` † | 2 | 1 | medium | none (watch) | 0 |
| `quote-notation-gap` † | 1 | 1 | low | none (watch) | 0 |
| `source-pointer-style-drift` † | 1 | 1 | low | none (watch) | 0 |
| `figure-panel-context-bleed` † | 1 | 1 | medium | none (watch) | 0 |
| `legal-posture-language-slip` † | 1 | 1 | low | none (watch) | 0 |
| `jargon-gloss-gap` † | 1 | 1 | medium | none (watch) | 0 |
| `fact-introduced-beyond-spans` | 1 | 1 | low | none (watch) | 0 |
| `quoted-title-emdash-policy-gap` † | 1 | 1 | low | none (watch) | 0 |
| `loose-anchor-attribution` † | 1 | 1 | low | none (watch) | 0 |
| `date-precision-rounding` † | 1 | 1 | low | none (watch) | 0 |

Counts derived from the ledger as of run `2026-06-20-us12430274b2-processor-on-nand-moat`
(third recorded run). `total records` counts substantive findings (severity ≠ none); each
class's proposal file under `meta/improvement-proposals/` lists the triggering finding ids and
is the append-only audit reference. `patches applied` is **0 for every class** — the system is
still propose-only; nothing has been applied by a human, so no CASCADE_CAP clock has started.
Do not hand-edit the counts.

Cross-essay recurrence (present in 3/3 essays): `mobile-paragraph-wall` (now the strongest
class — 8 records, reached **high** in run 3 via the §2 8-sentence paragraph, and shown
**revision-induced** when the §4 re-ground created a 150w wall; gate-invisible to
sentence-counting STRUCT-001), `redundancy-bloat`, `revision-induced-band-break` (now 3/3),
and `figure-token-regex-blindspot` (run 3 **fired the failure** — three spurious FIGUSE-001
from de-selection-prose mentions — a NEW variant beyond runs 1–2's lettered panels).
Present in 2/3: `claim-scope-misattribution` (did NOT recur in run 3 — the run-3 §4 high was an
*uncited external claim*, not a claim-scope misattribution; the two-independent-claims
statement verified byte-accurate), `external-fact-universalization` (run 3 added the strongest
sub-mechanism, the *unlogged* `uncited-external-claim` high), `fence-canon-verification-gap`
(did NOT recur in run 3 — the single 🤔 sat on an earned open-question close; the proposed
interrogative-host fix appears to hold pre-application), `banned-pattern-recurring`
(heterogeneous: contrast-pair density run 1, semicolon-join density run 3),
`paraphrase-hedge-compression`.

RECUR_THRESHOLD=3 reached by record count, with proposals **recommended-apply**:
`mobile-paragraph-wall`, `figure-token-regex-blindspot`, `external-fact-universalization`
(via the rolled-in `uncited-external-claim`), and the pre-existing `fence-canon-verification-gap`.
Reached 3 but deliberately **HELD at `watch`**: `redundancy-bloat` (7 records, all low,
heterogeneous sub-mechanisms — no single mechanical rule covers them, never cost a loop
iteration); `banned-pattern-recurring` (3 records, all low, heterogeneous — contrast-pair vs
semicolon density, same posture as redundancy-bloat); `revision-induced-band-break` (3 records,
all low, every instance an *accepted deliberate trade-off* that never gated a loop — diff on
record in `paragraph-length-joint-spec`, the companion to the word-wall gate). 7 proposals on
file as of 2026-06-20 (6 from 2026-06-11 + 1 new `2026-06-20-paragraph-length-joint-spec.md`);
4 are `recommended-apply`, 3 are `watch`.
† = new finding class with no row in the main routing table above; adding the missing rows
(now ~20 classes) is itself a pending small reference-edit proposal per this table's header
(human decision, carried from run 1).
