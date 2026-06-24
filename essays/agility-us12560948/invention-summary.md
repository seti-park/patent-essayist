# Invention summary — US 12,560,948 B2

Phase-1 grounding for the investor moat article. Holds the verbatim citation-anchor set
(the `[xxxx]` tokens the article is allowed to cite) and the claim-scope map that keeps the
moat verdict honest. Voice-off: facts and claim language only.

## Bibliographic facts

- **Number / kind:** US 12,560,948 B2 (granted patent).
- **Title:** "Escalating hazard-response of dynamically stable mobile robot in a collaborative
  environment and related technology."
- **Assignee / applicant:** Agility Robotics, Inc.
- **Priority:** 2024-03-01 (provisional 63/560,583). **Filed:** 2025-02-28 (appl. 19/067,681).
  **Granted:** 2026-02-24. Published as application US 2025/0278092 A1 on 2025-09-04.
- **Family:** Family ID 95065656. Co-pending US 19/067,693 and PCT/US25/17985 filed the same
  day (2025-02-28).
- **Claims:** 20 total, all method claims. 1 independent (claim 1).
- **Classification:** CPC G05D1/633, G05D1/495, G05D1/498, B62D57/032, G05D2101/15, G05D2109/12.
- **Inventors (12):** Kevin Reese, Andrew Abate, Tianyao Chen, Jay Jasper, Ezm Masoud,
  Brian Kirby, Melonee Wise, Prasanna Velagapudi, Ryan Domres, Todd Lewis,
  Matteo Parigi Polverini, Yves Georgy Daoud.
- **Examiner:** Nga X. Nguyen.

## Citation-anchor set (verbatim spans)

Each anchor is a published-paragraph identifier resolving to a verbatim span. The article may
cite only these. Claim language is cited by claim number, not by `[xxxx]`.

- `[0002]` — "Some analysts forecast a shortage of a million or more workers to staff
  order-fulfillment centers within the next ten to fifteen years."
- `[0010]` — "bipedal robots are dynamically stable in most, if not all cases. Such robots are
  always falling to some degree during normal operation." / "If a dynamically stable robot
  loses power or otherwise becomes disabled, it collapses."
- `[0011]` — "close encounters between humans and dynamically stable robots are potentially
  hazardous. Ironically, this includes close encounters associated with accessing and
  activating a disabling feature on such a robot."
- `[0013]` — "segregation strategies for hazard mitigation greatly reduce the productive
  potential of dynamically stable robots."
- `[0014]` — "a variable (e.g., escalating) hazard response by a mobile robot." / "features
  that increasingly prioritize hazard reduction over efficiency in response to information
  indicating an increasing level of risk to a human in the environment."
- `[0015]` — "the word 'bipedal' as used herein may be replaced with 'mobile' to encompass
  non-bipedal counterparts within the present technology unless the context clearly indicates
  otherwise."
- `[0024]` — "An example of this first model is YOLOV8 (Ultralytics Inc.)." / "An example of
  this second model is AMAZON REKOGNITION (Amazon Web Services, Inc.)."
- `[0027]` — "determining clearance information about a portion of the environment around the
  mobile robot."
- `[0028]` — "reconfiguring the mobile robot includes lowering the center-of-gravity of the
  mobile robot."
- `[0029]` — "Reconfiguring the mobile robot can reduce a fault-state fall extent of the mobile
  robot (e.g., by at least 30%, by at least 50%, etc.)."
- `[0031]` — "While in a safe operating stop, the mobile robot may halt all movement without
  completely shutting down." / recovery "may require a special input, such as an affirmative
  input from a human operator."
- `[0032]` — "decelerating the mobile robot, reconfiguring the mobile robot, and causing a safe
  operating stop of the mobile robot cause increasingly greater losses of efficiency while
  providing increasingly greater risk reduction."
- `[0033]` — "a reconfiguration of the mobile robot may increase rather than decrease the risk
  to the human." (e.g., at a blind corner or when the human is running)
- `[0041]` — "Stops in accordance with at least some embodiments of the present technology are
  protective and controlled forms of Category-1 and Category-2 stops."
- `[0046]` — reconfiguration lowers the center-of-gravity "in several phases."
- `[0047]` — after reconfiguration "the mobile robot may tend to collapse in a predictable
  manner and into a compact form, thereby reducing or eliminating a safety hazard to nearby
  humans."

## Independent claim 1 (verbatim)

> A method comprising: determining, by a computer system operably associated with a mobile
> robot in an environment, first hazard information about a human in the environment at a first
> time, wherein the first hazard information indicates a first level of risk of collision
> between the mobile robot and the human; decelerating the mobile robot based at least partially
> on the first hazard information; determining, by the computer system, second hazard
> information about the human at a second time after the first time, wherein the second hazard
> information indicates a second level of risk of collision between the mobile robot and the
> human, and wherein the second level of risk is greater than the first level of risk;
> determining, by the computer system, clearance information about a portion of the environment
> around the mobile robot after decelerating the mobile robot; and reconfiguring the mobile
> robot based at least partially on the second hazard information and the clearance information,
> wherein reconfiguring the mobile robot includes lowering a center-of-gravity of the mobile
> robot.

## Claim scope map (locked / open / pinned)

The discipline that keeps the moat verdict honest: what claim 1 actually requires versus what
the description and dependents merely offer. Never attribute an optional embodiment to the
independent claim.

| Layer | Content |
|---|---|
| **Locked (claim 1 requires)** | A time-ordered sequence with rising risk: first hazard info at a first time (first risk level); deceleration; second hazard info at a later time whose risk level is greater than the first; clearance information about the surroundings determined after decelerating; and a reconfiguration driven by both the second hazard info and the clearance info, where the reconfiguration lowers the robot's center-of-gravity. |
| **Open (description / dependents add, claim 1 does not require)** | Safe operating stop with manual release (claim 2, `[0031]`); specific triggers such as proximity (3), trajectory (5), speed (6), human state (8); machine-learning hazard model incl. YOLOv8 / Rekognition (7, 8, `[0024]`); foot-placement during deceleration (9); knee bend (10), torso tilt (11), crouch (12), kneel (14), standing-to-non-standing (19); selecting a reconfiguration type by hazard (17) or clearance (18); placing a carried payload on the ground (20). |
| **Pinned (approximate point limitations, not floors or ceilings)** | Fault-state fall-extent reduction "by at least 30%, by at least 50%" (`[0029]`); only claim 13 pins "at least 50%." Decision loops cycle "at a suitable interval (e.g., 1 Hz, 10 Hz)." These are example values; do not describe them as guaranteed bounds the independent claim states. |

## Scope-breadth note

`[0015]` lets "bipedal" read as "mobile," extending the method to one-arm, multi-arm,
non-legged, and wheeled dynamically stable robots. The independent claim is not limited to
biped form. This widens coverage but is a description-level construction aid, not an extra
claim limitation.
