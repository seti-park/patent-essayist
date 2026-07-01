---
essay_id: 001-st-histogram-mechanism
patent_reference: US 2026/0140238 A1
spine_source: handoff/01-design/thesis-spine.md
draft_version: 3
mode_used: strict-execution
posture_used: measured
---

# A Depth Sensor That Cannot Time a Single Photon With a Stopwatch

![FIG. 1: the ToF sensor system as one signal path.](figures/fig-01.png)

*FIG. 1: the ToF sensor system (100). The VCSEL (102) and VCSEL driver (104) emit the light pulse; the return SPAD array (106) and reference SPAD array (108) catch photons and feed two OR trees (110, 112) that combine per-SPAD signals into the reference and return histograms. Everything funnels into the histogram processing circuit (114), alongside the MCU (116), I/O interface (118), power management (120), and OTP memory (122) that round out the package.*

## Statistics Replaces the Stopwatch

Point a modern depth-sensing camera at a room and it renders a distance map in real time, false-colored so near is one shade and far is another. Ask how it knows those distances, and the honest first answer sounds like a contradiction. Light moves at roughly one meter every 3.3 nanoseconds. No clock on a consumer chip starts and stops fast enough to time a single photon's round trip with any precision that would matter at that distance. And yet the chip returns a number, thousands of times a second, across thousands of points in the frame at once.

The resolution to that contradiction is not a faster stopwatch. It is a decision to stop timing individual photons at all, and to count many of them instead. A patent recently published by STMicroelectronics, US 2026/0140238 A1, "Ultra-Lean Time-of-Flight Histogram Processing," describes the circuitry that makes that counting practical inside a chip small enough to fit under a fingernail `[0001]`.

## Light Is Too Fast to Time, So the Chip Counts Instead

Direct time-of-flight sensing (dToF) works by firing a laser pulse and measuring how long the reflection takes to come back. The "direct" in dToF means exactly that: a real, physical measurement of round-trip travel time, not the phase-shift trick that indirect ToF (iToF) sensors use instead. A single-photon avalanche diode, or SPAD, is the component that makes the direct measurement possible: it is sensitive enough to register one arriving photon at a time, and fast enough to timestamp when that photon arrived, via a time-to-digital converter (TDC) attached to it.

But one photon's arrival time is noise, not distance. Ambient light, sensor jitter, and stray reflections all produce their own photon arrivals, mixed in with the real signal. The fix the industry settled on, and the one this chip inherits, is statistical rather than literal: fire the laser many times, bucket every returning photon's arrival time into a bin, and build a histogram, a bar chart of how many photons arrived at each small slice of time.

A related STMicroelectronics filing, US 2023/0296739 A1, states the principle plainly: "each bin of the histogram representing a photon count corresponding to a distance from a light-ranging system." Real reflections cluster into a peak; noise spreads flat across the rest of the chart. Sweep the histogram left to right, and the peak is the signal.

That is the first half of the impossibility solved: you cannot time one photon, but you can count many and let the peak tell you where they landed. The second half is what this patent's title is actually about, and it turns out to be a harder problem than the first.

## The Claim Itself Says Bin by Bin, Not All at Once

Building the histogram is one problem. Processing it is another, and the patent's background section is candid about how the industry has typically handled it: "Conventional solutions for time-of-flight (ToF) sensor histogram processing typically involve utilizing full histogram processing with a powerful off-chip microcontroller unit (MCU)" `[0054]`. The word "full" is the tell. A histogram with a few hundred bins, each holding a photon count, has to be held in memory in its entirety before a general-purpose processor can hunt through it for crosstalk, segment out the real pulse, and estimate its phase.

"On-chip processing presents several drawbacks, such as necessitating a large MCU in the sensor package, which consumes significant power and increases read-out complexity" `[0055]`. Do that at frame rate, for thousands of zones, and the memory and the processor both become the bottleneck a compact, battery-powered device cannot afford.

Claim 1 of the patent describes a circuit that never holds that full copy. It calls for "a histogram processing circuit coupled to the detector array and configured to: receive time-of-flight measurement data from the detector array, process measurement data from the detector array using a sequential bin-by-bin histogram processing, and apply, during the sequential bin-by-bin histogram processing, one or more on-the-fly operations."

The patent's abstract states the same idea in one line: the system "processes time-of-flight measurement data using sequential bin-by-bin histogram processing." Bin by bin is the load-bearing phrase, repeated at claim level and abstract level because the entire architecture hangs on it.

**The histogram is never fully assembled in memory. It is consumed one bin at a time, the instant each bin arrives, and then discarded.**

Inside the circuit, that is a literal pipeline rather than a metaphor: "Rather than processing the full reference/return histogram input as an entire array in memory, the histogram processing circuit 200 is advantageously configured to iterate the histogram by serially computing relevant outputs in a single pass" `[0069]`.

"The histogram data is processed one bin at a time using the bin-serial processing method" `[0080]`. "The approach creates a state machine that maintains minimal internal buffers, significantly reducing memory requirements compared to traditional approaches that process entire histograms simultaneously" `[0080]`. A state machine with a handful of registers has replaced a memory bank sized to hold the whole chart.

## Every Zone Gets Its Own Bar Chart, Read as It Streams

Here is where the mechanism becomes intuitive rather than architectural. Picture the depth sensor's field of view as a grid, and give every cell in that grid, every zone, its own histogram, its own bar chart of "when did photons come back from this direction." A sensor with thousands of zones is running thousands of these bar charts, in effect, every frame.

The naive way to find each zone's distance is to build the whole bar chart first, then look across it afterward for the tallest bar. That is the "full histogram processing" the patent's background section describes, and it is exactly the approach this circuit avoids `[0054]`.

The bin-serial approach instead reads each bar the instant it arrives and updates a running answer, never waiting to see the whole chart.

FIG. 2 shows what that looks like as hardware. The reference and return histograms, plus a separately generated crosstalk histogram, feed into a correlator circuit (202) and a phase/bin computation circuit (204) that both process bin-by-bin. A range calculation circuit (206) and rate calculation circuit (208) then turn the running answer into an actual distance and signal strength. Nowhere in that path does a block wait for a complete histogram to sit in memory before it can start working.

*FIG. 2: the histogram processing circuit, exploded. Reference/return histogram, crosstalk histogram, and window-start/end signals flow into the correlator (202) and phase/bin computation (204) circuits; range calculation (206) and rate calculation (208) turn the running bin-by-bin answer into median range and per-SPAD rate.*

The payoff of that design shows up as a memory number small enough to be almost comic next to the alternative. The patent quantifies it for one specific piece of housekeeping, crosstalk calibration data: "Conventional approaches typically require storing 128 or 144 bins of 16-bit data, resulting in a memory footprint of approximately 256 bytes. However, the proposed implementation reduces the required storage to, for example, 19 bytes" `[0101]`.

Elsewhere the patent calls that "a significant optimization for the memory-constrained system" `[0103]`, and the arithmetic backs the claim: roughly a thirteenfold reduction, on this one sub-problem alone, from what a conventional full-histogram approach would need to keep in memory.

The chip's own microcontroller is demoted accordingly. Instead of running that math itself, "the system's microcontroller unit (MCU) functions primarily as a sequencer, with limited local storage in the form of registers" `[0043]`. The actual number-crunching goes to dedicated bin-serial hardware, with just enough local memory left to keep that hardware fed.

## ST Will Not Say Which Patent Built the VL53L9CX, but the Dates Line Up

None of this is abstract engineering for its own sake. In June 2026, STMicroelectronics announced the VL53L9CX, a direct-ToF 3D LiDAR module the company describes as the "first direct Time-of-Flight (dToF) 3D LiDAR all-in-one module in ST's portfolio." Its headline number is 2,268 zones, arranged in a 54-by-42 grid, running at up to 100 frames per second with on-chip processing (ST's own technical specifications).

The company's prior multi-zone dToF generation, the VL53L5CX and VL53L8CX family, topped out at 64 zones, an 8-by-8 grid. That is roughly a thirty-five-fold jump in zone count in one product generation, not a precise figure ST states outright but a straightforward ratio from the two generations' own published zone counts.

STMicroelectronics does not publish which patent maps to which line of silicon, and this patent never names the VL53L9CX. That has to be conceded plainly rather than argued around: there is no public document that ties this specific filing to that specific chip's production mask. What can be said is narrower and still worth saying.

Running 2,268 independent bin-by-bin histograms at 100 frames per second, entirely on-chip, inside a sensor package rather than on a host processor, is only power- and silicon-feasible if the per-zone histogram processing is this lean. A memory bank sized for full-histogram processing, multiplied by 2,268 zones, does not fit the power and area budget of a module this size. This patent was filed November 19, 2024; the VL53L9CX was announced roughly nineteen months later, in June 2026. The timing is consistent with this architecture underpinning that generation. It is not proof that it does.

**The engineering claim survives without the product claim: this is the kind of bin-serial, memory-lean processing that a chip like the VL53L9CX needs in order to exist at that zone count, whether or not this exact filing is the one running inside it.**

The peak of a photon-count histogram was never a stopwatch reading. It was always a vote, thousands of light pulses agreeing on when the reflection came back. This patent answers how to count that vote without ever writing down the whole tally. 🤔

# Sources

## Patents

- US 2026/0140238 A1, "Ultra-Lean Time-of-Flight Histogram Processing," STMicroelectronics International N.V., priority 2024-11-19, published 2026, inventors: Donald Baxter, Pascal Mellot, Stuart McLeod, Andreas Assmann.
- US 2023/0296739 A1, "Methods and devices for identifying peaks in histograms," STMicroelectronics International N.V., priority 2022-03-17, inventor: Andreas Aßmann.

## Official statements

- STMicroelectronics newsroom, VL53L9CX product announcement (2026-06-22). https://newsroom.st.com/media-center/press-item.html/p4783.html

## Technical specs

- STMicroelectronics, VL53L9CX data brief. https://www.st.com/en/imaging-and-photonics-solutions/vl53l9cx.html
- STMicroelectronics, VL53L5CX datasheet. https://www.st.com/resource/en/datasheet/vl53l5cx.pdf
- STMicroelectronics, VL53L8CX product page. https://www.st.com/en/imaging-and-photonics-solutions/vl53l8cx.html
