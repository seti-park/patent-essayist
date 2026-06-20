# Thesis spine (LOCKED)

## Single spine

**HBF gets HBM-class read bandwidth by deleting the per-read charge/discharge tax on both axes of
the NAND array — always-on bit lines ('885) and discharge-free word lines ('143) — and that
two-axis, adaptively-triggered read architecture, not any single narrow claim, is where a
technical moat would actually live.**

Throughline for the investor reader: judge the moat by the *architecture and the portfolio*, not
by one easily-designed-around claim — and remember these are published applications, not grants.

## Q7 hook pattern (hard gate)

- [x] `technical-impossibility` — anchor: reader's reasonable objection that NAND flash is too
  slow and too power-hungry to stand in for HBM (stated by the filing itself, '885 [0005]) →
  resolved by refusing to ramp the array down between reads (bit lines in '885, word lines in '143).
- [ ] `corporate-narrative-friction`

## Closing posture

- Residual risk: **Acknowledged** (published-not-granted; each independent claim is a narrow
  single-feature device-operation claim, designed around by accepting the performance loss).
- Closing voice pattern: `closing-aphoristic-landing` ("X is Y. But Z is W." syntax) — the pitch
  is a new memory; the patents are about not turning the old one off.

## Spine → section trace (contract)

1. **Lead — the impossible substitution.** Industry-norm framing: model weights need HBM-class
   bandwidth; NAND was the cheap-but-too-slow option ('885 [0004], [0005]). Inline bold thesis
   anchor: the fix is an omission, not a new cell. Figure 1 (HBF around a processor).
2. **The string, and the two voltages that cost time.** Bit line (column) vs word line (row);
   why each read pays a setup/recovery tax. Figure 2 (NAND string). Anchors [0146].
3. **Column axis — always-on bit lines ('885).** Before/after: conventional discharge/recharge
   (Figure 3) vs holding VBL≈0.2 V with sub-1µs settling (Figure 4). Anchors [0006], [0147], [0148].
4. **Row axis — discharge-free word lines ('143), and the adaptive trigger.** Unselected word
   lines held at VREAD across reads (Figure 5); the device switches into the mode on a detected
   read burst (Figure 6). Symmetry beat. Anchors [0047], [0007], [0178], [0179], [0181].
5. **The moat question.** What is actually fenced: narrow single-feature claims, but on both
   axes, adaptively triggered, and tied to HBF + ≥4-package accelerator systems ([0011], [0019]).
   Portfolio depth + citation chain + same read team. Fenced external context (spinoff, HBF
   program, HBM contrast). Honest design-around analysis. Published-not-granted caveat.
6. **Closing — built to be read.** Aphoristic landing; forward pointer = grant + continuations +
   whether HBF ships inside an accelerator.

Every patent claim in the draft traces to an anchor in invention-summary Quotable spans / Quote
anchor table. Every external claim traces to a fact-check-log Fact ID and a `# Sources` entry.
