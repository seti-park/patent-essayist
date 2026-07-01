# Search Log

## Note on methodology for this run

This run did not perform new live web search. Per this run's process instructions,
external-fact context research for this essay was already completed prior to this Phase 1
run and delivered pre-verified in `input/essay-context.md` ("External facts available for
this run," verified against ST first-party sources, dated 2026-06-30). This log records
those findings in the standard search-log schema — attributing each to the source given in
essay-context.md — rather than re-performing the web search. No new external fact beyond
what essay-context.md marks "Verified" is asserted anywhere in this Phase 1 bundle;
"Pending confirmation" items are treated as not safe to cite as bare fact, per
essay-context.md's own instruction, and are omitted from fact-check-log.md's load-bearing
rows.

## Queries (inherited findings, not re-run this session)

| # | Query | Result URL | Date | Result snippet | Used in | Framing |
|---|---|---|---|---|---|---|
| 1 | STMicroelectronics VL53L9CX press release mass production | ST press release (2026-06-22 announcement; exact URL not re-fetched this session — see Notes) | 2026-06-30 (verified by prior research; inherited, not re-run) | "VL53L9 is the first direct Time-of-Flight (dToF) 3D LiDAR all-in-one module in ST's portfolio." Applications: "small object detection, SLAM, obstacle avoidance for autonomous navigation" plus robotics/drones/humanoids. | fact-check-log: st-vl53l9cx-press-release-2026 → thesis-spine Axis 4 (baseline-difference), product tie-in | main-thread |
| 2 | STMicroelectronics VL53L9CX blog 2.3K zones flood illumination | ST blog (referenced in essay-context.md; exact URL not re-fetched this session — see Notes) | 2026-06-30 (verified by prior research; inherited, not re-run) | "1st 3D ToF LiDAR with 2.3K zones and flood illumination." Resolution 2,268 zones (54x42), prior generation (VL53L5/L8CX) topped out at 64 zones or fewer. | fact-check-log: st-vl53l9cx-blog-2026 → thesis-spine Axis 4 (baseline-difference, ~35x zone-count jump) | main-thread |
| 3 | VL53L9CX data brief FoV range detection specs | ST data brief (referenced in essay-context.md; exact URL not re-fetched this session — see Notes) | 2026-06-30 (verified by prior research; inherited, not re-run) | 54x42 deg FoV, 71 deg diagonal FoV at 1 deg angular resolution, 5cm-9m range, up to 100fps; BSI-stack SPAD array, dual-scan flood illumination; on-chip histogram processing + cover-glass crosstalk/veiling-glare correction, calibration-free; outputs depth/2D IR/reflectance/confidence; first ToF sensor with MIPI and I3C (plus I2C). | fact-check-log: st-vl53l9cx-datasheet-specs-2026 → invention-summary product-tie-in context (not a patent-text claim) | paragraph |
| 4 | secondary patent US2022-0184815 mobile robot movement path | Google Patents (patent number given in essay-context.md; not independently re-fetched this session) | 2026-06-30 (verified by prior research; inherited, not re-run) | "analyzing the image information to determine whether to modify the movement path of the mobile robot" — Hanratty & Raynor, STMicroelectronics R&D, filed 2020-12-15, CPC G05D1 / B25J. | fact-check-log: secondary-patent-us2022-0184815 → thesis-spine "widen the bridge" beat | paragraph |
| 5 | horizon-cluster patent numbers (anti-collision, histogram scene-change, depth+IMU fusion, multi-IMU robotics, egomotion) | corpus-index metadata (patent numbers given in essay-context.md; not independently re-fetched this session) | 2026-06-30 (verified by prior research; inherited, not re-run) | US2021-0268903 (anti-collision), US2026-0087695 (histogram scene-change), US2022-0067346 (depth+inertial fusion), US2024-0191996 (multi-IMU robotics fusion), US2022-0080979 (egomotion) — cited only as a SLAM-horizon gesture, never expanded into a case study. | phase2-handoff-notes §(d) traps — horizon cluster gets a clause each, never a hero-equivalent treatment | footnote |
| 6 | IMU/GNSS-only navigation patent caution (US2019-0033466) | corpus-index metadata (patent number given in essay-context.md; not independently re-fetched this session) | 2026-06-30 (verified by prior research; inherited, not re-run) | Flagged explicitly in essay-context.md as NOT a depth-bridge patent — must not be treated like the hero or secondary patent if it appears in the horizon paragraph. | phase2-handoff-notes §(d) traps | footnote |

## Framing-impact classification (Step 1d, applied to the inherited findings above)

- **Main thread** (#1, #2): the VL53L9CX product identity, its "first ... in ST's
  portfolio" qualified-first claim, and the ~35x zone-count jump over the prior
  VL53L5/L8CX generation are the load-bearing external anchors for Axis 4
  (baseline-difference) and for the product tie-in that makes the essay's closing land
  on a real, dated (2026-07) product rather than an abstract capability.
- **Paragraph** (#3, #4): the data-brief specs support the mechanism-color paragraphs but
  are not claim-critical to the thesis; the secondary patent grounds one generalization
  sentence/short passage, not a full section.
- **Footnote** (#5, #6): the horizon cluster and the IMU/GNSS-only caution are single-line
  or single-clause citations only — essay-context.md is explicit that the horizon cluster
  must never be expanded into a hero-equivalent case, and that US2019-0033466 is not a
  depth-bridge patent at all.

## Notes

- No live WebSearch/WebFetch calls were attempted or needed for this run: per this run's
  process instructions, `essay-context.md` already supplies pre-verified external facts
  with explicit verified-vs-pending-confirmation labeling, dated 2026-06-30 (the day before
  this run). Re-verifying live web sources was explicitly out of scope for this Phase 1
  pass; this log's job is to preserve traceability to that prior verification, not to
  duplicate it.
- Exact source URLs for queries 1-6 are not restated here beyond what essay-context.md
  itself provides (essay-context.md attributes them narratively — "ST press release,"
  "Blog," "data brief," "corpus-index metadata" — rather than as bare URLs). If Phase 2/3
  need a literal URL for the `# Sources` block, that is a fact-check-log.md /
  editorial-review Pass-3 concern; this run does not fabricate a URL that essay-context.md
  did not supply.
- "Pending confirmation" items from essay-context.md (940nm wavelength, BSI "stack"
  structure detail, dual VCSEL + BCD driver, ~150mW power draw, 12.8x6.1x4.6mm package,
  ~1% (TNR) accuracy) are deliberately NOT logged as findings here and are NOT used
  anywhere in this Phase 1 bundle as asserted fact, per essay-context.md's own instruction
  to omit them since they are not load-bearing for this bridge/action article.
- No query in this inherited set forced a re-extraction of `invention-summary.md` Layer 4
  angles — the inherited findings support Axis 4 and the product tie-in cleanly without
  contradicting anything drawn directly from `input/patent.md`.
