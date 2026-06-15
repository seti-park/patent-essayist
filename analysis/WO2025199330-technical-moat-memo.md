# Does Adept Have a Technical Moat? A Patent-Led Reading of WO2025199330

**Subject:** PCT application WO2025199330 A1, "Artificial Intelligence Agents for User Interface Task Workflow Automation," plus its granted US family.
**Origin:** Adept AI Labs (inventors: Zarkesh, Lukyantseva, Bavishi, Luan, Qian, Pajot, Bertsch, Elsen, Hawthorne).
**Prepared for:** technology-investor due diligence (moat assessment).
**Date:** 2026-06-15.

---

## Bottom line up front

This is well-drafted, genuinely technical, partly-granted IP. It is **not** a durable competitive moat for any single operating company, and the company that filed it has already proven the point: $415M went in, and the outcome was an acqui-hire in which investors roughly recouped principal with no upside.

The patent fences a *mechanism* (turn recorded human demonstrations into agent training data). The real moats in agentic AI sit one layer away from anything a patent can hold: the proprietary data flywheel, the post-training craft, and the people. All three have left the building, dispersing to **Amazon** (a 2024 acqui-hire plus a non-exclusive license) and to **Anthropic** (talent in 2024, and, on present evidence, the patent family itself in 2025). No single party holds an exclusive lock. On top of that, the architecture the patent protects, pixel-level visual UI automation driven by recorded demonstrations, is the exact approach the market began retreating from in 2025 and 2026 in favor of API-first agents.

Treat this portfolio as a **defensive and cross-licensing asset inside a larger lab**, not as the foundation of a standalone franchise.

### Moat scorecard

| Dimension | Rating | One-line basis |
|---|---|---|
| Patent / legal defensibility | **Weak to Moderate** | Real granted US coverage exists, and a few claims are narrow and crisp; but the broad concept overlaps decades of RPA and record-and-replay prior art, and training-data claims are very hard to detect infringement of. |
| Technical differentiation | **Moderate, eroding** | A handful of genuinely novel pieces; the surrounding agent loop is now industry-standard. |
| Talent / execution | **Weak** | The team was the moat. It scattered to Amazon and Anthropic, and the CEO has since left Amazon too. |
| Data flywheel | **Weak to Moderate** | A real data-generation engine, but the data and pipeline were licensed and (apparently) sold, not kept exclusive. |
| Strategic / market position | **Weak** | $415M in, acqui-hire out; the paradigm it protects is being exited. |
| **Overall investable moat** | **Weak** | Strong patent craftsmanship, weak durable advantage for any one company. |

---

## 1. What this patent actually is, and what it is not

WO2025199330 is one filing in a **16-application family**: eight US provisionals (filed March 20 and April 25, 2024) and eight US non-provisionals (filed October 2024), bundled under a single very large specification ([0001] to [0004]). The provisional titles read like Adept's product list: Persimmon-8B, Fuyu-8B, Fuyu-Heavy, **Adept Recorder**, **Adept Workflow Language (AWL)**, and "Frankenmodel."

The specification is a "kitchen sink." It carries roughly **174 figures** ([0036] to [00183]), a full textbook primer on Transformers and Vision Transformers (FIG. 1 to 10), and clause-set placeholders for at least five separable inventions (the Recorder, AWL the language, the AWL runtime, the training-data and data-flow system, and the Fuyu / magnitude-invariant model). That breadth supports a long pipeline of divisional filings, which is itself a signal of intent to build a portfolio rather than a single patent.

The point investors most often get wrong: **the operative claims of WO2025199330 are narrow.** The 20 claims (the legally binding part of the document) cover only the **recorder / training-data intermediary**, not the model, not AWL, not the runtime. Claim 1 reads:

> "A system for generating training data to train agents to automate tasks otherwise done by users, comprising: an intermediary interposed between an interface and a user, and configured to: intercept ... preserve a state of the interface prior to the execution of the task; translate the user-actuated actions into one or more actuation commands ...; and generate a training dataset ..."

Claims 19 and 20 are the matching method and computer-readable-medium versions. The Fuyu model, the magnitude-invariant encoding, AWL, and the runtime live in the shared specification and are pursued in **sibling** applications.

**Those siblings are real and several are already granted.** Confirmed US grants in this family include:

- **US 12,437,238 B1** "Generation of agentic trajectories for training artificial intelligence agents to automate multimodal interface task workflows" (filed 2024-10-07, **granted 2025-10-07**). This is the issued US counterpart of WO2025199330's recorder claims, with the identical inventor list.
- **US 12,387,036 B1** "Multimodal agent for efficient image-text interface automation" (the Fuyu / magnitude-invariant model).
- **US 12,566,913** "Artificial intelligence agents to automate multimodal interface task workflows."
- **US 12,430,150** "Runtime architecture for interfacing with agents to automate multimodal interface workflows."
- **US 2025/0299023 A1** "Systems and Methods for Configuring Artificial Intelligence Agents..." (pending application).

So there is genuine granted coverage with a useful early priority date (March 2024). The question is not "is anything granted" but "how much does it actually fence."

---

## 2. The invention in plain terms

**The recorder (the claimed core).** An intermediary sits literally between the user and the interface. When the user acts, the intermediary intercepts the action before it reaches the UI, snapshots the interface state, and converts the action into machine-replayable "actuation commands." The training pair is the load-bearing idea ([00372]):

> "The training dataset ... requires the agent ... to process, as input, the state of the interface prior to the execution of the task ... and to generate, as output, the actuation commands."

The captured state is unusually rich. Beyond screenshots and metadata, it can include the user's **thoughts** and **hints** and a natural-language task description ([00374]). That richer capture is the most defensible part of the recorder claim, because a bare "record the clicks" recorder is old.

**The model (sibling claims).** Fuyu-style decoder-only Transformer that handles arbitrary-length text and arbitrary-resolution images. Two distinctive moves: image patches are read line by line with a **newline token** marking row ends ([00551]), and text tokens and image-patch tokens are merged into a **single stream that is linearly projected with the embedding lookup bypassed** ([00554]). A second variant encodes each RGB subpixel as a **sign-only ("magnitude-invariant") bit vector** so the image representation survives the network's normalization layers ([00574] to [00577]). These are crisp, testable, narrow limitations and are the most patent-shaped material in the document.

**The data.** Eight training datasets ([00287] to [00294]), the most interesting being **agentic-trajectory data**: images of the agent performing workflows, interleaved with instructions, actions, the agent's "thoughts," interface DOMs, and URLs, organized per step and **gated by human-oracle approval** ([00294]). This is a concrete, layered data-pipeline claim and is closer to a real moat than the plumbing around it.

---

## 3. Patent strength: how much does it fence?

**Where it is genuinely defensible**

- The specific input/output training-pair contract plus the rich captured-state bundle (snapshots, metadata, user thoughts and hints, task description). Harder to design around than a generic recorder.
- The magnitude-invariant bit-vector encoding and the "bypass any embedding lookup" fused-stream design. Narrow, novel-sounding, and observable in a deployed model's architecture if disclosed.
- The agentic-trajectory dataset construction with human-oracle gating.

**Where it is weak or easy to route around**

- "Translate user actions into commands that replay on the UI" is, at altitude, what every robotic-process-automation and browser-automation tool has done for years (UiPath, Selenium and Playwright codegen). The novelty rests on the *training-data* framing ([00372]), not the replay.
- The screenshot plus task plus action-history observation loop ([00460], [00492]) is now the standard computer-use agent loop used across the industry, so broad claims there face heavy prior art.
- The client authors, server compiles, client interprets split ([00456], [00519]) is a conventional architecture.
- Large stretches are conceded prior art: synthetic data, transfer learning, human-in-the-loop, core sets, and active learning are all described as known background ([0009], [0012], [0014], [0016]), and FIG. 1 to 10 is a textbook Transformer primer. Background cannot anchor novelty.

**The enforceability problem (the part that most undercuts "moat").** The crown-jewel claims are about **how you generate training data** and **how you train**. These are internal processes. You usually cannot tell, from the outside, whether a competitor's agent was trained using an intercepting recorder that captured user "thoughts and hints" and emitted exactly this input/output pair. Method claims with low observability are hard to detect, hard to prove, and therefore weak as exclusionary weapons even when valid. By contrast, the model-architecture claims (embedding-lookup bypass, sign-only bit vectors) are more observable if a rival publishes or describes its architecture, which is why those, not the recorder, are the stronger enforcement candidates.

**Status caveat.** The PCT is a vehicle, not a grant. National-phase prosecution will test breadth, and the broad recorder concept is the most exposed to narrowing. The granted US members are the ones to read claim-by-claim before relying on scope.

---

## 4. The real moat question: where moats live in agentic AI

A common view among practitioners is that frontier-AI advantage does not live in describable architecture at all. It lives in tacit, hard-to-replicate craft: post-training judgment, evaluation discipline, data-engineering taste, and a compounding flywheel of proprietary interaction data. The persistent quality gaps between labs with similar model scale are the usual evidence for this view: the differentiator is not the thing you can write down, it is the accumulated know-how and data that you cannot.

Apply that lens here and the patent's own logic turns against the moat case. The invention is, by its own description, a **data-generation engine**. The durable advantage it implies is the **data it produces and the pipeline and people who operate it**, none of which a claim can hold. And data, pipelines, and people are exactly what an acquirer takes in an acqui-hire. A patent on the engine does not fence the fuel.

---

## 5. Did the moat hold? The market already voted

- **Funding.** Adept raised about **$415M total**, including a **$350M Series B in March 2023 at a roughly $1B valuation**, co-led by General Catalyst and Spark Capital, with strategic checks from **Microsoft, Nvidia, Workday Ventures, and Atlassian Ventures**, among others. Several of those strategics were natural acquirers or customers. None of them bought the company.
- **The 2024 outcome.** In **June 2024, Amazon hired the leadership** (CEO David Luan plus co-founders Augustus Odena, Maxwell Nye, Erich Elsen, Kelsey Szot) into its AGI group and took a **non-exclusive license** to Adept's models, agentic data, and web-interaction software. Adept reportedly received about **$25M**, and investors **roughly recouped their principal** with no return. Around 20 employees remained under a new CEO (Zach Brock). An acqui-hire at cost is the textbook signal that the moat was the team, not a defensible product franchise.
- **Further dispersion.** The talent did not consolidate in one place. Co-founder and CTO **Niki Parmar** (a co-inventor of the Transformer) joined **Anthropic** around the end of 2024. In **February 2026, David Luan left Amazon** to start something new, draining the original team a second time.
- **Where the technology actually shipped.** Inside Amazon, the Adept-derived work became **Nova Act**, an agent model and developer toolkit adopted by customers including Hertz, 1Password, and Amazon itself. The product lineage survived; the independent moat did not.

---

## 6. Who owns it now, and why that dilutes the moat further

- **Confirmed:** Amazon holds a **non-exclusive license** to the underlying technology from the 2024 deal. A non-exclusive license means the original owner kept the right to use and to license to others, so Amazon never had exclusivity here.
- **Strongly indicated, not yet primary-verified:** the Adept patent family appears to have been **assigned to Anthropic, PBC in 2025**. This shows up in patent-data aggregators and public commentary and is consistent with the corroborated flow of Adept people into Anthropic, but every authoritative patent source (USPTO, Google Patents, Justia, PubChem) blocked automated retrieval during this review. **Verify directly in the USPTO assignment database (assignment.uspto.gov) before relying on it in a transaction.**

Either way, the structural conclusion is the same and it is the opposite of a moat. If Adept still owns the patents, Amazon practices them non-exclusively and Adept can license to others. If Anthropic now owns them, it owns them **subject to Amazon's pre-existing non-exclusive license**. In both scenarios at least two well-resourced players have rights, and the company that built the technology is a shell. Exclusivity, the thing that makes a patent a moat, is absent.

---

## 7. Paradigm risk: is this even the winning architecture?

The patent is built end to end on **visual, demonstration-based UI automation**: screenshots, pixel-level perception, recorded human demonstrations, and replayed clicks. That bet looked strong in 2023. By 2025 and 2026 the field had started moving the other way.

- **Pixel agents are fragile.** Public research and benchmarks document the core problems: UI grounding is a bottleneck, errors accumulate over long action chains (a single misplaced click can derail a workflow), and an operation that is one API call becomes dozens of brittle GUI steps. Reported reliability sits around 58% on WebArena and about 87% on WebVoyager for visual agents, while tool and API agents clear 80% on harder benchmarks such as GAIA.
- **A major player exited the approach.** Google **shut down Project Mariner on May 4, 2026**, folding visual browsing into Gemini and routing its commerce roadmap through **structured data and API calls rather than screenshot interpretation**. Coverage framed it bluntly as the end of the visual web-agent era, with the industry pivoting to **API-first** agents for reliability and lower compute cost.
- **The research frontier is hybrid.** Newer work (for example, hybrid-action computer-use models) combines GUI actions with programmatic and API actions, treating pure pixel control as a fallback rather than the primary path.

A patent that fences a paradigm the market is leaving is a depreciating asset. The early priority date helps, but the scope that matters most (broad visual record-and-replay automation) is aimed at an approach being designed around at the architecture level, not just the claim level.

---

## 8. Competitive context

Every major lab now ships an agent stack, and they arrived largely in parallel rather than by building on Adept: OpenAI's Operator and Computer-Using Agent, Anthropic's computer use plus the Model Context Protocol and managed agents, Google's Gemini-absorbed agent work, Amazon's Nova Act, and Microsoft's offerings. Independent convergence by this many players is itself evidence that the core ideas were not uniquely held. The strongest current differentiation in the category is coming from tool and API integration, reliability engineering, and distribution, not from owning the visual record-and-replay mechanism this patent describes.

---

## 9. Investor implications

- **As a standalone moat:** weak. The company outcome already settled this question.
- **As a defensive and cross-licensing asset inside a larger lab** (Amazon's license plus apparent Anthropic ownership): moderate and real. The granted US members and the March 2024 priority date have value for freedom-to-operate and cross-licensing in a crowded field where everyone is shipping agents.
- **As an offensive, exclusionary weapon:** limited. The most novel claims are training-process claims with low infringement detectability, and the broad concept is exposed to RPA and computer-use prior art.

**Diligence to-do before any reliance:**
1. Pull the **USPTO assignment record** for the family to confirm the current owner (the Anthropic question).
2. Read the **granted claims and file histories** of US 12,437,238 and US 12,387,036, including examiner rejections and amendments, to see what survived prosecution.
3. Check for **continuations and divisionals still pending** off the kitchen-sink specification; the live scope may differ from what is granted today.
4. Assess whether the **data flywheel and trade secrets** transferred with the team, since that, not the claims, is where any real advantage sat.

---

## Confidence and caveats

- Technical reading of the patent: **high** (primary source, paragraph-level citations).
- Funding and acqui-hire facts: **high** (multiple reputable outlets).
- Anthropic assignment of the patent family: **medium** (consistent secondary sources and corroborated talent flow, but no primary record retrieved; verify at USPTO).
- Paradigm-shift claim: **medium to high** (a dated, concrete shutdown plus benchmark and research evidence).

This memo reads the patent and the public record. It is not legal advice and is not a validity or infringement opinion; a claim chart and an attorney's freedom-to-operate review are the next step if the asset matters to a deal.

---

## Sources

- Patent under review: WO2025199330 A1 (PCT/US2025/020719), provided text; Google Patents listing for [WO2025199330A1](https://patents.google.com/patent/WO2025199330A1/en).
- Granted family members: [US 12,437,238 B1](https://patents.google.com/patent/US12437238B1), [US 12,387,036 B1](https://patents.google.com/patent/US12387036B1), and related listings via [Justia (Adept AI Systems Inc.)](https://patents.justia.com/assignee/adept-ai-systems-inc) and [Justia (Anthropic, PBC)](https://patents.justia.com/assignee/anthropic-pbc).
- Amazon acqui-hire and license: [CNBC](https://www.cnbc.com/2024/06/28/amazon-hires-execs-from-ai-startup-adept-and-licenses-its-technology.html), [GeekWire](https://www.geekwire.com/2024/amazon-hires-founders-from-well-funded-enterprise-ai-startup-adept-to-boost-tech-giants-agi-team/), [TechCrunch](https://techcrunch.com/2024/06/28/amazon-hires-founders-away-from-ai-startup-adept).
- Investors recouped principal: [Semafor](https://www.semafor.com/article/08/02/2024/investors-in-adept-ai-will-be-paid-back-after-amazon-hires-startups-top-talent).
- Adept funding and investor roster: [TechCrunch (Series B, $350M)](https://techcrunch.com/2023/03/15/adept-a-startup-training-ai-to-use-existing-software-and-apis-raises-350m), [Adept press release](https://www.adept.ai/press/press-release-series-b/).
- David Luan leaves Amazon (2026) and Nova Act lineage: [CNBC](https://www.cnbc.com/2026/02/24/head-of-amazons-agi-lab-is-leaving-the-company.html), [GeekWire](https://www.geekwire.com/2026/head-of-amazons-agi-lab-is-leaving-in-latest-exit-from-high-profile-adept-deal/).
- Niki Parmar and other Adept staff to Anthropic: [OfficeChai](https://officechai.com/ai/ctos-of-companies-including-instagram-workday-you-com-and-adept-have-joined-anthropic-as-members-of-technical-staff/).
- Project Mariner shutdown and API-first pivot (May 2026): [Digital Trends](https://www.digitaltrends.com/computing/google-pulls-the-plug-on-project-mariner-the-ai-agent-that-browsed-the-web-like-a-human/), [Android Headlines](https://www.androidheadlines.com/2026/05/google-shuts-down-project-mariner-ai-agent.html).
- Pixel vs API/tool agent reliability and hybrid action: [AIMultiple](https://aimultiple.com/computer-use-agents), [UltraCUA (arXiv 2510.17790)](https://arxiv.org/pdf/2510.17790), [OpenAI Computer-Using Agent](https://openai.com/index/computer-using-agent/).
