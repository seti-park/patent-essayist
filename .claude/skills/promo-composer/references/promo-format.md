# Promo format: the promo-pack contract + per-deliverable rules

One file, two paste-ready deliverables. v3 supersedes v2's three-deliverable pack
(KR short post + EN digest + 3-tweet sketch): the pack now carries (1) a **Korean
long-form promo post** (400-800자, the publisher's primary channel) and (2) an **English
thread** (3-5 tweets). The EN digest is dropped as a deliverable; its paragraph/lede
craft migrates into the KR long post spec below. v2's grounding, counting, and hygiene
machinery is carried intact.

## The bold-selection rule (promo leads bold; the article hedges)

Owner decision, 2026-07-05 (class `promo-safe-harbor-overweight`): the promo's job is
the **boldest claim the essay's evidence supports**. Readers meet the promo first and
want the strong version; the article is where the claim gets priced, bounded, and
risk-hedged — the promo points there for exactly that reason.

- **Boldness comes from SELECTION, never fabrication.** The hook vocabulary is the
  protected surface (reader_sentence, signature lines, title, lead ¶1, closing call);
  pick the strongest of those lines and lead with it. The safe-claims defense is
  unchanged: every factual phrase still traces to the three sources, verbs of certainty
  stay verbatim-consistent (an application-era essay's "asks for" never becomes
  "patented"). Bold and grounded are not in tension: selection does the work.
- **Insurance budget: at most ONE status clause per deliverable**, positioned AFTER the
  bold beat, only when the essay's two-sided call requires it — and phrased as a fact
  with tension ("the patent office hasn't said yes yet"), never as a safe-harbor
  disclaimer ("다만 ... 확정이 아닙니다" 류 유보 마무리 금지).
- **Process narration 0.** Examination mechanics (최종거절, RCE, office actions), fees,
  liens, collateral walks are ARTICLE material, never promo material. The promo may
  point at them ("특허청 문턱에서 어디에 서 있는지까지 아티클에 정리했습니다"); it does
  not narrate them. This is the attention-budget doctrine
  (`_shared/references/reader-energy.md` §6) applied at promo altitude, where the budget
  is stricter than the essay's: the promo is 100% payload plus one status clause.
- **Hedge inheritance is one-way.** The promo must not OVERREACH the essay (never assert
  beyond it), but it also does not INHERIT the essay's in-body hedges: the essay hedges
  because it argues; the promo selects because it invites. Posture agreement
  (`closing-posture.md`) applies to the CLOSING call only.
- **Briefing reuse is vocabulary-only.** `owner-briefing.md` is an owner-comprehension
  document — its stance sentences carry insurance by design. Reuse its 검수된 기술
  어휘 (무스위치 하드와이어링, 채널-열 직결, 결합 어레이 등); never reuse its hedge/
  status SENTENCES as promo copy (v1 promo inherited "다만 ... 확정이 아닙니다" exactly
  this way).

## The promo-pack.md contract

Path: `essays/<id>/promo/promo-pack.md`. Structure, in order:

1. **YAML frontmatter**: `essay_id` (copied from essay-final.md frontmatter),
   `essay_source`, `closing_posture` (copied from essay-final.md), `promo_posture`
   (A/B/C/D per `closing-posture.md`; applies to both deliverables' closes),
   `promo_version`, `owner_briefing` (`read` or `ABSENT`).
2. **Verification Status header** between `=== Verification Status (promo-composer,
   promo-pack) ===` and `=== Deliverables ===` markers. Every line is a measured number
   or PASS/FAIL, never a bare checkmark: sources read, fact_trace + dropped-facts list,
   Sub-rules 1/2/3, per-deliverable counts, posture agreement, **bold-selection line**
   (which protected line leads each deliverable + insurance-clause count per
   deliverable), hygiene tallies, attachment list, `suspected_essay_defects` (default
   `none`).
3. **Two deliverable sections** (`## 1.` KR long post, `## 2.` EN thread). Each section
   = one or more fenced ```` ```text ```` blocks (the paste surface) followed by plain
   metadata list lines (counts, attach path, alt text).

**The fence is the strip boundary.** Nothing outside a fence is ever pasted, everything
inside a fence is paste-ready exactly as written. No separate publication file exists
for promo.

Pack-wide hygiene: em-dash 0 and bold 0 anywhere in the file (scaffolding included, so a
sloppy copy can never smuggle formatting into a post); emoji <=1 total; hashtags 0;
banned-term discipline per `_shared/scripts/banned_terms.txt`.

## Deliverable 1: Korean long-form promo post

발행자가 자기 아티클을 소개하는 X 장문 포스트 (프리미엄 장문). 한 개의 fenced block.
v2 의 280자 단문을 대체한다. 발행자의 주 채널이므로 pack 의 첫 deliverable 이다.

- **분량**: 400-800자, 공백 포함, `[ARTICLE-LINK]` 슬롯은 23자로 계산 (X 의 t.co 단축
  길이). 280자 단문이 아니라 장문이다: 기술의 핵심 그림 하나를 온전히 설명할 공간이
  생겼으므로, 그 공간은 기술에 쓴다.
- **목소리**: `_shared/references/working-dialogue-voice.md` register. 건조한 평서문,
  과장 배제, 발행자 1인칭 허용 (절제해서). 건조함과 대담함은 양립한다: 대담함은 수식어가
  아니라 문장 선택에서 나온다 (bold-selection rule).
- **구조 (3-5 단락, 단락당 1-3 문장)** — v2 digest 의 단락 아크를 한국어로 이식:
  - **¶1 훅**: 에세이의 가장 대담한 지지 가능 문장의 한국어 압축 (reader_sentence 또는
    signature line). 첫 문장만 읽어도 글이 무엇인지 안다. 보험성 사실 0.
  - **¶2(-3) 메커니즘**: 발명이 무엇을 하고 무엇을 바꾸는지. 구체 숫자/날짜/verbatim
    인용 1개 이상. 에세이 기술 섹션의 압축이지 심사/재무 섹션의 압축이 아니다.
  - **¶3(-4) 함의/receipts**: thesis 를 landing 하는 bold 비트 (signature line 압축이
    가장 강하다).
  - **마지막 ¶**: 아티클 포인터로 끝난다. 허용된 ONE status clause 는 여기 또는 함의
    단락에, 포인터와 결합해 배치하는 것이 기본형 ("특허청 문턱에서 지금 어디에 서
    있는지까지 아티클에 정리했습니다" + `[ARTICLE-LINK]`).
- **Insurance budget**: status clause 최대 1 (bold-selection rule). 심사 절차 서사
  (최종거절, RCE, 담보) 0. "다만/그러나 + 유보" 형 마무리 금지.
- **금지**: 클릭베이트 의문형 후킹 ("과연?", "어떻게 됐을까요?" 류), 해시태그, 볼드,
  em dash. 감탄사와 느낌표도 쓰지 않는다. 이모지는 팩 예산 <=1 의 슬롯이 이 포스트의
  마지막 문단에만 있다 (0 이 자연스러우면 0).
- **Protected terms verbatim**: 특허번호, 회사명, 부품번호, 영어 인용구는 원문 그대로.
  따옴표 안은 영어 원문을 유지하고 번역은 따옴표 밖에 둔다 (briefing 과 같은 규율).
- **한국어 표현의 출처**: 기술 어휘는 `owner-briefing.md` 의 검수된 표현을 우선 재사용;
  stance/hedge 문장은 재사용 금지 (bold-selection rule). briefing 이 없으면 에세이의
  protected lines 를 직역하되 숫자/날짜/이름은 원문과 일치시킨다.

## Deliverable 2: English thread (3-5 tweets)

English. One fenced block per tweet, each <=280 chars (`[ARTICLE-LINK]` = 23). Sketch
level: numbering ("1/") is the owner's call at post time; each tweet must read
standalone (Sub-rule 3 anchors self-contained).

- **Tweet 1 (bold hook)**: the boldest supportable line, compressed from the protected
  surface (reader_sentence / signature line / title beat); do not coin a new hook. NO
  insurance facts anywhere in tweet 1. No hashtag pile: hashtags 0; a single `$cashtag`
  only if the essay itself used one. Default attachment lives here
  (`figure-attachment-policy.md`).
- **Middle tweets (1-3 of them: mechanism / evidence / receipts)**: ONE beat each,
  carried by one concrete number or one verbatim essay quote. Not a second hook, not a
  list of features. A receipts beat (the dated-authorship / claim-language beat) is
  usually the strongest middle tweet for filing-vs-narrative essays.
- **Final tweet (verdict + link)**: the essay's call, call-first; the ONE permitted
  status clause may ride here after the call (never qualifier-first), then the article
  pointer ending with `[ARTICLE-LINK]`.

No emoji, no bold markers, no ALL-CAPS words (acronyms and part numbers excepted) in
any tweet.

## Hedge 정책 (bold-selection rule 의 표)

| Hedge 영역 | Promo 규칙 |
|---------|-----|
| Overreach (essay 보다 센 단정) | 0 건 — verbs of certainty 는 essay 와 verbatim-consistent |
| Essay 본문 hedge 의 상속 | 상속하지 않는다 — promo 는 선택하는 장르다; hedge 는 아티클의 몫 |
| Status clause | deliverable 당 최대 1, bold beat 뒤, 유보 마무리 금지 |
| 심사 절차 서사 (거절/RCE/담보) | 0 건 — 아티클 포인터로만 가리킨다 |
| Safe-harbor boilerplate | 0 건 ("a patent doesn't guarantee..." 류, `closing-posture.md` 회피 목록) |
| Universal claims / "significantly" 류 | 0 건 (essay 와 동일) |
| 시점 표현 | 정확성 필수 + `fact-verification.md` Sub-rule 1, 2 |

Essay 에 명시 없는 fact 는 promo 에 넣지 않는다 (drop, don't fetch — 불변).

## Counting methods

- KR 자수: paste block 본문을 그대로 세되 공백 포함, 줄바꿈 제외, `[ARTICLE-LINK]` 는
  23자로 치환해 계산. 예: `printf %s "<본문>" | wc -m` 후 슬롯 보정.
- Tweet chars: `printf %s "<tweet>" | wc -c` (English ASCII 기준), 링크 슬롯 23자 보정.
- 측정값을 Verification Status header 와 각 deliverable 의 metadata line 에 그대로
  적는다. "약 500" 같은 추정치 금지.

## Final Checklist

Pack level:

- [ ] Verification Status header 완결, 모든 줄이 측정치 또는 PASS/FAIL
- [ ] bold_selection line: 각 deliverable 의 리드가 어느 protected line 압축인지 +
      insurance clause 수 (<=1/deliverable, 절차 서사 0)
- [ ] Fact trace: 모든 factual phrase 가 세 source 의 문장에 매핑 (`fact-verification.md`)
- [ ] Sub-rule 1 (시점 sequence) / 2 (date arithmetic) / 3 (quote anchor) PASS
- [ ] Em dash 0, bold 0, emoji <=1 (KR post closing 슬롯만), 해시태그 0
- [ ] Banned terms 0 (`_shared/scripts/banned_terms.txt`) + Tier-2 tells 점검
  (`_shared/references/anti-ai-writing.md`)
- [ ] Attachment 는 `publication-package/` 경로 + alt-text line
- [ ] `suspected_essay_defects` line 존재 (none 또는 routed; essay 는 안 건드림)

KR long post:

- [ ] 400-800자 (공백 포함, 링크 슬롯 23자)
- [ ] ¶1 첫 문장이 가장 대담한 지지 가능 주장의 압축, 보험성 사실 0
- [ ] 메커니즘 단락이 기술을 설명 (심사/재무 압축 아님), 구체 숫자/날짜/인용 >=1
- [ ] status clause <=1, bold beat 뒤, "다만+유보" 마무리 아님; 절차 서사 0
- [ ] 마지막 문장이 아티클 포인터
- [ ] 클릭베이트 의문형 0, 해시태그 0, 느낌표 0, 이모지 <=1 (마지막 문단만)
- [ ] 건조한 평서문, working-dialogue-voice register
- [ ] 영어 인용은 따옴표 안 원문 그대로, 번역은 따옴표 밖
- [ ] 특허번호 / 회사명 / 숫자 / 날짜 원문 일치; briefing hedge 문장 재사용 없음

Thread:

- [ ] 3-5 tweets, 각 <=280 chars (링크 23자)
- [ ] T1 이 boldest-supportable hook, 보험성 사실 0
- [ ] 중간 tweet 각각이 하나의 beat + 구체 숫자 또는 verbatim quote 1 개
- [ ] 마지막 tweet 이 call-first verdict (+ status clause <=1, call 뒤) + `[ARTICLE-LINK]`
- [ ] 각 tweet standalone-readable (baseline / referent / anaphoric anchor 자급)

## v2 → v3 변경 사항

| 영역 | v2 promo-composer | v3 promo-composer |
|---|---|---|
| Deliverable | KR 단문 (<=280자) + EN digest (280-340w) + 3-tweet sketch | KR 장문 (400-800자) + EN thread (3-5 tweets); EN digest 폐기 (owner 결정 2026-07-05) |
| Hedge 자세 | digest hedge 강도 = essay 와 동일 | bold-selection rule: promo 는 boldest-supportable 을 리드, insurance <=1 clause/deliverable, 절차 서사 0; hedge 는 아티클의 몫 |
| Briefing 재사용 | 문장 표현 우선 재사용 | 기술 어휘만 재사용; stance/hedge 문장 재사용 금지 |
| Posture 필드 | `digest_posture` | `promo_posture` (양 deliverable 의 closing 에 적용) |
| 작성 모델 | (명시 없음) | posting copy 는 세션 최강 모델이 직접 작성 (`model: inherit`, 절대 하위 모델로 pin 금지) — 검증 절차만 위임 가능 |
| Grounding / counting / hygiene | safe-claims defense, 측정 의무, em-dash/bold/hashtag 0 | 동일 (carry-over, 불변) |

v1 → v2 변경 이력은 git history 의 이 파일 이전 판 참조.
