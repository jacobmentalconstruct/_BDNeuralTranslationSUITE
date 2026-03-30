# Facet-Ready Surface Design

_Status: doctrine note only. This file does not imply a runtime schema migration._

## Purpose

The active runtime contract still uses five flat surfaces on each HyperHunk:

- `verbatim`
- `structural`
- `grammatical`
- `statistical`
- `semantic`

That flat model remains the correct implementation footing for the current prototype. This note exists so future builders can deepen the model without losing continuity with the current code.

## Why Keep It Flat For Now

- The current pipeline is still proving which signals are worth preserving.
- Flat fields are easier to stream, serialize, inspect, and diff during probe work.
- The next measurable bottleneck is still signal quality, not contract complexity.
- A nested facet refactor now would add schema churn before the live graph behavior is stable enough to justify it.

## Future Shape

Treat each surface as a face with internal subfacets.

### `verbatim`

What the unit literally is.

Potential subfacets:
- content footprint
- origin identity
- raw span / byte offsets
- content hash lineage

### `structural`

Where the unit lives.

Potential subfacets:
- hierarchy
- locality
- sequence
- section ancestry
- list nesting

Current flat fields already pointing here:
- `structural_path`
- `parent_occurrence_id`
- `prev_sibling_occurrence_id`
- `heading_trail`
- `document_position`
- `sibling_count`
- `list_depth`

### `grammatical`

What kind of formed unit it is.

Potential subfacets:
- unit type
- code syntax role
- document rhetoric role
- explicit reference signals

Current flat fields already pointing here:
- `node_kind`
- `layer_type`
- `decorators`
- `base_classes`
- `import_context`
- `cross_refs`
- `normalized_cross_refs`
- `reference_kinds`
- `list_role`

### `statistical`

How the unit behaves in token/pattern space.

Potential subfacets:
- token geometry
- context continuity
- extraction provenance
- fragmentation lineage

Current flat fields already pointing here:
- `token_count`
- `context_window`
- `split_reason`
- `extraction_engine`
- `extraction_confidence`
- `reference_confidence`

### `semantic`

What the unit means in vector/latent space.

Potential subfacets:
- embedding family
- semantic confidence
- learned neighborhood traces
- later FFN-side interaction embeddings

## Guidance For Future Builders

- Do not introduce nested facet objects until probe evidence shows that the added structure will improve retrieval or scorer behavior.
- Prefer adding flat, optional, serializer-safe fields first, then grouping them conceptually here.
- When a future refactor does happen, keep a compatibility layer so old probe artifacts and journal notes remain interpretable.
- Use this note as a map for future contract evolution, not as a command to refactor now.
