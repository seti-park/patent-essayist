---
essay_id: vl53l9cx-ep2-crosstalk-us20240192337
patent_reference: US 2024-0192337 B2
spine_source: handoff/01-design/thesis-spine.md
draft_version: 2
mode_used: strict-execution
posture_used: measured
---

# The Chip Learns to Ignore Its Own Reflection in the Glass

![FIG. 1: the ToF imager and the histogram it produces](figures/fig-01.png)

*FIG. 1: the same architecture Article 1 introduced. The VCSEL emitter (103) fires a light pulse; the SPAD array (101) times the return through the TDCs (107); the result is the histogram (109), a per-distance count of returned photons, with a real target showing up as a peak. This piece picks up that same output and asks what else is hiding inside it.*

Look in a window at night and you will see two things at once: whatever is on the other side of the glass, and your own reflection staring back, layered right on top of it. A time-of-flight sensor has the same problem, except it cannot tell the two apart just by looking. It fires a laser pulse through its own protective cover glass and times how long the reflection takes to come back. That timing data becomes a histogram, the per-distance count of returned photons that Article 1 introduced as this sensor's raw material. A real object shows up as a peak in that histogram [0032]. So does the sensor's own reflection off the inside of its cover glass, and the two peaks are made of the exact same stuff: laser light bounced back into the same detector array. Nothing about the light itself says which peak is real.

That is the puzzle at the center of US 2024-0192337 B2, "Cross-talk rejecting convolution peak finding," an STMicroelectronics patent from the same inventor, Andreas Assmann, behind Article 1's mechanism. If Article 1 was about reading the histogram, this one is about cleaning it before anyone reads it.

## The Cover Glass Writes a Fake Target Into the Histogram

Every one of these sensors sits behind a window that protects the SPAD array and the emitter from dust and scratches. The window is only millimeters away, and it reflects some of the outgoing pulse straight back into the detector before the beam ever leaves the housing. The patent's own language for this is direct: "The window reflects a portion of the transmitted light signal 104 back to the SPAD array 101, this phenomenon is referred to as cross-talk (may also be referred to as cover glass reflection, or housing reflection), and the reflected light signal by the window is referred to as a cross-talk signal" [0029]. (The same word, cross-talk, also covers stray light bouncing around inside the housing itself, not only the cover glass case, though the window reflection is the one this patent works through in detail.)

Because the window sits so close to the array, that reflection lands in the first few bins of the histogram, at what the patent calls the "near zero distance" region. FIG. 3 makes the shape of the problem plain: a tall, sharp peak (201) parked right at the recalibrated zero point, and a shorter, real-target peak (203) further out.

*FIG. 3: the histogram recalibrated so the cover-glass reflection sits at the "reference zero-point." Peak 201 is the ghost; peak 203 is the real target further down the range. Nothing about the shape of either peak announces which one is which.*

That near-zero ghost is not a curiosity. It is a false reading. As the patent puts it plainly, "The cross-talk signal in the histogram, if not processed properly, may be incorrectly detected as a close target" [0029]. A sensor that trusts its own histogram without a way to tell the ghost from the real thing will report an object sitting almost on top of itself, every time, whether or not anything is actually there.

## The Test That Reads Where the Ghost Has to Sit, Not What It Looks Like

The two conventional ways of turning a histogram into a distance each fail against this problem in a different direction. A matched filter (MF) reaches out to long range, but "the MF based target detection is very sensitive to cross-talk" [0056]. A zero-crossing filter (ZCF) can be made to ignore the ghost, but "ZCF based target detection may not perform well for far-away target" [0055]. FIG. 6 shows both filters running on the same histogram, and both of them find the same two candidate peaks, 611 near the sensor and 613 further out. Neither filter, on its own, has any way of knowing that 611 is the ghost.

*FIG. 6: the matched filter (603) and zero-crossing filter (601) outputs overlaid on the histogram. Both filters flag the same two candidate peaks, 611 near zero and 613 further out. Neither filter alone can tell which one is real.*

So the chip does not try to make one filter smarter. It exploits something the ghost cannot hide: where it has to sit. The cross-talk reflection is fixed by the sensor's own geometry, the distance between the SPAD array and the cover-glass window, and that distance never moves. The patent locates the histogram bin at exactly that distance and calls it the reference zero-point: "the histogram bin having a distance equal to the distance between the SPAD array 101 and the window of the assembly housing is identified, and its location is used as the reference zero-point" [0060]. Every bin before that point gets a negative weight; every bin after it gets a positive one. Run the ZCF output through those weights and sum each candidate pulse region, and "the weighted sum calculation described above penalizes values of the positive pulse region before the distance D, because these values are mostly likely caused by cross-talk" [0054].

**The chip does not need an outside reference to catch its own reflection. Its own housing already told it where to look.**

FIG. 9 is that test running on the same two peaks from FIG. 6. The weighted curve (601W) pulls 611 down past the negative threshold, classifying it as cross-talk, while 613 clears the positive threshold as a validated target [0052]. Compare that to a mirror: you do not need a second window to know your reflection is behind you rather than in front of you. You just need to know where the window is. This patent gives the chip the equivalent of that fact, baked into its own dimensions, computed once and reused rather than measured anew for every unit.

*FIG. 9: the weighted ZCF curve (601W) against the P_thresh / N_thresh classification band. The near-zero peak lands below N_thresh and is discarded as cross-talk; the real target clears P_thresh and survives as a validated candidate.*

## Two Known Filters, One New Fence

A fair objection at this point: isn't this just switching between two filter types that already existed? Neither piece here is new. Matched filters and zero-crossing filters are both established signal-processing tools, and the patent itself concedes each one's failure mode outright, the ZCF's weakness at range [0055] and the MF's weakness against cross-talk [0056]. Read that way, the invention looks less like a new engine and more like a safe fence built around ground the industry already understood, switching between two known quantities rather than inventing a third.

That framing misses what is actually claimed. The invention is not "ZCF" or "MF." It is the specific weighted-sum classification pinned to the geometric reference zero-point, plus a decision module that runs both filters in parallel and switches between their outputs. FIG. 10 is that whole system in one diagram: the histogram feeds a zero-referencing step and a weight-coefficient generator on one side, and the raw ZCF and MF filters on the other, and only after the weighted output has classified each candidate does a switch-over decision module compare the strongest surviving target from each path. That comparison step, and the weighting scheme that feeds it, is what the claims actually protect, not the underlying filter math.

*FIG. 10: the full adaptive-detection flow. Histogram (801) into weight-coefficient generation (807, 809) and the ZCF/MF paths (811, 803) in parallel; target classification (817) and the switch-over criteria (821) sit between the raw filter outputs and the final valid-target list (825), the combination this patent claims.*

And the effect of that combination is the point. As the patent states it, "the disclosed ZCF based target detection method can reject false target caused by cross-talk, thus achieving robustness against cross-talk," and "the disclosed adaptive detection method enjoys benefit from both the ZCF based detection and MF based detection, thereby achieving robustness against cross-talk while still maintaining long detection range" [0076]. Two individually insufficient filters, combined through one classification rule keyed to the sensor's own housing, close a gap that neither filter closes by itself. That is engineering integration, not a rebrand of parts that already existed.

## What the Combination Actually Buys, With and Without the Ghost Present

The patent's own evidence for this is comparative rather than a single pinned number, and it is worth reading that way rather than looking for a headline percentage the specification does not state. With no cross-talk present, plain ZCF detection is accurate at close range but "was unable to correctly detect target at long range due to the SNR attenuation" [0067], while the adaptive method matches the long-range detection of MF without losing that close-range accuracy. Add cross-talk back in, and plain MF detection, "due to its sensitivity to cross-talk, locks on to the false target generated by cross-talk, and was unable to detect target correctly at close range" [0068]. FIG. 12 shows exactly that failure: the MF-only curve (903) tracks the ghost and locks onto it, while the adaptive method (905) stays on the true depth line (907) across the same range.

*FIG. 12: measured performance with cross-talk present. Plain MF (903) locks onto the false near-zero target; plain ZCF (901) rejects the ghost but loses range beyond about a meter; the adaptive method (905) tracks the true depth line (907) across the full measured range.*

The patent's own words for the combined result: "the adaptive detection method, by switching between MF based detection and ZCF based detection (e.g., choosing the ZCF based detection at close range and the MF based detection at long range if appropriate), was able to achieve correct target detection for a range comparable to that of the MF based target detection method" [0068]. That is the actual claim this essay is making, and no more than that. Neither filter is eliminated, and cross-talk sensitivity is not erased at the level of the physics. What the classification-and-switchover step removes is the forced choice between the two failure modes.

## The Patented Mechanism Behind a Marketing Line

All of this runs on the same silicon as the sensor itself, not on a separate processor bolted on afterward. The specification frames the conventional alternative as expensive: pushing histogram data off-chip "is not only costly (e.g., due to the number of IC devices needed), but also increases input/output (I/O) complexity of the ToF imager, requires large amounts of memory, and incurs time delay for data transfer" [0027]. FIG. 13 shows the fix built directly into the IC device (400): the SPAD array (401), the emitter (403), and the peak-finding circuit (407) all live on one die, so "the peaking finding circuit 407 performs on-chip processing of the histogram data from the SPAD array 401, which significantly reduces the chip complexity related to I/O transfer of histogram data to an off-chip processing module, and reduces the processing delay related to off-chip processing" [0069].

*FIG. 13: the peak-finding circuit (407) on the same IC device (400) as the SPAD array (401) and emitter (403), with the resulting depth map (409) staying on-chip.*

This is where the mechanism meets the product. ST's own public description of the VL53L9CX, the LiDAR module this patent family feeds into, states that its on-chip histogram processing and algorithmic compensation minimize the impact of cover-glass crosstalk and veiling glare. Set that marketing line next to the weighted-sum test just described and the connection is not a coincidence: this patent is the substance behind it, the specific, patented method by which "on-chip" stops being a marketing word and becomes an actual weighted-sum test running on the array's own die. ST separately describes the module as fully calibration-free. The patent's own word for fixing that reference point is, in fact, "a calibration of the bin distance" [0033], though it is a one-time geometric determination, "performed only once" with the result "saved for future use" [0060], rather than an external step that has to be repeated for every unit coming off the line.

A companion filing from the same inventor, US 2025-0012901, extends that same idea one step further, describing a system that "automatically adjusts the amount of cross-talk signal to be removed based on the current condition of the cover glass (e.g., scratch, smudge, dirt)," so the correction keeps working as the window itself changes over time rather than staying fixed at the factory-set value. None of this is the only problem a cover glass creates for a LiDAR sensor. ST holds separate patents against fingerprint smudging, mirror-like wraparound reflections reading as false-close targets, and overlapping clutter, each one its own fence around a different failure mode.

VL53L9CX is, in ST's own qualified words, "the first direct Time-of-Flight (dToF) 3D LiDAR all-in-one module in ST's portfolio." That claim is about the module, not this technique, and it is worth holding the two apart. This patent does not claim to be the first way to reject cross-talk, and it does not claim to solve the problem outright. What it claims, and what the record supports, is a specific way of doing it, on-chip, without an outside reference.

## Cleaning the Histogram Is What Makes Trusting It Possible

Article 1 showed how the chip pulls a distance out of a raw photon count. This one shows that the count arrives with the sensor's own reflection already mixed in, and that a fixed fact about the sensor's own housing, the distance to its own window, is enough to sort the ghost from the target without ever looking outside the chip for help. The histogram Article 1 taught you to read had to be cleaned before it was worth reading at all.

That cleaned, trustworthy histogram is also the input the next article in this series depends on. Article 3 asks what a robot does with a distance reading it can actually believe, when the question stops being "what is out there" and becomes "how do I move without falling off a ledge." The cross-talk rejection this patent claims is the reason that second question gets to be asked at all. 🤔

# Sources

## Patents

- US 2024-0192337 B2, "Cross-talk rejecting convolution peak finding," STMicroelectronics N.V., priority 2022-12-12, inventor: Andreas Assmann.
- US 2025-0012901, "Rising edge adaptive cross-talk correction," STMicroelectronics, priority 2023-07-07, inventor: Andreas Assmann.

## Official statements

- STMicroelectronics, VL53L9CX product page, https://www.st.com/en/imaging-and-photonics-solutions/vl53l9cx.html
- STMicroelectronics, VL53L9 press release, https://newsroom.st.com/media-center/press-item.html/p4783.html
- STMicroelectronics, VL53L9 blog post, https://blog.st.com/vl53l9/

## Technical specs

- STMicroelectronics community forum, "Ghost detections in VL53L7CX ToF sensor zones after crosstalk," https://community.st.com/t5/imaging-sensors/ghost-detections-in-vl53l7cx-tof-sensor-zones-after-crosstalk/td-p/864017
- STMicroelectronics, AN5856 application note, cover glass guidelines for VL53L5CX, https://www.st.com/resource/en/application_note/an5856-guidelines-for-the-cover-glass-of-the-vl53l5cx-timeofflight-8x8-multizone-sensor-with-wide-field-of-view-stmicroelectronics.pdf
