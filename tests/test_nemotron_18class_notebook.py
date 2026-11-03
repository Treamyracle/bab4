import ast
import json
import os
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
import zipfile

import nbformat as nbf

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.build_nemotron_18class_notebook import (
    DEFAULT_BUNDLE_PATH,
    DEFAULT_CELLS_DIR,
    DEFAULT_NEMOTRON_JSONL,
    DEFAULT_NOTEBOOK_PATH,
    build_colab_bundle,
    build_notebook,
    sha256_bytes,
)


class DummyEncoding(dict):
    """Minimal BatchEncoding-like mock supporting word_ids() for fast tokenizer testing."""

    def __init__(self, data: dict, word_ids_list: list[int | None]):
        super().__init__(data)
        self._word_ids = word_ids_list

    def word_ids(self):
        return list(self._word_ids)


class MockFastTokenizer:
    """Deterministic subword tokenizer mock for testing chunk_record & recombine_predictions."""

    is_fast = True
    unk_token = "[UNK]"

    def num_special_tokens_to_add(self, pair: bool = False) -> int:
        return 2

    def __call__(
        self,
        tokens: list[str],
        is_split_into_words: bool = True,
        add_special_tokens: bool = True,
        truncation: bool = False,
        return_attention_mask: bool = True,
    ) -> DummyEncoding:
        assert is_split_into_words
        input_ids = []
        word_ids = []
        if add_special_tokens:
            input_ids.append(101)
            word_ids.append(None)
        for w_idx, tok in enumerate(tokens):
            if not tok.strip():
                continue
            # Long words (>6 chars) split into 2 subwords to test multi-subword alignment
            n_sub = 2 if len(tok) > 6 and tok != self.unk_token else 1
            for s in range(n_sub):
                input_ids.append(200 + w_idx * 2 + s)
                word_ids.append(w_idx)
        if add_special_tokens:
            input_ids.append(102)
            word_ids.append(None)
        data = {"input_ids": input_ids}
        if return_attention_mask:
            data["attention_mask"] = [1] * len(input_ids)
        return DummyEncoding(data, word_ids)


class TestNemotron18ClassNotebook(unittest.TestCase):
    def test_01_bundle_integrity_and_determinism(self):
        self.assertTrue(DEFAULT_BUNDLE_PATH.is_file(), f"Missing bundle: {DEFAULT_BUNDLE_PATH}")
        with zipfile.ZipFile(DEFAULT_BUNDLE_PATH, "r") as zf:
            names = set(zf.namelist())
            expected_members = {
                "gold/train.txt",
                "gold/valid.txt",
                "gold/test.txt",
                "gold/labels-map.csv",
                "nemotron_18class/corrected.jsonl",
                "bundle_manifest.json",
            }
            self.assertEqual(names, expected_members)
            manifest = json.loads(zf.read("bundle_manifest.json").decode("utf-8"))
            for rel_path, expected_sha in manifest["sha256"].items():
                actual_sha = sha256_bytes(zf.read(rel_path))
                self.assertEqual(actual_sha, expected_sha, f"SHA-256 mismatch for {rel_path}")

            nemotron_records = [
                json.loads(line)
                for line in zf.read("nemotron_18class/corrected.jsonl").decode("utf-8").splitlines()
                if line.strip()
            ]
            self.assertEqual(len(nemotron_records), 17525)
            total_entities = sum(len(r.get("entities", [])) for r in nemotron_records)
            self.assertEqual(total_entities, 119680)
            for r in nemotron_records:
                txt = r["text"]
                for ent in r["entities"]:
                    self.assertNotIn(ent["type"], ("REG", "TTL"))
                    self.assertIn(ent["entity"], txt)

        # Verify deterministic rebuild produces identical SHA-256
        with tempfile.TemporaryDirectory() as tmpdir:
            rebuilt_path = Path(tmpdir) / "rebuilt_bundle.zip"
            rebuilt_manifest = build_colab_bundle(rebuilt_path, DEFAULT_NEMOTRON_JSONL)
            self.assertEqual(
                rebuilt_manifest["bundle_sha256"],
                sha256_bytes(DEFAULT_BUNDLE_PATH.read_bytes()),
            )

    def test_02_cells_syntax_and_notebook_validation(self):
        manifest_path = DEFAULT_CELLS_DIR / "cell_manifest.json"
        self.assertTrue(manifest_path.is_file())
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        self.assertEqual(manifest["training_seeds"], [42])
        self.assertEqual(manifest["entity_classes"], 18)
        self.assertEqual(manifest["bio_tags"], 37)
        self.assertEqual(len(manifest["cells"]), 10)

        for idx, spec in enumerate(manifest["cells"], start=1):
            self.assertEqual(spec["file"], f"cell{idx}.py")
            cell_path = DEFAULT_CELLS_DIR / spec["file"]
            self.assertTrue(cell_path.is_file())
            source = cell_path.read_text(encoding="utf-8").strip()
            if spec["cell_type"] == "markdown":
                doc = ast.get_docstring(ast.parse(source))
                self.assertIsNotNone(doc)
                self.assertIn("indobenchmark/indobert-large-p1", doc)
            else:
                compile(source, spec["file"], "exec")

        self.assertTrue(DEFAULT_NOTEBOOK_PATH.is_file())
        nb = nbf.read(DEFAULT_NOTEBOOK_PATH, as_version=4)
        nbf.validate(nb)
        self.assertEqual(len(nb.cells), 10)
        self.assertEqual(nb.cells[0].cell_type, "markdown")
        for c in nb.cells[1:]:
            self.assertEqual(c.cell_type, "code")

    def test_03_end_to_end_pipeline_cells_and_drive_sync(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_root = Path(tmpdir)
            local_work_dir = tmp_root / "local_workspace"
            drive_dir = tmp_root / "google_drive_mirror"

            old_local_env = os.environ.get("NEMOTRON_LOCAL_WORK_DIR")
            old_drive_env = os.environ.get("NEMOTRON_DRIVE_DIR")
            os.environ["NEMOTRON_LOCAL_WORK_DIR"] = str(local_work_dir)
            os.environ["NEMOTRON_DRIVE_DIR"] = str(drive_dir)

            try:
                ns = {"__name__": "__main__"}
                for cell_name in ("cell2.py", "cell3.py", "cell4.py", "cell5.py", "cell6.py"):
                    cell_code = (DEFAULT_CELLS_DIR / cell_name).read_text(encoding="utf-8")
                    exec(compile(cell_code, cell_name, "exec"), ns)

                # 1. Verify Hyperparameters & Seed = [42]
                cfg = ns["CONFIG"]
                self.assertEqual(ns["TRAINING_SEEDS"], [42])
                self.assertEqual(cfg["training_seeds"], [42])
                self.assertEqual(cfg["model_checkpoint"], "indobenchmark/indobert-large-p1")
                self.assertEqual(cfg["max_seq_length"], 256)
                self.assertEqual(cfg["train_batch_size"], 32)
                self.assertEqual(cfg["gradient_accumulation_steps"], 1)
                self.assertEqual(cfg["eval_batch_size"], 64)
                self.assertEqual(cfg["learning_rate"], 2e-5)
                self.assertEqual(cfg["weight_decay"], 0.01)
                self.assertEqual(cfg["warmup_ratio"], 0.10)
                self.assertEqual(cfg["lr_scheduler_type"], "linear")
                self.assertEqual(cfg["num_train_epochs"], 10)
                self.assertEqual(cfg["early_stopping_patience"], 2)
                self.assertEqual(cfg["metric_for_best_model"], "macro_f1")
                self.assertEqual(cfg["dropout"], 0.10)
                self.assertEqual(cfg["max_grad_norm"], 1.0)
                self.assertEqual(cfg["pad_to_multiple_of"], 8)
                self.assertEqual(cfg["optim"], "adamw_torch")
                self.assertEqual(len(cfg["labels"]), 37)

                # 2. Verify Automatic Google Drive Sync of Input Bundle in cell4.py
                drive_bundle = drive_dir / "nemotron_18class_colab_bundle.zip"
                self.assertTrue(drive_bundle.is_file(), "Bundle was not automatically synced to Google Drive!")
                self.assertEqual(
                    sha256_bytes(drive_bundle.read_bytes()),
                    sha256_bytes(DEFAULT_BUNDLE_PATH.read_bytes()),
                )

                # 3. Verify Partition Counts & Zero Leakage in cell5.py
                prepared = ns["PREPARED_DATA"]
                prep_manifest = ns["PREPARED_MANIFEST"]
                self.assertTrue(prep_manifest["leakage_check"]["passed"])
                self.assertEqual(prep_manifest["leakage_check"]["cross_partition_overlap_groups"], 0)
                self.assertEqual(len(prepared["gold"]["train"]), 12465)
                self.assertEqual(len(prepared["gold"]["validation"]), 2543)
                self.assertEqual(len(prepared["gold"]["test"]), 2423)
                self.assertEqual(prep_manifest["statistics"]["gold"]["test"]["E"], 8890)
                gold_train_digest = ns["stable_json_hash"]([
                    {"sentence_id": r["sentence_id"], "tokens": r["tokens"], "tags": r["tags"]}
                    for r in prepared["gold"]["train"]
                ])
                self.assertEqual(gold_train_digest[:12], "26d1055a4d59")
                self.assertEqual(len(prepared["nemotron_18class"]["train"]), 14896)
                self.assertEqual(len(prepared["nemotron_18class"]["validation"]), 2629)
                self.assertTrue((drive_dir / "tables" / "dataset_statistics.csv").is_file())
                self.assertTrue((drive_dir / "tables" / "per_class_distribution_corpus.csv").is_file())

                # 4. Verify Lossless Word-Aligned Chunking & Recombination Edge Cases in cell6.py
                chunk_record = ns["chunk_record"]
                recombine_predictions = ns["recombine_predictions"]
                span_metrics = ns["span_metrics"]
                labels = ns["LABELS"]
                label2id = ns["LABEL2ID"]
                mock_tok = MockFastTokenizer()

                # Edge case A: Long sentence with multi-token entity crossing chunk boundary + whitespace token
                tokens = ["Presiden", "Joko", "Widodo", "   "] + ["kata_panjang"] * 15
                tags = ["B-NOR", "B-PER", "I-PER", "O"] + ["O"] * 8 + ["B-ORG", "I-ORG"] + ["O"] * 5
                rec = {"sentence_id": "test-long-1", "tokens": tokens, "tags": tags}
                chunks_train = chunk_record(rec, mock_tok, labels, max_length=20, avoid_entity_boundaries=True)
                self.assertGreater(len(chunks_train), 1)
                # Ensure entity B-ORG I-ORG was not split across chunks when avoid_entity_boundaries=True
                for ch in chunks_train:
                    self.assertLessEqual(len(ch["inputs"]["input_ids"]), 20)
                    self.assertFalse(ch["start"] <= 12 < ch["end"] and ch["end"] == 13)

                # Recombine perfect predictions and verify 100% lossless roundtrip
                fake_pred_ids = []
                for ch in chunks_train:
                    seq_preds = [
                        (lbl if lbl != -100 else label2id["O"])
                        for lbl in ch["inputs"]["labels"]
                    ]
                    fake_pred_ids.append(seq_preds)
                recombined = recombine_predictions([rec], chunks_train, fake_pred_ids, labels)
                self.assertEqual(recombined[0], tags)
                perfect_score = span_metrics([tags], recombined, ns["ACTIVE_TYPES"])
                self.assertAlmostEqual(perfect_score["micro_f1"], 1.0)

                # 5. Simulate Evaluation & Execute cell10.py (Error Analysis, Figures, Zip & Drive Upload)
                test_subset = prepared["gold"]["test"][:30]
                gold_preds = [list(r["tags"]) for r in test_subset]
                # Introduce controlled errors in nemotron predictions (type confusion, boundary, spurious, missed)
                nem_preds = []
                for idx, r in enumerate(test_subset):
                    t_copy = list(r["tags"])
                    if idx == 0 and any(t.startswith("B-") for t in t_copy):
                        # Type confusion: change first entity to B-LOC/I-LOC
                        for ti, tv in enumerate(t_copy):
                            if tv.startswith("B-"):
                                t_copy[ti] = "B-LOC"
                            elif tv.startswith("I-"):
                                t_copy[ti] = "I-LOC"
                    elif idx == 1:
                        # Missed FN: set all to O
                        t_copy = ["O"] * len(t_copy)
                    elif idx == 2 and len(t_copy) >= 2:
                        # Spurious FP on O tokens
                        if t_copy[0] == "O":
                            t_copy[0] = "B-PRD"
                    nem_preds.append(t_copy)

                g_metrics = span_metrics([r["tags"] for r in test_subset], gold_preds, ns["ACTIVE_TYPES"])
                n_metrics = span_metrics([r["tags"] for r in test_subset], nem_preds, ns["ACTIVE_TYPES"])

                # Populate mock histories, predictions, and EVAL_BUNDLE for cell10.py
                for prefix in ("gold", "nemotron"):
                    hist_data = [
                        {"epoch": 1.0, "loss": 0.45},
                        {"epoch": 1.0, "eval_loss": 0.22, "eval_micro_f1": 0.80, "eval_macro_f1": 0.70},
                        {"epoch": 2.0, "loss": 0.18},
                        {"epoch": 2.0, "eval_loss": 0.19, "eval_micro_f1": 0.84, "eval_macro_f1": 0.75},
                    ]
                    (ns["HISTORIES_DIR"] / f"{prefix}_s42.json").write_text(
                        json.dumps(hist_data, indent=2), encoding="utf-8"
                    )
                    ns["write_csv_rows"](ns["HISTORIES_DIR"] / f"{prefix}_s42.csv", hist_data)

                ns["export_predictions"](
                    ns["PREDICTIONS_DIR"] / "gold_s42_test_predictions", test_subset, gold_preds
                )
                ns["export_predictions"](
                    ns["PREDICTIONS_DIR"] / "nemotron_s42_test_predictions", test_subset, nem_preds
                )

                per_class_rows = []
                for kind in ns["ACTIVE_TYPES"]:
                    gc_m = g_metrics["per_class"][kind]
                    nc_m = n_metrics["per_class"][kind]
                    per_class_rows.append({
                        "entity_class": kind,
                        "description": kind,
                        "support": gc_m["support"],
                        "gold_precision_pct": round(gc_m["precision"] * 100, 2),
                        "gold_recall_pct": round(gc_m["recall"] * 100, 2),
                        "gold_f1_pct": round(gc_m["f1"] * 100, 2),
                        "nemotron_18class_precision_pct": round(nc_m["precision"] * 100, 2),
                        "nemotron_18class_recall_pct": round(nc_m["recall"] * 100, 2),
                        "nemotron_18class_f1_pct": round(nc_m["f1"] * 100, 2),
                        "nemotron_old_bab4_f1_pct": 50.0,
                        "delta_new_vs_old_nemotron_f1_pct": round(nc_m["f1"] * 100 - 50.0, 2),
                        "delta_new_nemotron_vs_gold_f1_pct": round((nc_m["f1"] - gc_m["f1"]) * 100, 2),
                    })
                overall_rows = [
                    {"scenario_key": "gold", "seed": "42", "micro_f1_pct": round(g_metrics["micro_f1"] * 100, 2)},
                    {"scenario_key": "nemotron_18class", "seed": "42", "micro_f1_pct": round(n_metrics["micro_f1"] * 100, 2)},
                ]
                ns["write_csv_rows"](ns["TABLES_DIR"] / "overall_comparison.csv", overall_rows)
                ns["write_csv_rows"](ns["TABLES_DIR"] / "per_class_18_comparison.csv", per_class_rows)

                ns["PREPARED_DATA"]["gold"]["test"] = test_subset
                ns["GOLD_RUN_MANIFESTS"] = {42: {"run_id": "gold_s42", "status": "complete"}}
                ns["NEMOTRON_RUN_MANIFESTS"] = {42: {"run_id": "nemotron_18class_s42", "status": "complete"}}
                ns["EVAL_BUNDLE"] = {
                    "evaluation_results": {"gold": {42: g_metrics}, "nemotron_18class": {42: n_metrics}},
                    "predictions_by_run": {"gold": {42: gold_preds}, "nemotron_18class": {42: nem_preds}},
                    "overall_rows": overall_rows,
                    "per_class_rows": per_class_rows,
                    "delta_vs_old": {"micro_f1_pct_delta": 10.0},
                    "delta_vs_gold": {"micro_f1_pct_delta": -5.0},
                }

                cell10_code = (DEFAULT_CELLS_DIR / "cell10.py").read_text(encoding="utf-8")
                exec(compile(cell10_code, "cell10.py", "exec"), ns)

                results_zip = ns["RESULTS_ZIP_PATH"]
                self.assertTrue(results_zip.is_file())
                drive_results_zip = drive_dir / "nemotron_18class_experiment_results.zip"
                self.assertTrue(drive_results_zip.is_file(), "Results zip was not automatically uploaded to Drive!")
                self.assertEqual(
                    sha256_bytes(results_zip.read_bytes()),
                    sha256_bytes(drive_results_zip.read_bytes()),
                )

                with zipfile.ZipFile(results_zip, "r") as rzf:
                    znames = set(rzf.namelist())
                    for required_arc in (
                        "experiment_summary.json",
                        "tables/overall_comparison.csv",
                        "tables/per_class_18_comparison.csv",
                        "tables/dataset_statistics.csv",
                        "histories/gold_s42.csv",
                        "histories/nemotron_s42.csv",
                        "predictions/gold_s42_test_predictions.jsonl",
                        "predictions/nemotron_s42_test_predictions.jsonl",
                        "error_analysis/error_breakdown.json",
                        "figures/per_class_f1_comparison.png",
                        "figures/training_convergence_curves.png",
                        "figures/error_taxonomy_breakdown.png",
                        "results_manifest.json",
                    ):
                        self.assertIn(required_arc, znames, f"Missing {required_arc} in results zip!")

            finally:
                if old_local_env is None:
                    os.environ.pop("NEMOTRON_LOCAL_WORK_DIR", None)
                else:
                    os.environ["NEMOTRON_LOCAL_WORK_DIR"] = old_local_env
                if old_drive_env is None:
                    os.environ.pop("NEMOTRON_DRIVE_DIR", None)
                else:
                    os.environ["NEMOTRON_DRIVE_DIR"] = old_drive_env

    def test_04_cell4_github_download_auto_drive_upload(self):
        """Verify that when bundle is downloaded from GitHub URL, it is automatically uploaded to Google Drive."""
        import io
        import urllib.request
        from unittest.mock import patch

        bundle_bytes = DEFAULT_BUNDLE_PATH.read_bytes()

        class FakeHTTPResponse(io.BytesIO):
            def __enter__(self):
                return self

            def __exit__(self, *args):
                self.close()

        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_root = Path(tmpdir)
            local_work_dir = tmp_root / "work"
            drive_dir = tmp_root / "drive"
            old_cwd = Path.cwd()
            old_local_env = os.environ.get("NEMOTRON_LOCAL_WORK_DIR")
            old_drive_env = os.environ.get("NEMOTRON_DRIVE_DIR")
            os.environ["NEMOTRON_LOCAL_WORK_DIR"] = str(local_work_dir)
            os.environ["NEMOTRON_DRIVE_DIR"] = str(drive_dir)

            try:
                os.chdir(tmp_root)
                ns = {"__name__": "__main__"}
                for cell_name in ("cell2.py", "cell3.py"):
                    exec(compile((DEFAULT_CELLS_DIR / cell_name).read_text(encoding="utf-8"), cell_name, "exec"), ns)

                with patch.object(urllib.request, "urlopen", side_effect=lambda req, timeout=120: FakeHTTPResponse(bundle_bytes)):
                    cell4_code = (DEFAULT_CELLS_DIR / "cell4.py").read_text(encoding="utf-8")
                    exec(compile(cell4_code, "cell4.py", "exec"), ns)

                self.assertTrue(ns["BUNDLE_ORIGIN"].startswith("github:"))
                drive_bundle = drive_dir / "nemotron_18class_colab_bundle.zip"
                self.assertTrue(drive_bundle.is_file(), "GitHub-downloaded bundle was not copied to Google Drive!")
                self.assertEqual(sha256_bytes(drive_bundle.read_bytes()), sha256_bytes(bundle_bytes))
            finally:
                os.chdir(old_cwd)
                if old_local_env is None:
                    os.environ.pop("NEMOTRON_LOCAL_WORK_DIR", None)
                else:
                    os.environ["NEMOTRON_LOCAL_WORK_DIR"] = old_local_env
                if old_drive_env is None:
                    os.environ.pop("NEMOTRON_DRIVE_DIR", None)
                else:
                    os.environ["NEMOTRON_DRIVE_DIR"] = old_drive_env

    def test_05_edge_cases_and_cell9_evaluation(self):
        """Test error handling edge cases and cell9.py head-to-head evaluation table builder."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_root = Path(tmpdir)
            local_work_dir = tmp_root / "work"
            drive_dir = tmp_root / "drive"
            old_local_env = os.environ.get("NEMOTRON_LOCAL_WORK_DIR")
            old_drive_env = os.environ.get("NEMOTRON_DRIVE_DIR")
            os.environ["NEMOTRON_LOCAL_WORK_DIR"] = str(local_work_dir)
            os.environ["NEMOTRON_DRIVE_DIR"] = str(drive_dir)

            try:
                ns = {"__name__": "__main__"}
                for cell_name in ("cell2.py", "cell3.py", "cell4.py"):
                    exec(compile((DEFAULT_CELLS_DIR / cell_name).read_text(encoding="utf-8"), cell_name, "exec"), ns)

                # Load function definitions from cell5 before cell6
                cell5_code = (DEFAULT_CELLS_DIR / "cell5.py").read_text(encoding="utf-8")
                cell5_ast = ast.parse(cell5_code)
                func_nodes = [
                    n for n in cell5_ast.body
                    if isinstance(n, (ast.Import, ast.ImportFrom, ast.FunctionDef, ast.ClassDef))
                    or (
                        isinstance(n, ast.Assign)
                        and isinstance(n.targets[0], ast.Name)
                        and n.targets[0].id in ("WORD_PATTERN", "ALLOWED_TYPES_SET", "TYPE_ALIASES", "GOLD_EXTRA_ALIASES")
                    )
                ]
                mod = ast.Module(body=func_nodes, type_ignores=[])
                exec(compile(mod, "cell5_funcs.py", "exec"), ns)

                exec(compile((DEFAULT_CELLS_DIR / "cell6.py").read_text(encoding="utf-8"), "cell6.py", "exec"), ns)

                # Edge case 1: Invalid BIO tag in entity_spans
                with self.assertRaises(ValueError):
                    ns["entity_spans"](["B-PER", "INVALID_TAG"])

                # Edge case 2: Mismatched token/tag lengths in build_record
                with self.assertRaises(ValueError):
                    ns["build_record"]("gold", "train", "ref#0", ["Satu", "Dua"], ["O"], {})

                # Edge case 3: Unknown tag in chunk_record
                mock_tok = MockFastTokenizer()
                with self.assertRaises(ValueError):
                    ns["chunk_record"](
                        {"sentence_id": "s1", "tokens": ["Halo"], "tags": ["B-REG"]},
                        mock_tok,
                        ns["LABELS"],
                    )

                # Edge case 4: Unpredicted words or duplicate sentence IDs in recombine_predictions
                with self.assertRaises(ValueError):
                    ns["recombine_predictions"](
                        [{"sentence_id": "dup", "tokens": ["A"]}, {"sentence_id": "dup", "tokens": ["B"]}],
                        [],
                        [],
                        ns["LABELS"],
                    )

                # Test cell9.py evaluation with mocked predict_with_model and fake best_model
                test_records = [
                    {"sentence_id": "t1", "tokens": ["Presiden", "Joko", "Widodo", "di", "Jakarta", "."], "tags": ["B-NOR", "B-PER", "I-PER", "O", "B-GPE", "O"]},
                    {"sentence_id": "t2", "tokens": ["Harga", "BBM", "Rp", "10.000", "."], "tags": ["O", "B-PRD", "B-MON", "I-MON", "O"]},
                ]
                ns["PREPARED_DATA"] = {"gold": {"test": test_records}}
                ns["TOKENIZER"] = mock_tok

                for run_id in ("gold_s42", "nemotron_18class_s42"):
                    bm = ns["RUNS_DIR"] / run_id / "best_model"
                    bm.mkdir(parents=True, exist_ok=True)
                    (bm / "config.json").write_text("{}", encoding="utf-8")

                ns["predict_with_model"] = lambda model_dir, records, tokenizer, config=None, work_dir=None: [
                    list(r["tags"]) for r in records
                ]

                cell9_code = (DEFAULT_CELLS_DIR / "cell9.py").read_text(encoding="utf-8")
                exec(compile(cell9_code, "cell9.py", "exec"), ns)

                self.assertIn("EVAL_BUNDLE", ns)
                self.assertEqual(len(ns["EVAL_BUNDLE"]["per_class_rows"]), 18)
                self.assertTrue((drive_dir / "tables" / "overall_comparison.csv").is_file())
                self.assertTrue((drive_dir / "tables" / "per_class_18_comparison.csv").is_file())
                self.assertTrue((drive_dir / "predictions" / "gold_s42_test_predictions.jsonl").is_file())
                self.assertTrue((drive_dir / "predictions" / "nemotron_s42_test_predictions.jsonl").is_file())
            finally:
                if old_local_env is None:
                    os.environ.pop("NEMOTRON_LOCAL_WORK_DIR", None)
                else:
                    os.environ["NEMOTRON_LOCAL_WORK_DIR"] = old_local_env
                if old_drive_env is None:
                    os.environ.pop("NEMOTRON_DRIVE_DIR", None)
                else:
                    os.environ["NEMOTRON_DRIVE_DIR"] = old_drive_env

    def test_06_train_scenario_model_checkpoint_integrity_and_drive_resume(self):
        """Test train_scenario_model, cell7, cell8, predict_with_model, checkpoint verification, Drive resume, and cp1252 safety."""
        import subprocess
        import types
        from unittest.mock import patch

        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_root = Path(tmpdir)
            local_work_dir = tmp_root / "work"
            drive_dir = tmp_root / "drive"

            # 1. Verify cell2.py runs cleanly in a fresh subprocess with PYTHONIOENCODING=cp1252
            env_cp1252 = dict(os.environ)
            env_cp1252["PYTHONIOENCODING"] = "cp1252"
            env_cp1252["NEMOTRON_LOCAL_WORK_DIR"] = str(local_work_dir)
            env_cp1252["NEMOTRON_DRIVE_DIR"] = str(drive_dir)
            proc = subprocess.run(
                [sys.executable, str(DEFAULT_CELLS_DIR / "cell2.py")],
                env=env_cp1252,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                check=False,
            )
            self.assertEqual(proc.returncode, 0, f"cell2.py failed under cp1252: {proc.stderr}")

            # 2. Build stub torch, datasets, and transformers modules to exercise train_scenario_model & predict_with_model
            fake_torch = types.ModuleType("torch")
            fake_torch.__version__ = "2.5.0+mock"
            fake_torch.float32 = "float32"
            fake_torch.manual_seed = lambda s: None
            fake_torch.are_deterministic_algorithms_enabled = lambda: True
            fake_torch.cuda = types.SimpleNamespace(
                is_available=lambda: False,
                device_count=lambda: 0,
                is_bf16_supported=lambda: False,
                empty_cache=lambda: None,
            )
            fake_torch.backends = types.SimpleNamespace(
                cudnn=types.SimpleNamespace(deterministic=True, benchmark=False, allow_tf32=False, version=lambda: None),
                cuda=types.SimpleNamespace(matmul=types.SimpleNamespace(allow_tf32=False)),
            )

            fake_datasets = types.ModuleType("datasets")

            class FakeDataset:
                def __init__(self, items):
                    self.items = list(items)

                def __len__(self):
                    return len(self.items)

                @classmethod
                def from_list(cls, items):
                    return cls(items)

            fake_datasets.Dataset = FakeDataset

            fake_transformers = types.ModuleType("transformers")
            fake_transformers.__version__ = "4.46.0+mock"
            fake_transformers.set_seed = lambda seed, deterministic=True: None

            class FakeTokenizer(MockFastTokenizer):
                @classmethod
                def from_pretrained(cls, *args, **kwargs):
                    return cls()

                def save_pretrained(self, save_dir: str):
                    p = Path(save_dir)
                    p.mkdir(parents=True, exist_ok=True)
                    (p / "tokenizer_config.json").write_text("{}", encoding="utf-8")

            class FakeConfig:
                num_labels = 37
                id2label = {}
                label2id = {}
                hidden_dropout_prob = 0.1
                attention_probs_dropout_prob = 0.1
                classifier_dropout = 0.1

                @classmethod
                def from_pretrained(cls, *args, **kwargs):
                    return cls()

            class FakeModel:
                @classmethod
                def from_pretrained(cls, pretrained_model_name_or_path, *args, **kwargs):
                    p = Path(pretrained_model_name_or_path)
                    if p.exists() and not (p / "model.safetensors").is_file():
                        raise FileNotFoundError(f"Missing model.safetensors in {p}")
                    return cls()

            class FakeTrainingArguments:
                def __init__(
                    self,
                    output_dir="",
                    per_device_train_batch_size=32,
                    gradient_accumulation_steps=1,
                    per_device_eval_batch_size=64,
                    learning_rate=2e-5,
                    weight_decay=0.01,
                    adam_beta1=0.9,
                    adam_beta2=0.999,
                    adam_epsilon=1e-8,
                    warmup_ratio=0.10,
                    lr_scheduler_type="linear",
                    num_train_epochs=10,
                    max_grad_norm=1.0,
                    fp16=False,
                    bf16=False,
                    tf32=False,
                    gradient_checkpointing=False,
                    save_strategy="epoch",
                    eval_strategy="epoch",
                    logging_strategy="epoch",
                    load_best_model_at_end=True,
                    metric_for_best_model="macro_f1",
                    greater_is_better=True,
                    save_total_limit=1,
                    restore_callback_states_from_checkpoint=True,
                    seed=42,
                    data_seed=42,
                    report_to="none",
                    dataloader_num_workers=0,
                    dataloader_pin_memory=False,
                    dataloader_persistent_workers=False,
                    label_smoothing_factor=0.0,
                    optim="adamw_torch",
                    full_determinism=False,
                ):
                    self.output_dir = output_dir

            class FakeTrainerCallback:
                pass

            class FakeEarlyStoppingCallback(FakeTrainerCallback):
                def __init__(self, early_stopping_patience=2, early_stopping_threshold=0.0):
                    self.patience = early_stopping_patience

            class FakeCollator:
                def __init__(self, tokenizer, pad_to_multiple_of=8):
                    self.pad_to_multiple_of = pad_to_multiple_of

            class FakeLogits:
                def __init__(self, pred_ids_2d):
                    self._ids = pred_ids_2d

                def argmax(self, axis=-1):
                    return self._ids

            train_calls = []

            class FakeTrainer:
                def __init__(
                    self,
                    model=None,
                    args=None,
                    train_dataset=None,
                    eval_dataset=None,
                    data_collator=None,
                    compute_metrics=None,
                    callbacks=None,
                    processing_class=None,
                ):
                    self.model = model
                    self.args = args
                    self.train_dataset = train_dataset
                    self.eval_dataset = eval_dataset
                    self.compute_metrics = compute_metrics
                    self.callbacks = callbacks or []
                    self.state = types.SimpleNamespace(
                        global_step=12,
                        epoch=2.0,
                        best_metric=0.8125,
                        best_model_checkpoint=str(Path(args.output_dir) / "checkpoint-12"),
                        log_history=[
                            {"epoch": 1.0, "loss": 0.42},
                            {"epoch": 1.0, "eval_loss": 0.21, "eval_micro_f1": 0.80, "eval_macro_f1": 0.75},
                            {"epoch": 2.0, "loss": 0.19},
                            {"epoch": 2.0, "eval_loss": 0.16, "eval_micro_f1": 0.85, "eval_macro_f1": 0.8125},
                        ],
                        to_dict=lambda: {"global_step": 12, "epoch": 2.0, "best_metric": 0.8125},
                    )

                def train(self, resume_from_checkpoint=None):
                    train_calls.append(resume_from_checkpoint)
                    ckpt_dir = Path(self.args.output_dir) / "checkpoint-12"
                    ckpt_dir.mkdir(parents=True, exist_ok=True)
                    for req_file in ("optimizer.pt", "scheduler.pt", "trainer_state.json", "rng_state.pth", "config.json", "model.safetensors"):
                        (ckpt_dir / req_file).write_text(f"mock-{req_file}", encoding="utf-8")
                    for cb in self.callbacks:
                        if hasattr(cb, "on_save"):
                            cb.on_save(self.args, self.state, None)
                    if self.compute_metrics and self.eval_dataset:
                        pred_2d = [
                            [(lbl if lbl != -100 else 0) for lbl in item["labels"]]
                            for item in self.eval_dataset.items
                        ]
                        eval_out = types.SimpleNamespace(predictions=FakeLogits(pred_2d))
                        metrics = self.compute_metrics(eval_out)
                        self.state.best_metric = metrics.get("macro_f1", 0.8125)
                    return types.SimpleNamespace(metrics={"train_loss": 0.19, "train_runtime": 1.5})

                def save_model(self, output_dir: str):
                    out_p = Path(output_dir)
                    out_p.mkdir(parents=True, exist_ok=True)
                    (out_p / "config.json").write_text('{"architectures": ["BertForTokenClassification"]}', encoding="utf-8")
                    (out_p / "model.safetensors").write_bytes(b"MOCK_INDOBERT_LARGE_SAFENTENSORS_WEIGHTS")

                def predict(self, test_dataset):
                    pred_2d = [
                        [(lbl if lbl != -100 else 0) for lbl in item["labels"]]
                        for item in test_dataset.items
                    ]
                    return types.SimpleNamespace(predictions=FakeLogits(pred_2d))

            fake_transformers.AutoTokenizer = FakeTokenizer
            fake_transformers.AutoConfig = FakeConfig
            fake_transformers.AutoModelForTokenClassification = FakeModel
            fake_transformers.TrainingArguments = FakeTrainingArguments
            fake_transformers.TrainerCallback = FakeTrainerCallback
            fake_transformers.EarlyStoppingCallback = FakeEarlyStoppingCallback
            fake_transformers.DataCollatorForTokenClassification = FakeCollator
            fake_transformers.Trainer = FakeTrainer

            old_local_env = os.environ.get("NEMOTRON_LOCAL_WORK_DIR")
            old_drive_env = os.environ.get("NEMOTRON_DRIVE_DIR")
            os.environ["NEMOTRON_LOCAL_WORK_DIR"] = str(local_work_dir)
            os.environ["NEMOTRON_DRIVE_DIR"] = str(drive_dir)

            try:
                with patch.dict(
                    sys.modules,
                    {"torch": fake_torch, "datasets": fake_datasets, "transformers": fake_transformers},
                ):
                    ns = {"__name__": "__main__", "torch": fake_torch}
                    for cell_name in ("cell2.py", "cell3.py", "cell6.py"):
                        cell_5_defs = (
                            "from collections import Counter\n"
                            "import csv, re\n"
                            "def entity_spans(tags):\n"
                            "    res, s, k = [], None, None\n"
                            "    for idx, t in enumerate(list(tags)+['O']):\n"
                            "        p, c = ('O', None) if t == 'O' else t.split('-', 1)\n"
                            "        if s is not None and (p != 'I' or c != k):\n"
                            "            res.append((s, idx, k)); s, k = None, None\n"
                            "        if p != 'O' and s is None: s, k = idx, c\n"
                            "    return res\n"
                            "def write_csv_rows(path, rows):\n"
                            "    path.parent.mkdir(parents=True, exist_ok=True)\n"
                            "    path.write_text('ok', encoding='utf-8')\n"
                        )
                        if cell_name == "cell6.py":
                            exec(cell_5_defs, ns)
                        exec(compile((DEFAULT_CELLS_DIR / cell_name).read_text(encoding="utf-8"), cell_name, "exec"), ns)

                    mini_records = [
                        {"sentence_id": "s1", "tokens": ["Presiden", "Joko", "Widodo", "di", "Jakarta"], "tags": ["B-NOR", "B-PER", "I-PER", "O", "B-GPE"]},
                        {"sentence_id": "s2", "tokens": ["Harga", "BBM", "Rp", "10.000"], "tags": ["O", "B-PRD", "B-MON", "I-MON"]},
                    ]
                    ns["PREPARED_DATA"] = {
                        "gold": {"train": mini_records, "validation": mini_records, "test": mini_records},
                        "nemotron_18class": {"train": mini_records, "validation": mini_records},
                    }

                    # Execute cell7.py and cell8.py (fresh training + Drive backup)
                    exec(compile((DEFAULT_CELLS_DIR / "cell7.py").read_text(encoding="utf-8"), "cell7.py", "exec"), ns)
                    exec(compile((DEFAULT_CELLS_DIR / "cell8.py").read_text(encoding="utf-8"), "cell8.py", "exec"), ns)
                    self.assertEqual(len(train_calls), 2)
                    self.assertIsNone(train_calls[0])

                    # Verify Drive backup has intact best_model and run_manifest.json
                    drive_gold_run = drive_dir / "runs" / "gold_s42"
                    self.assertIsNotNone(ns["verify_completed_run_dir"](drive_gold_run))

                    # Simulate Colab VM disconnect: delete local run_dir, re-run cell7 -> must restore from Drive & skip training!
                    shutil.rmtree(ns["RUNS_DIR"] / "gold_s42")
                    exec(compile((DEFAULT_CELLS_DIR / "cell7.py").read_text(encoding="utf-8"), "cell7.py", "exec"), ns)
                    self.assertEqual(len(train_calls), 2, "Should have restored verified model from Drive without retraining!")

                    # Simulate corrupted/incomplete Drive backup (model.safetensors missing, config.json still present)
                    shutil.rmtree(ns["RUNS_DIR"] / "gold_s42")
                    (drive_gold_run / "best_model" / "model.safetensors").unlink()
                    self.assertIsNone(ns["verify_completed_run_dir"](drive_gold_run))

                    # Also place a verified checkpoint-8 and an incomplete checkpoint-9 on Drive to test checkpoint auto-restore
                    train_hash = ns["GOLD_RUN_MANIFESTS"][42]["train_hash"]
                    cp8 = drive_gold_run / "checkpoints" / "checkpoint-8"
                    cp8.mkdir(parents=True, exist_ok=True)
                    for req_file in ("optimizer.pt", "scheduler.pt", "trainer_state.json", "rng_state.pth", "config.json", "model.safetensors"):
                        (cp8 / req_file).write_text(f"cp8-{req_file}", encoding="utf-8")
                    ns["write_checkpoint_manifest"](cp8, train_hash, require_scaler=False)

                    cp9_corrupt = drive_gold_run / "checkpoints" / "checkpoint-9"
                    cp9_corrupt.mkdir(parents=True, exist_ok=True)
                    (cp9_corrupt / "config.json").write_text("{}", encoding="utf-8")

                    exec(compile((DEFAULT_CELLS_DIR / "cell7.py").read_text(encoding="utf-8"), "cell7.py", "exec"), ns)
                    self.assertEqual(len(train_calls), 3, "Corrupted best_model must trigger retraining!")
                    self.assertTrue(str(train_calls[-1]).endswith("checkpoint-8"), f"Expected resume from checkpoint-8, got {train_calls[-1]}")

                    # Execute cell9.py using the real predict_with_model (not monkeypatched)
                    exec(compile((DEFAULT_CELLS_DIR / "cell9.py").read_text(encoding="utf-8"), "cell9.py", "exec"), ns)
                    self.assertEqual(ns["EVAL_BUNDLE"]["evaluation_results"]["gold"][42]["support"], 5)
                    self.assertEqual(ns["EVAL_BUNDLE"]["evaluation_results"]["gold"][42]["fn"], 5)
            finally:
                if old_local_env is None:
                    os.environ.pop("NEMOTRON_LOCAL_WORK_DIR", None)
                else:
                    os.environ["NEMOTRON_LOCAL_WORK_DIR"] = old_local_env
                if old_drive_env is None:
                    os.environ.pop("NEMOTRON_DRIVE_DIR", None)
                else:
                    os.environ["NEMOTRON_DRIVE_DIR"] = old_drive_env


if __name__ == "__main__":
    unittest.main()
