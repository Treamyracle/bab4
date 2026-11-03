# =============================================================================
# SEL 3: INSTALASI DEPENDENSI, PEMERIKSAAN GPU (BF16/FP16), & REPRODUKSIBILITAS
# =============================================================================
import importlib
import importlib.util
import platform
import random
import subprocess

# 1. Kebijakan Determinisme CUDA (diatur sebelum inisialisasi konteks kernel GPU)
os.environ.pop("CUDA_LAUNCH_BLOCKING", None)
os.environ["CUBLAS_WORKSPACE_CONFIG"] = ":4096:8"
os.environ["FLASH_ATTENTION_DETERMINISTIC"] = "1"
os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
os.environ.setdefault("TQDM_MININTERVAL", "2")

# 2. Pemeriksaan & Pemasangan Pustaka Tanpa Merusak PyTorch CUDA Bawaan Colab
REQUIRED_PACKAGES = [
    ("transformers", "transformers>=4.40.0"),
    ("datasets", "datasets>=2.18.0"),
    ("accelerate", "accelerate>=0.28.0"),
    ("seqeval", "seqeval>=1.2.2"),
    ("evaluate", "evaluate>=0.4.1"),
    ("sklearn", "scikit-learn>=1.3.0"),
    ("matplotlib", "matplotlib>=3.7.0"),
]

def _is_module_available(module_name: str) -> bool:
    if module_name in sys.modules and sys.modules[module_name] is not None:
        return True
    try:
        return importlib.util.find_spec(module_name) is not None
    except (ValueError, ImportError):
        return module_name in sys.modules


missing_specs = [
    pip_spec
    for module_name, pip_spec in REQUIRED_PACKAGES
    if not _is_module_available(module_name)
]

if missing_specs and (IN_COLAB or os.environ.get("NEMOTRON_FORCE_PIP_INSTALL") == "1") and os.environ.get("NEMOTRON_SKIP_PIP") != "1":
    print(f"📦 Memasang pustaka yang belum tersedia: {missing_specs} ...")
    subprocess.check_call([
        sys.executable, "-m", "pip", "install", "--quiet",
        "--disable-pip-version-check", *missing_specs
    ])
    importlib.invalidate_caches()
    print("✅ Pemasangan pustaka selesai.")
elif not missing_specs:
    print("✅ Seluruh pustaka utama sudah terpasang di lingkungan runtime.")
else:
    print(f"ℹ️ Mode uji lokal tanpa instalasi pip otomatis (pustaka opsional belum terpasang: {missing_specs}).")

TORCH_AVAILABLE = _is_module_available("torch")
TRANSFORMERS_AVAILABLE = _is_module_available("transformers")

if TORCH_AVAILABLE:
    import torch
else:
    torch = None  # type: ignore

if TRANSFORMERS_AVAILABLE:
    import transformers
    from transformers import set_seed
else:
    transformers = None  # type: ignore
    set_seed = None  # type: ignore


def configure_reproducibility(seed: int = 42) -> None:
    """Atur seluruh generator angka acak dan bendera determinisme kernel."""
    os.environ.pop("CUDA_LAUNCH_BLOCKING", None)
    os.environ["CUBLAS_WORKSPACE_CONFIG"] = ":4096:8"
    os.environ["FLASH_ATTENTION_DETERMINISTIC"] = "1"
    random.seed(seed)
    if set_seed is not None:
        set_seed(seed, deterministic=True)
    if torch is not None:
        torch.manual_seed(seed)
        if hasattr(torch, "backends") and hasattr(torch.backends, "cudnn"):
            torch.backends.cudnn.deterministic = True
            torch.backends.cudnn.benchmark = False
        if torch.cuda.is_available():
            torch.cuda.manual_seed_all(seed)
            torch.backends.cuda.matmul.allow_tf32 = False
            torch.backends.cudnn.allow_tf32 = False


configure_reproducibility(TRAINING_SEEDS[0])

# 3. Deteksi Akselerator GPU & Penyesuaian Presisi Campuran (BF16 di A100/L4, FP16 di T4)
CUDA_AVAILABLE = bool(torch is not None and torch.cuda.is_available())
GPU_NAME = torch.cuda.get_device_name(0) if CUDA_AVAILABLE else "CPU"
GPU_COUNT = torch.cuda.device_count() if CUDA_AVAILABLE else 0
BF16_SUPPORTED = bool(CUDA_AVAILABLE and torch.cuda.is_bf16_supported())

if CUDA_AVAILABLE and BF16_SUPPORTED:
    USE_BF16 = True
    USE_FP16 = False
    PRECISION_MODE = "bf16"
elif CUDA_AVAILABLE:
    USE_BF16 = False
    USE_FP16 = True
    PRECISION_MODE = "fp16"
else:
    USE_BF16 = False
    USE_FP16 = False
    PRECISION_MODE = "fp32-cpu"

CONFIG["bf16"] = USE_BF16
CONFIG["fp16"] = USE_FP16
CONFIG["precision_mode"] = PRECISION_MODE

VRAM_GIB = (
    round(torch.cuda.get_device_properties(0).total_memory / (1024 ** 3), 2)
    if CUDA_AVAILABLE else 0.0
)
COMPUTE_CAPABILITY = (
    list(torch.cuda.get_device_capability(0))
    if CUDA_AVAILABLE else None
)

ENV_FINGERPRINT = {
    "python_version": platform.python_version(),
    "platform": platform.platform(),
    "torch_version": getattr(torch, "__version__", None),
    "torch_cuda_version": getattr(getattr(torch, "version", None), "cuda", None),
    "cudnn_version": (torch.backends.cudnn.version() if CUDA_AVAILABLE else None),
    "transformers_version": getattr(transformers, "__version__", None),
    "cuda_available": CUDA_AVAILABLE,
    "gpu_name": GPU_NAME,
    "gpu_count": GPU_COUNT,
    "vram_gib": VRAM_GIB,
    "compute_capability": COMPUTE_CAPABILITY,
    "bf16_supported": BF16_SUPPORTED,
    "precision_mode": PRECISION_MODE,
    "deterministic_algorithms": (
        torch.are_deterministic_algorithms_enabled() if torch is not None else True
    ),
    "cudnn_deterministic": (
        torch.backends.cudnn.deterministic if torch is not None else True
    ),
    "cudnn_benchmark": (
        torch.backends.cudnn.benchmark if torch is not None else False
    ),
    "tf32_allowed": False,
}

fingerprint_path = OUTPUT_DIR / "environment_fingerprint.json"
fingerprint_path.write_text(json.dumps(ENV_FINGERPRINT, indent=2, ensure_ascii=False), encoding="utf-8")
(OUTPUT_DIR / "experiment_config.json").write_text(json.dumps(CONFIG, indent=2, ensure_ascii=False), encoding="utf-8")
sync_to_drive(fingerprint_path, "environment_fingerprint.json")
sync_to_drive(OUTPUT_DIR / "experiment_config.json", "experiment_config.json")

print("=" * 72)
print("🖥️ LINGKUNGAN KOMPUTASI & AKSELERATOR GPU")
print(f"   Perangkat GPU       : {GPU_NAME} ({VRAM_GIB:.2f} GiB VRAM)")
print(f"   Compute Capability  : {COMPUTE_CAPABILITY}")
print(f"   Mode Presisi Aktif  : {PRECISION_MODE.upper()} (bf16={USE_BF16}, fp16={USE_FP16})")
print(f"   PyTorch / CUDA      : {ENV_FINGERPRINT['torch_version']} / CUDA {ENV_FINGERPRINT['torch_cuda_version']}")
print(f"   Transformers        : {ENV_FINGERPRINT['transformers_version']}")
print("=" * 72)
