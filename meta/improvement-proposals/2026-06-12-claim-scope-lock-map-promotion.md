---
proposal_id: 2026-06-12-claim-scope-lock-map-promotion
created: 2026-06-12T05:00:00Z
status: recommended-apply
lever: reference-edit
goal: "1"
root_cause_stage: design
root_cause_artifact: thesis-architect/references/invention-summary-schema.md (claim layer) + thesis-architect/SKILL.md Step 11 (phase2-handoff-notes trap spec)
recurrence_count: 3
confidence: high
supersedes: 2026-06-11-claim-scope-lock-map  # promotes watch -> recommended-apply; original diff still applies
triggering_findings:
  - essay_id: 2026-06-10-us12636684b1-deleted-dome, iter: 1, pattern_tag: claim-scope-misattribution      # HIGH: claim-1 internal ordering presented as claim-locked
  - essay_id: 2026-06-11-us20260158546a1-both-and-steel, iter: 1, pattern_tag: claim-scope-misattribution # trap-10 wording itself misled ("such floors")
  - essay_id: tesla-washer-pump-two-wire-moat, iter: 1, pattern_tag: claim-scope-misattribution           # HIGH EL-01: spec [0012] economics attributed to "the claims"
---

## Problem

`claim-scope-misattribution` has now appeared in **3/3 runs**, twice at HIGH severity, and is
the most damaging class in the system: each instance is a grounding hard-gate breach invisible
to every deterministic gate, and each cost a full inner-loop iteration. The variants triangulate
one root cause — Phase 1 hands Compose no explicit map of *what each claim locks versus leaves
open versus never mentions*:

1. deleted-dome: the description's preferred ordering narrated as locked by claim 1.
2. both-and-steel: the trap list's own wording mischaracterized limitation scope.
3. tesla-washer-pump EL-01: the *specification's* economics argument ([0012] part count,
   production cycle time) attributed to "the claims", which recite only the mechanism.

Run 3 adds a new direction the original proposal did not cover: misattribution **into** the
claim set of content that lives only in the spec (advantages, economics, design goals).

This promotes `2026-06-11-claim-scope-lock-map` from `watch` to `recommended-apply` per the
promotion rule (recurrence ≥ RECUR_THRESHOLD = 3, artifact patched 0 times — cascade cap not in
play).

## Proposed change (exact diff)

1. Apply the exact diff in `meta/improvement-proposals/2026-06-11-claim-scope-lock-map.md`
   unchanged (claim-scope lock map in the invention-summary claim layer + per-claim
   locks/leaves-open trap entries in phase2-handoff-notes).

2. Extend the lock-map spec with one additional mandatory line, appended to the lock-map
   bullet introduced by that diff (in `invention-summary-schema.md`, claim layer):

```diff
+- **Spec-only content line (required)**: after the per-claim locks/leaves-open entries, one
+  line listing salient specification content that the claim set does NOT recite (typically:
+  economic rationale, advantages, design goals, manufacturing benefits, named example
+  applications) with its home anchors, e.g.
+  `Spec-only (never attribute to the claims): part-count / cycle-time economics [0012];
+  cross-platform application list [0024].`
+  Compose must attribute such content to the specification, never to "the claims".
```

## Why this lever

Same rationale as the original proposal: the misattribution is created at composition time but
*preventable only at design time* — Compose cannot be expected to re-derive claim-scope
semantics from raw claim text under voice-on cognitive load; Phase 1 already reads the claims
closely and is voice-off. Gate-promotion is impossible (claim-scope semantics are judged).
The run-3 evidence strengthens rather than changes the lever; the extension closes the
spec-to-claims direction at a cost of one line per patent.

## Regression expectation

`python .claude/skills/_shared/scripts/test_gates.py` and `python meta/regression.py` must still
pass (fixtures' invention-summary.md files are minimal and the schema addition is
forward-compatible; no gate parses the claim layer). After applying, Pass-3 should produce no
new `claim-scope-misattribution` records; if a 4th instance appears with the map in place, the
class hits the cascade-cap path and must be escalated to a human design decision, not re-patched.
