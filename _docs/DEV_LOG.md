# BDNeuralTranslationSUITE — Dev Log

_Last updated: 2026-04-02. Journal mirror lives in `_docs/_journalDB/app_journal.sqlite3`._

---

## 2026-04-02 — Baseline-leg sidecar reintegration doctrine

Journal entry: pending mirror

- Treated the `baseline-leg-sidecar` work as a concluded diagnostic/reference branch rather than a second product line.
- Promoted the collaboration doctrine into mainline-facing docs:
  - shared registry as truth surface
  - `sync -> think -> act -> resync`
  - human-driven shared-state viewing is proven
  - agent-driven visible panel action remains a bounded follow-up seam
- Added a mainline-facing workflow note:
  - `_docs/SHARED_REGISTRY_WORKFLOW.md`
- Updated the builder constraint contract with:
  - `shared registry`
  - `shared visible workflow`
  - a new shared-registry synchronization rule
- Reframed corpus doctrine from narrow reference/code footing toward:
  - general English first
  - then technical/project prose
  - then code/doc bridge corpora
- Marked the minimal shared viewer as a separate sidecar direction in the tool docs.
- Kept the pending-action seam explicitly experimental by default:
  - `_BDHyperNeuronEMITTER/tools/baseline_leg_viewer.py` now requires `--enable-panel-actions` before it will try to consume queued panel actions
  - `_BDHyperNeuronEMITTER/tools/baseline_leg_panel_action.py` is now explicitly documented as experimental
- Moved the kept sidecar/shared-registry seam and English triplet generator out of `.dev-tools` into the tracked permanent home:
  - `_BDHyperNeuronEMITTER/tools/`
  - this includes the shared viewer/session/lib seam, the experimental panel-action helper, example job JSON, and the tracked general-English word-list pack
- Added branch conclusion note:
  - `_docs/_branch_baseline_leg/CONCLUSION.md`

Current read:
- the branch succeeded as a diagnostic experiment
- the shared viewer is worth carrying forward in minimal form
- the bugged pending-action seam should not be treated as mainline truth
- the next real corpus step is a functional English baseline, not broader workflow experimentation

---

## 2026-04-01 — Monitor hardening + semantic-gravity shape QC

Journal entry: pending mirror

- Upgraded the builder probe monitor UI:
  - clearer live metric cards
  - summary and sample tabs in the same window
  - five-surface color cues
  - the window now shows both the headline numbers and example source/target evidence
- Hardened the monitor event path:
  - `probe_monitor.py` now emits typed `report_summary` and `report_snapshot` events
  - `probe_monitor_viewer.py` can refresh the in-window summary/sample panels from those typed events
  - the old file-backed event stream is still the underlying transport, but the UI is no longer depending only on re-reading the saved report
- Fixed the reference probe launcher so deterministic monitor runs resolve the correct artifacts directory:
  - `_parts/_BDHyperNeuronEMITTER/artifacts` when present
- Validation:
  - emitter suite:
    - `python -m unittest discover _BDHyperNeuronEMITTER/tests -v`
    - `46/46` passing
  - monitor smoke:
    - `reference_probe_076_monitor_typed_event_smoke`
    - completed cleanly with typed report events and full probe bundle output

- Ran a compact deterministic semantic-gravity shape sweep on top of the active anchor lens:
  - Probe 073 `steep`
  - Probe 074 `softplus`
  - Probe 075 `xhigh`
- Combined with the earlier deterministic ladder:
  - control: `10955`
  - low: `11697`
  - mid: `12052`
  - steep: `12067`
  - softplus: `12106`
  - high: `12133`
  - xhigh: `12159`
- Read:
  - graph gains are now saturating rather than revealing a new regime
  - `xhigh` adds only marginal gain over `high`
  - `steep` preserves more `multi_surface` / `structural_bridge` winner geometry
  - `softplus` looks like the strongest practical compromise

- Ran a compact bag validation shelf across:
  - deterministic control
  - deterministic steep
  - deterministic softplus
  - deterministic high
  - deterministic xhigh
- Query shelf:
  - `lexical analysis`
  - `encoding declarations`
  - `yield expressions`
  - `operator precedence`
  - `assignment expressions`
  - `lambda expressions`
  - `function definitions`
  - `import statements`
  - `resolution of names`
  - `eval input`
  - `interactive input`
- Result:
  - all four semantic-shape variants preserved the same top shelf as deterministic control on `11/11` queries
  - current conclusion:
    - the choice is now about preserving useful winner geometry, not about preventing obvious bag breakage

Artifacts:
- `_docs/SESSION_CLOSE_REPORT_2026-04-01.md`
- `_docs/_analysis/bag_semantic_shape_qc_2026-04-01/bag_semantic_shape_qc_2026-04-01.md`
- `_docs/_analysis/bag_semantic_shape_qc_2026-04-01/bag_semantic_shape_qc_2026-04-01.json`
- `_docs/_analysis/reference_probe_076_monitor_typed_event_smoke`

---

## 2026-04-01 — Verbatim participation + contradiction counter-pressure mapping

Journal entry: pending mirror

- Mapped a first `verbatim` overlay family on top of the promoted safe deterministic semantic footing:
  - Probe 078 `verbatim_light`
  - Probe 079 `verbatim_mid`
  - Probe 080 `verbatim_strong`
- Result:
  - baseline `det_steep`: `12067` cross-document winners
  - `verbatim_light`: `12064`
  - `verbatim_mid`: `12051`
  - `verbatim_strong`: `11995`
- Read:
  - verbatim is participating, but not as a growth or long-range bridge lever
  - light promotion is survivable
  - stronger promotion steadily trims the winner field
  - current best hypothesis: `verbatim` is an articulation / framing control surface rather than a second semantic field

- Mapped a first contradiction counter-pressure family on the same footing:
  - Probe 081 `contradiction_soft`
  - Probe 082 `contradiction_mid`
  - Probe 083 `contradiction_block`
- Result:
  - `contradiction_soft`: `12070` cross-document winners
  - `contradiction_mid`: `12036`
  - `contradiction_block`: `12036`, but total relations drop sharply to `54839`
- Read:
  - soft contradiction is almost neutral and begins to emit explicit anti-signal reasons without collapsing the winner field
  - medium contradiction prunes more noticeably but does not create new lift
  - hard block is too blunt on this footing
  - current best counter-pressure seed: `contradiction_soft`

- Ran a focused bag shelf check across:
  - `det_steep`
  - `verbatim_light`
  - `contradiction_soft`
  - `contradiction_mid`
- Query shelf size:
  - `12`
- Result:
  - all four profiles preserved the same top item on `12/12` queries
- Current conclusion:
  - neither verbatim light nor soft contradiction is a major top-shelf mover yet
  - both should currently be treated as subtle field shapers rather than headline bag improvers

Artifacts:
- `_docs/_analysis/verbatim_contradiction_mapping_2026-04-01/verbatim_contradiction_mapping_2026-04-01.md`
- `_docs/_analysis/bag_verbatim_contradiction_qc_2026-04-01/bag_verbatim_contradiction_qc_2026-04-01.md`
- `_docs/_analysis/bag_verbatim_contradiction_qc_2026-04-01/bag_verbatim_contradiction_qc_2026-04-01.json`

---

## 2026-04-01 — First pairwise `verbatim + semantic` excursion map

Journal entry: pending mirror

- Built the first pairwise `verbatim` family with a coupled `semantic + verbatim` orientation.
- Method:
  - keep the promoted safe deterministic semantic footing as the anchor lens
  - preserve the baseline `semantic:verbatim` ratio (`2:1`)
  - push the pair mass outward while shrinking `grammatical`, `structural`, and `statistical` proportionally

- Probe ladder:
  - Probe 084 `pair_020`
  - Probe 085 `pair_028`
  - Probe 086 `pair_038`
  - Probe 087 `pair_050`

- Graph read:
  - baseline `det_steep`: `12067` cross-document winners
  - `pair_020`: `12112`
  - `pair_028`: `12157`
  - `pair_038`: `12180`
  - `pair_050`: `12190`
  - losers collapse sharply as the pair mass rises
  - but winner geometry becomes almost pure `semantic_resonance`

- Bag articulation read:
  - used an articulation shelf with alternate phrasings:
    - `lambda expressions` / `anonymous functions`
    - `assignment expressions` / `walrus operator`
    - `function definitions` / `def statements`
    - `resolution of names` / `name lookup`
    - `interactive input` / `repl input`
    - `encoding declarations` / `source encoding comments`
    - `import statements` / `module imports`
    - `yield expressions` / `generator yield`
  - result:
    - no profile in the pair family improved same-top or same-origin convergence beyond the safe baseline
  - current read:
    - this pair is graph-positive but articulation-neutral on the tested shelf
    - it looks more like semantic consolidation than usable wording-control

- Current conclusion:
  - do not promote this pair family as a default
  - likely next articulation candidate: `verbatim + structural`

Artifacts:
- `_docs/_analysis/verbatim_semantic_pair_mapping_2026-04-01/verbatim_semantic_pair_mapping_2026-04-01.md`
- `_docs/_analysis/bag_verbatim_semantic_articulation_qc_2026-04-01/bag_verbatim_semantic_articulation_qc_2026-04-01.md`
- `_docs/_analysis/bag_verbatim_semantic_articulation_qc_2026-04-01/bag_verbatim_semantic_articulation_qc_2026-04-01.json`

---

## 2026-04-01 — Second pairwise `verbatim + structural` excursion map

Journal entry: pending mirror

- Built the second pairwise `verbatim` family with a coupled `structural + verbatim` orientation.
- Method:
  - same safe deterministic anchor lens
  - preserve the live structural:verbatim ratio
  - push the pair mass outward while shrinking `grammatical`, `statistical`, and `semantic`

- Probe ladder:
  - Probe 088 `structpair_052`
  - Probe 089 `structpair_060`
  - Probe 090 `structpair_072`
  - Probe 091 `structpair_082`

- Graph read:
  - `structpair_052`: slight structural lift with mixed field still alive
  - `structpair_060`: no meaningful headline gain
  - `structpair_072`: structural rotation, rising losers
  - `structpair_082`: structural takeover, clear degradation

- Bag articulation read:
  - reused the same articulation shelf as the `verbatim + semantic` pair family
  - result:
    - no profile in the structural pair family improved same-top or same-origin convergence beyond the safe baseline

- Current conclusion:
  - `verbatim + structural` changes field orientation, but does not improve articulation control on the tested shelf
  - together with the earlier `verbatim + semantic` result, this suggests naive pairwise weight steering is not enough to solve articulation behavior
  - likely next articulation seam:
    - retrieval/rerank behavior
    - or finer-grain verbatim resolution

Artifacts:
- `_docs/_analysis/verbatim_structural_pair_mapping_2026-04-01/verbatim_structural_pair_mapping_2026-04-01.md`
- `_docs/_analysis/bag_verbatim_structural_articulation_qc_2026-04-01/bag_verbatim_structural_articulation_qc_2026-04-01.md`
- `_docs/_analysis/bag_verbatim_structural_articulation_qc_2026-04-01/bag_verbatim_structural_articulation_qc_2026-04-01.json`

---

## 2026-04-01 — Future verbatim-resolution seam clarified

Journal entry: pending mirror

- Clarified the current `CIS` truth boundary:
  - live runtime `CIS` is real as hunk-level content-addressed dedupe plus verbatim text persistence
  - it is not yet a full CAS / Merkle / BPE-backed verbatim system

- Clarified the likely articulation-control limitation:
  - current field strength is mostly at hunk / structural / heading / word-ish overlap resolution
  - this likely contributes to weak phrasing-shift / alternate-articulation control

- Chose the sane future middle ground rather than jumping straight to full subword infrastructure:
  - dedupe hardening first
  - then line/span-level sub-hunks
  - then rudimentary scope traversal

- Explicitly deferred:
  - full BPE-backed verbatim storage
  - full CAS/Merkle rollout
  - full walker/scope membrane work
  - all in the same tranche

- Current read:
  - this is a future branch worth keeping alive
  - but it should land as a restrained architecture seam, not as a simultaneous multi-system explosion

---

## 2026-04-01 — Query-side articulation strategy probe + contained BPE check

Journal entry: pending mirror

- Built a small repeatable builder-side comparison harness:
  - `.dev-tools/final-tools/tools/query_articulation_strategy_probe.py`
- Purpose:
  - burn through lightweight query-side articulation avenues before touching ingest or splitter granularity
  - compare:
    - baseline alias-aware bag behavior
    - `phrase_core` expansion
    - `identifier_norm`
    - `char_ngram` rerank

- Live `det_steep` articulation shelf result:
  - baseline: `same_top = 5`, `same_origin = 6`
  - `phrase_core`: `4 / 4`
  - `identifier_norm`: `5 / 6`
  - `char_ngram`: `6 / 6`

- Read:
  - char n-gram overlap is the first lightweight query-side articulation seam that actually improves the current shelf
  - phrase-core expansion is too blunt on this footing
  - identifier normalization alone is basically neutral
  - this keeps the next likely articulation move on the bag/query side, not the ingest side

- Also ran a contained BPE query-time probe against the same `det_steep` footing:
  - asked the deterministic BPE field for readable nearest-token neighbors on the articulation shelf
  - result: `0 / 16` queries produced any concept-relevant readable hits

- Read:
  - the active deterministic BPE field tied to this DB is not the right articulation field for the Python-reference shelf
  - do not wire BPE query expansion into this footing yet
  - if BPE is revisited later, it should be with corpus-aligned artifacts rather than the current field

Artifacts:
- `_docs/_analysis/query_articulation_strategy_probe_2026-04-01/query_articulation_strategy_probe.md`
- `_docs/_analysis/query_articulation_strategy_probe_2026-04-01/query_articulation_strategy_probe.json`
- `_docs/_analysis/bpe_query_articulation_probe_2026-04-01/bpe_query_articulation_probe_2026-04-01.md`
- `_docs/_analysis/bpe_query_articulation_probe_2026-04-01/bpe_query_articulation_probe_2026-04-01.json`

---

## 2026-04-01 — Bounded char-ngram seam promoted into the live bag rerank

Journal entry: pending mirror

- Promoted the bounded char-trigram overlap term into:
  - `_BDHyperNeuronEMITTER/src/core/engine/inference/bag_view.py`
- Kept it deliberately small and bag-side:
  - no graph-schema changes
  - no ingest changes
  - no durable score mutation

- Added focused bag tests:
  - verifies char-ngram can help a better articulation-fit section label outrank a wrong nearby heading
  - verifies articulation aliases still surface the right section anchor even when a generic paragraph echoes the alternate phrasing

- Validation:
  - `python -m unittest discover _BDHyperNeuronEMITTER/tests -v`
  - result: `49/49` passing

- Live articulation shelf result after integration:
  - baseline bag now sits at `same_top = 7`, `same_origin = 7`
  - the earlier standalone `char_ngram` overlay is no longer additive because the live bag already contains that seam

- Read:
  - the bag itself is now much stronger on same-concept/different-wording pairs
  - the main remaining articulation miss is now narrow:
    - `import statements` / `module imports`
  - this means the next articulation work can stay tightly focused on the import-style miss rather than the whole shelf

Artifacts:
- `_docs/_analysis/query_articulation_strategy_probe_2026-04-01_live_char_ngram/query_articulation_strategy_probe.md`
- `_docs/_analysis/query_articulation_strategy_probe_2026-04-01_live_char_ngram/query_articulation_strategy_probe.json`

---

## 2026-04-01 — Import-anchor articulation pass closes the shelf

Journal entry: pending mirror

- Followed the live char-ngram integration with one bounded import-focused rerank pass in:
  - `_BDHyperNeuronEMITTER/src/core/engine/inference/bag_view.py`
- Goal:
  - close the last articulation miss (`import statements` / `module imports`) without destabilizing the rest of the shelf

- What changed:
  - added punctuation-insensitive match normalization for query/alias phrase checks
  - widened section-like trust to short anchored list items only when they look like true statement/label anchors
  - explicitly avoided giving that extra trust to comma-fragment grammar list items

- Why:
  - the clean anchor `* "import" statements.` already existed in the bag
  - it was losing to broad import-origin prose because:
    - alias matching was too punctuation-literal
    - non-index short anchored list items were not trusted as section-like articulation anchors

- Validation:
  - focused bag tests:
    - `python -m unittest _BDHyperNeuronEMITTER.tests.test_bag_view -v`
    - `9/9` passing
  - full emitter suite:
    - `python -m unittest discover _BDHyperNeuronEMITTER/tests -v`
    - `50/50` passing
  - `py_compile` clean for:
    - `_BDHyperNeuronEMITTER/src/core/engine/inference/bag_view.py`
    - `.dev-tools/final-tools/tools/query_articulation_strategy_probe.py`

- Live articulation shelf result:
  - prior integrated live shelf: `same_top = 7`, `same_origin = 7`
  - after import-anchor tuning: `same_top = 8`, `same_origin = 8`

- Read:
  - the bag/query layer is still producing real articulation gains without a new ingest branch
  - the full tested eight-pair articulation shelf is now aligned on the baseline live bag path
  - this keeps the next likely branch as:
    - more bag/query articulation work while it is still paying off
    - finer-grain ingest only after that line plateaus
  - follow-up broader sanity check exposed a `top_k` sensitivity on `module imports`
  - that was then closed immediately by decoupling lexical-anchor breadth from displayed bag size

Artifacts:
- `_docs/_analysis/query_articulation_strategy_probe_2026-04-01_import_anchor_tune_v2/query_articulation_strategy_probe.md`
- `_docs/_analysis/query_articulation_strategy_probe_2026-04-01_import_anchor_tune_v2/query_articulation_strategy_probe.json`

---

## 2026-04-01 — Lexical-anchor budget decoupled from returned bag size

Journal entry: pending mirror

- Followed the import-anchor pass with one bounded robustness fix in:
  - `_BDHyperNeuronEMITTER/src/core/engine/inference/bag_view.py`
- Change:
  - lexical FTS anchor search now uses a minimum internal anchor budget of `8`
  - final returned bag size can stay smaller (`top_k = 5`, for example) without starving the anchor search itself

- Why:
  - the broader sanity pass showed `module imports` could reopen as a miss when `top_k` was squeezed
  - cause:
    - lexical-anchor breadth was still coupled to the final displayed bag size

- Validation:
  - focused bag tests:
    - `python -m unittest _BDHyperNeuronEMITTER.tests.test_bag_view -v`
    - `10/10` passing
  - full emitter suite:
    - `python -m unittest discover _BDHyperNeuronEMITTER/tests -v`
    - `51/51` passing
  - targeted check:
    - `module imports` now holds the same top item at `top_k = 5`, `8`, and `12`

- Read:
  - the articulation shelf remains `8 / 8`
  - the remaining narrow-bag sensitivity on the import pair is gone
  - current bag/query-side articulation work is still paying off without any new ingest branch

Artifacts:
- `_docs/_analysis/query_articulation_strategy_probe_2026-04-01_anchor_budget_decoupled/query_articulation_strategy_probe.md`
- `_docs/_analysis/query_articulation_strategy_probe_2026-04-01_anchor_budget_decoupled/query_articulation_strategy_probe.json`
- `_docs/_analysis/bag_broader_sanity_post_import_tune_2026-04-01/bag_broader_sanity_post_import_tune_2026-04-01.md`

---

## 2026-04-02 — Plain vector search baseline compared to the bag

Journal entry: pending mirror

- Added a builder-side comparison harness:
  - `.dev-tools/final-tools/tools/vector_baseline_compare.py`
- Purpose:
  - make ordinary ANN/vector search an explicit control instrument
  - compare plain nearest-neighbor retrieval against the live bag on the same query shelf

- Compared two live reference DBs:
  - deterministic:
    - `_docs/_analysis/reference_probe_073_semgrav_det_steep/cold_anatomy_reference_probe_073_semgrav_det_steep.db`
  - sentence-transformers:
    - `_docs/_analysis/reference_probe_069_semgrav_st_control/cold_anatomy_reference_probe_069_semgrav_st_control.db`

- Query shelf size:
  - `16`

- Deterministic read:
  - ordinary ANN top == bag top on only `4 / 16`
  - vector human-facing top count = `14 / 16`
  - bag human-facing top count = `15 / 16`
  - read:
    - deterministic plain vector retrieval works, but drifts hard on anchor-sensitive queries
    - the bag is clearly doing more than restating nearest-neighbor results

- Sentence-transformers read:
  - ordinary ANN top == bag top on `8 / 16`
  - vector human-facing top count = `13 / 16`
  - bag human-facing top count = `14 / 16`
  - read:
    - plain sentence-transformer retrieval is a stronger ordinary semantic baseline than the deterministic ANN lane on this shelf
    - the bag still improves anchor stability and section targeting over plain vector search

- Practical conclusion:
  - ordinary vector search is absolutely worth keeping as a baseline instrument
  - the bag is retrieving a shaped evidence slice, not just nearest vectors
  - this gives us a repeatable way to ask what each isolated surface is really buying us

Artifacts:
- `_docs/_analysis/vector_baseline_compare_2026-04-02/vector_baseline_compare_summary.json`
- `_docs/_analysis/vector_baseline_compare_2026-04-02/cold_anatomy_reference_probe_073_semgrav_det_steep_deterministic_vector_baseline_compare.md`
- `_docs/_analysis/vector_baseline_compare_2026-04-02/cold_anatomy_reference_probe_069_semgrav_st_control_sentence-transformers_vector_baseline_compare.md`

---

## 2026-04-01 — Five-vertex shock-load sweep on the `0.58` footing

Journal entry: pending mirror

- Ran a first deliberate five-vertex reactivity map on the origin-aware cross-document scorer footing.
- Baseline for this sweep family:
  - Probe 035 (`threshold = 0.58`)
  - `cross-document nucleus pull edges = 2703`
  - `relations = 20660`
  - `above-threshold training pairs = 19231`
- Sweep method:
  - keep the same pair budget and same reference footing
  - promote one cross-document surface aggressively (`0.25`, `0.50`, `0.75`, `0.90`)
  - shrink the other four surfaces proportionally
  - use the change in cross-document pull and relation volume as a first “load-bearing vs slack” read

- Semantic sweep:
  - `0.25 -> 1506`
  - `0.50 -> 128`
  - `0.75 -> 0`
  - `0.90 -> 0`
  - current read: semantic is still mostly a slack line on the active deterministic/reference footing

- Verbatim sweep:
  - `0.25 -> 1679`
  - `0.50 -> 346`
  - `0.75 -> 46`
  - `0.90 -> 35`
  - current read: verbatim is real but limited; modest promotion is survivable, heavy promotion quickly becomes destructive

- Grammatical sweep:
  - `0.25 -> 2752`
  - `0.50 -> 2463`
  - `0.75 -> 1352`
  - `0.90 -> 713`
  - current read: grammatical remains strongly active, but it is not the main growth lane and still decays as it is over-promoted

- Statistical sweep:
  - `0.25 -> 2703`
  - `0.50 -> 229`
  - `0.75 -> 0`
  - `0.90 -> 0`
  - current read: on this exact sweep shape, pushing statistical too hard also collapses the space; the lane is useful, but not as a dominant single carrying force

- Structural sweep:
  - `0.25 -> 364`
  - `0.50 -> 3766`
  - `0.75 -> 6826`
  - `0.90 -> 7810`
  - current read: structural is the strongest current load-bearing surface by far

- Net interpretation:
  - the active Phase 1 field is still being held mostly by structural support
  - grammatical remains very alive
  - verbatim is partially load-bearing but narrow
  - semantic is not yet functionally integrated on the current deterministic/reference footing
  - this is exactly why Phase 1 should now be treated as a five-vertex mapping program rather than a hunt for one lucky blended profile

- Artifacts:
  - `_docs/_analysis/vertex_reactivity_map_2026-04-01/vertex_reactivity_map_2026-04-01.md`
  - `_docs/_analysis/vertex_reactivity_map_2026-04-01/vertex_reactivity_map_2026-04-01.json`

## 2026-04-01 — Weight-pattern rotation test on the `0.58` footing

Journal entry: pending mirror

- Tested whether the current successful cross-document weight pattern was merely a lucky numeric shape or whether its surface assignment mattered.
- Method:
  - kept the same successful cross-document pattern shape
  - rotated it across the five surfaces instead of re-tuning each surface independently
- Results:
  - baseline structural-heavy footing: `2703`
  - rotated to statistical-heavy: `5`
  - rotated to semantic-heavy: `83`
  - rotated to verbatim-heavy: `144`
  - rotated to grammatical-heavy: `1052`
- Read:
  - the current lift is not just “a pattern of numbers that works anywhere”
  - the field cares about which surface gets which role
  - surface orientation matters

## 2026-04-01 — Bounded semantic gravity overlays

Journal entry: pending mirror

- Added an optional `semantic_gravity_profile` under the cross-document profile in `_BDHyperNeuronEMITTER/src/core/nucleus/bootstrap.py`.
- Kept the seam narrow:
  - disabled by default
  - cross-document only
  - bounded bonus
  - no base lens rewrite
- Added bootstrap tests proving:
  - the seam is inert without embeddings
  - the seam raises semantic share for embedding-bearing cross-document pairs
- Then tested the same gravity ladder on two semantic providers:

- Deterministic lane:
  - control: `10955`
  - low: `11697`
  - mid: `12052`
  - high: `12133`

- Sentence-transformers lane:
  - control: `3380`
  - low: `3528`
  - mid: `3700`
  - high: `3943`

- Current read:
  - semantic gravity is real in both lanes
  - semantic behaves better as an attraction overlay than as a primary support beam
  - the deterministic semantic lane is dramatically stronger on this footing
  - next job is quality-control through the bag before promoting any semantic-gravity profile as a default

## 2026-04-01 — Bag QC for semantic-gravity comparison

Journal entry: pending mirror

- Compared four bag states on the same human-facing reference query shelf (`top_k = 5`, `hop_limit = 1`):
  - deterministic control
  - deterministic high gravity
  - sentence-transformers control
  - sentence-transformers high gravity
- Aggregate top-item read:
  - deterministic control: `heading=5`, `locator=5`, `paragraph=1`, `fragment=0`, `qc_total=79`
  - deterministic high: `heading=5`, `locator=5`, `paragraph=1`, `fragment=0`, `qc_total=79`
  - sentence-transformers control: `heading=3`, `locator=6`, `paragraph=1`, `fragment=1`, `qc_total=66`
  - sentence-transformers high: `heading=3`, `locator=6`, `paragraph=1`, `fragment=1`, `qc_total=66`
- The most important qualitative differences:
  - `lambda expressions`:
    - deterministic variants surface the clean section locator `* 6.14.`
    - sentence-transformer variants surface fragment-heavy noise
  - `eval input` and `interactive input`:
    - deterministic variants surface the actual headings `9.4. Expression input` and `9.3. Interactive input`
    - sentence-transformer variants fall back to index locators
- Current read:
  - the deterministic semantic lane is not only graph-strong, it is also the stronger human-facing bag lane on this footing
  - high deterministic semantic gravity did not degrade the top shelf relative to deterministic control
- Artifacts:
  - `_docs/_analysis/bag_semantic_qc_2026-04-01/bag_semantic_qc_2026-04-01.md`
  - `_docs/_analysis/bag_semantic_qc_2026-04-01/bag_semantic_qc_2026-04-01.json`

## 2026-03-31 — Origin-aware cross-document scorer v1

Journal entry: pending mirror

- Implemented a narrow scorer-only Phase 1 experiment in `_BDHyperNeuronEMITTER/src/core/nucleus/bootstrap.py`:
  - added optional `cross_document_profile` support to `BootstrapConfig`
  - kept the same-document path close to the existing footing
  - added cross-document-only surface fractions, threshold scaling, and shared-anchor structural support
- Kept the tranche contract-tight:
  - no Splitter contract expansion
  - no intent-aware scoring
  - no FFN work
  - no broad retrieval redesign
- Shared-anchor support is intentionally v1 only:
  - uses current `cross_refs`, `normalized_cross_refs`, `import_context`, and target hints
  - does **not** claim full triadic closure or a full shared-target neighborhood
- Added emitter test coverage proving:
  - old config payloads still load without `cross_document_profile`
  - disabled branch behavior is inert
  - same-document evaluations remain unchanged when the branch is enabled
  - shared-anchor bonuses only appear when current fields support them
- Added tracked profile:
  - `_BDHyperNeuronEMITTER/_docs/bootstrap_profiles/python_reference_origin_aware_crossdoc_v1.json`
- Ran post-change control replay on the current Python-reference list/index footing:
  - `relations = 17457`
  - `cross-document nucleus pull edges = 115`
  - `training pairs total = 62896`
  - `above-threshold training pairs = 16028`
- Ran Probe 018 with the origin-aware branch enabled on the same footing:
  - `relations = 17592`
  - `cross-document nucleus pull edges = 234`
  - `training pairs total = 62896`
  - `above-threshold training pairs = 16163`
- This tranche cleared the acceptance bar:
  - `cross-document pull >= 140` yes (`234`)
  - `training pairs <= 70000` yes (`62896`)
  - no relation collapse; relation volume rose slightly instead
- The conversion geometry changed in exactly the direction we wanted:
  - control cross-document winners:
    - `grammatical_dominant = 106`
    - `structural_bridge = 2`
    - `multi_surface = 7`
  - origin-aware experiment winners:
    - `structural_bridge = 153`
    - `multi_surface = 69`
    - `grammatical_dominant = 12`
- The new read is sharper:
  - a single generic scorer lens was part of the `115` plateau
  - Phase 1 really does need different static evaluation profiles for different pair classes
  - origin-aware conversion helps materially
  - but it still recovers only part of the Probe 011 wide-window continent (`234` vs `1175`)
- Current next question:
  - refine the origin-aware cross-document profile further, or
  - decide whether the current partial outbound-reference seam is too weak and needs a later richer shared-target neighborhood

## 2026-03-31 — Origin-aware control gradient and threshold sweep

Journal entry: pending mirror

- Turned the new origin-aware scorer into a real control surface instead of a one-profile anecdote.
- Ran the first ablation gradient after Probe 018:
  - fractions only -> `cross-document pull = 150`
  - fractions + threshold scaling -> `228`
  - fractions + shared-anchor bonus -> `155`
- That clarified the leverage order:
  - the alternate cross-document lens matters
  - threshold scaling carries most of the next lift
  - the current shared-anchor seam is still secondary on this footing

- Then ran a fixed-budget threshold sweep on the same footing (`training pairs total = 62896` throughout):
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

- The strongest new read from this sweep:
  - the old cross-document threshold gate was much too strict
  - the graph can now match and exceed the old Probe 011 wide-window pull count without pair growth
  - the winner field stays dominated by `structural_bridge` / `statistical_echo` much deeper into the sweep than expected

- The sweep also created a new guardrail:
  - `0.50`–`0.65` looks like the most promising trust band so far
  - `0.40` is the first warning zone where weakest winners begin to look shaky
  - `0.30` is too permissive and admits fragment-heavy bridge fabric

- That changes the next-step logic:
  - the next job is no longer "prove the origin-aware branch helps"
  - the next job is "choose the trustworthy default band"
  - richer shared-target extraction should stay deferred until the current threshold/fraction line stops paying off
- Added a dedicated narrative capture for this turning point:
  - `_docs/BREAKTHROUGH_REPORT_2026-03-31.md`
  - this report explains the progression, the control ladder, and the human-readable meaning of the new lens behavior

## 2026-03-31 — Bag hotfix, post-fix bag read, and leading default candidate

Journal entry: pending mirror

- Shifted from graph-only evaluation into bag-first usefulness checks because the active user goal is now to make the bag useful to an observer/agent first.
- Confirmed a real bag/runtime bug in `_BDHyperNeuronEMITTER/src/core/engine/inference/hot_engine.py`:
  - stored relations are directional (`source_occ_id -> target_occ_id`)
  - the Hot Engine had been propagating activation backward relative to that direction
  - tiny proof:
    - edge `A -> B`
    - seed `A` only kept `A`
    - seed `B` incorrectly activated `A`
- Fixed the propagation orientation in the Hot Engine for both numpy and GraphBLAS paths.
- Added focused emitter tests in:
  - `_BDHyperNeuronEMITTER/tests/test_hot_engine.py`
  - proving forward propagation and no back-propagation from a seeded target
- Verified the full emitter suite after the fix:
  - `38 / 38` passing

- Ran post-fix bag sanity passes on the reference probe DBs.
- Strongest bag read after the fix:
  - `hop_limit = 1` remains the right human-facing regime
  - `hop_limit = 2` and `3` still drift badly into index-heavy noise
  - widening anchor budget alone still does not materially improve the awkward cases
  - dropping `index.txt` list-item anchors also does not materially change the good-footing outputs
- That means the current bag bottleneck is not:
  - too few lexical seeds
  - or simple index-anchor monopoly
- It is more about:
  - propagation/ranking behavior
  - and the underlying graph quality now that propagation is flowing the right way

- Post-fix query quality improved in ways that finally reflect the graph breakthrough:
  - `lexical analysis`
    - control still lands in `introduction.txt`
    - `0.58 / 0.55` land in `lexical_analysis.txt`
  - `encoding declarations`
    - control and `0.60` still surface a bad `datamodel.txt` item
    - `0.58 / 0.55` surface `lexical_analysis.txt -> 2.1.4. Encoding declarations`
  - `operator precedence`
    - control and `0.60` stay on `index.txt`
    - `0.58 / 0.55` move into `expressions.txt`

- Current bag-first default read:
  - `0.58` and `0.55` both beat `0.60` on the most interesting bag queries
  - `0.58` currently looks like the safer strong default candidate
  - `0.55` remains close behind and should stay in the experiment lane

- New bag artifacts from this pass:
  - `_docs/_analysis/bag_post_hotfix_compare_2026-03-31/`
  - `_docs/_analysis/bag_hop_post_hotfix_2026-03-31/`
  - `_docs/_analysis/bag_anchor_filter_sanity_2026-03-31/`
  - `_docs/_analysis/bag_band_compare_post_hotfix_2026-03-31/`
  - `_docs/_analysis/bag_055_vs_058_detail_2026-03-31/`

- Updated read:
  - the graph breakthrough was real
  - the bag bug was also real
  - after fixing the bag engine, the origin-aware graph improvements finally show up in human-facing evidence
  - current next move is not “more random tuning”; it is:
    - document the fix
    - keep bag checks attached to trust-band selection
    - and likely treat `0.58` as the leading default candidate until broader bag checks prove otherwise

- Kept pushing on bag usefulness after the engine fix:
  - added a light human-facing rerank in `_BDHyperNeuronEMITTER/src/core/engine/inference/bag_view.py`
  - when items are close, the bag now prefers:
    - exact query-phrase matches
    - exact heading/section anchors
    - anchor items over nearby non-anchor relays
    - cleaner non-fragment evidence over noisy fragment/code-block spill
  - bag items now also expose:
    - `rank_score`
    - `rank_signals`
- Fixed a readability seam in bag summaries:
  - short section labels like `2. Lexical analysis` or `6.2.9. Yield expressions` no longer collapse to snippets like `2.` or `6.2.9.`
- Added focused bag-view coverage proving:
  - an exact heading can outrank a slightly hotter but less helpful paragraph when building the human-facing bag
- New runtime read:
  - the graph chooses the substrate
  - the bag view now does a small amount of observer-helpful ordering on top of that substrate
  - this makes the bag more useful to a human/agent without pretending retrieval or graph construction changed

## 2026-04-01 — Bag lexicalization and refined origin-support rerank

Journal entry: pending mirror

- Kept working on the bag layer rather than the durable graph because the current goal is still “make the bag useful to a reader/agent first.”
- Added conservative lexical query variants in `_BDHyperNeuronEMITTER/src/core/engine/inference/provider.py`:
  - variants are used only for lexical anchor search
  - ANN/query embedding still uses the original query text
  - initial safe variants include:
    - underscore/space alternates
    - simple singularization
    - a tiny hand-curated alias seam such as:
      - `eval input -> expression input, eval_input`
      - `lambda expressions -> lambdas`
- Added tests proving lexical variants are generated conservatively and are actually used in the FTS anchor loop.

- Extended `_BDHyperNeuronEMITTER/src/core/engine/inference/bag_view.py` again:
  - bag rerank now sees lexical anchors produced by those conservative variants
  - a small origin-support bonus can now help when multiple lexical variants independently point into the same source origin
  - kept this bag-only and human-facing:
    - no graph mutation
    - no retrieval contract expansion
    - no durable-score changes
- Added bag tests proving origin-support can break close calls in favor of the more corroborated origin.

- Ran stubborn-query diagnostics across the current `0.60`, `0.58`, and `0.55` reference-probe DBs.
- Strongest positive result:
  - `eval input` is now clearly better:
    - top item becomes the `toplevel_components.txt` paragraph describing expression input
    - followed by the heading `9.4. Expression input`
    - then the `eval_input ::= ...` code block
- Strongest negative / cautionary read:
  - raw origin-anchor count was too blunt and could over-reward broad origins
  - refined the bonus so it depends on corroboration across lexical query variants rather than sheer anchor volume
- Current bag read after that refinement:
  - the graph/Hot Engine side of this problem is mostly no longer the blocker for the stubborn cases
  - the remaining awkward cases (`function definitions`, `lambda expressions`, `assignment expressions`, `operator precedence`) now look more like corpus-query wording mismatch / lexicalization problems than propagation failures
  - this means the next likely bag seam is targeted lexicalization/alias refinement, not another graph-direction fix

- Follow-up rerank refinement:
  - taught the bag rerank to notice safe lexical-variant exact matches, not only the original query string
  - softened the penalty on short exact section locators when they are clearly acting like useful human-facing anchors
- Post-refinement stubborn-query read on the current trust-band DBs:
  - `eval input` improved again and now surfaces the `9.4. Expression input` heading first
  - `function definitions` improved on the better bands (`0.58` / `0.55`) and now surfaces the section locator `* 8.7.` first
  - `operator precedence` remains clean
  - `assignment expressions` remains poor
  - `lambda expressions` remains poor, which is useful evidence that variant-aware rerank is not a universal rescue and that this case likely needs better lexical targeting or a different bag strategy
- Current sharper bag read:
  - graph-direction and propagation are no longer the main mystery
  - the next bag bottleneck is mostly query-to-corpus wording alignment on a small set of stubborn topics

- Validation after this pass:
  - full emitter suite is now `43 / 43` passing

- New artifacts from this bag tranche:
  - `_docs/_analysis/bag_stubborn_queries_origin_support_2026-04-01/`
  - `_docs/_analysis/bag_stubborn_queries_origin_support_refined_2026-04-01/`
  - `_docs/_analysis/bag_query_rewrite_effect_post_patch_2026-04-01/`
  - `_docs/_analysis/bag_stubborn_queries_variant_rerank_2026-04-01/`

## 2026-03-31 — Park-state freeze, conversion diagnostics, and doctrine consolidation

Journal entry: pending mirror

- Updated the root onboarding and parked-state docs so they reflect the real current footing instead of the older “next move = add cheap-fetch fallback” state.
- Clarified the real current blocker:
  - cheap-fetch fallback already exists
  - long-range candidates are being recovered
  - the scorer is still under-converting structurally plausible cross-document pairs
- Landed contradiction v1 as a narrow explicit anti-signal seam and recorded the first probe reads:
  - Probe 015 control replay
  - Probe 015b naive contradiction pass
  - Probe 015c cleaned contradiction pass
- The contradiction read is now sharper:
  - contradiction v1 is real and inspectable
  - contradiction v1 is safe to keep in-tree
  - contradiction v1 is **not** yet the main bottleneck mover
- Added hub/source concentration diagnostics and tested FTS per-origin capping through Probe 016.
- Falsified two tempting explanations:
  - cheap-fetch alone does not solve the plateau
  - FTS origin monopoly is not the main cause of the plateau
- Upgraded builder-side conversion reporting so winner/loser cross-document patterns can be compared directly.
- The new conversion reports established a stronger read:
  - most cross-document losers are not near-threshold misses
  - the dominant loser population is structural/statistical bridge-like pairs
  - the current scorer still prefers a narrower grammatical winner lane
- Consolidated the newer bag doctrine:
  - bag as a bounded observer-centered slice
  - current node as anchor
  - observer-side anchor plus source-side anchor
  - bag as the join boundary
  - later retrieval will need `scope root`, `resolution grammar`, `direction of spread`, and `stop-unwinding`
- Explicitly kept weather/chaos framing in the north-star bucket:
  - useful as a nested-resolution / complexity-control analogy
  - not current runtime nucleus math
- Captured the next scorer-side hypothesis for the next pickup:
  - the current candidate-selection path is already origin-aware
  - the current Bootstrap Nucleus is still origin-agnostic
  - the next likely Phase 1 experiment is an origin-aware cross-document scoring branch
  - current HyperHunks already expose `cross_refs`, `normalized_cross_refs`, and `import_context`, but not yet a fully normalized shared-target neighborhood

## 2026-03-30 — Root onboarding guide for fresh threads

- Added root [`ANY_NEW_CONVO_READ_THIS_FIRST.md`] as the one-file tour guide for a brand new conversation or agent pickup.
- Pointed `_docs/WE_ARE_HERE_NOW.md` at that file so fresh threads land on a single entry point before reading the deeper recovery surfaces.
- Locked the onboarding message to the real current footing:
  - Phase 1 active
  - bag exists and is usable
  - deterministic lane is currently winning the first embedder comparison
  - cross-document bottleneck is still long-range candidate recall
  - next likely move is deterministic cheap-fetch fallback behind the anchor-registry path
- Added [`_docs/CROSS_DOCUMENT_PULL_BOTTLENECK_ANALYSIS.md`] as the focused advanced breakdown of the current main problem, with Probe 011/012/013 evidence and the current read on why small windows, wide windows, and anchor-only recall each fail differently.

## 2026-03-27 — Recovery checkpoint + doctrine lock

Journal entry: `journal_resume_checkpoint_20260327`

- Re-centered the active project truth on the current repo root after the old `final/` move-up.
- Added root [`_docs/ARCHITECTURE.md`] as the authoritative architecture note for the active line.
- Added root [`_docs/WE_ARE_HERE_NOW.md`] as the fastest cold-start / crash-recovery note.
- Rewrote the backlog so it points forward to Splitter corpus hardening instead of lingering in “cleanup just happened” mode.
- Captured the current sequencing doctrine explicitly:
  - neurons first
  - living graph second
  - bag seam third
- Captured current non-goals explicitly:
  - no FFN work yet
  - no bag implementation yet
  - no broad retrieval redesign yet
- Recorded that the Emitter UI lifecycle/threading path was cleaned so worker-thread UI updates are queued back onto the main Tk thread safely.
- Left long-form historical docs in place, but demoted them behind the new active truth surfaces so resuming later will be much cleaner.

## 2026-03-27 — Splitter corpus baseline 001

Journal entry: `journal_splitter_corpus_baseline_001`

- Began Tranche 10 with real corpora instead of synthetic smoke only.
- Ran the Splitter against the Webster dictionary corpus as the prose-floor baseline.
- Confirmed Webster should remain `FallbackEngine` only, then fixed fallback provenance so emitted hunks now stamp `extraction_engine="FallbackEngine"` instead of leaving it blank.
- Ran routing inspection on the Python 3.11 reference docs and confirmed the initial problem: structured `reference/*.txt` documents were collapsing to fallback-only.
- Extended the PEG path so it can recognize structured `.txt` docs using underlined heading syntax rather than requiring only `.md` / `.markdown`.
- Confirmed `lexical_analysis.txt` now routes as `PEGEngine` + `FallbackEngine`, with emitted `md_heading` hunks and populated `heading_trail` instead of all-fallback paragraphs.
- Added `_docs/SPLITTER_CORPUS_BASELINES.md` as the running metrics/observations table for corpus hardening work.
- Remaining weak spots identified immediately:
  - `grammar.txt` and `index.txt` still route fallback-only in the sampled Python reference set
  - one `md_list` artifact remains in the `lexical_analysis.txt` sample and should be inspected later

## 2026-03-27 — Graph probe 001 (Python reference full-pipe)

Journal entry: `journal_graph_probe_001`

- Ran the improved Python reference corpus through the full Splitter → Emitter pipeline.
- Probe artifacts written under `_docs/_analysis/reference_probe_001/`.
- Full-pipe summary:
  - `1102` hunks ingested
  - `1083` content nodes
  - `22406` relations
  - `53825` training pairs
- Confirmed the stronger NL/document path is affecting the graph rather than dying at the handoff:
  - `1293` cross-document nucleus pull edges were created
- Confirmed the current bootstrap nucleus remains heavily grammar-skewed on prose-heavy corpora:
  - `grammatical_dominant` is the majority interaction mode
  - semantic remains zero because no embedding artifacts were loaded
- This is good enough progress to continue, but it also exposed the next meaningful question:
  - improve Splitter list/index representation more, or
  - start refining bootstrap prose interaction behavior in the Emitter

## 2026-03-27 — Probe reporting loop established

Journal entry: `journal_probe_reporting_001`

- Added builder-side probe reporting tool `.dev-tools/final-tools/tools/graph_probe_report.py`.
- Verified the tool against the existing Python-reference probe artifacts and confirmed it reproduces the manual counts exactly.
- Saved the first machine-readable report at `_docs/_analysis/reference_probe_001/graph_probe_report_001.json`.
- This gives the project a repeatable step-2 loop:
  - make one targeted change
  - rerun the full probe
  - save a JSON report
  - compare against Probe 001 instead of relying on ad hoc SQL and memory
- The project now has measurable ground for oscillating between Splitter and Emitter work without losing the thread.

## 2026-03-27 — Bootstrap de-bias pass 001 + Probe 002

Journal entry: `journal_bootstrap_probe_002`

- Inspected `_BDHyperNeuronEMITTER/src/core/nucleus/bootstrap.py` to trace the prose-heavy `grammatical_dominant` bias from code rather than from probe symptoms alone.
- Confirmed the main seam:
  - exact prose node-kind matches like `md_paragraph` were receiving the same full grammatical credit as exact code-node matches
  - semantic remained zero because no embedding artifacts were loaded
  - with fixed Phase 1 surface fractions, that combination pushed too many prose pairs into grammar-led routing
- Applied one targeted bootstrap change:
  - prose grammatical matching was de-amplified relative to code grammatical matching
- Ran Probe 002 against the same Python reference corpus and recorded artifacts under `_docs/_analysis/reference_probe_002/`.
- Results:
  - `grammatical_dominant` training labels dropped sharply
  - but relation volume also dropped sharply (`22406 -> 2897`)
  - cross-document nucleus pull edges also dropped sharply (`1293 -> 147`)
- Current interpretation:
  - the first de-bias pass proved the distortion is a bootstrap-math problem
  - the first pass is too aggressive to keep as the final tune
  - the next iteration should be moderate, not extreme, and likely needs either softer prose penalties or threshold retuning

## 2026-03-27 — Bootstrap scaffold dials shipped + Probe 003

Journal entry: `journal_bootstrap_scaffold_dials_001`

- Refactored the Emitter bootstrap scorer so it now consumes an explicit `BootstrapConfig` rather than hardcoded module constants.
- Exposed builder-facing tuning through:
  - `--bootstrap-profile`
  - `--edge-threshold`
  - `--dominance-threshold`
- Emit now writes `bootstrap_profile_effective.json` beside the output database, making probe bundles reproducible by default.
- Updated the builder-side `graph_probe_report` tool to include the adjacent effective bootstrap profile when present.
- Added emitter-local tests covering:
  - config validation
  - round-trip serialization
  - basic scaffold behavior expectations
  - semantic-absence threshold scaling behavior
- Added tracked starter profile:
  - `_BDHyperNeuronEMITTER/_docs/bootstrap_profiles/python_reference_prose_tuning.json`
- Verified default regression:
  - default-config emit reproduces Probe 002 top-line baseline (`relations = 2897`, `cross-document pull = 147`, `above-threshold = 1636`)
- Ran Probe 003 with the starter profile:
  - `relations = 13510`
  - `cross-document nucleus pull edges = 169`
  - `above-threshold pairs = 12249`
  - `grammatical_dominant` training labels reduced to `801`
- Current interpretation:
  - the scaffold dial surface is now good enough for deliberate tuning work
  - the starter profile successfully recovers live-graph volume over Probe 002
  - the next scoring target is cross-document pull recovery, not just raw relation count

## 2026-03-28 — Builder-side probe monitor shipped

Journal entry: pending mirror

- Added `.dev-tools/final-tools/tools/probe_monitor.py` as a builder-only probe runner for Splitter -> Emitter passes.
- The tool writes a replayable observability bundle under `_docs/_analysis/<probe>/`:
  - `probe_events.jsonl`
  - `probe_run.log`
  - `graph_probe_report_<probe>.json`
  - `bootstrap_profile_effective.json` from the runtime emit path
- Added an optional tiny Tk builder monitor window for live viewing while keeping the shipped app cleanly decoupled from `.dev-tools`.
- Added stage events and safer failure cleanup so probe runs leave a useful record even when something breaks midstream.
- Added example job:
  - `.dev-tools/final-tools/jobs/examples/probe_monitor.json`
- Updated the final-tools manifest/docs/smoke test so the probe monitor is part of the validated toolbox rather than an ad hoc local script.
- Verified:
  - `python -m py_compile` passed on the touched builder-tool files
  - `python .dev-tools/final-tools/smoke_test.py` passed, including `probe_monitor`
- Resulting workflow improvement:
  - future Probe 004+ runs can be watched live while still producing durable machine-readable artifacts for comparison

## 2026-03-28 — Probe 004 observable replay baseline

Journal entry: pending mirror

- Ran Probe 004 against the same Python reference corpus and the same tracked starter profile used for Probe 003, but through the new builder-side probe monitor.
- Probe 004 wrote the normal graph artifacts plus live-monitor artifacts:
  - `_docs/_analysis/reference_probe_004/probe_events.jsonl`
  - `_docs/_analysis/reference_probe_004/probe_run.log`
- Probe 004 matched Probe 003 exactly on the tracked top-line metrics:
  - `relations = 13510`
  - `cross-document nucleus pull edges = 169`
  - `above-threshold training pairs = 12249`
  - `grammatical_dominant` training labels = `801`
- Interpretation:
  - the monitor layer is observational only; it did not perturb the run
  - Probe 003 is now confirmed as a stable observable baseline rather than a one-off good pass
- Follow-up builder UX improvement:
  - extended `probe_monitor.py` with `hold_open` so the tiny monitor window can stay open after completion until manually closed

## 2026-03-28 — Probe 005/006 tuning negatives + monitor hold-open fix

Journal entry: pending mirror

- Probe 005 tested a profile-only shift from `structural` weight into `statistical` weight using:
  - `_BDHyperNeuronEMITTER/_docs/bootstrap_profiles/python_reference_crossdoc_tuning_v1.json`
- Result:
  - `relations = 9072` (`-4438` vs Probe 004)
  - `cross-document nucleus pull edges = 163` (`-6` vs Probe 004)
  - `above-threshold training pairs = 7811` (`-4438` vs Probe 004)
- Interpretation:
  - cross-document lift is not hiding behind a general statistical boost
  - this branch hurt graph activity and should not replace the Probe 003/004 baseline

- Probe 006 tested a heading-targeted grammatical boost using:
  - `_BDHyperNeuronEMITTER/_docs/bootstrap_profiles/python_reference_crossdoc_tuning_v2.json`
- Result:
  - `relations = 13510` (matches Probe 004)
  - `cross-document nucleus pull edges = 169` (matches Probe 004)
  - `grammatical_dominant` training labels rose from `801` to `879`
- Interpretation:
  - simple heading-weight amplification did not improve cross-document pull
  - it only shifted some interaction labeling toward grammar without lifting the target metric

- Builder monitor lifecycle fix:
  - the first `hold_open` implementation exposed a Tk teardown/thread issue
  - fixed by moving the tiny viewer into a standalone helper process:
    - `.dev-tools/final-tools/tools/probe_monitor_viewer.py`
  - validated with a UI auto-close smoke and the full final-tools smoke suite

- Current read after Probes 005 and 006:
  - Probe 003/004 remains the stable baseline
  - the next cross-document lift attempt likely needs either:
    - a more granular bootstrap-code dial, or
    - richer representation work from the Splitter

## 2026-03-28 — Probe 007 explicit-reference dial (signal too sparse)

Journal entry: pending mirror

- Added a narrow explicit-reference structural dial to the Bootstrap Nucleus:
  - builder-tunable `explicit_reference_profile`
  - current fields:
    - `overlap_weight`
    - `target_hint_bonus`
- Kept defaults at zero so existing baselines remain stable.
- Added `python_reference_crossdoc_tuning_v3.json` as the Probe 007 profile.
- Added emitter-local coverage proving the explicit-reference boost can raise structural similarity when a matching target hint exists.
- Ran Probe 007 through the live builder monitor.

- Results vs Probe 004 baseline:
  - `relations = +1`
  - `cross-document nucleus pull edges = 0`
  - `above-threshold training pairs = +1`
  - no shift in the main training interaction counts

- The one extra relation was an in-document structural bridge between two `lexical_analysis.txt` fragments carrying the extracted `cross_refs` value:
  - `shortstring | longstring`

- Interpretation:
  - the scorer-side dial works mechanically
  - but the active `cross_refs` signal in the Python reference corpus is too sparse or too weakly extracted to drive the next cross-document gain
  - this points the next improvement toward Splitter-side explicit reference extraction rather than further scorer-side boosting of the current sparse signal

## 2026-03-28 — Splitter signal-control layer + Probe 008/009

Journal entry: pending mirror

- Added a Splitter-owned signal profile layer in `_BDHyperNodeSPLITTER/src/core/signal_profile.py`.
- Wired builder-facing `--signal-profile` into `_BDHyperNodeSPLITTER/src/app.py` and through the Splitter coordinator/Negotiator path.
- Kept the active five-surface runtime contract stable while adding facet-ready flat fields:
  - `normalized_cross_refs`
  - `reference_kinds`
  - `list_role`
  - `list_depth`
  - `reference_confidence`
- Extended PEG extraction so it can now normalize richer explicit references when they are present:
  - Markdown links
  - reST role references
  - reST inline links
  - low-confidence grammar-symbol references
- Added optional list-item emission controls and fragment-inheritance controls under the new Splitter signal profile.
- Added Splitter tests covering:
  - profile validation
  - deterministic reference normalization
  - list-item emission
  - fragment inheritance behavior
- Updated the builder-side probe monitor so it now persists:
  - `splitter_signal_profile_effective.json`
  - `bootstrap_profile_effective.json`
  - graph report
  - event stream
  - run log
- Added tracked Splitter profile:
  - `_BDHyperNodeSPLITTER/_docs/signal_profiles/python_reference_richer_refs_v1.json`

## 2026-03-29 — Builder artifact-root control for probe outputs

Journal entry: pending mirror

- Added an optional builder-side `artifact_root` input to `.dev-tools/final-tools/tools/probe_monitor.py`.
- Current behavior stays unchanged by default:
  - if `artifact_root` is omitted, probe bundles still land under `_docs/_analysis/<probe>/`
- New behavior when supplied:
  - the entire builder-only probe bundle can be written to an external storage location
  - this includes the heavy `training_pairs_<probe>.json` export, SQLite DB, logs, events, and graph report
- Updated the final-tools README, builder guide, and example probe-monitor job to show the new storage choice explicitly.
- Verified:
  - `python -m py_compile .dev-tools/final-tools/tools/probe_monitor.py`
  - `python .dev-tools/final-tools/smoke_test.py`
- Operational reason:
  - `training_pairs_webster_probe_monitor_smoke.json` alone is ~`8.15 GB`
  - large raw pair dumps are now treated as builder storage decisions rather than fixed project-root outputs

## 2026-03-29 — External records library + `_docs/_analysis` junction

Journal entry: pending mirror

- Created a shared external records root at `E:\\_UsefulRECORDS`.
- Added project-local records structure for this repo:
  - `E:\\_UsefulRECORDS\\projects\\BDNeuralTranslationSUITE\\`
  - `E:\\_UsefulRECORDS\\projects\\BDNeuralTranslationSUITE\\probe_artifacts\\`
- Added root and project `README.md` files so the storage library remains self-describing.
- Added `.dev-tools/final-tools/builder_settings.local.json` so builder probes now default to the external artifact home automatically.
- Migrated the existing `_docs/_analysis` contents (`~9.14 GB`) into the external `probe_artifacts` library.
- Recreated `_docs/_analysis` as a directory junction pointing to the external probe library.
- Result:
  - existing project paths under `_docs/_analysis/...` still work
  - the storage lives on `E:`
  - future probe bundles go to the external builder records home by default

## 2026-03-29 — Rudimentary Bag CLI shipped

Journal entry: pending mirror

- Added `_BDHyperNeuronEMITTER/src/core/engine/inference/bag_view.py`.
- Added a new Emitter CLI command in `_BDHyperNeuronEMITTER/src/app.py`:
  - `bag`
- The new bag seam is intentionally narrow and built on the existing retrieval pipeline:
  - calls the current query path
  - enriches Bag-of-Evidence items from `occurrence_nodes` + `content_nodes`
  - emits:
    - ranked evidence items
    - group summaries
    - item summaries
    - pullback-ready text for selected occurrence ids
- This was kept CLI-first on purpose:
  - no Tk UI work yet
  - no new orchestration layer yet
  - no bag runtime dependency on `.dev-tools`
- Added `_BDHyperNeuronEMITTER/tests/test_bag_view.py`.
- Verified:
  - `python -m unittest _BDHyperNeuronEMITTER/tests/test_bag_view.py -v`
  - `python -m unittest discover _BDHyperNeuronEMITTER/tests -v`
- This is the first usable agent-facing bag seam, but not yet the full STM membrane architecture.
- Added doctrine note:
  - `_docs/FACET_READY_SURFACE_DESIGN.md`

- Probe 008:
  - default-profile regression after the Splitter control-layer tranche
  - result matched the stable Probe 003/004 footing exactly:
    - `relations = 13510`
    - `cross-document nucleus pull edges = 169`
    - `above-threshold training pairs = 12249`

- Probe 009:
  - same corpus + same bootstrap footing, but with the tracked richer-reference Splitter profile through the live monitor
  - result remained unchanged from Probe 008:
    - `relations = 13510`
    - `cross-document nucleus pull edges = 169`
    - `above-threshold training pairs = 12249`

- Follow-up Splitter signal inspection explained the flat result:
  - default and tuned runs both produced only `2` ref-bearing hunks in the Python reference text corpus
  - both runs exposed only `1` unique normalized target (`shortstring_longstring`)
  - so the new control layer is working and reproducible, but the active text corpus export still lacks a dense enough explicit-reference lane to move the graph metric

- Current interpretation:
  - the control layer is now in place and safe to iterate on
  - the next cross-document gain likely needs either:
    - list/index representation work, or
    - a different explicit-signal family than the sparse `cross_refs` currently present in the corpus

## 2026-03-30 — Pilot corpus set 001 + bag validation baseline

Journal entry: pending mirror

- Ran the current end-to-end builder probe pipeline against three fresh local corpora:
  - `_corpus_examples/tech_talks`
  - `_corpus_examples/Paradigm`
  - `_corpus_examples/_AppBuilderTOOLBOX`
- All probe bundles were written to the external builder records home and remain accessible through `_docs/_analysis/...` via the junctioned analysis path.

- `tech_talks_probe_001`
  - `5106` occurrence nodes
  - `160088` relations
  - `254775` training pairs
  - `1227` cross-document nucleus pull edges
  - bag artifact saved:
    - `_docs/_analysis/tech_talks_probe_001/bag_query_memory_graph.json`
  - bag query `"memory graph"` surfaced useful evidence from:
    - `Another Crazy Convo.txt`
    - `MicroserviceLIBRARY_ Architectural Overview and .md`

- `paradigm_probe_001`
  - `177` occurrence nodes
  - `3498` relations
  - `7575` training pairs
  - `2422` cross-document nucleus pull edges
  - bag artifact saved:
    - `_docs/_analysis/paradigm_probe_001/bag_query_identity.json`
  - bag query `"identity"` surfaced evidence across:
    - `MemoryLOG_ClosenessToSource_EnergyConcepts.txt`
    - `Dimensioning_Tools.txt`
    - `MemoryLOG_ComingToTermsWith_Consciousness.txt`
    - `Full_Apriori_Axiom.txt`

- `appbuilder_toolbox_probe_001`
  - `883` occurrence nodes
  - `11687` relations
  - `42875` training pairs
  - `2269` cross-document nucleus pull edges
  - first query `"registry stamper"` returned no evidence, which turned out to be a query-anchor issue rather than an ingest failure
  - follow-up bag artifact saved:
    - `_docs/_analysis/appbuilder_toolbox_probe_001/bag_query_mcp_server.json`
  - bag query `"mcp server"` surfaced real mixed code/doc evidence from:
    - `src/mcp_server.py`
    - `src/lib/journal_store.py`
    - `src/lib/tool_pack.py`
    - `README.md`

- Re-ran current automated validation after the new material ingest:
  - `python -m unittest discover _BDHyperNodeSPLITTER/tests -v`
  - `python -m unittest discover _BDHyperNeuronEMITTER/tests -v`
  - `python .dev-tools/final-tools/smoke_test.py`
  - all passed

- Current interpretation:
  - the prototype is no longer validated only on the Python-reference harness
  - the bag is already useful on both prose-heavy and mixed project graphs
  - next high-value step is no longer “does the bag work at all?”
  - next high-value step is side-by-side semantic comparison using the same bag/query workflow

## 2026-03-30 — Embedder comparison baseline 001

Journal entry: pending mirror

- Added a parallel embedding-provider seam to the Emitter:
  - `emit --embedder auto|deterministic|sentence-transformers|none`
  - `emit --sentence-model <model>`
  - `bag --embedder-override ...`
- Probe bundles now persist `embedding_provider_effective.json`, allowing query/bag to infer the correct query embedder from the DB bundle itself.
- Added provider-level tests for:
  - embedding-provider metadata round trip
  - query-time provider selection through DB-bundle metadata
- Re-ran emitter tests and final-tools smoke after the embedder work; all passed.

- Comparison prep surfaced and fixed a real deterministic-training seam:
  - `compute_counts()` returns a tuple
  - `cmd_train()` had been expecting named fields
  - the deterministic training path now handles the current return shape and produces usable artifacts again

- Built corpus-specific deterministic artifacts:
  - `E:\_UsefulRECORDS\projects\BDNeuralTranslationSUITE\embedding_artifacts\tech_talks_det_v1`
  - `E:\_UsefulRECORDS\projects\BDNeuralTranslationSUITE\embedding_artifacts\appbuilder_toolbox_det_v1`
- Staged small textized corpora for deterministic training under:
  - `E:\_UsefulRECORDS\projects\BDNeuralTranslationSUITE\training_corpora\tech_talks_textized`
  - `E:\_UsefulRECORDS\projects\BDNeuralTranslationSUITE\training_corpora\appbuilder_toolbox_textized`

- Ran first side-by-side comparison on `tech_talks`:
  - `tech_talks_probe_002_det`
    - `141879` relations
    - `1670` cross-document nucleus pull edges
    - `semantic_resonance = 658`
    - bag query `"memory graph"` surfaced a broader evidence mix across:
      - `Another Crazy Convo.txt`
      - `master_spec_text.txt`
      - `MicroserviceLIBRARY_ Architectural Overview and .md`
  - `tech_talks_probe_003_st`
    - `155790` relations
    - `1372` cross-document nucleus pull edges
    - `semantic_resonance = 48`
    - bag query `"memory graph"` skewed much more heavily toward `master_spec_text.txt`

- Ran first side-by-side comparison on `_AppBuilderTOOLBOX`:
  - `appbuilder_toolbox_probe_002_det`
    - `23676` relations
    - `4154` cross-document nucleus pull edges
    - strong `multi_surface` + `semantic_resonance`
    - bag query `"mcp server"` surfaced a broader mixed evidence set across:
      - `README.md`
      - `journal_store.py`
      - `tool_pack.py`
      - `mcp_server.py`
      - `scaffolds.py`
  - `appbuilder_toolbox_probe_003_st`
    - `14836` relations
    - `3232` cross-document nucleus pull edges
    - bag query `"mcp server"` still worked, but with a narrower and more code-heavy result mix

- Current interpretation:
  - the traditional sentence-transformer lane is now integrated and testable
  - but on both tested corpora the deterministic lane is stronger than the off-the-shelf sentence model
  - that is a useful result, not a failure:
    - it suggests the current five-surface + deterministic geometry is already carrying more useful relational signal than a default sentence embedder in this prototype shape

## 2026-03-30 — Anchor registry v1 + Probe 013

Journal entry: pending mirror

- Replaced the simple long-range token index in `GraphAssembler` with a ranked occurrence-level anchor registry.
- The new registry stays Phase-1-compatible:
  - same sliding window
  - same `reference_candidate_limit`
  - same heavy scorer as final gate
  - no FTS fallback yet
- New registry behavior:
  - heading anchors are stronger than generic cross-reference anchors
  - list/index-derived targets remain a mid-weight anchor lane
  - overly common anchor terms are suppressed after a configurable threshold so they stop flooding long-range recall
- Added emitter tests proving:
  - a stronger heading anchor wins over a weaker list-ref-only match when the long-range candidate budget is capped
  - common anchor terms are suppressed once they exceed the configured threshold
- Validation passed:
  - `python -m unittest _BDHyperNeuronEMITTER/tests/test_reference_candidate_selection.py -v`
  - `python -m unittest discover _BDHyperNeuronEMITTER/tests -v`
  - `python .dev-tools/final-tools/smoke_test.py`
- Ran `reference_probe_013_anchor_registry_v1` against the same footing as Probe 012:
  - Splitter profile: `python_reference_list_index_v1.json`
  - Bootstrap profile: `python_reference_prose_tuning.json`
  - `window_size = 50`
  - `reference_candidate_limit = 24`
- Probe 013 results:
  - `relations = 17428`
  - `cross-document nucleus pull edges = 115`
  - `above-threshold training pairs = 15999`
- Current interpretation:
  - the anchor registry made long-range candidate recall more selective
  - but it did not lift the `115` cross-document plateau reached by Probes 010 and 012
  - this points to the next likely move being a deterministic cheap-fetch fallback, probably reusing SQLite FTS when anchor recall is too sparse

## 2026-03-30 — Native FTS fallback v1 + Probe 014

Journal entry: pending mirror

- Added a native SQLite FTS cheap-fetch fallback behind the Emitter's anchor-registry path.
- Kept it Phase-1-native rather than introducing a new subsystem:
  - reused the existing SQLite FTS surface
  - kept HyperHunk objects as the scorer contract
  - resolved FTS hits back through an ingest-run occurrence cache
  - kept Bootstrap Nucleus as the final gate
- Added new emitter knobs:
  - `emit --fts-candidate-limit <N>`
  - `emit --fts-fallback-thin-threshold <N>`
- Cleaned the boundary after the first patch:
  - removed raw duplicated FTS SQL from `core.py`
  - introduced a narrow shared FTS helper/seam for both assembler-side and retrieval-side lookup
- Ran `reference_probe_014_fts_fallback_v1_run2` on the same Python-reference footing as Probe 013:
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
  - `fts_fallback_fires = 1275`
  - `fts_raw_hits = 975`
  - `fts_selected = 572`
  - `fts_selected_cross_doc = 548`
- Current interpretation:
  - the FTS fallback is cheap enough to keep studying
  - but v1 did not improve the `115` cross-document plateau
  - so the next problem is no longer "add cheap fetch"
  - the next problem is "explain why cheap fetch is not converting into new pull edges"

## 2026-03-30 — Anisotropic blur experiment 001

Journal entry: pending mirror

- Added builder-side tool:
  - `.dev-tools/final-tools/tools/anisotropic_blur_probe.py`
- The new tool is intentionally builder-only:
  - query-anchored
  - FTS-seeded
  - local-subgraph only
  - directional weighted blur over existing relations
  - no runtime coupling to the app
- Added example job and smoke coverage to the final-tools toolbox.
- Validation passed:
  - `python .dev-tools/final-tools/smoke_test.py`

- Ran the blur lens on the Python reference bottleneck case:
  - DB: `reference_probe_013_anchor_registry_v1`
  - query: `"lexical analysis"`
  - artifact: `_docs/_analysis/reference_probe_013_anchor_registry_v1/anisotropic_blur_lexical_analysis.json`
- Read:
  - seeds were sensible and cross-document (`index.txt`, `lexical_analysis.txt`, `introduction.txt`, `expressions.txt`)
  - but the blur collapsed into dense `index.txt` list-item neighborhoods
  - top-cross-document count in the blur top set was `0`
  - the current bag remained more evidentially useful and more source-diverse on the same query

- Ran the blur lens on a healthier mixed graph:
  - DB: `appbuilder_toolbox_probe_002_det`
  - query: `"mcp server"`
  - artifact: `_docs/_analysis/appbuilder_toolbox_probe_002_det/anisotropic_blur_mcp_server.json`
- Read:
  - the blur surfaced a strong procedural/topological neighborhood around `smoke_test.py` and several tool `run(...)` functions
  - top-cross-document count in the blur top set was `4`
  - the current bag remained more directly relevant to the external-agent evidence use case

- Current interpretation:
  - the blur line is useful as a field-shape / neighborhood diagnostic
  - it is not yet a better relevance surface than the bag
  - keep it builder-side for now

## 2026-03-28 — List/index lane activation + Probe 010

Journal entry: pending mirror

- Added a tracked list/index-focused Splitter profile:
  - `_BDHyperNodeSPLITTER/_docs/signal_profiles/python_reference_list_index_v1.json`
- Extended PEG list-item emission so navigational items can infer section-like targets deterministically:
  - examples: `lexical_analysis`, `execution_model`, `line_structure`
- Kept this logic builder-facing and profile-gated so the default Splitter footing remains stable.
- Added Splitter tests proving:
  - list items still emit correctly
  - section-like index entries now produce normalized explicit targets

- Inspection of `reference/index.txt` under the list profile:
  - old behavior: `5` hunks with the table of contents collapsed into `fragment_of_md_list`
  - new behavior: `79` hunks with individual `md_list_item` units carrying normalized section-like targets

- Probe 010 used:
  - Splitter profile: `_BDHyperNodeSPLITTER/_docs/signal_profiles/python_reference_list_index_v1.json`
  - Bootstrap profile: `_BDHyperNeuronEMITTER/_docs/bootstrap_profiles/python_reference_prose_tuning.json`

- Probe 010 results vs Probe 009:
  - `content_nodes: 1083 -> 1256` (`+173`)
  - `occurrence_nodes: 1102 -> 1275` (`+173`)
  - `relations: 13510 -> 17392` (`+3882`)
  - `above-threshold training pairs: 12249 -> 15963`
  - `cross-document nucleus pull edges: 169 -> 115` (`-54`)

- Splitter-side signal summary for the full corpus under the list profile:
  - `ref-bearing hunks = 79`
  - `unique normalized refs = 77`

- Current interpretation:
  - the list/index lane successfully creates the missing explicit navigational signal
  - but the current bootstrap mostly converts that into denser local structure rather than better cross-document pull
  - this means the next gain likely requires scorer-side handling that can exploit the new list/index signal without over-favoring local structural coupling

## 2026-03-28 — Probe 011 widened comparison window

Journal entry: pending mirror

- Inspected the Emitter ingest path and found an important hidden limiter:
  - `GraphAssembler` compares each new hunk only against the previous `window_size` hunks
  - default `window_size = 50`
- This matters for the new list/index lane because many early `index.txt` items age out of the buffer before their target documents arrive later in the corpus.

- Exposed `window_size` as a builder-facing dial:
  - `_BDHyperNeuronEMITTER/src/app.py` now accepts `--window-size`
  - `.dev-tools/final-tools/tools/probe_monitor.py` now accepts and persists `window_size`

- Probe 011 reused the same list/index Splitter profile as Probe 010, but widened the Emitter comparison window to `200`.

- Probe 011 vs Probe 010:
  - `relations: 17392 -> 22978` (`+5586`)
  - `cross-document nucleus pull edges: 115 -> 1175` (`+1060`)
  - `above-threshold training pairs: 15963 -> 21549`

- Interpretation:
  - recency clipping was a major hidden limiter
  - the list/index signal from Probe 010 was genuinely useful, but the default comparison window prevented many index-to-target comparisons from ever being evaluated

- New tradeoff:
  - the widened window restores strong cross-document pull
  - but it also explodes pair volume:
    - Probe 010 training pairs: `62475`
    - Probe 011 training pairs: `234900`
  - so the next likely step is smarter candidate selection rather than leaving the system on brute-force wider windows indefinitely

## 2026-03-28 — Probe 012 targeted reference candidates v1

Journal entry: pending mirror

- Added a targeted reference-aware candidate-selection path to `GraphAssembler`.
- New builder-facing dial:
  - `--reference-candidate-limit`
- The candidate path lets a new hunk compare against older prior hunks when:
  - the current hunk's normalized refs match prior target hints, or
  - the current hunk's target hints match prior normalized refs
- This is separate from the local sliding window and is meant to preserve long-range index-to-target comparisons without widening the entire recent-history window.

- Added emitter test coverage proving that a reference-targeted pair can survive beyond the normal sliding window when `reference_candidate_limit > 0`.

- Probe 012 configuration:
  - Splitter profile: `_BDHyperNodeSPLITTER/_docs/signal_profiles/python_reference_list_index_v1.json`
  - Bootstrap profile: `_BDHyperNeuronEMITTER/_docs/bootstrap_profiles/python_reference_prose_tuning.json`
  - `window_size = 50`
  - `reference_candidate_limit = 24`

- Probe 012 results:
  - `relations = 19602`
  - `cross-document nucleus pull edges = 115`
  - `above-threshold training pairs = 18173`

- Important forensic confirmation:
  - the concrete pair
    - `index.txt :: doc/h1_the_python_language_reference/li_4`
    - `lexical_analysis.txt :: doc/h1_2_lexical_analysis`
    now lands above threshold in Probe 012
  - so the targeted candidate path works mechanically

- Current interpretation:
  - candidate-selection v1 is too narrow or poorly ranked to recover the broad Probe 011 cross-document gain
  - but it is strong enough to prove the concept
  - this is now an optimization/design problem, not a “does targeted long-range comparison work at all?” problem

## 2026-03-26 — Phase 1 baseline cleanup + App Journal verification

Journal entry: `journal_final_cleanup_20260326`

- Promoted the extracted app line from design-stage staging area to a runnable Phase 1 baseline.
- Removed runtime dependence on the shared design contract by giving Splitter and Emitter local runtime contract ownership.
- Fixed Splitter CLI hygiene and UTF-8 output so NDJSON handoff is stable on Windows.
- Fixed Emitter runtime seams, including import fallbacks and embed-provider compatibility.
- Turned Splitter’s richer engines into declared dependencies and preserved provenance when the Negotiator fragments AST/CST-derived hunks.
- Re-ran smoke flows:
  - Splitter → Emitter markdown smoke passed
  - TreeSitter-backed code-path smoke passed with non-zero grammatical richness
  - App Journal manifest and package smoke passed after MCP stdio framing was corrected
- Restored a root launcher for the journal so the repo again has an obvious human entrypoint.

## Historical anchor

- `journal_tranche7_devlog` remains the tranche-specific log for the Emitter CLI, GUI, and original Phase 1 integration milestone.

## 2026-04-02 — Builder-side English triplet training loop

- Added a new builder-only tool:
  - `_BDHyperNeuronEMITTER/tools/english_triplet_training_loop.py`
- Purpose:
  - generate controlled general-English training data for later scorer / FFN work
  - keep the loop minimally invasive and outside live runtime paths
- V1 shape:
  - runtime-selected Ollama model
  - core-English seed-word list
  - high-contrast example families:
    - `anchor`
    - `semantic_match`
    - `structural_match`
    - `grammatical_nonsense`
    - `syntactic_shift`
  - accepted/rejected NDJSON outputs
  - SQLite/FTS uniqueness registry used as a deterministic filter, not the primary corpus artifact
- Added:
  - bundled core-English seed list
  - example JSON job
  - focused unit tests
- Ran a first real local smoke with:
  - `qwen2.5:0.5b`
  - built-in core-English list
  - `word_limit = 1`
  - result:
    - `accepted_bundle_count = 1`
    - `accepted_example_count = 5`
    - `rejected_attempt_count = 1`
- Current read after the real smoke:
  - the generation path is working end to end
  - but prompt/validator sharpness still needs follow-up before a larger English tranche
- Current trust boundary:
  - this is a builder-side corpus-growth seam only
  - it is not yet wired into live ingest, live training, or Phase 2 runtime behavior
