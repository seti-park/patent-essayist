# Context research (thesis-architect Step 2)

thesis-architect Step 2 의 web-search-first context research + placeholder stop + 발견 사실의 fact-check-log admission detail.

## Research procedure

Web search for cascade, industry baseline, prior art, related news. Output is *staged* for fact-check-log admission — not directly injected into the spine.

### Sub-step a: Web-search-first

본 step 의 모든 synthesis 는 web search 결과 기반. 모델의 내부 지식 기반 synthesis 는 금지. 출원인, 업계 동향, 경쟁사 기술 등의 industry context 는 web search 로 evidence 확보 후에만 작성.

검증 절차:

1. 연구 시작 시 `handoff/01-design/search-log.md` 생성. 매 web search 마다 query + date + top result URLs + result snippet + used-in column 기록 (SKILL post-condition 과 동일 schema).
2. Synthesis 전 search-log 존재 + 최소 3 query 기록 확인.
3. Synthesis 의 모든 claim 이 search log 의 specific URL 에 anchor 되는지 cross-check.
4. Self-check (mechanical gate 아님): search-log 부재 시 Step 3 candidate generation 진입 금지.

### Sub-step b: Source authority application

Industry context, 경쟁사 기술, 출원인 정보 의 source 는 primary source authority hierarchy 따름. Hierarchy detail 과 verification rule 의 SoT 는 editorial-review 의 `references/external-fact-verification.md` (thesis-architect 와 editorial-review Sub-pass 3.5 가 cross-skill share).

thesis-architect Step 2 적용 시 다음 application rule 만 의식:

- **경쟁사 또는 타사 기술 claim** 시 최소 Tier 2 source 필수 (그 회사의 official statement 또는 registered patent 또는 peer-reviewed paper). Tier 3 news media 만으로는 부족.
- **출원인 정보 또는 회사 전략** claim 시 Tier 1 우선 (Company official statement, press release, IR page, SEC filing).
- **시의성 이벤트** claim 시 Tier 1 과 Tier 3 양쪽 cross-check.
- **기술 mechanism** claim 시 Tier 2 (patent 또는 spec) 우선. Tier 4 의 reverse-engineered claim 은 hedge 필수.
- **Personal blog, Twitter, Reddit** (Tier 5) 은 Tier 1-4 의 backup 으로만 사용. 단독 anchor 불가.

### Sub-step c: Academic citation re-verify

External academic citations (author lists, DOI, journal, year, volume/issue) 의 web-search re-verify 의무. Memory caching 또는 prior session 의 reference 를 trusted 안 함.

본 의무가 Tesla 944 essay 의 "Tranter et al." → "Li, Marzook et al." 정정의 anchor — 본 정정이 web search re-verify 로 catch 됐고, Memory caching 으로 skip 했으면 stale citation 잔존 가능성.

### Sub-step d: Framing-impact classification

Each significant finding (web search result that anchors a 4-axis or shifts the thesis frame) must be classified for framing-impact at discovery time. Without this, Step 3 candidate generation may produce a candidate set that's invalidated by the next finding's framing impact.

| Class | Meaning | Phase 1 next action |
|---|---|---|
| **main thread** | finding shifts the thesis's primary anchor or audience hook | surface to SETI immediately; possibly re-extract `invention-summary.md` Layer 4 angles |
| **paragraph** | finding deserves one body paragraph but doesn't reshape the spine | record in `fact-check-log.md`; plan paragraph in spine |
| **footnote** | finding is supporting only — useful for credibility but not load-bearing | record only in `fact-check-log.md` |

The classification is a 1-line decision per finding. Claude proposes (with rationale), SETI accepts / overrides.

Origin: phase1-retrospective.md Insight 5-1 (STM partnership 발견의 framing 진동) + 5-2 (graceful degradation layer 구분의 정밀화).

## Placeholder stop (research 중간 게이트, candidate generation 진입 전)

Context research output 과 staged finding 들의 placeholder detection. TBD, [insert later], null, [...] 같은 unresolved placeholder 의 identification + blocking decision.

### Detection patterns (mechanical)

- `TBD`, `tbd`, `[TBD]`
- `[insert later]`, `[fill in]`, `[need]`, `[?]`
- `null` 또는 빈 essential fields
- `<...>` (unfilled template markers)
- Trailing `...` in fact statements

### Modes

- **Soft mode** (default): Placeholder 발견 시 warning + SETI elicit. Pipeline 진행 가능 (SETI 가 accept-with-knowledge 또는 fix).
- **Hard mode** (명시 시): Placeholder 발견 시 immediate STOP. Pipeline halt + FailureReport. SETI 의 fix 후 재진입.

### Default selection

- Time-constrained 또는 wire-style essays (strict-execution-mode): hard mode. 시간 제약 시 placeholder 의 silent passing 위험.
- Standard essays (walkthrough-mode): soft mode. SETI 의 mid-session catch 의 backup 가능.
- Adversarial reader 또는 strategic essays (conservative posture): hard mode. Placeholder 의 factual gap 위험.

본 placeholder stop 가 engineer-the-environment 적용 — placeholder 의 silent acceptance 회피.

## Recording findings: fact-check-log admission

v1 의 pool-admission skill 은 v2 에서 drop — admission 은 `fact-check-log.md` 기록으로 단순화. For each context research finding worth using:

1. `handoff/01-design/fact-check-log.md` 에 기록: claim text, source URL, usage type (verbatim quote / paraphrase background), 검증 상태.
2. 기록되지 않은 외부 fact 은 spine 과 Phase 2 composition 에서 사용 불가 (facts_locked = invention-summary Quotable spans + fact-check-log externals).
3. Reject 된 finding 은 discard 또는 revise.

SETI 가 full visibility 가짐 — every admission is explicit in the log.

### Hybrid strictness

- **Verbatim entries** (quote attribution): strict admission. Source verbatim match required at admission time.
- **Paraphrase entries** (background reference): lightweight admission. URL fetchable only.

### Output

`fact-check-log.md` 의 admitted entry list — Phase 2 가 사용할 수 있는 외부 fact 의 전부 (SKILL Step 10 의 post-condition 과 동일 파일).
