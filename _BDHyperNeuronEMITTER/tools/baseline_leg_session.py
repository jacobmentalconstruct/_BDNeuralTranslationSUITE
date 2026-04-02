"""Shared session helpers for the baseline-leg viewer."""

from __future__ import annotations

from copy import deepcopy
from typing import Any
from uuid import uuid4


CONTROL_MODES = ("shared-visible", "background")
RUN_QUERY_ACTION = "run_query"


def make_panel_action(
    *,
    db: str,
    query: str,
    mode: str,
    ann_provider: str,
    top_k: int,
    source: str = "agent",
    action_id: str | None = None,
) -> dict[str, Any]:
    """Create a shared-panel action payload."""
    return {
        "action_id": action_id or uuid4().hex,
        "kind": RUN_QUERY_ACTION,
        "source": source,
        "db": str(db),
        "query": str(query),
        "mode": str(mode),
        "ann_provider": str(ann_provider),
        "top_k": int(top_k),
    }


def merge_session_for_action(
    existing: dict[str, Any] | None,
    action: dict[str, Any],
    *,
    control_mode: str | None = None,
    sentence_model: str | None = None,
) -> dict[str, Any]:
    """Merge a pending action into an existing shared session document."""
    payload = deepcopy(existing) if isinstance(existing, dict) else {}
    payload["db"] = str(action.get("db", payload.get("db", "")) or "")
    payload["query"] = str(action.get("query", payload.get("query", "")) or "")
    payload["mode"] = str(action.get("mode", payload.get("mode", "bag")) or "bag")
    payload["ann_provider"] = str(
        action.get("ann_provider", payload.get("ann_provider", "auto")) or "auto"
    )
    payload["top_k"] = int(action.get("top_k", payload.get("top_k", 8)) or 8)
    payload["pending_action"] = deepcopy(action)
    payload["selected_occurrence_id"] = ""
    if control_mode:
        payload["control_mode"] = control_mode
    elif payload.get("control_mode") not in CONTROL_MODES:
        payload["control_mode"] = "shared-visible"
    if sentence_model:
        payload["sentence_model"] = sentence_model
    elif not payload.get("sentence_model"):
        payload["sentence_model"] = "sentence-transformers/all-MiniLM-L6-v2"
    payload.setdefault("last_action", {})
    return payload
