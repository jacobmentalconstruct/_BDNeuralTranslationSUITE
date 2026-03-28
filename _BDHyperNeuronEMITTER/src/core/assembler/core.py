"""core.py — Graph Assembler.

Ownership: core/assembler/core.py

The Graph Assembler is the Emitter's primary write path.  It ingests a stream
of HyperHunks, optionally embeds them, evaluates pair-wise edge scores via the
Bootstrap Nucleus, and persists the resulting graph into the Cold Artifact.

Architecture
------------
Ingest path (per hunk):
  1. Optionally embed (DeterministicEmbedProvider.embed) → set hunk.embedding
  2. Upsert into Cold Artifact via SqliteScribe (content_node + occurrence_node)
  3. Write structural relations (pull, precedes) from hunk.relations — these
     have real occurrence_id targets so go straight to the relations table
  4. Evaluate against a sliding window of recent hunks via BootstrapNucleus
  5. Write any Nucleus-scored edge above the strength threshold

Relation types written
----------------------
Structural (always written if pointers set):
  pull      — parent_occurrence_id is the target
  precedes  — prev_sibling_occurrence_id is the target
  Both carry a fixed "structural_bridge" routing_profile.

Nucleus-scored (written when strength ≥ threshold):
  op is derived from interaction_type:
    grammatical_dominant → "pull"     (grammatical match → treat as structural)
    structural_bridge    → "pull"     (structural affinity)
    statistical_echo     → "precedes" (sequential context)
    semantic_resonance   → "pull"     (semantic similarity)
    multi_surface        → "pull"     (mixed — default to pull)
  weight = connection_strength
  routing_profile and interaction metadata are stored on the edge.

Non-occurrence-id relations (scope_member_of, section_of, references) from
hunk.relations are NOT written into the relations table directly — they target
scope names / heading text / URLs that are not occurrence_ids.  These are
surfaced through the HyperHunk fields during retrieval and do not need to
be stored as Cold Artifact edges for Phase 1.

Sliding window
--------------
To avoid O(n²) comparisons, the Assembler maintains a buffer of the most
recent ``window_size`` hunks.  Each new hunk is compared against the entire
buffer.  Default window_size=50 covers dense cross-reference patterns while
keeping ingestion linear in practice.

Training data
-------------
Every Nucleus result (above and below threshold) can be exported as training
tuples via export_training_pairs().  The Assembler stores above-threshold
results only in the Cold Artifact; all pairs are available for Phase 2 FFN
training via the accumulated _training_pairs list.

No v1 counterpart — original for the v2 Relational Field Engine.
"""

from __future__ import annotations

import logging
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

log = logging.getLogger(__name__)

# ── Default op mapping from InteractionType ───────────────────────────────

_INTERACTION_TO_OP: Dict[str, str] = {
    "grammatical_dominant": "pull",
    "structural_bridge":    "pull",
    "statistical_echo":     "precedes",
    "semantic_resonance":   "pull",
    "multi_surface":        "pull",
}

# Routing profile for structural edges (fixed — no Nucleus involvement)
_STRUCTURAL_ROUTING = {"structural": 1.0, "grammatical": 0.0, "statistical": 0.0, "semantic": 0.0, "verbatim": 0.0}
_STRUCTURAL_VECTOR  = [0.0, 1.0, 0.0, 0.0, 0.0]


class GraphAssembler:
    """Builds the Cold Artifact graph from a HyperHunk stream.

    Parameters
    ----------
    db_path : Path or str
        Cold Artifact SQLite file path.
    nucleus : BootstrapNucleus
        Phase 1 fixed-weight Nucleus for edge scoring.
    embed_provider : optional
        DeterministicEmbedProvider instance.  If provided, each hunk is
        embedded before upsert and before Nucleus evaluation.
    window_size : int
        Sliding window for pair-wise Nucleus comparisons.  Default 50.
    """

    def __init__(
        self,
        db_path: "Path | str",
        nucleus: Any,  # BootstrapNucleus — lazy import avoids circular dep
        embed_provider: Optional[Any] = None,
        window_size: int = 50,
        reference_candidate_limit: int = 0,
    ) -> None:
        from .sqlite_scribe import SqliteScribe
        self.scribe = SqliteScribe(db_path)
        self.nucleus = nucleus
        self.embed_provider = embed_provider
        self.window_size = window_size
        self.reference_candidate_limit = max(0, int(reference_candidate_limit))

        # Sliding buffer: list of ingested HyperHunks (most recent last)
        self._buffer: List[Any] = []
        self._reference_index: Dict[str, List[Any]] = defaultdict(list)

        # All Nucleus evaluations (for Phase 2 training export)
        self._training_pairs: List[Dict] = []

        log.info(
            "GraphAssembler ready — db=%s window=%d reference_candidate_limit=%d",
            db_path,
            window_size,
            self.reference_candidate_limit,
        )

    # ── Public API ─────────────────────────────────────────────────────────

    def ingest(self, hunks: Iterable[Any]) -> int:
        """Ingest a stream of HyperHunks.

        Returns the total number of hunks processed.
        """
        count = 0
        for hunk in hunks:
            self._ingest_one(hunk)
            count += 1
        log.info("Ingested %d hunks", count)
        return count

    def ingest_one(self, hunk: Any) -> None:
        """Ingest a single HyperHunk.  Public alias for _ingest_one."""
        self._ingest_one(hunk)

    def export_training_pairs(self) -> List[Dict]:
        """Return all accumulated Nucleus evaluations for Phase 2 FFN training.

        Each dict has keys:
            source_occ_id, target_occ_id,
            connection_strength, routing_profile,
            interaction_type, interaction_vector, above_threshold
        """
        return list(self._training_pairs)

    def stats(self) -> Dict[str, int]:
        """Return Cold Artifact row counts + training pair count."""
        counts = self.scribe.stats()
        counts["training_pairs"] = len(self._training_pairs)
        return counts

    def close(self) -> None:
        """Flush all pending writes and close the database."""
        self.scribe.close()
        log.info("GraphAssembler closed — %d training pairs accumulated",
                 len(self._training_pairs))

    def __enter__(self) -> "GraphAssembler":
        return self

    def __exit__(self, *_: object) -> None:
        self.close()

    # ── Ingest internals ───────────────────────────────────────────────────

    def _ingest_one(self, hunk: Any) -> None:
        # Step 1: Embed if provider is available
        if self.embed_provider is not None:
            self._embed(hunk)

        # Step 2: Upsert into Cold Artifact
        self.scribe.upsert_hunk(hunk)

        # Step 3: Write inherent structural relations (pull, precedes only)
        self._write_structural_relations(hunk)

        # Step 4: Nucleus evaluation against local + targeted long-range candidates
        for prev_hunk in self._candidate_hunks_for(hunk):
            self._evaluate_pair(prev_hunk, hunk)

        # Step 5: Advance sliding window
        self._buffer.append(hunk)
        if len(self._buffer) > self.window_size:
            self._buffer.pop(0)
        self._index_hunk(hunk)

    def _embed(self, hunk: Any) -> None:
        """Embed a hunk's content and set hunk.embedding."""
        try:
            result = self.embed_provider.embed([hunk.content])
            if result.vectors:
                hunk.embedding = result.vectors[0]
        except Exception as exc:
            log.warning("Embedding failed for occ=%s: %s", hunk.occurrence_id, exc)

    def _write_structural_relations(self, hunk: Any) -> None:
        """Write pull and precedes edges derived from the hunk's DAG pointers.

        Works from either the Emitter's HyperHunk extension (which has a
        ``relations`` property) or the bare base HyperHunk (which exposes
        DAG pointers directly as fields).  Only occurrence_id targets are
        written (pull, precedes).  scope_member_of / section_of / references
        target non-occurrence-id strings and are skipped for Phase 1.
        """
        # Prefer the full relations property if available (Emitter HyperHunk)
        rels_attr = getattr(hunk, "relations", None)
        if rels_attr is not None:
            for rel in rels_attr:
                op = rel["op"]
                if op not in ("pull", "precedes"):
                    continue
                target_occ_id = rel["target"]
                if not target_occ_id:
                    continue
                self.scribe.write_relation(
                    source_occ_id=hunk.occurrence_id,
                    op=op,
                    target_occ_id=target_occ_id,
                    weight=rel["weight"],
                    routing_profile=_STRUCTURAL_ROUTING,
                    interaction_mode="structural_bridge",
                    interaction_vector=_STRUCTURAL_VECTOR,
                )
            return

        # Fallback: derive structural edges from bare HyperHunk DAG pointers
        if getattr(hunk, "parent_occurrence_id", None):
            self.scribe.write_relation(
                source_occ_id=hunk.occurrence_id,
                op="pull",
                target_occ_id=hunk.parent_occurrence_id,
                weight=1.0,
                routing_profile=_STRUCTURAL_ROUTING,
                interaction_mode="structural_bridge",
                interaction_vector=_STRUCTURAL_VECTOR,
            )
        if getattr(hunk, "prev_sibling_occurrence_id", None):
            self.scribe.write_relation(
                source_occ_id=hunk.occurrence_id,
                op="precedes",
                target_occ_id=hunk.prev_sibling_occurrence_id,
                weight=0.8,
                routing_profile=_STRUCTURAL_ROUTING,
                interaction_mode="structural_bridge",
                interaction_vector=_STRUCTURAL_VECTOR,
            )

    def _evaluate_pair(self, a: Any, b: Any) -> None:
        """Run Nucleus on a pair and write the edge if above threshold."""
        result = self.nucleus.evaluate(a, b)

        # Accumulate for Phase 2 training regardless of threshold
        self._training_pairs.append({
            "source_occ_id":    a.occurrence_id,
            "target_occ_id":    b.occurrence_id,
            "connection_strength": result.connection_strength,
            "routing_profile":  result.routing_profile,
            "interaction_type": result.interaction_type,
            "interaction_vector": result.interaction_vector,
            "above_threshold":  result.above_threshold,
        })

        if not result.above_threshold:
            return

        op = _INTERACTION_TO_OP.get(result.interaction_type, "pull")
        self.scribe.write_relation(
            source_occ_id=a.occurrence_id,
            op=op,
            target_occ_id=b.occurrence_id,
            weight=result.connection_strength,
            routing_profile=result.routing_profile,
            interaction_mode=result.interaction_type,
            interaction_vector=result.interaction_vector,
        )

    def _candidate_hunks_for(self, hunk: Any) -> List[Any]:
        candidates: List[Any] = list(self._buffer)
        if self.reference_candidate_limit <= 0:
            return candidates

        seen = {candidate.occurrence_id for candidate in candidates}
        token_order: List[str] = []
        for token in self._reference_candidate_tokens(hunk):
            if token and token not in token_order:
                token_order.append(token)

        targeted: List[Any] = []
        for token in token_order:
            for candidate in reversed(self._reference_index.get(token, [])):
                if candidate.occurrence_id in seen:
                    continue
                seen.add(candidate.occurrence_id)
                targeted.append(candidate)
                if len(targeted) >= self.reference_candidate_limit:
                    break
            if len(targeted) >= self.reference_candidate_limit:
                break

        candidates.extend(reversed(targeted))
        return candidates

    def _index_hunk(self, hunk: Any) -> None:
        for token in self._reference_candidate_tokens(hunk):
            if token:
                self._reference_index[token].append(hunk)

    def _reference_candidate_tokens(self, hunk: Any) -> List[str]:
        tokens: List[str] = []

        for ref in getattr(hunk, "normalized_cross_refs", []) or []:
            token = str(ref).strip().lower()
            if token:
                tokens.append(token)

        origin_text = str(getattr(hunk, "origin_id", "")).lower().replace("\\", "/")
        if origin_text:
            tail = origin_text.rsplit("/", 1)[-1]
            if tail:
                stem = Path(tail).stem.strip().lower()
                if stem:
                    tokens.append(stem)

        for part in str(getattr(hunk, "structural_path", "")).lower().split("/"):
            cleaned = part.strip().lower()
            if cleaned.startswith("h") and "_" in cleaned:
                slug = cleaned.split("_", 1)[1].strip("_")
                if slug:
                    tokens.append(slug)

        for heading in getattr(hunk, "heading_trail", []) or []:
            heading_slug = "".join(
                ch if ch.isalnum() else "_"
                for ch in str(heading).strip().lower()
            ).strip("_")
            if heading_slug:
                tokens.append(heading_slug)

        deduped: List[str] = []
        seen = set()
        for token in tokens:
            if token and token not in seen:
                seen.add(token)
                deduped.append(token)
        return deduped
