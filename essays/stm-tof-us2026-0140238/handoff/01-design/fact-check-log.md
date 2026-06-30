# Fact-check log

External (non-patent) facts the spine relies on, plus an explicit NON-assertable list. Patent-
internal claims use `[xxxx]` anchors (recorded in invention-summary.md) and are not listed here.
Each external fact is scoped to its source's literal claim; no universalization. Verified against
ST primary sources on 2026-06-30 (per the brief).

## Facts you MAY state (verified, ST primary sources)

| Fact ID | Claim (as scoped) | Tier | Source | Used in | Status |
|---|---|---|---|---|---|
| F1 | 2,268 zones (54x42), marketed as "2.3K zones"; about a 35x jump over the prior <=64-zone generation (VL53L5/L8CX) | 1 | ST newsroom press release (VL53L9, p4783); ST blog (blog.st.com/vl53l9) | Layer 4 | verified |
| F2 | 54x42 degree field of view; range 5 cm to 9 m; up to 100 fps | 1 | ST newsroom / ST databrief DB5805 (Rev 2) — FoV/range/fps framing only | Layer 4 | verified |
| F3 | On-chip processing (histogram processing plus correction on the module's own SoC); flood illumination; an all-in-one module | 1 | ST newsroom press release; ST blog | Layer 4 | verified |
| F4 | Production from early July 2026 (announced 2026-06-22) | 1 | ST newsroom press release | Layer 4 / Layer 5 seam | verified |
| F5 | Robotics uses ST names: small-object detection, SLAM, obstacle avoidance for autonomous navigation | 1 | ST newsroom press release; ST blog | Layer 4 (quote ST, do not inflate) | verified (attribute to ST) |

Low-power claim: use the **patent's own qualitative language** (minimal memory, low gate/logic
count, battery-powered devices — `[0013]`, `[0042]`). Do NOT pin a milliwatt number.

## "First" qualifier (handle with care)

- ST calls VL53L9 the **"first direct Time-of-Flight (dToF) 3D LiDAR all-in-one module in ST's
  portfolio."** Use only this qualified wording.
- It is **NOT the absolute first dToF** — multizone dToF already existed (VL53L5 / VL53L8). The
  real leap is **resolution + flood illumination**, not "first ever dToF." Do not drop the
  "in ST's portfolio" qualifier.

## Facts you may NOT assert (datasheet-only, cross-check pending — do NOT state)

These are datasheet-only figures that could not be cross-checked (ST www.st.com bot-blocked at
research time). Do NOT state any of them as fact in this article:

- **940 nm** wavelength — DO NOT ASSERT. (If the light source must be described, "a small infrared
  laser" is safe; do not give a wavelength.)
- **BSI "stacked"** SPAD structure — DO NOT ASSERT.
- **dual-VCSEL + BCD driver** detail — DO NOT ASSERT.
- **~150 mW** power figure — DO NOT ASSERT. Keep power qualitative.
- package size **12.8 x 6.1 x 4.6 mm** — DO NOT ASSERT. ("fingernail-sized" / "compact" is the safe
  framing.)
- **~1% (TNR)** accuracy figure — DO NOT ASSERT.

## Patent-internal pinned numbers (attribute, do not generalize)

These ARE in the hero patent but are illustrative "e.g." embodiment values, not claim limits or
product specs. If used, attribute to the paragraph and frame as example, not guarantee (see
invention-summary.md §claim-scope / §유리한 효과):

- crosstalk description "19 bytes" vs conventional "256 bytes" (`[0101]`, `[0103]`)
- "five-element" recent-bins buffer (`[0113]`)
- range modes 2.4 m / 4.8 m / 9.6 m (`[0107]`)

Notes:
- All product/market facts (F1-F5) are "outside the filing"; attach inline `[dddd]` anchors only to
  hero-patent facts, and name ST as the source for F1-F5 in prose.
- The ~35x leap (F1) is an ST framing of resolution vs the prior generation; present it as ST's
  comparison, tied to "resolution + flood illumination", not as the sensor being "first dToF".
