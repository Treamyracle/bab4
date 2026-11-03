# =============================================================================
# SEL 2: KONFIGURASI EKSPERIMEN, SEED [42], & MOUNT GOOGLE DRIVE OTOMATIS
# =============================================================================
from __future__ import annotations

from copy import deepcopy
import hashlib
import json
import os
from pathlib import Path
import shutil
import sys
import time

# 1. Taksonomi 18 Kelas Entitas Aktif (Tanpa REG dan TTL)
ACTIVE_TYPES = (
    "CRD", "DAT", "EVT", "FAC", "GPE", "LAN", "LAW", "LOC", "MON",
    "NOR", "ORD", "ORG", "PER", "PRC", "PRD", "QTY", "TIM", "WOA",
)
EXCLUDED_TYPES = ("REG", "TTL")
ALL_KNOWN_TYPES = frozenset(ACTIVE_TYPES) | frozenset(EXCLUDED_TYPES)
LABELS = ["O"] + [f"{prefix}-{kind}" for kind in ACTIVE_TYPES for prefix in ("B", "I")]
LABEL2ID = {tag: idx for idx, tag in enumerate(LABELS)}
ID2LABEL = {idx: tag for idx, tag in enumerate(LABELS)}

assert len(ACTIVE_TYPES) == 18, f"Harus tepat 18 kelas aktif, ditemukan: {len(ACTIVE_TYPES)}"
assert len(LABELS) == 37, f"Harus tepat 37 tag BIO, ditemukan: {len(LABELS)}"
assert not any("REG" in tag or "TTL" in tag for tag in LABELS), "REG dan TTL dilarang ada di LABELS!"

# 2. Konfigurasi Seed & Hiperparameter (100% Identik dengan Skripsi Tabel 3.2 & Tabel 4.13)
# Sesuai instruksi: gunakan 1 random seed (42) untuk NERGRIT Gold & Nemotron 18-Kelas Baru
TRAINING_SEEDS = [42]
SPLIT_SEED = 42
NEAR_THRESHOLD = 0.90

MODEL_CHECKPOINT = "indobenchmark/indobert-large-p1"
MAX_SEQ_LENGTH = 256
TRAIN_BATCH_SIZE = 32
GRADIENT_ACCUMULATION_STEPS = 1
EVAL_BATCH_SIZE = 64
LEARNING_RATE = 2e-5
WEIGHT_DECAY = 0.01
ADAM_BETA1 = 0.9
ADAM_BETA2 = 0.999
ADAM_EPSILON = 1e-8
WARMUP_RATIO = 0.10
LR_SCHEDULER_TYPE = "linear"
NUM_TRAIN_EPOCHS = 10
EARLY_STOPPING_PATIENCE = 2
EARLY_STOPPING_THRESHOLD = 0.0
METRIC_FOR_BEST_MODEL = "macro_f1"
LOAD_BEST_MODEL_AT_END = True
DROPOUT = 0.10
MAX_GRAD_NORM = 1.0
PAD_TO_MULTIPLE_OF = 8
OPTIM = "adamw_torch"
DATALOADER_NUM_WORKERS = 2
SAVE_BEST_WEIGHTS_TO_DRIVE = True

CONFIG = {
    "experiment_name": "eksperimen_komparatif_gold_vs_nemotron_18class",
    "model_checkpoint": MODEL_CHECKPOINT,
    "model_revision": None,
    "training_seeds": list(TRAINING_SEEDS),
    "split_seed": SPLIT_SEED,
    "near_threshold": NEAR_THRESHOLD,
    "active_types": list(ACTIVE_TYPES),
    "excluded_types": list(EXCLUDED_TYPES),
    "labels": list(LABELS),
    "max_seq_length": MAX_SEQ_LENGTH,
    "train_batch_size": TRAIN_BATCH_SIZE,
    "gradient_accumulation_steps": GRADIENT_ACCUMULATION_STEPS,
    "eval_batch_size": EVAL_BATCH_SIZE,
    "learning_rate": LEARNING_RATE,
    "weight_decay": WEIGHT_DECAY,
    "adam_beta1": ADAM_BETA1,
    "adam_beta2": ADAM_BETA2,
    "adam_epsilon": ADAM_EPSILON,
    "warmup_ratio": WARMUP_RATIO,
    "lr_scheduler_type": LR_SCHEDULER_TYPE,
    "num_train_epochs": NUM_TRAIN_EPOCHS,
    "early_stopping_patience": EARLY_STOPPING_PATIENCE,
    "early_stopping_threshold": EARLY_STOPPING_THRESHOLD,
    "metric_for_best_model": METRIC_FOR_BEST_MODEL,
    "load_best_model_at_end": LOAD_BEST_MODEL_AT_END,
    "dropout": DROPOUT,
    "max_grad_norm": MAX_GRAD_NORM,
    "pad_to_multiple_of": PAD_TO_MULTIPLE_OF,
    "optim": OPTIM,
    "dataloader_num_workers": DATALOADER_NUM_WORKERS,
    "bf16": True,
    "fp16": False,
    "tf32": False,
    "gradient_checkpointing": False,
    "save_best_weights_to_drive": SAVE_BEST_WEIGHTS_TO_DRIVE,
}


def compute_sha256(path: Path) -> str:
    """Hitung SHA-256 berkas secara streaming."""
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def stable_json_hash(obj) -> str:
    """Hitung SHA-256 deterministik dari struktur data JSON."""
    payload = json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


# 3. Mount Otomatis Google Drive & Penyiapan Direktori Kerja
IN_COLAB = "google.colab" in sys.modules or Path("/content").is_dir()
DRIVE_MOUNTED = False

if "NEMOTRON_DRIVE_DIR" in os.environ:
    DRIVE_BASE_DIR = Path(os.environ["NEMOTRON_DRIVE_DIR"]).resolve()
    DRIVE_BASE_DIR.mkdir(parents=True, exist_ok=True)
    DRIVE_MOUNTED = True
elif IN_COLAB:
    try:
        from google.colab import drive  # type: ignore
        if not Path("/content/drive/MyDrive").is_dir():
            print("🔗 Melakukan mount otomatis Google Drive (/content/drive)...")
            drive.mount("/content/drive", force_remount=False)
        DRIVE_BASE_DIR = Path("/content/drive/MyDrive/SKRIPSI_NER_BAB4/eksperimen_nemotron_18class")
        DRIVE_BASE_DIR.mkdir(parents=True, exist_ok=True)
        DRIVE_MOUNTED = True
        print(f"✅ Google Drive berhasil terhubung: {DRIVE_BASE_DIR}")
    except Exception as exc:
        print(f"⚠️ Peringatan: Gagal mount Google Drive otomatis ({exc}). Menggunakan fallback direktori lokal.")
        DRIVE_BASE_DIR = Path("/content/drive_fallback/eksperimen_nemotron_18class")
        DRIVE_BASE_DIR.mkdir(parents=True, exist_ok=True)
else:
    DRIVE_BASE_DIR = (Path.cwd() / "outputs" / "drive_mirror_nemotron_18class").resolve()
    DRIVE_BASE_DIR.mkdir(parents=True, exist_ok=True)

if "NEMOTRON_LOCAL_WORK_DIR" in os.environ:
    LOCAL_WORK_DIR = Path(os.environ["NEMOTRON_LOCAL_WORK_DIR"]).resolve()
elif IN_COLAB:
    LOCAL_WORK_DIR = Path("/content/nemotron_18class_workspace")
else:
    LOCAL_WORK_DIR = (Path.cwd() / "outputs" / "nemotron_18class_workspace").resolve()

DATA_DIR = LOCAL_WORK_DIR / "data"
PREPARED_DIR = LOCAL_WORK_DIR / "prepared"
OUTPUT_DIR = LOCAL_WORK_DIR / "outputs"
RUNS_DIR = OUTPUT_DIR / "runs"
TABLES_DIR = OUTPUT_DIR / "tables"
HISTORIES_DIR = OUTPUT_DIR / "histories"
PREDICTIONS_DIR = OUTPUT_DIR / "predictions"
ERROR_ANALYSIS_DIR = OUTPUT_DIR / "error_analysis"
FIGURES_DIR = OUTPUT_DIR / "figures"

for folder in (
    LOCAL_WORK_DIR, DATA_DIR, PREPARED_DIR, OUTPUT_DIR,
    RUNS_DIR, TABLES_DIR, HISTORIES_DIR, PREDICTIONS_DIR,
    ERROR_ANALYSIS_DIR, FIGURES_DIR,
    DRIVE_BASE_DIR, DRIVE_BASE_DIR / "runs", DRIVE_BASE_DIR / "tables",
    DRIVE_BASE_DIR / "histories", DRIVE_BASE_DIR / "predictions",
    DRIVE_BASE_DIR / "error_analysis", DRIVE_BASE_DIR / "figures",
):
    folder.mkdir(parents=True, exist_ok=True)

CONFIG["local_work_dir"] = str(LOCAL_WORK_DIR)
CONFIG["output_dir"] = str(OUTPUT_DIR)
CONFIG["drive_base_dir"] = str(DRIVE_BASE_DIR)
CONFIG["drive_mounted"] = DRIVE_MOUNTED


def sync_to_drive(src_path: Path | str, rel_dest: str | Path | None = None, verify_hash: bool = True) -> Path | None:
    """Salin otomatis berkas atau direktori ke Google Drive dan verifikasi integritasnya."""
    src = Path(src_path).resolve()
    if not src.exists():
        print(f"⚠️ [Drive Sync] Sumber tidak ditemukan: {src}")
        return None
    if rel_dest is None:
        try:
            rel_dest = src.relative_to(OUTPUT_DIR)
        except ValueError:
            rel_dest = src.name
    dest = (DRIVE_BASE_DIR / rel_dest).resolve()
    try:
        if src == dest:
            return dest
        if src.is_dir():
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copytree(src, dest, dirs_exist_ok=True)
            print(f"☁️ [Drive Sync] Direktori tersinkronisasi ke Google Drive: {dest}")
        else:
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dest)
            if verify_hash:
                src_hash = compute_sha256(src)
                dst_hash = compute_sha256(dest)
                if src_hash != dst_hash:
                    raise RuntimeError(f"Ketidakcocokan SHA-256 saat menyalin {src.name} ke Google Drive!")
            size_mb = dest.stat().st_size / (1024 * 1024)
            print(f"☁️ [Drive Sync] Berkas tersimpan di Google Drive: {dest} ({size_mb:.2f} MB)")
        return dest
    except Exception as exc:
        print(f"⚠️ [Drive Sync] Gagal menyalin {src} ke {dest}: {exc}")
        return None


# Simpan konfigurasi awal dan sinkronkan ke Google Drive
config_path = OUTPUT_DIR / "experiment_config.json"
config_path.write_text(json.dumps(CONFIG, indent=2, ensure_ascii=False), encoding="utf-8")
sync_to_drive(config_path, "experiment_config.json")

print("=" * 72)
print("⚙️ KONFIGURASI EKSPERIMEN SIAP")
print(f"   Model Fondasi        : {MODEL_CHECKPOINT}")
print(f"   Random Seed Latih    : {TRAINING_SEEDS} (1 seed deterministik)")
print(f"   Jumlah Kelas / Tag   : {len(ACTIVE_TYPES)} kelas aktif / {len(LABELS)} tag BIO")
print(f"   Direktori Kerja NVMe : {LOCAL_WORK_DIR}")
print(f"   Direktori Google Drive: {DRIVE_BASE_DIR} (Mounted={DRIVE_MOUNTED})")
print("=" * 72)
