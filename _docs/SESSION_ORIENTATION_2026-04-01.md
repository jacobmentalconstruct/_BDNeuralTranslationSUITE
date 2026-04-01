# Session Orientation — 2026-04-01

## Where We Are

- We are still in **Phase 1**.
- The Bootstrap Nucleus is still the active scorer.
- The bag is now useful enough to act as a real reader-facing inspection surface.
- The old `115` cross-document plateau is broken.
- The project has moved from “prove any lift exists” to “map the field honestly and choose the trustworthy operating regimes.”

## Important Highlights From This Stretch

### 1. The graph breakthrough was real

- Origin-aware cross-document scoring broke the old plateau.
- Threshold sweeps proved the previous cross-document gate was far too strict.
- The graph now exposes much more long-range structure at the same pair budget.

### 2. The bag became more trustworthy

- The Hot Engine propagation-direction bug was fixed.
- Human-facing bag rerank, lexical variants, origin support, and anchor backfill all improved evidence readability.
- The bag now behaves much more like a usable evidence shelf than raw graph exhaust.

### 3. Phase 1 is now better understood

- Phase 1 should not end when we find one lucky profile.
- Phase 1 should end when all five surfaces are **individually mapped and functionally integrated in context**.
- That does **not** mean mashing them back into one average.

### 4. Five-vertex shock-load sweeps clarified the field

On the active `0.58` origin-aware footing:

- `structural` is the strongest current load-bearing surface
- `grammatical` remains strongly active
- `verbatim` is real but narrow
- `semantic` is slack on the `embedder=none` footing
- `statistical` is useful, but not as a dominant single carrying force on that exact sweep shape

### 5. Rotation testing proved the orientation matters

Keeping the same weight pattern but rotating it across vertices did **not** preserve the lift.

Cross-document pull:

- baseline (`structural` heavy): `2703`
- rotated to `statistical`: `5`
- rotated to `semantic`: `83`
- rotated to `verbatim`: `144`
- rotated to `grammatical`: `1052`

Meaning:

- we did **not** just stumble onto a generic numeric pattern
- the field cares about **which surface** receives which role

### 6. Semantic is starting to look like an attraction field, not a beam

We tested a **bounded semantic gravity overlay** on top of the current anchor lens instead of trying to make semantic hold the scaffold by itself.

Deterministic semantic lane:

- control: `10955`
- low gravity: `11697`
- mid gravity: `12052`
- high gravity: `12133`

Sentence-transformers lane:

- control: `3380`
- low gravity: `3528`
- mid gravity: `3700`
- high gravity: `3943`

Current read:

- the semantic-gravity idea is real
- it helps in both lanes
- the deterministic semantic lane is much stronger on this footing
- semantic currently looks more like a **long-range attraction field** than a primary support beam

## What The Current Picture Seems To Be

- `structural` gives the lattice shape
- `grammatical` helps stabilize local readable alignment
- `statistical` reinforces recurring pattern structure
- `verbatim` gives exact contact / pullback truth
- `semantic` can act like bounded long-range attraction

This means the project is no longer just tuning one score. It is starting to map the different jobs of the surfaces.

## Immediate Next Steps

1. Quality-control the new semantic-gravity runs through the bag:
   - deterministic control
   - deterministic mid/high gravity
   - sentence-transformers control
   - sentence-transformers high gravity

2. Decide whether the deterministic semantic-gravity lane is:
   - genuinely better for evidence quality
   - or merely producing bigger graph numbers

3. Continue the Phase 1 five-vertex mapping program:
   - semantic in active conditions
   - verbatim/commonality behavior
   - contradiction / anti-signal as a real shaping field

4. Formalize Phase 1 exit criteria around:
   - all five surfaces mapped in context
   - bag trustworthy enough for human/agent use
   - training data disciplined enough for FFN comparison work

## Path To Phase 2

The path to Phase 2 is now clearer, not shorter.

Phase 2 should only begin after:

- the five-surface baseline is functionally real
- the bag is trustworthy as a bounded evidence slice
- the scorer control surfaces are understood well enough to generate believable training data
- we can compare a learned scorer against a strong deterministic baseline instead of using learning as a rescue move

So the direction is still:

- Phase 1: map and stabilize the field
- Phase 2: train against a trustworthy baseline
- Phase 3+: richer query/bag/walker behavior and later doctrine math
