
# Nine Levels, No Waveform Generator: Google's Patent for Qubit Control at 3 Kelvin

![FIG. 1: the claimed architecture, drawn as boxes.](input/figures/fig-01.jpg)

*FIG. 1: the whole bet in one frame. Driver circuits (102) each hold one calibrated constant current. The switch network (104) either grounds each current or adds it to the single output feeding the quantum computing circuit (108), with the controller (110) deciding which switches close. There is no waveform generator anywhere in the diagram.*

## The Missing Waveform Generator

To move a superconducting qubit between its operating frequencies, a control system has to deliver precisely shaped current pulses. The standard way to buy that precision is a general-purpose digital-to-analog converter, the chip that turns a stored number into a physical voltage, with 16,384 values of resolution at its disposal [0016]. Racks of such channels, running at room temperature, are the visible default of qubit labs. A Google patent granted June 9, 2026, builds its controller around nine current levels instead [0022].

Nine levels against fourteen bits invites a reasonable objection: a controller with a single-digit menu of outputs cannot run a quantum computer, and precision is exactly why the racks exist. Hold that objection. The patent's answer to it is the entire architecture. FIG. 1 shows what remains once the waveform generator is gone: driver circuits that each hold one constant current, a switch network that sums a chosen subset of them into the output (claim 1), and a controller deciding which switches close. Filed in February 2023 by Joseph Cheney Bardin and Seyed Mohammadreza Fatemi, the patent spends most of its pages explaining why that is enough.

## What the Attenuators Are For

The incumbent chain starts loud. In the patent's background description, control relies on "high-magnitude control signals generated at room temperature using general purpose digital-to-analog converters (DACs)" [0016]. The loudness is then deliberately unmade: on the way down to the qubits, the signals pass through cold attenuators, "lowering the signal's noise to near thermally-limited levels (the cryogenic noise floor) through high levels of attenuation, e.g., 20 dB" [0016]. An attenuator weakens a signal on purpose, and the energy it removes is dissipated right where the attenuator sits, next to the quantum hardware [0016].

That is the first cost, and the patent states it as the motivating problem:

> "However, this process results in a high level of power dissipation in the attenuators, which may negatively affect quantum circuit operation (e.g., increase the temperature of quantum components and reduce coherence)."
> US 12,652,259 B1, [0016]

Two more costs follow in the same paragraph. Running a converter at pulse speed is expensive, since "fast DAC operation (e.g., at GHz speeds) is associated with high power consumption" [0016]. And an entirely-DAC-based generator does not emit a clean tone. It emits "both signal and noise with a wide-band spectrum" [0016]. For scale, one industry survey of superconducting machines puts typical drive-line attenuation near 60 dB across the temperature stages, and notes that a naively wired 100-qubit system can spend its whole 100-millikelvin cooling budget on attenuators alone (PostQuantum overview).

The signal is made loud at room temperature. The refrigerator then pays, in its scarcest currency, to make it quiet again.

## Four Frequencies, Nine Levels

That whole chain exists to serve one assumption: controlling a qubit means being free to synthesize any waveform at any moment. The patent is built on the recognition that the assumption is wrong:

> "Some implementations of the present disclosure, such as the circuit device 100, are based on the recognition that, in practice, fast arbitrary waveform generation, such as that provided by a fast, high-power DAC, is not necessary for quantum control operations."
> US 12,652,259 B1, [0022]

The next sentence finishes the thought: "Rather, a relatively small number of signal levels may be sufficient" [0022]. How small? In the patent's worked picture, a qubit is switchable between four frequencies, one for single-qubit gates, one for two-qubit gates, one for readout, one for reset [0022]. Claim 10 carries the same structure in claim language: four switch settings, each summing a different subset of currents, each parking the qubit at the frequency for one of those four operations (claim 10).

The example current menu is concrete, "a 20 μA pulse to be set to a frequency for single-qubit gate operation" [0030], and the same example assigns 25 microamps to the two-qubit gate, 35 to readout, and 500 to reset [0030]. Fast switching then only ever chooses among "eight different well-defined current levels plus a zero-bias level, for nine total levels" [0022]. The patent hedges these counts as a worked example, not a claim limit. Claim 10's four settings are the version with legal weight.

FIG. 9 draws what the output actually looks like: a DC component (906) holding a bias, two stepped pulses (902, 904) of different heights, and a switching time (908) at the edges. No synthesized curve, no envelope. Quantum control, in this drawing, is a staircase of a few well-chosen currents.

*FIG. 9: the device's entire waveform vocabulary. A DC level (906), stepped pulses (902, 904), and edge switching times (908) specced below 10, 5, or 2 nanoseconds [0028].*

**The objection assumed control is a waveform problem. The patent bets it is a selection problem.**

What the objection still gets right is that something, somewhere, must be exact. The patent's move is to take that exactness off the clock.

## Splitting Precision from Speed

The organizing decision is to give precision and speed to different blocks, and the patent says so in one sentence:

> "As another way of describing operation of the circuit device 100, high-precision/high-bit current output with low noise (provided by reconfiguring the driver circuits 102) has been separated from high-speed switching (provided by the switch network 104), to facilitate low-noise, low-power, high-speed operation."
> US 12,652,259 B1, [0024]

The all-in-one alternative, a DAC that is simultaneously precise and quiet and fast, is named as the inferior design: combining the functions in one unit "may result in higher noise, higher power consumption, and/or lower-speed operation" [0024].

The precision half lives in the driver circuits, and FIG. 3A traces one: a reference voltage circuit (302) feeding a low-noise LDO regulator (304, a quiet voltage source), a programmable DAC (306), and a front-end circuit (308) built around an operational amplifier (314) and a load resistor (310), all to manufacture one stable current. The DAC here is slow on purpose. Driver currents are "adjusted as part of a calibration process performed periodically and/or upon startup" [0058]. Between calibrations they simply hold. Nothing on the precision path runs at pulse speed, so nothing on it pays the gigahertz power bill from the background chain [0016].

*FIG. 3A: one driver's calibration chain, the slow and careful half.*

The noise budget rests on one physical asymmetry: "resistor noise is thermal noise that decreases with decreasing temperature" [0041], while transistor channel noise does not fall with cooling the same way. So the patent commits to "resistor-dominated design" [0041]: place resistors where they set the noise, and let the cold do the filtering. FIGS. 3B-3D draw that discipline three ways, as output stages whose load resistors shield the transistor noise at low, high, or all frequencies, and claim 8 turns it into a claimed property: operated cold, a driver outputs a current whose dominant noise component is "associated with a resistance" (claim 8). The device itself "can be configured for operation at temperatures of 3K or lower" [0026]. The patent then runs the same discipline through six more front-end variants and an adjustable load-resistor network.

*FIGS. 3B-3D: three output stages with the noise sources drawn in. Resistor noise (4kT/R) collapses at cryogenic temperature, and each topology shields the transistor noise at low, high, or all frequencies [0041].*

The fast half is the switch network, and FIG. 8 is its unit cell: two identical, balanced switch networks (802, 804) driven by complementary enable commands (806), steering a driver current either to ground or to the output (808). The symmetry is itself noise engineering. Balancing "cancels clock feedthrough" and routes transistor channel charge "to/from ground rather than to/from the output" [0071]. The unit switches "with switching times less than 2 ns, while maintaining low noise" [0074], and claim 3 fixes that figure as a limitation (claim 3). At the output, the network performs the only real-time arithmetic the architecture needs, "a sum of a subset of the currents" (claim 1).

*FIG. 8: the fast half, one balanced switch unit.*

The numbers the patent attaches are pulse edges of "less than 10 ns, less than 5 ns, or less than 2 ns" [0028] and, in its example, a noise component below 30 nanoamps on a 1-milliamp output [0028]. Claim 6 writes low cryogenic noise into the claims as a property in its own right (claim 6).

The DACs did not get faster. They got taken off the clock.

## The Other Control Plane

Cold control chips, by themselves, are not the news here. Google's own team put one at 3 kelvin years ago: a 28-nanometer CMOS controller presented at ISSCC in 2019, about 1 by 1.6 millimeters, dissipating under 2 milliwatts while addressing a single transmon qubit (arXiv 1902.10864; UMass Amherst release). Intel announced Horse Ridge II in December 2020, a cryogenic chip meant to bring control functions "as close as possible to the qubits themselves" (Intel newsroom), and later operated it at the roughly 4-kelvin stage. If the thesis here were that control simply moves into the refrigerator, an informed reader could dismiss it on sight.

The line that separates this patent from those chips is which control plane it speaks. The 2019 controller's published scope is a 16-word, four-bit XY gate instruction set, the microwave drive that rotates a transmon's state (arXiv 1902.10864), and Intel's Horse Ridge family likewise targets the room-temperature microwave racks (Intel newsroom). This patent claims the other plane, the one made of steady currents rather than shaped tones. The specification's named examples are bias-type signals, "Z control signals and g control signals" [0015], and claim 9 names the physical coupling outright: "a qubit arranged to receive a magnetic flux associated with the output signal" (claim 9).

Two hedges belong on the record. The patent gives Z and g as examples, not an exclusive list [0015], so the fair statement is that its worked examples are flux-type bias controls. And the XY-versus-flux layering of the earlier chips comes from their own publications rather than from this patent's text.

On that plane, the differentiator is subtraction. The current path from drivers to qubit can have "no attenuation, less than two times attenuation, or less than five times attenuation" [0059], and in some implementations "these high-attenuation attenuators are not included" [0059]. The driver currents "originate at a cryogenic temperature" (claim 27), "instead of originating at room temperature and being attenuated for low-temperature operation" [0060]. Claim 26's ceiling of "less than five times current attenuation" and the background chain's 20 dB blocks [0016] are not the same kind of number, and the patent never converts between them. The contrast it draws is simpler: one chain is built around attenuators, the other deletes them.

The continuity runs through a person as well. Joseph Bardin, lead author of the 2019 ISSCC paper (UMass Amherst release), is one of this patent's two inventors. The 2019 chip proved a controller could live at 3 kelvin. This patent is about what a controller should be doing there.

## Calibrate Rarely, Switch Fast

The operating model that falls out is unusual for a control system. Precision happens rarely: the driver currents are set during a calibration pass, periodically or at startup, then treated as constant, the fixed raw material for every pulse until the next calibration [0058]. Speed happens constantly, and consists of nothing except choosing which of those constants reach the output, a sum the switch network can re-decide in under 2 nanoseconds [0083] (claim 3). The expensive thing, an exact and quiet current, is manufactured offline. The cheap thing, a switch flip, is the only thing done live.

Reading this against Google's public quantum program requires a hedge, since the patent says nothing about products. The public story is told in qubit counts and error rates: the Willow chip, announced in December 2024 with 105 qubits and the first below-threshold error-correction demonstration (Google announcement), and a roadmap whose final milestone is a machine of roughly a million physical qubits, targeted around 2029 (Google Quantum AI roadmap). What a patent like this one shows is a workstream underneath those headline numbers: the control plane those qubit counts quietly assume.

Which returns to the opening objection. The 14-bit generator was never wrong about precision. It was wrong about where precision has to live, and this patent moves it into the calibrated current, set long before the pulse, while the pulse itself is reduced to selection [0024]. Whether nine levels and four frequencies remain sufficient when error correction runs across a million qubits is the open end of the bet. The patent does not claim that scale. It claims the vocabulary. What is on the record, as of June 9, is the recognition itself: the qubit never asked for a waveform. 🤔

# Sources

## Patents

- US 12,652,259 B1, "Quantum control signal generation," Google LLC, priority 2023-02-16, granted 2026-06-09, inventors: Joseph Cheney Bardin, Seyed Mohammadreza Fatemi.

## Papers

- Bardin, et al. (2019). Cryogenic 28-nm bulk-CMOS qubit controller for transmon qubits (descriptive title; ISSCC 2019 / JSSC, Nov. 2019). https://arxiv.org/abs/1902.10864

## Official statements

- Intel Newsroom, Horse Ridge II announcement, 2020-12-03. https://www.intel.com/content/www/us/en/newsroom/news/2nd-gen-horse-ridge-cryogenic-quantum-control-chip.html
- Google, Willow quantum chip announcement, December 2024. https://blog.google/innovation-and-ai/technology/research/google-willow-quantum-chip/
- Google Quantum AI, error-correction roadmap, Milestone 6. https://quantumai.google/qecmilestone

## News & media

- UMass Amherst News Office, release on the 2019 cryogenic qubit controller. https://umass.edu/newsoffice/article/umass-amherst%E2%80%99s-joseph-c-bardin-helps

## Technical specs

- PostQuantum, superconducting qubits overview (wiring and attenuation baseline). https://postquantum.com/quantum-modalities/superconducting-qubits/

