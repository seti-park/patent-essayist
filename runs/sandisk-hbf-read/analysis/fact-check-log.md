# Fact-check log

Two classes of fact. **Patent-anchored** facts trace to invention-summary `[dddd]` anchors and
need no entry here. **External** facts (market/corporate context) each get a Fact ID, a source,
a confidence, and a fence note; every one must appear in the essay's `# Sources` block and be
framed as "not inside the filing."

## External facts

### F1 — sandisk-spinoff-2025  [high]
- **Claim**: SanDisk is again a standalone public company. Western Digital completed the
  separation of its flash business on 2025-02-21; SanDisk Corporation began regular-way trading
  on Nasdaq under ticker **SNDK** on 2025-02-24.
- **Sources**: SanDisk Investor Relations press release, 2025-02-24; Western Digital SEC Form 8-K, 2025-02.
- **Fence**: external corporate fact; not in either filing.

### F2 — hbf-program-2025  [high]
- **Claim**: SanDisk publicly unveiled "High Bandwidth Flash" (HBF) at its first post-spin
  Investor Day in February 2025 — a NAND-based memory pitched as an alternative/complement to
  HBM for AI inference.
- **Sources**: Tom's Hardware, 2025-08; SanDisk newsroom.
- **Fence**: the commercial "HBF" brand/program is external. The two filings DO use the term
  "high bandwidth flash" in-text ('143 [0019]; '885 claim 14), but they describe read techniques,
  not the product — the product linkage is a reasonable inference, stated as such.

### F3 — hbf-value-prop  [medium — SanDisk marketing claim, not independently benchmarked]
- **Claim**: SanDisk claims HBF can deliver bandwidth comparable to HBM at up to **8–16×** the
  capacity of HBM at similar cost. Exact bandwidth/capacity figures are generation-dependent and
  vary by source.
- **Sources**: Tom's Hardware, 2026-02-25; SK hynix newsroom, 2026-02-25.
- **Fence**: SanDisk's own claim; present as a claim, not a benchmark.

### F4 — hbf-advisory-board-2025  [high]
- **Claim**: SanDisk formed an HBF Technical Advisory Board chaired by Turing Award winner Prof.
  David Patterson (members include Raja Koduri).
- **Sources**: Blocks & Files, 2025-07-25.
- **Fence**: external.

### F5 — hbf-skhynix-standardization  [high]
- **Claim**: SanDisk and SK hynix signed an MOU (2025-08-06) to standardize HBF; the two
  companies launched a formal standardization push at a joint event on 2026-02-25.
- **Sources**: SanDisk press release, 2025-08-06; SK hynix newsroom, 2026-02-25.
- **Fence**: external.

### F6 — hbf-roadmap  [high]
- **Claim**: SanDisk's stated roadmap puts first HBF samples in H2 calendar-2026 and first
  AI-inference devices/systems using HBF in early 2027.
- **Sources**: TrendForce, 2025-11-11.
- **Fence**: external; forward-looking vendor roadmap.

### F7 — hbm-supply-constraint  [high]
- **Claim**: HBM has been effectively sold out through 2026 across the three suppliers (SK hynix,
  Samsung, Micron); HBM supply (with advanced packaging) is a primary constraint on AI compute.
- **Sources**: Bloomberg, 2025-10-28; TechSpot, 2025-10; TrendForce "Memory Wall".
- **Fence**: external market context.

### F8 — hbf-multivendor  [medium]
- **Claim**: HBF is becoming a multi-vendor effort; Kioxia showed a ~5 TB HBF prototype (Aug
  2025) and Samsung has done early HBF concept work.
- **Sources**: TrendForce, 2025-11-11; Digitimes, 2025-10-07.
- **Fence**: external; included only if the moat section needs the competitive beat.

## Explicitly NOT established (do not assert)

- **Forward-citation chain**: the run's original context notes claimed application US 18/748,826
  cites '885 at [0205]. This run could **not** verify any forward-citation or continuation
  relationship for either application (Google Patents citation graph not retrievable here). The
  essay must NOT assert a citation chain. The portfolio-depth argument rests only on what is
  verifiable: the two filings share a SanDisk read team (Yang / Cao / Dutta across both), and
  SanDisk runs a public HBF program (F2, F4, F5). Related same-inventor read patents may exist
  but are unconfirmed — omit specific numbers.
- **Quantified bandwidth gain for the two techniques**: neither filing gives a percentage; the
  HBF product figures (F3) are not the patents' figures.
