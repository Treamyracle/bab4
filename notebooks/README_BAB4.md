# Eksperimen Bab 4 — raw-v2

Notebook menggunakan **18 kelas entitas / 37 tag BIO**, dengan konfigurasi
pelatihan bersama yang sama seperti protokol sebelumnya. Revisi raw-v2
mempertahankan seluruh record, duplikat, konflik anotasi, token sumber, dan
transisi BIO. Pembagian partisi dikelompokkan ulang untuk mencegah overlap teks.

## Menjalankan di Google Colab A100

1. Buka **Eksperimen_NER_IndoBERT_A100.ipynb** melalui Upload notebook di Colab.
2. Pilih GPU A100, kemudian **Run all** dan berikan akses Drive saat diminta.
3. Input diunduh otomatis dari commit Hugging Face yang terkunci; tidak ada ZIP input
   yang perlu diunggah. Lihat [panduan satu notebook](README_COLAB.md).
4. Hasil profil baru tersimpan di **My Drive/SKRIPSI_NER_BAB4/bab4_results_raw_v2/a100_bf16_b32_v2/**.
   Kembalikan **a100_bf16_b32_v2.zip** setelah eksperimen selesai. Input/data persiapan yang
   terverifikasi digunakan kembali dari folder induk; run profil lama tetap tersimpan.

Gunakan notebook A100 terbaru untuk eksperimen baru. Snapshot lama `bab4_results/`
dan audit yang sudah diperiksa tetap disimpan. Checkpoint v1 tidak dipakai
untuk melanjutkan eksperimen dengan data v2. Resume v2 memverifikasi manifest,
model, optimizer, scheduler, dan RNG sebelum melanjutkan checkpoint. BF16 tidak
memerlukan gradient scaler; scaler tetap diwajibkan untuk checkpoint FP16 lama.
Bobot model terpilih tetap di Drive; sediakan ruang penyimpanan yang cukup.

## Kebijakan data dan koreksi kode label

- NERGRIT adalah dataset manusia/Gold; empat korpus sintetis adalah Nemotron,
  Luna, Gemma, dan GPT-OSS. Benchmark tambahan bersifat sintetis.
- Semua **88.252 record sumber** dipertahankan. Token sumber tetap sama,
  termasuk token kosong dan spasi yang tersimpan di dalam token.
- Kode label salah tulis dibaca memakai `labels-map.csv` dan pengecualian
  eksplisit yang sudah didokumentasikan. Misalnya `B-L0C → B-LOC`,
  `B=CRD → B-CRD`, dan `B-PER. → B-PER`. Setiap perubahan dicatat pada
  `tables/label_format_corrections.csv`; label mentah tetap diarsipkan.
- Transisi I yang tidak konsisten tidak diperbaiki. Decoder span membaca I
  tanpa pendahulu sejenis sebagai awal span untuk statistik/evaluasi.
- REG dikecualikan karena anotasinya ambigu dan dapat bertumpang tindih
  dengan kelas lain. Perbedaan Region/Religion merupakan contoh pendukung.
  REG/TTL dipetakan ke O pada eksperimen; token tetap disupervisi sebagai latar.
  CRD dan QTY tetap terpisah.
- WordPiece hanya digunakan pada adapter model. Token yang tidak menghasilkan
  subword diberi representasi [UNK] tanpa menghapus indeks token sumber.

## Partisi dan pemeriksaan kebocoran

Normalisasi Unicode, huruf, dan tanda baca digunakan hanya untuk pembandingan.
Teks sama dan kalimat minimal 10 token dengan Jaccard character 5-gram ≥0,90
dikelompokkan secara global. Semua anggota kelompok ditempatkan pada satu
peran dengan prioritas **test → validation → train**. Kelompok sintetis yang
tidak terikat test dibagi mendekati 85:15, seed 42. Konflik label tetap disimpan.

Partisi raw-v2 terverifikasi:

| Dataset | Train | Validation | Test | Total |
|---|---:|---:|---:|---:|
| NERGRIT/Gold | 12.465 | 2.543 | 2.423 | 17.431 |
| Nemotron | 14.896 | 2.629 | 0 | 17.525 |
| Luna | 14.813 | 2.614 | 0 | 17.427 |
| Gemma | 14.819 | 2.615 | 0 | 17.434 |
| GPT-OSS | 14.820 | 2.615 | 0 | 17.435 |
| Benchmark sintetis | — | — | 1.000 | 1.000 |

Test Gold tersebut adalah hasil pengelompokan ulang dan berbeda dari split
resmi NERGRIT. Pemeriksaan mencatat nol kelompok yang melintasi partisi dalam
cakupan tersebut. Document ID dan keanggotaan data pretraining tidak tersedia.
Korpus eksternal disimpan utuh secara privat; penanda kelayakan evaluasi
bersama menahan contoh overlap dari penghitungan skor generalisasi.

## Audit manusia yang telah selesai dan Audit Independen IAA

1. **Audit Konsensus Historis Satu Sesi (16 Oktober 2026)**:
   **Arif Athaya Harahap** dan **Muhammad Faiz Fauzan** memeriksa bersama
   100 kalimat per dataset pada snapshot awal. Seluruh 600 keputusan tercatat:
   **2.959 benar, 73 salah, dan 43 terlewat**.

2. **Audit Independen Dua Penilai & Inter-Annotator Agreement (22 Oktober 2026)**:
   Audit reliabilitas ilmiah definitif dilakukan secara mandiri (*blind* dan independen)
   pada sampel terstratifikasi 100 kalimat per korpus sintetis (total **400 kalimat**,
   **10.812 token**, **800 evaluasi independen**, seed `20261022`).
   Menghasilkan **κ token BIO = 0,987**, **κ token kelas = 0,989**, **Pairwise Span-F₁ = 97,63%**,
   dan **89,75% kalimat identik sempurna (359/400)**. Kualitas anotasi gabungan
   mencapai Presisi 84,60%, Recall 87,20%, dan F₁ = 85,88%.

Sampel berasal dari snapshot persiapan terdahulu. Bundle historis menyimpan
manifest lama, keenam TXT, dan manifest sampel tanpa mengubah hash aslinya.
Validasi memeriksa semua keputusan terhadap manifest itu dan menautkan kembali
600 sampel ke source record v2. Pada 14 sampel, token tampilan audit terdahulu
berbeda dari token sumber. Keputusan tetap dilaporkan untuk representasi yang
benar-benar diperiksa. Audit tidak mengubah label training dan bobot strata
lama tidak menjadi estimasi kualitas seluruh populasi raw-v2.

Preseden anggaran audit: [Koto et al. (2020)](https://aclanthology.org/2020.coling-main.66/).
Stratifikasi diadaptasi dari [Saldías Fuentes et al. (2022)](https://aclanthology.org/2022.humeval-1.7/),
dengan seed 20261016 dan strata panjang kalimat × jumlah entitas.

## Statistik dan pelatihan

S=kalimat, T=token sumber, E=rentang entitas, T_e=token berentitas, dan E_c=entitas
kelas c. Rata-rata token=T/S; rata-rata entitas=E/S; kepadatan token=100T_e/T%;
entitas per 100 token=100E/T; proporsi kelas=100E_c/E%. Subword dan padding
tidak dihitung. Statistik seluruh korpus dan train disajikan terpisah.

Seluruh kondisi: IndoBERT-large-p1 dengan revisi terkunci, AdamW, learning rate
2e-5, weight decay 0.01, warmup 0.10, scheduler linear, microbatch 32 × akumulasi
1 (batch efektif 32), eval batch 64, bobot FP32 / mixed precision BF16, panjang maksimum 256, maksimum 10 epoch, patience 2,
dan pemilihan checkpoint berdasarkan validation macro-F1 18 kelas tetap.
Seed: 42, 123, 2026. Test baru dinilai setelah pemilihan semua checkpoint.

Profil bersama `a100-bf16-b32-v2` menonaktifkan gradient checkpointing dan
pemaksaan CUDA launch blocking, sambil mempertahankan algoritme deterministik,
seed, serta TF32 nonaktif. Loader memakai empat worker dan padding kelipatan
delapan. Pemeriksaan singkat IndoBERT pada batch 32/panjang 256 mencatat throughput
serta peak VRAM aktual sebelum 84 fit; hasil setup tidak menjadi metrik penelitian.
Batch efektif 32 mengubah jumlah langkah optimasi dibandingkan profil 16 terdahulu.
Learning rate tidak dinaikkan otomatis. Profil BF16 baru dimulai dari backbone awal;
checkpoint FP16 sebelumnya dipertahankan dalam folder asal dan tidak digunakan ulang.

Jangkar iso-entity raw-v2 adalah **42.614 entitas Gold train**. Target tetap
30/50/75/100/125/150% dan maksimum. Rencana aktual memuat **84 fit berbeda**;
target Gemma 150% tidak tersedia. Seluruh angka dihitung dari manifest v2.

## Tahap, artefak, dan pembangunan ulang

Notebook umum mendukung `prepare_audit`, `audit_report`, `train_and_evaluate`,
dan `export_results`. Default memvalidasi audit historis. Untuk audit baru,
set `HISTORICAL_AUDIT_BUNDLE=None` dan gunakan output directory yang berbeda.
Kode impor audit baru tetap menolak manifest dari snapshot lain.

Artefak utama: `prepared/manifest.json`, `DATASET_ANALYSIS.md`, `tables/`,
`figures/`, `audit_results/audit_provenance.json`, `BAB_4_DRAFT.md`, dan hasil
model setelah training. ZIP ringkasan tidak menyertakan bobot model atau data
mentah/prediksi per kalimat korpus eksternal, terutama Singgalang.

Pembangunan ulang lokal:

```powershell
python scripts/package_a100_continue.py --historical-only
python scripts/prepare_raw_v2.py
python scripts/report_completed_audit.py
python scripts/build_hf_a100.py
```

Notebook A100 dibangun dari satu berkas `.py` per sel di
`Eksperimen_NER_IndoBERT_A100_cells/`. Edit `cell_1.py`, `cell_2.py`, dan
seterusnya lalu jalankan builder; build biasa tidak mengganti edit tersebut.

Bab 4 dan lampiran dihasilkan dari artefak tervalidasi. Hasil model yang belum
tersedia tidak diisi nol. Pemeriksaan CPU terpisah dari pelatihan IndoBERT
sesungguhnya di A100.

Input diterbitkan dengan allowlist melalui `scripts/publish_bab4_hf.py --publish-inputs`.
Sesudah commit input diverifikasi, notebook dibangun dengan revisi tersebut dan
diterbitkan melalui `--publish-notebook`. Receipt berada di `hf_input_release.json`
dan `hf_notebook_release.json`; token tidak disertakan.
