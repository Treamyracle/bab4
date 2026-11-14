# Skripsi: Analisis Perbandingan Kinerja Fine-Tuning IndoBERT pada Named Entity Recognition (NER) Bahasa Indonesia Menggunakan Data Berbasis Anotasi Manusia dan Sintetis Berbasis LLM

Repositori ini memuat seluruh kode program, naskah akademik, dataset evaluasi, visualisasi hasil, modul pengujian, dan riwayat audit untuk penelitian skripsi:

> **"ANALISIS PERBANDINGAN KINERJA FINE-TUNING INDOBERT PADA NAMED ENTITY RECOGNITION (NER) BAHASA INDONESIA MENGGUNAKAN DATA BERBASIS ANOTASI MANUSIA DAN SINTETIS BERBASIS LLM"**

> 💻 **Pindah Perangkat / Lanjutkan Percakapan Antigravity di Laptop?** Lihat panduan lengkap Markdown di [`antigravity_device_migration/README.md`](antigravity_device_migration/README.md) (Session ID: `81089962-53ae-4754-ac53-0a755e441870`).

---

## 📑 Struktur Repositori

```text
.
├── antigravity_device_migration/   # Paket & skrip pemulihan sesi obrolan Antigravity untuk perangkat lain
│   ├── README.md                   # Panduan transfer & pemulihan sesi lengkap (Markdown)
│   ├── restore_session.py          # Skrip 1-klik pemulihan sesi ke ~/.gemini/antigravity/
│   ├── link_to_workspace.py        # Skrip menautkan sesi ke folder repositori baru
│   ├── TUTORIAL_MIGRASI_PERANGKAT.txt # Panduan ringkas versi teks
│   ├── conversation_db_*.zip       # Database percakapan (.db)
│   ├── brain_*.zip                 # Artefak & riwayat pemikiran (.gemini/antigravity/brain/)
│   └── session_metadata.json       # Metadata sesi untuk conversation_summaries.db
│
├── audit_iaa_18class/              # Hasil & artefak Audit Independen Dua Penilai (IAA) 18-kelas terbaru (300 kalimat)
│   ├── audit_iaa_results.zip       # Sampel evaluasi & prediksi dua penilai
│   ├── IAA_REPORT.md               # Laporan koefisien kesepakatan Cohen's Kappa & F1 (18-kelas)
│   ├── iaa_summary.json            # Ringkasan metrik statistik terstruktur
│   ├── consensus_records.jsonl     # Data konsensus evaluasi dua penilai
│   ├── disagreements.jsonl         # Kasus-kasus perbedaan anotasi antarpenilai
│   └── *.csv                       # Tabel metrik kesepakatan per dataset dan per kelas
│
├── audit_iaa/                      # Arsip hasil Audit Independen Dua Penilai (IAA) sebelumnya (400 kalimat)
│   └── IAA_REPORT.md
│
├── data/
│   ├── distilled_nemotron_verified/# Korpus sintetis 18-kelas Nemotron Ultra terverifikasi (17.525 kalimat)
│   ├── distilled_gemma_verified/   # Korpus sintetis 18-kelas Gemma terverifikasi (17.434 kalimat)
│   ├── distilled_luna_verified/    # Korpus sintetis 18-kelas Luna terverifikasi Gemini 3.8 Flash (17.427 kalimat)
│   ├── distilled/raw/              # Dataset mentah sumber Hugging Face sebelum verifikasi 18-kelas
│   └── evaluation_tables/          # Tabel evaluasi lengkap 84 eksperimen model IndoBERT-Large
│       ├── evaluation_runs.csv     # Metrik per run (F1, Precision, Recall, Loss, Waktu)
│       ├── evaluation_mean_std.csv # Agregasi mean ± std deviasi antar seed (42, 123, 2026)
│       ├── evaluation_per_class.csv# Performa model per 18 kelas entitas NER
│       └── experiment_summary.json # Ringkasan JSON komprehensif
│
├── dataset_pipeline_code/          # Pipeline generasi dan koreksi sintetis 2-fase
│   ├── 1_nemotron_super_ultra/     # Nemotron-4 340B / Ultra 550B
│   ├── 2_gpt_5_6_luna/             # GPT-5 / GPT-6 Luna
│   ├── 3_gpt_oss_120b/             # GPT-OSS 120B
│   └── 4_gemma_4_31b/              # Gemma 4 31B
│
├── docs/
│   ├── NERGRIT_VERIFICATION_PROMPT.md # Spesifikasi prompt & aturan verifikasi 18 kelas (0 REG, 0 TTL)
│   ├── papers/                     # Makalah ilmiah primer rujukan naskah skripsi
│   ├── extracted_papers/           # Ekstraksi teks & metadata makalah untuk audit kutipan
│   └── exact_quotes_verified.json  # Katalog sitasi terverifikasi ketat
│
├── laporan/                        # Naskah tesis & berkas publikasi ilmiah
│   ├── BAB_1.md                    # Pendahuluan & Latar Belakang
│   ├── BAB_2.md                    # Tinjauan Pustaka & Landasan Teori
│   ├── BAB_3.md                    # Metodologi Penelitian & Desain Eksperimen
│   ├── BAB_4.md                    # Hasil Eksperimen, Optimasi LR & Pembahasan
│   ├── DAFTAR_PUSTAKA.md           # Daftar referensi naskah
│   ├── LAMPIRAN_EKSPERIMEN.md      # Rincian teknis 84 konfigurasi run
│   ├── LAMPIRAN_AUDIT_IAA.md       # Laporan resmi statistik Inter-Annotator Agreement
│   ├── figures/                    # Gambar visualisasi grafik & kurva konvergensi
│   ├── BAB_4_Hasil.docx            # Ekspor naskah Bab 4 format Microsoft Word
│   ├── BAB_4_Hasil.pdf             # Ekspor naskah Bab 4 format PDF
│   └── BAB_4_Hasil.html            # Ekspor naskah Bab 4 format HTML interaktif
│
├── notebooks/                      # Jupyter Notebooks & bundel eksperimen Google Colab A100 GPU
│   ├── Eksperimen_Nemotron_18Class_Colab.ipynb # Notebook eksperimen 18-kelas
│   ├── nemotron_18class_colab_bundle.zip       # Bundel eksperimen 18-kelas siap Colab
│   ├── experiments/nemotron_18class/           # Hasil eksperimen awal Nemotron 18-kelas
│   ├── Optimasi_Hyperparameter_LR_IndoBERT_A100.ipynb # Pencarian Learning Rate Pareto
│   ├── Eksperimen_NER_IndoBERT_A100.ipynb      # Notebook utama fine-tuning 84 run
│   └── bab4_pipeline/              # Modul Python pendukung notebook
│
├── scripts/                        # Skrip verifikasi 18-kelas, audit IAA, dan utilitas
│   ├── verify_nemotron_ultra.py    # Verifikator 18-kelas untuk Nemotron
│   ├── verify_gemma_nemotron_vl.py # Verifikator 18-kelas untuk Gemma (OpenRouter)
│   ├── verify_luna_gemini.py       # Verifikator 18-kelas untuk Luna (Gemini 3.8 Flash Low via 9router)
│   ├── verify_gemma_gemini.py      # Verifikator 18-kelas untuk Gemma (Gemini 3.8 Flash Low via 9router)
│   └── run_independent_audit_iaa.py# Skrip audit independen dua model LLM via 9router
│
├── tests/                          # Rangkaian pengujian unit & integrasi
└── README.md                       # Dokumentasi repositori ini
```

---

## 🛠️ Panduan Instalasi Lingkungan Lokal

1. **Clone Repositori**:
   ```bash
   # Pilih salah satu repo:
   git clone https://github.com/Treamyracle/skripsi.git && cd skripsi
   # atau repo Bab 4 & 18-class datasets:
   git clone https://github.com/Treamyracle/bab4.git && cd bab4
   ```

2. **Buat dan Aktifkan Virtual Environment**:
   ```bash
   python -m venv venv
   # Di Windows:
   venv\Scripts\activate
   # Di Linux / macOS:
   source venv/bin/activate
   ```

3. **Instal Dependensi**:
   ```bash
   pip install --upgrade pip requests
   ```

4. **Verifikasi Lingkungan dengan Menjalankan Unit Tests**:
   ```bash
   python -m unittest discover -s tests
   ```

---

## 🧬 Dataset Terverifikasi 18-Kelas & Audit IAA Terbaru (`audit_iaa_18class/`)

Seluruh korpus 18-kelas (`0 REG`, `0 TTL`) berdasarkan aturan terbaru (`docs/NERGRIT_VERIFICATION_PROMPT.md`) beserta Audit Independen Dua Penilai telah selesai dan tersinkronisasi:

### 1. Tiga Korpus Sintetis Terverifikasi 18-Kelas
- **`data/distilled_nemotron_verified/`** — **17.525 / 17.525 kalimat** (`nvidia/nemotron-3-ultra-550b-a55b:free`)
- **`data/distilled_gemma_verified/`** — **17.434 / 17.434 kalimat** (`nvidia/nemotron-3.5-super-vl:free`)
- **`data/distilled_luna_verified/`** — **17.427 / 17.427 kalimat** (`ag/gemini-3.8-flash-low` via 9router)
- **`data/distilled/raw/`** — Korpus sumber mentah Hugging Face untuk ketiga dataset
- **`notebooks/experiments/nemotron_18class/`** — Hasil evaluasi eksperimen awal Nemotron 18-kelas

### 2. Audit Independen Dua Penilai 18-Kelas (`audit_iaa_18class/`)
- **Sampel**: **300 / 300 kalimat terstratifikasi** (100 sampel per korpus: `nemotron`, `luna`, `gemma`; `7.732` token; seed `20261022`)
- **Penilai A1**: `cx/gpt-6-luna` (`reasoning_effort: high`)
- **Penilai A2**: `ag/gemini-3.8-flash-high` (`reasoning_effort: high`)
- **Metrik Total (95% Bootstrap CI)**:
  - **Token Cohen's $\kappa$ (37 BIO tags)**: **0,966** `[0,958–0,972]` (*Hampir sempurna / almost perfect*)
  - **Token Cohen's $\kappa$ (18 classes + O)**: **0,972** `[0,966–0,978]` (*Hampir sempurna / almost perfect*)
  - **Pairwise Exact Span-$F_1$**: **0,938** `[0,926–0,950]`
  - **Dataset Annotation Quality vs Dual-Agreement Consensus**: Presisi **95,07%**, Recall **95,13%**, **$F_1$-Score 95,10%**
- Laporan lengkap: [`audit_iaa_18class/IAA_REPORT.md`](audit_iaa_18class/IAA_REPORT.md)

---

## 📊 Arsip Hasil Audit Independen Sebelumnya (`audit_iaa/`, 400 Kalimat)

Audit independen terhadap 400 kalimat data sintetis sebelumnya (`audit_iaa/`):
- **Token Cohen's $\kappa$ (37 BIO tags)**: **0,987** [0,983 – 0,991] (*Almost Perfect Agreement*)
- **Token Cohen's $\kappa$ (18 entity classes)**: **0,989** [0,985 – 0,993] (*Almost Perfect Agreement*)
- **Pairwise Exact Span-$F_1$**: **97,63%** [96,84% – 98,34%]
- **Kualitas Anotasi Gabungan vs Konsensus**: **$F_1$-Score 85,88%**
- Hasil lengkap tersedia di [`audit_iaa/IAA_REPORT.md`](audit_iaa/IAA_REPORT.md).

---

## 💻 Transfer & Melanjutkan Percakapan Antigravity di Laptop / Perangkat Lain

> 📖 **Panduan lengkap transfer percakapan (Markdown):** [`antigravity_device_migration/README.md`](antigravity_device_migration/README.md)

Seluruh riwayat sesi percakapan ini (**Session ID:** `81089962-53ae-4754-ac53-0a755e441870`, **Title:** `SKRIPSI`), database chat SQLite, log, dan artefak telah dikemas di folder [`antigravity_device_migration/`](antigravity_device_migration/):

1. Pastikan Antigravity sudah terpasang di laptop Anda (buka 1x lalu **tutup Antigravity sepenuhnya** agar SQLite database tidak terkunci).
2. Clone repositori di perangkat baru (`https://github.com/Treamyracle/skripsi.git` atau `https://github.com/Treamyracle/bab4.git`).
3. Jalankan skrip pemulihan 1-klik dari root folder repositori:
   ```bash
   python antigravity_device_migration/restore_session.py
   ```
4. Buka kembali aplikasi Antigravity, pilih **Open Folder** ke folder repositori hasil clone — sesi **`SKRIPSI`** (`81089962-53ae-4754-ac53-0a755e441870`) akan langsung aktif di sidebar obrolan.
5. *(Opsional)* Untuk menjalankan ulang skrip OpenRouter di laptop, set `OPENROUTER_API_KEY` secara lokal (kunci asli sengaja tidak disimpan di GitHub). Baca panduan lengkap di [`antigravity_device_migration/README.md`](antigravity_device_migration/README.md).
