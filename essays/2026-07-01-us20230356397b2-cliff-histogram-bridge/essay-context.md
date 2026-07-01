# Essay context — US 2023/0356397 A1 (STM VL53L9CX series, Article 3 of 3 — "The Bridge")

Framing brief for the patent-essay pipeline. Read by Phase 1 (audience reframe) and carried
through Phase 2/3.

## Series identity and this article's place in it

This is article 3 of 3 in a series about STMicroelectronics' VL53L9CX direct-Time-of-Flight
(dToF) 3D LiDAR sensor. Channel identity: patent-analysis-based storytelling (the patent is the
protagonist, not the company). Audience: between a high-school senior and an early
undergraduate — visual, analogy-driven, "why does this matter" framing over dense technical
exposition.

Series arc (one throughline across all three articles): **the eye works → the eye can be
trusted → that eye becomes the robot's spatial behavior** (opening onto SLAM).

| # | Theme | Hero patent | One-line |
|---|---|---|---|
| 1 | Mechanism | US2026-0140238 | How the chip streams a photon histogram to pull out distance |
| 2 | Robustness | US2024-0192337 | The cleverness that filters out false targets past sunlight and glass |
| 3 (this one) | The Bridge (action) | US2023-0356397 | That eye keeps a robot from falling down stairs, opening onto SLAM |

**This article is the series' landing point.** Its one job: show how the depth map that
articles 1-2 built into a trustworthy "eye" turns into robot *behavior*, and gesture at (not
resolve) the SLAM horizon beyond it. This is a standalone essay — articles 1-2 are not attached
to this run, so treat the "callback" below as something this essay reconstructs briefly for a
first-time reader, not something it can assume the reader already saw.

### The load-bearing callback (this article's identity)

The hero claim reuses, essentially verbatim, the same "statistical distribution" (histogram)
language and the same multi-zone / row-of-zones (ROI) language that carries articles 1 and 2 of
this series. Make this callback explicit and central — the reader should land on: *the same
histogram-over-zones idea that made the eye work and made it trustworthy is the thing that just
kept this robot from falling down the stairs.* Use concrete, visual metaphor vocabulary
(photon counts, a bar chart / histogram, rows of zones scanning the floor) rather than abstract
statistics language, and keep it consistent rather than switching metaphors mid-essay.

## Hero patent

**US2023-0356397**, "Cliff detection in robotic devices" — priority date 2022-05-03, application
17/661,899, inventors Benoit Rivot and Xingyu Wang, assignee STMicroelectronics (Shenzhen) R&D
Co. Ltd / STMicroelectronics S.A. Full text is this run's `input/patent.md`.

CPC classification (corpus-index metadata, not independently re-verified against USPTO for this
run — cite as supporting color, not a claim-critical fact): includes B25J (robots) and
G01S17/931 (vehicle/robot LiDAR) — i.e., this patent is robot-native by classification, not just
by embodiment description.

**Verbatim anchor (must appear, unparaphrased):** "comparing a statistical distribution of the
reflected signals received at a plurality of different rows of zones"

**Claim hook:** a time-of-flight sensor (a SPAD array) mounted on the front of a mobile robot
compares the statistical distribution (histogram) of reflected signal across several rows of
zones in a region of interest (ROI). When the floor drops away (a stair edge, a curb, a
drop-off), that row-by-row comparison changes in specific, characterizable ways across three
distinct distance ranges — long, medium, short — and the robot changes its propulsion *before*
it reaches the edge, not after. (See `input/patent.md` paragraphs [0039]-[0080] for the full
three-range mechanism, and claims 1-3 for the claimed method.)

**Bridge action (the thing to land):** depth sensing becomes robot *action* — braking / a path
change — before contact. Not a data reading, but a decision to stop.

**Product tie-in:** a multi-zone dToF sensor like VL53L9CX, mounted on a robot, is exactly the
hardware this claim assumes. ST's own application list for VL53L9CX names robotics/humanoids and
SLAM/obstacle avoidance directly (see verified facts below) — the claim and the 2026 product
point at the same use case.

## Secondary patent (same beat, generalized — supporting only, must not compete with the hero)

**US2022-0184815**, "Controlling movement of a mobile robot" — filed 2020-12-15, inventors James
M. Hanratty and Jeffrey M. Raynor, assignee STMicroelectronics R&D. CPC G05D1 (robot position
control), B25J.

**Anchor:** "analyzing the image information to determine whether to modify the movement path of
the mobile robot"

**Role:** widens the bridge from the hero's specific case (a cliff) to general navigation — depth
map analysis leading to a path-change decision leading to a drive-motor command. Use it to
generalize the point in a sentence or a short passage, not as a second case study competing with
the hero for space.

## Horizon cluster ("beyond the bridge" — gesture only, never a hero-equivalent)

Turning one frame's reaction into actually remembering and mapping a space (SLAM) requires depth
to fuse with an IMU (balance) and edge AI (a brain). Cite only as a horizon, a line or clause
each, never expanded into a full case: US2021-0268903 (anti-collision), US2026-0087695
(histogram scene-change), US2022-0067346 (depth + inertial fusion), US2024-0191996 (multi-IMU
robotics fusion), US2022-0080979 (egomotion).

Close on the idea that STM is not solving the SLAM *algorithm* here — it is supplying the senses
and the legs (the nervous system) that a SLAM stack runs on top of.

**Caution:** IMU/GNSS-only navigation patents (e.g., US2019-0033466) are not depth-bridge
patents. They may appear in the horizon paragraph as context but must never be treated like the
hero or the secondary patent.

## Recommended structure (5 layers) + analogy seed

1. **Hook** — why doesn't a robot vacuum fall down the stairs? (then widen to humanoids, since
   the same question scales up.)
2. **Problem** — a depth map is a static snapshot. What has to happen for a snapshot to become
   *action*?
3. **Core claim (anchored)** — row-by-row histogram comparison across the ROI, across three
   distance ranges, ending in braking before the edge.
4. **Analogy** — the ToF eye is watching the floor a row at a time; the instant one row suddenly
   reads "much farther than before," the floor is gone there — that is the cliff. Stop.
5. **Meaning / horizon** — one sensor's reaction, fused with an IMU and edge AI, opens onto SLAM
   and the humanoid era.

## Tone and guardrails (hard constraints)

- **No overclaiming.** "First" only in ST's own qualified phrasing (e.g., "first dToF 3D LiDAR
  all-in-one module in ST's portfolio") — never state an unqualified "first."
- **Never say "STM solves SLAM."** Say STM supplies the senses and the legs/limbs — SLAM itself
  stays a horizon this essay opens onto, not a delivered result.
- **"Cliff" = drop-off / stair edge / curb, not a geological cliff.** Frame around robot-vacuum
  and service-robot floor safety, extending to humanoid foot safety at the close.
- **Keep "bridge" and "horizon" visibly distinct.** Do not imply that one depth map, by itself,
  completes SLAM.
- All `[dddd]` anchors verbatim against `input/patent.md`, no paraphrase.
- This is a standalone essay (articles 1-2 are referenced conceptually, not as citable sources
  in this run) — do not cite them in `# Sources`, and do not assume the reader has read them;
  earn the callback in a sentence or two rather than presupposing it.

## External facts available for this run (verified against ST first-party sources, 2026-06-30)

Use only what is listed below as fact; do not state the "pending confirmation" items as bare
fact, and prefer omitting them if they are not load-bearing for this article's thesis (they
matter more to article 1's mechanism deep-dive than to this bridge/action article).

**Verified — safe to cite as fact:**
- VL53L9CX: a direct Time-of-Flight (dToF) 3D LiDAR all-in-one module; evaluation board
  STEVAL-VL53L9; mass production announced for early July 2026 (announcement dated 2026-06-22).
- Resolution: 2,268 zones (54×42) — "2.3K zones," described as the industry's highest
  multi-zone resolution; the prior generation VL53L5/L8CX topped out at 64 zones or fewer
  (roughly a 35x jump).
- FoV / range: 54×42° FoV (2,268 zones), 71° diagonal FoV at 1° angular resolution (per data
  brief), 5cm-9m range, up to 100fps.
- Detection: a BSI-stack SPAD array (single-photon avalanche diode). Dual-scan flood
  illumination (vs. dot-scan) removes dead zones and improves small-object/edge detection and
  motion artifacts.
- Optics/processing: an on-chip SoC does histogram processing plus algorithmic correction to
  remove cover-glass crosstalk and veiling glare; calibration-free.
- Outputs: depth (3D) / 2D IR (active and passive) / reflectance / confidence — AI-ready for
  MCU edge AI. First ToF sensor with MIPI and I3C interfaces (plus I2C).
- Applications (ST press release, verbatim): "small object detection, SLAM, obstacle avoidance
  for autonomous navigation" — plus home/building/city automation, smart glasses (AR),
  industrial, robotics/drones/humanoids, edge AI.
- ST's own claim (verbatim, press release): "VL53L9 is the first direct Time-of-Flight (dToF)
  3D LiDAR all-in-one module in ST's portfolio." Blog: "1st 3D ToF LiDAR with 2.3K zones and
  flood illumination." This is a *qualified* first (within ST's own portfolio) — multi-zone
  dToF already existed via VL53L5/L8; the jump is resolution plus flood illumination, not the
  first multi-zone dToF sensor ever built.

**Pending confirmation — do not state as bare fact without a hedge; omit if not essential:**
940nm wavelength, the BSI "stack" structure detail, dual VCSEL + BCD driver, ~150mW power draw,
12.8×6.1×4.6mm package, ~1% (TNR) accuracy. These come from the data brief only and were not
independently cross-checked against the full datasheet as of this run.

## Figures available

Pre-cleaned in `input/figures/`, named to match this patent's own figure numbering (FIGS.
1A-1C, 2A-2D, 3-7). Note for whoever drafts figure references: figures 1 and 2 only exist here
as lettered sub-figures (1A/1B/1C, 2A/2B/2C/2D) — a caption that only ever writes "FIG. 1A" or
"FIGS. 1A-1C" will not register figure 1 as used by the mechanical figure-use gate (the trailing
letter breaks the word-boundary match on the bare number), so make sure at least one bare
"FIG. 1" and one bare "FIG. 2" token appears somewhere the two figures are used (e.g., "FIG. 1
shows..." or a parenthetical "(FIG. 1)"), in addition to the lettered captions.

- `fig-01AB.png` — FIGS. 1A-1B: the mobile robot (100) with a front-mounted ToF sensor (102)
  feeding a navigation system (106: wall tracking / material recognition / cliff detection /
  SLAM, split into close/medium/long range) — and the navigation system block diagram (IMU 112 +
  controller 108 + ToF sensor 102 + memory 109).
- `fig-01C.png` — FIG. 1C: the ToF sensor's zone array and the region of interest (ROI) — the
  bottom rows of zones (first/second/third row) used for cliff detection.
- `fig-02AB.png`, `fig-02CD.png` — FIGS. 2A-2D: the robot approaching a cliff edge, shown across
  the four schematic stages (too far to detect / long range / medium range / short range).
- `fig-03.png` — FIG. 3: the graph of median ground distance and peak intensity per row over
  time as the robot approaches the edge — this is the single best visual for the core mechanism
  (the row-lines hold flat, diverge, converge, then spike/drop at the edge).
- `fig-04.png` — FIG. 4: process flow, all three distance ranges together.
- `fig-05.png` — FIG. 5: process flow, long-range detection (peak-intensity-vs-ambient test).
- `fig-06.png` — FIG. 6: process flow, medium-range detection (median-distance convergence test).
- `fig-07.png` — FIG. 7: process flow, short-range detection (loss-of-ground test).
