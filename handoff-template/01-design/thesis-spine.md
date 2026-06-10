<!--
  TEMPLATE: handoff/01-design/thesis-spine.md
  Produced by: thesis-architect (Phase 1 Design, Step 8 — spine lock)
  Schema sources: thesis-architect/SKILL.md "Output" example
                  + references/4-axis-grounding.md (Output schema)
                  + references/hook-patterns.md (Q7 hard gate)
                  + references/adversarial-defense.md (Output schema)

  This is the LOCKED single spine that Phase 2 Compose executes against. Phase 2
  rejects this handoff if the Q7 hook is not declared or if Quotable spans are
  missing for the spine anchors. Example content: Tesla RCM / 70ms patent.
-->

# Thesis Spine

## Selected thesis

<!-- One-line spine = the single sentence the whole essay defends. -->
**One-line spine**:
> Tesla's RCM patent reveals an architectural decision made months before the public announcement that retroactively explains the 70-millisecond claim.

## 4-axis grounding

<!-- All 4 axes MUST be anchored. A missing axis disqualifies the candidate
     (it should never reach the locked spine). Anchors trace to invention-summary.md. -->

### Axis 1 — Claims anchor
<!-- Format: "청구항 N 의 (X) limitation — '...'". Independent claim preferred. -->
> 청구항 1 의 (b) limitation — "the vision sensor providing pre-impact prediction to the airbag controller"

### Axis 2 — Problem anchor
<!-- Format: "[XXXX] '기존 X 의 한계는 Y'". Source: §종래 문제 Quotable spans. -->
> `[0014]` "conventional accelerometer-based systems respond only after the collision has begun"

### Axis 3 — Effect anchor
<!-- Format: "[XXXX] '본 발명은 Z 효과'" or "why_novel synthesis".
     Source: §유리한 효과 Quotable spans + quantitative significance entries. -->
> `[0024]` "deployment decision is made approximately 70 milliseconds before traditional accelerometer-based systems would respond"

### Axis 4 — Baseline-difference anchor
<!-- Format: "<industry baseline> vs <claimed> (<comparison type>)".
     Source: Step 2 context research + §Prior-art differentiation. Needs an
     EXTERNAL baseline — patent novelty alone does not satisfy this axis. -->
> Bosch airbag baseline ~10ms accelerometer latency vs claimed ~70ms vision-path lead (industry-baseline-comparison)

## Consensus evidence (통념 실재 검증)

<!-- The 통념 this thesis overturns must be REAL. check_thesis_card.py enforces:
     0 external citations => TCARD-003 hard fail (a 통념 nobody holds is a strawman,
     and overturning it is not a thesis); 1 citation => TCARD-004 warn; >=2 clean.
     Citations come from Step 2 context research (search-log.md) and are seeded
     into fact-check-log.md so prepublish-verify re-resolves them live.
     (portfolio 확장 예약: 교차-특허 주장은 >=2 특허 네임스페이스 인용 — 추후) -->

- **통념 (one sentence)**: Pre-impact airbag deployment decisions are treated as an accelerometer-domain problem; vision systems are for avoidance, not restraint timing.
- **Citations (≥1 hard, ≥2 clean)**:
  - SAE technical brief — "restraint deployment remains anchored to inertial sensing" — https://www.sae.org/example-restraint-sensing (2023)
  - Automotive News analysis — "camera inputs inform braking, not airbag firing decisions" — https://www.autonews.com/example-adas-restraint (2024)
- **전복 (one sentence)**: Claim 1's vision-path limitation `[0016]` puts the camera directly in the deployment decision, ~70ms `[0024]` ahead of the inertial baseline.

## Q7 hook pattern (hard gate)

<!-- Exactly ONE of the 2 admitted patterns must be checked, with its anchor.
     corporate-narrative-friction | technical-impossibility.
     If neither maps, the candidate is rejected at Step 5. -->
- [x] `corporate-narrative-friction` — anchor: Tesla 公식 safety 발표가 patent publication 보다 11개월 후 → narrative friction
- [ ] `technical-impossibility`

## Adversarial defense

<!-- 3 layers. Strongest objection from the strictest reader (steelman, not weak-man).
     Mitigation must name WHERE in the essay the objection is disarmed.
     Residual risk: none | Acknowledged: <noted assumption> | Acceptance: <falsifier>. -->
**Strongest objection**: The 70ms claim could be measured against a different baseline than Bosch's 10ms accelerometer, making the comparison apples-to-oranges.

**Mitigation**: §3 explicitly cites both baselines (Bosch ~10ms accelerometer vs Tesla ~70ms vision-path) and shows both are pre-deployment-decision latencies — an apples-to-apples comparison.

**Residual risk**: Acknowledged — Bosch's ~10ms baseline assumes a 2020-era accelerometer ECU; §3 notes this and bounds the claim accordingly.

## Single-spine declaration

<!-- Single-spine is the v2 default. Multi-spine requires an explicit SETI override
     per references/single-spine-default.md. -->
- [x] Single-spine (default)
- [ ] Multi-spine (override — record SETI authorization)

## Arc budget

<!-- The length+structure DECISION, made once here in Phase 1 (not improvised at
     compose time). Declare THIS essay's arc as a list of roles, each with its
     share (%) of the body; shares sum to ~100. Mark a role `(once)` if it must
     appear in exactly one section (e.g. a single turn/reversal). The roles are
     declared per-essay — pick from the recommended set or name your own; do NOT
     force a fixed shape (a forced "reversal" the essay doesn't have is Goodhart).

     Recommended roles: lead, context, development, turn (reversal), implication,
     closing. Phase 2 derives each section's word_target from these shares ×
     the total budget (investor total ≈ the gate_readability ~1100 ceiling; deep
     total = the planned body length). Phase 3's `gate_arc` checks the draft's
     actual per-role word share against this declaration (±15%, warn) plus the
     `once` and mapping rules — a deterministic conformance FILTER, never a score
     to maximize. -->

| Role | Budget % | once? |
|---|---|---|
| lead | 10 | |
| development | 55 | |
| turn (reversal) | 25 | once |
| closing | 10 | |

<!-- gate_arc also accepts a bullet form: `- lead: 10%`, `- turn: 25% (once)`. -->

## Spine → section trace

<!-- The contract Phase 2 follows: every supporting point lands in exactly one
     section; no section advances claims outside the spine. Section ids are
     planned by the composer (section-blueprint.md). Each section also carries an
     `arc_role` (from the Arc budget above) in thesis-trace.md, which gate_arc
     reads to map sections to budgeted roles. -->
| Section | Arc role | Spine element carried | Primary anchors |
|---|---|---|---|
| 1-lead | lead | Hook — corporate-narrative-friction (announcement vs filing) | (framing; no patent claim) |
| 2-architecture | development | Axis 1 claims anchor + mechanism | `[0016]`, `[0017]` |
| 3-baseline | development | Axis 4 baseline-difference + adversarial mitigation | `[0014]`, `[0024]` |
| 4-implication | turn (reversal) | Axis 3 effect anchor → strategic reframe | `[0024]`, `[0029]` |
| 5-closing | closing | Thesis recap + forward pointer | (framing) |

<!--
  > Revision note — triggered by [step N] [date]: [what changed and why]
  (Append when Step 9 figure mapping or a feedback loop revises this file.)
-->
