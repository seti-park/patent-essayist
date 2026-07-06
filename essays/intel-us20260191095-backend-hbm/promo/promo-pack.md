---
essay_id: intel-us20260191095-backend-hbm
essay_source: essays/intel-us20260191095-backend-hbm/essay-final.md
closing_posture: measured
promo_posture: D
promo_version: 1
owner_briefing: read
---

# Promo pack: intel-us20260191095-backend-hbm

=== Verification Status (promo-composer, promo-pack) ===
sources: essay-final.md (draft_version 5) + publication-package/publication.md + owner-briefing.md (read)
fact_trace: PASS (every factual phrase in both deliverables maps to a sentence in essay-final.md / publication.md / owner-briefing.md; dropped facts: none)
external_guard: PASS (no ZAM property attributed to the filing; ZAM / Z-angle / hybrid bonding / ~171 mm2 / 2x HBM4 / Powerchip / VLSI 2026 / ~2029 / imec / IGZO channel material all sit in the sources as external-to-filing and are deliberately excluded from both deliverables; the reframe is carried only as a consequence of the back-end-cell move and labeled the essay's reading; 1T1C never called capacitor-less)
subrules: 1 sequence PASS (no before/after/interval expression used) / 2 arithmetic PASS (no date arithmetic used) / 3 anchors PASS (each tweet and each KR paragraph finishable standalone)
bold_selection: KR lead = reader_sentence / signature line 1 압축 (back-end cell reframe: who can make HBM need not stay a three-company club), insurance 1 clause; thread T1 = same reader_sentence / signature line 1 압축, insurance 1 clause (T5, after the call); examination-process narration 0 per deliverable
posture: essay closing_posture measured; promo_posture D (both closings carry signature line 2, "a question of yield, not of architecture"); agreement PASS (no open-question close, no safe-harbor boilerplate, closing sentence is the article pointer not a hedge)
kr_long: 772자 / 400-800 (공백 포함, 줄바꿈 제외, [ARTICLE-LINK]=23자), 5 단락 (문장 2/3/3/3/3), 아티클 포인터로 종료, 의문형 0, 느낌표 0, 이모지 0
thread: 5 tweets, 164 / 240 / 276 / 273 / 240 chars (each <=280, [ARTICLE-LINK]=23), verdict + link in T5
hygiene: em-dash 0, en-dash 0, bold 0, emoji 0/1, hashtags 0, banned terms 0 (literal + regex scan clean), semicolons 0
attachments: fig-01B.png (KR post + T1; cover source sheet, 5:2 feed crop applied at publish time per posting-checklist.md), fig-01F.png (T2, mechanism beat); alt lines below each block
suspected_essay_defects: none
=== Deliverables ===

## 1. Korean long-form promo post (X, 400-800자)

```text
인텔의 새 메모리 출원은 DRAM 셀을 로직 위에 쌓을 수 있는 백엔드 배선층으로 옮긴다. 수율 숫자만 맞으면, HBM을 누가 만들 수 있느냐가 더 이상 3사만의 클럽이 아니게 된다.

보통 DRAM은 다이 맨 아래 결정질 실리콘 전공정에 트랜지스터를 새겨 만든다. 이 출원은 그 트랜지스터를 위에 저온으로 쌓은 금속 배선층, 곧 후공정(백엔드)에 박막 트랜지스터로 올린다. 청구항 1이 실제로 요구하는 단어는 "backend" 하나다.

셀은 여전히 1T1C, 트랜지스터 하나에 커패시터 하나짜리 통상의 DRAM이다. 백엔드로 옮겨도 커패시터는 사라지지 않고 그대로 따라 올라간다. 명세서는 이런 다이를 0.5-5 GB로 설계해 8단 이상 쌓고, TSV 거터와 UCIe 베이스 다이로 묶어 HBM4의 풋프린트에 맞추는 것을 목표로 한다.

백엔드 트랜지스터는 저온 배선에서 만들어져 전용 DRAM 팹만 돌리는 결정질 실리콘 전공정이 필요 없다. 그래서 로직과 패키징을 이미 가진 파운드리가 원리상 HBM급 메모리를 세 공급사에서 사오는 대신 자기 라인으로 만들 수 있다. 청구항 1은 "backend"만 말할 뿐 파운드리도 로직 팹도 말하지 않고, 여기까지는 그 단어에서 읽어낸 해석이다.

셀이 백엔드에 있다는 것, 그 하나는 이 출원이 정했다. 그것이 HBM으로 가는 네 번째 길이 되느냐는 이제 아키텍처가 아니라 수율의 문제다. 아직 출원 단계이고 공개된 수치는 없다는 것, 그리고 어디까지가 문서이고 어디부터가 해석인지까지 아티클에 정리했다. [ARTICLE-LINK]
```

- 자수: 772 (공백 포함, 줄바꿈 제외, [ARTICLE-LINK]=23자)
- attach: publication-package/fig-01B.png (cover source sheet; crop to 5:2 at publish time, excluding the sideways USPTO header band, per posting-checklist.md)
- alt: "FIG. 1B: the claimed eight-high memory stack on its base die."

## 2. English thread (3-5 tweets)

```text
Intel's newest memory filing moves the DRAM cell into logic-stackable back-end layers. If the yield numbers land, who can make HBM stops being a three-company club.
```

- chars: 164 / 280
- attach: publication-package/fig-01B.png (cover source sheet; 5:2 crop at publish time)
- alt: "FIG. 1B: the claimed eight-high memory stack on its base die."

```text
Normally the transistor in a DRAM cell is etched into crystalline silicon at the base of the die, the front-end. This filing builds it up in the back-end wiring as a thin-film transistor instead. Claim 1 as filed turns on one word, backend.
```

- chars: 240 / 280
- attach: publication-package/fig-01F.png (mechanism beat, the back-end cell)
- alt: "FIG. 1F: the back-end cell made literal. An exploded view shows the tiers labeled TRANSISTOR, the thin-film transistors that switch each cell."

```text
A back-end transistor is built in the low-temperature wiring, so it skips the crystalline-silicon front-end only a dedicated DRAM fab runs. A foundry that owns logic and packaging could carry HBM-class memory itself. Claim 1 says backend, not foundry. The leap is the essay's.
```

- chars: 276 / 280

```text
The honest part is what the filing keeps. This is still a 1T1C cell, one transistor and one capacitor. The back-end move relocates DRAM's hardest part to shrink, the capacitor. It does not remove it. A back-end capacitor at HBM density and yield is what no one has shipped.
```

- chars: 273 / 280

```text
The cell is settled in the back-end. Whether that becomes a fourth path to HBM is now a question of yield, not of architecture. Still one published application, no public numbers yet. The full read is in the article. [ARTICLE-LINK]
```

- chars: 240 / 280 ([ARTICLE-LINK]=23)
