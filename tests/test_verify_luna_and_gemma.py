import sys
import unittest
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from scripts.verify_luna_gemini import (
    parse_json_from_response as parse_luna_json,
    sanitize_and_validate_entities as sanitize_luna_entities,
    align_entities_to_bio as align_luna_bio,
    ALLOWED_TYPES_SET as LUNA_ALLOWED_TYPES
)

from scripts.verify_gemma_gemini import (
    parse_json_from_response as parse_gemma_gemini_json,
    sanitize_and_validate_entities as sanitize_gemma_gemini_entities,
    align_entities_to_bio as align_gemma_gemini_bio,
    ALLOWED_TYPES_SET as GEMMA_GEMINI_ALLOWED_TYPES
)

from scripts.verify_gemma_nemotron_vl import (
    format_api_key as format_gemma_key,
    parse_json_from_response as parse_gemma_json,
    sanitize_and_validate_entities as sanitize_gemma_entities,
    align_entities_to_bio as align_gemma_bio,
    ALLOWED_TYPES_SET as GEMMA_ALLOWED_TYPES
)


class TestVerifyLunaAndGemma(unittest.TestCase):
    def test_gemma_format_api_key(self):
        self.assertEqual(format_gemma_key("testkey123"), "sk-or-v1-testkey123")
        self.assertEqual(format_gemma_key("sk-testkey123"), "sk-or-v1-testkey123")
        self.assertEqual(format_gemma_key("sk-or-testkey123"), "sk-or-v1-testkey123")
        self.assertEqual(format_gemma_key("sk-or-v1-testkey123"), "sk-or-v1-testkey123")

    def test_luna_sse_stream_json_parsing(self):
        sse_text = (
            'data: {"id":"chatcmpl-1","choices":[{"delta":{"role":"assistant"}}]}\n\n'
            'data: {"id":"chatcmpl-1","choices":[{"delta":{"content":"{\\"data\\": "}}]}\n\n'
            'data: {"id":"chatcmpl-1","choices":[{"delta":{"content":"[{\\"text\\": \\"Halo\\", \\"entities\\": []}]}"}}]}\n\n'
            'data: [DONE]\n\n'
        )
        res = parse_luna_json(sse_text)
        self.assertIsNotNone(res)
        self.assertIn("data", res)
        self.assertEqual(len(res["data"]), 1)
        self.assertEqual(res["data"][0]["text"], "Halo")

    def test_gemma_cot_reasoning_json_parsing(self):
        cot_text = (
            "<think>\n"
            "Analyzing sentence for Gemma verifier...\n"
            "Menteri Ketenagakerjaan is state leadership -> NOR.\n"
            "</think>\n"
            "```json\n"
            "{\"data\": [{\"text\": \"Ida Fauziah menteri\", \"entities\": [{\"entity\": \"Ida Fauziah\", \"type\": \"PER\"}]}]}\n"
            "```"
        )
        res = parse_gemma_json(cot_text)
        self.assertIsNotNone(res)
        self.assertIn("data", res)
        self.assertEqual(len(res["data"]), 1)
        self.assertEqual(res["data"][0]["entities"][0]["entity"], "Ida Fauziah")

    def test_luna_sanitization_and_letjen_rank_absorption(self):
        text = "Kepala BNPB Letjen Suharyanto memimpin evakuasi warga setelah erupsi Gunung Merapi di Kabupaten Sleman pada Senin 21 Mei 2018 ."
        raw_entities = [
            {"entity": "Kepala BNPB", "type": "TTL"},
            {"entity": "Letjen", "type": "TTL"},
            {"entity": "Suharyanto", "type": "PER"},
            {"entity": "Gunung Merapi", "type": "LOC"},
            {"entity": "di Kabupaten Sleman", "type": "GPE"},
            {"entity": "Senin", "type": "DAT"},
            {"entity": "21 Mei 2018", "type": "DAT"},
            {"entity": "umat Islam", "type": "NOR"},
            {"entity": "Bapak", "type": "TTL"},
            {"entity": "InvalidNotPresent", "type": "PER"}
        ]
        sanitized = sanitize_luna_entities(text, raw_entities)

        for s in sanitized:
            self.assertIn(s["entity"], text, f"Entity not in text: {s}")
            self.assertIn(s["type"], LUNA_ALLOWED_TYPES)
            self.assertNotIn(s["type"], ("REG", "TTL"))

        # Verify specific transformations
        self.assertTrue(any(s["entity"] == "Kepala BNPB" and s["type"] == "NOR" for s in sanitized))
        self.assertTrue(any(s["entity"] == "Letjen Suharyanto" and s["type"] == "PER" for s in sanitized))
        self.assertTrue(any(s["entity"] == "Gunung Merapi" and s["type"] == "LOC" for s in sanitized))
        self.assertTrue(any(s["entity"] == "Kabupaten Sleman" and s["type"] == "GPE" for s in sanitized))
        # Verify compound date merge
        self.assertTrue(any(s["entity"] == "Senin 21 Mei 2018" and s["type"] == "DAT" for s in sanitized))

        # Verify drops
        self.assertFalse(any(s["entity"] == "umat Islam" for s in sanitized))
        self.assertFalse(any(s["entity"] == "Bapak" for s in sanitized))
        self.assertFalse(any(s["entity"] == "InvalidNotPresent" for s in sanitized))

    def test_gemma_sanitization_and_rules(self):
        text = "Menteri Ketenagakerjaan Ida Fauziah menginstruksikan Bulog menjaga stok 5 juta ton beras di Jawa Barat pada Januari 2024 ."
        raw_entities = [
            {"entity": "Menteri Ketenagakerjaan", "type": "TTL"},
            {"entity": "Ida Fauziah", "type": "PER"},
            {"entity": "Bulog", "type": "ORG"},
            {"entity": "5 juta ton", "type": "QTY"},
            {"entity": "beras", "type": "PRD"},
            {"entity": "di Jawa Barat", "type": "LOC"},
            {"entity": "Januari 2024", "type": "DAT"},
            {"entity": "Islam", "type": "REG"}
        ]
        sanitized = sanitize_gemma_entities(text, raw_entities)

        for s in sanitized:
            self.assertIn(s["entity"], text, f"Entity not in text: {s}")
            self.assertIn(s["type"], GEMMA_ALLOWED_TYPES)
            self.assertNotIn(s["type"], ("REG", "TTL"))

        self.assertTrue(any(s["entity"] == "Menteri Ketenagakerjaan" and s["type"] == "NOR" for s in sanitized))
        self.assertTrue(any(s["entity"] == "Ida Fauziah" and s["type"] == "PER" for s in sanitized))
        self.assertTrue(any(s["entity"] == "Bulog" and s["type"] == "ORG" for s in sanitized))
        self.assertTrue(any(s["entity"] == "5 juta ton" and s["type"] == "QTY" for s in sanitized))
        self.assertTrue(any(s["entity"] == "beras" and s["type"] == "PRD" for s in sanitized))
        self.assertTrue(any(s["entity"] == "Jawa Barat" and s["type"] == "LOC" for s in sanitized))
        self.assertTrue(any(s["entity"] == "Januari 2024" and s["type"] == "DAT" for s in sanitized))
        self.assertFalse(any(s["entity"] == "Islam" for s in sanitized))

    def test_gemma_gemini_sse_and_sanitization(self):
        text = "Menteri Ketenagakerjaan Ida Fauziah menyalurkan beras Bulog sebanyak 5 juta ton ke Jawa Barat pada Januari 2024 ."
        raw_items = [
            {"entity": "Menteri", "type": "TTL"},
            {"entity": "Ida Fauziah", "type": "PER"},
            {"entity": "Bulog", "type": "ORG"},
            {"entity": "5 juta ton", "type": "QTY"},
            {"entity": "beras", "type": "PRD"},
            {"entity": "ke Jawa Barat", "type": "GPE"},
            {"entity": "Januari 2024", "type": "DAT"}
        ]
        sanitized = sanitize_gemma_gemini_entities(text, raw_items)
        types = {s["type"] for s in sanitized}
        self.assertIn("NOR", types)
        self.assertIn("PER", types)
        self.assertIn("ORG", types)
        self.assertIn("QTY", types)
        self.assertIn("PRD", types)
        self.assertIn("GPE", types)
        self.assertIn("DAT", types)
        self.assertNotIn("TTL", types)
        self.assertNotIn("REG", types)

    def test_bio_tag_alignment(self):
        text = "Letjen Suharyanto mengunjungi Monas di Jakarta ."
        ents = [
            {"entity": "Letjen Suharyanto", "type": "PER"},
            {"entity": "Monas", "type": "LOC"},
            {"entity": "Jakarta", "type": "GPE"}
        ]
        bio_luna = align_luna_bio(text, ents)
        bio_gemma = align_gemma_bio(text, ents)
        self.assertEqual(bio_luna, bio_gemma)
        self.assertGreater(len(bio_luna), 0)
        self.assertEqual(bio_luna[0], ("Letjen", "B-PER"))
        self.assertEqual(bio_luna[1], ("Suharyanto", "I-PER"))


if __name__ == "__main__":
    unittest.main()
