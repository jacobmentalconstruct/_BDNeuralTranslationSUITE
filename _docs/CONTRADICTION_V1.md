# Contradiction v1

_Status: doctrine + implementation note only. This file describes the current truthful seam and the first narrow contradiction shape. It does not imply anti-edge schema, curvature runtime math, or physics-lens execution._

## Current Truth

As of 2026-03-30, the active Bootstrap Nucleus is still a positive-support scaffold scorer:

- all five surface similarities are non-negative
- routing is normalized positive contribution share
- connection strength is a positive weighted aggregate
- threshold miss simply prevents an edge from being written

That means contradiction is **not** first-class runtime behavior yet.

Today, failed or conflicting evidence mostly collapses into:

- low score
- threshold miss
- or non-selection before scoring

There is currently no:

- contradiction object
- anti-edge persistence
- curvature state
- physics-style contradiction routing

## Contradiction v1 Definition

Contradiction v1 is intentionally narrow.

It means:

- explicit anti-signal pressure
- candidate-level or scorer-level negative evidence
- block / penalize / warn style handling
- visible reasons for why a pair was down-ranked or blocked

It does **not** mean:

- anti-edge graph schema
- contradiction-as-curvature runtime claims
- lens execution
- broad retrieval redesign

## Current v1 Implementation Shape

The current first implementation path uses scorer-local anti-signal fields:

- `positive_support`
- `anti_signal_total`
- `anti_signal_reasons`
- `blocked`
- `connection_strength = max(0, positive_support - anti_signal_total)`

For now:

- positive graph edges remain the only persisted relation form
- contradiction pressure is surfaced mainly through training/export/inspection data
- disabled-by-default contradiction settings preserve the current runtime baseline

## NodeWALKER Seed

`_NodeWALKER` is relevant as a conceptual seed only.

The reusable idea is:

- decomposed score components
- explicit penalty channels
- block / penalize / warn decision handling

It is **not** a runtime dependency for this project.

## What Comes Later

Later query-time contradiction work may grow into:

- relation-local negative evidence
- graph-neighborhood pressure fields
- inspectable contradiction records
- richer query lenses

Those belong to a later query/math tranche, not the current Phase 1 ingest bottleneck fix.
