# Fact-Check Log

## External facts

| Fact ID | Claim | Source URL | Tier | Sources category |
|---|---|---|---|---|
| st-vl53l9cx-press-release-2026 | STMicroelectronics announced the VL53L9CX, a direct Time-of-Flight (dToF) 3D LiDAR all-in-one module (evaluation board STEVAL-VL53L9), with mass production announced for early July 2026 (announcement dated 2026-06-22). ST's own verbatim claim: "VL53L9 is the first direct Time-of-Flight (dToF) 3D LiDAR all-in-one module in ST's portfolio" (a qualified first, within ST's own portfolio — multi-zone dToF already existed via VL53L5/L8). | <URL not independently re-fetched this run — attributed narratively in essay-context.md as "ST press release"; see search-log.md query 1 and Notes below> | tier-1 | Official statements |
| st-vl53l9cx-blog-2026 | ST blog verbatim: "1st 3D ToF LiDAR with 2.3K zones and flood illumination." Resolution: 2,268 zones (54x42) — described as the industry's highest multi-zone resolution; the prior generation VL53L5/L8CX topped out at 64 zones or fewer (roughly a 35x jump). | <URL not independently re-fetched this run — attributed narratively in essay-context.md as "Blog"; see search-log.md query 2 and Notes below> | tier-1 | Official statements |
| st-vl53l9cx-datasheet-specs-2026 | FoV/range: 54x42 deg FoV (2,268 zones), 71 deg diagonal FoV at 1 deg angular resolution, 5cm-9m range, up to 100fps. Detection: BSI-stack SPAD array; dual-scan flood illumination (vs. dot-scan) removes dead zones and improves small-object/edge detection and motion artifacts. Optics/processing: on-chip SoC does histogram processing plus algorithmic correction to remove cover-glass crosstalk and veiling glare; calibration-free. Outputs: depth (3D) / 2D IR (active and passive) / reflectance / confidence — AI-ready for MCU edge AI. First ToF sensor with MIPI and I3C interfaces (plus I2C). Applications (ST press release, verbatim): "small object detection, SLAM, obstacle avoidance for autonomous navigation" plus home/building/city automation, smart glasses (AR), industrial, robotics/drones/humanoids, edge AI. | <URL not independently re-fetched this run — attributed narratively in essay-context.md as "data brief"; see search-log.md query 3 and Notes below> | tier-2 | Technical specs |
| secondary-patent-us2022-0184815 | US2022-0184815, "Controlling movement of a mobile robot" — filed 2020-12-15, inventors James M. Hanratty and Jeffrey M. Raynor, assignee STMicroelectronics R&D, CPC G05D1 (robot position control), B25J. Anchor: "analyzing the image information to determine whether to modify the movement path of the mobile robot." Used only to generalize the hero's specific cliff case to general navigation, in a sentence or short passage — not as a second case study. | https://patents.google.com/ (patent number US2022-0184815; specific record URL not independently re-fetched this run — see search-log.md query 4) | tier-1 | Patents |
| horizon-cluster-us2021-0268903 | US2021-0268903 A1, "Speed Measurement Using Time-of-Flight Sensing and Anti-Collision Protection Using Time-of-Flight Sensing" — filed 2021-02-15, published 2021-09-02, inventor Thomas Perotto, assignee STMicroelectronics (Grenoble 2) SAS. Cited only as a line/clause (anti-collision), never expanded into a case. | patent document itself (USPTO Patent Application Publication front page, user-supplied PDF, post-acceptance) | tier-1 | Patents |
| horizon-cluster-us2026-0087695 | US2026-0087695 A1, "Compact Normalized Histograms and Scene Change Indicator" — filed 2024-09-25, published 2026-03-26, inventors Olivier Pothier, Thierry Lebihen, Victor Macela, assignee STMicroelectronics International N.V. Cited only as a line/clause (histogram-based scene change), never expanded into a case. | patent document itself (USPTO Patent Application Publication front page, user-supplied PDF, post-acceptance) | tier-1 | Patents |
| horizon-cluster-us2022-0067346 | US2022-0067346 A1, "System and Method for Detecting Human Presence Based on Depth Sensing and Inertial Measurement" — filed 2020-08-28, published 2022-03-03, inventors Xiaoyong Yang, Kalyan-Kumar Vadlamudi-Reddy, assignee STMicroelectronics, Inc. Cited only as a line/clause (depth + inertial fusion), never expanded into a case. | patent document itself (USPTO Patent Application Publication front page, user-supplied PDF, post-acceptance) | tier-1 | Patents |
| horizon-cluster-us2024-0191996 | US2024-0191996 A1, "System and Method for Time Synchronized Fusion of Multiple Inertial Sensors" — filed 2022-12-13, published 2024-06-13, inventors Swapnil Sayan Saha, Denis Ciocca, Mahesh Chowdhary, assignee STMicroelectronics International N.V. Cited only as a line/clause (multi-IMU robotics fusion), never expanded into a case. | patent document itself (USPTO Patent Application Publication front page, user-supplied PDF, post-acceptance) | tier-1 | Patents |
| horizon-cluster-us2022-0080979 | US2022-0080979 A1, "Method for Motion Estimation in a Vehicle, Corresponding Device and Computer Program Product" — filed 2021-09-09, published 2022-03-17, inventors Nicola Matteo Palella, Leonardo Colombo, Andrea Donadel, Roberto Mura, Mahaveer Jain, Joelle Philippe, assignees STMicroelectronics S.r.l. / STMicroelectronics, Inc. / STMicroelectronics (Grand Ouest) SAS. Cited only as a line/clause (egomotion / vehicle motion estimation), never expanded into a case. | patent document itself (USPTO Patent Application Publication front page, user-supplied PDF, post-acceptance) | tier-1 | Patents |
| imu-gnss-caution-us2019-0033466 | US2019-0033466 is explicitly flagged as an IMU/GNSS-only navigation patent, NOT a depth-bridge patent — must not be treated like the hero or secondary patent even if it appears in the horizon paragraph as context. | https://patents.google.com/ (patent number US2019-0033466; specific record URL not independently re-fetched this run — see search-log.md query 6) | tier-1 | Patents |

## Notes

- The original six rows above were **inherited** from `input/essay-context.md`'s "External
  facts available for this run" section (dated 2026-06-30, verified against ST first-party
  sources), not independently re-verified by this Phase 1 run — see `search-log.md` for
  the full inheritance note. This run did not fabricate or re-derive any external fact
  beyond what essay-context.md marked "Verified — safe to cite as fact."
- **Post-acceptance update (human-post-accept):** the single bundled
  `horizon-cluster-patents-2026` row (patent numbers only, no title/inventors/dates, sourced
  to a generic, not-independently-fetched Google Patents placeholder) was split into 5
  individual rows and fully verified after the user supplied the actual USPTO Patent
  Application Publication PDFs for all five horizon-cluster patents. Title, inventors,
  filing date, and publication date for each are now read directly from each patent's own
  front page (the primary source itself, stronger than the prior placeholder URL). None of
  the five are granted patents (all are `A1` publication-kind application publications, no
  registration/grant date applies). This resolves the `sources-entry-template-drift` gap
  pass-6 flagged (as a disclosed, non-blocking gap) in every editorial review round of this
  run — see `handoff/03-edit/revision-notes.md` for the delta record.
- The following items are listed in essay-context.md as **"Pending confirmation"** and are
  deliberately EXCLUDED from this log's load-bearing rows, per essay-context.md's own
  instruction to omit them if not load-bearing for this article: 940nm wavelength, the BSI
  "stack" structure detail, dual VCSEL + BCD driver, ~150mW power draw,
  12.8x6.1x4.6mm package, ~1% (TNR) accuracy. If Phase 2 finds a compelling reason to use
  any of these, they must be hedged explicitly, not stated as bare fact — this log does
  not currently support citing them as fact.
- `st-vl53l9cx-press-release-2026` and `st-vl53l9cx-blog-2026` carry Axis 4
  (baseline-difference) load — they are the single most important external facts in this
  bundle, since the spine's baseline-difference anchor depends on the 2,268-zone /
  ~35x-jump figure. If Phase 2 or Phase 3 need a literal source URL for the `# Sources`
  block and none is available, this should be flagged rather than a URL invented.
- No tier-5 (unattributed/forum/rumor) anchors appear in this log — all six facts trace to
  ST's own first-party channels (press release, blog, data brief) or to patent-office
  records (Google Patents / patent numbers), consistent with the source-authority
  hierarchy's preference for Tier 1 (company official statement) on applicant-strategy
  claims and Tier 2 (spec sheet) on technical-mechanism claims.
- Patent-text facts about the hero patent (US2023-0356397) itself are NOT logged here —
  they live as `[xxxx]` anchors in `invention-summary.md`, per this log's own scope rule.
