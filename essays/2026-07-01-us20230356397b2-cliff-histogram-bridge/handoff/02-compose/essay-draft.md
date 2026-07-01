---
essay_id: 2026-07-01-us20230356397b2-cliff-histogram-bridge
patent_reference: US 2023/0356397 A1
spine_source: handoff/01-design/thesis-spine.md
draft_version: 6
mode_used: walkthrough
posture_used: measured
---

# The Same Histogram That Reads Distance Now Reads a Cliff

![FIG. 1: the mobile robot, its navigation stack, and the region of interest inside its sensor.](figures/fig-01AB.png)

*FIG. 1: the mobile robot (100) carries a single front-mounted time-of-flight sensor (102) that feeds a navigation system (106) doing four jobs at once, wall tracking, material recognition, cliff detection, and SLAM (FIG. 1A), built from a controller (108), an IMU (112), and memory (109) around that one sensor (FIG. 1B). FIG. 1C opens the sensor itself: an 8x8 grid of zones (114), with a region of interest (116) drawn around the bottom three rows, first row (118), second row (120), third row (122), separated by a fixed, known spacing (124).*

## A Robot Vacuum Reads the Floor Before It Falls

Most cliff sensors on a mobile robot sit on the underside, pointed straight down. For decades that was the standard placement: a downward-looking ultrasonic or infrared unit that reports a drop only once it is already hanging over one. This patent's sensor sits on the front instead, and it never looks straight down at all.

That single relocation is not the invention. The invention is what the front-mounted sensor does with a whole grid of readings instead of one. A conventional bottom sensor is confined to reporting the edge "until a portion of its body is physically over the edge of the cliff" [0004], which is also why "the robot must move at low speeds in order to give the robot time to detect the cliff and change its path before it falls over the cliff" [0004].

A camera does not fix this either: it "cannot provide information about the distance to the cliff" [0018], only that something in the image changed.

This patent's answer widens the question. It is not "why doesn't a robot vacuum fall down the stairs," it is "how does a sensor see a stair edge coming before it arrives," and the same question scales up to a humanoid's foot.

## A Depth Map Is a Photograph, Not a Warning

A single time-of-flight reading is a snapshot: a number, a distance, a moment. A snapshot cannot warn anyone of anything, because a warning requires a *before* and an *after* to compare against each other. One frame has neither. This is the actual gap the patent is closing, not a faster sensor or a wider field of view, but the difference between a measurement and a comparison.

Cameras compound the same gap from the other direction: they "require complex camera systems to detect a cliff and cannot provide information about the distance to the cliff" [0018], trading the single-number problem for a whole vision pipeline that still cannot say how far away the edge is. What turns any of this into a decision the robot can act on, rather than a fact it merely records, is the subject of the next section.

## The Sensor Compares Rows Against Each Other, Not One Reading

Here is the callback this series has been building toward. The same statistical-distribution, same multi-zone comparison that turned a photon count into a trustworthy distance reading, and then filtered that reading against noise and false targets, is reused here for something else entirely: catching a robot before it falls.

Claim 1 states it directly, and it is worth quoting exactly as filed, because the essay's entire argument rests on this one sentence: "comparing a statistical distribution of the reflected signals received at a plurality of different rows of zones configured by the array of SPAD sensors in a region of interest (ROI) of the ToF sensor and based on the comparing detecting an approaching of the edge of the cliff, the comparing comprising identifying a convergence of an intensity of the reflected signals or of a median distance to a ground."

Picture the sensor's zone array as a small grid of tiles, an 8x8 checkerboard sitting on the robot's front bumper, six centimeters above the ground on the version this patent describes [0043]. The region of interest carves out the bottom three rows of that checkerboard, first, second, and third row, stacked directly on top of each other [0035], [0036].

Each row keeps its own running tally: a bar chart of how many photons came back, and a running median of how far away the floor is, updated continuously as the robot rolls forward.

**The controller is not reading one bar chart. It is watching three bar charts drift apart.** On flat floor, the three rows agree with each other in a fixed, predictable way, because a lower row on the sensor is physically closer to the ground and a higher row is farther away, so their readings should always differ from each other by the same fixed amount. The moment that fixed relationship breaks is the moment the floor is no longer flat, and it breaks in three recognizable stages, matched to three distance ranges.

Long range comes first, out around 45 centimeters (the patent's stated range is 30 to 60) [0051]: the highest of the three rows loses its floor reflection first, and its photon count falls to a small fraction of the ambient light level, "between five and one hundred times" below it [0050].

Next is medium range, closer in around 30 centimeters (stated range 20 to 40) [0054]: all three rows' distance readings begin sliding toward one shared number, because the field of view is now landing on the edge itself rather than the floor before it. Short range is the last and simplest stage: the ground disappears from all three rows at once, either the reading jumps upward (a shallow drop, now measuring the lower floor beyond it) or falls to nothing (a drop too deep for any signal to return).

The patent's own summary of the method restates the same idea in plain method-steps: "a statistical distribution of the reflected signals received at a plurality different rows of the array of zones 114 ... may be compared. Based on the comparing ... an approaching edge 204 of a cliff may be detected" [0083]. FIG. 1 makes the geometry itself visible, before any of these three stages even begins.

## One Row Reading Farther Means the Floor Is Gone There

The reason any of this works comes down to one geometric fact, and it is worth stating plainly: "the lower the row is on the ToF sensor 102, the shorter the distance from the row to the ground" [0045]. A lower row is closer to the floor by definition, and because "reflected signals have to travel farther to rows higher on the ToF sensor 102, the lower the row, the higher the intensity of the received signal" [0046].

That relationship is fixed by where the rows physically sit, not by anything the floor is doing. A flat floor obeys it every single reading.

FIG. 2 draws exactly this sequence, the robot's own beam grazing the edge, then slipping past it into empty air, across the four distances the essay has been narrating stage by stage. FIG. 3's graph is the same event turned into six lines: three median-distance lines and three peak-intensity lines, sitting flat and evenly spaced while the floor holds.

The peak-intensity lines drop through the ambient rate one after another first; then the median-distance lines converge toward each other as the edge itself comes into view; then, at the instant the sensor loses the near floor entirely, the three median-distance lines jump up together, reading the farther floor beyond the edge.

**One row suddenly reading much farther than the fixed geometry allows is not a data anomaly. It is the floor announcing that it is gone there.** That is the entire trick: not a smarter sensor, but a controller that already knows what "normal" looks like well enough to notice the exact instant reality stops matching it.

## The Three-Range Check Runs a Fixed Test, Not a Vague Impression

A skeptical read of the previous section is fair: a change in floor material, dark carpet next to light tile, could plausibly weaken a signal too, and mistaking that for a cliff would be worse than useless. The patent's flowcharts (FIGS. 4 through 7) show why that mistake is checked for. FIG. 4 restates the whole method in three blocks: sense while moving [0082], compare the rows and detect an approaching edge, then change the robot's propulsion before it reaches that edge [0086].

FIG. 5 makes the long-range test literal. A peak intensity is only treated as a cliff signal if it falls below a stated multiple of the *measured* ambient light level, not an arbitrary drop, so a merely darker floor that never crosses that ambient-relative threshold does not trigger a false stop.

FIG. 6 runs a different check for the medium range: not ambient light, but whether the rows' distance readings have moved within a set percentage of each other, a convergence test that works the same in bright light or dark.

FIG. 7 covers the simplest case, whether the ground has been lost entirely, and brings the ambient-light check back only for the sub-case where distances jump upward, as a guard against briefly glimpsing a lower floor rather than a genuine edge. Three separately-triggered tests, not one test run three times, is what keeps "the floor changed color" from reading as "the floor ended."

## The Same Trick Still Runs Under 35 Times More Zones

The payoff the patent states for itself is speed, not just safety: "One advantage of this is that it allows the mobile robot 100 to move at increased speeds because it can anticipate a cliff before it reaches it. Another advantage of anticipating a cliff is that the path of the mobile robot 100 may be optimized ahead of time" [0026].

Anticipating a hazard, rather than only reacting to one already underway, is what "allows for the mobile robot to travel at faster speeds by changing its propulsion prior to reaching the cliff, resulting in a more efficient mobile robot" [0019]. A robot that has to crawl to leave itself reaction time is a slower robot; a robot that already knows the edge is coming three ranges out does not have to crawl.

What makes this durable rather than a one-generation trick is that the row-comparison idea does not care how many zones the sensor has. The patent's own example uses just three rows compared against each other [0036] to work at all.

STMicroelectronics announced its VL53L9CX sensor in June 2026 with 2,268 zones arranged 54 by 42, roughly 35 times the zone count of the prior VL53L5/L8CX generation's 64 zones or fewer, ST's own words for it: "1st 3D ToF LiDAR sensor with 2.3K zones and flood illumination." (ST is careful about its own wording here too: its press release calls the VL53L9 "the first direct Time-of-Flight (dToF) 3D LiDAR all-in-one module in ST's portfolio," a qualified first inside its own product line, not a claim that multi-zone depth sensing itself is new.)

A sensor with far more zones in 2026 is still running the same comparison a 2022-filed patent already claimed, because the trick was never about zone count. It was about noticing when a few of those zones stop agreeing with each other.

ST's own application list for a sensor like this names "small object detection, SLAM, obstacle avoidance for autonomous navigation" directly, alongside robotics, drones, and humanoids. That is the honest way to describe what this patent opens onto, and it is worth being precise about what it does not claim. A companion ST filing, US2022-0184815, widens the same idea from one cliff to a general habit: "analyzing the image information to determine whether to modify the movement path of the mobile robot." Depth reading becomes a path decision, generalized past the specific case of an edge.

A wider cluster of ST patents extends the same reasoning further outward, anti-collision (US2021-0268903), histogram-based scene change (US2026-0087695), depth fused with inertial data (US2022-0067346), multi-IMU robotics fusion (US2024-0191996), and egomotion tracking (US2022-0080979), each a piece of the same picture, none of them expanded into a case of its own here.

What none of this amounts to, on its own, is SLAM. Detecting one cliff, once, from one sensor, is a narrow trick, and calling it a bridge to something as large as building and holding a map of a room is a fair objection to raise.

**STM is not solving SLAM here. It is building one of the senses, and a reflex, a SLAM stack needs if it is going to trust the ground under it.** A system that can map a room but cannot notice the room has a step in it has not solved navigation; it has drawn a very detailed floor plan of a fall.

The next sensor generation will keep shipping with more zones, and every one of them will still be running some version of the row-against-row comparison this 2022 filing already claimed. The question worth watching is not whether the zone count keeps climbing. It is whether the same reflex holds up in a body with far more ways to fall than a disc-shaped vacuum ever had. 🤔

# Sources

## Patents
- US 2023/0356397 A1, "Cliff Detection in Robotic Devices," STMicroelectronics (Shenzhen) R&D Co. Ltd / STMicroelectronics S.A., filed 2022-05-03, inventors: Benoit Rivot, Xingyu Wang.
- US 2022/0184815, "Controlling Movement of a Mobile Robot," STMicroelectronics R&D, filed 2020-12-15, inventors: James M. Hanratty, Jeffrey M. Raynor.
- US 2021/0268903 (anti-collision).
- US 2026/0087695 (histogram-based scene change).
- US 2022/0067346 (depth and inertial fusion).
- US 2024/0191996 (multi-IMU robotics fusion).
- US 2022/0080979 (egomotion).

## Official statements
- STMicroelectronics, VL53L9CX press release and blog (2026-06-22).

## Technical specs
- STMicroelectronics, VL53L9CX data brief (FoV, zone count, range, interfaces).
