# Cross-Document Pull Bottleneck Analysis

_Last updated: 2026-03-30. This is the focused analysis note for the main unresolved Phase 1 bottleneck._

---

## Executive Summary

The current blocker is **not** that the graph lacks useful signal. The blocker is now more specific than that.

The Emitter needed a cheap, high-recall way to bring the right distant candidates into comparison.

Probe 014 added that native cheap-fetch lane.

But cheap-fetch v1 still did **not** improve the headline cross-document pull metric.

The next diagnostic pass made the picture sharper still:
- the missed cross-document pairs are **not** mostly hovering just below threshold
- and the losers are dominated by a different interaction mix than the winners

In plain terms:
- if the comparison window stays small, many good long-range pairs are never scored
- if the comparison window gets widened too far, pair counts explode
- current targeted recall works mechanically, but still does not recover enough of the wide-window gain
- current native FTS fallback also works mechanically, but still does not convert recovered candidates into more cross-document pull

So the project is now fighting a **long-range candidate recall problem under cost constraints**, not a vague “semantic weakness” problem.

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

## What This Means

Together, these probes prove:
- the system has real long-range signal
- the current default comparison scope misses too much of it
- selective recall is possible
- but current targeted recall is not yet broad enough
- and cheap-fetch v1, while cheap, is not yet converting recovered breadth into actual pull improvement

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
the graph needs better **cheap long-range candidate recall that actually converts into scored cross-document relations**.

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

## 6. Pair explosion under brute force

Wide-window recovery proves the signal exists, but the pair count becomes too expensive.

That means the stable solution must improve recall **without** approaching Probe 011 cost behavior.

## 7. Dense local hubs can hijack softer field views

The blur experiment showed that dense local neighborhoods, especially index-heavy ones, can dominate soft spread.

Meaning:
- softer field lenses can be informative
- but they are not yet safe replacements for candidate selection

---

## The Best Current Read

The problem is now best described like this:

The system has crossed the threshold where better cross-document relations are possible, but it still lacks a robust low-cost mechanism for proposing the right distant candidates before the heavy scorer runs.

That is why:
- small windows underperform
- large windows overpay
- anchor-only recall plateaus
- and cheap-fetch v1 still fails to convert candidate recovery into actual pull lift
- and the newest conversion reports show that most misses are true out-competition failures, not near-threshold misses

---

## Likely Next Move

The next likely experiment is **not** "add FTS fallback." That has now been done.

The next likely experiment is:

- keep the current sliding window
- keep the heavy scorer as the final gate
- keep the anchor-registry path
- keep the native SQLite FTS fallback path
- keep the new conversion reports in the loop
- inspect why structurally recovered cross-document pairs stay far below threshold
- compare winner vs loser routing / interaction patterns rather than only counting candidate recall
- tighten when the fallback fires so it is not effectively universal on this corpus
- improve deterministic query lexicalization and ranking
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

1. **Cross-document pull must rise materially above `115`**
- otherwise recall is still too weak

2. **Pair cost must stay far below Probe 011**
- otherwise we are just recreating the wide-window brute-force path

3. **Cheap-fetch should not fire blindly on every hunk**
- otherwise the fallback is too broad to be interpretable

4. **Recovered fallback candidates must convert into actual scored wins**
- otherwise recall breadth is being recovered but not operationalized

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
