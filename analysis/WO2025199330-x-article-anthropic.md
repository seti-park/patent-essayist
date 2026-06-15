Anthropic's Recorder: The Adept Patent It Now Owns Is Not a Moat.

Adept built one of the most capable agent stacks of the 2023 era, raised $415M at a $1B valuation, then came apart in 2024. The part worth watching is where its core IP landed. The flagship "recorder" patent, WO2025199330 (granted in the US as US12437238), was assigned to Anthropic in 2025. So Anthropic now owns Adept's recorder. Does that give it a technical moat? Mostly no, and the reasons are worth understanding.

## What Anthropic Now Owns

The recorder is not a model. Its 20 claims describe an intermediary that sits between a user and an app, intercepts the clicks, snapshots the screen state, and turns that human demonstration into agent training data [00372]. The input is the screen before you act; the output is the action. It is a clean way to manufacture demonstrations at scale. But it claims a mechanism, not an advantage.

## Why Owning It Is Not a Moat

Three reasons. First, it is a training-process claim: you usually cannot tell from the outside whether a rival built its data the same way, which makes it hard to enforce. Second, Anthropic's ownership is not exclusive. Amazon took a non-exclusive license to Adept's technology in the 2024 acqui-hire, and that license survives the sale, so Amazon can still practice it. A patent two giants can both use is not a fence. Third, the field converged here in parallel; learning to act from human demonstrations (imitation learning) is decades old, not an Adept invention.

## Where the Value Actually Is

The point of a recorder is the data it produces, and that is where Anthropic's position gets interesting. It did not only buy the patent; it also hired Adept people, including co-founder and CTO Niki Parmar. A lab that already has the models, the compute, and the post-training craft can treat a demonstration-data recipe as an ingredient in a flywheel it already runs. That is a smart, cheap acquisition. It is still not a moat. It feeds the advantage Anthropic already has rather than fencing rivals out.

## The Paradigm Caveat

One more discount. The recorder assumes pixel-level, demonstration-based UI automation, and the market is shifting toward API-first agents for reliability and cost. Google shut down Project Mariner in May 2026 and routed its agents through structured APIs, not screenshots. The same vision-to-action idea thrives in robotics, where there is no API to bypass, but in software it is the approach being designed around.

## The Verdict

For Anthropic, the recorder is a sensible defensive and ingredient asset, not a moat. It is non-exclusive, it protects a mechanism rather than the craft, and its real worth is that Anthropic also got the people who can put it to use. The moat, to the extent one exists, is Anthropic's models and data. The recorder feeds that engine. It does not fence it.

# Sources

- US12437238B1, "Generation of Agentic Trajectories for Training Artificial Intelligence Agents to Automate Multimodal Interface Task Workflows," Adept AI Labs, priority 2024-03-20, granted 2025-10-07, inventors: Shaya Zarkesh, Lina Lukyantseva, Rohan Bavishi, Jiageng (David) Luan, John Qian, Claire Pajot, Fred Bertsch, Erich Elsen, Curtis Hawthorne.
- WO2025199330A1 (PCT/US2025/020719), "Artificial Intelligence Agents for User Interface Task Workflow Automation," Adept AI Labs, priority 2024-03-20, PCT filed 2025-03-20, inventors as in US12437238B1.
- Assignment of the Adept AI Labs patent family to Anthropic, PBC, recorded 2025 (USPTO patent assignment records, per patent-data sources).
- Amazon hires Adept executives and licenses its technology on a non-exclusive basis, CNBC, 2024-06-28.
- Niki Parmar and other Adept staff join Anthropic, OfficeChai, 2025.
- Google shuts down Project Mariner and folds it into Gemini, Android Headlines, 2026-05.
- Musk unveils joint Tesla and xAI project "Macrohard" (Digital Optimus), CNBC, 2026-03-11.
