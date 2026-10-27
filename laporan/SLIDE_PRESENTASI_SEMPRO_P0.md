# PANDUAN LENGKAP PRESENTASI SEMINAR PROPOSAL (P0) SKRIPSI
## FAKULTAS ILMU KOMPUTER UNIVERSITAS BRAWIJAYA

**Judul Skripsi**:
> **ANALISIS KINERJA FINE-TUNING INDOBERT PADA NAMED ENTITY RECOGNITION (NER) BAHASA INDONESIA MENGGUNAKAN ANOTASI MANUSIA DAN SINTETIS BERBASIS LLM**

**Identitas Peneliti**:
- **Nama Mahasiswa**: Arif Athaya Harahap
- **NIM**: 235150200111056
- **Program Studi**: S1 Teknik Informatika
- **Departemen**: Teknik Informatika, Fakultas Ilmu Komputer, Universitas Brawijaya
- **Dosen Pembimbing I**: Prof. Dr. Ir. Lailil Muflikhah, S.Kom., M.Sc., IPM., ASEAN Eng.
- **Dosen Pembimbing II**: Tirana Noor Fatyanosa, S.Kom., M.Kom., Ph.D.
- **Tipe Penelitian**: Non-implementatif – Analitik (Eksperimental)
- **Alokasi Waktu**: 15 Menit Presentasi + Sesi Tanya Jawab (Q&A)

---

## DAFTAR ISI SLIDE & ALOKASI WAKTU

| No | Judul Slide | Bagian | Estimasi Waktu | Rentang Menit |
|:--:|---|:---:|:---:|:---:|
| 01 | Judul Penelitian & Identitas Tim Pembimbing | Cover | 1 Menit | 00:00 – 01:00 |
| 02 | Latar Belakang Masalah (3 Pilar Berbasis Riset) | Bab 1 | 1 Menit 15 Detik | 01:00 – 02:15 |
| 03 | Rumusan Masalah & Tujuan Penelitian (1-to-1 Mapping) | Bab 1 | 1 Menit | 02:15 – 03:15 |
| 04 | Batasan Masalah (5 Poin Presisi) | Bab 1 | 1 Menit | 03:15 – 04:15 |
| 05 | Matriks Penelitian Terdahulu & Research Gap | Bab 2 | 1 Menit 15 Detik | 04:15 – 05:30 |
| 06 | Landasan Teori (3 Pilar Konsep Kunci) | Bab 2 | 1 Menit | 05:30 – 06:30 |
| 07 | Subjek & Karakteristik Dataset (Split 85:15) | Bab 3 | 1 Menit 15 Detik | 06:30 – 07:45 |
| 08 | Arsitektur Pipeline Distilasi Data 2-Fase Nemotron | Bab 3 | 1 Menit 15 Detik | 07:45 – 09:00 |
| 09 | Variabel Penelitian (Independen, Dependen, Kontrol) | Bab 3 | 1 Menit | 09:00 – 10:00 |
| 10 | Skenario Eksperimen Komparatif (Skenario 1 vs 2) | Bab 3 | 1 Menit | 10:00 – 11:00 |
| 11 | Desain Model IndoBERT & Penanganan Subword | Bab 3 | 1 Menit | 11:00 – 12:00 |
| 12 | Metode Evaluasi & Standar CoNLL Exact Chunk Match | Bab 3 | 1 Menit | 12:00 – 13:00 |
| 13 | Jadwal Pelaksanaan & Milestone Skripsi FILKOM UB | Bab 3 | 1 Menit | 13:00 – 14:00 |
| 14 | Penutup / Sesi Tanya Jawab (Q&A) | Penutup | 1 Menit | 14:00 – 15:00 |
| L1 | *Lampiran 1: Katalog 30 Domain Topik Bahasa Indonesia* | Backup | - | Sesi Q&A |
| L2 | *Lampiran 2: Template Prompt Generasi & Verifikasi LLM* | Backup | - | Sesi Q&A |
| L3 | *Lampiran 3: Taksonomi 18 Kelas Entitas & Normalisasi TTL* | Backup | - | Sesi Q&A |
| L4 | *Lampiran 4: Spesifikasi Lingkungan Komputasi Cloud (GPU T4)* | Backup | - | Sesi Q&A |

---

## NASKAH UJARAN PER SLIDE (SPEAKER NOTES) & KONTEN VISUAL

### SLIDE 1: JUDUL PENELITIAN & IDENTITAS
- **Navigasi / Kategori**: `PROPOSAL SKRIPSI / PENDEWASAAN 0 (P0)`
- **Judul**: ANALISIS KINERJA FINE-TUNING INDOBERT PADA NAMED ENTITY RECOGNITION (NER) BAHASA INDONESIA MENGGUNAKAN ANOTASI MANUSIA DAN SINTETIS BERBASIS LLM
- **Visual**: Logo Universitas Brawijaya & FILKOM, layout kartu simetris dengan aksen warna UB Tech Blue (`#004AAD`), informasi identitas peneliti dan tim dosen pembimbing secara terstruktur.
- **Teks Tampil**:
  - Peneliti: Arif Athaya Harahap (NIM: 235150200111056)
  - Dosen Pembimbing I: Prof. Dr. Ir. Lailil Muflikhah, S.Kom., M.Sc., IPM., ASEAN Eng.
  - Dosen Pembimbing II: Tirana Noor Fatyanosa, S.Kom., M.Kom., Ph.D.
  - Program Studi Teknik Informatika, Fakultas Ilmu Komputer, Universitas Brawijaya (2026)

> **Naskah Ujaran (Speaker Notes) [00:00 – 01:00]**:
> *"Selamat pagi/siang, yang terhormat Bapak dan Ibu Dewan Penguji, serta yang saya hormati Dosen Pembimbing I saya, Prof. Dr. Ir. Lailil Muflikhah, S.Kom., M.Sc., IPM., ASEAN Eng., dan Dosen Pembimbing II saya, Ibu Tirana Noor Fatyanosa, S.Kom., M.Kom., Ph.D.*
> 
> *Perkenalkan, saya Arif Athaya Harahap, mahasiswa Program Studi Teknik Informatika Fakultas Ilmu Komputer Universitas Brawijaya. Pada kesempatan hari ini, perkenankan saya mempresentasikan proposal skripsi saya yang berjudul: **'Analisis Kinerja Fine-Tuning IndoBERT pada Named Entity Recognition (NER) Bahasa Indonesia Menggunakan Anotasi Manusia dan Sintetis Berbasis LLM'**.*
> 
> *Penelitian ini berfokus pada pengujian empiris analitik mengenai efektivitas dataset sintetis hasil generasi berjenjang dua-fase Large Language Model sebagai alternatif solusi atas kelangkaan data beranotasi pada pemodelan deep learning bahasa Indonesia. Mari kita mulai dari latar belakang yang mendasari penelitian ini."*

---

### SLIDE 2: LATAR BELAKANG MASALAH
- **Navigasi**: `Bab 1 Pendahuluan > Latar Belakang`
- **Visual**: 3 Kolom Kartu Rounded berdampingan dengan ikon penanda, menyajikan alur logika bertingkat dari urgensi teknologi, tantangan empiris, hingga research gap.
- **Konten Teks Visual (Format 1 Paragraf per Kartu dengan Poin Kunci Di-Bold)**:
  - **Kartu 1: 01. URGENSI NER & DATA - Kebutuhan Ekstraksi Informasi**
    Dalam hierarki NLP, **Named Entity Recognition (NER)** menempati peran sentral sebagai **pilar utama ekstraksi informasi terstruktur** dari teks (Li et al., 2020). Untuk mencapai performa identifikasi yang presisi, implementasi model deep learning seperti **indobenchmark/indobert-large-p1** (Wilie et al., 2020) sangat bergantung pada ketersediaan **korpus beranotasi masif dan berkualitas tinggi** guna menguasai representasi semantik token secara optimal.
  - **Kartu 2: 02. TANTANGAN RESOURCE-LOW - Keterbatasan & Noise Sintetis**
    Namun, bahasa Indonesia tergolong sebagai **resource-low language** yang menghadapi **kelangkaan korpus berlabel** (Lovenia et al., 2024), di mana proses **human annotation** membutuhkan biaya finansial dan waktu yang sangat tinggi. Di sisi lain, sintesis korpus melalui **single-prompt LLM konvensional** rentan memicu **noise pergeseran batas kata (boundary shift)** serta kesalahan tipe entitas yang merusak akurasi model (Kamath et al., 2025).
  - **Kartu 3: 03. DISTILASI 2-FASE & GAP - Solusi Pemisahan Peran**
    Sebagai solusinya, **paradigma 2-phase generation** memisahkan peran generator (**Nemotron-3 Super 120B**) dan verifikator independen (**Nemotron-3 Ultra 550B**) untuk menekan halusinasi serta **memperbaiki batas entitas** (Zhang et al., 2024). Hal ini membuka **research gap empiris** untuk menguji efektivitas fine-tuning IndoBERT dengan rasio seimbang **1:1 pada unseen human test set**.

> **Naskah Ujaran (Speaker Notes) [01:00 – 02:15]**:
> *"Bapak dan Ibu Dewan Penguji, latar belakang penelitian ini berpijak pada tiga pilar utama.*
> 
> *Pertama, dalam ranah Pemrosesan Bahasa Alami (NLP), Named Entity Recognition (NER) menempati peran sentral sebagai fondasi ekstraksi informasi otomatis. Model representasi bahasa seperti IndoBERT varian large terbukti unggul, namun memerlukan data latih beranotasi dalam skala masif.*
> 
> *Kedua, realitas di lapangan menunjukkan bahwa bahasa Indonesia merupakan salah satu bahasa yang tergolong minim sumber daya (resource-low) dalam ketersediaan korpus berlabel standar industri. Pembuatan dataset manual oleh anotator manusia memakan biaya ribuan dolar dan waktu berbulan-bulan. Di sisi lain, studi dari Kamath et al. (2025) menunjukkan bahwa pembuatan data sintetis secara instan menggunakan single-prompt LLM masih kalah bersaing dengan data manusia akibat tingginya noise batas kata dan kesalahan klasifikasi label.*
> 
> *Ketiga, perkembangan kecerdasan artifisial terbaru memperkenalkan paradigma distilasi data dua fase (2-phase generation), seperti yang dirilis NVIDIA pada keluarga model Nemotron-3. Dengan memisahkan peran generator (Nemotron-3 Super) dan verifikator kualitas (Nemotron-3 Ultra), noise anotasi dapat ditekan secara dramatis. Berangkat dari sinilah muncul research gap: apakah fine-tuning IndoBERT-large-p1 yang dilatih sepenuhnya dengan data sintetis dua fase ini mampu menyaingi daya generalisasi model yang dilatih dengan data organik manusia? Penelitian ini hadir untuk menjawab persoalan empiris tersebut."*

---

### SLIDE 3: RUMUSAN MASALAH & TUJUAN PENELITIAN
- **Navigasi**: `Bab 1 Pendahuluan > Rumusan Masalah & Tujuan`
- **Visual**: Matriks 2 Baris × 2 Kolom dengan tanda panah timbal-balik (↔), mempertegas korespondensi 1-ke-1 antara Rumusan Masalah dan Tujuan.
- **Konten Visual**:
  - **Rumusan Masalah 1**: Bagaimana merancang dan mengimplementasikan proses *fine-tuning* model `indobenchmark/indobert-large-p1` untuk tugas NER bahasa Indonesia menggunakan *general dataset* beranotasi manusia dan anotasi sintetis hasil generasi dua fase?
    ↔ **Tujuan 1**: Merancang dan melaksanakan skenario *fine-tuning* pada model `indobenchmark/indobert-large-p1` untuk tugas NER bahasa Indonesia dengan variasi *general dataset* beranotasi manusia dan anotasi sintetis hasil generasi dua fase.
  - **Rumusan Masalah 2**: Bagaimana perbandingan kinerja metrik (presisi, *recall*, dan *F1-score*) model IndoBERT-large-p1 ketika dilatih menggunakan dataset anotasi manusia dan dataset anotasi sintetis?
    ↔ **Tujuan 2**: Mengevaluasi dan membandingkan kinerja metrik (presisi, *recall*, dan *F1-score*) dari model IndoBERT-large-p1 yang dihasilkan dari tiap skenario pelatihan untuk mengetahui efektivitas strategi anotasi sintetis berbasis LLM.

> **Naskah Ujaran (Speaker Notes) [02:15 – 03:15]**:
> *"Berdasarkan identifikasi masalah tersebut, penelitian ini merumuskan dua pertanyaan penelitian utama yang berkorespondensi langsung dengan tujuannya.*
> 
> *Rumusan masalah pertama difokuskan pada aspek perancangan: bagaimana kita merancang dan mengimplementasikan arsitektur pipeline fine-tuning IndoBERT-large-p1 di atas dua sumber data yang berbeda—yaitu korpus anotasi manusia dan korpus sintetis hasil generasi dua fase.*
> 
> *Rumusan masalah kedua berfokus pada evaluasi empiris: bagaimana perbandingan metrik kinerja komputasional yang mencakup presisi, recall, dan F1-score saat kedua model tersebut diuji pada himpunan data uji independen yang sama.*
> 
> *Tujuan akhir dari penelitian ini adalah memberikan bukti ilmiah apakah data sintetis hasil distilasi LLM dua-fase layak menjadi pengganti fungsional dari dataset manual manusia."*

---

### SLIDE 4: BATASAN MASALAH
- **Navigasi**: `Bab 1 Pendahuluan > Batasan Masalah`
- **Visual**: 5 Kartu Bernomor Vertikal/Horizontal dengan badge aksen biru, memperjelas ruang lingkup agar tidak melebar.
- **Konten Visual**:
  1. **Tipe Penelitian**: Bersifat Non-implementatif – Analitik (fokus pada investigasi eksperimen komparatif, bukan pembuatan aplikasi sistem untuk pengguna akhir).
  2. **Model Fondasi**: Dibatasi secara khusus pada varian arsitektur `indobenchmark/indobert-large-p1` (24 layers, 1024 hidden size, 340M parameter).
  3. **Domain Teks & Skema Anotasi**: Dataset teks berbahasa Indonesia domain umum (*general dataset*) dengan taksonomi 19 kelas entitas baku (39 label BIO).
  4. **Pipeline Sintetis 2-Fase**: Murni menggunakan orkestrasi generasi `nvidia/nemotron-3-super-120b` (T=0.75) dan verifikasi `nvidia/nemotron-3-ultra-550b` (T=0.20) dengan volume seimbang 1:1 (~17.431 kalimat).
  5. **Evaluasi & Pengujian**: Diuji secara ketat pada himpunan data uji *unseen human-annotated data* dari korpus Nergrit menggunakan standar tolok ukur CoNLL chunk-level (`seqeval`).

> **Naskah Ujaran (Speaker Notes) [03:15 – 04:15]**:
> *"Untuk menjaga ketepatan fokus dan kedalaman analisis, penelitian ini menetapkan lima batasan masalah.*
> 
> *Pertama, sesuai dengan Panduan Skripsi FILKOM UB, tipe penelitian ini adalah non-implementatif analitik eksperimental. Luaran utamanya adalah hasil analisis ilmiah dan pembuktian empiris, bukan produk perangkat lunak antarmuka pengguna.*
> 
> *Kedua, model fondasi yang dievaluasi difokuskan pada IndoBERT-large-p1 karena kapasitas representasinya yang mendalam.*
> 
> *Ketiga, ruang lingkup domain adalah general dataset bahasa Indonesia dengan skema resmi 18 kelas OntoNotes entitas atau 39 tag BIO.*
> 
> *Keempat, pembuatan korpus sintetis dijalankan secara deterministik menggunakan pipeline 2-fase Nemotron-3 dengan volume seimbang 1:1 terhadap korpus acuan.*
> 
> *Dan kelima, evaluasi performa diuji secara ketat pada unseen test set Nergrit manusia menggunakan metrik exact chunk-level match CoNLL untuk memastikan perbandingan yang sepenuhnya adil."*

---

### SLIDE 5: MATRIKS PENELITIAN TERDAHULU & RESEARCH GAP
- **Navigasi**: `Bab 2 Landasan Pustaka > Penelitian Terdahulu`
- **Visual**: Tabel Matriks Komparatif Pustaka dengan kolom Peneliti, Fokus, Metode, Temuan Utama, dan Research Gap / Posisi Penelitian Ini yang disorot dengan latar belakang kartu khusus (*highlight*).
- **Konten Visual**:
  - **Wilie et al. (2020)**: Benchmark IndoNLU & rilis model IndoBERT → Menembus SOTA NER bahasa Indonesia; *Celah: evaluasi hanya pada dataset berlabel manusia murni*.
  - **Lovenia et al. (2024)**: Proyek Regional SEACrowd → Mendokumentasikan minimnya data NLP Asia Tenggara; *Celah: fokus pada agregasi data yang ada, bukan sintesis data baru*.
  - **Kamath et al. (2025)**: Synthetic Data for Low-Resource NER → LLM *single-prompt* bermanfaat namun performanya kalah dari data manusia akibat *boundary noise*; *Celah: menegaskan perlunya mekanisme kurasi bertingkat*.
  - **NVIDIA (2026a, 2026b)**: Nemotron-3 Super & Ultra → Arsitektur hibrida Mamba-Attention MoE terbukti unggul untuk distilasi data; *Celah: laporan industri global, belum diuji untuk downstream NER bahasa Indonesia*.
  - **Posisi Penelitian Ini (Novelty)**: Mengintegrasikan keandalan IndoBERT-large-p1 dengan korpus sintetis hasil orkestrasi 2-Fase Nemotron berbanding data manusia Nergrit (1:1), membuktikan apakah agen verifikator LLM mampu mengatasi kelemahan yang ditemukan Kamath et al. (2025).

> **Naskah Ujaran (Speaker Notes) [04:15 – 05:30]**:
> *"Memasuki Bab 2, landasan penelitian ini dibangun di atas sintesis sejumlah studi kredibel terdahulu.*
> 
> *Wilie et al. (2020) telah meletakkan tonggak penting dengan merilis IndoBERT, namun pembuktiannya masih bertumpu pada dataset buatan manusia. Di tingkat regional, studi SEACrowd oleh Lovenia et al. (2024) mempertegas urgensi pengadaan data bahasa Indonesia yang representasinya masih sangat tertinggal.*
> 
> *Titik krusial yang mendasari kebaruan penelitian ini berasal dari temuan empiris Kamath et al. (2025). Mereka menguji sintesis data LLM pada bahasa resource-low dan menyimpulkan bahwa data sintetis tanpa kurasi bertingkat rentan kalah bersaing dengan data manusia karena tingginya tingkat pergeseran batas kata.*
> 
> *Untuk menjawab kelemahan tersebut, penelitian ini mengadopsi rilis teknis mutakhir NVIDIA (2026) mengenai arsitektur Nemotron-3. Posisi penelitian ini adalah menjadi pelopor studi empiris yang menguji efektivitas mekanisme distilasi dua-fase terhadap performa fine-tuning IndoBERT pada korpus general bahasa Indonesia."*

---

### SLIDE 6: LANDASAN TEORI
- **Navigasi**: `Bab 2 Landasan Pustaka > Landasan Teori`
- **Visual**: 3 Kartu Bernomor Konsep `01`, `02`, `03` dengan tipografi tebal, menyajikan konsep fundamental yang mendukung metodologi penelitian.
- **Konten Visual**:
  - **01. Named Entity Recognition & Format BIO (Li et al., 2020)**
    - Klasifikasi tingkat token (*token classification*) untuk mengekstrak entitas rigid ke dalam kategori semantik.
    - Format standar IOB2: `B-` (Beginning/Awal entitas), `I-` (Inside/Lanjutan entitas), dan `O` (Outside/Bukan entitas).
  - **02. IndoBERT Architecture & Transfer Learning (Wilie et al., 2020; Devlin et al., 2019)**
    - Arsitektur berbasis Bidirectional Transformer Encoder dengan 24 layer dan representasi konteks kiri-kanan secara simultan.
    - Adaptasi pada downstream task melalui penambahan *Token Classification Head* dengan penyesuaian bobot (*fine-tuning*).
  - **03. Paradigma Distilasi Data Dua Fase (Kamoi et al., 2024; Zhang et al., 2024)**
    - *Separation of concerns*: LLM mandiri rentan bias konfirmasi (Kamoi et al., 2024), sehingga memerlukan *strong verifier* terpisah (Zhang et al., 2024).
    - Generator ($T=0.75$) mengeksplorasi variasi bahasa; Verifikator ($T=0.20$) melakukan audit batas kata, pruning false positive, dan pemulihan entitas terlewat.

> **Naskah Ujaran (Speaker Notes) [05:30 – 06:30]**:
> *"Tiga teori fundamental yang menjadi pilar dalam penelitian ini adalah:*
> 
> *Pertama, formulasi tugas NER sebagai sequence labeling dengan skema IOB2. Ketepatan pemetaan tag BIO ini menentukan keberhasilan model dalam membedakan entitas majemuk dari teks biasa.*
> 
> *Kedua, arsitektur IndoBERT-large-p1 yang mengadopsi transfer learning. Melalui mekanisme self-attention pada 24 lapisannya, model mampu menangkap relasi semantik kata bahasa Indonesia yang sangat kompleks.*
> 
> *Ketiga, prinsip distilasi dua fase berbasis LLM. Teori dari Kamoi et al. dan Zhang et al. membuktikan bahwa satu model bahasa tidak dapat mengoreksi kesalahannya sendiri secara objektif. Diperlukan dua peran terpisah: satu agen bertindak sebagai pembuat ide (generator) dan satu agen yang lebih kuat bertindak sebagai pengawas mutu independen (verifier). Inilah landasan teoritis mengapa pendekatan dua fase dipilih."*

---

### SLIDE 7: SUBJEK DAN KARAKTERISTIK DATASET
- **Navigasi**: `Bab 3 Metodologi > Karakteristik Dataset`
- **Visual**: Tabel Perbandingan Statistik Dataset dan diagram proporsi pembagian data 85:15.
- **Konten Visual**:
  - **Dataset Human Benchmark (`nergrit-indo-ner-normalized`)**:
    - Porsi Latih (70%): **~12.202 kalimat**
    - Porsi Validasi (15%): **2.615 kalimat** (Tuning hyperparameter & early stopping)
    - Porsi Evaluasi / Held-out (15%): **2.615 kalimat** (Masuk himpunan uji evaluasi, Seed = 42)
  - **Dataset Synthetic LLM (`distilled-indonesian-ner-v2`)**:
    - Porsi Latih (70%): **~12.222 kalimat** (Seimbang 1:1 dengan Nergrit)
    - Porsi Validasi (15%): **2.619 kalimat**
    - Porsi Evaluasi (15%): **2.615 kalimat** (Uji in-domain sintetis)
    - **Gold Benchmark Utama**: **1.000 kalimat** (`ner_benchmark_1000` terkurasi QC manusia)
  - **Jaminan Integritas Riset**: Pembagian 85:15 menjamin data uji murni *unseen* (*zero data leakage*). Kedua model dievaluasi pada suite pengujian identik.

> **Naskah Ujaran (Speaker Notes) [06:30 – 07:45]**:
> *"Bapak dan Ibu Dewan Penguji, beralih ke Bab 3 Metodologi Penelitian, slide ini menyajikan subjek dan pembagian dataset yang digunakan.*
> 
> *Untuk korpus manusia Nergrit dan data sintetis Nemotron, kami menerapkan skema pembagian baku 70% data latih, 15% data validasi, dan 15% data evaluasi held-out. Data latih 70% (~12.200 kalimat) digunakan khusus untuk pembaruan bobot representasi IndoBERT. Data validasi 15% (2.615 kalimat) digunakan murni untuk memonitor kurva loss dan early stopping guna mencegah overfitting.*
> 
> *Sisa 15% data (2.615 kalimat) merupakan data evaluasi murni yang tidak pernah disentuh selama pelatihan maupun validasi. Porsi 15% inilah yang kami gabungkan ke dalam himpunan dataset evaluasi bersama Gold Benchmark 1.000 kalimat dan 5 korpus eksternal SEAcrowd untuk menjamin evaluasi yang komprehensif dan objektif (zero data leakage)."*

---

### SLIDE 8: ARSITEKTUR PIPELINE DISTILASI DUA FASE
- **Navigasi**: `Bab 3 Metodologi > Pipeline Distilasi 2-Fase`
- **Visual**: Diagram Alur Mermaid resolusi tinggi yang menampilkan tahapan orkestrasi pembuatan data sintetis dari katalog topik hingga publikasi ke Hugging Face Hub.
- **Poin Kunci Visual**:
  1. *Fase 1 (Generator)*: `nemotron-3-super-120b`, $T=0.75$, 10 kalimat per request untuk memastikan keberagaman kosakata.
  2. *Fase 2 (Verifier/QC)*: `nemotron-3-ultra-550b`, $T=0.20$, 5 kalimat per batch untuk penalaran kritis dan penghapusan halusinasi.
  3. *Peran Kategori TTL*: Dirancang khusus sebagai *negative constraint* untuk mencegah gelar/jabatan (misal "Presiden", "Menteri") tercampur ke dalam nama orang (`PER`). Pada tahap akhir dikembalikan ke label `O` agar selaras 100% dengan taksonomi 19 kelas Nergrit.

> **Naskah Ujaran (Speaker Notes) [07:45 – 09:00]**:
> *"Slide 8 mengilustrasikan arsitektur pipeline distilasi data dua fase yang kami kembangkan.*
> 
> *Alur dimulai dari katalog 30 topik nasional Indonesia. Setiap pemanggilan API secara acak mengambil 3 topik berbeda untuk merangsang keragaman kalimat. Pada Fase 1, model Nemotron-3 Super 120B dengan temperatur 0,75 bertugas membuat teks dan anotasi awal.*
> 
> *Keluaran mentah tersebut kemudian dialirkan ke Fase 2, di mana model Nemotron-3 Ultra 550B bertindak sebagai Quality Control dengan temperatur deterministik 0,20. Model ini memvalidasi batas entitas, menghapus false positive, dan mengoreksi kelas entitas yang keliru.*
> 
> *Salah satu kontribusi teknis penting di sini adalah penerapan entitas TTL (Title/Gelar) sebagai filter negatif. Kami mewajibkan LLM memisahkan gelar seperti 'Presiden' atau 'Dokter' dari nama orang. Sebelum dilatihkan ke IndoBERT, label TTL dinormalisasi kembali ke label O. Hal ini menjamin bahwa entitas PER bersih dari pencemaran gelar, sekaligus menyelaraskan taksonomi menjadi persis 19 kelas seperti korpus acuan."*

---

### SLIDE 9: VARIABEL PENELITIAN
- **Navigasi**: `Bab 3 Metodologi > Variabel Penelitian`
- **Visual**: Layout 3 Kolom Rapi (Independen, Dependen, Kontrol) dengan ikon pembeda.
- **Konten Visual**:
  - **Variabel Independen (Perlakuan)**:
    - Sumber dan metode anotasi dataset pelatihan:
      1. Dataset Anotasi Manusia (Nergrit Normalized).
      2. Dataset Anotasi Sintetis 2-Fase (Nemotron-3 Super + Ultra).
  - **Variabel Dependen (Hasil Ukur)**:
    - Metrik Kinerja Ekstraksi Token: *Precision*, *Recall*, dan *F1-Score* (Evaluasi *Exact Chunk-Level CoNLL* via `seqeval`).
    - Karakteristik Konvergensi: Nilai *training loss*, *validation loss*, dan jumlah *epoch* sebelum *Early Stopping*.
  - **Variabel Kontrol (Kondisi Konstan)**:
    - Model Fondasi: `indobenchmark/indobert-large-p1` (340M parameter).
    - Hiperparameter: Learning Rate ($2 \times 10^{-5}$), Batch Size (32), Optimizer AdamW (weight decay 0.01), Max Sequence Length (256).
    - Strategi Pelatihan: *Early Stopping* (patience = 2 epochs), pemantau Macro F1.
    - Dataset Pengujian: *Held-out Test Set Nergrit* (2.615 kalimat) & *Gold Benchmark* (1.000 kalimat).

> **Naskah Ujaran (Speaker Notes) [09:00 – 10:00]**:
> *"Sebagai penelitian non-implementatif analitik eksperimental, rancangan variabel penelitian dikontrol secara ketat.*
> 
> *Variabel independen atau perlakuan utama adalah sumber dataset latih, yaitu data anotasi manusia versus data anotasi sintetis dua fase.*
> 
> *Variabel dependen yang diamati mencakup metrik evaluasi sekuensial baku: Presisi, Recall, dan F1-Score pada tingkat exact chunk, serta dinamika konvergensi loss selama pelatihan.*
> 
> *Seluruh faktor lainnya dikunci sebagai variabel kontrol: mulai dari arsitektur model IndoBERT-large-p1, learning rate 2e-5, optimizer AdamW, toleransi early stopping, hingga dataset pengujian akhir. Dengan menjaga seluruh variabel kontrol ini konstan, perbedaan kinerja yang muncul nantinya dapat diatributkan secara murni kepada kualitas dari masing-masing dataset latih."*

---

### SLIDE 10: SKENARIO EKSPERIMEN KOMPARATIF
- **Navigasi**: `Bab 3 Metodologi > Skenario Eksperimen`
- **Visual**: Diagram Kotak Alur Perbandingan Skenario 1 (Baseline) vs Skenario 2 (Sintetis) bermuara pada modul evaluasi yang sama.
- **Konten Visual**:
  - **Skenario 1: Pelatihan Baseline Anotasi Manusia**
    - Data Latih: 14.816 kalimat Nergrit | Data Validasi: 2.615 kalimat.
    - Fungsi: Menetapkan batas ambang empiris (*gold-standard benchmark*) performa IndoBERT ketika dilatih dengan data organik buatan manusia.
  - **Skenario 2: Pelatihan Distilasi Sintetis 2-Fase**
    - Data Latih: 14.841 kalimat Sintetis Nemotron | Data Validasi: 2.619 kalimat.
    - Fungsi: Inti pengujian hipotesis untuk mengevaluasi apakah data sintetis mesin mampu menyaingi atau mendekati kemampuan generalisasi data manusia.
  - **Fase Pengujian Komparatif Bersama**:
    - Kedua model dievaluasi secara independen pada:
      1. **Evaluasi 1**: Gold Benchmark Set (1.000 kalimat emas).
      2. **Evaluasi 2**: Held-Out Nergrit Set (2.615 kalimat data riil).

> **Naskah Ujaran (Speaker Notes) [10:00 – 11:00]**:
> *"Slide 10 memaparkan perancangan skenario eksperimen komparatif.*
> 
> *Pada Skenario 1, model IndoBERT dilatih murni menggunakan 14.816 kalimat data manusia dari Nergrit. Skenario ini bertindak sebagai baseline acuan untuk melihat potensi maksimal IndoBERT pada domain ini.*
> 
> *Pada Skenario 2, model dengan bobot awal yang sama dilatih murni menggunakan 14.841 kalimat sintetis hasil distilasi dua-fase Nemotron. Skenario ini merupakan inti pembuktian hipotesis.*
> 
> *Setelah proses pelatihan selesai dan model terbaik disimpan melalui mekanisme Early Stopping, kedua model diuji pada dua himpunan data uji independen: pertama pada Gold Benchmark 1.000 kalimat, dan kedua pada Held-Out Nergrit 2.615 kalimat. Hasil dari kedua skenario ini akan dikomparasikan secara berdampingan untuk menilai efektivitas data sintetis."*

---

### SLIDE 11: DESAIN MODEL INDOBERT & PENANGANAN SUBWORD
- **Navigasi**: `Bab 3 Metodologi > Desain Model IndoBERT`
- **Visual**: Diagram Arsitektur Token Classification Head dan ilustrasi perataan subword WordPiece dengan masking label $-100$.
- **Konten Visual**:
  - **Token Classification Head**:
    - Vektor representasi tersembunyi ($h_t \in \mathbb{R}^{1024}$) dialirkan ke *Dropout Layer* ($p=0.1$).
    - Transformasi linier melalui matriks bobot $W \in \mathbb{R}^{1024 \times 37}$ dan bias $b \in \mathbb{R}^{39}$.
    - Probabilitas kelas dihitung melalui fungsi aktivasi *Softmax*:
      $$
P(y_t = k \mid h_t) = \frac{\exp(W_k h_t + b_k)}{\sum_{j=1}^K \exp(W_j h_t + b_j)}
$$
  - **Penanganan Subword Tokenizer**:
    - Tokenizer WordPiece dapat memecah kata menjadi beberapa sub-kata (misal *"Mandalika"* → `["Manda", "##lika"]`).
    - Aturan Integritas: Hanya sub-kata pertama yang disematkan label asli (`B-FAC`). Sub-kata pecahan lanjutan serta token format (`[CLS]`, `[SEP]`, `[PAD]`) diberi label semu $-100$.
  - **Masked Cross-Entropy Loss**:
    - Gradien kerugian hanya dihitung pada token valid ($y_t \neq -100$), mencegah distorsi bobot oleh token padding dan pecahan subword.

> **Naskah Ujaran (Speaker Notes) [11:00 – 12:00]**:
> *"Beralih ke Slide 11, bagaimana model IndoBERT dikonfigurasi untuk tugas klasifikasi token ini?*
> 
> *Pada lapisan teratas dari 24 layer encoder IndoBERT-large-p1, kami memasang Token Classification Head berupa dropout 0,1 dan linear projection layer yang memetakan vektor dimensi 1024 ke dalam 39 kelas label BIO.*
> 
> *Salah satu tantangan teknis dalam model berbasis BERT adalah algoritma tokenisasi subword WordPiece, di mana sebuah kata dapat terfragmentasi menjadi beberapa pecahan token. Jika seluruh pecahan diberi label, gradien kerugian akan terdistorsi.*
> 
> *Penelitian ini mengimplementasikan strategi first-subword labeling: hanya potongan subword pertama yang membawa label entitas sebenarnya. Seluruh pecahan lanjutan beserta token khusus seperti CLS dan PAD dipetakan ke nilai minus 100. Dengan memanfaatkan Masked Cross-Entropy Loss, fungsi loss secara cerdas mengabaikan token semu tersebut dan hanya memperbarui bobot berdasarkan token linguistik yang valid."*

---

### SLIDE 12: METODE EVALUASI & STANDAR CONLL EXACT CHUNK MATCH
- **Navigasi**: `Bab 3 Metodologi > Evaluasi Kinerja`
- **Visual**: Kartu Formulasi Matematis Metrik (Precision, Recall, F1-Score) dan diagram perbandingan *Token-Level Match* vs *Chunk-Level Match*.
- **Konten Visual**:
  - **Kriteria Baku CoNLL Exact Chunk-Level Match (`seqeval`)**:
    - Prediksi hanya dihitung sebagai *True Positive* (TP) apabila rentang token awal (`B-`), token lanjutan (`I-`), dan kelas semantiknya identik 100% dengan *ground-truth*.
    - Prediksi yang terpotong sebagian atau melenceng batasnya langsung dihitung sebagai *False Positive* (FP) sekaligus memicu *False Negative* (FN).
  - **Formulasi Metrik**:
    $$
\text{Precision} = \frac{\text{TP}}{\text{TP} + \text{FP}}, \quad \text{Recall} = \frac{\text{TP}}{\text{TP} + \text{FN}}
$$
    $$
\text{F1-Score} = 2 \times \frac{\text{Precision} \times \text{Recall}}{\text{Precision} + \text{Recall}}
$$
  - **Cakupan Evaluasi & Komparasi Multi-Dataset**:
    1. **In-Domain Held-Out (15% Split)**: 2.615 kalimat Manusia & 2.615 kalimat Sintetis (Zero Data Leakage).
    2. **Gold Benchmark Terkurasi (1.000 Kalimat)**: Evaluasi kualitas emas 18 kelas lengkap dengan QC manusia.
    3. **Cross-Dataset Generalization (5 Korpus SEAcrowd)**: IndoQNER, IndoLEM, Prosa, Singgalang, & WikiANN (>104k kalimat) untuk menguji ketahanan model terhadap *domain shift*.
    4. **Dimensi Analisis**: Macro/Micro F1 exact match, per-class breakdown (18 kelas), dan analisis kesalahan batas kata (*boundary shift*).

> **Naskah Ujaran (Speaker Notes) [12:00 – 13:00]**:
> *"Slide 12 menjelaskan standar evaluasi kinerja yang kami terapkan. Untuk menilai performa secara objektif, akurasi token sederhana tidak dapat digunakan karena lebih dari 85% token adalah kelas Outside ('O').*
> 
> *Oleh karena itu, kami mengadopsi standar internasional CoNLL chunk-level evaluation melalui pustaka `seqeval`. Standar ini menerapkan kriteria exact match yang sangat ketat: suatu prediksi hanya bernilai True Positive jika awal kata, kelanjutan kata, dan label semantiknya tepat seratus persen. Jika prediksi terpotong sebagian, model langsung divonis salah ganda—yaitu menjadi False Positive sekaligus False Negative.*
> 
> *Seluruh model dievaluasi secara komprehensif pada tiga tingkatan data: pertama, data uji in-domain 15% held-out dari pemisahan 70:15:15; kedua, Gold Benchmark 1.000 kalimat 19 kelas terkurasi; dan ketiga, uji ketahanan domain shift pada lima korpus eksternal SEAcrowd dengan lebih dari 100 ribu kalimat untuk membuktikan daya generalisasi data sintetis di dunia nyata."*

---

### SLIDE 13: JADWAL PELAKSANAAN & MILESTONE SKRIPSI FILKOM UB
- **Navigasi**: `Bab 3 Metodologi > Jadwal & Milestone`
- **Visual**: Roadmap Horizontal Milestone FILKOM UB (P0 → P1 → P2 → Sidang Akhir) dengan persentase ketercapaian.
- **Konten Visual**:
  - **P0: Seminar Proposal Skripsi (Status: 0% / Berjalan Hari Ini)**
    - Penyusunan Bab 1, Bab 2, Bab 3, penyelarasan metodologi, dan pengesahan rencana eksperimen.
  - **P1: Milestone Kemajuan Minimal 50% (Bulan 1 - 2)**
    - Penyelesaian pipeline distilasi data 2-fase Nemotron (~17.431 kalimat CoNLL).
    - Pelaksanaan pelatihan Skenario 1 (Baseline Nergrit) pada Google Colab GPU T4.
  - **P2: Milestone Kemajuan Minimal 80% (Bulan 3)**
    - Pelaksanaan pelatihan Skenario 2 (Sintetis 2-Fase).
    - Ekstraksi evaluasi komparatif pada test set (confusion matrix & classification report).
    - Penyusunan naskah Bab 4 (Hasil) dan Bab 5 (Pembahasan).
  - **Sidang Akhir Skripsi: Milestone 100% (Bulan 4)**
    - Penyempurnaan Bab 6 (Penutup), naskah skripsi komplit, dan manuskrip artikel ilmiah.

> **Naskah Ujaran (Speaker Notes) [13:00 – 14:00]**:
> *"Slide 13 menyajikan peta jalan pelaksanaan penelitian yang mengacu pada Panduan Skripsi FILKOM UB v3.0.*
> 
> *Tahap P0 adalah seminar proposal yang kita laksanakan hari ini untuk menyepakati metodologi dan batasan masalah.*
> 
> *Menuju milestone P1 dengan target kemajuan 50%, fokus kegiatan adalah menuntaskan kompilasi dataset sintetis 17.431 kalimat dan merampungkan fine-tuning Skenario 1 sebagai baseline acuan.*
> 
> *Pada milestone P2 atau 80%, eksperimen pelatihan Skenario 2 akan diselesaikan, dilanjutkan dengan ekstraksi classification report komparatif dan penyusunan draf Bab 4 serta Bab 5.*
> 
> *Dan puncaknya pada milestone 100%, seluruh dokumentasi Bab 1 hingga Bab 6 beserta artikel publikasi ilmiah akan dirampungkan untuk maju ke Ujian Akhir Skripsi."*

---

### SLIDE 14: PENUTUP & SESI TANYA JAWAB (Q&A)
- **Navigasi**: `Penutup`
- **Visual**: Tipografi elegan "SEKIAN DAN TERIMA KASIH" dengan ringkasan pesan utama (*takeaway message*), informasi kontak, serta kartu transisi menuju sesi diskusi.
- **Konten Visual**:
  - **Pesan Kunci**:
    *"Penelitian ini siap membuktikan secara empiris apakah orkestrasi dua-fase Large Language Model mampu menjadi solusi terpercaya dalam mengatasi kelangkaan korpus beranotasi pada pemrosesan bahasa alami bahasa Indonesia."*
  - **Identitas**: Arif Athaya Harahap (NIM: 235150200111056)
  - Pembimbing I: Prof. Dr. Ir. Lailil Muflikhah | Pembimbing II: Tirana Noor Fatyanosa, Ph.D.
  - **Status**: Sesi Tanya Jawab dan Diskusi Dibuka.

> **Naskah Ujaran (Speaker Notes) [14:00 – 15:00]**:
> *"Bapak dan Ibu Dewan Penguji serta Dosen Pembimbing yang saya hormati, sebagai penutup, penelitian ini dirancang dengan metodologi yang ketat dan terkontrol untuk memberikan sumbangsih empiris bagi pengembangan NLP bahasa Indonesia. Kami siap melaksanakan seluruh tahapan eksperimen ini guna membuktikan kelayakan data sintetis dua-fase.*
> 
> *Demikian pemaparan proposal skripsi saya. Saya sangat mengharapkan saran, masukan, dan arahan dari Bapak dan Ibu Dewan Penguji demi penyempurnaan penelitian ini.*
> 
> *Waktu dan tempat saya kembalikan kepada Dosen Pembimbing / Ketua Penguji. Terima kasih."*

---

## SLIDE LAMPIRAN / CADANGAN TANYA JAWAB (BACKUP SLIDES)

### LAMPIRAN 1: KATALOG 30 DOMAIN TOPIK BAHASA INDONESIA
- **Tujuan Pertahanan**: Menjawab pertanyaan: *"Bagaimana Anda menjamin bahwa kalimat sintetis tidak bias dan mencerminkan bahasa alami sehari-hari?"*
- **Konten**: Daftar 30 topik nasional (Politik, Ekonomi Makro, Pasar Saham, Bisnis BUMN/Swasta, Olahraga, Teknologi Informasi & AI, Hukum/Peradilan MK/MA, Kriminalitas Polri, Layanan Kesehatan BPJS, Pendidikan Tinggi & LPDP, Seni Budaya Nusantara, Industri Hiburan/Film, Lingkungan Hidup, Bencana Alam BMKG, Infrastruktur Jalan Tol, Transportasi MRT/LRT/Whoosh, Pertahanan Militer TNI, dsb.).
- **Argumen Jawaban**: Pada setiap permintaan API, modul memilih 3 topik secara seragam acak (*uniform random sampling*). Ini memaksa model menggabungkan domain berbeda dalam 10 kalimat per request, mereplikasi variasi korpus general Nergrit.

### LAMPIRAN 2: TEMPLATE PROMPT GENERASI & VERIFIKASI
- **Tujuan Pertahanan**: Menjawab pertanyaan: *"Bagaimana bentuk instruksi prompt yang diberikan pada Fase 1 dan Fase 2?"*
- **Konten**:
  - Kutipan prompt Fase 1: Peran pakar NER, kewajiban 10 kalimat JSON, pemisahan mutlak nama orang (`PER`) dan jabatan (`TTL`).
  - Kutipan prompt Fase 2: Peran Quality Control, koreksi batas kata (*boundary refinement*), eliminasi kata benda umum (*false positive pruning*), pemulihan entitas terlewat (*omitted entity recovery*), dan validasi integritas panjang array.

### LAMPIRAN 3: TAKSONOMI 18 KELAS ENTITAS & NORMALISASI TTL
- **Tujuan Pertahanan**: Menjawab pertanyaan: *"Mengapa membuat kelas TTL jika pada akhirnya dibuang atau dinormalisasi ke label O?"*
- **Konten**:
  - Daftar 19 kelas entitas: PER, GPE, LOC, ORG, FAC, EVT, PRD, NOR, DAT, TIM, MON, QTY, CRD, ORD, PRC, LAW, LAN, WOA, REG.
  - Skema 39 BIO Label: `O` + 19 pasangan `B-` dan `I-`.
  - **Argumen Jawaban**: Kelas `TTL` (Title/Gelar) bertindak sebagai *negative constraint / buffer layer*. Jika tidak ada kelas `TTL`, LLM cenderung menggabungkan jabatan ke nama (misal *"Presiden Joko Widodo"* menjadi satu entitas `PER`). Dengan adanya `TTL`, LLM memisahkannya menjadi `TTL` (*"Presiden"*) dan `PER` (*"Joko Widodo"*). Pada tahap akhir, `TTL` dipetakan ke `O`, menghasilkan entitas `PER` yang murni dan taksonomi yang 100% kompatibel dengan dataset Nergrit.

### LAMPIRAN 4: SPESIFIKASI LINGKUNGAN KOMPUTASI CLOUD
- **Tujuan Pertahanan**: Menjawab pertanyaan: *"Apakah komputasi Anda mencukupi untuk melakukan fine-tuning IndoBERT varian Large?"*
- **Konten**:
  - Platform: Google Colaboratory Pro (Ubuntu 22.04 LTS).
  - GPU: NVIDIA T4 Tensor Core (16 GB GDDR6 VRAM).
  - CPU: Intel Xeon Processor (2 vCPU) dengan 12.7 GB High-Memory RAM.
  - Framework: PyTorch 2.x, Transformers 4.x, Datasets, Accelerate, evaluate, seqeval.
  - VRAM Optimization: Batch size 32 dan sequence length 256 terbukti stabil mengonsumsi ~11-12 GB VRAM pada IndoBERT-Large (340M params) tanpa memicu *Out-Of-Memory* (OOM).

---

## SKRIP ANTISIPASI PERTANYAAN KRITIS PENGUJI (DEFENSE SCRIPT)

### Pertanyaan 1: "Mengapa Anda menggunakan model IndoBERT varian Large (340M parameter) bukannya Base? Bukankah model Base lebih hemat komputasi?"
> **Rekomendasi Jawaban**:
> *"Terima kasih atas pertanyaannya, Bapak/Ibu Penguji. Alasan kami memilih varian `indobert-large-p1` didasarkan pada kapasitas representasi arsitekturnya. IndoBERT-Large memiliki 24 layer dan representasi vektor tersembunyi sebesar 1024, dibandingkan varian Base yang hanya 12 layer dan 768 dimensi.
> Penelitian kami mengevaluasi kualitas data sintetis. Model berkapasitas besar seperti IndoBERT-Large memiliki sensitivitas yang lebih tinggi dalam menangkap representasi linguistik halus dan hubungan semantik antar entitas. Jika kita menggunakan model yang terlalu kecil, ada risiko bahwa keterbatasan kinerja bukan disebabkan oleh kualitas data sintetisnya, melainkan karena keterbatasan kapasitas representasi model itu sendiri. Selain itu, alokasi VRAM 16 GB pada GPU NVIDIA T4 kami sudah mencukupi untuk batch size 16 pada model Large."*

### Pertanyaan 2: "Mengapa proporsi pembagian dataset menggunakan 85% latih dan 15% validasi/held-out, bukan 80:20 atau 90:10?"
> **Rekomendasi Jawaban**:
> *"Terima kasih Bapak/Ibu. Rasio 85:15 kami tetapkan untuk mengoptimalkan dua kebutuhan sekaligus. Dengan volume korpus acuan Nergrit sekitar 17.431 kalimat, rasio 85% menghasilkan korpus latih sebesar 14.816 kalimat yang sangat memadai bagi model berskala 340M parameter untuk mencapai konvergensi optimal.
> Di sisi lain, porsi 15% menyisakan 2.615 kalimat sebagai held-out test set. Angka 2.615 kalimat ini memiliki signifikansi statistik yang sangat kuat untuk menguji generalisasi model pada 19 kelas entitas yang berbeda, jauh lebih representatif dibandingkan jika pengujian hanya menggunakan 5% atau 10% data. Proporsi yang sama persis diterapkan pada data sintetis (14.841 train : 2.619 val) dengan random seed 42 untuk menjamin keterulangan (reproducibility) eksperimen."*

### Pertanyaan 3: "Mengapa harus menggunakan dua model Nemotron yang berbeda (Super 120B dan Ultra 550B)? Mengapa tidak satu model saja?"
> **Rekomendasi Jawaban**:
> *"Terima kasih Bapak/Ibu. Hal ini berlandaskan pada temuan empiris Kamoi et al. (2024) dan Zhang et al. (2024) mengenai fenomena bias konfirmasi diri (self-confirmation bias) pada LLM. Jika satu model diminta membuat teks sekaligus memvalidasi dirinya sendiri, model cenderung mempertahankan kesalahan awal karena berada pada jalur penalaran yang sama.
> Kami memisahkan dua peran: Nemotron-3 Super (120B) dioperasikan pada temperatur lebih tinggi (0,75) untuk memaksimalkan variasi kosakata dan sintaksis bahasa Indonesia. Sedangkan Nemotron-3 Ultra (550B) yang memiliki kapasitas penalaran lima kali lipat lebih besar dioperasikan pada temperatur rendah (0,20) sebagai verifikator kritis eksternal. Pemisahan tugas ini terbukti secara ilmiah mampu menekan halusinasi dan memperbaiki batas kata yang keliru."*

### Pertanyaan 4: "Apakah adil menguji model yang dilatih dengan data sintetis pada data uji manusia (Nergrit)?"
> **Rekomendasi Jawaban**:
> *"Sangat adil dan justru merupakan inti kontribusi penelitian ini, Bapak/Ibu. Tujuan utama pengadaan data sintetis dalam dunia nyata adalah untuk melatih sistem AI yang nantinya akan beroperasi dan berhadapan dengan data manusia di dunia nyata.
> Jika model sintetis hanya diuji pada data sintetis juga, akan terjadi bias evaluasi sirkular (synthetic-to-synthetic). Dengan menguji kedua model pada Unseen Human-Annotated Test Set yang identik dari Nergrit, kita memperoleh jawaban empiris yang jujur: apakah korpus sintetis hasil distilasi LLM mampu memberikan daya generalisasi yang setara dengan data manusia ketika dihadapkan pada teks riil organik."*

### Pertanyaan 5: "Mengapa menggunakan evaluasi exact chunk-level match seqeval, dan bukan akurasi token standar?"
> **Rekomendasi Jawaban**:
> *"Akurasi berbasis token standar memiliki kelemahan fundamental pada tugas NER, yaitu fenomena ketidakseimbangan kelas (class imbalance). Pada korpus teks, lebih dari 85% hingga 90% token adalah kata umum di luar entitas (label 'O'). Model yang memprediksi semua token sebagai 'O' secara naif bisa memperoleh akurasi di atas 85%, namun model tersebut gagal total sebagai ekstraktor entitas.
> Standar baku CoNLL menggunakan pustaka `seqeval` menerapkan kriteria exact chunk-level match. Suatu entitas hanya dihitung benar jika seluruh rentang katanya (B- dan I-) beserta kelas semantiknya tepat seratus persen. Standar ketat inilah yang diakui secara global di komunitas NLP untuk mengukur ketepatan deteksi entitas yang sesungguhnya."*
