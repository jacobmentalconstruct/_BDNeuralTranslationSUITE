"""HyperHunk v2 — shared wire-format contract between Splitter and Emitter.

WIRE FORMAT CONTRACT
--------------------
This is the boundary object between _BDHyperNodeSPLITTER and _BDHyperNeuronEMITTER.

Version 2 preserves the v1 identity model exactly (no hash breaks) and adds
richly contextual optional fields that the v2 engines populate during splitting.

HASH STABILITY (DO NOT CHANGE)
-------------------------------
  hunk_id       sha256(node_kind + ':' + content)
                ContentNode identity. CIS dedup invariant.
                Same content + same node_kind = same hunk_id, regardless of origin.

  occurrence_id sha256(origin_id + ':' + structural_path + ':' +
                       str(sibling_index) + ':' + hunk_id)
                OccurrenceNode identity. Unique per structural position.
                Two identical paragraphs in different sections → same hunk_id,
                different occurrence_ids.

DAG EDGES
---------
  parent_occurrence_id      upward edge (structural parent)
  prev_sibling_occurrence_id sequence edge (left sibling)

These always reference occurrence_ids, never hunk_ids.

V2 FIELDS — WHAT WAS BEING LOST AND IS NOW CAPTURED
----------------------------------------------------
All v2 fields are optional with safe defaults. A v1 producer emitting only
the v1 fields will produce a valid v2 HyperHunk with all new fields at default.

Scope context (TreeSitter engine):
  scope_stack         Full name chain from outermost scope to immediate parent.
                      e.g. ["AuthModule", "OAuthHandler", "refresh_token"]
                      v1 equivalent: only the structural_path type string was kept.

  scope_docstrings    Docstrings of enclosing named scopes (name → docstring).
                      e.g. {"OAuthHandler": "Handles all OAuth 2.0 flows..."}
                      v1 equivalent: completely discarded.

  base_classes        For class_definition nodes: inherited base class names.
                      e.g. ["BaseHandler", "LogMixin"]
                      v1 equivalent: completely discarded.

  decorators          Decorator strings applied to this node.
                      e.g. ["@staticmethod", "@app.route('/api/v1/token')"]
                      v1 equivalent: completely discarded.

  import_context      File-level import statements relevant to this hunk.
                      Subset: only imports whose names appear in content.
                      v1 equivalent: completely discarded.

Document structure (PEG engine):
  heading_trail       Breadcrumb of heading TEXT from document root to this block.
                      e.g. ["Getting Started", "Windows", "Troubleshooting"]
                      v1 equivalent: structural_path had the type but not the text.

  cross_refs          Markdown [text](target) references found in this block.
                      e.g. ["../installation.md#step-3", "https://example.com"]
                      v1 equivalent: completely discarded.

Neighborhood context (all engines):
  context_window      Last N BPE tokens of the preceding hunk (sliding window).
                      Empty string if this is the first hunk or overlap is off.
                      This is the key integration point: the Splitter's Negotiator
                      carries forward a token-budget-sized overlap so the Emitter
                      sees smooth cross-hunk signal rather than hard cut edges.
                      v1 equivalent: completely absent. Hard cuts everywhere.

  sibling_count       Total siblings at this scope level (including self).
                      Used by the Emitter for relative position weighting.
                      v1 equivalent: not tracked.

  document_position   Approximate 0.0–1.0 position in source (char_offset / total).
                      Rough spatial signal for the hot engine's topology state.
                      v1 equivalent: not tracked.

Budget / quality (Negotiator):
  token_count         BPE token count of content. Set by the token-aware Negotiator.
                      0 means "not computed" (backwards compat with v1 Negotiator).
                      v1 equivalent: Negotiator used len(content) (character count).

  split_reason        Why this split happened. One of:
                      "ast_boundary"       engine hit a clean AST node boundary
                      "token_budget"       Negotiator cut at token limit
                      "paragraph_boundary" PEG/Fallback hit a blank-line boundary
                      "char_limit"         fallback character-count cut
                      "heading_boundary"   PEG hit a markdown heading
                      ""                   not tracked (v1 compatibility)
                      v1 equivalent: not tracked.

Provenance (engine self-report):
  extraction_engine   Name of the engine class that produced this hunk.
                      e.g. "TreeSitterEngine", "PEGEngine", "FallbackEngine"
                      "" means not reported (v1 compatibility).
                      v1 equivalent: not tracked.

  extraction_confidence  Engine's confidence in its parse quality. 0.0–1.0.
                         1.0 = AST-precise boundary. 0.9 = PEG grammar match.
                         Lower values for regex fallback or sub-split fragments.
                         Default 1.0 (v1 compatibility — assume confident).
                         v1 equivalent: not tracked.

SURFACE MODEL (Relational Field Engine)
----------------------------------------
The flat fields above are grouped into 5 named data surfaces via property
accessors. These are READ lenses — no storage change, no wire format change.

  verbatim      content, origin_id
  structural    structural_path, sibling_index, parent/prev occurrence IDs,
                scope_stack, heading_trail, document_position, sibling_count
  grammatical   node_kind, layer_type, decorators, base_classes,
                import_context, scope_docstrings, cross_refs
  statistical   token_count, context_window, split_reason,
                extraction_engine, extraction_confidence
  semantic      (empty at base — Emitter populates with embeddings/relations)

A neuron's identity in the Relational Field Engine is defined by which
surfaces are populated. The surface_richness() method reports this.

RELATIONAL DSL (Emitter extension)
-----------------------------------
The Emitter's local copy of HyperHunk adds:
  attention_weight    property — semantic gravity by node_kind
  relations           property — algebraic JSON DAG relations

These are NOT defined here. They live in the Emitter's
  src/core/contract/hyperhunk.py
which extends this base dataclass.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class HyperHunk:
    """A content-addressed, structurally-aware, richly-contextual text hunk.

    Produced by the v2 Splitter. Consumed by the v2 Emitter.

    Required fields
    ---------------
    content       : str  — text payload (what gets embedded)
    origin_id     : str  — document/file identifier
    layer_type    : str  — 'AST' | 'CST' | 'REGEX' | 'CHAR'
    node_kind     : str  — semantic label for the hunk's role

    V1-compat optional fields (same as v1)
    ---------------------------------------
    structural_path              : str  — hierarchical doc path
    sibling_index                : int  — scope-local sequence counter
    parent_occurrence_id         : str  — upward DAG edge
    prev_sibling_occurrence_id   : str  — sequence DAG edge
    metadata                     : dict — pass-through bag

    V2 context fields (all optional, default-safe)
    -----------------------------------------------
    scope_stack        : List[str]        — full enclosing name chain
    scope_docstrings   : Dict[str, str]   — docstrings of enclosing scopes
    base_classes       : List[str]        — inherited class names (class nodes)
    decorators         : List[str]        — decorator strings on this node
    import_context     : List[str]        — relevant file-level import lines
    heading_trail      : List[str]        — markdown heading breadcrumb (PEG)
    cross_refs         : List[str]        — [text](target) links in content
    context_window     : str              — last N BPE tokens of preceding hunk
    sibling_count      : int              — total siblings at this scope
    document_position  : float            — 0.0–1.0 position in source
    token_count        : int              — BPE token count of content
    split_reason       : str              — why this split happened

    V2 provenance fields
    --------------------
    extraction_engine     : str   — engine class name that produced this hunk
    extraction_confidence : float — engine confidence in parse quality (0.0–1.0)
    """

    # ── Required ────────────────────────────────────────────────────────────
    content:     str
    origin_id:   str
    layer_type:  str
    node_kind:   str

    # ── V1-compat optional ──────────────────────────────────────────────────
    structural_path:            str            = ""
    sibling_index:              int            = 0
    metadata:                   Dict[str, Any] = field(default_factory=dict)
    parent_occurrence_id:       Optional[str]  = None
    prev_sibling_occurrence_id: Optional[str]  = None

    # ── V2: scope context (TreeSitter) ──────────────────────────────────────
    scope_stack:       List[str]        = field(default_factory=list)
    scope_docstrings:  Dict[str, str]   = field(default_factory=dict)
    base_classes:      List[str]        = field(default_factory=list)
    decorators:        List[str]        = field(default_factory=list)
    import_context:    List[str]        = field(default_factory=list)

    # ── V2: document structure (PEG) ────────────────────────────────────────
    heading_trail: List[str] = field(default_factory=list)
    cross_refs:    List[str] = field(default_factory=list)

    # ── V2: neighborhood context (all engines) ──────────────────────────────
    context_window:    str   = ""
    sibling_count:     int   = 0
    document_position: float = 0.0

    # ── V2: budget / quality (Negotiator) ───────────────────────────────────
    token_count:  int = 0
    split_reason: str = ""

    # ── V2: provenance (engine self-report) ───────────────────────────────
    extraction_engine:     str   = ""
    extraction_confidence: float = 1.0

    # ── Auto-computed — excluded from __init__ ──────────────────────────────
    hunk_id:       str = field(init=False, repr=True)
    occurrence_id: str = field(init=False, repr=True)

    def __post_init__(self) -> None:
        # ContentNode identity — hash inputs MUST NOT CHANGE from v1
        content_payload = f"{self.node_kind}:{self.content}"
        self.hunk_id = hashlib.sha256(content_payload.encode()).hexdigest()

        # OccurrenceNode identity — hash inputs MUST NOT CHANGE from v1
        occurrence_payload = (
            f"{self.origin_id}:{self.structural_path}:"
            f"{self.sibling_index}:{self.hunk_id}"
        )
        self.occurrence_id = hashlib.sha256(
            occurrence_payload.encode()
        ).hexdigest()

    def __len__(self) -> int:
        return len(self.content)

    # ── Surface Accessors (Relational Field Engine) ───────────────────────
    #
    # These properties group the flat fields into 5 named data surfaces.
    # They are READ lenses — the underlying storage is still flat fields.
    # Wire format (to_dict/from_dict) is unchanged.
    #
    # The Emitter's extension populates the semantic surface.

    @property
    def verbatim_surface(self) -> Dict[str, Any]:
        """CIS-addressed raw content."""
        return {
            "content":   self.content,
            "origin_id": self.origin_id,
        }

    @property
    def structural_surface(self) -> Dict[str, Any]:
        """Topological position in the source document DAG."""
        return {
            "structural_path":            self.structural_path,
            "sibling_index":              self.sibling_index,
            "parent_occurrence_id":       self.parent_occurrence_id,
            "prev_sibling_occurrence_id": self.prev_sibling_occurrence_id,
            "scope_stack":                self.scope_stack,
            "heading_trail":              self.heading_trail,
            "document_position":          self.document_position,
            "sibling_count":              self.sibling_count,
        }

    @property
    def grammatical_surface(self) -> Dict[str, Any]:
        """Ontological classification and language-level metadata."""
        return {
            "node_kind":       self.node_kind,
            "layer_type":      self.layer_type,
            "decorators":      self.decorators,
            "base_classes":    self.base_classes,
            "import_context":  self.import_context,
            "scope_docstrings": self.scope_docstrings,
            "cross_refs":      self.cross_refs,
        }

    @property
    def statistical_surface(self) -> Dict[str, Any]:
        """Budget, provenance, and extraction quality metrics."""
        return {
            "token_count":           self.token_count,
            "context_window":        self.context_window,
            "split_reason":          self.split_reason,
            "extraction_engine":     self.extraction_engine,
            "extraction_confidence": self.extraction_confidence,
        }

    @property
    def semantic_surface(self) -> Dict[str, Any]:
        """Embedding-space data. Empty at base level — populated by Emitter."""
        return {}

    @property
    def surfaces(self) -> Dict[str, Dict[str, Any]]:
        """All 5 data surfaces as a single dict."""
        return {
            "verbatim":    self.verbatim_surface,
            "structural":  self.structural_surface,
            "grammatical": self.grammatical_surface,
            "statistical": self.statistical_surface,
            "semantic":    self.semantic_surface,
        }

    def surface_richness(self) -> Dict[str, float]:
        """Fraction of non-default fields populated per surface (0.0–1.0).

        Useful for the Surveyor to report which engines contributed data.
        """
        _DEFAULTS: Dict[str, Any] = {
            # structural
            "structural_path": "", "sibling_index": 0,
            "parent_occurrence_id": None, "prev_sibling_occurrence_id": None,
            "scope_stack": [], "heading_trail": [],
            "document_position": 0.0, "sibling_count": 0,
            # grammatical — node_kind and layer_type are always set (required)
            "decorators": [], "base_classes": [], "import_context": [],
            "scope_docstrings": {}, "cross_refs": [],
            # statistical
            "token_count": 0, "context_window": "",
            "split_reason": "", "extraction_engine": "",
            "extraction_confidence": 1.0,
        }
        result = {}
        for name, surface in self.surfaces.items():
            if name == "verbatim":
                # verbatim is always populated (content is required)
                result[name] = 1.0
                continue
            if name == "semantic":
                # semantic is empty at base level
                result[name] = 0.0
                continue
            total = len(surface)
            if total == 0:
                result[name] = 0.0
                continue
            populated = sum(
                1 for k, v in surface.items()
                if v != _DEFAULTS.get(k, v)
            )
            result[name] = round(populated / total, 2)
        return result

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to a plain dict suitable for json.dumps() / NDJSON streaming.

        Includes all v2 fields. Emitter must handle missing keys gracefully
        when consuming v1 producer output (use .get() with defaults).
        """
        return {
            # Required
            "content":      self.content,
            "origin_id":    self.origin_id,
            "layer_type":   self.layer_type,
            "node_kind":    self.node_kind,
            # V1-compat
            "structural_path":            self.structural_path,
            "sibling_index":              self.sibling_index,
            "parent_occurrence_id":       self.parent_occurrence_id,
            "prev_sibling_occurrence_id": self.prev_sibling_occurrence_id,
            "metadata":                   self.metadata,
            # V2: scope context
            "scope_stack":      self.scope_stack,
            "scope_docstrings": self.scope_docstrings,
            "base_classes":     self.base_classes,
            "decorators":       self.decorators,
            "import_context":   self.import_context,
            # V2: document structure
            "heading_trail": self.heading_trail,
            "cross_refs":    self.cross_refs,
            # V2: neighborhood
            "context_window":    self.context_window,
            "sibling_count":     self.sibling_count,
            "document_position": self.document_position,
            # V2: budget / quality
            "token_count":  self.token_count,
            "split_reason": self.split_reason,
            # V2: provenance
            "extraction_engine":     self.extraction_engine,
            "extraction_confidence": self.extraction_confidence,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "HyperHunk":
        """Deserialize from a dict (v1 or v2 wire format).

        Missing v2 keys are filled with safe defaults so v1 producer
        output can be ingested without modification.
        """
        return cls(
            content=     d["content"],
            origin_id=   d["origin_id"],
            layer_type=  d["layer_type"],
            node_kind=   d["node_kind"],
            structural_path=            d.get("structural_path", ""),
            sibling_index=              d.get("sibling_index", 0),
            metadata=                   d.get("metadata", {}),
            parent_occurrence_id=       d.get("parent_occurrence_id"),
            prev_sibling_occurrence_id= d.get("prev_sibling_occurrence_id"),
            scope_stack=      d.get("scope_stack", []),
            scope_docstrings= d.get("scope_docstrings", {}),
            base_classes=     d.get("base_classes", []),
            decorators=       d.get("decorators", []),
            import_context=   d.get("import_context", []),
            heading_trail=    d.get("heading_trail", []),
            cross_refs=       d.get("cross_refs", []),
            context_window=    d.get("context_window", ""),
            sibling_count=     d.get("sibling_count", 0),
            document_position= d.get("document_position", 0.0),
            token_count=  d.get("token_count", 0),
            split_reason= d.get("split_reason", ""),
            extraction_engine=     d.get("extraction_engine", ""),
            extraction_confidence= d.get("extraction_confidence", 1.0),
        )
