---
proposal_id: 2026-06-10-canon-gap-admission-tesla-investor
created: 2026-06-10T00:00:00Z
status: proposed            # → applied per-entry upon SETI approval
lever: voice-canon-admission
goal: "4b"
root_cause_stage: compose
root_cause_artifact: voice-canon-lookup/voice-canon/ (coverage gap)
recurrence_count: n/a (audit finding, not a recurrence)
confidence: high (source essay cleared gates + 6-pass editorial + independent verify + SETI review)
triggering_findings:
  - canon audit 2026-06-10: development/mechanism categories = 0 entries while arc budget
    allocates ~55% of the body to development; investor-altitude canon = 0 entries;
    thesis-trace template referenced 3 phantom ids in exactly these gap categories.
---

## Problem

The 33-entry canon covers the essay's *edges* (opening 9, closing 16, inline-bold 4, sig-ko 4)
but has **zero development/mechanism-section entries** — the very sections the arc budget gives
the most weight — and **zero investor-altitude exemplars**. Compose therefore writes the bulk of
every essay with no cadence anchor, and Pass-1 has no canon to check those sections against.

## Source + admission criterion

All candidates are verbatim from `691-tesla-rotor-nonmagnetic-filler-investor` `essay-final.md`
(clean inner-loop pass, independent pre-publish verify, multiple SETI reviews in-session).
Per the 2-tier admission policy (`voice-canon-lookup/SKILL.md`): full-loop pass = **necessary**
(met); **SETI per-passage approval = sufficient (PENDING — apply only approved entries)**.
Each admitted entry carries `provenance: system-generated-seti-approved` in `index.yaml`.

## Candidates (8 entries / 7 new categories)

### 1. `development-mechanism-bind-tesla-steel-tax`  — category `development-mechanism-bind`
> To see the trade, you have to see the bind the designer is in. At high speed the rotor wants
> to tear itself apart, and the force trying to do that climbs with the square of the speed, so
> a motor spinning twice as fast pulls four times as hard. Steel struts are the cheap, strong
> answer that keeps the magnets seated. The problem is that steel is magnetic.

usage_note: development 진입의 표준형 — *To see X, you have to see Y* 독자 인도형 오프너 → 물리량을
평이어 결과로 번역 ("twice as fast pulls four times as hard") → 짧은 문제 선언("The problem is...").
mechanism 단락이 숫자/기호 없이 인과의 압력을 만드는 cadence.

### 2. `development-mechanism-bind-tesla-designer-stuck`  — category `development-mechanism-bind`
> So the designer is stuck. Thicker struts are safer at speed but leak more. Thinner struts leak
> less but may not survive. The whole field has accepted that you cannot have both, and the loss
> is worst exactly where an electric car most wants its efficiency: at high speed, where range
> and power density are decided.

usage_note: 딜레마 압축형 — 두 대칭 단문(Thicker.../Thinner...)으로 trade-off 양끝 제시 → 업계 전체의
체념("The whole field has accepted") → 고통이 가장 큰 지점 명시(콜론 후 구체화). baseline-comparison
역할을 서술형으로 수행.

### 3. `development-objection-answer-tesla-keyed-filler`  — category `development-objection-answer`
> The obvious objection is the one a skeptical engineer raises first. You cannot just delete the
> steel that keeps a rotor from flying apart and pour in plastic. The patent's answer is
> mechanical. The metal layers of the rotor are stamped with small staggered teeth that jut into
> the empty pocket. When the filler is injected, it flows around those teeth and hardens, locking
> itself to the metal so nothing can shift or pull loose under load. The filler is not a passive
> bystander in a cavity. It is a structural member keyed into the rotor.

usage_note: steelman 반론 선제 제기 → 특허의 구체 메커니즘으로 응답 → *not X. It is Y.* 재정의
랜딩. adversarial-defense 의 본문 실현형. 반론을 독자보다 먼저 말하는 것이 신뢰 cadence 의 핵심.

### 4. `development-curve-removal-tesla-no-better-point`  — category `development-curve-removal`
> The field spent years optimizing the steel strut, trading strength for leakage and back again.
> Tesla did not find a better point on that curve. It removed the curve. There is no strut to
> make thinner, because the thing doing the holding no longer leaks.

usage_note: turn/reframe 단락의 aphoristic 압축 — *did not find a better point on that curve. It
removed the curve.* 2단문 반전. 점진 개선 vs 구조 제거의 대비를 곡선 은유 하나로. 본문 중반에서
closing-aphoristic cadence 를 미리 쓰는 변형.

### 5. `inline-honest-caveat-tesla-no-disclosed-number`  — category `inline-honest-caveat`
> One honest caveat belongs here, because it bounds the claim. The patent describes the benefit
> only in words, saying the change reduces leakage and improves performance "particularly in
> high-speed applications." It puts no number on it. So the direction is clear and the mechanism
> is sound, but the size of the win is not something this document proves. That is a thing to
> watch for, not a thing to assume.

usage_note: 주장 경계 명시형 — caveat 의 *위치 선언*("belongs here, because it bounds the claim")
→ 근거의 정확한 한계("It puts no number on it") → *watch for, not assume* 랜딩.
red-team-overclaim 이 지키려는 정직성을 생성 단계에서 앵커링.

### 6. `inline-scope-fence-tesla-rare-earth-program`  — category `inline-scope-fence`
> It is worth keeping one thing separate here. Tesla has a different, well-publicized program
> aimed at building motors with no rare-earth magnets at all, a response to a supply chain where
> most permanent magnets come from a single country. This patent is not that program. It keeps
> the magnets and changes only what holds them.

usage_note: 인접 프로그램 fence — *It is worth keeping one thing separate here* 선언 → 인접 사실
한 문장 요약 → *This patent is not that program* 단문 차단 → 무엇만 바꾸는지 재명시.
red-team-scope 가 지키려는 경계를 생성 단계에서 앵커링.

### 7. `opening-stake-first-tesla-quiet-tax`  — category `opening-stake-first`  (audience: investor)
> Every engineer who designs a high-efficiency electric motor lives with the same quiet tax.
> [...] For decades that steel has been treated as the price of admission. It holds the rotor
> together, and in exchange it bleeds away some of the motor's efficiency. Everyone pays it. A
> new Tesla patent, with the company's principal motor engineer Konstantinos Laskaris among the
> named inventors, refuses to.
>
> That refusal is the reason this filing is worth an investor's attention.

usage_note: investor stake-first 리드 — 보편 비용("quiet tax", "Everyone pays it") 프레임 →
*refuses to* 피벗 단문 → 다음 단락 첫 문장에서 독자 스테이크 직접 선언("worth an investor's
attention"). 뉴스 이벤트 없이도 스테이크로 여는 investor 변형.

### 8. `closing-watch-signal-tesla-moat-or-footnote`  — category `closing-watch-signal`  (audience: investor)
> The signal worth watching is whichever teardown or disclosure first quantifies the leakage
> Tesla just engineered out, and whether the number is large enough to be a moat or small enough
> to be a footnote. Until then, the more durable fact is the one already on the record: Tesla
> looked at the steel tax everyone pays and decided it did not have to.

usage_note: investor 클로징 — 반증 가능한 관찰 신호 지정(teardown/disclosure) → *moat or footnote*
이진 프레임 → *Until then, the more durable fact...* 으로 이미 확정된 사실에 착지. 리드의 "tax"
모티프 회수로 수미상관.

## Apply procedure (per approved entry)

1. Write `voice-canon/<entry_id>.md` (frontmatter: entry_id / pattern_category / source_essay:
   `essay-691-tesla-rotor-investor` / provenance: `system-generated-seti-approved` / usage_note /
   added_timestamp) + `# Example` verbatim body.
2. Append to `voice-canon/index.yaml` with `provenance` field.
3. Add the new categories to `references/category-descriptions.md`.
4. Resolve the matching `pending canon admission` refs in `handoff-template/02-compose/thesis-trace.md`.
5. `python meta/regression.py` (must stay green — canon은 게이트 비대상이라 무영향 기대).

## Rejected source (recorded for the audit trail)

`meta/fixtures/investor-altitude/draft.md` (SpaceX investor 축약본)는 fixture 용 재구성본이라
provenance 부적격 — 발행/검증 이력이 있는 원문이 아님. SpaceX deep/investor 원문은 handoff 덮어쓰기로
소실(Move-3a 가 향후 보존). admission 대상에서 제외.
