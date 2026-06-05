---
name: patent-thread
description: "Write a fast, single-patent X (Twitter) thread in SETI's expert-register voice, Korean draft first, optionally published in English, with a public/subscriber two-branch split. Use whenever the user asks for a thread, X thread, 스레드, 타래, quick take, or a lightweight patent post, even without the word 'thread'. Picks one of three archetypes (Champion, Roadmap-read, Decode) by coverage intent. NOT a long-form essay (that is the 4-Phase Compose pipeline) and NOT a promo digest."
---

# patent-thread

단일 특허를 빠르고 밀도 높은 X Thread로 만든다. 한글 초안을 먼저 내고(검토 게이트), 발행 언어를 스레드마다 고른다(KO / EN).

목적은 투자자에게 (1) 보유 종목 확신, (2) 고민 중인(미보유) 핫 종목의 기술력 인지, (3) 새 종목 소개를 주는 것. buy/sell 추천이 아니다.

## Register

이 스킬의 voice는 **expert 단일 register**다. 독자가 기술 투자자이고 소재가 심층 기술 특허라, 용어를 풀어 쓰기보다 정밀을 지킨다. 원어·한자어 기술용어 보존, 명세서 어법 허용, 긴 설명형 복문 허용. 상세는 `references/thread-voice.md`. (명세서 어법 *허용*이 행위자 흐리기 *허가*는 아니다. Gotchas 참고.)

## Inputs
- 특허: `patent.md`, 붙여넣은 텍스트, 또는 원본 PDF (PDF는 Code 환경 only, `patent-pdf-to-md`로 변환. Claude.ai는 변환본 붙여넣기).
- 티커 (예: $TSLA, $PENG).
- coverage intent (= 아키타입 결정 입력): 보유 확신 / 고민중·미보유 기술력 / 신규 소개 / 장기 보유자 방향성.
- (선택) 발행 언어 선호 (KO / EN, 초안 후 변경 가능), 각도 선호, 완전공개 여부, cleaned figures.

## Process

1. **Intake**: 위 입력 확인. 부족하면 체크리스트 제시 후 대기.
2. **Archetype + 구조 제안**: `references/archetypes.md` 결정표(coverage intent 키)로 1 모드 + 1줄 근거 → 사용자 확인. two-branch 구조 확인(공개 스레드 단독 완결 + 구독 브랜치, 또는 완전공개 override). register는 expert 고정이라 선택 단계 없음.
3. **Read & extract**: 핵심 발명(what/how/why-novel), 가장 날카로운 hook 1개, 특허 근거 anchor 2-4개. anchor는 그 특허 자체의 convention (상세 `references/rigor.md`).
4. **Rigor pass**: Tier 1/2/3 분리. Decode / 신규 / 미보유 unfamiliar ticker면 Tier-1 gate 체크리스트 + no-buy-read 가드 (`references/rigor.md`).
5. **한글 초안 작성**: `outputs/{PATENT}/thread/thread.ko.md`. 구조는 공개 스레드(hook → 메커니즘 → 아하 + edge 존재 → 열린 close 🤔) → `🔒` 헤더 → `S#/` 구독 브랜치(노력형 종합). 밀도 높은 post, 티저 없음. 작성 중 함께 적용: voice = `references/thread-voice.md`(expert), 한글 anti-AI tell = `references/korean-anti-ai.md`, 인과·논리 = `references/causality.md`, 구조 craft = `references/craft.md`. figure는 `outputs/{PATENT}/figures/` 클린본 재사용(없고 Code면 `patent-figures-clean`), post당 최대 4장.
6. **검토 게이트**: 사용자가 한글 초안으로 품질·완성도 확인·승인. Decode / 신규 / 미보유면 여기서 핵심 사업 해석 sign-off 겸함.
7. **발행 분기**:
   - **KO**: `thread.ko.md`를 발행본으로 확정(다듬기). 언어 무관 규칙(em-dash·인용-해석 pair·격언조 분포·no puffery) 점검.
   - **EN**: 승인된 한글 초안의 voice 보존 영어 적응(직역 아님) → `thread.en.md`. 영어 thread register 적용. 번들 스크립트 `scripts/anti_ai_lint.py`로 EN 본문 금지어 린트(`python scripts/anti_ai_lint.py <thread.en.md>`, exit 0 = 통과; 금지어는 `references/anti-ai-writing.md`에서 읽음).
8. **Self-check + Output**: `references/thread-format.md` 체크리스트 통과. 산출물은 `thread.ko.md` (+ EN 발행 시 `thread.en.md`), 넘버링 post + `🔒` 헤더 + `S#/` + 인라인 `[verify:]`/`[추론]` 라벨.

## Gotchas

작성 중 가장 자주 어긋나는 지점. 실패 사례에서 모음. 새 케이스는 누적한다.

- **expert ≠ 명세서 어법 남발.** 명세서 주어법("본 특허는 ~에 관한 것입니다")은 *허용*이지 행위자를 흐리라는 *허가*가 아니다. 행위자를 또렷이 하는 craft가 register 관습에 우선한다 (`references/craft.md` S2). expert라도 누가 무엇을 하는지 또렷이.
- **calibration 통과 ≠ 논리 구조 통과.** "~수 있습니다"를 적절히 넣어 헤징 점검을 통과해도, 빠진 보증·뒤집힌 인과 같은 *구조* 결함은 그대로 남는다. 인과·논리는 `references/causality.md`가 따로 본다.
- **anchor는 그 특허 자체의 convention만.** 외부 비교·업계 통념을 anchor처럼 쓰지 않는다. 쓰려면 Tier 표시 (`references/rigor.md`).
- **Decode·신규·미보유는 매수추천처럼 안 읽히게.** 정체를 해독하되 "사라" 톤이 새어들지 않게. no-buy-read 가드 (`references/rigor.md`).

## Voice 가드 (register 우선, 특히 검토 게이트 Step 6)
사용자(voice 설계자)가 기준 문서와 다른 문체를 직접 쓰거나 반복 제시하면, `korean-anti-ai` 룰로 되돌리기 전에 그것이 의도된 voice 선택인지 먼저 확인한다. 사용자가 직접 쓴 텍스트는 기준과 충돌해도 즉시 무효화하지 않는다. deliverable voice의 최종 권한은 SETI다(규칙 문서는 가이드). 단 이 우선권은 문체에만 적용한다. no-buy-read 가드·Tier 분리·anchor·정확성·안전 가드는 voice 선호와 무관하게 유지 (`references/rigor.md` · `references/causality.md`).

## References
- `references/archetypes.md`: 3 모드 (Champion / Roadmap-read / Decode), coverage-intent 결정표, 3목적 매핑, tie-break.
- `references/thread-format.md`: X 메커닉, two-branch 구독 모델, emoji whitelist, 도면(≤4/post), KO/EN 출력 포맷, self-check.
- `references/thread-voice.md`: thread register (voice-profile delta). expert 단일 register 정의.
- `references/korean-anti-ai.md`: 한글 초안 anti-AI tell 체크리스트 (judgment self-check; `anti-ai-writing.md`의 한글 대칭). SETI 재조정 박스 포함.
- `references/anti-ai-writing.md`: 영어 본문 anti-AI 금지어·패턴 (EN canonical, `anti-ai-lint` 기준).
- `references/rigor.md`: 3-tier (가설→근거문서→현실) + Decode/신규/미보유 gate + no-buy-read 가드 + anchor 규칙 + hard nos. (출처 위계.)
- `references/causality.md`: 인과·논리 게이트 (보증·귀속·방향·상관/인과). rigor의 논리 짝. 작성 중 + 검토에서 적용.
- `references/craft.md`: 구조 craft (구정보→신정보, controlling idea+전개, 원자→종합). 작성 중 구조 예방.

## Hard nos
buy/sell call (Q47: 미보유·고민중·신규는 매수추천처럼 안 읽히게, `references/rigor.md` no-buy-read 가드), 인지하는 진실 왜곡 (Q95), 가정 2중 적층 (Q71), 비-1차 숫자 (Q84), 본문 disclaimer (Q32).

## Out of scope
장문 essay (별도 essay 파이프라인), promo digest (별도 promo 트랙), editorial 6-pass (별도 edit 단계), deep handoff 의존 (단 `invention-summary.md` 존재 시 기회적 재사용 허용).
