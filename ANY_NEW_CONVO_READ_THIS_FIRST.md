# ANY_NEW_CONVO_READ_THIS_FIRST

If you are a fresh conversation, start here before proposing changes.

## What This Project Is

BDNeuralTranslationSUITE is a durable relational memory prototype. It splits source material into multi-surface units called HyperHunks, scores relations between them through the Emitter/Nucleus, stores the resulting graph in SQLite, and now exposes a first rudimentary evidence `bag` over that graph.

This project is past vague-concept stage. The pipeline is real, measurable, and already useful enough to test on prose-heavy and mixed code/doc corpora.

## Current Exact Footing

- We are still in **Phase 1**, not Phase 2.
- A late-Phase-1 diagnostic branch (`baseline-leg-sidecar`) has now clarified two mainline truths:
  - shared registry / shared visible state is the right collaboration doctrine
  - a narrow code/reference footing is not enough; corpus planning now needs a real English baseline
- The active scorer is still the **Bootstrap Nucleus**.
- The **bag CLI exists** and is useful enough to inspect evidence on real corpora.
- A minimal separate shared viewer sidecar now exists for collaborative retrieval work:
  - human-driven shared-state viewing is proven
  - agent-driven visible panel action is still an experimental follow-up seam
  - collaboration doctrine is now: `sync -> think -> act -> resync`
- The bag path now also has a confirmed Hot Engine direction fix:
  - activation had been propagating backward relative to stored `source_occ_id -> target_occ_id` relations
  - that bug is now fixed
  - post-fix bag behavior is materially more trustworthy on the reference footing
- The bag path now also has a first conservative lexicalization/rerank layer:
  - lexical query variants shape lexical anchors
  - corroborated origins can receive a small bag-only support bonus
  - this already improves `eval input`
- The **deterministic semantic lane currently outperforms** the first traditional sentence embedder we tested.
- We now also have first evidence that semantic works better as an **overlay attraction field** than as a primary support surface:
  - bounded semantic-gravity overlays improve cross-document pull in both semantic lanes
  - the deterministic lane is currently far stronger than the sentence-transformer lane on this footing
  - a later deterministic shape sweep (`steep` / `softplus` / `high` / `xhigh`) shows the graph gains are now saturating rather than revealing a wholly new regime
  - on the current 11-query human-facing shelf, all those deterministic shape variants preserved the same top-item set as deterministic control
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
  - the most useful current bag-facing sub-band looks closer to `0.55`–`0.58`, with `0.58` as the current leading default candidate
  - that `0.58` read still applies to the current no-semantic-overlay bag footing; the new semantic-gravity path is promising but still needs bag-side QC before promotion

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
- **Probe 041-060** turned the current `0.58` footing into a first five-vertex shock-load map:
  - structural is the strongest current load-bearing surface
  - grammatical remains strongly active
  - verbatim is real but narrow
  - semantic is slack on the `embedder=none` footing
  - statistical is useful, but not as a dominant single carrying force on that exact sweep shape
- **Probe 061-064** rotated the successful cross-document weight pattern around the five vertices:
  - baseline structural-heavy footing: `2703`
  - rotated to statistical-heavy: `5`
  - rotated to semantic-heavy: `83`
  - rotated to verbatim-heavy: `144`
  - rotated to grammatical-heavy: `1052`
  - result: the field cares about surface assignment, not just the numeric pattern
- **Probe 065-072** tested a bounded semantic-gravity overlay on top of the anchor lens:
  - deterministic control/high:
    - `10955 -> 12133`
  - sentence-transformers control/high:
    - `3380 -> 3943`
  - result:
    - semantic gravity is a real phenomenon in both lanes
    - the deterministic semantic lane is much stronger on this footing
    - semantic currently looks more like a long-range attraction field than a primary support beam
- **Probe 073-076** refined and validated that semantic-gravity seam:
  - `steep`, `softplus`, and `xhigh` all sit very close to the earlier `high` point on graph metrics
  - current read:
    - `xhigh` adds only marginal gain over `high`
    - `steep` preserves more `multi_surface` / `structural_bridge` winner geometry and is now the promoted safe default
    - `softplus` is a strong compromise point that remains worth keeping as an option
  - the current semantic-shape QC artifact is:
    - [`_docs/_analysis/bag_semantic_shape_qc_2026-04-01/bag_semantic_shape_qc_2026-04-01.md`](C:\Users\jacob\Documents\_AppDesign\_LivePROJECTS\BDNeuralTranslationSUITE\_docs\_analysis\bag_semantic_shape_qc_2026-04-01\bag_semantic_shape_qc_2026-04-01.md)
  - the live monitor was also upgraded in this stretch:
    - clearer metric cards
    - summary and sample tabs
    - five-surface color cues
    - typed `report_summary` / `report_snapshot` events
- We have now started mapping two more Phase 1 surface families on top of that safe semantic footing:
  - `verbatim` currently looks more like a precision / articulation-control surface than a growth lever
  - light verbatim promotion is survivable, but stronger promotion steadily trims cross-document winners
  - `contradiction_soft` is the most interesting current counter-pressure seed
  - `contradiction_block` is too blunt on this reference footing
  - the combined mapping note is:
    - [`_docs/_analysis/verbatim_contradiction_mapping_2026-04-01/verbatim_contradiction_mapping_2026-04-01.md`](C:\Users\jacob\Documents\_AppDesign\_LivePROJECTS\BDNeuralTranslationSUITE\_docs\_analysis\verbatim_contradiction_mapping_2026-04-01\verbatim_contradiction_mapping_2026-04-01.md)
- We now also have the first paired `verbatim` excursion map:
  - `verbatim + semantic` lifts graph metrics slightly and reduces cross-document losers
  - but it does not improve articulation convergence on the tested bag shelf
  - current read: this pair produces semantic consolidation more than wording-control
  - the next better articulation candidate is likely `verbatim + structural`
  - mapping note:
    - [`_docs/_analysis/verbatim_semantic_pair_mapping_2026-04-01/verbatim_semantic_pair_mapping_2026-04-01.md`](C:\Users\jacob\Documents\_AppDesign\_LivePROJECTS\BDNeuralTranslationSUITE\_docs\_analysis\verbatim_semantic_pair_mapping_2026-04-01\verbatim_semantic_pair_mapping_2026-04-01.md)
- We now also have the second paired `verbatim` excursion map:
  - `verbatim + structural` changes the field orientation, but still does not improve articulation convergence on the tested bag shelf
  - current joint read from both pair maps:
    - naive pairwise weight steering is not enough to solve articulation control
    - the next better seam is likely retrieval/rerank behavior or finer-grain verbatim resolution
  - mapping note:
    - [`_docs/_analysis/verbatim_structural_pair_mapping_2026-04-01/verbatim_structural_pair_mapping_2026-04-01.md`](C:\Users\jacob\Documents\_AppDesign\_LivePROJECTS\BDNeuralTranslationSUITE\_docs\_analysis\verbatim_structural_pair_mapping_2026-04-01\verbatim_structural_pair_mapping_2026-04-01.md)
- We also clarified a future verbatim-resolution seam:
  - the live `CIS` layer is currently hunk-level content-addressed dedupe plus verbatim text persistence
  - it is **not** yet a full CAS / Merkle / BPE-backed verbatim store
  - current sane middle-ground branch, when we are ready, is:
    - dedupe hardening first
    - then line/span-level sub-hunks
    - then rudimentary scope traversal
  - current explicit non-goal:
    - do **not** try to land BPE + CAS + Merkle + full walker scope control all in one tranche
- We now also have the first query-side articulation strategy comparison over the live `det_steep` DB:
  - baseline current bag shelf: `same_top = 5`, `same_origin = 6`
  - `phrase_core` expansion is worse: `4 / 4`
  - `identifier_norm` is basically neutral: `5 / 6`
  - `char_ngram` rerank is the first light query-side mover: `6 / 6`
  - current read:
    - char n-gram overlap is the most promising next query-side articulation seam on the existing hunk field
    - phrase-core expansion is too blunt on this footing
    - identifier normalization alone does not buy much yet
  - mapping note:
    - [`_docs/_analysis/query_articulation_strategy_probe_2026-04-01/query_articulation_strategy_probe.md`](C:\Users\jacob\Documents\_AppDesign\_LivePROJECTS\BDNeuralTranslationSUITE\_docs\_analysis\query_articulation_strategy_probe_2026-04-01\query_articulation_strategy_probe.md)
- We then promoted the bounded char n-gram term into the live bag rerank in [`_BDHyperNeuronEMITTER/src/core/engine/inference/bag_view.py`](C:\Users\jacob\Documents\_AppDesign\_LivePROJECTS\BDNeuralTranslationSUITE\_BDHyperNeuronEMITTER\src\core\engine\inference\bag_view.py):
  - first integrated live articulation shelf: `same_top = 7`, `same_origin = 7`
  - punctuation-insensitive alias matching plus bounded short-anchor trust then closed the remaining import-style miss
  - current integrated live articulation shelf now sits at `same_top = 8`, `same_origin = 8`
  - current read:
    - the bag is now aligned across the full tested articulation shelf
    - this win came from bag/query shaping, not a new ingest branch
    - lexical-anchor breadth has now also been decoupled from final bag return count, so the `module imports` win holds even when the displayed bag is narrow
  - integrated mapping notes:
    - [`_docs/_analysis/query_articulation_strategy_probe_2026-04-01_live_char_ngram/query_articulation_strategy_probe.md`](C:\Users\jacob\Documents\_AppDesign\_LivePROJECTS\BDNeuralTranslationSUITE\_docs\_analysis\query_articulation_strategy_probe_2026-04-01_live_char_ngram\query_articulation_strategy_probe.md)
    - [`_docs/_analysis/query_articulation_strategy_probe_2026-04-01_import_anchor_tune_v2/query_articulation_strategy_probe.md`](C:\Users\jacob\Documents\_AppDesign\_LivePROJECTS\BDNeuralTranslationSUITE\_docs\_analysis\query_articulation_strategy_probe_2026-04-01_import_anchor_tune_v2\query_articulation_strategy_probe.md)
    - [`_docs/_analysis/query_articulation_strategy_probe_2026-04-01_anchor_budget_decoupled/query_articulation_strategy_probe.md`](C:\Users\jacob\Documents\_AppDesign\_LivePROJECTS\BDNeuralTranslationSUITE\_docs\_analysis\query_articulation_strategy_probe_2026-04-01_anchor_budget_decoupled\query_articulation_strategy_probe.md)
- We also ran a contained BPE query-time articulation probe against the same `det_steep` footing:
  - result: `0 / 16` queries produced any concept-relevant readable nearest-token hits
  - current read:
    - the active deterministic BPE space tied to this DB is not the right articulation field for the Python-reference shelf
    - do **not** wire BPE query expansion into this footing yet
  - probe note:
    - [`_docs/_analysis/bpe_query_articulation_probe_2026-04-01/bpe_query_articulation_probe_2026-04-01.md`](C:\Users\jacob\Documents\_AppDesign\_LivePROJECTS\BDNeuralTranslationSUITE\_docs\_analysis\bpe_query_articulation_probe_2026-04-01\bpe_query_articulation_probe_2026-04-01.md)

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
- bounded semantic-gravity overlays behind profile control
- a richer live probe monitor that can show both numbers and example evidence in the same window

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
- bag usefulness now also matters as a first-class acceptance surface
- after the Hot Engine fix, bag behavior is finally reflecting the stronger graph instead of partially hiding it

## Next Best Move

The parked next step is:

- keep the baseline-leg-sidecar branch as a concluded diagnostic/reference seam, not a second product line
- promote only the proven collaboration pieces into mainline:
  - shared registry
  - minimal separate sidecar viewer
  - explicit action provenance
- shift corpus doctrine toward:
  - general English first
  - then technical/project English
  - then code/doc bridge corpora
- keep the current sliding window and current SQLite/FTS reuse path
- keep the origin-aware cross-document branch in the active scorer experiment lane
- keep the Hot Engine direction fix as current runtime truth
- keep the upgraded live monitor as the normal probe-observer surface
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
- keep bag checks on `hop_limit = 1` for human-facing evaluation
- treat `0.58` as the current leading bag-first default candidate unless broader checks disprove it
- if current bag quality stalls, the next likely bag seams are:
  - targeted lexicalization / alias refinement for stubborn queries
  - then, if needed, decoupling anchor budget from final bag size
- on the active semantic-gravity lane, the next close choice is now:
  - no longer “is semantic gravity real at all?”
  - the safe default is now `steep`
  - `softplus` remains the strongest practical alternative
  - `high` / `xhigh` remain labeled ceiling/stress points rather than promoted defaults

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
8. Current session wrap-up: [`_docs/SESSION_ORIENTATION_2026-04-01.md`](C:\Users\jacob\Documents\_AppDesign\_LivePROJECTS\BDNeuralTranslationSUITE\_docs\SESSION_ORIENTATION_2026-04-01.md)
9. Session close freeze: [`_docs/SESSION_CLOSE_REPORT_2026-04-01.md`](C:\Users\jacob\Documents\_AppDesign\_LivePROJECTS\BDNeuralTranslationSUITE\_docs\SESSION_CLOSE_REPORT_2026-04-01.md)
10. Optional doctrine follow-up: [`_docs/_research/2026-03-31_scope_root_bag_slice_and_two_sided_anchoring.md`](C:\Users\jacob\Documents\_AppDesign\_LivePROJECTS\BDNeuralTranslationSUITE\_docs\_research\2026-03-31_scope_root_bag_slice_and_two_sided_anchoring.md)

## If You Are Picking Up Work Immediately

Start by restating these three things plainly:

- we are in Phase 1
- the bag exists and is usable
- cheap-fetch fallback already exists, and origin-aware threshold sweeps proved the old cross-document gate was far too strict while revealing a likely trust band around `0.50`–`0.65`, with `0.58` currently leading the bag-first default race

If you say anything that contradicts those three points, you probably have not finished onboarding yet.
