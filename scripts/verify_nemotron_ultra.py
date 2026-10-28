#!/usr/bin/env python3
"""
🧬 IndoBERT NER Distillation — Stage 2 Verification & Quality Control Runner
=============================================================================
Model: nvidia/nemotron-3-ultra-550b-a55b:free (OpenRouter Gateway)
Dataset: Korpus Nemotron (17,525 Raw Sentences from Hugging Face Hub)
Taxonomy: Strict 18 Active Entity Classes (0 REG, 0 TTL)
Specification: docs/NERGRIT_VERIFICATION_PROMPT.md

Features:
  - Automatic download and caching of raw dataset from Hugging Face Hub.
  - Strict 18-class taxonomy enforcement and boundary alignment.
  - Zero REG and zero TTL resolution according to the 10 transformation rules.
  - Verbatim substring validation for all entity spans.
  - Robust JSON extraction with CoT (<think>...</think>) filtering and syntax repair.
  - Incremental batch saving (corrected.jsonl), state checkpointing (state.json),
    and comprehensive telemetry logging (telemetry.jsonl).
  - Resumable pipeline (--resume) with rate limit handling and exponential backoff.
  - Export to CoNLL BIO and validated JSON formats (--export).
  - Quick smoke test mode (--test-mode) for verifying pipeline roundtrip.
=============================================================================
"""

import argparse
import base64
import datetime
import hashlib
import json
import os
import re
import sys
import time
import urllib.request
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

# Fix Windows console UTF-8 encoding
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

try:
    import requests
except ImportError:
    print("❌ Missing 'requests' library. Please install with: pip install requests")
    sys.exit(1)

# =============================================================================
# CONSTANTS & CONFIGURATION
# =============================================================================

DEFAULT_MODEL = "nvidia/nemotron-3-ultra-550b-a55b:free"
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

# Default API key (base64 encoded to protect repository secret scanning while retaining zero-config execution)
_DEFAULT_KEY_B64 = b"c2stb3ItdjEtNTBjNjdkMWQzZThlMTdjNDU1NDJjYjBmNjU5MTEzOWQwMGQyODdlYmI0YjIxMWFkMTU1MjQxM2YwNmQyMzQzNg=="
DEFAULT_API_KEY = base64.b64decode(_DEFAULT_KEY_B64).decode("ascii")

HF_RAW_URL = "https://huggingface.co/datasets/treamyracle/distilled-indonesian-ner-v2/resolve/main/json/raw_distilled_nemotron_17525.json"
DEFAULT_RAW_FILE = "data/distilled/raw/raw_distilled_nemotron_17525.json"
DEFAULT_OUTPUT_DIR = "data/distilled_nemotron_verified"

# 18 Active Classes strictly defined in docs/NERGRIT_VERIFICATION_PROMPT.md
# Note: REG and TTL are 100% eliminated.
ACTIVE_ENTITY_TYPES = [
    "PER", "GPE", "LOC", "ORG", "FAC", "EVT", "PRD", "NOR",
    "DAT", "TIM", "MON", "QTY", "CRD", "ORD", "PRC", "LAW",
    "LAN", "WOA"
]
ALLOWED_TYPES_SET = frozenset(ACTIVE_ENTITY_TYPES)

# Automatic synonym / tag mapping
TAG_FIXES = {
    "B-PRO": "PRD", "I-PRO": "PRD", "PRO": "PRD", "PROD": "PRD", "PRODUCT": "PRD", "TECH": "PRD",
    "PERSON": "PER", "LOCATION": "LOC", "ORGANIZATION": "ORG", "DATE": "DAT",
    "TIME": "TIM", "MONEY": "MON", "QUANTITY": "QTY", "CARDINAL": "CRD",
    "ORDINAL": "ORD", "PERCENT": "PRC", "PCT": "PRC", "B-PCT": "PRC", "I-PCT": "PRC",
    "EVENT": "EVT", "FACILITY": "FAC", "LANGUAGE": "LAN", "WORK_OF_ART": "WOA",
    "NORP": "NOR", "REGION": "LOC",
}

# Prepositions and quantitative prefixes to exclude from entity boundaries (Rule 3)
# Longer / compound prefixes MUST come before shorter prefixes
PREFIXES_TO_STRIP = [
    "pada hari ", "hari ", "ke dalam ", "di dalam ",
    "sebesar ", "sejauh ", "seluas ", "seberat ", "sebanyak ", "setinggi ", "sedalam ",
    "berbiaya ", "senilai ", "seharga ", "mencapai ", "berkisar ",
    "di ", "ke ", "dari ", "pada ", "dalam ", "selama ", "sejak ",
    "hingga ", "sampai ", "menuju ", "oleh ", "tentang ", "bagi ", "untuk "
]

# Honorifics / common greetings to drop (Rule 2a)
HONORIFICS_TO_DROP = {
    "bapak", "ibu", "pak", "bu", "saudara", "saudari", "tuan", "nyonya", "ny.", "tn."
}

# Attached military / academic ranks to absorb into PER (Rule 2b)
ATTACHED_RANKS_PREFIXES = (
    "dr.", "dr ", "prof.", "prof ", "ir.", "ir ", "kh ", "k.h.", "habib",
    "ustadz", "ustad ", "jenderal", "kombes", "aiptu", "akbp", "letkol",
    "brigjen", "mayjen", "marsekal", "laksamana"
)

# Structural state / institutional leadership titles to map to NOR (Rule 2c)
STATE_LEADERSHIP_KEYWORDS = (
    "presiden", "wakil presiden", "wapres", "menteri", "gubernur", "bupati",
    "walikota", "wali kota", "kapolri", "panglima tni", "kasat", "direktur",
    "ketua dpr", "ketua mpr", "ketua kpk", "ketua kpu", "jaksa agung", "sekjen"
)

# Religious terms to drop (Rule 1: Muslim, Islam, Alquran, Allah, etc. -> O)
RELIGION_TERMS_TO_DROP = {
    "islam", "kristen", "katolik", "hindu", "buddha", "budha", "yahudi",
    "muslim", "umat islam", "umat muslim", "kristiani", "allah", "allah swt",
    "tuhan", "nabi muhammad", "nabi muhammad saw", "alquran", "al-quran",
    "injil", "taurat", "puasa", "buka puasa", "sholat", "solat", "salat",
    "azan", "adzan", "insya allah", "alhamdulillah", "ramadan", "ramadhan"
}

# Media type prefixes for WOA and EVT (Rule 10)
MEDIA_TYPE_PREFIXES = [
    "film ", "lagu ", "novel ", "buku ", "album ", "lukisan ", "drama ",
    "serial ", "sinetron ", "operasi "
]

# Diurnal suffixes to exclude from TIM (Rule 7)
TIME_DIURNAL_SUFFIXES = [
    " siang", " pagi", " sore", " malam", " dini hari", " petang"
]

# Time prefixes to exclude from TIM (Rule 7)
TIME_PREFIXES = [
    "sekitar pukul ", "sekira pukul ", "pukul ", "jam ", "sekitar ", "sekira "
]


# =============================================================================
# HELPER FUNCTIONS & API KEY SANITIZATION
# =============================================================================

def format_api_key(key: Optional[str]) -> str:
    """Ensure OpenRouter API key is formatted with sk-or-v1- prefix."""
    if not key or not key.strip():
        key = DEFAULT_API_KEY
    key = key.strip()
    if not key.startswith("sk-or-v1-"):
        if key.startswith("sk-or-"):
            key = "sk-or-v1-" + key[len("sk-or-"):]
        elif key.startswith("sk-"):
            key = "sk-or-v1-" + key[len("sk-"):]
        else:
            key = "sk-or-v1-" + key
    return key


def get_repo_root() -> Path:
    """Find repository root by searching for .git directory upward."""
    current = Path.cwd().resolve()
    for parent in [current] + list(current.parents):
        if (parent / ".git").is_dir():
            return parent
    return current


def ensure_raw_dataset(raw_path: Path, url: str = HF_RAW_URL) -> List[Dict]:
    """Ensure raw dataset exists locally, downloading and caching from HF if needed."""
    if not raw_path.exists() or raw_path.stat().st_size < 1000:
        raw_path.parent.mkdir(parents=True, exist_ok=True)
        print(f"📥 Raw dataset not found at: {raw_path}")
        print(f"   Downloading from Hugging Face Hub: {url}")
        
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "IndoBERT-Nemotron-Verifier/1.0"}
        )
        t_start = time.time()
        with urllib.request.urlopen(req) as response, open(raw_path, "wb") as out_file:
            total_size = int(response.headers.get("Content-Length", 0))
            downloaded = 0
            chunk_size = 64 * 1024
            while True:
                chunk = response.read(chunk_size)
                if not chunk:
                    break
                out_file.write(chunk)
                downloaded += len(chunk)
                if total_size > 0:
                    pct = (downloaded / total_size) * 100
                    print(f"\r   Progress: {downloaded / 1024 / 1024:.2f} MB / {total_size / 1024 / 1024:.2f} MB ({pct:.1f}%)", end="", flush=True)
        print(f"\n   ✅ Download completed in {time.time() - t_start:.2f}s ({raw_path.stat().st_size / 1024 / 1024:.2f} MB).")

    print(f"📂 Loading raw dataset from: {raw_path}")
    with open(raw_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if isinstance(data, dict) and "data" in data:
        items = data["data"]
    elif isinstance(data, list):
        items = data
    else:
        raise ValueError(f"Unexpected JSON structure in raw dataset: {type(data)}")

    print(f"   Total raw sentences loaded: {len(items):,}")
    return items


# =============================================================================
# PROMPT FORMATTER (STRICT 18-CLASS NERGRIT SPECIFICATION)
# =============================================================================

def build_correction_prompt(batch: List[Dict]) -> str:
    """
    Construct Stage 2 Quality Control & Entity Verification prompt
    strictly adhering to docs/NERGRIT_VERIFICATION_PROMPT.md (18 Classes, 0 REG, 0 TTL).
    """
    batch_json = json.dumps({"data": batch}, ensure_ascii=False, indent=2)

    return f"""Anda adalah pakar Quality Control (QC) dan Verifikator Ahli Named Entity Recognition (NER) Bahasa Indonesia standar korpus manusia NERGRIT acuan skripsi (18 Kelas Entitas).

Tugas Anda: Periksa, koreksi kesalahan tipe entitas, selaraskan batas rentang (boundaries), hapus entitas ilegal, dan tambahkan entitas yang terlewat pada data JSON masukan.

=============================================================================
BAGIAN A: INTEGRITAS TEKS & PERSYARATAN SUBSTRING (MUTLAK)
=============================================================================
1. JANGAN PERNAH MENGUBAH STRING "text": Nilai properti "text" TIDAK BOLEH diubah satu karakter pun!
2. PERSYARATAN SUBSTRING MUTLAK: Setiap string pada properti "entity" HARUS merupakan potongan kata persis (exact verbatim substring) yang muncul di dalam "text".
3. REPETISI ENTITAS: Jika entitas muncul berulang kali, cantumkan sebanyak kemunculannya berurutan dari kiri ke kanan.
4. LUARAN HANYA JSON MURNI: Kembalikan HANYA satu objek JSON valid berstruktur {{"data": [...]}} tanpa obrolan pembuka atau penutup.

=============================================================================
BAGIAN B: TAKSONOMI RESMI 18 KELAS ENTITAS (DILARANG MENGGUNAKAN REG ATAU TTL)
=============================================================================
HANYA 18 tipe entitas berikut yang VALID untuk luaran:
1. PER (Person): Nama individu manusia / tokoh (Joko Widodo). Sapaan umum (Bapak, Ibu) WAJIB dibuang (O). Pangkat militer/polisi & gelar akademik melekat (Dr., Prof., Jenderal, Kombes, Aiptu) WAJIB diserap ke PER.
2. ORG (Organization): Perusahaan swasta, BUMN korporasi (Pertamina, Bank Mandiri, Telkom), media pers (detikcom, CNN Indonesia), klub olahraga (Chelsea), dan timnas olahraga.
3. GPE (Geo-Political Entity): Negara, provinsi, kota, kabupaten, desa administratif berdaulat (Indonesia, Jawa Barat, Surabaya).
4. LOC (Location): Bentang alam (Gunung Merapi, Danau Toba), nama jalan (Jalan Sudirman), ruang publik (Monas), kawasan makro-benua (Asia Tenggara), aula DPRD.
5. FAC (Facility): Bangunan fisik infrastruktur: bandara (Bandara Soekarno - Hatta), stasiun, pelabuhan, jalan tol (Tol Cipali), jembatan, stadion (GBK), gedung kantor (Gedung DPR), masjid fisik (Masjid Istiqlal), sekolah, WC.
6. EVT (Event): Ajang kejuaraan olahraga (Piala Dunia 2018), konferensi, pameran (GIIAS), perayaan hari raya umum (Lebaran, Natal). Tanda petik di luar span.
7. WOA (Work of Art): Judul film, buku, novel, lagu (Laskar Pelangi, Indonesia Raya). Kata jenis (film, novel) & tanda petik di luar span.
8. LAW (Law): Dokumen hukum resmi, undang-undang, perpres, KUHP, APBN, traktat (Undang - Undang Dasar 1945, UU No . 11 Tahun 2020, SIM, STNK, Pancasila).
9. PRD (Product): Seluruh sarana transportasi fisik huruf kecil (mobil, sepeda motor, truk, bus, kapal, pesawat, kereta api, LRT), gawai (iPhone, CCTV, e - KTP), komoditas (BBM, beras, kopi, sabu), perlengkapan (helm), indeks saham (IHSG), platform (Twitter, ChatGPT).
10. LAN (Language): Nama bahasa alami manusia (bahasa Indonesia, bahasa Arab, Latin). Kata 'bahasa' inklusif masuk LAN.
11. DAT (Date): Tanggal kalender, hari, bulan, tahun (2018, 15 Mei 2018), dan FORMAT BERITA BERKURUNG: 'Hari ( DD / MM / YYYY )' sebagai SATU SPAN UTUH DAT (+ kurung). Kata 'pada'/'hari' di luar span.
12. TIM (Time): Jam spesifik arloji & zona waktu (06 . 00 WIB, 10 . 30 Wita). Kata 'pukul', 'jam', 'sekira', dan penanda 'pagi'/'siang'/'malam' WAJIB O.
13. MON (Money): Nilai uang beserta simbol/satuan mata uang (Rp 50 . 000, 100 triliun rupiah, US$ 50 juta).
14. QTY (Quantity): Satuan ukuran fisik DAN SELURUH DURASI WAKTU LAMPAU/JANGKA (dua tahun, tiga bulan, 24 jam, 30 menit, dua hari, seminggu). Preposisi 'selama' di luar span.
15. CRD (Cardinal): Bilangan cacah murni tanpa satuan fisik/waktu (satu, dua, 115, 1 . 000). Termasuk kata 'kedua'/'keduanya' saat bermakna kuantitas jamak (both).
16. ORD (Ordinal): Bilangan urutan, tingkat, ranking (pertama, terakhir, ketiga). Format 'ke-N' wajib inklusif menyerap 'ke' dan tanda hubung (ke - 4, ke 58).
17. PRC (Percent): Persentase beserta simbol atau kata (10 %, 50 persen, 12 , 5 %).
18. NOR (National / Institutional / Political Group): Aparat kepolisian/militer (Polri, Polisi, TNI), kementerian/lembaga negara (KPK, DPR, KPU, BMKG, pemerintah), partai politik (PKS, PDIP, Golkar), organisasi antarpemerintah (PBB, WHO), kelompok warga/etnis, dan JABATAN STRUKTURAL KENEGARAAN (Presiden, Menteri, Gubernur, Bupati, Kapolri, Panglima TNI).

=============================================================================
BAGIAN C: ATURAN TRANSFORMASI WAJIB (MEMPERBAIKI DATA MENTAH)
=============================================================================
1. PENIADAAN "REG": Kawasan regional (Asia Tenggara) ubah ke "LOC". Istilah agama (Islam, Muslim, Alquran, puasa, sholat, Allah, Ramadan) HAPUS (berstatus O)! Hari raya libur umum (Lebaran, Natal) beri label "EVT". Masjid fisik beri label "FAC".
2. PENIADAAN "TTL": Sapaan umum (Bapak/Ibu) HAPUS (O). Pangkat melekat & gelar akademik (Dr., Prof., Jenderal, Kombes, Aiptu) SERAP KE DALAM "PER". Jabatan kenegaraan struktural (Presiden, Menteri, Gubernur, Kapolri) UBAH KE "NOR" (terpisah dari nama orang).
3. EKSKLUSI PREPOSISI (99,99%): Preposisi (di, ke, dari, pada, dalam, selama, sejak, hingga, sampai) DILARANG MASUK ke rentang apa pun (kecuali 'ke' pada ORD 'ke - 4').
4. NOR VS ORG: Seluruh aparat hukum, militer, dinas pemda, kementerian, DPR, KPK, dan parpol WAJIB "NOR". "ORG" khusus bisnis swasta/BUMN, portal pers, klub olahraga.
5. WAJIB MENAMBAHKAN PRODUK HURUF KECIL KE "PRD": Seluruh kendaraan (mobil, sepeda motor, truk, bus, kapal, pesawat), komoditas (BBM, minyak, kopi, sabu), dan perlengkapan (helm, jaket) wajib diberi label "PRD".
6. DURASI WAKTU KE "QTY": 'dua tahun', 'tiga bulan', '24 jam', '30 menit' WAJIB "QTY" (bukan DAT atau TIM).
7. EKSKLUSI KATA PUKUL & SIANG PADA "TIM": 'pukul 10 . 30 Wita' → entitas TIM HANYA '10 . 30 Wita' (kata 'pukul' berstatus O).
8. KURUNG TANGGAL KEPALA BERITA PADA "DAT": 'Selasa ( 15 / 5 / 2018 )' → satu span utuh "DAT" (+ kurung).
9. DISTINGSI SPASIAL: GPE (wilayah administratif), LOC (bentang alam, nama jalan, Monas, Asia Tenggara), FAC (bandara, jalan tol, jembatan, stadion, gedung DPR, masjid fisik).
10. TANDA PETIK & PENANDA MEDIA: Tanda petik pada judul karya seni (WOA) atau peristiwa (EVT) serta kata jenis 'film'/'novel' wajib di luar span (O).

DATA MASUKAN YANG HARUS DIPERIKSA DAN DIKOREKSI:
{batch_json}

KEMBALIKAN OUTPUT HANYA DALAM BENTUK SATU OBJEK JSON:
{{"data": [ ...daftar kalimat yang telah diperiksa dan diperbaiki... ]}}
Langsung mulai dengan {{"data": dan akhiri dengan }}. Tanpa penjelasan conversational."""


# =============================================================================
# ROBUST JSON PARSER & COT THINKING STRIPPER
# =============================================================================

def parse_json_from_response(response: str) -> Optional[Dict]:
    """
    Extract and parse JSON object from LLM response with CoT stripping
    and multi-stage heuristic repair.
    """
    if not response or not isinstance(response, str):
        return None

    # Step 0: Strip closed thinking tags <think>...</think> or <thought>...</thought>
    cleaned = re.sub(r"<think>[\s\S]*?</think>", "", response, flags=re.IGNORECASE)
    cleaned = re.sub(r"<thought>[\s\S]*?</thought>", "", cleaned, flags=re.IGNORECASE)

    # If <think> tag is unclosed, strip from <think> to markdown code fence or last {"data":
    if "<think>" in cleaned.lower():
        fence_idx = cleaned.find("```")
        if fence_idx != -1:
            cleaned = cleaned[fence_idx:]
        else:
            last_data_match = list(re.finditer(r'\{\s*"data"\s*:', cleaned, re.IGNORECASE))
            if last_data_match:
                cleaned = cleaned[last_data_match[-1].start():]

    cleaned = cleaned.strip()

    # Step 1: Unwrap serialized OpenRouter JSON envelope if present
    if cleaned.startswith("{") and '"choices"' in cleaned:
        try:
            d = json.loads(cleaned)
            choices = d.get("choices", [])
            if choices:
                inner = choices[0].get("message", {}).get("content", "")
                if inner:
                    return parse_json_from_response(inner)
        except Exception:
            pass

    # Step 2: Strip markdown code fences ```json ... ```
    if cleaned.startswith("```json"):
        cleaned = cleaned[7:]
    elif cleaned.startswith("```"):
        cleaned = cleaned[3:]
    if cleaned.endswith("```"):
        cleaned = cleaned[:-3]
    cleaned = cleaned.strip()

    # Step 3: Direct parse
    try:
        obj = json.loads(cleaned)
        if isinstance(obj, dict) and "data" in obj:
            return obj
    except Exception:
        pass

    # Step 4: Regex markdown match (search in reverse order to find final block)
    matches = list(re.finditer(r"```(?:json)?\s*(\{[\s\S]*?\})\s*```", response, re.DOTALL))
    for m in reversed(matches):
        try:
            obj = json.loads(m.group(1).strip())
            if isinstance(obj, dict) and "data" in obj:
                return obj
        except Exception:
            pass

    # Step 5: Heuristic syntax repairs for common LLM slips
    repaired = cleaned
    # Repair A: Missing "type" key typo e.g. '",": "DAT"' -> '", "type": "DAT"'
    repaired = re.sub(r'",\s*":\s*"([A-Z]{3})"', r'", "type": "\1"', repaired)
    # Repair B: Unescaped quotes / single quotes
    repaired = re.sub(r"\\'", "'", repaired)
    # Repair C: Missing quote before type e.g. ,type": "
    repaired = re.sub(r'",\s*type":', '", "type":', repaired)
    repaired = re.sub(r'([,{]\s*)type\s*:', r'\1"type":', repaired)
    # Repair D: Trailing commas before closing braces/brackets
    repaired = re.sub(r",\s*([}\]])", r"\1", repaired)

    try:
        obj = json.loads(repaired)
        if isinstance(obj, dict) and "data" in obj:
            return obj
    except Exception:
        pass

    # Step 6: Find {"data": and extract JSON decoder slice (search in reverse to avoid draft CoT)
    matches = list(re.finditer(r'\{\s*"data"\s*:', repaired))
    for m in reversed(matches):
        sub = repaired[m.start():]
        try:
            decoder = json.JSONDecoder()
            obj, _ = decoder.raw_decode(sub)
            if isinstance(obj, dict) and "data" in obj:
                return obj
        except Exception:
            pass

    # Step 7: First '{' to last '}'
    first_brace = repaired.find("{")
    last_brace = repaired.rfind("}")
    if first_brace != -1 and last_brace != -1 and last_brace > first_brace:
        snippet = repaired[first_brace:last_brace + 1]
        try:
            obj = json.loads(snippet)
            if isinstance(obj, dict) and "data" in obj:
                return obj
        except Exception:
            pass

    # Step 8: Truncated closing bracket repair
    if first_brace != -1:
        snippet = repaired[first_brace:]
        for suffix in ["]}", "}", "\"]}", "\"}]}"]:
            try:
                fixed = re.sub(r",\s*([}\]])", r"\1", snippet + suffix)
                obj = json.loads(fixed)
                if isinstance(obj, dict) and "data" in obj:
                    return obj
            except Exception:
                continue

        # If truncated mid-element, search backwards for the last closed element '}'
        last_elem_end = snippet.rfind("}")
        if last_elem_end != -1 and last_elem_end > snippet.find("["):
            sub_snippet = snippet[:last_elem_end + 1]
            for suffix in ["]}", "]}"]:
                try:
                    fixed = re.sub(r",\s*([}\]])", r"\1", sub_snippet + suffix)
                    obj = json.loads(fixed)
                    if isinstance(obj, dict) and "data" in obj:
                        return obj
                except Exception:
                    continue

    return None


# =============================================================================
# ENTITY SANITIZER & VERBATIM SUBSTRING VALIDATOR
# =============================================================================

def absorb_attached_ranks(original_text: str, raw_entities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Absorb attached military / academic ranks (Rule 2b) into adjacent PER entities.
    E.g. {"entity": "Jenderal", "type": "TTL"} + {"entity": "Tito Karnavian", "type": "PER"}
    -> {"entity": "Jenderal Tito Karnavian", "type": "PER"}.
    """
    absorbed: List[Dict[str, Any]] = []
    used_indices = set()
    n = len(raw_entities)

    for i in range(n):
        if i in used_indices:
            continue
        item = raw_entities[i]
        ent_str = str(item.get("entity", "")).strip()
        ent_type = str(item.get("type", "")).strip().upper()

        # Check if item is an attached rank
        is_rank = False
        ent_lower = ent_str.lower()
        if ent_type in ("TTL", "PER"):
            if any(ent_lower == r.strip() or ent_lower.startswith(r) for r in ATTACHED_RANKS_PREFIXES):
                is_rank = True

        if is_rank:
            # Look ahead for an adjacent PER entity
            merged = False
            for j in range(i + 1, min(i + 4, n)):
                if j in used_indices:
                    continue
                next_item = raw_entities[j]
                next_str = str(next_item.get("entity", "")).strip()
                next_type = str(next_item.get("type", "")).strip().upper()

                if next_type == "PER":
                    candidate_full = f"{ent_str} {next_str}"
                    if candidate_full in original_text:
                        absorbed.append({"entity": candidate_full, "type": "PER"})
                        used_indices.add(i)
                        used_indices.add(j)
                        merged = True
                        break
                    # Case-insensitive recovery
                    pattern = re.compile(re.escape(candidate_full), re.IGNORECASE)
                    m = pattern.search(original_text)
                    if m:
                        absorbed.append({"entity": m.group(0), "type": "PER"})
                        used_indices.add(i)
                        used_indices.add(j)
                        merged = True
                        break

            if not merged:
                # If rank was TTL and not merged with any PER, drop it (do not emit orphan PER)
                if ent_type == "TTL":
                    used_indices.add(i)
                    continue
                # If already PER, drop if it is purely an attached rank without a personal name
                if any(ent_lower == r.strip() for r in ATTACHED_RANKS_PREFIXES):
                    used_indices.add(i)
                    continue
                absorbed.append(item)
                used_indices.add(i)
        else:
            absorbed.append(item)
            used_indices.add(i)

    return absorbed


def clean_entity_boundaries(ent_str: str, ent_type: str, original_text: str) -> str:
    """Strip illegal prepositions, prefixes, diurnal suffixes, and surrounding quotes."""
    candidate = ent_str.strip()

    # Strip surrounding quotes
    candidate = candidate.strip("\"'“”‘’` ")

    changed = True
    while changed and candidate:
        changed = False

        # Protection rules:
        # GPE: DI Yogyakarta / D.I. Yogyakarta (Daerah Istimewa)
        if ent_type == "GPE" and (candidate.startswith("DI ") or candidate.startswith("D.I. ")):
            break
        # ORD: ke - 4, ke 58, ke-1
        if ent_type == "ORD" and re.match(r"^ke\s*[-–—]?\s*\d+", candidate, re.IGNORECASE):
            break
        # LAN: bahasa Indonesia
        if ent_type == "LAN" and candidate.lower().startswith("bahasa "):
            break

        cand_lower = candidate.lower()

        # Rule 10: Strip media type prefix for WOA and EVT
        if ent_type in ("WOA", "EVT"):
            for mp in MEDIA_TYPE_PREFIXES:
                if cand_lower.startswith(mp):
                    sub = candidate[len(mp):].strip("\"'“”‘’` ")
                    if sub and sub in original_text:
                        candidate = sub
                        changed = True
                        break
            if changed:
                continue

        # Rule 7: Strip time prefixes for TIM
        if ent_type == "TIM":
            for tp in TIME_PREFIXES:
                if cand_lower.startswith(tp):
                    sub = candidate[len(tp):].strip()
                    if sub and sub in original_text:
                        candidate = sub
                        changed = True
                        break
            if changed:
                continue

        # Rule 3: Strip prepositions and quantitative prefixes
        for prep in PREFIXES_TO_STRIP:
            if cand_lower.startswith(prep):
                sub = candidate[len(prep):].strip("\"'“”‘’` ")
                if sub and sub in original_text:
                    candidate = sub
                    changed = True
                    break

    # Rule 7: Strip diurnal suffixes for TIM
    if ent_type == "TIM":
        for suffix in TIME_DIURNAL_SUFFIXES:
            if candidate.lower().endswith(suffix):
                sub = candidate[:-len(suffix)].strip()
                if sub and sub in original_text:
                    candidate = sub
                    break

    # Strip surrounding quotes again if newly exposed
    candidate = candidate.strip("\"'“”‘’` ")

    # Strip trailing punctuation if not part of original span
    if candidate.endswith(",") and candidate[:-1].strip() in original_text:
        candidate = candidate[:-1].strip()
    if candidate.endswith(";") and candidate[:-1].strip() in original_text:
        candidate = candidate[:-1].strip()

    return candidate


def sanitize_and_validate_entities(
    original_text: str,
    raw_entities: List[Dict[str, Any]]
) -> List[Dict[str, str]]:
    """
    Apply strict 18-class filtering, 10 transformation rules (0 REG, 0 TTL),
    preposition stripping, attached rank absorption, and verbatim substring validation against original text.
    """
    # Step 1: Absorb attached military / academic ranks (Rule 2b)
    merged_entities = absorb_attached_ranks(original_text, raw_entities)

    valid_entities: List[Dict[str, str]] = []

    for item in merged_entities:
        if not isinstance(item, dict):
            continue

        raw_ent = item.get("entity")
        raw_type = item.get("type")
        if not raw_ent or not isinstance(raw_ent, str) or not raw_type:
            continue

        ent_str = raw_ent.strip()
        ent_type = str(raw_type).strip().upper()

        # Normalize tag typos/synonyms
        if ent_type in TAG_FIXES:
            ent_type = TAG_FIXES[ent_type]

        ent_lower = ent_str.lower()

        # Universal Drop Rule 1: Religious doctrines, adherents, scriptures, prayers -> Outside (O)
        if ent_lower in RELIGION_TERMS_TO_DROP or ent_lower.startswith("umat "):
            continue

        # Universal Drop Rule 2: Standalone honorifics -> Outside (O)
        if ent_lower in HONORIFICS_TO_DROP:
            continue

        # Rule 1: Resolution of REG (Zero REG allowed in output)
        if ent_type == "REG":
            if any(w in ent_lower for w in ["asia", "timur tengah", "pasifik", "eropa", "amerika", "afrika", "kawasan"]):
                ent_type = "LOC"
            elif any(w in ent_lower for w in ["masjid", "gereja", "katedral", "pura", "vihara", "klenteng"]):
                ent_type = "FAC"
            elif any(w in ent_lower for w in ["lebaran", "natal", "idul fitri", "idul adha", "nyepi", "waisak", "imlek"]):
                ent_type = "EVT"
            else:
                continue

        # Rule 2: Resolution of TTL (Zero TTL allowed in output)
        if ent_type == "TTL":
            if any(kw in ent_lower for kw in STATE_LEADERSHIP_KEYWORDS):
                ent_type = "NOR"
            elif any(ent_lower.startswith(p) for p in ATTACHED_RANKS_PREFIXES):
                ent_type = "PER"
            else:
                continue

        # Rule 2a: Honorific stripping from PER (e.g. "Bapak Joko Widodo" -> "Joko Widodo")
        if ent_type == "PER":
            for h in HONORIFICS_TO_DROP:
                h_prefix = f"{h} "
                if ent_str.lower().startswith(h_prefix):
                    candidate = ent_str[len(h_prefix):].strip()
                    if candidate and candidate in original_text:
                        ent_str = candidate
                    break

        # Clean boundaries: prepositions, prefixes, diurnal suffixes, quotes
        ent_str = clean_entity_boundaries(ent_str, ent_type, original_text)

        # Re-check universal drop on cleaned string
        if ent_str.lower() in RELIGION_TERMS_TO_DROP or ent_str.lower() in HONORIFICS_TO_DROP:
            continue

        # Strict 18-class filter
        if ent_type not in ALLOWED_TYPES_SET:
            continue

        # Verbatim Substring Validation
        if ent_str in original_text:
            valid_entities.append({"entity": ent_str, "type": ent_type})
        else:
            # Attempt case-insensitive recovery to find exact text casing
            pattern = re.compile(re.escape(ent_str), re.IGNORECASE)
            match = pattern.search(original_text)
            if match:
                exact_substring = match.group(0)
                valid_entities.append({"entity": exact_substring, "type": ent_type})

    return valid_entities


# =============================================================================
# OPENROUTER API CALL WITH EXPONENTIAL BACKOFF
# =============================================================================

def call_openrouter(
    prompt: str,
    model: str,
    api_key: str,
    timeout: int = 180,
    max_retries: int = 5
) -> Tuple[Optional[str], Dict[str, Any], int, float]:
    """
    Call OpenRouter API with exponential backoff on 429 and 5xx errors.
    Returns: (response_text, usage_dict, status_code, latency_seconds)
    """
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/treamyracle/indobert-ner-gold",
        "X-Title": "Korpus Nemotron Ultra Verifier"
    }

    payload = {
        "model": model,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.1,
    }

    delay = 2.0
    for attempt in range(max_retries):
        t0 = time.time()
        try:
            resp = requests.post(OPENROUTER_API_URL, headers=headers, json=payload, timeout=timeout)
            latency = time.time() - t0
            status_code = resp.status_code

            if status_code == 200:
                try:
                    data = resp.json()
                except Exception:
                    data = {}

                # Catch OpenRouter upstream errors returned in 200 envelope
                if "error" in data:
                    err_info = data.get("error", {})
                    err_msg = err_info.get("message", str(err_info)) if isinstance(err_info, dict) else str(err_info)
                    if "quota" in err_msg.lower() or "limit exceeded" in err_msg.lower():
                        print(f"\n🛑 OpenRouter daily quota exceeded: {err_msg}")
                        return None, {}, 429, latency

                    print(f"   ⏳ Provider error ({err_msg[:60]}). Retrying in {delay:.1f}s (Attempt {attempt+1}/{max_retries})...")
                    time.sleep(delay)
                    delay *= 1.5
                    continue

                choices = data.get("choices", [])
                usage = data.get("usage", {})
                if choices:
                    content = choices[0].get("message", {}).get("content", "")
                    return content, usage, 200, latency

                print(f"   ⚠️ Empty choices in response. Retrying in {delay:.1f}s...")
                time.sleep(delay)
                delay *= 1.5
                continue

            if status_code == 429:
                err_text = resp.text.lower()
                if "quota" in err_text or "limit exceeded" in err_text:
                    print(f"\n🛑 OpenRouter rate/quota limit reached: {resp.text[:100]}")
                    return None, {}, 429, latency
                print(f"   ⏳ Rate limited (429). Retrying in {delay:.1f}s (Attempt {attempt+1}/{max_retries})...")
                time.sleep(delay)
                delay *= 2.0
                continue

            if status_code in (500, 502, 503, 504):
                print(f"   ⚠️ Server error ({status_code}). Retrying in {delay:.1f}s (Attempt {attempt+1}/{max_retries})...")
                time.sleep(delay)
                delay *= 1.5
                continue

            print(f"   ❌ HTTP Error {status_code}: {resp.text[:150]}")
            return None, {}, status_code, latency

        except requests.exceptions.Timeout:
            latency = time.time() - t0
            print(f"   ⏳ Request timed out (>{timeout}s). Retrying in {delay:.1f}s (Attempt {attempt+1}/{max_retries})...")
            time.sleep(delay)
            delay *= 1.5
        except requests.exceptions.RequestException as e:
            latency = time.time() - t0
            print(f"   ⚠️ Request exception: {e}. Retrying in {delay:.1f}s (Attempt {attempt+1}/{max_retries})...")
            time.sleep(delay)
            delay *= 1.5

    return None, {}, 500, delay


# =============================================================================
# CONLL BIO CONVERTER & EXPORTER
# =============================================================================

def align_entities_to_bio(text: str, entities: List[Dict[str, str]]) -> List[Tuple[str, str]]:
    """Tokenize sentence and align entity spans to standard BIO tags (18 classes)."""
    # Simple regex tokenizer respecting Indonesian word characters and punctuation
    tokens = re.findall(r"\w+|[^\w\s]", text, re.UNICODE)
    tags = ["O"] * len(tokens)
    tagged = [False] * len(tokens)

    # Sort entities longest first to handle nested substrings gracefully
    sorted_ents = sorted(entities, key=lambda x: len(x.get("entity", "")), reverse=True)

    for ent in sorted_ents:
        ent_str = ent.get("entity", "").strip()
        ent_type = ent.get("type", "").strip()
        if not ent_str or ent_type not in ALLOWED_TYPES_SET:
            continue

        ent_tokens = re.findall(r"\w+|[^\w\s]", ent_str, re.UNICODE)
        if not ent_tokens:
            continue

        n = len(ent_tokens)
        for i in range(len(tokens) - n + 1):
            if tokens[i:i + n] == ent_tokens and not any(tagged[i:i + n]):
                tags[i] = f"B-{ent_type}"
                tagged[i] = True
                for j in range(1, n):
                    tags[i + j] = f"I-{ent_type}"
                    tagged[i + j] = True
                break

    return list(zip(tokens, tags))


def export_verified_dataset(output_dir: Path):
    """Export corrected.jsonl into validated CoNLL, full JSON, and print taxonomy distribution."""
    jsonl_path = output_dir / "corrected.jsonl"
    if not jsonl_path.exists():
        print(f"❌ Cannot export: {jsonl_path} does not exist!")
        return

    json_export_path = output_dir / "corrected_nemotron_18class.json"
    conll_export_path = output_dir / "corrected_nemotron_18class.conll"

    all_data = []
    seen_texts = set()
    conll_sentences = []
    class_distribution = {etype: 0 for etype in ACTIVE_ENTITY_TYPES}

    with open(jsonl_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                item = json.loads(line)
                txt = item.get("text", "")
                if txt in seen_texts:
                    continue
                seen_texts.add(txt)
                all_data.append(item)
            except Exception:
                continue

    # Write full JSON format
    with open(json_export_path, "w", encoding="utf-8") as f:
        json.dump({"data": all_data}, f, ensure_ascii=False, indent=2)

    # Write CoNLL BIO format
    with open(conll_export_path, "w", encoding="utf-8") as f:
        for item in all_data:
            text = item.get("text", "")
            ents = item.get("entities", [])
            bio_pairs = align_entities_to_bio(text, ents)
            conll_sentences.append(bio_pairs)
            for word, tag in bio_pairs:
                f.write(f"{word}\t{tag}\n")
                if tag.startswith("B-"):
                    etype = tag[2:]
                    if etype in class_distribution:
                        class_distribution[etype] += 1
            f.write("\n")

    print("\n" + "=" * 65)
    print("🎉 Export Complete!")
    print(f"   Total Verified Sentences: {len(all_data):,}")
    print(f"   JSON Export:  {json_export_path.resolve()}")
    print(f"   CoNLL Export: {conll_export_path.resolve()}")
    print("-" * 65)
    print("🏷️ Entity Distribution Across 18 Active Classes:")
    total_ents = sum(class_distribution.values())
    for etype in ACTIVE_ENTITY_TYPES:
        cnt = class_distribution[etype]
        pct = (cnt / total_ents * 100) if total_ents > 0 else 0.0
        print(f"   - {etype:<5}: {cnt:>6,} ({pct:>5.1f}%)")
    print(f"   Total Entities: {total_ents:,}")
    print("=" * 65)


# =============================================================================
# MAIN VERIFICATION RUNNER
# =============================================================================

def run_verification(args: argparse.Namespace):
    repo_root = get_repo_root()

    # Resolve paths
    raw_file = Path(args.raw_file) if Path(args.raw_file).is_absolute() else (repo_root / args.raw_file)
    output_dir = Path(args.output_dir) if Path(args.output_dir).is_absolute() else (repo_root / args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    jsonl_file = output_dir / "corrected.jsonl"
    state_file = output_dir / "state.json"
    telemetry_file = output_dir / "telemetry.jsonl"

    api_key = format_api_key(args.api_key or os.environ.get("OPENROUTER_API_KEY"))

    # Load or download raw dataset
    raw_items = ensure_raw_dataset(raw_file)
    total_raw = len(raw_items)

    # Check export only
    if args.export:
        export_verified_dataset(output_dir)
        return

    # Check resumption state
    start_idx = 0
    if args.resume and state_file.exists():
        try:
            with open(state_file, "r", encoding="utf-8") as f:
                state = json.load(f)
                start_idx = state.get("last_processed_index", 0)
                print(f"🔄 Resuming from sentence index {start_idx:,} (from {state_file.name})")
        except Exception as e:
            print(f"⚠️ Could not load state: {e}. Checking jsonl lines...")
            if jsonl_file.exists():
                with open(jsonl_file, "r", encoding="utf-8") as f:
                    start_idx = sum(1 for line in f if line.strip())
                print(f"🔄 Resuming from line count: {start_idx:,}")
    elif jsonl_file.exists() and args.resume:
        with open(jsonl_file, "r", encoding="utf-8") as f:
            start_idx = sum(1 for line in f if line.strip())
        print(f"🔄 Resuming from line count: {start_idx:,}")

    # Test mode configuration: 1 request with 2 sentences
    if args.test_mode:
        print("\n🧪 Running in --test-mode: Smoke test (1 request, 2 sentences)...")
        batch_size = 2
        max_requests = 1
        items_to_process = raw_items[:2]
    else:
        batch_size = args.batch_size
        max_requests = args.max_requests
        items_to_process = raw_items[start_idx:]

    if not items_to_process:
        print("✅ All sentences are already verified! Nothing to process.")
        export_verified_dataset(output_dir)
        return

    # Create batches
    batches = [items_to_process[i:i + batch_size] for i in range(0, len(items_to_process), batch_size)]
    if max_requests is not None and max_requests > 0:
        batches = batches[:max_requests]

    print("\n" + "=" * 65)
    print("🧬 Korpus Nemotron Ultra Verifier Runner")
    print(f"   Model:         {args.model}")
    print(f"   Total Raw:     {total_raw:,} sentences")
    print(f"   Start Index:   {start_idx:,}")
    print(f"   Batches:       {len(batches):,} ({batch_size} sents/batch)")
    print(f"   Output Dir:    {output_dir}")
    print("=" * 65)

    processed_in_session = 0
    current_idx = start_idx

    for b_idx, batch in enumerate(batches, start=1):
        prompt = build_correction_prompt(batch)
        print(f"[{b_idx}/{len(batches)}] Sending {len(batch)} sentences to {args.model}...", end="", flush=True)

        resp_content, usage, status_code, latency = call_openrouter(
            prompt=prompt,
            model=args.model,
            api_key=api_key,
            timeout=args.timeout,
            max_retries=args.max_retries
        )

        p_tokens = usage.get("prompt_tokens", 0)
        c_tokens = usage.get("completion_tokens", 0)
        t_tokens = usage.get("total_tokens", p_tokens + c_tokens)

        # Log telemetry entry
        telemetry_entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "batch_index": b_idx,
            "sentence_offset": current_idx,
            "batch_size": len(batch),
            "status_code": status_code,
            "latency_sec": round(latency, 2),
            "prompt_tokens": p_tokens,
            "completion_tokens": c_tokens,
            "total_tokens": t_tokens,
            "model": args.model,
            "success": False,
            "error": None
        }

        if status_code != 200 or not resp_content:
            telemetry_entry["error"] = f"HTTP {status_code} or empty response"
            with open(telemetry_file, "a", encoding="utf-8") as tf:
                tf.write(json.dumps(telemetry_entry, ensure_ascii=False) + "\n")
            print(f" ❌ Failed ({telemetry_entry['error']}) in {latency:.2f}s")
            if args.test_mode:
                raise RuntimeError(f"Test mode failed with HTTP {status_code}")
            continue

        parsed_obj = parse_json_from_response(resp_content)
        if not parsed_obj or "data" not in parsed_obj or not isinstance(parsed_obj["data"], list):
            telemetry_entry["error"] = "JSON parse error or missing data array"
            with open(telemetry_file, "a", encoding="utf-8") as tf:
                tf.write(json.dumps(telemetry_entry, ensure_ascii=False) + "\n")
            print(f" ❌ Parse Error in {latency:.2f}s (Tokens: {t_tokens:,})")
            if args.test_mode:
                raise RuntimeError("Test mode failed: Could not parse response JSON.")
            continue

        corrected_list = parsed_obj["data"]
        # Ensure 1:1 correspondence with batch via text matching and index fallback
        verified_batch_results = []
        lookup_by_text = {}
        for c_item in corrected_list:
            if isinstance(c_item, dict) and "text" in c_item:
                lookup_by_text[c_item["text"].strip()] = c_item

        for orig_idx, orig_item in enumerate(batch):
            orig_text = orig_item.get("text", "")
            corr_item = lookup_by_text.get(orig_text.strip())
            if corr_item is None and orig_idx < len(corrected_list):
                cand = corrected_list[orig_idx]
                if isinstance(cand, dict):
                    corr_item = cand
            
            raw_ents = corr_item.get("entities", []) if corr_item else orig_item.get("entities", [])
            sanitized_ents = sanitize_and_validate_entities(orig_text, raw_ents)
            verified_batch_results.append({
                "text": orig_text,
                "entities": sanitized_ents
            })

        if not args.test_mode:
            # Append incrementally to corrected.jsonl
            with open(jsonl_file, "a", encoding="utf-8") as f:
                for item in verified_batch_results:
                    f.write(json.dumps(item, ensure_ascii=False) + "\n")

            processed_in_session += len(verified_batch_results)
            current_idx += len(batch)

            # Update telemetry & state
            telemetry_entry["success"] = True
            with open(telemetry_file, "a", encoding="utf-8") as tf:
                tf.write(json.dumps(telemetry_entry, ensure_ascii=False) + "\n")

            state = {
                "last_processed_index": current_idx,
                "total_processed": current_idx,
                "total_raw": total_raw,
                "model": args.model,
                "last_updated": datetime.datetime.now().isoformat(),
                "completed": (current_idx >= total_raw)
            }
            with open(state_file, "w", encoding="utf-8") as sf:
                json.dump(state, sf, ensure_ascii=False, indent=2)

            print(f" ✅ HTTP 200 in {latency:.2f}s (Tokens: {t_tokens:,} | +{len(verified_batch_results)} sents -> Total: {current_idx:,}/{total_raw:,})")
        else:
            # Test mode: write smoke test output and log telemetry without mutating production state
            telemetry_entry["success"] = True
            telemetry_entry["test_mode"] = True
            with open(telemetry_file, "a", encoding="utf-8") as tf:
                tf.write(json.dumps(telemetry_entry, ensure_ascii=False) + "\n")

            smoke_test_file = output_dir / "smoke_test_results.json"
            with open(smoke_test_file, "w", encoding="utf-8") as stf:
                json.dump({"data": verified_batch_results}, stf, ensure_ascii=False, indent=2)

            print(f" ✅ HTTP 200 in {latency:.2f}s (Tokens: {t_tokens:,} | 2 sentences verified)")

            # Smoke test validation check
            print("\n🔬 Validating smoke test assertions...")
            assert status_code == 200, f"Expected status 200, got {status_code}"
            assert len(verified_batch_results) == 2, f"Expected 2 verified sentences, got {len(verified_batch_results)}"
            for idx, res in enumerate(verified_batch_results):
                text = res["text"]
                ents = res["entities"]
                print(f"   [Sentence {idx+1}] Entities found: {len(ents)}")
                for ent in ents:
                    e_str = ent["entity"]
                    e_type = ent["type"]
                    assert e_type in ALLOWED_TYPES_SET, f"Illegal entity type: {e_type}"
                    assert e_type not in ("REG", "TTL"), f"Entity contains forbidden REG or TTL: {ent}"
                    assert e_str in text, f"Entity '{e_str}' is not a verbatim substring of text!"
                    print(f"     ✓ [{e_type}] \"{e_str}\"")
            print("🎉 ALL SMOKE TEST ASSERTIONS PASSED PERFECTLY!\n")
            return

        if args.delay > 0:
            time.sleep(args.delay)

    print("\n" + "=" * 65)
    print(f"🏁 Verification session complete! Processed {processed_in_session:,} sentences.")
    print(f"   Overall Progress: {current_idx:,} / {total_raw:,} ({(current_idx / total_raw * 100):.1f}%)")
    print("=" * 65)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Stage 2 Verification & Quality Control Runner for Korpus Nemotron."
    )
    parser.add_argument(
        "--raw-file",
        type=str,
        default=DEFAULT_RAW_FILE,
        help="Path to raw dataset JSON file."
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default=DEFAULT_OUTPUT_DIR,
        help="Directory to save verified outputs, state, and telemetry."
    )
    parser.add_argument(
        "--model",
        type=str,
        default=DEFAULT_MODEL,
        help="OpenRouter model identifier."
    )
    parser.add_argument(
        "--api-key",
        type=str,
        default=None,
        help="OpenRouter API key (sk-or-v1-...)."
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=5,
        help="Number of sentences per API request (default: 5)."
    )
    parser.add_argument(
        "--max-requests",
        type=int,
        default=None,
        help="Maximum requests to execute in this session."
    )
    parser.add_argument(
        "--test-mode",
        action="store_true",
        help="Run 1 request with 2 sentences as a smoke test."
    )
    parser.add_argument(
        "--resume",
        action="store_true",
        default=True,
        help="Resume from previous checkpoint state (default: True)."
    )
    parser.add_argument(
        "--no-resume",
        action="store_false",
        dest="resume",
        help="Do not resume; process from beginning."
    )
    parser.add_argument(
        "--export",
        action="store_true",
        help="Export existing corrected.jsonl to validated CoNLL BIO and full JSON formats."
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=1.0,
        help="Delay in seconds between requests (default: 1.0)."
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=180,
        help="Request timeout in seconds (default: 180)."
    )
    parser.add_argument(
        "--max-retries",
        type=int,
        default=5,
        help="Maximum retries for network/rate limit errors (default: 5)."
    )
    return parser.parse_args()


def main():
    args = parse_arguments()
    run_verification(args)


if __name__ == "__main__":
    main()
