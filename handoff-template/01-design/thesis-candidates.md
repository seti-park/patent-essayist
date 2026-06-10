<!--
  TEMPLATE: handoff/01-design/thesis-candidates.md
  Produced by: thesis-architect (Phase 1 Design, Step 3 — candidate generation)
  Schema source: thesis-architect/references/thesis-candidate-presentation.md

  2-4 candidates. Each carries a frame + 통념/전복 statements + draft 4-axis
  grounding (locked in Step 4) + card-gate checklist (Step 4.5) + draft Q7 hook
  (hard-gated in Step 5) + draft adversarial defense incl. pre-selection red-team
  (Step 6). Survivors (2+) enter the pairwise Tournament (Step 7); the winner +
  rationale is what the orchestrator surfaces as the thesis card at the
  --thesis-gate checkpoint. Rejected candidates MUST record a rejection reason.
  Example: Tesla RCM / 70ms.
-->

# Thesis Candidates

## Candidate 1: The architectural pre-commitment

**Statement**: Tesla's RCM patent reveals an architectural decision made months before the public announcement that retroactively explains the 70-millisecond claim.

**통념 (one sentence)**: restraint deployment is an accelerometer-domain problem; cameras inform avoidance, not airbag timing.

**전복 (one sentence)**: claim 1's vision-path limitation puts the camera in the deployment decision, ~70ms ahead of the inertial baseline.

**Framing**: investigative reframe — let the filing date reorder the public narrative.

**Evidence required**:
- Patent filing/publication timeline
- Vision-path claim language
- Quantified pre-impact lead time

**Evidence available in invention-summary**:
- ✓ Timeline (filing 2024-10-23, publication 2026-04-23)
- ✓ Claims anchor (`[0016]` vision-path)
- ✓ Quantitative effect (`[0024]` 70ms)

**Structural tension**: the public "70ms is unprecedented" announcement, then the patent that was already on file explaining how.

**Risks**:
- Reader may read the timeline as coincidence rather than pre-commitment.

**Grounding (4-axis — draft, locked in Step 4)**:
- Claims anchor: 청구항 1 (b) — "the vision sensor providing pre-impact prediction to the airbag controller"
- Problem anchor: `[0014]` "conventional accelerometer-based systems respond only after the collision has begun"
- Effect anchor: `[0024]` "approximately 70 milliseconds before traditional accelerometer-based systems"
- Baseline-difference anchor: Bosch ~10ms accelerometer vs ~70ms vision-path lead

**Q7 hook pattern (draft, hard-gated in Step 5)**:
- corporate-narrative-friction
- anchor: Tesla 公식 발표가 patent publication 보다 11개월 후 → narrative friction

**Adversarial defense (draft, locked in Step 6)**:
- Strongest objection: 70ms could be measured against a non-comparable baseline.
- Mitigation: §3 cites both baselines and shows apples-to-apples.

### Card-gate checklist (Step 4.5)
<!-- Mirrors check_thesis_card.py: a candidate failing a hard item never reaches
     the tournament. Citations counted from Step 2 context research. -->
- [x] 4-axis anchored (4/4)
- [x] Consensus citations: 2 (≥1 hard, ≥2 clean)
- [x] Q7 hook maps to an admitted pattern
- [x] Arc-sustainable (enough anchors/figures to fill the declared arc)

### Red-team survival (Step 6, pre-selection — 3 vectors)
<!-- survived | killed (+reason). One revise-and-retry allowed per candidate. -->
- Strawman consensus: **survived** — both citations state the inertial-only view in their own words.
- Triviality reduction: **survived** — timeline + claim language excludes "routine defensive filing" reading.
- Scope overreach: **survived** — thesis claims pre-commitment, not production deployment.

---

## Candidate 2: Optical beats electrical

**Statement**: Tesla's airbag controller commits to deployment from a photon-based prediction faster than any accelerometer can register the crash.

**통념 (one sentence)**: electrical (inertial) sensing is the fastest possible crash trigger.

**전복 (one sentence)**: prediction-before-impact makes the optical path commit earlier than any post-impact electrical signal.

**Framing**: technical-impossibility reframe — answer the reader's "how can optical be faster than electrical?"

**Evidence required**:
- Vision-path mechanism
- Latency comparison

**Evidence available in invention-summary**:
- ✓ Mechanism (`[0017]` predictive input)
- ✓ Effect (`[0024]` 70ms)
- ✗ Independent external baseline for the optical-vs-electrical latency framing (needs more context research)

**Structural tension**: reader assumes electrical sensing is fastest; the patent inverts it via prediction-before-impact.

**Risks**:
- Conflates "prediction lead time" with "sensor latency" — could mislead a technical reader.

**Grounding (4-axis — draft, locked in Step 4)**:
- Claims anchor: 청구항 1 (b) vision-path limitation
- Problem anchor: `[0014]` accelerometer responds after collision begins
- Effect anchor: `[0024]` 70ms lead
- Baseline-difference anchor: ✗ baseline not yet externally anchored (3/4)

**Q7 hook pattern (draft, hard-gated in Step 5)**:
- technical-impossibility
- anchor: reader's "how can an optical input beat an electrical one?" is the entry point

**Adversarial defense (draft, locked in Step 6)**:
- Strongest objection: prediction lead time is not the same axis as raw sensor latency.
- Mitigation: would require an explicit definitional section.

### Card-gate checklist (Step 4.5)
- [ ] 4-axis anchored (3/4 — Axis 4 baseline not externally anchored) **← hard fail**
- [x] Consensus citations: 2
- [x] Q7 hook maps to an admitted pattern
- [x] Arc-sustainable

### Red-team survival (Step 6, pre-selection — 3 vectors)
- Strawman consensus: survived.
- Triviality reduction: survived.
- Scope overreach: **killed** — "faster than any accelerometer" conflates prediction lead with sensor latency; anchors support lead time only. Revise-and-retry consumed.

**Rejection reason**: Axis 4 (baseline-difference) only 3/4 anchored — no external baseline for the optical-vs-electrical framing; risk of conflating prediction lead with sensor latency. Reframed into Candidate 1's apples-to-apples baseline treatment instead.

---

## Comparison

| Dimension | Candidate 1 | Candidate 2 |
|-----------|-------------|-------------|
| Evidence completeness | Full | Partial |
| Audience appeal | High | High |
| Architectural depth | High | Medium |
| Defensive strength | High | Medium |
| 4-axis grounding | 4/4 | 3/4 (no baseline) |
| Q7 hook | corporate-narrative-friction | technical-impossibility |
| Hook accessibility | High | High |

## Tournament (Step 7 — survivors only)

<!-- Pairwise, relative judgment ONLY (no absolute scores — anti-Goodhart).
     Single criterion: "which one more decisively overturns a better-evidenced
     통념?" With 1 survivor, skip and record why. With 0 survivors, return to
     Step 3 and regenerate (max 2 P1 inner-loop rounds), then surface the least-bad
     candidate + failure reasons at the checkpoint. -->

- Survivors: Candidate 1 only (Candidate 2 killed at card gate + red-team).
- Tournament skipped (single survivor); rationale: n/a.
<!-- Multi-survivor form: `C1 vs C3 → C1 — C3's 통념 has one citation and it is
     adjacent, not contradicted; C1's consensus is directly stated and recent.` -->

## Selection rationale (surfaced as the thesis card at the checkpoint)

Candidate 1 — strongest 4-axis grounding (Bosch baseline well documented in context
research), consensus 실재 입증 2건, clearest hook (Tesla's announcement timing is
specific and recent), survived all 3 red-team vectors.

## Recommendation

<!-- Single line. SETI decides per references/thesis-candidate-presentation.md
     selection options (Select N / Combine / Revise / Reject all). -->
Candidate 1 — see Selection rationale above.

## SETI selection

- **Decision**: Select Candidate 1
- **Notes**: proceed to spine lock (Step 8) with Candidate 1's grounding + hook + defense.
