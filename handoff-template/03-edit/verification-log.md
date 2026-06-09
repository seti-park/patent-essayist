<!--
  TEMPLATE: handoff/03-edit/verification-log.md
  Produced by: prepublish-verify (independent pre-publish verification stage)
  Schema source: editorial-review/references/feedback-format.md (REUSED severity model
                 + severity->assessment table) + the verify-specific pass enum below.

  This file is structured YAML feedback (NOT auto-fix). The orchestrator reads the
  findings and applies the publish policy: low -> surgical fix / surface;
  medium+ -> revision loop (+1 round) then re-verify.

  REQUIRED per finding: pass / severity / location / finding / recommendation
  OPTIONAL per finding: quote / source_tier / verification_status
  Empty pass MUST still appear, using the "no findings" + scoped_to form.

  pass enum (verify-specific):
    red-team-grounding | red-team-mechanism | red-team-overclaim | red-team-scope
    | red-team-insinuation                          (sub-check A: red-team)
    source-resolution | external-claim-verification (sub-check B: live sources)

  severity enum: critical | high | medium | low
  verification_status enum (sub-check B): verified | partially-verified
                                          | unverifiable | contradicted
  web_access: available | offline   (offline => source-resolution items are warns, non-blocking)
  overall_assessment: pass | revise-recommended | revise-required
    (Yes critical OR Yes high => revise-required; only medium => revise-recommended;
     none => pass. Low findings do not affect assessment.)

  Example content: Tesla rotor / non-magnetic filler patent, investor altitude
  (reviewing essay-final.md). Illustrates the two low findings the real run caught.
-->

# Verification Log

```yaml
verification_id: 691-tesla-rotor-nonmagnetic-filler-investor-verify-1
source_draft: handoff/03-edit/essay-final.md
verify_timestamp: 2026-06-09T04:00:00Z
audience: investor
web_access: available
overall_assessment: pass

findings:
  # ---- sub-check A: red-team ----
  - pass: red-team-grounding
    finding: "no findings"
    scoped_to: "Every load-bearing claim traced to invention-summary / thesis-trace; all grounded."

  - pass: red-team-mechanism
    location: "§3 'stop using steel ... at all'"
    severity: low
    finding: |
      Overbroad negation (precision nit, not a factual break). The patent replaces the
      steel rib/strut MEMBER with a non-magnetic filler; the laminations themselves remain
      steel. "at all" slightly overstates by implying total de-steeling of the holding
      function. A surgical scoping fix; assessment stays pass.
    recommendation: |
      Scope the negation to the replaced member, e.g. "stop using a steel strut for
      the holding job."
    quote: "Tesla's move is to stop using steel for the holding job at all."

  - pass: red-team-overclaim
    finding: "no findings"
    scoped_to: "Body numbers (~15%, square-of-speed) read as industry/physics context; honest no-disclosed-numbers caveat intact."

  - pass: red-team-scope
    finding: "no findings"
    scoped_to: "Rare-earth-free program explicitly fenced in §5 ('this patent is not that program')."

  - pass: red-team-insinuation
    finding: "no findings"
    scoped_to: "Laskaris appears as a neutral credibility fact; no raise-then-disavow."

  # ---- sub-check B: live source-resolution ----
  - pass: source-resolution
    location: "# Sources -> Papers"
    severity: low
    verification_status: verified
    source_tier: 2
    finding: |
      Real paper, but the cited title is truncated.
    recommendation: |
      Correct to the full title: "Influence of Flux Barriers and Permanent Magnet
      Arrangements on Performance of High-Speed Flux-Intensifying IPM Motor" (IEEE, 2023).

  - pass: external-claim-verification
    finding: "no findings"
    scoped_to: |
      ~15% leakage = plausible/adequately hedged (industry estimate); centrifugal force
      proportional to speed^2 verified; Laskaris credentials + patent metadata + the
      separate rare-earth-free program all verified against Tier 1-3 sources.
```
