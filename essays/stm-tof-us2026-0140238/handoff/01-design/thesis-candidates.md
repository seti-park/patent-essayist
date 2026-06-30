# Thesis Candidates

Single-spine default. Three candidates generated from invention-summary Layer 4 angles; one
selected (the Mechanism spine fixed by the brief), two rejected with rationale. The brief locks
the angle to **Mechanism** (Part 1 of the series), so candidate selection is constrained — the
alternatives are recorded for trace and to show why the spine is framed the way it is.

## C1 — "Peak = distance, streamed bin by bin, lean enough to run on-chip" (SELECTED)

- **Frame**: The VL53L9CX recovers distance from photon statistics — a per-zone histogram streamed
  one bin at a time, peak = distance — and the hero patent is what makes that processing lean
  enough to run on a fingernail-sized, battery-friendly module.
- **Layer 4 source**: angle-bin-serial-streaming (+ angle-memory-collapse, angle-peak-equals-distance).
- **4-axis**: all four anchored (claims = claim 1 / `[0015]` + VERBATIM ANCHOR; problem =
  `[0004]`/`[0013]`; effect = `[0042]`/`[0069]`; baseline = conventional off-chip/large-MCU dToF
  `[0054]`-`[0056]` + support single-pass principle). Complete.
- **Q7**: `technical-impossibility` — the reader's "you can't start a stopwatch on a few photons"
  intuition is the entry; the patent resolves it (histogram + streaming). Derivable from the patent,
  no external-event research needed.
- **Why selected**: it is the Mechanism the brief requires, it puts the patent in the protagonist
  seat, it lets the claim carry the verbatim moment, and it defines the callback vocabulary
  (histogram, zone/multizone, peak=distance) the later parts reuse.

## C2 — "Full-histogram quality with almost no memory" (REJECTED → folded into Layer 4)

- **Frame**: memory-first entry — conventional ToF needs substantial RAM holding multiple copies of
  the histogram, which is prohibitive on a tiny battery device; the invention keeps the quality and
  drops the memory.
- **Layer 4 source**: angle-memory-collapse.
- **4-axis**: anchored, but Axis 2 (problem) and Axis 4 (baseline) overlap C1 heavily.
- **Q7**: could map to `technical-impossibility` ("how do you do full histogram processing without
  the memory") but it is an engineering-constraint hook, less vivid for a general-reader Mechanism
  piece than C1's "few photons / too fast to time" entry.
- **Rejection reason**: it is the *effect* of C1's mechanism, not a separate spine. Folded into
  Layer 4 (product connection) as the "why it fits on a chip" payoff, and into Axis 3. Not used as
  the spine because the brief wants the reader to start from light-and-photons, not from RAM budgets.

## C3 — "The same engineer, two patents: principle then on-chip" (REJECTED)

- **Frame**: a storytelling thread — Andreas Assmann filed the 2022 single-pass peak-finding
  principle (support patent), then co-invented the 2024 ultra-lean on-chip implementation (hero);
  the arc is principle → product.
- **Layer 4 source**: none directly (a metadata/inventor observation, not a technical novelty axis).
- **Rejection reason**: it is a biographical thread, not the Mechanism. It risks pulling the
  protagonist seat away from the patent's content and toward a personality story, and it is not the
  series' Part-1 job (how it works). Demoted to an **optional single-sentence thread** inside the
  mechanism layer (the 2022 principle, then the 2024 on-chip implementation), per the brief — at
  most one sentence, only if it earns its place, never the spine.
