# Adversarial defense (Step 6)

For each thesis candidate that survived 4-axis grounding (Step 4) and the Q7 hook gate (Step 5), surface the strongest objection and draft a mitigation. Output goes to `thesis-spine.md` §"Adversarial defense".

## 원칙

가장 strict 한 reader (편집장, 경쟁 분석가, 회의적 투자자) 의 시각에서 thesis 를 공격. Steelman 의 반대 — weak-man 회피.

3 layer:

1. **Strongest objection** — 어느 reader 가 가장 강하게 제기할 challenge.
2. **Mitigation** — essay 가 어떻게 그 challenge 를 disarm 하는가. 본문의 어느 영역에서.
3. **Residual risk** — mitigation 적용 후에도 남는 weakness. 명시 (acknowledged) 또는 acceptance (post-hoc 검증 가능).

## Priority inputs

Beyond patent text itself, the following are highest-value sources for objection surfacing:

1. **Context research's layer-confusion findings** — when an informed reader can distinguish patent's contribution level from broader/narrower claims (e.g., "patent claims X at layer A, but industry's well-known result is at layer A' — informed reader expects this distinction but thesis collapses them"), this is an immediate-dismissal risk. Surface these as **Category 1 (Claim scope)** objections first.
2. **Industry baseline references** with explicit numeric data — these enable **Category 2 (Baseline)** objections.
3. **Prior-art citations within patent's own text** — these reveal what the patent acknowledges as alternative explanations (**Category 4**).

Origin: phase1-retrospective.md Insight 5-2 — context research 의 layer-confusion 발견이 informed reader 의 thesis dismissal 의 가장 강한 source. 이 priority 가 의식되지 않으면 weak-man objections 만 surface 하고 진짜 reader risk 가 catch 안 됨.

## Step-by-step

### A. Objection surfacing

각 thesis candidate 에 대해 4 카테고리 challenge 를 시도. 가장 강한 것 선정.

#### Category 1: Claim scope challenge

"Patent 의 claim scope 가 thesis 가 주장하는 mechanism 을 cover 안 한다"

Source: `invention-summary.md` §"청구항 분석" + Layer 3 `why_novel.relative_to_prior_art`.

판정: 청구항 limitation 중 thesis 가 의존하는 element 가 명시되어 있는가. Embodiment-only 인가.

#### Category 2: Baseline challenge

"Thesis 가 비교하는 baseline 이 잘못 선정되었거나 outdated 다"

Source: Step 2 context research + `references/4-axis-grounding.md` Axis 4 anchor.

판정: Industry baseline 의 정확성, 시점, attribution. Apples-to-apples 비교인가.

#### Category 3: Correlation vs causation

"Patent evidence 가 thesis 의 causal claim 을 지지하지 않는다 — correlation 만"

Source: Patent text 의 명시 인과 vs thesis 의 인과 주장.

판정: Patent 이 "X causes Y" 명시하는가, 아니면 "X is associated with Y" 인가. Thesis 가 후자를 전자로 격상하는가.

#### Category 4: Alternative explanation

"Patent evidence 가 다른 thesis 로도 설명 가능하다"

Source: `invention-summary.md` §"청구항 분석" Layer 4 `innovation_angles` — 같은 evidence 를 anchor 하는 다른 angle.

판정: 선택된 thesis 가 evidence 의 유일한 reading 인가, 가장 strong 한 reading 인가.

### B. Mitigation drafting

선정된 objection 에 대해 essay 의 어느 영역이 disarm 하는지 명시.

Format:
```
**Mitigation**: <how>. <Where in essay>.
```

예시:
- "Mitigation: §3 explicitly cites both baselines (Bosch 10ms accelerometer vs Tesla 70ms vision-path) and shows the comparison is apples-to-apples — both are pre-deployment decision latencies."
- "Mitigation: §2 quotes 청구항 1 의 (b) limitation verbatim, where the vision sensor is explicitly part of the airbag controller's decision path — not an optional accelerator."

Mitigation 이 명시 안 되면 thesis disqualification 위험. Thesis 가 weak 한 신호.

### C. Residual risk acknowledgement

Mitigation 적용 후에도 남는 weakness 명시. 3 옵션:

1. **None** — patent text 가 strict, thesis 가 완전 anchored. 최선.
2. **Acknowledged** — essay 본문에서 "본 분석은 X 가정에 기반한다" 명시. Reader 가 가정을 보고 disagree 할 수 있음.
3. **Acceptance** — post-hoc 검증 가능. "다음 patent filing 또는 product launch 가 thesis 를 yes/no 로 falsify"

예시:
- "Residual risk: none — patent text quantitatively grounded."
- "Residual risk: Acknowledged — Bosch's 10ms baseline assumes 2020-era accelerometer; modern (2025+) accelerometers may be faster. Essay §4 notes this and bounds the claim accordingly."
- "Residual risk: Acceptance — thesis predicts Tesla will publish a continuation in 2026 H2 with explicit 70ms benchmark. Falsifiable."

## Output schema (thesis-spine.md)

```markdown
## Adversarial defense

**Strongest objection**: <one-sentence challenge from a critical reader>

**Mitigation**: <how the essay disarms it + where in the essay>

**Residual risk**: none | Acknowledged: <what gets noted> | Acceptance: <falsifier event>
```

## 실패 사례

### 사례 1: Mitigation 부재

Thesis: "Tesla CAM 공정이 industry-first 다"

Objection: "BASF 가 2019 년에 유사 공정 publish 했다 — industry-first 아니다"

Mitigation 시도: ... (essay 본문에서 다루지 않음)

**판정**: Mitigation 없음 → thesis disqualification. 후보 reframe 필요. "Tesla CAM 공정이 industry-first" → "Tesla CAM patent 가 BASF approach 를 dry-electrode 와 결합한 첫 case" (다른 angle 로 reframe + BASF 차이 명시).

### 사례 2: Mitigation 이 본문에 안 들어감

Mitigation 으로 "§3 에서 baseline 비교 명시" 라고 적었지만 essay 본문에는 baseline 비교 영역이 spine 에 없음.

**판정**: Spine→section trace 와 mitigation 의 inconsistency. Spine 에 baseline 비교 section 추가 또는 mitigation 변경 (다른 section 으로).

### 사례 3: Residual risk 누락

"Residual risk: none" 으로 명시했지만 실제로는 acknowledged 영역 (e.g., baseline 시점 가정).

**판정**: Reader 가 가정을 보지 못함 → essay 의 trustworthiness 손상. Acknowledged 로 격상 + essay 본문에 1-line 가정 명시 의무.

## Pre-selection red-team (3 attack vectors — Step 6, before Step 7 selection)

기존 4 objection categories 가 *선택된 thesis 의 본문 방어*를 설계한다면, 이 3 벡터는
**선택 전에 후보 자체를 죽이는** 공격이다. card-gate (Step 4.5) 를 통과한 모든 후보에
적용한다. 하나라도 못 버티면 후보 kill — 단, 후보당 **revise-and-retry 1회** 허용
(공격을 반영해 통념/전복/범위를 고쳐 재시도). 결과는 후보별로 `thesis-candidates.md`
의 `### Red-team survival` 에 survived/killed + 사유로 기록한다.

1. **Strawman consensus** — 그 통념을 *실제로 믿는 사람이 있는가*? Consensus evidence
   의 인용이 통념을 정말 자기 언어로 진술하는가, 아니면 인접 주제일 뿐인가? 아무도
   믿지 않는 통념의 전복은 thesis 가 아니다. (기계 측: `check_thesis_card.py`
   TCARD-003/004 — 인용 0건 fail / 1건 warn. 이 벡터는 인용의 *내용 적합성*을 본다.)
2. **Triviality reduction** — 특허 물증이 지루한 설명으로도 환원되는가? (통상적 개량,
   비용 절감, 방어적 출원, 법무 관행.) 환원 가능하면 전복이 아니라 과대 해석이다.
   살아남으려면 지루한 설명을 *배제하는* 앵커가 있어야 한다.
3. **Scope overreach** — 전복 주장이 앵커가 실제 지지하는 범위를 넘는가? (예측 lead 를
   센서 latency 로, 출원을 양산 결정으로 바꿔 말하는 류.) 본문의 scope-fence 로 막을 수
   있는 수준인지, thesis 자체가 과장인지 구분한다.

생존자 2+ 이면 Step 7 쌍대 토너먼트로, 1 이면 토너먼트 생략(사유 기록), 0 이면 Step 3
복귀 (P1 내부 루프, 최대 2회).
