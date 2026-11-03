# =============================================================================
# SEL 9: EVALUASI HEAD-TO-HEAD PADA NERGRIT GOLD TEST SET (AGREGAT & PER KELAS)
# =============================================================================

# Referensi Skor Bab 4 Sebelum Verifikasi Ulang 18-Kelas (untuk Perbandingan Dampak Pembersihan)
HISTORICAL_BAB4_REFERENCE = {
    "gold_bab4_seed42": {
        "micro_precision": 0.8365,
        "micro_recall": 0.8422,
        "micro_f1": 0.8393,
        "macro_f1": 0.7552,
        "weighted_f1": 0.8380,
        "support": 8890,
    },
    "nemotron_old_seed42": {
        "micro_precision": 0.5474,
        "micro_recall": 0.5111,
        "micro_f1": 0.5286,
        "macro_f1": 0.4181,
        "weighted_f1": 0.5083,
        "support": 8890,
    },
    "nemotron_old_mean_3seeds": {
        "micro_precision": 0.5413,
        "micro_recall": 0.5056,
        "micro_f1": 0.5228,
        "macro_f1": 0.4176,
        "weighted_f1": 0.5030,
        "support": 8890,
        "per_class_f1": {
            "CRD": 0.6617, "DAT": 0.4313, "EVT": 0.5668, "FAC": 0.2067,
            "GPE": 0.7485, "LAN": 0.0000, "LAW": 0.3671, "LOC": 0.1550,
            "MON": 0.7298, "NOR": 0.0121, "ORD": 0.5691, "ORG": 0.4423,
            "PER": 0.7327, "PRC": 0.8911, "PRD": 0.2673, "QTY": 0.1955,
            "TIM": 0.4155, "WOA": 0.1237,
        },
    },
    "gold_bab4_mean_3seeds_per_class_f1": {
        "CRD": 0.8880, "DAT": 0.9471, "EVT": 0.7059, "FAC": 0.4585,
        "GPE": 0.8912, "LAN": 0.0000, "LAW": 0.7110, "LOC": 0.6227,
        "MON": 0.9712, "NOR": 0.7983, "ORD": 0.7619, "ORG": 0.7520,
        "PER": 0.9657, "PRC": 0.9441, "PRD": 0.6875, "QTY": 0.6451,
        "TIM": 0.9430, "WOA": 1.0000,
    },
}

ENTITY_CLASS_DESCRIPTIONS = {
    "CRD": "Bilangan Kardinal (Cardinal)",
    "DAT": "Tanggal Kalender (Date)",
    "EVT": "Peristiwa / Acara (Event)",
    "FAC": "Fasilitas Bangunan / Infrastruktur (Facility)",
    "GPE": "Entitas Geo-Politik (Negara, Kota, Provinsi)",
    "LAN": "Bahasa Tertutur / Tertulis (Language)",
    "LAW": "Hukum dan Perundang-undangan (Law)",
    "LOC": "Lokasi Non-Geopolitik (Gunung, Sungai, Wilayah)",
    "MON": "Jumlah Nilai Uang (Money)",
    "NOR": "Kebangsaan, Agama, Suku, Jabatan Politik/Negara (NORP)",
    "ORD": "Bilangan Ordinal / Tingkatan (Ordinal)",
    "ORG": "Organisasi, Perusahaan, Lembaga (Organization)",
    "PER": "Nama Individu / Tokoh Manusia (Person)",
    "PRC": "Nilai Persentase (Percent)",
    "PRD": "Nama Produk / Sarana Transportasi / Komoditas (Product)",
    "QTY": "Besaran Ukuran Fisik / Durasi Kuantitas (Quantity)",
    "TIM": "Waktu Jam Spesifik (Time)",
    "WOA": "Karya Cipta Seni / Sastra / Film (Work of Art)",
}


def evaluate_all_scenarios_on_gold_test(
    test_records: list[dict],
    tokenizer,
    seeds: list[int] = TRAINING_SEEDS,
    runs_dir: Path = RUNS_DIR,
    predictions_dir: Path = PREDICTIONS_DIR,
    tables_dir: Path = TABLES_DIR,
) -> dict:
    """Jalankan inferensi kedua model pada Gold Test Set dan susun tabel komparasi lengkap."""
    ref_tags = [rec["tags"] for rec in test_records]
    evaluation_results = {"gold": {}, "nemotron_18class": {}}
    predictions_by_run = {"gold": {}, "nemotron_18class": {}}

    scenario_specs = (
        ("gold", "gold", "NERGRIT Gold Baseline"),
        ("nemotron_18class", "nemotron", "Nemotron 18-Kelas Baru (Terverifikasi)"),
    )

    for dataset_key, file_prefix, label_title in scenario_specs:
        for seed in seeds:
            run_id = f"{dataset_key}_s{seed}"
            model_dir = runs_dir / run_id / "best_model"
            if not (model_dir / "config.json").is_file():
                drive_model_dir = DRIVE_BASE_DIR / "runs" / run_id / "best_model"
                if (drive_model_dir / "config.json").is_file():
                    print(f"☁️ Memulihkan best_model {run_id} dari Google Drive...")
                    shutil.copytree(drive_model_dir, model_dir, dirs_exist_ok=True)
                else:
                    raise FileNotFoundError(f"Model terbaik tidak ditemukan untuk {run_id} di {model_dir}")

            print(f"🔍 Mengevaluasi {label_title} ({run_id}) pada NERGRIT Gold Test Set ({len(test_records):,} kalimat)...")
            pred_tags = predict_with_model(
                model_dir=model_dir,
                records=test_records,
                tokenizer=tokenizer,
                config=CONFIG,
                work_dir=OUTPUT_DIR / "eval_runtime" / run_id,
            )
            predictions_by_run[dataset_key][seed] = pred_tags

            base_pred_path = predictions_dir / f"{file_prefix}_s{seed}_test_predictions"
            jsonl_p, conll_p = export_predictions(base_pred_path, test_records, pred_tags)
            sync_to_drive(jsonl_p, f"predictions/{jsonl_p.name}")
            sync_to_drive(conll_p, f"predictions/{conll_p.name}")

            if dataset_key == "nemotron_18class":
                alias_base = predictions_dir / f"nemotron_18class_s{seed}_test_predictions"
                a_jsonl, a_conll = export_predictions(alias_base, test_records, pred_tags)
                sync_to_drive(a_jsonl, f"predictions/{a_jsonl.name}")
                sync_to_drive(a_conll, f"predictions/{a_conll.name}")

            metrics = span_metrics(ref_tags, pred_tags, ACTIVE_TYPES)
            evaluation_results[dataset_key][seed] = metrics

    # Susun Tabel Komparasi Agregat (overall_comparison.csv)
    overall_rows = []
    metric_keys = (
        "micro_precision", "micro_recall", "micro_f1",
        "macro_precision", "macro_recall", "macro_f1",
        "weighted_precision", "weighted_recall", "weighted_f1",
    )

    for dataset_key, file_prefix, label_title in scenario_specs:
        for seed in seeds:
            m = evaluation_results[dataset_key][seed]
            row = {
                "scenario_key": dataset_key,
                "scenario_name": label_title,
                "seed": str(seed),
                "test_sentences": len(test_records),
                "support": m["support"],
                "predicted": m["predicted"],
                "tp": m["tp"],
                "fp": m["fp"],
                "fn": m["fn"],
            }
            for mk in metric_keys:
                row[mk] = round(m[mk], 6)
                row[mk + "_pct"] = round(m[mk] * 100.0, 2)
            overall_rows.append(row)

        if len(seeds) >= 1:
            mean_row = {
                "scenario_key": dataset_key,
                "scenario_name": f"{label_title} (Mean)",
                "seed": "mean",
                "test_sentences": len(test_records),
                "support": evaluation_results[dataset_key][seeds[0]]["support"],
                "predicted": round(statistics.mean(evaluation_results[dataset_key][s]["predicted"] for s in seeds), 1),
                "tp": round(statistics.mean(evaluation_results[dataset_key][s]["tp"] for s in seeds), 1),
                "fp": round(statistics.mean(evaluation_results[dataset_key][s]["fp"] for s in seeds), 1),
                "fn": round(statistics.mean(evaluation_results[dataset_key][s]["fn"] for s in seeds), 1),
            }
            for mk in metric_keys:
                vals = [evaluation_results[dataset_key][s][mk] for s in seeds]
                mean_val = statistics.mean(vals)
                std_val = statistics.stdev(vals) if len(vals) > 1 else 0.0
                mean_row[mk] = round(mean_val, 6)
                mean_row[mk + "_pct"] = round(mean_val * 100.0, 2)
                mean_row[mk + "_std_pct"] = round(std_val * 100.0, 2)
            overall_rows.append(mean_row)

    # Tambahkan baris referensi Nemotron Lama (Bab 4 Sebelum Verifikasi 18-Kelas) untuk perbandingan langsung
    old_s42 = HISTORICAL_BAB4_REFERENCE["nemotron_old_seed42"]
    overall_rows.append({
        "scenario_key": "nemotron_old_bab4_ref",
        "scenario_name": "Nemotron Lama (Referensi Bab 4 Sebelum Verifikasi 18-Kelas)",
        "seed": "42",
        "test_sentences": len(test_records),
        "support": old_s42["support"],
        "predicted": 0,
        "tp": 0,
        "fp": 0,
        "fn": 0,
        "micro_precision": old_s42["micro_precision"],
        "micro_recall": old_s42["micro_recall"],
        "micro_f1": old_s42["micro_f1"],
        "macro_precision": 0.0,
        "macro_recall": 0.0,
        "macro_f1": old_s42["macro_f1"],
        "weighted_precision": 0.0,
        "weighted_recall": 0.0,
        "weighted_f1": old_s42["weighted_f1"],
        "micro_precision_pct": round(old_s42["micro_precision"] * 100.0, 2),
        "micro_recall_pct": round(old_s42["micro_recall"] * 100.0, 2),
        "micro_f1_pct": round(old_s42["micro_f1"] * 100.0, 2),
        "macro_precision_pct": 0.0,
        "macro_recall_pct": 0.0,
        "macro_f1_pct": round(old_s42["macro_f1"] * 100.0, 2),
        "weighted_precision_pct": 0.0,
        "weighted_recall_pct": 0.0,
        "weighted_f1_pct": round(old_s42["weighted_f1"] * 100.0, 2),
    })

    # Hitung Delta (Nemotron 18-Kelas Baru vs Nemotron Lama & vs Gold Baseline)
    primary_seed = seeds[0]
    gold_m = evaluation_results["gold"][primary_seed]
    nem_m = evaluation_results["nemotron_18class"][primary_seed]

    delta_vs_old = {
        "micro_precision_pct_delta": round((nem_m["micro_precision"] - old_s42["micro_precision"]) * 100.0, 2),
        "micro_recall_pct_delta": round((nem_m["micro_recall"] - old_s42["micro_recall"]) * 100.0, 2),
        "micro_f1_pct_delta": round((nem_m["micro_f1"] - old_s42["micro_f1"]) * 100.0, 2),
        "macro_f1_pct_delta": round((nem_m["macro_f1"] - old_s42["macro_f1"]) * 100.0, 2),
        "weighted_f1_pct_delta": round((nem_m["weighted_f1"] - old_s42["weighted_f1"]) * 100.0, 2),
    }
    delta_vs_gold = {
        "micro_precision_pct_delta": round((nem_m["micro_precision"] - gold_m["micro_precision"]) * 100.0, 2),
        "micro_recall_pct_delta": round((nem_m["micro_recall"] - gold_m["micro_recall"]) * 100.0, 2),
        "micro_f1_pct_delta": round((nem_m["micro_f1"] - gold_m["micro_f1"]) * 100.0, 2),
        "macro_f1_pct_delta": round((nem_m["macro_f1"] - gold_m["macro_f1"]) * 100.0, 2),
        "weighted_f1_pct_delta": round((nem_m["weighted_f1"] - gold_m["weighted_f1"]) * 100.0, 2),
    }

    # Susun Tabel Per Kelas 18 Kelas (per_class_18_comparison.csv)
    per_class_rows = []
    old_per_class = HISTORICAL_BAB4_REFERENCE["nemotron_old_mean_3seeds"]["per_class_f1"]
    for kind in ACTIVE_TYPES:
        g_cls = gold_m["per_class"][kind]
        n_cls = nem_m["per_class"][kind]
        old_f1 = old_per_class.get(kind, 0.0)
        per_class_rows.append({
            "entity_class": kind,
            "description": ENTITY_CLASS_DESCRIPTIONS.get(kind, kind),
            "support": g_cls["support"],
            "gold_precision_pct": round(g_cls["precision"] * 100.0, 2),
            "gold_recall_pct": round(g_cls["recall"] * 100.0, 2),
            "gold_f1_pct": round(g_cls["f1"] * 100.0, 2),
            "gold_tp": g_cls["tp"],
            "gold_fp": g_cls["fp"],
            "gold_fn": g_cls["fn"],
            "nemotron_18class_precision_pct": round(n_cls["precision"] * 100.0, 2),
            "nemotron_18class_recall_pct": round(n_cls["recall"] * 100.0, 2),
            "nemotron_18class_f1_pct": round(n_cls["f1"] * 100.0, 2),
            "nemotron_18class_tp": n_cls["tp"],
            "nemotron_18class_fp": n_cls["fp"],
            "nemotron_18class_fn": n_cls["fn"],
            "nemotron_old_bab4_f1_pct": round(old_f1 * 100.0, 2),
            "delta_new_vs_old_nemotron_f1_pct": round((n_cls["f1"] - old_f1) * 100.0, 2),
            "delta_new_nemotron_vs_gold_f1_pct": round((n_cls["f1"] - g_cls["f1"]) * 100.0, 2),
        })

    overall_csv = tables_dir / "overall_comparison.csv"
    overall_json = tables_dir / "overall_comparison.json"
    per_class_csv = tables_dir / "per_class_18_comparison.csv"
    per_class_json = tables_dir / "per_class_18_comparison.json"

    write_csv_rows(overall_csv, overall_rows)
    overall_json.write_text(
        json.dumps(
            {
                "rows": overall_rows,
                "delta_nemotron_18class_vs_old_nemotron": delta_vs_old,
                "delta_nemotron_18class_vs_gold": delta_vs_gold,
            },
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    write_csv_rows(per_class_csv, per_class_rows)
    per_class_json.write_text(json.dumps(per_class_rows, indent=2, ensure_ascii=False), encoding="utf-8")

    for path_item in (overall_csv, overall_json, per_class_csv, per_class_json):
        sync_to_drive(path_item, f"tables/{path_item.name}")

    return {
        "evaluation_results": evaluation_results,
        "predictions_by_run": predictions_by_run,
        "overall_rows": overall_rows,
        "per_class_rows": per_class_rows,
        "delta_vs_old": delta_vs_old,
        "delta_vs_gold": delta_vs_gold,
    }


EVAL_BUNDLE = evaluate_all_scenarios_on_gold_test(
    test_records=PREPARED_DATA["gold"]["test"],
    tokenizer=TOKENIZER,
    seeds=TRAINING_SEEDS,
)

_s0 = TRAINING_SEEDS[0]
_g_res = EVAL_BUNDLE["evaluation_results"]["gold"][_s0]
_n_res = EVAL_BUNDLE["evaluation_results"]["nemotron_18class"][_s0]
_old_res = HISTORICAL_BAB4_REFERENCE["nemotron_old_seed42"]

print("\n" + "=" * 92)
print("🏆 HASIL EVALUASI UTAMA PADA NERGRIT GOLD TEST SET (EXACT SPAN MATCH - SEED 42)")
print("=" * 92)
print(
    f"   {'Skenario Model':<42} | {'Presisi':>8} | {'Recall':>8} | {'Micro-F1':>9} | {'Macro-F1':>9} | {'Weighted-F1':>11}"
)
print("-" * 92)
print(
    f"   {'1. NERGRIT Gold Baseline (Seed 42)':<42} | "
    f"{_g_res['micro_precision']*100:>7.2f}% | {_g_res['micro_recall']*100:>7.2f}% | "
    f"{_g_res['micro_f1']*100:>8.2f}% | {_g_res['macro_f1']*100:>8.2f}% | {_g_res['weighted_f1']*100:>10.2f}%"
)
print(
    f"   {'2. Nemotron 18-Kelas Baru (Seed 42)':<42} | "
    f"{_n_res['micro_precision']*100:>7.2f}% | {_n_res['micro_recall']*100:>7.2f}% | "
    f"{_n_res['micro_f1']*100:>8.2f}% | {_n_res['macro_f1']*100:>8.2f}% | {_n_res['weighted_f1']*100:>10.2f}%"
)
print(
    f"   {'3. Nemotron Lama (Bab 4 Seed 42 Ref)':<42} | "
    f"{_old_res['micro_precision']*100:>7.2f}% | {_old_res['micro_recall']*100:>7.2f}% | "
    f"{_old_res['micro_f1']*100:>8.2f}% | {_old_res['macro_f1']*100:>8.2f}% | {_old_res['weighted_f1']*100:>10.2f}%"
)
print("-" * 92)
print(
    f"   {'Δ (Nemotron 18-Kelas Baru vs Nemotron Lama)':<42} | "
    f"{EVAL_BUNDLE['delta_vs_old']['micro_precision_pct_delta']:>+7.2f}% | "
    f"{EVAL_BUNDLE['delta_vs_old']['micro_recall_pct_delta']:>+7.2f}% | "
    f"{EVAL_BUNDLE['delta_vs_old']['micro_f1_pct_delta']:>+8.2f}% | "
    f"{EVAL_BUNDLE['delta_vs_old']['macro_f1_pct_delta']:>+8.2f}% | "
    f"{EVAL_BUNDLE['delta_vs_old']['weighted_f1_pct_delta']:>+10.2f}%"
)
print(
    f"   {'Δ (Nemotron 18-Kelas Baru vs Gold Baseline)':<42} | "
    f"{EVAL_BUNDLE['delta_vs_gold']['micro_precision_pct_delta']:>+7.2f}% | "
    f"{EVAL_BUNDLE['delta_vs_gold']['micro_recall_pct_delta']:>+7.2f}% | "
    f"{EVAL_BUNDLE['delta_vs_gold']['micro_f1_pct_delta']:>+8.2f}% | "
    f"{EVAL_BUNDLE['delta_vs_gold']['macro_f1_pct_delta']:>+8.2f}% | "
    f"{EVAL_BUNDLE['delta_vs_gold']['weighted_f1_pct_delta']:>+10.2f}%"
)
print("=" * 92)

print("\n📋 RINCIAN SKOR PER KELAS (18 KELAS ENTITAS PADA GOLD TEST SET):")
print("-" * 92)
print(
    f"   {'Kelas':<5} | {'Support':>7} | {'Gold F1':>8} | {'Nemotron Baru F1':>16} | "
    f"{'Nemotron Lama F1':>16} | {'Δ Baru vs Lama':>14} | {'Δ Baru vs Gold':>14}"
)
print("-" * 92)
for row in EVAL_BUNDLE["per_class_rows"]:
    print(
        f"   {row['entity_class']:<5} | {row['support']:>7,} | {row['gold_f1_pct']:>7.2f}% | "
        f"{row['nemotron_18class_f1_pct']:>15.2f}% | {row['nemotron_old_bab4_f1_pct']:>15.2f}% | "
        f"{row['delta_new_vs_old_nemotron_f1_pct']:>+13.2f}% | {row['delta_new_nemotron_vs_gold_f1_pct']:>+13.2f}%"
    )
print("=" * 92)
