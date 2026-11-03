# =============================================================================
# SEL 10: ANALISIS GALAT OTOMATIS, VISUALISASI GRAFIK, PAKET .ZIP, & UPLOAD DRIVE OTOMATIS
# =============================================================================
from datetime import datetime, timezone
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def analyze_prediction_errors(
    records: list[dict],
    predictions: list[list[str]],
    entity_types: tuple[str, ...] = ACTIVE_TYPES,
) -> dict:
    """Klasifikasikan setiap galat prediksi pada Test Set ke dalam taksonomi galat CoNLL."""
    exact_tp = 0
    type_confusion_count = 0
    boundary_same_type_count = 0
    boundary_and_type_count = 0
    spurious_fp_count = 0
    missed_fn_count = 0

    confusion_pairs = Counter()
    spurious_by_class = Counter()
    missed_by_class = Counter()
    boundary_by_class = Counter()
    sample_errors = {
        "type_confusion": [],
        "boundary_error_same_type": [],
        "boundary_and_type_error": [],
        "spurious_fp": [],
        "missed_fn": [],
    }

    for rec, pred_tags in zip(records, predictions):
        tokens = rec["tokens"]
        gold_spans = spans(rec["tags"])
        pred_spans = spans(pred_tags)

        gold_set = set(gold_spans)
        pred_set = set(pred_spans)

        exact_matches = gold_set & pred_set
        exact_tp += len(exact_matches)

        rem_gold = [g for g in gold_spans if g not in exact_matches]
        rem_pred = [p for p in pred_spans if p not in exact_matches]

        matched_gold_idx = set()
        matched_pred_idx = set()

        # 1. Cek Type Confusion dengan batas rentang kata yang 100% sama persis
        gold_by_bounds = {(s, e): (idx, k) for idx, (s, e, k) in enumerate(rem_gold)}
        for p_idx, (ps, pe, pk) in enumerate(rem_pred):
            if (ps, pe) in gold_by_bounds:
                g_idx, gk = gold_by_bounds[(ps, pe)]
                if g_idx not in matched_gold_idx:
                    matched_gold_idx.add(g_idx)
                    matched_pred_idx.add(p_idx)
                    type_confusion_count += 1
                    confusion_pairs[(gk, pk)] += 1
                    if len(sample_errors["type_confusion"]) < 25:
                        sample_errors["type_confusion"].append({
                            "sentence_id": rec["sentence_id"],
                            "span_text": " ".join(tokens[ps:pe]),
                            "gold_type": gk,
                            "pred_type": pk,
                        })

        # 2. Cek Boundary Overlap (irisan token > 0 pada rentang yang belum terpasangkan)
        for p_idx, (ps, pe, pk) in enumerate(rem_pred):
            if p_idx in matched_pred_idx:
                continue
            best_g_idx = None
            best_overlap = 0
            for g_idx, (gs, ge, gk) in enumerate(rem_gold):
                if g_idx in matched_gold_idx:
                    continue
                overlap = max(0, min(pe, ge) - max(ps, gs))
                if overlap > best_overlap:
                    best_overlap = overlap
                    best_g_idx = g_idx
            if best_g_idx is not None and best_overlap > 0:
                gs, ge, gk = rem_gold[best_g_idx]
                matched_gold_idx.add(best_g_idx)
                matched_pred_idx.add(p_idx)
                if pk == gk:
                    boundary_same_type_count += 1
                    boundary_by_class[gk] += 1
                    if len(sample_errors["boundary_error_same_type"]) < 25:
                        sample_errors["boundary_error_same_type"].append({
                            "sentence_id": rec["sentence_id"],
                            "entity_type": gk,
                            "gold_text": " ".join(tokens[gs:ge]),
                            "pred_text": " ".join(tokens[ps:pe]),
                        })
                else:
                    boundary_and_type_count += 1
                    confusion_pairs[(gk, pk)] += 1
                    if len(sample_errors["boundary_and_type_error"]) < 25:
                        sample_errors["boundary_and_type_error"].append({
                            "sentence_id": rec["sentence_id"],
                            "gold_type": gk,
                            "gold_text": " ".join(tokens[gs:ge]),
                            "pred_type": pk,
                            "pred_text": " ".join(tokens[ps:pe]),
                        })

        # 3. Sisanya adalah Spurious False Positive & Missed False Negative murni
        for p_idx, (ps, pe, pk) in enumerate(rem_pred):
            if p_idx not in matched_pred_idx:
                spurious_fp_count += 1
                spurious_by_class[pk] += 1
                if len(sample_errors["spurious_fp"]) < 25:
                    sample_errors["spurious_fp"].append({
                        "sentence_id": rec["sentence_id"],
                        "pred_type": pk,
                        "pred_text": " ".join(tokens[ps:pe]),
                    })

        for g_idx, (gs, ge, gk) in enumerate(rem_gold):
            if g_idx not in matched_gold_idx:
                missed_fn_count += 1
                missed_by_class[gk] += 1
                if len(sample_errors["missed_fn"]) < 25:
                    sample_errors["missed_fn"].append({
                        "sentence_id": rec["sentence_id"],
                        "gold_type": gk,
                        "gold_text": " ".join(tokens[gs:ge]),
                    })

    total_non_tp_events = (
        type_confusion_count
        + boundary_same_type_count
        + boundary_and_type_count
        + spurious_fp_count
        + missed_fn_count
    )

    def pct(val: int) -> float:
        return round(100.0 * val / total_non_tp_events, 2) if total_non_tp_events else 0.0

    top_confusions = [
        {"gold_type": gk, "pred_type": pk, "count": cnt}
        for (gk, pk), cnt in confusion_pairs.most_common(30)
    ]

    return {
        "exact_match_tp": exact_tp,
        "total_error_events": total_non_tp_events,
        "counts": {
            "type_confusion": type_confusion_count,
            "boundary_error_same_type": boundary_same_type_count,
            "boundary_and_type_error": boundary_and_type_count,
            "spurious_fp": spurious_fp_count,
            "missed_fn": missed_fn_count,
        },
        "proportions_pct": {
            "type_confusion": pct(type_confusion_count),
            "boundary_error_same_type": pct(boundary_same_type_count),
            "boundary_and_type_error": pct(boundary_and_type_count),
            "spurious_fp": pct(spurious_fp_count),
            "missed_fn": pct(missed_fn_count),
        },
        "top_type_confusions": top_confusions,
        "spurious_fp_by_class": {k: spurious_by_class[k] for k in entity_types},
        "missed_fn_by_class": {k: missed_by_class[k] for k in entity_types},
        "boundary_error_by_class": {k: boundary_by_class[k] for k in entity_types},
        "sample_errors": sample_errors,
    }


def generate_experiment_figures(
    per_class_rows: list[dict],
    histories_dir: Path,
    error_breakdown: dict,
    figures_dir: Path = FIGURES_DIR,
    seed: int = TRAINING_SEEDS[0],
) -> list[Path]:
    """Buat grafik visualisasi perbandingan F1 per kelas, kurva konvergensi, dan komposisi galat."""
    figures_dir.mkdir(parents=True, exist_ok=True)
    generated = []

    # 1. Grafik Perbandingan F1 Per Kelas (18 Kelas)
    classes = [r["entity_class"] for r in per_class_rows]
    gold_f1s = [r["gold_f1_pct"] for r in per_class_rows]
    nem_new_f1s = [r["nemotron_18class_f1_pct"] for r in per_class_rows]
    nem_old_f1s = [r["nemotron_old_bab4_f1_pct"] for r in per_class_rows]

    fig, ax = plt.subplots(figsize=(15, 6.5), dpi=300)
    x_pos = list(range(len(classes)))
    width = 0.27

    ax.bar([x - width for x in x_pos], gold_f1s, width=width, label="NERGRIT Gold Baseline", color="#1f77b4")
    ax.bar(x_pos, nem_new_f1s, width=width, label="Nemotron 18-Kelas Baru (Terverifikasi)", color="#2ca02c")
    ax.bar([x + width for x in x_pos], nem_old_f1s, width=width, label="Nemotron Lama (Bab 4 Sebelum Verifikasi)", color="#ff7f0e", alpha=0.85)

    ax.set_title("Perbandingan Skor F1 per Kelas Entitas pada NERGRIT Gold Test Set (18 Kelas)", fontsize=13, fontweight="bold")
    ax.set_xlabel("Kelas Entitas (18 Kelas Standar BIO)", fontsize=11)
    ax.set_ylabel("Exact Span F1-Score (%)", fontsize=11)
    ax.set_xticks(x_pos)
    ax.set_xticklabels(classes, fontsize=10, fontweight="bold")
    ax.set_ylim(0, 108)
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    ax.legend(loc="upper right", fontsize=10)
    fig.tight_layout()

    f1_chart_path = figures_dir / "per_class_f1_comparison.png"
    fig.savefig(f1_chart_path, dpi=300)
    plt.close(fig)
    generated.append(f1_chart_path)

    # 2. Grafik Kurva Konvergensi Pelatihan (Loss & Validation Macro-F1)
    fig, axes = plt.subplots(1, 2, figsize=(13, 5.2), dpi=300)
    for prefix, title_label, color in (
        ("gold", "NERGRIT Gold", "#1f77b4"),
        ("nemotron", "Nemotron 18-Kelas Baru", "#2ca02c"),
    ):
        hist_json = histories_dir / f"{prefix}_s{seed}.json"
        if not hist_json.is_file():
            continue
        history = json.loads(hist_json.read_text(encoding="utf-8"))
        eval_rows = [r for r in history if "eval_loss" in r and "epoch" in r]
        train_rows = [r for r in history if "loss" in r and "eval_loss" not in r and "epoch" in r]

        if train_rows:
            axes[0].plot(
                [r["epoch"] for r in train_rows],
                [r["loss"] for r in train_rows],
                linestyle="--",
                marker="o",
                color=color,
                alpha=0.75,
                label=f"{title_label} — Train Loss",
            )
        if eval_rows:
            axes[0].plot(
                [r["epoch"] for r in eval_rows],
                [r["eval_loss"] for r in eval_rows],
                linestyle="-",
                marker="s",
                color=color,
                label=f"{title_label} — Val Loss",
            )
            axes[1].plot(
                [r["epoch"] for r in eval_rows],
                [r.get("eval_macro_f1", 0.0) * 100.0 for r in eval_rows],
                linestyle="-",
                marker="o",
                color=color,
                linewidth=2.0,
                label=f"{title_label} — Val Macro-F1",
            )
            axes[1].plot(
                [r["epoch"] for r in eval_rows],
                [r.get("eval_micro_f1", 0.0) * 100.0 for r in eval_rows],
                linestyle=":",
                marker="^",
                color=color,
                alpha=0.8,
                label=f"{title_label} — Val Micro-F1",
            )

    axes[0].set_title("Dinamika Training & Validation Loss per Epoch", fontsize=12, fontweight="bold")
    axes[0].set_xlabel("Epoch")
    axes[0].set_ylabel("Cross-Entropy Loss")
    axes[0].grid(True, linestyle="--", alpha=0.4)
    axes[0].legend(fontsize=9)

    axes[1].set_title("Konvergensi Validation Macro-F1 & Micro-F1 per Epoch", fontsize=12, fontweight="bold")
    axes[1].set_xlabel("Epoch")
    axes[1].set_ylabel("F1-Score (%)")
    axes[1].grid(True, linestyle="--", alpha=0.4)
    axes[1].legend(fontsize=9)
    fig.tight_layout()

    conv_chart_path = figures_dir / "training_convergence_curves.png"
    fig.savefig(conv_chart_path, dpi=300)
    plt.close(fig)
    generated.append(conv_chart_path)

    # 3. Grafik Komposisi Taksonomi Galat (Error Breakdown)
    err_categories = [
        ("type_confusion", "Type Confusion\n(Batas Tepat)"),
        ("boundary_error_same_type", "Boundary Error\n(Kelas Tepat)"),
        ("boundary_and_type_error", "Boundary +\nType Error"),
        ("spurious_fp", "Spurious FP\n(Over-Tagging)"),
        ("missed_fn", "Missed FN\n(Entitas Terlewat)"),
    ]
    g_err = error_breakdown["gold"]["counts"]
    n_err = error_breakdown["nemotron_18class"]["counts"]

    fig, ax = plt.subplots(figsize=(10, 5.2), dpi=300)
    idx_pos = list(range(len(err_categories)))
    w = 0.35
    ax.bar(
        [i - w / 2 for i in idx_pos],
        [g_err[k] for k, _ in err_categories],
        width=w,
        label="NERGRIT Gold Baseline",
        color="#1f77b4",
    )
    ax.bar(
        [i + w / 2 for i in idx_pos],
        [n_err[k] for k, _ in err_categories],
        width=w,
        label="Nemotron 18-Kelas Baru",
        color="#2ca02c",
    )
    ax.set_title("Perbandingan Distribusi Kategori Galat pada NERGRIT Gold Test Set", fontsize=12, fontweight="bold")
    ax.set_xticks(idx_pos)
    ax.set_xticklabels([lbl for _, lbl in err_categories], fontsize=10)
    ax.set_ylabel("Jumlah Kejadian Galat (Rentang Entitas)")
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    ax.legend(fontsize=10)
    fig.tight_layout()

    err_chart_path = figures_dir / "error_taxonomy_breakdown.png"
    fig.savefig(err_chart_path, dpi=300)
    plt.close(fig)
    generated.append(err_chart_path)

    for fig_p in generated:
        sync_to_drive(fig_p, f"figures/{fig_p.name}")

    return generated


def package_experiment_results_zip(
    output_dir: Path = OUTPUT_DIR,
    zip_filename: str = "nemotron_18class_experiment_results.zip",
) -> tuple[Path, dict]:
    """Kemas seluruh hasil eksperimen ke dalam arsip .zip dan unggah otomatis ke Google Drive."""
    zip_path = output_dir / zip_filename
    folders_to_include = ("tables", "histories", "predictions", "error_analysis", "figures")
    root_files_to_include = (
        "experiment_summary.json",
        "experiment_config.json",
        "environment_fingerprint.json",
        "bundle_verification.json",
    )

    packaged_files = {}
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for fname in root_files_to_include:
            fpath = output_dir / fname
            if fpath.is_file():
                zf.write(fpath, arcname=fname)
                packaged_files[fname] = compute_sha256(fpath)

        for folder in folders_to_include:
            folder_path = output_dir / folder
            if not folder_path.is_dir():
                continue
            for fpath in sorted(folder_path.rglob("*")):
                if fpath.is_file():
                    rel_arc = f"{folder}/{fpath.relative_to(folder_path).as_posix()}"
                    zf.write(fpath, arcname=rel_arc)
                    packaged_files[rel_arc] = compute_sha256(fpath)

        manifest_payload = {
            "archive_name": zip_filename,
            "created_utc": datetime.now(timezone.utc).isoformat(),
            "file_count": len(packaged_files),
            "files_sha256": packaged_files,
        }
        zf.writestr("results_manifest.json", json.dumps(manifest_payload, indent=2, ensure_ascii=False))

    # Salin juga ke working directory root (/content jika di Colab) agar mudah diakses
    if IN_COLAB:
        colab_root_zip = Path("/content") / zip_filename
        if colab_root_zip.resolve() != zip_path.resolve():
            shutil.copy2(zip_path, colab_root_zip)

    # Unggah otomatis berkas .zip ke Google Drive dan verifikasi SHA-256
    drive_zip = sync_to_drive(zip_path, zip_filename, verify_hash=True)
    return zip_path, {
        "zip_path": str(zip_path),
        "drive_zip_path": str(drive_zip) if drive_zip else None,
        "zip_sha256": compute_sha256(zip_path),
        "zip_size_bytes": zip_path.stat().st_size,
        "file_count": len(packaged_files),
    }


# 1. Jalankan Analisis Galat Otomatis pada Gold Test Set
_primary_seed = TRAINING_SEEDS[0]
ERROR_BREAKDOWN = {
    "seed": _primary_seed,
    "gold": analyze_prediction_errors(
        PREPARED_DATA["gold"]["test"],
        EVAL_BUNDLE["predictions_by_run"]["gold"][_primary_seed],
        ACTIVE_TYPES,
    ),
    "nemotron_18class": analyze_prediction_errors(
        PREPARED_DATA["gold"]["test"],
        EVAL_BUNDLE["predictions_by_run"]["nemotron_18class"][_primary_seed],
        ACTIVE_TYPES,
    ),
}

error_json_path = ERROR_ANALYSIS_DIR / "error_breakdown.json"
error_json_path.write_text(json.dumps(ERROR_BREAKDOWN, indent=2, ensure_ascii=False), encoding="utf-8")
sync_to_drive(error_json_path, "error_analysis/error_breakdown.json")

error_table_rows = []
for sc_key, sc_label in (("gold", "NERGRIT Gold Baseline"), ("nemotron_18class", "Nemotron 18-Kelas Baru")):
    eb = ERROR_BREAKDOWN[sc_key]
    error_table_rows.append({
        "scenario_key": sc_key,
        "scenario_name": sc_label,
        "seed": _primary_seed,
        "exact_match_tp": eb["exact_match_tp"],
        "total_error_events": eb["total_error_events"],
        "type_confusion_count": eb["counts"]["type_confusion"],
        "type_confusion_pct": eb["proportions_pct"]["type_confusion"],
        "boundary_same_type_count": eb["counts"]["boundary_error_same_type"],
        "boundary_same_type_pct": eb["proportions_pct"]["boundary_error_same_type"],
        "boundary_and_type_count": eb["counts"]["boundary_and_type_error"],
        "boundary_and_type_pct": eb["proportions_pct"]["boundary_and_type_error"],
        "spurious_fp_count": eb["counts"]["spurious_fp"],
        "spurious_fp_pct": eb["proportions_pct"]["spurious_fp"],
        "missed_fn_count": eb["counts"]["missed_fn"],
        "missed_fn_pct": eb["proportions_pct"]["missed_fn"],
    })
write_csv_rows(TABLES_DIR / "error_taxonomy_comparison.csv", error_table_rows)
sync_to_drive(TABLES_DIR / "error_taxonomy_comparison.csv", "tables/error_taxonomy_comparison.csv")

# 2. Buat Grafik Visualisasi (.png)
GENERATED_FIGURES = generate_experiment_figures(
    per_class_rows=EVAL_BUNDLE["per_class_rows"],
    histories_dir=HISTORIES_DIR,
    error_breakdown=ERROR_BREAKDOWN,
    figures_dir=FIGURES_DIR,
    seed=_primary_seed,
)

# 3. Susun Ringkasan Eksekutif Lengkap (experiment_summary.json)
EXPERIMENT_SUMMARY = {
    "status": "complete",
    "timestamp_utc": datetime.now(timezone.utc).isoformat(),
    "configuration": CONFIG,
    "environment": ENV_FINGERPRINT,
    "dataset_statistics": PREPARED_MANIFEST["statistics"],
    "leakage_verification": PREPARED_MANIFEST["leakage_check"],
    "training_runs": {
        "gold": {str(k): v for k, v in GOLD_RUN_MANIFESTS.items()},
        "nemotron_18class": {str(k): v for k, v in NEMOTRON_RUN_MANIFESTS.items()},
    },
    "evaluation_gold_test": {
        "overall_rows": EVAL_BUNDLE["overall_rows"],
        "delta_nemotron_18class_vs_old_nemotron": EVAL_BUNDLE["delta_vs_old"],
        "delta_nemotron_18class_vs_gold": EVAL_BUNDLE["delta_vs_gold"],
        "per_class_18_comparison": EVAL_BUNDLE["per_class_rows"],
    },
    "error_analysis_summary": {
        "gold": {
            "exact_match_tp": ERROR_BREAKDOWN["gold"]["exact_match_tp"],
            "counts": ERROR_BREAKDOWN["gold"]["counts"],
            "proportions_pct": ERROR_BREAKDOWN["gold"]["proportions_pct"],
            "top_type_confusions": ERROR_BREAKDOWN["gold"]["top_type_confusions"][:15],
        },
        "nemotron_18class": {
            "exact_match_tp": ERROR_BREAKDOWN["nemotron_18class"]["exact_match_tp"],
            "counts": ERROR_BREAKDOWN["nemotron_18class"]["counts"],
            "proportions_pct": ERROR_BREAKDOWN["nemotron_18class"]["proportions_pct"],
            "top_type_confusions": ERROR_BREAKDOWN["nemotron_18class"]["top_type_confusions"][:15],
        },
    },
}

summary_path = OUTPUT_DIR / "experiment_summary.json"
summary_path.write_text(json.dumps(EXPERIMENT_SUMMARY, indent=2, ensure_ascii=False), encoding="utf-8")
sync_to_drive(summary_path, "experiment_summary.json")

# 4. Kemas Seluruh Artefak ke nemotron_18class_experiment_results.zip & Upload Otomatis ke Google Drive
RESULTS_ZIP_PATH, ZIP_INFO = package_experiment_results_zip(OUTPUT_DIR)

print("\n" + "=" * 88)
print("🎉 EKSPERIMEN SELESAI & ARSIP .ZIP BERHASIL DISIMPAN KE GOOGLE DRIVE!")
print("=" * 88)
print(f"   Berkas ZIP Lokal       : {ZIP_INFO['zip_path']} ({ZIP_INFO['zip_size_bytes'] / (1024 * 1024):.2f} MB)")
print(f"   Berkas ZIP Google Drive: {ZIP_INFO['drive_zip_path']}")
print(f"   SHA-256 Arsip ZIP      : {ZIP_INFO['zip_sha256']}")
print(f"   Jumlah Berkas di ZIP   : {ZIP_INFO['file_count']} berkas")
print("=" * 88)

try:
    from IPython.display import FileLink, display  # type: ignore
    display(FileLink(str(RESULTS_ZIP_PATH)))
except Exception:
    pass

if IN_COLAB:
    try:
        from google.colab import files  # type: ignore
        print("⬇️ Memulai pengunduhan otomatis nemotron_18class_experiment_results.zip ke peramban...")
        files.download(str(RESULTS_ZIP_PATH))
    except Exception as exc:
        print(f"ℹ️ Unduhan langsung peramban dilewati ({exc}). Berkas sudah aman di Google Drive: {ZIP_INFO['drive_zip_path']}")
