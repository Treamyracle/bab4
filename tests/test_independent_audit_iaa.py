"""Unit tests for the 18-class NERGRIT Independent Dual-Annotator IAA Pipeline."""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.run_independent_audit_iaa import (  # noqa: E402
    ACTIVE_TYPES,
    AUDIT_PROMPT,
    InvalidResult,
    _quotas,
    _stratified,
    aggregate,
    align_entities_to_bio,
    bootstrap,
    compute_iaa,
    consensus_spans,
    entity_spans,
    kappa,
    normalize_result,
    parse_json,
    quality_record,
    spans_to_bio,
    summarize_quality,
    unit_stats,
    write_json,
)


class TestIndependentAuditIAA(unittest.TestCase):
    def test_audit_prompt_enforces_latest_nergrit_rules(self):
        required_phrases = [
            "Presiden",
            "NOR",
            "Letjen Suharyanto",
            "Jenderal Tito Karnavian",
            "Selasa ( 15 / 5 / 2018 )",
            "EKSKLUSI PREPOSISI",
            "dua tahun",
            "QTY",
            "PRD",
            "Alquran",
            "umat Islam",
            "REG",
            "TTL",
        ]
        for phrase in required_phrases:
            self.assertIn(phrase, AUDIT_PROMPT, f"AUDIT_PROMPT missing rule marker: {phrase}")

    def test_align_entities_to_bio_and_spans(self):
        text = "Presiden Joko Widodo meresmikan Tol Cipali pada Selasa ( 15 / 5 / 2018 ) ."
        entities = [
            {"entity": "Presiden", "type": "NOR"},
            {"entity": "Joko Widodo", "type": "PER"},
            {"entity": "Tol Cipali", "type": "FAC"},
            {"entity": "Selasa ( 15 / 5 / 2018 )", "type": "DAT"},
        ]
        pairs = align_entities_to_bio(text, entities)
        toks = [w for w, _ in pairs]
        tags = [t for _, t in pairs]
        self.assertEqual(toks[0], "Presiden")
        self.assertEqual(tags[0], "B-NOR")
        self.assertEqual(tags[1:3], ["B-PER", "I-PER"])
        spans = entity_spans(tags)
        self.assertEqual(spans[0], (0, 1, "NOR"))
        self.assertEqual(spans[1], (1, 3, "PER"))
        self.assertEqual(spans[2], (4, 6, "FAC"))
        self.assertEqual(spans[3], (7, 15, "DAT"))
        self.assertEqual(spans_to_bio(len(toks), spans), tags)

    def test_parse_json_strips_thinking_and_fences(self):
        raw = (
            "<think>Checking span boundaries...</think>\n"
            "```json\n"
            '{"results": [{"sample_id": "D01-001", "entities": [], "missing_entities": "NONE", "notes": ""},]}\n'
            "```"
        )
        parsed = parse_json(raw)
        self.assertIsNotNone(parsed)
        self.assertEqual(parsed["results"][0]["sample_id"], "D01-001")

    def test_normalize_result_rules_keep_remove_replace_missing_and_drop_reg_ttl(self):
        sample = {
            "sample_id": "D01-001",
            "tokens": ["Presiden", "Joko", "Widodo", "membaca", "Alquran", "naik", "mobil", "."],
            "entities": [
                [0, 1, "NOR"],
                [1, 3, "PER"],
                [4, 5, "WOA"],
            ],
        }
        res = {
            "sample_id": "D01-001",
            "entities": [
                {"id": "E001", "decision": "CORRECT", "action": "KEEP", "note": ""},
                {"id": "E002", "decision": "INCORRECT", "action": "REPLACE:PER:2-3", "note": "same span"},
                {"id": "E003", "decision": "INCORRECT", "action": "REMOVE", "note": "religious scripture -> O"},
            ],
            "missing_entities": "PRD:7-7; REG:5-5",
            "notes": "",
        }
        norm = normalize_result(sample, res)
        # E002 REPLACE identical to original should normalize to CORRECT/KEEP
        self.assertEqual(norm["decisions"][1]["decision"], "CORRECT")
        self.assertEqual(norm["decisions"][1]["category"], "KEEP")
        # E003 removed; PRD:7-7 kept as missing; REG:5-5 automatically dropped
        self.assertEqual(norm["missing_spans"], [[6, 7, "PRD"]])
        self.assertEqual(norm["final_spans"], [[0, 1, "NOR"], [1, 3, "PER"], [6, 7, "PRD"]])

    def test_zero_entity_sentence_e0_stratum(self):
        sample = {
            "sample_id": "D03-001",
            "tokens": ["Pemerintah", "membahas", "anggaran", "."],
            "entities": [],
        }
        res = {
            "sample_id": "D03-001",
            "entities": [],
            "missing_entities": "NOR:1-1",
            "notes": "Pemerintah seharusnya NOR",
        }
        norm = normalize_result(sample, res)
        self.assertEqual(norm["decisions"], [])
        self.assertEqual(norm["missing_spans"], [[0, 1, "NOR"]])
        self.assertEqual(norm["final_spans"], [[0, 1, "NOR"]])

    def test_normalize_result_rejects_overlap(self):
        sample = {
            "sample_id": "D01-002",
            "tokens": ["Letjen", "Suharyanto", "hadir"],
            "entities": [[0, 2, "PER"]],
        }
        bad = {
            "sample_id": "D01-002",
            "entities": [{"id": "E001", "decision": "CORRECT", "action": "KEEP"}],
            "missing_entities": "NOR:1-1",
        }
        with self.assertRaises(InvalidResult):
            normalize_result(sample, bad)

    def test_quotas_and_stratified(self):
        strata = {
            "E0_SHORT": [{"id": 1}],
            "E1_SHORT": [{"id": 2}, {"id": 3}],
            "E2PLUS_SHORT": [{"id": i} for i in range(10, 60)],
            "E2PLUS_LONG": [{"id": i} for i in range(60, 120)],
        }
        q = _quotas(strata, budget=100)
        self.assertEqual(sum(q.values()), 100)
        self.assertEqual(q["E0_SHORT"], 1)
        self.assertEqual(q["E1_SHORT"], 2)

        frame = []
        for idx in range(150):
            toks = ["Presiden", "Joko", "Widodo"] + (["extra"] * (idx % 5))
            tags = ["B-NOR", "B-PER", "I-PER"] + (["O"] * (idx % 5))
            frame.append({"sentence_id": f"ds-{idx:04d}", "tokens": toks, "tags": tags})
        selected, details = _stratified(frame, "nemotron", seed=20261022, sample_size=100)
        self.assertEqual(len(selected), 100)
        self.assertEqual(sum(s["n_h"] for s in details["strata"]), 100)

    def test_kappa_consensus_and_full_iaa_pipeline(self):
        self.assertEqual(kappa(10, 10, Counter({"O": 10}), Counter({"O": 10})), 1.0)
        with tempfile.TemporaryDirectory() as tmp:
            out_dir = Path(tmp)
            sample = {
                "sample_id": "D01-001",
                "dataset": "nemotron",
                "dataset_code": "D01",
                "sentence_id": "nemotron-001",
                "source_split": "verified_18class",
                "stratum": "E2PLUS_SHORT",
                "inclusion_probability": 0.5,
                "duplicate_records": 1,
                "conflicting_annotations": False,
                "tokens": ["Presiden", "Joko", "Widodo", "naik", "mobil", "."],
                "original_tags": ["B-NOR", "B-PER", "I-PER", "O", "O", "O"],
                "tags": ["B-NOR", "B-PER", "I-PER", "O", "O", "O"],
                "entities": [[0, 1, "NOR"], [1, 3, "PER"]],
                "source_record_hash": "abc",
            }
            manifest = {
                "schema_version": 2,
                "method": "independent_dual_annotator_llm_audit",
                "sampling_seed": 20261022,
                "sample_size_per_dataset": 1,
                "active_types": list(ACTIVE_TYPES),
                "datasets": {
                    "D01": {
                        "dataset": "nemotron",
                        "strata": [{"stratum": "E2PLUS_SHORT", "N_h": 10, "n_h": 1, "inclusion_probability": 0.1}],
                    }
                },
                "samples": [sample],
                "sample_manifest_hash": "deadbeef",
            }
            write_json(out_dir / "audit_sample_manifest.json", manifest)

            a1_rec = {
                "sample_id": "D01-001",
                "decisions": [
                    {"id": "E001", "original": [0, 1, "NOR"], "decision": "CORRECT", "category": "KEEP", "action": "KEEP", "replacement_spans": [[0, 1, "NOR"]], "note": ""},
                    {"id": "E002", "original": [1, 3, "PER"], "decision": "CORRECT", "category": "KEEP", "action": "KEEP", "replacement_spans": [[1, 3, "PER"]], "note": ""},
                ],
                "missing_spans": [[4, 5, "PRD"]],
                "final_spans": [[0, 1, "NOR"], [1, 3, "PER"], [4, 5, "PRD"]],
                "notes": "",
                "normalizations": [],
                "sample_manifest_hash": "deadbeef",
            }
            a2_rec = dict(a1_rec)
            write_json(out_dir / "annotator_A1" / "samples" / "D01-001.json", a1_rec)
            write_json(out_dir / "annotator_A2" / "samples" / "D01-001.json", a2_rec)

            cons = consensus_spans(sample, a1_rec, a2_rec)
            self.assertEqual(cons, {(0, 1, "NOR"), (1, 3, "PER"), (4, 5, "PRD")})
            q = quality_record(sample, cons)
            self.assertTrue(q["error"])
            self.assertEqual(dict(q["missing"]), {"PRD": 1})

            u = unit_stats(sample, a1_rec, a2_rec)
            agg = aggregate([u])
            self.assertEqual(agg["token_bio_kappa"], 1.0)
            self.assertEqual(agg["span_f1_agreement"], 1.0)
            ci = bootstrap([u], iterations=20, seed=42)
            self.assertEqual(ci["token_bio_kappa"], [1.0, 1.0])

            sq = summarize_quality([sample], [q], manifest["datasets"]["D01"])
            self.assertEqual(sq["weighted_sentence_error_rate"], 1.0)

            summary = compute_iaa(out_dir, manifest, allow_partial=False)
            self.assertEqual(summary["status"], "complete")
            self.assertTrue((out_dir / "IAA_REPORT.md").is_file())
            self.assertTrue((out_dir / "audit_iaa_results.zip").is_file())


if __name__ == "__main__":
    unittest.main()
