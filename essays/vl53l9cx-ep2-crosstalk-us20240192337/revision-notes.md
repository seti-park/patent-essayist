# Revision notes — vl53l9cx-ep2-crosstalk-us20240192337

Post-acceptance self-audit deltas (`origin: self-post-accept`) for the round after the inner
Compose↔Edit loop returned `overall_assessment: pass` on `editorial-review-2` with all
deterministic gates green. Two fresh-context reviewers (impatient investor, skeptical
pro-subject reader — see `.claude/skills/editorial-review/references/pass-7-adversarial-reader.md`)
ran independently against `essay-final.md` + `input/patent.md`, with no exposure to the design
process. Multi-vote applied per `_shared/references/scoring-rubric.md` Layer 3: a finding was
applied only when both reviewers agreed, or when a single reviewer's grounding finding was
independently verifiable against `input/patent.md` directly.

## delta
class: anchor-offbyone
round: self-audit-1
before: "[0003]" cited for "A real object shows up as a peak in that histogram"
after: "[0032]" (the paragraph that actually introduces peak 201 as cross-talk and peak 203 as the real target; [0003] only covers SPAD avalanche-photodiode mechanics and never mentions peaks or targets)
rationale: single-reviewer grounding finding, independently verified against input/patent.md directly (byte-check confirmed [0003] contains no mention of "peak"); fixed at the source in handoff/01-design/invention-summary.md so a recompose cannot reintroduce it, then propagated to essay-draft.md, publication.md, essay-final.md.

## delta
class: external-fact-universalization
goal: 1
round: self-audit-1
before: "ST separately describes the module as fully calibration-free, and that framing lines up with what the reference zero-point actually is: a fixed value derived from the sensor's own known geometry, set once and reused, not a per-unit factory trim."
after: "ST separately describes the module as fully calibration-free. The patent's own word for fixing that reference point is, in fact, \"a calibration of the bin distance\" [0033], though it is a one-time geometric determination, \"performed only once\" with the result \"saved for future use\" [0060], rather than an external step that has to be repeated for every unit coming off the line."
rationale: single-reviewer grounding finding, independently verified against input/patent.md directly ([0033] literally uses the word "calibration" for this mechanism, and neither [0033] nor [0060] state whether the one-time determination is per-unit or per-design) -- the prior text asserted "not a per-unit factory trim" as if the patent said so, when that specific framing is ST's external marketing claim, not the specification's own language. Fixed at the source in handoff/01-design/invention-summary.md's calibration-free-reference-point innovation angle (added q-0033-2 as the verbatim "calibration" anchor so a recompose cannot reintroduce the same overreach), then propagated to essay-draft.md, publication.md, essay-final.md.

## delta
class: external-fact-universalization
goal: 1
round: self-audit-1 (orchestrator consistency pass, post round-2-dry)
before: "This patent gives the chip the equivalent of that fact, baked into its own dimensions, and no factory calibration step to set it."
after: "This patent gives the chip the equivalent of that fact, baked into its own dimensions, computed once and reused rather than measured anew for every unit."
rationale: same overreach pattern as the applied §6 delta above (asserting no per-unit/factory calibration step as patent fact, when [0033] itself uses "calibration" for this mechanism and the spec does not settle per-unit vs. per-design), found by the orchestrator on a final full read-through after both self-audit rounds reported dry -- neither reviewer's brief scoped them to check this second, parallel occurrence in §3 (they were asked specifically about the §6 sentence). Applied directly (single well-understood mechanical consistency fix, not a new open question) to handoff/02-compose/essay-draft.md, publication.md, handoff/03-edit/essay-final.md, and the essays/ mirror; gates re-verified clean after the edit.

## Considered, not applied (split between reviewers, or single-reviewer taste/depth suggestions — not forced in per the "gates OVERREACH, not OVER-HEDGE" rule)

- **BLUF lead-altitude** — impatient-investor reviewer: NO (lead opens on the window-reflection
  analogy before the verdict lands in para 3). Skeptical-pro-subject-reader reviewer: YES (verdict
  lands by the lead block's final sentence). Split 1-1; this exact question was also separately
  checked PASS by `editorial-review-2`'s own pass-7. Not applied — the technical-impossibility
  hook pattern's scene-then-reveal structure is a deliberate, sanctioned lead shape for this hook
  type, not a defect by majority read.
- **Header-as-claim** — impatient-investor reviewer: NO ("Two Known Filters, One New Fence" and
  "What the Combination Actually Buys..." read as topic labels, not assertions). Skeptical-
  pro-subject-reader reviewer: YES (all headers are assertions). Split 1-1, and `editorial-
  review-2` separately found all 6 headers compliant. Not applied.
- **Section-rhythm / stub balance** — impatient-investor reviewer: NO ("The Patented Mechanism
  Behind a Marketing Line" reads denser than "Two Known Filters, One New Fence"). Skeptical-
  pro-subject-reader reviewer: YES (sections roughly matched). Split 1-1; `gate_stub` (mechanical)
  and `editorial-review-2`'s pass-7 both independently read PASS. Not applied.
- **Mild self-reference phrase** — impatient-investor reviewer flagged `"That is the actual claim
  this essay is making, and no more than that"` as borderline self-reference, but hedged its own
  finding as likely exempt under the functional-scope-disclaimer carve-out. Single-reviewer,
  self-doubted, and `editorial-review-2`'s pass-7 found no meta-posturing issue at all. Not
  applied; noted for awareness only.
- **Steelman could raise a sharper technical objection** — skeptical-pro-subject-reader reviewer
  suggested the strongest available expert objection is not the "just switching between two known
  filters" framing already in the essay, but a housing-geometry-drift/aging risk: the reference
  zero-point is a one-time-computed value ([0060]) with no run-time recalibration in Claims 1-20,
  so physical drift (a replaced cover glass, thermal expansion) could silently misclassify targets
  over a unit's lifetime, a gap the companion patent's adaptive correction implicitly concedes.
  This is a single reviewer's own analytical construction (not itself a source-text contradiction,
  since the patent never discusses drift/aging), not corroborated by the other reviewer. Not
  applied to avoid over-editing a passing essay on one reviewer's un-corroborated depth
  suggestion, per the self-audit's conservative bias; logged here in case a future essay in this
  series (or a revision) wants to build on it deliberately.
