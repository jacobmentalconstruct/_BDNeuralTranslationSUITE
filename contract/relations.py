"""relations.py — Edge predicate registry for the v2 Relational DSL.

Dimension 2 (Ontological): formal definitions for every edge type in the DAG.

This module is the single source of truth for edge predicates. The Emitter's
Relational DSL, the A-matrix builder, and the query engine all derive their
edge semantics from this registry. Nobody hardcodes op strings elsewhere.

Each EdgePredicate defines:
  - name        — the canonical op string (e.g. "pull")
  - inverse     — the name of the reverse predicate (e.g. "pulled_by")
  - cardinality — how many targets a source can have ("1:1", "1:N", "N:1", "N:N")
  - transitive  — whether the relation chains (A→B + B→C implies A→C)
  - default_weight — default coupling weight for A-matrix construction
  - description — human-readable explanation

Predicate Set
-------------
V1 predicates (carried forward):
  pull        — structural parent edge (from child to parent)
  precedes    — left sibling sequence edge (from right to left)

V2 predicates (new):
  scope_member_of — scope containment (from inner to outer scope name)
  section_of      — heading containment (from block to heading text)
  references      — cross-reference link (from source to target)

Physics Interpretation
----------------------
In the equation h_{t+1} = alpha*h_t + A*h_t - H*h_t:
  - Each predicate contributes entries to the A matrix.
  - The default_weight determines the coupling strength.
  - Transitive predicates may contribute indirect entries (A^2, A^3)
    depending on the query engine's hop configuration.
  - Inverse predicates allow bidirectional traversal without storing
    redundant edges — the inverse is derived at query time.

Usage
-----
    from contract.relations import lookup, inverse_of, validate_relation

    pred = lookup("pull")
    assert pred.inverse == "pulled_by"
    assert pred.cardinality == "N:1"
    assert pred.default_weight == 1.0

    assert inverse_of("precedes") == "follows"

    rel = {"op": "pull", "target": "abc123", "weight": 1.0}
    assert validate_relation(rel) is True
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

log = logging.getLogger(__name__)

# ── Data model ──────────────────────────────────────────────────────────────


@dataclass(frozen=True)
class EdgePredicate:
    """Formal definition of a Relational DSL edge type.

    Parameters
    ----------
    name : str
        The canonical op string used in the wire format.
    inverse : str or None
        Name of the inverse predicate. None if no inverse is defined.
    cardinality : str
        Relationship cardinality. One of "1:1", "1:N", "N:1", "N:N".
        "N:1" means many sources can point to one target (e.g. pull → parent).
    transitive : bool
        Whether the relation chains. If True, A→B and B→C implies A→C
        (relevant for multi-hop query traversal).
    default_weight : float
        Default coupling weight for A-matrix entries.
    description : str
        Human-readable explanation.
    """

    name: str
    inverse: Optional[str]
    cardinality: str
    transitive: bool
    default_weight: float
    description: str


# ── Registry ────────────────────────────────────────────────────────────────

_PREDICATES: Dict[str, EdgePredicate] = {}


def _register(pred: EdgePredicate) -> None:
    """Add an EdgePredicate to the registry. Internal use at module load time."""
    _PREDICATES[pred.name] = pred


# ── V1 predicates (carried forward) ────────────────────────────────────────

_register(EdgePredicate(
    name="pull",
    inverse="pulled_by",
    cardinality="N:1",
    transitive=False,
    default_weight=1.0,
    description="Structural parent edge. Child pulls toward parent.",
))

_register(EdgePredicate(
    name="pulled_by",
    inverse="pull",
    cardinality="1:N",
    transitive=False,
    default_weight=1.0,
    description="Inverse of pull. Parent is pulled_by children.",
))

_register(EdgePredicate(
    name="precedes",
    inverse="follows",
    cardinality="1:1",
    transitive=True,
    default_weight=0.8,
    description="Left sibling sequence edge. Right node precedes left.",
))

_register(EdgePredicate(
    name="follows",
    inverse="precedes",
    cardinality="1:1",
    transitive=True,
    default_weight=0.8,
    description="Inverse of precedes. Left node follows right.",
))

# ── V2 predicates (new) ────────────────────────────────────────────────────

_register(EdgePredicate(
    name="scope_member_of",
    inverse="scope_contains",
    cardinality="N:1",
    transitive=True,
    default_weight=0.6,
    description="Scope containment. Inner scope is member_of outer scope name.",
))

_register(EdgePredicate(
    name="scope_contains",
    inverse="scope_member_of",
    cardinality="1:N",
    transitive=True,
    default_weight=0.6,
    description="Inverse of scope_member_of. Outer scope contains inner.",
))

_register(EdgePredicate(
    name="section_of",
    inverse="section_contains",
    cardinality="N:1",
    transitive=False,
    default_weight=0.5,
    description="Heading containment. Block belongs to a heading section.",
))

_register(EdgePredicate(
    name="section_contains",
    inverse="section_of",
    cardinality="1:N",
    transitive=False,
    default_weight=0.5,
    description="Inverse of section_of. Heading contains blocks.",
))

_register(EdgePredicate(
    name="references",
    inverse="referenced_by",
    cardinality="N:N",
    transitive=False,
    default_weight=0.4,
    description="Cross-reference link. Source block references a target.",
))

_register(EdgePredicate(
    name="referenced_by",
    inverse="references",
    cardinality="N:N",
    transitive=False,
    default_weight=0.4,
    description="Inverse of references. Target is referenced_by source.",
))


# ── Public API ──────────────────────────────────────────────────────────────


def lookup(name: str) -> Optional[EdgePredicate]:
    """Look up an EdgePredicate by name. Returns None if not found."""
    pred = _PREDICATES.get(name)
    if pred is None:
        log.warning("Unregistered edge predicate: %r", name)
    return pred


def inverse_of(name: str) -> Optional[str]:
    """Return the inverse predicate name, or None if undefined."""
    pred = _PREDICATES.get(name)
    if pred is None:
        return None
    return pred.inverse


def validate_relation(rel: Dict[str, Any]) -> bool:
    """Validate a Relational DSL dict.

    A valid relation must have:
      - "op" key with a registered predicate name
      - "target" key with a non-empty string
      - "weight" key with a positive number

    Returns True if valid, False otherwise.
    """
    if not isinstance(rel, dict):
        return False
    op = rel.get("op")
    if not isinstance(op, str) or op not in _PREDICATES:
        return False
    target = rel.get("target")
    if not isinstance(target, str) or not target:
        return False
    weight = rel.get("weight")
    if not isinstance(weight, (int, float)) or weight < 0:
        return False
    return True


def validate_relations(rels: List[Dict[str, Any]]) -> List[str]:
    """Validate a list of Relational DSL dicts.

    Returns a list of warning strings (empty = all valid).
    """
    warnings: List[str] = []
    for i, rel in enumerate(rels):
        if not isinstance(rel, dict):
            warnings.append(f"relation[{i}]: not a dict")
            continue
        op = rel.get("op", "<missing>")
        if op not in _PREDICATES:
            warnings.append(f"relation[{i}]: unregistered op {op!r}")
        if not rel.get("target"):
            warnings.append(f"relation[{i}]: missing or empty target")
        weight = rel.get("weight")
        if not isinstance(weight, (int, float)):
            warnings.append(f"relation[{i}]: weight is not a number")
        elif weight < 0:
            warnings.append(f"relation[{i}]: negative weight {weight}")
    return warnings


def register(predicate: EdgePredicate) -> None:
    """Register a custom EdgePredicate at runtime.

    Use this for project-specific edge types that aren't in the default set.
    """
    if predicate.name in _PREDICATES:
        log.info("Overwriting existing EdgePredicate: %s", predicate.name)
    _PREDICATES[predicate.name] = predicate


def all_predicates() -> Dict[str, EdgePredicate]:
    """Return a copy of the full predicate registry."""
    return dict(_PREDICATES)
