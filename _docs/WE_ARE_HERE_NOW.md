# WE_ARE_HERE_NOW

_Overwrite this file at each small milestone. It is the fastest crash-recovery / cold-start note in the project._

## Last updated

2026-04-02

## Fresh-thread start

- If this is a brand new conversation, read [`ANY_NEW_CONVO_READ_THIS_FIRST.md`](C:\Users\jacob\Documents\_AppDesign\_LivePROJECTS\BDNeuralTranslationSUITE\ANY_NEW_CONVO_READ_THIS_FIRST.md) before proposing new work.
- Then use this file as the fast state checkpoint.
- If the work is specifically about the cross-document recall bottleneck, also read [`CROSS_DOCUMENT_PULL_BOTTLENECK_ANALYSIS.md`](C:\Users\jacob\Documents\_AppDesign\_LivePROJECTS\BDNeuralTranslationSUITE\_docs\CROSS_DOCUMENT_PULL_BOTTLENECK_ANALYSIS.md) immediately after.

## Current footing

- The repo root is now the active portable project root.
- A root new-conversation onboarding guide now exists.
- Phase 1 baseline is real and runnable.
- Splitter and Emitter are both live enough to continue development.
- Bootstrap Nucleus is the active scorer.
- A rudimentary bag seam now exists through the Emitter CLI.
- A late-Phase-1 baseline-leg sidecar pass has now clarified a new collaboration doctrine:
  - shared registry / shared visible state is the right collaboration baseline
  - human-driven shared-state viewing is proven
  - agent-driven visible action is still a bounded follow-up seam
- A minimal separate shared viewer sidecar now exists as the intended mainline collaboration surface:
  - DB path
  - query
  - mode (`fts` / `ann` / `bag`)
  - provider selection
  - visible shelf
  - selected-item detail pane
  - shared session JSON
  - JSONL event log
  - session-level control mode
  - last-action provenance
- A builder-only English triplet training loop now exists:
  - `_BDHyperNeuronEMITTER/tools/english_triplet_training_loop.py`
  - runtime-selected Ollama model
  - NDJSON-first output
  - SQLite/FTS uniqueness registry
  - required example families:
    - `anchor`
    - `semantic_match`
    - `structural_match`
    - `grammatical_nonsense`
    - `syntactic_shift`
  - current use:
    - controlled general-English corpus growth for later scorer / FFN work
    - not a live runtime feature
    - tracked permanent inputs now live under `_BDHyperNeuronEMITTER/tools/examples/`
    - current preferred broader general-English list:
      - `_BDHyperNeuronEMITTER/tools/examples/iambic-mnemonic-master/word-lists/basic-english-850.txt`
  - first real smoke:
    - `qwen2.5:0.5b`
    - `word_limit = 1`
    - accepted `5` example rows, rejected `1`
    - current read: generation path is real, but prompt/validator quality still needs tightening before larger corpus passes
- Corpus doctrine has also shifted:
  - general English first
  - then technical/project prose
  - then code/doc bridge corpora
  - code is now treated as a second variable, not the initial baseline footing
- We now have first non-Python pilot corpus baselines across text-heavy and mixed project material.
- The Emitter now supports a parallel traditional embedder lane beside the deterministic semantic path.
- A builder-side anisotropic blur lens now exists for query-neighborhood experiments over existing Cold Artifact DBs.
- The Emitter now has a native SQLite FTS fallback lane for ingest-time candidate recall experiments.
- The Bootstrap Nucleus now also has an optional origin-aware cross-document scoring branch behind profile control.
- We now have a real cross-document threshold control ladder on that branch, with a likely trust band around `0.50`–`0.65`.
- The Hot Engine bag propagation direction bug is now fixed.
- Post-fix bag checks make `0.58` look like the leading bag-first default candidate, with `0.55` close behind.
- We now also have a first five-vertex shock-load map on that `0.58` footing:
  - structural is the strongest current load-bearing surface
  - grammatical remains strongly active
  - verbatim is real but narrow
  - semantic is still mostly slack on the active deterministic/reference footing
- The bag view now also applies a light human-facing rerank:
  - prefers exact section/heading anchors when activations are close
  - exposes `rank_score` / `rank_signals` for inspection
  - keeps short section labels intact instead of collapsing them to snippets like `2.`
- The bag now also uses conservative lexical query variants for lexical anchor shaping.
- The bag rerank now has a refined origin-support seam:
  - small bonus only when multiple lexical variants independently point into the same origin
  - clearest current win: `eval input`
  - current remaining misses look more lexicalization-bound than graph-direction-bound
- We now also have first bounded semantic-gravity overlay results:
  - deterministic control/high: `10955 -> 12133`
  - sentence-transformers control/high: `3380 -> 3943`
  - current read: semantic behaves more like a long-range attraction field than a primary support beam
  - current warning: this is graph-strong, but still needs bag-side QC before becoming a default
- That bag-side QC has now started to come in:
  - deterministic control and deterministic high both preserve the same strong human-facing top shelf on the reference query set
  - both sentence-transformer variants lag behind on the same shelf
  - current read: the deterministic lane is not only graph-strong, it is also the better evidence-facing lane on this footing
- We now also have a compact deterministic semantic-gravity shape sweep:
  - `steep`, `softplus`, `high`, and `xhigh` all preserve the same human-facing top shelf on the current 11-query validation set
  - graph gains are now saturating rather than opening a wholly new regime
  - current read:
    - `steep` is the safest balanced candidate and is now the promoted safe default
    - `softplus` is the strongest practical compromise
    - `xhigh` is a useful stress point, not an obvious default
  - current profile organization:
    - `python_reference_origin_aware_crossdoc_v1_threshold_058_semantic_gravity_default_safe.json`
      - promoted safe default (`steep` shape)
    - `..._softplus.json`
      - stronger practical alternative
    - `..._high.json`
      - near-ceiling reference
    - `..._xhigh.json`
      - stress / saturation probe
- We now also have first mapping results for `verbatim` and `contradiction` on top of that safe semantic footing:
  - `verbatim_light` is basically neutral at the graph level and does not change the current 12-query bag top shelf
  - `verbatim_mid` / `verbatim_strong` steadily trim cross-document winners without compensating lift
  - current read: `verbatim` looks more like a precision / articulation-control surface than a bridge-growth surface
  - `contradiction_soft` is almost neutral and starts to produce explicit anti-signal reasons without collapsing the winner field
  - `contradiction_mid` prunes more but still does not improve cross-document pull
  - `contradiction_block` is too blunt as a general default on this footing
  - current best counter-pressure seed: `contradiction_soft`
- We now also have the first pairwise `verbatim` excursion map:
  - `verbatim + semantic` produces modest graph lift and sharply reduces cross-document losers as the pair mass increases
  - but the same pair does not improve articulation convergence on the tested bag shelf
  - current read:
    - graph-positive
    - articulation-neutral
    - increasingly geometry-collapsing at higher settings
  - that follow-up `verbatim + structural` test is now also complete:
    - it rotates the field toward `structural_bridge`
    - but it also does not improve articulation convergence on the tested bag shelf
  - current joint read:
    - pairwise weight steering alone is not solving articulation control
    - next likely articulation seam is retrieval/rerank behavior or finer-grain verbatim resolution
- We also clarified the next sane future verbatim-resolution seam:
  - live `CIS` is real, but only as hunk-level content-addressed dedupe plus verbatim text persistence
  - we do **not** yet have a full CAS / Merkle / BPE-backed verbatim layer
  - if we branch into finer verbatim resolution later, the sane starting shape is:
    - dedupe hardening
    - line/span-level sub-hunks
    - rudimentary scope traversal
  - explicit caution:
    - do not stack BPE + CAS + Merkle + full scope-walker work into one tranche
- The probe monitor is now a more useful observer surface too:
  - live metric cards
  - summary and sample tabs in the same window
  - five-surface color cues
  - typed `report_summary` / `report_snapshot` events behind the viewer
- The kept builder/sidecar tools that now matter to the saved app no longer depend on `.dev-tools`:
  - permanent tracked home: `_BDHyperNeuronEMITTER/tools/`
  - `.dev-tools` remains builder-only and disposable

## Broad tuning read

- We are past “does this idea work at all?” and into “which concrete constraints are still warping it?”
- The tuning phase is productive because it is isolating real bottlenecks instead of generating vague theory.
- The project is healthy:
  - the Splitter is producing meaningful multi-surface units
  - the Emitter is producing measurable graph behavior
  - the probe loop is visible, repeatable, and durable
- The most important shift is that we can now distinguish between:
  - bad signal
  - bad scorer math
  - bad comparison scope
  - and genuinely useful new signal lanes
- We can now also distinguish between:
  - a useful softer cross-document gate
  - and a too-permissive gate that starts admitting fragment-heavy bridge fabric
- The next doctrinal shift is also clearer:
  - the bag should be treated as a bounded observer-centered slice, not a whole-manifold activation
  - the project is missing a cleaner later retrieval control layer:
    - `scope root`
    - `resolution grammar`
    - `direction of spread`
    - `stop-unwinding`
- The next practical bag shift is also clearer:
  - bag usefulness is now constrained more by query/ranking behavior than by missing graph signal
  - `hop_limit = 1` is still the right human-facing regime
  - widening lexical seed count alone does not materially improve the current awkward cases
  - the remaining awkward cases now separate into:
    - ranking misses
    - lexicalization / alias misses
    - and cases where the best item is still not entering the candidate set cleanly
- The next Phase 1 framing is sharper too:
  - Phase 1 should not end when we find one lucky cross-document profile
  - Phase 1 should end when all five surfaces are individually mapped and functionally integrated in context
- Rotation testing clarified something important too:
  - keeping the same weight pattern but rotating it around the five surfaces does not preserve the lift
  - the field cares about orientation, not just numeric shape
- Semantic-shape testing clarified something important too:
  - once the deterministic semantic field is active, the next question is shape/saturation rather than raw existence
  - the bag shelf is stable across the tested deterministic semantic shapes, so the next choice is about preserving useful winner geometry rather than preventing obvious shelf breakage
  - the safe operational move is to keep one promoted default while preserving the shape family as a labeled option library
- Verbatim / contradiction mapping clarified something important too:
  - `verbatim` should not currently be treated like a second semantic field
  - the better hypothesis is that it helps control articulation, wording regime, or chosen framing inside an already-grounded neighborhood
  - contradiction is promising as a later trust-preserving counter-pressure, but only in softer forms
- First verbatim pair-mapping clarified something important too:
  - `verbatim + semantic` is not yet giving usable wording-control at the bag surface
  - it is giving semantic consolidation
  - so if the goal is chosen framing or articulation control, we should likely pivot to `verbatim + structural` next
- Second verbatim pair-mapping clarified something important too:
  - `verbatim + structural` also does not solve wording-control at the bag surface
  - so the next likely gain is not another naive pair excursion
  - it is more likely:
    - retrieval/rerank articulation logic
    - or finer-grain verbatim resolution
- Verbatim-resolution discussion clarified something important too:
  - current articulation limits may partly reflect missing finer lexical resolution in the field
  - but the right next move is not “jump straight to subword”
  - the right middle ground is likely line/span granularity with strong dedupe and simple scope movement first
- Query-side articulation strategy mapping clarified something important too:
  - on the live `det_steep` DB, the current bag shelf now sits at `same_top = 5`, `same_origin = 6`
  - `phrase_core` expansion is worse (`4 / 4`)
  - `identifier_norm` is effectively neutral (`5 / 6`)
  - `char_ngram` rerank is the first light query-side mover (`6 / 6`)
  - current read:
    - char n-gram overlap is the best next query-side articulation seam on the existing hunk field
    - phrase-core expansion is too blunt on this footing
    - identifier normalization alone does not add much yet
- We then promoted that bounded char n-gram seam into the live bag rerank:
  - first integrated articulation shelf: `same_top = 7`, `same_origin = 7`
  - the standalone char-ngram overlay is no longer additive because the live bag already includes it
  - a follow-up import-anchor tuning pass then closed the remaining miss:
    - punctuation-insensitive alias matching
    - bounded section-like trust for short anchored list items that look like true statement/label anchors
  - current integrated articulation shelf now sits at `same_top = 8`, `same_origin = 8`
  - current read:
    - the bag itself is now aligned across the full tested articulation shelf
    - current articulation work can stay bag/query-side until that line stops paying off
    - lexical-anchor breadth is now decoupled from final bag `top_k`, so the `module imports` import-anchor win survives narrow returned bags too
- BPE query-probe testing clarified something important too:
  - the current deterministic BPE space tied to the live `det_steep` DB is not yielding useful articulation neighbors on the Python-reference shelf
  - `0 / 16` articulation queries produced any concept-relevant readable nearest-token hits
  - current read:
    - do not wire BPE query expansion into this reference footing yet
    - if we revisit BPE later, it should be with corpus-aligned artifacts rather than this current field
- Plain vector-baseline comparison clarified something important too:
  - ordinary ANN/vector retrieval is now measured directly against the live bag on the same query shelf
  - deterministic ANN baseline:
    - `same_top = 4 / 16`
    - vector human-facing tops = `14 / 16`
    - bag human-facing tops = `15 / 16`
  - sentence-transformer ANN baseline:
    - `same_top = 8 / 16`
    - vector human-facing tops = `13 / 16`
    - bag human-facing tops = `14 / 16`
  - current read:
    - plain vector retrieval absolutely works as a real baseline
    - but it is flatter and less anchor-stable than the bag
    - the bag is retrieving a shaped evidence slice, not just nearest semantic neighbors
- The baseline-leg-sidecar real-English pass clarified something important too:
  - `tech_talks` was a much better natural-language footing than the dictionary baseline
  - `fts` was often the cleanest leg for explicit phrase queries
  - sentence-transformers ANN behaved most like a conventional semantic prose baseline
  - deterministic ANN could be provisioned on the same corpus, but on that footing it remained weaker as a standalone prose retriever
  - this branch should now be treated as a concluded diagnostic/reference seam rather than expanded indefinitely

## What tuning has already taught us

- Probe 001:
  - architecture works loosely
  - but graph behavior was grammar-collapsed
- Probe 002:
  - proved the collapse was a bootstrap-math problem
- Probe 003/004:
  - gave us a stable working Phase 1 baseline
- Probe 007:
  - showed sparse explicit refs alone were not enough
- Probe 010:
  - proved list/index representation creates a real new explicit signal lane
- Probe 011:
  - proved the Emitter comparison window was a major hidden limiter
- Probe 012:
  - proved targeted long-range comparison is viable
  - but candidate-selection v1 is still too weak to replace the wider-window gain
- Pilot corpus probe set 001:
  - proved the current pipeline can ingest real local text/project slices beyond the Python-reference harness
  - proved the rudimentary bag is already useful on both prose-heavy and mixed code/doc graphs
- Embedder comparison baseline 001:
  - proved the deterministic semantic lane is now runnable again
  - proved a cached sentence-transformer lane can be compared on the same bag workflow
  - on the current corpora, deterministic is outperforming the sentence model on cross-document pull and evidence usefulness
- Probe 013:
  - upgraded the long-range candidate path into a deterministic occurrence-level anchor registry
  - proved anchor ranking/common-term suppression changes behavior
  - but did not improve the `115` cross-document pull plateau on the Python reference list/index footing
- Probe 014:
  - added a native SQLite FTS cheap-fetch fallback behind the anchor-registry path
  - proved the fallback stays cheap on the Probe 013 footing (`63155` total pairs vs `62583`)
  - but did not improve the `115` cross-document pull plateau even though it selected `548` cross-document fallback candidates
- Probe 015/015b/015c:
  - landed contradiction v1 as a real inspectable anti-signal seam
  - proved naive contradiction pressure can suppress useful navigational traffic
  - proved the cleaned contradiction seam is safe but not the main bottleneck mover
- Probe 016:
  - falsified the idea that one FTS origin monopolizing the fallback lane is the main reason for the plateau
  - preserved the `115` plateau even after de-monopolizing the fallback lane
- Conversion diagnostics:
  - proved the current cross-document losers are mostly not near-threshold misses
  - showed the main loser population is structurally plausible cross-document pairs that still fail badly at conversion time
- Probe 017/018:
  - proved a post-change control replay still holds the current `115` plateau on the same Python-reference footing
  - proved the origin-aware cross-document scorer v1 lifts `cross-document nucleus pull` from `115` to `234` without increasing pair count
  - proved cross-document winners can shift from mostly `grammatical_dominant` to mostly `structural_bridge` plus `multi_surface`
- Probe 019/020/021:
  - turned the origin-aware branch into a rudimentary control gradient
  - showed the alternate cross-document fractions alone lift the footing to `150`
  - showed fractions + threshold scaling lift it to `228`
  - showed fractions + shared-anchor bonus lift it only to `155`
  - current read: the alternate cross-document lens matters, threshold scaling carries most of the extra lift, and the current shared-anchor seam is still weak on this footing
- Probe 022-033:
  - turned cross-document threshold scaling into a full control ladder on the same fixed pair budget (`62896`)
  - showed the old cross-document gate was far too strict
  - showed softer thresholds keep the winner field strongly `structural_bridge` / `statistical_echo` much deeper than expected
  - revealed a practical trust boundary:
    - `0.50`–`0.65` looks like the most promising band so far
    - `0.40` is the first warning zone
    - `0.30` looks too permissive and fragment-heavy
- Query experiment 001:
  - proved a builder-side anisotropic blur lens can be run safely over existing graph probes
  - showed the blur lens exposes neighborhood/topology information that the bag does not
  - also showed the blur is currently easier to hijack by dense local hubs than the bag
- Bag diagnostics post-origin-aware sweep:
  - confirmed the bag did not automatically improve just because graph pull improved
  - isolated a real Hot Engine bug: activation was propagating backward relative to stored edge direction
  - fixed that bug and added focused emitter tests
  - post-fix bag checks now show the graph improvements on human-facing queries such as:
    - `lexical analysis`
    - `encoding declarations`
    - `operator precedence`
  - current read:
    - `0.58` and `0.55` both beat `0.60` on the most interesting bag queries
    - `0.58` is currently the safer strong default candidate
    - `hop_limit = 2` and `3` still drift badly into index-heavy noise
    - dropping `index.txt` list-item anchors does not materially change the good-footing bag results
    - the bag view can now surface cleaner top items without mutating the graph itself
    - conservative query lexicalization plus refined origin-support reranking can now rescue `eval input`
    - but the remaining stubborn misses (`function definitions`, `lambda expressions`, `assignment expressions`, `operator precedence`) still look more like corpus-query wording mismatch than graph propagation failure

## Phase 2 readiness read

We are approaching Phase 2 readiness structurally, but not yet behaviorally.

### Structurally ready enough

- pipeline exists
- contracts exist
- probe/report loop exists
- builder-side visibility exists
- docs and onboarding are now strong enough for cold restart

### Not yet behaviorally ready enough

- candidate selection / comparison scope is still unsettled
- the current bootstrap still needs more than one static viewing regime for all relation types
- we do not yet have a disciplined “training data we trust” checkpoint
- semantic is still not fully alive as an active lane in the working probes
- the bag exists only as a first CLI evidence surface, not yet as the full STM-facing membrane
- semantic comparison against a traditional embedder is not yet wired into the bag workflow
- only one traditional sentence model has been compared so far (`sentence-transformers/all-MiniLM-L6-v2`)
- long-range candidate recall is still unresolved beyond anchor-bearing hunks
- long-range candidate recall is still unresolved even after anchor + FTS fallback v1
- origin-aware conversion is now materially better
- threshold sweeps show the graph can match and exceed the old Probe 011 pull count at fixed pair cost
- but we have not yet locked the trustworthy default regime for that lift
- the blur lens is informative, but not yet a trustworthy runtime retrieval surface
- the bag exists only as a first CLI slice/evidence seam, not yet as the full observer-centered STM membrane
- the later bag/walker doctrine is getting clearer, but it is not yet runtime behavior

### Practical meaning

- We should not jump to FFN yet.
- One more tranche of scorer/comparison-path refinement is the responsible move.
- If we moved to Phase 2 right now, we would risk teaching the FFN around unresolved scaffold defects instead of teaching it from a trustworthy interaction substrate.
- The immediate live blocker is now narrower:
  - the graph has moved far past the `115` plateau under origin-aware scoring
  - the remaining questions are:
    - where to set the cross-document trust boundary
    - and how to keep the bag human-usable on top of that stronger graph
- The next likely scorer experiment is now sharper:
  - keep the origin-aware cross-document branch
  - keep the stronger alternate cross-document fractions
  - refine threshold behavior inside the `0.50`–`0.65` band before widening the contract
  - treat the current shared-anchor seam as additive but still weak until later evidence proves otherwise

## What we just finished

- Added an optional `cross_document_profile` to the Bootstrap Nucleus config with:
  - cross-document-only surface fractions
  - cross-document threshold scaling
  - a shared-anchor structural bonus built only from current fields (`cross_refs`, `normalized_cross_refs`, `import_context`, and target hints)
- Added emitter tests proving:
  - old configs still load without the new profile block
  - disabled cross-document branching is inert
  - same-document behavior stays unchanged
  - shared-anchor bonuses appear only when the current contract actually supports them
- Added tracked profile:
  - `_BDHyperNeuronEMITTER/_docs/bootstrap_profiles/python_reference_origin_aware_crossdoc_v1.json`
- Ran Probe 017 control on the same Python-reference list/index footing as the current plateau:
  - `relations = 17457`
  - `cross-document nucleus pull edges = 115`
  - `training pairs total = 62896`
- Ran Probe 018 with origin-aware cross-document scoring v1:
  - `relations = 17592`
  - `cross-document nucleus pull edges = 234`
  - `training pairs total = 62896`
- That means the Phase 1 scorer does need to evaluate different relation classes differently:
  - the same-document path can stay close to the old footing
  - the cross-document path benefits from a different static lens
- The lift is real, but still partial:
  - `234` is materially better than `115`
  - but still far below Probe 011 `1175`
- Ran a three-profile ablation sweep after Probe 018:
  - fractions-only:
    - `cross-document nucleus pull edges = 150`
  - fractions + threshold scaling:
    - `cross-document nucleus pull edges = 228`
  - fractions + shared-anchor bonus:
    - `cross-document nucleus pull edges = 155`
- That gives us a usable control gradient:
  - the alternate cross-document lens is the first big move
  - threshold scaling carries most of the next lift
  - the current shared-anchor bonus contributes only lightly on this corpus/contract footing
- Ran a deeper threshold sweep on the same fixed pair budget:
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
- That changed the project read again:
  - the old cross-document threshold gate was much too strict
  - the graph can recover and exceed the old Probe 011 pull count without pair growth
  - but the weakest admitted winners become visibly shakier by `0.40`
  - `0.30` is now the first clearly too-permissive band
- Current next step:
  - fine-sweep and inspect weakest winners inside `0.50`–`0.65`
  - keep shared-anchor refinement secondary unless that band stalls
  - keep bag evaluation at `hop_limit = 1`
  - if `0.58` continues to hold its current bag quality, promote it as the first bag-first default candidate

- Re-centered the project after the old `final/` move-up.
- Verified the App Journal install and launcher path.
- Cleaned major runtime seams in Splitter and Emitter.
- Fixed Emitter UI lifecycle/thread handling so worker-thread UI updates are queued safely onto the main Tk thread.
- Wrote root architecture and recovery docs so the project can survive interruption cleanly.
- Started Splitter corpus hardening with the first recorded corpus baseline.
- Fixed blank fallback provenance (`extraction_engine`) and taught PEG to claim structured reST-style `.txt` reference docs.
- Fixed an NL parsing seam where indented literal blocks in `grammar.txt` were being mistaken for headings.
- Ran the first full Splitter → Emitter probe on the Python reference corpus and confirmed the graph is reacting to the stronger NL path.
- Turned the graph-probe pass into a repeatable measurement loop with a saved JSON report artifact and builder-side reporter tool.
- Inspected the bootstrap nucleus and confirmed the prose-heavy `grammatical_dominant` skew comes from coarse prose node-kind matching plus fixed Phase 1 weights.
- Ran Probe 002 after a first de-bias pass and confirmed the skew is reducible, but the first pass overcorrected and starved relation volume.
- Shipped builder-facing bootstrap scaffold dials through the Emitter CLI plus JSON profile loading.
- Added emitter-local tests for scaffold config validation and behavior.
- Verified default-config regression against Probe 002 and saved effective bootstrap profiles beside probe artifacts.
- Ran Probe 003 with the tracked starter profile and recovered graph volume substantially without returning to grammar collapse.
- Added a builder-only probe monitor under `.dev-tools/final-tools/tools/probe_monitor.py`.
- Verified the monitor writes live `probe_events.jsonl` and `probe_run.log` artifacts under `_docs/_analysis/<probe>/`.
- Added an optional tiny builder monitor window while preserving machine-readable outputs and keeping the shipped app free of `.dev-tools` coupling.
- Updated the final-tools smoke test and example jobs so the probe monitor is part of the validated builder toolbox.
- Ran Probe 004 through the live builder monitor and confirmed it reproduces the Probe 003 footing exactly.
- Fixed the monitor `hold_open` path by moving the tiny Tk viewer into its own helper process so it can stay open for review without crashing the probe runner.
- Ran Probe 005 with a profile-only structural -> statistical shift and confirmed it hurts relation volume while also lowering cross-document pull.
- Ran Probe 006 with a heading-specific grammatical boost and confirmed it does not improve cross-document pull over the Probe 003/004 footing.
- Added a narrow explicit-reference structural dial to the Bootstrap Nucleus and ran Probe 007 against the same corpus through the live monitor.
- Probe 007 added exactly one extra above-threshold relation, but it was an in-document fragment pair; cross-document pull remained flat at `169`.
- That strongly suggests the current `cross_refs` signal in this corpus is too sparse or too weakly extracted to unlock the next gain by scorer-side boosting alone.
- Added a Splitter-owned signal control layer with builder-facing JSON profiles and wired it through the Splitter CLI as `--signal-profile`.
- Kept the runtime HyperHunk contract flat but facet-ready by adding optional fields for:
  - `normalized_cross_refs`
  - `reference_kinds`
  - `list_role`
  - `list_depth`
  - `reference_confidence`
- Added Splitter tests covering profile validation, deterministic reST-style reference normalization, list-item emission, and fragment inheritance behavior.
- Taught the builder-side probe monitor to persist `splitter_signal_profile_effective.json` beside the existing bootstrap profile and graph artifacts.
- Ran Probe 008 as the default-profile regression for the Splitter signal-control tranche and confirmed it matches the stable Probe 003/004 footing exactly.
- Ran Probe 009 with `_BDHyperNodeSPLITTER/_docs/signal_profiles/python_reference_richer_refs_v1.json` through the live monitor.
- Probe 009 did not change graph metrics over Probe 008:
  - `relations = 13510`
  - `cross-document nucleus pull edges = 169`
  - `above-threshold training pairs = 12249`
- Splitter-side signal inspection showed why:
  - the Python reference text corpus still yields only `2` ref-bearing hunks
  - only `1` unique normalized target is being extracted (`shortstring_longstring`)
  - so the new control layer is working, but the active corpus export still lacks enough explicit reference material to move the cross-document metric
- Added a list/index-focused Splitter signal profile at `_BDHyperNodeSPLITTER/_docs/signal_profiles/python_reference_list_index_v1.json`.
- Taught list-item emission to infer section-like targets such as `lexical_analysis`, `execution_model`, and `line_structure` from navigational lists.
- Probe 010 proved that this richer navigational lane is real:
  - `1275` hunks
  - `79` ref-bearing hunks
  - `77` unique normalized targets
- But Probe 010 also showed the current bootstrap turns that into stronger local structure more than better cross-document pull:
  - `relations = 17392` (`+3882` vs Probe 009)
  - `above-threshold training pairs = 15963`
  - `cross-document nucleus pull edges = 115` (`-54` vs Probe 009)
- So the new list/index lane is promising as extracted signal, but it is not yet the new behavioral baseline.
- Exposed the Emitter comparison window as a builder dial (`--window-size`) and passed it through the builder probe monitor.
- Probe 011 reran the same list/index profile with `window_size = 200`.
- Probe 011 changed the picture dramatically:
  - `relations = 22978`
  - `cross-document nucleus pull edges = 1175`
  - `above-threshold training pairs = 21549`
- That means recency clipping was a major hidden limiter. The list/index lane was useful, but the default `window_size = 50` was preventing many index-to-target comparisons from ever occurring.
- New tradeoff:
  - the gain is real
  - but training pairs exploded from `62475` in Probe 010 to `234900` in Probe 011
  - so the next question is now about smarter candidate selection, not just richer extraction
- Added a targeted reference-aware candidate-selection path in the Emitter so a new hunk can compare against older prior hunks when normalized refs / target hints line up, even if those hunks have fallen out of the local sliding window.
- Probe 012 tested that path with the normal `window_size = 50` and `reference_candidate_limit = 24`.
- Probe 012 proved the candidate path works mechanically:
  - the concrete `index.txt li_4 -> lexical_analysis.txt h1_2_lexical_analysis` pair now lands above threshold without using `window_size = 200`
- But Probe 012 did **not** recover the full Probe 011 corpus-wide gain:
  - `relations = 19602`
  - `cross-document nucleus pull edges = 115`
  - `above-threshold training pairs = 18173`
- So the pause-point truth is now:
  - list/index signal is real
  - window clipping was real
- targeted candidates work on specific pairs
- but candidate-selection v1 is not yet broad or well-ranked enough to replace the brute-force wider window
- Builder-side probe artifact location is now configurable through `.dev-tools/final-tools/tools/probe_monitor.py` via `artifact_root`.
- This matters operationally because full `training_pairs_*.json` exports can become multi-GB files and should live on a larger builder storage drive when needed.
- The preferred policy is now one user-set builder-artifact home via `.dev-tools/final-tools/builder_settings.local.json`, with per-run `artifact_root` treated as an override rather than the normal workflow.
- On this machine, the builder-artifact home is configured externally and `_docs/_analysis` is a junction into that external probe library, so legacy project paths still resolve while storage lives off the app drive.
- Added the first rudimentary Bag of Evidence CLI seam via `_BDHyperNeuronEMITTER/src/app.py` command `bag`.
- The current bag is intentionally narrow:
  - ranked evidence items from the existing retrieval path
  - grouping by `origin_id`, `node_kind`, or `structural_root`
  - item / group / whole-bag summaries
  - pullback-ready text for selected occurrence ids
- This is enough for external-agent inspection and STM pullback experiments, but not yet the full bag membrane architecture.
- Ran a first new-material pilot corpus set end to end:
  - `_corpus_examples/tech_talks`
  - `_corpus_examples/Paradigm`
  - `_corpus_examples/_AppBuilderTOOLBOX`
- Verified all three through the full builder probe pipeline with artifacts saved to the external records library and mirrored via `_docs/_analysis/`.
- Recorded first bag artifacts on the new corpora:
  - `tech_talks_probe_001/bag_query_memory_graph.json`
  - `paradigm_probe_001/bag_query_identity.json`
  - `appbuilder_toolbox_probe_001/bag_query_mcp_server.json`
- New pilot results:
  - `tech_talks_probe_001`
    - `5106` occurrence nodes
    - `160088` relations
    - `1227` cross-document nucleus pull edges
    - bag query `"memory graph"` surfaced useful evidence concentrated in `Another Crazy Convo.txt`
  - `paradigm_probe_001`
    - `177` occurrence nodes
    - `3498` relations
    - `2422` cross-document nucleus pull edges
    - bag query `"identity"` surfaced evidence across four source files
  - `appbuilder_toolbox_probe_001`
    - `883` occurrence nodes
    - `11687` relations
    - `2269` cross-document nucleus pull edges
    - bag query `"mcp server"` surfaced mixed code/doc evidence from `mcp_server.py`, `journal_store.py`, and `tool_pack.py`
- Re-ran current automated validation after the new corpus passes:
  - `python -m unittest discover _BDHyperNodeSPLITTER/tests -v`
  - `python -m unittest discover _BDHyperNeuronEMITTER/tests -v`
  - `python .dev-tools/final-tools/smoke_test.py`
  - all passed
- Fixed a real training seam in the deterministic semantic path:
  - `compute_counts()` was returning a tuple while `cmd_train()` expected named fields
  - the deterministic train command now handles the current return shape and produces usable artifacts again
- Added parallel embedder controls:
  - `emit --embedder auto|deterministic|sentence-transformers|none`
  - `emit --sentence-model <model>`
  - `bag --embedder-override ...`
- Probe bundles now persist `embedding_provider_effective.json` so bag/query can infer the correct query embedder from the DB bundle itself.
- Ran the first side-by-side embedder comparison on two corpora:
  - `tech_talks_probe_002_det`
    - `141879` relations
    - `1670` cross-document nucleus pull edges
    - bag query `"memory graph"` surfaced a broader evidence mix across `Another Crazy Convo.txt`, `master_spec_text.txt`, and `MicroserviceLIBRARY_...`
  - `tech_talks_probe_003_st`
    - `155790` relations
    - `1372` cross-document nucleus pull edges
    - bag query `"memory graph"` collapsed more heavily toward `master_spec_text.txt`
  - `appbuilder_toolbox_probe_002_det`
    - `23676` relations
    - `4154` cross-document nucleus pull edges
    - strong `multi_surface` and `semantic_resonance` presence
    - bag query `"mcp server"` surfaced a broader mixed evidence set across `README.md`, `journal_store.py`, `tool_pack.py`, `mcp_server.py`, and `scaffolds.py`
  - `appbuilder_toolbox_probe_003_st`
    - `14836` relations
    - `3232` cross-document nucleus pull edges
    - bag query `"mcp server"` still worked, but with a narrower and more code-heavy evidence mix
- Current read from comparison baseline 001:
  - the sentence-transformer lane is integrated and usable
  - but the deterministic lane is currently stronger on both corpora we tested
  - this means our own five-surface/deterministic geometry is carrying more of the retrieval burden than a default off-the-shelf sentence model in the current prototype shape
- Replaced the simple in-memory reference-token index in `GraphAssembler` with a ranked occurrence-level anchor registry:
  - headings register as stronger anchors than generic cross-refs
  - list/index targets remain the mid-weight anchor lane
  - overly common anchor terms are now suppressed instead of continuing to flood long-range recall
- Added emitter tests proving:
  - a heading anchor beats a weaker list-ref-only match when the long-range candidate budget is capped
  - overly common anchor terms are suppressed once they exceed the configured threshold
- Ran `reference_probe_013_anchor_registry_v1` against the same Python reference footing as Probe 012:
  - Splitter profile: `python_reference_list_index_v1.json`
  - Bootstrap profile: `python_reference_prose_tuning.json`
  - `window_size = 50`
  - `reference_candidate_limit = 24`
- Probe 013 results:
  - `relations = 17428`
  - `cross-document nucleus pull edges = 115`
  - `above-threshold training pairs = 15999`
- Interpretation:
  - the anchor registry made the targeted long-range path more selective
  - but it did **not** recover the Probe 011 wide-window gain
  - this means anchor-only recall is still too narrow for the next lift
  - the likely next step is a deterministic cheap-fetch fallback, probably by reusing SQLite FTS when anchor recall returns too little signal
- Added a native SQLite FTS fallback lane to the Emitter:
  - `emit --fts-candidate-limit <N>`
  - `emit --fts-fallback-thin-threshold <N>`
  - shared FTS lookup now goes through a narrow local seam instead of raw SQL duplication in the assembler
- Ran `reference_probe_014_fts_fallback_v1_run2` against the same Python-reference footing:
  - Splitter profile: `python_reference_list_index_v1.json`
  - Bootstrap profile: `python_reference_prose_tuning.json`
  - `window_size = 50`
  - `reference_candidate_limit = 24`
  - `fts_candidate_limit = 24`
  - `fts_fallback_thin_threshold = 2`
- Probe 014 results:
  - `relations = 17457`
  - `cross-document nucleus pull edges = 115`
  - `above-threshold training pairs = 16028`
  - `training pairs total = 63155`
  - `fts_selected_cross_doc = 548`
- Interpretation:
  - the FTS fallback is cheap enough to keep studying
  - but v1 did **not** convert selected fallback recall into actual new cross-document pull
  - the next likely move is to explain why the fallback is not converting:
    tighten trigger rules, improve deterministic FTS query lexicalization/ranking, and inspect scorer rejection patterns on recovered pairs
- Added builder-side query experiment tool:
  - `.dev-tools/final-tools/tools/anisotropic_blur_probe.py`
- Anisotropic blur experiment 001 on `reference_probe_013_anchor_registry_v1` with query `"lexical analysis"`:
  - seeds were sensible and cross-document (`index.txt`, `lexical_analysis.txt`, `introduction.txt`, `expressions.txt`)
  - but the blur collapsed into dense `index.txt` list-item neighborhoods
  - top-cross-document count in the blur top set was `0`
  - the current bag remained more source-diverse and more evidentially useful on the same query
- Anisotropic blur experiment 001 on `appbuilder_toolbox_probe_002_det` with query `"mcp server"`:
  - the blur surfaced a strong procedural neighborhood around `smoke_test.py` and several `src/tools/*.py` functions
  - top-cross-document count in the blur top set was `4`
  - the current bag remained more directly relevant to the external-agent use case (`README.md`, `tool_pack.py`, `mcp_server.py`, `journal_store.py`)
- Current read from the blur line:
  - it is useful as a builder-side neighborhood/field diagnostic
  - it is not yet better than the bag as a relevance/evidence surface
  - it should stay out of runtime for now
- Added contradiction v1 as a narrow explicit anti-signal seam in the Bootstrap Nucleus and export path.
- Ran Probe 015 control plus contradiction variants and confirmed:
  - contradiction is now inspectable and safe to keep in-tree
  - but it is not the main bottleneck mover on the Python reference footing
- Added hub/source concentration reporting and an FTS per-origin cap, then ran Probe 016.
- Confirmed Probe 016 does not change the `115` plateau even though the fallback lane becomes less monopolized by any one origin.
- Upgraded the builder-side conversion reporting so winner/loser cross-document patterns can be compared directly.
- Confirmed the sharper current read:
  - the graph is finding long-range candidates
  - the scorer is still under-converting structurally plausible cross-document bridges
- Clarified the future bag/walker doctrine:
  - bag as bounded observer-centered slice
  - current node as anchor
  - later retrieval needs `scope root`, `resolution grammar`, `direction of spread`, and `stop-unwinding`
  - this is planning truth, not current runtime implementation

## What to do next

Next tranche: **origin-aware lens refinement + delayed shared-target decision**

1. Choose the next targeted change:
  - refine the origin-aware cross-document fractions and threshold behavior and measure whether `234` can move higher without pair growth, or
  - decide whether the current partial outbound-reference seam is too weak and needs a later shared-target neighborhood tranche only after the lens/threshold line stops paying off, or
  - compare at least one more traditional model or query strategy against the current deterministic footing
2. Keep blur work diagnostic only unless a later pass can prove:
   - less hub collapse
   - better cross-document spread
   - and better evidence usefulness than the bag
3. Keep bag work narrow and agent-facing:
   - evidence list
   - summary lenses
   - pullback into STM
4. Do not widen into UI or full bag orchestration until the CLI bag payload feels useful.
5. When disk pressure matters, run probes with the external builder artifact home instead of writing raw exports on the app drive.

## One-line read

The graph is real, the bag is validated, and origin-aware cross-document scoring plus threshold control has finally exposed the latent cross-document bridge layer. The next job is to choose the trustworthy default band for that lift.

## Do not drift into yet

- FFN Nucleus
- full bag orchestration / UI buildout
- big retrieval redesign
- broad polishing passes

## Read in this order if resuming cold

1. `_docs/WE_ARE_HERE_NOW.md`
2. `_docs/ARCHITECTURE.md`
3. `_docs/TODO.md`
4. `_docs/DEV_LOG.md`
5. `_docs/SPLITTER_CORPUS_BASELINES.md`
6. `_docs/GRAPH_PROBES.md`
7. `_docs/FACET_READY_SURFACE_DESIGN.md`
8. `_docs/QUERY_EXPERIMENTS.md`
9. `_docs/NL_NarrativeDESC.md`
10. `_docs/PARKING_LOT_QUESTIONS.md`
11. `.dev-tools/final-tools/jobs/examples/probe_monitor.json`
12. App Journal entries:
   - `journal_resume_checkpoint_20260327`
   - `journal_splitter_corpus_baseline_001`
   - `journal_backlog_001`
   - `journal_pilot_corpus_probe_set_001_20260330`
   - `journal_embedder_comparison_baseline_001_20260330`
   - `journal_anisotropic_blur_experiment_001_20260330`
   - `journal_3e9561e03e68`

## Quick sanity checks

```powershell
python _BDHyperNodeSPLITTER/src/app.py --help
python _BDHyperNeuronEMITTER/src/app.py --help
python .dev-tools/_app-journal/tools/journal_manifest.py run --input-json "{\"project_root\":\"C:/Users/jacob/Documents/_AppDesign/_LivePROJECTS/BDNeuralTranslationSUITE\"}"
```

## Known truth about the docs

- `_docs/ARCHITECTURE.md` is the root doctrine.
- `_docs/_BagOfEVIDENCE.md` is legacy context, not active architecture truth.
