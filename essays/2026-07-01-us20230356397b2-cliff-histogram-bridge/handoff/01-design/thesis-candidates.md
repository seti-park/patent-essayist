# Thesis Candidates

## Candidate 1: The bridge — same histogram, now a decision to stop

**Statement**: The same row-of-zones histogram comparison that this series already
established as the ToF eye's trustworthy read on the world is the exact mechanism this
patent reuses to turn one bad reading into a robot's decision to stop before it falls.

**Framing**: continuity reframe — this essay's job is not to introduce a new idea but to
show a familiar one crossing a threshold, from "the eye can be trusted" to "the eye now
drives the legs."

**Evidence required**:
- Verbatim reuse of "statistical distribution" / histogram-over-zones claim language
- A concrete, single mechanism the reader can picture (row-by-row comparison, three
  ranges)
- A clean before/after: depth reading vs. actual propulsion change
- A generalizing secondary anchor + a horizon gesture that does not overclaim

**Evidence available in invention-summary**:
- ✓ Claim-anchored histogram language (`[0005]`, claim 1 — "comparing a statistical
  distribution of the reflected signals received at a plurality of different rows of
  zones")
- ✓ Full 3-range mechanism with quantified boundaries (`[0043]`, `[0050]`, `[0051]`,
  `[0054]`)
- ✓ Explicit "before reaching the edge" action clause (`[0005]`, `[0086]`, claim 1)
- ✓ Secondary-patent generalization available (US2022-0184815, per essay-context.md)
- ✓ Product tie-in (VL53L9CX, robotics/SLAM application list — essay-context.md verified
  facts)

**Structural tension**: reader starts with an everyday, slightly comic question (why
doesn't my robot vacuum fall down the stairs?), gets shown that the answer is the exact
same "read a histogram across rows of zones" idea already established as the eye's
trustworthy read, and ends widened to humanoids and a SLAM horizon this one bridge does
not itself resolve.

**Risks**:
- Reader who has not seen articles 1-2 may not register the callback as a callback
  rather than a new idea introduced from nothing.
- Risk of overclaiming "STM solves SLAM" if the horizon paragraph is not carefully
  fenced.

**Grounding (4-axis — draft, locked in Step 4)**:
- Claims anchor: claim 1 — "comparing a statistical distribution of the reflected
  signals received at a plurality of different rows of zones configured by the array of
  SPAD sensors in a region of interest (ROI) of the ToF sensor and based on the
  comparing detecting an approaching of the edge of the cliff, the comparing comprising
  identifying a convergence of an intensity of the reflected signals or of a median
  distance to a ground"
- Problem anchor: `[0004]` "the mobile robot cannot detect the cliff until a portion of
  its body is physically over the edge of the cliff"
- Effect anchor: `[0026]` "it allows the mobile robot 100 to move at increased speeds
  because it can anticipate a cliff before it reaches it"
- Baseline-difference anchor: VL53L9CX's 2,268-zone resolution (a ~35x jump over the
  prior VL53L5/L8CX generation, per ST's own verified figures) vs. this patent's claimed
  mechanism needing only a handful of rows (as few as 3, per `[0036]`) compared against
  each other — the row-comparison idea scales from a coarse array to a dense one without
  changing in kind, which is exactly why a 2026 sensor with far more zones is still doing
  the same trick this 2022-filed patent claims.

**Q7 hook pattern (draft, hard-gated in Step 5)**:
- technical-impossibility
- anchor: reader's first-order assumption is "a depth sensor just measures distance — how
  does a distance reading turn into a *decision* to stop?" The patent's answer:
  it is not one distance reading, it is a *comparison* across rows that changes in a
  specific, recognizable way right before the floor drops away.

**Adversarial defense (draft, locked in Step 6)**:
- Strongest objection: this is a standalone essay — the reader has not seen articles 1-2,
  so "the same histogram that made the eye work" is an assertion with nothing behind it
  unless the essay earns it inline.
- Mitigation: the essay reconstructs the histogram/multi-zone idea briefly and concretely
  (photon counts across rows of zones) before making the callback, rather than assuming
  the reader remembers it.

---

## Candidate 2: Two metrics, one convergence — the three-range detector as an engineering
puzzle

**Statement**: A single sensor's own row-to-row geometry — fixed and known in advance —
is turned into a three-stage tripwire, using nothing but a median distance and a peak
brightness, each cross-checked against the other so the robot never has to guess between
a change in floor material and an actual cliff.

**Framing**: mechanism-first reframe — treat the three-range logic as the star and lead
with the engineering cleverness (two independent metrics, two failure modes disambiguated)
before widening to the robot-behavior payoff.

**Evidence required**:
- The full three-range logic (long/medium/short) with the two metrics disambiguated
- The ambient-rate cross-check that rules out "just a rug" false positives
- A payoff that lands on why this matters practically

**Evidence available in invention-summary**:
- ✓ Full three-range logic quantified (`[0049]`–`[0056]`, `[0060]`–`[0080]`)
- ✓ Ambient-rate false-positive guard (`[0064]`, `[0079]`)
- ✗ Weaker connection to the series' load-bearing callback — this framing treats the
  histogram-over-zones idea as one clever trick among several (median distance AND peak
  intensity AND ambient-rate cross-check), rather than putting the single
  histogram-over-zones idea front and center the way the series brief requires

**Structural tension**: reader is walked through an engineering puzzle (how do you tell
"the floor changed color" from "the floor is gone") and the three-range solution unfolds
range by range.

**Risks**:
- Buries the series' single load-bearing callback (the histogram/multi-zone idea) under
  a broader "look at this clever multi-metric system" framing — this is a structural
  mismatch with essay-context.md's explicit instruction to keep the callback "explicit
  and central," not one clever mechanism among several.
- Reads more like a standalone mechanism deep-dive (closer to article 1's job) than the
  series' bridge/action landing point this article is supposed to be.

**Grounding (4-axis — draft, locked in Step 4)**:
- Claims anchor: claim 1 (b) — "identifying a convergence of an intensity of the
  reflected signals or of a median distance to a ground"
- Problem anchor: `[0018]` "cameras require complex camera systems to detect a cliff and
  cannot provide information about the distance to the cliff"
- Effect anchor: `[0019]` "this allows for the mobile robot to travel at faster speeds by
  changing its propulsion prior to reaching the cliff"
- Baseline-difference anchor: 3/4 — the multi-metric framing does not need a specific
  external product baseline to be internally coherent (patent-only anchors suffice for
  axes 1-3), but Axis 4 as stated in essay-context.md's brief (VL53L9CX resolution jump)
  fits awkwardly here since this framing's "baseline" is really the prior single-zone/
  camera art already covered by Axis 2, not an external product-generation contrast.

**Q7 hook pattern (draft, hard-gated in Step 5)**:
- technical-impossibility
- anchor: reader's "how do you tell a cliff apart from the floor just changing texture or
  color?" — patent's answer is the ambient-rate + convergence cross-check.

**Adversarial defense (draft, locked in Step 6)**:
- Strongest objection: a mechanism-first, puzzle-style lead is a legitimate essay shape
  in isolation, but this is article 3 of 3 and its stated job (per essay-context.md) is
  to be the series' *landing point* on the callback, not a second mechanism deep-dive.
- Mitigation: would require restructuring the lead entirely around the callback anyway,
  which converges back toward Candidate 1.

**Rejection reason**: Not disqualified on 4-axis or Q7 grounds (it clears both), but
rejected against the brief: essay-context.md specifies a single strongly-preferred spine
built around the histogram/multi-zone callback as the load-bearing, central device — this
candidate's engineering-puzzle framing treats that callback as one input among several
(median distance, peak intensity, ambient-rate cross-check) rather than the central,
explicit, consistently-used metaphor the brief requires. Reframed into Candidate 1, which
keeps the same underlying patent mechanism but leads with the callback instead of the
puzzle.

---

## Candidate 3: The sensor that already does four jobs — cliff detection as a software
feature, not new hardware

**Statement**: The same forward-facing multi-zone sensor a robot already carries for wall
tracking, material recognition, and SLAM gets a fourth job — cliff detection — for free,
because the invention is a new way to read data the sensor was already producing, not a
new sensor.

**Framing**: efficiency/no-new-hardware reframe — lead with the "one sensor, four jobs"
angle from `[0027]`.

**Evidence required**:
- Explicit patent language that one sensor serves multiple navigation functions
- A clear sense of what's "new" (the reading, not the hardware)

**Evidence available in invention-summary**:
- ✓ Mechanism (`[0027]` "single multi zone ToF sensor 102 may be used by the controller
  to perform wall tracking, material recognition, cliff detection, and SLAM")
- ✗ Weaker Q7 hook — "one sensor does many jobs" is a mild efficiency observation, not a
  reader-facing "how could that possibly work" tension nor a corporate-narrative friction;
  it does not cleanly map to either admitted Q7 pattern without stretching
- ✗ Does not foreground the series' required load-bearing callback (histogram/multi-zone
  comparison) at all — this framing is about sensor reuse across *functions*, not about
  the row-comparison statistic itself

**Structural tension**: reader learns the robot isn't adding hardware, just getting
smarter about data it already has.

**Risks**:
- Undersells the actual inventive mechanism (the row-to-row statistical comparison) in
  favor of a much softer "software reuse" framing.
- Q7 gate risk: "efficiency of sensor reuse" is not a technical-impossibility (no
  reader objection is being answered) and not a corporate-narrative-friction (no
  narrative event is in tension with patent evidence).

**Grounding (4-axis — draft, locked in Step 4)**:
- Claims anchor: claim 6 — "the ToF sensor is also used for object detection, wall
  tracking, and simultaneous localization and mapping (SLAM)" — this is a dependent
  claim describing shared sensor use, not the core row-comparison mechanism of claim 1
- Problem anchor: `[0018]` (indirect only — the problem being solved is still cliff
  detection latency, not sensor proliferation)
- Effect anchor: ✗ no paragraph frames "avoiding extra hardware" as an "effect of the
  invention" in its own right — this is an inference from `[0027]`, not a stated benefit
- Baseline-difference anchor: ✗ no external baseline available for "how many sensors do
  robots typically carry" — would require new context research outside this run's scope

**Q7 hook pattern (draft, hard-gated in Step 5)**:
- (none — does not cleanly map to either admitted pattern; see Risks)

**Adversarial defense (draft, locked in Step 6)**:
- Strongest objection: N/A — candidate fails the Q7 hard gate before adversarial defense
  is meaningful.
- Mitigation: N/A.

**Rejection reason**: Q7 hard gate failure (Step 5) — does not map to either
`corporate-narrative-friction` or `technical-impossibility` without forcing the frame;
also weak on Axis 3 (effect) and Axis 4 (baseline-difference), 2/4 at best. Per
`references/hook-patterns.md` §"거부 사례" case 1, a candidate with no clean pattern
mapping is rejected rather than reframed into a weak fit.

---

## Comparison

| Dimension | Candidate 1 | Candidate 2 | Candidate 3 |
|-----------|-------------|-------------|-------------|
| Evidence completeness | Full | Full (patent-only) | Partial |
| Audience appeal | High (concrete, familiar-then-surprising) | Medium (puzzle framing skews more technical) | Low (soft "efficiency" framing) |
| Architectural depth | High | High | Medium |
| Defensive strength | High | Medium | Low |
| 4-axis grounding | 4/4 | 3/4 (baseline anchor awkward fit) | 2/4 |
| Q7 hook | technical-impossibility | technical-impossibility | (none — disqualified) |
| Hook accessibility | High | Medium-High | n/a |
| Fit with essay-context.md brief (callback centrality) | Exact match — callback is the spine | Partial mismatch — callback is one of several metrics | No match — callback absent |

## Recommendation

Candidate 1 — full 4-axis grounding, a clean technical-impossibility hook, and it is the
only candidate that keeps the series' required histogram/multi-zone callback as the
explicit, central, single load-bearing device rather than one mechanism among several,
matching essay-context.md's brief.

## SETI selection

- **Decision**: Select Candidate 1
- **Notes**: Matches essay-context.md's strongly-preferred spine (cliff-detection claim as
  the "bridge" from depth-sensing to robot action, with the histogram/multi-zone callback
  as the load-bearing device, secondary patent US2022-0184815 generalizing it, SLAM horizon
  cluster gestured at but never treated as a hero). All 4 axes independently verified
  against patent text before selection, per this run's instruction that the brief's
  preference still requires genuine grounding, not just assertion. Proceed to spine lock
  (Step 8).
