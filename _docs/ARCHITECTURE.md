# BDNeuralTranslationSUITE — Root Architecture

_Last updated: 2026-03-27. This is the root architecture truth for the active project line._

---

## What This App Is

BDNeuralTranslationSUITE is a durable evidence and relational-memory engine for agents.

It is not primarily an answer generator.
Its job is to preserve context as inspectable multi-surface units, connect those units in a living graph, and expose evidence with a traceable reason for why that evidence rose.

---

## Core Doctrine

The system is built around three layers:

1. **Neuron / HyperHunk layer**
   - The durable unit is a neuron-like fragment with five surfaces:
     - `verbatim`
     - `structural`
     - `grammatical`
     - `statistical`
     - `semantic`

2. **Living graph layer**
   - Neurons are connected by interaction, not just by fixed schema.
   - The Nucleus decides how strongly two neurons couple and which surfaces mattered.
   - The graph stores not only that an edge exists, but why it exists via routing data.

3. **Bag layer** _(future, not current tranche)_
   - The bag is the membrane between an agent's sliding-window short-term memory and the durable graph-backed memory.
   - When context would normally fall off, the bag captures it as durable inspectable units and later helps re-surface it when relevant.

Compressed:

- neurons are the durable unit
- the graph is the living memory substrate
- the bag is the STM-to-memory membrane

---

## Current Component Boundaries

### `_BDHyperNodeSPLITTER`

The Splitter reads source files and documents, then emits NDJSON HyperHunks.

Its responsibility is to populate surfaces, not to decide graph meaning.

Current engines:
- `FallbackEngine` — universal baseline
- `PEGEngine` — structured prose / markdown path
- `TreeSitterEngine` — code path when parser deps are present
- `Negotiator` — token-budget enforcement after merge

### `_BDHyperNeuronEMITTER`

The Emitter consumes HyperHunks, enriches semantic state, evaluates interaction, and writes the Cold Artifact graph.

Its responsibility is to decide relation strength and preserve explainable edge data.

Current major pieces:
- training pipeline
- deterministic embedding provider
- Bootstrap Nucleus
- Graph Assembler
- SQLite Cold Artifact
- Tk UI for training / inspection / demo

### `contract/`

`contract/` is the shared design surface for wire-format and registry coordination.
Each app owns its local runtime contract copies under `src/core/contract/`.

---

## The Nucleus

The Nucleus is the interaction axis.

It does not generate final prose answers.
It scores how two neurons should relate.

Current Phase 1 behavior:
- fixed-weight bootstrap scorer
- outputs connection strength
- outputs routing profile
- stores why an edge happened

Future Phase 2 behavior:
- learned FFN scorer trained on accumulated interaction data
- compared against the bootstrap scorer before adoption

---

## The Bag

The bag is not the first thing to build.

It depends on the neuron layer and living graph being trustworthy first.

Target role of the bag:
- sit under STM falloff
- retain context that would otherwise be summarized away or dropped
- expose bag contents to the agent as inspectable memory
- bridge agent-local conversational subgraphs to other data-source subgraphs

This means the correct build order is:
- neurons first
- living graph second
- bag seam third

---

## Current Project State

The current root is a self-contained project bundle.

What is working now:
- Splitter CLI is runnable
- Emitter CLI/UI are runnable
- HyperHunk NDJSON handoff works
- Bootstrap Nucleus writes routing-aware edges
- Cold Artifact graph path is live
- App Journal is installed and verified

What is intentionally not done yet:
- FFN Nucleus
- full bag implementation
- final retrieval polish for agent integration

---

## Active Tranche

Current tranche: **cleanup, recovery checkpointing, and Splitter corpus hardening**

This tranche exists to make the project survivable across interruption and to improve the quality of the neuron substrate before any FFN or bag work begins.

### In scope now

- authoritative root docs
- recovery/onboarding note
- synced TODO/dev-log/journal state
- real corpus ingest on `_corpus_examples`
- Splitter surface-quality improvements

### Explicit non-goals now

- no bag implementation
- no FFN implementation
- no major new UI work
- no broad retrieval redesign

---

## Prototype-Done Definition

A solid prototype exists when:

- real corpora ingest cleanly
- neurons carry useful multi-surface data
- the graph is inspectable and stable
- evidence can be surfaced with traceable reasons
- bootstrap interaction data is sufficient to begin FFN training

That is the finish line for the current planning horizon.
