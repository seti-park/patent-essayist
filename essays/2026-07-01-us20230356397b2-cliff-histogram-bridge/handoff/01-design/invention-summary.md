# Invention Summary

## Metadata

- **Patent ID**: US 2023/0356397 A1 (US2023-0356397B2)
- **Title**: Cliff Detection in Robotic Devices
- **Filing date**: 2022-05-03
- **Publication date**: <unknown — not stated on the extracted cover fields; corpus record gives 공개번호 US2023-0356397B2 and 출원일 (filing) 2022-05-03 only>
- **Inventors**: Benoit Rivot, Xingyu Wang
- **Classification**: <unknown on this extraction's own cover metadata — essay-context.md separately supplies corpus-index CPC B25J, G01S17/931; not independently re-verified against USPTO for this run, so not asserted here as a cover-page fact. See fact-check-log.md>
- **Assignee**: STMicroelectronics (Shenzhen) R&D Co. Ltd; STMicroelectronics S.A.

## 발명 명칭 / 기술분야

Cliff detection for mobile robots — turning a multi-zone time-of-flight sensor's own
signal statistics into an early-warning system that lets a robot brake before a stair
edge or curb, not after. Technical field: robotic device navigation and sensing, in
particular the use of a time-of-flight (ToF) SPAD-array sensor mounted on the front of
a mobile robot to anticipate an approaching cliff edge before the robot's chassis passes
over it `[0001]`.

## 종래 문제 / 과제

Conventional cliff detection puts the sensor in the wrong place and gives it too little
warning. Cameras and single-zone or bottom-mounted sensors (ultrasonic cliff detectors,
PIR, single-zone ToF) can only report a cliff once part of the robot's body is already
physically over the edge — the robot cannot change path until it is already committed
`[0004]`, `[0018]`. That forces the robot to move slowly, since slow speed is the only way
to leave enough reaction time between "cliff detected" and "falls off cliff" `[0004]`.
Cameras compound the problem: they need complex vision systems and still cannot report
distance to the edge, only that something changed in the image `[0018]`, `[0025]`.

**Quotable spans:**
- `[0004]`: "the mobile robot cannot detect the cliff until a portion of its body is physically over the edge of the cliff"
- `[0004]`: "the robot must move at low speeds in order to give the robot time to detect the cliff and change its path before it falls over the cliff"
- `[0018]`: "mobile robots cannot detect the cliff until a portion of its body is physically over the edge of the cliff"
- `[0018]`: "cameras require complex camera systems to detect a cliff and cannot provide information about the distance to the cliff"
- `[0025]`: "cameras used to detect a cliff require complex camera systems and cannot provide information about the distance to the cliff"

## 청구항 분석 — 4-layer core mechanism

### Layer 1 — What (one sentence)

A front-mounted, multi-zone time-of-flight sensor compares the statistical distribution
(median ground distance and peak signal intensity) of reflected signals across several
rows of its own zone array, and that row-by-row comparison — not a single reading —
lets the robot detect an approaching cliff edge from three successively closer distance
ranges and change its propulsion before it reaches the edge.

### Layer 2 — How (mechanism)

1. A ToF sensor (102), comprising an array of single-photon avalanche diode (SPAD)
   sensors (114) arranged in rows and columns, is attached to the front of a mobile
   robot (100) and continuously transmits and receives reflected signals while the
   robot is in motion `[0021]`, `[0034]`.
2. A region of interest (ROI) (116) — a group of at least two consecutive rows of
   zones including the bottom row, e.g. the bottom three rows — is designated within
   the SPAD array: first row (118, bottom), second row (120), third row (122) `[0035]`,
   `[0036]`.
3. The controller (108) continuously determines, per row in the ROI: (a) the median
   ground distance (the median, across the zones in that row, of the time-of-flight
   distance to the ground), and (b) the peak rate of the intensity of reflected light
   for that row `[0040]`–`[0042]`.
4. The controller compares these per-row statistics against each other and against an
   ambient light rate (309) to identify a **convergence** — either an intensity
   convergence (a row's peak intensity falls below the ambient rate) or a
   median-distance convergence (the rows' median distances converge to the same
   value, or invert/increase) — and classifies the convergence into one of three
   distance ranges `[0083]`, `[0084]`; claim 1.
5. **Long range** (208–~45 cm from the edge, e.g. 30–60 cm `[0051]`): because the
   third row (122) sits higher on the sensor, it is first to lose reflected signal
   from the floor once the field of view starts to clip the drop-off, so its peak
   intensity falls below the ambient rate (309) first, then the second row (120),
   then the first row (118) `[0049]`–`[0051]`, `[0065]`–`[0067]`; block 502–508.
6. **Medium range** (~30 cm, e.g. 20–40 cm `[0054]`): as the field of view starts
   landing on the edge itself, all three rows' median ground distances begin to drop
   and converge toward the same value (within a threshold, e.g. ≤20%, typically 10%)
   `[0053]`, `[0075]`, `[0100]`; block 602–608.
7. **Short range** (closest to the edge): the ROI loses the presence of the ground
   entirely — either the median distances jump up (they are now measuring the lower
   floor beyond the edge, if the drop is shallow) or fall to zero (if the drop is too
   tall for any reflection to return) `[0056]`, `[0076]`–`[0078]`; block 702–706.
8. On any one of the three detections (or a stricter combination requiring two or
   three ranges to agree, at the designer's option), the controller changes the
   robot's propulsion — braking or altering its path — before the robot's chassis
   reaches the edge `[0068]`, `[0086]`, `[0087]`; claim 1.

**Key components**: mobile robot (100), ToF sensor / SPAD array (102), navigation
system (106), controller (108), memory (109), IMU (112), zones (114), region of
interest / ROI (116), first row (118), second row (120), third row (122), spatial
separation between rows (124), ambient rate (309).

### Layer 3 — Why novel

- **Relative to prior art**: Bottom-mounted or single-zone sensors and PIR/ultrasonic
  cliff detectors are physically confined to reporting the edge only once the sensor
  itself is over it `[0004]`, `[0018]`; camera-based systems substitute a complex
  vision pipeline that still cannot report a metric distance to the edge `[0018]`,
  `[0025]`. This patent's claim 1 differentiates by putting a *forward-facing,
  multi-zone* ToF sensor's own internal row-to-row statistics to work, so the
  anticipation happens well before physical arrival, using one existing sensor rather
  than adding a bottom sensor or camera pipeline.
- **Industry practice contrast**: The same multi-zone ToF sensor and array the patent
  describes ("manufactured by ST Microelectronics, or any other multi-zone ToF sensor
  known in the art" `[0030]`) is also concurrently used by the robot for wall
  tracking, material recognition, and SLAM `[0024]`, `[0027]` — the novelty here is
  not a new sensor, but a new *use* of the sensor's existing zone geometry: reading
  the spatial separation between rows (124) as a signal in itself, rather than only
  reading each zone's raw distance independently.

### Layer 4 — Innovation angles

- **row-comparison-as-anticipation**: the core inventive move — comparing rows of
  zones against each other (not reading a single zone) is what converts a spatial
  snapshot into an early warning, because the spatial separation between rows (124)
  is a known, fixed geometry that a flat floor should preserve and a cliff edge must
  break.
  - Evidence paragraphs: `[0035]`, `[0045]`, `[0046]`
  - Quote anchor refs: `q-0035-1`, `q-0045-1`
- **three-range-graduated-detection**: the same underlying comparison yields three
  successively more certain (and more urgent) detections — long range from intensity
  divergence, medium range from distance convergence, short range from lost ground —
  giving the robot layered warning rather than a single trip-wire.
  - Evidence paragraphs: `[0039]`, `[0060]`, `[0083]`, `[0084]`
  - Quote anchor refs: `q-0060-1`, `q-0083-1`
- **action-before-contact**: the claim does not stop at detection — it requires
  changing propulsion "before reaching the edge," making anticipation, not reaction,
  the claimed outcome. This is the mechanism that converts a depth reading into robot
  behavior.
  - Evidence paragraphs: `[0005]`, `[0019]`, `[0086]`
  - Quote anchor refs: `q-0005-1`, `q-0019-1`
- **single-sensor-multi-function**: the same forward ToF sensor and its ROI logic
  that does cliff detection is explicitly also used for wall tracking, material
  recognition, object detection, and SLAM — cliff detection is one behavior grown out
  of a sensing capability the robot already carries for other tasks, not a bolted-on
  extra sensor.
  - Evidence paragraphs: `[0024]`, `[0027]`, claim 6
  - Quote anchor refs: `q-0027-1`

## Reference number table

| Number | Label | Paragraphs | Figures |
|---|---|---|---|
| 100 | Mobile robot | `[0009]`, `[0010]`, `[0020]`–`[0027]`, `[0032]`–`[0038]`, `[0044]`–`[0059]`, `[0068]`–`[0082]` | FIG. 1, FIG. 2, FIG. 3 |
| 102 | Time-of-flight (ToF) sensor / SPAD array | `[0009]`, `[0020]`, `[0021]`, `[0026]`, `[0029]`–`[0036]`, `[0043]`, `[0045]`, `[0046]`, `[0049]`, `[0062]`, `[0065]`, `[0082]` | FIG. 1, FIG. 2, FIG. 3 |
| 106 | Navigation system | `[0009]`, `[0020]`, `[0023]`, `[0028]`, `[0029]` | FIG. 1 |
| 108 | Controller | `[0028]`, `[0029]`, `[0032]`, `[0033]`, `[0040]`, `[0041]`, `[0053]`, `[0064]`, `[0068]`, `[0071]`, `[0072]` | FIG. 1 |
| 109 | Memory | `[0028]`, `[0032]` | FIG. 1 |
| 112 | Inertial measurement unit (IMU) | `[0028]`, `[0029]`, `[0033]` | FIG. 1 |
| 114 | Zones (of the SPAD array) | `[0034]`–`[0036]`, `[0039]`–`[0046]`, `[0060]`–`[0074]` | FIG. 1 |
| 116 | Region of interest (ROI) | `[0035]`, `[0036]`, `[0039]`, `[0042]`, `[0053]`, `[0056]`, `[0060]`–`[0069]`, `[0075]`, `[0079]`, `[0083]`, `[0089]`, `[0096]` | FIG. 1 |
| 118 | First row (bottom row of ROI) | `[0036]`, `[0045]`, `[0046]`, `[0051]`, `[0062]`, `[0065]`, `[0067]`, `[0072]`, `[0073]` | FIG. 1 |
| 120 | Second row | `[0036]`, `[0045]`, `[0051]`, `[0062]`, `[0065]`, `[0067]`, `[0072]`, `[0073]` | FIG. 1 |
| 122 | Third row (top row of ROI) | `[0036]`, `[0045]`, `[0049]`, `[0051]`, `[0062]`, `[0065]`–`[0067]`, `[0072]`, `[0073]` | FIG. 1 |
| 124 | Spatial separation between rows | `[0035]`, `[0045]`, `[0046]`, `[0062]`, `[0073]` | FIG. 1 |
| 200/212/214/218 | Schematic-diagram labels (per-stage diagram numbers, FIGS. 2A–2D) | `[0044]`, `[0047]`, `[0052]`, `[0055]` | FIG. 2 |
| 202 | Ground | `[0038]`, `[0044]`, `[0048]`, `[0059]`, `[0070]`–`[0080]` | FIG. 2, FIG. 3 |
| 204 | Edge of the cliff | `[0038]`, `[0044]`–`[0080]`, `[0086]`–`[0107]` | FIG. 2, FIG. 3 |
| 206 | Field-of-view / signal transmission arrows (drawing annotation) | (figure-only annotation, FIGS. 2A–2D) | FIG. 2 |
| 208 | Distance range too far to detect the edge | `[0044]`, `[0046]` | FIG. 2, FIG. 3 |
| 209 | Ground past the edge (lower ground) | `[0049]`, `[0056]`, `[0065]`, `[0077]`–`[0079]` | FIG. 2, FIG. 3 |
| 210 | Long distance range | `[0047]`–`[0051]`, `[0058]`, `[0060]`–`[0068]`, `[0079]` | FIG. 2, FIG. 3 |
| 211 | Signal reflected past the edge, long-range case (drawing annotation) | (figure-only annotation, FIG. 2B) | FIG. 2 |
| 216 | Medium distance range | `[0052]`–`[0054]`, `[0058]`, `[0060]`, `[0069]`, `[0075]` | FIG. 2, FIG. 3 |
| 220 | Short distance range | `[0055]`, `[0056]`, `[0058]`, `[0060]`, `[0069]`, `[0076]`, `[0079]`, `[0080]` | FIG. 2, FIG. 3 |
| 302 | Graph (overall figure label) | `[0057]`, `[0059]`, `[0061]`, `[0070]` | FIG. 3 |
| 304 | Peak-intensity line, first row | `[0061]`–`[0063]` (drawing annotation) | FIG. 3 |
| 306 | Peak-intensity line, second row | `[0061]`–`[0063]` (drawing annotation) | FIG. 3 |
| 308 | Peak-intensity line, third row | `[0061]`–`[0063]` (drawing annotation) | FIG. 3 |
| 309 | Ambient rate | `[0063]`–`[0068]`, `[0079]` | FIG. 3 |
| 310 | Median-ground-distance line, third row | `[0072]`, `[0073]`, `[0077]` (drawing annotation) | FIG. 3 |
| 312 | Median-ground-distance line, second row | `[0072]`, `[0073]`, `[0077]` (drawing annotation) | FIG. 3 |
| 314 | Median-ground-distance line, first row | `[0072]`, `[0073]`, `[0077]` (drawing annotation) | FIG. 3 |
| 402/404/406 | Process-flow blocks, three-range overview | `[0082]`–`[0087]` | FIG. 4 |
| 502/504/506/508/510 | Process-flow blocks, long-range detection | `[0089]`–`[0094]` | FIG. 5 |
| 602/604/606/608/610 | Process-flow blocks, medium-range detection | `[0096]`–`[0101]` | FIG. 6 |
| 702/704/706/708 | Process-flow blocks, short-range detection | `[0103]`–`[0108]` | FIG. 7 |

## Figure relationships

| Figure | Paired with | Relationship | Page (if known) |
|---|---|---|---|
| FIG. 1A | FIG. 1B, FIG. 1C | same-page sub-figure set — robot overview, navigation-system block diagram, ToF sensor/ROI detail | <unknown — page not visible on this extraction> |
| FIG. 2A | FIG. 2B, FIG. 2C, FIG. 2D | progressive sequence (too-far → long range → medium range → short range) | <unknown> |
| FIG. 3 | (standalone) | single combined graph covering the same event as FIGS. 2A-2D, plotted over time/distance | <unknown> |
| FIG. 4 | FIG. 5, FIG. 6, FIG. 7 | overview-then-detail sequence — FIG. 4 is the three-range overview flowchart; FIGS. 5/6/7 are its long/medium/short-range sub-flowcharts respectively | <unknown> |

## Quote anchor table

| Quote ID | Paragraph | Verbatim text | Significance |
|---|---|---|---|
| q-0004-1 | `[0004]` | "the mobile robot cannot detect the cliff until a portion of its body is physically over the edge of the cliff" | prior-art-contrast |
| q-0004-2 | `[0004]` | "the robot must move at low speeds in order to give the robot time to detect the cliff and change its path before it falls over the cliff" | prior-art-contrast |
| q-0018-1 | `[0018]` | "cameras require complex camera systems to detect a cliff and cannot provide information about the distance to the cliff" | prior-art-contrast |
| q-0019-1 | `[0019]` | "Embodiments of the present application relate to a mobile robot that utilizes a time of flight (ToF) sensor that can be used to anticipate an approaching edge of a cliff from three different distance ranges." | claim-supporting |
| q-0005-1 | `[0005]` | "comparing a statistical distribution of the reflected signals received at a plurality of different rows of zones configured by the array of SPADs in a region of interest (ROI) of the ToF sensor and based on the comparing detecting an approaching of the edge of the cliff" | claim-supporting |
| q-0026-1 | `[0026]` | "the array of SPADs allow the mobile robot 100 to detect a cliff at three different ranges of distance: long range, medium range, and short range distances" | mechanism-critical |
| q-0027-1 | `[0027]` | "The single multi zone ToF sensor 102 may be used by the controller to perform wall tracking, material recognition, cliff detection, and SLAM." | mechanism-critical |
| q-0035-1 | `[0035]` | "a spatial separation 124 between the rows of the zones 114 may be leveraged to anticipate a cliff" | mechanism-critical |
| q-0045-1 | `[0045]` | "the lower the row is on the ToF sensor 102, the shorter the distance from the row to the ground 202" | mechanism-critical |
| q-0046-1 | `[0046]` | "because reflected signals have to travel farther to rows higher on the ToF sensor 102, the lower the row, the higher the intensity of the received signal" | mechanism-critical |
| q-0050-1 | `[0050]` | "The factor may be between five and one hundred times the ambient rate, for example fifty time below the ambient rate." | quantitative |
| q-0051-1 | `[0051]` | "the long distance range 210 may be between 30 cm and 60 cm from the edge 204, for example 45 cm" | quantitative |
| q-0054-1 | `[0054]` | "the medium distance range 216 may be between 20 cm and 40 cm from the edge 204, for example 30 cm" | quantitative |
| q-0043-1 | `[0043]` | "The ToF sensor 102 may be attached to the robotic device 100 so that it is between 5 cm to 7 cm from the ground, for example, 6 cm." | quantitative |
| q-0060-1 | `[0060]` | "The median distance between the rows of zones 114 in the region of interest (ROI) 116 may be used to detect the edge 204 from a short distance range 220 and a medium distance range 216. The peak intensity rate of photons received by each row of zones 114 in the ROI 116 may be used to detect the edge 204 from a long distance range 210." | mechanism-critical |
| q-0064-1 | `[0064]` | "in order to detect that the decrease in the peak intensity rate of the rows of zones 114 is due to the edge 204, the peak intensity rate must be lower than the ambient rate 309" | mechanism-critical |
| q-0083-1 | `[0083]` | "a statistical distribution of the reflected signals received at a plurality different rows of the array of zones 114 in a region of interest (ROI) 116 of the ToF sensor 102 may be compared. Based on the comparing of the statistical distribution the reflected signals an approaching edge 204 of a cliff may be detected." | claim-supporting |
| q-0086-1 | `[0086]` | "based on detecting the approaching edge 204 of the cliff, the path of the mobile robot 100 may be change such that a propulsion of the mobile robot 100 changes before reaching the edge 204" | claim-supporting |
| q-0100-1 | `[0100]` | "the threshold percent difference may a percentage less than 20%" | quantitative |

## Timeline

- **Filing date**: 2022-05-03
- **Publication date**: <unknown on this extraction's own cover fields — corpus record labels this "US2023-0356397B2" (a B2-suffixed grant number in the corpus identifier), consistent with essay-context.md's framing of this as a granted claim set, but the grant/publication date itself is not present in the extracted cover metadata. Do not assert a specific publication date.>
- **Examination period**: <unknown — cannot compute without a verified publication/grant date>
- **Prior-art chronology**: (none cited by application number/date in this patent's own text — the Background section `[0002]`–`[0004]`, `[0016]`–`[0018]` describes prior-art *approaches* — bottom-mounted sensors, PIR, ultrasonic, cameras — generically, without citing specific prior-art patent numbers or dates to build a chronology table against.)

## Prior-art references + differentiation

- **Bottom/underside-mounted sensors and cameras** (described generically at `[0004]`, `[0018]`, `[0025]`; no specific citation number given): significance — this is the baseline the patent argues against. Differentiation: a bottom-mounted or single-zone sensor (ultrasonic, PIR, single-zone ToF) cannot report a cliff until the robot's body is already over the edge, forcing low speeds; a camera can detect a scene change but not a metric distance to the edge. This patent's claim 1 differentiates on both axes at once — forward-mounted (not bottom-mounted) and multi-zone with a ranged distance output (not scene-change-only).

## 유리한 효과 + 정량 데이터

Because the ToF sensor sits on the front of the robot rather than underneath it, and
because it reads multiple rows at once instead of one zone, the robot can anticipate the
edge across three successively closer ranges and change its propulsion before any part of
it reaches the edge — which the specification states directly increases travel speed and
lets the path be optimized ahead of time, instead of reacting only after physical contact
with the edge is imminent `[0019]`, `[0026]`.

**Quotable spans:**
- `[0026]`: "One advantage of this is that it allows the mobile robot 100 to move at increased speeds because it can anticipate a cliff before it reaches it. Another advantage of anticipating a cliff is that the path of the mobile robot 100 may be optimized ahead of time."
- `[0019]`: "this allows for the mobile robot to travel at faster speeds by changing its propulsion prior to reaching the cliff, resulting in a more efficient mobile robot"

| Metric | Value | Paragraph |
|---|---|---|
| Sensor height above ground | 5 cm–7 cm (example: 6 cm) | `[0043]` |
| Long distance range | 30 cm–60 cm from edge (example: 45 cm) | `[0051]` |
| Medium distance range | 20 cm–40 cm from edge (example: 30 cm) | `[0054]` |
| Long-range intensity-drop factor | 5x–100x below ambient rate (example: 50x) | `[0050]` |
| Medium-range convergence threshold | <20% difference (example: 10%) | `[0053]`, `[0100]` |
| ROI size (example embodiment) | bottom 3 rows of an 8x8 zone array | `[0034]`, `[0036]`, claim 4 |

<!-- No revision-loop triggers encountered during Step 1 extraction of this run. -->
