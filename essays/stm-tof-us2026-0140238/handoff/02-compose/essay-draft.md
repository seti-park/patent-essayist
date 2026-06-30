---
essay_id: stm-tof-us2026-0140238
patent_reference: US 2026/0140238 A1
spine_source: handoff/01-design/thesis-spine.md
draft_version: 1
mode_used: walkthrough
posture_used: measured
---

# How a Sensor Turns Light Into Distance, One Photon Bin at a Time

## Light Is Too Fast to Time, So the Sensor Counts Photons Instead

Point a flashlight at a wall three metres away and ask how long the light takes to come back. The honest answer is about twenty billionths of a second. Light crosses one metre in roughly 3.3 nanoseconds, and the round trip doubles that. You cannot start a stopwatch on something that quick by hand, and a sensor cannot really start one either.

It gets harder. The light that bounces off a real surface and makes it back to a tiny sensor is not a beam. It is a thin sprinkle of individual photons, sometimes only a few per pulse, mixed in with stray light from the sun and the room. There is nothing clean to time. So a direct Time-of-Flight sensor, or dToF, does not time one pulse. It fires the same short pulse many times and records, for each returning photon, how long after firing it arrived [0004]. Out of thousands of those tiny timing events, a pattern appears. Distance comes from the statistics of when photons return, not from one clean measurement.

A dToF sensor measures the actual travel time of light and reads distance straight off it [0003]. Its cousin, indirect Time-of-Flight, or iToF, shines a gently flickering light and measures how far the flicker has slipped out of step by the time it returns [0003]. Both reach distance, but dToF works in raw time, which is why timing a few photons is the whole game. Two parts make it possible. The detector that can catch a single photon is a single-photon avalanche diode, a SPAD, and the circuit that stamps each arrival with a time is a time-to-digital converter, a TDC. They are the front door of the whole sensor.

## The Patent's Claim Is One Sentence About Bins

Strip the sensor down to its load-bearing idea and you reach US 2026/0140238 A1, a 2024 STMicroelectronics filing with the plain title "Ultra-Lean Time-of-Flight Histogram Processing." The patent puts the whole idea on one line of its abstract, a processing circuit that:

> processes time-of-flight measurement data using sequential bin-by-bin histogram processing

US 2026/0140238 A1, Abstract.

The first claim requires the same step in nearly the same words, a circuit that processes the data "using a sequential bin-by-bin histogram processing" and applies, as it does so, "one or more on-the-fly operations" [0015]. Two phrases do all the work. A bin is a single slice of time, one narrow window after the laser fires, holding the count of photons that came back during that window. "Bin by bin" means the circuit reads those slices one at a time, in order, the way you might read a ruler mark by mark rather than taking in the whole ruler at once. The cleverness is in that "one at a time."

## A Histogram Read One Bar at a Time

Picture a bar chart. Along the bottom runs time since the laser fired, which, because light travels at a fixed speed, is really distance. Up the side runs how many photons arrived in each little time window. Fire the pulse thousands of times, drop each returning photon into the slice it belongs to, and the bars grow. Most stay low, fed by random room light. But at the slice that matches the real surface, returns pile up and one bar climbs above the rest. That bar chart is a **histogram**, and the tall bar is the answer: its position along the bottom is the round-trip time, and the round-trip time is the distance. Find the peak and you have found the surface.

One more piece makes it a camera rather than a single tape measure. The sensor splits its view into a grid of cells, and each cell builds its own histogram and reports its own peak. Each cell is a **zone**, and a grid of them is a multizone sensor, so the output is a whole array of distances, one per zone, a coarse depth picture of whatever the sensor faces.

Here is the move the hero patent is built around. The obvious way to find the tallest bar is to store the whole chart, every bar for every zone, and then scan it. That works on a big computer with memory to spare, and the patent refuses to do it. Imagine the bars riding past on a conveyor belt instead. The circuit looks at each bar as it arrives, keeps only the last few in view, and watches for the moment a bar rises and then falls back. **The peak is marked as it streams past, so the full chart never has to be stored.**

The patent puts it directly: rather than storing full histograms or several copies of the data, the system "employs a bin-serial processing approach" that handles the data "in a streaming fashion, significantly reducing memory requirements" [0042], and the circuit is built "to iterate the histogram by serially computing relevant outputs in a single pass" [0069]. To spot a true peak it only needs that short run of recent bars, a small running state instead of the whole picture [0016].

The single-pass idea did not appear from nowhere. An earlier STMicroelectronics filing, US 2023/0296739 B2, "Methods and devices for identifying peaks in histograms," sets out the underlying principle, with each bin of the histogram, in its words:

> each bin of the histogram representing a photon count corresponding to a distance from a light-ranging system

US 2023/0296739 B2, paragraph [0003].

That support filing walks the bins once, in order, against a moving threshold. It marks a peak where the count rises above the line and then drops back below it, all in a single sweep. The hero patent's contribution is to carve that principle lean enough to run on the sensor's own chip. The same engineer, Andreas Assmann, is named on both filings, one idea carried from its 2022 statement to its 2024 landing in silicon. The streaming peak finder is the part this story is about. Around it sits a small cluster of adjacent ST filings that each handle one other step of the pipeline: building the bins, summing several SPAD outputs into one, pulling distance from a histogram, sharpening that distance, and assembling the full multizone grid. Those five filings are listed in the sources below.

## Lean Math Is Why the Whole Sensor Fits on a Fingernail

Memory is the reason this matters in your hand rather than on a bench. The patent is blunt that conventional Time-of-Flight holds the full histogram, often in several copies, in substantial memory, and that those large memory banks become "prohibitive" in battery-powered or compact devices [0013]. Take the memory away and the rest follows. The processing no longer needs a power-hungry chip with room to spare. With local storage cut to a handful of registers, it can ride on the sensor's own small circuitry [0043], which is part of what lets a complete sensor shrink to roughly the size of a fingernail.

This is where the patent meets a real product. STMicroelectronics describes its VL53L9 module as resolving 2,268 zones, a grid of 54 by 42 cells it markets as "2.3K zones." That grid spans a 54-by-42-degree view, reaches from about 5 cm out to 9 m, and refreshes up to 100 times a second, with the histogram processing done on the module's own chip and the scene lit by a spread of infrared light rather than a single spot. The company frames the jump as roughly thirty-five times the resolution of its prior generation, which topped out near 64 zones. It is careful with the word "first," calling the module the first direct Time-of-Flight 3D LiDAR all-in-one module in its own portfolio rather than the first ever, since multizone dToF already existed. What is genuinely new is the resolution and the spread of light, and underneath both sits the lean processing the patent describes.

## The Grammar the Rest of the Story Is Written In

Three plain ideas carry the whole sensor: a histogram is photons sorted by arrival time, a zone is one cell of the view with its own histogram, and the peak in that histogram is the distance. Stream those slices in order, mark the peak on the way past, and keep almost nothing in memory. That is what lets the idea run on a chip small enough to disappear into a phone or a robot, and it is the grammar everything in this series is built on. There is a catch, and it is the next chapter. A peak is only as trustworthy as the histogram under it, and bright sunlight or a pane of glass can stack returns in the wrong slice and raise a peak that points at nothing. Part 2 is about learning to trust the distance.

# Sources

## Patents
- US 2026/0140238 A1, "Ultra-Lean Time-of-Flight Histogram Processing," STMicroelectronics International N.V., priority 2024-11-19, published 2026, inventors: Donald Baxter, Pascal Mellot, Stuart McLeod, Andreas Assmann.
- US 2023/0296739 B2, "Methods and devices for identifying peaks in histograms," STMicroelectronics Research & Development Ltd., priority 2022-03-17, inventor: Andreas Aßmann.
- US 2021/0302550 A1, STMicroelectronics (cluster context: time-to-digital conversion that builds the histogram bins).
- US 2020/0400792 A1, STMicroelectronics (cluster context: summing several single-photon detector outputs into a bin).
- US 2018/0253404 A1, STMicroelectronics (cluster context: extracting distance from a time-of-flight histogram).
- US 2024/0353538 A1, STMicroelectronics (cluster context: rising-edge super-resolution to sharpen distance).
- US 2019/0109977 A1, STMicroelectronics (cluster context: assembling the multizone sensor array).

## Official statements
- STMicroelectronics, VL53L9 launch press release (newsroom item p4783, 2026-06-22). https://newsroom.st.com/media-center/press-item.html/p4783.html
- STMicroelectronics, VL53L9 product blog. https://blog.st.com/vl53l9

## Technical specs
- STMicroelectronics, VL53L9 databrief DB5805 (Rev 2). https://www.st.com/resource/en/data_brief/vl53l9.pdf
