# BDNeuralTranslationSUITE — Breakthrough Report

_Date: 2026-03-31_

_Purpose: capture the Phase 1 scorer breakthrough, the control-ladder results, and a plain-English explanation of what changed and why it matters._

---

## Why This Moment Matters

This session changed the project in a meaningful way.

Before this work, the Python reference footing looked stuck behind a familiar wall:
- wide-window brute force could recover a lot of cross-document pull
- targeted cheap recall could not convert enough of that pull into real graph edges
- the headline plateau sat at `115`

After this session, that is no longer the right story.

We now have proof that:
- the old plateau was partly caused by the scorer itself
- a single generic bootstrap lens was too strict for cross-document pairs
- the graph can recover and exceed the old wide-window high-water mark at fixed pair cost
- the new live job is not "prove lift exists" but "choose the trustworthy operating band"

That is a real change in project state.

---

## The Starting Point

The earlier bottleneck looked like this:

- **Probe 011**
  - `cross-document pull = 1175`
  - `training pairs total = 234900`
  - read: the signal exists, but brute force is too expensive

- **Probe 014**
  - `cross-document pull = 115`
  - `training pairs total = 63155`
  - `fts_selected_cross_doc = 548`
  - read: cheap recall can find faraway candidates, but the scorer still rejects most of them

So the real question became:

**Can we keep the cheap candidate pool, but judge cross-document pairs more intelligently?**

---

## The Breakthrough

We added a narrow, scorer-only branch to the Bootstrap Nucleus:

- same-document pairs still use the old lens
- cross-document pairs can use a different static lens
- that cross-document lens can:
  - shift surface weights
  - lower only the cross-document gate
  - add a small shared-anchor structural bonus from existing fields

This was intentionally small:
- no Splitter contract changes
- no intent-aware scoring
- no FFN work
- no broad retrieval redesign

### Result

On the same fixed footing:

| Probe | Variant | Relations | Cross-document Pull | Training Pairs |
| --- | --- | ---: | ---: | ---: |
| 017 | Control replay | 17457 | 115 | 62896 |
| 018 | Origin-aware cross-document scorer v1 | 17592 | 234 | 62896 |

This is the first clean proof that the scorer lens itself was part of the bottleneck.

---

## What The Lenses Are Actually Doing

This section is the human-readable version.

Think of the scorer like a judge looking at two pieces of information and asking:

**"Do these belong together strongly enough to become a real connection?"**

The judge does not use just one clue. It looks through several lenses:

- **Verbatim**
  - do the actual words or exact phrases line up?
- **Structural**
  - do they live in related parts of the source shape?
- **Grammatical**
  - do they behave like similar kinds of things?
- **Statistical**
  - do they share token patterns or overlap strongly enough to matter?
- **Semantic**
  - do they feel alike in meaning?

### Why One Lens Was Not Enough

The old bootstrap treated all pairs too similarly.

That works better for **same-document** pairs, because those pairs often do share:
- local grammar
- local structure
- nearby flow

But **cross-document** pairs are different.

They often do **not** look locally similar.
They are more likely to be:
- structural bridges
- repeated topic echoes
- shared dependency neighborhoods
- distant but still meaningful correspondences

So the old generic lens was often asking a cross-document bridge to behave like a local paragraph neighbor.
That is why good long-range candidates were being found and then thrown away.

### What The New Cross-Document Lens Does

The new branch changes the judge for cross-document pairs only.

In plain language:
- it trusts local grammar less
- it trusts structural bridge evidence more
- it trusts broader statistical bridge evidence more
- it gives a small bonus when two hunks point into similar reference/import neighborhoods

That is why the winner mix changed from mostly `grammatical_dominant` to mostly `structural_bridge` and `multi_surface`.

---

## What Threshold Scaling Is Actually Doing

The threshold is the bouncer at the door.

After the scorer adds everything up, the threshold asks:

**"Is this strong enough to let in?"**

For cross-document pairs, the old bouncer was much too strict.

That is why the next step was to sweep the cross-document threshold downward while keeping:
- the same candidate pool
- the same pair budget
- the same origin-aware cross-document lens

This matters a lot:

we were **not** widening search again.

We were testing whether the same already-found bridge candidates had been unfairly kept outside.

---

## The Control Ladder

On the same fixed pair budget (`62896` throughout), the threshold sweep looked like this:

| Threshold Scale | Cross-document Pull | Read |
| --- | ---: | --- |
| `0.95` | 206 | better than control, still conservative |
| `0.90` | 255 | clear lift |
| `0.85` | 368 | still disciplined |
| `0.80` | 588 | strong lift |
| `0.75` | 912 | approaching wide-window territory |
| `0.70` | 1406 | exceeds old Probe 011 high-water mark |
| `0.65` | 1975 | very strong lift, still structurally dominated |
| `0.60` | 2480 | still strong, still usable-looking |
| `0.50` | 3876 | huge lift, weakest winners mostly still defensible |
| `0.40` | 6312 | first warning zone |
| `0.30` | 8458 | too permissive / fragment-heavy |

### The Most Important Point

These gains happened **without pair growth**.

That means:
- we were not "buying" lift by brute force
- we were revealing a latent bridge layer that the older scorer gate had been suppressing

---

## What The Ablations Told Us

We also broke the origin-aware profile apart to see which pieces mattered most.

| Probe | Variant | Cross-document Pull | What It Told Us |
| --- | --- | ---: | --- |
| 019 | fractions only | 150 | different cross-document weighting helps |
| 020 | fractions + threshold | 228 | threshold scaling is the biggest lever |
| 021 | fractions + shared-anchor | 155 | current shared-anchor seam helps a bit, but is secondary |

So the leverage order is currently:

1. cross-document threshold behavior
2. cross-document surface fractions
3. current shared-anchor approximation

That is useful because it tells us what **not** to over-invest in too early.

---

## What Changed In The Winner Geometry

Before the new branch, cross-document winners were mostly grammar-led.

After the origin-aware branch, they became much more bridge-led.

That matters because our earlier loser diagnostics had already told us:
- many cross-document losers looked structurally plausible
- the scorer was just not rewarding that kind of relation enough

So the new winner geometry supports the same story:

the graph did not mainly need "more candidates."
It needed a better way to recognize a cross-document bridge as a real relation.

---

## The Human Takeaway

If we explain the progression without the jargon, it looks like this:

1. We knew there were a lot of real long-range connections in the data.
2. We proved that by checking a huge number of pairs, but that was too expensive.
3. We then built cheaper ways to find likely long-range candidates.
4. Those candidates still were not turning into enough real edges.
5. This session showed why:
   - the judge was using the wrong standards for cross-document pairs
6. Once we gave cross-document pairs their own lens and their own gate, the hidden bridge layer started showing up.

So the project moved from:

**"Can we recover this at all?"**

to:

**"How much of this recovered bridge layer is real enough to trust as the default?"**

That is a much better problem to have.

---

## Current Trust Read

Right now the most promising operating band looks like:

- **likely trust band:** `0.50`–`0.65`
- **warning zone:** `0.40`
- **too permissive:** `0.30`

Why:

- at `0.50`, the weakest admitted winners still mostly looked borderline-but-defensible
- at `0.40`, weaker fragment-heavy bridges started becoming more common
- at `0.30`, the gate was clearly too soft and admitted too much shaky bridge fabric

So the current task is not to chase the biggest possible number.

It is to find the highest-performing band that still looks trustworthy.

---

## What This Changes In The Todo Path

Before this session, the next steps were still framed around:
- proving the scorer could move the plateau at all
- deciding whether richer reference extraction had to happen immediately

After this session, the trajectory is different:

1. Keep the origin-aware cross-document branch.
2. Fine-sweep and inspect the `0.50`–`0.65` band.
3. Study weakest admitted winners inside that band.
4. Decide on a trustworthy default operating point.
5. Only then decide whether richer shared-target extraction is actually needed.

That means the project is now getting real **tuning gradients**, not just isolated experiments.

---

## What We Still Do Not Know

Even with the breakthrough, several things remain unresolved:

- which exact point inside `0.50`–`0.65` should become the default
- whether current shared-anchor signals are enough, or whether the contract will later need richer target-neighborhood data
- how much of the very large recovered bridge layer remains useful on other corpora
- how Phase 2 bag/walker retrieval should sit on top of this improved substrate

So this is a breakthrough, but not the end of the story.

---

## Current Best Summary

The Phase 1 bottleneck was not just a recall bottleneck.
It was also a scorer-lens bottleneck.

This session proved that:
- origin-aware static branching works
- cross-document threshold control is a powerful and measurable lever
- the graph contains a much larger latent bridge layer than the old `115` plateau suggested
- the next engineering task is to choose the trustworthy operating band for that layer

In short:

**We are no longer fighting to prove cross-document lift exists. We are now learning how to control it well.**

---

## Bag Follow-Through

One more important thing happened after the scorer breakthrough:

the bag finally started reflecting the better graph, but only after a real engine fix.

### What Was Wrong

The Hot Engine was propagating activation backward relative to stored edge direction.

That means the bag could still look awkward even when the graph underneath had improved, because activation was not flowing through the graph the way the stored relations claimed it should.

### What Changed

After fixing the propagation orientation:
- `hop_limit = 1` remained the best human-facing mode
- `hop_limit = 2` and `3` still became noisy
- wider seed budgets still did not help much
- but the stronger origin-aware graph bands now showed up clearly in the bag

### Human Read

Before the fix:
- some graph improvements were real, but the bag was partially hiding them

After the fix:
- `lexical analysis` moved from a stray `introduction.txt` result into `lexical_analysis.txt`
- `encoding declarations` stopped surfacing a bad `datamodel.txt` item on the better bands
- `operator precedence` moved from `index.txt` into `expressions.txt` on the better bands

That means the project is now in a better place than the raw graph numbers alone suggested:

- the graph breakthrough was real
- the bag bug was real
- once the bug was fixed, the bag started showing the value of the better lens bands

### Current Bag-First Read

Right now:
- `0.58` looks like the leading default candidate
- `0.55` is close behind
- `0.60` is safer-looking on paper but less useful on several important bag queries

So the control problem is now:

**pick the strongest graph/bag band that still feels trustworthy to a human reader.**
