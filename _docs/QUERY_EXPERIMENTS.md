# Query Experiments

_Last updated: 2026-03-30. This file records builder-side query/retrieval experiments that are informative, but not yet promoted into the app runtime doctrine._

Long-horizon query doctrine artifacts and north-star codexes live under `_docs/_research/_codexes/`. They are reference surfaces, not active runtime truth.

The current retrieval-doctrine synthesis for later bag/walker work now also lives here:
- `_docs/_research/2026-03-31_scope_root_bag_slice_and_two_sided_anchoring.md`

That note captures:
- bag as a bounded observer-centered slice
- two-sided anchoring
- scope root
- resolution grammar
- direction of spread
- stop-unwinding logic

It is planning/doctrine truth only, not a claim that runtime retrieval already behaves that way.

---

## Experiment 001 — Anisotropic Blur Lens

**Date:** 2026-03-30

### Purpose

Test a light, builder-side "anisotropic blur" experiment over existing Cold Artifact DBs to see what kind of neighborhood data a soft query-conditioned field projection yields before any runtime integration work.

This was intentionally run as a builder-only experiment:
- no runtime coupling to `.dev-tools`
- no change to the app retrieval contract
- read-only over existing probe databases

Builder tool:
- `.dev-tools/final-tools/tools/anisotropic_blur_probe.py`

Saved artifacts:
- `_docs/_analysis/reference_probe_013_anchor_registry_v1/anisotropic_blur_lexical_analysis.json`
- `_docs/_analysis/appbuilder_toolbox_probe_002_det/anisotropic_blur_mcp_server.json`

### Experiment shape

For each query:
- seed from existing SQLite `content_fts`
- load a local subgraph around those seed occurrences
- apply a directional blur over the relation graph
- bias spread by:
  - relation `op`
  - `interaction_mode`
  - small cross-document bonus
- rank the resulting activated neighborhood

This is a **lens**, not a replacement retrieval engine.

### Result A — Python reference bottleneck case

Query:
- `lexical analysis`

DB:
- `reference_probe_013_anchor_registry_v1`

Read:
- seeds were sensible and cross-document:
  - `index.txt`
  - `lexical_analysis.txt`
  - `introduction.txt`
  - `expressions.txt`
- but the blur result collapsed into dense `index.txt` list-item neighborhoods
- top-cross-document count in the blur top set was `0`
- by contrast, the current bag stayed more diverse:
  - `introduction.txt`
  - `lexical_analysis.txt`
  - `expressions.txt`
  - `index.txt`

Interpretation:
- the blur is sensitive to high-degree local hub structure
- in this corpus, it currently over-amplifies dense index neighborhoods
- this makes it useful as a **field-shape diagnostic**
- but not yet better than the bag as an evidence surface
- tooling note:
  - this run reported `orphan_edge_skips = 2`
  - the tool now reports these gracefully instead of failing

### Result B — Mixed code/doc graph

Query:
- `mcp server`

DB:
- `appbuilder_toolbox_probe_002_det`

Read:
- the blur produced a strong operational neighborhood around:
  - `src/smoke_test.py`
  - `src/tools/journal_acknowledge.py`
  - `src/tools/journal_actions.py`
  - `src/tools/journal_init.py`
  - `src/tools/journal_export.py`
- top-cross-document count in the blur top set was `4`
- the current bag remained more directly user-relevant:
  - `README.md`
  - `tool_pack.py`
  - `mcp_server.py`
  - `journal_store.py`
  - `scaffolds.py`

Interpretation:
- the blur is surfacing **procedural / topological neighborhood**
- the bag is surfacing **more directly relevant evidence**
- this means the blur lens is adding a different kind of information, not just duplicating the bag
- tooling note:
  - this run reported `orphan_edge_skips = 137`
  - that is worth keeping in mind as a possible data-shape seam in some graphs/subgraph loads

### What this experiment gives us

The anisotropic blur lens currently provides:
- neighborhood shape
- hub sensitivity
- cross-document spread behavior
- a way to see when relation geometry is being hijacked by dense local structures
- a distinct procedural/topological view that can complement the bag

### What it does not justify yet

- not a runtime replacement for the current bag/query path
- not evidence that we should move blur into the main retrieval loop yet
- not evidence that the blur solves the cross-document recall bottleneck by itself

### Current read

The blur lens is worth keeping as a builder-side experiment surface.

Right now:
- the bag remains the better relevance/evidence surface
- the blur is useful as a **diagnostic neighborhood lens**

If this line continues later, the likely next refinements would be:
- stronger damping for dense list/index hubs
- seed-diversity balancing
- cross-document diversity bias
- source-root / container-aware traversal penalties or bonuses
