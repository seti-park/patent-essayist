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
| `mobile-paragraph-wall` † | 0 | 0 | 8 | 0 | 0 | 0 |
| `redundancy-bloat` | 0 | 7 | 0 | 0 | 0 | 0 |
| `claim-scope-misattribution` † | 0 | 0 | 5 | 0 | 0 | 0 |
| `external-fact-universalization` † | 0 | 0 | 4 | 0 | 0 | 0 |
| `fence-canon-verification-gap` † | 0 | 0 | 3 | 0 | 0 | 0 |
| `figure-token-regex-blindspot` † | 0 | 0 | 3 | 0 | 0 | 0 |
| `meta-reader-instruction` † | 0 | 3 | 0 | 0 | 0 | 0 |
| `revision-induced-duplication` † | 0 | 3 | 0 | 0 | 0 | 0 |
| `sources-entry-template-drift` † | 0 | 3 | 0 | 0 | 0 | 0 |
| `thesis-restatement-redundancy` † | 0 | 3 | 0 | 0 | 0 | 0 |
| `anchor-incomplete` † | 0 | 2 | 0 | 0 | 0 | 0 |
| `anchor-offbyone` † | 0 | 2 | 0 | 0 | 0 | 0 |
| `figure-caption-scope-deferral` † | 0 | 2 | 0 | 0 | 0 | 0 |
| `lead-thesis-deferral` † | 0 | 2 | 0 | 0 | 0 | 0 |
| `legal-posture-language-slip` † | 0 | 2 | 0 | 0 | 0 | 0 |
| `nonclaim-section-header` † | 0 | 2 | 0 | 0 | 0 | 0 |
| `paragraph-eight-sentence-slip` † | 0 | 0 | 2 | 0 | 0 | 0 |
| `paraphrase-hedge-compression` † | 0 | 2 | 0 | 0 | 0 | 0 |
| `revision-induced-band-break` † | 0 | 2 | 0 | 0 | 0 | 0 |
| `steelman-absent` † | 0 | 2 | 0 | 0 | 0 | 0 |
| `venue-ticker-convention` † | 0 | 2 | 0 | 0 | 0 | 0 |
| `banned-pattern-recurring` | 0 | 1 | 0 | 0 | 0 | 0 |
| `claim-citation-narrowing-benign` † | 0 | 1 | 0 | 0 | 0 | 0 |
| `claim-vs-spec-citation-conflation` † | 0 | 1 | 0 | 0 | 0 | 0 |
| `conclusion-over-hedge` † | 0 | 0 | 1 | 0 | 0 | 0 |
| `fact-introduced-beyond-spans` | 0 | 1 | 0 | 0 | 0 | 0 |
| `figure-composition-tooling-gap` † | 0 | 1 | 0 | 0 | 0 | 0 |
| `figure-cover-undervalued` † | 0 | 0 | 1 | 0 | 0 | 0 |
| `figure-panel-context-bleed` † | 0 | 1 | 0 | 0 | 0 | 0 |
| `figuse-selection-scope-overread` † | 0 | 0 | 1 | 0 | 0 | 0 |
| `jargon-gloss-gap` † | 0 | 1 | 0 | 0 | 0 | 0 |
| `jargon-overdepth` † | 0 | 1 | 0 | 0 | 0 | 0 |
| `longsent-quote-integrated-warn` † | 0 | 1 | 0 | 0 | 0 | 0 |
| `prosecution-record-overstatement` † | 0 | 1 | 0 | 0 | 0 | 0 |
| `publication-hard-wrap` † | 0 | 0 | 1 | 0 | 0 | 0 |
| `quote-notation-gap` † | 0 | 1 | 0 | 0 | 0 | 0 |
| `quoted-title-emdash-policy-gap` † | 0 | 1 | 0 | 0 | 0 | 0 |
| `restrained-bold-drift` † | 0 | 1 | 0 | 0 | 0 | 0 |
| `rule-of-three-warn` † | 0 | 1 | 0 | 0 | 0 | 0 |
| `section-stub-imbalance` † | 0 | 1 | 0 | 0 | 0 | 0 |
| `source-pointer-style-drift` † | 0 | 1 | 0 | 0 | 0 | 0 |
| `source-tier-hedge-posture` † | 0 | 1 | 0 | 0 | 0 | 0 |

Counts derived from the ledger (105 records) as of run
`2026-06-27-us20260179833a1-deleted-hole` (Tesla metallized-ferrite planar transformer; sixth
recorded run; inner-loop PASS @ iter-2, self-audit DRY in 2 rounds). A class with a proposal on
file shows its triggering records under `proposed` (the proposal file under
`meta/improvement-proposals/` lists the triggering finding ids and is the append-only audit
reference).

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

Run `2026-06-27-us20260179833a1-deleted-hole` update (counts only; no new lever):
`claim-scope-misattribution` recurred at **count 5** but at the *opposite end of the severity
spectrum to runs 1–2* — a single LOW `self-post-accept` delta (§4 over-described independent
claim 1 as parts "bonded together"; claim 1 recites no bonding limitation), caught
**autonomously by the skeptic-persona self-audit in fresh context**, no human and no inner-loop
breach. It errs *against the subject* (makes claim 1 read narrower than it is), the inverse of
the runs 1–2 grounding hard-gate breaches that read the subject *too broadly*. The on-file
`2026-06-11-claim-scope-lock-map.md` (reference-edit, still `watch`) already owns the class; this
run is confirming evidence that the lock-map is the right lever, not a new failure mode.
`mobile-paragraph-wall` reached **count 8** (caught-in-loop iter-1 medium + a *demoted* round-2
low, the quote-integrated paragraph exception working as designed) — the on-file
`2026-06-11-gate-structure-word-wall.md` (recommended-apply) still owns it; no new lever.
`external-fact-universalization` reached **count 4** via an orphan-source variant (two Sources
entries backing an unmade borrowed-from-PV silver/glass-frit lineage claim; resolved by dropping
the sources, not the prose) — owned by `2026-06-11-external-fact-scope-discipline.md`
(recommended-apply).

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

New first-seen classes in run `2026-06-27-us20260179833a1-deleted-hole` (all count 1, `watch`):
**`restrained-bold-drift`** (round-2 LOW — two load-bearing **bold** thesis anchors vs
deliverable-voice-rules' single-anchor target; each is a genuine argument landing so neither is
wrong alone, voice-fenced to `deliverable-voice-rules.md`, NOT `voice-profile.md`),
**`longsent-quote-integrated-warn`** (iter-1 MEDIUM — a 44-55-word §3/§4 sentence cluster, split
at the sentence level in iter-2; the residual gate_typography LONGSENT-001 warns are the
patent-domain quote exception or gate-merge boundary artifacts — behaving as designed, warn never
fails the round), and **`claim-citation-narrowing-benign`** (round-2 LOW — the draft cites only
claim 5 where the spine framed claims 5/9/10; an accurate *narrowing*, errs toward under-claiming
the subject, the benign inverse polarity of `claim-scope-misattribution`, no grounding risk).

RECUR_THRESHOLD=3 reached by record count (as of run
`2026-06-27-us20260179833a1-deleted-hole`): `mobile-paragraph-wall` (8),
`claim-scope-misattribution` (5), `external-fact-universalization` (4),
`fence-canon-verification-gap` (3), `figure-token-regex-blindspot` (3) — all five have a proposal
on file. Two classes **newly crossed 3 this run**: `meta-reader-instruction` (now 3 — but its
mechanical lever `gate_meta` is already promoted/done; this run's instance was a *soft* imperative
"Read that twice" below gate_meta's literal trigger set, caught by editorial pass-1, a low in-loop
catch — no new lever, `watch`) and `thesis-restatement-redundancy` (now 3 — a sub-mechanism of
`redundancy-bloat`, which is itself deliberately HELD at `watch`; the instance is a 4-distinct-frames
vs ≤3 pass-7 judgment that has never cost a loop iteration, so it inherits the parent's hold —
`watch`, no rubric-tuning warranted on a borderline distinct-frames count). `redundancy-bloat`
(now at 7) remains deliberately HELD at `watch`: heterogeneous sub-mechanisms — anchor doubling,
caption echo, sanctioned-layering awareness, intensifier tics, thesis re-assertion — no single
mechanical rule covers them and the class has never cost a loop iteration. 12 proposals on file
as of this run; no new proposal written for `2026-06-27-us20260179833a1-deleted-hole` (every
threshold-crossing class already has an on-file proposal or routes to a done/held lever —
nothing crossed cleanly with a new, mechanically-safe lever this run materially advances). Do not
hand-edit the counts.
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
