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
| `thesis-quality` | `--thesis-gate` checkpoint rejection / verify red-team-overclaim on the 전복 | 1 | design | thesis-architect adversarial-defense (red-team vectors) / thesis-spine consensus-evidence | reference-edit (new attack vector or card item) |
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
| `arc-budget-deviation` | gate ARC-001 | 3,4a | compose | section-blueprint.md word_target distribution (vs spine arc budget) | reference-edit (gate-promotion if recurring) |
| `arc-mapping-incomplete` | gate ARC-002 | 4a | design/compose | thesis-spine `## Arc budget` ↔ thesis-trace `arc_role` sync | reference-edit |
| `arc-once-violation` | gate ARC-003 | 4a | design | thesis-spine arc budget (`once` marker vs the essay's real shape) | reference-edit |
| `lead-conclusion-weak` | pass-6 6A/6B | 4a | design/compose | thesis-spine arc / section-blueprint closing_directive | reference-edit |
| `section-thesis-misalignment` | pass-4 | 4a | design | thesis-spine spine→section trace | reference-edit |
| `reader-engagement-break` | pass-5 | 3 | compose | mode-spec posture / section-blueprint | rubric-tuning (posture) |
| `redundancy-bloat` | pass-2 | 3 | compose | section-blueprint word_target | reference-edit |
| `banned-word` | gate BANNED-001 / pass-1 1B | 4b | canon | anti-ai-writing.md → banned_terms.txt | gate-promotion |
| `banned-pattern-recurring` | pass-1 1B (judged) | 4b | canon | anti-ai-writing.md | gate-promotion (if mechanically safe) |
| `em-dash` | gate EMDASH-001 / pass-6 6E | 4b | compose | strip-pipeline.md | reference-edit |
| `voice-canon-cadence-drift` | pass-1 1A | 4b | compose | voice-canon entry (weak/missing) | voice-canon-admission |
| `voice-canon-structural-miss` | pass-1 1A | 4b | compose | voice-canon entry + section-blueprint | voice-canon-admission |
| `leaked-toolcall-tags` | gate SOURCES-005 | 4a | compose | essay-en-composer/strip-pipeline.md | gate-promotion (done) |
| `patent-attributed-number` | prepublish-verify red-team (source:red-team) | 1 | compose/edit | citation-format.md + editorial pass-3 | reference-edit |
| `overbroad-negation` | prepublish-verify red-team (source:red-team) | 1 | compose | section-blueprint precision note | reference-edit |
| `scope-conflation` | prepublish-verify red-team (source:red-team) | 1 | design/compose | thesis-spine fencing + section-blueprint | reference-edit |
| `manufactured-insinuation` | prepublish-verify red-team (source:red-team) | 4b | edit | anti-ai-writing.md (raise-then-disavow) | reference-edit |
| `source-unresolvable` | prepublish-verify source-resolution (source:fact-check) | 1 | design | thesis-architect fact-check-log / context-research.md | reference-edit |
| `citation-title-truncation` | prepublish-verify source-resolution (source:fact-check) | 4a | design | fact-check-log full-title capture | reference-edit |

**Verification-origin priority (U5):** rows whose Source signal is `prepublish-verify` (`source:"red-team"`
or `"fact-check"`) were caught by an *independent* pre-publish reviewer — i.e. the inner loop's
editorial + gates *systematically missed* them. `pipeline-retro` weights these higher: a 2nd
recurrence (not the usual 3) fast-tracks a proposal, and the proposal targets the **stage that
should have caught it** (editorial pass / compose reference / gate), never an essay-only patch.

**Canon drift watch (2-tier provenance):** the canon now admits `system-generated-seti-approved`
entries (see `voice-canon-lookup/SKILL.md` "Admission policy"). Echo-chamber risk: the system
imitating its own output. Per run, `pipeline-retro` notes the share of system-originated anchors
in `thesis-trace.md` `voice_canon_reference`s; if pass-1 voice findings trend UP as that share
rises across essays, flag the system-originated entries for SETI re-review (demote, don't
auto-delete). Human (`published-human`) entries are never displaced.

## Recurrence ledger summary (auto-maintained by pipeline-retro)

`pipeline-retro` keeps a running count per class here so a human can see system health at a
glance. Counts are derived from `meta/findings-ledger.jsonl`; do not hand-edit the counts.

| pattern_tag | open | watch | proposed | resolved | escalated | patches applied |
|---|---|---|---|---|---|---|
| claim-accuracy-paraphrase | 0 | 0 | 0 | 2 | 0 | 0 |
| verbatim-normalization-artifact | 0 | 1 | 0 | 1 | 0 | 0 |
| sources-format | 0 | 0 | 0 | 1 | 0 | 0 |
| leaked-toolcall-tags | 0 | 0 | 0 | 2 | 0 | 1 |
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
- **leaked-toolcall-tags** (NEW, Tesla rotor investor run 691) — a Phase-2 compose subagent emitted
  trailing `</content>` / `</invoke>` tags after the Sources block; the strip pipeline did not catch
  them and the gates ignore them, so they reached the deliverable (stripped by hand before archive).
  1 instance. **RESOLVED (gate-promotion)** — promoted to deterministic gate `SOURCES-005`
  (`gate_sources.py`): any leaked tool-call / harness XML tag (`</content>`, `</invoke>`, etc.)
  is now a hard gate fail anywhere in the draft, caught every round in the normal gate harness
  (test: `test_gates.py::TestSources::test_leaked_toolcall_tag_fails`). The strip-pipeline
  reference-edit remains a follow-up so Phase 2 stops emitting them at source.
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
