<!--
  TEMPLATE: handoff/02-compose/thesis-trace.md
  Produced by: essay-en-composer (Phase 2 Compose, Step 7)
  Schema sources: essay-en-composer/SKILL.md (thesis-trace.md output)
                  + references/section-blueprint.md (per-section internal plan fields)

  Externalizes the composer's internal Step-3 section plan so Phase 3 Edit Pass 4
  can check thesis-section alignment against thesis-spine.md's spine→section trace.

  Per section, record:
    - spine element carried (from thesis-spine.md)
    - arc_role (from thesis-spine.md `## Arc budget`; gate_arc maps sections by this)
    - voice_canon_reference (voice-canon-lookup entry_ids, >=1)
    - paragraph_anchors_used ([xxxx], from invention-summary Quotable spans)
    - external_facts_used (fact-check-log.md Fact IDs; [] if purely patent-anchored)
    - word_target / word_actual (DERIVED from the spine arc budget × total body;
      composer writes within ±20% of target — see section-blueprint.md)

  Example content: Tesla RCM / 70ms patent (matches essay-draft.md). Word targets
  below realize the spine arc budget lead 10 / development 55 / turn 25 / closing 10.
-->

# Thesis Trace

## Spine source

- **Spine**: handoff/01-design/thesis-spine.md
- **One-line spine**: Tesla's RCM patent reveals an architectural decision made months before the public announcement that retroactively explains the 70-millisecond claim.
- **Q7 hook**: corporate-narrative-friction

## Section → spine mapping

### 1-lead — "When the Announcement Arrived Late"
- **Spine element carried**: Hook (announcement vs filing friction)
- **arc_role**: lead
- **voice_canon_reference**: `opening-corporate-event-spacex-xai-merger-exclusion`
- **paragraph_anchors_used**: [] (framing only — no patent claim)
- **external_facts_used**: `tesla-safety-announcement-2026-03`, `tesla-rcm-filing-date`
- **word_target / word_actual**: 50 / 47

### 2-architecture — "What the Patent Actually Routes"
- **Spine element carried**: Axis 1 claims anchor + mechanism
- **arc_role**: development
- **voice_canon_reference**: `inline-bold-thesis-anchor-etherloop-steady-state`, `development-mechanism-bind-tesla-steel-tax`
- **paragraph_anchors_used**: `[0016]`, `[0017]`
- **external_facts_used**: []
- **word_target / word_actual**: 150 / 146

### 3-baseline — "The Baseline the Number Hides"
- **Spine element carried**: Axis 4 baseline-difference + adversarial mitigation (apples-to-apples)
- **arc_role**: development
- **voice_canon_reference**: `development-mechanism-bind-tesla-designer-stuck`
- **paragraph_anchors_used**: `[0014]`, `[0024]`
- **external_facts_used**: `bosch-ecu-10ms-2020`
- **word_target / word_actual**: 115 / 120

### 4-implication — "What the Filing Date Reframes"
- **Spine element carried**: Axis 3 effect anchor → strategic reframe (claim bounded)
- **arc_role**: turn
- **voice_canon_reference**: `development-curve-removal-tesla-no-better-point`
- **paragraph_anchors_used**: `[0029]`
- **external_facts_used**: `tesla-rcm-filing-date`
- **word_target / word_actual**: 120 / 118

### 5-closing — "What the Number Was Always Going to Confirm"
- **Spine element carried**: thesis recap + forward pointer
- **arc_role**: closing
- **voice_canon_reference**: `closing-forward-watching-event-etherloop-next-iteration`
- **paragraph_anchors_used**: []
- **external_facts_used**: []
- **word_target / word_actual**: 50 / 47

## Coverage check

<!-- Confirms every spine element lands in exactly one section and no section
     advances a claim outside the spine (the section-blueprint contract). -->
- All 4 axes carried: Axis 1 → §2, Axis 2 (problem) → §3, Axis 3 → §4, Axis 4 → §3.
- No out-of-spine claims introduced.
- Every `[xxxx]` used traces to an invention-summary Quotable span / Quote anchor.
- Every external fact used traces to a fact-check-log Fact ID and appears in # Sources.
