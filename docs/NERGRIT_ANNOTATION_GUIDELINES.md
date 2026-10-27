# Panduan Baku Anotasi Named Entity Recognition Korpus NERGRIT (Indonesian NER Annotation Guidelines)

## Pedoman Praktis & Teoretis Anotasi Korpus Berbahasa Indonesia Standar 19 Entitas NERGRIT untuk Anotator Manusia dan Rekayasa Prompt *Large Language Model* (LLM)

> **Status Dokumen**: Buku Panduan Definitif (*Authoritative Handbook*)  
> **Dasar Empiris**: Audit Komputasional 17.431 Kalimat Bersih & 60.448 Rentang Entitas Korpus Acuan Manusia NERGRIT (*Indonesian Named Entity Recognition Corpus*)  
> **Format Representasi**: BIO (*Beginning-Inside-Outside*) Tagging Scheme  
> **Cakupan Taksonomi**: 19 Kelas Entitas Aktif (`PER`, `ORG`, `LOC`, `GPE`, `FAC`, `EVT`, `WOA`, `LAW`, `PRD`, `LAN`, `DAT`, `TIM`, `MON`, `QTY`, `CRD`, `ORD`, `PRC`, `NOR`, `REG`)

---

## 📑 Daftar Isi

- [1. Pendahuluan & Karakteristik Korpus NERGRIT](#1-pendahuluan-karakteristik-korpus-nergrit)
  - [1.1 Profil dan Sejarah Singkat NERGRIT](#11-profil-dan-sejarah-singkat-nergrit)
  - [1.2 Urgensi Pedoman Baku](#12-urgensi-pedoman-baku)
  - [1.3 Hubungan Taksonomi: NERGRIT (19 Tag) vs OntoNotes 5.0 (18 Tag)](#13-hubungan-taksonomi-nergrit-19-tag-vs-ontonotes-50-18-tag)
- [2. Alur Kerja Anotasi & Protokol Penandaan BIO](#2-alur-kerja-anotasi-protokol-penandaan-bio)
  - [2.1 Mekanika Skema Penandaan BIO](#21-mekanika-skema-penandaan-bio)
  - [2.2 Aturan Validitas Transisi BIO (*Transition Integrity*)](#22-aturan-validitas-transisi-bio-transition-integrity)
  - [2.3 Nuansa Tokenisasi Bahasa Indonesia & Tanda Baca Lepas](#23-nuansa-tokenisasi-bahasa-indonesia-tanda-baca-lepas)
- [3. Taksonomi Semantik Komprehensif 19 Kelas Entitas](#3-taksonomi-semantik-komprehensif-19-kelas-entitas)
  - [3.1 PER — Person (Orang)](#31-per-person-orang)
  - [3.2 ORG — Organization (Organisasi / Korporasi / Klub Olahraga)](#32-org-organization-organisasi-korporasi-klub-olahraga)
  - [3.3 GPE — Geo-Political Entity (Wilayah Geopolitik Administratif)](#33-gpe-geo-political-entity-wilayah-geopolitik-administratif)
  - [3.4 LOC — Location (Lokasi Non-Geopolitik / Bentang Alam / Jalan)](#34-loc-location-lokasi-non-geopolitik-bentang-alam-jalan)
  - [3.5 FAC — Facility (Fasilitas Infrastruktur Fisik Buatan)](#35-fac-facility-fasilitas-infrastruktur-fisik-buatan)
  - [3.6 EVT — Event (Peristiwa / Ajang / Bencana)](#36-evt-event-peristiwa-ajang-bencana)
  - [3.7 WOA — Work of Art (Karya Seni & Cipta Intelektual)](#37-woa-work-of-art-karya-seni-cipta-intelektual)
  - [3.8 LAW — Law (Hukum / Perundang-Undangan / Traktat)](#38-law-law-hukum-perundang-undangan-traktat)
  - [3.9 PRD — Product (Produk / Komoditas Fisik / Sarana Transportasi)](#39-prd-product-produk-komoditas-fisik-sarana-transportasi)
  - [3.10 LAN — Language (Bahasa)](#310-lan-language-bahasa)
  - [3.11 DAT — Date (Tanggal / Hari / Bulan / Tahun / Kalender)](#311-dat-date-tanggal-hari-bulan-tahun-kalender)
  - [3.12 TIM — Time (Waktu Jam / Pukul)](#312-tim-time-waktu-jam-pukul)
  - [3.13 MON — Money (Nominal Moneter & Valuta)](#313-mon-money-nominal-moneter-valuta)
  - [3.14 QTY — Quantity (Kuantitas Fisik & Durasi Waktu)](#314-qty-quantity-kuantitas-fisik-durasi-waktu)
  - [3.15 CRD — Cardinal (Bilangan Kardinal Murni)](#315-crd-cardinal-bilangan-kardinal-murni)
  - [3.16 ORD — Ordinal (Bilangan Tingkat / Urutan)](#316-ord-ordinal-bilangan-tingkat-urutan)
  - [3.17 PRC — Percent (Persentase & Kadar)](#317-prc-percent-persentase-kadar)
  - [3.18 NOR — NORP (Organisasi Negara, Aparat, Parpol, & Demografi)](#318-nor-norp-organisasi-negara-aparat-parpol-demografi)
  - [3.19 REG — Religion (Agama, Penganut, Hari Raya, & Ritual)](#319-reg-religion-agama-penganut-hari-raya-ritual)
- [4. Kaidah Emas Penentuan Batas Rentang Entitas](#4-kaidah-emas-penentuan-batas-rentang-entitas)
  - [4.1 Eksklusi Preposisi Spasial & Temporal (99,99% Aturan Preposisi)](#41-eksklusi-preposisi-spasial-temporal-9999-aturan-preposisi)
  - [4.2 Perlakuan Gelar, Sapaan Kehormatan, dan Jabatan Formal](#42-perlakuan-gelar-sapaan-kehormatan-dan-jabatan-formal)
  - [4.3 Tanda Kurung Tanggal Kepala Berita pada DAT](#43-tanda-kurung-tanggal-kepala-berita-pada-dat)
  - [4.4 Inklusi Kata Benda Umum Huruf Kecil pada PRD](#44-inklusi-kata-benda-umum-huruf-kecil-pada-prd)
  - [4.5 Klasifikasi Durasi Waktu Lampau/Jangka ke dalam QTY](#45-klasifikasi-durasi-waktu-lampaujangka-ke-dalam-qty)
  - [4.6 Eksklusi Tanda Petik Ganda/Tunggal pada WOA dan EVT](#46-eksklusi-tanda-petik-gandatunggal-pada-woa-dan-evt)
  - [4.7 Penanganan Tanda Hubung (*Hyphenation*) & Reduplikasi](#47-penanganan-tanda-hubung-hyphenation-reduplikasi)
- [5. Pohon Keputusan Disambiguasi Kasus Rawan Tertukar](#5-pohon-keputusan-disambiguasi-kasus-rawan-tertukar)
  - [5.1 Pohon Keputusan: NOR vs ORG](#51-pohon-keputusan-nor-vs-org)
  - [5.2 Pohon Keputusan: PRD vs ORG](#52-pohon-keputusan-prd-vs-org)
  - [5.3 Pohon Keputusan: FAC vs LOC vs GPE](#53-pohon-keputusan-fac-vs-loc-vs-gpe)
  - [5.4 Pohon Keputusan Kelas Numerik: CRD vs QTY vs MON vs PRC vs DAT vs TIM](#54-pohon-keputusan-kelas-numerik-crd-vs-qty-vs-mon-vs-prc-vs-dat-vs-tim)
  - [5.5 Pohon Keputusan: REG vs (NOR, EVT, WOA, PER, FAC, O)](#55-pohon-keputusan-reg-vs-nor-evt-woa-per-fac-o)
- [6. Contoh Anotasi Berjalan Token-demi-Token](#6-contoh-anotasi-berjalan-token-demi-token)
  - [Kasus 1: Berita Politik & Pemerintahan](#kasus-1-berita-politik-pemerintahan)
  - [Kasus 2: Berita Kriminalitas & Penegakan Hukum](#kasus-2-berita-kriminalitas-penegakan-hukum)
  - [Kasus 3: Berita Ekonomi & Finansial](#kasus-3-berita-ekonomi-finansial)
  - [Kasus 4: Berita Keagamaan & Hari Raya](#kasus-4-berita-keagamaan-hari-raya)
  - [Kasus 5: Berita Olahraga Internasional](#kasus-5-berita-olahraga-internasional)
  - [Kasus 6: Berita Hukum, Pengadilan, & Perundang-Undangan](#kasus-6-berita-hukum-pengadilan-perundang-undangan)
  - [Kasus 7: Berita Fasilitas Transportasi & Infrastruktur](#kasus-7-berita-fasilitas-transportasi-infrastruktur)
  - [Kasus 8: Berita Kebudayaan, Karya Seni, & Bahasa](#kasus-8-berita-kebudayaan-karya-seni-bahasa)
- [7. Daftar Uji Kualitas Anotator & 10 Jebakan Fatal](#7-daftar-uji-kualitas-anotator-10-jebakan-fatal)
  - [7.1 Daftar Periksa Mandiri (*Self-Checklist*)](#71-daftar-periksa-mandiri-self-checklist)
  - [7.2 10 Kesalahan Fatal Anotasi (*Top 10 Annotation Pitfalls*)](#72-10-kesalahan-fatal-anotasi-top-10-annotation-pitfalls)
- [8. Panduan Rekayasa Prompt LLM untuk Replikasi Batas NERGRIT](#8-panduan-rekayasa-prompt-llm-untuk-replikasi-batas-nergrit)
  - [8.1 Spesifikasi Meta-Prompt Anotator](#81-spesifikasi-meta-prompt-anotator)
  - [8.2 Format Output Terstruktur (JSON & CoNLL)](#82-format-output-terstruktur-json-conll)
  - [8.3 Few-Shot Demonstrations in Prompt (Contoh Few-Shot LLM)](#83-few-shot-demonstrations-in-prompt-contoh-few-shot-llm)
- [9. Matriks Perbandingan Taksonomi](#9-matriks-perbandingan-taksonomi)

---

## 1. Pendahuluan & Karakteristik Korpus NERGRIT

### 1.1 Profil dan Sejarah Singkat NERGRIT
Korpus **NERGRIT** (*Named Entity Recognition Grit*) merupakan korpus beranotasi entitas bernama bahasa Indonesia multi-kelas terbesar yang dianotasi secara manual oleh annotator manusia. Korpus ini berakar dari kumpulan teks berita daring berbahasa Indonesia yang mencakup berbagai domain (politik, hukum, ekonomi, olahraga, sosial budaya, dan kriminalitas).

Secara komputasional, korpus bersih NERGRIT memiliki karakteristik volume sebagai berikut:
- **Partisi Latih (*Train*)**: 12.514 kalimat | 43.125 rentang entitas.
- **Partisi Validasi (*Validation*)**: 2.520 kalimat | 8.433 rentang entitas.
- **Partisi Uji (*Test*)**: 2.397 kalimat | 8.890 rentang entitas.
- **Total Keseluruhan**: **17.431 kalimat terverifikasi** | **60.448 rentang entitas unik**.

### 1.2 Urgensi Pedoman Baku
Anotasi manual pada korpus NERGRIT dikerjakan oleh annotator manusia dengan seperangkat intuisi linguistik yang konsisten namun memiliki sejumlah deviasi khas dibanding standar annotasi Barat (seperti CoNLL-2003 atau OntoNotes 5.0 murni). Tanpa pedoman tertulis yang komprehensif, annotator manusia baru maupun model kecerdasan buatan (*Large Language Models*) berisiko besar menghasilkan batas token (*boundary*) yang tidak selaras (*misaligned*).

Tujuan pedoman ini adalah mendokumentasikan secara presisi dan deterministik seluruh kaidah sintaksis, perlakuan tanda baca, batas leksikal, serta pohon disambiguasi empiris korpus NERGRIT.

### 1.3 Hubungan Taksonomi: NERGRIT (19 Tag) vs OntoNotes 5.0 (18 Tag)
1. **NERGRIT**: Mengadopsi 18 kelas dengan penamaan yang mirip dengan OntoNotes 5.0, ditambah 1 kelas kustom khusus konteks Indonesia: **`REG` (Religion)**. Selain itu, cakupan `NOR` pada NERGRIT menyerap seluruh lembaga pemerintahan, aparat penegak hukum, dan partai politik.
2. **OntoNotes 5.0**: Memiliki 18 kelas standar internasional (tanpa kelas `REG`). Lembaga negara dan partai politik pada OntoNotes masuk ke `ORGANIZATION`.
3. **Penyelarasan dalam Riset Skripsi**: Pada penelitian evaluasi kinerja model terhadap standar OntoNotes 5.0, kelas `REG` dinormalisasi menjadi label `O` (*Outside*), dan penampung gelar jabatan `TTL` dipetakan kembali ke `O` agar tercipta perbandingan yang adil (*fair evaluation benchmark*).

---

## 2. Alur Kerja Anotasi & Protokol Penandaan BIO

### 2.1 Mekanika Skema Penandaan BIO
Korpus NERGRIT direpresentasikan dalam format urutan token berbasis skema **BIO** (*Beginning, Inside, Outside*):

| Prefix | Nama Lengkap | Definisi Operasional |
| :---: | :--- | :--- |
| **`B-`** | *Beginning* | Diberikan pada **token pertama** yang mengawali sebuah rentang entitas bernama. Jika entitas hanya terdiri dari 1 token, token tersebut tetap diberi awalan `B-`. |
| **`I-`** | *Inside* | Diberikan pada **token kedua dan seterusnya** yang masih berada dalam satu rentang entitas yang sama tanpa terputus. |
| **`O`** | *Outside* | Diberikan pada seluruh token yang **bukan merupakan bagian dari entitas bernama manapun**. |

Format visualisasi rentang entitas:
$$\text{[TAG} \quad \text{Token}_1 \quad \text{Token}_2 \quad \dots \quad \text{Token}_n \quad \text{/TAG]}$$
Diterjemahkan menjadi urutan token BIO:
- $\text{Token}_1 \rightarrow \mathbf{B\text{-}TAG}$
- $\text{Token}_2 \rightarrow \mathbf{I\text{-}TAG}$
- $\dots$
- $\text{Token}_n \rightarrow \mathbf{I\text{-}TAG}$

### 2.2 Aturan Validitas Transisi BIO (*Transition Integrity*)
Agar korpus memiliki integritas struktural yang sempurna tanpa galat parsing (*CoNLL parsing error*), urutan transisi tag wajib mematuhi kaidah formal tata bahasa terbatas (*finite-state automata*):

1. **Kaidah Inisiasi Rentang**:
   - Rentang entitas baru dari kelas `X` **WAJIB** dimulai dengan `B-X`.
   - Transisi langsung dari `O` menuju `I-X` adalah **ILEGAL / CACAT STRUKTURAL**.
2. **Kaidah Kontinuitas Rentang**:
   - Token `I-X` hanya boleh muncul setelah `B-X` atau sesama `I-X`.
   - Transisi dari `B-X` menuju `I-Y` (di mana $X \neq Y$) adalah **ILEGAL**. Jika terjadi pergantian entitas berturutan tanpa jeda kata `O`, token pertama entitas kedua harus diberi tag `B-Y`.
3. **Kaidah Entitas Bertetangga Sejenis**:
   - Jika terdapat dua entitas dari kelas yang sama yang posisinya bersanding langsung tanpa dipisahkan token `O`, entitas kedua **WAJIB** diawali dengan `B-X`, bukan `I-X`.
   - *Contoh*: Frasa nama wilayah `DKI Jakarta` (`B-GPE`, `I-GPE`) disusul nama negara `Indonesia` (`B-GPE`).

```
BENAR:
DKI         B-GPE
Jakarta     I-GPE
Indonesia   B-GPE  <-- Awal entitas GPE baru yang berdekatan

SALAH:
DKI         B-GPE
Jakarta     I-GPE
Indonesia   I-GPE  <-- Dianggap sebagai 1 entitas raksasa yang keliru
```

### 2.3 Nuansa Tokenisasi Bahasa Indonesia & Tanda Baca Lepas
Korpus NERGRIT menerapkan tokenisasi berbasis pemisahan spasi ketat (*whitespace-delimited tokenization*) di mana tanda baca diperlakukan sebagai token mandiri:
1. **Tanda Baca Terpisah (*Detached Punctuation*)**: Koma (`,`), titik akhir kalimat (`.`), tanda petik (`"`, `'`), tanda kurung (`(`, `)`), titik dua (`:`), dan garis miring (`/`) wajib dipisahkan dengan spasi sebelum anotasi.
2. **Titik Singkatan (*Abbreviation Dots*)**: Titik yang melekat pada singkatan gelar atau inisial (`Dr.`, `dr.`, `H.`, `PT.`, `Tbk.`, `A.M.`) diperlakukan sebagai satu kesatuan token utuh bersama huruf singkatannya.
3. **Tanda Hubung (*Hyphen*)**: Tanda hubung pada nomor ordinal (`ke - 4`) atau nama majemuk (`Soekarno - Hatta`) dipisahkan menjadi token mandiri (`ke`, `-`, `4`), namun seluruh token tersebut berada dalam satu rentang BIO yang utuh.

---

## 3. Taksonomi Semantik Komprehensif 19 Kelas Entitas

Di bawah ini adalah definisi operasional, batasan leksikal, serta kriteria inklusi dan eksklusi untuk seluruh 19 kelas entitas korpus NERGRIT:

---

### 3.1 `PER` — Person (Orang)
- **Definisi Semantik**: Nama individu manusia nyata, tokoh sejarah, tokoh fiksi humanoid, inisial nama tokoh, dan nama panggilan unik.
- **Karakteristik Korpus**: Total 9.544 sebutan (3.838 entitas unik). Panjang rata-rata: 1,66 token. Kapitalisasi dominan: Huruf Kapital Kata (*Titlecase* 89,7%).
- **Kriteria Inklusi**:
  - Nama lengkap atau nama panggilan individu: `Joko Widodo`, `Prabowo`, `Sandiaga Uno`, `Aisha Li`.
  - Inisial nama berkarakter formal: `MAZ`, `AS`, `FI`, `RBT`, `A.M. Hendropriyono`.
  - Tokoh fiksi atau mitologis: `Harry Potter`, `Gatotkaca`.
  - **Penyerapan Gelar Melekat**: Gelar akademis dan keagamaan yang melekat langsung di depan nama diserap ke dalam rentang `PER` sebagai token pembuka (`B-PER`): `Dr. Mahathir Mohamad`, `KH Ma'ruf Amin`, `Prof. Dr. Ir. Harijono`, `Habib Salim Segaf Al Jufri`.
- **Kriteria Eksklusi**:
  - Sapaan kekeluargaan/penghormatan umum (`Bapak`, `Ibu`, `Saudara`, `Tuan`, `Ny.`): Diberi label `O`.
  - Gelar jabatan kenegaraan, kepolisian, atau militer (`Presiden`, `Menteri`, `Gubernur`, `Kapolri`, `Jenderal`, `Aiptu`): Diberi label `NOR` atau `O`.
  - Kelompok manusia kolektif atau etnisitas: Diberi label `NOR`.
- **Contoh Valid NERGRIT**:
  1. `[PER Joko Widodo /PER]`
  2. `[PER Dr. Mahathir Mohamad /PER]`
  3. `[PER K.H. Ma'ruf Amin /PER]`
  4. `[PER Sri Mulyani /PER]`
  5. `[PER Dominggus Ngungubulu /PER]`

---

### 3.2 `ORG` — Organization (Organisasi / Korporasi / Klub Olahraga)
- **Definisi Semantik**: Entitas komersial, perusahaan swasta, Badan Usaha Milik Negara (BUMN) yang berbadan hukum perseroan, media pers/portal berita, klub olahraga profesional, institusi pendidikan swasta/yayasan, dan lembaga non-pemerintah (LSM).
- **Karakteristik Korpus**: Total 5.608 sebutan (2.363 entitas unik). Panjang rata-rata: 2,25 token.
- **Kriteria Inklusi**:
  - Korporasi dan badan usaha: `PT Telkom`, `Pertamina`, `Bank Mandiri`, `BTN`, `Apple`, `Proton`.
  - Portal media daring dan surat kabar: `detikcom`, `CNN Indonesia`, `Kompas . com`, `TEMPO`, `Reuters`.
  - Klub dan tim olahraga profesional: `Chelsea`, `Manchester United`, `Persib`, `Persija`.
  - Tim nasional olahraga dalam konteks kompetisi kesebelasan: `Timnas Brasil`, `Jerman` (saat bermain di Piala Dunia).
  - Yayasan amal dan lembaga nirlaba swasta: `Greenpeace`, `Yayasan Lembaga Konsumen Indonesia`.
- **Kriteria Eksklusi**:
  - Lembaga negara, kementerian, badan peradilan, dinas pemerintah, dan komisi negara: Diberi label `NOR` (misal: `KPK`, `KPU`, `DPR`, `Kemenkeu`).
  - Satuan kepolisian dan kesatuan militer: Diberi label `NOR` (misal: `Polri`, `TNI`, `Polda Metro Jaya`).
  - Partai politik dan fraksi parlemen: Diberi label `NOR` (misal: `PKS`, `Gerindra`, `PDIP`).
- **Contoh Valid NERGRIT**:
  1. `[ORG CNN Indonesia /ORG]`
  2. `[ORG Bank Mandiri /ORG]`
  3. `[ORG Chelsea /ORG]`
  4. `[ORG detikcom /ORG]`
  5. `[ORG PT . Kereta Api Indonesia /ORG]`

---

### 3.3 `GPE` — Geo-Political Entity (Wilayah Geopolitik Administratif)
- **Definisi Semantik**: Wilayah geografis yang memiliki batas administratif formal yang diakui hukum, memiliki pemerintahan resmi, dan dihuni oleh warga masyarakat.
- **Karakteristik Korpus**: Total 9.115 sebutan (2.096 entitas unik). Panjang rata-rata: 1,35 token.
- **Kriteria Inklusi**:
  - Nama negara berdaulat: `Indonesia`, `Malaysia`, `Turki`, `Amerika Serikat`, `China`.
  - Nama provinsi/negara bagian: `Jawa Timur`, `DKI Jakarta`, `Jawa Barat`, `Sulawesi Selatan`, `Bali`.
  - Nama kota, kabupaten, dan wilayah administratif tingkat dua: `Surabaya`, `Bandung`, `Denpasar`, `Kabupaten Sinjai`, `Solo`.
  - Wilayah kecamatan dan desa administratif resmi: `Seminyak`, `Kuta`, `Cangkreng`.
- **Kriteria Eksklusi**:
  - Preposisi penunjuk lokasi (`di`, `ke`, `dari`, `menuju`): **WAJIB DIEKSKLUSI** (berstatus `O`).
  - Bentang alam non-administratif (gunung, sungai, danau, laut, pantai): Diberi label `LOC`.
  - Bangunan fisik infrastruktur atau gedung pemerintahan: Diberi label `FAC`.
  - Nama jalan raya dan koridor lalu lintas: Diberi label `LOC`.
- **Contoh Valid NERGRIT**:
  1. `di [GPE Jakarta /GPE]` $\rightarrow$ `di` berstatus `O`
  2. `[GPE Jawa Timur /GPE]`
  3. `pemerintah [GPE Turki /GPE]`
  4. `[GPE Kota Pahlawan /GPE]` (julukan resmi geopolitik Surabaya)
  5. `[GPE Kabupaten Karanganyar /GPE]`

---

### 3.4 `LOC` — Location (Lokasi Non-Geopolitik / Bentang Alam / Jalan)
- **Definisi Semantik**: Tempat fisik di permukaan bumi yang tidak memiliki struktur batas pemerintahan administratif resmi, mencakup bentang alam alami, koridor jalan raya, perairan, ruang terbuka publik (taman/alun-alun), dan kawasan regional benua.
- **Karakteristik Korpus**: Total 3.500 sebutan (2.245 entitas unik). Panjang rata-rata: 2,59 token.
- **Kriteria Inklusi**:
  - Bentang alam alami beserta kata jenisnya: `Gunung Agung`, `Danau Toba`, `Laut Cina Selatan`, `Pantai Kuta`.
  - Koridor jalan raya dan alamat lalu lintas: `Jalan Kayu Cendana`, `Jl . Sudirman`, `Jalan Ahmad Yani`, `Bourke Street`.
  - Kawasan regional, kawasan geopolitik tanpa pemerintahan tunggal, dan benua: `Asia Tenggara`, `Timur Tengah`, `Eropa Barat`.
  - Ruang terbuka publik dan taman non-fasilitas tertutup: `Taman Fatahillah`, `Monas`, `kawasan Kota Tua Jakarta`.
- **Kriteria Eksklusi**:
  - Preposisi lokasi (`di`, `ke`, `dari`): **WAJIB DIEKSKLUSI** (`O`).
  - Bangunan tertutup, gedung, stasiun, terminal, dan bandara: Diberi label `FAC`.
  - Wilayah desa/kota/provinsi berpemerintahan: Diberi label `GPE`.
- **Contoh Valid NERGRIT**:
  1. `ke [LOC Gunung Agung /LOC]` $\rightarrow$ `ke` berstatus `O`
  2. `di [LOC Jalan Kayu Cendana /LOC]` $\rightarrow$ `di` berstatus `O`
  3. `[LOC Danau Toba /LOC]`
  4. `[LOC Pantai Kuta /LOC]`
  5. `[LOC Taman Fatahillah /LOC]`

---

### 3.5 `FAC` — Facility (Fasilitas Infrastruktur Fisik Buatan)
- **Definisi Semantik**: Struktur bangunan, prasarana fisik buatan manusia, infrastruktur transportasi, gedung olahraga, aula, utilitas, atau kompleks perkantoran fisik.
- **Karakteristik Korpus**: Total 624 sebutan (394 entitas unik). Panjang rata-rata: 2,96 token.
- **Kriteria Inklusi**:
  - Bandara dan pelabuhan transportasi: `Bandara Soekarno - Hatta`, `Bandara International Minangkabau`, `Pelabuhan Bakauheni`.
  - Terminal bus dan stasiun kereta: `Terminal Bus Tanjung Priok`, `Stasiun Gambir`.
  - Stadion olahraga dan arena pertunjukan: `Stadion Gelora Bung Karno`, `GBK`.
  - Bangunan fisik dan aula pertemuan: `Balai Kota`, `Aula Mapolresta Solo`, `Lembaga Pemasyarakatan ( LP ) Salemba`, `ruang paripurna DPRD`.
  - Infrastruktur jalan tol dan utilitas buatan: `Tol Cipali`, `PLTA Waduk Cirata`, `WC`.
- **Kriteria Eksklusi**:
  - Koridor jalan raya biasa tanpa tol (`Jalan Sudirman`): Diberi label `LOC`.
  - Lembaga atau badan hukum yang menempati fasilitas tersebut: Diberi label `NOR` atau `ORG`.
  - Tempat ibadah formal (`Masjid`, `Gereja`, `Surau`): Diberi label `REG` dalam korpus NERGRIT.
- **Contoh Valid NERGRIT**:
  1. `[FAC Bandara Soekarno - Hatta /FAC]`
  2. `[FAC Stadion Gelora Bung Karno /FAC]`
  3. `[FAC Terminal Bus Tanjung Priok /FAC]`
  4. `[FAC PLTA Waduk Cirata /FAC]`
  5. `[FAC Lembaga Pemasyarakatan ( LP ) Salemba /FAC]`

---

### 3.6 `EVT` — Event (Peristiwa / Ajang / Bencana)
- **Definisi Semantik**: Peristiwa terikat waktu dan sejarah yang memiliki nama spesifik, ajang olahraga, festival budaya, konferensi, operasi pengamanan militer/polisi, krisis bersejarah, atau insiden bencana bernama.
- **Karakteristik Korpus**: Total 1.788 sebutan (847 entitas unik). Panjang rata-rata: 2,64 token.
- **Kriteria Inklusi**:
  - Ajang kejuaraan dan turnamen olahraga: `Piala Dunia 2018`, `Asian Games`, `Copa Ramadhan`.
  - Operasi resmi kepolisian/keamanan: `Operasi Ketupat 2018`.
  - Peristiwa bersejarah dan insiden tragis spesifik: `tragedi Bourke Street`, `kudeta yang gagal tahun 2016`.
  - Festival budaya, konferensi, dan pameran: `Festival Lampion`, `G20 Summit`.
- **Kriteria Eksklusi**:
  - Tanda petik yang mengapit nama acara: Diberi label `O`.
  - Hari raya dan ritual peribadatan keagamaan formal (`Idul Fitri`, `Waisak`, `Natal`, `Lebaran`): Diberi label `REG` dalam NERGRIT.
- **Contoh Valid NERGRIT**:
  1. `[EVT Piala Dunia 2018 /EVT]`
  2. `[EVT Asian Games /EVT]`
  3. `[EVT Operasi Ketupat 2018 /EVT]`
  4. `[EVT tragedi Bourke Street /EVT]`
  5. `[EVT Copa Ramadhan /EVT]`

---

### 3.7 `WOA` — Work of Art (Karya Seni & Cipta Intelektual)
- **Definisi Semantik**: Judul karya cipta manusia berwujud buku sastra, judul film, lagu, album musik, program radio/televisi, karya lukis, patung seni, atau kolom reguler media.
- **Karakteristik Korpus**: Total 208 sebutan (142 entitas unik). Panjang rata-rata: 2,86 token.
- **Kriteria Inklusi**:
  - Judul film dan sinematografi: `The Dark Knight`, `Dilan 1990`.
  - Judul buku, novel, dan publikasi sastra: `Laskar Pelangi`, `Bumi Manusia`.
  - Judul lagu dan album musik: `Indonesia Raya`, `Bohemian Rhapsody`.
  - Judul acara televisi dan sandiwara: `Mata Najwa`, `Si Doel Anak Sekolahan`.
- **Kriteria Eksklusi**:
  - Tanda petik tunggal atau ganda di sekitar judul (`"..."` atau `'...'`): **SELALU DIEKSKLUSI** (berstatus `O`).
  - Kitab suci agama (`Alquran`, `Injil`, `Taurat`): Diberi label `REG` dalam korpus NERGRIT.
  - Nama dokumen perundang-undangan resmi: Diberi label `LAW`.
- **Contoh Valid NERGRIT**:
  1. `film " [WOA The Dark Knight /WOA] "` $\rightarrow$ tanda petik berstatus `O`
  2. `lagu [WOA Indonesia Raya /WOA]`
  3. `buku [WOA Laskar Pelangi /WOA]`
  4. `program [WOA Mata Najwa /WOA]`

---

### 3.8 `LAW` — Law (Hukum / Perundang-Undangan / Traktat)
- **Definisi Semantik**: Dokumen hukum berkekuatan formal, peraturan perundang-undangan pemerintah, kitab hukum, peraturan menteri, perjanjian/traktat internasional, atau pasal perundangan tertentu.
- **Karakteristik Korpus**: Total 445 sebutan (299 entitas unik). Panjang rata-rata: 5,37 token (maksimal 87 token).
- **Kriteria Inklusi**:
  - Undang-undang nasional beserta nomor dan tahunnya: `Undang - Undang No . 11 Tahun 2008`, `Undang - Undang Dasar 1945`.
  - Undang-undang asing atau traktat internasional: `Undang - undang Rahasia Negara Myanmar ( Official Secrets Act )`.
  - Kitab hukum dan peraturan pemerintah: `KUHP`, `KUHAP`, `Perpres Nomor 20 Tahun 2018`.
- **Kriteria Eksklusi**:
  - Hukum syariat agama atau dogma moral (`rukun Islam`, `syariat Islam`): Diberi label `REG` atau `O`.
  - Tanda hubung pada kata `Undang - Undang`: Diserap ke dalam `LAW` sebagai `I-LAW`.
- **Contoh Valid NERGRIT**:
  1. `[LAW Undang - undang Rahasia Negara Myanmar ( Official Secrets Act ) /LAW]`
  2. `[LAW KUHP /LAW]`
  3. `[LAW Undang - Undang Nomor 5 Tahun 2018 /LAW]`
  4. `[LAW UUD 1945 /LAW]`

---

### 3.9 `PRD` — Product (Produk / Komoditas Fisik / Sarana Transportasi)
- **Definisi Semantik**: Barang komersial berwujud, produk industri bermerek, sarana moda transportasi (kendaraan bermotor, pesawat, kapal), komoditas perdagangan fisik pangan/energi, zat kimia/narkotika terlarang, alat perlengkapan, serta indeks pasar modal.
- **Karakteristik Korpus**: Total 5.833 sebutan (2.637 entitas unik). Panjang rata-rata: 1,98 token.
- **Kriteria Inklusi (Termasuk Kata Benda Huruf Kecil Empiris NERGRIT)**:
  - Seluruh sarana moda transportasi fisik: `mobil`, `sepeda motor`, `truk`, `bus`, `pesawat`, `kapal`.
  - Komoditas pangan, perkebunan, dan energi: `beras`, `kopi`, `rendang`, `semur daging`, `daging`, `gemitir`, `BBM`, `minyak`.
  - Zat kimia, obat-obatan, dan narkotika: `sabu`.
  - Alat, busana, dan perlengkapan fisik: `helm`, `jaket`, `sulaman tangan`.
  - Gadget elektronik dan peranti keras bermerek: `iPhone`, `Galaxy S9`, `Boeing 737`.
  - Indeks pasar modal dan finansial: `IHSG`.
  - Aplikasi perangkat lunak/platform digital saat merujuk pada produk/aplikasi: `Twitter`, `Facebook`, `Instagram`.
- **Kriteria Eksklusi**:
  - Korporasi produsen pembuat produk (`Apple Inc.`, `Samsung Electronics`): Diberi label `ORG`.
  - Jasa pelayanan non-fisik: Diberi label `O`.
- **Contoh Valid NERGRIT**:
  1. `[PRD mobil /PRD]`
  2. `[PRD sepeda motor /PRD]`
  3. `[PRD sabu /PRD]`
  4. `[PRD helm /PRD]`
  5. `[PRD IHSG /PRD]`
  6. `[PRD Beras /PRD]`

---

### 3.10 `LAN` — Language (Bahasa)
- **Definisi Semantik**: Nama bahasa alami manusia yang digunakan dalam komunikasi lisan maupun tulisan.
- **Karakteristik Korpus**: Sangat langka di korpus NERGRIT (total 13 sebutan, 9 unik). Panjang rata-rata: 1,92 token.
- **Kriteria Inklusi**:
  - Frasa bahasa alami: `bahasa Arab`, `bahasa Indonesia`, `bahasa Inggris`, `bahasa Mandarin`.
  - Kata benda bahasa tanpa prefiks `bahasa` jika konteksnya merujuk pada sistem bahasa: `Arab` (dalam kalimat *"pelajaran bahasa Arab dan Al Quran"*).
- **Kriteria Eksklusi**:
  - Nama negara atau wilayah tempat bahasa dituturkan (`Arab Saudi`): Diberi label `GPE`.
  - Etnisitas atau warga negara (`orang Arab`): Diberi label `NOR`.
- **Contoh Valid NERGRIT**:
  1. `[LAN bahasa Arab /LAN]`
  2. `[LAN bahasa Indonesia /LAN]`
  3. `[LAN bahasa Inggris /LAN]`

---

### 3.11 `DAT` — Date (Tanggal / Hari / Bulan / Tahun / Kalender)
- **Definisi Semantik**: Penanda titik waktu penanggalan spesifik pada kalender Masehi/Hijriah, nama hari, nama bulan, angka tahun, dan format stempel tanggal khas kepala berita.
- **Karakteristik Korpus**: Total 5.232 sebutan (1.754 entitas unik). Panjang rata-rata: 3,60 token.
- **Kriteria Inklusi**:
  - Tanggal kalender lengkap: `15 Mei 2018`, `29 Mei`, `14 - 16 Juni 2018`.
  - Nama hari tunggal: `Senin`, `Selasa`, `Rabu`, `Jumat`.
  - Angka tahun tunggal: `2018`, `2017`, `2016`, `1802 Masehi`.
  - Penanda relatif hari: `hari ini`, `kemarin`, `besok`.
  - **Kaidah Khusus Tanggal Berita dalam Kurung**: Format berita daring `Hari ( DD / MM / YYYY )` dianotasi sebagai **SATU SPAN UTUH `DAT`** mencakup tanda kurung buka dan tutupnya. Bukti empiris: 1.356 entitas `DAT` di NERGRIT berakhir dengan token `)`.
- **Kriteria Eksklusi**:
  - Preposisi temporal (`pada`, `dalam`, `sejak`, `hingga`): **WAJIB DIEKSKLUSI** (`O`).
  - Durasi atau rentang waktu lampau (`selama dua tahun`, `36 hari`): Diberi label `QTY`.
  - Jam dan penunjuk waktu pukul (`06 . 00 WIB`): Diberi label `TIM`.
- **Contoh Valid NERGRIT**:
  1. `[DAT Selasa ( 15 / 5 / 2018 ) /DAT]`
  2. `[DAT Senin ( 30 / 1 / 2017 ) /DAT]`
  3. `[DAT 15 Mei 2018 /DAT]`
  4. `[DAT 2018 /DAT]`
  5. `pada [DAT 21 Mei 2018 /DAT]` $\rightarrow$ `pada` berstatus `O`

---

### 3.12 `TIM` — Time (Waktu Jam / Pukul)
- **Definisi Semantik**: Penanda titik waktu spesifik dalam siklus 24 jam sehari, jam dinding, pembacaan arloji, beserta penanda zona waktu (*WIB, WITA, WIT, GMT*).
- **Karakteristik Korpus**: Total 1.060 sebutan (731 entitas unik). Panjang rata-rata: 3,87 token.
- **Kriteria Inklusi**:
  - Jam berskala titik atau titik dua: `06 . 00 WIB`, `pukul 10 . 30 Wita`, `sekira pukul 18 . 00 WIB`, `17 : 00 WIB`.
  - Penanda siang/malam spesifik bila merujuk pada jam: `pukul 12 . 00 siang`.
- **Kriteria Eksklusi**:
  - Durasi rentang waktu (`selama 24 jam`, `30 menit`): Diberi label `QTY`.
  - Kata keterangan waktu umum tanpa jam spesifik (`pagi tadi`, `malam nanti`): Berstatus `O` atau diserap tergantung konteks kepala berita.
- **Contoh Valid NERGRIT**:
  1. `[TIM pukul 10 . 30 Wita /TIM]`
  2. `[TIM 06 . 00 - 11 . 00 WIB /TIM]`
  3. `[TIM sekira pukul 18 . 00 WIB /TIM]`
  4. `[TIM 17 : 00 WIB /TIM]`

---

### 3.13 `MON` — Money (Nominal Moneter & Valuta)
- **Definisi Semantik**: Nilai nominal uang, harga, pagu anggaran, denda finansial, atau nilai valuta asing beserta simbol mata uang atau kata satuan moneternya.
- **Karakteristik Korpus**: Total 1.719 sebutan (1.029 entitas unik). Panjang rata-rata: 3,46 token.
- **Kriteria Inklusi**:
  - Simbol mata uang disusul angka: `Rp 40 Ribu`, `Rp 3 , 6 miliar`, `Rp 4 , 2 miliar`, `US$ 50 juta`.
  - Angka nominal disusul kata mata uang: `100 triliun rupiah`, `500 dollar AS`.
  - Angka pecahan desimal moneter: `Rp 1 . 500 , 50`.
- **Kriteria Eksklusi**:
  - Angka murni tanpa simbol mata uang: Diberi label `CRD`.
  - Nilai persentase bunga finansial (`10 %`): Diberi label `PRC`.
- **Contoh Valid NERGRIT**:
  1. `[MON Rp 40 Ribu /MON]`
  2. `[MON Rp 3 , 6 miliar /MON]`
  3. `[MON 100 triliun rupiah /MON]`
  4. `[MON US$ 50 juta /MON]`

---

### 3.14 `QTY` — Quantity (Kuantitas Fisik & Durasi Waktu)
- **Definisi Semantik**: Pengukuran besaran fisik terukur (bobot, panjang/jarak, luas, volume, kapasitas) DAN **durasi atau rentang waktu lampau/jangka**.
- **Karakteristik Korpus**: Total 2.081 sebutan (1.236 entitas unik). Panjang rata-rata: 2,57 token.
- **Kriteria Inklusi (Kaidah Durasi Khas NERGRIT)**:
  - Besaran fisik dan satuan metrik: `41 . 227 ton`, `15 kilogram`, `1 . 700 cm`, `50 meter`, `10 km`.
  - **Durasi Waktu / Jangka Waktu Lampau**: `dua tahun`, `dua tahun lebih`, `tiga bulan`, `24 jam`, `30 menit`, `dua hari`, `setahun`, `36 hari`, `dua abad`, `10 hari lalu`.
- **Kriteria Eksklusi**:
  - Titik penanggalan kalender (`15 Mei 2018`): Diberi label `DAT`.
  - Titik jam spesifik (`06 . 00 WIB`): Diberi label `TIM`.
  - Angka pembilang tanpa satuan: Diberi label `CRD`.
- **Contoh Valid NERGRIT**:
  1. `[QTY 41 . 227 ton /QTY]`
  2. `[QTY 15 kilogram /QTY]`
  3. `[QTY selama dua tahun lebih /QTY]` atau `[QTY dua tahun /QTY]`
  4. `[QTY 36 hari /QTY]`
  5. `[QTY 24 jam /QTY]`
  6. `[QTY dua abad /QTY]`

---

### 3.15 `CRD` — Cardinal (Bilangan Kardinal Murni)
- **Definisi Semantik**: Bilangan bulat atau pecahan yang menunjukkan jumlah atau kuantitas cacah murni tanpa terikat langsung pada satuan metrik fisik, simbol uang, atau persen.
- **Karakteristik Korpus**: Total 5.617 sebutan (1.422 entitas unik). Panjang rata-rata: 1,40 token.
- **Kriteria Inklusi**:
  - Angka cacah numerik: `1`, `2`, `3`, `41`, `115`, `1 . 000`, `6 . 583`.
  - Kata bilangan tekstual: `satu`, `dua`, `tiga`, `empat`, `ratusan`.
  - Bilangan yang mendahului nomina orang/benda: `tiga orang`, `tiga gereja`, `dua wartawan`, `dua menteri`.
  - Kata rujukan kembar: `kedua`, `Keduanya` (saat bermakna *"both of them"*, bukan nomor urut).
- **Kriteria Eksklusi**:
  - Nomor urut/peringkat (`pertama`, `ke - 4`): Diberi label `ORD`.
  - Nilai uang (`Rp 1.000`): Diberi label `MON`.
  - Angka tahun (`2018`): Diberi label `DAT`.
- **Contoh Valid NERGRIT**:
  1. `[CRD tiga /CRD] orang`
  2. `[CRD 115 /CRD] bus`
  3. `[CRD dua /CRD] sindikat`
  4. `[CRD Keduanya /CRD] shalat Jumat`
  5. `[CRD 1 . 000 /CRD] Anak Yatim`

---

### 3.16 `ORD` — Ordinal (Bilangan Tingkat / Urutan)
- **Definisi Semantik**: Bilangan atau kata penunjuk peringkat, hierarki, tahapan urutan, atau posisi relatif dalam sebuah sekuens.
- **Karakteristik Korpus**: Total 817 sebutan (106 entitas unik). Panjang rata-rata: 1,06 token.
- **Kriteria Inklusi**:
  - Kata urutan tekstual: `pertama`, `kedua`, `ketiga`, `terakhir`, `kesekian`.
  - Nomor ordinal berpola prefiks `ke`: `ke - 4`, `ke - 6`, `ke - 12`, `ke 58`.
  - **Kaidah Batas Eksklusif**: Prefiks `ke` dan tanda hubung `-` **WAJIB DIINKLUSI** ke dalam span `ORD` (`B-ORD` pada `ke`, `I-ORD` pada `-`, `I-ORD` pada angka).
- **Kriteria Eksklusi**:
  - Kata `kedua` saat bermakna kata ganti *"both"* (kedua belah pihak): Diberi label `CRD`.
  - Preposisi penunjuk arah `ke` (seperti `ke Bandung`): Berstatus `O`.
- **Contoh Valid NERGRIT**:
  1. `korban tewas [ORD ke - 6 /ORD]`
  2. `pelopor [ORD pertama /ORD]`
  3. `generasi [ORD kesekian /ORD]`
  4. `peringkat [ORD ke - 4 /ORD]`

---

### 3.17 `PRC` — Percent (Persentase & Kadar)
- **Definisi Semantik**: Nilai proporsi per seratus, rasio persentase, atau kadar konsentrasi beserta simbol persen (`%`) atau kata `"persen"`.
- **Karakteristik Korpus**: Total 1.139 sebutan (593 entitas unik). Panjang rata-rata: 2,97 token.
- **Kriteria Inklusi**:
  - Angka desimal disusul simbol `%`: `10 %`, `2 , 5 %`, `0 , 75 %`.
  - Angka disusul kata tekstual: `50 persen`, `tiga puluh persen`.
- **Kriteria Eksklusi**:
  - Angka rasio tanpa satuan persen: Diberi label `CRD`.
- **Contoh Valid NERGRIT**:
  1. `[PRC 10 % /PRC]`
  2. `[PRC 50 persen /PRC]`
  3. `[PRC 2 , 5 % /PRC]`
  4. `turun [PRC 17 persen /PRC]`

---

### 3.18 `NOR` — NORP (Organisasi Negara, Aparat, Parpol, & Demografi)
- **Definisi Semantik**: Kategori gabungan yang sangat unik di NERGRIT: mencakup institusi kementerian dan lembaga tinggi negara, aparat kepolisian dan militer, partai politik, pejabat kenegaraan formal, serta kelompok kebangsaan/demografi.
- **Karakteristik Korpus**: Total 5.651 sebutan (2.352 entitas unik). Panjang rata-rata: 2,45 token.
- **Kriteria Inklusi**:
  - Aparat kepolisian dan militer nasional: `polisi`, `Polri`, `kepolisian`, `TNI`, `Polda Metro Jaya`, `Polres Purwakarta`, `Tim Polsek Kuta`, `Satreskrim`, `Kepolisian Victoria`, `Bataliyon aksi cepat`.
  - Lembaga tinggi negara, kementerian, dan komisi negara: `KPK`, `DPR`, `KPU`, `BMKG`, `pemerintah`, `pemkab`, `Pemerintah Provinsi DKI Jakarta`, `Dewan Perwakilan Rakyat Daerah ( DPRD ) Kabupaten Karanganyar`.
  - Partai politik dan fraksi legislatif: `PKS`, `Gerindra`, `Demokrat`, `PDIP`, `Golkar`.
  - Organisasi antarpemerintah dunia: `PBB`, `WHO`, `CBF`.
  - Jabatan dan kepangkatan kenegaraan/militer resmi: `Presiden`, `Menteri`, `Gubernur DKI Jakarta`, `Kapolri`, `Kasat Lantas Polres Sarolangun`, `Komisaris Jenderal Polisi`, `Direktur Kriminal Khusus Polda Bali`, `Aiptu`.
  - Kelompok kebangsaan dan kewarganegaraan: `warga negara Malaysia`, `Cina` (dalam konteks polisi Cina).
- **Kriteria Eksklusi**:
  - Perusahaan swasta, BUMN korporasi, dan klub olahraga: Diberi label `ORG`.
  - Tempat ibadah dan penganut agama: Diberi label `REG`.
  - Nama orang yang menjabat: Diberi label `PER`.
- **Contoh Valid NERGRIT**:
  1. `[NOR KPK /NOR]`
  2. `[NOR Polda Metro Jaya /NOR]`
  3. `[NOR Presiden /NOR] [PER Joko Widodo /PER]`
  4. `[NOR PKS /NOR]`
  5. `[NOR Dewan Perwakilan Rakyat Daerah ( DPRD ) Kabupaten Karanganyar /NOR]`
  6. `[NOR Kapolresta Solo /NOR]`

---

### 3.19 `REG` — Religion (Agama, Penganut, Hari Raya, & Ritual)
- **Definisi Semantik**: Entitas kustom khas NERGRIT yang memayungi seluruh konsep keagamaan: nama agama formal, penganut agama, hari raya/musim ibadah, kitab suci, tempat ibadah umum, istilah ibadah/doa, sebutan Tuhan/nabi, dan seruan keagamaan.
- **Karakteristik Korpus**: Total 454 sebutan (141 entitas unik). Panjang rata-rata: 1,50 token.
- **Kriteria Inklusi**:
  - Agama formal: `Islam`, `Kristen`, `Katolik`, `Hindu`, `Buddha`, `Konghucu`, `Yahudi`, `Sunda Wiwitan`.
  - Penganut dan umat beragama: `Muslim`, `muslim`, `umat Islam`, `Kristiani`, `umat Hindu`, `Muslim Rohingya`.
  - Hari raya dan bulan ibadah: `Ramadan`, `Ramadhan`, `Lebaran`, `Idul Fitri`, `Hari Raya Waisak`, `Galungan`, `Natal`.
  - Kitab suci dan bagiannya: `Alquran`, `Al Quran`, `Al - Qur ' an`, `Injil`, `Taurat`, `juz`.
  - Sebutan Tuhan dan figur suci: `Allah SWT`, `Allah`, `Tuhan`, `Nabi Muhammad SAW`, `Rasulullah`, `sang Budha`.
  - Aktivitas ibadah dan ritus keagamaan: `puasa`, `sholat`, `sholat tarawih`, `salat Maghrib berjamaah`, `Buka Puasa`, `takbiran`, `misa`, `shalat Jumat`, `tausiyah`, `azan`.
  - Tempat peribadatan umum: `masjid`, `Masjid`, `Gereja`, `Surau`, `musala`.
  - Gelar rohaniwan keagamaan: `ulama`, `ustaz`, `pendeta`, `kyai`.
  - Ungkapan doa dan seruan keagamaan: `Insya Allah`, `insyaallah`, `Alhamdulillah`, `Astaghfirullah`, `kalimat hauqalah`, `Laa Haula Wa Laa Quwwata Illa Billaah`.
- **Kriteria Eksklusi**:
  - Yayasan dakwah komersial berbadan hukum: Diberi label `ORG`.
  - Nama pribadi tokoh rohaniwan: Diberi label `PER` (misal: `[PER Ustaz Abdul Somad /PER]`).
- **Contoh Valid NERGRIT**:
  1. `[REG Ramadan /REG]`
  2. `[REG Idul Fitri /REG]`
  3. `[REG Alquran /REG]`
  4. `[REG Insya Allah /REG]`
  5. `[REG masjid /REG]`
  6. `[REG Allah SWT /REG]`

---

## 4. Kaidah Emas Penentuan Batas Rentang Entitas

Audit komputasional mendalam terhadap 60.448 rentang entitas acuan manusia NERGRIT menetapkan 7 kaidah emas (*Golden Boundary Rules*) berikut:

```
+=============================================================================+
|                      7 KAIDAH EMAS BATAS NERGRIT                            |
+=============================================================================+
| 1. Preposisi Spasial & Temporal (di, ke, dari, pada) SELALU O (99,99%).     |
| 2. Sapaan Umum (Bapak, Ibu) = O; Gelar Akademik/Agama (Dr., KH) = B-PER;   |
|    Jabatan Resmi Kenegaraan (Presiden, Gubernur, Kapolri) = NOR.            |
| 3. Format Berita "Hari ( DD / MM / YYYY )" = 1 SPAN UTUH DAT (+ kurung).    |
| 4. Komoditas & Sarana Transportasi Huruf Kecil (mobil, sabu, kopi) = PRD.   |
| 5. Durasi Waktu Lampau/Jangka (dua tahun, 24 jam, 30 menit) = QTY.          |
| 6. Tanda Petik ("...", '...') Mengapit Judul/Ajang DIEKSKLUSI = O.          |
| 7. Tanda Hubung (-) pada Ordinal (ke - 4) & Hukum (Undang - Undang) = I-TAG.|
+=============================================================================+
```

### 4.1 Eksklusi Preposisi Spasial & Temporal (99,99% Aturan Preposisi)
- **Kaidah Mutlak**: Kata depan penunjuk tempat (`di`, `ke`, `dari`, `menuju`) dan penunjuk waktu (`pada`, `dalam`, `selama`, `sejak`, `hingga`, `sampai`) **SELALU BERSTATUS `O`** dan tidak pernah dimasukkan ke dalam rentang entitas.
- **Tingkat Kepatuhan Empiris**:
  - `di [GPE Jakarta /GPE]` $\rightarrow$ `di` (O), `Jakarta` (B-GPE).
  - `ke [LOC Gunung Agung /LOC]` $\rightarrow$ `ke` (O), `Gunung` (B-LOC), `Agung` (I-LOC).
  - `pada [DAT 15 Mei 2018 /DAT]` $\rightarrow$ `pada` (O), `15` (B-DAT), `Mei` (I-DAT), `2018` (I-DAT).
- **Satu-satunya Pengecualian**: Kata `ke` **HANYA INKLUSIF** apabila berfungsi sebagai prefiks pembentuk bilangan bertingkat ordinal `ORD` (`ke - 4`, `ke 58`).

### 4.2 Perlakuan Gelar, Sapaan Kehormatan, dan Jabatan Formal
Korpus manusia NERGRIT memisahkan perlakuan sapaan ke dalam 3 hierarki sintaksis:
1. **Sapaan Kehormatan Kekerabatan (`Bapak`, `Ibu`, `Saudara`, `Tuan`, `Nona`)**:
   - Status: **100% DIEKSKLUSI** dari `PER` (berstatus `O`).
   - Contoh: `Bapak [PER Joko Widodo /PER]`, `Ibu [PER Iriana /PER]`.
2. **Gelar Akademis & Keagamaan Melekat (`Dr.`, `dr.`, `Prof.`, `Ir.`, `K.H.`, `Habib`, `Ustadz`)**:
   - Status: **DISERAP KE DALAM `PER`** sebagai token `B-PER`.
   - Contoh: `[PER Dr. Mahathir Mohamad /PER]`, `[PER K.H. Ma'ruf Amin /PER]`, `[PER Habib Salim Segaf Al Jufri /PER]`.
3. **Jabatan Kenegaraan, Kepolisian, dan Militer (`Presiden`, `Menteri`, `Gubernur`, `Kapolri`, `Jenderal`, `Aiptu`)**:
   - Status: **DILABELI SEBAGAI `NOR`**, TIDAK diserap ke dalam `PER`.
   - Contoh: `[NOR Presiden /NOR] [PER Joko Widodo /PER]`, `[NOR Menteri Keuangan /NOR] [PER Sri Mulyani /PER]`, `[NOR Gubernur DKI Jakarta /NOR] [PER Anies Baswedan /PER]`.

### 4.3 Tanda Kurung Tanggal Kepala Berita pada `DAT`
- **Fenomena Berita Daring**: Wartawan media daring Indonesia kerap menuliskan format penanggalan kepala berita berupa `Hari ( DD / MM / YYYY )`.
- **Kaidah NERGRIT**: Seluruh blok tanggal beserta tanda kurung buka `(` dan tutup `)` dianotasi sebagai **SATU SPAN UTUH `DAT`**.
- **Bukti Empiris**: Sebanyak 1.356 entitas `DAT` di korpus acuan berakhiran token `)`.
  - Contoh: `[DAT Selasa ( 15 / 5 / 2018 ) /DAT]`, `[DAT Senin ( 30 / 1 / 2017 ) /DAT]`, `[DAT Rabu ( 16 / 5 ) /DAT]`.

### 4.4 Inklusi Kata Benda Umum Huruf Kecil pada `PRD`
- **Deviasi dari Standar Barat**: Berbeda dari standar CoNLL atau OntoNotes yang mensyaratkan produk berupa nama diri (*proper noun* bermerek seperti *iPhone* atau *Boeing*), annotator manusia NERGRIT secara konsisten melabeli **kata benda umum huruf kecil (*common lowercase nouns*)** untuk kendaraan dan komoditas.
- **Kategori yang Wajib Dilabeli `PRD`**:
  - Kendaraan: `mobil`, `sepeda motor`, `truk`, `bus`, `pesawat`, `kapal`.
  - Komoditas pangan/energi: `beras`, `kopi`, `rendang`, `semur daging`, `daging`, `BBM`, `minyak`.
  - Narkotika & bahan sitaan: `sabu`.
  - Perlengkapan: `helm`, `jaket`.

### 4.5 Klasifikasi Durasi Waktu Lampau/Jangka ke dalam `QTY`
- **Distingsi Kritis**:
  - OntoNotes 5.0 memasukkan durasi waktu $\ge 24$ jam ke dalam `DATE` dan $< 24$ jam ke dalam `TIME`.
  - **NERGRIT**: Seluruh durasi waktu lampau, jangka waktu, atau satuan rentang waktu **WAJIB DILABELI `QTY`**.
- **Contoh Baku**:
  - `selama [QTY dua tahun /QTY]`
  - `dalam waktu [QTY 24 jam /QTY]`
  - `selama [QTY 36 hari /QTY]`
  - `kurun waktu [QTY 30 menit /QTY]`
  - `usia lebih [QTY dua abad /QTY]`

### 4.6 Eksklusi Tanda Petik Ganda/Tunggal pada `WOA` dan `EVT`
- **Kaidah Batas Tanda Petik**: Apabila judul lagu, buku, film, atau nama sandi peristiwa diapit tanda petik (`"..."` atau `'...'`), tanda petik tersebut **SELALU BERSTATUS `O`**.
- **Contoh**:
  - `film " [WOA The Dark Knight /WOA] "` $\rightarrow$ Tanda petik di luar span.
  - `lagu ' [WOA Indonesia Raya /WOA] '` $\rightarrow$ Tanda petik di luar span.
  - `bertulisan ' [O Rahasia Negara /O] '` $\rightarrow$ Tanda petik di luar span.

### 4.7 Penanganan Tanda Hubung (*Hyphenation*) & Reduplikasi
- **Tanda Hubung Ordinal**: `ke - 4` $\rightarrow$ `ke` (`B-ORD`), `-` (`I-ORD`), `4` (`I-ORD`).
- **Tanda Hubung Reduplikasi Hukum**: `Undang - Undang` $\rightarrow$ `Undang` (`B-LAW`), `-` (`I-LAW`), `Undang` (`I-LAW`).
- **Tanda Hubung Nama Majemuk Fasilitas/Lokasi**: `Soekarno - Hatta` $\rightarrow$ `Soekarno` (`B-FAC`), `-` (`I-FAC`), `Hatta` (`I-FAC`).
- **Tanda Hubung Produk**: `e - KTP` $\rightarrow$ `e` (`B-PRD`), `-` (`I-PRD`), `KTP` (`I-PRD`).

---

## 5. Pohon Keputusan Disambiguasi Kasus Rawan Tertukar

Gunakan pohon keputusan di bawah ini saat menghadapi ambiguitas klasifikasi antar kelas:

### 5.1 Pohon Keputusan: `NOR` vs `ORG`

```
Apakah entitas berwujud organisasi, lembaga, atau kelompok?
  |
  +---> Apakah entitas merupakan lembaga negara, kementerian, parlemen,
  |     badan peradilan, komisi tinggi, atau dinas pemerintah daerah?
  |       |-- YA  ==> Beri label NOR (misal: KPK, DPR, KPU, BMKG, Kemenkeu, Pemkab)
  |       |-- TIDAK
  |
  +---> Apakah entitas merupakan kesatuan aparat kepolisian atau militer?
  |       |-- YA  ==> Beri label NOR (misal: Polri, Polisi, TNI, Polda Metro Jaya, Satreskrim)
  |       |-- TIDAK
  |
  +---> Apakah entitas merupakan partai politik atau fraksi parlemen?
  |       |-- YA  ==> Beri label NOR (misal: PKS, PDIP, Gerindra, Golkar, Demokrat)
  |       |-- TIDAK
  |
  +---> Apakah entitas merupakan organisasi antarpemerintah dunia?
  |       |-- YA  ==> Beri label NOR (misal: PBB, WHO)
  |       |-- TIDAK
  |
  +---> Apakah entitas merupakan badan usaha komersial, perusahaan swasta,
  |     BUMN perseroan, media pers, universitas/sekolah, atau klub olahraga?
  |       |-- YA  ==> Beri label ORG (misal: Bank Mandiri, Pertamina, detikcom, Chelsea, UNS)
```

### 5.2 Pohon Keputusan: `PRD` vs `ORG`

```
Apakah entitas merujuk pada nama korporasi/merek manufaktur?
  |
  +---> Apakah entitas merujuk pada BADAN HUKUM korporasi yang memproduksi,
  |     mempekerjakan karyawan, atau merilis pernyataan bisnis?
  |       |-- YA  ==> Beri label ORG (misal: Apple Inc., PT Astra, Twitter Inc.)
  |       |-- TIDAK
  |
  +---> Apakah entitas merujuk pada PERANGKAT FISIK, KENDARAAN, BARANG KOMODITAS,
  |     APLIKASI/PLATFORM DIGITAL, atau INDEKS PASAR?
  |       |-- YA  ==> Beri label PRD (misal: iPhone, mobil, truk, sabu, beras, Twitter, IHSG)
```

### 5.3 Pohon Keputusan: `FAC` vs `LOC` vs `GPE`

```
Apakah entitas merupakan entitas spasial / tempat?
  |
  +---> Apakah wilayah tersebut memiliki batas administratif resmi, pemerintahan,
  |     dan penduduk masyarakat berdaulat? (Negara, Provinsi, Kota, Kabupaten, Desa)
  |       |-- YA  ==> Beri label GPE (misal: Indonesia, Jawa Timur, Surabaya, Badung)
  |       |-- TIDAK
  |
  +---> Apakah merupakan fasilitas infrastruktur buatan manusia yang tertutup, gedung,
  |     bandara, pelabuhan, terminal bus, stasiun, jalan tol, atau stadion?
  |       |-- YA  ==> Beri label FAC (misal: Bandara Soekarno - Hatta, GBK, Terminal Tanjung Priok)
  |       |-- TIDAK
  |
  +---> Apakah merupakan bentang alam alami (gunung, danau, pantai, laut) ATAU
  |     koridor jalan raya terbuka / kawasan taman publik?
  |       |-- YA  ==> Beri label LOC (misal: Danau Toba, Jalan Sudirman, Taman Fatahillah)
```

### 5.4 Pohon Keputusan Kelas Numerik: `CRD` vs `QTY` vs `MON` vs `PRC` vs `DAT` vs `TIM`

```
Apakah token mengandung angka, bilangan, atau penunjuk urutan?
  |
  +---> Apakah memiliki simbol mata uang atau kata satuan valuta?
  |       |-- YA  ==> Beri label MON (misal: Rp 40 Ribu, 100 triliun rupiah, US$ 50 juta)
  |       |-- TIDAK
  |
  +---> Apakah memiliki simbol persen (%) atau kata "persen"?
  |       |-- YA  ==> Beri label PRC (misal: 10 %, 50 persen, 2 , 5 %)
  |       |-- TIDAK
  |
  +---> Apakah menunjukkan peringkat, tahapan, urutan ke-N, atau hierarki sekuens?
  |       |-- YA  ==> Beri label ORD (misal: pertama, ke - 4, ke - 12, kesekian)
  |       |-- TIDAK
  |
  +---> Apakah terikat dengan besaran fisik metrik (kg, ton, cm, km) ATAU
  |     merupakan durasi/jangka rentang waktu (tahun, bulan, hari, jam, abad)?
  |       |-- YA  ==> Beri label QTY (misal: 15 kilogram, 41 ton, dua tahun, 24 jam, 36 hari)
  |       |-- TIDAK
  |
  +---> Apakah menunjukkan titik penanggalan kalender (hari, tanggal, bulan, tahun)?
  |       |-- YA  ==> Beri label DAT (misal: 15 Mei 2018, Selasa ( 15 / 5 / 2018 ), 2018)
  |       |-- TIDAK
  |
  +---> Apakah menunjukkan waktu pembacaan jam arloji / titik waktu harian?
  |       |-- YA  ==> Beri label TIM (misal: 06 . 00 WIB, pukul 10 . 30 Wita)
  |       |-- TIDAK
  |
  +---> Apakah angka kuantitas cacah murni tanpa satuan di atas?
          |-- YA  ==> Beri label CRD (misal: satu, dua, tiga, 115, 1 . 000, kedua)
```

### 5.5 Pohon Keputusan: `REG` vs (`NOR`, `EVT`, `WOA`, `PER`, `FAC`, `O`)

```
Apakah entitas berakar dari konteks keagamaan / spiritual?
  |
  +---> Apakah merupakan nama agama formal atau ajaran spiritual?
  |       |-- YA  ==> Beri label REG (misal: Islam, Kristen, Hindu, Buddha, Sunda Wiwitan)
  |       |-- TIDAK
  |
  +---> Apakah merupakan sebutan penganut/umat beragama?
  |       |-- YA  ==> Beri label REG (misal: Muslim, umat Islam, Kristiani, umat Hindu)
  |       |-- TIDAK
  |
  +---> Apakah merupakan hari raya, musim ibadah, atau peringatan suci?
  |       |-- YA  ==> Beri label REG (misal: Ramadan, Idul Fitri, Lebaran, Waisak, Galungan, Natal)
  |       |-- TIDAK
  |
  +---> Apakah merupakan kitab suci keagamaan atau bagiannya?
  |       |-- YA  ==> Beri label REG (misal: Alquran, Al - Qur ' an, Injil, Taurat, juz)
  |       |-- TIDAK
  |
  +---> Apakah merupakan figur suci Tuhan, Dewa, atau Nabi?
  |       |-- YA  ==> Beri label REG (misal: Allah SWT, Tuhan, Nabi Muhammad SAW, Rasulullah)
  |       |-- TIDAK
  |
  +---> Apakah merupakan aktivitas ibadah, ritus, atau doa ibadah?
  |       |-- YA  ==> Beri label REG (misal: puasa, sholat tarawih, Buka Puasa, takbiran, misa, azan)
  |       |-- TIDAK
  |
  +---> Apakah merupakan tempat ibadah fisik umum (masjid, gereja, surau)?
  |       |-- YA  ==> Beri label REG (misal: masjid, Masjid, Gereja, Surau, musala)
  |       |-- TIDAK
  |
  +---> Apakah merupakan gelar rohaniwan umum (ulama, ustaz, pendeta)?
  |       |-- YA  ==> Beri label REG (misal: ulama, ustaz, pendeta)
  |       |-- TIDAK
  |
  +---> Apakah merupakan seruan / interjeksi doa keagamaan dalam percakapan?
          |-- YA  ==> Beri label REG (misal: Insya Allah, insyaallah, Alhamdulillah, Astaghfirullah)
```

---

## 6. Contoh Anotasi Berjalan Token-demi-Token

Berikut adalah 5 contoh teks berita riil yang dianotasi token demi token secara lengkap sesuai standar baku NERGRIT:

### Kasus 1: Berita Politik & Pemerintahan
**Kalimat Masukan**:  
`Presiden Joko Widodo menegaskan bahwa pemerintah tidak akan menaikkan harga BBM hingga tahun 2019 mendatang .`

| Indeks | Token | Label BIO | Kategori Entitas | Catatan & Justifikasi Batas |
| :---: | :--- | :---: | :---: | :--- |
| 1 | Presiden | **`B-NOR`** | `NOR` | Jabatan kepala negara formal dilabeli `NOR` (bukan bagian dari `PER`). |
| 2 | Joko | **`B-PER`** | `PER` | Nama orang dimulai dari token pertama nama diri. |
| 3 | Widodo | **`I-PER`** | `PER` | Token lanjutan nama diri individu. |
| 4 | menegaskan | **`O`** | - | Verba predikat. |
| 5 | bahwa | **`O`** | - | Konjungsi subordinatif. |
| 6 | pemerintah | **`B-NOR`** | `NOR` | Entitas eksekutif kenegaraan dilabeli `NOR`. |
| 7 | tidak | **`O`** | - | Adverbia negasi. |
| 8 | akan | **`O`** | - | Modalitas. |
| 9 | menaikkan | **`O`** | - | Verba. |
| 10 | harga | **`O`** | - | Nomina umum. |
| 11 | BBM | **`B-PRD`** | `PRD` | Komoditas energi bahan bakar minyak dilabeli `PRD`. |
| 12 | hingga | **`O`** | - | Preposisi temporal wajib dieksklusi (`O`). |
| 13 | tahun | **`O`** | - | Nomina umum penunjuk waktu dieksklusi (`O`). |
| 14 | 2019 | **`B-DAT`** | `DAT` | Angka tahun kalender murni dilabeli `DAT`. |
| 15 | mendatang | **`O`** | - | Adjektiva penunjuk waktu relatif. |
| 16 | . | **`O`** | - | Tanda baca titik penutup kalimat. |

---

### Kasus 2: Berita Kriminalitas & Penegakan Hukum
**Kalimat Masukan**:  
`Satreskrim Polres Purwakarta berhasil membekuk pelaku pencurian mobil dan menyita barang bukti berupa 5 kg sabu di Jalan Ahmad Yani .`

| Indeks | Token | Label BIO | Kategori Entitas | Catatan & Justifikasi Batas |
| :---: | :--- | :---: | :---: | :--- |
| 1 | Satreskrim | **`B-NOR`** | `NOR` | Satuan unit aparat kepolisian dilabeli `NOR`. |
| 2 | Polres | **`I-NOR`** | `NOR` | Kelanjutan nama satuan kepolisian resor. |
| 3 | Purwakarta | **`I-NOR`** | `NOR` | Wilayah yurisdiksi kepolisian yang melekat dalam nama satuan. |
| 4 | berhasil | **`O`** | - | Verba bantu. |
| 5 | membekuk | **`O`** | - | Verba aktif. |
| 6 | pelaku | **`O`** | - | Nomina pelaku. |
| 7 | pencurian | **`O`** | - | Nomina tindakan. |
| 8 | mobil | **`B-PRD`** | `PRD` | Sarana kendaraan roda empat huruf kecil dilabeli `PRD`. |
| 9 | dan | **`O`** | - | Konjungsi koordinatif. |
| 10 | menyita | **`O`** | - | Verba. |
| 11 | barang | **`O`** | - | Nomina. |
| 12 | bukti | **`O`** | - | Nomina. |
| 13 | berupa | **`O`** | - | Verba perujuk. |
| 14 | 5 | **`B-QTY`** | `QTY` | Angka pengukuran fisik bobot. |
| 15 | kg | **`I-QTY`** | `QTY` | Satuan metrik massa kilogram yang melekat pada angka. |
| 16 | sabu | **`B-PRD`** | `PRD` | Narkotika komoditas sitaan dilabeli `PRD`. |
| 17 | di | **`O`** | - | Preposisi tempat wajib dieksklusi (`O`). |
| 18 | Jalan | **`B-LOC`** | `LOC` | Kata jenis koridor jalan raya. |
| 19 | Ahmad | **`I-LOC`** | `LOC` | Bagian dari nama koridor jalan raya. |
| 20 | Yani | **`I-LOC`** | `LOC` | Bagian akhir dari nama koridor jalan raya. |
| 21 | . | **`O`** | - | Tanda baca titik penutup kalimat. |

---

### Kasus 3: Berita Ekonomi & Finansial
**Kalimat Masukan**:  
`Bank Mandiri menyiapkan uang tunai Rp 40 triliun pada Selasa ( 15 / 5 / 2018 ) untuk mengantisipasi lonjakan transaksi hingga 15 % .`

| Indeks | Token | Label BIO | Kategori Entitas | Catatan & Justifikasi Batas |
| :---: | :--- | :---: | :---: | :--- |
| 1 | Bank | **`B-ORG`** | `ORG` | Entitas perbankan perseroan komersial. |
| 2 | Mandiri | **`I-ORG`** | `ORG` | Kelanjutan nama korporasi bank. |
| 3 | menyiapkan | **`O`** | - | Verba. |
| 4 | uang | **`O`** | - | Nomina umum. |
| 5 | tunai | **`O`** | - | Adjektiva. |
| 6 | Rp | **`B-MON`** | `MON` | Simbol mata uang pembuka nominal uang. |
| 7 | 40 | **`I-MON`** | `MON` | Angka pembilang nominal uang. |
| 8 | triliun | **`I-MON`** | `MON` | Satuan pengali nominal uang. |
| 9 | pada | **`O`** | - | Preposisi waktu wajib dieksklusi (`O`). |
| 10 | Selasa | **`B-DAT`** | `DAT` | Awal rentang tanggal kepala berita berformat kurung. |
| 11 | ( | **`I-DAT`** | `DAT` | Tanda kurung buka diserap ke dalam rentang `DAT`. |
| 12 | 15 | **`I-DAT`** | `DAT` | Angka tanggal. |
| 13 | / | **`I-DAT`** | `DAT` | Garis miring pemisah tanggal. |
| 14 | 5 | **`I-DAT`** | `DAT` | Angka bulan. |
| 15 | / | **`I-DAT`** | `DAT` | Garis miring pemisah tahun. |
| 16 | 2018 | **`I-DAT`** | `DAT` | Angka tahun. |
| 17 | ) | **`I-DAT`** | `DAT` | Tanda kurung tutup diserap ke dalam rentang `DAT`. |
| 18 | untuk | **`O`** | - | Preposisi tujuan. |
| 19 | mengantisipasi | **`O`** | - | Verba. |
| 20 | lonjakan | **`O`** | - | Nomina. |
| 21 | transaksi | **`O`** | - | Nomina. |
| 22 | hingga | **`O`** | - | Preposisi rentang nilai. |
| 23 | 15 | **`B-PRC`** | `PRC` | Angka persentase. |
| 24 | % | **`I-PRC`** | `PRC` | Simbol persen yang melekat. |
| 25 | . | **`O`** | - | Tanda baca titik akhir kalimat. |

---

### Kasus 4: Berita Keagamaan & Hari Raya
**Kalimat Masukan**:  
`Selama bulan Ramadan , umat Islam di Surabaya berbondong - bondong melaksanakan sholat tarawih di Masjid Agung .`

| Indeks | Token | Label BIO | Kategori Entitas | Catatan & Justifikasi Batas |
| :---: | :--- | :---: | :---: | :--- |
| 1 | Selama | **`O`** | - | Preposisi durasi wajib dieksklusi (`O`). |
| 2 | bulan | **`O`** | - | Nomina pengantar dieksklusi (`O`). |
| 3 | Ramadan | **`B-REG`** | `REG` | Nama bulan suci / musim ibadah keagamaan. |
| 4 | , | **`O`** | - | Tanda koma pemisah klausa. |
| 5 | umat | **`B-REG`** | `REG` | Sebutan kolektif penganut agama. |
| 6 | Islam | **`I-REG`** | `REG` | Kelanjutan frasa umat penganut agama. |
| 7 | di | **`O`** | - | Preposisi tempat wajib dieksklusi (`O`). |
| 8 | Surabaya | **`B-GPE`** | `GPE` | Entitas kota geopolitik administratif. |
| 9 | berbondong | **`O`** | - | Kata kerja reduplikasi. |
| 10 | - | **`O`** | - | Tanda hubung reduplikasi verba. |
| 11 | bondong | **`O`** | - | Kelanjutan verba reduplikasi. |
| 12 | melaksanakan | **`O`** | - | Verba aktif transitif. |
| 13 | sholat | **`B-REG`** | `REG` | Ritus peribadatan keagamaan. |
| 14 | tarawih | **`I-REG`** | `REG` | Jenis ritual ibadah malam Ramadan. |
| 15 | di | **`O`** | - | Preposisi tempat wajib dieksklusi (`O`). |
| 16 | Masjid | **`B-REG`** | `REG` | Tempat peribadatan dalam NERGRIT dilabeli `REG`. |
| 17 | Agung | **`I-REG`** | `REG` | Bagian dari nama tempat peribadatan. |
| 18 | . | **`O`** | - | Tanda titik penutup kalimat. |

---

### Kasus 5: Berita Olahraga Internasional
**Kalimat Masukan**:  
`Timnas Brasil mempersiapkan bonus besar untuk menjuarai Piala Dunia 2018 di Rusia setelah meraih kemenangan ke - 4 .`

| Indeks | Token | Label BIO | Kategori Entitas | Catatan & Justifikasi Batas |
| :---: | :--- | :---: | :---: | :--- |
| 1 | Timnas | **`B-ORG`** | `ORG` | Tim olahraga kesebelasan nasional dalam kompetisi. |
| 2 | Brasil | **`I-ORG`** | `ORG` | Kelanjutan nama tim olahraga kesebelasan. |
| 3 | mempersiapkan | **`O`** | - | Verba. |
| 4 | bonus | **`O`** | - | Nomina. |
| 5 | besar | **`O`** | - | Adjektiva. |
| 6 | untuk | **`O`** | - | Preposisi tujuan. |
| 7 | menjuarai | **`O`** | - | Verba. |
| 8 | Piala | **`B-EVT`** | `EVT` | Awal nama ajang kejuaraan olahraga internasional. |
| 9 | Dunia | **`I-EVT`** | `EVT` | Kelanjutan nama turnamen olahraga. |
| 10 | 2018 | **`I-EVT`** | `EVT` | Tahun edisi ajang turnamen yang melekat pada nama. |
| 11 | di | **`O`** | - | Preposisi tempat wajib dieksklusi (`O`). |
| 12 | Rusia | **`B-GPE`** | `GPE` | Nama negara penyelenggara (wilayah geopolitik). |
| 13 | setelah | **`O`** | - | Konjungsi temporal. |
| 14 | meraih | **`O`** | - | Verba. |
| 15 | kemenangan | **`O`** | - | Nomina. |
| 16 | ke | **`B-ORD`** | `ORD` | Prefiks pembentuk bilangan ordinal tingkat wajib inklusif. |
| 17 | - | **`I-ORD`** | `ORD` | Tanda hubung pembentuk ordinal diserap ke dalam span. |
| 18 | 4 | **`I-ORD`** | `ORD` | Angka urutan kemenangan. |
| 19 | . | **`O`** | - | Tanda titik akhir kalimat. |

---

---

### Kasus 6: Berita Hukum, Pengadilan, & Perundang-Undangan
**Kalimat Masukan**:  
`Majelis hakim Pengadilan Negeri Jakarta Pusat menjatuhkan vonis kepada 3 terdakwa pelanggar Undang - Undang Nomor 11 Tahun 2008 pada Kamis ( 18 / 5 ) .`

| Indeks | Token | Label BIO | Kategori Entitas | Catatan & Justifikasi Batas |
| :---: | :--- | :---: | :---: | :--- |
| 1 | Majelis | **`O`** | - | Nomina umum peradilan. |
| 2 | hakim | **`O`** | - | Nomina jabatan peradilan non-kenegaraan. |
| 3 | Pengadilan | **`B-NOR`** | `NOR` | Badan peradilan yurisdiksi negara dilabeli `NOR`. |
| 4 | Negeri | **`I-NOR`** | `NOR` | Kelanjutan nama tingkat peradilan. |
| 5 | Jakarta | **`I-NOR`** | `NOR` | Wilayah yurisdiksi yang menyatu dalam nama institusi hukum. |
| 6 | Pusat | **`I-NOR`** | `NOR` | Bagian akhir nama satuan pengadilan. |
| 7 | menjatuhkan | **`O`** | - | Verba. |
| 8 | vonis | **`O`** | - | Nomina proses hukum. |
| 9 | kepada | **`O`** | - | Preposisi tujuan. |
| 10 | 3 | **`B-CRD`** | `CRD` | Angka kardinal cacah murni tanpa satuan fisik/moneter. |
| 11 | terdakwa | **`O`** | - | Nomina umum. |
| 12 | pelanggar | **`O`** | - | Nomina. |
| 13 | Undang | **`B-LAW`** | `LAW` | Awal nama dokumen perundang-undangan formal negara. |
| 14 | - | **`I-LAW`** | `LAW` | Tanda hubung reduplikasi dokumen hukum wajib diserap. |
| 15 | Undang | **`I-LAW`** | `LAW` | Kelanjutan reduplikasi nama undang-undang. |
| 16 | Nomor | **`I-LAW`** | `LAW` | Kata penomoran regulasi resmi diserap. |
| 17 | 11 | **`I-LAW`** | `LAW` | Angka nomor urut regulasi resmi diserap. |
| 18 | Tahun | **`I-LAW`** | `LAW` | Kata penanda tahun legislasi diserap. |
| 19 | 2008 | **`I-LAW`** | `LAW` | Angka tahun pengesahan legislasi diserap ke dalam `LAW`. |
| 20 | pada | **`O`** | - | Preposisi temporal wajib dieksklusi (`O`). |
| 21 | Kamis | **`B-DAT`** | `DAT` | Awal rentang tanggal kepala berita format kurung. |
| 22 | ( | **`I-DAT`** | `DAT` | Tanda kurung buka diserap ke dalam `DAT`. |
| 23 | 18 | **`I-DAT`** | `DAT` | Angka tanggal penanggalan. |
| 24 | / | **`I-DAT`** | `DAT` | Garis miring pemisah kalender. |
| 25 | 5 | **`I-DAT`** | `DAT` | Angka bulan. |
| 26 | ) | **`I-DAT`** | `DAT` | Tanda kurung tutup diserap ke dalam `DAT`. |
| 27 | . | **`O`** | - | Tanda titik akhir kalimat. |

---

### Kasus 7: Berita Fasilitas Transportasi & Infrastruktur
**Kalimat Masukan**:  
`Penerbangan pesawat Boeing 737 menuju Bandara Soekarno - Hatta ditunda hingga pukul 14 . 30 WIB karena cuaca buruk di Tangerang .`

| Indeks | Token | Label BIO | Kategori Entitas | Catatan & Justifikasi Batas |
| :---: | :--- | :---: | :---: | :--- |
| 1 | Penerbangan | **`O`** | - | Nomina aktivitas. |
| 2 | pesawat | **`B-PRD`** | `PRD` | Sarana kendaraan fisik udara huruf kecil dilabeli `PRD`. |
| 3 | Boeing | **`I-PRD`** | `PRD` | Merek manufaktur wahana yang melekat pada produk. |
| 4 | 737 | **`I-PRD`** | `PRD` | Nomor seri tipe komoditas transportasi fisik. |
| 5 | menuju | **`O`** | - | Preposisi arah spasial wajib dieksklusi (`O`). |
| 6 | Bandara | **`B-FAC`** | `FAC` | Fasilitas infrastruktur transportasi buatan manusia. |
| 7 | Soekarno | **`I-FAC`** | `FAC` | Bagian dari nama fasilitas fisik bandara. |
| 8 | - | **`I-FAC`** | `FAC` | Tanda hubung nama ganda fasilitas diserap ke `FAC`. |
| 9 | Hatta | **`I-FAC`** | `FAC` | Kelanjutan nama fasilitas fisik bandara. |
| 10 | ditunda | **`O`** | - | Verba pasif. |
| 11 | hingga | **`O`** | - | Preposisi temporal batas waktu wajib dieksklusi (`O`). |
| 12 | pukul | **`B-TIM`** | `TIM` | Kata pengantar titik penunjuk jam arloji harian. |
| 13 | 14 | **`I-TIM`** | `TIM` | Angka penunjuk jam dalam siklus 24 jam. |
| 14 | . | **`I-TIM`** | `TIM` | Tanda titik pemisah jam dan menit yang terpisah spasi. |
| 15 | 30 | **`I-TIM`** | `TIM` | Angka penunjuk menit. |
| 16 | WIB | **`I-TIM`** | `TIM` | Penanda zona waktu resmi Indonesia Barat diserap ke `TIM`. |
| 17 | karena | **`O`** | - | Konjungsi kausal. |
| 18 | cuaca | **`O`** | - | Nomina kondisi alam. |
| 19 | buruk | **`O`** | - | Adjektiva. |
| 20 | di | **`O`** | - | Preposisi spasial lokasi wajib dieksklusi (`O`). |
| 21 | Tangerang | **`B-GPE`** | `GPE` | Wilayah kota administratif berpemerintahan. |
| 22 | . | **`O`** | - | Tanda titik penutup kalimat. |

---

### Kasus 8: Berita Kebudayaan, Karya Seni, & Bahasa
**Kalimat Masukan**:  
`Penerbit Gramedia merilis 2 edisi novel " Laskar Pelangi " karangan Andrea Hirata dalam bahasa Indonesia dan bahasa Inggris .`

| Indeks | Token | Label BIO | Kategori Entitas | Catatan & Justifikasi Batas |
| :---: | :--- | :---: | :---: | :--- |
| 1 | Penerbit | **`O`** | - | Nomina deskriptor peran usaha umum. |
| 2 | Gramedia | **`B-ORG`** | `ORG` | Korporasi penerbitan swasta komersial berbadan hukum. |
| 3 | merilis | **`O`** | - | Verba aktif. |
| 4 | 2 | **`B-CRD`** | `CRD` | Angka bilangan cacah murni kuantitas edisi. |
| 5 | edisi | **`O`** | - | Nomina umum. |
| 6 | novel | **`O`** | - | Nomina format buku sastra. |
| 7 | " | **`O`** | - | Tanda petik ganda pembuka WAJIB DIEKSKLUSI (`O`). |
| 8 | Laskar | **`B-WOA`** | `WOA` | Awal judul karya cipta seni/sastra intelektual. |
| 9 | Pelangi | **`I-WOA`** | `WOA` | Kelanjutan judul karya cipta sastra. |
| 10 | " | **`O`** | - | Tanda petik ganda penutup WAJIB DIEKSKLUSI (`O`). |
| 11 | karangan | **`O`** | - | Nomina relasional pengarang. |
| 12 | Andrea | **`B-PER`** | `PER` | Nama depan pencipta individu manusia. |
| 13 | Hirata | **`I-PER`** | `PER` | Nama belakang pencipta individu manusia. |
| 14 | dalam | **`O`** | - | Preposisi medium wajib dieksklusi (`O`). |
| 15 | bahasa | **`B-LAN`** | `LAN` | Prefiks kata jenis bahasa alami manusia. |
| 16 | Indonesia | **`I-LAN`** | `LAN` | Nama bahasa alami manusia yang dituturkan. |
| 17 | dan | **`O`** | - | Konjungsi koordinatif pemisah dua entitas bahasa. |
| 18 | bahasa | **`B-LAN`** | `LAN` | Awal entitas bahasa kedua yang bersanding (`B-LAN`). |
| 19 | Inggris | **`I-LAN`** | `LAN` | Nama bahasa alami manusia kedua. |
| 20 | . | **`O`** | - | Tanda titik penutup kalimat. |

---

## 7. Daftar Uji Kualitas Anotator & 10 Jebakan Fatal

### 7.1 Daftar Periksa Mandiri (*Self-Checklist*)
Sebelum menyelesaikan sebuah set kalimat atau memvalidasi output model, setiap annotator wajib memverifikasi butir-butir pemeriksaan berikut:

- [ ] **Uji Preposisi Spasial & Temporal**: Pastikan tidak ada kata `di`, `ke`, `dari`, `pada`, `dalam`, atau `selama` yang berada di dalam span entitas (satu-satunya pengecualian adalah `ke` sebagai prefiks ordinal `ke - N` pada `ORD`).
- [ ] **Uji Sapaan Kekerabatan**: Pastikan kata sapaan umum seperti `Bapak`, `Ibu`, `Saudara`, `Tuan` berstatus `O` dan tidak masuk ke dalam `PER`.
- [ ] **Uji Gelar Melekat vs Jabatan**: Pastikan gelar akademis/religi (`Dr.`, `KH`, `Habib`) diserap ke `PER` (`B-PER`), sedangkan jabatan politik/militer/kenegaraan (`Presiden`, `Gubernur`, `Kapolri`) dilabeli `NOR`.
- [ ] **Uji Lembaga Negara vs Korporasi**: Pastikan lembaga eksekutif, yudikatif, legislatif, kepolisian, militer, dan parpol dilabeli `NOR`. Pastikan `ORG` hanya digunakan untuk korporasi komersial swasta/BUMN, portal media berita, dan klub olahraga.
- [ ] **Uji Sarana & Komoditas Huruf Kecil**: Pastikan sarana transportasi huruf kecil (`mobil`, `sepeda motor`, `truk`, `pesawat`) serta komoditas perdagangan (`sabu`, `beras`, `kopi`, `BBM`) diberi label `PRD`.
- [ ] **Uji Format Tanggal Berita**: Pastikan format penanggalan kepala berita berformat kurung `Hari ( DD / MM / YYYY )` ditandai sebagai **satu kesatuan utuh `DAT`** mencakup tanda kurung buka dan tutupnya.
- [ ] **Uji Durasi Waktu**: Pastikan seluruh satuan rentang/durasi waktu lampau atau masa jangka (`dua tahun`, `24 jam`, `36 hari`, `30 menit`) dilabeli `QTY`, bukan `DAT` atau `TIM`.
- [ ] **Uji Bilangan Cacah Murni vs Satuan**: Pastikan angka cacah tanpa satuan (`3 terdakwa`, `2 edisi`, `kedua`) dilabeli `CRD`, bukan `QTY` atau `ORD`.
- [ ] **Uji Fasilitas Buatan vs Lokasi Terbuka**: Pastikan bangunan buatan manusia tertutup, bandara, stadion, dan terminal bus dilabeli `FAC`, sedangkan bentang alam alami dan nama jalan raya dilabeli `LOC`.
- [ ] **Uji Tanda Petik Karya Seni & Ajang**: Pastikan tanda petik (`"..."` atau `'...'`) di sekitar nama karya cipta (`WOA`) atau ajang kegiatan (`EVT`) selalu berada di luar rentang (berstatus `O`).
- [ ] **Uji Nama Bahasa Alami**: Pastikan nama bahasa alami manusia (`bahasa Indonesia`, `bahasa Arab`, `bahasa Inggris`) dilabeli `LAN`.
- [ ] **Uji Entitas Keagamaan**: Pastikan seluruh konsep keagamaan (agama, penganut, hari raya, kitab suci, tempat ibadah, ritual sholat/puasa, dan seruan doa) dilabeli `REG`.
- [ ] **Uji Integritas Transisi BIO**: Pastikan tidak ada token `I-TAG` liar yang muncul tanpa diawali `B-TAG` dari kelas yang sama, dan dua entitas bersebelahan sejenis diawali dengan `B-TAG` baru.

---

### 7.2 10 Kesalahan Fatal Anotasi (*Top 10 Annotation Pitfalls*)

| No | Jebakan Fatal (*Pitfall*) | Bentuk Kesalahan (*Error*) | Solusi Baku NERGRIT |
| :-: | :--- | :--- | :--- |
| **1** | **Preposisi Terbawa ke Dalam Entitas** | Anotasi `[LOC di Gunung Agung /LOC]` atau `[DAT pada 15 Mei /DAT]` | **Keluarkan preposisi!** Preposisi selalu berstatus `O`: `di [LOC Gunung Agung /LOC]`. |
| **2** | **Melabeli Polisi / TNI / KPK sebagai `ORG`** | Menganggap kepolisian dan lembaga tinggi negara sebagai organisasi biasa (`ORG`) | **Wajib `NOR`!** Seluruh aparat penegak hukum, militer, kementerian, dan lembaga negara adalah `NOR`. |
| **3** | **Melabeli Partai Politik sebagai `ORG`** | Menganggap `PKS`, `PDIP`, `Gerindra` sebagai `ORG` | **Wajib `NOR`!** Seluruh partai politik dan fraksi parlemen berstatus `NOR`. |
| **4** | **Mengabaikan Kata Benda Huruf Kecil pada `PRD`** | Membiarkan kata `mobil`, `sepeda motor`, `sabu`, `beras` sebagai `O` karena bukan nama diri (*proper noun*) | **Wajib `PRD`!** NERGRIT secara empiris melabeli kendaraan fisik dan komoditas perdagangan sebagai `PRD`. |
| **5** | **Menyerap Jabatan Presiden/Menteri ke dalam `PER`** | Memberi label `[PER Presiden Joko Widodo /PER]` | **Pisahkan!** Jabatan adalah `NOR`: `[NOR Presiden /NOR] [PER Joko Widodo /PER]`. |
| **6** | **Menyerap Sapaan Umum ke dalam `PER`** | Memberi label `[PER Bapak Joko Widodo /PER]` | **Eksklusi sapaan!** Sapaan umum adalah `O`: `Bapak [PER Joko Widodo /PER]`. |
| **7** | **Mengklasifikasikan Durasi Waktu ke dalam `DAT` / `TIM`** | Melabeli `selama [DAT dua tahun /DAT]` atau `dalam [TIM 24 jam /TIM]` | **Wajib `QTY`!** Seluruh rentang dan durasi waktu lampau/jangka di korpus NERGRIT adalah `QTY`. |
| **8** | **Memotong Tanda Kurung Tanggal Berita pada `DAT`** | Anotasi `Selasa ( [DAT 15 / 5 / 2018 /DAT] )` | **Satukan utuh!** Format berita daring `[DAT Selasa ( 15 / 5 / 2018 ) /DAT]` adalah satu kesatuan `DAT`. |
| **9** | **Menyertakan Tanda Petik ke dalam `WOA` / `EVT`** | Memberi label `[WOA " The Dark Knight " /WOA]` | **Eksklusi tanda petik!** Tanda petik adalah `O`: `" [WOA The Dark Knight /WOA] "`. |
| **10** | **Menyebarkan Agama ke Luar Tag `REG`** | Melabeli `Muslim` sebagai `NOR`, `Idul Fitri` sebagai `EVT`, `Alquran` sebagai `WOA`, atau `Masjid` sebagai `FAC` | **Satukan ke `REG`!** Seluruh konsep keagamaan di korpus NERGRIT dikelompokkan khusus ke tag `REG`. |

---

## 8. Panduan Rekayasa Prompt LLM untuk Replikasi Batas NERGRIT

Untuk menghasilkan anotasi baru atau mengekstrak entitas menggunakan model kecerdasan buatan (*Large Language Models* seperti GPT-4o, Claude 3.5 Sonnet, atau Gemini 1.5 Pro) dengan akurasi 100% selaras batas korpus manusia NERGRIT, gunakan rancangan prompt berikut:

### 8.1 Spesifikasi Meta-Prompt Anotator

```markdown
Anda adalah annotator ahli korpus Named Entity Recognition (NER) bahasa Indonesia standar korpus manusia acuan NERGRIT.
Tugas Anda adalah melakukan tokenisasi dan pelabelan BIO (Beginning, Inside, Outside) secara presisi terhadap teks bahasa Indonesia yang diberikan, dengan mematuhi 19 taksonomi kelas dan kaidah batas empiris baku NERGRIT.

19 KELAS ENTITAS NERGRIT:
1. PER (Person): Nama individu manusia (Joko Widodo). Sapaan umum (Bapak/Ibu) WAJIB O. Gelar akademik/religi melekat (Dr., KH, Habib) DISERAP ke B-PER. Jabatan kenegaraan/militer (Presiden, Menteri, Kapolri) DIBERI LABEL NOR.
2. ORG (Organization): Perusahaan swasta, BUMN komersial (Bank Mandiri, Pertamina), portal media pers (detikcom, CNN Indonesia), dan klub sepak bola (Chelsea, Timnas Brasil).
3. GPE (Geo-Political Entity): Negara, provinsi, kota, kabupaten, desa administratif berpemerintahan (Indonesia, Jawa Timur, Surabaya).
4. LOC (Location): Bentang alam alami (Gunung Agung, Danau Toba), koridor jalan (Jalan Sudirman), taman publik (Taman Fatahillah), kawasan benua.
5. FAC (Facility): Bangunan infrastruktur fisik buatan, bandara (Bandara Soekarno - Hatta), stadion (GBK), terminal bus, aula, jalan tol.
6. EVT (Event): Ajang kejuaraan olahraga (Piala Dunia 2018), operasi pengamanan resmi, peristiwa bersejarah bernama. Tanda petik WAJIB O.
7. WOA (Work of Art): Judul film, buku, lagu, karya seni (Laskar Pelangi, Indonesia Raya). Tanda petik WAJIB O.
8. LAW (Law): Undang-undang, perpres, traktat, dokumen hukum resmi (Undang - Undang Dasar 1945, KUHP). Tanda hubung diserap ke I-LAW.
9. PRD (Product): Seluruh kendaraan fisik huruf kecil (mobil, sepeda motor, truk, bus, pesawat), komoditas (sabu, beras, kopi, BBM), gawai elektronik, dan indeks bursa (IHSG).
10. LAN (Language): Nama bahasa alami manusia (bahasa Arab, bahasa Indonesia).
11. DAT (Date): Tanggal kalender, hari, bulan, angka tahun tunggal, dan format berita daring 'Hari ( DD / MM / YYYY )' sebagai SATU SPAN UTUH DAT (+ kurung).
12. TIM (Time): Jam spesifik arloji / pukul (06 . 00 WIB, pukul 10 . 30 Wita).
13. MON (Money): Nilai nominal moneter beserta simbol mata uang (Rp 40 Ribu, 100 triliun rupiah, US$ 50 juta).
14. QTY (Quantity): Satuan metrik fisik (15 kilogram, 41 ton) DAN DURASI WAKTU LAMPAU/JANGKA (dua tahun, 24 jam, 36 hari, 30 menit).
15. CRD (Cardinal): Bilangan cacah/kuantitas murni tanpa satuan fisik/uang (satu, dua, 115, 1 . 000, kedua saat bermakna both).
16. ORD (Ordinal): Bilangan urutan/peringkat (pertama, terakhir). Prefiks 'ke' dan tanda hubung wajib inklusif (ke - 4, ke 58).
17. PRC (Percent): Persentase beserta simbol atau kata (10 %, 50 persen).
18. NOR (NORP & State Org): Aparat kepolisian/militer (Polri, Polisi, TNI), kementerian & lembaga negara (KPK, DPR, KPU), partai politik (PKS, PDIP), organisasi antarpemerintah (PBB), dan jabatan kenegaraan (Presiden, Menteri).
19. REG (Religion): Agama (Islam), penganut (Muslim), hari raya (Idul Fitri, Ramadan), kitab suci (Alquran), sebutan Tuhan/nabi, ritus ibadah (puasa, sholat tarawih, Buka Puasa), tempat ibadah (masjid, gereja), dan doa seruan (Insya Allah).

ATURAN BATAS MUTLAK:
- Preposisi spasial/temporal (di, ke, dari, pada, dalam, selama) 99,99% BERSTATUS O.
- Jangan pernah membuat transisi ilegal (misal: O langsung ke I-TAG, atau B-PER langsung ke I-ORG).
```

### 8.2 Format Output Terstruktur (JSON & CoNLL)
Saat memerintahkan model, selalu tegaskan format luaran deterministik:

#### Format Baris Token CoNLL (*Recommended for Token Classification*):
```
<Token> <BIO-Tag>
```
Contoh:
```
Presiden    B-NOR
Joko        B-PER
Widodo      I-PER
meninjau    O
di          O
Surabaya    B-GPE
.           O
```

#### Format JSON Spans (*Recommended for Information Extraction Pipelines*):
Dalam format JSON rentang (*span-based*), indeks token menggunakan penomoran berbasis 0 (*0-indexed*) dengan konvensi interval setengah terbuka (*half-open interval*) `[start_token, end_token)` di mana `end_token` bersifat eksklusif:

```json
{
  "text": "Presiden Joko Widodo meninjau di Surabaya .",
  "tokens": ["Presiden", "Joko", "Widodo", "meninjau", "di", "Surabaya", "."],
  "entities": [
    {"start_token": 0, "end_token": 1, "label": "NOR", "text": "Presiden"},
    {"start_token": 1, "end_token": 3, "label": "PER", "text": "Joko Widodo"},
    {"start_token": 5, "end_token": 6, "label": "GPE", "text": "Surabaya"}
  ]
}
```
> **Catatan Kritis Batas**: Perhatikan bahwa token ke-4 adalah preposisi `"di"` yang wajib berstatus `O`. Oleh sebab itu, rentang entitas `Surabaya` dimulai pada indeks token `5` hingga `6` (`[5, 6)`), bukan `4`!

---

### 8.3 Few-Shot Demonstrations in Prompt (Contoh Few-Shot LLM)

Berikut adalah 3 contoh *in-context few-shot demonstrations* terstruktur yang siap disematkan ke dalam *system prompt* atau *few-shot context* untuk memandu LLM mereplikasi batas token BIO dan JSON span NERGRIT secara sempurna:

#### Contoh Few-Shot 1: Politik, Gelar Jabatan, & Format Kurung Tanggal Kepala Berita
**Teks Masukan**:
```
Gubernur DKI Jakarta Anies Baswedan meresmikan proyek pada Rabu ( 16 / 5 / 2018 ) .
```
**Luaran CoNLL**:
```
Gubernur       B-NOR
DKI            I-NOR
Jakarta        I-NOR
Anies          B-PER
Baswedan       I-PER
meresmikan     O
proyek         O
pada           O
Rabu           B-DAT
(              I-DAT
16             I-DAT
/              I-DAT
5              I-DAT
/              I-DAT
2018           I-DAT
)              I-DAT
.              O
```
**Luaran JSON Spans**:
```json
{
  "text": "Gubernur DKI Jakarta Anies Baswedan meresmikan proyek pada Rabu ( 16 / 5 / 2018 ) .",
  "tokens": ["Gubernur", "DKI", "Jakarta", "Anies", "Baswedan", "meresmikan", "proyek", "pada", "Rabu", "(", "16", "/", "5", "/", "2018", ")", "."],
  "entities": [
    {"start_token": 0, "end_token": 3, "label": "NOR", "text": "Gubernur DKI Jakarta"},
    {"start_token": 3, "end_token": 5, "label": "PER", "text": "Anies Baswedan"},
    {"start_token": 8, "end_token": 16, "label": "DAT", "text": "Rabu ( 16 / 5 / 2018 )"}
  ]
}
```

#### Contoh Few-Shot 2: Kriminalitas, Komoditas Huruf Kecil, Besaran Fisik, & Nama Jalan
**Teks Masukan**:
```
Aparat Polresta Solo menyita sebuah mobil pikap dan 15 kg beras di Jalan Slamet Riyadi .
```
**Luaran CoNLL**:
```
Aparat         B-NOR
Polresta       I-NOR
Solo           I-NOR
menyita        O
sebuah         O
mobil          B-PRD
pikap          I-PRD
dan            O
15             B-QTY
kg             I-QTY
beras          B-PRD
di             O
Jalan          B-LOC
Slamet         I-LOC
Riyadi         I-LOC
.              O
```
**Luaran JSON Spans**:
```json
{
  "text": "Aparat Polresta Solo menyita sebuah mobil pikap dan 15 kg beras di Jalan Slamet Riyadi .",
  "tokens": ["Aparat", "Polresta", "Solo", "menyita", "sebuah", "mobil", "pikap", "dan", "15", "kg", "beras", "di", "Jalan", "Slamet", "Riyadi", "."],
  "entities": [
    {"start_token": 0, "end_token": 3, "label": "NOR", "text": "Aparat Polresta Solo"},
    {"start_token": 5, "end_token": 7, "label": "PRD", "text": "mobil pikap"},
    {"start_token": 8, "end_token": 10, "label": "QTY", "text": "15 kg"},
    {"start_token": 10, "end_token": 11, "label": "PRD", "text": "beras"},
    {"start_token": 12, "end_token": 15, "label": "LOC", "text": "Jalan Slamet Riyadi"}
  ]
}
```

#### Contoh Few-Shot 3: Hukum, Fasilitas, Karya Seni, & Bahasa Alami
**Teks Masukan**:
```
Penerbit meluncurkan novel " Bumi Manusia " karya Pramoedya Ananta Toer di Bandara Changi dalam bahasa Indonesia .
```
**Luaran CoNLL**:
```
Penerbit       O
meluncurkan    O
novel          O
"              O
Bumi           B-WOA
Manusia        I-WOA
"              O
karya          O
Pramoedya      B-PER
Ananta         I-PER
Toer           I-PER
di             O
Bandara        B-FAC
Changi         I-FAC
dalam          O
bahasa         B-LAN
Indonesia      I-LAN
.              O
```
**Luaran JSON Spans**:
```json
{
  "text": "Penerbit meluncurkan novel \" Bumi Manusia \" karya Pramoedya Ananta Toer di Bandara Changi dalam bahasa Indonesia .",
  "tokens": [
    "Penerbit",
    "meluncurkan",
    "novel",
    "\"",
    "Bumi",
    "Manusia",
    "\"",
    "karya",
    "Pramoedya",
    "Ananta",
    "Toer",
    "di",
    "Bandara",
    "Changi",
    "dalam",
    "bahasa",
    "Indonesia",
    "."
  ],
  "entities": [
    {
      "start_token": 4,
      "end_token": 6,
      "label": "WOA",
      "text": "Bumi Manusia"
    },
    {
      "start_token": 8,
      "end_token": 11,
      "label": "PER",
      "text": "Pramoedya Ananta Toer"
    },
    {
      "start_token": 12,
      "end_token": 14,
      "label": "FAC",
      "text": "Bandara Changi"
    },
    {
      "start_token": 15,
      "end_token": 17,
      "label": "LAN",
      "text": "bahasa Indonesia"
    }
  ]
}
```

---

## 9. Matriks Perbandingan Taksonomi

Tabel perbandingan antara taksonomi korpus acuan manusia NERGRIT (19 kelas), standar internasional OntoNotes 5.0 (18 kelas), dan pipeline rekayasa prompt penelitian skripsi:

| Kode Tag | Nama Kelas Entitas | Standar NERGRIT (19 Tag) | Standar OntoNotes 5.0 (18 Tag) | Pipeline Prompt Generasi Skripsi | Pemetaan Evaluasi Skripsi |
| :---: | :--- | :--- | :--- | :--- | :---: |
| `PER` | Person | Nama orang + gelar melekat (`Dr.`) | Nama orang murni (tanpa gelar) | Nama orang murni | `PER` |
| `ORG` | Organization | Korporasi swasta, BUMN, pers, klub olahraga | Korporasi, lembaga negara, parpol, ormas | Korporasi, BUMN, pers, klub olahraga | `ORG` |
| `GPE` | Geo-Political Entity | Wilayah administratif berpenduduk | Wilayah administratif berpenduduk | Wilayah administratif berpenduduk | `GPE` |
| `LOC` | Location | Bentang alam, jalan raya, taman | Bentang alam, jalan raya, benua | Bentang alam, jalan raya, taman | `LOC` |
| `FAC` | Facility | Bangunan buatan, bandara, stadion | Bangunan buatan, jalan raya, bandara | Bangunan buatan, bandara, stadion | `FAC` |
| `EVT` | Event | Peristiwa, turnamen olahraga, bencana | Peristiwa sejarah, bencana, festival | Ajang olahraga, konferensi, peristiwa | `EVT` |
| `WOA` | Work of Art | Judul buku, film, lagu | Judul buku, film, karya seni | Judul karya seni, lagu, film | `WOA` |
| `LAW` | Law | Undang-undang, KUHP, traktat | Dokumen hukum, undang-undang | Perundang-undangan resmi | `LAW` |
| `PRD` | Product | Komoditas umum, kendaraan, gadget | Produk bermerek, wahana transportasi | Komoditas, kendaraan, produk | `PRD` |
| `LAN` | Language | Bahasa alami manusia | Bahasa alami manusia & pemrograman | Bahasa alami manusia | `LAN` |
| `DAT` | Date | Tanggal kalender, tahun, `Hari ( Tgl )` | Tanggal, tahun, durasi $\ge 24$ jam | Tanggal kalender, tahun | `DAT` |
| `TIM` | Time | Jam arloji / waktu harian | Jam arloji, durasi $< 24$ jam | Jam arloji / penunjuk waktu | `TIM` |
| `MON` | Money | Nilai moneter + simbol/kata valuta | Nilai moneter + simbol/kata valuta | Nilai nominal moneter | `MON` |
| `QTY` | Quantity | Besaran fisik metrik + DURASI WAKTU | Besaran fisik metrik (tanpa durasi) | Besaran fisik metrik + durasi | `QTY` |
| `CRD` | Cardinal | Angka cacah kuantitas murni | Angka cacah kuantitas murni | Angka bilangan cacah | `CRD` |
| `ORD` | Ordinal | Nomor urut tingkat (`ke - N`) | Nomor urut tingkat | Nomor urut tingkat | `ORD` |
| `PRC` | Percent | Persentase nilai proporsi | Persentase nilai proporsi | Nilai persentase | `PRC` |
| `NOR` | NORP & State Org | Lembaga negara, polisi, parpol, etnis | Bangsa, kelompok etnis, agama, partai | Lembaga negara, parpol, demografi | `NOR` |
| `REG` | Religion | Agama, penganut, hari raya, masjid, doa | *Tidak ada* (disebar ke NORP/EVT/FAC/O) | Konsep keagamaan terisolasi | **Dipetakan ke `O`** |
| `TTL` | Title / Jabatan | *Tidak ada* (masuk ke NOR atau O) | *Tidak ada* (diberi label O) | Tag buffer penampung gelar jabatan | **Dipetakan ke `O`** |

---

*(Pedoman ini disusun secara sistematis dan disinkronkan dengan basis data eksperimen repositori skripsi untuk memastikan standardisasi anotasi korpus Named Entity Recognition bahasa Indonesia).*
