# BDNeuralTranslationSUITE — Project Backlog

_Last updated: 2026-04-01. Mirrored in journal as entry `journal_backlog_001`. Use `_docs/WE_ARE_HERE_NOW.md` as the fastest pickup note after interruption._

---

## Current Footing

Phase 1 baseline is complete and runnable:
- Splitter → NDJSON → Emitter → Nucleus → Cold Artifact works
- Bootstrap Nucleus is live
- App Journal is installed and verified
- Root docs now carry an explicit recovery checkpoint and root architecture note

The project is now pointed at a solid prototype path, not at open-ended invention.

---

## Tranche 9 — Recovery Checkpoint + Doctrine Lock ✅ (2026-03-27)

- [x] Added root [`_docs/ARCHITECTURE.md`] — authoritative architecture truth for the active project line
- [x] Added root [`_docs/WE_ARE_HERE_NOW.md`] — overwrite-at-each-milestone crash-recovery / onboarding note
- [x] Re-centered backlog and dev log on the current root project rather than the old `final/` staging layout
- [x] Recorded current sequencing doctrine:
  - neurons first
  - living graph second
  - bag seam third
- [x] Recorded explicit non-goals so the project does not drift into FFN or bag work too early
- [x] Captured the latest Emitter UI lifecycle cleanup in the active project memory surfaces

---

## Tranche 10 — Splitter Corpus Hardening ACTIVE

Goal: turn the Splitter from “runnable baseline” into a trustworthy neuron-population substrate using real corpus passes.

### Immediate tasks

- [ ] Run `info` and `stream` passes against `_corpus_examples/python-3.10.20-docs-text`
- [ ] Run `info` and `stream` passes against `_corpus_examples/python-3.11.15-docs-text`
- [x] Run a baseline prose ingest against `_corpus_examples/webstersdictinoary.txt`
- [x] Start a recorded corpus metrics table in `_docs/SPLITTER_CORPUS_BASELINES.md`
- [ ] Capture richness / node-kind / engine-mix observations for each corpus
- [ ] Identify the weakest surface populations by corpus and file type
- [ ] Improve TreeSitter / PEG / fallback seams where output is thin, noisy, or obviously mis-shaped
- [x] Push representative corpus output through the Emitter and inspect resulting graph/training-pair quality
- [x] Record graph probe results in `_docs/GRAPH_PROBES.md`
- [x] Establish a repeatable probe-report loop with `.dev-tools/final-tools/tools/graph_probe_report.py`
- [x] Expose bootstrap scaffold dials through Emitter CLI + optional JSON profile
- [x] Persist `bootstrap_profile_effective.json` with emit/probe artifacts
- [x] Add emitter-local tests for bootstrap config validation and scaffold behavior
- [x] Add a tracked starter tuning profile for Python reference probe work
- [x] Add a builder-only probe monitor with live event/log capture and optional tiny monitor UI

### Immediate follow-up fork

- [ ] Decide whether to improve NL/list/index representation one more step before more Emitter work
- [x] If staying in Emitter next: inspect whether prose-heavy bootstrap routing is too grammar-dominant
- [x] After the next targeted change, run Probe 002 and compare it against Probe 001 mechanically
- [x] Moderate the first bootstrap de-bias pass so relation volume recovers without returning to grammar collapse
- [x] Test whether edge-threshold retuning is needed once prose grammatical matching is less absolute
- [x] Run Probe 003 with the tracked starter profile
- [ ] Improve cross-document pull recovery while keeping `grammatical_dominant` well below Probe 001
- [ ] Decide whether Probe 003 should be the new tuning baseline or whether one more starter-profile pass is needed first
- [x] Run Probe 004 through `.dev-tools/final-tools/tools/probe_monitor.py` so the next tuning pass is both observable and reproducible
- [x] Confirm Probe 004 matches the Probe 003 footing and can serve as an observable replay baseline
- [x] Run Probe 005 through `.dev-tools/final-tools/tools/probe_monitor.py` after one targeted profile change
- [x] Run Probe 006 through `.dev-tools/final-tools/tools/probe_monitor.py` after one heading-targeted profile change
- [x] Fix the builder monitor `hold_open` lifecycle by isolating the tiny Tk viewer in its own helper process
- [x] Run Probe 007 through `.dev-tools/final-tools/tools/probe_monitor.py` after adding a narrow explicit-reference structural dial
- [x] Confirm Probe 007 does not improve cross-document pull because the current `cross_refs` signal is too sparse/weakly extracted
- [x] Add a Splitter-side signal control layer with builder-facing JSON profiles and effective-profile persistence in probe artifacts
- [x] Keep the five-surface runtime contract stable while adding flat facet-ready fields (`normalized_cross_refs`, `reference_kinds`, `list_role`, `list_depth`, `reference_confidence`)
- [x] Add root `_docs/FACET_READY_SURFACE_DESIGN.md` as doctrine only, without runtime schema migration
- [x] Run a default-profile regression probe after the Splitter control-layer tranche
- [x] Run a richer-reference probe with persisted Splitter signal profile through the live builder monitor
- [x] Confirm the new Splitter control layer does not perturb the Probe 003/004 footing by default
- [x] Confirm the Python reference text corpus still exposes only sparse explicit-reference signal (`2` ref-bearing hunks, `1` unique normalized target) even after richer Splitter reference extraction
- [x] Test list/index representation as a stronger explicit-signal lane by emitting `md_list_item` hunks with inferred section-title targets
- [x] Measure the list/index lane against the same bootstrap footing in a visible probe
- [x] Expose emitter comparison window as a builder-side dial and test whether recency clipping is suppressing list/index-derived cross-document pull
- [x] Expose a targeted reference-aware candidate-selection path and test whether it can recover Probe 011 behavior without a brute-force wider window
- [ ] Decide whether the next move is:
  - keep a larger window temporarily as the new probe baseline, or
  - refine the targeted candidate-selection path so it recovers more of the Probe 011 gain without brute-force window growth
- [ ] Keep an eye on pair explosion when widening the window (`62475 -> 234900` training pairs from Probe 010 to Probe 011)
- [ ] Keep an eye on recall loss when narrowing back to targeted candidates (`1175 -> 115` cross-document pull from Probe 011 to Probe 012 at limit 24)
- [x] Replace the simple long-range token index with a ranked occurrence-level anchor registry
- [x] Add anchor-registry tests for stronger-anchor preference and common-term suppression
- [x] Run Probe 013 against the same Python-reference list/index footing after the anchor-registry upgrade
- [x] Add a deterministic FTS cheap-fetch fallback when anchor recall returns too little signal
- [x] Run Probe 014 against the same Python-reference list/index footing after the FTS fallback landed
- [x] Decide why Probe 014 stayed flat on the headline metric:
  - `cross-document pull = 115` unchanged
  - even though `fts_selected_cross_doc = 548`
  - current read: the one-lens Bootstrap scorer was part of the plateau
- [x] Inspect structural losers versus grammatical winners directly:
  - used the conversion reports to compare winner/loser routing patterns
  - confirmed structurally plausible cross-document pairs were losing badly under the generic lens
- [x] Test scorer-side promotion of structurally plausible cross-document bridges without broad architecture changes
- [x] Test an origin-aware Bootstrap branch for cross-document pairs:
  - kept the same-document path close to the current footing
  - reduced cross-document dependence on grammatical / verbatim similarity
  - rewarded shared-anchor / shared-dependency structure before any intent-aware logic
  - used current `cross_refs`, `normalized_cross_refs`, and `import_context` as the first v1 signal seam
- [x] Turn the origin-aware branch into a rudimentary ablation gradient:
  - fractions only -> `150`
  - fractions + threshold scaling -> `228`
  - fractions + shared-anchor bonus -> `155`
  - current read: threshold scaling is the strongest near-term lever
- [x] Run a threshold sweep on the origin-aware branch at fixed pair cost:
  - current ladder now spans `0.95 -> 206` through `0.30 -> 8458`
  - current read: the old cross-document gate was far too strict
  - current read: `0.40` is the first warning zone and `0.30` is too permissive
- [ ] Refine the origin-aware cross-document profile inside the promising trust band:
  - current likely band: `0.50`–`0.65`
  - keep pair count stable while choosing a trustworthy default
  - inspect weakest admitted winners, not just top-line pull count
- [ ] Treat the current `0.58` origin-aware footing as the active anchor lens while mapping overlay lenses:
  - do not churn the anchor lens casually
  - use overlays or bounded side-lenses when exploring new behavior
- [ ] Promote bag usefulness to a co-equal acceptance surface during trust-band selection:
  - keep bag checks on `hop_limit = 1`
  - prefer profiles that improve human-facing top-item quality on representative queries
  - current leading bag-first default candidate: `0.58`
- [x] Quality-control the first semantic-gravity overlay family through the bag:
  - deterministic control
  - deterministic high gravity
  - sentence-transformers control
  - sentence-transformers high gravity
  - read: deterministic remains stronger on both graph shape and current human-facing shelf
- [x] Run a compact deterministic semantic-gravity shape QC on the same human-facing shelf:
  - `steep`
  - `softplus`
  - `high`
  - `xhigh`
  - read: all preserve the same top shelf on the 11-query validation set
- [ ] Decide whether deterministic high semantic gravity should become the next promoted experiment lane:
  - graph result is stronger
  - current bag QC did not degrade the top shelf
  - still inspect broader/stubborn query families before promoting it as a default
- [ ] Decide whether `steep` or `softplus` should be the promoted deterministic semantic-gravity default:
  - `steep` currently looks safer for preserving more non-semantic winner geometry
  - `softplus` currently looks like the strongest practical compromise
  - `xhigh` is a useful ceiling point, not an obvious default
- [ ] Decide whether semantic should now be treated as a bounded overlay field:
  - current read: attraction field yes
  - primary support beam no
  - only promote if bag-side quality supports the graph-side lift
- [ ] Keep the live probe monitor evolving as a first-class observer surface:
  - current state now includes live metric cards, summary/sample tabs, and five-surface color cues
  - next likely UI seam is a richer same-window message/update model for panel-specific refresh
- [ ] Record explicit Phase 1 exit criteria around five-surface functional integration:
  - each surface mapped in context
  - each surface measurably useful somewhere meaningful
  - bag trustworthy enough to act as the reader-facing evidence slice
  - training data stable enough to justify FFN comparison work
- [ ] Record the trust boundary explicitly in the active defaults:
  - do not promote `0.40` or lower as the default without stronger quality evidence
  - keep the sweep summaries attached to the chosen default so later agents can see why
- [ ] Keep bag-side quality checks attached to the chosen default:
  - `lexical analysis`
  - `encoding declarations`
  - `operator precedence`
  - `yield expressions`
  - `eval input`
  - `function definitions`
  - `lambda expressions`
  - `assignment expressions`
- [ ] Decide whether the Splitter contract needs a richer shared-target neighborhood for cross-document scoring:
  - current hunks already carry partial outbound-reference signal
  - triadic/shared-anchor scoring may still need stronger normalized target extraction
  - only do this after the `0.50`–`0.65` band stops paying off
- [ ] Keep an eye on the new Probe 013 tradeoff:
  - `relations = 17428` vs Probe 012 `19602`
  - `cross-document pull = 115` unchanged
  - this means the anchor registry is more selective, but not yet more cross-document effective
- [ ] Keep an eye on the new Probe 014 tradeoff:
  - `relations = 17457` vs Probe 013 `17428`
  - `training pairs = 63155` vs Probe 013 `62583`
  - `cross-document pull = 115` unchanged
  - this means cheap-fetch v1 stayed cheap, but did not convert into better pull
- [ ] Keep an eye on the new Probe 018 tradeoff:
  - `relations = 17592` vs control `17457`
  - `training pairs = 62896` vs control `62896`
  - `cross-document pull = 234` vs control `115`
  - this means origin-aware scoring materially improves conversion, but still recovers only part of Probe 011 `1175`
- [ ] Keep an eye on the new threshold-sweep tradeoff:
  - `0.65 -> 1975`, `0.60 -> 2480`, `0.50 -> 3876`
  - `0.40 -> 6312` is the first warning zone
  - `0.30 -> 8458` is too permissive on weakest-winner inspection
  - the next job is now trust-band selection, not raw metric escalation
- [ ] Decide whether the next targeted recall move is:
  - refine the origin-aware cross-document profile first, or
  - tighten the FTS fallback trigger/query/ranking so it fires only on signal-bearing hunks and retrieves better targets, or
  - broaden deterministic anchor/query surfaces beyond the current heading/index footing before fallback
- [ ] Do not promote the list/index profile to the new baseline unless it can recover cross-document pull, not just local relation volume
- [x] Expose a builder-side `artifact_root` for probe bundles so large `training_pairs_*.json` exports can be written to a larger storage drive
- [x] Add a single user-set builder-artifact home policy via `.dev-tools/final-tools/builder_settings.local.json`
- [x] Do a disk-pressure cleanup pass:
  - moved the existing `_docs/_analysis` probe library (`~9.14 GB`) into the external records home
  - restored `_docs/_analysis` as a junction so legacy paths still work
- [ ] Keep the external records library organized as future builder artifacts accumulate
- [x] Add a rudimentary agent-facing `bag` CLI seam over the existing retrieval path
- [x] Validate the `bag` command on real text/project graphs and record baseline bag artifacts/examples
- [x] Fix the Hot Engine bag propagation direction so activation follows stored `source_occ_id -> target_occ_id`
- [x] Add focused emitter tests proving the Hot Engine now propagates forward and does not back-propagate from seeded targets
- [ ] Decide whether bag query should decouple anchor budget from final returned item count:
  - current `provider.query()` still ties both to `top_k`
  - diagnostics so far say wider anchor counts alone do not improve the awkward reference queries
  - keep this as the next bag-shaping seam if the current default-band work stalls
- [ ] Tighten bag lexicalization / alias handling for stubborn human-facing queries:
  - current conservative lexical variants already help `eval input`
  - variant-aware bag rerank now also helps `function definitions` on the better trust-band DBs
  - remaining awkward cases look more like corpus-query wording mismatch than graph-direction failure
  - current clearest stubborn cases: `assignment expressions` and `lambda expressions`
  - keep this query-side / bag-side and do not mutate durable graph scoring for it
- [x] Prepare side-by-side deterministic-vs-traditional embedder comparison using the same bag/query workflow
- [x] Choose the first traditional embedder lane for comparison and define artifact/eval parity rules
- [x] Run a first side-by-side bag comparison on one text corpus and one mixed project corpus
- [ ] Decide whether to compare another traditional model next or to deepen bag-eval criteria around the current deterministic win
- [ ] Add a compact comparison reporter for bag-output deltas so future embedder/model tests are less manual
- [ ] Determine whether the deterministic train path should be widened beyond `.txt`-only corpora preparation
- [ ] Decide whether the next ingestion baseline should stay separated by corpus type or add one blended corpus probe
- [x] Add a builder-side anisotropic blur experiment lens over existing Cold Artifact DBs
- [x] Run the blur lens on:
  - the Python reference bottleneck case
  - one healthier mixed code/doc graph
- [ ] Decide whether to continue the blur line at all, and only if it remains diagnostic:
  - add hub damping / seed-diversity bias, or
  - stop there and keep the blur as a builder-only exploratory lens
- [ ] Do not treat the blur as a replacement for the bag unless it proves both:
  - better cross-document spread, and
  - better evidence usefulness

### Exit criteria

- [ ] At least one code-heavy corpus and one prose-heavy corpus ingest cleanly
- [x] At least one code-heavy corpus and one prose-heavy corpus ingest cleanly
- [ ] Grammatical and structural richness are meaningfully above all-fallback baseline where richer parsers apply
- [ ] Representative output survives Splitter → Emitter handoff without schema/path surprises
- [x] Representative output survives Splitter → Emitter handoff without schema/path surprises
- [x] We have a small, real training batch worth keeping for later FFN work

---

## Prototype Path After Tranche 10

### Tranche 11 — Graph Validation + Retrieval Sanity
- [ ] Treat the rest of Phase 1 as a five-vertex mapping program rather than a single-profile tuning exercise
- [ ] Record explicit Phase 1 exit criteria around functional integration of all five surfaces:
  - not equal strength
  - not mashed averaging
  - each surface mapped in context
  - each surface measurably affects scoring/routing somewhere meaningful
- [ ] Continue the vertex-reactivity map after the first shock-load sweep:
  - refine structural/statistical interaction mapping
  - re-run semantic mapping on a footing where the semantic lane is actually active
  - map verbatim/commonality behavior more deliberately
- [ ] Inspect Cold Artifact output on real ingests
- [ ] Verify routing profiles and edge reasons are useful to a human/agent inspector
- [ ] Tighten schema/versioning/query seams only where real corpus behavior demands it
- [ ] Promote the rudimentary bag from CLI proof to a stable query contract if it holds up on real graph use
- [ ] Record the Hot Engine direction fix and post-fix bag behavior as part of the stable bag contract if it survives another broader query pass
- [ ] Define the missing control layer for later retrieval:
  - scope-root types
  - resolution grammar by scope type
  - direction-of-spread categories
  - stop-unwinding logic
- [ ] Define the bag as a bounded slice rather than a generic retrieval list:
  - observer-side anchor
  - source-side anchor
  - bag as join boundary
  - response anchor as answer-shape constraint
- [ ] Define contradiction math for query-time graph use:
  - model contradiction first as explicit anti-signal pressure / penalty, not as missing similarity
  - separate positive support from negative pressure in scorer/query outputs
  - decide which contradiction signals are candidate-local, relation-local, or graph-neighborhood-local
  - keep v1 storage positive-edge-compatible unless a real anti-edge need is proven
- [ ] Prove contradiction handling is inspectable:
  - a human/agent should be able to see why something was down-ranked, blocked, or pressure-bent
  - contradiction math must not collapse into invisible threshold behavior
- [ ] Keep SPO / proposition-role refinement as a later retrieval/query upgrade, not the immediate bottleneck fix

### Tranche 12 — FFN Training Data Discipline
- [ ] Define training-record quality checks
- [ ] Define evaluation metrics and bootstrap-vs-FFN comparison method
- [ ] Export and curate enough interaction data to justify FFN bring-up

### Tranche 13 — First FFN Nucleus Prototype
- [ ] Implement the first learned scorer
- [ ] Compare against bootstrap behavior before allowing it to replace the bootstrap path

### Tranche 14 — Bag Seam Prototype
- [ ] Define the bag as the STM falloff membrane into the durable graph
- [ ] Prove capture, listing, resurfacing, and context rehydration

---

## Explicit Non-Goals Right Now

- [ ] Do not jump from the rudimentary bag into the full STM-facing bag membrane yet
- [ ] Do not jump from the rudimentary `bag` CLI straight into full bag orchestration/UI without validating the query contract first
- [ ] Do not implement the FFN yet
- [ ] Do not do broad retrieval redesign before corpus-driven graph validation
- [ ] Do not treat long-form historical docs as the primary truth over `_docs/ARCHITECTURE.md` and `_docs/WE_ARE_HERE_NOW.md`

---

## Known Technical Debt

| Item | Component | Priority | Notes |
|---|---|---|---|
| Keep shared and local contract copies synchronized | Both | Pre-ship | The shared `contract/` design surface and the component-local copies can drift. Any contract evolution must be mirrored deliberately before shipping standalone cuts. |
| Token budget uses char-estimate, not real tokenizer | Splitter | Phase 2 | `negotiator.py` still estimates tokens via character count. Real BPE tokenizer integration should wait until corpus/training artifacts are stable enough to justify it. |
| `_merge_hunk_stream` position heuristic | Splitter | Low | Secondary-engine hunk matching still relies on `document_position` tolerance. Good enough for now, but content-hash matching may be needed after larger corpus passes. |
| Cold Artifact schema evolution needs versioning discipline | Emitter | Medium | Future query/index work should be versioned deliberately rather than patched ad hoc. |
| Historical `final/...` path language remains in long-form docs and journal history | Root docs + journal | Low | This is mostly historical drift, not runtime risk. Keep active truth in the new root docs and normalize long-form/historical surfaces gradually. |
| `_docs/_BagOfEVIDENCE.md` is legacy, not active architecture truth | Root docs | Low | Keep as historical context for now, but do not let it compete with the current neuron/graph/bag doctrine. Archive or relocate later if it keeps confusing pickup flow. |

---

## Compliance Checklist (per builder contract)

- [x] Root `_docs/ARCHITECTURE.md` exists
- [x] Root recovery note `_docs/WE_ARE_HERE_NOW.md` exists
- [x] `_docs/builder_constraint_contract.md` exists
- [x] Component builder contracts exist in both component `_docs/` folders
- [x] `SOURCE_PROVENANCE.md` exists in both component `_docs/` folders
- [x] App journal install verified — manifest, DB, launcher path, and MCP smoke pass
- [x] App journal backlog mirror exists (`journal_backlog_001`)
- [x] Root docs now identify active truth surfaces and current next tranche
- [ ] Long-form historical docs and journal exports still need gradual normalization away from `final/...` language
