# ANY_NEW_CONVO_READ_THIS_FIRST

If you are a fresh conversation, start here before proposing changes.

## What This Project Is

BDNeuralTranslationSUITE is a durable relational memory prototype. It splits source material into multi-surface units called HyperHunks, scores relations between them through the Emitter/Nucleus, stores the resulting graph in SQLite, and now exposes a first rudimentary evidence `bag` over that graph.

This project is past vague-concept stage. The pipeline is real, measurable, and already useful enough to test on prose-heavy and mixed code/doc corpora.

## Current Exact Footing

- We are still in **Phase 1**, not Phase 2.
- The active scorer is still the **Bootstrap Nucleus**.
- The **bag CLI exists** and is useful enough to inspect evidence on real corpora.
- The **deterministic semantic lane currently outperforms** the first traditional sentence embedder we tested.
- The main unresolved bottleneck is still **cross-document pull**, but the current read is now sharper:
  - cheap-fetch fallback exists
  - origin-aware cross-document scoring v1 has now materially improved conversion
  - threshold sweeps on that branch can now match and exceed the old Probe 011 wide-window pull count at fixed pair cost
  - but very soft cross-document thresholds become too permissive, so the trustworthy default band is still being chosen
- The focused breakdown of that bottleneck lives here:
  - [`_docs/CROSS_DOCUMENT_PULL_BOTTLENECK_ANALYSIS.md`](C:\Users\jacob\Documents\_AppDesign\_LivePROJECTS\BDNeuralTranslationSUITE\_docs\CROSS_DOCUMENT_PULL_BOTTLENECK_ANALYSIS.md)
- The current best explanation is:
  - the graph has real long-range signal
  - widening the window works, but pair counts explode
  - anchor + native FTS cheap-fetch recover candidates cheaply
  - a single generic scorer lens was part of the plateau
  - the old cross-document threshold gate was much too strict
  - the promising current trust band looks closer to `0.50`–`0.65` than the first accepted `0.92` profile

## The Important Probe Story

- **Probe 003/004** gave us the stable observable baseline.
- **Probe 010** proved list/index representation creates a real explicit signal lane.
- **Probe 011** proved the comparison window was clipping real long-range pairs:
  - `cross-document pull = 1175`
  - but total scored pairs exploded badly
- **Probe 012** proved targeted long-range candidates work mechanically, but recall v1 was too weak:
  - `cross-document pull = 115`
- **Probe 013** upgraded that path into an occurrence-level anchor registry:
  - `relations = 17428`
  - `cross-document pull = 115`
  - `training pairs total = 62583`
  - result: more selective, but still plateaued
- **Probe 014** added native SQLite FTS cheap-fetch fallback:
  - `fts_selected_cross_doc = 548`
  - `cross-document pull = 115`
  - result: cheap recall exists, but does not convert
- **Probe 015/016** clarified the failure:
  - contradiction v1 is real but not the main bottleneck mover
  - FTS origin monopoly is not the main cause
  - current losers are mostly structural/statistical cross-document pairs that stay far below threshold
- **Probe 017/018** tested an origin-aware Bootstrap branch:
  - control replay held the current headline plateau:
    - `relations = 17457`
    - `cross-document pull = 115`
    - `training pairs total = 62896`
  - origin-aware cross-document scorer v1 lifted the same footing to:
    - `relations = 17592`
    - `cross-document pull = 234`
    - `training pairs total = 62896`
  - winner geometry shifted strongly away from grammar-heavy cross-document wins toward `structural_bridge` and `multi_surface`
- **Probe 019/020/021** turned that branch into a rudimentary control gradient:
  - alternate cross-document fractions alone lifted the footing to `150`
  - fractions + shared-anchor bonus lifted it to `155`
  - fractions + cross-document threshold scaling lifted it to `228`
  - full profile reached `234`
  - current read:
    - the alternate cross-document lens matters
    - cross-document threshold scaling carries most of the extra lift
    - the current shared-anchor seam is real but still weak on this footing
- **Probe 022-033** turned threshold scaling into a true control ladder on the same fixed pair budget (`62896`):
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
  - current read:
    - the old cross-document gate was suppressing a very large structural/statistical layer
    - the winner field stays mostly `structural_bridge` / `statistical_echo` deep into the sweep
    - `0.40` is the first warning zone where weakest winners begin to look shaky
    - `0.30` is too permissive and lets fragment-heavy bridge fabric through

## What Works Right Now

- local corpus intake through the current CLI path
- Splitter swarm:
  - Fallback
  - PEG
  - Tree-sitter where supported
- Negotiator / token-budget fracture with lineage preservation
- HyperHunk hashing, provenance, and occurrence identity
- Emitter scoring and Cold Artifact SQLite persistence
- builder-side observable probe loop
- rudimentary bag query workflow
- side-by-side deterministic vs traditional embedder testing

## The Current Bottleneck

The graph now has enough signal to make better cross-document links, and we do have a cheap way to recover distant candidates.

The sharper problem now is:
- too-small window = missed long-range pairs
- too-large window = pair explosion
- anchor-only recall = not broad enough yet
- cheap-fetch fallback = real
- origin-aware scoring = materially better than the one-lens baseline
- threshold scaling proves the old cross-document gate was too strict
- the new practical problem is choosing a trustworthy default band that recovers the latent bridge layer without admitting too many fragment-heavy wins
- current partial shared-anchor / shared-target support still looks secondary to threshold behavior on this footing

## Next Best Move

The parked next step is:

- keep the current sliding window and current SQLite/FTS reuse path
- keep the origin-aware cross-document branch in the active scorer experiment lane
- refine the scorer now that the branch has proved useful:
  - keep the stronger alternate cross-document lens
  - treat cross-document threshold scaling as the main near-term gain lever
  - fine-sweep the `0.50`–`0.65` range and inspect weakest admitted winners there
  - do not promote `0.40` or lower as a default without stronger quality proof
  - keep the current shared-anchor seam in play, but do not widen the contract yet unless threshold/fraction refinement stalls
- define the missing control layer for later retrieval work:
  - `scope root`
  - `resolution grammar`
  - `direction of spread`
  - `stop-unwinding`
- treat bag/walker slice doctrine as future retrieval guidance, not current runtime truth

Phase 2 remains the goal, but it is **not** unlocked yet.

## What Not To Do Next

Do **not** jump to these yet unless the docs explicitly justify it:

- no FFN / Phase 2 jump
- no runtime integration of the anisotropic blur lens
- no broad UI/platform redesign
- no `.dev-tools` coupling into shipped runtime code
- no giant architecture rewrite because one research idea sounds elegant

## Builder / Storage Notes

- `.dev-tools` is builder-only. It may disappear later. Do not make runtime depend on it.
- Heavy builder artifacts live outside the project at:
  - `E:\_UsefulRECORDS\projects\BDNeuralTranslationSUITE\probe_artifacts`
- The repo path [`_docs/_analysis`](C:\Users\jacob\Documents\_AppDesign\_LivePROJECTS\BDNeuralTranslationSUITE\_docs\_analysis) is a junction to that external artifact store.
- This repo is often used as a **sandbox** and then copied into a separate live project folder. Keep that wall intact.

## Read In This Order

1. [`_docs/WE_ARE_HERE_NOW.md`](C:\Users\jacob\Documents\_AppDesign\_LivePROJECTS\BDNeuralTranslationSUITE\_docs\WE_ARE_HERE_NOW.md)
2. [`_docs/CROSS_DOCUMENT_PULL_BOTTLENECK_ANALYSIS.md`](C:\Users\jacob\Documents\_AppDesign\_LivePROJECTS\BDNeuralTranslationSUITE\_docs\CROSS_DOCUMENT_PULL_BOTTLENECK_ANALYSIS.md)
3. [`_docs/TODO.md`](C:\Users\jacob\Documents\_AppDesign\_LivePROJECTS\BDNeuralTranslationSUITE\_docs\TODO.md)
4. [`_docs/QUERY_EXPERIMENTS.md`](C:\Users\jacob\Documents\_AppDesign\_LivePROJECTS\BDNeuralTranslationSUITE\_docs\QUERY_EXPERIMENTS.md)
5. [`_docs/GRAPH_PROBES.md`](C:\Users\jacob\Documents\_AppDesign\_LivePROJECTS\BDNeuralTranslationSUITE\_docs\GRAPH_PROBES.md)
6. [`_docs/DEV_LOG.md`](C:\Users\jacob\Documents\_AppDesign\_LivePROJECTS\BDNeuralTranslationSUITE\_docs\DEV_LOG.md)
7. [`_docs/ARCHITECTURE.md`](C:\Users\jacob\Documents\_AppDesign\_LivePROJECTS\BDNeuralTranslationSUITE\_docs\ARCHITECTURE.md)
8. Optional doctrine follow-up: [`_docs/_research/2026-03-31_scope_root_bag_slice_and_two_sided_anchoring.md`](C:\Users\jacob\Documents\_AppDesign\_LivePROJECTS\BDNeuralTranslationSUITE\_docs\_research\2026-03-31_scope_root_bag_slice_and_two_sided_anchoring.md)

## If You Are Picking Up Work Immediately

Start by restating these three things plainly:

- we are in Phase 1
- the bag exists and is usable
- cheap-fetch fallback already exists, and origin-aware threshold sweeps proved the old cross-document gate was far too strict while revealing a likely trust band around `0.50`–`0.65`

If you say anything that contradicts those three points, you probably have not finished onboarding yet.
