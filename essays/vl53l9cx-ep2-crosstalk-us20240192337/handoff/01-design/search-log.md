# Search Log

## Queries

| # | Query | Result URL | Date | Result snippet | Used in | Framing |
|---|---|---|---|---|---|---|
| 1 | STMicroelectronics VL53L9CX dToF LiDAR cross-talk veiling glare compensation | https://www.st.com/en/imaging-and-photonics-solutions/vl53l9cx.html | 2026-07-01 | "The VL53L9CX incorporates dedicated post-processing that automatically mitigates or removes the performance degradation caused by veiling glare and cover-glass crosstalk... on-chip histogram processing and algorithmic compensation minimizes impact of cover glass crosstalk and veiling glare." | fact-check-log: st-onchip-crosstalk-veiling-glare-2026 → thesis-spine Axis 4 + product-connection beat | main-thread |
| 2 | VL53L9CX "first" direct Time-of-Flight 3D LiDAR module ST portfolio | https://newsroom.st.com/media-center/press-item.html/p4783.html | 2026-07-01 | "VL53L9 is the first direct Time-of-Flight (dToF) 3D LiDAR all-in-one module in ST's portfolio." | fact-check-log: st-vl53l9-first-in-portfolio-2026 → Q7 hook / hard-requirement (qualified "first" only) | main-thread |
| 3 | VL53L9CX 940nm VCSEL wavelength BSI SPAD stack | https://www.st.com/en/imaging-and-photonics-solutions/vl53l9cx.html ; https://www.edn.com/lidar-module-generates-high-resolution-depth-maps/ | 2026-07-01 | "The VL53L9CX uses two vertical-cavity surface-emitting lasers (VCSEL) with 940 nm invisible light... single-photon avalanche diode (SPAD) array built on ST's proprietary stacked Backside-Illuminated (BSI) semiconductor technology." | fact-check-log: vl53l9cx-940nm-2vcsel-bsi-spec → product-facts hedge resolution | paragraph |
| 4 | VL53L9CX power consumption mW package size mm accuracy | https://www.st.com/resource/en/data_brief/vl53l9cx.pdf (via search snippet; direct PDF fetch blocked — see Notes) | 2026-07-01 | "The VL53L9CX consumes only 150 mW of typical system power... package that measures 12.8 mm x 6.1 mm x 4.6 mm... accurate ranging from below 5 cm up to 8.8 m." | fact-check-log: vl53l9cx-150mw-package-size-2026 → product-facts hedge resolution | paragraph |
| 5 | "VL53L9" ST press release "first" "portfolio" LiDAR | https://newsroom.st.com/media-center/press-item.html/p4783.html ; https://blog.st.com/vl53l9/ | 2026-07-01 | "VL53L9 is the first direct Time-of-Flight (dToF) 3D LiDAR all-in-one module in ST's portfolio, offering a resolution of 2.3K zones... The VL53L9 measures just 12.8 mm x 6.1 mm x 4.6 mm... fully calibration-free." | fact-check-log: st-vl53l9-first-in-portfolio-2026 (corroborating second source) + vl53l9cx-calibration-free-2026 | main-thread |
| 6 | ToF sensor cover glass crosstalk problem ghost target industry | https://community.st.com/t5/imaging-sensors/ghost-detections-in-vl53l7cx-tof-sensor-zones-after-crosstalk/td-p/864017 ; https://www.st.com/resource/en/application_note/an5856-guidelines-for-the-cover-glass-of-the-vl53l5cx-timeofflight-8x8-multizone-sensor-with-wide-field-of-view-stmicroelectronics.pdf | 2026-07-01 | "Crosstalk is the interference caused by the ranging laser light that is reflected by a cover glass and not the intended target... The crosstalk optical path is short, so the crosstalk pulse appears close to zero distance/delay... A cover glass with poor quality design or manufacture increases the crosstalk level, and smudge or haze on the top of the cover glass degrade the target vs crosstalk signal ratio." | fact-check-log: industry-cover-glass-crosstalk-baseline-2026 → thesis-spine Axis 4 (industry-wide, not single-competitor, baseline) | main-thread |
| 7 | VL53L9CX ranging accuracy "1%" OR "TNR" distance accuracy percent | (no authoritative hit) | 2026-07-01 | Search did not return a specific ~1% (TNR) accuracy figure for VL53L9CX from any source; only generic "accurate distance measurements" language surfaced, no percentage. | discarded — figure remains unverified; NOT entered as a fact-check-log row per essay-context.md's caution against presenting unverified numbers as settled | n/a |

## Notes

- Queries 1, 2, 3, 4, 5, 6 returned search-engine result snippets (via the available WebSearch
  tool) rather than full page fetches — direct `WebFetch` attempts against
  `newsroom.st.com/media-center/press-item.html/p4783.html`, `www.st.com/resource/en/datasheet/vl53l9cx.pdf`,
  `globenewswire.com` (the syndicated press release), and `cnx-software.com` all failed in this
  environment (HTTP 473 / 503 / 403 respectively) — the fetch tool itself appears blocked or
  rate-limited for these domains in this session, not a content-availability problem. The
  WebSearch tool's own result snippets are treated as the load-bearing evidence for queries 1-6;
  they are attributed to ST's own official pages/press release and to independent trade-press
  coverage (EDN, press aggregators), which corroborate each other and are logged at tier-1
  (ST's own product page / press release wording, as surfaced by search) and tier-3
  (independent trade press repeating the same figures) respectively — see fact-check-log.md for
  per-fact tiering.
- The "first ... in ST's portfolio" qualified claim (query 2, 5) independently confirms
  essay-context.md's pre-supplied wording is current and accurate as of this run — no drift
  found. This directly satisfies essay-context.md's hard requirement to reserve "first"
  language only for this qualified product-level phrasing, never for the individual patent's
  technique.
- Query 7 is a genuine dead end: the ~1% (TNR) accuracy figure that essay-context.md flagged
  as needing independent cross-check could NOT be corroborated through available web access.
  Per essay-context.md's own instruction ("prefer to hedge or omit if unverifiable"), this
  figure is NOT promoted to a settled fact-check-log entry and Phase 2 is instructed
  (phase2-handoff-notes.md) to omit it rather than quote it as a hard number.
- No query forced a Layer 4 re-extraction of invention-summary.md — the patent-anchored angles
  were fully derivable from `input/patent.md` alone; context research served Axis 4
  (baseline-difference) and the product-connection beat, not the core mechanism extraction.
- No timing-anomaly or visual-contradiction candidate emerged from this research (consistent
  with the v2 Q7 gate dropping those patterns) — the corporate-narrative-friction candidate
  that did emerge is addressed in thesis-candidates.md.
