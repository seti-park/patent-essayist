# Fact-Check Log

## External facts

| Fact ID | Claim | Source URL | Tier | Sources category |
|---|---|---|---|---|
| st-onchip-crosstalk-veiling-glare-2026 | ST's own public product page states that on-chip histogram processing and algorithmic compensation on VL53L9CX mitigate/remove performance degradation from veiling glare and cover-glass crosstalk. | https://www.st.com/en/imaging-and-photonics-solutions/vl53l9cx.html | tier-1 | Official statements |
| st-vl53l9-first-in-portfolio-2026 | ST's own press release states "VL53L9 is the first direct Time-of-Flight (dToF) 3D LiDAR all-in-one module in ST's portfolio" — a qualified claim ("in ST's portfolio"), not an unqualified industry-first claim. | https://newsroom.st.com/media-center/press-item.html/p4783.html (corroborated by https://blog.st.com/vl53l9/) | tier-1 | Official statements |
| vl53l9cx-940nm-2vcsel-bsi-spec | VL53L9CX uses two VCSEL emitters at 940nm (invisible/IR) light, and a SPAD array built on ST's stacked Backside-Illuminated (BSI) process. | https://www.st.com/en/imaging-and-photonics-solutions/vl53l9cx.html ; corroborated by https://www.edn.com/lidar-module-generates-high-resolution-depth-maps/ | tier-2 | Technical specs |
| vl53l9cx-150mw-package-size-2026 | VL53L9CX typical system power is ~150mW; package dimensions are 12.8 x 6.1 x 4.6mm. | https://www.st.com/resource/en/data_brief/vl53l9cx.pdf (surfaced via search snippet; direct PDF fetch unavailable this session) | tier-2 | Technical specs |
| vl53l9cx-calibration-free-2026 | ST describes the VL53L9CX module as "fully calibration-free," with on-chip dToF processing and a dedicated PMIC, simplifying integration. | https://blog.st.com/vl53l9/ (corroborated by press release, same p4783 URL as above) | tier-1 | Official statements |
| industry-cover-glass-crosstalk-baseline-2026 | Cover-glass cross-talk (reflection of the outgoing laser pulse back into the sensor near zero distance) is an established, named, recurring problem across the ToF sensor industry — not unique to this one patent or a single competitor — evidenced by ST's own multi-generation cover-glass application notes (VL53L5CX, VL53L8, etc.) and community-reported "ghost detections" on other ST ToF parts. | https://community.st.com/t5/imaging-sensors/ghost-detections-in-vl53l7cx-tof-sensor-zones-after-crosstalk/td-p/864017 ; https://www.st.com/resource/en/application_note/an5856-guidelines-for-the-cover-glass-of-the-vl53l5cx-timeofflight-8x8-multizone-sensor-with-wide-field-of-view-stmicroelectronics.pdf | tier-2 | Technical specs |

## Notes

- **Unverifiable / deliberately NOT entered as a settled fact**: the ~1% (TNR) ranging-accuracy
  figure that `essay-context.md` explicitly flagged as needing independent cross-check could
  not be corroborated through available web-search access this session (see search-log.md query
  7 — no authoritative source surfaced any specific accuracy percentage for VL53L9CX). Per
  essay-context.md's own instruction to "hedge or omit if unverifiable," this number is
  **not** promoted to a Fact ID here and Phase 2 is instructed (phase2-handoff-notes.md) to
  omit it from the essay rather than assert it.
- **Access caveat**: direct `WebFetch` of ST's own press-release page, the VL53L9CX datasheet
  PDF, the GlobeNewswire syndication of the press release, and one third-party trade-press
  mirror (CNX Software) all failed in this session (HTTP 473 / 503 / 403). The tier-1 and
  tier-2 facts above rest on WebSearch's own result snippets, which quote what appear to be
  verbatim fragments from those same official pages/press release, corroborated across at
  least two independently-surfaced sources per fact (ST's own product page + press release +
  blog, cross-checked against independent trade press reporting the same figures verbatim).
  This is treated as reasonably reliable for framing and product-fact hedging purposes, but
  Phase 2/3 should not treat any single number here as having been read directly off the
  primary-source PDF — if a stronger guarantee is later needed (e.g. before quoting the 150mW
  or 940nm figures as settled), a direct fetch of `https://www.st.com/resource/en/datasheet/vl53l9cx.pdf`
  or `.../data_brief/vl53l9cx.pdf` should be retried outside this session's fetch restrictions.
- `st-vl53l9-first-in-portfolio-2026` directly satisfies essay-context.md's hard requirement:
  reserve "first" language only for this qualified, product-level phrasing ("in ST's
  portfolio"), never for this individual patent's cross-talk-rejection technique itself.
- The supporting-patent anchor (US 2025-0012901, "automatically adjusts the amount of
  cross-talk signal to be removed based on the current condition of the cover glass (e.g.,
  scratch, smudge, dirt)") is NOT a web-research fact — it was pre-verified by the essay's
  author directly against that patent's source text (per essay-context.md) and is therefore a
  patent-anchored quote, not an external fact requiring a Fact ID here. It is tracked instead
  as a patent-text anchor for the supporting patent in thesis-spine.md / phase2-handoff-notes.md.
- The five cluster patents named in essay-context.md (US 2022-0187431, US 2026-0036684,
  US 2025-0008232, US 2022-0308173, US 2024-0426985) have no source text available this run and
  are not investigated here — essay-context.md is explicit that they get one-line mention only,
  no quotes, no mechanism claims.
