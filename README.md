# Skripsi: Analisis Perbandingan Kinerja Fine-Tuning IndoBERT pada Named Entity Recognition (NER) Bahasa Indonesia Menggunakan Data Berbasis Anotasi Manusia dan Sintetis Berbasis LLM

Repositori ini memuat seluruh kode program, naskah akademik, dataset evaluasi, visualisasi hasil, modul pengujian, dan riwayat audit untuk penelitian skripsi:

> **"ANALISIS PERBANDINGAN KINERJA FINE-TUNING INDOBERT PADA NAMED ENTITY RECOGNITION (NER) BAHASA INDONESIA MENGGUNAKAN DATA BERBASIS ANOTASI MANUSIA DAN SINTETIS BERBASIS LLM"**

---

## 📑 Struktur Repositori

```text
.
├── antigravity_device_migration/   # Paket & skrip pemulihan sesi obrolan Antigravity untuk perangkat lain
│   ├── restore_session.py          # Skrip 1-klik pemulihan sesi ke ~/.gemini/antigravity/
│   ├── TUTORIAL_MIGRASI_PERANGKAT.txt # Panduan lengkap teks pemulihan sesi
│   ├── conversation_db_*.zip       # Database percakapan (.db)
│   ├── brain_*.zip                 # Artefak & riwayat pemikiran (.gemini/antigravity/brain/)
│   └── session_metadata.json       # Metadata sesi untuk conversation_summaries.db
│
├── audit_iaa/                      # Hasil & artefak Audit Independen Dua Penilai (IAA) 400 kalimat sintetis
│   ├── audit_iaa_results.zip       # Sampel evaluasi & prediksi dua penilai (2,2 MB)
│   ├── IAA_REPORT.md               # Laporan koefisien kesepakatan Cohen's Kappa & F1
│   ├── iaa_summary.json            # Ringkasan metrik statistik terstruktur
│   ├── consensus_records.jsonl     # Data konsensus evaluasi dua penilai
│   ├── disagreements.jsonl         # Kasus-kasus perbedaan anotasi antarpenilai
│   └── *.csv                       # Tabel metrik kesepakatan per dataset dan per kelas
│
├── data/
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
│   ├── papers/                     # 22 PDF makalah ilmiah primer rujukan naskah skripsi
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
│   ├── figures/                    # 16 gambar visualisasi grafik & kurva konvergensi (terlacak Git)
│   ├── BAB_4_Hasil.docx            # Ekspor naskah Bab 4 format Microsoft Word siap cetak
│   ├── BAB_4_Hasil.pdf             # Ekspor naskah Bab 4 format PDF profesional
│   └── BAB_4_Hasil.html            # Ekspor naskah Bab 4 format HTML interaktif (KaTeX)
│
├── notebooks/                      # Jupyter Notebooks untuk pelatihan Google Colab A100 GPU
│   ├── Optimasi_Hyperparameter_LR_IndoBERT_A100.ipynb # Notebook pencarian Learning Rate Pareto
│   ├── Eksperimen_NER_IndoBERT_A100.ipynb             # Notebook utama fine-tuning 84 run
│   ├── bab4_pipeline/              # Modul Python modular pendukung notebook
│   └── bab4_source_bundle.zip      # Bundel sumber data esensial untuk runtime Colab
│
├── scripts/                        # Skrip utilitas, audit, dan ekspor naskah
│   ├── run_independent_audit_iaa.py # Skrip audit independen dua model LLM via 9router
│   ├── export_chapter.py           # Generator ekspor naskah ke HTML, PDF, dan Word DOCX
│   └── *.py                        # Utilitas verifikasi kutipan dan integritas data
│
├── tests/                          # Rangkaian pengujian unit & integrasi (109 passed tests)
├── pytest.ini                      # Konfigurasi eksekusi pytest
├── requirements.txt                # Daftar seluruh dependensi pustaka Python
└── README.md                       # Dokumentasi repositori ini
```

---

## 🛠️ Panduan Instalasi Lingkungan Lokal

1. **Clone Repositori**:
   ```bash
   git clone https://github.com/Treamyracle/skripsi.git
   cd skripsi
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
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Verifikasi Lingkungan dengan Menjalankan Unit Tests**:
   ```bash
   pytest
   ```
   *(Seluruh 109 pengujian unit akan berjalan otomatis dan dipastikan lulus)*.

---

## 🚀 Menjalankan Eksperimen di Google Colab (GPU A100)

1. Buka Google Colab dan pilih runtime **GPU A100 High-RAM**.
2. Unggah atau tautkan salah satu notebook dari folder `notebooks/`:
   - [`notebooks/Optimasi_Hyperparameter_LR_IndoBERT_A100.ipynb`](notebooks/Optimasi_Hyperparameter_LR_IndoBERT_A100.ipynb): Untuk mereproduksi pencarian Learning Rate optimal ($1\times 10^{-5}$, $2\times 10^{-5}$, $3\times 10^{-5}$, $5\times 10^{-5}$). Temuan empiris membuktikan bahwa **$2\times 10^{-5}$** merupakan titik Pareto-optimal dengan konvergensi paling stabil dan $F_1$-score tertinggi ($84,79\%$).
   - [`notebooks/Eksperimen_NER_IndoBERT_A100.ipynb`](notebooks/Eksperimen_NER_IndoBERT_A100.ipynb): Untuk mereproduksi pelatihan 84 run model IndoBERT-Large lintas 7 dataset dan 3 seed acak (42, 123, 2026).

---

## 📊 Hasil Audit Independen (Inter-Annotator Agreement)

Audit independen terhadap 400 kalimat data sintetis (100 sampel terstratifikasi per korpus sintetis: Nemotron, Luna, Gemma, GPT-OSS; 10.812 token, 800 evaluasi independen) dilakukan secara mandiri oleh dua penilai independen:
- **Penilai A1**: Arif Athaya Harahap
- **Penilai A2**: Muhammad Faiz Fauzan

### Metrik Kesepakatan Utama (4 Korpus Sintetis):
- **Token Cohen's $\kappa$ (37 BIO tags)**: **0,987** [0,983 – 0,991] (*Almost Perfect Agreement*)
- **Token Cohen's $\kappa$ (18 entity classes)**: **0,989** [0,985 – 0,993] (*Almost Perfect Agreement*)
- **Pairwise Exact Span-$F_1$**: **97,63%** [96,84% – 98,34%]
- **Kesepakatan Token Identik**: **99,13%** (10.718 dari 10.812 token berlabel BIO identik)
- **Kalimat Identik Sempurna**: **89,75%** (359 / 400 kalimat disepakati 100% tanpa selisih)
- **Kualitas Anotasi Gabungan vs Konsensus**: Presisi **84,60%**, Recall **87,20%**, **$F_1$-Score 85,88%**

Hasil lengkap dan data per dataset tersedia di [`audit_iaa/IAA_REPORT.md`](audit_iaa/IAA_REPORT.md) dan [`laporan/LAMPIRAN_AUDIT_IAA.md`](laporan/LAMPIRAN_AUDIT_IAA.md).

---

## 💻 Melanjutkan Sesi Antigravity di Komputer / Laptop Lain

Jika Anda berpindah ke komputer atau laptop lain dan ingin melanjutkan sesi percakapan dengan AI asisten Antigravity secara utuh:

1. Clone repositori ini di perangkat baru:
   ```bash
   git clone https://github.com/Treamyracle/skripsi.git
   cd skripsi
   ```
2. Pastikan aplikasi Antigravity tertutup terlebih dahulu.
3. Jalankan skrip pemulihan 1-klik:
   ```bash
   python antigravity_device_migration/restore_session.py
   ```
4. Buka kembali aplikasi Antigravity. Sesi obrolan *"IndoBERT NER Thesis Progress Review"* akan langsung tampil di *sidebar* kiri beserta seluruh konteks pemikiran, kode, dan artefak sebelumnya!
