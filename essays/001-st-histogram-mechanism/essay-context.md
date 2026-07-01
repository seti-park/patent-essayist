# Essay context — US 2026/0140238 A1 (Article 1 of 3, "Mechanism")

Framing brief for the patent-essay pipeline, synthesized from a Korean series brief
(`_series-context.md`) and a Korean article-1 brief (`article1-mechanism.context.md`). Read by
Phase 1 (audience reframe) and carried through Phase 2/3. Where this brief and the Korean
sources conflict, this brief controls (it is the reconciled version); the Korean sources' verified
facts and anchors are preserved here, translated to English since the deliverable is English-only.

## Audience and deliverable

- **Audience:** general tech-curious reader, roughly high-school-to-early-undergrad literacy —
  visual- and analogy-driven, oriented around "why this matters," not a specialist or investor
  audience.
- **Deliverable:** one English long-form essay for X Articles — **Article 1 of a 3-part
  narrative series** on STMicroelectronics' VL53L9CX (dToF 3D LiDAR) patent portfolio. Channel
  identity is patent-analysis-as-storytelling — the patent is the protagonist.
- **Series arc:** (1) the eye *works* [**this article** — mechanism] → (2) the eye is *trusted*
  [robustness, Article 2, hero US 2024/0192337] → (3) that eye becomes the robot's *spatial
  action* [the bridge to SLAM, Article 3, hero US 2023/0356397]. Articles 2 and 3 are out of
  scope for this run but will reuse this article's vocabulary and hero as continuity.
- **One-line thesis seed:** how the chip pulls a distance measurement out of a photon
  arrival-time histogram by streaming it bin-by-bin on-chip, almost memory-free.

## Series-wide vocabulary this essay must DEFINE (callback contract)

Articles 2 and 3 will reuse these terms without redefining them — this essay owns the
definitions:

- **histogram** = the bar chart of photon arrival times for one zone.
- **zone / multi-zone** = the grid the field of view is divided into; each cell yields its own
  distance reading.
- **peak = distance** = the histogram's tallest bin marks the round-trip time, hence the
  distance.

Also unpack **dToF**, **SPAD**, and **TDC** in plain language the first time each appears.

## Hero patent

**US 2026/0140238 A1** — "Ultra-Lean Time-of-Flight Histogram Processing." Filed 2024-11-19.
Inventors: Donald Baxter, Pascal Mellot, Stuart McLeod, Andreas Assmann. Assignee:
STMicroelectronics International N.V. Full text at `input/patent.md`.

- **Verbatim anchor** (Abstract): "processes time-of-flight measurement data using sequential
  bin-by-bin histogram processing" — quote exactly, no paraphrase.
- **Claim hook, plain language:** the chip streams the photon-count histogram one bin at a time
  and finds the peak on the fly, so it needs almost no memory — light enough to run inside the
  sensor package itself (on-chip) instead of on a host processor. That is what opens the door to
  edge-AI use.
- **Mechanism to land:** for every zone, the chip accumulates "when did photons come back" into
  a histogram; the peak (most-populated bin) is that cell's distance. At 2,268 zones, that is
  2,268 histograms effectively running at once.
- **Product tie:** this on-chip, ultra-lean histogram processing is *why* VL53L9CX can advertise
  on-chip processing, AI-readiness, and a low power budget — it is the mechanism behind those
  spec-sheet bullets. The patent's 2024-11-19 filing lines up with the shipping (2026) generation.

## Auxiliary patent — principle scaffold ONLY (same beat as the hero)

**US 2023/0296739 A1** — "Methods and devices for identifying peaks in histograms." Filed
2022-03-17. Inventor: Andreas Aßmann (STMicroelectronics).

Its full text is **not** available this run — only one pre-verified verbatim anchor: "each bin
of the histogram representing a photon count corresponding to a distance from a light-ranging
system." **Quote only this exact sentence if this patent is used at all; do not paraphrase or
attribute any other quote, paragraph number, or claim detail to it** — nothing else about it has
been checked against source text.

Narrative role: establish the *baseline principle* — sweep the histogram left to right, the peak
that rises then falls is the distance — as a brief "first, the principle" beat, then land on the
hero's efficient on-chip implementation. One supporting appearance, not a parallel deep-dive; do
not let it compete with the hero for attention.

## Cluster patents — one-line breadth cue ONLY, do not deep-dive

No full text is available for any of these. Use only the one-line description below (if at all),
as a single aside signaling breadth, not depth — do not attribute verbatim quotes to them:

- US 2021/0302550 — a TDC (time-to-digital converter) builds the histogram bins.
- US 2020/0400792 — multiple SPAD outputs summed into bins.
- US 2018/0253404 — extracting distance out of a histogram.
- US 2024/0353538 — super-resolving the rising edge to sharpen the distance estimate.
- US 2019/0109977 — assembling the grid up to 2,268 zones.

## Recommended structure (5 layers) + analogy seed

1. **Hook** — the purple depth-map demo: "how does this image get made?" (No image asset exists
   for this — see the Figures constraint below; render it in prose, not as a captioned figure.)
2. **Problem** — light is too fast to time directly (light covers ~1 m in ~3.3 ns), so you can't
   just start a stopwatch. Instead you count photons and look at when they came back — statistics,
   not a stopwatch.
3. **Core claim** (verbatim anchor) — sequential bin-by-bin histogram streaming.
4. **Analogy** — every zone gets its own bar chart; the tallest bar's time is the distance; the
   chip reads each bar the instant it arrives instead of holding the whole chart in memory.
5. **Product/stakes** — that is how a fingernail-sized chip runs 2,268 zones at up to 100 fps
   inside a tight power budget.

## Figures — constraint (read before figure selection)

Only 7 figure assets exist, at `input/figures/fig-01.png` … `fig-07.png`, matching the patent's
own FIG. 1–7 (all block diagrams / flowcharts, no photos):

- FIG. 1 [0023] — ToF sensor system block diagram (VCSEL, SPAD arrays, histogram processing
  circuit, MCU, …).
- FIG. 2 [0024] — histogram processing circuit block diagram (correlator + phase/bin computation
  + range/rate calculators).
- FIG. 3 [0025] — flowchart: generating the crosstalk calibration data.
- FIG. 4 [0026] — correlator circuit block diagram (ambient/filter/crosstalk MAC circuits,
  closest-target + strongest-maximum circuits).
- FIG. 5 [0027] — flowchart: bin-serial ToF processing method.
- FIG. 6 [0028] — phase/bin computation circuit block diagram.
- FIG. 7 [0029] — flowchart: on-the-fly median estimation (lean pulse-weighted histogram
  approach).

**The "purple depth-map" hook image is a conceptual reference only (a product GUI demo still) —
it is NOT an available figure asset.** Do not cite it as a numbered figure or invent a caption
for a nonexistent image; describe the demo in prose in the hook, then transition into the real
FIG. 1 / FIG. 2 diagrams as the essay's actual visual anchors. FIG. 1 and FIG. 2 are the
strongest header candidates given the mechanism thesis; FIG. 3–7 are denser circuit/flow detail.
Not every figure needs use — select for audience accessibility, but do not orphan any figure you
do select (`gate_figure_use`).

## Design-intent musts

- The hero, US 2026/0140238, is the sole protagonist. The auxiliary patent appears once, for
  principle only. Do not let the cluster list sprawl into a survey piece.
- Define histogram / zone / multi-zone / peak=distance explicitly in this essay — Articles 2 and
  3 call back to these definitions without re-explaining them.
- Verbatim-quote every patent anchor; never paraphrase claim language.
- Cross-check numeric claims (2,268 zones, 100 fps, power draw, etc.) against the tiered facts
  below before stating them as settled fact.
- Tone: friendly and visual; unpack dToF / SPAD / TDC in plain language on first use.

## Cautions — hold the line against overclaiming

- Do NOT say the system "directly measures the speed of light" or "times light directly" — it
  measures photon-arrival statistics via a histogram, not a literal stopwatch on a photon.
- Do NOT confuse this with iToF (indirect, phase-based ToF) — this is **direct** (d)ToF.
- "First" claims are only allowed in ST's own qualified phrasing (see sourced quote below) —
  never state an unqualified "world's first" or "first multi-zone dToF sensor" claim (multi-zone
  dToF already existed in VL53L5/L8CX; the jump here is resolution + flood illumination, not the
  category itself).
- Inventor Andreas Assmann appears on both the hero and the auxiliary patent, and recurs in
  Article 2 — a light "same engineer, same problem, different angle" thread is fine as an
  optional connective touch, not a forced device.
- SLAM / robotics framing is Article 3's territory. If robotics applications come up at all here
  (e.g. in a closing gesture toward "why this matters"), keep ST's role as supplying senses and
  inputs, not "solving" navigation.

## Product facts — STM VL53L9CX / STEVAL-VL53L9 (tiered sourcing)

These are carried from the series brief's own primary-source pass, not re-verified by me this
session. Identity: dToF (direct Time-of-Flight) 3D LiDAR all-in-one module; mass production
early July 2026 (announced 2026-06-22).

**Verified against ST's own press release** (newsroom.st.com release "p4783", per the series
brief — not re-fetched by me this session):
- 2,268 zones (54×42 grid) — "2.3K zones," the highest multi-zone resolution in category to date.
- 54×42° field of view, up to 100 fps, 5 cm–9 m range.
- On-chip processing.
- Applications listed include small-object detection, SLAM, and obstacle avoidance for
  autonomous navigation (verbatim from the release, per the brief).
- Verbatim company claim: "first direct Time-of-Flight (dToF) 3D LiDAR all-in-one module in ST's
  portfolio" — quote exactly, with the "in ST's portfolio" qualifier intact, if used at all.

**Verified against ST's blog** (blog.st.com/vl53l9, per the series brief):
- BSI-stack SPAD array; metasurface optical element (MOE) + physical IR filter; dual-scan flood
  illumination (vs. dot-scan — reduces dead zones, better on small objects/edges, less motion
  artifact); on-chip ASIC; positioned for AR/VR, drones, humanoid robotics.

**Verified against databrief DB5805 Rev2** (per the series brief; PDF not available to me this
session):
- 71° diagonal FOV, ~1° angular resolution, MIPI + I3C (+I2C) interfaces, application list.

**NOT yet independently verified — the series brief itself flags these as pending a human
datasheet cross-check (ST's main datasheet site blocks automated access). Treat as approximate /
attribute cautiously; do not state as a confirmed spec without a source:**
- 940 nm (invisible) wavelength, Class-1.
- Detector described as a "BSI stacked" SPAD array structure.
- 2x VCSEL emitters + BCD driver.
- ~150 mW power draw (at 30 fps).
- ~1% accuracy (TNR).
- 12.8 x 6.1 x 4.6 mm package.

**Baseline-difference axis:** prior-generation VL53L5/L8CX topped out at ≤64 zones, so 2,268 is
roughly a 35x jump in resolution. Keep "~35x" as an approximation, not a precise ST-stated
figure.

If Phase 1's own web research can independently source any of the "not yet verified" items,
prefer that fresh citation and log it in `fact-check-log.md`; otherwise keep these qualified /
attributed rather than flatly asserted.

## Posture and mode

- **Posture: measured.** Friendly and visual per the series' tone rule, but keep the
  anti-overclaim guards above in force. Default posture; no prior-run lesson overrides it for
  this patent.
- **Mode: strict-execution.** This is a one-shot autonomous pipeline run with no live
  back-and-forth mid-composition, so there is no interactive checkpoint to pause at.

## Series continuity note

This is Article 1 of 3. Articles 2 and 3 will be produced in later runs, reusing this essay's
hero, its vocabulary (histogram / zone / peak=distance), and its anchors as shared series
continuity — keep definitions and analogy language reusable rather than article-1-specific.

## Figures available

FIG. 1–7, all pre-cleaned in `input/figures/`.
