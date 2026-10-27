# LAMPIRAN: AUDIT INDEPENDEN DUA PENILAI & INTER-ANNOTATOR AGREEMENT (IAA)

Dokumen ini mendokumentasikan hasil pengujian reliabilitas anotasi independen (*independent dual-annotator agreement*) pada 400 sampel kalimat (100 sampel per dataset sintetis terstratifikasi: Nemotron, Luna, Gemma, GPT-OSS) yang dievaluasi secara mandiri (*blind* dan independen) oleh dua penilai pada tanggal **22 Oktober 2026** (*seed* = `20261022`).

---

## 1. Konfigurasi Evaluator & Metodologi Audit

- **Evaluator A1**: Arif Athaya Harahap
- **Evaluator A2**: Muhammad Faiz Fauzan
- **Tanggal Pelaksanaan**: 22 Oktober 2026 (*seed* = `20261022`)
- **Jumlah Kalimat Sampel**: 400 kalimat (10.812 token, 800 evaluasi independen)
- **Cakupan Dataset Sintetis**:
  - `nemotron`: 100 kalimat (Sintetis Nemotron-3 Super 120B / Ultra 550B)
  - `luna`: 100 kalimat (Sintetis GPT-5.6 Luna / Gemini 3.6 Flash Medium)
  - `gemma`: 100 kalimat (Sintetis Gemma 4 31B / Nemotron-3 Super 120B)
  - `gpt_oss`: 100 kalimat (Sintetis GPT-OSS 120B / Nemotron-3 Nano 30B)
- **Aturan Konsensus Dual-Agreement**:
  - Rentang anotasi asli hanya dibatalkan (*False Positive* / *Wrong*) apabila **kedua penilai secara independen sepakat menolaknya** (keduanya menandai *REMOVE* atau mengajukan perbaikan).
  - Entitas baru atau perbaikan tipe (*replacement*) hanya ditambahkan ke dalam konsensus apabila **kedua penilai secara independen mengajukan batas rentang (*boundary*) dan label kelas yang identik**.
  - Jika terjadi perbedaan evaluasi antarkedua penilai, anotasi asli dipertahankan (*benefit of the doubt*).

---

## 2. Hasil Koefisien Reliabilitas Inter-Annotator Agreement (IAA)

Pengujian statistik kesepakatan antarpenilai dihitung menggunakan metrik Cohen's Kappa (κ) pada tingkat token BIO dan tingkat kelas entitas, serta Pairwise Exact Span-F₁ (dilengkapi 95% *bootstrap confidence interval*, 1.000 iterasi):

| Metrik Kesepakatan Antarpenilai | Nilai Empiris | 95% Bootstrap CI | Interpretasi Ilmiah (Landis & Koch, 1977) |
| :--- | :---: | :---: | :--- |
| **Token Cohen's κ (37 tag BIO)** | **0,987** | [0,983 – 0,991] | Kesepakatan Hampir Sempurna (*Almost Perfect Agreement*) |
| **Token Cohen's κ (18 kelas entitas + O)** | **0,989** | [0,985 – 0,993] | Kesepakatan Hampir Sempurna (*Almost Perfect Agreement*) |
| **Entity-Decision κ (KEEP / REMOVE / REPLACE)** | **0,923** | [0,895 – 0,947] | Kesepakatan Hampir Sempurna (*Almost Perfect Agreement*) |
| **Entity-Decision κ (CORRECT / INCORRECT)** | **0,928** | [0,899 – 0,952] | Kesepakatan Hampir Sempurna (*Almost Perfect Agreement*) |
| **Pairwise Exact Span-F₁ Agreement** | **97,63%** | [96,84% – 98,34%] | Konsistensi Batas Rentang Sangat Tinggi (1.975 sepakat) |
| **Persentase Kesepakatan Token (BIO)** | **99,13%** | — | 10.718 dari 10.812 token berlabel BIO identik |
| **Kalimat Identik Sempurna (*Zero Disagreement*)** | **89,75%** | — | 359 dari 400 kalimat disepakati 100% tanpa selisih |

---

## 3. Rincian IAA Berdasarkan Dataset Sintetis

| Dataset Sintetis | Populasi Asal | Sampel | Token | κ Token BIO | κ Token Kelas | κ Keputusan Entitas | Span-F₁ IAA | Persentase Kalimat Identik |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| Nemotron | 17.439 | 100 | 3.245 | 0,977 | 0,981 | 0,886 | 95,93% | 82,00% |
| Luna | 17.236 | 100 | 2.537 | 0,992 | 0,992 | 0,911 | 98,46% | 92,00% |
| Gemma | 15.666 | 100 | 2.029 | 0,988 | 0,989 | 0,927 | 97,60% | 92,00% |
| GPT-OSS | 13.384 | 100 | 3.001 | 0,994 | 0,995 | 0,965 | 98,72% | 93,00% |
| **Total / Agregat** | **63.725** | **400** | **10.812** | **0,987** | **0,989** | **0,923** | **97,63%** | **89,75%** |

---

## 4. Evaluasi Kualitas Anotasi Dataset terhadap Konsensus Dual-Agreement

Berdasarkan konsensus *dual-agreement*, dihitung metrik presisi, recall, dan $F_1$-score kualitas anotasi bawaan masing-masing dataset sintetis:

| Dataset Sintetis | Kalimat | Benar (TP) | Salah (FP) | Terlewat (Missed) | FN Total | Presisi Anotasi | Recall Anotasi | F1 Anotasi | Kalimat Bermasalah | Estimasi Galat Terbobot (p̂_error) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| Nemotron | 100 | 517 | 118 | 21 | 83 | 81,42% | 86,17% | **83,72%** | 73 | 72,93% |
| Luna | 100 | 493 | 27 | 12 | 25 | 94,81% | 95,17% | **94,99%** | 28 | 28,05% |
| Gemma | 100 | 297 | 78 | 14 | 57 | 79,20% | 83,90% | **81,48%** | 62 | 61,43% |
| GPT-OSS | 100 | 451 | 97 | 36 | 93 | 82,30% | 82,90% | **82,60%** | 75 | 74,78% |
| **Total Gabungan** | **400** | **1.758** | **320** | **83** | **258** | **84,60%** | **87,20%** | **85,88%** | **238** | — |

---

## 5. Analisis Temuan Kualitas Anotasi

1. **Korpus Luna (`gpt_5_6_luna`) Meraih Kualitas Tertinggi Secara Mutlak**:
   Dataset sintetis Luna mencapai F₁ = 94,99% dengan presisi 94,81% dan recall 95,17%. Tingkat kesalahan kalimatnya sangat rendah, yaitu hanya 28 kalimat bermasalah dari 100 sampel (estimasi galat terbobot p̂_error = 28,05%). Hal ini membuktikan keunggulan sinergi antara generator GPT-5.6 dan verifikator Gemini Flash dalam menyaring kata benda umum dan menjaga batas rentang entitas.
2. **Karakteristik Kesalahan per Dataset**:
   - **Nemotron** ($F_1 = 83,72\%$): Menghasilkan recall yang solid (86,17%), namun presisi sedikit tertekan (81,42%) akibat 118 *false positives*, terutama pada kelas `PRD` (20 salah), `LAW` (12 salah), `TIM` (12 salah), serta 4 kesalahan pelabelan kelompok politik/ormas pada kelas `NOR`.
   - **GPT-OSS** ($F_1 = 82,60\%$): Menunjukkan performa berimbang antara presisi (82,30%) dan recall (82,90%), dengan 97 kesalahan anotasi yang mayoritas terkonsentrasi pada `PRD` (27 salah) dan `ORG` (10 salah).
   - **Gemma** ($F_1 = 81,48\%$): Menunjukkan presisi 79,20% dan recall 83,90%, dengan kesalahan dominan pada `ORG` (17 salah), `DAT` (10 salah), dan `TIM` (10 salah akibat preposisi waktu).
3. **Penyelarasan Taksonomi NOR Bebas False Positive**:
   Pada kelas `NOR`, korpus **Luna, Gemma, dan GPT-OSS** mencatatkan **0 kesalahan positif palsu (`FP = 0`, Presisi 100,00%)**, membuktikan keberhasilan instruksi prompt tanpa `REG` dalam mendefinisikan kelompok etnis, kebangsaan, dan penganut agama.
4. **Validitas Metodologis Ilmiah**:
   Nilai reliabilitas antarpenilai Cohen's κ = 0,987 (BIO) dan κ = 0,989 (kelas) serta Pairwise Span-F₁ = 97,63% membuktikan bahwa audit kualitas data sintetis pada penelitian ini memiliki konsistensi ilmiah yang sangat tinggi dan dapat dipertanggungjawabkan secara akademis.
