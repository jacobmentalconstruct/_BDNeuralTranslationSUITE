# contract/ — Shared v2 Wire Format

This folder is the shared design surface for the v2 HyperHunk wire contract.

## Status

SCAFFOLD — design in progress. Not yet stable.

## Files

- `hyperhunk.py`    — v2 HyperHunk dataclass. The keystone of the whole suite.
- `token_budget.py` — BPE-aware token budget module. Used by the Negotiator.

## Vendoring Note

This folder exists only during development. When a component is vendored out,
its local copy lives at:
  `src/core/contract/hyperhunk.py`
  `src/core/contract/token_budget.py`

There must be NO runtime import from this shared folder in the final vendored component.
Each vendored project owns its own local copy.

## Hash Stability Rule

The `hunk_id` and `occurrence_id` hash inputs MUST NOT CHANGE from v1:
  hunk_id       = sha256(node_kind + ':' + content)
  occurrence_id = sha256(origin_id + ':' + structural_path + ':' + sibling_index + ':' + hunk_id)

All new fields in v2 are additive context only. They do not affect identity.
This ensures v1 and v2 producers can coexist in the same cold_anatomy.db.
