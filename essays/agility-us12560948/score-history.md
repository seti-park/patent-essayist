# Score history — US 12,560,948 B2 investor moat article

Compose↔Edit inner loop. Threshold `pass`, posture `measured`, max 4 iterations. Two layers per
round: deterministic gates (hard) + editorial `overall_assessment` (severity model). A round
passes only when gates are all green AND the editorial assessment meets the threshold AND the
grounding/goal-2 hard-gates are clear.

| Iter | Deterministic gates | Editorial assessment | Round result | Driver |
|---|---|---|---|---|
| 1 | PASS (0 fail) | revise-required | FAIL | 3 high: 8-sentence paragraphs (Pass 2C) the gate's `>8` threshold let through |
| 2 | PASS (0 fail) | revise-required | FAIL | 1 high regression: iter-1's grounding fix created a new 8-sentence paragraph; + 1 medium mobile wall |
| 3 | PASS (0 fail) | pass | **PASS** | all passes clean; loop terminates |

Terminated at iteration 3 (within the 4-iteration cap), result PASS.

## Notes

- The deterministic gates were green from the start; the loop's work was entirely in the
  qualitative editorial layer. The recurring catch was the same class both times: an essay
  paragraph at exactly 8 sentences, which `gate_structure` (threshold strictly `> 8`) cannot
  see but editorial Pass 2C (`>= 8` is high) does. This is the gate/editor division working as
  designed, and a candidate the meta-loop could note (a `>= 8` warn in `gate_structure` would
  have surfaced both instances mechanically).
- No grounding hard-gate breach at any iteration: every pass-3 finding was `medium` or `low`,
  never `high`/`critical`, and `gate_anchors` passed each round.
- Final artifacts: `essay-final.md` (draft), `edit-log.md` (3 reviews), `gate-result.json` /
  `gate-result.txt` (final gates), `invention-summary.md` (anchor set + claim-scope map).
