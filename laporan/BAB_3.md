# BAB 3 METODOLOGI PENELITIAN


## 3.1 Tipe dan Pendekatan Penelitian

Penelitian ini menggunakan tipe penelitian Non-implementatif – Analitik (*Analytical/Explanatory*). Fokus utama dari studi ini adalah untuk mengeksplorasi dan menganalisis perbandingan performa model bahasa secara komprehensif, bukan membangun atau mengimplementasikan sebuah sistem perangkat lunak untuk pengguna akhir.
Strategi penelitian yang dijalankan berupa perancangan dan pelaksanaan eksperimen *fine-tuning* pada model `indobenchmark/indobert-large-p1` di atas tugas NER. Eksperimen ini dirancang untuk membuktikan validitas hipotesis bahwa data berlabel hasil sintesis (*synthetic data*) dari *Large Language Model* (LLM) mampu menghasilkan metrik performa yang sebanding atau bahkan melampaui data berlabel yang dianotasi oleh pakar manusia (*gold-standard*).

## 3.2 Alur Penelitian

Pelaksanaan penelitian ini disusun dalam tahapan-tahapan yang sistematis dan berurutan. Secara umum, alur penelitian terbagi ke dalam enam tahap utama:

1. **Studi Literatur**: Mengkaji konsep dasar NLP, *Named Entity Recognition* (NER), arsitektur Transformer dan IndoBERT, serta mekanisme augmentasi dan distilasi data menggunakan orkestrasi model bahasa besar (*Large Language Models* / LLM).
2. **Pengumpulan Dataset Acuan**: Mengakuisisi korpus acuan NER bahasa Indonesia beranotasi manusia (*Gold-standard*) dari pangkalan data NERGRIT.
3. **Pembuatan Data Sintetis Dua Fase**: Mengeksekusi pembuatan empat korpus data sintetis berbasis orkestrasi 2-fase LLM (*generation* dan *verification/refining*) mencakup pasangan Nemotron-3 Super–Ultra, GPT-5.6 Luna–Gemini Flash, Gemma 4–Nemotron Super, dan GPT-OSS–Nemotron Nano.
4. **Penyiapan Data dan Audit Mutu Anotasi**: Melakukan pengelompokan ulang n-gram teks untuk mencegah kebocoran data (*data leakage*), pemetaan format label BIO 18 kelas entitas, serta audit manual independen dua penilai pada 400 kalimat sampel terstratifikasi data sintetis.
5. **Pelatihan Model (*Fine-Tuning*) IndoBERT**: Melakukan *fine-tuning* model `indobenchmark/indobert-large-p1` pada 5 skenario korpus utama serta variasi kurva pembelajaran kesetaraan jumlah entitas (*iso-entity*) dengan 3 *random seed* pelatihan (42, 123, 2026).
6. **Evaluasi dan Analisis Komparatif**: Menguji seluruh model pada himpunan data uji beranotasi manusia (*Gold test set*), tolok ukur sintetis independen, serta evaluasi daya generalisasi transfer lintas enam korpus eksternal berbahasa Indonesia.

Diagram alir keseluruhan dari penelitian ini disajikan pada Gambar 3.1.

```mermaid
graph TD
    A[Mulai] --> B[Studi Literatur]
    B --> C[Pengumpulan Dataset Acuan<br/>NERGRIT Gold]
    B --> D[Pembuatan Data Sintetis Dua Fase<br/>4 Pipeline Generator-Korektor LLM]
    C --> E[Penyiapan Data & Audit Manual<br/>Pencegahan Kebocoran 0 Group]
    D --> E
    E --> F[Pelatihan Fine-Tuning IndoBERT<br/>5 Kondisi Utama & Kurva Iso-Entity<br/>Seed 42, 123, 2026]
    F --> G[Evaluasi Komparatif:<br/>1. Data Uji Acuan Gold Manusia<br/>2. Tolok Ukur Sintetis Independen<br/>3. Transfer Lintas 6 Korpus Eksternal]
    G --> H[Analisis Hasil dan Pembahasan]
    H --> I[Kesimpulan dan Rekomendasi]
    I --> J[Selesai]
```

**Gambar 3.1 Flowchart Alur Penelitian**

## 3.3 Subjek dan Pengumpulan Data

Bagian ini menguraikan asal dan karakteristik dataset teks berbahasa Indonesia yang digunakan sebagai pilar utama pelabelan NER. Proses pemerolehan data terbagi menjadi dua bagian, yaitu perolehan dataset manual dan pembuatan dataset sintetis.

### 3.3.1 Dataset Anotasi Manusia (NERGRIT)

Sebagai representasi data pelabelan organik dari manusia (*human annotation*), penelitian ini tidak melakukan pengumpulan data primer, melainkan memanfaatkan dataset sekunder yang sudah tersedia secara publik. Dataset yang digunakan adalah korpus NERGRIT, sebuah himpunan data NLP ekstensif berbahasa Indonesia yang dikembangkan oleh Grit ID.

Korpus NERGRIT memuat ribuan kalimat teks berdomain umum (*general domain*) berbahasa Indonesia dengan anotasi NER hasil karya penilai manusia, yang dalam penelitian ini diposisikan sebagai *baseline* acuan (*Gold-standard*). Penetapan kedudukan sebagai korpus acuan tidak serta-merta mengasumsikan bahwa seluruh label di dalamnya bebas dari kesalahan. Oleh karena itu, karakteristik intrinsik, variasi, dan ketidakkonsistenan anotasi bawaan tetap dicatat dan dianalisis secara objektif.

### 3.3.2 Pembuatan Data Sintetis Berbasis LLM (2-Phase Generation)

Dataset beranotasi sintetis tidak diambil dari repositori publik yang sudah ada, melainkan dibangun secara mandiri (*synthetically generated*) menggunakan arsitektur agen LLM ganda melalui mekanisme generasi dua fase (*2-Phase Generation*). Mekanisme ini memisahkan tugas penciptaan teks dan pengoreksian anotasi untuk menekan tingkat anomali dan halusinasi penandaan entitas sebagaimana disarankan oleh Kamoi et al. (2024) serta Zhang et al. (2024).

Penelitian ini mengevaluasi empat kombinasi pasangan model generator dan korektor (*refiner*) LLM:
1. **Nemotron**: Nemotron-3 Super 120B sebagai generator dan Nemotron-3 Ultra 550B sebagai verifikator/korektor.
2. **Luna**: GPT-5.6 Luna sebagai generator dan Gemini 3.6 Flash Medium sebagai verifikator/korektor.
3. **Gemma**: Gemma 4 31B sebagai generator dan Nemotron-3 Super 120B sebagai verifikator/korektor.
4. **GPT-OSS**: GPT-OSS 120B sebagai generator dan Nemotron-3 Nano 30B sebagai verifikator/korektor.

Masing-masing *pipeline* dioperasikan menggunakan instruksi sistem (*prompt*) yang disesuaikan dengan karakteristik arsitektur model dan diarsipkan versinya secara terprogram. Target awal pembangkitan data dirancang mendekati skala volume korpus acuan NERGRIT (sekitar 17.431 kalimat). Seluruh data hasil generasi dari keempat *pipeline* disimpan secara utuh tanpa penyaringan sepihak pasca-generasi, sehingga sifat asli data hasil sintesis dapat diamati secara transparan. Keempat *pipeline* menerapkan arsitektur distilasi dua fase dengan rancangan taksonomi *prompt* generasi dan verifikasi terstandarisasi 19 kategori entitas (18 kelas OntoNotes ditambah kategori penampung gelar `TTL` guna mengisolasi sapaan dan gelar kehormatan agar tidak mengotori nama individu `PER`, tanpa menyertakan kategori `REG` yang ambigu). Kategori `TTL` (beserta label `REG` pada sumber NERGRIT Gold) kemudian dinormalisasi ke label `O` pada tahap pelatihan dan evaluasi, menghasilkan ruang klasifikasi 18 kelas entitas baku (37 tag BIO). Pada sub-subbab berikut, arsitektur *pipeline*, perancangan *prompt*, dan konversi format diuraikan secara rinci.

#### 3.3.2.1 Arsitektur Pipeline Distilasi Dua Fase

Arsitektur sistem distilasi data dirancang berjenjang dengan memanfaatkan dua varian model bahasa dari lini NVIDIA Nemotron-3 yang memiliki spesialisasi komputasi berbeda. Alur kerja komputasi pipeline distilasi disajikan pada Gambar 3.2.

```mermaid
graph TD
    A[Katalog 30 Domain Topik Indonesia] -->|Sampling 3 Topik Acak| B[Modul Penyusun Prompt Generasi]
    B -->|Instruksi & Format JSON| C[Fase 1: Nemotron-3 Super 120B<br/>Generator, Temp = 0.75]
    C -->|Batch 10 Kalimat Mentah + Entitas| D[Validasi Struktur JSON Mentah]
    D -->|Data Lolos Parsing| E[Fase 2: Nemotron-3 Ultra 550B<br/>Verifier/Refiner, Temp = 0.20]
    E -->|Koreksi Batas, Tipe, & Integritas| F{Validasi Integritas Batch<br/>Jumlah Kalimat Sesuai?}
    F -->|Ya| G[Anotasi JSON Terverifikasi]
    F -->|Tidak / Galat| H[Fallback: Pertahankan Anotasi Mentah]
    G --> I[Penyelarasan Token & Greedy Longest-Match]
    H --> I
    I --> J{Validasi Sintaksis IOB2<br/>validate_sentence_bio}
    J -->|Valid| K[Kompilasi Korpus Format CoNLL-2003]
    J -->|Tidak Valid| L[Eksklusi Kalimat Anomali]
    K --> M[Repositori Hugging Face Hub<br/>indobert-ner-distillation-data]
```

**Gambar 3.2 Diagram Alur Pipeline Pembuatan dan Pemurnian Data Sintetis 2-Fase**

Kedua model yang diorkestrasi dalam pipeline ini memiliki konfigurasi hiperparameter inferensi yang disesuaikan dengan peran fungsionalnya, sebagaimana ditunjukkan pada Tabel 3.1.

**Tabel 3.1 Spesifikasi Konfigurasi Inferensi Model Generator dan Verifier**

| Parameter Konfigurasi | Fase 1: Generator | Fase 2: Verifier / Refiner |
|---|---|---|
| Nama Model | `nvidia/nemotron-3-super-120b-a12b:free` | `nvidia/nemotron-3-ultra-550b-a55b:free` |
| Arsitektur Model | Hibrida Mamba-Attention (LatentMoE) | Hibrida Mamba-Attention (LatentMoE) |
| Total Parameter | 120 Miliar Parameter | 550 Miliar Parameter |
| Parameter Aktif per Token | 12 Miliar Parameter | 55 Miliar Parameter |
| Kedalaman Arsitektur | 88 Lapisan (*Layers*) | 108 Lapisan (*Layers*) |
| Nilai *Temperature* (T) | 0.75 | 0.20 |
| Ukuran *Batch* (*Batch Size*) | 10 kalimat per permintaan (*request*) | 5 kalimat per permintaan (*request*) |
| Peran Fungsional | Kreativitas teks sintaksis & variasi semantik | Penalaran logis kritis & audit batas entitas |

Pada Fase 1, model Nemotron-3 Super dioperasikan dengan *temperature* relatif tinggi ($T = 0,75$) untuk mendorong fleksibilitas kosakata dan keragaman struktur gramatikal bahasa Indonesia. Sebaliknya, pada Fase 2, model Nemotron-3 Ultra dioperasikan dengan *temperature* rendah ($T = 0,20$) untuk mengurangi variasi inferensi dan memusatkan perhatian pada tugas koreksi tanpa menambahkan teks halusinatif baru.

#### 3.3.2.2 Desain Rekayasa Prompt Generasi (Generation Prompt Engineering)

Untuk memastikan bahwa data yang dihasilkan tidak bias pada ranah tertentu dan menyerupai distribusi bahasa alami pada korpus NERGRIT, perancangan *prompt* generasi menerapkan strategi diversifikasi domain tematik. *Pipeline* menyusun katalog yang terdiri dari 30 topik bahasa Indonesia yang mencakup berbagai sektor kehidupan nasional:

1. Politik, kabinet pemerintahan, pemilu, dan birokrasi kementerian nasional.
2. Ekonomi makro, pasar saham (IHSG), kebijakan moneter Bank Indonesia, dan inflasi.
3. Bisnis korporasi, merger/akuisisi BUMN dan swasta, serta UMKM daerah.
4. Olahraga nasional dan internasional (Liga 1, Timnas, BWF, SEA Games).
5. Industri teknologi informasi, *startup unicorn* lokal, dan adopsi AI.
6. Hukum dan peradilan (sidang MK, Mahkamah Agung, KPK, UU ITE).
7. Kriminalitas, penegakan hukum Polri, dan keamanan siber.
8. Layanan kesehatan masyarakat, BPJS Kesehatan, dan riset kedokteran.
9. Pendidikan tinggi, riset universitas (UI, UGM, ITB, dsb.), dan beasiswa LPDP.
10. Seni rupa, budaya tradisional nusantara, dan warisan UNESCO (batik, wayang).
11. Industri hiburan nasional, perfilman (FFI), dan musik internasional.
12. Lingkungan hidup, konservasi satwa langka, dan penanganan polusi perkotaan.
13. Bencana alam dan sistem mitigasi BMKG (gempa bumi, banjir, letusan gunung).
14. Infrastruktur sipil, jalan tol nasional, dan perumahan rakyat.
15. Transportasi massal (MRT, LRT, Kereta Cepat Whoosh) dan logistik pelabuhan.
16. Pertahanan dan militer nasional (TNI AD, AL, AU) dan modernisasi alutsista.
17. Kehidupan beragama, ormas kemasyarakatan (NU, Muhammadiyah), dan toleransi.
18. Pertanian, ketahanan pangan, perkebunan sawit, dan kedaulatan pangan.
19. Kelautan, perikanan tangkap, dan kekayaan maritim nusantara.
20. Pariwisata, destinasi super prioritas (Labuan Bajo, Borobudur), dan kuliner lokal.
21. Sains dan riset antariksa (BRIN, satelit SATRIA, observatorium).
22. Hubungan internasional, diplomasi KTT ASEAN/G20, dan kerja sama bilateral.
23. Sejarah nasional, kemerdekaan RI, dan tokoh pahlawan nusantara.
24. Peristiwa dan festival daerah (Pesta Danau Toba, Festival Tabuik, dsb.).
25. Energi terbarukan, transisi energi bersih, PLTS, dan nikel/baterai EV.
26. Keuangan digital, perbankan syariah, dompet digital, dan QRIS.
27. Transportasi udara, maskapai penerbangan, dan bandara perintis.
28. Otomotif, industri kendaraan listrik nasional, dan pameran GIIAS.
29. Ketenagakerjaan, upah minimum (UMR), hak buruh, dan bonus demografi.
30. Hubungan sosial masyarakat, kearifan lokal, dan gotong royong pedesaan.

Setiap kali modul pengirim meminta kalimat baru ke model generator, sistem secara acak memilih tiga tema dari katalog tersebut (*random multi-topic sampling*) untuk disisipkan ke dalam *prompt*. Hal ini mencegah model terjebak dalam pengulangan pola kalimat (*pattern collapse*).

Format instruksi (*Generation Prompt Template*) yang dirancang untuk mengarahkan model generator disajikan sebagai berikut:

```text
Anda adalah pakar anotasi Named Entity Recognition (NER) standar internasional untuk bahasa Indonesia.
Tugas Anda: Buatlah TEPAT {batch_size} kalimat berita bahasa Indonesia yang kaya entitas, realistis, dan beragam secara kontekstual, lalu tandai seluruh entitas yang muncul sesuai 19 taksonomi standar di bawah.

Topik kalimat yang harus diangkat dalam batch ini:
{topics_str}

Daftar 19 Entitas Resmi (HANYA gunakan label ini):
1.  PER (Person): Nama individu manusia (HANYA nama orang, JANGAN sertakan gelar/jabatan).
2.  TTL (Title): Gelar kehormatan, keagamaan, bangsawan, akademis, profesi, atau jabatan resmi (cth: Presiden, Menteri, dr., Prof., Kiai, Gubernur, Dirut, Brigjen).
3.  GPE (Geo-Political Entity): Negara, provinsi, kota, kabupaten, desa/kelurahan berdaulat (cth: Indonesia, Jawa Barat, Jakarta, Surabaya).
4.  LOC (Non-GPE Location): Lokasi geografis alami/spesifik non-politik (sungai, laut, selat, gunung, benua, danau, samudra).
5.  ORG (Organization): Lembaga pemerintah, kementerian, BUMN, korporasi swasta, partai politik, LSM, universitas.
6.  FAC (Facility): Bangunan buatan manusia, infrastruktur fisik, bandara, pelabuhan, stasiun, jalan tol, jembatan, rumah sakit, stadion.
7.  EVT (Event): Peristiwa bersejarah, festival budaya, konferensi, KTT diplomatik, bencana alam berpenamaan, turnamen olahraga.
8.  PRD (Product): Barang komersial, teknologi bermerek, kendaraan, perangkat lunak/aplikasi berpemilik, model alutsista.
9.  NOR (Nationality/Religious/Political Group): Kewarganegaraan, suku bangsa, kelompok etnis, penganut agama, faksi ideologi (cth: WNI, suku Dayak, umat Muslim).
10. DAT (Date): Tanggal kalender, hari, bulan, tahun, dekade, atau rentang tanggal spesifik (cth: 17 Agustus 1945, Senin, 2026).
11. TIM (Time): Waktu jam spesifik dalam hari (cth: pukul 09.30 WIB, 14:00, tengah malam).
12. MON (Money): Nilai nominal moneter beserta satuan mata uang (cth: Rp 5 triliun, 50 miliar rupiah, USD 200 juta).
13. QTY (Quantity): Angka pengukuran fisik bersama satuan ukurnya (berat, panjang, luas, volume, kapasitas listrik, cth: 50 ton, 100 km, 15 megawatt).
14. CRD (Cardinal Number): Bilangan cacah murni yang BUKAN tanggal, uang, atau kuantitas terukur (cth: tiga, 150, puluhan, ratusan ribu).
15. ORD (Ordinal Number): Bilangan urutan atau tingkatan (cth: pertama, ke-75, ketiga).
16. PRC (Percent): Nilai persentase bersama lambang atau kata persen (cth: 5,2 persen, 10%).
17. LAW (Law): Dokumen perundang-undangan formal, UU, PP, Perpres, KUHP, pasal konstitusi (cth: UU No. 19 Tahun 2019, KUHAP).
18. LAN (Language): Bahasa komunikasi manusia (cth: bahasa Indonesia, bahasa Jawa, bahasa Inggris).
19. WOA (Work of Art): Judul buku, film, lagu, lukisan, album, atau karya cipta terpublikasi resmi.

⚠️ ATURAN EMAS: PEMISAHAN "TTL" DAN "PER" (SANGAT KRUSIAL!):
- DILARANG KERAS menggabungkan gelar/jabatan ke dalam PER!
- Contoh SALAH: {"entity": "Presiden Joko Widodo", "type": "PER"}
- Contoh BENAR:  {"entity": "Presiden", "type": "TTL"}, {"entity": "Joko Widodo", "type": "PER"}
- Contoh SALAH: {"entity": "Menteri Keuangan Sri Mulyani", "type": "PER"}
- Contoh BENAR:  {"entity": "Menteri Keuangan", "type": "TTL"}, {"entity": "Sri Mulyani", "type": "PER"}

Keluaran WAJIB berupa JSON murni dengan skema persis seperti ini:
{
  "data": [
    {
      "text": "Presiden Joko Widodo meresmikan Sirkuit Mandalika di Lombok Tengah pada hari Minggu.",
      "entities": [
        {"entity": "Presiden", "type": "TTL"},
        {"entity": "Joko Widodo", "type": "PER"},
        {"entity": "Sirkuit Mandalika", "type": "FAC"},
        {"entity": "Lombok Tengah", "type": "GPE"},
        {"entity": "Minggu", "type": "DAT"}
      ]
    }
  ]
}
```

#### 3.3.2.3 Mekanisme Koreksi dan Kontrol Kualitas (Quality Control & Verification Prompt)

Meskipun model generator mampu menghasilkan kalimat dengan keluwesan sintaksis yang baik, anotasi entitas awal yang disematkan kerap memuat ketidaksempurnaan. Oleh karena itu, seluruh himpunan kalimat hasil generasi dialirkan ke Nemotron-3 Ultra sebagai agen pengoreksi kualitas (*Quality Control Refiner*).

Model verifikator menerima masukan berupa paket data JSON berisi 5 kalimat hasil generasi mentah beserta entitasnya. *Prompt* verifikasi menginstruksikan model untuk melakukan lima tindakan korektif:
1. **Pemurnian Batas Kata (*Boundary Refinement*)**: Memastikan bahwa teks entitas mencakup kata secara lengkap dan bersih dari pemotongan karakter atau tanda baca yang tidak relevan.
2. **Eliminasi Entitas Palsu (*False Positive Pruning*)**: Menghapus penandaan pada kata benda umum (*common nouns*) yang keliru dianggap sebagai entitas bernama.
3. **Penemuan Entitas Terlewat (*Omitted Entity Recovery*)**: Mendeteksi dan menambahkan entitas bernama yang secara kontekstual hadir pada teks kalimat namun terlewat dari daftar anotasi pada Fase 1.
4. **Koreksi Kesalahan Tipe (*Type Reclassification*)**: Memperbaiki kekeliruan klasifikasi label kelas (sebagai contoh, nama entitas wilayah perkotaan yang keliru dilabeli `LOC` dikoreksi menjadi entitas geopolitik `GPE`).
5. **Pengawasan Integritas *Batch* (*Batch Integrity Guard*)**: Sistem melakukan validasi komputasi terhadap panjang array keluaran. Apabila jumlah kalimat hasil verifikasi tidak sama persis dengan jumlah kalimat masukan pada *batch* bersangkutan (*length mismatch*), sistem secara otomatis membatalkan pembaruan pada *batch* tersebut dan mempertahankan data mentah asli demi mencegah korupsi atau pergeseran indeks kalimat.

Struktur rancangan *prompt* kontrol kualitas (*Verification & Quality Control Prompt Template*) yang diinjeksikan ke agen pengoreksi kualitas disajikan sebagai berikut:

```text
Anda adalah pakar Quality Control (QC) dan Verifikator Ahli untuk Named Entity Recognition (NER) bahasa Indonesia.
Tugas: Periksa, koreksi kesalahan anotasi, dan perbaiki batas entitas pada kumpulan data JSON berikut secara SANGAT TELITI dan KETAT.

Daftar 19 Entity Types yang VALID:
1.  PER (Person): Nama orang, tokoh, individu. JANGAN sertakan gelar/jabatan!
2.  TTL (Title): Gelar kehormatan, gelar akademik, profesi, jabatan resmi, gelar keagamaan (dr., Prof., Presiden, Menteri, Kiai, Jenderal, dll).
3.  GPE (Geo-Political Entity): Negara, kota, provinsi, kabupaten, desa, wilayah administratif.
4.  LOC (Location): Nama geografis non-GPE (Gunung, Sungai, Danau, Laut, Benua, Pulau).
5.  ORG (Organization): Perusahaan, partai politik, instansi pemerintah, lembaga, BUMN, LSM, universitas, klub, yayasan.
6.  FAC (Facility): Gedung, bandara, jembatan, stadion, jalan tol, monumen buatan manusia.
7.  EVT (Event): Peristiwa bersejarah, festival, perang, konferensi, bencana bernama, piala dunia.
8.  PRD (Product): Merk dagang, tipe gawai, perangkat lunak, kendaraan, produk komersial.
9.  NOR (Nationality/Religious/Political Group): Kewarganegaraan, suku bangsa, kelompok etnis, penganut agama, faksi ideologi (cth: WNI, suku Dayak, umat Muslim).
10. DAT (Date): Tanggal, hari, bulan, tahun spesifik, tanggal relatif (kemarin, lusa).
11. TIM (Time): Jam spesifik, durasi waktu, rentang waktu (14.00 WIB, 2 jam).
12. MON (Money): Nilai uang beserta mata uangnya (Rp 50.000, 10 dollar AS).
13. QTY (Quantity): Angka dengan satuan ukur/bobot/panjang (50 kg, 100 meter, 3 hektar).
14. CRD (Cardinal): Bilangan cacah murni tanpa satuan ukur (10, lima, 1.000).
15. ORD (Ordinal): Bilangan urutan/peringkat (pertama, ke-2, ketiga).
16. PRC (Percent): Persentase (50%, 10 persen).
17. LAW (Law): Undang-Undang, Perpres, regulasi, pasal hukum resmi (UU No. 11 Tahun 2020).
18. LAN (Language): Bahasa (Bahasa Indonesia, Jawa, Mandarin).
19. WOA (Work of Art): Judul film, lagu, buku, novel, karya seni lukis.

PEDOMAN KOREKSI WAJIB DAN KETAT:
1. INTEGRITAS TEKS (SANGAT PENTING):
   - JANGAN PERNAH mengubah, memotong, mengoreksi, atau memparafrase teks kalimat asli di properti "text".
   - Nilai "text" harus 100% SAMA PERSIS dengan input (karakter per karakter). Hanya perbaiki daftar anotasi pada properti "entities".
2. PEMISAHAN NAMA ORANG VS GELAR (PER VS TTL - SANGAT PENTING):
   - "PER" HANYA boleh berisi nama orang/individu itu sendiri.
   - Semua gelar, pangkat, sapaan, atau jabatan harus dipisahkan menjadi "TTL", BUKAN digabung ke "PER".
   - CONTOH PERBAIKAN:
     * SALAH: {"entity": "Presiden Joko Widodo", "type": "PER"}
     * BENAR: {"entity": "Presiden", "type": "TTL"}, {"entity": "Joko Widodo", "type": "PER"}
     * SALAH: {"entity": "dr. Andi Wijaya", "type": "PER"}
     * BENAR: {"entity": "dr.", "type": "TTL"}, {"entity": "Andi Wijaya", "type": "PER"}
     * SALAH: {"entity": "Menteri Keuangan Sri Mulyani", "type": "PER"}
     * BENAR: {"entity": "Menteri Keuangan", "type": "TTL"}, {"entity": "Sri Mulyani", "type": "PER"}
3. BATAS KATA & TANDA BACA (BOUNDARIES):
   - Pastikan teks entitas mencakup kata lengkap tanpa terpotong atau kelebihan tanda baca, serta persis sama dengan substring di dalam "text".
   - Singkatan dan Tanda Kurung: Jangan sertakan tanda kurung `()` ke dalam batas entitas. Pisahkan:
     * SALAH: {"entity": "Komisi Pemilihan Umum (KPU)", "type": "ORG"}
     * BENAR: {"entity": "Komisi Pemilihan Umum", "type": "ORG"}, {"entity": "KPU", "type": "ORG"}
   - Batas Tanggal (DAT): Jangan menyertakan kata bantu seperti "tanggal", "pada", atau "hari" ke dalam entitas DAT (misal: gunakan "14 Februari 2024", bukan "tanggal 14 Februari 2024").
4. ENTITAS TERLEWAT: Tambahkan entitas valid yang ada di teks namun belum masuk daftar "entities".
5. TIPE SALAH: Perbaiki tipe entitas yang keliru (misal kota diberi LOC seharusnya GPE; instansi/partai diberi NOR seharusnya ORG; ransomware diberi EVT seharusnya PRD).
6. FALSE POSITIVES: Hapus kata benda umum atau halusinasi yang salah dimasukkan sebagai entitas bernama.
7. STANDAR 19 TIPE RESMI: Gunakan 19 tipe: PER, TTL, GPE, LOC, ORG, FAC, EVT, PRD, NOR, DAT, TIM, MON, QTY, CRD, ORD, PRC, LAW, LAN, WOA.

DATA YANG HARUS DIPERIKSA DAN DIPERBAIKI:
{batch_json}

KEMBALIKAN OUTPUT HANYA DALAM BENTUK SATU OBJEK JSON:
{
  "data": [ ...daftar kalimat yang telah diperiksa dan diperbaiki... ]
}
Langsung mulai dengan { dan akhiri dengan }. Tanpa penjelasan conversational.
```

#### 3.3.2.4 Penyelarasan Rentang Entitas (Span Alignment) dan Format BIO

Tahap akhir dalam pembuatan data sintetis adalah mentransformasikan anotasi entitas berbasis rentang teks (*character/word span*) dari format JSON ke dalam representasi sekuensial tingkat token dengan skema BIO (*Beginning, Inside, Outside*) berstandar CoNLL-2003 yang siap diproses oleh modul tokenisasi IndoBERT.

Proses penyelarasan dilaksanakan melalui tahapan komputasi berikut:
1. **Tokenisasi Teks**: Teks kalimat dipecah menjadi sekuens token kata dan tanda baca menggunakan ekspresi reguler `[\w]+|[^\s\w]`.
2. **Penyelarasan Rentang Terpanjang (*Greedy Longest-Match Alignment*)**: Anotasi entitas diurutkan secara menurun (*descending*) berdasarkan panjang karakter string entitas sebelum dipetakan ke urutan token. Prioritas pada entitas terpanjang ini mencegah entitas multi-kata (misalnya *"Sirkuit Internasional Mandalika"*) terpotong atau teranotasi sebagian oleh entitas kata tunggal di dalamnya. Setiap token yang telah terpasangkan ditandai dengan larik boolean untuk mencegah konflik penimpaan (*overlapping annotations*).
3. **Validasi Konsistensi Sintaksis IOB2**: Seluruh kalimat berformat token-tag diuji menggunakan fungsi penjamin mutu `validate_sentence_bio`. Algoritme ini memastikan secara ketat bahwa tidak ada tag `I-TYPE` yang muncul secara mandiri (*orphaned tag*) tanpa didahului oleh tag `B-TYPE` atau `I-TYPE` dari kelas entitas yang bersesuaian. Kalimat yang memuat anomali sintaksis BIO langsung dieksklusi dari himpunan data akhir.
4. **Penyusunan Format CoNLL-2003**: Kalimat yang lolos validasi dikompilasi ke dalam berkas teks berformat CoNLL-2003 (Sang & De Meulder, 2003) di mana setiap baris berisi pasangan token dan tag yang dipisahkan oleh karakter tabulasi, serta dipisahkan oleh satu baris kosong antar kalimat.

Seluruh berkas korpus sumber beserta riwayat *prompt* generasi diarsipkan secara permanen tanpa menghapus label aslinya. Untuk kebutuhan pelatihan dan evaluasi model IndoBERT, diterapkan skema representasi eksperimen 18 kelas entitas (37 tag BIO). Dalam representasi ini, label gelar `TTL` (*Title*) serta `REG` (*Religion* pada skema asli NERGRIT) dipetakan ke dalam label latar belakang `O`. Pengecualian kategori `REG` didasarkan pada tingginya ambiguitas dan tumpang tindih taksonomi (*semantic collision*) pada korpus acuan NERGRIT, di mana label `REG` tidak hanya memuat nama agama murni (12,6%), melainkan didominasi oleh entitas yang bertabrakan langsung dengan kelas aktif lain—meliputi hari raya keagamaan yang bertabrakan dengan `EVT`/`DAT` (seperti *Idul Fitri*, *Lebaran*, dan *Natal*), kelompok umat yang bertabrakan dengan `NOR` (*Muslim*, *Kristiani*), kitab suci yang bertabrakan dengan `WOA` (*Al-Qur'an*), tempat ibadah yang bertabrakan dengan `FAC`/`LOC` (*masjid*, *gereja*), sebutan tokoh/Tuhan yang beririsan dengan `PER`/`TTL`, serta ungkapan doa lisan dan verba ibadah umum (*Alhamdulillah*, *Insya Allah*, *puasa*, *salat*) yang secara linguistik bukan merupakan entitas bernama. Pemetaan `REG` dan `TTL` ke label `O` ini mencegah timbulnya penalti evaluasi semu lintas kelas sekaligus menyelaraskan ruang evaluasi penelitian secara presisi dengan standar internasional **OntoNotes 5.0** (18 kelas entitas). Token yang dipetakan ke label O ini tetap disupervisi sebagai kelas negatif selama pelatihan, sehingga model terlatih untuk mengenali kata-kata non-entitas. Sementara itu, kategori angka kardinal (`CRD`) dan kuantitas berukuran (`QTY`) tetap dipisahkan sebagai dua kelas independen.

Prosedur penyiapan data eksperimen mempertahankan seluruh *record* kalimat, token sumber, dan transisi BIO apa adanya guna menjaga integritas data riil. Penyesuaian sintaksis terbatas pada koreksi kekeliruan ketik kode label BIO pada korpus NERGRIT (seperti `B-L0C` menjadi `B-LOC` dan `B=CRD` menjadi `B-CRD`) melalui pemetaan eksplisit yang terdokumentasi. Penyesuaian ini murni bersifat standardisasi kode format tanpa mengubah keputusan substantif atas anotasi semantik entitas. Token yang tidak menghasilkan token sub-kata saat tokenisasi diwakili oleh token khusus `[UNK]` pada lapisan adaptor masukan model tanpa memodifikasi token teks sumber aslinya.

### 3.3.3 Pembagian Data dan Pencegahan Kebocoran

Untuk menjamin perbandingan performa yang objektif dan mencegah bias estimasi, dilakukan prosedur pembagian data global dengan mekanisme pencegahan kebocoran (*data leakage prevention*). Partisi asal dari setiap kalimat dicatat terlebih dahulu, kemudian seluruh kalimat dari keenam korpus dikelompokkan ulang ke dalam kelompok-kelompok ekuivalensi (*equivalence groups*). Normalisasi teks berbasis NFKC, pengubahan huruf kecil (*case folding*), dan pembersihan spasi ganda diterapkan secara khusus untuk keperluan perbandingan kemiripan teks. Tingkat kemiripan antarkalimat diukur menggunakan koefisien *Jaccard similarity* karakter 5-gram dengan nilai ambang ≥ 0,90 untuk kalimat dengan panjang minimal 10 token.

Setiap kelompok kalimat yang memiliki tingkat kemiripan tinggi tersebut ditempatkan secara utuh ke dalam satu partisi data dengan urutan prioritas: kelompok yang memuat kalimat uji dialokasikan ke partisi *test*, kelompok yang memuat kalimat validasi dialokasikan ke *validation*, dan sisanya dialokasikan ke partisi *train*. Seluruh record berulang maupun variasi anotasi dalam satu kalimat dipertahankan di dalam partisi yang sama. Kelompok data sintetis yang tidak terikat dengan data uji dialokasikan ke dalam rasio 85% latih dan 15% validasi menggunakan *random seed* 42.

Partisi validasi digunakan secara eksklusif untuk pemantauan proses konvergensi dan pemilihan *checkpoint* terbaik selama pelatihan (*early stopping*). Evaluasi akhir utama dilaksanakan secara bersama pada partisi uji manusia (*Gold test*) hasil pengelompokan ulang. Selain itu, dataset tolok ukur (*benchmark*) sintetis tambahan dipertahankan seluruhnya dan dilaporkan secara terpisah. Korpus evaluasi eksternal juga diarsipkan secara utuh, di mana kalimat yang memiliki irisan teks terhadap data latih atau validasi ditandai secara eksplisit agar pengujian generalisasi bersifat murni *out-of-domain*. Keterbatasan metadata publik, seperti tidak tersedianya identitas dokumen (*document ID*) dan ketiadaan informasi keanggotaan korpus pra-latih IndoBERT, diakui secara terbuka sebagai batasan penelitian.

### 3.3.4 Analisis Karakteristik Dataset

Karakteristik struktural dan distribusi entitas pada setiap korpus dianalisis secara kuantitatif melalui formulasi metrik deskriptif. Misalkan $S$ menyatakan jumlah kalimat, $T$ menyatakan jumlah total token sumber sebelum pemecahan subword, $E$ menyatakan total rentang entitas aktif, $T_e$ menyatakan jumlah token yang tercakup dalam rentang entitas aktif, dan $E_c$ menyatakan jumlah rentang entitas pada kelas $c$. Metrik-metrik tersebut dirumuskan pada Persamaan 3.1 sampai Persamaan 3.5:

$$
\overline{L} = \frac{T}{S} \qquad (3.1)
$$

$$
\overline{E} = \frac{E}{S} \qquad (3.2)
$$

$$
D_{\text{token}} = \frac{T_e}{T} \times 100\% \qquad (3.3)
$$

$$
D_{\text{span}} = \frac{E}{T} \times 100 \qquad (3.4)
$$

$$
P_c = \frac{E_c}{E} \times 100\% \qquad (3.5)
$$

di mana:
- $\overline{L}$ adalah panjang rata-rata kalimat dalam satuan token,
- $\overline{E}$ adalah rata-rata rentang entitas per kalimat,
- $D_{\text{token}}$ merepresentasikan kepadatan token berentitas (persentase token teks yang merupakan bagian dari entitas bernama),
- $D_{\text{span}}$ merepresentasikan frekuensi rentang entitas per 100 token, dan
- $P_c$ menyatakan proporsi relatif kelas entitas $c$ terhadap total rentang entitas aktif.

Entitas multi-kata dihitung sebagai satu rentang entitas tunggal, sedangkan token format khusus (`[CLS]`, `[SEP]`, `[PAD]`) dan pecahan subword tidak disertakan dalam penghitungan statistik korpus. Modul penganalisis membaca tag `I-TYPE` tanpa pendahulu sebagai awal rentang entitas baru untuk keperluan penghitungan tanpa mengubah berkas data asli. Titik jangkar jumlah entitas pada eksperimen *iso-entity* dihitung secara tepat dari total entitas pada partisi latih Gold hasil pengelompokan ulang.

### 3.3.5 Pemeriksaan Manual Anotasi dan Reliabilitas Antarpenilai (IAA)

Untuk mengevaluasi mutu anotasi data sintetis secara empiris dan menguji reliabilitas pelabelan manusia, dilakukan audit manual independen terhadap keempat korpus sintetis hasil generasi LLM (`Nemotron`, `Luna`, `Gemma`, dan `GPT-OSS`). Pengambilan sampel dilakukan sebanyak 100 kalimat representatif per korpus sintetis melalui teknik acak berstrata tanpa pengembalian (*stratified random sampling without replacement*) dengan *seed* acak tetap `20261022`, menghasilkan total sampel audit sebanyak **400 kalimat** (**10.812 token**, mencakup **800 evaluasi independen**). Stratifikasi dibentuk melalui persilangan antara jumlah entitas dalam kalimat (strata 0 entitas, 1 entitas, dan ≥ 2 entitas) dengan panjang kalimat (di bawah atau sama dengan median populasi, serta di atas median populasi). Alokasi sampel dilakukan secara proporsional dengan alokasi minimum dua kalimat per stratum dan sensus penuh untuk stratum tunggal, di mana sisa anggaran didistribusikan menggunakan metode *largest remainder* hingga genap 100 kalimat per korpus. Penerapan audit berbasis 100 kalimat pada korpus NER mengacu pada preseden Koto et al. (2020), sedangkan prinsip stratifikasi diadaptasi dari metodologi Saldías Fuentes et al. (2022).

Evaluasi dilaksanakan secara mandiri (*blind* dan independen) oleh dua penilai manusia—Arif Athaya Harahap (Penilai A1) dan Muhammad Faiz Fauzan (Penilai A2)—tanpa saling berkomunikasi selama proses anotasi berlangsung. Reliabilitas antarpenilai (*Inter-Annotator Agreement* / IAA) diukur menggunakan **Cohen's Kappa (κ)** pada tingkat token (37 tag BIO dan 18 kelas + O) serta tingkat keputusan entitas (*KEEP* / *REMOVE* / *REPLACE* dan *CORRECT* / *INCORRECT*), didukung oleh **Pairwise Exact Span-F₁ Agreement** dan selang kepercayaan *bootstrap* 95% (1.000 iterasi) sesuai kaidah Landis & Koch (1977).

Setelah evaluasi independen selesai, keputusan akhir ditetapkan melalui aturan **Konsensus Dual-Agreement** yang ketat dan objektif:
1. Suatu rentang anotasi asli hanya dibatalkan (*False Positive* / *Wrong*) apabila kedua penilai secara independen sepakat menolaknya (keduanya menandai *REMOVE* atau mengajukan perbaikan).
2. Entitas baru atau pengganti (*Missing*) hanya ditambahkan ke dalam label konsensus apabila kedua penilai secara independen mengajukan batas rentang kata (*boundary*) dan label kelas entitas yang identik.
3. Apabila terjadi perbedaan pendapat antarpenilai (salah satu penilai mempertahankan rentang asli sementara penilai lainnya membatalkan), prinsip konservatif diterapkan dengan mempertahankan anotasi asli korpus (*benefit of the doubt*).

Penghitungan estimasi tingkat anomali kalimat pada sampel terstratifikasi dirumuskan pada Persamaan 3.6:

$$
\widehat{p}_{\text{error}} = \sum_h \frac{N_h}{N} \frac{e_h}{n_h} \qquad (3.6)
$$

di mana:
- $N$ adalah total ukuran populasi kalimat dalam korpus,
- $N_h$ adalah ukuran stratum $h$,
- $n_h$ adalah jumlah sampel kalimat yang diperiksa pada stratum $h$, dan
- $e_h$ menyatakan jumlah kalimat yang memuat setidaknya satu kekeliruan anotasi (*Wrong > 0* atau *Missing > 0*) terhadap konsensus pada stratum tersebut.

Nilai *True Positive* ($TP$), *False Positive* ($FP$), dan *False Negative* ($FN$) dihitung melalui perbandingan himpunan rentang entitas antara anotasi awal dan konsensus *dual-agreement*. Seluruh data audit dan catatan keputusan penilai diarsipkan secara permanen dan transparan dalam repositori penelitian tanpa memodifikasi berkas data latih model.

## 3.4 Perancangan Pelatihan (Fine-Tuning) IndoBERT

Proses *fine-tuning* pada penelitian ini memanfaatkan model representasi bahasa *pre-trained* `indobenchmark/indobert-large-p1`. Model ini diadaptasi untuk tugas penandaan sekuens (*sequence labeling*) dengan menambahkan arsitektur *Token Classification Head* di atas lapisan *encoder*.

### 3.4.1 Arsitektur Lapisan Klasifikasi Token (Token Classification Head)

Arsitektur IndoBERT-Large menghasilkan representasi vektor tersembunyi (*hidden states*) untuk setiap token masukan $t$ pada lapisan terakhirnya, dinyatakan sebagai vektor $h_t \in \mathbb{R}^d$ dengan dimensi ketersembunyian $d = 1024$. Untuk memetakan representasi tersebut ke dalam ruang probabilitas kelas entitas NER, diterapkan lapisan klasifikasi linear:

1. **Dropout Layer**: Diterapkan regularisasi *dropout* dengan probabilitas p = 0,1 untuk mencegah ketergantungan bobot yang berlebihan (*overfitting*).
2. **Linear Projection Layer**: Vektor tersembunyi ditransformasikan ke dalam ruang label sejumlah $K$ kelas ($K = 37$, mencakup label `O` serta pasangan `B-` dan `I-` dari 18 kelas entitas) melalui matriks bobot $W \in \mathbb{R}^{d \times K}$ dan bias $b \in \mathbb{R}^K$.
3. **Fungsi Aktivasi Softmax**: Distribusi probabilitas prediksi kelas entitas untuk setiap token $t$ dihitung menggunakan Persamaan 3.7:

$$
P(y_t = k \mid h_t) = \frac{\exp(W_k h_t + b_k)}{\sum_{j=1}^K \exp(W_j h_t + b_j)} \qquad (3.7)
$$

di mana $P(y_t = k \mid h_t)$ merepresentasikan probabilitas token $t$ tergolong ke dalam kelas entitas $k$, dengan $W_k$ menyatakan baris ke-$k$ dari matriks bobot proyeksi linear dan $b_k$ adalah suku bias yang bersesuaian.

### 3.4.2 Penanganan Subword dan Masked Cross-Entropy Loss

Tokenizer IndoBERT mengadopsi algoritma sub-kata (*WordPiece*), yang berpotensi memecah sebuah kata utuh menjadi beberapa sub-kata (*subword tokens*). Untuk menjaga integritas anotasi rentang entitas:
- Hanya sub-kata pertama dari sebuah kata yang diberikan label entitas asli (`B-TYPE` atau `I-TYPE`).
- Sub-kata pecahan lanjutan (misalnya `##kan` atau subword berikutnya) serta token format khusus (`[CLS]`, `[SEP]`, `[PAD]`) secara sengaja dipetakan ke nilai label semu $-100$.

Fungsi kerugian pelatihan dihitung menggunakan *Masked Cross-Entropy Loss*, sebagaimana disajikan pada Persamaan 3.8:

$$
\mathcal{L}_{\text{CE}} = -\frac{1}{\sum_{t=1}^T \mathbb{I}(y_t \neq -100)} \sum_{t=1}^T \mathbb{I}(y_t \neq -100) \sum_{k=1}^K y_{t,k} \log P(y_t = k \mid h_t) \qquad (3.8)
$$

di mana $\mathbb{I}(\cdot)$ merupakan fungsi indikator yang bernilai 1 jika label target valid ($y_t \neq -100$) dan bernilai 0 jika berupa token semu, sedangkan $y_{t,k} \in \{0, 1\}$ adalah representasi *one-hot* dari label *ground truth* token $t$ pada kelas $k$. Mekanisme ini memastikan gradien optimasi tidak terdistorsi oleh token *padding* maupun fragmentasi sub-kata.

### 3.4.3 Konfigurasi Hiperparameter dan Mekanisme Early Stopping

Pelatihan seluruh kondisi dikonfigurasi dengan batas atas durasi pelatihan sebanyak 10 *epochs*. Untuk menjaga agar model mencapai konvergensi optimal tanpa mengalami degradasi akibat *overfitting*, penelitian ini menerapkan strategi *Early Stopping*:
- *Early Stopping Callback* memantau nilai metrik *Macro F1-Score* pada himpunan data validasi di setiap akhir *epoch* (*eval_strategy="epoch"*).
- Parameter kesabaran (*patience*) ditetapkan sebesar 2 *epochs*. Apabila skor F1 validasi tidak menunjukkan kenaikan selama 2 *epoch* berturut-turut, proses pelatihan akan dihentikan secara otomatis.
- Parameter *load_best_model_at_end* diaktifkan (`True`), sehingga bobot model yang disimpan dan digunakan pada evaluasi akhir pengujian adalah bobot pada *epoch* dengan performa validasi tertinggi, bukan bobot dari *epoch* terakhir.

Penetapan konfigurasi hiperparameter pelatihan IndoBERT-large-p1 menerapkan protokol dua tahap guna menjamin landasan teoretis sekaligus validitas empiris:
1. **Penapisan Ruang Kandidat Berbasis Literatur (*Literature-Grounded Screening*)**: Ruang pencarian laju pembelajaran difokuskan pada empat kandidat standar {1 × 10⁻⁵, 2 × 10⁻⁵, 3 × 10⁻⁵, 5 × 10⁻⁵} yang direkomendasikan pada studi kestabilan *fine-tuning* BERT-Large (Devlin et al., 2019; Mosbach et al., 2021), rujukan baku model IndoBERT (Wilie et al., 2020), serta tolok ukur klasifikasi token NusaCrowd (Cahyawijaya et al., 2023).
2. **Verifikasi Empiris Bebas Kebocoran (*Zero-Leakage Validation Grid Search*)**: Sebelum menjalankan 84 proses pelatihan eksperimen utama, dilakukan eksperimen penalaan hiperparameter (*hyperparameter tuning*) terisolasi pada korpus acuan manusia (NERGRIT Gold) dan korpus sintetis representatif (Nemotron). Pengujian dievaluasi murni pada subset validasi (*validation split*) tanpa menyentuh subset pengujian (*test split*), guna mengukur dinamika konvergensi epoch, fungsi kerugian validasi (*loss calibration*), dan metrik *Macro/Micro F1-Score*. Hasil eksperimen empiris ini (dibahas rinci pada Subbab 4.4.1) membuktikan bahwa $lr = 2 \times 10^{-5}$ merupakan titik operasional terbaik (*Pareto-optimal*) yang menghasilkan nilai *loss* terendah dan konvergensi cepat pada epoch 4,0 secara konsisten di kedua jenis data.

Rincian spesifikasi hiperparameter pelatihan bersama dirangkum pada Tabel 3.2.

**Tabel 3.2 Spesifikasi Hiperparameter Pelatihan Model IndoBERT-large-p1**

| Parameter Pelatihan | Nilai Konfigurasi | Rasionalisasi & Keterangan |
|---|---|---|
| Model Fondasi (*Backbone*) | `indobenchmark/indobert-large-p1` | 24 *layers*, 1024 *hidden size*, 340M parameter (Wilie et al., 2020) |
| Panjang Sekuens Maksimum | 256 token termasuk token khusus | *Chunk* pada batas kata; prediksi digabungkan ke kalimat asli |
| Ukuran *Batch* Latih (*Train Batch Size*) | Microbatch 32, akumulasi gradien 1 | Effective batch 32 pada satu GPU A100, seragam antarkondisi |
| Ukuran *Batch* Evaluasi (*Eval Batch Size*) | 64 chunk per *batch* | Mempercepat evaluasi per *epoch* pada validasi |
| Laju Pembelajaran (*Learning Rate*) | 2 × 10⁻⁵ | Titik baku *Pareto-optimal* terverifikasi empiris pada validasi (Subbab 4.4.1; Devlin et al., 2019; Mosbach et al., 2021; Wilie et al., 2020) |
| Algoritme Pengoptimal (*Optimizer*) | AdamW (*weight decay* = 0,01) | Regularisasi L2 untuk mencegah pembesaran magnitudo bobot |
| Batas Maksimum *Epoch* | 10 *Epochs* | Batas atas pelatihan iteratif |
| Mekanisme Penghentian | *Early Stopping* (*patience* = 2) | Menghentikan pelatihan saat Macro-F1 validasi stagnan |
| Metrik Penentu Model Terbaik | *Validation Macro F1-Score* | Mengutamakan keseimbangan presisi dan *recall* lintas kelas |
| Strategi Penyimpanan Bobot | *Load Best Model at End* = True | Memilih *checkpoint* dengan performa validasi puncak |
| Seed Pelatihan | 42, 123, 2026 | Tiga pengulangan dengan *split* tetap; laporkan rerata dan simpangan baku |
| Penjadwal (*Scheduler*) dan Warmup | Linear, rasio *warmup* 0,10 | Kebijakan peningkatan laju pembelajaran awal yang seragam |
| Presisi dan Memori | Bobot FP32, *mixed precision* BF16 | Profil a100-bf16-b32-v2 konsisten untuk seluruh kondisi komputasi |
| Pemotongan Gradien (*Gradient Clipping*) | 1,0 | Batas atas norm gradien untuk kestabilan konvergensi |

## 3.5 Skenario Pengujian dan Eksperimen Komparatif

Eksperimen komparatif dirancang secara sistematis untuk menguji performa model IndoBERT-large-p1 pada beberapa dimensi pengujian yang komprehensif:

1. **Skenario Pelatihan Utama 5 Korpus**: Model di-*fine-tune* pada lima kondisi data latih yang berbeda, yaitu satu kondisi data acuan manusia (NERGRIT Gold) dan empat kondisi data sintetis penuh (Nemotron, Luna, Gemma, dan GPT-OSS). Seluruh kondisi dilatih dari bobot awal *backbone* yang identik (`indobenchmark/indobert-large-p1`) menggunakan tiga *random seed* pelatihan (42, 123, dan 2026). Inisialisasi bobot *classification head* diatur ulang secara independen sebelum setiap proses pelatihan dimulai. Model terbaik untuk setiap kondisi dipilih murni berdasarkan metrik *Macro F1-Score* pada data validasi melalui mekanisme *early stopping* dengan *patience* 2.
2. **Skenario Kesetaraan Jumlah Entitas (*Iso-Entity Experiment*)**: Untuk mengisolasi pengaruh volume entitas terhadap performa model, keempat korpus sintetis diuji pada variasi subset bersarang (*nested subsets*) dengan anggaran entitas bertingkat, yaitu 30%, 50%, 75%, 100%, 125%, 150%, dan maksimum dari total entitas latih NERGRIT Gold (42.614 entitas). Pemilihan kalimat dilakukan secara utuh menggunakan *seed* 42 dan diuji pada ketiga *seed* pelatihan model. Kelebihan sedikit entitas (*overshoot*) akibat pemotongan batas kalimat dicatat secara terbuka, sedangkan kondisi yang melampaui kapasitas korpus (seperti target 150% pada korpus Gemma) ditetapkan berstatus tidak tersedia (*unavailable*).
3. **Mekanisme Inferensi Bebas Label (*Label-Blind Chunking*)**: Selama tahap evaluasi validasi dan pengujian, pemecahan kalimat panjang menjadi potongan sekuens (*chunks*) bersifat *label-blind*, di mana batas pemotongan semata-mata mengacu pada batas kata teks tanpa memanfaatkan informasi letak entitas. Setiap potongan sekuens diprediksi secara independen dan direkonstruksi kembali ke posisi token aslinya sebelum penilaian metrik tingkat rentang entitas (*exact span match*) dilakukan.
4. **Pengujian Generalisasi Lintas Dataset (*Cross-Dataset Transfer*)**: Model terbaik dari setiap skenario diuji kemampuannya dalam melakukan generalisasi pada enam himpunan data NER independen berbahasa Indonesia, yaitu IndQNER, IndoLEM UI, IndoLEM UGM, Prosa, Singgalang, dan WikiANN Indonesia. Evaluasi lintas korpus menerapkan proyeksi label bersama pada kelas universal nama orang (`PER`) dan lokasi geografis (`LOC`), serta organisasi (`ORG`) pada korpus yang memuatnya, guna menguji ketahanan model di luar domain data latih.

## 3.6 Metode Analisis Data dan Evaluasi Kinerja

Data prediksi dari masing-masing skenario pada himpunan data uji (*test set*) dicatat dan dianalisis secara komparatif. Evaluasi performa model klasifikasi sekuens token mengadopsi pencocokan *span* dan kelas secara tepat bergaya CoNLL, dengan konvensi BIO eksplisit yang diuji terhadap contoh *multi-token*.

Penilaian kinerja dilakukan dengan kriteria *exact chunk-level match*, di mana sebuah entitas hanya dianggap benar apabila batas rentang token awal (`B-`), token lanjutan (`I-`), serta label kelas entitasnya bersesuaian persis dengan *ground-truth*. Tiga metrik utama yang digunakan adalah:

1. **Precision**: Mengukur rasio ketepatan entitas yang diprediksi oleh model terhadap seluruh prediksi positif, guna memastikan model tidak menghasilkan entitas halusinatif (*false positives*) (Persamaan 2.1 pada Bab 2).
2. **Recall**: Mengukur sensitivitas model dalam menemukan seluruh entitas aktual yang terdapat di dalam teks masukan, guna meminimalkan entitas nyata yang terlewat (*false negatives*) (Persamaan 2.2 pada Bab 2).
3. **F1-Score**: Rata-rata harmonik dari *Precision* dan *Recall* yang bertindak sebagai metrik utama penentu keunggulan model secara agregat (Persamaan 2.3 pada Bab 2).

Setiap metrik dihitung secara per kelas beserta jumlah dukungannya (*support*). Dalam perbandingan performa antarkondisi eksperimen, *Micro F1-Score* (Persamaan 2.4) bertindak sebagai metrik ringkasan agregat utama, sedangkan *Macro F1-Score* (Persamaan 2.5) digunakan sebagai instrumen pemilihan model terbaik (*checkpoint selection*), dengan *Weighted F1-Score* (Persamaan 2.6) dilaporkan sebagai metrik pendukung. Untuk menjamin reliabilitas statistik dan memastikan performa tidak bergantung pada inisialisasi bobot acak tertentu, seluruh hasil eksperimen disajikan dalam bentuk rerata (*mean*) dan simpangan baku sampel (*sample standard deviation*) dari ketiga pengulangan *seed* pelatihan (42, 123, dan 2026).

## 3.7 Lingkungan dan Peralatan Pendukung

Seluruh tahapan komputasi, mulai dari orkestrasi *pipeline* API distilasi data hingga pelatihan model *deep learning*, dijalankan pada lingkungan komputasi berbasis awan (*cloud computing*). Spesifikasi peralatan yang digunakan adalah sebagai berikut:

1. **Platform Komputasi**: Google Colaboratory (Google Colab).
2. **Perangkat Keras (*Hardware*)**:
   - Akselerator Grafis: GPU NVIDIA A100-SXM4 Tensor Core (40 GB / 80 GB HBM2e VRAM) dengan dukungan akselerasi komputasi *mixed precision* BF16 (*Bfloat16*).
   - Unit Pemroses Sentral: Intel Xeon Processor (12 vCPU).
   - Memori Sistem: ~83.5 GB *High-Memory System RAM*.
   - Media Penyimpanan: 100 GB *Cloud Disk Space* (terintegrasi dengan Google Drive 5 TB).
3. **Perangkat Lunak (*Software*) dan Pustaka Pendukung**:
   - Sistem Operasi: Linux Ubuntu 22.04 LTS (x86_64).
   - Bahasa Pemrograman: Python 3.10+.
   - Kerangka Kerja Deep Learning: PyTorch 2.x dengan akselerasi CUDA.
   - Pustaka Pemodelan Bahasa: Hugging Face `transformers` (v5.10.2) dan `accelerate` (v1.12.0).
   - Pustaka Manajemen Data: Hugging Face `datasets` (v5.0.0) dan `huggingface_hub` (v1.5.0).
   - Pustaka Metrik Evaluasi: `seqeval` dan `evaluate` untuk kalkulasi metrik *exact chunk-level* berstandar CoNLL.
   - Pustaka Ekstraksi & Statistik: `scikit-learn`, `numpy`, dan `pandas`.
