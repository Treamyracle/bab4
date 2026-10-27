# BAB 2 LANDASAN KEPUSTAKAAN


## 2.1 Natural Language Processing (NLP)

*Natural Language Processing* (NLP) merupakan cabang dari kecerdasan buatan (*Artificial Intelligence*) yang berfokus pada interaksi antara komputer dan bahasa manusia. Tujuan utama NLP adalah untuk memampukan komputer dalam memahami, menafsirkan, dan menghasilkan bahasa alami dengan cara yang bernilai guna. Seiring dengan perkembangan teknologi komputasi, pendekatan *deep learning* telah menjadi dominan dalam berbagai tugas NLP, menggantikan metode tradisional berbasis aturan (*rule-based*) dan metode statistik klasik (Young et al., 2017).

Terkait pergeseran paradigma ini, Young et al. (2017, p.1) menegaskan keunggulan representasi bertingkat jaringan saraf dalam naskah aslinya:

> *"Deep learning methods employ multiple processing layers to learn hierarchical representations of data, and have produced state-of-the-art results in many domains."*  
> *(Artinya: Metode deep learning menggunakan banyak lapisan pemrosesan untuk mempelajari representasi data secara hierarkis, dan telah menghasilkan hasil state-of-the-art di banyak domain).*

Meskipun model *deep learning* telah menunjukkan kapabilitas yang luar biasa dalam NLP, keberhasilan model-model tersebut sangat bergantung pada ketersediaan kumpulan data besar yang beranotasi berkualitas tinggi. Kondisi ini menjadi tantangan tersendiri bagi bahasa yang minim sumber daya (*low-resource languages*), seperti bahasa Indonesia, di mana pembuatan dataset berskala besar membutuhkan biaya, waktu, dan keterlibatan pakar yang tidak sedikit.


## 2.2 Named Entity Recognition (NER)

*Named Entity Recognition* (NER) adalah salah satu tugas esensial dalam ekstraksi informasi dan NLP yang bertujuan untuk mendeteksi entitas bernama di dalam teks yang tidak terstruktur, lalu mengklasifikasikannya ke dalam kategori yang telah ditentukan sebelumnya, seperti nama orang (PER), organisasi (ORG), lokasi (LOC), dan waktu (TIME). NER sering kali diposisikan sebagai tugas klasifikasi tingkat token (Li et al., 2020).

Sebagaimana didefinisikan secara formal oleh Li et al. (2020, p.1):

> *"Named entity recognition (NER) is the task to identify mentions of rigid designators from text belonging to predefined semantic types such as person, location, organization etc."*  
> *(Artinya: Named Entity Recognition adalah tugas untuk mengidentifikasi sebutan penanda kaku dari teks yang termasuk dalam tipe semantik yang telah ditentukan sebelumnya seperti orang, lokasi, organisasi, dll).*

Sebagai tahapan awal dari *pipeline* pemahaman bahasa, keakuratan sistem NER sangat berdampak pada kinerja aplikasi NLP tingkat lanjut seperti sistem tanya jawab (*question answering*), perangkuman teks (*text summarization*), dan terjemahan mesin (*machine translation*). Penggunaan pendekatan *deep learning* pada NER memungkinkan model untuk menangkap fitur representasi semantik kompleks secara otomatis dari teks tanpa memerlukan rekayasa fitur manual.

Lebih lanjut, Lample et al. (2016, p.1) menggarisbawahi inovasi pemodelan sekuensial neural untuk penandaan entitas:

> *"In this paper, we introduce two new neural architectures—one based on bidirectional LSTMs and conditional random fields, and the other that constructs and labels segments using a transition-based approach inspired by shift-reduce parsers."*  
> *(Artinya: Dalam makalah ini, kami memperkenalkan dua arsitektur neural baru—satu didasarkan pada bidirectional LSTM dan conditional random fields, dan yang lainnya menyusun serta melabeli segmen menggunakan pendekatan berbasis transisi yang terinspirasi oleh parser shift-reduce).*

Untuk memperjelas format data masukan pada model NER, standar anotasi yang sering digunakan adalah format IOB/BIO (*Inside, Outside, Beginning*), sebagaimana dicontohkan pada Tabel 2.1.

**Tabel 2.1 Pemetaan token teks ke dalam label entitas BIO**

| Token | Tag | Keterangan |
|---|---|---|
| Budi | B-PER | Awal dari entitas Person (Orang) |
| Gunawan | I-PER | Lanjutan dari entitas Person |
| pergi | O | Bukan sebuah entitas (Outside) |
| ke | O | Bukan sebuah entitas |
| Jakarta | B-LOC | Awal dari entitas Location (Lokasi) |


## 2.3 Arsitektur Transformer

Arsitektur Transformer, yang pertama kali diperkenalkan oleh Vaswani et al. (2017) dalam penelitian bertajuk *"Attention Is All You Need"*, telah merevolusi bidang pemrosesan bahasa alami. Berbeda dengan model *Recurrent Neural Network* (RNN) maupun *Long Short-Term Memory* (LSTM) yang memproses token secara sekuensial, Transformer beroperasi sepenuhnya berdasarkan mekanisme *self-attention* (perhatian mandiri).

Vaswani et al. (2017, p.2) merumuskan kebaruan arsitektural ini sebagai berikut:

> *"In this work we propose the Transformer, a model architecture eschewing recurrence and instead relying entirely on an attention mechanism to draw global dependencies between input and output."*  
> *(Artinya: Dalam karya ini kami mengusulkan Transformer, sebuah arsitektur model yang menghindari rekurensi dan sebaliknya sepenuhnya mengandalkan mekanisme perhatian untuk menarik ketergantungan global antara masukan dan keluaran).*

Mekanisme ini memungkinkan model untuk mempertimbangkan relasi dan signifikansi dari setiap kata dalam sebuah kalimat terhadap kata-kata lainnya secara paralel, tanpa memandang jarak posisi antar kata tersebut. Secara struktural, Transformer klasik terdiri dari blok *Encoder* (yang bertugas merepresentasikan teks input ke dalam ruang vektor) dan *Decoder* (yang bertugas menghasilkan teks output). Arsitektur revolusioner ini memutus masalah kelemahan paralelisasi pada model *sequence-to-sequence* klasik dan menjadi cikal bakal dari banyak model bahasa berskala masif saat ini.


## 2.4 Large Language Model (LLM)

*Large Language Model* (LLM) adalah model komputasional berbasis *deep learning* (mayoritas mengadopsi struktur Transformer) yang dilatih di atas korpus data teks berskala raksasa dengan miliaran hingga triliunan parameter. Berkat proses prapelatihan (*pre-training*) yang ekstensif, LLM memiliki kapabilitas luar biasa dalam memahami sintaksis, semantik, serta konteks dunia nyata untuk menghasilkan teks yang sangat natural dan menyerupai buatan manusia (Zhao et al., 2023).

Sebagaimana dipaparkan oleh Zhao et al. (2023, p.1) mengenai karakteristik dasar bahasa alami dan pemodelannya:

> *"Language is essentially a complex, intricate system of human expressions governed by grammatical rules."*  
> *(Artinya: Bahasa pada hakikatnya adalah sistem ekspresi manusia yang rumit dan berbelit-belit yang diatur oleh kaidah-kaidah tata bahasa).*

Selain mahir dalam pembuatan teks, penerjemahan, dan perangkuman, model generatif skala besar ini mampu melakukan penalaran (*reasoning*) secara *zero-shot* maupun *few-shot*. Artinya, LLM dapat menyelesaikan tugas NLP yang belum pernah dilatih secara eksplisit hanya dengan diberikan instruksi (*prompt*) yang sesuai. Kapabilitas generasi ini juga memosisikan LLM sebagai alat yang menjanjikan untuk rekayasa sintesis data pada domain yang kekurangan sumber daya teks.


## 2.5 Bidirectional Encoder Representations from Transformers (BERT)

*Bidirectional Encoder Representations from Transformers* (BERT) merupakan lompatan besar dalam teknik *pre-training* model bahasa yang dikembangkan oleh Google. BERT hanya memanfaatkan tumpukan *Encoder* dari arsitektur Transformer dan dirancang untuk memahami representasi kata berdasarkan konteks kiri dan kanannya secara bersamaan (dua arah/*bidirectional*) di seluruh *layer* (Devlin et al., 2019).

Devlin et al. (2019, p.1) memperkenalkan arsitektur ini secara resmi:

> *"We introduce a new language representation model called BERT, which stands for Bidirectional Encoder Representations from Transformers."*  
> *(Artinya: Kami memperkenalkan model representasi bahasa baru yang disebut BERT, yang merupakan singkatan dari Bidirectional Encoder Representations from Transformers).*

Inovasi utama dalam pelatihan awal BERT mencakup tugas *Masked Language Modeling* (MLM), di mana model diinstruksikan untuk menebak token yang disembunyikan (*masked*) dalam sebuah kalimat, serta *Next Sentence Prediction* (NSP). Kemampuan membaca konteks dari dua arah sekaligus ini memberikan keunggulan telak bagi BERT dibandingkan model bahasa searah (*unidirectional*) sebelumnya, menjadikannya standar industri atau tulang punggung (*backbone*) untuk mengekstraksi representasi semantik mendalam pada berbagai *downstream task* klasifikasi seperti NER.


## 2.6 IndoBERT

Berangkat dari kesuksesan BERT standar yang didominasi oleh korpus bahasa Inggris, IndoBERT dikembangkan secara spesifik untuk memproses dan merepresentasikan teks berbahasa Indonesia (Wilie et al., 2020). Model bahasa pralatih (*pre-trained*) ini dilatih pada korpus berskala raksasa yang berisi gabungan dari berbagai sumber teks berbahasa Indonesia, termasuk Wikipedia, portal berita, dan korpus web lainnya (Indo4B).

Wilie et al. (2020, p.1) menegaskan cakupan evaluasi tolok ukur IndoNLU:

> *"IndoNLU includes twelve tasks, ranging from single sentence classification to pair-sentences sequence labeling with different levels of complexity."*  
> *(Artinya: IndoNLU mencakup dua belas tugas, mulai dari klasifikasi kalimat tunggal hingga pelabelan sekuens pasangan kalimat dengan tingkat kompleksitas yang berbeda).*

Varian khusus yang diutamakan dalam penelitian ini adalah `indobenchmark/indobert-large-p1`. Varian *large* ini memiliki kapasitas parameter yang jauh lebih besar (340M parameter) dan arsitektur *layer* yang lebih dalam (24 *layer*, dimensi tersembunyi $d = 1024$) dibandingkan varian *base*. Konsekuensinya, model ini memiliki kepekaan linguistik dan potensi tingkat akurasi yang lebih maksimal pada tugas turunan spesifik seperti NER di atas dataset teks yang kompleks.


## 2.7 Fine-Tuning dan Klasifikasi Sekuens

*Fine-tuning* adalah tahapan krusial dalam paradigma *Transfer Learning* pada ranah NLP, yang pertama kali dipelopori keefektifannya secara meluas melalui metode ULMFiT (Howard & Ruder, 2018). Prinsip dasar dari *fine-tuning* adalah mengambil model bahasa yang telah melalui fase *pre-training* tanpa pengawasan (*unsupervised learning*) pada miliaran teks sehingga menguasai representasi umum dari suatu bahasa, lalu melatihnya lebih lanjut pada pangkalan data (*dataset*) yang spesifik dan beranotasi.

Howard & Ruder (2018, p.1) merumuskan efektivitas *transfer learning* ini sebagai berikut:

> *"We propose Universal Language Model Fine-tuning (ULMFiT), an effective transfer learning method that can be applied to any task in NLP, and introduce techniques that are key for fine-tuning a language model."*  
> *(Artinya: Kami mengusulkan Universal Language Model Fine-tuning (ULMFiT), metode transfer learning efektif yang dapat diterapkan pada tugas apa pun dalam NLP, dan memperkenalkan teknik-teknik yang merupakan kunci untuk melakukan fine-tuning model bahasa).*

Dalam konteks penelitian ini, model dasar yang digunakan adalah IndoBERT. Agar IndoBERT dapat menyelesaikan tugas spesifik, yaitu klasifikasi kelas entitas NER, model tersebut di-*fine-tune* menggunakan dataset NER sintesis maupun data acuan manusia. Pada proses ini, bobot (*weights*) yang sudah terbentuk pada seluruh lapisan *encoder* dalam arsitektur IndoBERT tidak diinisialisasi dari awal, melainkan disesuaikan (*updated*) secara halus dengan laju pembelajaran (*learning rate*) yang kecil berdasarkan kesalahan (*loss*) prediksi dari model terhadap *ground truth* (label asli NER). Pendekatan ini memampukan pencapaian kinerja *state-of-the-art* dengan waktu dan kebutuhan data konvergensi yang jauh lebih efisien dibandingkan melatih jaringan neural dari nol.

### 2.7.1 Lapisan Klasifikasi Token (Token Classification Head)

Dalam tugas *sequence labeling* seperti NER, representasi vektor keadaan tersembunyi (*hidden state*) dari lapisan terakhir *encoder* Transformer diekstraksi untuk setiap token masukan $t$, dinyatakan sebagai $h_t \in \mathbb{R}^d$, di mana $d$ adalah dimensi ketersembunyian model ($d = 1024$ pada IndoBERT-Large). Untuk memetakan representasi kontekstual berdimensi tinggi ini ke dalam distribusi probabilitas kelas entitas NER, ditambahkan lapisan adaptasi berupa *Token Classification Head*.

Secara struktural, lapisan ini terdiri dari:
1. Lapisan regularisasi *dropout* dengan probabilitas p = 0,1 untuk memitigasi risiko *overfitting* bobot representasi.
2. Lapisan proyeksi linear dengan matriks parameter bobot $W \in \mathbb{R}^{d \times K}$ dan vektor bias $b \in \mathbb{R}^K$, di mana $K$ menyatakan jumlah total label kelas aktif (misalnya $K = 37$ pada skema representasi BIO 18 kelas).
3. Fungsi normalisasi eksponensial *Softmax* yang mengubah nilai skor linear (*logits*) menjadi distribusi probabilitas prediksi kategori entitas, sebagaimana dirumuskan pada persamaan matematis:

$$
P(y_t = k \mid h_t) = \frac{\exp(W_k h_t + b_k)}{\sum_{j=1}^K \exp(W_j h_t + b_j)}
$$

di mana $P(y_t = k \mid h_t)$ merepresentasikan estimasi probabilitas bahwa token ke-$t$ memiliki label kelas entitas $k \in \{1, 2, \dots, K\}$.

### 2.7.2 Penanganan Subword dan Masked Cross-Entropy Loss

Model keluarga BERT mengandalkan algoritma tokenisasi sub-kata (*subword tokenization*), seperti *WordPiece*, untuk mengatasi permasalahan kosakata di luar kamus (*out-of-vocabulary*). Algoritma ini kerap memecah satu kata leksikal utuh menjadi beberapa fragmen sub-kata (misalnya, kata *"Mandalika"* dipecah menjadi fragmen sub-kata). Kondisi ini menimbulkan permasalahan konsistensi pelabelan, karena anotasi entitas pada hakikatnya beroperasi pada batas kata utuh.

Standar baku penanganan fragmen sub-kata pada *sequence labeling* adalah strategi *first-subword labeling*:
1. Hanya token sub-kata pertama dari sebuah kata leksikal yang diasosiasikan dengan label kelas target asli (`B-TYPE` atau `I-TYPE`).
2. Seluruh sub-kata pecahan lanjutan (ditandai dengan awalan khusus seperti `##`), serta token pembatas format khusus (`[CLS]`, `[SEP]`, dan `[PAD]`), secara sengaja dipetakan ke nilai label semu -100.

Dalam kerangka kerja optimasi *deep learning* (seperti PyTorch), nilai $-100$ diakui sebagai indeks pengabaian baku (*ignore_index*). Fungsi kerugian pelatihan dirumuskan menggunakan *Masked Cross-Entropy Loss*:

$$
\mathcal{L}_{\text{CE}} = -\frac{1}{\sum_{t=1}^T \mathbb{I}(y_t \neq -100)} \sum_{t=1}^T \mathbb{I}(y_t \neq -100) \sum_{k=1}^K y_{t,k} \log P(y_t = k \mid h_t)
$$

di mana $\mathbb{I}(\cdot)$ adalah fungsi indikator biner yang bernilai 1 apabila label target valid ($y_t \neq -100$) dan 0 apabila berupa token semu atau bantalan (*padding*). Melalui formulasi ini, pembaruan gradien selama proses *backpropagation* semata-mata dihitung berdasarkan keputusan prediksi pada token awal kata, sehingga mencegah bias gradien akibat fragmentasi morfologis sub-kata.


## 2.8 Pembuatan Data Sintetis Berbasis LLM

Sejalan dengan masifnya perkembangan LLM, paradigma pembuatan data sintetis (*synthetic data generation*) telah muncul sebagai alternatif utama untuk mengatasi kelangkaan data beranotasi (*data scarcity*). Penggunaan LLM memungkinkan otomatisasi perancangan korpus teks pelengkap yang dapat memperbaiki kinerja (*robustness*) model turunan (*downstream model*) yang selama ini terkendala oleh minimnya data latih nyata.

Terkait tantangan mendasar ketersediaan data, Long et al. (2024, p.1) mencatat:

> *"Within the evolving landscape of deep learning, the dilemma of data quantity and quality has been a long-standing problem."*  
> *(Artinya: Dalam lanskap deep learning yang terus berkembang, dilema kuantitas dan kualitas data telah menjadi masalah yang sudah berlangsung lama).*

Tantangan tersebut dipertegas oleh temuan empiris Kamath et al. (2025, p.5) pada tugas NER bahasa minim sumber daya, yang menemukan bahwa data sintetis tanpa kurasi bertingkat rentan kalah bersaing dengan data manusia:

> *"A small amount of carefully annotated data yields better performance than a large amount of synthetic data."*  
> *(Artinya: Sejumlah kecil data yang dianotasi secara cermat menghasilkan kinerja yang lebih baik daripada data sintetis dalam jumlah besar).*

Oleh karena itu, penelitian ini memanfaatkan mekanisme augmentasi dan anotasi sintesis data berskema dua fase (*2-phase generation*) yang diotaki oleh lini model berkinerja tinggi dari NVIDIA Nemotron serta variasi pasangan LLM komparatif lainnya. Mekanisme berjenjang ini memastikan bahwa dataset akhir memiliki rasio *noise* yang rendah serta keakuratan sintaksis yang tinggi.


## 2.9 Mekanisme Sintesis Dua Fase (2-Phase Generation)

Pembuatan data menggunakan LLM dengan metode *single-prompt* konvensional seringkali memicu permasalahan akurasi, di mana model generatif kerap menghasilkan halusinasi atau pelabelan (*ground truth*) yang cacat tanpa menyadarinya. Kamoi et al. (2024) dalam studinya mengenai *self-correction* menemukan bahwa LLM secara independen sering mengalami kesulitan dalam mengoreksi kesalahannya sendiri, karena bias pada konfirmasi awal (*initial confirmation bias*). 

Kamoi et al. (2024, p.1) membuktikan keterbatasan koreksi mandiri tanpa pengawas eksternal ini:

> *"Our critical survey based on the newly categorized research questions shows that (1) no prior work demonstrates successful self-correction with feedback from prompted LLMs, except for studies in tasks that are exceptionally suited for self-correction, (2) self-correction works well in tasks that can use reliable external feedback, and (3) large-scale fine-tuning enables self-correction."*  
> *(Artinya: Survei kritis kami berdasarkan pertanyaan penelitian yang baru dikategorikan menunjukkan bahwa [1] tidak ada penelitian sebelumnya yang menunjukkan keberhasilan koreksi diri dengan umpan balik dari LLM berbasis prompt, kecuali untuk studi pada tugas-tugas yang sangat cocok untuk koreksi diri, [2] koreksi diri bekerja dengan baik pada tugas-tugas yang dapat menggunakan umpan balik eksternal yang andal, dan [3] fine-tuning skala besar memungkinkan koreksi diri).*

Untuk mengatasi kelemahan tersebut, pendekatan *2-Phase Generation* memisahkan peran penciptaan data dan peran pengawasan ke dalam dua entitas (*agent*) atau tahapan yang berbeda. Zhang et al. (2024, p.9) menegaskan bahwa model bahasa yang berperan sebagai verifikator (*strong verifier* atau *refiner*) mutlak diperlukan untuk menelaah dan mengoreksi hasil penalaran serta anotasi yang diinisiasi oleh model pertama:

> *"We find that SCORE-fine-tuned small LMs become better refiner models without relying on knowledge distillation from stronger LMs, yet they still need strong verifiers to be successful at self-correcting their reasoning errors."*  
> *(Artinya: Kami menemukan bahwa LM kecil yang di-fine-tune dengan SCORE menjadi model refiner yang lebih baik tanpa bergantung pada distilasi pengetahuan dari LM yang lebih kuat, namun mereka tetap membutuhkan verifikator yang kuat agar berhasil mengoreksi kesalahan penalaran mereka sendiri).*

Melalui mekanisme pemisahan tugas ini, pengoreksian (koreksi silang) dapat berlangsung secara lebih objektif, sehingga rasio *noise* dan anomali sintaksis pada sintesis korpus teks maupun entitas di dalamnya dapat ditekan semaksimal mungkin.


## 2.10 Model Generatif dan Orkestrasi Generator–Verifikator

Dalam merealisasikan mekanisme sintesis dua fase seperti yang telah diuraikan, penelitian ini mengeksploitasi keluarga model Nemotron sebagai tulang punggung utama, serta mengikutsertakan variasi arsitektur LLM modern lainnya untuk analisis komparatif. Secara spesifik, seri Nemotron-3 memadukan arsitektur gabungan Mamba-Attention (hibrida) dengan kerangka *Mixture-of-Experts* (MoE) inovatif yang disebut LatentMoE. Arsitektur ini dirancang secara khusus untuk mencapai tingkat akurasi optimal baik per parameter maupun per operasi komputasi (FLOP). Selain itu, lini model ini dilengkapi dengan *Multi-Token Prediction* (MTP) yang secara signifikan mempercepat proses inferensi melalui mekanisme *speculative decoding* secara bawaan (NVIDIA, 2026a; NVIDIA, 2026b). Eksperimen ini memanfaatkan duet khusus dari lini model Nemotron-3 untuk mengeksekusi kedua fase pembuatan data secara komprehensif.

### 2.10.1 Nemotron-3 Super

Pada fase pertama (*Generation Phase*), model Nemotron-3 Super bertindak sebagai generator utama untuk mensintesis korpus teks baru sekaligus menyematkan anotasi awal entitasnya. Varian model ini dibangun dengan 120 miliar total parameter, di mana hanya 12 miliar parameter aktif yang digunakan pada setiap proses *forward pass*. NVIDIA (2026a, p.1) merilis spesifikasi ini dalam laporan teknis resminya:

> *"We describe the pre-training, post-training, and quantization of Nemotron 3 Super, a 120 billion (active 12 billion) parameter hybrid Mamba-Attention Mixture-of-Experts model."*  
> *(Artinya: Kami mendeskripsikan prapelatihan, pascapelatihan, dan kuantisasi Nemotron 3 Super, sebuah model Mixture-of-Experts hibrida Mamba-Attention dengan 120 miliar parameter [12 miliar aktif]).*

Terdiri dari 88 *layer* arsitektural dan dimensi model sebesar 4096, efisiensi skala ini memberikan sensitivitas eksekusi *prompt* yang sangat tanggap dan irit komputasi. Model ini didesain secara khusus untuk *high-fidelity generation* dengan kemampuan pemahaman konteks hingga 1 juta token. Fungsi utamanya adalah memastikan variasi semantik, keberagaman kosakata, dan keluwesan gramatikal yang senatural mungkin meniru distribusi bahasa atau pola penulisan yang nyata dalam konteks teks Indonesia (NVIDIA, 2026a).

### 2.10.2 Nemotron-3 Ultra

Pada fase kedua (*Correction Phase*), keluaran kasar dari Nemotron-3 Super diteruskan ke dalam Nemotron-3 Ultra yang mengambil peran mutlak sebagai pengkritik (*critic*), evaluator, sekaligus penilai (*refiner*). Model skala raksasa ini memiliki 550 miliar total parameter dengan 55 miliar parameter aktif yang diorkestrasi melalui 108 *layer* dan dimensi model sebesar 8192. NVIDIA (2026b, p.1) menegaskan fungsi pengawasan tingkat lanjut model ini:

> *"We introduce Nemotron 3 Ultra, a 550 billion total and 55 billion active parameter Mixture-of-Experts Hybrid Mamba-Attention language model."*  
> *(Artinya: Kami memperkenalkan Nemotron 3 Ultra, model bahasa Mixture-of-Experts Hibrida Mamba-Attention dengan total 550 miliar dan 55 miliar parameter aktif).*

Berbekal skala parameter aktif yang nyaris lima kali lipat lebih padat dari varian Super, model Ultra ini difokuskan sepenuhnya pada kedalaman penalaran logis tingkat lanjut dan keakuratan analisis *agentic*. Model ini akan mendeteksi secara presisi dan mengoreksi ketidaktepatan (*hallucination*), memperbaiki struktur entitas yang bertumpang tindih, serta memvalidasi kebenaran anotasi (NVIDIA, 2026b). Proses berjenjang (pembuat dan pengoreksi silang) ini menjadi fondasi jaminan bahwa dataset sintetis akhir memiliki kelayakan pakai (*validity*) dan presisi (*precision*) yang mampu mengimbangi atau bahkan melebihi konsistensi anotasi manual manusia.

### 2.10.3 Variasi Arsitektur Generator–Verifikator Komparatif

Selain duet Nemotron-3 Super dan Ultra, penelitian ini juga menginvestigasi tiga kombinasi pasangan generator–verifikator lintas keluarga LLM guna menganalisis dampak keberagaman arsitektur model terhadap kualitas anotasi sintetis:

1. **Pasangan Luna dan Gemini Flash (GPT-5.6 Luna → Gemini 3.6 Flash Medium)**:  
   Pasangan ini mewakili paradigma distilasi lintas platform komersial tertutup. GPT-5.6 Luna difungsikan sebagai generator cepat berkemampuan produksi teks luwes dengan latensi inferensi rendah, sedangkan Gemini 3.6 Flash Medium dioperasikan sebagai verifikator berkecepatan tinggi yang memiliki penalaran kontekstual tajam untuk memeriksa validitas batas rentang entitas. Kombinasi ini memberikan perbandingan efisiensi waktu komputasi yang signifikan.
2. **Pasangan Gemma dan Nemotron Super (Gemma 4 31B → Nemotron-3 Super 120B)**:  
   Pasangan ini mengevaluasi arsitektur di mana generator berskala parameter menengah yang efisien (Gemma 4 dengan 31 miliar parameter) disupervisi oleh model verifikator berskala jauh lebih besar (Nemotron-3 Super dengan 120 miliar parameter / 12 miliar aktif). Desain ini secara langsung menguji hipotesis Zhang et al. (2024) mengenai peran model penilai yang berkapasitas lebih kuat (*stronger verifier*) dalam menyempurnakan keluaran generator berukuran lebih kecil.
3. **Pasangan GPT-OSS dan Nemotron Nano (GPT-OSS 120B → Nemotron-3 Nano 30B)**:  
   Pasangan ini merepresentasikan arsitektur asimetris terbalik, di mana generator berkapasitas besar (GPT-OSS 120B) menghasilkan korpus masif, sementara fase kurasi dan penyaringan dilakukan oleh model verifikator berskala kompak (Nemotron-3 Nano 30B). Pola ini dirancang untuk meneliti apakah verifikator yang lebih ringkas namun dikhususkan pada penalaran kritis (*Chain-of-Thought*) mampu mempertahankan konsistensi koreksi tanpa membebani sumber daya komputasi inferensi secara berlebihan.


## 2.11 Metrik Evaluasi Kinerja

Evaluasi terhadap kinerja model klasifikasi token seperti NER secara umum tidak dapat direpresentasikan secara adil dengan metrik akurasi tradisional, karena sering terjadinya ketidakseimbangan kelas (kategori di luar entitas/*Out-of-Entity* biasanya mendominasi jumlah token hingga lebih dari 80–90%). Oleh karena itu, metrik standar yang digunakan dalam pemodelan sekuens NLP adalah *Precision*, *Recall*, dan *F1-Score*.

Dalam tugas NER, penghitungan metrik evaluasi dapat didekati melalui dua paradigma: evaluasi tingkat token (*token-level*) dan evaluasi tingkat entitas utuh (*chunk-level* atau *exact span-level*). Evaluasi berbasis token hanya menilai kebenaran klasifikasi pada masing-masing potongan kata secara independen. Namun, standar baku evaluasi tolok ukur internasional seperti CoNLL-2003 (Sang & De Meulder, 2003) yang diimplementasikan oleh pustaka evaluasi `seqeval` menerapkan kriteria *exact chunk-level match*. Dalam kriteria ketat ini, suatu entitas hanya dihitung sebagai *True Positive* (TP) apabila rentang token awal (*beginning*), rentang token lanjutan (*inside*), dan kelas semantiknya tepat identik 100% dengan label rujukan (*ground truth*). Jika model memprediksi rentang kata yang terpotong sebagian atau melenceng batasnya, prediksi tersebut langsung dianggap sebagai *False Positive* (FP) sekaligus menyebabkan entitas rujukan menjadi *False Negative* (FN).

Berdasarkan identifikasi TP, FP, dan FN tersebut, persamaan matematis dari masing-masing metrik diuraikan pada subbab-subbab berikut.

### 2.11.1 Precision

*Precision* adalah rasio dari prediksi entitas positif yang benar terhadap seluruh prediksi positif yang dihasilkan oleh model, sebagaimana dirumuskan pada Persamaan 2.1:

$$
\text{Precision} = \frac{\text{TP}}{\text{TP} + \text{FP}} \qquad (2.1)
$$

### 2.11.2 Recall

*Recall* (sensitivitas) adalah rasio dari prediksi entitas positif yang berhasil ditemukan dengan benar terhadap total entitas positif aktual yang ada di dalam korpus data rujukan, sebagaimana disajikan pada Persamaan 2.2:

$$
\text{Recall} = \frac{\text{TP}}{\text{TP} + \text{FN}} \qquad (2.2)
$$

### 2.11.3 F1-Score

*F1-Score* merupakan rata-rata harmonik (*harmonic mean*) dari *Precision* dan *Recall*. Metrik tunggal ini sangat krusial untuk memberikan gambaran performa model yang berimbang dan terhindar dari bias salah satu metrik, sebagaimana dirumuskan pada Persamaan 2.3:

$$
\text{F1-Score} = 2 \times \frac{\text{Precision} \times \text{Recall}}{\text{Precision} + \text{Recall}} \qquad (2.3)
$$

### 2.11.4 Perhitungan Agregat: Micro-F1, Macro-F1, dan Weighted-F1

Dalam evaluasi multi-kelas dengan ketidakseimbangan frekuensi antarentitas, agregasi skor performa dihitung melalui tiga pendekatan matematis:

1. **Micro-averaged F1-Score ($F_{1,\text{micro}}$)**:  
   Menghitung rasio global dengan menjumlahkan total TP, FP, dan FN di seluruh kelas entitas $C$ terlebih dahulu sebelum menghitung *Precision* dan *Recall* gabungan, sebagaimana dirumuskan pada Persamaan 2.4:

   $$
F_{1,\text{micro}} = \frac{2 \sum_{c=1}^C \text{TP}_c}{2 \sum_{c=1}^C \text{TP}_c + \sum_{c=1}^C \text{FP}_c + \sum_{c=1}^C \text{FN}_c} \qquad (2.4)
$$

   Metrik *Micro-F1* mencerminkan kinerja agregat global pada seluruh token dan rentang entitas. Namun, metrik ini cenderung didominasi oleh kelas entitas berfrekuensi tinggi (seperti `PER`, `LOC`, dan `ORG`).

2. **Macro-averaged F1-Score ($F_{1,\text{macro}}$)**:  
   Menghitung rata-rata aritmetika murni dari nilai *F1-Score* masing-masing kelas tanpa mempertimbangkan jumlah frekuensi kemunculannya (*support*), sebagaimana disajikan pada Persamaan 2.5:

   $$
F_{1,\text{macro}} = \frac{1}{C} \sum_{c=1}^C F_{1,c} \qquad (2.5)
$$

   Metrik *Macro-F1* memberikan bobot yang setara untuk setiap kelas entitas. Pada penelitian ini, *Macro-F1* pada data validasi ditetapkan sebagai kriteria utama penghentian dini (*early stopping*) dan pemilihan model terbaik (*checkpoint selection*). Pemilihan ini krusial untuk memastikan bahwa model yang dipilih tidak hanya unggul pada kelas mayoritas, melainkan juga memiliki sensitivitas dan daya diskriminasi yang tinggi pada kelas-kelas entitas minoritas yang jarang muncul (seperti `WOA`, `LAW`, dan `LAN`).

3. **Weighted-averaged F1-Score ($F_{1,\text{weighted}}$)**:  
   Menghitung rata-rata berbobot dari *F1-Score* tiap kelas berdasarkan proporsi jumlah entitas aktual ($N_c$) terhadap total keseluruhan entitas ($N = \sum_{c=1}^C N_c$), sebagaimana dirumuskan pada Persamaan 2.6:

   $$
F_{1,\text{weighted}} = \sum_{c=1}^C \left( \frac{N_c}{N} \right) F_{1,c} \qquad (2.6)
$$


## 2.12 Penelitian Terdahulu

Fondasi teoretis dan praktis yang digunakan dalam skripsi ini didasarkan pada temuan dari berbagai penelitian sebelumnya yang telah dipublikasikan. Young et al. (2017) dan Li et al. (2020) menguraikan transisi teknologi fundamental pemrosesan bahasa dari pendekatan berbasis aturan menjadi *deep learning*, khususnya mengenai urgensi otomatisasi penggalian fitur pada tugas seperti NER. Sejalan dengan perkembangan tersebut, Wilie et al. (2020) merilis IndoBERT yang mendemonstrasikan bahwa *fine-tuning* pada model representasi yang di-*pre-trained* dengan korpus spesifik bahasa (Indonesia) mampu menembus *state-of-the-art* atau pencapaian kinerja terbaik untuk beragam tugas NLP komparatif (IndoNLU).

Berkaitan dengan pemenuhan sumber daya bahasa Indonesia, Lovenia et al. (2024, p.1) dalam proyek inisiatif SEACrowd mendokumentasikan ketimpangan sumber daya data bahasa-bahasa di Asia Tenggara:

> *"Despite Southeast Asia (SEA) being home to 1,300 indigenous languages (18% of the world’s languages) and 671 million people (8.75% of the world’s population), the representation of texts, images, and audio datasets from this region is significantly lacking in machine learning models."*  
> *(Artinya: Meskipun Asia Tenggara merupakan rumah bagi 1.300 bahasa asli [18% bahasa dunia] dan 671 juta jiwa [8,75% populasi dunia], keterwakilan dataset teks, citra, dan audio dari kawasan ini masih sangat minim dalam model-model machine learning).*

Menanggapi kelangkaan tersebut, Long et al. (2024) menelaah potensi masif LLM dalam perannya sebagai pencipta data (*data annotator* dan *curator*). Namun, pengujian dari Kamath et al. (2025) mengungkapkan bahwa data sintetis rentan mengalami penurunan generalisasi apabila dihasilkan melalui *single-prompt* tanpa kurasi bertingkat. Mekanisme berjenjang penciptaan data sintetis pada skripsi ini mengadopsi rilis teknis dari NVIDIA (2026a; 2026b) mengenai duet model Nemotron-3 Super untuk pembuatan data dan Nemotron-3 Ultra untuk pemurnian dan verifikasi.

Selain itu, Ding et al. (2023) meneliti kelayakan model LLM berskala besar sebagai penganotasi data untuk tugas NLP dan menunjukkan bahwa model *downstream* yang dilatih dengan data sintetis dapat bersaing dengan anotasi manusia, meski menghadapi tantangan ketepatan batas penandaan. Dari sudut pandang efisiensi pengadaan data sekuensial, Settles & Craven (2008) serta Settles et al. (2008) membuktikan bahwa pembiayaan anotasi NER berkorelasi langsung dengan jumlah entitas dan tindakan penandaan (*entity cost*), bukan semata-mata kuantitas kalimat (*sentence cost*). Hal ini mendasari penerapan metodologi evaluasi berbasis kesetaraan anggaran entitas (*iso-entity budget*) pada penelitian ini, yang mengadaptasi prinsip pengambilan sampel progresif bersarang (*progressive sampling*) dari Provost et al. (1999) dan kaidah skala daya (*power-law scaling*) dari Hestness et al. (2017). Dalam aspek penjaminan mutu anotasi, Koto et al. (2020) memberikan preseden audit manual 100 sampel kalimat untuk evaluasi korpus NER Indonesia, sementara metodologi stratifikasi jumlah entitas dan panjang kalimat diadaptasi dari rekomendasi evaluasi manusia oleh Saldías Fuentes et al. (2022).

Ringkasan perbandingan antara penelitian terdahulu yang mendasari skripsi ini disajikan pada Tabel 2.2, guna memperjelas posisi serta kebaruan (*research gap*) yang diusulkan.

**Tabel 2.2 Ringkasan Penelitian Terdahulu dan Posisi Penelitian**

| Penulis (Tahun) | Fokus Penelitian | Metode/Model | Hasil Singkat | Perbedaan dengan Penelitian Ini |
|---|---|---|---|---|
| Wilie et al. (2020) | Standarisasi *benchmark* NLP Bahasa Indonesia (IndoNLU) | IndoBERT (*Pre-trained*) | IndoBERT menembus *state-of-the-art* pada berbagai tugas NLP (termasuk NER) | Hanya menggunakan dataset NER beranotasi manual (*human annotation*) |
| Lovenia et al. (2024) | Pengumpulan dataset regional Asia Tenggara | Inisiatif SEACrowd | Memusatkan sekitar 500 korpus untuk hampir 1.000 bahasa di Asia Tenggara | Fokus SEACrowd pada agregasi data murni, sedangkan penelitian ini fokus pada sintesis data baru dengan LLM |
| Kamath et al. (2025) | Data sintetis untuk NER *low-resource* | Penggunaan LLM (*zero-shot/few-shot*) | Data sintetis bermanfaat pada model tanpa label, namun kinerjanya masih di bawah data manusia tanpa kurasi bertingkat | Penelitian ini menggunakan mekanisme sintetis berjenjang mutakhir (4 variasi generator–verifikator) alih-alih LLM tunggal |
| Ding et al. (2023) | Investigasi LLM sebagai penganotasi data NLP | GPT-3 untuk tugas klasifikasi dan ekstraksi | Data anotasi LLM mampu mendekati performa anotasi manusia pada domain umum | Tidak mengevaluasi mekanisme verifikasi dua fase terpisah pada representasi 18 kelas NER bahasa Indonesia |
| Settles & Craven (2008); Settles et al. (2008) | Analisis biaya anotasi riil pada *sequence labeling* | *Active learning* dan analisis biaya per entitas vs per kalimat | Biaya dan supervisi berbanding lurus dengan kepadatan entitas, bukan sekadar jumlah kalimat | Diadaptasi menjadi metodologi kurva pembelajaran kesetaraan entitas (*iso-entity budget*) untuk perbandingan data sintetis vs manusia |
| Penelitian Ini | Efektivitas sintesis data 2-Fase LLM untuk NER Bahasa Indonesia | IndoBERT-Large, 4 Pasangan Generator–Verifikator LLM | (Fokus Skripsi) | Memadukan keandalan IndoBERT dengan 4 arsitektur sintesis LLM 2-Fase pada 18 kelas, audit independen dua penilai 400 sampel data sintetis, eksperimen *iso-entity*, dan transfer generalisasi pada 6 dataset eksternal |
