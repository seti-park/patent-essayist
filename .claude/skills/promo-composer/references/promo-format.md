# Promo format: the promo-pack contract + per-deliverable rules

One file, three paste-ready deliverables. v2 supersedes v1's single-digest
`promotion-post.md`: the pack carries (1) a Korean promo post, (2) the English digest in
v1's FT/Economist genre, (3) a 3-tweet thread sketch. v1's title/lede/paragraph craft is
preserved in full for the digest.

## The promo-pack.md contract

Path: `essays/<id>/promo/promo-pack.md`. Structure, in order:

1. **YAML frontmatter**: `essay_id` (copied from essay-final.md frontmatter),
   `essay_source`, `closing_posture` (copied from essay-final.md), `digest_posture`
   (A/B/C/D per `closing-posture.md`), `promo_version`, `owner_briefing` (`read` or
   `ABSENT`).
2. **Verification Status header** between `=== Verification Status (promo-composer,
   promo-pack) ===` and `=== Deliverables ===` markers. Every line is a measured number or
   PASS/FAIL, never a bare checkmark: sources read, fact_trace + dropped-facts list,
   Sub-rules 1/2/3, per-deliverable counts, digest posture agreement, hygiene tallies,
   attachment list, `suspected_essay_defects` (default `none`).
3. **Three deliverable sections** (`## 1.` KR post, `## 2.` EN digest, `## 3.` thread).
   Each section = one or more fenced ```` ```text ```` blocks (the paste surface) followed
   by plain metadata list lines (counts, attach path, alt text).

**The fence is the strip boundary.** v1's awk strip pipeline (promo-draft.md →
promotion-post.md) is superseded: nothing outside a fence is ever pasted, everything
inside a fence is paste-ready exactly as written. No separate publication file exists for
promo.

Pack-wide hygiene: em-dash 0 and bold 0 anywhere in the file (scaffolding included, so a
sloppy copy can never smuggle formatting into a post); emoji <=1 total; hashtags 0;
banned-term discipline per `_shared/scripts/banned_terms.txt`.

## Deliverable 1: Korean promo post

발행자가 자기 아티클을 소개하는 X 포스트. 한 개의 fenced block.

- **분량**: 280자 이하, 공백 포함, 한글 문자 수 기준. `[ARTICLE-LINK]` 슬롯은 23자로
  계산한다 (X 의 t.co 단축 길이).
- **목소리**: `_shared/references/working-dialogue-voice.md` register. 건조한 평서문,
  과장 배제, 발행자 1인칭 허용 (절제해서). 에세이의 영어 deliverable 목소리를 번역해
  옮기지 않는다.
- **구조**: 2-5 문장. 문장 1-2 가 에세이의 discovery beat 를 압축한다 (reader_sentence
  또는 signature line 의 한국어 압축). 보험성 사실 (계류 중, 담보, 거절 이력) 은 beat
  뒤에 온다, beat 앞에 오지 않는다. 마지막 문장은 아티클 포인터로 끝난다 (예: "전문은
  아티클에 정리했습니다." + `[ARTICLE-LINK]`).
- **금지**: 클릭베이트 의문형 후킹 ("과연?", "어떻게 됐을까요?" 류), 해시태그, 이모지,
  볼드, em dash. 감탄사와 느낌표도 쓰지 않는다.
- **Protected terms verbatim**: 특허번호, 회사명, 부품번호, 영어 인용구는 원문 그대로.
  따옴표 안은 영어 원문을 유지하고 번역은 따옴표 밖에 둔다 (briefing 과 같은 규율).
- **한국어 표현의 출처**: `owner-briefing.md` 가 있으면 그 문장 표현을 우선 재사용한다
  (검수된 한국어). 없으면 에세이의 protected lines 를 직역하되 숫자/날짜/이름은 원문과
  일치시킨다.

## Deliverable 2: English promo digest

v1's genre, carried intact. One fenced block: ALL-CAPS title line, blank line, 3-5
paragraphs.

### Digest 격 정의

FT (FirstFT, Edit), The Economist (Espresso, World in Brief) 같은 editor-curated digest
의 격. **Trust-driven** (engagement-driven 아님). 첫 sentence 에 thesis 가 압축되고,
본문은 핵심 fact 정리, 마무리는 담담한 implication 관찰.

| 형식 | 분량 | 격 | 목적 | hedge 강도 |
|------|----|----|----|----------|
| Essay | 2,000-3,500w | FT/Economist prose, paragraph 3-7 sentence | 분석 backup evidence layer | essay 기준 |
| Digest | 280-340w | 단락 1-3 sentence, 3-5 단락 | Trust-driven self-contained digest | essay 와 동일, backup 은 essay |

Digest 는 essay 에 의존한다. 단독으로 finishable 해야 하지만, 모든 fact 는 essay 본문에
backup 으로 존재한다.

### 3-5 단락 구조

**3-paragraph** (단일 patent, tight thesis arc): §1 Lede (~30w) → §2 Patent mechanism +
thesis (~80w) → §3 Closing (~25w). Total ~135w + title.

**4-paragraph** (default): §1 Lede (~30w) → §2 Patent mechanism + thesis (~80w) → §3
Implication (~50w) → §4 Closing (~25w). Total ~185w.

**5-paragraph** (multi-patent 또는 rich evidence): §1 Lede (~30w) → §2 Patent one (~55w)
→ §3 Patent two + thesis (~80w) → §4 Implication (~50w) → §5 Closing (~25w). Total ~240w.

Word budgets are the arc's shape, not the 280-340 total; expand paragraphs evenly to hit
the total.

### Paragraph signatures

- **§1 Lede**: 첫 sentence 에 thesis 압축. Specific date / number / quote 1 개 이상.
  Drama 없음. Voice canon `opening-news-event` 패턴 (declarative 진입).
- **§2 (or §2-§3) Patent mechanism**: mechanism + 정량 1-2 개. Quote 인용 가능 (essay
  carry-over, verbatim). 첫 sentence 가 무엇을 해결, 다음이 메커니즘.
- **§3 or §4 Implication**: thesis statement + external connection (product / cost /
  시의성). Essay 의 implication section 압축. Essay 에 없는 external fact 는 못 쓴다.
- **§N Closing**: 담담한 observation 또는 forward pointer. Essay closing 의 회수가 가장
  강하다. Defensive hedge 0 회. 4 posture taxonomy 는 `closing-posture.md`, essay 의
  `closing_posture` 와 합치해야 한다.

### Title 작성

- **원칙**: 본문을 안 읽어도 글이 무엇인지 알 수 있어야 한다 (self-contained).
  Metaphor 에 의존하지 말고, patent 가 실제로 무엇을 다루는지 직설.
- **형식**: ALL-CAPS, 12-16 단어.
- **좋은 패턴**: `TESLA PATENT DETAILS [MECHANISM] BEHIND [PRODUCT/LINE]`,
  multi-patent 은 `TWO TESLA PATENTS DETAIL [M1] AND [M2] BEHIND ITS [PRODUCT/LINE]`.
  Canon 예시: `TWO TESLA PATENTS DETAIL THE POWDER FLOW AND ROLLER GAP BEHIND ITS DRY
  4680 LINE`.
- **회피**: "X JUST PATENTED Y" (클릭베이트), "X REVEALS / UNVEILS" (매체 hype), 본문
  없이 의미 안 통하는 echo 제목.
- **판정**: 본문 안 읽어도 무엇인지 안다. 분석가 voice. "of what?" 의문이 안 떠오른다.
- **주의**: essay 제목의 70자 규칙 (SURF-001) 은 아티클 카드용이다. digest title 은
  포스트 본문 첫 줄이므로 단어 수 규칙 (12-16) 만 적용한다.

### Lede 작성

Declarative news statement. 첫 sentence 에 thesis 압축. 패턴:

```
[Company] published [N] patent application(s) on [date] that, [optional read-together
clause], describe(s) [the mechanism / system] behind [related event].
```

판정: 첫 sentence 에 thesis 가 다 들어간다. Hook drama 없음. Specific date / number /
quote 1 개 이상. 시제와 확실성 동사 (published / filed / asks for / describes) 는 essay
의 표현과 일치.

### 단락 + 문장 규칙

- 1-3 sentences per paragraph; 4+ sentence 단락 회피. 한 단락 = 한 역할.
- 문장 최대 35 words. Closing 은 15-25 words 권장.

### Format 규칙

- Title: ALL-CAPS 12-16 단어, self-contained. 본문에는 markdown header 금지 (title 줄만).
- Bold 0. Em dash 0. Colon 2 회 이내 (lede 또는 list 도입에만).
- Emoji: 팩 전체 예산 <=1. 사용한다면 슬롯은 digest closing 의 🤔 하나뿐이다. essay 가
  🤔 없이 끝났다면 digest 도 0 이 자연스럽다.
- `[dddd]` paragraph anchor, reference numeral, 내부 ID (fact ID, canon entry ID) 는
  본문에서 제거한다 (`audience-adaptation.md`).

### Hedge 정책

Digest 의 hedge 강도는 essay 와 동일하다. 양방향으로: essay 보다 세게 단정하지 않고
(overreach), essay 가 firm 하게 내린 결론을 무르게 하지도 않는다 (over-hedge, gate_hedge
가 essay 에서 걷어낸 바로 그 격).

| Hedge 영역 | Digest 규칙 |
|---------|-----|
| Universal claims | 0 건 (essay 와 동일) |
| "significantly" 류 modifiers | 0 건 |
| 1차 source attribution | 핵심 인용만 명시, 나머지는 essay backup 에 위임 |
| 시점 표현 | 정확성 필수 + `fact-verification.md` Sub-rule 1, 2 |
| Safe-harbor boilerplate | 0 건 ("a patent doesn't guarantee..." 류, `closing-posture.md` 회피 목록) |

Essay 에 명시 없는 fact 는 digest 에 넣지 않는다.

## Deliverable 3: 3-tweet thread sketch

English. Three fenced blocks, one per tweet, each <=280 chars (`[ARTICLE-LINK]` = 23).
Sketch level: numbering ("1/") is the owner's call at post time; each tweet must read
standalone (Sub-rule 3 anchors self-contained).

- **Tweet 1 (hook)**: reader_sentence-adjacent. Compress the README.md `reader_sentence`
  or a declared signature line; do not coin a new hook. No insurance facts before the
  beat. No hashtag pile: hashtags 0; a single `$cashtag` only if the essay itself used
  one. Default attachment lives here (`figure-attachment-policy.md`).
- **Tweet 2 (mechanism/evidence)**: ONE mechanism or evidence beat, carried by one
  concrete number or one verbatim essay quote. Not a second hook, not a list of features.
- **Tweet 3 (verdict + link)**: the essay's two-sided call in one tweet, both halves (the
  call + its guard), then the article pointer ending with `[ARTICLE-LINK]`.

No emoji, no bold markers, no ALL-CAPS words (acronyms and part numbers excepted) in any
tweet.

## Counting methods

- KR 자수: paste block 본문을 그대로 세되 공백 포함, 줄바꿈 제외, `[ARTICLE-LINK]` 는
  23자로 치환해 계산. 예: `printf %s "<본문>" | wc -m` 후 슬롯 보정.
- Digest words: title 줄 제외한 본문 `wc -w`.
- Tweet chars: `printf %s "<tweet>" | wc -c` (English ASCII 기준), 링크 슬롯 23자 보정.
- 측정값을 Verification Status header 와 각 deliverable 의 metadata line 에 그대로
  적는다. "약 300" 같은 추정치 금지.

## Final Checklist

Pack level:

- [ ] Verification Status header 완결, 모든 줄이 측정치 또는 PASS/FAIL
- [ ] Fact trace: 모든 factual phrase 가 세 source 의 문장에 매핑 (`fact-verification.md`)
- [ ] Sub-rule 1 (시점 sequence) / 2 (date arithmetic) / 3 (quote anchor) PASS
- [ ] Em dash 0, bold 0, emoji <=1 (digest closing 슬롯만), 해시태그 0
- [ ] Banned terms 0 (`_shared/scripts/banned_terms.txt`) + Tier-2 tells 점검
  (`_shared/references/anti-ai-writing.md`)
- [ ] Attachment 는 `publication-package/` 경로 + alt-text line
- [ ] `suspected_essay_defects` line 존재 (none 또는 routed; essay 는 안 건드림)

KR post:

- [ ] <=280자 (공백 포함, 링크 슬롯 23자)
- [ ] 문장 1-2 에 discovery beat 압축, 보험성 사실은 beat 뒤
- [ ] 마지막 문장이 아티클 포인터
- [ ] 클릭베이트 의문형 0, 해시태그 0, 이모지 0, 느낌표 0
- [ ] 건조한 평서문, working-dialogue-voice register
- [ ] 영어 인용은 따옴표 안 원문 그대로, 번역은 따옴표 밖
- [ ] 특허번호 / 회사명 / 숫자 / 날짜 원문 일치

EN digest:

- [ ] Title: ALL-CAPS, 12-16 단어, self-contained ("of what?" 의문 안 떠오름)
- [ ] Lede: declarative, 첫 sentence 에 thesis, specific date/number/quote >=1
- [ ] 3, 4, or 5 단락 (essay 복잡도에 맞춤); 단락 1-3 sentences; 문장 <=35 words
- [ ] Word count 280-340 (title 제외)
- [ ] Closing posture 가 essay `closing_posture` 와 합치 (`closing-posture.md`)
- [ ] Universal claims 0, safe-harbor boilerplate 0, colon <=2
- [ ] `[dddd]` anchor / reference numeral / 내부 ID 없음

Thread:

- [ ] 3 tweets, 각 <=280 chars (링크 23자)
- [ ] T1 hook 이 reader_sentence-adjacent, 보험성 사실이 beat 앞에 없음
- [ ] T2 가 하나의 mechanism/evidence beat + 구체 숫자 또는 verbatim quote 1 개
- [ ] T3 가 two-sided verdict + `[ARTICLE-LINK]`
- [ ] 각 tweet standalone-readable (baseline / referent / anaphoric anchor 자급)

## v1 → v2 변경 사항

| 영역 | v1 promo-composer | v2 promo-composer |
|---|---|---|
| Deliverable | EN digest 단일 (promotion-post.md) | promo-pack.md 한 파일에 KR post + EN digest + thread sketch |
| 입력 | handoff/03-edit/essay-final.md | essays/<id>/ 아카이브 (essay-final, publication.md, owner-briefing.md, signature lines, reader_sentence) |
| Strip pipeline | awk marker 추출 → promotion-post.md | fenced paste block 이 strip 경계, 별도 파일 없음 |
| Fact 부재 시 | web search verify 또는 삭제 | 삭제만 (drop, don't fetch) |
| Korean | 폐기 (tech-essay-ko-pub) | KR post 부활 (<=280자, 발행자 목소리); full-article adaptation 은 여전히 폐기 |
| Emoji | 1 회 고정 (🤔 closing) | 팩 전체 <=1, digest closing 슬롯만, 0 허용 |
| Figure source | Layer 1 input/figures 원본 sheet | essays/<id>/publication-package/ (cover-5x2.png default) |
| Digest 구조/제목/lede 규칙 | 3-5 단락, ALL-CAPS 12-16, declarative lede | 동일 (carry-over) |
