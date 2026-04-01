# Cross-Document Pull Bottleneck Analysis

_Last updated: 2026-03-31. This is the focused analysis note for the main unresolved Phase 1 bottleneck._

---

## Executive Summary

The current blocker is **not** that the graph lacks useful signal. It is also no longer accurate to say the graph is simply stuck at the old `115` plateau.

Probe 014 proved that native cheap-fetch recall exists and stays cheap.

Probe 018 then proved that the old plateau was partly a scorer-lens problem:
- a post-change control replay still held `cross-document pull = 115`
- the origin-aware cross-document scorer v1 lifted that same footing to `234`
- pair cost stayed flat at `62896`

Probe 022-033 then proved that the old cross-document threshold gate was also much too strict:
- on the same fixed pair budget, softer cross-document thresholds climbed far past the old plateau
- the graph could match and exceed the old Probe 011 wide-window pull count without pair growth
- but a softer gate is not automatically a safe gate; very low thresholds eventually admit shakier fragment-heavy winners

The next diagnostic pass therefore became sharper still:
- the missed cross-document pairs were **not** mostly hovering just below threshold
- the losers were dominated by a different interaction mix than the winners
- and a single generic scorer lens was part of why recovered cross-document candidates kept losing

In plain terms:
- if the comparison window stays small, many good long-range pairs are never scored
- if the comparison window gets widened too far, pair counts explode
- current targeted recall works mechanically, but still does not recover enough of the wide-window gain
- current native FTS fallback works mechanically, but needed a better cross-document scoring lens before recovered candidates could convert
- origin-aware scoring materially improves conversion
- and threshold control on that branch shows the wide-window continent can be reached at fixed pair cost
- the new bottleneck is now the trust boundary: where to place the cross-document gate so the recovered bridge layer stays useful rather than fragment-heavy

So the project is now fighting a **long-range recall-and-conversion problem under cost constraints**, not a vague “semantic weakness” problem.

---

## The Actual Issue

During ingest, each new hunk is compared against:
- a recent sliding buffer
- plus any targeted long-range candidates surfaced by the current recall path

If a useful cross-document target is too far back in the ingest stream and is **not** explicitly pulled into comparison, then:
- no pair is scored
- no edge is created
- no cross-document pull is recorded

This means the graph can contain enough information to support a good long-range relation in theory, while still failing to express that relation in practice because the pair was never evaluated.

---

## Why This Is A Problem

This bottleneck matters for four reasons:

1. **Graph quality**
- the graph under-represents real long-range relationships
- index-to-target, section-to-section, and cross-document evidence stays artificially weak

2. **Bag quality**
- the bag can only surface evidence that actually exists in the graph or local retrieval neighborhood
- weaker cross-document pull means weaker evidence diversity

3. **Probe interpretation**
- without fixing recall, we risk misreading the system as signal-poor when it is actually comparison-poor

4. **Phase 2 risk**
- an FFN trained too early would learn from incomplete interaction data
- that would teach around Phase 1 scaffold defects instead of learning a trustworthy relation substrate

---

## What The Probes Have Proven

## Probe 011 — Wide Window Recovery

Key result:
- `cross-document pull = 1175`

Interpretation:
- the signal is there
- wider comparison recovers it

Cost:
- `training pairs total = 234900`

Meaning:
- brute-force recall works
- but the cost shape is too expensive to promote as the stable baseline

## Probe 012 — Targeted Candidate Recall v1

Key result:
- `cross-document pull = 115`

Interpretation:
- targeted long-range comparison works mechanically
- but recall v1 is far too weak to recover the Probe 011 gain

## Probe 013 — Anchor Registry v1

Key results:
- `relations = 17428`
- `cross-document pull = 115`
- `training pairs total = 62583`

Interpretation:
- anchor ranking and common-term suppression made the long-range path more selective
- but anchor-only recall is still too narrow
- it did not move the `115` plateau

## Probe 014 — Native FTS Cheap-Fetch Fallback v1

Key results:
- `relations = 17457`
- `cross-document pull = 115`
- `training pairs total = 63155`
- `above-threshold training pairs = 16028`
- `fts_fallback_fires = 1275`
- `fts_raw_hits = 975`
- `fts_selected = 572`
- `fts_selected_cross_doc = 548`

Interpretation:
- the native FTS lane is real and active
- it stayed cheap relative to Probe 011
- it recovered and selected many cross-document fallback candidates
- but none of that changed the headline `115` cross-document pull plateau
- so the bottleneck is no longer only "missing cheap fetch"
- the bottleneck is now also "why cheap-fetch v1 is not converting into scored pull lift"

## Probe 017 — Post-Change Control Replay

Key results:
- `relations = 17457`
- `cross-document pull = 115`
- `training pairs total = 62896`

Interpretation:
- the scorer refactor itself did not accidentally move the headline metric
- the old plateau was still reproducible on the same Python-reference list/index footing

## Probe 018 — Origin-Aware Cross-Document Scorer v1

Key results:
- `relations = 17592`
- `cross-document pull = 234`
- `training pairs total = 62896`
- `above-threshold training pairs = 16163`

Conversion shift:
- control cross-document winners:
  - `grammatical_dominant = 106`
  - `structural_bridge = 2`
  - `multi_surface = 7`
- origin-aware winners:
  - `structural_bridge = 153`
  - `multi_surface = 69`
  - `grammatical_dominant = 12`

Interpretation:
- this tranche cleared the Phase 1 acceptance bar cleanly
- a single generic scorer lens was part of the old plateau
- cross-document pairs should not be judged exactly like same-document pairs
- origin-aware static branching is now a real Phase 1 tool, not just a hypothesis
- but the wide-window gap is still large (`234` vs Probe 011 `1175`)

## Probe 019 / 020 / 021 — Origin-Aware Ablation Gradient

Key results:
- fractions only:
  - `cross-document pull = 150`
- fractions + threshold scaling:
  - `cross-document pull = 228`
- fractions + shared-anchor bonus:
  - `cross-document pull = 155`

Interpretation:
- the alternate cross-document lens matters
- cross-document threshold scaling is the strongest near-term lever
- the current shared-anchor seam is real but still weak on this footing

## Probe 022-033 — Cross-Document Threshold Sweep

Shared footing:
- same fixed pair budget: `62896`
- same origin-aware branch and current partial shared-anchor seam
- only the cross-document threshold scale moved

Representative ladder:
- `0.95 -> 206`
- `0.90 -> 255`
- `0.85 -> 368`
- `0.80 -> 588`
- `0.75 -> 912`
- `0.70 -> 1406`
- `0.65 -> 1975`
- `0.60 -> 2480`
- `0.50 -> 3876`
- `0.40 -> 6312`
- `0.30 -> 8458`

Interpretation:
- the old cross-document threshold was far too strict
- softer thresholds kept the winner field strongly `structural_bridge` / `statistical_echo` much deeper than expected
- the graph can now match and exceed the old Probe 011 wide-window pull count without pair growth
- but the sweep also revealed a trust boundary:
  - `0.50`–`0.65` looks like the most promising band so far
  - `0.40` is the first warning zone where weakest winners start looking shaky
  - `0.30` is too permissive and admits fragment-heavy bridge fabric

## What This Means

Together, these probes prove:
- the system has real long-range signal
- the current default comparison scope misses too much of it
- selective recall is possible
- current targeted recall is not yet broad enough by itself
- cheap-fetch v1, while cheap, needed a better scorer lens before conversion improved
- origin-aware scoring can convert more of the recovered breadth into actual pull improvement
- the old cross-document threshold gate was suppressing a very large structural/statistical layer
- current partial shared-anchor support is still not the main lever compared with threshold behavior
- the current problem is no longer raw inability to recover long-range pull; it is choosing the trustworthy control band for that recovery

---

## What Is Not The Main Problem

These things are important, but they are **not** the primary blocker right now:

- lack of any semantic lane at all
  - deterministic semantics are running again
  - and currently outperform the first traditional sentence embedder we tested

- lack of explicit signal entirely
  - list/index work proved a real explicit signal lane exists

- lack of a usable evidence surface
  - the rudimentary bag already works

- lack of a builder-side neighborhood lens
  - the anisotropic blur experiment exists
  - but it is diagnostic, not the missing retrieval fix

So the main issue is narrower and more concrete than it might appear:
the graph needs better **cheap long-range candidate recall plus cross-document-aware conversion that can recover more of the wide-window gain without pair explosion**.

---

## The Current Limiting Factors

## 1. Sliding-window clipping

The default comparison scope is still too local.

Effect:
- many distant but relevant hunks are never compared

## 2. Anchor-only recall is too narrow

The current registry mainly exploits:
- heading-style anchors
- normalized list/index targets
- related explicit reference signals

That helps, but it does not cast a broad enough recall net for all useful long-range pairs.

## 3. Cheap-fetch v1 is not converting

Probe 014 changed the diagnosis.

Before Probe 014, the likely next fix was:
- add a deterministic cheap-fetch fallback

After Probe 014, we know:
- the fallback can be added natively
- it can remain Phase-1-compatible
- it can recover cross-document candidates
- it can stay far below Probe 011 cost
- and it still may fail to improve the graph if those recovered candidates are too weak, too noisy, too broad, or badly timed

The sharpest warning signs from Probe 014 were:
- `fts_fallback_fires = 1275`
  - it fired for every hunk on this footing
- `fts_selected_cross_doc = 548`
  - it really did recover cross-document candidates
- `cross-document pull = 115`
  - the headline pull metric did not move at all

That strongly suggests at least one of these is true:
- the fallback trigger rule is too broad
- the deterministic FTS query lexicalization is too weak or too noisy
- the fallback ranking is not surfacing the right distant targets
- the Bootstrap Nucleus is rejecting most recovered pairs for stable reasons

## 4. Conversion diagnostics: most losers are not near-threshold

The new builder-side conversion reports are:
- `_docs/_analysis/reference_probe_015_contradiction_control/graph_probe_report_015_conversion.json`
- `_docs/_analysis/reference_probe_016_fts_origin_cap1/graph_probe_report_016_conversion.json`

These reports answer the next important question:

Are the missed cross-document candidates failing by a hair, or are they being soundly out-competed?

The answer on the current control footing is:
- `cross_document_winners = 147`
- `cross_document_losers = 12313`
- `edge_threshold = 0.24`
- only `17` cross-document losers are within `20%` of threshold
- mean loser margin to threshold is `0.1522`
- median loser margin to threshold is `0.1545`

That is a very important result.

It means the current plateau is **not** mainly a "lower the threshold a little" problem. Most missed cross-document pairs are far enough below threshold that a small threshold relaxation would not create the phase shift we want.

The interaction mix is also sharply split:
- cross-document winners are mostly `grammatical_dominant` (`106`) plus a smaller `statistical_echo` lane (`32`)
- cross-document losers are overwhelmingly `structural_bridge` (`8992`), then `statistical_echo` (`1870`) and `multi_surface` (`1440`)

So the current scorer is doing something very specific:
- it is willing to let a narrow grammar-heavy lane win across documents
- while most structurally recovered long-range candidates still fail to accumulate enough support to cross threshold

That makes the bottleneck much more concrete than before:
- we are not just "missing distant candidates"
- we are also under-converting structurally plausible long-range candidates once they are found

## 5. FTS per-origin cap did not change the conversion geometry

Probe 016 plus its conversion report sharpened a second point:
- `cross-document pull` stayed at `115`
- `fts_selected_cross_doc` dropped from `548` to `179`
- the loser-margin picture stayed almost unchanged
- the winner/loser interaction split also stayed almost unchanged

Meaning:
- the FTS fallback lane was successfully de-monopolized
- but one-origin crowding was not the hidden cause of the plateau
- the real problem remains downstream conversion

## 6. One generic scorer lens was part of the plateau

Probe 018 proved a specific point that earlier probes only implied:
- candidate selection already knew which pairs were cross-document
- the old Bootstrap Nucleus still scored all pairs through one generic static lens
- letting cross-document pairs use a different static profile lifted the headline pull metric from `115` to `234` at the same pair cost

That means the prior bottleneck was not only:
- "find more distant candidates cheaply"

It was also:
- "stop asking cross-document pairs to behave like same-document pairs"

## 7. Pair explosion under brute force

Wide-window recovery proves the signal exists, but the pair count becomes too expensive.

That means the stable solution must improve recall **without** approaching Probe 011 cost behavior.

## 8. Dense local hubs can hijack softer field views

The blur experiment showed that dense local neighborhoods, especially index-heavy ones, can dominate soft spread.

Meaning:
- softer field lenses can be informative
- but they are not yet safe replacements for candidate selection

## 9. Very soft cross-document gates eventually admit shakier bridge fabric

The threshold sweep changed the bottleneck read one more time.

At first, softer thresholds looked almost suspiciously good because:
- pair cost stayed fixed
- grammar-heavy winners did not come roaring back
- the winner field stayed mostly `structural_bridge` / `statistical_echo`

But weakest-winner inspection finally found the warning zone:
- around `0.50`, weakest admitted winners still looked borderline-but-defensible
- around `0.40`, weakest winners began to look noticeably shakier
- at `0.30`, fragment-heavy and abstract-neighborhood matches became too easy to admit

That means the next Phase 1 job is not "keep lowering the gate until the metric gets huge."
It is:
- locate the trustworthy band
- inspect weakest winners there
- choose a default that recovers the latent bridge layer without drifting into fragment noise

---

## The Best Current Read

The problem is now best described like this:

The system has crossed the threshold where much better cross-document relations are possible, and it now has proof that origin-aware scoring plus cross-document threshold control can recover that layer at fixed pair cost. The remaining problem is to choose the trustworthy operating band for that recovery and avoid drifting into fragment-heavy permissiveness.

That is why:
- small windows underperform
- large windows overpay
- anchor-only recall plateaus
- cheap-fetch plus a one-lens scorer plateaus
- origin-aware scoring improves conversion materially
- threshold sweeps expose a very large latent bridge layer
- and weakest-winner inspection becomes the new guardrail for choosing a default

---

## Likely Next Move

The next likely experiment is **not** "add FTS fallback." That has now been done.

The next likely experiment is:

- keep the current sliding window
- keep the heavy scorer as the final gate
- keep the anchor-registry path
- keep the native SQLite FTS fallback path
- keep the new conversion reports in the loop
- keep the origin-aware cross-document scorer branch in play
- keep the stronger alternate cross-document fractions
- fine-sweep the `0.50`–`0.65` range and inspect weakest admitted winners there
- do not promote `0.40` or lower as a default unless stronger quality evidence appears
- keep shared-anchor work secondary until the threshold/fraction line stops paying off
- decide whether the current partial outbound-reference seam is enough, or whether a later shared-target neighborhood tranche is justified only after that fine sweep stalls
- keep reusing the current SQLite / FTS infrastructure instead of inventing a large new subsystem

This is the most responsible next step because it targets the actual bottleneck while keeping the Phase 1 scaffold stable.

---

## What Not To Confuse With The Fix

Do not treat these as the immediate solution:

- FFN / Phase 2 work
- runtime anisotropic blur integration
- broad UI work
- giant ontology rewrite
- broad app-platform integration

Those may matter later, but they do not directly solve the current comparison-recall bottleneck.

---

## Success Criteria For The Next Recall Experiment

The next recall-focused tranche should be judged against these realities:

1. **The default operating band must stay above the old `234` accepted profile and remain comfortably beyond the old `115` plateau**
- otherwise the new scorer control surface is not buying enough real progress

2. **Pair cost must stay fixed or clearly below Probe 011**
- otherwise we are just recreating the wide-window brute-force path

3. **Cheap-fetch should not fire blindly on every hunk**
- otherwise the fallback is too broad to be interpretable

4. **Recovered cross-document winners must remain structurally plausible under weakest-winner inspection**
- Probe 022-033 proved the metric can become huge
- the next tranche must choose a trustworthy band, not just a larger number

5. **The bag should become more source-diverse and evidentially useful**
- especially on the Python reference bottleneck case

6. **The fix should remain Phase-1-compatible**
- deterministic
- inspectable
- measurable
- no major architecture rewrite

---

## Read This With

- [`WE_ARE_HERE_NOW.md`](C:\Users\jacob\Documents\_AppDesign\_LivePROJECTS\BDNeuralTranslationSUITE\_docs\WE_ARE_HERE_NOW.md)
- [`GRAPH_PROBES.md`](C:\Users\jacob\Documents\_AppDesign\_LivePROJECTS\BDNeuralTranslationSUITE\_docs\GRAPH_PROBES.md)
- [`QUERY_EXPERIMENTS.md`](C:\Users\jacob\Documents\_AppDesign\_LivePROJECTS\BDNeuralTranslationSUITE\_docs\QUERY_EXPERIMENTS.md)

If a new conversation understands this file clearly, it should be able to discuss the current bottleneck accurately without immediately drifting into Phase 2 or abstract redesign.
