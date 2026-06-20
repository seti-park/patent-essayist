# SanDisk Is Trying to Own the Packaging Grammar of High Bandwidth Flash, Unexamined

![Figure 36A: the high bandwidth flash package.](figures/fig-36A.png)

*Figure 36A: the full package. A high bandwidth flash memory stack (2000) sits on an optional system level logic die (3000), an interposer (4000), and a packaging substrate (5000), joined into one vertical tower by arrays of solder bumps. It is the patent's most system-level view, and to an investor's eye it looks like an HBM package with flash where the DRAM would be.*

## The Second Front Nobody Announced

For the last two years the high-bandwidth-memory moat has had a fixed shape in investors' minds. Stack DRAM dies on top of a logic base die, wire the whole tower together with through-silicon vias, and you get HBM: the memory architecture that feeds AI accelerators and the one the DRAM incumbents now fight over as industry context rather than commodity (News & media). The grammar of that moat (stacked memory, dedicated logic underneath, vertical interconnect) has been treated as a DRAM story.

This SanDisk filing quietly applies the same grammar to NAND. It gives the result a name. The application states that "Each vertical stack of two or more bonded assemblies 1000 constitutes a high bandwidth flash memory stack 2000." [0153] High bandwidth flash, framed by the wider market as the NAND-side analogue of HBM (News & media), is being staked out by a flash maker using the structural move the DRAM incumbents already made. The question for diligence is not whether the architecture is clever. **The question is whether this is a real second front in the memory moat, or a broad bet on an obvious analogy.**

## What the Application Actually Claims

The architecture is easier to judge once you see its atom. Each NAND memory die is bonded face-to-face to its own dedicated memory-controller die, a separate piece of CMOS logic whose job is to run that one array. The application is specific about the division of labor: "The memory controller circuit 720 is configured to control operation of the memory array within the memory die 900." [0115] One controller, one array, bonded into what the patent calls a unit bonded assembly (1000).

*Figure 21: the unit bonded assembly. A memory die (900), the upper block of alternating layers and vertical channels, bonded at its front bonding structures to a dedicated memory-controller die (700) below, which carries the controller circuit (720) and through-substrate vias (716).*

That dedicated pairing is the load-bearing choice. Because every die already has its own controller, the system logic die above the stack is freed from per-cell work: the application notes that "Each bonded assembly 1000 chip includes a dedicated memory-controller die 700, and the system level logic die 3000 is not required to directly control the operation of each memory cell in each of the memory dies 900." [0188] The long paths to that top-level logic carry system commands rather than cell control, "which reduces control signal delay" [0188].

From the atom the structure stacks. Independent claim 1, restated in the description, recites "a plurality of stacked bonded assemblies 1000" in which each neighboring pair is bonded so that "electrically conductive paths vertically extend from a first horizontal plane HP1 including a bottom surface of a bottommost bonded assembly 1000 of the plurality of bonded assemblies 1000 at least to a second horizontal plane HP2 including a bottom surface of a topmost bonded assembly 1000 of the plurality of bonded assemblies 1000." [0174] Power and signal run bottom to top through the whole tower. The disclosed payoff is stated qualitatively, as "increased bandwidth and memory capacity" [0055]; the application discloses no bandwidth number, and neither will this essay.

*Figure 33: a vertical stack of bonded assemblies, with reference planes HP1, HP2, and HP3 marked and conductive paths running the full height through through-substrate vias and bonding-pad arrays. The illustration shows three assemblies, but claim 1 recites only a plurality, not a count.*

## Where the Defensibility Actually Lives

For a packaging patent, the most revealing section is how the dies are made, because that is where a moat is either cheap to build or easy to copy. Here the application leans hard on optionality. The NAND array and the CMOS controller are fabricated on separate wafers and then bonded, and almost every join in the flow is offered two ways. Assemblies stack "using chip to chip (i.e., assembly to assembly) bonding or wafer-to-wafer bonding to reduce production costs." [0056] The bond itself can be either route: "A metal-to-metal bonding or a solder-mediated bonding may be employed to bond vertically neighboring pairs of bonded assemblies." [0056] Even the metal-to-metal path is plural, since it "may comprise wafer to wafer bonding, die to wafer bonding or die to die bonding." [0171]

*Figure 20: the finished memory-controller die (700) on its own semiconductor substrate (709), with the controller circuit (720), through-substrate vias (716), and front bonding structures ready to mate with a memory die.*

Splitting the controller onto its own logic-optimized wafer (Figure 20) is what makes that menu possible, and it is the strategically important part. Hybrid and metal-to-metal die-to-die bonding is established practice for separating a memory array from its CMOS (News & media), so no single step here is exotic. The application's own framing is that "the chips can be stacked using micro-bumps or by direct metal-to-metal bonding to form the flash memory stack 2000 using a lower cost, simplified method." [0176] **The defensibility on offer is not one hard trick but a cost-and-process envelope, the kind of moat that holds only if it is broad on paper and backed by a family.**

## Real, But Conditional

Breadth is the strong side of the ledger, and it lives in the independent structure claim. Claim 1 reads on essentially any stack of dedicated-controller-plus-memory bonded assemblies with bottom-to-top vertical paths [0174], regardless of which bonding route a competitor picks. A claim written at that altitude is hard to design around by swapping process steps. The exposure sits in the short independent method claim, claim 15, which the summary describes as little more than "bonding a first memory die to a first memory-controller die to form a first bonded assembly" [0004] and then stacking the assemblies. A bond-bond-stack method stated that plainly is the kind of broad claim most open to prior-art narrowing.

The decisive qualifier is status. US 2026/0006802 A1 is a published application, not a granted patent: these are rights sought, not rights held, and claim 1 could narrow before it issues.

Two design-arounds sit right at the claim's edge, and the patent names both by what it defines itself against. One is the monolithic path it disposes of in its own background, "sequentially depositing memory device layers over a driver circuit located on a silicon wafer" [0002]: build the stack as one wafer rather than bonded assemblies and the structure claim has nothing to grip. The other is the inverse of the dedicated-controller limitation, a single shared controller doing the per-cell work that here is distributed; the application assumes the opposite, that "The system level logic die 3000, if present, controls the operation of the memory-controller dies 700 in each bonded assembly 1000" [0159] rather than the cells. A rival that keeps one controller in charge of the cells reads outside the claim's center of gravity.

## What Will Confirm or Break It

The moat is real but conditional. It is real in the breadth of the structure claim and in a manufacturing envelope that prices defensibility into cost and optionality rather than one fragile step. It is conditional on a prosecution that has not happened and on a patent family that, for now, is industry inference rather than verified fact (Patents).

Two events will settle it. The first is how claim 1 issues: substantially as filed, and the second-front reading strengthens; narrowed to the specific bonding embodiments, and the monolithic and shared-controller design-arounds win. The second is whether a real HBF family stands behind this one application, because a single broad claim is a flag planted, and a thicket is a moat held. The packaging grammar is staked. Whether SanDisk gets to keep it is a question the patent office, not the filing, will answer.

# Sources

## Patents
- US 2026/0006802 A1, "High Bandwidth Flash Memory Containing a Stack of Bonded Logic and Memory Die Assemblies and Methods for Forming the Same," SanDisk Technologies, Inc., priority 2024-06-28, published 2026-01-01, inventors: Mitsuteru Mushiga, Masaaki Higashitani.

## Official statements
- Sandisk, "Sandisk and SK hynix Begin Global Standardization of Next-Generation Memory Solution, High Bandwidth Flash (HBF)," Sandisk Newsroom, 2026-02-25. https://www.sandisk.com/company/newsroom/press-releases/2026/2026-02-25-sandisk-and-sk-hynix-begin-global-standardization-of-next-generation-memory-solution-high-bandwidth-flash-hbf

## News & media
- "Sandisk and SK hynix join forces to standardize High Bandwidth Flash memory, a NAND-based alternative to HBM for AI GPUs," Tom's Hardware. https://www.tomshardware.com/tech-industry/sandisk-and-sk-hynix-join-forces-to-standardize-high-bandwidth-flash-memory-a-nand-based-alternative-to-hbm-for-ai-gpus-move-could-enable-8-16x-higher-capacity-compared-to-dram
- "Hybrid Bonding Makes Strides Toward Manufacturability," Semiconductor Engineering. https://semiengineering.com/hybrid-bonding-makes-strides-toward-manufacturability/
