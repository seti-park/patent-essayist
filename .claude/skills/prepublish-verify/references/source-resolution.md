# Source resolution (live external verification)

Sub-check B of `prepublish-verify`. This is the **authoritative live external check**, run once
at the publication threshold (the role `external-fact-verification.md` line 47 reserves for this
point). It is **not** a re-run of editorial Pass-3: Pass-3 now only *flags* external claims as
candidates; here you actually resolve them against the web.

## Single source of truth (do not redefine)

The **5-tier source authority hierarchy** and the **verification-status vocabulary**
(`verified` / `partially-verified` / `unverifiable` / `contradicted`) live in
`editorial-review/references/external-fact-verification.md`. Read them there and apply them —
do not restate or fork the tables here.

## What to resolve

1. **Every external (non-patent) claim in the body** — named-entity attributes (credentials,
   company history), industry statistics / percentages / counts, prior-publication references,
   third-party technology claims, dates and events. (Patent-internal `[xxxx]` attribution is the
   anchors gate's + editorial Pass-3's job, not this one.)
2. **Every `# Sources` entry** — does it resolve to a real, reachable item with the title /
   author / venue / date as written?

## Procedure (per item)

1. **Extract** the specific assertion (entity + attribute, statistic + value, date + event) or
   the Sources citation.
2. **Web-search / fetch** a current source. Source rot (dead URL, retracted claim, updated page)
   and citation drift (truncated/wrong title, wrong venue/year) are the failure patterns this
   stage catches.
3. **Assign the tier** of the best source found (per the SoT hierarchy).
4. **Set the verification status** (per the SoT table) and a severity:
   - `contradicted` → **high** (fix required before publication).
   - `unverifiable` with a **quantitative** body claim resting on it → **high** (Tier-5-only +
     number rule from the SoT).
   - `partially-verified` (e.g. Tier 3-4 only, or Tier 1-2 but stale) → **medium** (hedge or
     re-anchor).
   - Citation **drift** that does not change the underlying fact (truncated title, wrong year on
     a real paper) → **low** (correct the citation).
   - `verified` → no finding (emit the pass `"no findings"` when the whole layer is clean).
5. **Recommend** the concrete fix: soften / add hedge / re-anchor to a Tier 1-2 source / correct
   the citation title / remove an unsupported number.

## No-web fallback

If web access is unavailable: set `web_access: offline` in the log, mark every item
`unverifiable — no web` as a **warn** (not fail), and do **not** block publication on this layer
(soft mode). Note the gap explicitly so a human can run the live check later. Switch to hard
(halt) only when the run explicitly demands web-confirmed sourcing.

## Output

`verification-log` findings under passes `source-resolution` (Sources-entry resolution) and
`external-claim-verification` (body-claim resolution), each carrying `source_tier` and
`verification_status` in addition to the standard fields. Clean layer → emit the pass with
`finding: "no findings"` and `scoped_to:`.
