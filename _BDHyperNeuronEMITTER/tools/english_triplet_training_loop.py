"""
FILE: english_triplet_training_loop.py
ROLE: Builder-side controlled English corpus generator for later scorer/FFN work.
WHAT IT DOES: Generates high-contrast English example bundles from a seed word list,
applies deterministic bundle validation plus SQLite/FTS uniqueness filtering, and
writes accepted/rejected NDJSON artifacts.
HOW TO USE:
  - Metadata: python _BDHyperNeuronEMITTER/tools/english_triplet_training_loop.py metadata
  - Run: python _BDHyperNeuronEMITTER/tools/english_triplet_training_loop.py run --input-file _BDHyperNeuronEMITTER/tools/examples/english_triplet_training_loop_core_v1.json
INPUT OBJECT:
  - model: required Ollama model name to use for generation
  - word_list_path: optional path to a seed word list; defaults to the bundled core-English list
  - output_dir: optional output directory; defaults under _docs/_analysis/english_triplet_training_loop
  - registry_db: optional uniqueness-registry SQLite path; defaults inside output_dir
  - target_count_per_word: optional bundles per seed word, default 1
  - max_attempts_per_type: optional retry cap per example type, default 6
  - timeout_seconds: optional per-generation timeout, default 45
  - base_url: optional Ollama base URL, default http://localhost:11434
  - generation_pass: optional integer tag for later corpus evolution, default 1
  - word_limit: optional cap on how many seed words to process
"""

from __future__ import annotations

import json
import re
import sqlite3
import sys
import urllib.error
import urllib.request
import argparse
from dataclasses import dataclass
from datetime import datetime, timezone
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any

FILE_METADATA = {
    "tool_name": "english_triplet_training_loop",
    "version": "1.0.0",
    "entrypoint": "_BDHyperNeuronEMITTER/tools/english_triplet_training_loop.py",
    "category": "corpus",
    "summary": "Generate controlled English triplet bundles with deterministic validation and SQLite/FTS uniqueness filtering.",
    "mcp_name": "english_triplet_training_loop",
    "input_schema": {
        "type": "object",
        "properties": {
            "model": {"type": "string", "description": "Ollama model name to use for generation."},
            "word_list_path": {"type": "string", "description": "Optional seed word list path."},
            "output_dir": {"type": "string", "description": "Optional output directory."},
            "registry_db": {"type": "string", "description": "Optional SQLite uniqueness registry path."},
            "target_count_per_word": {"type": "integer", "default": 1},
            "max_attempts_per_type": {"type": "integer", "default": 6},
            "timeout_seconds": {"type": "integer", "default": 45},
            "base_url": {"type": "string", "default": "http://localhost:11434"},
            "generation_pass": {"type": "integer", "default": 1},
            "word_limit": {"type": "integer"},
        },
        "required": ["model"],
        "additionalProperties": False,
    },
}

TOOL_ROOT = Path(__file__).resolve().parent
REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUTPUT_ROOT = REPO_ROOT / "_docs" / "_analysis" / "english_triplet_training_loop"
DEFAULT_CORE_WORDS = [
    "time",
    "day",
    "night",
    "person",
    "child",
    "friend",
    "family",
    "house",
    "room",
    "door",
    "window",
    "water",
    "food",
    "light",
    "sound",
    "story",
    "question",
    "answer",
    "idea",
    "place",
    "way",
    "part",
    "point",
    "group",
    "number",
    "work",
    "rest",
    "move",
    "hold",
    "bring",
    "leave",
    "make",
    "build",
    "find",
    "lose",
    "think",
    "know",
    "learn",
    "teach",
    "open",
    "close",
    "good",
    "quiet",
    "heavy",
    "small",
    "before",
    "after",
    "between",
    "under",
    "through",
]
REQUIRED_EXAMPLE_TYPES = (
    "anchor",
    "semantic_match",
    "structural_match",
    "grammatical_nonsense",
    "syntactic_shift",
)
EXAMPLE_TYPE_ORDER = {name: idx for idx, name in enumerate(REQUIRED_EXAMPLE_TYPES)}
STOPWORDS = {
    "a",
    "an",
    "the",
    "and",
    "or",
    "of",
    "to",
    "in",
    "on",
    "for",
    "with",
    "at",
    "by",
    "from",
    "up",
    "down",
    "into",
    "over",
    "under",
    "before",
    "after",
    "between",
    "through",
    "during",
    "without",
    "about",
    "against",
    "is",
    "are",
    "was",
    "were",
    "be",
    "been",
    "being",
    "do",
    "does",
    "did",
    "have",
    "has",
    "had",
}


@dataclass
class CandidateCheck:
    ok: bool
    reason: str = ""


def emit_json(payload: Any) -> None:
    print(json.dumps(payload, indent=2, sort_keys=False))


def tool_result(tool_name: str, arguments: dict[str, Any], result: Any, *, status: str = "ok") -> dict[str, Any]:
    return {
        "status": status,
        "tool": tool_name,
        "input": arguments,
        "result": result,
    }


def tool_error(tool_name: str, arguments: dict[str, Any], message: str) -> dict[str, Any]:
    return tool_result(tool_name, arguments, {"message": message}, status="error")


def load_input(input_json: str | None, input_file: str | None) -> dict[str, Any]:
    if input_json and input_file:
        raise ValueError("Use either --input-json or --input-file, not both.")
    if input_json:
        payload = json.loads(input_json)
    elif input_file:
        payload = json.loads(Path(input_file).read_text(encoding="utf-8"))
    else:
        payload = {}
    if not isinstance(payload, dict):
        raise ValueError("Tool input must be a JSON object.")
    return payload


def standard_main(metadata: dict[str, Any], run_func, argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=metadata["summary"])
    subparsers = parser.add_subparsers(dest="command")
    subparsers.add_parser("metadata", help="Print tool metadata as JSON.")
    run_parser = subparsers.add_parser("run", help="Run the tool with a JSON object input.")
    run_parser.add_argument("--input-json", help="Inline JSON object input.")
    run_parser.add_argument("--input-file", help="Path to a JSON file containing the tool input object.")
    args = parser.parse_args(argv)

    if args.command == "metadata":
        emit_json(metadata)
        return 0

    if args.command == "run":
        try:
            payload = load_input(args.input_json, args.input_file)
            emit_json(run_func(payload))
            return 0
        except Exception as exc:
            emit_json(tool_error(metadata["tool_name"], {}, str(exc)))
            return 1

    parser.print_help()
    return 2


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _slug(value: str) -> str:
    collapsed = re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")
    return collapsed or "item"


def _ensure_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def _write_ndjson(path: Path, rows: list[dict[str, Any]]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=True) + "\n")
    return path


def _write_json(path: Path, payload: Any) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=True), encoding="utf-8")
    return path


def _write_text(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def _display_path(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(REPO_ROOT.resolve()))
    except ValueError:
        return str(path.resolve())


def _load_word_list(path: Path, limit: int | None) -> list[str]:
    words: list[str] = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        stripped = raw.strip()
        if not stripped or stripped.startswith("#"):
            continue
        words.append(stripped)
    if limit is not None:
        return words[:limit]
    return words


def _default_word_list(limit: int | None) -> list[str]:
    if limit is not None:
        return DEFAULT_CORE_WORDS[:limit]
    return list(DEFAULT_CORE_WORDS)


def _normalize_text(text: str) -> str:
    lowered = text.lower()
    lowered = re.sub(r"\s+", " ", lowered)
    lowered = re.sub(r"[^a-z0-9\s]", "", lowered)
    lowered = re.sub(r"\s+", " ", lowered).strip()
    return lowered


def _tokenize(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", text.lower())


def _content_tokens(text: str) -> set[str]:
    return {token for token in _tokenize(text) if token not in STOPWORDS}


def _token_overlap(a: str, b: str) -> int:
    return len(_content_tokens(a) & _content_tokens(b))


def _similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, _normalize_text(a), _normalize_text(b)).ratio()


def _contains_seed(text: str, seed_word: str) -> bool:
    seed_tokens = _tokenize(seed_word)
    text_tokens = _tokenize(text)
    if not seed_tokens:
        return False
    if len(seed_tokens) == 1:
        return seed_tokens[0] in text_tokens
    normalized = _normalize_text(text)
    return _normalize_text(seed_word) in normalized


def _sentence_like(text: str) -> CandidateCheck:
    stripped = text.strip()
    if not stripped:
        return CandidateCheck(False, "empty_text")
    if len(stripped) < 12:
        return CandidateCheck(False, "too_short")
    if len(_tokenize(stripped)) < 4:
        return CandidateCheck(False, "too_few_tokens")
    if not re.search(r"[A-Za-z]", stripped):
        return CandidateCheck(False, "no_alpha_content")
    return CandidateCheck(True)


def _extract_first_sentence(text: str) -> str:
    cleaned = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL | re.IGNORECASE).strip()
    cleaned = cleaned.replace("```", " ").strip()
    lines = [line.strip(" -*\t") for line in cleaned.splitlines() if line.strip()]
    if not lines:
        return ""
    first = lines[0].strip().strip("\"' ")
    match = re.search(r"(.+?[.!?])(?:\s|$)", first)
    if match:
        first = match.group(1).strip()
    return first.strip("\"' ")


def _candidate_query(text: str) -> str:
    tokens = [token for token in _tokenize(text) if len(token) > 2]
    unique_tokens: list[str] = []
    for token in tokens:
        if token not in unique_tokens:
            unique_tokens.append(token)
    if not unique_tokens:
        return ""
    return " OR ".join(unique_tokens[:6])


class SentenceRegistry:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(str(path))
        self.conn.row_factory = sqlite3.Row
        self._ensure_schema()

    def close(self) -> None:
        self.conn.close()

    def _ensure_schema(self) -> None:
        self.conn.executescript(
            """
            create table if not exists accepted_samples (
                sample_id integer primary key autoincrement,
                bundle_id text not null,
                seed_word text not null,
                example_type text not null,
                model_name text not null,
                text_value text not null,
                normalized_text text not null unique,
                created_at_utc text not null
            );

            create virtual table if not exists accepted_fts using fts5(
                sample_id unindexed,
                text_value,
                tokenize='unicode61'
            );

            create index if not exists idx_accepted_seed_type
            on accepted_samples(seed_word, example_type);
            """
        )
        self.conn.commit()

    def record_accepted_rows(self, rows: list[dict[str, Any]]) -> None:
        for row in rows:
            cursor = self.conn.execute(
                """
                insert into accepted_samples(
                    bundle_id, seed_word, example_type, model_name, text_value, normalized_text, created_at_utc
                ) values(?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    row["bundle_id"],
                    row["seed_word"],
                    row["example_type"],
                    row["generator_model"],
                    row["text"],
                    _normalize_text(row["text"]),
                    row["created_at_utc"],
                ),
            )
            sample_id = int(cursor.lastrowid)
            self.conn.execute(
                "insert into accepted_fts(rowid, sample_id, text_value) values(?, ?, ?)",
                (sample_id, sample_id, row["text"]),
            )
        self.conn.commit()

    def check_candidate(
        self,
        *,
        text: str,
        seed_word: str,
        example_type: str,
        local_texts: list[str],
    ) -> CandidateCheck:
        normalized = _normalize_text(text)
        if not normalized:
            return CandidateCheck(False, "empty_normalized_text")

        local_normalized = {_normalize_text(item) for item in local_texts}
        if normalized in local_normalized:
            return CandidateCheck(False, "same_run_duplicate")

        row = self.conn.execute(
            "select 1 from accepted_samples where normalized_text = ? limit 1",
            (normalized,),
        ).fetchone()
        if row is not None:
            return CandidateCheck(False, "registry_exact_duplicate")

        query = _candidate_query(text)
        if not query:
            return CandidateCheck(True)

        hits = self.conn.execute(
            """
            select s.seed_word, s.example_type, s.text_value
            from accepted_fts f
            join accepted_samples s on s.sample_id = f.sample_id
            where accepted_fts match ?
            limit 32
            """,
            (query,),
        ).fetchall()

        for hit in hits:
            existing_text = str(hit["text_value"])
            if normalized == _normalize_text(existing_text):
                return CandidateCheck(False, "registry_exact_duplicate")
            ratio = _similarity(text, existing_text)
            overlap = len(_content_tokens(text) & _content_tokens(existing_text))
            same_family = hit["seed_word"] == seed_word and hit["example_type"] == example_type
            if same_family and (ratio >= 0.92 or overlap >= 5):
                return CandidateCheck(False, "registry_near_duplicate_same_family")
            if ratio >= 0.97:
                return CandidateCheck(False, "registry_near_duplicate")

        return CandidateCheck(True)


def _available_ollama_models(base_url: str, timeout_seconds: int) -> list[str]:
    request = urllib.request.Request(f"{base_url.rstrip('/')}/api/tags", method="GET")
    with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
        payload = json.loads(response.read().decode("utf-8"))
    models = payload.get("models", [])
    names: list[str] = []
    for model in models:
        name = model.get("name")
        if isinstance(name, str) and name.strip():
            names.append(name.strip())
    return names


def _ollama_generate(*, base_url: str, model: str, prompt: str, timeout_seconds: int) -> str:
    body = json.dumps(
        {
            "model": model,
            "prompt": prompt,
            "stream": False,
        }
    ).encode("utf-8")
    request = urllib.request.Request(
        f"{base_url.rstrip('/')}/api/generate",
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
        payload = json.loads(response.read().decode("utf-8"))
    return str(payload.get("response", ""))


def _prompt_for_type(*, seed_word: str, example_type: str, anchor_text: str) -> str:
    if example_type == "anchor":
        return (
            "Write one short, ordinary English sentence using the seed word "
            f"'{seed_word}' in a clear everyday sense. Return only the sentence."
        )
    if example_type == "semantic_match":
        return (
            "Anchor sentence:\n"
            f"{anchor_text}\n\n"
            "Write one different short English sentence with a very similar meaning. "
            f"Avoid copying the anchor wording. You may omit the exact seed word '{seed_word}' if better wording exists. "
            "Return only the sentence."
        )
    if example_type == "structural_match":
        return (
            "Anchor sentence:\n"
            f"{anchor_text}\n\n"
            "Write one short English sentence that still uses the seed word "
            f"'{seed_word}' and shares some surface wording with the anchor, "
            "but clearly changes the meaning. Return only the sentence."
        )
    if example_type == "grammatical_nonsense":
        return (
            "Write one short grammatical English sentence using the seed word "
            f"'{seed_word}' that is semantically odd, implausible, or nonsensical. "
            "It should read like a sentence, but not like a sensible claim. Return only the sentence."
        )
    if example_type == "syntactic_shift":
        return (
            "Anchor sentence:\n"
            f"{anchor_text}\n\n"
            "Rewrite the anchor as one short English sentence with different word order or framing, "
            "while keeping the same core meaning. Return only the sentence."
        )
    raise ValueError(f"Unknown example_type: {example_type}")


def _generate_example_text(
    *,
    base_url: str,
    model: str,
    seed_word: str,
    example_type: str,
    anchor_text: str,
    timeout_seconds: int,
) -> str:
    prompt = _prompt_for_type(seed_word=seed_word, example_type=example_type, anchor_text=anchor_text)
    raw = _ollama_generate(base_url=base_url, model=model, prompt=prompt, timeout_seconds=timeout_seconds)
    return _extract_first_sentence(raw)


def validate_example(
    *,
    seed_word: str,
    example_type: str,
    text: str,
    anchor_text: str,
) -> CandidateCheck:
    basic = _sentence_like(text)
    if not basic.ok:
        return basic

    normalized = _normalize_text(text)
    normalized_anchor = _normalize_text(anchor_text)

    if example_type in {"anchor", "structural_match", "grammatical_nonsense"} and not _contains_seed(text, seed_word):
        return CandidateCheck(False, "missing_seed_word")

    if example_type != "anchor" and normalized == normalized_anchor:
        return CandidateCheck(False, "identical_to_anchor")

    if example_type == "structural_match" and _token_overlap(text, anchor_text) < 1:
        return CandidateCheck(False, "needs_surface_overlap")

    if example_type == "syntactic_shift" and _token_overlap(text, anchor_text) < 2:
        return CandidateCheck(False, "needs_anchor_overlap")

    if example_type == "grammatical_nonsense" and _similarity(text, anchor_text) >= 0.9:
        return CandidateCheck(False, "too_close_to_anchor")

    return CandidateCheck(True)


def validate_bundle_rows(rows: list[dict[str, Any]]) -> CandidateCheck:
    types_present = {row["example_type"] for row in rows}
    missing = [example_type for example_type in REQUIRED_EXAMPLE_TYPES if example_type not in types_present]
    if missing:
        return CandidateCheck(False, f"missing_example_types:{','.join(missing)}")

    anchor_text = next(row["text"] for row in rows if row["example_type"] == "anchor")
    for row in rows:
        if row["example_type"] == "anchor":
            continue
        if _normalize_text(row["text"]) == _normalize_text(anchor_text):
            return CandidateCheck(False, f"{row['example_type']}_identical_to_anchor")

    normalized_texts = [_normalize_text(row["text"]) for row in rows]
    if len(normalized_texts) != len(set(normalized_texts)):
        return CandidateCheck(False, "bundle_has_duplicate_text")

    structural = next(row["text"] for row in rows if row["example_type"] == "structural_match")
    if _token_overlap(structural, anchor_text) < 1:
        return CandidateCheck(False, "structural_match_lacks_surface_overlap")

    syntactic = next(row["text"] for row in rows if row["example_type"] == "syntactic_shift")
    if _token_overlap(syntactic, anchor_text) < 2:
        return CandidateCheck(False, "syntactic_shift_lacks_anchor_overlap")

    return CandidateCheck(True)


def _rejected_row(
    *,
    seed_word: str,
    bundle_id: str,
    model: str,
    generation_pass: int,
    example_type: str,
    text: str,
    anchor_text: str,
    rejection_reason: str,
    notes: str,
) -> dict[str, Any]:
    return {
        "seed_word": seed_word,
        "bundle_id": bundle_id,
        "generator_model": model,
        "generation_pass": generation_pass,
        "example_type": example_type,
        "text": text,
        "anchor_text": anchor_text,
        "notes": notes,
        "accepted": False,
        "rejection_reason": rejection_reason,
        "created_at_utc": _utc_now(),
    }


def _accepted_row(
    *,
    seed_word: str,
    bundle_id: str,
    model: str,
    generation_pass: int,
    example_type: str,
    text: str,
    anchor_text: str,
    notes: str,
) -> dict[str, Any]:
    return {
        "seed_word": seed_word,
        "bundle_id": bundle_id,
        "generator_model": model,
        "generation_pass": generation_pass,
        "example_type": example_type,
        "text": text,
        "anchor_text": anchor_text,
        "notes": notes,
        "accepted": True,
        "rejection_reason": "",
        "created_at_utc": _utc_now(),
    }


def _run_bundle(
    *,
    registry: SentenceRegistry,
    seed_word: str,
    bundle_id: str,
    model: str,
    base_url: str,
    timeout_seconds: int,
    max_attempts_per_type: int,
    generation_pass: int,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], str]:
    pending_rows: list[dict[str, Any]] = []
    rejected_rows: list[dict[str, Any]] = []
    local_texts: list[str] = []
    anchor_text = ""

    for example_type in REQUIRED_EXAMPLE_TYPES:
        accepted_row: dict[str, Any] | None = None
        for attempt_no in range(1, max_attempts_per_type + 1):
            try:
                text = _generate_example_text(
                    base_url=base_url,
                    model=model,
                    seed_word=seed_word,
                    example_type=example_type,
                    anchor_text=anchor_text,
                    timeout_seconds=timeout_seconds,
                )
            except urllib.error.URLError as exc:
                return [], rejected_rows, f"ollama_unreachable:{exc}"
            except TimeoutError:
                text = ""
                rejected_rows.append(
                    _rejected_row(
                        seed_word=seed_word,
                        bundle_id=bundle_id,
                        model=model,
                        generation_pass=generation_pass,
                        example_type=example_type,
                        text=text,
                        anchor_text=anchor_text,
                        rejection_reason="generation_timeout",
                        notes=f"attempt={attempt_no}",
                    )
                )
                continue

            validation = validate_example(
                seed_word=seed_word,
                example_type=example_type,
                text=text,
                anchor_text=anchor_text,
            )
            if not validation.ok:
                rejected_rows.append(
                    _rejected_row(
                        seed_word=seed_word,
                        bundle_id=bundle_id,
                        model=model,
                        generation_pass=generation_pass,
                        example_type=example_type,
                        text=text,
                        anchor_text=anchor_text,
                        rejection_reason=validation.reason,
                        notes=f"attempt={attempt_no}",
                    )
                )
                continue

            uniqueness = registry.check_candidate(
                text=text,
                seed_word=seed_word,
                example_type=example_type,
                local_texts=local_texts,
            )
            if not uniqueness.ok:
                rejected_rows.append(
                    _rejected_row(
                        seed_word=seed_word,
                        bundle_id=bundle_id,
                        model=model,
                        generation_pass=generation_pass,
                        example_type=example_type,
                        text=text,
                        anchor_text=anchor_text,
                        rejection_reason=uniqueness.reason,
                        notes=f"attempt={attempt_no}",
                    )
                )
                continue

            accepted_row = _accepted_row(
                seed_word=seed_word,
                bundle_id=bundle_id,
                model=model,
                generation_pass=generation_pass,
                example_type=example_type,
                text=text,
                anchor_text=anchor_text,
                notes=f"accepted_after_attempt={attempt_no}",
            )
            pending_rows.append(accepted_row)
            local_texts.append(text)
            if example_type == "anchor":
                anchor_text = text
            break

        if accepted_row is None:
            rejected_rows.append(
                _rejected_row(
                    seed_word=seed_word,
                    bundle_id=bundle_id,
                    model=model,
                    generation_pass=generation_pass,
                    example_type="bundle_validation",
                    text="",
                    anchor_text=anchor_text,
                    rejection_reason="incomplete_bundle",
                    notes=f"missing_type={example_type}",
                )
            )
            return [], rejected_rows, "incomplete_bundle"

    pending_rows.sort(key=lambda row: EXAMPLE_TYPE_ORDER[row["example_type"]])
    bundle_check = validate_bundle_rows(pending_rows)
    if not bundle_check.ok:
        rejected_rows.append(
            _rejected_row(
                seed_word=seed_word,
                bundle_id=bundle_id,
                model=model,
                generation_pass=generation_pass,
                example_type="bundle_validation",
                text="",
                anchor_text=anchor_text,
                rejection_reason=bundle_check.reason,
                notes="bundle_level_validation",
            )
        )
        return [], rejected_rows, bundle_check.reason

    registry.record_accepted_rows(pending_rows)
    return pending_rows, rejected_rows, ""


def _summary_markdown(summary: dict[str, Any]) -> str:
    lines = [
        "# English Triplet Training Loop Run",
        "",
        f"- model: `{summary['model']}`",
        f"- word list: `{summary.get('word_list_label', summary['word_list_path'])}`",
        f"- bundles accepted: `{summary['accepted_bundle_count']}`",
        f"- bundles rejected: `{summary['rejected_bundle_count']}`",
        f"- accepted example rows: `{summary['accepted_example_count']}`",
        f"- rejected attempts: `{summary['rejected_attempt_count']}`",
        f"- registry db: `{summary['registry_db']}`",
        "",
        "## Per-Type Counts",
        "",
    ]
    for example_type, count in summary["accepted_example_type_counts"].items():
        lines.append(f"- `{example_type}`: `{count}`")
    lines.extend(
        [
            "",
            "## Rejection Reasons",
            "",
        ]
    )
    if not summary["rejection_reason_counts"]:
        lines.append("- none")
    else:
        for reason, count in summary["rejection_reason_counts"].items():
            lines.append(f"- `{reason}`: `{count}`")
    return "\n".join(lines) + "\n"


def run(arguments: dict[str, Any]) -> dict[str, Any]:
    model = str(arguments["model"]).strip()
    if not model:
        raise ValueError("model is required")

    base_url = str(arguments.get("base_url", "http://localhost:11434")).strip() or "http://localhost:11434"
    timeout_seconds = int(arguments.get("timeout_seconds", 45))
    target_count_per_word = int(arguments.get("target_count_per_word", 1))
    max_attempts_per_type = int(arguments.get("max_attempts_per_type", 6))
    generation_pass = int(arguments.get("generation_pass", 1))
    word_limit = int(arguments["word_limit"]) if arguments.get("word_limit") is not None else None

    word_list_path_arg = arguments.get("word_list_path")
    if word_list_path_arg:
        word_list_path = Path(str(word_list_path_arg)).resolve()
        if not word_list_path.is_file():
            raise FileNotFoundError(f"word_list_path not found: {word_list_path}")
    else:
        word_list_path = None

    run_stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    output_dir = Path(arguments.get("output_dir") or (DEFAULT_OUTPUT_ROOT / run_stamp)).resolve()
    registry_db = Path(arguments.get("registry_db") or (output_dir / "uniqueness_registry.sqlite3")).resolve()
    _ensure_dir(output_dir)

    available_models = _available_ollama_models(base_url, timeout_seconds)
    if model not in available_models:
        raise ValueError(
            f"Requested model '{model}' not found in Ollama tags. Available models: {', '.join(available_models[:20])}"
        )

    seed_words = _load_word_list(word_list_path, word_limit) if word_list_path is not None else _default_word_list(word_limit)
    if not seed_words:
        raise ValueError("No seed words available for generation")

    accepted_rows: list[dict[str, Any]] = []
    rejected_rows: list[dict[str, Any]] = []
    accepted_bundle_count = 0
    rejected_bundle_count = 0

    registry = SentenceRegistry(registry_db)
    try:
        for seed_word in seed_words:
            for bundle_no in range(1, target_count_per_word + 1):
                bundle_id = f"{_slug(seed_word)}-{generation_pass:03d}-{bundle_no:03d}"
                bundle_rows, bundle_rejects, failure_reason = _run_bundle(
                    registry=registry,
                    seed_word=seed_word,
                    bundle_id=bundle_id,
                    model=model,
                    base_url=base_url,
                    timeout_seconds=timeout_seconds,
                    max_attempts_per_type=max_attempts_per_type,
                    generation_pass=generation_pass,
                )
                accepted_rows.extend(bundle_rows)
                rejected_rows.extend(bundle_rejects)
                if bundle_rows:
                    accepted_bundle_count += 1
                else:
                    rejected_bundle_count += 1
                    if failure_reason.startswith("ollama_unreachable"):
                        raise RuntimeError(failure_reason)
    finally:
        registry.close()

    accepted_type_counts = {example_type: 0 for example_type in REQUIRED_EXAMPLE_TYPES}
    for row in accepted_rows:
        accepted_type_counts[row["example_type"]] += 1

    rejection_reason_counts: dict[str, int] = {}
    for row in rejected_rows:
        reason = row["rejection_reason"] or "unknown"
        rejection_reason_counts[reason] = rejection_reason_counts.get(reason, 0) + 1

    accepted_path = _write_ndjson(output_dir / "accepted_examples.ndjson", accepted_rows)
    rejected_path = _write_ndjson(output_dir / "rejected_attempts.ndjson", rejected_rows)

    summary = {
        "model": model,
        "base_url": base_url,
        "word_list_path": str(word_list_path) if word_list_path is not None else "<built-in-core-english-v1>",
        "word_list_label": _display_path(word_list_path) if word_list_path is not None else "<built-in-core-english-v1>",
        "output_dir": str(output_dir),
        "registry_db": str(registry_db),
        "generation_pass": generation_pass,
        "seed_word_count": len(seed_words),
        "target_count_per_word": target_count_per_word,
        "accepted_bundle_count": accepted_bundle_count,
        "rejected_bundle_count": rejected_bundle_count,
        "accepted_example_count": len(accepted_rows),
        "rejected_attempt_count": len(rejected_rows),
        "accepted_example_type_counts": accepted_type_counts,
        "rejection_reason_counts": dict(sorted(rejection_reason_counts.items(), key=lambda item: (-item[1], item[0]))),
        "accepted_examples_path": str(accepted_path),
        "rejected_attempts_path": str(rejected_path),
        "available_models_sample": available_models[:20],
    }

    summary_json_path = _write_json(output_dir / "summary.json", summary)
    summary_md_path = _write_text(output_dir / "summary.md", _summary_markdown(summary))

    return tool_result(
        FILE_METADATA["tool_name"],
        arguments,
        {
            **summary,
            "summary_json_path": str(summary_json_path),
            "summary_markdown_path": str(summary_md_path),
        },
    )


if __name__ == "__main__":
    raise SystemExit(standard_main(FILE_METADATA, run))
