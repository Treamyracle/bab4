# =============================================================================
# SEL 4: UNDUH / MUAT BUNDLE DATA, UPLOAD OTOMATIS KE GOOGLE DRIVE, & VERIFIKASI SHA-256
# =============================================================================
import urllib.request
import zipfile

BUNDLE_FILENAME = "nemotron_18class_colab_bundle.zip"
GITHUB_BUNDLE_URLS = (
    "https://raw.githubusercontent.com/Treamyracle/bab4/main/notebooks/nemotron_18class_colab_bundle.zip",
    "https://raw.githubusercontent.com/Treamyracle/skripsi/main/notebooks/nemotron_18class_colab_bundle.zip",
    "https://github.com/Treamyracle/bab4/raw/main/notebooks/nemotron_18class_colab_bundle.zip",
    "https://github.com/Treamyracle/skripsi/raw/main/notebooks/nemotron_18class_colab_bundle.zip",
)

REQUIRED_BUNDLE_MEMBERS = (
    "gold/train.txt",
    "gold/valid.txt",
    "gold/test.txt",
    "gold/labels-map.csv",
    "nemotron_18class/corrected.jsonl",
    "bundle_manifest.json",
)


def locate_or_download_bundle(
    local_work_dir: Path = LOCAL_WORK_DIR,
    drive_base_dir: Path = DRIVE_BASE_DIR,
    urls: tuple[str, ...] = GITHUB_BUNDLE_URLS,
) -> tuple[Path, str]:
    """Cari bundel data di lokal/Drive atau unduh otomatis dari GitHub, lalu unggah otomatis ke Google Drive."""
    drive_bundle_path = drive_base_dir / BUNDLE_FILENAME
    local_candidates = [
        Path.cwd() / "notebooks" / BUNDLE_FILENAME,
        Path.cwd() / BUNDLE_FILENAME,
        Path("/content") / BUNDLE_FILENAME,
        local_work_dir / BUNDLE_FILENAME,
        drive_bundle_path,
        Path("/content/drive/MyDrive/SKRIPSI_NER_BAB4") / BUNDLE_FILENAME,
    ]

    found_path: Path | None = None
    source_origin = "unknown"

    for candidate in local_candidates:
        if candidate.is_file() and candidate.stat().st_size > 100_000:
            found_path = candidate.resolve()
            source_origin = "google_drive" if str(drive_base_dir) in str(found_path) else "local_filesystem"
            print(f"📂 Bundel data ditemukan ({source_origin}): {found_path} ({found_path.stat().st_size / (1024 * 1024):.2f} MB)")
            break

    if found_path is None:
        download_target = local_work_dir / BUNDLE_FILENAME
        download_target.parent.mkdir(parents=True, exist_ok=True)
        last_error: Exception | None = None
        for url in urls:
            try:
                print(f"🌐 Mengunduh {BUNDLE_FILENAME} dari GitHub:\n   {url}")
                req = urllib.request.Request(
                    url,
                    headers={"User-Agent": "IndoBERT-Nemotron18Class-Colab/1.0"},
                )
                t0 = time.time()
                with urllib.request.urlopen(req, timeout=120) as resp, download_target.open("wb") as out_f:
                    shutil.copyfileobj(resp, out_f)
                if download_target.stat().st_size < 100_000:
                    raise RuntimeError("Ukuran berkas unduhan terlalu kecil / tidak valid.")
                elapsed = time.time() - t0
                print(f"✅ Unduhan dari GitHub selesai dalam {elapsed:.2f}s ({download_target.stat().st_size / (1024 * 1024):.2f} MB).")
                found_path = download_target.resolve()
                source_origin = f"github:{url}"
                break
            except Exception as exc:
                last_error = exc
                print(f"⚠️ Gagal mengunduh dari {url}: {exc}")

        if found_path is None and IN_COLAB:
            try:
                from google.colab import files  # type: ignore
                print("📤 Silakan unggah berkas 'nemotron_18class_colab_bundle.zip' secara manual:")
                uploaded = files.upload()
                if uploaded:
                    first_name = next(iter(uploaded))
                    download_target.write_bytes(uploaded[first_name])
                    found_path = download_target.resolve()
                    source_origin = "colab_manual_upload"
            except Exception as exc:
                last_error = exc

        if found_path is None:
            raise FileNotFoundError(
                f"Tidak dapat menemukan atau mengunduh {BUNDLE_FILENAME}. Galat terakhir: {last_error}"
            )

    # Pastikan bundel otomatis disalin/diunggah ke Google Drive agar tersimpan permanen
    try:
        need_drive_copy = (
            not drive_bundle_path.is_file()
            or compute_sha256(drive_bundle_path) != compute_sha256(found_path)
        )
        if need_drive_copy:
            print(f"☁️ Menyimpan otomatis {BUNDLE_FILENAME} ke Google Drive ({drive_bundle_path})...")
            sync_to_drive(found_path, BUNDLE_FILENAME, verify_hash=True)
        else:
            print(f"☁️ Salinan {BUNDLE_FILENAME} di Google Drive sudah mutakhir dan terverifikasi SHA-256.")
    except Exception as exc:
        print(f"⚠️ Peringatan: Gagal menyinkronkan bundel ke Google Drive: {exc}")

    return found_path, source_origin


def extract_and_verify_bundle(bundle_path: Path, extract_dir: Path = DATA_DIR) -> dict:
    """Ekstrak bundel input dan verifikasi integritas SHA-256 serta jumlah kalimat."""
    extract_dir.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(bundle_path, "r") as zf:
        names = set(zf.namelist())
        missing = [req for req in REQUIRED_BUNDLE_MEMBERS if req not in names]
        if missing:
            raise ValueError(f"Bundel data tidak lengkap! Berkas hilang: {missing}")
        zf.extractall(extract_dir)

    manifest_path = extract_dir / "bundle_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    expected_hashes = manifest.get("sha256", {})

    verified_files = {}
    for rel_path, expected_sha in expected_hashes.items():
        target = extract_dir / rel_path
        if not target.is_file():
            raise FileNotFoundError(f"Berkas hasil ekstraksi tidak ditemukan: {target}")
        actual_sha = compute_sha256(target)
        if actual_sha != expected_sha:
            raise ValueError(
                f"Verifikasi SHA-256 gagal untuk {rel_path}: diharapkan {expected_sha}, aktual {actual_sha}"
            )
        verified_files[rel_path] = actual_sha

    nemotron_jsonl = extract_dir / "nemotron_18class" / "corrected.jsonl"
    nemotron_lines = [
        line for line in nemotron_jsonl.read_text(encoding="utf-8").splitlines() if line.strip()
    ]
    expected_nemotron_count = manifest.get("record_counts", {}).get("nemotron_18class_sentences", 17525)
    if len(nemotron_lines) != expected_nemotron_count:
        raise ValueError(
            f"Jumlah kalimat Nemotron 18-Kelas tidak cocok: diharapkan {expected_nemotron_count}, ditemukan {len(nemotron_lines)}"
        )

    bundle_report = {
        "bundle_path": str(bundle_path),
        "bundle_sha256": compute_sha256(bundle_path),
        "extracted_dir": str(extract_dir),
        "verified_files": verified_files,
        "record_counts": manifest.get("record_counts", {}),
        "nemotron_sentences_verified": len(nemotron_lines),
    }
    report_path = OUTPUT_DIR / "bundle_verification.json"
    report_path.write_text(json.dumps(bundle_report, indent=2, ensure_ascii=False), encoding="utf-8")
    sync_to_drive(report_path, "bundle_verification.json")
    return bundle_report


BUNDLE_PATH, BUNDLE_ORIGIN = locate_or_download_bundle()
BUNDLE_VERIFICATION = extract_and_verify_bundle(BUNDLE_PATH, DATA_DIR)

print("=" * 72)
print("📦 BUNDEL DATA INPUT TERVERIFIKASI (SHA-256 LULUS 100%)")
print(f"   Sumber Bundel        : {BUNDLE_ORIGIN}")
print(f"   Lokasi Bundel Lokal  : {BUNDLE_PATH}")
print(f"   SHA-256 Bundel       : {BUNDLE_VERIFICATION['bundle_sha256']}")
print(f"   Kalimat Nemotron 18C : {BUNDLE_VERIFICATION['nemotron_sentences_verified']:,} kalimat")
for rel_file, sha_val in sorted(BUNDLE_VERIFICATION["verified_files"].items()):
    print(f"   ✓ {rel_file:<34} sha256={sha_val[:16]}...")
print("=" * 72)
