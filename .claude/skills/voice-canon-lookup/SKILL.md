---
name: voice-canon-lookup
description: "Lookup-only skill that serves SETI's voice canon (21 pattern categories, 41 canonical example entries — 33 published-human + 8 system-generated-seti-approved). Invoked by essay-en-composer when a section needs a concrete voice anchor (opening pattern, closing pattern, inline bold thesis anchor, Korean signature phrase). Returns the requested voice-canon entry's verbatim body so the composer can match cadence and structure. Use when the composer asks for a voice example, voice pattern reference, or canon lookup. NOT for: voice judgment (caller decides what to do with the example), essay drafting, editorial review, or category creation."
---

# voice-canon-lookup

Lookup-only. 어떤 voice category 가 있고, 각 category 가 무엇이고, 실제 example 이 무엇인지만 제공합니다.

본 skill 은 SETI 가 직접 trigger 하는 영역이 아닙니다. `essay-en-composer` 의 내부 호출로만 작동합니다. 작성, 편집, 판단, 분석 같은 적극적 작업은 안 합니다 — 그건 호출하는 skill 의 책임입니다.

## When to invoke

`essay-en-composer` 가 section 작성 시 voice anchor 가 필요할 때. SETI 가 직접 트리거하지 않음 (PI 가 명시).

## Voice 의 핵심 3 가지

1. **SETI 글쓰기의 목적**: 통념을 특허 물증으로 전복하는 아하 모먼트 + 결론을 열어두기
2. **핵심 패턴**: 통념 → 특허 물증으로 전복 구조. 인용-해석 동반. 본문 원자적 해석 → 결론부 종합.
3. **절대 하지 않는 것**: 인지하고 있는 명확한 진실 왜곡. 근거 없는 희망. 선동성 톤.

자세한 voice 정의는 `references/voice-profile.md` 참조.

## voice-canon/ 구조

각 entry 는 `voice-canon/` 안의 markdown 파일. frontmatter + 본문.

```markdown
---
entry_id: <unique-slug>
pattern_category: <category from list below>
source_essay: <essay-id or path>
usage_note: <why this example works for this category>
added_timestamp: <ISO 8601, optional>
---

# example 본문 (essay 단락 verbatim)
...
```

## Categories (21)

Full descriptions in `references/category-descriptions.md`.

**Opening 계열** (6)

- `opening-news-event`
- `opening-reader-experience`
- `opening-industry-norm-reversal`
- `opening-corporate-event`
- `opening-visual-anomaly`
- `opening-stake-first` — investor altitude (2026-06-10 admission)

**Development 계열** (3) — 본문 중반 anchor (2026-06-10 admission)

- `development-mechanism-bind`
- `development-objection-answer`
- `development-curve-removal`

**Closing 계열** (5)

- `closing-aphoristic-landing`
- `closing-open-question`
- `closing-forward-watching-event`
- `closing-binary-test`
- `closing-watch-signal` — investor altitude (2026-06-10 admission)

**Inline 계열** (3)

- `inline-bold-thesis-anchor`
- `inline-honest-caveat` — 주장 경계 (2026-06-10 admission)
- `inline-scope-fence` — 인접 주제 차단 (2026-06-10 admission)

**Signature phrase 계열 — 한국어** (4)

- `sig-ko-hypothesis-statement`
- `sig-ko-core-claim`
- `sig-ko-next-question`
- `sig-ko-interesting-pivot`

## Lookup logic

각 호출은 다음 조건에 따라 진행.

1. **Voice 통합 정의** (정체성, beliefs, 핵심 voice 패턴) 가 필요할 때
   → `references/voice-profile.md` view
2. **Specific category 의 example** 이 필요할 때
   → `voice-canon/index.yaml` 에서 entry_id 찾고 해당 entry .md 파일 view
3. **Category 의 정의 / 용례** 가 필요할 때
   → `references/category-descriptions.md` view

> Note: Deliverable 본문의 mechanical 규칙 (em-dash, paragraph 길이, 인용-해석 동반 등) 은 Project Knowledge 의 `deliverable-voice-rules.md` 영역. Banned-pattern list 는 Project Knowledge 의 `anti-ai-writing.md`. 본 skill 영역 아님.

## Index format (`voice-canon/index.yaml`)

```yaml
entries:
  - entry_id: opening-news-event-tesla-terafab
    pattern_category: opening-news-event
    source_essay: <essay-id>
    file: opening-news-event-tesla-terafab.md
    # provenance: 생략 시 published-human; 시스템 산출 발췌는
    # provenance: system-generated-seti-approved 명시 (Admission policy 참조)
  - entry_id: ...
```

## 호출 패턴

- **essay-en-composer Step 3** — Section 마다 voice_canon_reference 로 entry_id 명시. 본 skill 이 entry_id 받아 해당 entry 의 verbatim body return.
- **essay-en-composer Step 4 (compose)** — section 작성 시 해당 entry 의 cadence/structure 를 anchor.

## Out of scope

- Voice judgment (caller decides).
- Essay drafting.
- Editorial review (Phase 3 영역).
- New category 정의 (단순 lookup, mutation 아님).
- Banned-pattern detection (Knowledge file 영역).

## References

- `references/voice-profile.md` — full voice 정의 (정체성, beliefs, 핵심 voice 패턴, voice 의 3가지 핵심)
- `references/category-descriptions.md` — 21 categories 의 정의 + 용례 + 적용 예시

## Voice canon directory

- `voice-canon/index.yaml` — entry metadata list
- `voice-canon/<entry_id>.md` — 41 individual entries (frontmatter + verbatim 단락 본문; 33 published-human + 8 system-generated-seti-approved)

## Admission policy (2-tier provenance)

The canon's value is that it anchors "human-like" to an **exogenous human signal**. Two
provenance tiers, recorded per entry in `index.yaml`:

- **`published-human`** (default; all original 33 entries) — verbatim from SETI's actually
  published essays/interviews. The ground-truth tier. These entries are **never displaced** by
  system-generated ones.
- **`system-generated-seti-approved`** — excerpted from a pipeline-produced essay. Admission
  requires BOTH: (1) the essay cleared the full loop (gates + editorial + pre-publish verify) —
  *necessary*, and (2) **SETI explicitly approved the specific passage** as "this is my voice" —
  *sufficient*. A gate-pass alone NEVER admits an entry (filters are one-directional: they prove
  absence of tells, not presence of voice). Primary use: filling categories the human canon
  does not cover (e.g. development/mechanism sections, investor-altitude variants).

**Drift guard.** Self-referential canon risks echo-chamber drift (the system imitating its own
output). The meta-loop watches the correlation between the share of system-originated anchors
used in a run and that run's pass-1 voice findings; a rising trend flags the system-originated
entries for re-review (see `meta/attribution-table.md`).
