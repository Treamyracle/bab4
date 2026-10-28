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

        # Test unclosed <think> tag
        raw_unclosed = "<think>\nThinking without closing tag...\n```json\n{\"data\": [{\"text\": \"Dunia\", \"entities\": []}]}\n```"
        res_unclosed = parse_json_from_response(raw_unclosed)
        self.assertEqual(res_unclosed, {"data": [{"text": "Dunia", "entities": []}]})

    def test_parse_json_from_response_syntax_repair(self):
        raw_malformed = '{"data": [{"text": "A", "entities": [{"entity": "A", "type": "PER",},],},],}'
        res2 = parse_json_from_response(raw_malformed)
        self.assertIsNotNone(res2)
        self.assertEqual(len(res2["data"]), 1)

        # Test truncated JSON recovery
        raw_truncated = '{"data": [{"text": "Sentence 1", "entities": []}, {"text": "Sentence 2", "entities": [{"entity": "Joko", "type": "PER"'
        res3 = parse_json_from_response(raw_truncated)
        self.assertIsNotNone(res3)
        self.assertIn("data", res3)
        self.assertEqual(len(res3["data"]), 1)
        self.assertEqual(res3["data"][0]["text"], "Sentence 1")

    def test_sanitize_and_validate_entities_10_rules(self):
        text = (
            "Presiden Joko Widodo bersama dr. Andi dan Jenderal Tito Karnavian mengunjungi "
            "Masjid Istiqlal di DI Yogyakarta pada hari Selasa selama dua tahun di Asia Tenggara . "
            "PT Telkom mencatat laba sebesar 12 , 5 % pada kuartal ke - 4 seharga Rp 350 . 000 "
            "setelah menempuh jarak sejauh 500 kilometer pada sekitar pukul 08 . 00 WIB siang . "
            "Mereka membaca novel ' Laskar Pelangi ' yang diterjemahkan ke dalam bahasa Arab oleh umat Islam ."
        )
        raw_entities = [
            # Rule 2c: State leadership -> NOR
            {"entity": "Presiden", "type": "TTL"},
            # Rule 2b: Attached ranks absorbed into PER
            {"entity": "dr.", "type": "TTL"},
            {"entity": "Andi", "type": "PER"},
            {"entity": "Jenderal", "type": "TTL"},
            {"entity": "Tito Karnavian", "type": "PER"},
            # Rule 2a: Honorifics dropped to O
            {"entity": "Bapak", "type": "TTL"},
            # Rule 1: Places of worship -> FAC
            {"entity": "Masjid Istiqlal", "type": "REG"},
            # Exception to Rule 3: DI Yogyakarta (Daerah Istimewa) preserved as GPE
            {"entity": "DI Yogyakarta", "type": "GPE"},
            # Rule 3: Prepositions stripped
            {"entity": "pada hari Selasa", "type": "DAT"},
            {"entity": "selama dua tahun", "type": "QTY"},
            # Rule 1: Macro-regions -> LOC
            {"entity": "Asia Tenggara", "type": "REG"},
            # Rule 4: Commercial company -> ORG
            {"entity": "PT Telkom", "type": "ORG"},
            # Rule 3 & 17: Percentage predicate prefix stripped
            {"entity": "sebesar 12 , 5 %", "type": "PRC"},
            # Exception to Rule 3: ke - 4 preserved as ORD
            {"entity": "ke - 4", "type": "ORD"},
            # Rule 3 & 13: Monetary predicate prefix stripped
            {"entity": "seharga Rp 350 . 000", "type": "MON"},
            # Rule 3 & 14: Distance predicate prefix stripped
            {"entity": "sejauh 500 kilometer", "type": "QTY"},
            # Rule 7: Time prefix and diurnal suffix stripped
            {"entity": "sekitar pukul 08 . 00 WIB siang", "type": "TIM"},
            # Rule 10: Media type and quotes stripped
            {"entity": "novel ' Laskar Pelangi '", "type": "WOA"},
            # Rule 3 & 10: Chained prepositions stripped, 'bahasa' preserved
            {"entity": "ke dalam bahasa Arab", "type": "LAN"},
            # Rule 1: Religious terms dropped regardless of incoming tag
            {"entity": "Islam", "type": "NOR"},
            {"entity": "umat Islam", "type": "NOR"},
            # Invalid entity not in text
            {"entity": "NonExistentEntity", "type": "PER"},
        ]

        sanitized = sanitize_and_validate_entities(text, raw_entities)
        
        # Verify 18-class adherence
        for s in sanitized:
            self.assertIn(s["entity"], text, f"Entity not in text: {s}")
            self.assertIn(s["type"], ALLOWED_TYPES_SET, f"Type not allowed: {s}")
            self.assertNotIn(s["type"], ("REG", "TTL"), f"Forbidden tag: {s}")

        # Check expected transformations
        self.assertTrue(any(s["entity"] == "Presiden" and s["type"] == "NOR" for s in sanitized))
        self.assertTrue(any(s["entity"] == "dr. Andi" and s["type"] == "PER" for s in sanitized))
        self.assertTrue(any(s["entity"] == "Jenderal Tito Karnavian" and s["type"] == "PER" for s in sanitized))
        self.assertTrue(any(s["entity"] == "Masjid Istiqlal" and s["type"] == "FAC" for s in sanitized))
        self.assertTrue(any(s["entity"] == "DI Yogyakarta" and s["type"] == "GPE" for s in sanitized))
        self.assertTrue(any(s["entity"] == "Selasa" and s["type"] == "DAT" for s in sanitized))
        self.assertTrue(any(s["entity"] == "dua tahun" and s["type"] == "QTY" for s in sanitized))
        self.assertTrue(any(s["entity"] == "Asia Tenggara" and s["type"] == "LOC" for s in sanitized))
        self.assertTrue(any(s["entity"] == "PT Telkom" and s["type"] == "ORG" for s in sanitized))
        self.assertTrue(any(s["entity"] == "12 , 5 %" and s["type"] == "PRC" for s in sanitized))
        self.assertTrue(any(s["entity"] == "ke - 4" and s["type"] == "ORD" for s in sanitized))
        self.assertTrue(any(s["entity"] == "Rp 350 . 000" and s["type"] == "MON" for s in sanitized))
        self.assertTrue(any(s["entity"] == "500 kilometer" and s["type"] == "QTY" for s in sanitized))
        self.assertTrue(any(s["entity"] == "08 . 00 WIB" and s["type"] == "TIM" for s in sanitized))
        self.assertTrue(any(s["entity"] == "Laskar Pelangi" and s["type"] == "WOA" for s in sanitized))
        self.assertTrue(any(s["entity"] == "bahasa Arab" and s["type"] == "LAN" for s in sanitized))

        # Check dropped terms
        self.assertFalse(any(s["entity"] == "Bapak" for s in sanitized))
        self.assertFalse(any(s["entity"] == "Islam" for s in sanitized))
        self.assertFalse(any(s["entity"] == "umat Islam" for s in sanitized))
        self.assertFalse(any(s["entity"] == "NonExistentEntity" for s in sanitized))

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
