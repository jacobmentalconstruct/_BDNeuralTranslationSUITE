"""Tiny Tk sidecar viewer for baseline-leg shelves.

Mainline-proven workflow in this tranche:
- human-driven shared-state viewing
- shared session JSON + event log parity
- visible provenance for the last completed action

Experimental follow-up seam:
- agent-driven pending-action execution
- intentionally disabled by default until reliability is proven
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path
from typing import Any

if __package__ in {None, ""}:
    sys.path.append(str(Path(__file__).resolve().parent))

from baseline_leg_session import CONTROL_MODES, RUN_QUERY_ACTION
from baseline_leg_sidecar_lib import build_sidecar_shelf, write_json


def _safe_load_json(path: Path) -> dict[str, Any] | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def _append_event(path: Path | None, event_type: str, payload: dict[str, Any]) -> None:
    if path is None:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    record = {
        "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "event": event_type,
        "payload": payload,
    }
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record) + "\n")


def _write_session(path: Path | None, payload: dict[str, Any]) -> None:
    if path is None:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def _item_button_label(item: dict[str, Any], index: int) -> str:
    origin_name = Path(str(item.get("origin_id", "") or "")).name
    kind = str(item.get("node_kind", "") or "")
    score = item.get("rank_score", item.get("score", ""))
    snippet = str(item.get("content_snippet", "") or "")
    snippet = snippet[:90] + ("..." if len(snippet) > 90 else "")
    return f"{index}. [{origin_name}] {kind} | {score} | {snippet}"


def _detail_text(item: dict[str, Any]) -> str:
    lines = [
        f"occurrence_id: {item.get('occurrence_id', '')}",
        f"origin_id: {item.get('origin_id', '')}",
        f"structural_path: {item.get('structural_path', '')}",
        f"node_kind: {item.get('node_kind', '')}",
    ]
    if "rank_score" in item:
        lines.append(f"rank_score: {item.get('rank_score')}")
    if "score" in item:
        lines.append(f"score: {item.get('score')}")
    if "activation" in item:
        lines.append(f"activation: {item.get('activation')}")
    if "rank_signals" in item:
        lines.append("rank_signals:")
        lines.append(json.dumps(item.get("rank_signals", {}), indent=2))
    lines.extend(
        [
            "",
            "snippet:",
            str(item.get("content_snippet", "") or ""),
            "",
            "content:",
            str(item.get("content", "") or ""),
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Open a tiny Tk sidecar baseline-leg viewer.")
    parser.add_argument("--db", required=True, help="Path to cold_anatomy DB.")
    parser.add_argument("--mode", choices=["fts", "ann", "bag"], default="bag", help="Retrieval leg to inspect.")
    parser.add_argument(
        "--ann-provider",
        choices=["auto", "deterministic", "sentence-transformers", "none"],
        default="auto",
        help="Provider override for ANN mode.",
    )
    parser.add_argument(
        "--sentence-model",
        default="sentence-transformers/all-MiniLM-L6-v2",
        help="Sentence-transformers model name when ANN provider is sentence-transformers.",
    )
    parser.add_argument("--query", default="lambda expressions", help="Initial query text.")
    parser.add_argument("--top-k", type=int, default=8, help="Maximum number of shelf items to show.")
    parser.add_argument(
        "--save-dir",
        default="",
        help="Optional directory to save the latest viewer payload JSON after each run.",
    )
    parser.add_argument(
        "--session-file",
        default="",
        help="Optional shared viewer state JSON path. Viewer reads and writes this state.",
    )
    parser.add_argument(
        "--event-log",
        default="",
        help="Optional JSONL event log path for viewer actions and state changes.",
    )
    parser.add_argument(
        "--enable-panel-actions",
        action="store_true",
        help="Enable experimental agent-driven pending-action execution through the visible panel path.",
    )
    args = parser.parse_args()

    import tkinter as tk
    from tkinter import ttk

    root = tk.Tk()
    root.title("Baseline-Leg Viewer")
    root.geometry("1380x860")

    query_var = tk.StringVar(value=args.query)
    mode_var = tk.StringVar(value=args.mode)
    provider_var = tk.StringVar(value=args.ann_provider)
    db_var = tk.StringVar(value=str(Path(args.db).resolve()))
    control_mode_var = tk.StringVar(value="shared-visible")
    last_action_var = tk.StringVar(value="last action: none")
    status_var = tk.StringVar(value="ready")
    session_path = Path(args.session_file) if args.session_file else None
    event_log_path = Path(args.event_log) if args.event_log else None

    payload_holder: dict[str, Any] = {"payload": None}
    item_lookup: dict[str, dict[str, Any]] = {}
    selected_occurrence_id = {"value": ""}
    last_session_mtime = {"value": 0.0}
    last_processed_action_id = {"value": ""}

    frame = ttk.Frame(root, padding=10)
    frame.pack(fill="both", expand=True)

    controls = ttk.LabelFrame(frame, text="Query", padding=8)
    controls.pack(fill="x", expand=False)

    ttk.Label(controls, text="DB").grid(row=0, column=0, sticky="w")
    db_entry = ttk.Entry(controls, textvariable=db_var, width=120)
    db_entry.grid(row=0, column=1, columnspan=5, sticky="ew", padx=(8, 0))

    ttk.Label(controls, text="Control").grid(row=0, column=6, sticky="w", padx=(12, 0))
    control_box = ttk.Combobox(
        controls,
        textvariable=control_mode_var,
        state="readonly",
        values=CONTROL_MODES,
        width=16,
    )
    control_box.grid(row=0, column=7, sticky="w", padx=(8, 0))

    ttk.Label(controls, text="Query").grid(row=1, column=0, sticky="w", pady=(8, 0))
    query_entry = ttk.Entry(controls, textvariable=query_var, width=80)
    query_entry.grid(row=1, column=1, columnspan=2, sticky="ew", padx=(8, 0), pady=(8, 0))

    ttk.Label(controls, text="Mode").grid(row=1, column=3, sticky="w", padx=(12, 0), pady=(8, 0))
    mode_box = ttk.Combobox(controls, textvariable=mode_var, state="readonly", values=("fts", "ann", "bag"), width=12)
    mode_box.grid(row=1, column=4, sticky="w", padx=(8, 0), pady=(8, 0))

    ttk.Label(controls, text="ANN Provider").grid(row=1, column=5, sticky="w", padx=(12, 0), pady=(8, 0))
    provider_box = ttk.Combobox(
        controls,
        textvariable=provider_var,
        state="readonly",
        values=("auto", "deterministic", "sentence-transformers", "none"),
        width=18,
    )
    provider_box.grid(row=1, column=6, sticky="w", padx=(8, 0), pady=(8, 0))

    controls.columnconfigure(1, weight=1)
    controls.columnconfigure(2, weight=1)

    response_frame = ttk.LabelFrame(frame, text="Response", padding=8)
    response_frame.pack(fill="x", expand=False, pady=(10, 10))
    response_text = tk.Text(response_frame, wrap="word", height=8)
    response_text.pack(fill="both", expand=True)

    body = ttk.Panedwindow(frame, orient="horizontal")
    body.pack(fill="both", expand=True)

    shelf_frame = ttk.LabelFrame(body, text="Shelf Items", padding=8)
    detail_frame = ttk.LabelFrame(body, text="Item Content", padding=8)
    body.add(shelf_frame, weight=1)
    body.add(detail_frame, weight=2)

    shelf_canvas = tk.Canvas(shelf_frame, highlightthickness=0)
    shelf_scroll = ttk.Scrollbar(shelf_frame, orient="vertical", command=shelf_canvas.yview)
    shelf_inner = ttk.Frame(shelf_canvas)
    shelf_inner.bind(
        "<Configure>",
        lambda event: shelf_canvas.configure(scrollregion=shelf_canvas.bbox("all")),
    )
    shelf_canvas.create_window((0, 0), window=shelf_inner, anchor="nw")
    shelf_canvas.configure(yscrollcommand=shelf_scroll.set)
    shelf_canvas.pack(side="left", fill="both", expand=True)
    shelf_scroll.pack(side="right", fill="y")

    detail_text = tk.Text(detail_frame, wrap="word")
    detail_text.pack(fill="both", expand=True)

    meta_bar = ttk.Frame(frame)
    meta_bar.pack(fill="x", expand=False, pady=(8, 0))
    status_bar = ttk.Label(meta_bar, textvariable=status_var)
    status_bar.pack(side="left", anchor="w")
    last_action_label = ttk.Label(meta_bar, textvariable=last_action_var)
    last_action_label.pack(side="right", anchor="e")

    def _set_last_action(source: str, kind: str) -> None:
        last_action_var.set(f"last action: {source} / {kind}")

    def _show_item(item: dict[str, Any]) -> None:
        selected_occurrence_id["value"] = str(item.get("occurrence_id", "") or "")
        detail_text.delete("1.0", "end")
        detail_text.insert("end", _detail_text(item))
        _write_session_state()
        _append_event(
            event_log_path,
            "select_item",
            {
                "query": query_var.get().strip(),
                "mode": mode_var.get(),
                "ann_provider": provider_var.get(),
                "occurrence_id": selected_occurrence_id["value"],
            },
        )

    def _refresh_shelf(items: list[dict[str, Any]]) -> None:
        for child in shelf_inner.winfo_children():
            child.destroy()
        item_lookup.clear()
        for index, item in enumerate(items, start=1):
            key = str(item.get("occurrence_id", f"item-{index}"))
            item_lookup[key] = item
            button = ttk.Button(
                shelf_inner,
                text=_item_button_label(item, index),
                command=lambda item_key=key: _show_item(item_lookup[item_key]),
            )
            button.pack(fill="x", expand=True, pady=3)

    def _render_response(payload: dict[str, Any]) -> None:
        response_text.delete("1.0", "end")
        summary = payload.get("summary", {})
        lines = [
            f"query: {payload.get('query', '')}",
            f"mode: {payload.get('mode', '')}",
            f"provider: {payload.get('provider', {}).get('provider', '')}",
            f"retrieval_leg: {payload.get('retrieval_leg', '')}",
            "",
            f"summary: {summary.get('summary', '')}",
            f"item_count: {summary.get('item_count', 0)}",
            f"group_count: {summary.get('group_count', 0)}",
        ]
        if payload.get("error"):
            lines.extend(["", f"error: {payload['error']}"])
        response_text.insert("end", "\n".join(lines))

    def _save_payload(payload: dict[str, Any]) -> None:
        if not args.save_dir:
            return
        save_dir = Path(args.save_dir)
        save_dir.mkdir(parents=True, exist_ok=True)
        stem = f"viewer_{payload.get('mode', 'unknown')}_{query_var.get().strip().replace(' ', '_') or 'query'}"
        write_json(save_dir / f"{stem}.json", payload)

    def _session_payload() -> dict[str, Any]:
        return {
            "db": db_var.get().strip(),
            "query": query_var.get().strip(),
            "mode": mode_var.get(),
            "ann_provider": provider_var.get(),
            "control_mode": control_mode_var.get(),
            "sentence_model": args.sentence_model,
            "top_k": args.top_k,
            "selected_occurrence_id": selected_occurrence_id["value"],
            "last_action": {
                "label": last_action_var.get(),
            },
            "pending_action": None,
            "payload": payload_holder.get("payload"),
        }

    def _write_session_state() -> None:
        session_payload = _session_payload()
        _write_session(session_path, session_payload)
        if session_path is not None:
            try:
                last_session_mtime["value"] = session_path.stat().st_mtime
            except OSError:
                pass

    def _apply_session_state(session_payload: dict[str, Any]) -> None:
        db_value = str(session_payload.get("db", "") or "")
        query_value = str(session_payload.get("query", "") or "")
        mode_value = str(session_payload.get("mode", "") or mode_var.get())
        provider_value = str(session_payload.get("ann_provider", "") or provider_var.get())
        control_mode = str(session_payload.get("control_mode", "") or control_mode_var.get())
        query_var.set(query_value or query_var.get())
        db_var.set(db_value or db_var.get())
        if mode_value in {"fts", "ann", "bag"}:
            mode_var.set(mode_value)
        if provider_value in {"auto", "deterministic", "sentence-transformers", "none"}:
            provider_var.set(provider_value)
        if control_mode in CONTROL_MODES:
            control_mode_var.set(control_mode)
        last_action = session_payload.get("last_action")
        if isinstance(last_action, dict) and last_action.get("label"):
            last_action_var.set(str(last_action.get("label")))

        payload = session_payload.get("payload")
        if isinstance(payload, dict) and payload:
            payload_holder["payload"] = payload
            _render_response(payload)
            _refresh_shelf(payload.get("items", []))
            selected_id = str(session_payload.get("selected_occurrence_id", "") or "")
            selected_occurrence_id["value"] = selected_id
            if selected_id and selected_id in item_lookup:
                _show_item(item_lookup[selected_id])
            elif payload.get("items"):
                selected_occurrence_id["value"] = str(payload["items"][0].get("occurrence_id", "") or "")
                detail_text.delete("1.0", "end")
                detail_text.insert("end", _detail_text(payload["items"][0]))
            else:
                detail_text.delete("1.0", "end")

    def _run_query(*, source: str = "human", action_kind: str = RUN_QUERY_ACTION) -> None:
        status_var.set("running...")
        root.update_idletasks()
        try:
            payload = build_sidecar_shelf(
                query_text=query_var.get().strip(),
                db_path=db_var.get().strip(),
                mode=mode_var.get(),
                top_k=args.top_k,
                group_by="origin_id",
                include_full_text=True,
                ann_provider=provider_var.get(),
                sentence_model=args.sentence_model,
            )
            payload_holder["payload"] = payload
            _set_last_action(source, action_kind)
            _render_response(payload)
            _refresh_shelf(payload.get("items", []))
            if payload.get("items"):
                selected_occurrence_id["value"] = str(payload["items"][0].get("occurrence_id", "") or "")
                detail_text.delete("1.0", "end")
                detail_text.insert("end", _detail_text(payload["items"][0]))
            else:
                selected_occurrence_id["value"] = ""
                detail_text.delete("1.0", "end")
            _save_payload(payload)
            _write_session_state()
            _append_event(
                event_log_path,
                "run_query",
                {
                    "query": payload.get("query", ""),
                    "mode": payload.get("mode", ""),
                    "ann_provider": payload.get("provider", {}).get("provider", ""),
                    "source": source,
                    "item_count": len(payload.get("items", [])),
                },
            )
            status_var.set(
                f"loaded {len(payload.get('items', []))} items for '{payload.get('query', '')}' in {payload.get('mode', '')} mode ({source})"
            )
        except Exception as exc:  # pragma: no cover - viewer error path
            response_text.delete("1.0", "end")
            response_text.insert("end", f"viewer error:\n{exc}")
            detail_text.delete("1.0", "end")
            for child in shelf_inner.winfo_children():
                child.destroy()
            _append_event(
                event_log_path,
                "viewer_error",
                {
                    "query": query_var.get().strip(),
                    "mode": mode_var.get(),
                    "source": source,
                    "error": str(exc),
                },
            )
            status_var.set("error")

    def _handle_pending_action(session_payload: dict[str, Any]) -> bool:
        if not args.enable_panel_actions:
            return False
        pending = session_payload.get("pending_action")
        if not isinstance(pending, dict):
            return False
        action_id = str(pending.get("action_id", "") or "")
        if not action_id or action_id == last_processed_action_id["value"]:
            return False
        if str(pending.get("kind", "")) != RUN_QUERY_ACTION:
            return False
        if control_mode_var.get() != "shared-visible":
            status_var.set("pending agent action ignored in background mode")
            last_processed_action_id["value"] = action_id
            return True

        db_value = str(pending.get("db", "") or db_var.get())
        query_value = str(pending.get("query", "") or query_var.get())
        mode_value = str(pending.get("mode", "") or mode_var.get())
        provider_value = str(pending.get("ann_provider", "") or provider_var.get())
        if db_value:
            db_var.set(db_value)
        if query_value:
            query_var.set(query_value)
        if mode_value in {"fts", "ann", "bag"}:
            mode_var.set(mode_value)
        if provider_value in {"auto", "deterministic", "sentence-transformers", "none"}:
            provider_var.set(provider_value)

        last_processed_action_id["value"] = action_id
        _run_query(source=str(pending.get("source", "agent") or "agent"), action_kind=RUN_QUERY_ACTION)
        return True

    def _poll_session() -> None:
        if session_path is not None and session_path.exists():
            try:
                current_mtime = session_path.stat().st_mtime
            except OSError:
                current_mtime = 0.0
            if current_mtime and current_mtime > last_session_mtime["value"]:
                session_payload = _safe_load_json(session_path)
                if isinstance(session_payload, dict):
                    last_session_mtime["value"] = current_mtime
                    if not _handle_pending_action(session_payload):
                        _apply_session_state(session_payload)
                        status_var.set("synced from shared session")
        root.after(800, _poll_session)

    run_button = ttk.Button(controls, text="Run Query", command=lambda: _run_query(source="human"))
    run_button.grid(row=1, column=7, sticky="e", padx=(12, 0), pady=(8, 0))

    query_entry.bind("<Return>", lambda event: _run_query(source="human"))
    mode_box.bind("<<ComboboxSelected>>", lambda event: _run_query(source="human"))
    provider_box.bind("<<ComboboxSelected>>", lambda event: _run_query(source="human"))
    control_box.bind("<<ComboboxSelected>>", lambda event: _write_session_state())

    if session_path is not None and session_path.exists():
        existing = _safe_load_json(session_path)
        if isinstance(existing, dict):
            _apply_session_state(existing)
            try:
                last_session_mtime["value"] = session_path.stat().st_mtime
            except OSError:
                pass
            if not isinstance(existing.get("payload"), dict) or not existing.get("payload"):
                _run_query(source="human")
        else:
            _run_query(source="human")
    else:
        _run_query(source="human")
    _poll_session()
    root.mainloop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
