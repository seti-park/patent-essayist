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
| claim-accuracy-paraphrase | 0 | 0 | 0 | 2 | 0 | 0 |
| verbatim-normalization-artifact | 0 | 1 | 0 | 1 | 0 | 0 |
| sources-format | 0 | 0 | 0 | 1 | 0 | 0 |
| redundancy-bloat | 0 | 0 | 0 | 1 | 0 | 0 |
| spec-undercoverage | 0 | 1 | 0 | 0 | 0 | 0 |

Class-level signals (across essays):
- **verbatim-normalization-artifact** (NEW, production run 045) — the patent.md carries `**NNN**`
  bold reference-number markers glued to adjacent words (`**104**and` → "104and" after bold
  strip), and the invention-summary captured such a span; quoting it verbatim tripped Pass-3.
  Same family as the preserved "deterioriation" typo. 1 instance so far. **Watch** — if a 2nd
  bold-marker patent shows it, promote a `reference-edit` to
  `thesis-architect/references/quote-anchor-conventions.md`: when extracting a Quotable span,
  normalize `**NNN**word` joins to `NNN word`, or flag spans containing such joins as
  paraphrase-only so Phase 2 does not quote them verbatim.
- **claim-accuracy-paraphrase** — 2 instances (essay 045 dry-run). Within-essay cluster, below
  the cross-essay threshold (3). Watch.
- **spec-undercoverage** — 1 low instance. Watch.
- **goal-3 / accessibility classes** (NEW, audience=investor run of 045) — `payoff-backloaded`,
  `long-sentence-mobile`, `fix-induced-paragraph-overlong`. These appeared ONLY at the investor
  altitude (the deep run produced goal-1/goal-2 findings instead), which validates the
  audience encoding: the investor reader profile (pass-5) + load-bearing audit (pass-2 2D) +
  `gate_readability` genuinely shifted the loop's focus to reader-accessibility. All resolved
  in 3 iterations; goal-3 hard-gate (READAB-001/002) cleared. `fix-induced-paragraph-overlong`
  is a "a fix introduced a new finding" class worth watching — the loop caught its own side
  effect, which is the loop working as intended.

Applied out-of-band during run 045 (gate-promotion lever, human-applied with tests):
- `gate_figure_use` + `gate_anchors`: sub-figure letter tokens (1A/1B/5B) — commits 5c2249a / fed6acf.
- `gate_figure_use`: scope the selected set to the "## Selected figures" section + strip HTML
  comments — commit 5c2249a.
