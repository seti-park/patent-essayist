# Thesis Candidates

## Candidate 1: Cleaning the histogram (the cover-glass ghost)

**Statement**: The histogram Article 1 taught readers to trust arrives contaminated by the
sensor's own reflection off its cover glass — this patent is the specific, patented way STM's
VL53L9CX tells that ghost apart from a real target, on-chip, without a factory calibration step.

**Framing**: continuity reframe — "Article 1 = reading the histogram, Article 2 = cleaning the
histogram" (per essay-context.md's specified series throughline); technical-impossibility hook
("how does the chip know its own reflection from a real object, using the same raw signal?").

**Evidence required**:
- Patent's own statement of the cross-talk/cover-glass problem
- The specific mechanism (ZCF + weighted sum + MF switch-over) that resolves it
- A quantified or at least clearly comparative before/after effect
- An external tie to ST's own marketing claim about on-chip cross-talk compensation

**Evidence available in invention-summary**:
- ✓ Problem anchor, verbatim and strong (`[0029]` cross-talk / cover-glass reflection)
- ✓ Mechanism anchor across claims 1-16 and `[0030]`, `[0054]`, `[0060]`
- ✓ Comparative effect anchor (FIGS. 11/12, `[0067]`-`[0068]`, `[0076]`)
- ✓ External tie confirmed via context research (`st-onchip-crosstalk-veiling-glare-2026`)

**Structural tension**: reader already trusts the histogram from Article 1; this essay reveals
it arrives dirty, then shows the specific fix, then closes the loop back to the product claim.

**Risks**:
- Could read as "STM solved cross-talk" if not carefully scoped to this patent's specific
  technique (essay-context.md explicitly forbids this framing) — needs a scoping clause.
- Cross-talk-as-cover-glass-reflection is the core analogy, but the patent's own language
  allows cross-talk to include internal optical leakage too (`[0029]` frames it generally before
  the cover-glass explanation) — needs a one-clause acknowledgment, not a detour.

**Grounding (4-axis — draft, locked in Step 4)**:
- Claims anchor: claim 1 (ZCF filtering → zero-crossing pulse regions → weighted sum →
  classify first/second type of peak → generate ZCF target list) + claim 6/12 (MF combined in)
- Problem anchor: `[0029]` "The cross-talk signal in the histogram, if not processed properly,
  may be incorrectly detected as a close target."
- Effect anchor: `[0076]` "the disclosed ZCF based target detection method can reject false
  target caused by cross-talk, thus achieving robustness against cross-talk" + FIGS. 11/12
  comparative curves
- Baseline-difference anchor: industry-wide, recurring cover-glass cross-talk problem across
  ST's own multi-generation ToF product line (context research: ghost-detection reports,
  cover-glass application notes for VL53L5CX/L7CX/L8) vs this patent's specific on-chip,
  calibration-free classification fix

**Q7 hook pattern (draft, hard-gated in Step 5)**:
- technical-impossibility
- anchor: reader's intuitive objection — "if the ghost and the real target are made of the
  exact same stuff (reflected laser light, same histogram), how can the chip possibly tell them
  apart without an outside reference?" → patent's answer: it doesn't need an outside reference,
  it uses *where* the ghost has to sit (near-zero distance, fixed by the sensor's own geometry)
  and a weighted-sum test keyed to that fixed geometry.

**Adversarial defense (draft, locked in Step 6)**:
- Strongest objection: this reads as ST/the essay overclaiming that cross-talk is "solved" —
  a critical reader could point out the patent's own data (FIGS. 11/12) shows the ZCF path still
  loses range, and the MF path is still fooled at close range; only the *combination*, gated by
  a switch-over rule, gets the benefit of both — the essay must not flatten that into "STM fixed
  it" language.
- Mitigation: the mechanism section states plainly that neither filter alone solves it — ZCF
  trades range for cross-talk immunity, MF trades cross-talk immunity for range — and that the
  invention is specifically the classification-and-switchover step that lets the system use
  both without inheriting either one's single failure mode. This mirrors essay-context.md's own
  hard requirement never to claim STM "solves" cross-talk outright.

---

## Candidate 2: The zero-point trick (calibration-free framing)

**Statement**: Instead of factory-calibrating out its own cover-glass reflection, STM's patent
teaches the chip to recognize where that reflection *must* sit — a fixed "reference zero-point"
set by the sensor's own geometry — and use that as the pivot for a weight-coefficient test that
never needs re-tuning per unit.

**Framing**: technical-impossibility hook, narrower — leads with "no calibration screen, no
factory step" rather than the histogram-contamination framing.

**Evidence required**:
- Reference zero-point mechanism (`[0033]`, `[0060]`)
- The calibration-free product claim it explains
- A hook that doesn't require re-teaching the histogram concept from Article 1

**Evidence available in invention-summary**:
- ✓ Mechanism anchor (`[0060]` reference zero-point tied to SPAD-to-window distance)
- ✓ Product tie (context research: `vl53l9cx-calibration-free-2026`)
- ✗ Weaker Axis 2 (problem) anchor on its own terms — "no calibration screen" is a downstream
  *consequence* of solving cross-talk, not the problem the patent's Background section itself
  states; the patent's own stated problem is the cross-talk/false-target issue (`[0029]`), not
  a calibration-cost problem. Using this framing risks inverting cause and effect: the patent
  fixes cross-talk, and calibration-freedom follows from doing that on-chip and generically —
  it is not itself the "종래 문제."

**Structural tension**: would need to open on "why does every unit need a calibration step" —
a real but secondary problem this patent's specification does not itself foreground.

**Risks**:
- Drops the specified series throughline (essay-context.md requires the explicit "Article 1 =
  reading, Article 2 = cleaning" framing) — this candidate has no natural histogram callback,
  making it harder to satisfy the hard requirement of an explicit Article 1 tie-back.
- Narrower entry point for the general-audience reader (calibration is a manufacturing/ops
  concept, less immediately visual/intuitive than "is that a ghost or a real thing").

**Grounding (4-axis — draft, locked in Step 4)**:
- Claims anchor: claim 4 (reference zero-point = bin corresponding to emitter-to-window
  distance) — present, but a dependent-claim-level detail, not the independent claim's core
- Problem anchor: 3/4 — the patent's own stated problem (`[0029]`) is cross-talk/false-target
  detection, not calibration cost; this candidate would have to import the calibration-cost
  framing from context research rather than from the specification's own Background section
- Effect anchor: present via `vl53l9cx-calibration-free-2026`, but this is a product-level
  external fact, not something the patent text itself states as an "effect of the invention"
- Baseline-difference anchor: present (factory-calibration industry norm vs this claimed
  zero-touch approach), but weaker than Candidate 1's because it leans more heavily on external
  product marketing than on the patent's own text

**Q7 hook pattern (draft, hard-gated in Step 5)**:
- technical-impossibility
- anchor: "how can a sensor work behind any cover glass — scratched, dusty, different
  thicknesses — without someone tuning it at the factory?" — a real question, but requires
  importing the calibration framing rather than following from the patent's stated Background.

**Adversarial defense (draft, locked in Step 6)**:
- Strongest objection: this candidate's Axis 2 (problem) is not squarely the patent's own
  stated problem — a sharp reader who checks the Background of the Invention will find
  cross-talk/false-target detection, not calibration burden, as the "종래 문제."
- Mitigation: would require reframing the lead to fold calibration-freedom in as a downstream
  consequence rather than the headline problem — which converges back toward Candidate 1's
  framing anyway.

**Rejection reason**: Axis 2 (problem anchor) is a 3/4-strength anchor at best — the patent's
own Background of the Invention foregrounds cross-talk/false-target detection, not calibration
cost; "calibration-free" is a real and valuable product-level consequence of the invention, but
using it as the entry-point problem inverts the specification's own cause-and-effect and would
require importing an external framing not native to the patent text. It also drops the specific,
required series throughline from essay-context.md (explicit histogram callback to Article 1),
which Candidate 1 satisfies directly. Candidate 2's strongest material — the reference
zero-point mechanism and the calibration-free product tie — is retained as a **secondary beat
inside Candidate 1** (the "calibration-free operation" product/meaning closer, per
essay-context.md's recommended structure point 5), not promoted to its own spine.

---

## Comparison

| Dimension | Candidate 1 | Candidate 2 |
|-----------|-------------|-------------|
| Evidence completeness | Full (4/4) | Partial (problem anchor weak) |
| Audience appeal | High — visual, analogy-ready ("catching your own reflection") | Medium — calibration is a less intuitive entry point |
| Architectural depth | High — covers ZCF + MF + weighted sum + switch-over as one system | Medium — isolates one dependent-claim-level detail |
| Defensive strength | High — objection squarely anticipated and mitigated in-scope | Medium — objection exposes a genuine anchor weakness |
| 4-axis grounding | 4/4 | 3/4 (no clean problem anchor) |
| Q7 hook | technical-impossibility | technical-impossibility |
| Hook accessibility | High | Medium |
| Satisfies essay-context.md hard requirements (histogram callback, marketing tie, single hero) | Yes, directly | Only with reframing back toward Candidate 1 |

## Recommendation

Candidate 1 — full 4-axis grounding entirely from the patent's own text, the only candidate that
directly satisfies essay-context.md's required series throughline and explicit histogram
callback, and the strongest, most defensible technical-impossibility hook for a general-audience
reader. This is also the angle essay-context.md itself specifies as the required thesis frame.

## SETI selection

- **Decision**: Select Candidate 1
- **Notes**: essay-context.md's hard requirements pre-specify this exact thesis angle
  ("the cleverness that filters fake targets out of sunlight and cover glass" /
  "Article 1 = reading the histogram, Article 2 = cleaning the histogram"), and Candidate 1
  is independently the stronger candidate on 4-axis grounding and Q7 hook accessibility as well
  — selection is not a mere pass-through of the brief but an evidence-grounded confirmation of
  it. Candidate 2's calibration-free material is folded into Candidate 1 as a secondary beat
  rather than discarded. Proceed to spine lock (Step 8) with Candidate 1's grounding + hook +
  defense.
