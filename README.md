# BDNeuralTranslationSUITE — Portable Project Bundle

This repository root is now the portable bundle for the extracted v2 project.

## Purpose

This bundle contains the extracted Splitter + Emitter line, its shared design surface,
its project docs, its vendored App Journal tooling, a parts attic for older suite pieces,
and example corpora for training/ingestion work.

## Portable layout

```
project-root/
  _docs/                      <- root docs + journal DB + journal exports/config
  .dev-tools/_app-journal/    <- vendored journal package
  contract/                   <- shared design surface
  _BDHyperNodeSPLITTER/       <- extracted Splitter app
  _BDHyperNeuronEMITTER/      <- extracted Emitter app
  _parts/                     <- older suite pieces retained for reference / parts reuse
  _corpus_examples/           <- example ingest/training corpora
  open_journal.bat            <- launcher for the local copied journal
```

## Current status

Phase 1 baseline is runnable and self-contained inside this folder:

- `_BDHyperNodeSPLITTER` streams UTF-8 HyperHunk NDJSON.
- `_BDHyperNeuronEMITTER` ingests HyperHunk NDJSON and writes the Cold Artifact SQLite graph.
- Both components now own local runtime contract copies under `src/core/contract/`.
- `_docs/` carries the local docs and journal database.
- `.dev-tools/_app-journal/` carries the local journal UI/MCP package.

Known remaining gaps are Phase 2 / stub work, not basic runtime wiring:

- TreeSitter and PEG still need deeper enrichment passes where noted in component docs.
- FFN Nucleus remains deferred; Bootstrap Nucleus is the active scorer.
- The shared `contract/` folder is still the design surface and sync point for contract evolution.

## Start here after interruption

- `_docs/WE_ARE_HERE_NOW.md` is the fastest recovery note.
- `_docs/ARCHITECTURE.md` is the current root doctrine.
- `_docs/TODO.md` is the forward plan and tranche tracker.
- `_docs/DEV_LOG.md` is the short execution history.

## Notes for copy-out

- Treat this repository root as the project root.
- In `_docs` files, any historical `final/...` path references should be read as project-root-relative references from the old suite context.
- Run `open_journal.bat` from this folder to open the local journal against this root.

## Support folders

- `_parts/` keeps older suite components available as a reusable parts bin without mixing them back into the active extracted app line.
- `_corpus_examples/` holds example corpora, including a Webster dictionary source and a Python documentation corpus for ingestion/training experiments.

## Why a suite, not a monolith

Each component:
- Has a distinct dependency profile (tree-sitter vs numpy vs SQLite)
- Can be operated independently (split without embedding, query without re-splitting)
- Pipes cleanly to the next stage via NDJSON streams
- Can be tested and replaced independently

## Build order

1. `contract/hyperhunk.py` — the keystone. Nothing else starts until this is locked.
2. `contract/token_budget.py` — BPE budget module (pulled from Emitter's engine).
3. `_BDHyperNodeSPLITTER` — TreeSitter engine first, then PEG, then Fallback, then Negotiator.
4. `_BDHyperNeuronEMITTER` — surveyor, then assembler, then training, then inference.

## Active builder constraint

Each component folder contains `_docs/builder_constraint_contract.md`.
That contract governs all build decisions within the component.
