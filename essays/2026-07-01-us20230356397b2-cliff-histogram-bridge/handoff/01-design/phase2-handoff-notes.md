# Phase 2 Handoff Notes

## (a) Audience reframe decision

Per essay-context.md: audience held between a high-school senior and an early
undergraduate — visual, analogy-driven, "why does this matter" framing over dense
technical exposition. This is a deliberate reframe DOWN from the pipeline's usual default
"technically literate generalist" audience (see e.g. the handoff-template example's Tesla
RCM audience note) — favor concrete, physical language (photon counts, bar charts, rows
scanning a floor) over abstract statistics vocabulary (avoid "statistical distribution,"
"convergence," "median" as load-bearing reader-facing terms outside of direct patent
quotes; translate them into "a bar chart of photon counts across a few rows" and "the bars
line up, then don't" in the connective prose). This is also the series' third and final
article — it is the landing point of a three-part arc (eye works -> eye can be trusted ->
eye becomes robot behavior) and should read as a payoff, not an introduction.

## (b) Citation priority mapping

| Quotable span | Primary section | Role |
|---|---|---|
| `[0005]` / claim 1 (statistical-distribution / convergence claim language) | 3-core-claim | claims anchor, used first — this IS the verbatim callback anchor essay-context.md requires to appear unparaphrased |
| `[0004]` (physically over the edge before detecting) | 2-problem | problem framing |
| `[0035]`, `[0036]` (ROI, first/second/third row, spatial separation) | 3-core-claim, 4-analogy | mechanism support — the row geometry the analogy is built on |
| `[0045]`, `[0046]` (lower row = shorter distance / higher intensity, by fixed geometry) | 4-analogy | the geometric fact that makes "one row suddenly reads farther" mean "the floor is gone there" |
| `[0050]`, `[0051]`, `[0054]`, `[0043]` (quantified ranges: 6cm sensor height, 45cm long range, 30cm medium range, 50x ambient factor) | 3-core-claim | quantitative payoff — concrete numbers ground the mechanism in something a reader can picture as real distances |
| `[0026]`, `[0019]` (speed + path-optimization effect) | 5-meaning-horizon | effect anchor — the "why this matters" payoff |
| `[0027]` (single sensor, four jobs: wall tracking, material recognition, cliff detection, SLAM) | 5-meaning-horizon | bridges into the SLAM horizon gesture without overclaiming |

## (c) Framing trace (rejected candidates)

- Candidate 2 ("two metrics, one convergence" — engineering-puzzle framing) rejected: not
  disqualified on 4-axis or Q7 grounds, but it treats the histogram/multi-zone callback as
  one clever mechanism among several (median distance AND peak intensity AND ambient-rate
  cross-check) rather than the single, explicit, central device essay-context.md's brief
  requires. Phase 2 must NOT let the three-range mechanism's genuine cleverness pull focus
  away from the row-comparison-as-histogram framing in the lead and analogy sections —
  those two metrics are supporting detail under the callback, not co-equal with it.
- Candidate 3 ("one sensor, four jobs" efficiency framing) rejected: failed the Q7 hard
  gate (no clean mapping to either admitted pattern) and was weak on Axis 3/Axis 4. Phase
  2 may still use the `[0027]` "one sensor, four jobs" fact as color (it is in the
  citation-priority table above, §5), but must NOT lead the essay with it or treat it as
  the thesis.

## (d) Traps to avoid

- **MECHANICAL — bare "FIG. 1" / "FIG. 2" tokens (carried from figure-selection.md,
  repeated here because it is load-bearing for gate compliance)**: figures 1 and 2 in
  this patent only exist as lettered sub-figures (1A/1B/1C, 2A/2B/2C/2D). The
  deterministic figure-use gate's regex (`\bfig(?:ure|\.|-)?\s*0*(\d+)\b`) requires a
  word boundary immediately after the digits, so "FIG. 1A" / "FIGS. 1A-1C" and "FIG. 2A" /
  "FIGS. 2A-2D" do NOT register as uses of figure 1 or figure 2 — only a bare "FIG. 1" /
  "FIG. 2" token (no trailing letter) does. **The draft must include at least one bare
  "FIG. 1" token and at least one bare "FIG. 2" token** somewhere in the body prose (e.g.
  "FIG. 1 shows the robot's front-mounted sensor..." or a parenthetical "(FIG. 1)"), in
  addition to whatever lettered captions are used. Omitting this will hard-fail
  `gate_figure_use.py` with two spurious FIGUSE-001 orphan findings even though both
  figures are genuinely, heavily used. (Analogous to a prior run's FIG. 5A-5AD handling —
  see `meta/improvement-proposals/2026-06-11-figure-token-panel-suffix.md`; the gate fix
  is proposed but not yet applied as of this run.)
- **Do not overclaim "first."** "First" is only usable in ST's own qualified phrasing
  (e.g., "first dToF 3D LiDAR all-in-one module in ST's portfolio") — never state an
  unqualified "first." Multi-zone dToF already existed via VL53L5/L8; the actual jump is
  resolution (2,268 vs 64-or-fewer zones) plus flood illumination, not "the first
  multi-zone dToF sensor ever."
- **Never say "STM solves SLAM."** Frame the closing as STM supplying the senses and the
  legs/limbs — SLAM itself stays a horizon this essay opens onto, not a delivered result.
  This is the steelman beat locked in thesis-spine.md's adversarial defense: concede that
  one cliff-detection event, from one sensor, is a narrow trick — then refine into why a
  narrow, reliable trick is exactly the load-bearing primitive a SLAM stack needs
  underneath it. Do not let this concession get lost or skipped.
- **"Cliff" = drop-off / stair edge / curb, not a geological cliff.** Frame around
  robot-vacuum and service-robot floor safety, extending to humanoid foot safety only at
  the close, not throughout.
- **Keep "bridge" and "horizon" visibly distinct.** Do not imply that one depth map, by
  itself, completes SLAM. The secondary patent (US2022-0184815) widens the bridge to
  general navigation in a sentence or short passage — it must not compete with the hero
  for space, and it must not be conflated with the horizon-cluster patents (which get a
  line/clause each and are never expanded into a case).
- **IMU/GNSS-only navigation caution**: if US2019-0033466 or a similar IMU/GNSS-only
  patent appears anywhere in the horizon paragraph as context, it must never be treated
  like the hero or the secondary patent — it is not a depth-bridge patent.
- **This is a standalone essay.** Articles 1 and 2 are not citable sources in this run —
  do not cite them in `# Sources`, and do not presuppose the reader has read them. The
  histogram/multi-zone callback must be reconstructed briefly and concretely (a sentence
  or two) before being used as a callback, framed as something "this series already
  established," not introduced as if brand new and not cited as an external source either.
- **Verbatim anchor discipline.** The verbatim anchor "comparing a statistical
  distribution of the reflected signals received at a plurality of different rows of
  zones" (essay-context.md's required unparaphrased phrase) must appear unparaphrased
  somewhere in the essay — it is available verbatim at `[0005]` and in claim 1 (see
  invention-summary.md Quote anchor table / claim analysis). Do not paraphrase it away
  in the name of the "translate abstract stats language into plain visual language"
  instruction in (a) above — the instruction in (a) is about the CONNECTIVE PROSE around
  quotes, not about mutating the quote itself.
- **Em-dash is banned in essay body** (deliverable voice, Phase 2/3 concern) — patent
  verbatim quotes keep their em-dashes if present (none of the selected quote anchors in
  this bundle contain an em-dash, so this is a low-risk trap for this specific run, but
  stated for completeness).
- **Do not present the 2,268-zone figure as if it were a cover glass or wavelength
  spec claim** — the "Pending confirmation" facts (940nm, package dimensions, power draw,
  etc.) are explicitly excluded from fact-check-log.md and must not be asserted as bare
  fact anywhere in the essay.

## (e) Open questions for Phase 2 (awaiting SETI)

- Title pattern: the locked spine's technical-impossibility hook and the "bridge" framing
  both admit a few title shapes (a question form echoing "why doesn't a robot vacuum fall
  down the stairs," or a declarative "the same histogram that..." form). Default:
  question-form title, since the Q7 hook itself is phrased as the reader's own question —
  SETI/Phase 2 may override at compose time.
- Whether to name the specific quantitative ranges (45cm / 30cm / 6cm sensor height) in
  the main body prose or push them to a caption under FIG. 3 — both are supported by the
  citation-priority mapping above. Default: at least the 6cm sensor-height and one of the
  30/45cm range figures in body prose (concrete numbers support the "visual, why-does-this
  -matter" audience framing per (a)), with the other range figure available for a caption.
- How much weight to give the two independent metrics (peak intensity vs. median
  distance, FIGS. 5-6) inside the 3-core-claim section without letting them compete with
  the single histogram-callback framing (see rejected-Candidate-2 trap in (c)) — left to
  Phase 2's judgment; both are available in the citation-priority table if needed.
