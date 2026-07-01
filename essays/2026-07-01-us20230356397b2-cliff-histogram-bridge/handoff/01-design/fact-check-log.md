# Fact-Check Log

## External facts

| Fact ID | Claim | Source URL | Tier | Sources category |
|---|---|---|---|---|
| st-vl53l9cx-press-release-2026 | STMicroelectronics announced the VL53L9CX, a direct Time-of-Flight (dToF) 3D LiDAR all-in-one module (evaluation board STEVAL-VL53L9), with mass production announced for early July 2026 (announcement dated 2026-06-22). ST's own verbatim claim: "VL53L9 is the first direct Time-of-Flight (dToF) 3D LiDAR all-in-one module in ST's portfolio" (a qualified first, within ST's own portfolio — multi-zone dToF already existed via VL53L5/L8). | <URL not independently re-fetched this run — attributed narratively in essay-context.md as "ST press release"; see search-log.md query 1 and Notes below> | tier-1 | Official statements |
| st-vl53l9cx-blog-2026 | ST blog verbatim: "1st 3D ToF LiDAR with 2.3K zones and flood illumination." Resolution: 2,268 zones (54x42) — described as the industry's highest multi-zone resolution; the prior generation VL53L5/L8CX topped out at 64 zones or fewer (roughly a 35x jump). | <URL not independently re-fetched this run — attributed narratively in essay-context.md as "Blog"; see search-log.md query 2 and Notes below> | tier-1 | Official statements |
| st-vl53l9cx-datasheet-specs-2026 | FoV/range: 54x42 deg FoV (2,268 zones), 71 deg diagonal FoV at 1 deg angular resolution, 5cm-9m range, up to 100fps. Detection: BSI-stack SPAD array; dual-scan flood illumination (vs. dot-scan) removes dead zones and improves small-object/edge detection and motion artifacts. Optics/processing: on-chip SoC does histogram processing plus algorithmic correction to remove cover-glass crosstalk and veiling glare; calibration-free. Outputs: depth (3D) / 2D IR (active and passive) / reflectance / confidence — AI-ready for MCU edge AI. First ToF sensor with MIPI and I3C interfaces (plus I2C). Applications (ST press release, verbatim): "small object detection, SLAM, obstacle avoidance for autonomous navigation" plus home/building/city automation, smart glasses (AR), industrial, robotics/drones/humanoids, edge AI. | <URL not independently re-fetched this run — attributed narratively in essay-context.md as "data brief"; see search-log.md query 3 and Notes below> | tier-2 | Technical specs |
| secondary-patent-us2022-0184815 | US2022-0184815, "Controlling movement of a mobile robot" — filed 2020-12-15, inventors James M. Hanratty and Jeffrey M. Raynor, assignee STMicroelectronics R&D, CPC G05D1 (robot position control), B25J. Anchor: "analyzing the image information to determine whether to modify the movement path of the mobile robot." Used only to generalize the hero's specific cliff case to general navigation, in a sentence or short passage — not as a second case study. | https://patents.google.com/ (patent number US2022-0184815; specific record URL not independently re-fetched this run — see search-log.md query 4) | tier-1 | Patents |
| horizon-cluster-patents-2026 | Horizon-cluster patent numbers, cited only as a line/clause each, never expanded: US2021-0268903 (anti-collision), US2026-0087695 (histogram scene-change), US2022-0067346 (depth + inertial fusion), US2024-0191996 (multi-IMU robotics fusion), US2022-0080979 (egomotion). | https://patents.google.com/ (patent numbers as listed; specific record URLs not independently re-fetched this run — see search-log.md query 5) | tier-1 | Patents |
| imu-gnss-caution-us2019-0033466 | US2019-0033466 is explicitly flagged as an IMU/GNSS-only navigation patent, NOT a depth-bridge patent — must not be treated like the hero or secondary patent even if it appears in the horizon paragraph as context. | https://patents.google.com/ (patent number US2019-0033466; specific record URL not independently re-fetched this run — see search-log.md query 6) | tier-1 | Patents |

## Notes

- All six rows above are **inherited** from `input/essay-context.md`'s "External facts
  available for this run" section (dated 2026-06-30, verified against ST first-party
  sources), not independently re-verified by this Phase 1 run — see `search-log.md` for
  the full inheritance note. This run did not fabricate or re-derive any external fact
  beyond what essay-context.md marked "Verified — safe to cite as fact."
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
