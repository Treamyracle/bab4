import sys
import unittest
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from scripts.verify_nemotron_ultra import (
    format_api_key, parse_json_from_response,
    sanitize_and_validate_entities, align_entities_to_bio,
    ALLOWED_TYPES_SET, ACTIVE_ENTITY_TYPES
)

class TestVerifyNemotron(unittest.TestCase):
    def test_format_api_key(self):
        self.assertEqual(format_api_key("50c67d1d"), "sk-or-v1-50c67d1d")
        self.assertEqual(format_api_key("sk-50c67d1d"), "sk-or-v1-50c67d1d")
        self.assertEqual(format_api_key("sk-or-50c67d1d"), "sk-or-v1-50c67d1d")
        self.assertEqual(format_api_key("sk-or-v1-50c67d1d"), "sk-or-v1-50c67d1d")

    def test_parse_json_from_response_cot(self):
        raw_with_cot = "<think>\nThinking about entities...\nPresiden is NOR.\n</think>\n```json\n{\"data\": [{\"text\": \"Halo\", \"entities\": []}]}\n```"
        res = parse_json_from_response(raw_with_cot)
        self.assertEqual(res, {"data": [{"text": "Halo", "entities": []}]})

    def test_parse_json_from_response_syntax_repair(self):
        raw_malformed = '{"data": [{"text": "A", "entities": [{"entity": "A", "type": "PER",},],},],}'
        res2 = parse_json_from_response(raw_malformed)
        self.assertIsNotNone(res2)
        self.assertEqual(len(res2["data"]), 1)

    def test_sanitize_and_validate_entities_10_rules(self):
        text = "Presiden Joko Widodo bersama dr. Andi mengunjungi Masjid Istiqlal di Jakarta pada hari Selasa selama dua tahun di Asia Tenggara."
        raw_entities = [
            {"entity": "Presiden", "type": "TTL"},           # -> NOR
            {"entity": "Joko Widodo", "type": "PER"},        # -> PER
            {"entity": "Bapak", "type": "TTL"},              # -> dropped (O)
            {"entity": "dr.", "type": "TTL"},                # -> PER
            {"entity": "Masjid Istiqlal", "type": "REG"},    # -> FAC
            {"entity": "di Jakarta", "type": "GPE"},         # -> prep stripped: Jakarta
            {"entity": "pada hari Selasa", "type": "DAT"},   # -> prep stripped: Selasa
            {"entity": "selama dua tahun", "type": "QTY"},   # -> prep stripped: dua tahun
            {"entity": "Asia Tenggara", "type": "REG"},      # -> LOC
            {"entity": "Islam", "type": "REG"},              # -> dropped (O, religion)
            {"entity": "NonExistent", "type": "PER"},        # -> dropped (not in text)
        ]
        sanitized = sanitize_and_validate_entities(text, raw_entities)
        self.assertEqual(len(sanitized), 8)
        for s in sanitized:
            self.assertIn(s["entity"], text)
            self.assertIn(s["type"], ALLOWED_TYPES_SET)
            self.assertNotIn(s["type"], ("REG", "TTL"))

        self.assertTrue(any(s["entity"] == "Presiden" and s["type"] == "NOR" for s in sanitized))
        self.assertTrue(any(s["entity"] == "Jakarta" and s["type"] == "GPE" for s in sanitized))
        self.assertTrue(any(s["entity"] == "Selasa" and s["type"] == "DAT" for s in sanitized))
        self.assertTrue(any(s["entity"] == "dua tahun" and s["type"] == "QTY" for s in sanitized))
        self.assertTrue(any(s["entity"] == "Asia Tenggara" and s["type"] == "LOC" for s in sanitized))
        self.assertTrue(any(s["entity"] == "Masjid Istiqlal" and s["type"] == "FAC" for s in sanitized))
        self.assertFalse(any(s["entity"] == "Islam" for s in sanitized))
        self.assertFalse(any(s["entity"] == "NonExistent" for s in sanitized))

    def test_align_entities_to_bio(self):
        text = "Presiden Joko Widodo mengunjungi Monas di Jakarta ."
        ents = [
            {"entity": "Presiden", "type": "NOR"},
            {"entity": "Joko Widodo", "type": "PER"},
            {"entity": "Monas", "type": "LOC"},
            {"entity": "Jakarta", "type": "GPE"}
        ]
        bio = align_entities_to_bio(text, ents)
        self.assertGreater(len(bio), 0)
        last_t = None
        for tok, tag in bio:
            if tag.startswith("B-"):
                last_t = tag[2:]
            elif tag.startswith("I-"):
                self.assertEqual(tag[2:], last_t, f"Orphan I- tag: {tok} {tag}")
            else:
                last_t = None

if __name__ == "__main__":
    unittest.main()
