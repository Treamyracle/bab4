# =============================================================================
# SEL 8: PELATIHAN MODEL SKENARIO 2 — NEMOTRON 18-KELAS BARU (SEED 42)
# =============================================================================
NEMOTRON_RUN_MANIFESTS = {}

for seed in TRAINING_SEEDS:
    print("\n" + "=" * 78)
    print(f"🤖 SKENARIO 2: PELATIHAN KORPUS SINTETIS NEMOTRON 18-KELAS BARU (SEED = {seed})")
    print("=" * 78)
    manifest = train_scenario_model(
        dataset_key="nemotron_18class",
        history_prefix="nemotron",
        seed=seed,
        train_records=PREPARED_DATA["nemotron_18class"]["train"],
        val_records=PREPARED_DATA["nemotron_18class"]["validation"],
        tokenizer=TOKENIZER,
        config=CONFIG,
        runs_dir=RUNS_DIR,
    )
    NEMOTRON_RUN_MANIFESTS[seed] = manifest

    # Buat salinan alias riwayat dengan nama eksplisit nemotron_18class_s{seed}
    src_csv = HISTORIES_DIR / f"nemotron_s{seed}.csv"
    src_json = HISTORIES_DIR / f"nemotron_s{seed}.json"
    alias_csv = HISTORIES_DIR / f"nemotron_18class_s{seed}.csv"
    alias_json = HISTORIES_DIR / f"nemotron_18class_s{seed}.json"
    if src_csv.is_file():
        shutil.copy2(src_csv, alias_csv)
        sync_to_drive(alias_csv, f"histories/{alias_csv.name}")
    if src_json.is_file():
        shutil.copy2(src_json, alias_json)
        sync_to_drive(alias_json, f"histories/{alias_json.name}")

    print_training_history_summary(manifest, RUNS_DIR / manifest["run_id"])
    print(
        f"✅ Selesai {manifest['run_id']}: Best Val Macro-F1 = {manifest['best_validation_macro_f1'] * 100:.2f}% | "
        f"Epochs = {manifest['epochs_completed']} | Steps = {manifest['optimizer_steps']} | "
        f"Durasi = {manifest['elapsed_minutes']:.2f} menit"
    )
