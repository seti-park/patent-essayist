# US 18/635,524 + US 18/678,647 — HBF 고속판독의 두 메커니즘 (always-on bit line / discharge-free read) · essayist 컨텍스트

> 시리즈 위치: **프리퀄 Episode II — "무엇이 HBF를 빠르게 하나"(핵심 기능)**. *두 특허를 한 편으로 묶음*
> (열=비트라인 / 행=워드라인의 대칭 쌍).
> ⚠️ **두 건 모두 전문 미독** — 근거는 (요약)·(대표청구항)·서지. 단락앵커 불가. 전문으로 교차검증.

## 0. 식별정보 (cite-safe)
**A) US 18/635,524** — "A High Bandwidth Memory Device With Always On Bit Lines" (항상 비트라인을 가진 고대역폭 메모리)
- 공개 US 2025/0322885 A1 · 공개 2025-10-16 · 출원 2024-04-15 · 출원인 SanDisk Technologies, Inc.
- 발명자 Xiang Yang, Wei Cao, Deepanshu Dutta · Family 106436033 · CPC **G11C-0016/26**(read), 11/5642(MLC), 16/0483, 16/24, 16/32 · 분류 read-sensing
- ★ **#1(18/748,826) 명세서가 직접 인용** ([0205] "…ALWAYS ON BIT LINES…incorporated by reference")

**B) US 18/678,647** — "Discharge-Free Read Operations for High Bandwidth Nonvolatile Memory Devices" (고대역폭 비휘발성 메모리용 무방전 판독)
- 공개 US 2025/0279143 A1 · 공개 2025-09-04 · 출원 2024-05-30 · 출원인 SanDisk Technologies, Inc.
- 발명자 Wei Cao, Xiang Yang, Jiahui Yuan, Deepanshu Dutta, Richard New · Family 105250448 · CPC **G11C-0016/26**, 11/5642, 16/0483, 16/08, 16/102, 16/32 · 분류 read-sensing
- 상태(둘 다) 미국 공개출원(등록 아님). 발명자 **Yang·Cao·Dutta 중첩** = 동일 HBF read 팀.

## 1. TL;DR — 한 줄 논지
HBF가 HBM급 read 대역폭을 내는 비결은 **연속 판독 사이의 충·방전 오버헤드 제거** — A는 **비트라인(열)을 0V로 안 내리고 양전압 유지**, B는 **선택안된 워드라인(행)을 방전 안 하고 read-pass 전압 유지**. 두 축에서 같은 원리.

## 2. 문제·배경 (도입부 재료)
- 종래 NAND read는 매 판독마다 비트라인 프리차지/방전, 워드라인 바이어스 설정/해제를 반복 → **이 셋업·리커버리 시간이 연속 read의 throughput과 전력을 갉아먹음**.
- AI 가중치처럼 **같은 데이터를 초고속·반복 read** 하는 워크로드(=HBF의 주 용도)에선 이 오버헤드가 치명적. → "사이사이 안 내린다"는 발상.

## 3. 핵심 메커니즘 (요약·대표청구항 기준)
**A) Always-On Bit Lines (18/635,524)**:
- 비트라인 세트를 **0V보다 큰 제1 전압**으로 둔 채 제1 블록 read → **그 전압에서 다운램핑(방전) 없이** 곧바로 제2 블록 read 수행 (요약·대표청구항1).
- 효과: 블록 간 비트라인 재충전 시간 제거 → read 처리량↑·전력↓.

**B) Discharge-Free Read (18/678,647)**:
- 메모리 블록의 **선택되지 않은 워드라인들을 read-pass 전압으로 바이어스**한 상태에서 제1 셀 read → **그 워드라인들을 방전하지 않고** read-pass 전압을 유지한 채 제2 셀 read (요약·대표청구항1).
- 명시 한정: "선택안된 워드라인은 제1·제2 판독 *동안 그리고 그 사이* 방전되지 않고 read-pass 전압 유지" (요약).
- 효과: 워드라인 바이어스 셋업/리커버리 제거 → 연속 read throughput↑·전력↓.

**대칭 구조(에세이 핵심 도식)**: A=비트라인(열 방향), B=워드라인(행 방향). 둘을 합치면 read에 필요한 두 전극축 모두에서 "유지(always-on)" 전략 → HBF 대역폭의 물리적 토대.

## 4. 청구항 구조
- **A 대표 독립항1(방법)**: 평면 준비 → 제1전압(>0V) 유지하며 제1블록 read → 다운램핑 없이 제2블록 read.
- **B 대표 독립항1(장치)**: 블록+제어회로; 선택안된 WL을 read-pass로 바이어스한 채 제1셀 read → 방전 없이 제2셀 read; WL은 두 read 동안·사이에 read-pass 유지.
- **넓이/관찰**: 둘 다 "사이에 내리지 않는다"는 단일 동작특징이 핵심 한정 — *좁지만 명확한 디바이스 동작 클레임*. 회피=사이에 방전하는 종래 read(=성능 손해 감수). 종속항(전압값·MLC·타이밍)은 전문 확인 요.

## 5. 검증된 사실·수치 (cite-safe)
| 항목 | A 18/635,524 | B 18/678,647 |
|---|---|---|
| 유지 대상 | 비트라인(열) | 선택안된 워드라인(행) |
| 핵심 동작 | 제1전압(>0V) 유지, 다운램핑 없이 연속 read | read-pass 전압 유지, 방전 없이 연속 read |
| CPC 핵심 | G11C-0016/26(read) | G11C-0016/26(read) |
| #1 인용 | ✅ ([0205]) | (미확인 — 전문 확인) |
> 구체 전압값(예: #1의 Vread 2.4V, VBL 0.15V)은 *#1 명세서* 값이며 본 두 건의 수치는 전문 확인 전 인용 금지.

## 6. 시장·경쟁 맥락 (외부 — "검증요")
- read 오버헤드 제거는 NAND read 대역폭 향상의 정공법 — 타사 기법 비교는 외부·검증요.
- #1의 "positive sensing / 저전압화 / in-place read refresh"와 **한 묶음의 read 설계 철학**: HBF는 *쓰기*가 아니라 *반복 read* 최적화 디바이스라는 점을 보여주는 가장 좋은 증거.

## 7. 에세이 앵글
1. **"내리지 않는 기술"** — 충·방전을 생략한다는 단순한 발상이 어떻게 대역폭·전력을 동시에 잡나(열·행 대칭).
2. **"읽기 위해 태어난 메모리"** — HBF가 쓰기(P/E)보다 *반복 read*에 최적화됐음을 디바이스 레벨로 입증.
3. **#1과의 직접 연결** — #1이 인용한 18/635,524를 깊이 파서, 응용(LoRA)과 디바이스(read) 사이의 인용 사슬을 드러내기.

## 8. 인용 가능한 직접 문장 (요약, 번역본 — 원문 확보 후 교체)
- (A) "상기 비트 라인을 상기 제 1 전압으로부터 다운 램핑하지 않고 … 제 2 메모리 블록에 대해 제 2 판독 동작을 수행" (요약)
- (B) "선택되지 않은 워드 라인들은 방전되지 않고, 제1 판독 동작 및 제2 판독 동작 동안 그리고 그 사이에서 판독 패스 전압으로 바이어스된 채로 유지된다." (요약)
> 영문 정식 인용은 전문에서 원문 문장으로 교체할 것.

## 9. 용어집
- **비트라인(BL)/워드라인(WL)**: NAND 셀의 열/행 전극.
- **read-pass 전압(Vread)**: 비선택 WL에 인가해 스트링을 도통시키는 전압.
- **프리차지/다운램핑/방전**: read 전후 전극 전압을 올리고 내리는 동작(=오버헤드 원천).
- **always-on / discharge-free**: 그 전압을 read 사이에도 내리지 않고 유지하는 전략.

## 10. 가드레일 — 단정·과장 금지
- **두 건 전문 미독** — 동작 디테일·전압값·종속항은 전문 확보 후 검증. [3·4] 일부는 요약 기반 요지.
- **출원 단계** — granted 아님.
- 두 건은 **별개 특허**(BL vs WL) — "하나의 특허"로 합치지 말 것. 한 *에세이*로 묶을 뿐.
- 구체 전압수치를 #1에서 끌어와 본 두 건 값으로 단정 금지(특허별 실시예 다를 수 있음).
- "대역폭 X% 향상" 같은 정량 효과는 요약에 없음 — 만들지 말 것.

## 11. 확장용 관련 특허
- 정의: **KR 10-2026-7011303**(같은 발명자 Yang/Dutta) · 공정: **KR 10-2026-7011302** · 통합: **US 18/519,210**
- 응용(공개됨): #1 **US 18/748,826**(본 기능을 인용), #2 **US 18/977,519**
- 관련 read/디바이스: **US 18/420,719**(고용량 고대역폭 NVM, TSV 직결)

---

## RUN NOTES (orchestrator addendum, 2026-06-20) — English

**Deliverable for this run.** A SETI narrative essay (standard pipeline voice + X-Articles
format) whose *throughline* is the question a tech investor actually has: **does SanDisk hold a
technical moat here, or just a marketing story?** The moat verdict is the implication section
and the closing, not the hook.

**Hook (Q7 gate).** `technical-impossibility`. The reader's reasonable objection is stated by
the patent itself: NAND is "significantly less expensive than DRAM, but the bandwidth … is too
low, and the power consumption … is too high to provide a viable alternative to HBM" ('885
[0005]). The resolution: you do not pay the per-read setup/recovery tax — you stop ramping the
array down between reads.

**Two patents, one essay.** '885 (US20250322885A1) holds the **bit lines** (columns) up;
'143 (US20250279143A1) holds the unselected **word lines** (rows) up. Column + row = both
electrode axes of the NAND array. That symmetry is the essay's central image. Keep them as two
distinct filings — do not merge them into "one patent."

**Full text now read.** Unlike the cite-safe notes above (written before the full texts were
available), the run has both specifications in full. The previously-unverifiable numbers are
now confirmed from the filings' own embodiments and are safe to cite: VBL ≈ 0.2 V, 25% floor,
sub-1-µs settling ('885 [0147]-[0148]); the adaptive non-discharging trigger on a detected read
burst ('143 [0181]-[0182]). Still do NOT invent quantitative bandwidth-gain percentages — the
filings give none.

**Figures.** See `input/figures-source-map.md`. Use essay-local Figure 1-6 only; cite each
figure's source by patent shorthand + paragraph anchor, never by a literal source "FIG. N".

**External context: include, but fenced + sourced.** A moat is comparative, so the essay may
reach beyond the filings (Western Digital→SanDisk spinoff; the HBF program; HBM cost/supply;
the forward citation chain to SanDisk's application patents). Every such claim is fenced as
"not inside the filing," carries a `# Sources` entry, and is dated. See the fact-check-log
external-fact block (populated from a sourced research brief). Where a fact cannot be verified,
say so rather than asserting it.

**Moat verdict — be honest, not bullish.** The strongest reading: each independent claim is a
*narrow, single-feature device-operation claim* ("do not ramp/discharge between reads"), which
is easy to design around — by accepting the very performance loss the patent exists to avoid.
The durable moat is not any one claim; it is the *combination* (both axes + an adaptive
trigger), the *portfolio depth* (same read team, a citation chain into application patents,
continuations), and the head start on a specific read architecture tied explicitly to HBF and
to ≥4-package AI-accelerator systems ('885 claims 14/19; '143 claim 13). Caveat throughout:
these are **published applications, not granted patents**.
