# =============================================================================
# SEL 6: WORD-ALIGNED LOSSLESS CHUNKING (256) & EVALUATOR SPAN CONLL EXACT-MATCH
# =============================================================================
import gc
import inspect

spans = entity_spans


def metrics_from_counts(counts: dict[str, dict[str, int]]) -> dict:
    """Hitung Micro, Macro, Weighted Precision/Recall/F1 dan metrik per kelas dari TP/FP/FN."""
    def score(tp: int, fp: int, fn: int) -> dict:
        precision = tp / (tp + fp) if tp + fp else 0.0
        recall = tp / (tp + fn) if tp + fn else 0.0
        f1 = 2 * tp / (2 * tp + fp + fn) if 2 * tp + fp + fn else 0.0
        return {
            "precision": precision,
            "recall": recall,
            "f1": f1,
            "support": tp + fn,
            "predicted": tp + fp,
            "tp": tp,
            "fp": fp,
            "fn": fn,
        }

    per_class = {kind: score(**values) for kind, values in counts.items()}
    micro = score(*(sum(row[key] for row in counts.values()) for key in ("tp", "fp", "fn")))
    total_support = micro["support"]
    result = {"micro_" + key: micro[key] for key in ("precision", "recall", "f1")}
    for key in ("precision", "recall", "f1"):
        result["macro_" + key] = (
            sum(x[key] for x in per_class.values()) / len(per_class) if per_class else 0.0
        )
        result["weighted_" + key] = (
            sum(x[key] * x["support"] for x in per_class.values()) / total_support
            if total_support else 0.0
        )
    result.update({
        "support": total_support,
        "predicted": micro["predicted"],
        "tp": micro["tp"],
        "fp": micro["fp"],
        "fn": micro["fn"],
        "per_class": per_class,
    })
    return result


def span_metrics(
    references: list[list[str]],
    predictions: list[list[str]],
    entity_types: tuple[str, ...] | list[str] = ACTIVE_TYPES,
) -> dict:
    """Evaluasi Exact Whole-Span Match tingkat CoNLL pada himpunan 18 kelas tetap."""
    if len(references) != len(predictions):
        raise ValueError("Jumlah kalimat referensi dan prediksi berbeda!")
    kinds = tuple(entity_types)
    counts = {kind: {"tp": 0, "fp": 0, "fn": 0} for kind in kinds}
    for truth, predicted in zip(references, predictions):
        if len(truth) != len(predicted):
            raise ValueError("Jumlah token kata referensi dan prediksi berbeda!")
        gold_set, pred_set = set(spans(truth)), set(spans(predicted))
        for group, key in ((gold_set & pred_set, "tp"), (pred_set - gold_set, "fp"), (gold_set - pred_set, "fn")):
            for _, _, kind in group:
                if kind not in counts:
                    raise ValueError(f"Tipe entitas tidak dikenal saat evaluasi: {kind}")
                counts[kind][key] += 1
    return metrics_from_counts(counts)


def chunk_record(
    record: dict,
    tokenizer,
    labels: list[str] = LABELS,
    max_length: int = MAX_SEQ_LENGTH,
    avoid_entity_boundaries: bool = True,
) -> list[dict]:
    """Potong kalimat panjang pada batas kata secara lossless (tanpa kehilangan token)."""
    tokens, tags = record["tokens"], record["tags"]
    if not tokens or len(tokens) != len(tags):
        raise ValueError(f"Panjang token/tag tidak valid untuk {record['sentence_id']}")
    unknown = set(tags) - set(labels)
    if unknown:
        raise ValueError(f"Tag model tidak dikenal: {sorted(unknown)}")
    capacity = max_length - tokenizer.num_special_tokens_to_add(pair=False)
    if capacity <= 0:
        raise ValueError("Tidak ada kapasitas token tersisa setelah special tokens")

    full = tokenizer(
        tokens,
        is_split_into_words=True,
        add_special_tokens=False,
        truncation=False,
        return_attention_mask=False,
    )
    word_ids = full.word_ids()
    lengths = [0] * len(tokens)
    for word in word_ids:
        if word is not None:
            lengths[word] += 1

    missing = [index for index, length in enumerate(lengths) if length == 0]
    if missing:
        unknown_word = getattr(tokenizer, "unk_token", None)
        if not unknown_word:
            raise ValueError("Tokenizer tidak memiliki unk_token untuk token kosong/spasi")
        tokens = list(tokens)
        for index in missing:
            tokens[index] = unknown_word
        full = tokenizer(
            tokens,
            is_split_into_words=True,
            add_special_tokens=False,
            truncation=False,
            return_attention_mask=False,
        )
        lengths = [0] * len(tokens)
        for word in full.word_ids():
            if word is not None:
                lengths[word] += 1

    if any(length == 0 or length > capacity for length in lengths):
        raise ValueError(f"Terdapat kata yang melebihi kapasitas subword pada {record['sentence_id']}")

    entity_ranges = spans(tags) if avoid_entity_boundaries else []
    for start, end, _ in entity_ranges:
        if sum(lengths[start:end]) > capacity:
            raise ValueError(f"Rentang entitas melebihi kapasitas input di {record['sentence_id']}:{start}:{end}")

    label2id = {tag: i for i, tag in enumerate(labels)}
    chunks, start = [], 0
    while start < len(tokens):
        end, used = start, 0
        while end < len(tokens) and used + lengths[end] <= capacity:
            used += lengths[end]
            end += 1
        for ent_start, ent_end, _ in entity_ranges:
            if ent_start < end < ent_end:
                end = ent_start
                break
        if end <= start:
            raise ValueError(f"Tidak dapat membentuk chunk lossless untuk {record['sentence_id']}")
        encoded = tokenizer(
            tokens[start:end],
            is_split_into_words=True,
            add_special_tokens=True,
            truncation=False,
        )
        if len(encoded["input_ids"]) > max_length:
            raise ValueError("Panjang subword melampaui max_length saat chunking")
        local_ids = encoded.word_ids()
        aligned, first_positions, previous = [], [], None
        for position, word in enumerate(local_ids):
            if word is None or word == previous:
                aligned.append(-100)
            else:
                aligned.append(label2id[tags[start + word]])
                first_positions.append(position)
            previous = word
        if len(first_positions) != end - start:
            raise ValueError("Tokenizer gagal mempertahankan setiap kata sumber")
        inputs = {
            key: value
            for key, value in encoded.items()
            if key in ("input_ids", "attention_mask", "token_type_ids")
        }
        inputs["labels"] = aligned
        chunks.append({
            "inputs": inputs,
            "sentence_id": record["sentence_id"],
            "start": start,
            "end": end,
            "first_positions": first_positions,
            "unk_source_positions": [idx for idx in missing if start <= idx < end],
        })
        start = end
    return chunks


def recombine_predictions(
    records: list[dict],
    chunks: list[dict],
    predicted_ids: list,
    labels: list[str] = LABELS,
) -> list[list[str]]:
    """Gabungkan kembali prediksi tingkat chunk menjadi prediksi kata utuh tingkat kalimat."""
    if len(chunks) != len(predicted_ids):
        raise ValueError("Jumlah chunk dan prediksi tidak cocok")
    by_id = {row["sentence_id"]: [None] * len(row["tokens"]) for row in records}
    if len(by_id) != len(records):
        raise ValueError("Terdapat duplikasi sentence_id pada records")
    for chunk, ids in zip(chunks, predicted_ids):
        words = by_id[chunk["sentence_id"]]
        for offset, position in enumerate(chunk["first_positions"]):
            absolute = chunk["start"] + offset
            if words[absolute] is not None:
                raise ValueError("Satu kata diprediksi lebih dari satu kali")
            words[absolute] = labels[int(ids[position])]
    if any(tag is None for tags in by_id.values() for tag in tags):
        raise ValueError("Terdapat kata yang belum memiliki hasil prediksi")
    return [by_id[row["sentence_id"]] for row in records]


def _file_hashes(root: Path) -> dict[str, str]:
    root = Path(root)
    result = {}
    for path in sorted(root.rglob("*")):
        if path.is_file():
            rel = str(path.relative_to(root)).replace("\\", "/")
            result[rel] = compute_sha256(path)
    return result


def _trainer_tokenizer_kwarg(tokenizer) -> dict:
    from transformers import Trainer
    sig = inspect.signature(Trainer.__init__).parameters
    return {"processing_class" if "processing_class" in sig else "tokenizer": tokenizer}


def build_training_arguments(config: dict, run_dir: Path, seed: int):
    """Bangun TrainingArguments yang 100% sesuai spesifikasi Tabel 3.2 skripsi."""
    from transformers import TrainingArguments
    sig = inspect.signature(TrainingArguments.__init__).parameters
    use_workers = config["dataloader_num_workers"] if CUDA_AVAILABLE else 0
    values = dict(
        output_dir=str(Path(run_dir) / "checkpoints"),
        per_device_train_batch_size=config["train_batch_size"],
        gradient_accumulation_steps=config["gradient_accumulation_steps"],
        per_device_eval_batch_size=config["eval_batch_size"],
        learning_rate=config["learning_rate"],
        weight_decay=config["weight_decay"],
        adam_beta1=config["adam_beta1"],
        adam_beta2=config["adam_beta2"],
        adam_epsilon=config["adam_epsilon"],
        lr_scheduler_type=config["lr_scheduler_type"],
        num_train_epochs=config["num_train_epochs"],
        max_grad_norm=config["max_grad_norm"],
        fp16=bool(config["fp16"] and CUDA_AVAILABLE),
        bf16=bool(config["bf16"] and CUDA_AVAILABLE),
        tf32=False,
        gradient_checkpointing=config["gradient_checkpointing"],
        save_strategy="epoch",
        logging_strategy="epoch",
        load_best_model_at_end=True,
        metric_for_best_model=config["metric_for_best_model"],
        greater_is_better=True,
        save_total_limit=1,
        restore_callback_states_from_checkpoint=True,
        seed=seed,
        data_seed=seed,
        report_to="none",
        dataloader_num_workers=use_workers,
        dataloader_pin_memory=bool(CUDA_AVAILABLE),
        dataloader_persistent_workers=bool(use_workers > 0),
        label_smoothing_factor=0.0,
        optim=config["optim"],
        full_determinism=False,
    )
    if "warmup_ratio" in sig:
        values["warmup_ratio"] = config["warmup_ratio"]
    else:
        values["warmup_steps"] = config["warmup_ratio"]
    eval_key = "eval_strategy" if "eval_strategy" in sig else "evaluation_strategy"
    values[eval_key] = "epoch"
    allowed = set(sig)
    return TrainingArguments(**{k: v for k, v in values.items() if k in allowed})


def load_initial_indobert_model(config: dict):
    """Muat model indobenchmark/indobert-large-p1 dengan 37 tag BIO dan dropout=0.1."""
    from transformers import AutoConfig, AutoModelForTokenClassification
    labels = config["labels"]
    model_config = AutoConfig.from_pretrained(
        config["model_checkpoint"],
        revision=config.get("model_revision"),
    )
    model_config.num_labels = len(labels)
    model_config.id2label = dict(enumerate(labels))
    model_config.label2id = {tag: i for i, tag in enumerate(labels)}
    model_config.hidden_dropout_prob = config["dropout"]
    model_config.attention_probs_dropout_prob = config["dropout"]
    model_config.classifier_dropout = config["dropout"]
    init_kwargs = dict(
        pretrained_model_name_or_path=config["model_checkpoint"],
        revision=config.get("model_revision"),
        config=model_config,
        ignore_mismatched_sizes=False,
    )
    sig = inspect.signature(AutoModelForTokenClassification.from_pretrained).parameters
    if "dtype" in sig:
        init_kwargs["dtype"] = torch.float32
    else:
        init_kwargs["torch_dtype"] = torch.float32
    return AutoModelForTokenClassification.from_pretrained(**init_kwargs)


def train_scenario_model(
    dataset_key: str,
    history_prefix: str,
    seed: int,
    train_records: list[dict],
    val_records: list[dict],
    tokenizer,
    config: dict = CONFIG,
    runs_dir: Path = RUNS_DIR,
) -> dict:
    """Latih atau pulihkan model untuk satu skenario dan cadangkan otomatis ke Google Drive."""
    from datasets import Dataset
    from transformers import DataCollatorForTokenClassification, EarlyStoppingCallback, Trainer

    run_id = f"{dataset_key}_s{seed}"
    run_dir = runs_dir / run_id
    drive_run_dir = DRIVE_BASE_DIR / "runs" / run_id
    manifest_path = run_dir / "run_manifest.json"
    best_model_dir = run_dir / "best_model"

    train_hash = stable_json_hash([
        {"sentence_id": r["sentence_id"], "tokens": r["tokens"], "tags": r["tags"]}
        for r in train_records
    ])
    val_hash = stable_json_hash([
        {"sentence_id": r["sentence_id"], "tokens": r["tokens"], "tags": r["tags"]}
        for r in val_records
    ])

    # 1. Cek apakah run sudah selesai di lokal atau di Google Drive (mendukung auto-resume penuh)
    if not manifest_path.is_file() and (drive_run_dir / "run_manifest.json").is_file():
        try:
            drive_manifest = json.loads((drive_run_dir / "run_manifest.json").read_text(encoding="utf-8"))
            if (
                drive_manifest.get("status") == "complete"
                and drive_manifest.get("train_hash") == train_hash
                and (drive_run_dir / "best_model" / "config.json").is_file()
            ):
                print(f"☁️ Memulihkan model {run_id} yang telah selesai dari Google Drive...")
                shutil.copytree(drive_run_dir, run_dir, dirs_exist_ok=True)
        except Exception as exc:
            print(f"⚠️ Gagal memulihkan {run_id} dari Google Drive: {exc}")

    if manifest_path.is_file():
        existing = json.loads(manifest_path.read_text(encoding="utf-8"))
        if (
            existing.get("status") == "complete"
            and existing.get("train_hash") == train_hash
            and (best_model_dir / "config.json").is_file()
        ):
            hist_csv_path = HISTORIES_DIR / f"{history_prefix}_s{seed}.csv"
            hist_json_path = HISTORIES_DIR / f"{history_prefix}_s{seed}.json"
            if (run_dir / "training_history.csv").is_file() and not hist_csv_path.is_file():
                shutil.copy2(run_dir / "training_history.csv", hist_csv_path)
            if (run_dir / "training_history.json").is_file() and not hist_json_path.is_file():
                shutil.copy2(run_dir / "training_history.json", hist_json_path)
            print(f"✅ Run {run_id} sudah selesai dan terverifikasi. Melewati pelatihan ulang.")
            return existing

    # 2. Chunking kalimat latih & validasi
    print(f"✂️ Melakukan word-aligned chunking (max_length={config['max_seq_length']}) untuk {run_id}...")
    train_chunks = []
    for rec in train_records:
        train_chunks.extend(
            chunk_record(rec, tokenizer, config["labels"], config["max_seq_length"], avoid_entity_boundaries=True)
        )
    val_chunks = []
    for rec in val_records:
        val_chunks.extend(
            chunk_record(rec, tokenizer, config["labels"], config["max_seq_length"], avoid_entity_boundaries=False)
        )
    print(
        f"   Train: {len(train_records):,} kalimat -> {len(train_chunks):,} chunks | "
        f"Validasi: {len(val_records):,} kalimat -> {len(val_chunks):,} chunks"
    )

    run_dir.mkdir(parents=True, exist_ok=True)
    ckpt_root = run_dir / "checkpoints"
    resume_ckpt = None
    if ckpt_root.is_dir():
        ckpts = sorted(
            (p for p in ckpt_root.glob("checkpoint-*") if p.is_dir() and re.fullmatch(r"checkpoint-\d+", p.name)),
            key=lambda p: int(p.name.rsplit("-", 1)[-1]),
        )
        if ckpts:
            resume_ckpt = str(ckpts[-1])
            print(f"🔄 Melanjutkan pelatihan {run_id} dari checkpoint: {resume_ckpt}")

    configure_reproducibility(seed)
    model = load_initial_indobert_model(config)

    labels = config["labels"]
    kinds = tuple(config["active_types"])

    def compute_metrics(eval_pred):
        logits = eval_pred.predictions[0] if isinstance(eval_pred.predictions, tuple) else eval_pred.predictions
        pred_ids = logits.argmax(axis=-1)
        pred_tags = recombine_predictions(val_records, val_chunks, pred_ids, labels)
        scores = span_metrics([row["tags"] for row in val_records], pred_tags, kinds)
        return {k: v for k, v in scores.items() if k != "per_class"}

    trainer = Trainer(
        model=model,
        args=build_training_arguments(config, run_dir, seed),
        train_dataset=Dataset.from_list([c["inputs"] for c in train_chunks]),
        eval_dataset=Dataset.from_list([c["inputs"] for c in val_chunks]),
        data_collator=DataCollatorForTokenClassification(
            tokenizer, pad_to_multiple_of=config["pad_to_multiple_of"]
        ),
        compute_metrics=compute_metrics,
        callbacks=[
            EarlyStoppingCallback(
                early_stopping_patience=config["early_stopping_patience"],
                early_stopping_threshold=config["early_stopping_threshold"],
            )
        ],
        **_trainer_tokenizer_kwarg(tokenizer),
    )

    print(f"🚀 Memulai fine-tuning {run_id} pada {GPU_NAME} ({PRECISION_MODE.upper()})...")
    t_start = time.time()
    train_output = trainer.train(resume_from_checkpoint=resume_ckpt)
    elapsed_sec = time.time() - t_start

    # 3. Simpan model terbaik, tokenizer, dan riwayat pelatihan
    best_model_dir.mkdir(parents=True, exist_ok=True)
    trainer.save_model(str(best_model_dir))
    tokenizer.save_pretrained(str(best_model_dir))

    log_history = list(trainer.state.log_history)
    (run_dir / "training_history.json").write_text(
        json.dumps(log_history, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    write_csv_rows(run_dir / "training_history.csv", log_history)

    # Salin ke direktori histories/ untuk arsip akhir
    hist_csv_path = HISTORIES_DIR / f"{history_prefix}_s{seed}.csv"
    hist_json_path = HISTORIES_DIR / f"{history_prefix}_s{seed}.json"
    write_csv_rows(hist_csv_path, log_history)
    hist_json_path.write_text(json.dumps(log_history, indent=2, ensure_ascii=False), encoding="utf-8")

    trainer_state_dict = (
        trainer.state.to_dict() if hasattr(trainer.state, "to_dict") else vars(trainer.state)
    )
    (run_dir / "trainer_state.json").write_text(
        json.dumps(trainer_state_dict, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    manifest = {
        "status": "complete",
        "run_id": run_id,
        "dataset": dataset_key,
        "history_prefix": history_prefix,
        "seed": seed,
        "model_checkpoint": config["model_checkpoint"],
        "precision_mode": PRECISION_MODE,
        "gpu_name": GPU_NAME,
        "train_sentences": len(train_records),
        "train_chunks": len(train_chunks),
        "train_tokens": sum(len(r["tokens"]) for r in train_records),
        "train_entities": sum(len(spans(r["tags"])) for r in train_records),
        "validation_sentences": len(val_records),
        "validation_chunks": len(val_chunks),
        "train_hash": train_hash,
        "validation_hash": val_hash,
        "best_checkpoint": trainer.state.best_model_checkpoint,
        "best_validation_macro_f1": float(trainer.state.best_metric or 0.0),
        "epochs_completed": float(trainer.state.epoch or 0.0),
        "optimizer_steps": int(trainer.state.global_step or 0),
        "elapsed_seconds": round(elapsed_sec, 2),
        "elapsed_minutes": round(elapsed_sec / 60.0, 2),
        "training_metrics": train_output.metrics,
        "model_files": _file_hashes(best_model_dir),
    }
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")

    # 4. Bersihkan checkpoint optimizer sementara setelah best_model aman
    if ckpt_root.is_dir():
        shutil.rmtree(ckpt_root, ignore_errors=True)

    del trainer, model
    gc.collect()
    if CUDA_AVAILABLE:
        torch.cuda.empty_cache()

    # 5. Cadangkan otomatis ke Google Drive
    print(f"☁️ Mencadangkan artefak {run_id} ke Google Drive...")
    for fname in ("run_manifest.json", "training_history.json", "training_history.csv", "trainer_state.json"):
        sync_to_drive(run_dir / fname, f"runs/{run_id}/{fname}")
    sync_to_drive(hist_csv_path, f"histories/{hist_csv_path.name}")
    sync_to_drive(hist_json_path, f"histories/{hist_json_path.name}")
    if config.get("save_best_weights_to_drive", True):
        sync_to_drive(best_model_dir, f"runs/{run_id}/best_model", verify_hash=False)

    return manifest


def predict_with_model(
    model_dir: Path,
    records: list[dict],
    tokenizer,
    config: dict = CONFIG,
    work_dir: Path | None = None,
) -> list[list[str]]:
    """Jalankan inferensi label-blind pada himpunan uji dan gabungkan kembali ke token kata."""
    from datasets import Dataset
    from transformers import AutoModelForTokenClassification, DataCollatorForTokenClassification, Trainer, TrainingArguments

    blind_records = [{**rec, "tags": ["O"] * len(rec["tokens"])} for rec in records]
    chunks = []
    for rec in blind_records:
        chunks.extend(
            chunk_record(rec, tokenizer, config["labels"], config["max_seq_length"], avoid_entity_boundaries=False)
        )

    init_kwargs = dict(pretrained_model_name_or_path=str(model_dir))
    sig = inspect.signature(AutoModelForTokenClassification.from_pretrained).parameters
    if "dtype" in sig:
        init_kwargs["dtype"] = torch.float32
    else:
        init_kwargs["torch_dtype"] = torch.float32
    model = AutoModelForTokenClassification.from_pretrained(**init_kwargs)

    tmp_eval_dir = str(work_dir or (OUTPUT_DIR / "eval_runtime"))
    eval_args = TrainingArguments(
        output_dir=tmp_eval_dir,
        per_device_eval_batch_size=config["eval_batch_size"],
        report_to="none",
        fp16=bool(config["fp16"] and CUDA_AVAILABLE),
        bf16=bool(config["bf16"] and CUDA_AVAILABLE),
        tf32=False,
        dataloader_num_workers=0,
    )
    trainer = Trainer(
        model=model,
        args=eval_args,
        data_collator=DataCollatorForTokenClassification(
            tokenizer, pad_to_multiple_of=config["pad_to_multiple_of"]
        ),
        **_trainer_tokenizer_kwarg(tokenizer),
    )
    output = trainer.predict(Dataset.from_list([c["inputs"] for c in chunks]))
    logits = output.predictions[0] if isinstance(output.predictions, tuple) else output.predictions
    pred_ids = logits.argmax(axis=-1)
    predictions = recombine_predictions(records, chunks, pred_ids, config["labels"])

    del trainer, model, output, logits
    gc.collect()
    if CUDA_AVAILABLE:
        torch.cuda.empty_cache()
    return predictions


def export_predictions(base_path: Path, records: list[dict], predictions: list[list[str]]) -> tuple[Path, Path]:
    """Ekspor hasil prediksi token demi token ke format .jsonl dan .conll."""
    base_path = Path(base_path)
    base_path.parent.mkdir(parents=True, exist_ok=True)
    jsonl_path = base_path.with_suffix(".jsonl")
    conll_path = base_path.with_suffix(".conll")
    with jsonl_path.open("w", encoding="utf-8") as jf, conll_path.open("w", encoding="utf-8") as cf:
        for rec, pred_tags in zip(records, predictions):
            jf.write(
                json.dumps(
                    {
                        "sentence_id": rec["sentence_id"],
                        "tokens": rec["tokens"],
                        "reference_tags": rec["tags"],
                        "predicted_tags": pred_tags,
                        "reference_entities": [
                            {"start": s, "end": e, "type": k, "text": " ".join(rec["tokens"][s:e])}
                            for s, e, k in spans(rec["tags"])
                        ],
                        "predicted_entities": [
                            {"start": s, "end": e, "type": k, "text": " ".join(rec["tokens"][s:e])}
                            for s, e, k in spans(pred_tags)
                        ],
                    },
                    ensure_ascii=False,
                )
                + "\n"
            )
            cf.write(f"# sentence_id = {rec['sentence_id']}\n")
            for tok, ref_tag, pred_tag in zip(rec["tokens"], rec["tags"], pred_tags):
                cf.write(f"{tok}\t{ref_tag}\t{pred_tag}\n")
            cf.write("\n")
    return jsonl_path, conll_path


# Uji Mandiri (Self-Test) Evaluator Span CoNLL
_dummy_ref = [["B-PER", "I-PER", "O", "B-GPE", "O", "B-NOR"]]
_dummy_pred = [["B-PER", "I-PER", "O", "B-LOC", "O", "B-NOR"]]
_dummy_score = span_metrics(_dummy_ref, _dummy_pred, ACTIVE_TYPES)
assert _dummy_score["tp"] == 2 and _dummy_score["fp"] == 1 and _dummy_score["fn"] == 1
print("✅ Fungsi chunk_record, recombine_predictions, dan span_metrics siap digunakan.")
