#!/usr/bin/env python3
"""
Independent Dual-Annotator Audit (18-Class NERGRIT Standard) + IAA Pipeline
===========================================================================
Annotator A1 : cx/gpt-6-luna             (9router, reasoning_effort="high")
Annotator A2 : ag/gemini-3.8-flash-high  (9router, high thinking effort)

Default Dataset Scope (Option A — 300 Stratified Samples):
  D01: nemotron  (data/distilled_nemotron_verified/corrected.jsonl)  -> 100 sents
  D02: luna      (data/distilled_luna_verified/corrected.jsonl)      -> 100 sents
  D03: gemma     (data/distilled_gemma_verified/corrected.jsonl)     -> 100 sents

Pipeline:
  1. Load verified 18-class datasets, align entities -> BIO tags using the exact
     Stage-2 tokenizer/alignment contract, deduplicate normalized texts, and draw
     a deterministic stratified sample (seed 20261022; 100 sentences/dataset).
  2. Each annotator audits every sample INDEPENDENTLY using the exact Stage-2
     18-class NERGRIT rules (0 REG, 0 TTL). Checkpoints are written per sample so
     runs can stop and resume safely at any time.
  3. Compute Inter-Annotator Agreement (Token BIO kappa, Token Class kappa,
     Entity-Decision kappa [3-class & binary], Pairwise Exact Span-F1, 95%
     bootstrap CIs), Dual-Agreement Consensus, dataset annotation quality P/R/F1,
     Horvitz-Thompson weighted sentence error rate, and export full report + ZIP.

Usage:
  python scripts/run_independent_audit_iaa.py                  # sample + annotate + compute
  python scripts/run_independent_audit_iaa.py --status         # show progress only
  python scripts/run_independent_audit_iaa.py --sample-only    # build manifest only
  python scripts/run_independent_audit_iaa.py --max-batches 1 --batch-size 2 --allow-partial  # smoke test
  python scripts/run_independent_audit_iaa.py --annotator A1   # run only Annotator A1
  python scripts/run_independent_audit_iaa.py --compute-only   # recompute IAA from checkpoints

Environment (.env or shell): NINEROUTER_BASE_URL, NINEROUTER_API_KEY
"""
from __future__ import annotations

import argparse
import concurrent.futures
import csv
import datetime
import hashlib
import json
import os
import random
import re
import sys
import threading
import time
import unicodedata
import zipfile
from collections import Counter, defaultdict
from pathlib import Path
from statistics import median
from typing import Any

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

try:
    import requests
except ImportError:
    print("Missing 'requests'. Install with: pip install requests")
    sys.exit(1)

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


# =============================================================================
# CONFIGURATION & CONSTANTS
# =============================================================================
ROOT = Path(__file__).resolve().parents[1]
SCHEMA_VERSION = 2
AUDIT_IAA_SEED = 20261022
SAMPLE_SIZE = 100
DEFAULT_DATASETS = ("nemotron", "luna", "gemma")

VERIFIED_DATASET_PATHS = {
    "nemotron": Path("data/distilled_nemotron_verified/corrected.jsonl"),
    "luna": Path("data/distilled_luna_verified/corrected.jsonl"),
    "gemma": Path("data/distilled_gemma_verified/corrected.jsonl"),
}

DEFAULT_OUT_DIR = ROOT / "audit_iaa_18class"
LEGACY_AUDIT_MANIFEST = ROOT / "audit_iaa" / "audit_sample_manifest.json"

ANNOTATORS: dict[str, dict[str, Any]] = {
    "A1": {"model": "cx/gpt-6-luna", "reasoning_effort": "high"},
    "A2": {"model": "ag/gemini-3.8-flash-high", "reasoning_effort": "high"},
}

NINEROUTER_BASE_URL = os.environ.get("NINEROUTER_BASE_URL", "http://localhost:20128/v1").rstrip("/")
NINEROUTER_API_KEY = os.environ.get("NINEROUTER_API_KEY", "sk-11c534e8cfebe28d-nmcu15-b59f004b")
CHAT_URL = f"{NINEROUTER_BASE_URL}/chat/completions"

BOOTSTRAP_ITERATIONS = 1000
BOOTSTRAP_SEED = 20261022

ACTIVE_TYPES = tuple(sorted((
    "PER", "GPE", "LOC", "ORG", "FAC", "EVT", "PRD", "NOR",
    "DAT", "TIM", "MON", "QTY", "CRD", "ORD", "PRC", "LAW",
    "LAN", "WOA",
)))
ACTIVE_SET = frozenset(ACTIVE_TYPES)
DROPPED_TYPES = frozenset({"TTL", "REG"})

TAG_ALIASES = {
    "PRO": "PRD", "PROD": "PRD", "PRODUCT": "PRD", "TECH": "PRD",
    "PERSON": "PER", "LOCATION": "LOC", "ORGANIZATION": "ORG", "DATE": "DAT",
    "TIME": "TIM", "MONEY": "MON", "QUANTITY": "QTY", "CARDINAL": "CRD",
    "ORDINAL": "ORD", "PERCENT": "PRC", "PCT": "PRC", "EVENT": "EVT",
    "FACILITY": "FAC", "LANGUAGE": "LAN", "WORK_OF_ART": "WOA", "NORP": "NOR",
    "REGION": "LOC",
}
GOLD_EXTRA_ALIASES = {"O\u201a\u00c4\u00e9": "O", "O -": "O"}
WORD_PATTERN = re.compile(r"\w+|[^\s\w]", flags=re.UNICODE)
TOKEN_PATTERN = re.compile(r"\w+|[^\w\s]", flags=re.UNICODE)

PRINT_LOCK = threading.Lock()


def log(message: str) -> None:
    with PRINT_LOCK:
        print(message, flush=True)


def stable_hash(obj: Any) -> str:
    payload = json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def file_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.replace(tmp, path)


def write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = list(dict.fromkeys(key for row in rows for key in row))
    with path.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


# =============================================================================
# 1. CORPUS LOADER, ALIGNMENT & STRATIFIED SAMPLER
# =============================================================================
def align_entities_to_bio(text: str, entities: list[dict[str, Any]]) -> list[tuple[str, str]]:
    """Tokenize sentence and align verified entity spans to 18-class BIO tags."""
    tokens = TOKEN_PATTERN.findall(text)
    tags = ["O"] * len(tokens)
    tagged = [False] * len(tokens)
    sorted_ents = sorted(entities, key=lambda x: len(str(x.get("entity", ""))), reverse=True)
    for ent in sorted_ents:
        ent_str = str(ent.get("entity", "")).strip()
        ent_type = TAG_ALIASES.get(str(ent.get("type", "")).strip().upper(), str(ent.get("type", "")).strip().upper())
        if not ent_str or ent_type not in ACTIVE_SET:
            continue
        ent_tokens = TOKEN_PATTERN.findall(ent_str)
        if not ent_tokens:
            continue
        width = len(ent_tokens)
        for i in range(len(tokens) - width + 1):
            if tokens[i:i + width] == ent_tokens and not any(tagged[i:i + width]):
                tags[i] = f"B-{ent_type}"
                tagged[i] = True
                for j in range(1, width):
                    tags[i + j] = f"I-{ent_type}"
                    tagged[i + j] = True
                break
    return list(zip(tokens, tags))


def entity_spans(tags: list[str]) -> list[tuple[int, int, str]]:
    """Extract zero-based, end-exclusive (start, end, label) spans from BIO tags."""
    spans: list[tuple[int, int, str]] = []
    start, kind = None, None
    for index, tag in enumerate(list(tags) + ["O"]):
        if tag == "O":
            prefix, current = "O", None
        elif isinstance(tag, str) and re.fullmatch(r"[BI]-.+", tag):
            prefix, current = tag.split("-", 1)
        else:
            raise ValueError(f"Invalid BIO tag at token {index}: {tag!r}")
        if start is not None and (prefix != "I" or current != kind):
            spans.append((start, index, kind))
            start, kind = None, None
        if prefix != "O" and start is None:
            start, kind = index, current
    return spans


def normalized_text(record: dict) -> str:
    text = unicodedata.normalize("NFKC", " ".join(record["tokens"]))
    return " ".join(WORD_PATTERN.findall(text)).casefold()


def _load_gold_records() -> tuple[list[dict], dict[str, str]]:
    """Load 18-class NERGRIT Gold (train/valid/test) from bundle archive or local data/."""
    bundle_candidates = [
        ROOT / "notebooks" / "nemotron_18class_colab_bundle.zip",
        ROOT / "notebooks" / "bab4_source_bundle.zip",
        Path(r"C:\Users\tream\OneDrive\Documents\SKRIPSI\skripsi\notebooks\bab4_source_bundle.zip"),
    ]
    raw_files: dict[str, str] = {}
    hashes: dict[str, str] = {}

    for bpath in bundle_candidates:
        if bpath.is_file():
            with zipfile.ZipFile(bpath, "r") as zf:
                names = set(zf.namelist())
                prefix = "gold/" if "gold/train.txt" in names else "data/"
                if f"{prefix}train.txt" in names:
                    for key_name in ("train.txt", "valid.txt", "test.txt", "labels-map.csv"):
                        raw_bytes = zf.read(f"{prefix}{key_name}")
                        raw_files[key_name] = raw_bytes.decode("utf-8-sig")
                        hashes[f"gold/{key_name}"] = hashlib.sha256(raw_bytes).hexdigest()
                    break

    if not raw_files:
        raise FileNotFoundError("Could not find Gold CoNLL files in notebook bundles.")

    aliases = dict(GOLD_EXTRA_ALIASES)
    for line in raw_files["labels-map.csv"].splitlines():
        if line.strip():
            left, right = line.split()
            aliases[left] = right

    records: list[dict] = []
    for split_name, fname in (("train", "train.txt"), ("validation", "valid.txt"), ("test", "test.txt")):
        tok_buf, tag_buf, sent_idx = [], [], 0
        for line in raw_files[fname].splitlines() + [""]:
            if not line.strip():
                if tok_buf:
                    orig_tags = []
                    for raw_tag in tag_buf:
                        norm = aliases.get(raw_tag, raw_tag).strip().upper()
                        if norm != "O" and "-" in norm:
                            p, k = norm.split("-", 1)
                            norm = f"{p}-{TAG_ALIASES.get(k, k)}"
                        orig_tags.append(norm)
                    tags = ["O" if t != "O" and t[2:] in DROPPED_TYPES else t for t in orig_tags]
                    sid = "gold-" + stable_hash({"source": f"data/{fname}#{sent_idx}", "tokens": tok_buf, "tags": tag_buf})[:20]
                    records.append({
                        "sentence_id": sid,
                        "dataset": "gold",
                        "source_split": split_name,
                        "tokens": list(tok_buf),
                        "original_tags": orig_tags,
                        "tags": tags,
                    })
                    sent_idx += 1
                    tok_buf, tag_buf = [], []
                continue
            parts = line.rstrip().rsplit("\t", 1) if "\t" in line.rstrip() else line.rstrip().rsplit(None, 1)
            if len(parts) != 2:
                raise ValueError(f"Malformed CoNLL row in gold/{fname}: {line!r}")
            tok_buf.append(parts[0])
            tag_buf.append(parts[1])
    return records, hashes


def _load_verified_jsonl(dataset: str) -> tuple[list[dict], dict[str, str]]:
    if dataset == "gold":
        return _load_gold_records()
    rel = VERIFIED_DATASET_PATHS.get(dataset)
    if rel is None:
        raise ValueError(f"Unknown dataset {dataset!r}. Supported: {sorted((*VERIFIED_DATASET_PATHS, 'gold'))}")
    path = ROOT / rel
    if not path.is_file():
        raise FileNotFoundError(f"Verified dataset not found: {path}")

    records: list[dict] = []
    for idx, line in enumerate(path.read_text(encoding="utf-8").splitlines()):
        if not line.strip():
            continue
        item = json.loads(line)
        text = item.get("text", "")
        ents = item.get("entities", [])
        for ent in ents:
            etype = str(ent.get("type", "")).strip().upper()
            if etype in DROPPED_TYPES:
                raise ValueError(f"{dataset}#{idx}: forbidden class {etype} in verified dataset")
        pairs = align_entities_to_bio(text, ents)
        if not pairs:
            raise ValueError(f"{dataset}#{idx}: empty token list after alignment")
        toks = [w for w, _ in pairs]
        tags = [t for _, t in pairs]
        sid = f"{dataset}-" + stable_hash({"source": f"{rel.as_posix()}#{idx}", "tokens": toks, "tags": tags})[:20]
        records.append({
            "sentence_id": sid,
            "dataset": dataset,
            "source_split": "verified_18class",
            "tokens": toks,
            "original_tags": list(tags),
            "tags": tags,
        })
    return records, {rel.as_posix(): file_hash(path)}


def _previous_audit_exclusions() -> tuple[set[str], set[str]]:
    if not LEGACY_AUDIT_MANIFEST.is_file():
        return set(), set()
    manifest = json.loads(LEGACY_AUDIT_MANIFEST.read_text(encoding="utf-8"))
    ids = {s["sentence_id"] for s in manifest.get("samples", [])}
    texts = {normalized_text(s) for s in manifest.get("samples", [])}
    return ids, texts


def _unique_population(dataset: str, exclude_ids: set[str], exclude_texts: set[str]) -> tuple[list[dict], dict, dict[str, str]]:
    records, hashes = _load_verified_jsonl(dataset)
    groups: dict[str, list[dict]] = defaultdict(list)
    for rec in records:
        groups[normalized_text(rec)].append(rec)

    frame: list[dict] = []
    excluded = 0
    for text, members in groups.items():
        members = sorted(members, key=lambda r: r["sentence_id"])
        if text in exclude_texts or any(m["sentence_id"] in exclude_ids for m in members):
            excluded += 1
            continue
        rep = dict(members[0])
        rep["duplicate_records"] = len(members)
        rep["conflicting_annotations"] = len({tuple(m["tags"]) for m in members}) > 1
        frame.append(rep)

    info = {
        "population_records": len(records),
        "population_unique_texts": len(groups),
        "excluded_previous_audit": excluded,
        "sampling_frame_size": len(frame),
    }
    return frame, info, hashes


def _quotas(strata: dict[str, list[dict]], budget: int = SAMPLE_SIZE) -> dict[str, int]:
    """Minimum coverage (>=2 per nonempty stratum when available), then largest-remainder allocation."""
    sizes = {k: len(rows) for k, rows in strata.items() if rows}
    if sum(sizes.values()) < budget:
        raise ValueError(f"Audit requires {budget} unique sentences; found {sum(sizes.values())}.")
    quotas = {k: min(2, size) for k, size in sizes.items()}
    remaining = budget - sum(quotas.values())
    if remaining < 0:
        raise ValueError("Audit budget cannot cover all nonempty strata.")
    capacity = {k: sizes[k] - quotas[k] for k in sizes}
    capacity_total = sum(capacity.values())
    if remaining:
        extras = {k: (remaining * cap) // capacity_total for k, cap in capacity.items()}
        left = remaining - sum(extras.values())
        ranked = sorted(capacity, key=lambda k: (-(remaining * capacity[k] % capacity_total), k))
        for k in ranked[:left]:
            extras[k] += 1
        quotas = {k: quotas[k] + extras[k] for k in quotas}
    return quotas


def _stratified(frame: list[dict], dataset: str, seed: int, sample_size: int = SAMPLE_SIZE) -> tuple[list[dict], dict]:
    if len(frame) < sample_size:
        raise ValueError(f"{dataset}: sampling frame has only {len(frame)} unique sentences (need {sample_size}).")
    length_median = median(len(r["tokens"]) for r in frame)
    strata: dict[str, list[dict]] = defaultdict(list)
    for row in frame:
        count = len(entity_spans(row["tags"]))
        entity_group = str(count) if count < 2 else "2PLUS"
        length_group = "SHORT" if len(row["tokens"]) <= length_median else "LONG"
        row["stratum"] = f"E{entity_group}_{length_group}"
        strata[row["stratum"]].append(row)

    quotas = _quotas(dict(strata), sample_size)
    rng = random.Random(f"{seed}:{dataset}")
    selected, details = [], []
    for key in sorted(strata):
        population = sorted(strata[key], key=lambda r: r["sentence_id"])
        n_h, N_h = quotas[key], len(population)
        for row in rng.sample(population, n_h):
            row["inclusion_probability"] = n_h / N_h
            selected.append(row)
        details.append({"stratum": key, "N_h": N_h, "n_h": n_h, "inclusion_probability": n_h / N_h})
    rng.shuffle(selected)
    return selected, {"length_median": length_median, "strata": details}


def build_or_load_manifest(
    out_dir: Path,
    datasets_order: tuple[str, ...],
    seed: int,
    sample_size: int = SAMPLE_SIZE,
    exclude_previous: bool = False,
) -> dict:
    path = out_dir / "audit_sample_manifest.json"
    if path.is_file():
        manifest = json.loads(path.read_text(encoding="utf-8"))
        unhashed = {k: v for k, v in manifest.items() if k != "sample_manifest_hash"}
        if stable_hash(unhashed) != manifest["sample_manifest_hash"]:
            raise ValueError("Existing audit_sample_manifest.json was modified (hash mismatch).")
        if manifest["sampling_seed"] != seed:
            raise ValueError(f"Existing manifest uses seed {manifest['sampling_seed']}; use a new --out-dir for seed {seed}.")
        existing_ds = tuple(v["dataset"] for v in manifest["datasets"].values())
        if existing_ds != datasets_order:
            raise ValueError(f"Existing manifest covers {existing_ds}, requested {datasets_order}; use a separate --out-dir.")
        return manifest

    exclude_ids, exclude_texts = _previous_audit_exclusions() if exclude_previous else (set(), set())
    datasets_meta, samples, file_hashes = {}, [], {}
    for index, dataset in enumerate(datasets_order, 1):
        code = f"D{index:02d}"
        frame, frame_info, ds_hashes = _unique_population(dataset, exclude_ids, exclude_texts)
        file_hashes.update(ds_hashes)
        selected, strata_info = _stratified(frame, dataset, seed, sample_size=sample_size)
        datasets_meta[code] = {"dataset": dataset, **frame_info, **strata_info}
        for number, row in enumerate(selected, 1):
            sample = {
                "sample_id": f"{code}-{number:03d}",
                "dataset_code": code,
                "dataset": dataset,
                "sentence_id": row["sentence_id"],
                "source_split": row.get("source_split"),
                "stratum": row["stratum"],
                "inclusion_probability": row["inclusion_probability"],
                "duplicate_records": row["duplicate_records"],
                "conflicting_annotations": row["conflicting_annotations"],
                "tokens": row["tokens"],
                "original_tags": row["original_tags"],
                "tags": row["tags"],
                "entities": [list(span) for span in entity_spans(row["tags"])],
            }
            sample["source_record_hash"] = stable_hash({
                k: sample[k] for k in ("sentence_id", "tokens", "original_tags", "tags", "source_split")
            })
            samples.append(sample)

    manifest = {
        "schema_version": SCHEMA_VERSION,
        "method": "independent_dual_annotator_llm_audit",
        "sampling_seed": seed,
        "sample_size_per_dataset": sample_size,
        "active_types": list(ACTIVE_TYPES),
        "excluded_previous_audit_samples": exclude_previous,
        "source_file_hashes": file_hashes,
        "datasets": datasets_meta,
        "samples": samples,
    }
    manifest["sample_manifest_hash"] = stable_hash(manifest)
    write_json(path, manifest)
    write_json(out_dir / "dataset_code_key.json", {c: info["dataset"] for c, info in datasets_meta.items()})
    log(f"Created NEW sample manifest: {path}  ({len(samples)} samples across {len(datasets_order)} datasets)")
    return manifest


# =============================================================================
# 2. AUDIT PROMPT (STRICT 18-CLASS STAGE-2 NERGRIT SPECIFICATION — 0 REG, 0 TTL)
# =============================================================================
AUDIT_PROMPT = """Kamu adalah Auditor Ahli dan Verifikator Independen untuk evaluasi kualitas dataset Named Entity Recognition (NER) Bahasa Indonesia standar korpus manusia NERGRIT acuan skripsi (18 Kelas Entitas Aktif).

Tugasmu adalah memeriksa secara kritis, mengoreksi kesalahan batas rentang kata (boundary) atau kelas entitas, menghapus entitas ilegal, serta menemukan entitas yang terlewat (missing entities) pada setiap kalimat dalam batch berikut secara SANGAT TELITI, OBJEKTIF, dan 100% PATUH PADA PEDOMAN NERGRIT TERBARU DI BAWAH INI.

=============================================================================
BAGIAN A: TAKSONOMI RESMI 18 KELAS ENTITAS AKTIF (DILARANG MENGGUNAKAN REG ATAU TTL)
=============================================================================
1.  PER (Person): Nama individu manusia atau tokoh fiksi (Joko Widodo, Sri Mulyani, Tito Karnavian, Harry Potter). Sapaan umum (Bapak, Ibu, Pak, Bu, Saudara, Tuan, Nyonya) WAJIB dibuang (O). Pangkat militer/polisi dan gelar akademik/religi melekat (Dr., dr., Prof., Ir., KH, K.H., Habib, Ustadz, Jenderal, Letjen, Mayjen, Brigjen, Marsekal, Laksamana, Kolonel, Letkol, Mayor, Kapten, Kombes, AKBP, Kompol, AKP, Iptu, Ipda, Aiptu, Aipda, Bripka, Brigadir) WAJIB DISERAP ke dalam satu rentang PER bersama namanya (contoh: "Letjen Suharyanto", "Jenderal Tito Karnavian", "dr. Andi Wijaya" = satu span PER).
2.  ORG (Organization): Perusahaan komersial swasta, BUMN korporasi (Pertamina, Bank Mandiri, PT Telkom, PLN, Bulog, Apple), portal media pers daring (detikcom, CNN Indonesia, Kompas.com, TEMPO), klub olahraga profesional (Chelsea, Persib), dan tim nasional olahraga dalam konteks kejuaraan (Timnas Indonesia, Jerman).
3.  GPE (Geo-Political Entity): Entitas geopolitik administratif berdaulat, berpemerintahan, dan berpenduduk: negara, provinsi, kota, kabupaten, kecamatan, desa (Indonesia, Jawa Barat, Jakarta, Surabaya, Kabupaten Sleman).
4.  LOC (Location): Bentang alam alami non-administratif (Gunung Merapi, Danau Toba, Laut Jawa, Pantai Kuta), nama jalan/koridor lalu lintas (Jalan Jenderal Sudirman, Jalan Ahmad Yani, Jl. Thamrin), ruang terbuka publik (Monas, Lapangan Sunburst BSD), kawasan makro-benua (Asia Tenggara, Timur Tengah, kawasan Pasifik), dan aula legislatif (ruang paripurna DPRD).
5.  FAC (Facility): Bangunan fisik infrastruktur buatan manusia: bandara (Bandara Soekarno - Hatta), stasiun (Stasiun Pondokcina), pelabuhan (Pelabuhan Bakauheni), jalan tol (Tol Cipali), jembatan (Jembatan Kalikuto), stadion (Stadion GBK), gedung perkantoran/pemerintahan fisik (Gedung DPR, Balai Kota, Gedung Negara), rumah sakit (RS Cipto Mangunkusumo), penjara (LP Salemba), tempat ibadah fisik (Masjid Istiqlal, Gereja Katedral, masjid), sekolah, dan WC.
6.  EVT (Event): Peristiwa bersejarah, ajang kompetisi olahraga (Piala Dunia 2018, Asian Games), konferensi resmi (KTT G20), pameran (GIIAS 2018), operasi keamanan resmi (Operasi Ketupat), serta perayaan hari raya umum/nasional dalam konteks peristiwa (Lebaran, Natal, Idul Fitri, Idul Adha, Waisak, Nyepi, Imlek). Tanda petik dan kata "operasi" di luar span.
7.  WOA (Work of Art): Judul karya cipta seni: film, buku, novel, lagu kebangsaan/populer, lukisan, patung seni, relief, motif wayang (Laskar Pelangi, Indonesia Raya, The Dark Knight, Patung Soekarno). Kata jenis (film, lagu, novel, buku, album, lukisan, drama, serial, sinetron) dan tanda petik WAJIB di luar span (O).
8.  LAW (Law): Dokumen hukum resmi, undang-undang, peraturan pemerintah, perpres, KUHP, APBN, traktat internasional, dan izin resmi (Undang - Undang Dasar 1945, UU No . 11 Tahun 2020, Perpres, APBN 2018, SIM, STNK, Pancasila). Judul bilingual dalam tanda kurung dipisah menjadi dua span LAW terpisah (tanpa kurung).
9.  PRD (Product): Seluruh sarana transportasi fisik huruf kecil maupun bermerek (mobil, sepeda motor, motor, truk, bus, kapal, pesawat, kereta, kereta api, LRT, Avanza, Boeing 737), gawai teknologi (iPhone, CCTV, ponsel, smartphone, e - KTP), komoditas energi/pangan/kimia/narkotika (BBM, minyak, biodiesel, beras, kopi, rendang, daging, sabu, petasan), perlengkapan keselamatan (helm, jaket, sabuk pengaman), indeks pasar modal (IHSG), dan aplikasi perangkat lunak (Twitter, Instagram, ChatGPT).
10. LAN (Language): Nama bahasa alami manusia (bahasa Indonesia, bahasa Arab, bahasa Inggris, Latin). Kata jenis "bahasa" diserap masuk ke rentang LAN.
11. DAT (Date): Tanggal kalender, nama hari, nama bulan, angka tahun tunggal (2018, 15 Mei 2018, Senin, Januari, Januari 2024), dan FORMAT KEPALA BERITA BERKURUNG: "Hari ( DD / MM / YYYY )" atau "Hari ( DD / MM )" sebagai SATU SPAN UTUH DAT termasuk tanda kurung buka dan tutupnya (misal: "Selasa ( 15 / 5 / 2018 )" adalah satu span DAT penuh). Kata bantu "pada", "tanggal", "hari" di luar span (O).
12. TIM (Time): Angka jam spesifik arloji dan penanda zona waktu (06 . 00 WIB, 10 . 30 Wita, 09 . 30 WIB, 17 : 00 WIB). Kata "pukul", "jam", "sekira", "sekitar" dan penanda diurnal ("pagi", "siang", "sore", "malam", "dini hari", "petang") WAJIB DIEKSKLUSI (O).
13. MON (Money): Nilai nominal moneter beserta simbol mata uang atau kata satuan nominalnya (Rp 40 Ribu, Rp 50 . 000, 100 triliun rupiah, US$ 50 juta, 10 dollar AS).
14. QTY (Quantity): Satuan ukuran fisik (panjang, berat, luas, volume, kecepatan: 500 kilometer, 10 ton, 5 juta ton, 3 liter) DAN SELURUH DURASI WAKTU LAMPAU/JANGKA: "dua tahun", "tiga bulan", "15 tahun", "24 jam", "30 menit", "dua hari", "dua minggu", "setahun", "seminggu", "36 hari". Preposisi "selama" dan prefiks "sebesar/sejauh/seluas/sebanyak" di luar span (O).
15. CRD (Cardinal): Bilangan cacah/kuantitas murni tanpa satuan fisik/waktu (satu, dua, tiga, 115, 1 . 000, 12, 50). Termasuk kata "kedua" atau "keduanya" saat bermakna kuantitas jamak (both).
16. ORD (Ordinal): Bilangan urutan, ranking, tingkat juara, tahapan (pertama, terakhir, ketiga). Format "ke-N" WAJIB inklusif menyerap "ke" dan tanda hubung (ke - 4, ke - 12, ke 58).
17. PRC (Percent): Nilai persentase beserta simbol persen atau kata leksikalnya (10 %, 50 persen, 12 , 5 %, 3 , 5 %).
18. NOR (National / Institutional / Political Group): Aparat kepolisian dan militer nasional (polisi, Polri, kepolisian, TNI, Polda Metro Jaya, Polres, Satreskrim), lembaga tinggi negara/kementerian/komisi independen (KPK, DPR, DPR RI, MPR, KPU, BMKG, BNPB, Bawaslu, pemerintah, pemkab, pemkot, Kementerian Keuangan), partai politik (PKS, Gerindra, Demokrat, PDIP, Golkar), organisasi antarpemerintah (PBB, WHO), kelompok kewarganegaraan/etnis (warga negara Indonesia, suku Dayak), dan JABATAN STRUKTURAL KENEGARAAN (Presiden, Wakil Presiden, Wapres, Menteri, Gubernur, Bupati, Walikota, Wali Kota, Kapolri, Wakapolri, Panglima TNI, Kepala BNPB, Kepala BMKG, Kasat, Direktur, Ketua DPR, Ketua KPK, Jaksa Agung, Sekjen, Kapolda, Kapolres, Camat, Lurah) yang TERPISAH dari span nama PER!

=============================================================================
BAGIAN B: 10 ATURAN WAJIB & PENYELARASAN BATAS NERGRIT (KONTRAK AUDITOR)
=============================================================================
1. PENIADAAN TOTAL "REG" DAN "TTL" -> O / PEMETAAN RESMI:
   - Label REG dan TTL DILARANG digunakan sebagai keluaran!
   - KAWASAN REGIONAL (Asia Tenggara, Timur Tengah, kawasan Pasifik) -> LOC.
   - ISTILAH AGAMA & RITUS: Nama agama formal (Islam, Kristen, Katolik, Hindu, Buddha, Yahudi), penganut (Muslim, muslim, umat Islam, umat muslim, Kristiani), sebutan Tuhan/Nabi (Allah SWT, Tuhan, Nabi Muhammad SAW), kitab suci (Alquran, Injil), ritus (puasa, Buka Puasa, sholat, azan), seruan doa (Insya Allah, Alhamdulillah), serta bulan suci (Ramadan, Ramadhan) WAJIB berstatus O! Jika ada entitas asli yang melabeli kata-kata tersebut sebagai NOR/WOA/PER/DAT, tandai INCORRECT dan ACTION=REMOVE!
   - HARI RAYA KEAGAMAAN (Lebaran, Natal, Idul Fitri, Idul Adha, Nyepi, Waisak, Imlek) -> EVT.
   - TEMPAT IBADAH FISIK (Masjid Istiqlal, Gereja Katedral, masjid) -> FAC.
2. PENANGANAN 3-CABANG GELAR/JABATAN PADA "PER" VS "NOR":
   - a. Sapaan Umum (Bapak, Ibu, Pak, Bu, Saudara, Tuan, Nyonya, Ny., Tn.) -> WAJIB O (REMOVE jika dilabeli, atau REPLACE PER tanpa sapaan).
   - b. Pangkat Kedinasan & Gelar Akademik/Religi Melekat (Dr., dr., Prof., Ir., KH, K.H., Habib, Ustadz, Jenderal, Letjen, Mayjen, Brigjen, Kombes, AKBP, Aiptu, dll.) -> WAJIB DISERAP ke dalam rentang PER! Contoh benar: "Letjen Suharyanto" sebagai satu PER:3-4, "Jenderal Tito Karnavian" sebagai satu PER:2-4. Jika terpisah atau dibuang ke O, wajib koreksi REPLACE agar pangkat masuk PER!
   - c. Jabatan Struktural Kenegaraan (Presiden, Menteri Keuangan, Gubernur, Bupati, Kapolri, Panglima TNI, Kepala BNPB) -> WAJIB "NOR" dan TERPISAH dari span PER! Contoh benar: "Presiden" (NOR:1-1) + "Joko Widodo" (PER:2-3); "Menteri Ketenagakerjaan" (NOR:1-2) + "Ida Fauziah" (PER:3-4). JANGAN mencabut "Presiden" dari NOR ke O, dan JANGAN menggabungkan "Presiden" masuk ke PER!
3. EKSKLUSI PREPOSISI 99,99%:
   - Preposisi spasial/temporal & penanda jumlah (di, ke, dari, pada, dalam, selama, sejak, hingga, sampai, menuju, oleh, tentang, bagi, untuk, sebesar, sejauh, seluas, seberat, sebanyak, setinggi, sedalam, berbiaya, senilai, seharga, mencapai, berkisar, pada hari, hari) DILARANG masuk ke dalam rentang entitas apa pun!
   - Satu-satunya pengecualian: awalan "ke" pada ORD (misal: "ke - 4", "ke 58").
4. NOR VS ORG:
   - Aparat hukum, militer, kementerian, DPR, KPK, KPU, BMKG, pemda, pemerintah, parpol WAJIB "NOR".
   - "ORG" khusus perusahaan komersial/BUMN korporasi (Pertamina, Bank Mandiri, PT Telkom, PLN, Bulog), media pers (detikcom, CNN Indonesia, Kompas.com), klub olahraga (Chelsea, Persib), dan timnas olahraga.
5. PRODUK HURUF KECIL WAJIB "PRD":
   - Kendaraan huruf kecil (mobil, sepeda motor, motor, truk, bus, kapal, pesawat, kereta, LRT), komoditas (BBM, minyak, beras, kopi, sabu, petasan), alat keselamatan/gawai (helm, jaket, CCTV, ponsel, e - KTP), IHSG, serta aplikasi (Twitter, ChatGPT) WAJIB "PRD".
6. DURASI WAKTU KE "QTY" (BUKAN DAT / TIM):
   - "dua tahun", "tiga bulan", "15 tahun", "24 jam", "30 menit", "dua hari", "setahun", "seminggu", "36 hari" WAJIB "QTY" (tanpa "selama").
7. JAM SPESIFIK PADA "TIM":
   - HANYA angka jam & zona waktu ("09 . 30 WIB", "10 . 30 Wita"). Kata "pukul", "jam", "sekira", "pagi/siang/sore/malam" WAJIB O.
8. KURUNG TANGGAL KEPALA BERITA PADA "DAT":
   - Format "Hari ( DD / MM / YYYY )" atau "Hari ( DD / MM )" -> SATU span DAT utuh mencakup tanda kurung buka dan tutup! Contoh: "Selasa ( 15 / 5 / 2018 )" = DAT.
9. DISTINGSI SPASIAL GPE VS LOC VS FAC:
   - GPE = wilayah administratif (Indonesia, Jawa Barat, Kabupaten Sleman).
   - LOC = bentang alam (Gunung Merapi), nama jalan (Jalan Jenderal Sudirman), ruang terbuka publik (Monas), kawasan makro (Asia Tenggara), aula DPRD.
   - FAC = infrastruktur fisik buatan manusia (Bandara Soekarno - Hatta, Tol Cipali, Stasiun Pondokcina, Stadion GBK, Gedung DPR, Gedung Negara, Masjid Istiqlal, sekolah, WC).
10. TANDA PETIK, PENANDA MEDIA, & TANDA BACA AKHIR:
   - Tanda petik (" / ') serta kata jenis media ("film", "lagu", "novel", "buku", "operasi") di luar span WOA/EVT (O).
   - Tanda baca akhir kalimat (titik, koma, tanda kutip penutup) TIDAK BOLEH masuk ke rentang entitas kecuali bagian resmi singkatan (misal "dr.", "PT.", "No.") atau kurung tutup dateline aturan 8.

=============================================================================
BAGIAN C: ATURAN PENILAIAN & FORMAT OUTPUT JSON
=============================================================================
Untuk setiap entitas asli (E001, E002, dst.) pada input:
- Jika rentang indeks token (1-based, inklusif) DAN tipe kelasnya SUDAH TEPAT sesuai aturan NERGRIT 18 kelas di atas:
  * "decision": "CORRECT"
  * "action": "KEEP"
- Jika entitas asli tersebut salah (False Positive: bukan entitas, istilah agama, sapaan umum Bapak/Ibu, kata benda umum di luar PRD):
  * "decision": "INCORRECT"
  * "action": "REMOVE"
- Jika rentang token kurang/berlebih kata (misal pangkat Letjen belum masuk PER, atau preposisi "di"/"pukul" ikut masuk, atau kurung dateline terpotong) ATAU kelas entitasnya salah (misal DPR/Presiden dilabeli ORG padahal NOR, durasi dilabeli DAT padahal QTY, jalan dilabeli FAC padahal LOC):
  * "decision": "INCORRECT"
  * "action": "REPLACE:KELAS:TOKEN_AWAL-TOKEN_AKHIR"
    (Contoh: "REPLACE:PER:2-3" atau bila dipecah menjadi beberapa span: "REPLACE:NOR:1-1; PER:2-3")

Untuk entitas terlewat pada token berlabel O:
- Jika ada entitas sah 18 kelas (termasuk kendaraan huruf kecil PRD, jabatan struktural NOR, durasi QTY) yang terlewat dan belum tercakup KEEP/REPLACE:
  * "missing_entities": "KELAS:TOKEN_AWAL-TOKEN_AKHIR" (pisahkan dengan "; " bila >1)
- Jika tidak ada yang terlewat:
  * "missing_entities": "NONE"
- JANGAN mengulang span yang sudah ada di KEEP atau REPLACE ke dalam "missing_entities".

Kembalikan HANYA satu objek JSON valid (tanpa markdown fence, tanpa teks lain di luar JSON):
{
  "results": [
    {
      "sample_id": "D01-001",
      "entities": [
        {
          "id": "E001",
          "decision": "CORRECT",
          "action": "KEEP",
          "note": ""
        },
        {
          "id": "E002",
          "decision": "INCORRECT",
          "action": "REPLACE:PER:3-4",
          "note": "Serap pangkat Letjen ke dalam span PER"
        }
      ],
      "missing_entities": "PRD:12-12",
      "notes": ""
    }
  ]
}"""


def _span_text(span: tuple[int, int, str] | list[Any]) -> str:
    start, end, label = span
    return f"{label}:{start + 1}-{end}"


def sample_payload(sample: dict) -> dict:
    return {
        "sample_id": sample["sample_id"],
        "sentence": " ".join(sample["tokens"]),
        "tokens": [
            {"index": i, "token": tok, "active_bio": tag}
            for i, (tok, tag) in enumerate(zip(sample["tokens"], sample["tags"]), 1)
        ],
        "original_entities": [
            {
                "id": f"E{n:03d}",
                "span": _span_text(span),
                "text": " ".join(sample["tokens"][span[0]:span[1]]),
            }
            for n, span in enumerate(sample["entities"], 1)
        ],
    }


def build_audit_prompt(batch: list[dict]) -> str:
    data = json.dumps([sample_payload(s) for s in batch], ensure_ascii=False, indent=2)
    return (
        f"{AUDIT_PROMPT}\n\n"
        "=============================================================================\n"
        "DATA BATCH YANG HARUS DIAUDIT:\n"
        "=============================================================================\n"
        f"{data}\n\n"
        f"Kembalikan tepat {len(batch)} objek pada array \"results\" (satu untuk setiap sample_id di atas).\n"
        "Keluaran (HANYA JSON VALID):"
    )


# =============================================================================
# 3. 9ROUTER CLIENT (STREAMING SSE + THINKING-SAFE PARSER)
# =============================================================================
def _consume_sse_response(resp: requests.Response) -> tuple[str, str]:
    """Consume OpenAI-compatible SSE stream, collecting delta.content and raw trace."""
    content_parts: list[str] = []
    raw_lines: list[str] = []
    for line in resp.iter_lines(decode_unicode=True):
        if not line:
            continue
        raw_lines.append(line)
        stripped = line.strip()
        if not stripped.startswith("data:"):
            continue
        payload = stripped[5:].strip()
        if payload == "[DONE]":
            break
        try:
            chunk = json.loads(payload)
        except Exception:
            continue
        choices = chunk.get("choices") or []
        if not choices:
            continue
        delta = choices[0].get("delta") or {}
        if delta.get("content"):
            content_parts.append(delta["content"])
        elif choices[0].get("message", {}).get("content"):
            content_parts.append(choices[0]["message"]["content"])
    return "".join(content_parts), "\n".join(raw_lines)


def call_model(
    model: str,
    prompt: str,
    temperature: float | None,
    reasoning_effort: str | None,
    timeout: int,
    max_retries: int = 5,
    use_stream: bool = True,
) -> tuple[str | None, str]:
    headers = {"Authorization": f"Bearer {NINEROUTER_API_KEY}", "Content-Type": "application/json"}
    payload: dict[str, Any] = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "stream": use_stream,
    }
    if temperature is not None:
        payload["temperature"] = temperature
    if reasoning_effort:
        payload["reasoning_effort"] = reasoning_effort

    delay, last_raw = 4.0, ""
    for _ in range(max_retries):
        try:
            resp = requests.post(CHAT_URL, headers=headers, json=payload, timeout=timeout, stream=use_stream)
            if resp.status_code == 200:
                ctype = (resp.headers.get("content-type") or "").lower()
                if use_stream or "text/event-stream" in ctype:
                    content, raw = _consume_sse_response(resp)
                    last_raw = raw
                    if content.strip():
                        return content, last_raw
                    # Non-stream JSON may still have been returned despite stream=True
                    try:
                        data = json.loads(raw)
                        msg = data["choices"][0]["message"]
                        content = msg.get("content") or ""
                        if content.strip():
                            return content, raw
                    except Exception:
                        pass
                else:
                    last_raw = resp.text
                    try:
                        content = resp.json()["choices"][0]["message"]["content"]
                        if content and content.strip():
                            return content, last_raw
                    except Exception:
                        pass
                log(f"   [{model}] empty response, retrying in {delay:.0f}s")
            elif resp.status_code == 400:
                err_txt = resp.text
                last_raw = err_txt
                low = err_txt.lower()
                if "temperature" in low and "temperature" in payload:
                    payload.pop("temperature")
                    log(f"   [{model}] temperature rejected by upstream; retrying without temperature")
                    continue
                if ("reasoning_effort" in low or "reasoning" in low) and "reasoning_effort" in payload:
                    payload.pop("reasoning_effort")
                    log(f"   [{model}] reasoning_effort rejected by upstream; retrying without reasoning_effort")
                    continue
                log(f"   [{model}] HTTP 400: {err_txt[:180]}")
            elif resp.status_code == 429:
                last_raw = resp.text
                log(f"   [{model}] rate limited (429), retrying in {delay * 2:.0f}s")
                time.sleep(delay)
            else:
                last_raw = resp.text
                log(f"   [{model}] HTTP {resp.status_code}: {last_raw[:160]}")
        except requests.exceptions.Timeout:
            log(f"   [{model}] timeout (>{timeout}s), retrying in {delay:.0f}s")
        except Exception as exc:
            log(f"   [{model}] network error: {exc}; retrying in {delay:.0f}s")
        time.sleep(delay + random.uniform(0.5, 1.5))
        delay = min(delay * 1.6, 90)
    return None, last_raw


def parse_json(text: str | None) -> dict | None:
    if not text:
        return None
    cleaned = re.sub(r"<think>[\s\S]*?</think>", "", text, flags=re.IGNORECASE)
    cleaned = re.sub(r"<thought>[\s\S]*?</thought>", "", cleaned, flags=re.IGNORECASE).strip()

    candidates = [cleaned] + re.findall(r"```(?:json)?\s*([\s\S]*?)\s*```", cleaned)
    first, last = cleaned.find("{"), cleaned.rfind("}")
    if first != -1 and last > first:
        candidates.append(cleaned[first:last + 1])
        candidates.append(re.sub(r",\s*([}\]])", r"\1", cleaned[first:last + 1]))

    for candidate in candidates:
        try:
            value = json.loads(candidate)
        except (json.JSONDecodeError, TypeError):
            continue
        if isinstance(value, list):
            return {"results": value}
        if isinstance(value, dict):
            return value
    return None


# =============================================================================
# 4. RESPONSE VALIDATION & NORMALIZATION
# =============================================================================
class InvalidResult(ValueError):
    pass


SPAN_RE = re.compile(r"^\s*([A-Za-z_]+)\s*:\s*(\d+)\s*(?:-\s*(\d+))?\s*$")


def parse_spans(value: str, n_tokens: int, normalizations: list[str], context: str) -> set[tuple[int, int, str]]:
    spans: set[tuple[int, int, str]] = set()
    for item in re.split(r"[;,]\s*(?=[A-Za-z_]+\s*:)", value.strip()):
        if not item.strip():
            continue
        match = SPAN_RE.match(item)
        if not match:
            raise InvalidResult(f"{context}: invalid span {item!r}")
        raw_label = match[1].upper()
        label = TAG_ALIASES.get(raw_label, raw_label)
        if label != raw_label:
            normalizations.append(f"{context}: mapped alias {raw_label} -> {label}")
        start = int(match[2])
        end = int(match[3]) if match[3] else start
        if label in DROPPED_TYPES:
            normalizations.append(f"{context}: dropped {label} span {item.strip()} (mapped to O)")
            continue
        if label not in ACTIVE_SET:
            raise InvalidResult(f"{context}: unsupported class {label}")
        if not 1 <= start <= end <= n_tokens:
            raise InvalidResult(f"{context}: token range {start}-{end} outside 1-{n_tokens}")
        spans.add((start - 1, end, label))
    return spans


def normalize_result(sample: dict, result: dict) -> dict:
    sid = sample["sample_id"]
    n = len(sample["tokens"])
    normalizations: list[str] = []
    raw_entities = result.get("entities") or []
    by_id: dict[str, dict] = {}
    for item in raw_entities:
        if isinstance(item, dict) and item.get("id"):
            eid = str(item["id"]).strip().upper()
            if eid in by_id:
                raise InvalidResult(f"{sid}: duplicate decision for {eid}")
            by_id[eid] = item

    expected_ids = [f"E{k:03d}" for k in range(1, len(sample["entities"]) + 1)]
    if set(by_id) != set(expected_ids):
        raise InvalidResult(f"{sid}: entity ids {sorted(by_id)} != expected {expected_ids}")

    final: set[tuple[int, int, str]] = set()
    decisions: list[dict] = []
    for eid, original in zip(expected_ids, sample["entities"]):
        orig_tuple = (int(original[0]), int(original[1]), str(original[2]))
        item = by_id[eid]
        decision = str(item.get("decision", "")).strip().upper()
        action = str(item.get("action", "")).strip()
        action_up = action.upper()

        if decision == "CORRECT":
            if action_up not in ("KEEP", ""):
                raise InvalidResult(f"{sid}/{eid}: CORRECT requires KEEP (got {action!r})")
            category, replacements = "KEEP", {orig_tuple}
        elif decision == "INCORRECT":
            if action_up == "REMOVE":
                category, replacements = "REMOVE", set()
            elif action_up.startswith("REPLACE:"):
                replacements = parse_spans(action[len("REPLACE:"):], n, normalizations, f"{sid}/{eid}")
                if replacements == {orig_tuple}:
                    normalizations.append(f"{sid}/{eid}: REPLACE identical to original -> CORRECT/KEEP")
                    decision, category = "CORRECT", "KEEP"
                elif not replacements:
                    category = "REMOVE"
                else:
                    category = "REPLACE"
            else:
                raise InvalidResult(f"{sid}/{eid}: INCORRECT requires REMOVE or REPLACE:<spans> (got {action!r})")
        else:
            raise InvalidResult(f"{sid}/{eid}: decision must be CORRECT or INCORRECT (got {decision!r})")

        final |= replacements
        decisions.append({
            "id": eid,
            "original": list(orig_tuple),
            "decision": decision,
            "category": category,
            "action": action,
            "replacement_spans": [list(s) for s in sorted(replacements)],
            "note": str(item.get("note", "") or ""),
        })

    missing_value = str(result.get("missing_entities", "NONE") or "NONE").strip()
    missing: set[tuple[int, int, str]] = set()
    if missing_value.upper() not in ("NONE", "-", "TIDAK ADA", "[]"):
        missing = parse_spans(missing_value, n, normalizations, f"{sid}/MISSING")

    duplicated = missing & final
    if duplicated:
        normalizations.append(f"{sid}: removed {len(duplicated)} missing span(s) already kept/replaced")
        missing -= duplicated

    incorrect_originals = {tuple(d["original"]) for d in decisions if d["decision"] == "INCORRECT"}
    if missing & incorrect_originals:
        raise InvalidResult(f"{sid}: an original marked INCORRECT was re-added as missing")

    final |= missing
    ordered = sorted(final)
    for prev, nxt in zip(ordered, ordered[1:]):
        if prev[1] > nxt[0]:
            raise InvalidResult(f"{sid}: overlapping final spans {_span_text(prev)} / {_span_text(nxt)}")

    return {
        "sample_id": sid,
        "decisions": decisions,
        "missing_spans": [list(s) for s in sorted(missing)],
        "final_spans": [list(s) for s in ordered],
        "notes": str(result.get("notes", "") or ""),
        "normalizations": normalizations,
    }


# =============================================================================
# 5. ANNOTATION RUNNER (INDEPENDENT & RESUMABLE PER SAMPLE)
# =============================================================================
def sample_path(out_dir: Path, annotator: str, sid: str) -> Path:
    return out_dir / f"annotator_{annotator}" / "samples" / f"{sid}.json"


def pending_samples(out_dir: Path, annotator: str, manifest: dict) -> list[dict]:
    return [s for s in manifest["samples"] if not sample_path(out_dir, annotator, s["sample_id"]).is_file()]


def run_batch(
    out_dir: Path,
    annotator: str,
    model: str,
    reasoning_effort: str | None,
    batch: list[dict],
    manifest_hash: str,
    args: argparse.Namespace,
) -> tuple[int, list[str]]:
    remaining = list(batch)
    saved, errors = 0, []
    for attempt in range(1, args.max_attempts + 1):
        if not remaining:
            break
        prompt = build_audit_prompt(remaining)
        started = time.time()
        content, raw = call_model(
            model=model,
            prompt=prompt,
            temperature=args.temperature,
            reasoning_effort=reasoning_effort,
            timeout=args.timeout,
            use_stream=not args.no_stream,
        )
        stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        raw_dir = out_dir / f"annotator_{annotator}" / "raw_responses"
        write_json(
            raw_dir / f"{stamp}_{remaining[0]['sample_id']}_a{attempt}.json",
            {
                "model": model,
                "reasoning_effort": reasoning_effort,
                "sample_ids": [s["sample_id"] for s in remaining],
                "attempt": attempt,
                "prompt_hash": stable_hash(prompt),
                "elapsed_s": round(time.time() - started, 2),
                "content": content,
                "raw": raw[:200000],
            },
        )
        parsed = parse_json(content) if content else None
        results = parsed.get("results") if isinstance(parsed, dict) else None
        if not isinstance(results, list):
            errors.append(f"attempt {attempt}: unparseable response")
            log(f"   [{annotator}] unparseable response for {remaining[0]['sample_id']}.. (attempt {attempt})")
            continue

        by_sid = {str(r.get("sample_id", "")).strip(): r for r in results if isinstance(r, dict)}
        still = []
        for sample in remaining:
            result = by_sid.get(sample["sample_id"])
            if result is None and len(remaining) == 1 and len(results) == 1 and isinstance(results[0], dict):
                result = results[0]
            try:
                if result is None:
                    raise InvalidResult(f"{sample['sample_id']}: missing from response")
                record = normalize_result(sample, result)
            except InvalidResult as exc:
                errors.append(f"attempt {attempt}: {exc}")
                log(f"   [{annotator}] invalid: {exc}")
                still.append(sample)
                continue

            record.update({
                "annotator": annotator,
                "model": model,
                "reasoning_effort": reasoning_effort,
                "dataset": sample["dataset"],
                "dataset_code": sample["dataset_code"],
                "sample_manifest_hash": manifest_hash,
                "attempt": attempt,
                "annotated_at": datetime.datetime.now().isoformat(timespec="seconds"),
            })
            write_json(sample_path(out_dir, annotator, sample["sample_id"]), record)
            saved += 1

        remaining = still
        if remaining and len(remaining) > 1 and attempt >= 2:
            for single in remaining:
                s_saved, s_err = run_batch_single(out_dir, annotator, model, reasoning_effort, single, manifest_hash, args)
                saved += s_saved
                errors += s_err
            remaining = []
            break

    if remaining:
        fail_log = out_dir / f"annotator_{annotator}" / "failed_samples.log"
        fail_log.parent.mkdir(parents=True, exist_ok=True)
        with fail_log.open("a", encoding="utf-8") as handle:
            for sample in remaining:
                handle.write(f"{datetime.datetime.now().isoformat()} {sample['sample_id']} {errors[-3:]}\n")
    return saved, errors


def run_batch_single(out_dir, annotator, model, reasoning_effort, sample, manifest_hash, args):
    class _One:
        pass
    sub = _One()
    sub.__dict__.update(vars(args))
    sub.max_attempts = max(2, args.max_attempts - 1)
    return run_batch(out_dir, annotator, model, reasoning_effort, [sample], manifest_hash, sub)


def annotate(out_dir: Path, manifest: dict, args: argparse.Namespace) -> None:
    annotators = [args.annotator] if args.annotator in ANNOTATORS else list(ANNOTATORS)
    tasks = []
    for annotator in annotators:
        pend = pending_samples(out_dir, annotator, manifest)
        batches = [pend[i:i + args.batch_size] for i in range(0, len(pend), args.batch_size)]
        if args.max_batches:
            batches = batches[:args.max_batches]
        tasks += [(annotator, batch) for batch in batches]
        log(
            f"[{annotator}] {ANNOTATORS[annotator]['model']} "
            f"(reasoning_effort={ANNOTATORS[annotator].get('reasoning_effort')}): "
            f"{len(pend)} pending -> {len(batches)} batch(es)"
        )

    if not tasks:
        log("All annotations already complete.")
        return

    done = Counter()
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {
            pool.submit(
                run_batch,
                out_dir,
                a,
                ANNOTATORS[a]["model"],
                ANNOTATORS[a].get("reasoning_effort"),
                b,
                manifest["sample_manifest_hash"],
                args,
            ): (a, b)
            for a, b in tasks
        }
        for future in concurrent.futures.as_completed(futures):
            annotator, batch = futures[future]
            try:
                saved, _ = future.result()
            except Exception as exc:
                log(f"   [{annotator}] batch {batch[0]['sample_id']} crashed: {exc}")
                continue
            done[annotator] += saved
            total = len(manifest["samples"]) - len(pending_samples(out_dir, annotator, manifest))
            log(
                f"[{annotator}] batch {batch[0]['sample_id']}..{batch[-1]['sample_id']}: "
                f"saved {saved}/{len(batch)} | progress {total}/{len(manifest['samples'])}"
            )
    write_progress(out_dir, manifest)


def write_progress(out_dir: Path, manifest: dict) -> dict:
    total = len(manifest["samples"])
    state = {
        "updated_at": datetime.datetime.now().isoformat(timespec="seconds"),
        "sample_manifest_hash": manifest["sample_manifest_hash"],
        "annotators": {},
    }
    for annotator, info in ANNOTATORS.items():
        pend = pending_samples(out_dir, annotator, manifest)
        per_ds = Counter(s["dataset_code"] for s in manifest["samples"]) - Counter(s["dataset_code"] for s in pend)
        state["annotators"][annotator] = {
            "model": info["model"],
            "reasoning_effort": info.get("reasoning_effort"),
            "completed": total - len(pend),
            "total": total,
            "per_dataset_completed": dict(sorted(per_ds.items())),
        }
    write_json(out_dir / "progress" / "state.json", state)
    return state


def show_status(out_dir: Path, manifest: dict) -> None:
    state = write_progress(out_dir, manifest)
    print("=" * 74)
    print("Independent dual-annotator audit (18-class NERGRIT) — status")
    print(f"Output dir     : {out_dir}")
    print(f"Manifest hash  : {manifest['sample_manifest_hash'][:16]}…  (seed {manifest['sampling_seed']})")
    print(f"Gateway        : {CHAT_URL}")
    for annotator, info in state["annotators"].items():
        pct_val = 100 * info["completed"] / info["total"] if info["total"] else 0.0
        eff = info.get("reasoning_effort") or "default"
        label = f"{info['model']} [{eff}]"
        print(f"  {annotator} {label:<34} {info['completed']:>3}/{info['total']} ({pct_val:5.1f}%)  {info['per_dataset_completed']}")
    print("=" * 74)


# =============================================================================
# 6. INTER-ANNOTATOR AGREEMENT & DUAL-AGREEMENT CONSENSUS
# =============================================================================
def spans_to_bio(n: int, spans) -> list[str]:
    tags = ["O"] * n
    for start, end, label in spans:
        tags[start] = f"B-{label}"
        for i in range(start + 1, end):
            tags[i] = f"I-{label}"
    return tags


def kappa(agree: int, n: int, ca: Counter, cb: Counter) -> float | None:
    if n == 0:
        return None
    po = agree / n
    pe = sum(ca[k] * cb.get(k, 0) for k in ca) / (n * n)
    if pe >= 1.0:
        return 1.0 if po == 1.0 else 0.0
    return (po - pe) / (1 - pe)


def prf(tp: int, fp: int, fn: int) -> dict[str, float]:
    return {
        "precision": tp / (tp + fp) if tp + fp else 0.0,
        "recall": tp / (tp + fn) if tp + fn else 0.0,
        "f1": 2 * tp / (2 * tp + fp + fn) if 2 * tp + fp + fn else 0.0,
    }


def landis_koch(value: float | None) -> str:
    if value is None:
        return "-"
    if value < 0:
        return "Buruk (poor)"
    for limit, label in (
        (0.20, "Sangat rendah (slight)"),
        (0.40, "Rendah (fair)"),
        (0.60, "Sedang (moderate)"),
        (0.80, "Substansial (substantial)"),
        (1.00, "Hampir sempurna (almost perfect)"),
    ):
        if value <= limit + 1e-12:
            return label
    return "Hampir sempurna (almost perfect)"


def unit_stats(sample: dict, a: dict, b: dict) -> dict:
    n = len(sample["tokens"])
    s1 = {tuple(x) for x in a["final_spans"]}
    s2 = {tuple(x) for x in b["final_spans"]}
    bio1, bio2 = spans_to_bio(n, s1), spans_to_bio(n, s2)
    typ1 = [t if t == "O" else t[2:] for t in bio1]
    typ2 = [t if t == "O" else t[2:] for t in bio2]
    dec_pairs = [
        (d1["category"], d2["category"], d1["replacement_spans"] == d2["replacement_spans"])
        for d1, d2 in zip(a["decisions"], b["decisions"])
    ]
    orig = {tuple(x) for x in sample["entities"]}
    return {
        "n": n,
        "bio_agree": sum(x == y for x, y in zip(bio1, bio2)),
        "bio_a": Counter(bio1),
        "bio_b": Counter(bio2),
        "typ_agree": sum(x == y for x, y in zip(typ1, typ2)),
        "typ_a": Counter(typ1),
        "typ_b": Counter(typ2),
        "s1": len(s1),
        "s2": len(s2),
        "inter": len(s1 & s2),
        "dec": dec_pairs,
        "identical": s1 == s2,
        "err_a": s1 != orig,
        "err_b": s2 != orig,
    }


def aggregate(units: list[dict]) -> dict:
    n = sum(u["n"] for u in units)
    bio_a, bio_b, typ_a, typ_b = Counter(), Counter(), Counter(), Counter()
    for u in units:
        bio_a.update(u["bio_a"])
        bio_b.update(u["bio_b"])
        typ_a.update(u["typ_a"])
        typ_b.update(u["typ_b"])
    bio_agree = sum(u["bio_agree"] for u in units)
    typ_agree = sum(u["typ_agree"] for u in units)
    s1, s2, inter = (sum(u[k] for u in units) for k in ("s1", "s2", "inter"))
    decs = [d for u in units for d in u["dec"]]
    cat_a, cat_b = Counter(d[0] for d in decs), Counter(d[1] for d in decs)
    bin_a = Counter("CORRECT" if d[0] == "KEEP" else "INCORRECT" for d in decs)
    bin_b = Counter("CORRECT" if d[1] == "KEEP" else "INCORRECT" for d in decs)
    sent_a = Counter(u["err_a"] for u in units)
    sent_b = Counter(u["err_b"] for u in units)
    return {
        "sentences": len(units),
        "tokens": n,
        "token_bio_percent_agreement": bio_agree / n if n else None,
        "token_bio_kappa": kappa(bio_agree, n, bio_a, bio_b),
        "token_type_percent_agreement": typ_agree / n if n else None,
        "token_type_kappa": kappa(typ_agree, n, typ_a, typ_b),
        "spans_annotator_1": s1,
        "spans_annotator_2": s2,
        "spans_agreed": inter,
        "span_f1_agreement": 2 * inter / (s1 + s2) if s1 + s2 else 1.0,
        "original_entities_judged": len(decs),
        "entity_decision_percent_agreement_3class": sum(d[0] == d[1] for d in decs) / len(decs) if decs else None,
        "entity_decision_kappa_3class": kappa(sum(d[0] == d[1] for d in decs), len(decs), cat_a, cat_b),
        "entity_decision_kappa_binary": kappa(
            sum((d[0] == "KEEP") == (d[1] == "KEEP") for d in decs), len(decs), bin_a, bin_b
        ),
        "entity_decision_exact_agreement": sum(d[0] == d[1] and d[2] for d in decs) / len(decs) if decs else None,
        "sentence_identical_rate": sum(u["identical"] for u in units) / len(units) if units else None,
        "sentence_error_kappa": kappa(sum(u["err_a"] == u["err_b"] for u in units), len(units), sent_a, sent_b),
    }


CI_KEYS = (
    "token_bio_kappa",
    "token_type_kappa",
    "span_f1_agreement",
    "entity_decision_kappa_3class",
    "entity_decision_kappa_binary",
)


def bootstrap(units: list[dict], iterations: int, seed: int) -> dict:
    if not units:
        return {}
    rng = random.Random(seed)
    draws: dict[str, list[float]] = defaultdict(list)
    for _ in range(iterations):
        resample = [units[rng.randrange(len(units))] for _ in units]
        stats = aggregate(resample)
        for key in CI_KEYS:
            if stats[key] is not None:
                draws[key].append(stats[key])
    out = {}
    for key, values in draws.items():
        values.sort()
        out[key] = [values[int(0.025 * (len(values) - 1))], values[int(0.975 * (len(values) - 1))]]
    return out


def consensus_spans(sample: dict, a: dict, b: dict) -> set[tuple[int, int, str]]:
    """Dual-agreement rule: original span overturned only if BOTH reject; new span added only if BOTH propose identically."""
    originals = {tuple(x) for x in sample["entities"]}
    s1 = {tuple(x) for x in a["final_spans"]}
    s2 = {tuple(x) for x in b["final_spans"]}
    return (originals & (s1 | s2)) | ((s1 & s2) - originals)


def quality_record(sample: dict, final: set[tuple[int, int, str]]) -> dict:
    originals = {tuple(x) for x in sample["entities"]}
    added = final - originals
    covered: set[int] = set()
    for start, end, _ in originals:
        covered.update(range(start, end))
    literal_missing = {s for s in added if not covered.intersection(range(s[0], s[1]))}
    return {
        "right": Counter(s[2] for s in originals & final),
        "wrong": Counter(s[2] for s in originals - final),
        "missing": Counter(s[2] for s in literal_missing),
        "tp": originals & final,
        "fp": originals - final,
        "fn": final - originals,
        "error": originals != final,
    }


def summarize_quality(samples: list[dict], records: list[dict], ds_info: dict | None) -> dict:
    tp = sum(len(r["tp"]) for r in records)
    fp = sum(len(r["fp"]) for r in records)
    fn = sum(len(r["fn"]) for r in records)
    out: dict[str, Any] = {
        "sentences": len(records),
        "right": sum(sum(r["right"].values()) for r in records),
        "wrong": sum(sum(r["wrong"].values()) for r in records),
        "missing": sum(sum(r["missing"].values()) for r in records),
        "tp": tp,
        "fp": fp,
        "fn": fn,
        **prf(tp, fp, fn),
        "sentences_with_error": sum(r["error"] for r in records),
    }
    out["raw_sentence_error_rate"] = out["sentences_with_error"] / len(records) if records else 0.0
    if ds_info:
        estimate, population = 0.0, sum(s["N_h"] for s in ds_info["strata"])
        for stratum in ds_info["strata"]:
            idx = [i for i, s in enumerate(samples) if s["stratum"] == stratum["stratum"]]
            errors = sum(records[i]["error"] for i in idx)
            if idx and population:
                estimate += stratum["N_h"] / population * errors / len(idx)
        out["weighted_sentence_error_rate"] = estimate
    return out


def load_annotations(out_dir: Path, manifest: dict, allow_partial: bool):
    loaded: dict[str, dict[str, dict]] = {}
    for annotator in ANNOTATORS:
        loaded[annotator] = {}
        for sample in manifest["samples"]:
            path = sample_path(out_dir, annotator, sample["sample_id"])
            if path.is_file():
                record = json.loads(path.read_text(encoding="utf-8"))
                if record["sample_manifest_hash"] != manifest["sample_manifest_hash"]:
                    raise ValueError(f"{path}: belongs to a different sample manifest")
                loaded[annotator][sample["sample_id"]] = record
    common = [s for s in manifest["samples"] if all(s["sample_id"] in loaded[a] for a in ANNOTATORS)]
    if len(common) != len(manifest["samples"]) and not allow_partial:
        missing = {a: len(manifest["samples"]) - len(loaded[a]) for a in ANNOTATORS}
        raise RuntimeError(f"Annotations incomplete {missing}. Finish the run or use --allow-partial.")
    return loaded, common


def write_annotator_txt(out_dir: Path, manifest: dict, loaded: dict) -> None:
    today = datetime.date.today().isoformat()
    for annotator, info in ANNOTATORS.items():
        for code in manifest["datasets"]:
            lines = [
                "BAB4 INDEPENDENT ANNOTATOR AUDIT (18-CLASS NERGRIT)",
                f"SCHEMA_VERSION={SCHEMA_VERSION}",
                f"DATASET_CODE={code}",
                f"SAMPLE_MANIFEST_HASH={manifest['sample_manifest_hash']}",
                f"ANNOTATOR_ID={annotator}",
                f"ANNOTATOR_MODEL={info['model']}",
                f"REASONING_EFFORT={info.get('reasoning_effort') or 'default'}",
                f"EXPORT_DATE={today}",
            ]
            for sample in (s for s in manifest["samples"] if s["dataset_code"] == code):
                record = loaded[annotator].get(sample["sample_id"])
                lines += [
                    "",
                    f"=== SAMPLE {sample['sample_id']} ===",
                    f"SOURCE_RECORD_REF={sample['source_record_hash']}",
                    f"SOURCE_SPLIT={sample['source_split']}",
                    f"STRATUM={sample['stratum']}",
                    "SENTENCE=" + json.dumps(" ".join(sample["tokens"]), ensure_ascii=False),
                    "TOKENS_BEGIN",
                    "INDEX\tTOKEN_JSON\tORIGINAL_BIO\tACTIVE_BIO",
                ]
                for i, (tok, orig, tag) in enumerate(zip(sample["tokens"], sample["original_tags"], sample["tags"]), 1):
                    lines.append(f"{i}\t{json.dumps(tok, ensure_ascii=False)}\t{orig}\t{tag}")
                lines += ["TOKENS_END", "ENTITIES_BEGIN"]
                decisions = {d["id"]: d for d in (record or {}).get("decisions", [])}
                for k, span in enumerate(sample["entities"], 1):
                    eid = f"E{k:03d}"
                    d = decisions.get(eid, {})
                    lines += [
                        f"ENTITY {eid}",
                        f"ORIGINAL={_span_text(span)}",
                        "TEXT=" + json.dumps(" ".join(sample["tokens"][span[0]:span[1]]), ensure_ascii=False),
                        f"DECISION={d.get('decision', '')}",
                        f"ACTION={d.get('action', '')}",
                        f"NOTE={d.get('note', '')}".replace("\n", " "),
                        "END_ENTITY",
                    ]
                missing = (record or {}).get("missing_spans")
                lines += [
                    "ENTITIES_END",
                    "MISSING_ENTITIES=" + (
                        "; ".join(_span_text(s) for s in missing)
                        if missing
                        else ("NONE" if record else "")
                    ),
                    f"SENTENCE_REVIEWED={'YES' if record else ''}",
                    f"NOTES={(record or {}).get('notes', '')}".replace("\n", " "),
                    f"=== END SAMPLE {sample['sample_id']} ===",
                ]
            path = out_dir / f"annotator_{annotator}" / f"audit_{code}.txt"
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def pct(v: float | None) -> str:
    return "-" if v is None else f"{100 * v:.2f}%".replace(".", ",")


def num(v: float | None, d: int = 3) -> str:
    return "-" if v is None else f"{v:.{d}f}".replace(".", ",")


def compute_iaa(out_dir: Path, manifest: dict, allow_partial: bool) -> dict:
    loaded, common = load_annotations(out_dir, manifest, allow_partial)
    if not common:
        raise RuntimeError("No overlapping samples completed by both A1 and A2 yet.")
    a1, a2 = loaded["A1"], loaded["A2"]
    datasets = manifest["datasets"]
    units = {s["sample_id"]: unit_stats(s, a1[s["sample_id"]], a2[s["sample_id"]]) for s in common}

    per_dataset_iaa, per_dataset_quality, annotator_quality = [], [], []
    per_class_iaa, per_class_quality = [], []
    consensus_rows, disagreements = [], []

    all_units = [units[s["sample_id"]] for s in common]
    total_iaa = aggregate(all_units)
    total_iaa["ci95"] = bootstrap(all_units, BOOTSTRAP_ITERATIONS, BOOTSTRAP_SEED)

    all_cons_records, all_cons_samples = [], []
    for code, info in datasets.items():
        ds_samples = [s for s in common if s["dataset_code"] == code]
        if not ds_samples:
            continue
        ds_units = [units[s["sample_id"]] for s in ds_samples]
        stats = aggregate(ds_units)
        stats["ci95"] = bootstrap(ds_units, BOOTSTRAP_ITERATIONS, BOOTSTRAP_SEED)
        per_dataset_iaa.append({"dataset_code": code, "dataset": info["dataset"], **stats})

        cons_records = []
        for sample in ds_samples:
            sid = sample["sample_id"]
            final = consensus_spans(sample, a1[sid], a2[sid])
            q = quality_record(sample, final)
            cons_records.append(q)
            consensus_rows.append({
                "sample_id": sid,
                "dataset": info["dataset"],
                "dataset_code": code,
                "stratum": sample["stratum"],
                "tokens": sample["tokens"],
                "original_spans": sample["entities"],
                "annotator_1_spans": a1[sid]["final_spans"],
                "annotator_2_spans": a2[sid]["final_spans"],
                "consensus_spans": [list(s) for s in sorted(final)],
                "sentence_error": q["error"],
            })
            if not units[sid]["identical"]:
                disagreements.append({
                    "sample_id": sid,
                    "dataset": info["dataset"],
                    "sentence": " ".join(sample["tokens"]),
                    "original": [_span_text(s) for s in sample["entities"]],
                    "A1": [_span_text(s) for s in a1[sid]["final_spans"]],
                    "A2": [_span_text(s) for s in a2[sid]["final_spans"]],
                    "consensus": [_span_text(s) for s in sorted(final)],
                    "A1_decisions": a1[sid]["decisions"],
                    "A2_decisions": a2[sid]["decisions"],
                    "A1_notes": a1[sid]["notes"],
                    "A2_notes": a2[sid]["notes"],
                })
        all_cons_records += cons_records
        all_cons_samples += ds_samples
        per_dataset_quality.append({
            "dataset_code": code,
            "dataset": info["dataset"],
            **summarize_quality(ds_samples, cons_records, info),
        })
        for annotator, records in (("A1", a1), ("A2", a2)):
            own = [quality_record(s, {tuple(x) for x in records[s["sample_id"]]["final_spans"]}) for s in ds_samples]
            annotator_quality.append({
                "annotator": annotator,
                "model": ANNOTATORS[annotator]["model"],
                "dataset_code": code,
                "dataset": info["dataset"],
                **summarize_quality(ds_samples, own, info),
            })
        for label in ACTIVE_TYPES:
            right = sum(r["right"][label] for r in cons_records)
            wrong = sum(r["wrong"][label] for r in cons_records)
            missing = sum(r["missing"][label] for r in cons_records)
            tp = sum(sum(s[2] == label for s in r["tp"]) for r in cons_records)
            fp = sum(sum(s[2] == label for s in r["fp"]) for r in cons_records)
            fn = sum(sum(s[2] == label for s in r["fn"]) for r in cons_records)
            per_class_quality.append({
                "dataset_code": code,
                "dataset": info["dataset"],
                "entity_class": label,
                "right": right,
                "wrong": wrong,
                "missing": missing,
                "tp": tp,
                "fp": fp,
                "fn": fn,
                **prf(tp, fp, fn),
            })

    for label in ACTIVE_TYPES:
        s1_cnt = sum(sum(1 for x in a1[s["sample_id"]]["final_spans"] if x[2] == label) for s in common)
        s2_cnt = sum(sum(1 for x in a2[s["sample_id"]]["final_spans"] if x[2] == label) for s in common)
        inter_cnt = sum(
            len(
                {tuple(x) for x in a1[s["sample_id"]]["final_spans"] if x[2] == label}
                & {tuple(x) for x in a2[s["sample_id"]]["final_spans"] if x[2] == label}
            )
            for s in common
        )
        per_class_iaa.append({
            "entity_class": label,
            "spans_annotator_1": s1_cnt,
            "spans_annotator_2": s2_cnt,
            "spans_agreed": inter_cnt,
            "span_f1_agreement": 2 * inter_cnt / (s1_cnt + s2_cnt) if s1_cnt + s2_cnt else None,
        })

    total_quality = summarize_quality(all_cons_samples, all_cons_records, None)
    normalization_count = sum(len(r.get("normalizations", [])) for a in (a1, a2) for r in a.values())
    summary = {
        "schema_version": SCHEMA_VERSION,
        "status": "complete" if len(common) == len(manifest["samples"]) else "partial",
        "method": "independent_dual_annotator_llm_audit",
        "nergrit_spec": "18-class Stage 2 (0 REG, 0 TTL)",
        "annotators": {
            k: {"model": v["model"], "reasoning_effort": v.get("reasoning_effort")}
            for k, v in ANNOTATORS.items()
        },
        "independent_annotation": True,
        "inter_annotator_agreement_available": True,
        "consensus_rule": (
            "dual_agreement: original span overturned only if both annotators reject it; "
            "new/replacement span added only if both annotators propose the identical span"
        ),
        "sample_manifest_hash": manifest["sample_manifest_hash"],
        "sampling_seed": manifest["sampling_seed"],
        "samples_compared": len(common),
        "bootstrap_iterations": BOOTSTRAP_ITERATIONS,
        "response_normalizations": normalization_count,
        "iaa_total": total_iaa,
        "iaa_per_dataset": per_dataset_iaa,
        "iaa_per_class": per_class_iaa,
        "consensus_quality_total": total_quality,
        "consensus_quality_per_dataset": per_dataset_quality,
        "annotator_quality_per_dataset": annotator_quality,
        "interpretation_scale": "Landis & Koch (1977)",
        "generated_at": datetime.datetime.now().isoformat(timespec="seconds"),
    }
    write_json(out_dir / "iaa_summary.json", summary)
    flat = lambda rows: [{k: (json.dumps(v) if isinstance(v, (dict, list)) else v) for k, v in r.items()} for r in rows]
    write_csv(out_dir / "iaa_per_dataset.csv", flat(per_dataset_iaa))
    write_csv(out_dir / "iaa_per_class.csv", per_class_iaa)
    write_csv(out_dir / "consensus_quality_per_dataset.csv", per_dataset_quality)
    write_csv(out_dir / "consensus_quality_per_class.csv", per_class_quality)
    write_csv(out_dir / "annotator_quality_per_dataset.csv", annotator_quality)
    with (out_dir / "consensus_records.jsonl").open("w", encoding="utf-8") as handle:
        for row in consensus_rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
    with (out_dir / "disagreements.jsonl").open("w", encoding="utf-8") as handle:
        for row in disagreements:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
    write_annotator_txt(out_dir, manifest, loaded)
    write_report(out_dir, summary)
    bundle = make_bundle(out_dir)
    print_summary(summary, bundle)
    return summary


def write_report(out_dir: Path, summary: dict) -> None:
    t = summary["iaa_total"]
    ci = t.get("ci95", {})

    def with_ci(key: str) -> str:
        lo_hi = ci.get(key)
        return f"{num(t[key])} [{num(lo_hi[0])}–{num(lo_hi[1])}]" if lo_hi else num(t[key])

    a1_info = summary["annotators"]["A1"]
    a2_info = summary["annotators"]["A2"]
    lines = [
        "# Independent Dual-Annotator Audit — IAA Report (18-Class NERGRIT)",
        "",
        f"- Annotator A1: `{a1_info['model']}` (reasoning_effort: `{a1_info.get('reasoning_effort')}`)",
        f"- Annotator A2: `{a2_info['model']}` (reasoning_effort: `{a2_info.get('reasoning_effort')}`)",
        f"- Samples compared: {summary['samples_compared']} ({t['tokens']:,} tokens, seed {summary['sampling_seed']})",
        f"- Consensus rule: {summary['consensus_rule']}",
        "",
        "## IAA Total (95% Bootstrap CI)",
        "",
        "| Metric | Value | Interpretation |",
        "| --- | --- | --- |",
        f"| Token Cohen's κ (37 BIO tags) | {with_ci('token_bio_kappa')} | {landis_koch(t['token_bio_kappa'])} |",
        f"| Token Cohen's κ (18 classes + O) | {with_ci('token_type_kappa')} | {landis_koch(t['token_type_kappa'])} |",
        f"| Entity-decision κ (KEEP/REMOVE/REPLACE) | {with_ci('entity_decision_kappa_3class')} | {landis_koch(t['entity_decision_kappa_3class'])} |",
        f"| Entity-decision κ (CORRECT/INCORRECT) | {with_ci('entity_decision_kappa_binary')} | {landis_koch(t['entity_decision_kappa_binary'])} |",
        f"| Pairwise exact span-F1 | {with_ci('span_f1_agreement')} | - |",
        f"| Token % agreement (BIO) | {pct(t['token_bio_percent_agreement'])} | - |",
        f"| Identical sentences | {pct(t['sentence_identical_rate'])} | - |",
        "",
        "## IAA per Dataset",
        "",
        "| Dataset | κ token BIO | κ token kelas | κ keputusan (3) | Span-F1 IAA | Kalimat identik |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for r in summary["iaa_per_dataset"]:
        lines.append(
            f"| {r['dataset']} | {num(r['token_bio_kappa'])} | {num(r['token_type_kappa'])} | "
            f"{num(r['entity_decision_kappa_3class'])} | {pct(r['span_f1_agreement'])} | {pct(r['sentence_identical_rate'])} |"
        )
    lines += [
        "",
        "## Dataset Annotation Quality vs Dual-Agreement Consensus",
        "",
        "| Dataset | Benar | Salah | Terlewat | Presisi | Recall | F1 | Kalimat bermasalah |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for r in summary["consensus_quality_per_dataset"] + [{"dataset": "TOTAL", **summary["consensus_quality_total"]}]:
        lines.append(
            f"| {r['dataset']} | {r['right']} | {r['wrong']} | {r['missing']} | {pct(r['precision'])} | "
            f"{pct(r['recall'])} | {pct(r['f1'])} | {r['sentences_with_error']} |"
        )
    (out_dir / "IAA_REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def make_bundle(out_dir: Path) -> Path:
    bundle = out_dir / "audit_iaa_results.zip"
    with zipfile.ZipFile(bundle, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(out_dir.rglob("*")):
            if path.is_file() and path != bundle and not path.name.endswith(".tmp"):
                archive.write(path, path.relative_to(out_dir))
    return bundle


def print_summary(summary: dict, bundle: Path) -> None:
    t = summary["iaa_total"]
    print("=" * 74)
    print(f"IAA RESULT ({summary['status']}, {summary['samples_compared']} samples)")
    print(f"  Token kappa (BIO)        : {num(t['token_bio_kappa'])}  {landis_koch(t['token_bio_kappa'])}")
    print(f"  Token kappa (class)      : {num(t['token_type_kappa'])}  {landis_koch(t['token_type_kappa'])}")
    print(f"  Entity-decision kappa    : {num(t['entity_decision_kappa_3class'])}  {landis_koch(t['entity_decision_kappa_3class'])}")
    print(f"  Pairwise span-F1         : {pct(t['span_f1_agreement'])}")
    print(f"  Identical sentences      : {pct(t['sentence_identical_rate'])}")
    q = summary["consensus_quality_total"]
    print(f"  Consensus P/R/F1 dataset : {pct(q['precision'])} / {pct(q['recall'])} / {pct(q['f1'])}")
    print("-" * 74)
    print(f"Results archive saved to:\n  {bundle}")
    print("=" * 74)


# =============================================================================
# MAIN CLI ENTRYPOINT
# =============================================================================
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Independent dual-LLM audit (Option A: 300 verified samples) + IAA")
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    parser.add_argument("--datasets", default=",".join(DEFAULT_DATASETS), help="Comma-separated dataset names")
    parser.add_argument("--sample-size", type=int, default=SAMPLE_SIZE)
    parser.add_argument("--seed", type=int, default=AUDIT_IAA_SEED)
    parser.add_argument("--exclude-previous", action="store_true", help="Exclude texts present in legacy audit_iaa manifest")
    parser.add_argument("--annotator", choices=["A1", "A2", "both"], default="both")
    parser.add_argument("--model-1", default=ANNOTATORS["A1"]["model"])
    parser.add_argument("--model-2", default=ANNOTATORS["A2"]["model"])
    parser.add_argument("--effort-1", default=ANNOTATORS["A1"]["reasoning_effort"])
    parser.add_argument("--effort-2", default=ANNOTATORS["A2"]["reasoning_effort"])
    parser.add_argument("--batch-size", type=int, default=5)
    parser.add_argument("--workers", type=int, default=4, help="Parallel worker threads across annotators")
    parser.add_argument("--max-batches", type=int, default=0, help="Limit batches per annotator (for smoke test)")
    parser.add_argument("--max-attempts", type=int, default=4)
    parser.add_argument("--timeout", type=int, default=300)
    parser.add_argument("--temperature", type=float, default=0.0, help="Sampling temperature (dropped if rejected)")
    parser.add_argument("--no-stream", action="store_true", help="Disable SSE streaming mode")
    parser.add_argument("--status", action="store_true")
    parser.add_argument("--sample-only", action="store_true")
    parser.add_argument("--compute-only", action="store_true")
    parser.add_argument("--allow-partial", action="store_true", help="Compute IAA on samples finished by both annotators")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    ANNOTATORS["A1"]["model"] = args.model_1
    ANNOTATORS["A2"]["model"] = args.model_2
    ANNOTATORS["A1"]["reasoning_effort"] = args.effort_1
    ANNOTATORS["A2"]["reasoning_effort"] = args.effort_2

    if args.model_1 == args.model_2:
        raise SystemExit("Error: The two annotators must be different models.")

    datasets_order = tuple(d.strip() for d in args.datasets.split(",") if d.strip())
    out_dir = args.out_dir.resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    manifest = build_or_load_manifest(
        out_dir=out_dir,
        datasets_order=datasets_order,
        seed=args.seed,
        sample_size=args.sample_size,
        exclude_previous=args.exclude_previous,
    )

    if args.status or args.sample_only:
        show_status(out_dir, manifest)
        return
    if not args.compute_only:
        annotate(out_dir, manifest, args)
        show_status(out_dir, manifest)

    complete = all(not pending_samples(out_dir, a, manifest) for a in ANNOTATORS)
    if complete or args.allow_partial:
        compute_iaa(out_dir, manifest, args.allow_partial)
    else:
        log("IAA not computed yet: annotations incomplete. Re-run the same command to resume "
            "(or add --allow-partial to preview).")


if __name__ == "__main__":
    main()
