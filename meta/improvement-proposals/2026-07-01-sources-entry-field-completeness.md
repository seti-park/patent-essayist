---
proposal_id: 2026-07-01-sources-entry-field-completeness
created: 2026-07-01T00:00:00Z
status: recommended-apply
lever: reference-edit
goal: "4a"
root_cause_stage: compose
root_cause_artifact: essay-en-composer/references/x-articles-format-en.md (Sources per-item citation format — field labels + no stated convention for an unverifiable/unstated field)
recurrence_count: 4
confidence: high
triggering_findings:
  - essay_id: 2026-06-11-us20260158546a1-both-and-steel, iter: 1, pattern_tag: sources-entry-template-drift
  - essay_id: 2026-06-11-us20260158546a1-both-and-steel, iter: 2, pattern_tag: sources-entry-template-drift
  - essay_id: 2026-06-24-us12560948b2-safe-stop, iter: 1, pattern_tag: sources-entry-template-drift
  - essay_id: vl53l9cx-ep2-crosstalk-us20240192337, iter: 2, pattern_tag: sources-entry-template-drift
---

## Problem

`sources-entry-template-drift` has now recurred four times across three different essays, each
time as a different flavor of the same root gap: `x-articles-format-en.md`'s Sources per-item
citation format states the field **sequence** but not (a) a strict field-4 **label** the
composer is bound to reuse verbatim, or (b) what to do when a field is **genuinely unstated or
unverifiable** in the source material.

- `2026-06-11-us20260158546a1-both-and-steel` (iter 1, low-then-medium): Papers entries used a
  descriptive label instead of a real title, and author forms varied (surname-only vs. full,
  with/without "et al."); an authorless entry had to open on its title with no explicit sanction
  for doing so.
- `2026-06-24-us12560948b2-safe-stop` (iter 1, low): three academic papers cited with only the
  patent's own "Other Publications" title + year, no venue — again an unstated-field case with
  no on-file convention for how to render it.
- `vl53l9cx-ep2-crosstalk-us20240192337` (iter 2, low, **this run**): the spec names field 4
  "priority date" but the draft wrote `filed YYYY-MM-DD` on both new Patents entries, and the
  hero-patent entry omitted field 5 (publication date) — genuinely unknown per
  `invention-summary.md`'s Metadata — with **no placeholder marker**, leaving a reader unable to
  tell "omitted because unknown" from "omitted by mistake."

Every instance so far has been low/medium severity and none has cost a loop iteration (the
composer's ad-hoc handling has consistently been *defensible*, just inconsistent) — this is
exactly the "small, recurring, mechanically fixable, no false-positive risk" profile the
reference-edit lever exists for, and the 4th occurrence crosses `RECUR_THRESHOLD` (3).

## Proposed change (exact diff)

**File: `.claude/skills/essay-en-composer/references/x-articles-format-en.md`**

Against the current text (lines 66–77, Korean-language reference; edit is additive, placed
directly after the existing 6-field list and before the current example):

```diff
 **Patents**. 6 field 의 sequence.
 
 1. 공개 / 등록번호 (publication number 또는 grant number)
 2. 발명의 명칭 (인용 부호 안)
 3. 출원인 (assignee)
 4. priority date (`YYYY-MM-DD`)
 5. publication date (`YYYY-MM-DD`)
 6. inventors (전원, full name)
 
+**Field label 고정 (field 4/5)**. Field 4 는 반드시 `priority` label 사용 (`filed` 또는 다른
+동의어 금지 — priority date 와 filing date 는 특허법상 구별되는 개념이므로 label drift 는
+field 의 의미 자체를 흐림). Field 5 는 `published` (publication) 또는 `granted` (grant, B2/B1
+등 등록 특허의 경우) label 사용, patent 의 실제 status 에 맞춰 선택.
+
+**Field 미상 시 (unstated / unverifiable) 처리**. Source 자체에 해당 field 값이 없거나
+(예: cover page 에 publication date 미기재) 검증 불가한 경우, field 를 조용히 생략하지 않고
+`<field label>: unknown` placeholder 유지 — 예: *publication date: unknown*. Placeholder 는
+"확인했으나 값이 없음"을 "누락 실수"와 구별시키는 유일한 신호이므로 항상 명시. 값을 추정하거나
+발명하는 것은 금지 (fact-introduction 위반).
+
 예 — *US20260134331A1, "Systems and Methods for Structure-Conforming Generation of Content," Google DeepMind, priorited 2024-11-08, published 2026-05-14, inventors: Ishita Dasgupta, Nikita Saxena, Isabelle M. Guyon, Mathangi Venkatesan, Benjamin Jan Pietrzak.*
```

And for the Papers half of the same class (author-form / venue drift), immediately after the
existing Papers rule (line 62–64):

```diff
 **Papers (academic)**. 저자 4명 이상 시 *First, et al.* 형식 (full author list 안 함). citation 의 simplicity + Chicago / IEEE style 의 정합.
 
 예 — *Li, Marzook, et al. (2024). "Title". Journal Name, Vol(Issue).*
 
+**저자 미상 시**. Author 가 verifiable 하지 않은 경우 (예: 특허의 Other Publications 목록에
+저자 없이 title + year 만 기재), citation 을 title 로 시작 (author 없이). 저자를 추정하거나
+patent 의 다른 citation 에서 유추해 채우는 것 금지 — 확인되지 않은 이름의 도입은
+fact-introduction 위반과 동일하게 취급.
+
+**Venue 미상 시**. Paper 가 patent 자신의 citation 목록에서만 확인 가능하고 원 venue 가
+검증되지 않은 경우, venue field 생략 가능 (title + year 로 충분) — patent 자체가 citation 의
+provenance 이므로 venue 는 load-bearing 하지 않음. Placeholder 불필요 (venue 는 Patents 의
+priority/publication date 와 달리 optional field 로 이미 취급됨).
+
```

## Why this lever

- The defect lives entirely in an under-specified reference the composer reads at draft time
  (`root_cause_stage: compose`, `root_cause_artifact: x-articles-format-en.md`) — a
  reference-edit is the cheapest lever that durably fixes the class, per the promotion rules.
- **Not a gate-promotion**: field-label choice and unstated-field handling require judgment
  about what the source material actually supports (e.g., is a B2's publication date truly
  absent from the provided cover page, or just not yet transcribed?) — not a mechanically safe
  regex the way `em-dash` or `$cashtag` are. A gate could false-positive on a legitimately
  omitted field.
- **Not rubric-tuning**: no threshold, posture, or scoring weight is miscalibrated here — the
  editorial pass-3/pass-6 judgment calls in all four triggering findings were exactly right
  (correctly downgraded to low/medium, never blocked publication); the gap is that Compose has
  no fixed convention to follow in the first place, so each essay improvises its own defensible
  but different answer.
- **Not voice-canon-admission**: this is a citation-mechanics gap, not a voice/cadence pattern.

## Regression expectation

This is a reference-only text addition inside a `references/*.md` file; it does not touch any
gate script, `banned_terms.txt`, or `test_gates.py` fixture, so `python meta/regression.py` and
`python .claude/skills/_shared/scripts/test_gates.py` are expected to pass unchanged (no new
test case required by this diff — no mechanical/gate surface changed).

Observable success criterion for the next essay whose Sources block includes a Patents or
Papers entry with an unstated field: the composer emits field 4/5 with the fixed
`priority`/`published`|`granted` labels (no `filed` drift), and any genuinely unstated field
carries an explicit `<label>: unknown` placeholder rather than silent omission — eliminating a
new `sources-entry-template-drift` low/medium finding at the next editorial-review pass-3/pass-6
round on that essay.
