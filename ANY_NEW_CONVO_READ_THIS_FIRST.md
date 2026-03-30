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
- The main unresolved bottleneck is **cross-document pull**.
- The focused breakdown of that bottleneck lives here:
  - [`_docs/CROSS_DOCUMENT_PULL_BOTTLENECK_ANALYSIS.md`](C:\Users\jacob\Documents\_UsefulAgenticBuilderSANDBOX\Claude-Code\_BDNeuralTranslationSUITE\_docs\CROSS_DOCUMENT_PULL_BOTTLENECK_ANALYSIS.md)
- The current best explanation is:
  - the graph has real long-range signal
  - but candidate recall is still too weak unless we widen the comparison window too far
  - widening the window works, but pair counts explode

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

The graph now has enough signal to make better cross-document links, but we still do not have a good cheap way to bring the right distant candidates into comparison.

That means:
- too-small window = missed long-range pairs
- too-large window = pair explosion
- anchor-only recall = not broad enough yet

## Next Best Move

The next likely tranche is:

- keep the current sliding window
- keep the heavy scorer as the final gate
- add a **deterministic cheap-fetch fallback** behind the anchor-registry path
- prefer reusing existing SQLite / FTS surfaces instead of inventing a broad new subsystem

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
- The repo path [`_docs/_analysis`](C:\Users\jacob\Documents\_UsefulAgenticBuilderSANDBOX\Claude-Code\_BDNeuralTranslationSUITE\_docs\_analysis) is a junction to that external artifact store.
- This repo is often used as a **sandbox** and then copied into a separate live project folder. Keep that wall intact.

## Read In This Order

1. [`_docs/WE_ARE_HERE_NOW.md`](C:\Users\jacob\Documents\_UsefulAgenticBuilderSANDBOX\Claude-Code\_BDNeuralTranslationSUITE\_docs\WE_ARE_HERE_NOW.md)
2. [`_docs/CROSS_DOCUMENT_PULL_BOTTLENECK_ANALYSIS.md`](C:\Users\jacob\Documents\_UsefulAgenticBuilderSANDBOX\Claude-Code\_BDNeuralTranslationSUITE\_docs\CROSS_DOCUMENT_PULL_BOTTLENECK_ANALYSIS.md)
3. [`_docs/TODO.md`](C:\Users\jacob\Documents\_UsefulAgenticBuilderSANDBOX\Claude-Code\_BDNeuralTranslationSUITE\_docs\TODO.md)
4. [`_docs/QUERY_EXPERIMENTS.md`](C:\Users\jacob\Documents\_UsefulAgenticBuilderSANDBOX\Claude-Code\_BDNeuralTranslationSUITE\_docs\QUERY_EXPERIMENTS.md)
5. [`_docs/GRAPH_PROBES.md`](C:\Users\jacob\Documents\_UsefulAgenticBuilderSANDBOX\Claude-Code\_BDNeuralTranslationSUITE\_docs\GRAPH_PROBES.md)
6. [`_docs/DEV_LOG.md`](C:\Users\jacob\Documents\_UsefulAgenticBuilderSANDBOX\Claude-Code\_BDNeuralTranslationSUITE\_docs\DEV_LOG.md)
7. [`_docs/ARCHITECTURE.md`](C:\Users\jacob\Documents\_UsefulAgenticBuilderSANDBOX\Claude-Code\_BDNeuralTranslationSUITE\_docs\ARCHITECTURE.md)

## If You Are Picking Up Work Immediately

Start by restating these three things plainly:

- we are in Phase 1
- the bag exists and is usable
- the next likely move is deterministic cheap-fetch fallback for long-range candidate recall

If you say anything that contradicts those three points, you probably have not finished onboarding yet.
