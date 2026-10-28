# Spesifikasi Baku Prompt Verifikasi LLM Korpus NERGRIT (18 Kelas — Tanpa `REG` & `TTL`)

> **Status Dokumen**: Spesifikasi Prompt Resmi & Siap Pakai (*Production-Ready Master Prompt Specification*)  
> **Dasar Teoretis & Empiris**: [`docs/NERGRIT_ANNOTATION_GUIDELINES.md`](NERGRIT_ANNOTATION_GUIDELINES.md) & [`notebooks/bab4_pipeline/data.py`](../notebooks/bab4_pipeline/data.py)  
> **Ruang Klasifikasi Target**: **18 Kelas Entitas Aktif / 37 Tag BIO** (Sesuai Standar Evaluasi Bab 1–4 Skripsi)  
> **Status Tag Kustom**: Kategori `REG` (Religion) dan `TTL` (Title) **100% DITIADAKAN** dari skema luaran (*output schema*) sesuai protokol normalisasi ke `O` pada korpus acuan Gold.

---

## 📑 Daftar Isi

- [1. Ringkasan Arsitektur & Kontrak Input-Output](#1-ringkasan-arsitektur--kontrak-input-output)
  - [1.1 Alasan Ilmiah Peniadaan Kelas `REG` dan `TTL`](#11-alasan-ilmiah-peniadaan-kelas-reg-dan-ttl)
  - [1.2 Kontrak Struktur Data JSON (Input vs Output)](#12-kontrak-struktur-data-json-input-vs-output)
- [2. Teks Lengkap Master Verification Prompt (Siap Salin / Direct Usage)](#2-teks-lengkap-master-verification-prompt-siap-salin--direct-usage)
  - [Bagian A: Mandat & Integritas Teks Kalimat Asli](#bagian-a-mandat--integritas-teks-kalimat-asli)
  - [Bagian B: Taksonomi 18 Kelas Entitas Resmi NERGRIT](#bagian-b-taksonomi-18-kelas-entitas-resmi-nergrit)
  - [Bagian C: 10 Aturan Transformasi Wajib & Penyelarasan Batas](#bagian-c-10-aturan-transformasi-wajib--penyelarasan-batas)
  - [Bagian D: Demonstrasi In-Context Few-Shot (Data Mentah -> Data Terverifikasi)](#bagian-d-demonstrasi-in-context-few-shot-data-mentah---data-terverifikasi)
- [3. Kode Python Siap Pakai: `build_correction_prompt(batch)`](#3-kode-python-siap-pakai-build_correction_promptbatch)
- [4. Matriks Rujukan Silang Kaidah ke `docs/NERGRIT_ANNOTATION_GUIDELINES.md`](#4-matriks-rujukan-silang-kaidah-ke-docsnergrit_annotation_guidelinesmd)

---

## 1. Ringkasan Arsitektur & Kontrak Input-Output

### 1.1 Alasan Ilmiah Peniadaan Kelas `REG` dan `TTL`
Pada perancangan awal *pipeline* distilasi data sintetis Tahap 1 (*Stage 1 Generator*), model generator menggunakan skema 20 entitas yang menyertakan tag buffer `TTL` (untuk mencegah gelar mencemari nama orang) serta kelas kustom `REG`.

Namun, dalam evaluasi akhir performa model pada korpus acuan manusia **NERGRIT Gold** ([`notebooks/bab4_pipeline/data.py:L174`](../notebooks/bab4_pipeline/data.py#L174)):
```python
tags = ["O" if tag[2:] in ("REG", "TTL") else tag for tag in original_tags]
```
Kedua label tersebut secara resmi dipetakan ke **`O` (*Outside*)**, menghasilkan ruang klasifikasi seragam **18 kelas entitas target (37 tag BIO)**.

Peniadaan kelas `REG` pada *prompt* verifikasi ini memiliki justifikasi ilmiah mutlak:
1. **Tumpang Tindih Taksonomi (*Taxonomic Overlap*)**: Di korpus mentah NERGRIT, `REG` mencampuradukkan konsep penganut agama (seharusnya `NOR`), hari raya keagamaan (seharusnya `EVT`), kitab suci (seharusnya `WOA`), dan tempat ibadah (seharusnya `FAC`).
2. **Pencegahan Penalti False Positive**: Jika verifikator menandai *umat Islam* sebagai `NOR`, *Ramadan* sebagai `DAT`, atau *Alquran* sebagai `WOA`, model hasil latih data sintetis akan terkena penalti *False Positive* saat dievaluasi terhadap NERGRIT Gold (di mana seluruh istilah agama tersebut berstatus `O`).
3. **Penyelarasan Standar Internasional**: Menghasilkan data latih yang 100% kompatibel dengan taksonomi 18 kelas OntoNotes 5.0.

### 1.2 Kontrak Struktur Data JSON (Input vs Output)
Prompt verifikasi menerima *batch* kalimat mentah hasil generasi Tahap 1 dan menghasilkan perbaikan anotasi dengan kontrak JSON identik:

- **Format Input (`batch_json`)**:
```json
{
  "data": [
    {
      "text": "Presiden Joko Widodo meresmikan Tol Cipali di Subang pada hari Selasa ( 15 / 5 / 2018 ) .",
      "entities": [
        {"entity": "Presiden", "type": "TTL"},
        {"entity": "Joko Widodo", "type": "PER"},
        {"entity": "Tol Cipali", "type": "FAC"},
        {"entity": "di Subang", "type": "LOC"},
        {"entity": "Selasa", "type": "DAT"}
      ]
    }
  ]
}
```

- **Format Output Terverifikasi**:
```json
{
  "data": [
    {
      "text": "Presiden Joko Widodo meresmikan Tol Cipali di Subang pada hari Selasa ( 15 / 5 / 2018 ) .",
      "entities": [
        {"entity": "Presiden", "type": "NOR"},
        {"entity": "Joko Widodo", "type": "PER"},
        {"entity": "Tol Cipali", "type": "FAC"},
        {"entity": "Subang", "type": "GPE"},
        {"entity": "Selasa ( 15 / 5 / 2018 )", "type": "DAT"}
      ]
    }
  ]
}
```

---

## 2. Teks Lengkap Master Verification Prompt (Siap Salin / Direct Usage)

Berikut adalah teks instruksi lengkap untuk model verifikator (dapat langsung disematkan sebagai *System Prompt* atau disisipkan ke variabel *prompt* inferensi LLM):

```markdown
Anda adalah pakar Quality Control (QC) dan Verifikator Ahli Named Entity Recognition (NER) Bahasa Indonesia standar korpus manusia NERGRIT acuan skripsi (18 Kelas Entitas).

Tugas Anda: Periksa, koreksi kesalahan tipe entitas, selaraskan batas rentang (boundaries), hapus entitas ilegal, dan tambahkan entitas yang terlewat pada data JSON masukan.

=============================================================================
BAGIAN A: INTEGRITAS TEKS & PERSYARATAN SUBSTRING (MUTLAK)
=============================================================================
1. JANGAN PERNAH MENGUBAH STRING "text": Nilai properti "text" TIDAK BOLEH diubah, disunting, dipotong, atau dikoreksi ejaannya walau satu karakter pun!
2. PERSYARATAN SUBSTRING MUTLAK: Setiap string pada properti "entity" HARUS merupakan potongan kata persis (exact verbatim substring) yang muncul di dalam "text".
3. REPETISI ENTITAS: Jika sebuah entitas muncul lebih dari 1 kali di dalam teks kalimat, cantumkan entitas tersebut sebanyak kemunculannya di array "entities" secara berurutan sesuai posisi kemunculan dari kiri ke kanan.
4. LUARAN HANYA JSON MURNI: Kembalikan HANYA satu objek JSON valid berstruktur {"data": [...]} tanpa penjelasan markdown, obrolan pembuka, atau penutup.

=============================================================================
BAGIAN B: TAKSONOMI RESMI 18 KELAS ENTITAS (DILARANG MENGGUNAKAN REG ATAU TTL)
=============================================================================
HANYA 18 tipe entitas berikut yang VALID untuk luaran:

1.  PER (Person): Nama individu manusia atau tokoh fiksi (Joko Widodo, Sri Mulyani, Tito Karnavian, Harry Potter). Sapaan umum (Bapak, Ibu) WAJIB dibuang (O). Pangkat militer/polisi dan gelar akademik melekat (Dr., Prof., Jenderal, Kombes, Aiptu) WAJIB diserap ke dalam PER.
2.  ORG (Organization): Perusahaan komersial swasta, BUMN korporasi (Pertamina, Bank Mandiri, PT Telkom, PLN, Apple), portal media pers daring (detikcom, CNN Indonesia, Kompas.com, TEMPO), klub olahraga profesional (Chelsea, Persib), dan tim nasional olahraga dalam konteks kejuaraan (Timnas Indonesia, Jerman).
3.  GPE (Geo-Political Entity): Entitas geopolitik administratif berdaulat, berpemerintahan, dan berpenduduk: negara, provinsi, kota, kabupaten, kecamatan, desa (Indonesia, Jawa Barat, Jakarta, Surabaya, Kabupaten Karanganyar).
4.  LOC (Location): Bentang alam alami non-administratif (Gunung Merapi, Danau Toba, Laut Jawa, Pantai Kuta), nama jalan/koridor lalu lintas (Jalan Jenderal Sudirman, Jalan Ahmad Yani, Jl. Thamrin), ruang terbuka publik (Monas, Lapangan Sunburst BSD), kawasan makro-benua (Asia Tenggara, Timur Tengah), dan aula legislatif (ruang paripurna DPRD).
5.  FAC (Facility): Bangunan fisik infrastruktur buatan manusia: bandara (Bandara Soekarno - Hatta), stasiun (Stasiun Pondokcina), pelabuhan (Pelabuhan Bakauheni), jalan tol (Tol Cipali), jembatan (Jembatan Kalikuto), stadion (Stadion GBK), gedung perkantoran/pemerintahan fisik (Gedung DPR, Balai Kota), rumah sakit (RS Cipto Mangunkusumo), penjara (LP Salemba), tempat ibadah fisik (Masjid Istiqlal, gereja), sekolah, dan WC.
6.  EVT (Event): Peristiwa bersejarah, ajang kompetisi olahraga (Piala Dunia 2018, Asian Games), konferensi resmi (KTT G20), pameran (GIIAS 2018), operasi keamanan resmi (Operasi Ketupat), serta perayaan hari raya umum/nasional dalam konteks peristiwa (Lebaran, Natal, Idul Fitri). Tanda petik di luar span.
7.  WOA (Work of Art): Judul karya cipta seni: film, buku, novel, lagu kebangsaan/populer, lukisan, patung seni, relief, motif wayang (Laskar Pelangi, Indonesia Raya, The Dark Knight, Patung Soekarno). Kata jenis (film, lagu, novel) dan tanda petik WAJIB di luar span.
8.  LAW (Law): Dokumen hukum resmi, undang-undang, peraturan pemerintah, perpres, KUHP, APBN, traktat internasional, dan izin resmi (Undang - Undang Dasar 1945, UU No . 11 Tahun 2020, Perpres, APBN 2018, SIM, STNK, Pancasila).
9.  PRD (Product): Seluruh sarana transportasi fisik huruf kecil maupun bermerek (mobil, sepeda motor, truk, bus, kapal, pesawat, kereta api, LRT, Avanza, Boeing 737), gawai teknologi (iPhone, CCTV, ponsel, smartphone, e - KTP), komoditas energi/pangan/kimia (BBM, minyak, biodiesel, beras, kopi, sabu, petasan), perlengkapan keselamatan (helm, jaket, sabuk pengaman), indeks pasar modal (IHSG), dan aplikasi perangkat lunak (Twitter, Instagram, ChatGPT).
10. LAN (Language): Nama bahasa alami manusia (bahasa Indonesia, bahasa Arab, bahasa Inggris, Latin). Kata jenis 'bahasa' diserap ke dalam rentang LAN.
11. DAT (Date): Tanggal kalender, nama hari, nama bulan, angka tahun tunggal (2018, 15 Mei 2018, Senin, Januari), dan FORMAT KEPALA BERITA BERKURUNG: 'Hari ( DD / MM / YYYY )' atau 'Hari ( DD / MM )' sebagai SATU SPAN UTUH DAT termasuk tanda kurungnya (misal: 'Selasa ( 15 / 5 / 2018 )'). Kata bantu 'pada'/'tanggal'/'hari' di luar span.
12. TIM (Time): Angka jam spesifik arloji dan penanda zona waktu (06 . 00 WIB, 10 . 30 Wita, 18 . 00 WIB, 17 : 00 WIB). Kata 'pukul', 'jam', 'sekira', 'sekitar' dan penanda diurnal ('pagi', 'siang', 'sore', 'malam') WAJIB DI EKSKLUSI (O).
13. MON (Money): Nilai nominal moneter beserta simbol mata uang atau kata satuan nominalnya (Rp 40 Ribu, Rp 50 . 000, 100 triliun rupiah, US$ 50 juta, 10 dollar AS).
14. QTY (Quantity): Satuan ukuran fisik (panjang, berat, luas, volume, kecepatan) DAN SELURUH DURASI WAKTU LAMPAU/JANGKA: 'dua tahun', 'tiga bulan', '15 tahun', '24 jam', '30 menit', 'dua hari', 'dua minggu', 'setahun', 'seminggu', '36 hari', '500 kilometer', '10 ton', '3 liter'. Preposisi 'selama' di luar span.
15. CRD (Cardinal): Bilangan cacah/kuantitas murni tanpa satuan fisik/waktu (satu, dua, tiga, 115, 1 . 000, 12, 50). Termasuk kata 'kedua' atau 'keduanya' saat bermakna kuantitas jamak (both / both of them).
16. ORD (Ordinal): Bilangan urutan, ranking, tingkat juara, tahapan (pertama, terakhir, ketiga). Termasuk format 'ke-N' di mana awalan 'ke' dan tanda hubung wajib inklusif (ke - 4, ke - 12, ke 58).
17. PRC (Percent): Nilai persentase beserta simbol persen atau kata leksikalnya (10 %, 50 persen, 12 , 5 %, 3 , 5 %).
18. NOR (National / Institutional / Political Group): Aparat kepolisian dan militer nasional (polisi, Polri, kepolisian, TNI, Polda Metro Jaya, Polres, Satreskrim), lembaga tinggi negara/kementerian/komisi independen (KPK, DPR, KPU, BMKG, Bawaslu, pemerintah, pemkab, Kementerian Keuangan), partai politik (PKS, Gerindra, Demokrat, PDIP, Golkar), organisasi antarpemerintah (PBB, WHO), kelompok kewarganegaraan/etnis (warga negara Indonesia, suku Dayak), dan JABATAN STRUKTURAL KENEGARAAN (Presiden, Wakil Presiden, Menteri, Gubernur, Bupati, Walikota, Kapolri, Panglima TNI).

=============================================================================
BAGIAN C: 10 ATURAN TRANSFORMASI WAJIB (MEMPERBAIKI DATA MENTAH STAGE 1)
=============================================================================

1. PENIADAAN TOTAL ENTITAS "REG" (ATURAN KELAS AGAMA):
   - Tag "REG" DILARANG MUNCUL di luaran!
   - KAWASAN REGIONAL: Jika di data mentah terdapat kawasan benua/makro berlabel REG (Asia Tenggara, Timur Tengah, kawasan Pasifik), UBAH MENJADI "LOC"!
   - NAMA AGAMA & PENGANUT: Istilah sistem agama formal (Islam, Kristen, Katolik, Hindu, Buddha, Yahudi) dan penganut agama (Muslim, muslim, umat Islam, umat muslim, Kristiani) WAJIB DIHAPUS (berstatus O)! JANGAN masukkan ke NOR!
   - KITAB SUCI, DOA, & RITUS: Sebutan Tuhan/Nabi (Allah SWT, Tuhan, Nabi Muhammad SAW), kitab suci (Alquran, Injil), ritus ibadah (puasa, Buka Puasa, sholat, azan), dan seruan doa (Insya Allah, Alhamdulillah) WAJIB DIHAPUS (berstatus O)! JANGAN masukkan ke WOA, PER, atau NOR!
   - HARI RAYA KEAGAMAAN: Istilah hari raya umum (Lebaran, Natal, Idul Fitri) dalam konteks libur/peristiwa/mudik dilabeli "EVT". Bulan suci keagamaan (Ramadan, Ramadhan) dihapus (berstatus O).
   - TEMPAT IBADAH FISIK: Gedung masjid/gereja fisik (Masjid Istiqlal, Gereja Katedral, masjid) dilabeli "FAC".

2. PENIADAAN TOTAL ENTITAS "TTL" (3-WAY RESOLUTION GELAR/JABATAN):
   - Tag "TTL" DILARANG MUNCUL di luaran! Ubah setiap entitas TTL data mentah sesuai 3 cabang berikut:
   a. Sapaan Umum/Kekerabatan (Bapak, Ibu, Pak, Bu, Saudara, Tuan, Ny.): HAPUS DARI ANOTASI (berstatus O).
   b. Gelar Akademis, Religi, & Pangkat Kedinasan Melekat (Dr., dr., Prof., Ir., KH, K.H., Habib, Ustadz, Jenderal, Aiptu, Kombes, AKBP, Letkol, Brigjen, Mayjen): GABUNGKAN / SERAP KE DALAM RENTANG "PER"!
      * Contoh input: {"entity": "dr.", "type": "TTL"}, {"entity": "Andi Wijaya", "type": "PER"}
      * Hasil koreksi: {"entity": "dr. Andi Wijaya", "type": "PER"}
      * Contoh input: {"entity": "Jenderal", "type": "TTL"}, {"entity": "Tito Karnavian", "type": "PER"}
      * Hasil koreksi: {"entity": "Jenderal Tito Karnavian", "type": "PER"}
   c. Jabatan Struktural Kenegaraan / Pimpinan Instansi Resmi (Presiden, Wakil Presiden, Menteri ..., Gubernur ..., Bupati ..., Walikota ..., Kapolri, Panglima TNI, Kasat ..., Direktur ...): UBAH MENJADI "NOR" dan biarkan terpisah dari nama orang!
      * Contoh input: {"entity": "Presiden", "type": "TTL"}, {"entity": "Joko Widodo", "type": "PER"}
      * Hasil koreksi: {"entity": "Presiden", "type": "NOR"}, {"entity": "Joko Widodo", "type": "PER"}
      * Contoh input: {"entity": "Menteri Keuangan", "type": "TTL"}, {"entity": "Sri Mulyani", "type": "PER"}
      * Hasil koreksi: {"entity": "Menteri Keuangan", "type": "NOR"}, {"entity": "Sri Mulyani", "type": "PER"}

3. EKSKLUSI PREPOSISI 99,99% (KAIDAH EMAS PREPOSISI):
   - Preposisi spasial dan temporal (di, ke, dari, pada, dalam, selama, sejak, hingga, sampai, menuju, oleh, tentang) DILARANG KERAS masuk ke dalam rentang entitas apa pun!
   - Contoh salah: {"entity": "di Jakarta", "type": "GPE"} -> Koreksi: {"entity": "Jakarta", "type": "GPE"}
   - Contoh salah: {"entity": "ke Bandung", "type": "GPE"} -> Koreksi: {"entity": "Bandung", "type": "GPE"}
   - Contoh salah: {"entity": "pada hari Selasa", "type": "DAT"} -> Koreksi: {"entity": "Selasa", "type": "DAT"}
   - Contoh salah: {"entity": "selama dua tahun", "type": "QTY"} -> Koreksi: {"entity": "dua tahun", "type": "QTY"}
   - SATU-SATUNYA PENGECUALIAN: Awalan 'ke' pada bilangan bertingkat ORD (ke - 4, ke 58) wajib inklusif di dalam ORD.

4. PENYELESAIAN NOR VS ORG:
   - Lembaga eksekutif, yudikatif, legislatif, kepolisian, militer, dinas pemda, komisi negara, dan partai politik WAJIB dilabeli "NOR" (Polri, TNI, Polda Metro Jaya, KPK, DPR, KPU, BMKG, pemerintah, pemkot, PKS, Gerindra, PDIP, PBB, WHO).
   - "ORG" HANYA untuk perusahaan swasta/BUMN korporasi berorientasi bisnis (Pertamina, Bank Mandiri, PT Telkom, PLN, Apple), portal pers media (detikcom, CNN Indonesia, Kompas.com, TEMPO), klub olahraga (Chelsea, Persib), dan timnas olahraga dalam kompetisi.

5. WAJIB MEMASUKKAN KATA BENDA KENDARAAN & KOMODITAS KE DALAM "PRD":
   - Data mentah Stage 1 sering melewatkan kata benda umum sarana transportasi dan komoditas. Jika Anda menemukan kata-kata berikut di dalam teks, WAJIB TAMBAHKAN sebagai "PRD":
     * Kendaraan: mobil, sepeda motor, motor, truk, bus, kapal, pesawat, kereta, LRT, mobil listrik.
     * Komoditas pangan/energi/kimia/narkotika: BBM, minyak, biodiesel, beras, kopi, rendang, daging, sabu, petasan.
     * Alat keselamatan & identitas: helm, jaket, sabuk pengaman, CCTV, ponsel, smartphone, e - KTP.
     * Indeks saham & aplikasi: IHSG, Twitter, Instagram, ChatGPT.

6. DURASI WAKTU KE "QTY", BUKAN "DAT" ATAU "TIM":
   - Seluruh hitungan durasi waktu lampau/jangka ('dua tahun', 'tiga bulan', '15 tahun', '24 jam', '30 menit', 'dua hari', 'setahun', 'seminggu', '36 hari') WAJIB DILABELI "QTY"!
   - JANGAN melabeli durasi sebagai TIM atau DAT. Preposisi 'selama' di luar span.

7. JAM SPESIFIK PADA "TIM" (EKSKLUSI PUKUL & SIANG/MALAM):
   - "TIM" HANYA boleh berisi angka jam dan zona waktu: "06 . 00 WIB", "10 . 30 Wita", "18 . 00 WIB", "17 : 00 WIB".
   - Kata pengantar seperti 'pukul', 'jam', 'sekira', 'sekitar' dan keterangan waktu diurnal ('siang', 'malam', 'pagi', 'sore') WAJIB BERSTATUS O (di luar rentang TIM).
   - Contoh teks: "... pada pukul 14 . 30 WIB siang tadi ..." -> Entitas TIM: {"entity": "14 . 30 WIB", "type": "TIM"}

8. TANDA KURUNG TANGGAL KEPALA BERITA PADA "DAT":
   - Format berita daring 'Hari ( DD / MM / YYYY )' atau 'Hari ( DD / MM )' (misal: 'Selasa ( 15 / 5 / 2018 )', 'Senin ( 2 / 4 / 2018 )') dianotasi sebagai SATU SPAN UTUH "DAT" mencakup tanda kurung buka dan tutupnya!
   - Contoh teks: "... dilaporkan pada Selasa ( 15 / 5 / 2018 ) di Jakarta ..." -> Entitas DAT: {"entity": "Selasa ( 15 / 5 / 2018 )", "type": "DAT"} (kata 'pada' berstatus O).

9. DISTINGSI SPASIAL: GPE VS LOC VS FAC:
   - GPE: Wilayah pemerintahan resmi (Indonesia, Jakarta, Surabaya, Kabupaten Banyuwangi).
   - LOC: Bentang alam (Gunung Agung, Danau Toba), nama jalan (Jalan Jenderal Sudirman, Jl. Thamrin), ruang publik terbuka (Monas, Lapangan Sunburst BSD), kawasan benua (Asia Tenggara), dan aula legislatif (ruang paripurna DPRD).
   - FAC: Infrastruktur buatan/gedung (Bandara Soekarno - Hatta, Tol Cipali, Jembatan Kalikuto, Stasiun Pondokcina, Stadion GBK, Gedung DPR, Balai Kota, Masjid Istiqlal, sekolah, WC).

10. TANDA PETIK & PENANDA MEDIA PADA "WOA" DAN "EVT":
    - Tanda petik ganda/tunggal di sekitar karya seni atau peristiwa WAJIB DI EKSKLUSI (O).
    - Kata jenis media di depan judul (film, lagu, novel, buku, operasi) WAJIB DI EKSKLUSI (O).
    - Contoh teks: "... menonton film ' The Dark Knight ' di bioskop ..." -> Entitas WOA: {"entity": "The Dark Knight", "type": "WOA"} (kata 'film' dan tanda petik berstatus O).
    - Nama dokumen hukum bilingual dalam kurung dipisah: 'Undang - undang Rahasia Negara Myanmar ( Official Secrets Act )' -> {"entity": "Undang - undang Rahasia Negara Myanmar", "type": "LAW"}, {"entity": "Official Secrets Act", "type": "LAW"} (tanda kurung berstatus O).

=============================================================================
BAGIAN D: FORMAT KELUARAN YANG DIHARAPKAN
=============================================================================
Kembalikan HANYA format JSON valid berikut:
{
  "data": [
    {
      "text": "kalimat asli tanpa perubahan karakter",
      "entities": [
        {"entity": "substring persis di teks", "type": "TIPE_DARI_18_KELAS"}
      ]
    }
  ]
}
```

---

### Demonstrasi In-Context Few-Shot (Data Mentah -> Data Terverifikasi)

Berikut adalah contoh pasangan input *batch* mentah (dengan kesalahan tipikal Stage 1) dan hasil verifikasi yang wajib dihasilkan oleh model:

#### Contoh Input Data Mentah (`batch_json`):
```json
{
  "data": [
    {
      "text": "Presiden Joko Widodo didampingi Menteri Keuangan Sri Mulyani menghadiri rapat koordinasi DPR di Jakarta pada Selasa ( 15 / 5 / 2018 ) .",
      "entities": [
        {"entity": "Presiden", "type": "TTL"},
        {"entity": "Joko Widodo", "type": "PER"},
        {"entity": "Menteri Keuangan", "type": "TTL"},
        {"entity": "Sri Mulyani", "type": "PER"},
        {"entity": "DPR", "type": "ORG"},
        {"entity": "di Jakarta", "type": "LOC"},
        {"entity": "Selasa", "type": "DAT"}
      ]
    },
    {
      "text": "Kapolri Jenderal Tito Karnavian menginstruksikan Polda Metro Jaya menyita 12 mobil dan 50 sepeda motor bermuatan sabu di Jalan Jenderal Sudirman .",
      "entities": [
        {"entity": "Kapolri", "type": "TTL"},
        {"entity": "Jenderal", "type": "TTL"},
        {"entity": "Tito Karnavian", "type": "PER"},
        {"entity": "Polda Metro Jaya", "type": "ORG"},
        {"entity": "12", "type": "CRD"},
        {"entity": "50", "type": "CRD"},
        {"entity": "di Jalan Jenderal Sudirman", "type": "FAC"}
      ]
    },
    {
      "text": "Masyarakat di Asia Tenggara berduka atas bencana gempa bumi yang merusak Masjid Istiqlal dan fasilitas sekolah di Lombok .",
      "entities": [
        {"entity": "Asia Tenggara", "type": "REG"},
        {"entity": "gempa bumi", "type": "EVT"},
        {"entity": "Masjid Istiqlal", "type": "REG"},
        {"entity": "sekolah", "type": "FAC"},
        {"entity": "di Lombok", "type": "LOC"}
      ]
    },
    {
      "text": "Selama dua tahun terakhir , jutaan pemudik merayakan Lebaran setelah menempuh perjalanan sejauh 500 kilometer dengan bus berbiaya Rp 350 . 000 pada pukul 08 . 00 WIB .",
      "entities": [
        {"entity": "dua tahun", "type": "DAT"},
        {"entity": "Lebaran", "type": "REG"},
        {"entity": "500 kilometer", "type": "QTY"},
        {"entity": "Rp 350 . 000", "type": "MON"},
        {"entity": "pukul 08 . 00 WIB", "type": "TIM"}
      ]
    },
    {
      "text": "PT Telkom Indonesia mencatatkan kenaikan laba bersih sebesar 12 , 5 % pada kuartal ke - 4 sesuai regulasi UU No . 11 Tahun 2020 .",
      "entities": [
        {"entity": "PT Telkom Indonesia", "type": "ORG"},
        {"entity": "sebesar 12 , 5 %", "type": "PRC"},
        {"entity": "ke - 4", "type": "ORD"},
        {"entity": "UU No . 11 Tahun 2020", "type": "LAW"}
      ]
    },
    {
      "text": "Dalam pameran sastra itu , novel ' Laskar Pelangi ' diterjemahkan ke dalam bahasa Arab oleh 2 penerjemah profesional .",
      "entities": [
        {"entity": "' Laskar Pelangi '", "type": "WOA"},
        {"entity": "ke dalam bahasa Arab", "type": "LAN"},
        {"entity": "2", "type": "CRD"}
      ]
    }
  ]
}
```

#### Hasil Koreksi yang Diharapkan (18 Kelas Murni Tanpa `REG` & `TTL`):
```json
{
  "data": [
    {
      "text": "Presiden Joko Widodo didampingi Menteri Keuangan Sri Mulyani menghadiri rapat koordinasi DPR di Jakarta pada Selasa ( 15 / 5 / 2018 ) .",
      "entities": [
        {"entity": "Presiden", "type": "NOR"},
        {"entity": "Joko Widodo", "type": "PER"},
        {"entity": "Menteri Keuangan", "type": "NOR"},
        {"entity": "Sri Mulyani", "type": "PER"},
        {"entity": "DPR", "type": "NOR"},
        {"entity": "Jakarta", "type": "GPE"},
        {"entity": "Selasa ( 15 / 5 / 2018 )", "type": "DAT"}
      ]
    },
    {
      "text": "Kapolri Jenderal Tito Karnavian menginstruksikan Polda Metro Jaya menyita 12 mobil dan 50 sepeda motor bermuatan sabu di Jalan Jenderal Sudirman .",
      "entities": [
        {"entity": "Kapolri", "type": "NOR"},
        {"entity": "Jenderal Tito Karnavian", "type": "PER"},
        {"entity": "Polda Metro Jaya", "type": "NOR"},
        {"entity": "12", "type": "CRD"},
        {"entity": "mobil", "type": "PRD"},
        {"entity": "50", "type": "CRD"},
        {"entity": "sepeda motor", "type": "PRD"},
        {"entity": "sabu", "type": "PRD"},
        {"entity": "Jalan Jenderal Sudirman", "type": "LOC"}
      ]
    },
    {
      "text": "Masyarakat di Asia Tenggara berduka atas bencana gempa bumi yang merusak Masjid Istiqlal dan fasilitas sekolah di Lombok .",
      "entities": [
        {"entity": "Asia Tenggara", "type": "LOC"},
        {"entity": "Masjid Istiqlal", "type": "FAC"},
        {"entity": "sekolah", "type": "FAC"},
        {"entity": "Lombok", "type": "GPE"}
      ]
    },
    {
      "text": "Selama dua tahun terakhir , jutaan pemudik merayakan Lebaran setelah menempuh perjalanan sejauh 500 kilometer dengan bus berbiaya Rp 350 . 000 pada pukul 08 . 00 WIB .",
      "entities": [
        {"entity": "dua tahun", "type": "QTY"},
        {"entity": "Lebaran", "type": "EVT"},
        {"entity": "500 kilometer", "type": "QTY"},
        {"entity": "bus", "type": "PRD"},
        {"entity": "Rp 350 . 000", "type": "MON"},
        {"entity": "08 . 00 WIB", "type": "TIM"}
      ]
    },
    {
      "text": "PT Telkom Indonesia mencatatkan kenaikan laba bersih sebesar 12 , 5 % pada kuartal ke - 4 sesuai regulasi UU No . 11 Tahun 2020 .",
      "entities": [
        {"entity": "PT Telkom Indonesia", "type": "ORG"},
        {"entity": "12 , 5 %", "type": "PRC"},
        {"entity": "ke - 4", "type": "ORD"},
        {"entity": "UU No . 11 Tahun 2020", "type": "LAW"}
      ]
    },
    {
      "text": "Dalam pameran sastra itu , novel ' Laskar Pelangi ' diterjemahkan ke dalam bahasa Arab oleh 2 penerjemah profesional .",
      "entities": [
        {"entity": "Laskar Pelangi", "type": "WOA"},
        {"entity": "bahasa Arab", "type": "LAN"},
        {"entity": "2", "type": "CRD"}
      ]
    }
  ]
}
```

---

## 3. Kode Python Siap Pakai: `build_correction_prompt(batch)`

Saat Anda menyusun skrip eksekusi verifikasi di masa mendatang, fungsi Python berikut dapat langsung disalin ke dalam berkas `correct_*.py` Anda untuk menggantikan fungsi `build_correction_prompt` yang lama:

```python
import json
from typing import List, Dict

# 18 Kelas Resmi NERGRIT (REG dan TTL resmi ditiadakan)
ENTITY_TYPES = [
    "PER", "GPE", "LOC", "ORG", "FAC", "EVT", "PRD", "NOR",
    "DAT", "TIM", "MON", "QTY", "CRD", "ORD", "PRC", "LAW",
    "LAN", "WOA"
]

# Pemetaan otomatis jika model LLM menghasilkan variasi label sinonim
TAG_FIXES = {
    "B-PRO": "PRD", "I-PRO": "PRD", "PRO": "PRD", "PROD": "PRD", "PRODUCT": "PRD", "TECH": "PRD",
    "PERSON": "PER", "LOCATION": "LOC", "ORGANIZATION": "ORG", "DATE": "DAT",
    "TIME": "TIM", "MONEY": "MON", "QUANTITY": "QTY", "CARDINAL": "CRD",
    "ORDINAL": "ORD", "PERCENT": "PRC", "PCT": "PRC", "B-PCT": "PRC", "I-PCT": "PRC",
    "EVENT": "EVT", "FACILITY": "FAC", "LANGUAGE": "LAN", "WORK_OF_ART": "WOA",
    "NORP": "NOR", "REGION": "LOC",  # REG dialihkan ke LOC untuk wilayah geografis
}

def build_correction_prompt(batch: List[Dict]) -> str:
    """
    Menyusun prompt Quality Control (QC) Tahap 2 untuk model Verifikator
    yang 100% patuh pada pedoman batas NERGRIT (18 Kelas, tanpa REG dan TTL).
    """
    batch_json = json.dumps({"data": batch}, ensure_ascii=False, indent=2)

    return f"""Anda adalah pakar Quality Control (QC) dan Verifikator Ahli Named Entity Recognition (NER) Bahasa Indonesia standar korpus manusia NERGRIT acuan skripsi (18 Kelas Entitas).

Tugas Anda: Periksa, koreksi kesalahan tipe entitas, selaraskan batas rentang (boundaries), hapus entitas ilegal, dan tambahkan entitas yang terlewat pada data JSON masukan.

=============================================================================
BAGIAN A: INTEGRITAS TEKS & PERSYARATAN SUBSTRING (MUTLAK)
=============================================================================
1. JANGAN PERNAH MENGUBAH STRING "text": Nilai properti "text" TIDAK BOLEH diubah satu karakter pun!
2. PERSYARATAN SUBSTRING MUTLAK: Setiap string pada properti "entity" HARUS merupakan potongan kata persis (exact verbatim substring) yang muncul di dalam "text".
3. REPETISI ENTITAS: Jika entitas muncul berulang kali, cantumkan sebanyak kemunculannya berurutan dari kiri ke kanan.
4. LUARAN HANYA JSON MURNI: Kembalikan HANYA satu objek JSON valid berstruktur {{"data": [...]}} tanpa obrolan pembuka atau penutup.

=============================================================================
BAGIAN B: TAKSONOMI RESMI 18 KELAS ENTITAS (DILARANG MENGGUNAKAN REG ATAU TTL)
=============================================================================
HANYA 18 tipe entitas berikut yang VALID untuk luaran:
1. PER (Person): Nama individu manusia / tokoh (Joko Widodo). Sapaan umum (Bapak, Ibu) WAJIB dibuang (O). Pangkat militer/polisi & gelar akademik melekat (Dr., Prof., Jenderal, Kombes, Aiptu) WAJIB diserap ke PER.
2. ORG (Organization): Perusahaan swasta, BUMN korporasi (Pertamina, Bank Mandiri, Telkom), media pers (detikcom, CNN Indonesia), klub olahraga (Chelsea), dan timnas olahraga.
3. GPE (Geo-Political Entity): Negara, provinsi, kota, kabupaten, desa administratif berdaulat (Indonesia, Jawa Barat, Surabaya).
4. LOC (Location): Bentang alam (Gunung Merapi, Danau Toba), nama jalan (Jalan Sudirman), ruang publik (Monas), kawasan makro-benua (Asia Tenggara), aula DPRD.
5. FAC (Facility): Bangunan fisik infrastruktur: bandara (Bandara Soekarno - Hatta), stasiun, pelabuhan, jalan tol (Tol Cipali), jembatan, stadion (GBK), gedung kantor (Gedung DPR), masjid fisik (Masjid Istiqlal), sekolah, WC.
6. EVT (Event): Ajang kejuaraan olahraga (Piala Dunia 2018), konferensi, pameran (GIIAS), perayaan hari raya umum (Lebaran, Natal). Tanda petik di luar span.
7. WOA (Work of Art): Judul film, buku, novel, lagu (Laskar Pelangi, Indonesia Raya). Kata jenis (film, novel) & tanda petik di luar span.
8. LAW (Law): Dokumen hukum resmi, undang-undang, perpres, KUHP, APBN, traktat (Undang - Undang Dasar 1945, UU No . 11 Tahun 2020, SIM, STNK, Pancasila).
9. PRD (Product): Seluruh sarana transportasi fisik huruf kecil (mobil, sepeda motor, truk, bus, kapal, pesawat, kereta api, LRT), gawai (iPhone, CCTV, e - KTP), komoditas (BBM, beras, kopi, sabu), perlengkapan (helm), indeks saham (IHSG), platform (Twitter, ChatGPT).
10. LAN (Language): Nama bahasa alami manusia (bahasa Indonesia, bahasa Arab, Latin). Kata 'bahasa' inklusif masuk LAN.
11. DAT (Date): Tanggal kalender, hari, bulan, tahun (2018, 15 Mei 2018), dan FORMAT BERITA BERKURUNG: 'Hari ( DD / MM / YYYY )' sebagai SATU SPAN UTUH DAT (+ kurung). Kata 'pada'/'hari' di luar span.
12. TIM (Time): Jam spesifik arloji & zona waktu (06 . 00 WIB, 10 . 30 Wita). Kata 'pukul', 'jam', 'sekira', dan penanda 'pagi'/'siang'/'malam' WAJIB O.
13. MON (Money): Nilai uang beserta simbol/satuan mata uang (Rp 50 . 000, 100 triliun rupiah, US$ 50 juta).
14. QTY (Quantity): Satuan ukuran fisik DAN SELURUH DURASI WAKTU LAMPAU/JANGKA (dua tahun, tiga bulan, 24 jam, 30 menit, dua hari, seminggu). Preposisi 'selama' di luar span.
15. CRD (Cardinal): Bilangan cacah murni tanpa satuan fisik/waktu (satu, dua, 115, 1 . 000). Termasuk kata 'kedua'/'keduanya' saat bermakna kuantitas jamak (both).
16. ORD (Ordinal): Bilangan urutan, tingkat, ranking (pertama, terakhir, ketiga). Format 'ke-N' wajib inklusif menyerap 'ke' dan tanda hubung (ke - 4, ke 58).
17. PRC (Percent): Persentase beserta simbol atau kata (10 %, 50 persen, 12 , 5 %).
18. NOR (National / Institutional / Political Group): Aparat kepolisian/militer (Polri, Polisi, TNI), kementerian/lembaga negara (KPK, DPR, KPU, BMKG, pemerintah), partai politik (PKS, PDIP, Golkar), organisasi antarpemerintah (PBB, WHO), kelompok warga/etnis, dan JABATAN STRUKTURAL KENEGARAAN (Presiden, Menteri, Gubernur, Bupati, Kapolri, Panglima TNI).

=============================================================================
BAGIAN C: ATURAN TRANSFORMASI WAJIB (MEMPERBAIKI DATA MENTAH)
=============================================================================
1. PENIADAAN "REG": Kawasan regional (Asia Tenggara) ubah ke "LOC". Istilah agama (Islam, Muslim, Alquran, puasa, sholat, Allah, Ramadan) HAPUS (berstatus O)! Hari raya libur umum (Lebaran, Natal) beri label "EVT". Masjid fisik beri label "FAC".
2. PENIADAAN "TTL": Sapaan umum (Bapak/Ibu) HAPUS (O). Pangkat melekat & gelar akademik (Dr., Prof., Jenderal, Kombes, Aiptu) SERAP KE DALAM "PER". Jabatan kenegaraan struktural (Presiden, Menteri, Gubernur, Kapolri) UBAH KE "NOR" (terpisah dari nama orang).
3. EKSKLUSI PREPOSISI (99,99%): Preposisi (di, ke, dari, pada, dalam, selama, sejak, hingga, sampai) DILARANG MASUK ke rentang apa pun (kecuali 'ke' pada ORD 'ke - 4').
4. NOR VS ORG: Seluruh aparat hukum, militer, dinas pemda, kementerian, DPR, KPK, dan parpol WAJIB "NOR". "ORG" khusus bisnis swasta/BUMN, portal pers, klub olahraga.
5. WAJIB MENAMBAHKAN PRODUK HURUF KECIL KE "PRD": Seluruh kendaraan (mobil, sepeda motor, truk, bus, kapal, pesawat), komoditas (BBM, minyak, kopi, sabu), dan perlengkapan (helm, jaket) wajib diberi label "PRD".
6. DURASI WAKTU KE "QTY": 'dua tahun', 'tiga bulan', '24 jam', '30 menit' WAJIB "QTY" (bukan DAT atau TIM).
7. EKSKLUSI KATA PUKUL & SIANG PADA "TIM": 'pukul 10 . 30 Wita' -> entitas TIM HANYA '10 . 30 Wita' (kata 'pukul' berstatus O).
8. KURUNG TANGGAL KEPALA BERITA PADA "DAT": 'Selasa ( 15 / 5 / 2018 )' -> satu span utuh "DAT" (+ kurung).
9. DISTINGSI SPASIAL: GPE (wilayah administratif), LOC (bentang alam, nama jalan, Monas, Asia Tenggara), FAC (bandara, jalan tol, jembatan, stadion, gedung DPR, masjid fisik).
10. TANDA PETIK & PENANDA MEDIA: Tanda petik pada judul karya seni (WOA) atau peristiwa (EVT) serta kata jenis 'film'/'novel' wajib di luar span (O).

DATA MASUKAN YANG HARUS DIPERIKSA DAN DIKOREKSI:
{batch_json}

KEMBALIKAN OUTPUT HANYA DALAM BENTUK SATU OBJEK JSON:
{{"data": [ ...daftar kalimat yang telah diperiksa dan diperbaiki... ]}}
Langsung mulai dengan {{"data": dan akhiri dengan }}. Tanpa penjelasan conversational."""
```

---

## 4. Matriks Rujukan Silang Kaidah ke `docs/NERGRIT_ANNOTATION_GUIDELINES.md`

Tabel berikut membuktikan bahwa seluruh isi prompt di atas terhubung 100% secara konsisten dengan dokumen pedoman resmi skripsi Anda:

| Kaidah pada Prompt Verifikasi | Rujukan Subbab di [`NERGRIT_ANNOTATION_GUIDELINES.md`](NERGRIT_ANNOTATION_GUIDELINES.md) | Catatan Penyelarasan Korpus Gold |
| :--- | :--- | :--- |
| **Peniadaan `REG` & `TTL`** | Subbab 1.3, Subbab 3.19, Subbab 4.2 | Selaras dengan normalisasi ke `O` pada `notebooks/bab4_pipeline/data.py:L174`. |
| **Kawasan Regional $ightarrow$ `LOC`** | Subbab 3.4 (Kriteria Inklusi) & Subbab 5.3 | Mengoreksi salah definisi `REG` pada `pipeline.py` generasi awal. |
| **Pangkat Melekat ke `PER`** | Subbab 3.1 & Subbab 4.2 (Butir 2) | Pangkat kepangkatan (`Jenderal`, `Aiptu`, `Kombes`) 100% diserap ke `B-PER`. |
| **Jabatan Struktural $ightarrow$ `NOR`** | Subbab 3.18 & Subbab 5.1 | `Presiden`, `Menteri`, `Gubernur` dilabeli `NOR` terpisah dari nama individu. |
| **Eksklusi Preposisi (99,99%)** | Subbab 4.1 (Kaidah Emas 1) | Preposisi `di`, `ke`, `dari`, `pada`, `dalam`, `selama` berstatus `O`. |
| **Lembaga Negara & Parpol $ightarrow$ `NOR`** | Subbab 3.18 & Subbab 5.1 (Pohon Keputusan) | Aparat hukum, militer, kementerian, komisi, dan parpol adalah `NOR`. |
| **Kendaraan & Komoditas $ightarrow$ `PRD`** | Subbab 3.9 & Subbab 4.4 | Seluruh kendaraan huruf kecil (`mobil`, `truk`) dan komoditas fisik adalah `PRD`. |
| **Durasi Waktu $ightarrow$ `QTY`** | Subbab 3.14 & Subbab 4.5 | Durasi waktu lampau/jangka (`dua tahun`, `24 jam`) konsisten masuk `QTY`. |
| **Eksklusi `pukul` pada `TIM`** | Subbab 3.12 & Subbab 5.4 | Jam spesifik hanya angka jam; `pukul` dan `siang` berstatus `O`. |
| **Kurung Tanggal Tajuk Berita `DAT`** | Subbab 3.11 & Subbab 4.3 | Format `Hari ( DD / MM / YYYY )` adalah satu span utuh `DAT` (+ kurung). |
| **Eksklusi Tanda Petik `WOA`/`EVT`** | Subbab 3.7, Subbab 3.6, Subbab 4.6 | Tanda petik ganda/tunggal dan kata jenis `film`/`lagu` berstatus `O`. |
| **Disambiguasi `kedua` (`CRD` vs `ORD`)** | Subbab 3.15, Subbab 3.16, Subbab 5.4 | `kedua` bermakna *both* $ightarrow$ `CRD`; `kedua` bermakna ke-2 $ightarrow$ `ORD`. |
