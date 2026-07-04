---
essay_id: etched-0378175-memory-in-writing-r2
essay_source: essays/etched-us20240378175-r2/essay-final.md
closing_posture: firm
digest_posture: D
promo_version: 1
owner_briefing: read
---

# Promo pack: etched-us20240378175-r2

=== Verification Status (promo-composer, promo-pack) ===
sources: essay-final.md (draft_version 5, closing_posture firm) + publication-package/publication.md + owner-briefing.md (read)
fact_trace: PASS (every factual phrase mapped to a sentence in the three sources; dropped facts: none)
subrules: 1 sequence PASS (filing May 2023 before pitch late June 2026, relationship explicit in essay ¶1) / 2 arithmetic PASS (the essay's own "three years" span carried verbatim, no self-computed or parallel-structure intervals) / 3 anchors PASS (per-deliverable referent check; venue is "stealth-exit thread" throughout, founder phrasing kept non-exhaustive)
kr_post: 265자/280 (공백 포함, [ARTICLE-LINK]=23자), 문장 4, 아티클 포인터 있음, 의문형 0, 느낌표 0
en_digest: 295w/280-340 (title line excluded), title 15 words ALL-CAPS, 5 paragraphs (1-3 sentences each, max sentence 32w), colon 0, posture D agrees with closing_posture firm
thread: 223/275/234 chars/280 (link slot = 23, in tweet 3), each tweet standalone-checked
hygiene: em-dash 0, bold 0, emoji 0/1, hashtags 0, exclamation 0, banned terms 0 (banned_terms.txt literals + regexes, self-run)
attachments: cover-5x2.png (KR post, tweet 1) + fig-05.png (tweet 2 mechanism sheet, aspect 0.99), alt text verbatim from posting-checklist.md, paths verified present
suspected_essay_defects: none in essay-final.md; owner-briefing.md §⑤ dates the stealth-exit thread "2026년 7월" while essay-final.md and its cited TechCrunch source say late June 2026 (30 June), the month-slip class sa1B-F5 already fixed in the essay; promo follows the essay's dating; routed to the human-post-accept channel (revision-notes.md)
=== Deliverables ===

## 1. Korean promo post (X, <=280자)

```text
Etched가 스텔스 종료 스레드에서 "the best layer is no layer"라고 내세운 메모리 철학은 3년 앞선 2023년 5월, 회사 첫 출원 US 2024/0378175 A1에 청구항 언어로 적혀 있었습니다. 공동창업자 두 사람이 발명자로 서명했습니다. 다만 최종거절 후 RCE로 심사가 계속 중이라 청구 범위는 아직 확정이 아닙니다. 이 문서가 회사 서사와 담보 기록 사이에서 갖는 자리까지 아티클에 정리했습니다. [ARTICLE-LINK]
```

- 자수: 265 (공백 포함, [ARTICLE-LINK]=23자)
- 표현 출처: owner-briefing.md 한 줄 요약("최종거절 후 RCE로 심사가 계속 중", "청구 범위는 확정이 아니다"), §⑤("청구항 언어", "스텔스 종료 스레드"); 발명자 문구는 essay ¶1의 "two of its co-founders had signed" 압축
- attach: publication-package/cover-5x2.png
- alt: "Patent drawing: two memory chips wired straight down into a processor chip, four independent channels, no switch between them."

## 2. English promo digest (280-340 words)

```text
ETCHED'S FIRST PATENT FILING CLAIMS THE NO-SWITCH MEMORY DESIGN THE COMPANY PITCHED THREE YEARS LATER

Three years before Etched pitched "the best layer is no layer" as its memory philosophy, two of its co-founders had signed that idea into the company's very first patent filing. US 2024/0378175 A1, filed 10 May 2023, asks for memory channels wired straight into the columns of a giant multi-chip math array, no switch in between. The public pitch arrived in late June 2026, in the company's stealth-exit thread.

High-bandwidth memory, the stacked memory that feeds modern AI accelerators, exposes its capacity through independent channels that cannot communicate with each other, so a switch, or a crossbar, typically sits in between. The filing's claim 39 deletes it for workloads whose weights never change, hardwiring every memory channel to its own column or columns of the array, "without any switching element". The stated payoff is saved space and power, and the stated trade is that a column can read only its own channel.

The stealth-exit thread made the same idea its memory pillar and named it CSM. The no-layer pitch is not marketing retrofitted onto hardware. It is claim language, dated May 2023.

As of the May 2026 record, the application is still pending, with examination continuing after a final rejection mailed 23 October 2025 and a request for continued examination docketed 24 April 2026. The examiner has assembled eight references against it, with Intel, IBM and Rambus among the assignees. Etched has kept paying anyway, and the filing sits inside the patent stack the company has twice pledged as loan collateral.

Until the patent office says yes, Etched holds a dated, signed statement of the memory idea it pitches, not an exclusive right to it. In the pitch the layer is already gone. At the patent office, Etched is still paying to own the deletion.
```

- words: 295 (title line excluded), title 15 words ALL-CAPS
- structure: 5 paragraphs (lede / mechanism / claim-language beat / pricing / closing), 1-3 sentences each, max sentence 32 words
- closing posture: D. The closing carries the essay's verdict sentence ("Until the patent office says yes...") and its final two sentences (declared signature line 3) word for word; agrees with closing_posture: firm, no open-question or safe-harbor close
- signature lines carried: line 2 verbatim in paragraph 3 (plain, not bold, per promo markdown rules); line 3 verbatim in the closing
- attach: none (post with the article link and let the link card render; media would displace the card per figure-attachment-policy.md)

## 3. Thread sketch (3 tweets)

Sketch level: "1/" numbering is the owner's call at post time; each tweet reads standalone.

Tweet 1 (hook, reader_sentence-adjacent):

```text
Etched wrote the no-switch memory idea into its first patent filing in May 2023, three years before the company pitched "the best layer is no layer" in its stealth-exit thread. The patent office still hasn't said yes to it.
```

- chars: 223/280
- source: README.md reader_sentence, re-punctuated without the em-dash; venue word aligned to the essay's "stealth-exit thread"
- attach: publication-package/cover-5x2.png
- alt: "Patent drawing: two memory chips wired straight down into a processor chip, four independent channels, no switch between them."

Tweet 2 (mechanism beat):

```text
High-bandwidth memory channels cannot communicate with each other, so accelerator designs typically put a switch in between. Etched's first patent filing deletes the switch. Claim 39 hardwires each channel to its own column of the math array, "without any switching element".
```

- chars: 275/280
- attach: publication-package/fig-05.png (mechanism sheet swap per figure-attachment-policy.md: the full FIG. 5 sheet, aspect 0.99, shows the whole channel-to-column path the 5:2 cover band crops)
- alt: "Patent drawing: two memory chips wired straight down into a processor chip, four independent channels, no switch between them."

Tweet 3 (two-sided verdict + link):

```text
Etched holds a dated, signed statement of the memory idea it pitches, not an exclusive right to it. The place to watch is the application's public docket, not the company's thread. Full analysis in the article. [ARTICLE-LINK]
```

- chars: 234/280 ([ARTICLE-LINK] = 23)
- verdict halves: the call (dated, signed statement; authorship) + its guard (not an exclusive right), both from the essay's §6 verdict paragraph; watch pointer is the essay's own docket pointer
