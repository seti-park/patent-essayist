# Figure selection

Four figures carry the spine. The full filing has eight figure sheets in total (including a
multi-panel kneel sequence and two system block diagrams); the rest are supporting detail not
needed for a moat read.

| Figure | Thesis point (section) | caption_role | Anchor |
|---|---|---|---|
| **FIG. 1** | §2 the body that creates the problem (tall, balancing, falls on a power cut) | establishing | — |
| **FIG. 3** | §3 the claimed escalation logic (decelerate → clearance gate → reconfigure → safe stop, with hold states) | mechanism | `[0033]` |
| **FIG. 5** | cover strip + §4 the motion of the center-of-gravity-lowering step (curated frames 5A, 5K, 5T, 5AD) | sequence (one embodiment) | `[0047]` |
| **FIG. 6** | §4 the end state: compact kneel, center-of-gravity dropped, predictable collapse | payoff | `[0047]` |

Selected figure set: **1, 3, 5, 6**. All four are referenced in the draft; no other figure
numbers are referenced, keeping the figure-use gate clean. FIG. 5 token note: lettered panels
(`FIG. 5A`) do not parse in the figure-use/figref regex (the trailing letter kills the word
boundary), so the draft carries at least one bare `FIG. 5` token (cover alt text + the §4 inline
reference) to register the figure as used; the human-readable `FIG. 5A-5AD` caption is additive.
The cover strip is a curated 4-frame crop (start → fold → deep fold → kneel) composed from the
patent's own panels; the full sequence composites (fig-05AF / GO / PX / YAD) ship in figures/.
