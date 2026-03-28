"""ontology.py — Node type registry for the v2 HyperHunk wire format.

Dimension 2 (Ontological): WHAT things are.

This module is the single source of truth for node type definitions in the
entire suite. Every system behavior attached to a node type (attention weights,
coupling constants, dynamical role assignment, validation) derives from this
registry. Nobody hardcodes node_kind strings elsewhere.

Dynamical Roles
---------------
Each node type is assigned a dynamical role that describes its behavior in the
manifold physics (h_{t+1} = alpha*h_t + A*h_t - H*h_t):

  attractor   — High semantic gravity, pulls activation toward itself.
                Function/class definitions. Strong coupling in A.
  conductor   — Transmits activation efficiently between attractors.
                Module preambles, export statements.
  guide       — Structures traversal without holding much mass.
                Headings, section markers.
  carrier     — Default content carriers. Highest density in the graph.
                Paragraphs, prose blocks, list items.
  resonator   — Amplifies co-occurring signals at fine granularity.
                Code blocks, tables, data-dense blocks.

Type Hierarchy
--------------
Each NodeType has an optional `parent` field naming its supertype. This forms
a tree rooted at implicit abstract types (code_node, prose_node, fragment_node).
`is_subtype("method_definition", "code_node")` returns True.

Usage
-----
    from contract.ontology import lookup, validate, get_coupling, is_subtype

    nt = lookup("function_definition")
    assert nt.dynamical_role == "attractor"
    assert nt.default_coupling == 2.0
    assert validate("function_definition") is True
    assert validate("typo_definitoin") is False
    assert is_subtype("method_definition", "code_node") is True
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Dict, Optional

log = logging.getLogger(__name__)

# ── Data model ──────────────────────────────────────────────────────────────


@dataclass(frozen=True)
class NodeType:
    """Formal definition of a HyperHunk node_kind.

    Parameters
    ----------
    name : str
        The canonical node_kind string (e.g. "function_definition").
    parent : str or None
        Supertype in the type hierarchy (e.g. "code_node").
    layer_type : str
        Which engine layer typically produces this type.
        One of "AST", "CST", "REGEX", "CHAR".
    dynamical_role : str
        Role in the manifold physics.
        One of "attractor", "conductor", "guide", "carrier", "resonator".
    default_coupling : float
        Default coupling constant for A-matrix construction.
        Higher values = stronger pull on activation propagation.
    description : str
        Human-readable explanation.
    """

    name: str
    parent: Optional[str]
    layer_type: str
    dynamical_role: str
    default_coupling: float
    description: str


# ── Registry ────────────────────────────────────────────────────────────────

_REGISTRY: Dict[str, NodeType] = {}


def _register(nt: NodeType) -> None:
    """Add a NodeType to the registry. Internal use at module load time."""
    _REGISTRY[nt.name] = nt


# ── Abstract root types (not emitted directly, used for hierarchy) ──────────

_register(NodeType(
    name="code_node",
    parent=None,
    layer_type="AST",
    dynamical_role="attractor",
    default_coupling=1.0,
    description="Abstract root for all code-derived node types.",
))

_register(NodeType(
    name="prose_node",
    parent=None,
    layer_type="CST",
    dynamical_role="carrier",
    default_coupling=1.0,
    description="Abstract root for all prose/document-derived node types.",
))

_register(NodeType(
    name="fragment_node",
    parent=None,
    layer_type="CHAR",
    dynamical_role="resonator",
    default_coupling=0.7,
    description="Abstract root for sub-split fragment types.",
))

# ── Code types (AST engine) ────────────────────────────────────────────────

_register(NodeType(
    name="function_definition",
    parent="code_node",
    layer_type="AST",
    dynamical_role="attractor",
    default_coupling=2.0,
    description="Top-level or nested function.",
))

_register(NodeType(
    name="class_definition",
    parent="code_node",
    layer_type="AST",
    dynamical_role="attractor",
    default_coupling=2.0,
    description="Class definition.",
))

_register(NodeType(
    name="method_definition",
    parent="code_node",
    layer_type="AST",
    dynamical_role="conductor",
    default_coupling=1.8,
    description="Method inside a class body.",
))

_register(NodeType(
    name="decorated_definition",
    parent="code_node",
    layer_type="AST",
    dynamical_role="conductor",
    default_coupling=1.8,
    description="Function or class with decorators.",
))

_register(NodeType(
    name="class_declaration",
    parent="code_node",
    layer_type="AST",
    dynamical_role="conductor",
    default_coupling=1.8,
    description="Class declaration (JS/TS).",
))

_register(NodeType(
    name="function_declaration",
    parent="code_node",
    layer_type="AST",
    dynamical_role="conductor",
    default_coupling=1.8,
    description="Function declaration (JS/TS).",
))

_register(NodeType(
    name="export_statement",
    parent="code_node",
    layer_type="AST",
    dynamical_role="conductor",
    default_coupling=1.5,
    description="Module export (JS/TS).",
))

_register(NodeType(
    name="module_preamble",
    parent="code_node",
    layer_type="AST",
    dynamical_role="conductor",
    default_coupling=1.2,
    description="Accumulated imports and module-level constants.",
))

# ── Prose types (CST / PEG engine) ─────────────────────────────────────────

_register(NodeType(
    name="md_heading",
    parent="prose_node",
    layer_type="CST",
    dynamical_role="guide",
    default_coupling=1.5,
    description="Markdown heading (any level).",
))

_register(NodeType(
    name="md_code_block",
    parent="prose_node",
    layer_type="CST",
    dynamical_role="resonator",
    default_coupling=1.4,
    description="Fenced or indented code block in Markdown.",
))

_register(NodeType(
    name="md_paragraph",
    parent="prose_node",
    layer_type="CST",
    dynamical_role="carrier",
    default_coupling=1.0,
    description="Markdown paragraph.",
))

_register(NodeType(
    name="md_list",
    parent="prose_node",
    layer_type="CST",
    dynamical_role="carrier",
    default_coupling=1.0,
    description="Markdown list block.",
))

_register(NodeType(
    name="md_table",
    parent="prose_node",
    layer_type="CST",
    dynamical_role="resonator",
    default_coupling=1.0,
    description="Markdown table.",
))

_register(NodeType(
    name="md_blockquote",
    parent="prose_node",
    layer_type="CST",
    dynamical_role="carrier",
    default_coupling=0.9,
    description="Markdown blockquote.",
))

_register(NodeType(
    name="md_hr",
    parent="prose_node",
    layer_type="CST",
    dynamical_role="guide",
    default_coupling=0.3,
    description="Markdown horizontal rule (thematic break).",
))

# ── Fallback types (REGEX engine) ──────────────────────────────────────────

_register(NodeType(
    name="paragraph",
    parent="prose_node",
    layer_type="REGEX",
    dynamical_role="carrier",
    default_coupling=1.0,
    description="Blank-line-delimited paragraph (fallback engine).",
))

# ── Fragment types (Negotiator sub-split) ──────────────────────────────────
# Fragment types are dynamically named "fragment_of_<parent_kind>".
# The registry stores the base pattern; lookup falls back to this
# when the exact name isn't registered.

_register(NodeType(
    name="fragment_of_",
    parent="fragment_node",
    layer_type="CHAR",
    dynamical_role="resonator",
    default_coupling=0.7,
    description="Sub-split fragment of an oversized hunk (base pattern).",
))

# ── Default for unknown types ──────────────────────────────────────────────

_UNKNOWN = NodeType(
    name="_unknown",
    parent=None,
    layer_type="REGEX",
    dynamical_role="carrier",
    default_coupling=1.0,
    description="Fallback for unregistered node_kind values.",
)


# ── Public API ──────────────────────────────────────────────────────────────


def lookup(name: str) -> NodeType:
    """Look up a NodeType by name.

    For fragment types ("fragment_of_function_definition", etc.),
    returns the base "fragment_of_" definition if no exact match exists.

    Returns the _UNKNOWN sentinel for completely unrecognized names.
    """
    if name in _REGISTRY:
        return _REGISTRY[name]
    if name.startswith("fragment_of_"):
        return _REGISTRY.get("fragment_of_", _UNKNOWN)
    log.warning("Unregistered node_kind: %r — using default", name)
    return _UNKNOWN


def validate(name: str) -> bool:
    """Return True if name is a known (registered) node_kind."""
    if name in _REGISTRY:
        return True
    if name.startswith("fragment_of_"):
        return True
    return False


def get_coupling(name: str) -> float:
    """Return the default coupling constant for a node_kind."""
    return lookup(name).default_coupling


def get_dynamical_role(name: str) -> str:
    """Return the dynamical role for a node_kind."""
    return lookup(name).dynamical_role


def is_subtype(name: str, ancestor: str) -> bool:
    """Return True if `name` is a subtype of `ancestor` (walks parent chain).

    A type is considered a subtype of itself.
    """
    if name == ancestor:
        return True
    current = lookup(name)
    visited = {current.name}
    while current.parent is not None:
        if current.parent == ancestor:
            return True
        if current.parent in visited:
            break  # cycle guard
        visited.add(current.parent)
        current = lookup(current.parent)
    return False


def register(node_type: NodeType) -> None:
    """Register a custom NodeType at runtime.

    Use this for project-specific node kinds that aren't in the default
    registry. The registration is global for the process lifetime.
    """
    if node_type.name in _REGISTRY:
        log.info("Overwriting existing NodeType: %s", node_type.name)
    _REGISTRY[node_type.name] = node_type


def all_types() -> Dict[str, NodeType]:
    """Return a copy of the full registry."""
    return dict(_REGISTRY)
