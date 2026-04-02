"""Write a pending action into a shared baseline-leg viewer session.

Experimental helper:
- useful for branch-local workflow exploration
- not part of the first mainline-proven shared-view workflow unless the viewer
  is explicitly launched with ``--enable-panel-actions``
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.append(str(Path(__file__).resolve().parent))

from baseline_leg_session import CONTROL_MODES, make_panel_action, merge_session_for_action


def _safe_load_json(path: Path) -> dict | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def main() -> int:
    parser = argparse.ArgumentParser(description="Queue a shared-panel action for baseline_leg_viewer.")
    parser.add_argument("--session-file", required=True, help="Shared viewer session JSON path.")
    parser.add_argument("--db", required=True, help="Path to cold_anatomy DB.")
    parser.add_argument("--query", required=True, help="Query text to run in the panel.")
    parser.add_argument("--mode", choices=["fts", "ann", "bag"], required=True, help="Panel retrieval mode.")
    parser.add_argument(
        "--ann-provider",
        choices=["auto", "deterministic", "sentence-transformers", "none"],
        default="auto",
        help="ANN provider to select in the panel.",
    )
    parser.add_argument("--top-k", type=int, default=8, help="Top-k size to set in the action payload.")
    parser.add_argument("--source", default="agent", help="Action source label (default: agent).")
    parser.add_argument(
        "--control-mode",
        choices=CONTROL_MODES,
        default="shared-visible",
        help="Viewer control mode to set in the shared session.",
    )
    parser.add_argument(
        "--sentence-model",
        default="sentence-transformers/all-MiniLM-L6-v2",
        help="Sentence model metadata to preserve in session.",
    )
    args = parser.parse_args()

    session_path = Path(args.session_file)
    existing = _safe_load_json(session_path) if session_path.exists() else None
    action = make_panel_action(
        db=args.db,
        query=args.query,
        mode=args.mode,
        ann_provider=args.ann_provider,
        top_k=args.top_k,
        source=args.source,
    )
    payload = merge_session_for_action(
        existing,
        action,
        control_mode=args.control_mode,
        sentence_model=args.sentence_model,
    )
    session_path.parent.mkdir(parents=True, exist_ok=True)
    session_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps({"action_id": action["action_id"], "session_file": str(session_path)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
