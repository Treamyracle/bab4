# Panduan Anotasi Named Entity Recognition (OntoNotes 5.0)

> **Dokumen Rujukan**: Emi Maekawa (2018). *Annotation Guidelines for Named Entities (Version 1.1)*, mengacu pada standar *OntoNotes Release 5.0* (Weischedel et al., 2012) dan *OntoNotes Named Entity Guidelines Version 14.0* (BBN Technologies, 2004).  
> **Cakupan Dokumen Ini**: Khusus merangkum **18 kelas entitas baku OntoNotes 5.0** yang digunakan pada evaluasi penelitian skripsi ini, ditambah kategori penyaring gelar/jabatan **`TTL` (`NE-PER-N`)** yang digunakan pada tahap *prompt engineering* generasi data sintetis. Kategori tambahan di luar taksonomi penelitian (seperti `NE-CHA`, `NE-ADD`, `NE-PJT`, dan `NE-UC`) telah dieksklusi.

---

## 📑 Daftar Isi
1. [Ringkasan Pemetaan Kelas Entitas](#1-ringkasan-pemetaan-kelas-entitas)
2. [Pedoman Anotasi Entitas Nama (10 Kelas Utama)](#2-pedoman-anotasi-entitas-nama-10-kelas-utama)
   - [2.1 PERSON (`PER`)](#21-person-per)
   - [2.2 NORP (`NOR`)](#22-norp-nor)
   - [2.3 FACILITY (`FAC`)](#23-facility-fac)
   - [2.4 ORGANIZATION (`ORG`)](#24-organization-org)
   - [2.5 GPE (`GPE`)](#25-gpe-gpe)
   - [2.6 LOCATION (`LOC`)](#26-location-loc)
   - [2.7 PRODUCT (`PRD`)](#27-product-prd)
   - [2.8 EVENT (`EVT`)](#28-event-evt)
   - [2.9 WORK OF ART (`WOA`)](#29-work-of-art-woa)
   - [2.10 LAW (`LAW`)](#210-law-law)
3. [Pedoman Anotasi Entitas Numerik dan Temporal (8 Kelas Nilai)](#3-pedoman-anotasi-entitas-numerik-dan-temporal-8-kelas-nilai)
   - [3.1 LANGUAGE (`LAN`)](#31-language-lan)
   - [3.2 DATE (`DAT`)](#32-date-dat)
   - [3.3 TIME (`TIM`)](#33-time-tim)
   - [3.4 PERCENT (`PRC`)](#34-percent-prc)
   - [3.5 MONEY (`MON`)](#35-money-mon)
   - [3.6 QUANTITY (`QTY`)](#36-quantity-qty)
   - [3.7 ORDINAL (`ORD`)](#37-ordinal-ord)
   - [3.8 CARDINAL (`CRD`)](#38-cardinal-crd)
4. [Kategori Penampung Khusus: POST / JOB TITLE (`TTL` / `NE-PER-N`)](#4-kategori-penampung-khusus-post--job-title-ttl--ne-per-n)
5. [Kaidah Penentuan Batas Rentang Entitas (*Extent Rules*)](#5-kaidah-penentuan-batas-rentang-entitas-extent-rules)
6. [Kasus-Kasus Ambigu & Aturan Resolusi (*Problematic Cases*)](#6-kasus-kasus-ambigu--aturan-resolusi-problematic-cases)

---

## 1. Ringkasan Pemetaan Kelas Entitas

| Kode Skripsi | Tag OntoNotes 5.0 | Tag Dokumen Panduan | Deskripsi Singkat | Status dalam Skripsi |
| :---: | :---: | :---: | :--- | :--- |
| **`PER`** | `PERSON` | `NE-PER` | Nama orang (termasuk nama fiksi, panggilan unik, dan gelar kebangsawanan monarki). | 18 Kelas Baku Evaluasi |
| **`NOR`** | `NORP` | `NE-NRP` | Kebangsaan, kelompok etnis, afiliasi politik, dan kelompok agama (bentuk ajektiva/kolektif). | 18 Kelas Baku Evaluasi |
| **`FAC`** | `FACILITY` | `NE-FAC` | Bangunan buatan manusia, infrastruktur jalan, jembatan, bandara, monumen, dsb. | 18 Kelas Baku Evaluasi |
| **`ORG`** | `ORGANIZATION` | `NE-ORG` | Perusahaan, lembaga pemerintah, partai, institusi pendidikan, tim olahraga, dsb. | 18 Kelas Baku Evaluasi |
| **`GPE`** | `GPE` | `NE-GPE` | Entitas geopolitik administratif (negara, provinsi, kota, kabupaten, desa). | 18 Kelas Baku Evaluasi |
| **`LOC`** | `LOCATION` | `NE-LOC` | Lokasi non-administratif (sungai, gunung, danau, benua, kawasan regional). | 18 Kelas Baku Evaluasi |
| **`PRD`** | `PRODUCT` | `NE-PRO` | Produk fisik buatan, wahana transportasi (mobil, pesawat, roket), instrumen finansial. | 18 Kelas Baku Evaluasi |
| **`EVT`** | `EVENT` | `NE-EVT` | Peristiwa bersejarah, perang, bencana alam, festival, konferensi, ajang olahraga. | 18 Kelas Baku Evaluasi |
| **`WOA`** | `WORK_OF_ART` | `NE-ART` | Judul buku, film, lagu, lukisan, nama penghargaan, dan indeks bursa saham. | 18 Kelas Baku Evaluasi |
| **`LAW`** | `LAW` | `NE-LAW` | Dokumen hukum resmi, undang-undang, traktat internasional, pasal perundangan. | 18 Kelas Baku Evaluasi |
| **`LAN`** | `LANGUAGE` | `NE-LAN` | Nama bahasa lisan/tulisan manusia dan bahasa pemrograman komputer. | 18 Kelas Baku Evaluasi |
| **`DAT`** | `DATE` | `NE-DT` | Tanggal kalender, durasi $\ge 24$ jam, nama hari, bulan, tahun, abad, dan usia. | 18 Kelas Baku Evaluasi |
| **`TIM`** | `TIME` | `NE-TM` | Waktu jam, penunjuk waktu harian, dan rentang durasi $< 24$ jam. | 18 Kelas Baku Evaluasi |
| **`PRC`** | `PERCENT` | `NE-PC` | Nilai persentase beserta simbol `%` atau kata *"persen"*. | 18 Kelas Baku Evaluasi |
| **`MON`** | `MONEY` | `NE-MO` | Nilai nominal moneter beserta satuan mata uangnya. | 18 Kelas Baku Evaluasi |
| **`QTY`** | `QUANTITY` | `NE-QT` | Pengukuran fisik (panjang, jarak, berat, suhu, kecepatan, luas, volume data). | 18 Kelas Baku Evaluasi |
| **`ORD`** | `ORDINAL` | `NE-OD` | Angka tingkat / urutan (*pertama*, *kedua*, *ke-10*, *secondly*). | 18 Kelas Baku Evaluasi |
| **`CRD`** | `CARDINAL` | `NE-CD` | Angka kuantitas murni yang tidak masuk ke dalam kategori numerik lain. | 18 Kelas Baku Evaluasi |
| **`TTL`** | *(Non-OntoNotes)* | `NE-PER-N` | Nama jabatan, profesi, sapaan kehormatan formal (*President*, *Hakim*, *Menteri*). | Penampung Generasi (*Mapped to O*) |

---

## 2. Pedoman Anotasi Entitas Nama (10 Kelas Utama)

### 2.1 PERSON (`PER`)
- **Deskripsi**: Nama diri orang, termasuk nama depan, nama belakang, nama keluarga, tokoh fiksi, dan nama panggilan unik.
- **Cakupan Inklusi**:
  - Penanda generasi: `Jr.`, `IV`, `III`.
  - Gelar kebangsawanan kerajaan resmi yang melekat: `Queen Elizabeth II`, `Princess Diana`, `Sir Alex Ferguson`.
  - Karakter fiksi: `Charlie Brown`, `Harry Potter`.
  - Tokoh agama, nabi, dewa/dewi mitologi: ditandai sebagai `PER`.
- **Pengecualian / Unmarked**:
  - Sapaan formal kehormatan umum: `Mr.`, `Mrs.`, `Miss`, `Ms.`, `Dr.`, `Prof.` **TIDAK** dimasukkan ke dalam rentang `PER`.  
    *Contoh*: `Dr. [Brown]` $\rightarrow$ `Dr.` tidak ditandai, hanya `[Brown]` yang diberi label `PER`.
  - Kata sandang dan sebutan jabatan di depan nama: `the President [Kennedy]` $\rightarrow$ kata `President` masuk ke kategori `TTL`, hanya `[Kennedy]` yang masuk `PER`.
- **Contoh Baku**:
  - `(Ray Parker Jr.)`
  - `Dr. (Brown)` / `(St. Marks)`
  - `(Queen Elizabeth II)`
  - `(Princess Diana)`
  - `(Charlie Brown)`
  - `the President (Kennedy)`

---

### 2.2 NORP (`NOR`)
- **Deskripsi**: Kebangsaan (*Nationality*), kelompok etnis, kelompok keagamaan, dan afiliasi politik.
- **Kaidah Semantik**:
  - **Bentuk Adjektiva vs. Nominal**: Bentuk kata sifat (*adjectival forms*) dari nama tempat/negara selalu masuk ke `NOR`, sedangkan bentuk nomina tempat selalu masuk ke `GPE`.  
    *Contoh*: *"French"* adalah `NOR`, sedangkan *"France"* adalah `GPE`.
  - Penganut / kelompok agama: `Jewish`, `Muslims`, `Hindu`.
  - Anggota partai / afiliasi politik: `Democrats`, `Republicans`, `Socialist`.
- **Contoh Baku**:
  - `(European) euphoria`
  - `an (American) publishing group`
  - `He is (Jewish).`
  - `The (Hindu) newspaper`
  - `Three (Democrats)`
  - `the (Muslims)`
  - `France's (Socialist) government`

---

### 2.3 FACILITY (`FAC`)
- **Deskripsi**: Struktur fisik dan infrastruktur buatan manusia.
- **Cakupan Inklusi**:
  - Bangunan gedung, stadion, bandara, stasiun, infrastruktur transportasi (jembatan, jalan raya, terowongan), monumen bersejarah, kilang minyak, kebun binatang, lapangan golf, rumah sakit, pusat perbelanjaan.
  - Huruf kecil pada nama fasilitas tetap dimasukkan ke dalam rentang entitas jika merupakan bagian dari nama jalan/fasilitas resmi (misal: `Waterman street`).
- **Resolusi Konteks FAC vs. ORG**:
  - Nama fasilitas dapat menjadi `ORG` tergantung konteks pemakaian (apabila merujuk pada institusi/lembaga operasionalnya, bukan fisik bangunannya).
  - *Fisik Fasilitas*: *"We got out of the [City Library]."* $\rightarrow$ `FAC`
  - *Badan Organisasi*: *"[City Library] said that..."* $\rightarrow$ `ORG`
- **Contoh Baku**:
  - `the (Brooklyn Bridge)`
  - `(Yankee Stadium)`
  - `(Madison Avenue)`
  - `(42nd Street)` / `the (Eiffel Tower)`
  - `(Statue of Liberty)`
  - `(NE-FAC Waterman street)`

---

### 2.4 ORGANIZATION (`ORG`)
- **Deskripsi**: Nama perusahaan komersial, badan pemerintah, partai politik, lembaga pendidikan, tim olahraga, rumah sakit, museum, perpustakaan, organisasi keagamaan, dsb.
- **Kaidah Khusus**:
  - Fasilitas politik dan pemerintahan utama (seperti *White House*, *Pentagon*, *Capitol Hill*) ditandai sebagai `ORG`.
  - Bentuk adjektiva nama organisasi tetap ditandai sebagai `ORG` (misal: `A (Democratic) candidate`).
  - Nama surat kabar, majalah, dan situs web selalu ditandai sebagai `ORG`, baik saat merujuk pada korporasi penerbitnya maupun artefak terbitannya (`(The New York Times)`, `(YouTube)`, `(Wikipedia)`).
  - Nama kota yang merujuk pada tim olahraga ditandai sebagai `ORG` (misal: `a (Boston) shortstop`), sedangkan nama negara selalu tetap `GPE`.
  - Kata sandang *"The"* sebelum nama organisasi **TIDAK** disertakan dalam rentang entitas (misal: `... by The (New York Times)`).
- **Contoh Baku**:
  - `(IBM)` / `(Capitol Hill)`
  - `(White House)`
  - `(Democratic Party)`
  - `(Hilton Hotel)`
  - `(New York Stock Exchange)`
  - `(LIFE)` / `The (New York Times)`
  - `(YouTube)` / `a (Wikipedia) article`
  - `the (Japanese Government)`
  - `(Obama administration)`
  - *Head Sharing*: `(NE-ORG Scottish and Irish FAs)`

---

### 2.5 GPE (`GPE` — Geopolitical Entity)
- **Deskripsi**: Entitas wilayah administratif geografis yang memiliki pemerintahan/otoritas hukum (negara, negara bagian, provinsi, kota, kabupaten, distrik, desa).
- **Kaidah Khusus**:
  - Nama pulau ditandai sebagai `GPE` apabila pulau tersebut merupakan unit administratif resmi.
  - **Aturan Default**: Apabila Anda ragu apakah suatu entitas geografis merupakan unit administratif atau bukan, **tandai sebagai `GPE`** (bukan `LOC`).
  - Kata sandang *"the"* tidak dimasukkan (misal: `the (Philippines)`), kecuali jika pemisahan artikel melanggar aturan sintaksis Penn Treebank (`(the United States of America)`).
- **Contoh Baku**:
  - `a (US) company` / `(Paris)`
  - `southern (California)`
  - `the (United Kingdom)`
  - `(NE-GPE the United States of America)`
  - `(NE-GPE Normandy province)`

---

### 2.6 LOCATION (`LOC`)
- **Deskripsi**: Lokasi geografis alami dan nama tempat non-administratif (non-GPE).
- **Cakupan Inklusi**:
  - Benda langit dan planet (`Earth`, `Sun`, `Mars`).
  - Benua (`Europe`, `Asia`, `Latin America`).
  - Bentang alam alami: pegunungan, samudra, pesisir pantai, sungai, danau, perbatasan alam.
  - Kawasan regional atau kawasan kultural tanpa batas administratif resmi (`Middle East`, `Silicon Valley`, `Greenwich Village`).
- **Contoh Baku**:
  - `the (Hudson River)` / `(Europe)`
  - `(Brighton Beach)`
  - `(Long Island)` / `(Latin America)`
  - `(Silicon Valley)`
  - `(Earth)` / `the (Sun)`
  - `(Greenwich Village)`

---

### 2.7 PRODUCT (`PRD`)
- **Deskripsi**: Produk buatan manusia, baik komersial maupun non-komersial, termasuk wahana transportasi (mobil, pesawat, roket, kapal).
- **Kaidah Khusus**:
  - Jika penyebutan menggabungkan nama produsen dan nama produk, keduanya dipisahkan sebagai dua entitas independen: `((NE-ORG Ford) (NE-PRO Taurus))`.
  - Jika produk hanya dirujuk menggunakan nama produsennya (misal: *"Saya baru membeli sebuah Ford"*), maka kata tersebut ditandai sebagai `PRD` (`Two (NE-PRO Fords)`).
  - Berbeda dari definisi sempit OntoNotes lama, produk finansial dan layanan terstruktur (*financial products and services*) dapat disertakan di bawah kelas produk/layanan terdaftar.
- **Contoh Baku**:
  - `((NE-ORG Ford) (NE-PRO Taurus))`
  - `Two (NE-PRO Fords)`
  - `(Space Shuttle Discovery)`
  - `(Lotto 6)`

---

### 2.8 EVENT (`EVT`)
- **Deskripsi**: Peristiwa bernama yang terjadi dalam ruang dan waktu tertentu.
- **Cakupan Inklusi**:
  - Bencana alam bersejarah (badai, gempa bumi besar).
  - Revolusi, pertempuran, perang dunia (`Vietnam War`, `Mexican Revolution`).
  - Unjuk rasa berskala besar, konser musik tahunan.
  - Kejuaraan dan ajang olahraga resmi (`World Cup`, `F1`, `Olimpiade`).
- **Contoh Baku**:
  - `(Hurricane Hugo)`
  - `the (Vietnam War)`
  - `the (Mexican Revolution)`
  - `the (2016 World Cup)` / `(F1)`

---

### 2.9 WORK OF ART (`WOA`)
- **Deskripsi**: Judul karya cipta manusia (karya seni, sastra, dan publikasi).
- **Cakupan Inklusi**:
  - Judul buku, lagu, album musik, film bioskop, drama teater.
  - Nama penghargaan resmi (`Oscar`, `Nobel Prize`, `Academy Award for Best Actor`).
  - Indeks harga bursa saham (`Dow Jones Industrial Average`, `IHSG`).
  - Nama bendera atau simbol kebangsaan resmi (`the (Union Flag)`).
  - Nama waralaba/seri karya cipta (`Harry Potter series`).
- **Kaidah Kata Sandang**:
  - Apabila kata sandang (*article*) merupakan bagian permanen dari judul resmi, maka kata sandang **WAJIB dimasukkan** ke dalam rentang `WOA` (misal: `the film "(The Thing)"`).
- **Contoh Baku**:
  - `(Gone with the Wind)`
  - `(Oscar)` / `(Nobel Prize)`
  - `(Academy Award for Best Actor)`
  - `I read a (Harry Potter) book.`
  - `(Dow Jones Industrial Average)`
  - `the (Union Flag)`

---

### 2.10 LAW (`LAW`)
- **Deskripsi**: Dokumen hukum dan perundang-undangan resmi yang telah disahkan.
- **Cakupan Inklusi**:
  - Undang-undang, traktat, konvensi internasional, piagam konstitusi, pasal dan bab perundangan resmi.
- **Contoh Baku**:
  - `(Bill of Rights)`
  - `the (Johnson Act)`
  - `the (Warsaw Pact)`
  - `(Article II of the Constitution)`

---

## 3. Pedoman Anotasi Entitas Numerik dan Temporal (8 Kelas Nilai)

### 3.1 LANGUAGE (`LAN`)
- **Deskripsi**: Semua nama bahasa lisan atau tulisan manusia, termasuk bahasa pemrograman komputer resmi.
- **Contoh Baku**:
  - `a (Japanese) dictionary`
  - `written in (English)`
  - `developed in (Python)`

---

### 3.2 DATE (`DAT`)
- **Deskripsi**: Tanggal kalender mutlak atau relatif yang mewakili periode **24 jam atau lebih**.
- **Cakupan Inklusi**:
  - Hari spesifik, tanggal, bulan, kuartal, musim, tahun, dekade, abad.
  - Frasa usia (*age*), baik bertindak sebagai nomina, adjektiva, maupun adverbia (`aged 35`, `at the age of 65`, `50 years old`).
  - Preposisi rentang seperti *"from"*, *"to"*, dan *"between"* disertakan jika membentuk satu kesatuan rentang tanggal (`(from the 26th to 28th of April)`).
  - Ungkapan durasi tepat 24 jam dimasukkan ke `DAT`, **BUKAN** `TIM`.
- **Pengecualian / Unmarked**:
  - Kata temporal generik seperti *"now"*, *"past"*, *"future"*, serta adverbia relatif tanpa jangkar seperti *"recent"*, *"recently"*, *"previously"* **TIDAK DITANDAI**.
- **Contoh Baku**:
  - `(Dec. 31 2001)` / `(Monday)`
  - `(several years)` / `(today)`
  - `(every year)` / `(last month)`
  - `Mark, (aged 35), is …`
  - `at (the age of 65)` / `(50 years old)`
  - `(the previous quarter)` / `(Spring)`
  - `(a year ago)` / `(1990-1995)`
  - `(these days)` / `(the weekend)`
  - `(23, 24, and 28 January)`
  - `(the 21st century)` / `the (first day)`
  - *Head Sharing*: `June 7 and 8 => (NE-DT June 7 and 8)`

---

### 3.3 TIME (`TIM`)
- **Deskripsi**: Waktu harian atau rentang durasi yang **kurang dari 24 jam**.
- **Kaidah Khusus**:
  - Ungkapan jam dan waktu spesifik: `4 p.m.`, `08:30 WIB`.
  - Durasi pendek: `3 hours`, `the first 5 minutes`.
  - Bagian dari siklus harian: `morning`, `afternoon`, `night`.
  - Periode kuartal/babak pertandingan: `the second quarter`, `the 42nd minute`, `the first half`.
  - Keterangan zona waktu tambahan dalam tanda kurung **TIDAK** disertakan: `at (two p.m.) (UTC)`.
- **Contoh Baku**:
  - `(4 p.m.)` / `(this morning)`
  - `(3 hours)` / `(the first 5 minutes)`
  - `the (morning/afternoon/night)`
  - `the (second quarter)`
  - `the (42nd minute)` / `the (first half)`

---

### 3.4 PERCENT (`PRC`)
- **Deskripsi**: Nilai persentase numerik.
- **Kaidah Khusus**:
  - Simbol persen (`%`) atau kata *"percent"* / *"persen"* **WAJIB disertakan** di dalam batas rentang entitas.
- **Contoh Baku**:
  - `(60 %)`
  - `(12,5 persen)`

---

### 3.5 MONEY (`MON`)
- **Deskripsi**: Nilai moneter nominal.
- **Kaidah Khusus**:
  - Satuan mata uang atau simbol mata uang wajib tertulis eksplisit di dalam rentang.
  - Keterangan tarif agregat seperti *"per share"* atau *"per lembar saham"* **TIDAK** dimasukkan ke dalam rentang nominal uang.
- **Contoh Baku**:
  - `(50 yen)` / `($ 1000.00)`
  - `($3) per share`
  - `(3 dollars) per share`
  - `(Rp 500.000)`

---

### 3.6 QUANTITY (`QTY`)
- **Deskripsi**: Pengukuran fisik terkuantifikasi (panjang, jarak, luas, berat, suhu, kecepatan, daya, volume penyimpanan data).
- **Kaidah Khusus**:
  - Satuan unit pengukuran wajib tertulis eksplisit.
  - Kata pembatas perkiraan (*about*, *more than*) disertakan di dalam rentang.
- **Contoh Baku**:
  - `(about 5 miles)`
  - `the (100-m) race`
  - `(more than 4 acres)`
  - `(60 miles an hour)`
  - `(40 megabytes)`
  - *Aposisi*: `3550 pounds [16100 kg] => (NE-QT 3550 pounds) [(NE-QT 16100 kg)]`

---

### 3.7 ORDINAL (`ORD`)
- **Deskripsi**: Angka urutan atau tingkat numerik.
- **Cakupan Inklusi**:
  - Seluruh bilangan bertingkat, termasuk bentuk adverbial.
- **Contoh Baku**:
  - `(first)` / `(second)` / `(secondly)`
  - `(pertama)` / `(kedua)` / `(ke-10)`

---

### 3.8 CARDINAL (`CRD`)
- **Deskripsi**: Angka kuantitas murni yang tidak masuk ke dalam kategori numerik lain (bukan tanggal, waktu, uang, persentase, atau besaran fisik).
- **Cakupan Inklusi**:
  - Bilangan bulat, pecahan (*half*, *one-third*), angka butir daftar (*list item numbers*).
  - Skor pertandingan: `The Yankees won (4-1)`.
  - Pengubah kuantifikasi seperti *"only"* dan *"just"* dimasukkan ke dalam rentang.
- **Pengecualian / Unmarked**:
  - Ungkapan frekuensi tak terhitung seperti *"many times"* tidak ditandai.
- **Contoh Baku**:
  - `(half)` / `(hundreds)` / `(one-third)`
  - `(100) people` / `(7) goals`
  - `The Yankees won (4-1).`
  - `(10 times) more`

---

## 4. Kategori Penampung Khusus: POST / JOB TITLE (`TTL` / `NE-PER-N`)

> [!NOTE]
> Kategori ini berasal dari bagian **Newly Added Categories: NE-PER-N** pada pedoman Emi Maekawa (2018). Pada rancangan *pipeline* pembangkitan data sintetis skripsi, kategori ini diadopsi sebagai **`TTL`** untuk memisahkan gelar kehormatan dan sebutan jabatan resmi dari nama orang (`PER`).

- **Deskripsi**: Sebutan jabatan, posisi dinas pemerintahan, gelar politik, atau profesi resmi seseorang.
- **Kaidah Penandaan**:
  - Kata pembatas seperti *"former"* atau *"previous"* **TIDAK** disertakan.
  - Gelar kehormatan sosial umum (*Mr.*, *Dr.*, *Bapak*, *Ibu*) **TIDAK** ditandai sebagai `TTL`.
  - Sebutan juru bicara (*spokesman/spokeswoman*) hanya ditandai apabila bertugas pada lembaga instansi pemerintah resmi (`(White House spokesman)`), sedangkan juru bicara korporasi komersial tidak ditandai (`(ORG IBM) spokesman`).
- **Contoh Baku**:
  - `(ambassador to France)`
  - `(Baron) Brown`
  - `(Coach) Chip Kelly`
  - `(Western Australian district court judge)`
  - `(California governor)`
  - `(government attorney)`
  - `(FA chief executive)`
  - `(FIFA President)`
  - `(Foreign minister)`
  - `(Conservative Party leader)`
  - `(Member of Parliament)`
  - `(President) Bush` / `(US President) Bush`
  - `(President of the United States)`
  - `(Moroccan Prince)`
  - `Professor (NE-PER Brown)`
  - `(White House spokesman)`
  - `(White House adviser)`
- **Perlakuan pada Skripsi**:
  - Pada tahap evaluasi dan pelatihan model IndoBERT, seluruh label `TTL` ini dinormalisasi ke dalam label latar belakang **`O`** (*Outside*), sehingga model dievaluasi secara murni pada 18 kelas OntoNotes baku.

---

## 5. Kaidah Penentuan Batas Rentang Entitas (*Extent Rules*)

1. **Kata Sandang (*Articles: the, a, an*)**:
   - Secara umum **TIDAK DIMASUKKAN** ke dalam rentang entitas.
     - `the (NE-GPE Philippines)`
     - `... by The (NE-ORG New York Times)`
   - **Pengecualian**:
     - Pada karya seni (`WOA`), artikel yang menyatu dengan judul resmi **wajib dimasukkan**: `the film "(NE-ART The Thing)"`.
     - Pada ungkapan sintaksis tak terpisahkan: `(NE-GPE the United States of America)`.
2. **Tanda Baca dan Preposisi (*Punctuations and Prepositions*)**:
   - Frasa yang dipisahkan oleh tanda baca koma atau preposisi harus ditandai sebagai entitas terpisah:  
     `It happened in (NE-GPE Boston), (NE-GPE MA).`
   - *Pengecualian*: Pada tanggal dan waktu rentang (`from the 26th to 28th of April`), preposisi pembentuk rentang dimasukkan ke dalam entitas.
3. **Frasa dalam Tanda Kurung / Aposisi (*Bracketed Phrases: Apposition*)**:
   - Jika frasa dalam kurung merupakan aposisi dari entitas sebelumnya, keduanya ditandai sebagai dua entitas terpisah:
     - `(NE-ORG International Business Machine) [(NE-ORG IBM)]`
     - `(NE-QT 3550 pounds) [(NE-QT 16100 kg)]`
   - Jika tanda kurung memuat keterangan pelengkap (seperti zona waktu `UTC`), isi kurung **tidak dimasukkan**:  
     `at (NE-TM two p.m.) (UTC)`
4. **Huruf Kecil dalam Nama Entitas (*Lowercase Letters*)**:
   - Jika kata berhuruf kecil merupakan bagian dari nama resmi, kata tersebut **tetap dimasukkan** ke dalam rentang:
     - `(NE-ORG Central Intelligence agency)`
     - `(NE-ORG U.S. navy)`
     - `the (NE-LOC Hudson river)`
     - `(NE-FAC Waterman street)`
     - `(NE-GPE Normandy province)`
   - Jika kata tersebut bukan bagian nama resmi, jangan dimasukkan:  
     `(NE-ORG KGB) security agency`

---

## 6. Kasus-Kasus Ambigu & Aturan Resolusi (*Problematic Cases*)

1. **Penggabungan Inti Frasa (*Head Sharing*)**:
   - Apabila dua atau lebih entitas berbagi kata inti (*head*) yang sama (misalnya: *Scottish and Irish FAs*), seluruh frasa ditandai sebagai satu kesatuan entitas untuk menjaga struktur pohon sintaksis:
     - `(NE-ORG Scottish and Irish FAs)`
     - `(NE-DT June 7 and 8)`
2. **Ambiguitas Lokasi: `LOC` vs. `GPE`**:
   - Jika Anda menghadapi entitas geografis dan tidak yakin apakah entitas tersebut memiliki struktur administratif atau tidak, **tetapkan sebagai `GPE`**.
3. **Pemisahan Batas Tanggal dan Waktu**:
   - Frasa adverbial penjelas waktu spesifik disertakan, namun preposisi durasi (seperti *"for"* pada *"for two days"*) tidak disertakan:
     - `(NE-DT two years ago)`
     - `a (NE-DT two-year-old) girl`
     - `in (NE-TM two hours)` *(Bukan: `[in two hours]`)*
   - Jika waktu dan tanggal muncul berurutan, keduanya dipisahkan:  
     `at (NE-TM 3 p.m.) on (NE-DT Monday)`

---
*Dokumen ini disusun sebagai panduan anotasi acuan baku untuk standardisasi dataset NER Bahasa Indonesia berbasis taksonomi OntoNotes 5.0.*
