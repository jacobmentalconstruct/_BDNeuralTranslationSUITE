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
- The main unresolved bottleneck is still **cross-document pull**, but the live failure mode is now more specific:
  - cheap-fetch fallback exists
  - long-range candidates are being recovered
  - too many structurally plausible cross-document pairs still fail to convert into winning edges
- The focused breakdown of that bottleneck lives here:
  - [`_docs/CROSS_DOCUMENT_PULL_BOTTLENECK_ANALYSIS.md`](C:\Users\jacob\Documents\_AppDesign\_LivePROJECTS\BDNeuralTranslationSUITE\_docs\CROSS_DOCUMENT_PULL_BOTTLENECK_ANALYSIS.md)
- The current best explanation is:
  - the graph has real long-range signal
  - widening the window works, but pair counts explode
  - anchor + native FTS cheap-fetch recover candidates cheaply
  - the current scorer still under-converts many structural long-range candidates

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
- cheap-fetch fallback = real, but too many recovered structural cross-document candidates still lose at conversion time

## Next Best Move

The parked next step is:

- inspect structural losers versus grammatical winners
- keep the current sliding window and current SQLite/FTS reuse path
- focus the next scorer work on promotion of structurally plausible cross-document bridges
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
- cheap-fetch fallback already exists, and the next likely move is scorer-side conversion work on structural losers

If you say anything that contradicts those three points, you probably have not finished onboarding yet.
