# =============================================================================
# SEL 5: PRE-PROCESSING, ANTI-LEAKAGE SPLIT (JACCARD 5-GRAM >= 0.90), & STATISTIK 18 KELAS
# =============================================================================
from collections import Counter, defaultdict
import csv
import math
import random
import re
import statistics
import unicodedata

WORD_PATTERN = re.compile(r"\w+|[^\s\w]", flags=re.UNICODE)
ALLOWED_TYPES_SET = frozenset(ACTIVE_TYPES)

TYPE_ALIASES = {
    "PRO": "PRD", "PROD": "PRD", "PRODUCT": "PRD", "TECH": "PRD",
    "PERSON": "PER", "LOCATION": "LOC", "ORGANIZATION": "ORG", "DATE": "DAT",
    "TIME": "TIM", "MONEY": "MON", "QUANTITY": "QTY", "CARDINAL": "CRD",
    "ORDINAL": "ORD", "PERCENT": "PRC", "PCT": "PRC", "EVENT": "EVT",
    "FACILITY": "FAC", "LANGUAGE": "LAN", "WORK_OF_ART": "WOA", "NORP": "NOR",
    "REGION": "REG", "TITLE": "TTL",
}
GOLD_EXTRA_ALIASES = {"O\u201a\u00c4\u00e9": "O", "O -": "O"}


def write_csv_rows(path: Path, rows: list[dict]) -> None:
    """Simpan daftar dictionary ke berkas CSV UTF-8-SIG."""
    rows = list(rows)
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fields = list(dict.fromkeys(k for row in rows for k in row))
    with path.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def align_entities_to_bio(text: str, entities: list[dict[str, str]]) -> list[tuple[str, str]]:
    """Tokenisasi kalimat dan selaraskan rentang entitas ke tag BIO 18 kelas."""
    tokens = re.findall(r"\w+|[^\w\s]", text, re.UNICODE)
    tags = ["O"] * len(tokens)
    tagged = [False] * len(tokens)

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


def entity_spans(tags: list[str]) -> list[tuple[int, int, str]]:
    """Ekstrak rentang entitas (start, end-exclusive, type) dari barisan tag BIO (konvensi CoNLL/seqeval)."""
    result = []
    start, kind = None, None
    for index, tag in enumerate(list(tags) + ["O"]):
        if tag == "O":
            prefix, current = "O", None
        elif isinstance(tag, str) and re.fullmatch(r"[BI]-.+", tag):
            prefix, current = tag.split("-", 1)
        else:
            raise ValueError(f"Tag BIO tidak valid pada indeks {index}: {tag!r}")
        if start is not None and (prefix != "I" or current != kind):
            result.append((start, index, kind))
            start, kind = None, None
        if prefix != "O" and start is None:
            start, kind = index, current
    return result


def _percentile(values: list[int | float], q: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    position = (len(ordered) - 1) * q
    lower = int(position)
    upper = min(lower + 1, len(ordered) - 1)
    return ordered[lower] + (ordered[upper] - ordered[lower]) * (position - lower)


def dataset_statistics(records: list[dict]) -> dict:
    """Hitung statistik deskriptif korpus: kalimat, token, entitas, kepadatan, dan distribusi 18 kelas."""
    records = list(records)
    lengths, counts, vocabulary = [], [], set()
    class_counts, entity_tokens = Counter(), 0
    for record in records:
        tokens, tags = record["tokens"], record["tags"]
        if len(tokens) != len(tags):
            raise ValueError(f"Ketidakcocokan panjang token/tag pada {record.get('sentence_id', '?')}")
        spans_list = entity_spans(tags)
        lengths.append(len(tokens))
        counts.append(len(spans_list))
        vocabulary.update(unicodedata.normalize("NFKC", token).casefold() for token in tokens)
        class_counts.update(kind for _, _, kind in spans_list)
        entity_tokens += sum(end - start for start, end, _ in spans_list)
    sentences, tokens_total, entities_total = len(records), sum(lengths), sum(counts)
    return {
        "S": sentences,
        "T": tokens_total,
        "E": entities_total,
        "T_entity": entity_tokens,
        "avg_tokens": tokens_total / sentences if sentences else 0.0,
        "avg_entities": entities_total / sentences if sentences else 0.0,
        "density_token_pct": 100.0 * entity_tokens / tokens_total if tokens_total else 0.0,
        "entities_per_100_tokens": 100.0 * entities_total / tokens_total if tokens_total else 0.0,
        "class_counts": {kind: class_counts[kind] for kind in ACTIVE_TYPES},
        "class_proportions_pct": {
            kind: (100.0 * class_counts[kind] / entities_total if entities_total else 0.0)
            for kind in ACTIVE_TYPES
        },
        "unique_vocab": len(vocabulary),
        "median_tokens": statistics.median(lengths) if lengths else 0.0,
        "p95_tokens": _percentile(lengths, 0.95),
        "no_entity_sentences": sum(c == 0 for c in counts),
        "no_entity_pct": 100.0 * sum(c == 0 for c in counts) / sentences if sentences else 0.0,
    }


def normalized_text(record: dict) -> str:
    """Normalisasi teks kanonis untuk pemeriksaan duplikasi & kebocoran antar-partisi."""
    text = unicodedata.normalize("NFKC", " ".join(record["tokens"]))
    return " ".join(WORD_PATTERN.findall(text)).casefold()


def _read_aliases(path: Path) -> dict[str, str]:
    aliases = {}
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        if not line.strip():
            continue
        values = line.split()
        if len(values) != 2:
            raise ValueError(f"Baris alias label tidak valid di {path}: {line!r}")
        aliases[values[0]] = values[1]
    return aliases


def _normalize_tag(raw: str, aliases: dict[str, str]) -> str:
    tag = aliases.get(raw, raw).strip().upper()
    if tag == "O":
        return tag
    if not re.fullmatch(r"[BI]-.+", tag):
        raise ValueError(f"Label tidak dikenali: {raw!r}")
    prefix, kind = tag.split("-", 1)
    kind = TYPE_ALIASES.get(kind, kind)
    if kind not in ALL_KNOWN_TYPES:
        raise ValueError(f"Tipe entitas tidak dikenal pada label {raw!r}")
    return f"{prefix}-{kind}"


def build_record(dataset: str, split: str, source_ref: str, tokens: list[str], raw_tags: list[str], aliases: dict[str, str]) -> dict:
    """Bangun satu record standar dengan pemetaan REG & TTL -> O."""
    if not tokens or len(tokens) != len(raw_tags):
        raise ValueError(f"Kalimat kosong atau panjang token/tag berbeda di {source_ref}")
    original_tags, changes, invalid_i = [], [], []
    for index, (token, raw_tag) in enumerate(zip(tokens, raw_tags)):
        tag = _normalize_tag(raw_tag, aliases)
        if tag != raw_tag:
            changes.append({"kind": "label_alias", "source_token": index, "from": raw_tag, "to": tag})
        if tag.startswith("I-") and (
            not original_tags or original_tags[-1] not in ("B-" + tag[2:], "I-" + tag[2:])
        ):
            invalid_i.append(index)
        original_tags.append(tag)
    tags = ["O" if tag[2:] in ("REG", "TTL") else tag for tag in original_tags]
    sentence_id = dataset + "-" + stable_json_hash({"source": source_ref, "tokens": tokens, "tags": raw_tags})[:20]
    return {
        "sentence_id": sentence_id,
        "dataset": dataset,
        "source_split": split,
        "source_refs": [source_ref],
        "tokens": list(tokens),
        "original_tags": original_tags,
        "tags": tags,
        "group_id": "",
        "changes": changes,
        "invalid_I_positions": invalid_i,
    }


class _UnionFind:
    def __init__(self, count: int):
        self.parent = list(range(count))
        self.size = [1] * count

    def find(self, item: int) -> int:
        while item != self.parent[item]:
            self.parent[item] = self.parent[self.parent[item]]
            item = self.parent[item]
        return item

    def union(self, left: int, right: int) -> None:
        left, right = self.find(left), self.find(right)
        if left == right:
            return
        if self.size[left] < self.size[right]:
            left, right = right, left
        self.parent[right] = left
        self.size[left] += self.size[right]


def _grams(text: str) -> set[str]:
    return {text[index:index + 5] for index in range(max(0, len(text) - 4))}


def _similar_sorted(left: list[int], right: list[int], threshold: float) -> bool:
    required = math.ceil(threshold * (len(left) + len(right)) / (1 + threshold) - 1e-12)
    i = j = overlap = 0
    while i < len(left) and j < len(right):
        if overlap + min(len(left) - i, len(right) - j) < required:
            return False
        if left[i] == right[j]:
            overlap += 1
            i += 1
            j += 1
        elif left[i] < right[j]:
            i += 1
        else:
            j += 1
    return overlap >= required


def duplicate_groups(records: list[dict], threshold: float = NEAR_THRESHOLD) -> tuple[dict[str, str], dict]:
    """Pengelompokan duplikat eksak dan near-duplicate (character 5-gram Jaccard >= 0.90)."""
    records = list(records)
    texts, representatives = {}, []
    for index, record in enumerate(records):
        text = normalized_text(record)
        texts.setdefault(text, []).append(index)
    union = _UnionFind(len(records))
    for members in texts.values():
        for member in members[1:]:
            union.union(members[0], member)
        if len(normalized_text(records[members[0]]).split()) >= 10:
            representatives.append(members[0])
    gram_sets = {index: _grams(normalized_text(records[index])) for index in representatives}
    frequencies = Counter()
    for values in gram_sets.values():
        frequencies.update(values)
    order = {
        gram: rank
        for rank, gram in enumerate(sorted(frequencies, key=lambda gram: (frequencies[gram], gram)))
    }
    ranked = {index: sorted(order[gram] for gram in values) for index, values in gram_sets.items()}
    del gram_sets, frequencies, order
    inverted = defaultdict(list)
    comparisons = links = 0
    for index in sorted(representatives, key=lambda item: (len(ranked[item]), normalized_text(records[item]))):
        values = ranked[index]
        size = len(values)
        if not size:
            continue
        prefix_size = size - math.ceil(threshold * size - 1e-12) + 1
        minimum_size = math.ceil(threshold * size - 1e-12)
        candidates = set()
        for gram in values[:prefix_size]:
            for previous in inverted[gram]:
                if len(ranked[previous]) >= minimum_size:
                    candidates.add(previous)
        for previous in candidates:
            if union.find(previous) == union.find(index):
                continue
            comparisons += 1
            if _similar_sorted(values, ranked[previous], threshold):
                union.union(previous, index)
                links += 1
        for gram in values[:prefix_size]:
            inverted[gram].append(index)
    members_by_root = defaultdict(list)
    for index in range(len(records)):
        members_by_root[union.find(index)].append(index)
    mapping, multi = {}, []
    for members in members_by_root.values():
        group_id = "grp-" + stable_json_hash(sorted({normalized_text(records[idx]) for idx in members}))[:20]
        for index in members:
            mapping[records[index]["sentence_id"]] = group_id
        if len(members) > 1:
            multi.append({
                "group_id": group_id,
                "sentence_ids": [records[idx]["sentence_id"] for idx in members],
            })
    return mapping, {
        "method": "exact_character_5gram_Jaccard_prefix_join",
        "threshold": threshold,
        "minimum_tokens": 10,
        "candidate_comparisons": comparisons,
        "near_links": links,
        "multi_record_groups": len(multi),
    }


def assert_no_leakage(prepared: dict[str, dict[str, list[dict]]]) -> dict:
    """Pastikan tidak ada group_id yang muncul di lebih dari satu partisi (train/validation/test)."""
    roles = defaultdict(set)
    ids = set()
    for dataset_key, splits in prepared.items():
        for split_name, records in splits.items():
            for record in records:
                sid = record["sentence_id"]
                if sid in ids:
                    raise ValueError(f"Sentence ID duplikat terdeteksi: {sid}")
                ids.add(sid)
                roles[record["group_id"]].add(split_name)
    violating = {gid: sorted(sp) for gid, sp in roles.items() if len(sp) > 1}
    if violating:
        raise ValueError(f"Kebocoran lintas-partisi terdeteksi pada grup: {violating}")
    return {
        "passed": True,
        "cross_partition_overlap_groups": 0,
        "scope": "global normalized exact text and character-5gram Jaccard >= 0.90 for >= 10 tokens",
    }


def load_and_prepare_corpora(
    data_dir: Path = DATA_DIR,
    prepared_dir: Path = PREPARED_DIR,
    split_seed: int = SPLIT_SEED,
) -> tuple[dict[str, dict[str, list[dict]]], dict]:
    """Muat NERGRIT Gold & Nemotron 18-Kelas Baru, lakukan anti-leakage screening, dan bagi 85/15."""
    aliases = {**GOLD_EXTRA_ALIASES, **_read_aliases(data_dir / "gold" / "labels-map.csv")}
    gold_rows = []
    for split, filename in (("train", "train.txt"), ("validation", "valid.txt"), ("test", "test.txt")):
        rel_path = f"gold/{filename}"
        token_buf, tag_buf, sent_idx = [], [], 0
        lines = (data_dir / "gold" / filename).read_text(encoding="utf-8-sig").splitlines() + [""]
        for line in lines:
            if not line.strip():
                if token_buf:
                    gold_rows.append(
                        build_record("gold", split, f"{rel_path}#{sent_idx}", token_buf, tag_buf, aliases)
                    )
                    sent_idx += 1
                    token_buf, tag_buf = [], []
                continue
            content = line.rstrip()
            values = content.rsplit("\t", 1) if "\t" in content else content.rsplit(None, 1)
            if len(values) != 2:
                raise ValueError(f"Baris CoNLL tidak valid di {rel_path}: {line!r}")
            token_buf.append(values[0])
            tag_buf.append(values[1])

    nemotron_rows = []
    nemotron_jsonl_path = data_dir / "nemotron_18class" / "corrected.jsonl"
    for idx, line in enumerate(nemotron_jsonl_path.read_text(encoding="utf-8").splitlines()):
        if not line.strip():
            continue
        item = json.loads(line)
        text = item.get("text", "")
        entities = item.get("entities", [])
        for ent in entities:
            if ent.get("type") in ("REG", "TTL") or ent.get("type") not in ALLOWED_TYPES_SET:
                raise ValueError(f"Entitas terlarang di corrected.jsonl#{idx}: {ent}")
        bio_pairs = align_entities_to_bio(text, entities)
        if not bio_pairs:
            raise ValueError(f"Kalimat kosong setelah tokenisasi di corrected.jsonl#{idx}")
        toks = [w for w, _ in bio_pairs]
        tags = [t for _, t in bio_pairs]
        nemotron_rows.append(
            build_record("nemotron_18class", "unassigned", f"nemotron_18class/corrected.jsonl#{idx}", toks, tags, {})
        )

    flat = gold_rows + nemotron_rows
    groups, near_report = duplicate_groups(flat, threshold=NEAR_THRESHOLD)
    by_group = defaultdict(list)
    for record in flat:
        record["group_id"] = groups[record["sentence_id"]]
        by_group[record["group_id"]].append(record)

    group_role = {}
    for group_id, recs in by_group.items():
        fixed = {r["source_split"] for r in recs if r["dataset"] == "gold"}
        if "test" in fixed:
            group_role[group_id] = "test"
        elif "validation" in fixed:
            group_role[group_id] = "validation"
        elif "train" in fixed:
            group_role[group_id] = "train"

    # Anti-leakage: jika ada kalimat Nemotron yang satu grup dengan Gold Test, eksklusi dari train/validation
    leakage_excluded = [
        r["sentence_id"]
        for r in nemotron_rows
        if group_role.get(r["group_id"]) == "test"
    ]
    eligible_nemotron = sum(1 for r in nemotron_rows if group_role.get(r["group_id"]) != "test")
    target_val = round(eligible_nemotron * 0.15)
    current_val = sum(1 for r in nemotron_rows if group_role.get(r["group_id"]) == "validation")

    free_groups = sorted(gid for gid in by_group if gid not in group_role)
    random.Random(split_seed).shuffle(free_groups)
    for gid in free_groups:
        nem_count = sum(1 for r in by_group[gid] if r["dataset"] == "nemotron_18class")
        improvement = abs(target_val - current_val) - abs(target_val - current_val - nem_count)
        role = "validation" if improvement > 0 else "train"
        group_role[gid] = role
        if role == "validation":
            current_val += nem_count

    prepared = {
        "gold": {"train": [], "validation": [], "test": []},
        "nemotron_18class": {"train": [], "validation": []},
    }
    gold_moves = []
    for record in gold_rows:
        role = group_role[record["group_id"]]
        record["assigned_split"] = role
        if record["source_split"] != role:
            gold_moves.append({
                "sentence_id": record["sentence_id"],
                "from": record["source_split"],
                "to": role,
            })
        prepared["gold"][role].append(record)

    for record in nemotron_rows:
        role = group_role[record["group_id"]]
        if role == "test":
            continue
        record["assigned_split"] = role
        prepared["nemotron_18class"][role].append(record)

    for dataset_key, splits in prepared.items():
        for split_name, recs in splits.items():
            recs.sort(key=lambda r: r["sentence_id"])

    leakage_check = assert_no_leakage(prepared)

    # Simpan partisi JSONL dan hitung statistik
    prepared_dir.mkdir(parents=True, exist_ok=True)
    stats_by_dataset = {}
    split_hashes = {}
    for dataset_key, splits in prepared.items():
        stats_by_dataset[dataset_key] = {}
        split_hashes[dataset_key] = {}
        all_recs = []
        for split_name, recs in splits.items():
            out_jsonl = prepared_dir / dataset_key / f"{split_name}.jsonl"
            out_jsonl.parent.mkdir(parents=True, exist_ok=True)
            with out_jsonl.open("w", encoding="utf-8", newline="\n") as handle:
                for rec in recs:
                    handle.write(json.dumps(rec, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n")
            split_hashes[dataset_key][split_name] = compute_sha256(out_jsonl)
            stats_by_dataset[dataset_key][split_name] = dataset_statistics(recs)
            all_recs.extend(recs)
        stats_by_dataset[dataset_key]["all"] = dataset_statistics(all_recs)

    manifest = {
        "format": "nemotron-18class-prepared-v1",
        "split_seed": split_seed,
        "near_threshold": NEAR_THRESHOLD,
        "labels": LABELS,
        "active_types": list(ACTIVE_TYPES),
        "near_duplicate_report": near_report,
        "gold_split_moves_count": len(gold_moves),
        "nemotron_test_leakage_excluded_count": len(leakage_excluded),
        "leakage_check": leakage_check,
        "split_hashes": split_hashes,
        "statistics": stats_by_dataset,
    }
    manifest["prepared_hash"] = stable_json_hash({
        "split_hashes": split_hashes,
        "labels": LABELS,
        "split_seed": split_seed,
    })

    manifest_path = prepared_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")

    # Ekspor tabel statistik korpus & distribusi 18 kelas ke CSV
    stat_rows = []
    for d_key, d_label in (("gold", "NERGRIT Gold"), ("nemotron_18class", "Nemotron 18-Kelas Baru")):
        for sp_name, sp_stats in stats_by_dataset[d_key].items():
            stat_rows.append({
                "dataset_key": d_key,
                "dataset_name": d_label,
                "split": sp_name,
                "sentences": sp_stats["S"],
                "tokens": sp_stats["T"],
                "entities": sp_stats["E"],
                "entity_tokens": sp_stats["T_entity"],
                "avg_tokens_per_sentence": round(sp_stats["avg_tokens"], 2),
                "avg_entities_per_sentence": round(sp_stats["avg_entities"], 2),
                "density_token_pct": round(sp_stats["density_token_pct"], 2),
                "entities_per_100_tokens": round(sp_stats["entities_per_100_tokens"], 2),
                "unique_vocab": sp_stats["unique_vocab"],
                "median_tokens": round(sp_stats["median_tokens"], 1),
                "p95_tokens": round(sp_stats["p95_tokens"], 1),
                "no_entity_sentences": sp_stats["no_entity_sentences"],
                "no_entity_pct": round(sp_stats["no_entity_pct"], 2),
            })
    write_csv_rows(TABLES_DIR / "dataset_statistics.csv", stat_rows)

    class_dist_rows = []
    gold_all_cls = stats_by_dataset["gold"]["all"]["class_counts"]
    gold_train_cls = stats_by_dataset["gold"]["train"]["class_counts"]
    gold_test_cls = stats_by_dataset["gold"]["test"]["class_counts"]
    nem_all_cls = stats_by_dataset["nemotron_18class"]["all"]["class_counts"]
    nem_train_cls = stats_by_dataset["nemotron_18class"]["train"]["class_counts"]
    nem_val_cls = stats_by_dataset["nemotron_18class"]["validation"]["class_counts"]

    for kind in ACTIVE_TYPES:
        class_dist_rows.append({
            "entity_class": kind,
            "gold_all": gold_all_cls[kind],
            "gold_train": gold_train_cls[kind],
            "gold_test": gold_test_cls[kind],
            "nemotron_18class_all": nem_all_cls[kind],
            "nemotron_18class_train": nem_train_cls[kind],
            "nemotron_18class_validation": nem_val_cls[kind],
        })
    write_csv_rows(TABLES_DIR / "per_class_distribution_corpus.csv", class_dist_rows)

    sync_to_drive(TABLES_DIR / "dataset_statistics.csv", "tables/dataset_statistics.csv")
    sync_to_drive(TABLES_DIR / "per_class_distribution_corpus.csv", "tables/per_class_distribution_corpus.csv")
    sync_to_drive(manifest_path, "prepared_manifest.json")

    return prepared, manifest


PREPARED_DATA, PREPARED_MANIFEST = load_and_prepare_corpora()

print("=" * 84)
print("📊 STATISTIK PARTISI KORPUS & PEMERIKSAAN ANTI-KEBOCORAN (ZERO TEST LEAKAGE)")
print(f"   Status Anti-Leakage   : LULUS (Overlap Lintas-Partisi = {PREPARED_MANIFEST['leakage_check']['cross_partition_overlap_groups']})")
print(f"   Eksklusi Kebocoran    : {PREPARED_MANIFEST['nemotron_test_leakage_excluded_count']} kalimat Nemotron terindikasi mirip Test Gold")
print("-" * 84)
print(f"   {'Dataset / Partisi':<30} | {'Kalimat (S)':>11} | {'Token (T)':>11} | {'Entitas (E)':>11} | {'E/Kal':>6} | {'D_tok%':>6}")
print("-" * 84)
for d_key, d_title in (("gold", "NERGRIT Gold"), ("nemotron_18class", "Nemotron 18-Class")):
    for sp in PREPARED_DATA[d_key]:
        st = PREPARED_MANIFEST["statistics"][d_key][sp]
        label_str = f"{d_title} ({sp})"
        print(
            f"   {label_str:<30} | {st['S']:>11,} | {st['T']:>11,} | {st['E']:>11,} | "
            f"{st['avg_entities']:>6.2f} | {st['density_token_pct']:>5.1f}%"
        )
print("-" * 84)
print("🏷️ DISTRIBUSI ENTITAS 18 KELAS (TOTAL KORPUS GOLD vs NEMOTRON 18-KELAS BARU):")
for kind in ACTIVE_TYPES:
    g_cnt = PREPARED_MANIFEST["statistics"]["gold"]["all"]["class_counts"][kind]
    n_cnt = PREPARED_MANIFEST["statistics"]["nemotron_18class"]["all"]["class_counts"][kind]
    g_test = PREPARED_MANIFEST["statistics"]["gold"]["test"]["class_counts"][kind]
    print(f"   - {kind:<4}: Gold All = {g_cnt:>6,} (Test = {g_test:>5,}) | Nemotron 18-Kelas Baru = {n_cnt:>6,}")
print("=" * 84)
