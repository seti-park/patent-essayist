# Revision notes — intel-us20250266395

> Post-acceptance self-audit deltas. Each `## delta` block: one edit, `class` (attribution-table
> pattern_tag), `round`, `origin`, `before`, `after`, `rationale` — each on ONE line.
> `pipeline-retro` normalizes these into `meta/findings-ledger.jsonl` under `origin: self-post-accept`.

## delta
class: fact-introduced-beyond-spans
round: self-post-accept-1
origin: self-post-accept
finding_id: SKEP-01
before: "This is the most concrete piece of after-EMIB-T assembly thinking on the public record."
after: "What Intel put on file is the specific after-EMIB-T move: the assembly order inverted, the whole cluster test-gated before a board is committed."
rationale: overreach (medium) — the superlative asserts a survey of the entire public record no source supports; NARROW (not hedge) to this filing's specific move (inverted, test-gated flow), energy and firmness preserved, no safe-harbor qualifier added.

## delta
class: fact-introduced-beyond-spans
round: self-post-accept-1
origin: self-post-accept
finding_id: SKEP-03
before: "one of the places where the glass roadmap and the bridge roadmap touch."
after: "one of the places where the glass roadmap and the bridge work on file touch."
rationale: filed-not-roadmap (low) — "the bridge roadmap" leans toward productization the essay elsewhere denies; narrowed to non-scheduling "the bridge work on file." SKEP-03 applied.

## delta
class: reader-engagement-break
round: self-post-accept-1
origin: self-post-accept
finding_id: goal-5-4a
before: "§4 glass paragraph stacks ~six concepts (glass bridge, glass frame, TGVs, Example 17, Intel Sept-2023 glass-core announcement) off the order-of-operations spine; §5 later concedes glass is claimed narrowly, so the reader invests in a thread the essay de-emphasizes."
after: "LEFT — no clean light-touch fix available."
rationale: CONSIDERED-NOT-APPLIED (structurally blocked). The paragraph already opens with an explicit side-thread signal ("There is a quiet glass thread here"). A stronger forward-reference signal was drafted ("the claims keep the glass narrow, as the next section shows") but could not land cleanly: the paragraph already sits at the gate's 7-sentence ceiling (gate_typography/structure counts "FIG. 6A" as a phantom sentence break), so adding a sentence trips STRUCT-001 at 8; folding the clause into the existing sentence pushes it past the 35-word LONGSENT-001 threshold (measured 47). Per the goal-5 light-touch constraint (no change to fact/number/anchor/quote and no new warn), and the contract "if a clean trim isn't possible, leave it and say so", the extra signal was reverted; the existing "quiet glass thread" frame carries the side-thread cue. No grounded fact dropped.

## delta
class: fact-introduced-beyond-spans
round: self-post-accept-1
origin: self-post-accept
finding_id: SKEP-02
before: "hangs off the no-cavity inverted package of claim 16, not off the cavity packages described above. The parallel Example paragraph is written broader [0138]."
after: "hangs off the no-cavity inverted package of claim 16, not off the cavity packages described above, going by the published claims themselves (Google Patents). The parallel Example paragraph is written broader [0138]."
rationale: grounding-label (low) — the claim-17-hangs-off-claim-16 dependency read as asserted from the (claimless) patent.md snapshot; attributed to the published claims / Google Patents, the same conservative sourcing §5 already uses for claim scope and application status. No em-dash used (gate_emdash clean); sentence count unchanged.

## delta
class: reader-engagement-break
round: self-post-accept-1
origin: self-post-accept
finding_id: goal-5-4b
before: "§3 the two Example-21 claim-language blockquotes (q-0142-1 naming quote; q-0142-2 test-and-commit quote), a cold reader flagged as a raw claim-language wall."
after: "LEFT UNCHANGED."
rationale: CONSIDERED-NOT-APPLIED. The two blockquotes are already separated by a momentum-carrying transition ("Then comes the half Intel's shipped bridge flow does not contain, the test-and-commit order:"), each with its own lead-in. The thesis-critical quote (q-0142-2, the test-and-commit order) must remain raw and verbatim. The only structural fix — dropping the first (naming) blockquote q-0142-1 — would alter a protected verbatim blockquote, which the goal-5 light-touch constraint forbids. Per the contract ("if a clean trim isn't possible, leave it and say so"), left in place.

## delta
class: fact-introduced-beyond-spans
round: self-post-accept-1
origin: self-post-accept
finding_id: F-IMP-01
before: "impatient reader requested an added stock-price / stock-impact clause."
after: "REJECTED — not applied."
rationale: A stock-impact clause would overreach the filed-not-roadmap discipline the essay holds throughout (pending application, no granted claim, no scheduled product). The essay's IP-signal altitude is deliberate; adding market-move language would introduce a fact beyond the Quotable spans and fact-check-log and re-inflate the exact overreach the firm-but-not-hype verdict guards against. Verdict left firm, no re-hedge.

## delta — self-audit round 2 (confirmation)

self-audit: no unresolved findings

- Round 2 applied nothing at medium+. Skeptical-pro reader R2: 0 findings (narrowed lead confirmed clean, no regression on SKEP-01/02/03). Cold reader R2: read to the end (round-1 bail resolved); repeat-to-a-friend matches the reader_sentence.
- Carried goal-5 signal (NOT auto-applied — cold-reader stop-point outside the lead, uncorroborated by a rubric reader this round): §4 "Power Comes Up Through the Floor" part-number / FIG-reference density (526, 536, 701, 872, 882). Routed to Phase 3.7 prose-polish as a plain-language smoothing priority (surface jurisdiction; no grounded fact or [0035] verbatim quote may be dropped).
