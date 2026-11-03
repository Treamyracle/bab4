# =============================================================================
# SEL 7: PELATIHAN MODEL SKENARIO 1 — NERGRIT GOLD BASELINE (SEED 42)
# =============================================================================
from transformers import AutoTokenizer

# Kunci revisi model & muat Fast Tokenizer IndoBERT-Large-p1
if CONFIG.get("model_revision") is None:
    try:
        from huggingface_hub import HfApi
        CONFIG["model_revision"] = HfApi().model_info(MODEL_CHECKPOINT).sha
        print(f"🔒 Revisi model terkunci pada commit SHA: {CONFIG['model_revision']}")
    except Exception as exc:
        print(f"ℹ️ Menggunakan revisi default cabang utama untuk {MODEL_CHECKPOINT} ({exc})")

TOKENIZER = AutoTokenizer.from_pretrained(
    MODEL_CHECKPOINT,
    revision=CONFIG.get("model_revision"),
    use_fast=True,
)
if not TOKENIZER.is_fast:
    raise RuntimeError("Word-aligned token classification membutuhkan Fast Tokenizer (Rust).")

tokenizer_lock_dir = OUTPUT_DIR / "tokenizer_lock"
tokenizer_lock_dir.mkdir(parents=True, exist_ok=True)
TOKENIZER.save_pretrained(str(tokenizer_lock_dir))


def print_training_history_summary(run_manifest: dict, run_dir: Path) -> None:
    """Tampilkan ringkasan per-epoch dari riwayat pelatihan model."""
    hist_path = run_dir / "training_history.json"
    if not hist_path.is_file():
        return
    history = json.loads(hist_path.read_text(encoding="utf-8"))
    eval_entries = [row for row in history if "eval_macro_f1" in row or "eval_loss" in row]
    train_losses = {
        round(float(row["epoch"]), 2): row["loss"]
        for row in history
        if "loss" in row and "eval_loss" not in row and "epoch" in row
    }
    print("-" * 78)
    print(f"   {'Epoch':>5} | {'Train Loss':>10} | {'Val Loss':>10} | {'Val Micro-F1':>12} | {'Val Macro-F1':>12}")
    print("-" * 78)
    for row in eval_entries:
        ep = round(float(row.get("epoch", 0.0)), 2)
        t_loss = train_losses.get(ep)
        t_loss_str = f"{t_loss:.4f}" if isinstance(t_loss, (int, float)) else "—"
        v_loss = row.get("eval_loss", 0.0)
        v_mic = row.get("eval_micro_f1", 0.0) * 100.0
        v_mac = row.get("eval_macro_f1", 0.0) * 100.0
        print(f"   {ep:>5.1f} | {t_loss_str:>10} | {v_loss:>10.4f} | {v_mic:>11.2f}% | {v_mac:>11.2f}%")
    print("-" * 78)


GOLD_RUN_MANIFESTS = {}
for seed in TRAINING_SEEDS:
    print("\n" + "=" * 78)
    print(f"🏅 SKENARIO 1: PELATIHAN NERGRIT GOLD BASELINE (SEED = {seed})")
    print("=" * 78)
    manifest = train_scenario_model(
        dataset_key="gold",
        history_prefix="gold",
        seed=seed,
        train_records=PREPARED_DATA["gold"]["train"],
        val_records=PREPARED_DATA["gold"]["validation"],
        tokenizer=TOKENIZER,
        config=CONFIG,
        runs_dir=RUNS_DIR,
    )
    GOLD_RUN_MANIFESTS[seed] = manifest
    print_training_history_summary(manifest, RUNS_DIR / manifest["run_id"])
    print(
        f"✅ Selesai {manifest['run_id']}: Best Val Macro-F1 = {manifest['best_validation_macro_f1'] * 100:.2f}% | "
        f"Epochs = {manifest['epochs_completed']} | Steps = {manifest['optimizer_steps']} | "
        f"Durasi = {manifest['elapsed_minutes']:.2f} menit"
    )
