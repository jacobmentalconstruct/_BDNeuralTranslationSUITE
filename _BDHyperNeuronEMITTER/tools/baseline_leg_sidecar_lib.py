"""Sidecar retrieval shelves for baseline-leg comparison work.

This module is kept outside the live app path on purpose:
- it does not modify runtime bag/query behavior
- it reuses retrieval/bag helpers as read-only dependencies
- it normalizes shelf output so FTS, ANN, and bag legs can be compared honestly
"""

from __future__ import annotations

import json
import sqlite3
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable

if __package__ in {None, ""}:
    sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from core.engine.inference.bag_view import build_bag
from core.engine.inference.provider import (
    EmbeddingProviderSpec,
    create_embed_provider,
    load_embedding_provider_spec,
)
from core.engine.inference.retrieval import ann_search, fts_search


DEFAULT_QUERY_SHELF = [
    "lexical analysis",
    "encoding declarations",
    "yield expressions",
    "operator precedence",
    "assignment expressions",
    "lambda expressions",
    "function definitions",
    "import statements",
    "module imports",
    "resolution of names",
    "name lookup",
    "eval input",
    "interactive input",
    "repl input",
    "function calls",
    "decorators",
]

DEFAULT_SENTENCE_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


def _normalize_whitespace(text: str) -> str:
    return " ".join(str(text or "").split())


def _snippet(text: str, *, limit: int = 180) -> str:
    normalized = _normalize_whitespace(text)
    return normalized[:limit]


def _is_human_facing_kind(node_kind: str) -> bool:
    return node_kind in {
        "md_heading",
        "rst_section",
        "rst_title",
        "md_list_item",
        "md_paragraph",
    }


def _load_rows(conn: sqlite3.Connection, occurrence_ids: Iterable[str]) -> dict[str, dict[str, Any]]:
    ids = list(dict.fromkeys(str(occ_id) for occ_id in occurrence_ids if str(occ_id).strip()))
    if not ids:
        return {}

    placeholders = ",".join("?" * len(ids))
    rows = conn.execute(
        f"""
        SELECT o.occurrence_id, o.origin_id, o.structural_path,
               c.hunk_id, c.node_kind, c.content
        FROM occurrence_nodes o
        JOIN content_nodes c ON c.hunk_id = o.hunk_id
        WHERE o.occurrence_id IN ({placeholders})
        """,
        ids,
    ).fetchall()

    payload: dict[str, dict[str, Any]] = {}
    for row in rows:
        content = str(row[5] or "")
        payload[str(row[0])] = {
            "occurrence_id": str(row[0]),
            "origin_id": str(row[1] or ""),
            "structural_path": str(row[2] or ""),
            "hunk_id": str(row[3] or ""),
            "node_kind": str(row[4] or ""),
            "content": content,
            "content_snippet": _snippet(content),
        }
    return payload


def _group_items(items: list[dict[str, Any]], group_by: str) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for item in items:
        key = str(item.get(group_by, "") or "") or "ungrouped"
        grouped[key].append(item)

    groups: list[dict[str, Any]] = []
    for key, group_items in grouped.items():
        max_score = max(float(item.get("score", 0.0)) for item in group_items)
        groups.append(
            {
                "group_key": key,
                "item_count": len(group_items),
                "max_score": round(max_score, 6),
                "occurrence_ids": [item["occurrence_id"] for item in group_items],
            }
        )
    groups.sort(key=lambda group: (-group["max_score"], -group["item_count"], group["group_key"]))
    return groups


def _baseline_summary(
    query_text: str,
    items: list[dict[str, Any]],
    groups: list[dict[str, Any]],
    *,
    score_kind: str,
    group_by: str,
) -> dict[str, Any]:
    origin_counts = Counter(Path(str(item.get("origin_id", "") or "")).name for item in items)
    kind_counts = Counter(str(item.get("node_kind", "") or "") for item in items)
    top_origins = ", ".join(f"{name} ({count})" for name, count in origin_counts.most_common(3)) or "none"
    top_kinds = ", ".join(f"{name} ({count})" for name, count in kind_counts.most_common(3)) or "none"
    return {
        "item_count": len(items),
        "group_count": len(groups),
        "group_by": group_by,
        "summary": (
            f'{len(items)} {score_kind}-ranked evidence items surfaced for "{query_text}" '
            f"across {len(groups)} groups. Top sources: {top_origins}. "
            f"Top node kinds: {top_kinds}."
        ),
    }


def _resolve_provider_spec(
    db_path: Path,
    *,
    provider: str | None = None,
    sentence_model: str | None = None,
) -> EmbeddingProviderSpec:
    base = load_embedding_provider_spec(db_path)
    if provider is None or provider == "auto":
        return base
    if provider == "sentence-transformers":
        return EmbeddingProviderSpec(
            provider="sentence-transformers",
            model_name=sentence_model or base.model_name or DEFAULT_SENTENCE_MODEL,
            artifacts_dir=base.artifacts_dir,
        )
    if provider == "deterministic":
        return EmbeddingProviderSpec(
            provider="deterministic",
            artifacts_dir=base.artifacts_dir or str(db_path.parent),
        )
    if provider == "none":
        return EmbeddingProviderSpec(provider="none")
    return EmbeddingProviderSpec(
        provider=provider,
        model_name=sentence_model or base.model_name,
        artifacts_dir=base.artifacts_dir,
    )


def build_sidecar_shelf(
    *,
    query_text: str,
    db_path: str | Path,
    mode: str,
    top_k: int = 8,
    group_by: str = "origin_id",
    pull_occurrence_ids: list[str] | None = None,
    include_full_text: bool = False,
    ann_provider: str | None = None,
    sentence_model: str | None = None,
) -> dict[str, Any]:
    db_path = Path(db_path)
    pull_targets = set(pull_occurrence_ids or [])

    if mode == "bag":
        bag = build_bag(
            query_text=query_text,
            db_path=db_path,
            top_k=top_k,
            hop_limit=1,
            decay=0.9,
            group_by=group_by,
            include_full_text=include_full_text,
            pull_occurrence_ids=list(pull_targets) if pull_targets else None,
        )
        return {
            "query": bag["query"],
            "mode": "bag",
            "db_path": bag["db_path"],
            "provider": {"provider": "bag-control"},
            "summary": bag["bag_summary"],
            "groups": bag["groups"],
            "items": bag["items"],
            "pullback": bag["pullback"],
            "retrieval_leg": "Current bag control path (fused anchors + subgraph + Hot Engine + bag shaping).",
        }

    conn = sqlite3.connect(str(db_path))
    try:
        if mode == "fts":
            hits = fts_search(conn, query_text, top_k=top_k)
            score_kind = "bm25"
            provider_payload = {"provider": "fts"}
            retrieval_leg = "FTS-only lexical retrieval over content nodes."
        elif mode == "ann":
            provider_spec = _resolve_provider_spec(
                db_path,
                provider=ann_provider,
                sentence_model=sentence_model,
            )
            provider = create_embed_provider(provider_spec)
            if provider is None:
                return {
                    "query": query_text,
                    "mode": "ann",
                    "db_path": str(db_path.resolve()),
                    "provider": provider_spec.to_dict(),
                    "summary": {
                        "item_count": 0,
                        "group_count": 0,
                        "group_by": group_by,
                        "summary": "No embedding provider available for ANN shelf.",
                    },
                    "groups": [],
                    "items": [],
                    "pullback": {"selected_occurrence_ids": [], "items": []},
                    "retrieval_leg": "ANN-only vector retrieval over occurrence vectors.",
                    "error": "no embedding provider configured",
                }
            result = provider.embed_texts([query_text])
            if not result.vectors or not result.vectors[0]:
                return {
                    "query": query_text,
                    "mode": "ann",
                    "db_path": str(db_path.resolve()),
                    "provider": provider_spec.to_dict(),
                    "summary": {
                        "item_count": 0,
                        "group_count": 0,
                        "group_by": group_by,
                        "summary": "ANN shelf could not build a query vector.",
                    },
                    "groups": [],
                    "items": [],
                    "pullback": {"selected_occurrence_ids": [], "items": []},
                    "retrieval_leg": "ANN-only vector retrieval over occurrence vectors.",
                    "error": "empty query vector",
                }
            hits = ann_search(conn, result.vectors[0], top_k=top_k)
            score_kind = "cosine"
            provider_payload = provider_spec.to_dict()
            retrieval_leg = "ANN-only vector retrieval over occurrence vectors."
        else:
            raise ValueError(f"Unsupported mode: {mode}")

        rows = _load_rows(conn, [hit.occurrence_id for hit in hits])
        items: list[dict[str, Any]] = []
        for hit in hits:
            row = rows.get(hit.occurrence_id, {})
            item = {
                "occurrence_id": hit.occurrence_id,
                "origin_id": row.get("origin_id", hit.origin_id),
                "structural_path": row.get("structural_path", ""),
                "node_kind": row.get("node_kind", hit.node_kind),
                "content_snippet": row.get("content_snippet", hit.content_snippet),
                "score": round(float(hit.score), 6),
                "score_kind": score_kind,
            }
            if include_full_text:
                item["content"] = row.get("content", "")
            items.append(item)

        groups = _group_items(items, group_by)

        pullback_items: list[dict[str, Any]] = []
        for occurrence_id in pull_targets:
            row = rows.get(occurrence_id) or _load_rows(conn, [occurrence_id]).get(occurrence_id)
            if row is None:
                continue
            pullback_items.append(
                {
                    "occurrence_id": occurrence_id,
                    "origin_id": row.get("origin_id", ""),
                    "structural_path": row.get("structural_path", ""),
                    "node_kind": row.get("node_kind", ""),
                    "pullback_text": row.get("content", ""),
                }
            )

        return {
            "query": query_text,
            "mode": mode,
            "db_path": str(db_path.resolve()),
            "provider": provider_payload,
            "summary": _baseline_summary(
                query_text,
                items,
                groups,
                score_kind=score_kind,
                group_by=group_by,
            ),
            "groups": groups,
            "items": items,
            "pullback": {
                "selected_occurrence_ids": [item["occurrence_id"] for item in pullback_items],
                "items": pullback_items,
            },
            "retrieval_leg": retrieval_leg,
        }
    finally:
        conn.close()


def render_shelf_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Baseline-Leg Shelf",
        "",
        f"- Query: `{payload['query']}`",
        f"- Mode: `{payload['mode']}`",
        f"- DB: `{payload['db_path']}`",
        f"- Retrieval leg: {payload['retrieval_leg']}",
        f"- Provider: `{payload['provider'].get('provider', '')}`",
    ]
    model_name = payload["provider"].get("model_name", "")
    if model_name:
        lines.append(f"- Model: `{model_name}`")
    lines.extend(
        [
            f"- Summary: {payload['summary']['summary']}",
            "",
            "| Rank | Origin | Kind | Score | Snippet |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for index, item in enumerate(payload.get("items", []), start=1):
        score = item.get("rank_score", item.get("score", ""))
        origin_name = Path(str(item.get("origin_id", "") or "")).name
        lines.append(
            f"| `{index}` | `{origin_name}` | `{item.get('node_kind', '')}` | "
            f"`{score if score != '' else 'n/a'}` | {item.get('content_snippet', '')} |"
        )
    if payload.get("pullback", {}).get("items"):
        lines.extend(["", "## Pullback", ""])
        for item in payload["pullback"]["items"]:
            lines.extend(
                [
                    f"### `{item['occurrence_id']}`",
                    "",
                    f"- Origin: `{item['origin_id']}`",
                    f"- Structural path: `{item['structural_path']}`",
                    "",
                    "```text",
                    item["pullback_text"],
                    "```",
                    "",
                ]
            )
    return "\n".join(lines).rstrip() + "\n"


def _top_item(shelf: dict[str, Any]) -> dict[str, Any]:
    return (shelf.get("items") or [{}])[0]


def _same_origin(left: dict[str, Any], right: dict[str, Any]) -> bool:
    return bool(left.get("origin_id")) and left.get("origin_id") == right.get("origin_id")


def _difference_read(legs: dict[str, dict[str, Any]], query_count: int) -> list[str]:
    lines: list[str] = []
    bag = legs.get("bag")
    st_ann = legs.get("ann_sentence")
    det_ann = legs.get("ann_deterministic")
    fts = legs.get("fts")
    if fts:
        lines.append(
            f"- FTS-only preserves exact lexical anchors well, but it only matches the bag top on `{fts['summary']['same_top_count_vs_bag']}/{query_count}` queries."
        )
    if st_ann:
        lines.append(
            f"- Sentence-transformers ANN is the closest 'normal vector' leg here, matching the bag top on `{st_ann['summary']['same_top_count_vs_bag']}/{query_count}` queries."
        )
    if det_ann and st_ann:
        det_same = int(det_ann["summary"]["same_top_count_vs_bag"])
        st_same = int(st_ann["summary"]["same_top_count_vs_bag"])
        if det_same < st_same:
            lines.append(
                f"- Deterministic ANN diverges more from the bag than sentence-transformers ANN (`{det_same}` vs `{st_same}` same-top hits), which suggests a shifted or specialized field rather than a conventional semantic neighborhood map."
            )
        elif det_same > st_same:
            lines.append(
                f"- Deterministic ANN aligns with the bag more than sentence-transformers ANN (`{det_same}` vs `{st_same}` same-top hits), which suggests a useful nonstandard field rather than obvious misalignment."
            )
        else:
            lines.append(
                f"- Deterministic ANN and sentence-transformers ANN currently tie on same-top overlap (`{det_same}/{query_count}`), so the field difference is still ambiguous."
            )
    if bag:
        lines.append(
            f"- The bag's added value is anchor stability and readable evidence shaping; it lands a human-facing top item on `{bag['summary']['human_facing_top_count']}/{query_count}` queries in this run."
        )
    return lines


def compare_leg_specs(
    *,
    leg_specs: list[dict[str, Any]],
    query_shelf: list[str] | None = None,
    top_k: int = 8,
) -> dict[str, Any]:
    shelf = list(query_shelf or DEFAULT_QUERY_SHELF)
    leg_results: dict[str, dict[str, Any]] = {}
    rows: list[dict[str, Any]] = []

    for spec in leg_specs:
        leg_results[spec["label"]] = {
            "label": spec["label"],
            "mode": spec["mode"],
            "db_path": str(Path(spec["db"]).resolve()),
            "provider": spec.get("ann_provider", spec["mode"]),
        }

    for query in shelf:
        row = {"query": query, "legs": {}}
        bag_top: dict[str, Any] = {}
        raw_tops: dict[str, dict[str, Any]] = {}
        for spec in leg_specs:
            shelf_payload = build_sidecar_shelf(
                query_text=query,
                db_path=spec["db"],
                mode=spec["mode"],
                top_k=top_k,
                group_by="origin_id",
                ann_provider=spec.get("ann_provider"),
                sentence_model=spec.get("sentence_model"),
            )
            raw_tops[spec["label"]] = _top_item(shelf_payload)
            if spec["label"] == "bag":
                bag_top = raw_tops[spec["label"]]

        for spec in leg_specs:
            top_item = raw_tops[spec["label"]]
            row["legs"][spec["label"]] = {
                "occurrence_id": top_item.get("occurrence_id"),
                "origin_id": top_item.get("origin_id"),
                "node_kind": top_item.get("node_kind"),
                "content_snippet": top_item.get("content_snippet"),
                "same_top_as_bag": bool(bag_top.get("occurrence_id"))
                and top_item.get("occurrence_id") == bag_top.get("occurrence_id"),
                "same_origin_as_bag": _same_origin(top_item, bag_top),
            }
        rows.append(row)

    for label, payload in leg_results.items():
        tops = [row["legs"][label] for row in rows]
        payload["summary"] = {
            "query_count": len(shelf),
            "human_facing_top_count": sum(
                int(_is_human_facing_kind(str(item.get("node_kind", "")))) for item in tops
            ),
            "same_top_count_vs_bag": sum(int(item["same_top_as_bag"]) for item in tops),
            "same_origin_count_vs_bag": sum(int(item["same_origin_as_bag"]) for item in tops),
        }

    return {
        "query_shelf": shelf,
        "top_k": top_k,
        "legs": leg_results,
        "rows": rows,
        "difference_read": _difference_read(leg_results, len(shelf)),
        "branch_note": (
            "Branch-local diagnostic artifact only. This compare does not alter the live bag path "
            "and should not be treated as promotive truth without explicit review."
        ),
    }


def render_compare_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Baseline-Leg Compare",
        "",
        f"- Query shelf size: `{len(payload['query_shelf'])}`",
        f"- Top-k: `{payload['top_k']}`",
        f"- Branch note: {payload['branch_note']}",
        "",
        "## Leg Summary",
        "",
        "| Leg | DB | Human-facing tops | Same top vs bag | Same origin vs bag |",
        "| --- | --- | --- | --- | --- |",
    ]
    for label, leg in payload["legs"].items():
        lines.append(
            f"| `{label}` | `{Path(leg['db_path']).name}` | "
            f"`{leg['summary']['human_facing_top_count']}/{leg['summary']['query_count']}` | "
            f"`{leg['summary']['same_top_count_vs_bag']}/{leg['summary']['query_count']}` | "
            f"`{leg['summary']['same_origin_count_vs_bag']}/{leg['summary']['query_count']}` |"
        )
    lines.extend(["", "## Difference Read", ""])
    lines.extend(payload["difference_read"])
    lines.extend(
        [
            "",
            "## Top-Item Compare",
            "",
            "| Query | FTS | ANN (ST) | ANN (Det) | Bag |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for row in payload["rows"]:
        def _cell(label: str) -> str:
            item = row["legs"].get(label, {})
            origin_name = Path(str(item.get("origin_id", "") or "")).name
            return f"`{origin_name}` `{item.get('node_kind', '')}` :: {item.get('content_snippet', '')}"

        lines.append(
            f"| `{row['query']}` | {_cell('fts')} | {_cell('ann_sentence')} | {_cell('ann_deterministic')} | {_cell('bag')} |"
        )
    return "\n".join(lines).rstrip() + "\n"


def write_json(path: str | Path, payload: Any) -> Path:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return output_path


def write_markdown(path: str | Path, content: str) -> Path:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content, encoding="utf-8")
    return output_path
