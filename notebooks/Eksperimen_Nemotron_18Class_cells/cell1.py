r"""# Eksperimen Komparatif NER Bahasa Indonesia: NERGRIT Gold vs Korpus Sintetis Nemotron 18-Kelas Baru (Terverifikasi Tahap 2)

**Cara Menjalankan di Google Colab (1-Klik):**
1. Buka notebook ini di Google Colab.
2. Pilih menu **Runtime → Change runtime type → Hardware accelerator: GPU (A100 / L4 / T4)**.
3. Klik **Runtime → Run all** dan izinkan akses **Google Drive** saat diminta.

---

### 1. Tujuan Eksperimen
Notebook mandiri (*self-contained*) ini dirancang untuk melatih dan mengevaluasi secara *head-to-head* model fondasi **`indobenchmark/indobert-large-p1`** (340M parameter, 24 layer) pada dua kondisi korpus latih:
1. **Skenario 1 — NERGRIT Gold Baseline (`gold`)**:
   Korpus anotasi manusia asli (`12.465` kalimat latih, `2.543` kalimat validasi) dengan normalisasi `REG` & `TTL` $\rightarrow$ `O` (**18 kelas entitas aktif / 37 tag BIO**).
2. **Skenario 2 — Korpus Sintetis Nemotron 18-Kelas Baru (`nemotron_18class`)**:
   Korpus hasil distilasi LLM yang telah selesai melalui **Verifikasi & Quality Control Tahap 2 (100% selesai: `17.525` kalimat, `119.680` entitas JSON / `118.596` rentang BIO)** menggunakan spesifikasi taksonomi 18 kelas ketat (`0` `REG`, `0` `TTL`, `0` kegagalan substring), disaring dengan penapis anti-kebocoran *character 5-gram Jaccard* $\ge 0,90$ terhadap Gold Test Set, dan dibagi secara deterministik ke dalam **85% Train (`14.896` kalimat) / 15% Validation (`2.629` kalimat)**.

Kedua model dievaluasi secara *blind* pada himpunan uji acuan manusia yang sama: **NERGRIT Gold Test Set (`2.423` kalimat, `8.890` rentang entitas)** menggunakan metrik **Exact Span Match tingkat CoNLL**.

---

### 2. Spesifikasi Hiperparameter Bersama (Identik 100% dengan Protokol Skripsi Tabel 3.2 & Tabel 4.13)

| Parameter Pelatihan | Nilai Konfigurasi | Keterangan |
| :--- | :--- | :--- |
| **Model Fondasi (*Backbone*)** | `indobenchmark/indobert-large-p1` | 24 layer, hidden size 1024, 340M parameter |
| **Taksonomi Label** | 18 Kelas Entitas / 37 Tag BIO | Eksklusi penuh `REG` & `TTL` $\rightarrow$ `O` |
| **Random Seed Pelatihan (`TRAINING_SEEDS`)** | `[42]` (1 Seed Deterministik) | Seed pembagian partisi `SPLIT_SEED = 42` |
| **Panjang Sekuens Maksimum (`max_seq_length`)** | `256` subword | *Lossless word-aligned chunking* & *recombination* |
| **Ukuran Batch Latih (`train_batch_size`)** | `32` (`grad_accum = 1`) | Ukuran batch efektif = 32 sekuens |
| **Ukuran Batch Evaluasi (`eval_batch_size`)** | `64` | Evaluasi akhir tiap epoch |
| **Laju Pembelajaran (`learning_rate`)** | `2e-5` ($2 \times 10^{-5}$) | Titik Pareto-optimal hasil penalaan empiris |
| **Pengoptimal (`optim`)** | `adamw_torch` | $\beta_1 = 0,9$; $\beta_2 = 0,999$; $\epsilon = 10^{-8}$; `weight_decay = 0,01` |
| **Penjadwal LR (`lr_scheduler_type`)** | `linear` (`warmup_ratio = 0,10`) | Pemanasan linier 10% dari total langkah |
| **Batas Epoch & Penghentian Dini** | `10` Epoch (`patience = 2`) | Pemantauan `eval_macro_f1` terbaik (`load_best_model_at_end = True`) |
| **Regularisasi & Gradien** | `dropout = 0,10`, `max_grad_norm = 1,0` | `pad_to_multiple_of = 8` |
| **Presisi Komputasi** | `bf16=True` (A100/L4) / `fp16=True` (T4) | Bobot utama model dalam `float32` |

---

### 3. Pencadangan & Pengunggahan Otomatis ke Google Drive
Seluruh tahapan eksperimen terintegrasi otomatis dengan **Google Drive** pada direktori:
`/content/drive/MyDrive/SKRIPSI_NER_BAB4/eksperimen_nemotron_18class/`
- **Sel 4**: Jika bundel input `nemotron_18class_colab_bundle.zip` diunduh dari GitHub, bundel tersebut langsung disalin otomatis ke Google Drive agar tersimpan permanen.
- **Sel 7 & Sel 8**: Setiap kali pelatihan model selesai, *checkpoint* model terbaik (`best_model`), riwayat pelatihan per epoch (`training_history.csv`/`.json`), dan manifes langsung dicadangkan otomatis ke Google Drive (mendukung *auto-resume* jika sesi Colab terputus).
- **Sel 10**: Seluruh tabel komparasi, prediksi `.jsonl`/`.conll`, analisis galat otomatis, dan grafik `.png` dikemas ke dalam **`nemotron_18class_experiment_results.zip`**, diunggah otomatis ke Google Drive, serta diunduh ke peramban Anda.
"""
