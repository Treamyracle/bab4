# Independent Dual-Annotator Audit & Inter-Annotator Agreement (IAA)

Direktori ini berisi seluruh data artefak, manifest sampling, prediksi dua model penilai independen, dan metrik reliabilitas kesepakatan (*inter-annotator agreement*) untuk evaluasi kualitas dataset pada penelitian skripsi.

## Ringkasan Eksekutif
- **Evaluator A1**: Arif Athaya Harahap
- **Evaluator A2**: Muhammad Faiz Fauzan
- **Jumlah Sampel**: 400 kalimat (100 sampel terstratifikasi per korpus sintetis: Nemotron, Luna, Gemma, GPT-OSS; 10.812 token, 800 evaluasi independen)
- **Token Cohen's $\kappa$ (37 BIO tags)**: **0,987** [0,983 – 0,991] (*Almost Perfect Agreement*)
- **Token Cohen's $\kappa$ (18 classes + O)**: **0,989** [0,985 – 0,993] (*Almost Perfect Agreement*)
- **Pairwise Exact Span-$F_1$**: **97,63%** [96,84% – 98,34%]
- **Kesepakatan Token Identik**: **99,13%** (10.718 dari 10.812 token berlabel BIO identik)
- **Kalimat Identik Sempurna**: **89,75%** (359 dari 400 kalimat disepakati 100% tanpa selisih)
- **Kualitas Anotasi Gabungan vs Konsensus**: Presisi **84,60%**, Recall **87,20%**, **$F_1$-Score 85,88%**

## Berkas dalam Direktori Ini:
1. `audit_iaa_results.zip`: Arsip terkompresi lengkap seluruh output perbandingan dan prediksi JSONL dari kedua model penilai (2,2 MB).
2. `IAA_REPORT.md`: Laporan metrik statistik kesepakatan Cohen's Kappa dan perbandingan presisi/recall kualitas dataset.
3. `iaa_summary.json`: Ringkasan metrik dalam format JSON terstruktur untuk konsumsi programatis.
4. `audit_sample_manifest.json`: Metadata sampel kalimat beserta hash dan indeks data aslinya.
5. `consensus_records.jsonl`: Rekaman kalimat konsensus hasil kesepakatan kedua penilai.
6. `disagreements.jsonl`: Daftar seluruh kasus selisih anotasi (*disagreements*) antara kedua penilai beserta analisis kategorinya.
7. File CSV:
   - `iaa_per_dataset.csv`: Metrik kesepakatan per dataset.
   - `iaa_per_class.csv`: Metrik kesepakatan per kelas entitas.
   - `consensus_quality_per_dataset.csv`: Kualitas anotasi dataset terhadap konsensus per dataset.
   - `consensus_quality_per_class.csv`: Kualitas anotasi per kelas entitas.
   - `annotator_quality_per_dataset.csv`: Perbandingan performa kedua penilai terhadap konsensus.

## Reproduksi Audit
Skrip eksekusi audit dapat dijalankan ulang menggunakan:
```bash
python scripts/run_independent_audit_iaa.py
```
*(Memerlukan konfigurasi `ROUTER_BASE_URL` dan `ROUTER_API_KEY` pada file `.env`)*
