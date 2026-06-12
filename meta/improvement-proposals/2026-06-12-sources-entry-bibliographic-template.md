---
proposal_id: 2026-06-12-sources-entry-bibliographic-template
created: 2026-06-12T05:00:00Z
status: recommended-apply
lever: reference-edit
goal: "4a"
root_cause_stage: compose
root_cause_artifact: essay-en-composer/references/x-articles-format-en.md (Sources per-item citation format)
recurrence_count: 4
confidence: high
triggering_findings:
  - essay_id: 2026-06-10-us12636684b1-deleted-dome, iter: 1, pattern_tag: sources-entry-template-drift  # F12 Papers title/author-form drift
  - essay_id: 2026-06-10-us12636684b1-deleted-dome, iter: 2, pattern_tag: sources-entry-template-drift  # F12 round-2 author-form residual
  - essay_id: tesla-washer-pump-two-wire-moat, iter: 1, pattern_tag: sources-entry-template-drift       # EL-03 "priority" label on a Filed date
  - essay_id: tesla-washer-pump-two-wire-moat, iter: 2, pattern_tag: sources-entry-template-drift       # R2-01 "inventors:" plural for a single inventor
---

## Problem

Four findings across 3/3 runs show the composer improvising bibliographic field labels in
`# Sources` entries, threatening goal 4a (well-structured) and, in the EL-03 case, goal 1
accuracy (a date assertion a patent-literate reader can falsify). The decisive evidence from
`tesla-washer-pump-two-wire-moat`: **the fix for EL-03 itself introduced R2-01** — two improvised
fields in the same entry in one run — which rules out composer care and pins the root cause on
the template.

And the template is not merely missing; the current one is **wrong for common documents**:

- Field 4 of the Patents sequence mandates a *priority date* unconditionally. US 2026/0162475 A1
  asserts no priority claim and the document field is *Filed*, so following the template produced
  the EL-03 mislabel. The worked example even carries the typo "priorited 2024-11-08".
- Field 6 hardcodes the plural label "inventors", producing R2-01 ("inventors: Christian
  Schotte") for a single-inventor document.
- The Papers rule never states that the title must be the *published title verbatim*, which
  permitted deleted-dome F12's descriptive-label substitution and varying author forms.

This class is judged content (label-vs-document-field semantics), so `gate_sources` cannot catch
it mechanically without false positives; the fix belongs in the reference the composer follows.

## Proposed change (exact diff)

Against `.claude/skills/essay-en-composer/references/x-articles-format-en.md`,
section `### Sources per-item citation format`:

```diff
 **Papers (academic)**. 저자 4명 이상 시 *First, et al.* 형식 (full author list 안 함). citation 의 simplicity + Chicago / IEEE style 의 정합.
+제목은 published title 의 verbatim (descriptive label 로 대체 금지); 저자 표기는 전 entry 에 동일 형식 (surname-only 와 full-name 혼용 금지).
 
 예 — *Li, Marzook, et al. (2024). "Title". Journal Name, Vol(Issue).*
 
 **Patents**. 6 field 의 sequence.
 
 1. 공개 / 등록번호 (publication number 또는 grant number)
 2. 발명의 명칭 (인용 부호 안)
 3. 출원인 (assignee)
-4. priority date (`YYYY-MM-DD`)
+4. date(s) — label 은 문서의 실제 field 를 따름: priority claim 이 문서에 실재할 때만 *priority `YYYY-MM-DD`*; 그 외에는 *filed `YYYY-MM-DD`* (출원일). filing date 를 priority 로 relabel 금지.
 5. publication date (`YYYY-MM-DD`)
-6. inventors (전원, full name)
+6. inventor(s) (전원, full name) — label 의 수 일치: 1인이면 *inventor:*, 2인 이상이면 *inventors:*.
 
-예 — *US20260134331A1, "Systems and Methods for Structure-Conforming Generation of Content," Google DeepMind, priorited 2024-11-08, published 2026-05-14, inventors: Ishita Dasgupta, Nikita Saxena, Isabelle M. Guyon, Mathangi Venkatesan, Benjamin Jan Pietrzak.*
+예 — *US20260134331A1, "Systems and Methods for Structure-Conforming Generation of Content," Google DeepMind, priority 2024-11-08, published 2026-05-14, inventors: Ishita Dasgupta, Nikita Saxena, Isabelle M. Guyon, Mathangi Venkatesan, Benjamin Jan Pietrzak.*
+
+예 (priority claim 없음, 단독 발명자) — *US 2026/0162475 A1, "Vehicle Systems with Integrated Sensors and Integrated Actuators," Tesla, Inc., filed 2024-12-10, published 2026-06-11, inventor: Christian Schotte.*
```

## Why this lever

Reference-edit is the cheapest durable fix: the composer demonstrably follows this template
faithfully (EL-03 *was* template compliance), so correcting the template corrects the output.
Gate-promotion is unsafe — distinguishing a legitimate priority date from a mislabeled filing
date, or inventor count, requires reading the patent document, outside `gate_sources`' scope.
Rubric-tuning is disproportionate for an entry-format defect.

## Regression expectation

`python .claude/skills/_shared/scripts/test_gates.py` and `python meta/regression.py` must still
pass (both fixtures' drafts use flat Sources lists; no fixture asserts the old field labels).
After applying, the next run's `# Sources` Patents entry must label dates per the document and
agree inventor-label number; the `sources-entry-template-drift` class should produce no new
ledger records.
