import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


REPO_ROOT = Path(__file__).resolve().parents[2]
TOOLS_DIR = REPO_ROOT / "_BDHyperNeuronEMITTER" / "tools"
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))

from english_triplet_training_loop import (  # noqa: E402
    SentenceRegistry,
    REQUIRED_EXAMPLE_TYPES,
    run,
    validate_bundle_rows,
)


def _row(example_type: str, text: str, anchor_text: str = "") -> dict:
    return {
        "seed_word": "time",
        "bundle_id": "time-001",
        "generator_model": "demo-model",
        "generation_pass": 1,
        "example_type": example_type,
        "text": text,
        "anchor_text": anchor_text,
        "notes": "",
        "accepted": True,
        "rejection_reason": "",
        "created_at_utc": "2026-04-02T00:00:00+00:00",
    }


class EnglishTripletTrainingLoopTests(unittest.TestCase):
    def test_validate_bundle_rejects_missing_required_types(self):
        bundle = [
            _row("anchor", "Time keeps the station open at dawn."),
            _row("semantic_match", "The station opens early in the morning.", "Time keeps the station open at dawn."),
        ]

        result = validate_bundle_rows(bundle)

        self.assertFalse(result.ok)
        self.assertIn("missing_example_types", result.reason)

    def test_validate_bundle_rejects_duplicate_anchor_and_semantic_match(self):
        anchor = "Time keeps the station open at dawn."
        bundle = [
            _row("anchor", anchor),
            _row("semantic_match", anchor, anchor),
            _row("structural_match", "Time keeps the station open to doubt.", anchor),
            _row("grammatical_nonsense", "Time folds the station into a polite thunder.", anchor),
            _row("syntactic_shift", "At dawn, time keeps the station open.", anchor),
        ]

        result = validate_bundle_rows(bundle)

        self.assertFalse(result.ok)
        self.assertIn("semantic_match_identical_to_anchor", result.reason)

    def test_registry_rejects_exact_duplicate_and_near_duplicate(self):
        with tempfile.TemporaryDirectory() as tmp:
            registry = SentenceRegistry(Path(tmp) / "registry.sqlite3")
            try:
                registry.record_accepted_rows(
                    [
                        _row("anchor", "Time keeps the station open at dawn."),
                    ]
                )

                exact = registry.check_candidate(
                    text="Time keeps the station open at dawn.",
                    seed_word="time",
                    example_type="anchor",
                    local_texts=[],
                )
                near = registry.check_candidate(
                    text="Time keeps the station open at dawn!",
                    seed_word="time",
                    example_type="anchor",
                    local_texts=[],
                )
            finally:
                registry.close()

        self.assertFalse(exact.ok)
        self.assertEqual(exact.reason, "registry_exact_duplicate")
        self.assertFalse(near.ok)
        self.assertIn("duplicate", near.reason)

    def test_run_writes_outputs_and_uses_runtime_selected_model(self):
        fake_responses = {
            ("time", "anchor"): "Time keeps the room quiet after dusk.",
            ("time", "semantic_match"): "The room stays calm once evening arrives.",
            ("time", "structural_match"): "Time keeps the room quiet for trouble.",
            ("time", "grammatical_nonsense"): "Time politely folds the room under a blue ladder.",
            ("time", "syntactic_shift"): "After dusk, time keeps the room quiet.",
        }

        def _fake_generate(*, base_url, model, seed_word, example_type, anchor_text, timeout_seconds):
            self.assertEqual(model, "tiny-local:latest")
            return fake_responses[(seed_word, example_type)]

        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            word_list = tmp_path / "words.txt"
            word_list.write_text("time\n", encoding="utf-8")

            with patch(
                "english_triplet_training_loop._available_ollama_models",
                return_value=["tiny-local:latest", "other-model:latest"],
            ), patch(
                "english_triplet_training_loop._generate_example_text",
                side_effect=_fake_generate,
            ):
                result = run(
                    {
                        "model": "tiny-local:latest",
                        "word_list_path": str(word_list),
                        "output_dir": str(tmp_path / "out"),
                        "registry_db": str(tmp_path / "out" / "registry.sqlite3"),
                        "target_count_per_word": 1,
                        "max_attempts_per_type": 2,
                        "generation_pass": 3,
                    }
                )
                payload = result["result"]
                self.assertEqual(payload["model"], "tiny-local:latest")
                self.assertEqual(payload["accepted_bundle_count"], 1)
                self.assertEqual(payload["accepted_example_count"], len(REQUIRED_EXAMPLE_TYPES))
                self.assertTrue(Path(payload["accepted_examples_path"]).is_file())
                self.assertTrue(Path(payload["rejected_attempts_path"]).is_file())
                self.assertTrue(Path(payload["summary_json_path"]).is_file())
                self.assertTrue(Path(payload["summary_markdown_path"]).is_file())

                rows = [
                    json.loads(line)
                    for line in Path(payload["accepted_examples_path"]).read_text(encoding="utf-8").splitlines()
                    if line.strip()
                ]
                self.assertEqual({row["example_type"] for row in rows}, set(REQUIRED_EXAMPLE_TYPES))
                self.assertTrue(all(row["generator_model"] == "tiny-local:latest" for row in rows))


if __name__ == "__main__":
    unittest.main()
