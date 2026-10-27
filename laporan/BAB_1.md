# BAB 1 PENDAHULUAN


## 1.1 Latar Belakang

Perkembangan teknologi Kecerdasan Buatan (*Artificial Intelligence* / AI) telah membawa perubahan signifikan dalam cara mesin memproses informasi komputasional. Salah satu cabang AI yang mengalami perkembangan yang sangat pesat adalah Pemrosesan Bahasa Alami (*Natural Language Processing* / NLP). NLP memampukan komputer untuk tidak sekadar membaca, melainkan menafsirkan dan mengekstraksi makna dari sejumlah besar data teks tidak terstruktur yang terus diproduksi setiap harinya. Kemampuan mengekstraksi informasi (*information extraction*) ini menjadi fondasi penting bagi berbagai sistem interaksi manusia-komputer yang cerdas.

Dalam hierarki tugas pemahaman teks pada NLP, *Named Entity Recognition* (NER) menempati posisi sebagai salah satu pilar utama. NER bertujuan untuk mengidentifikasi dan mengklasifikasikan potongan teks (entitas bernama) seperti nama orang, lokasi geografis, organisasi, dan waktu ke dalam kategori semantik yang telah terdefinisi. Penguasaan ekstraksi entitas ini sangat penting karena bertindak sebagai landasan bagi aplikasi lanjutan seperti sistem tanya jawab (*question answering*), penerjemahan mesin (*machine translation*), serta perangkuman teks otomatis (*text summarization*) (Li et al., 2020). Untuk mencapai tingkat kinerja identifikasi yang optimal, model NER saat ini umumnya dibangun di atas algoritma berbasis *deep learning* (Lample et al., 2016) yang membutuhkan dataset beranotasi dalam jumlah besar (Devlin et al., 2019).

Meskipun model bahasa telah berkembang pesat, ketersediaan dataset umum (*general dataset*) berskala besar yang dilengkapi anotasi manusia dengan kualitas tinggi masih menjadi tantangan utama, khususnya bagi bahasa-bahasa dengan sumber daya komputasi terbatas (*low-resource languages*) seperti bahasa Indonesia (Wilie et al., 2020). Proses pelabelan data atau anotasi manusia (*human annotation*) merupakan kegiatan yang memakan waktu, tenaga, serta biaya yang tinggi. Hal ini sering kali menjadi hambatan mendasar dalam pengembangan model NLP bahasa Indonesia yang dapat bekerja secara presisi dan adaptif.

Dalam konteks bahasa Indonesia, telah diperkenalkan IndoBERT, sebuah model representasi bahasa *pre-trained* yang mampu memahami konteks dan semantik teks dengan baik. Varian `indobenchmark/indobert-large-p1` menunjukkan potensi kinerja yang unggul berkat arsitekturnya yang lebih dalam (24 *layers*) dan telah dilatih pada korpus bahasa Indonesia berskala besar (Indo4B). Namun, untuk mencapai performa yang optimal pada tugas spesifik seperti NER, model IndoBERT tetap memerlukan proses *fine-tuning* pada dataset beranotasi yang memadai.

Seiring dengan kemajuan teknologi kecerdasan buatan generatif, muncul pendekatan baru dalam anotasi data yang memanfaatkan *Large Language Models* (LLM) untuk menghasilkan data sintetis (*synthetic data*). Penggunaan LLM berpotensi mereduksi beban anotasi manusia dan mempercepat pengumpulan data. Salah satu metode yang dikembangkan adalah strategi pelabelan berbasis LLM dengan mekanisme generasi dua fase (*2-phase generation*), yaitu tahap pembangkitan teks dan anotasi awal (*generation*) yang dilanjutkan dengan tahap koreksi dan pemurnian anotasi (*correction/refining*) menggunakan model yang lebih kapabel. Proses berjenjang yang melibatkan model pemeriksa (*verifier/refiner*) ini dilaporkan lebih efektif dalam meningkatkan kualitas hasil akhir dibandingkan mekanisme generasi tunggal (*single-prompt generation*) (Kamoi et al., 2024; Zhang et al., 2024). Melalui strategi ini, anotasi sintetis yang dihasilkan berpotensi memiliki kualitas dan konsistensi yang mendekati anotasi manusia.

Dalam konteks penelitian terdahulu, efektivitas model IndoBERT untuk bahasa Indonesia, termasuk pemanfaatannya dalam tugas klasifikasi token seperti NER, telah dievaluasi oleh Wilie et al. (2020). Sementara itu, kajian mengenai prospek penggunaan *synthetic data* pada *low-resource languages* telah disoroti oleh Kamath et al. (2025), yang menyelidiki sejauh mana efektivitas anotasi sintetis berbanding anotasi manusia. Di sisi lain, terkait dengan penggunaan data sintetis, laporan teknis NVIDIA (2026a; 2026b) memaparkan pemanfaatan data sintetis dalam *pre-training* model Nemotron melalui mekanisme generasi dan koreksi, yang dilaporkan mampu menghasilkan korpus pelatihan berkualitas tinggi. Penelitian-penelitian terdahulu ini menjadi landasan argumen bahwa pemanfaatan IndoBERT yang di-*fine-tune* dengan dataset sintetis dari *pipeline* *Large Language Models* (LLM) merupakan pendekatan yang sangat relevan dan strategis untuk diteliti lebih lanjut.

Berdasarkan kebutuhan akan akurasi dan efisiensi pelabelan tersebut, diperlukan suatu analisis perbandingan empiris untuk menguji efektivitas penggunaan dataset sintetis ini. Oleh karena itu, penelitian ini melakukan *fine-tuning* model IndoBERT-large-p1 pada tugas NER bahasa Indonesia dengan *general dataset*. Pengujian membandingkan performa pelatihan yang menggunakan dataset hasil anotasi manusia (*human annotation*) dari korpus rujukan NERGRIT dan empat variasi dataset sintetis dari pasangan *pipeline* LLM generasi dua fase (Nemotron-3 Super–Ultra, GPT-5.6 Luna–Gemini Flash, Gemma 4–Nemotron Super, dan GPT-OSS–Nemotron Nano). Penelitian ini penting untuk mengevaluasi apakah pendekatan berbasis LLM dapat menjadi alternatif yang lebih efisien dalam pengembangan sistem NLP bahasa Indonesia.

## 1.2 Rumusan Masalah

Berdasarkan latar belakang yang telah diuraikan, masalah penelitian ini dirumuskan ke dalam beberapa pertanyaan penelitian berikut:

1. Bagaimana merancang dan mengimplementasikan proses *fine-tuning* model `indobenchmark/indobert-large-p1` untuk tugas *Named Entity Recognition* (NER) bahasa Indonesia menggunakan *general dataset* beranotasi manusia dan anotasi sintetis hasil generasi dua fase?
2. Bagaimana perbandingan kinerja metrik (presisi, *recall*, dan *F1-score*) model IndoBERT-large-p1 ketika dilatih menggunakan dataset anotasi manusia dan dataset anotasi sintetis pada evaluasi data uji acuan (*Gold test set* dan tolok ukur sintetis), analisis kurva pembelajaran berbasis kesetaraan jumlah entitas (*iso-entity*), serta evaluasi daya generalisasi transfer lintas korpus eksternal?

## 1.3 Tujuan

Sejalan dengan rumusan masalah di atas, penelitian ini memiliki tujuan sebagai berikut:

1. Merancang dan melaksanakan skenario *fine-tuning* pada model `indobenchmark/indobert-large-p1` untuk tugas NER bahasa Indonesia dengan variasi *general dataset* beranotasi manusia dan anotasi sintetis hasil generasi dua fase.
2. Mengevaluasi dan membandingkan kinerja metrik (presisi, *recall*, dan *F1-score*) dari model IndoBERT-large-p1 yang dihasilkan dari tiap skenario pelatihan pada evaluasi data uji acuan (*Gold test set* dan tolok ukur sintetis), analisis kurva pembelajaran kesetaraan entitas (*iso-entity*), serta evaluasi generalisasi lintas korpus eksternal untuk menguji efektivitas dan batas kemampuan strategi anotasi sintetis berbasis LLM.

## 1.4 Manfaat

Adapun hasil penelitian yang dilakukan diharapkan dapat memberikan manfaat sebagai berikut:

1. **Manfaat Akademis**: Memperkaya literatur NLP dan menyediakan analisis empiris mengenai efektivitas serta kelayakan strategi augmentasi data sintetis menggunakan mekanisme dua fase LLM terhadap model IndoBERT-large-p1 pada konteks bahasa Indonesia.
2. **Manfaat Praktis**: Memberikan alternatif solusi bagi peneliti dan praktisi NLP dalam mengatasi kendala kelangkaan dataset beranotasi bahasa Indonesia, dengan memanfaatkan LLM untuk menghemat biaya dan waktu pelabelan tanpa mengorbankan kualitas secara signifikan.

## 1.5 Batasan Masalah

Untuk menjaga ruang lingkup penelitian agar tetap fokus dan terarah, batasan-batasan masalah yang diterapkan adalah:

1. Model *pre-trained* utama yang dievaluasi difokuskan secara khusus pada varian `indobenchmark/indobert-large-p1`.
2. Tugas pemrosesan bahasa alami yang diuji dibatasi pada *Named Entity Recognition* (NER) berbahasa Indonesia berstandar OntoNotes 5.0 dengan skema 18 kelas entitas (37 tag BIO), di mana label gelar `TTL` serta label `REG` (pada skema asli korpus sumber NERGRIT) dipetakan ke label latar (`O`) pada representasi eksperimen untuk menghindari ambiguitas dan tumpang tindih taksonomi lintas korpus.
3. Dataset teks yang digunakan merupakan *general dataset* (teks berdomain umum) berbahasa Indonesia.
4. Evaluasi komparatif mencakup satu dataset acuan beranotasi manusia (NERGRIT) dan empat dataset sintetis hasil generasi dua fase (*generator–corrector*), yaitu: (a) Nemotron-3 Super 120B & Nemotron-3 Ultra 550B, (b) GPT-5.6 Luna & Gemini 3.6 Flash Medium, (c) Gemma 4 31B & Nemotron-3 Super 120B, serta (d) GPT-OSS 120B & Nemotron-3 Nano 30B.
5. Eksperimen mempertahankan keutuhan seluruh *record* sumber tanpa pembersihan sepihak selain penyesuaian sintaksis kode label yang salah ketik dan pemetaan representasi 18 kelas entitas. Analisis tambahan mencakup kurva pembelajaran berbasis kesetaraan jumlah entitas (*iso-entity*) serta evaluasi generalisasi lintas dataset.
6. Seluruh kondisi pelatihan dievaluasi secara objektif pada himpunan data uji (*test set*) beranotasi manusia yang sama setelah melalui prosedur pengelompokan ulang berbasis kemiripan teks guna mencegah kebocoran data (*data leakage*) antarpartisi.
7. Pengukuran dan perbandingan kinerja model difokuskan pada metrik standar evaluasi sekuens token NLP, yaitu *Precision*, *Recall*, dan *F1-Score*.

## 1.6 Sistematika Pembahasan

Struktur penulisan isi pada bagian utama skripsi ini dibagi ke dalam enam bab dengan rincian sebagai berikut:

1. **BAB 1 PENDAHULUAN**: Membahas latar belakang pentingnya penelitian, perumusan masalah, tujuan yang hendak dicapai, manfaat penelitian, batasan-batasan masalah yang dikerjakan, dan gambaran umum mengenai sistematika pembahasan skripsi.
2. **BAB 2 LANDASAN KEPUSTAKAAN**: Memaparkan teori-teori dasar dan tinjauan pustaka terdahulu mengenai *Natural Language Processing*, *Named Entity Recognition*, arsitektur Transformer dan BERT/IndoBERT, *Large Language Model* (terutama seri Nemotron-3), serta konsep dan metode sintesis data dua fase.
3. **BAB 3 METODOLOGI PENELITIAN**: Menguraikan tahapan-tahapan yang digunakan dalam penelitian, mulai dari pengumpulan *general dataset*, penerapan *2-phase generation* untuk pembentukan data sintetis, perancangan prosedur pelatihan *fine-tuning* IndoBERT, skenario pengujian komparatif, hingga instrumen evaluasi kinerja model.
4. **BAB 4 HASIL**: Menyajikan data hasil eksperimen secara objektif dari pelaksanaan *fine-tuning*, termasuk visualisasi kurva pelatihan dan tabulasi metrik kinerja (presisi, *recall*, dan *F1-score*) dari masing-masing skenario pelatihan.
5. **BAB 5 PEMBAHASAN**: Menyediakan ruang untuk analisis kritis yang mendalam dan perbandingan komparatif terhadap data hasil pengujian di Bab 4, guna mengidentifikasi kekuatan serta batasan anotasi sintetis berbasis LLM.
6. **BAB 6 PENUTUP**: Berisi kesimpulan akhir berupa rangkuman jawaban penelitian dari setiap rumusan masalah yang diajukan, disertai rekomendasi perbaikan dan saran untuk arah pengembangan penelitian lanjutan.
