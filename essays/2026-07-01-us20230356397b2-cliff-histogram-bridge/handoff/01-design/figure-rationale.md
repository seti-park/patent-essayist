# Figure Rationale

## FIG. 1 — System overview + ROI detail (fig-01AB.png: 1A-1B; fig-01C.png: 1C)

- **Purpose**: FIG. 1A shows the mobile robot (100, drawn as a disc-shaped vacuum-style
  robot) with a front-mounted ToF sensor (102) feeding a "Key Environment Extraction"
  block inside the navigation system (106), which fans out into wall tracking, material
  recognition, cliff detection, and SLAM — and cliff detection itself fans out into
  close/medium/long range outputs. FIG. 1B is the navigation system's own block diagram:
  IMU (112) and ToF sensor (102) both feed the controller (108), with memory (109)
  alongside. FIG. 1C isolates the ToF sensor's own zone array (114, an 8x8 grid of square
  zones) and marks the region of interest (116) as the bottom three rows — first row
  (118), second row (120), third row (122) — with the spatial separation between rows
  (124) called out explicitly between the bottom two rows.
- **Intended effect**: Establishes, before any mechanism explanation, that this is one
  sensor doing several jobs (grounding the "single-sensor-multi-function" Layer-4 angle)
  and that cliff detection is one branch of a larger navigation stack — then FIG. 1C
  immediately narrows the reader's attention to the exact three rows of zones that carry
  the entire cliff-detection claim, so the mechanism section that follows has a concrete
  picture to point at rather than an abstract "rows of zones" description.
- **Draft compliance note**: caption_role `header_composite` calls for a detailed header
  caption; per the mechanical gotcha flagged in `figure-selection.md`, ensure the caption
  or surrounding prose includes at least one bare "FIG. 1" token (not only "FIG. 1A" /
  "FIG. 1B" / "FIG. 1C").

## FIG. 2 — The approach, in four stages (fig-02AB.png: 2A-2B; fig-02CD.png: 2C-2D)

- **Purpose**: Four schematic side-view diagrams of the same robot (100) traveling across
  the same rippled ground (202) toward the same cliff edge (204), at four successive
  distances. 2A: too far to detect anything — the sensor's field of view only sees flat
  ground ahead (distance range 208). 2B: long range (210) — the sensor's forward-cast
  beam (206) now grazes the edge and a dashed portion (211) shows it slipping past the
  edge to the lower ground beyond (209). 2C: medium range (216) — the beam angle has
  steepened further as the robot has closed distance. 2D: short range (220) — the beam
  (206, now drawn dashed, i.e. weak/lost return) points down past the edge to the lower
  ground (209), visually showing signal loss.
- **Intended effect**: This is the event the whole essay narrates, made literal and
  sequential — the reader watches the same robot get closer across four frames and can
  see, stage by stage, why the sensor's read of the world has to change as the edge comes
  into range. It is the visual backbone for the "row-by-row reading of the floor" analogy
  section, since each frame corresponds to a distinct row-comparison behavior described
  in FIG. 3's graph.
- **Draft compliance note**: same bare-token requirement as FIG. 1 — see
  `figure-selection.md`'s mechanical gotcha note. At least one bare "FIG. 2" token is
  required in the draft in addition to "FIG. 2A"/"FIGS. 2A-2D"-style captions.

## FIG. 3 — The graph: three lines drift, converge, then spike (fig-03.png)

- **Purpose**: A single time/distance-axis graph plotting six lines across the same
  four-stage approach as FIG. 2: three "Median Ground Distances" lines (one per row —
  310 third row, 312 second row, 314 first row) and three "Peak Intensities" lines (304
  first row, 306 second row, 308 third row), all measured against a dashed ambient rate
  (309). Reading left to right: in the "too far" zone the three median-distance lines sit
  at three flat, evenly stepped levels (the fixed spatial separation between rows shows
  up directly as three parallel lines); moving through long and medium range the three
  peak-intensity lines start dropping toward and through the ambient-rate line one after
  another (third row first, since it is highest on the sensor and loses ground-reflection
  soonest), while the three median-distance lines begin to converge toward one shared
  value; at the edge itself, all six lines jump sharply upward together (the sensor is
  now reading the lower floor beyond the edge, or losing the ground return entirely).
- **Intended effect**: This is, per essay-context.md's own figure note, the single best
  visual for the core mechanism — it makes the abstract claim language ("identifying a
  convergence of an intensity ... or of a median distance") into something the reader can
  see happen: flat parallel lines (normal floor) that drift, cross, and then leap
  (the cliff). It is the figure that should carry the most weight in the 3-core-claim /
  4-analogy sections, since it visually IS the histogram-over-zones comparison the
  thesis's callback describes.

## FIG. 4 — The claimed method, three blocks (fig-04.png)

- **Purpose**: A three-block flowchart: (402) move the robot toward the edge while the
  ToF sensor senses reflected signals; (404) compare the statistical distribution of
  reflected signals across the ROI's rows of zones and, based on that comparison, detect
  an approaching edge; (406) in response, change the robot's propulsion before reaching
  the edge. This is claim 1 restated as a diagram.
- **Intended effect**: Gives the reader a clean, three-step visual restatement of the
  claim immediately after the mechanism has been built up in prose and in FIGS. 2-3 — it
  functions as a recap/anchor rather than new information, reinforcing that "compare,
  then act" is the entire inventive step.

## FIG. 5 — Long-range test: peak intensity vs. ambient (fig-05.png)

- **Purpose**: Decision-diamond flowchart: determine the peak rate of intensity across
  the ROI's rows (502); ask whether at least one row's peak intensity has fallen to or
  below a factor of the ambient rate (504); if yes, detect the edge from long range (506)
  and change propulsion before reaching the edge (508); if no, the edge is not yet
  detected from long range (510).
- **Intended effect**: Makes explicit that the long-range detection is a genuine
  cross-check (a fixed factor threshold against a measured ambient light level), not a
  vague "the signal got weaker" claim — useful for grounding the adversarial-defense
  concern that a change in floor material, not a cliff, could produce a similar reading.

## FIG. 6 — Medium-range test: do the medians converge? (fig-06.png)

- **Purpose**: Decision-diamond flowchart: determine median distances between each ROI
  row and the ground (602); ask whether the median distances converge to a similar
  distance (604); if yes, detect the edge from medium range (606) and change propulsion
  (608); if no, the edge is not yet detected from medium range (610).
- **Intended effect**: Shows the second of the two independent metrics (median distance,
  as opposed to FIG. 5's peak intensity) as its own clean decision test — reinforces that
  the patent's "convergence" language in claim 1 covers two distinct, independently
  checkable signals, not one.

## FIG. 7 — Short-range test: is the ground gone? (fig-07.png)

- **Purpose**: Decision-diamond flowchart: ask whether the presence of the ground is lost
  (702); if yes, detect the edge from short range (704) and change propulsion before
  reaching the edge (706); if no, the edge is not detected from short range (708).
- **Intended effect**: The simplest and most visually final of the three range tests —
  useful as a closing beat for the mechanism section, since "the ground is just gone" is
  the most intuitively graspable of the three detections and pairs naturally with the
  analogy section's "the floor is gone there — stop" framing.

<!-- No revision-loop triggers encountered during Step 9 of this run. -->
