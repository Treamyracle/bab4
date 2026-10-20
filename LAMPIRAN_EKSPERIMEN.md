# LAMPIRAN EKSPERIMEN: DOKUMENTASI TELEMETRI DAN HASIL LENGKAP PELATIHAN MODEL

Lampiran ini mendokumentasikan seluruh 84 proses pelatihan independen (*fine-tuning model fits*) arsitektur `indobenchmark/indobert-large-p1` pada kluster akselerator **NVIDIA A100-SXM4 Tensor Core GPU** (340M parameter, profil komputasi BF16 batch 32). Seluruh metrik dicatat secara otomatis oleh sistem evaluasi *reproducible pipeline*.

## L.1 Telemetri Eksekusi Pelatihan Seluruh 84 Model Fit

Tabel L.1 merangkum realisasi jumlah epoch aktual, langkah optimasi, titik checkpoint validasi terbaik, dan durasi pelatihan komputasi GPU.

**Tabel L.1 Telemetri pelaksanaan pelatihan 84 model fit pada NVIDIA A100 GPU**

| Run ID | Epoch Selesai | Langkah Optimasi | Checkpoint Terpilih | Durasi (Detik) | Durasi (Menit) | Status Early Stopping |
| --- | --- | --- | --- | --- | --- | --- |
| gold_s42_26d1055a4d59 | 6.0 | 2340 | checkpoint-1560 | 583,1 | 9,72 | Konvergen Dini (Early Stopped) |
| gold_s123_26d1055a4d59 | 7.0 | 2730 | checkpoint-1950 | 687,6 | 11,46 | Konvergen Dini (Early Stopped) |
| gold_s2026_26d1055a4d59 | 10.0 | 3900 | checkpoint-3900 | 981,7 | 16,36 | Maksimum 10 Epoch |
| nemotron_s42_4ba70b8a3fd8 | 6.0 | 2796 | checkpoint-1864 | 660,7 | 11,01 | Konvergen Dini (Early Stopped) |
| nemotron_s123_4ba70b8a3fd8 | 7.0 | 3262 | checkpoint-2330 | 771,0 | 12,85 | Konvergen Dini (Early Stopped) |
| nemotron_s2026_4ba70b8a3fd8 | 4.0 | 1864 | checkpoint-932 | 442,8 | 7,38 | Konvergen Dini (Early Stopped) |
| nemotron_s42_07b4fd089e27 | 10.0 | 630 | checkpoint-504 | 438,4 | 7,31 | Maksimum 10 Epoch |
| nemotron_s123_07b4fd089e27 | 10.0 | 630 | checkpoint-504 | 442,7 | 7,38 | Maksimum 10 Epoch |
| nemotron_s2026_07b4fd089e27 | 10.0 | 630 | checkpoint-567 | 441,8 | 7,36 | Maksimum 10 Epoch |
| nemotron_s42_5e9da60a4fe2 | 10.0 | 1040 | checkpoint-936 | 513,9 | 8,57 | Maksimum 10 Epoch |
| nemotron_s123_5e9da60a4fe2 | 6.0 | 624 | checkpoint-416 | 337,3 | 5,62 | Konvergen Dini (Early Stopped) |
| nemotron_s2026_5e9da60a4fe2 | 6.0 | 624 | checkpoint-416 | 327,1 | 5,45 | Konvergen Dini (Early Stopped) |
| nemotron_s42_902168c087cc | 6.0 | 936 | checkpoint-624 | 390,1 | 6,50 | Konvergen Dini (Early Stopped) |
| nemotron_s123_902168c087cc | 5.0 | 780 | checkpoint-468 | 318,1 | 5,30 | Konvergen Dini (Early Stopped) |
| nemotron_s2026_902168c087cc | 6.0 | 936 | checkpoint-624 | 383,3 | 6,39 | Konvergen Dini (Early Stopped) |
| nemotron_s42_0721cec63b94 | 5.0 | 1040 | checkpoint-624 | 371,0 | 6,18 | Konvergen Dini (Early Stopped) |
| nemotron_s123_0721cec63b94 | 8.0 | 1664 | checkpoint-1248 | 593,8 | 9,90 | Konvergen Dini (Early Stopped) |
| nemotron_s2026_0721cec63b94 | 7.0 | 1456 | checkpoint-1040 | 521,4 | 8,69 | Konvergen Dini (Early Stopped) |
| nemotron_s42_a8fd1ec234f4 | 8.0 | 2080 | checkpoint-1560 | 670,5 | 11,18 | Konvergen Dini (Early Stopped) |
| nemotron_s123_a8fd1ec234f4 | 9.0 | 2340 | checkpoint-1820 | 757,9 | 12,63 | Konvergen Dini (Early Stopped) |
| nemotron_s2026_a8fd1ec234f4 | 8.0 | 2080 | checkpoint-1560 | 666,8 | 11,11 | Konvergen Dini (Early Stopped) |
| nemotron_s42_8b2bda912844 | 8.0 | 2496 | checkpoint-1872 | 734,5 | 12,24 | Konvergen Dini (Early Stopped) |
| nemotron_s123_8b2bda912844 | 7.0 | 2184 | checkpoint-1560 | 631,9 | 10,53 | Konvergen Dini (Early Stopped) |
| nemotron_s2026_8b2bda912844 | 7.0 | 2184 | checkpoint-1560 | 633,1 | 10,55 | Konvergen Dini (Early Stopped) |
| luna_s42_b9c0290a259d | 8.0 | 3704 | checkpoint-2778 | 914,5 | 15,24 | Konvergen Dini (Early Stopped) |
| luna_s123_b9c0290a259d | 7.0 | 3241 | checkpoint-2315 | 276,2 | 4,60 | Konvergen Dini (Early Stopped) |
| luna_s2026_b9c0290a259d | 6.0 | 2778 | checkpoint-1852 | 569,7 | 9,49 | Konvergen Dini (Early Stopped) |
| luna_s42_dea45c03a9af | 6.0 | 462 | checkpoint-308 | 206,2 | 3,44 | Konvergen Dini (Early Stopped) |
| luna_s123_dea45c03a9af | 8.0 | 616 | checkpoint-462 | 276,5 | 4,61 | Konvergen Dini (Early Stopped) |
| luna_s2026_dea45c03a9af | 7.0 | 539 | checkpoint-385 | 246,5 | 4,11 | Konvergen Dini (Early Stopped) |
| luna_s42_0bed7d10da03 | 9.0 | 1152 | checkpoint-896 | 389,6 | 6,49 | Konvergen Dini (Early Stopped) |
| luna_s123_0bed7d10da03 | 8.0 | 1024 | checkpoint-768 | 340,9 | 5,68 | Konvergen Dini (Early Stopped) |
| luna_s2026_0bed7d10da03 | 6.0 | 768 | checkpoint-512 | 260,9 | 4,35 | Konvergen Dini (Early Stopped) |
| luna_s42_df512bf8139b | 7.0 | 1344 | checkpoint-960 | 376,3 | 6,27 | Konvergen Dini (Early Stopped) |
| luna_s123_df512bf8139b | 10.0 | 1920 | checkpoint-1536 | 536,7 | 8,94 | Maksimum 10 Epoch |
| luna_s2026_df512bf8139b | 7.0 | 1344 | checkpoint-960 | 369,9 | 6,16 | Konvergen Dini (Early Stopped) |
| luna_s42_9c87c64ef810 | 8.0 | 2040 | checkpoint-1530 | 502,2 | 8,37 | Konvergen Dini (Early Stopped) |
| luna_s123_9c87c64ef810 | 8.0 | 2040 | checkpoint-1530 | 505,3 | 8,42 | Konvergen Dini (Early Stopped) |
| luna_s2026_9c87c64ef810 | 4.0 | 1020 | checkpoint-510 | 250,8 | 4,18 | Konvergen Dini (Early Stopped) |
| luna_s42_68c51598fa04 | 8.0 | 2552 | checkpoint-1914 | 580,8 | 9,68 | Konvergen Dini (Early Stopped) |
| luna_s123_68c51598fa04 | 10.0 | 3190 | checkpoint-2871 | 730,4 | 12,17 | Maksimum 10 Epoch |
| luna_s2026_68c51598fa04 | 7.0 | 2233 | checkpoint-1595 | 512,5 | 8,54 | Konvergen Dini (Early Stopped) |
| luna_s42_71eed3bb8d18 | 7.0 | 2681 | checkpoint-1915 | 579,1 | 9,65 | Konvergen Dini (Early Stopped) |
| luna_s123_71eed3bb8d18 | 9.0 | 3447 | checkpoint-2681 | 751,8 | 12,53 | Konvergen Dini (Early Stopped) |
| luna_s2026_71eed3bb8d18 | 5.0 | 1915 | checkpoint-1149 | 423,0 | 7,05 | Konvergen Dini (Early Stopped) |
| gemma_s42_4e4ee518be16 | 6.0 | 2784 | checkpoint-1856 | 572,8 | 9,55 | Konvergen Dini (Early Stopped) |
| gemma_s123_4e4ee518be16 | 6.0 | 2784 | checkpoint-1856 | 573,3 | 9,56 | Konvergen Dini (Early Stopped) |
| gemma_s2026_4e4ee518be16 | 5.0 | 2320 | checkpoint-1392 | 479,9 | 8,00 | Konvergen Dini (Early Stopped) |
| gemma_s42_4155b32fc57f | 6.0 | 642 | checkpoint-428 | 243,2 | 4,05 | Konvergen Dini (Early Stopped) |
| gemma_s123_4155b32fc57f | 5.0 | 535 | checkpoint-321 | 198,6 | 3,31 | Konvergen Dini (Early Stopped) |
| gemma_s2026_4155b32fc57f | 6.0 | 642 | checkpoint-428 | 239,1 | 3,98 | Konvergen Dini (Early Stopped) |
| gemma_s42_f0ae407dedfe | 5.0 | 885 | checkpoint-531 | 253,2 | 4,22 | Konvergen Dini (Early Stopped) |
| gemma_s123_f0ae407dedfe | 10.0 | 1770 | checkpoint-1416 | 507,1 | 8,45 | Maksimum 10 Epoch |
| gemma_s2026_f0ae407dedfe | 6.0 | 1062 | checkpoint-708 | 304,3 | 5,07 | Konvergen Dini (Early Stopped) |
| gemma_s42_babfa72e8b68 | 6.0 | 1590 | checkpoint-1060 | 386,7 | 6,45 | Konvergen Dini (Early Stopped) |
| gemma_s123_babfa72e8b68 | 6.0 | 1590 | checkpoint-1060 | 388,2 | 6,47 | Konvergen Dini (Early Stopped) |
| gemma_s2026_babfa72e8b68 | 6.0 | 1590 | checkpoint-1060 | 397,0 | 6,62 | Konvergen Dini (Early Stopped) |
| gemma_s42_0898c1ce7ae2 | 9.0 | 3186 | checkpoint-2478 | 713,2 | 11,89 | Konvergen Dini (Early Stopped) |
| gemma_s123_0898c1ce7ae2 | 6.0 | 2124 | checkpoint-1416 | 474,9 | 7,92 | Konvergen Dini (Early Stopped) |
| gemma_s2026_0898c1ce7ae2 | 6.0 | 2124 | checkpoint-1416 | 477,1 | 7,95 | Konvergen Dini (Early Stopped) |
| gemma_s42_5e5556d943f9 | 5.0 | 2210 | checkpoint-1326 | 468,2 | 7,80 | Konvergen Dini (Early Stopped) |
| gemma_s123_5e5556d943f9 | 10.0 | 4420 | checkpoint-3536 | 928,6 | 15,48 | Maksimum 10 Epoch |
| gemma_s2026_5e5556d943f9 | 7.0 | 3094 | checkpoint-2210 | 648,2 | 10,80 | Konvergen Dini (Early Stopped) |
| gpt_oss_s42_f91f501e4d7f | 5.0 | 2320 | checkpoint-1392 | 484,8 | 8,08 | Konvergen Dini (Early Stopped) |
| gpt_oss_s123_f91f501e4d7f | 6.0 | 2784 | checkpoint-1856 | 579,8 | 9,66 | Konvergen Dini (Early Stopped) |
| gpt_oss_s2026_f91f501e4d7f | 7.0 | 3248 | checkpoint-2320 | 681,3 | 11,36 | Konvergen Dini (Early Stopped) |
| gpt_oss_s42_63ef5b83ef6c | 10.0 | 700 | checkpoint-700 | 347,5 | 5,79 | Maksimum 10 Epoch |
| gpt_oss_s123_63ef5b83ef6c | 9.0 | 630 | checkpoint-490 | 306,7 | 5,11 | Konvergen Dini (Early Stopped) |
| gpt_oss_s2026_63ef5b83ef6c | 5.0 | 350 | checkpoint-210 | 171,2 | 2,85 | Konvergen Dini (Early Stopped) |
| gpt_oss_s42_3661b2350fa6 | 8.0 | 928 | checkpoint-696 | 326,2 | 5,44 | Konvergen Dini (Early Stopped) |
| gpt_oss_s123_3661b2350fa6 | 8.0 | 928 | checkpoint-696 | 328,2 | 5,47 | Konvergen Dini (Early Stopped) |
| gpt_oss_s2026_3661b2350fa6 | 7.0 | 812 | checkpoint-580 | 288,1 | 4,80 | Konvergen Dini (Early Stopped) |
| gpt_oss_s42_03cce2dac1b7 | 8.0 | 1392 | checkpoint-1044 | 400,7 | 6,68 | Konvergen Dini (Early Stopped) |
| gpt_oss_s123_03cce2dac1b7 | 6.0 | 1044 | checkpoint-696 | 304,5 | 5,08 | Konvergen Dini (Early Stopped) |
| gpt_oss_s2026_03cce2dac1b7 | 8.0 | 1392 | checkpoint-1044 | 409,3 | 6,82 | Konvergen Dini (Early Stopped) |
| gpt_oss_s42_19d8974c216d | 7.0 | 1624 | checkpoint-1160 | 421,8 | 7,03 | Konvergen Dini (Early Stopped) |
| gpt_oss_s123_19d8974c216d | 7.0 | 1624 | checkpoint-1160 | 415,3 | 6,92 | Konvergen Dini (Early Stopped) |
| gpt_oss_s2026_19d8974c216d | 6.0 | 1392 | checkpoint-928 | 361,4 | 6,02 | Konvergen Dini (Early Stopped) |
| gpt_oss_s42_1ef01ae1b729 | 6.0 | 1734 | checkpoint-1156 | 417,4 | 6,96 | Konvergen Dini (Early Stopped) |
| gpt_oss_s123_1ef01ae1b729 | 9.0 | 2601 | checkpoint-2023 | 626,3 | 10,44 | Konvergen Dini (Early Stopped) |
| gpt_oss_s2026_1ef01ae1b729 | 6.0 | 1734 | checkpoint-1156 | 416,1 | 6,94 | Konvergen Dini (Early Stopped) |
| gpt_oss_s42_76f1ae0fa7b2 | 8.0 | 2776 | checkpoint-2082 | 626,5 | 10,44 | Konvergen Dini (Early Stopped) |
| gpt_oss_s123_76f1ae0fa7b2 | 7.0 | 2429 | checkpoint-1735 | 549,4 | 9,16 | Konvergen Dini (Early Stopped) |
| gpt_oss_s2026_76f1ae0fa7b2 | 10.0 | 3470 | checkpoint-2776 | 785,1 | 13,08 | Maksimum 10 Epoch |

## L.2 Evaluasi Komparatif Lengkap pada Test Gold dan Benchmark Sintetis

Tabel L.2 mendokumentasikan metrik pencocokan penuh CoNLL BIO 18 kelas untuk setiap model run pada Test Gold (2.423 kalimat) dan Benchmark Sintetis (1.000 kalimat).

**Tabel L.2 Rincian metrik per-run pada Test Gold dan Benchmark Sintetis**

| Korpus Latih | Kondisi | Rasio | Seed | Himpunan Uji | Presisi (%) | Recall (%) | Micro-F1 (%) | Macro-F1 (%) | Weighted-F1 (%) | Support |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NERGRIT (Gold) | main | max | 42 | Test Gold | 83,65 | 84,22 | 83,93 | 75,52 | 83,80 | 8.890 |
| NERGRIT (Gold) | main | max | 42 | Benchmark Sintetis | 51,22 | 49,49 | 50,34 | 54,48 | 50,28 | 6.426 |
| NERGRIT (Gold) | main | max | 123 | Test Gold | 83,54 | 84,77 | 84,15 | 75,69 | 84,07 | 8.890 |
| NERGRIT (Gold) | main | max | 123 | Benchmark Sintetis | 50,42 | 49,18 | 49,79 | 55,00 | 49,94 | 6.426 |
| NERGRIT (Gold) | main | max | 2026 | Test Gold | 84,26 | 85,19 | 84,72 | 77,01 | 84,64 | 8.890 |
| NERGRIT (Gold) | main | max | 2026 | Benchmark Sintetis | 50,82 | 49,46 | 50,13 | 55,15 | 50,30 | 6.426 |
| Nemotron | main | max | 42 | Test Gold | 54,74 | 51,11 | 52,86 | 41,81 | 50,83 | 8.890 |
| Nemotron | main | max | 42 | Benchmark Sintetis | 77,98 | 84,89 | 81,29 | 75,83 | 81,92 | 6.426 |
| Nemotron | main | max | 123 | Test Gold | 54,71 | 50,87 | 52,72 | 41,92 | 50,69 | 8.890 |
| Nemotron | main | max | 123 | Benchmark Sintetis | 78,03 | 84,64 | 81,20 | 75,57 | 81,67 | 6.426 |
| Nemotron | main | max | 2026 | Test Gold | 52,94 | 49,70 | 51,26 | 41,54 | 49,38 | 8.890 |
| Nemotron | main | max | 2026 | Benchmark Sintetis | 78,83 | 85,93 | 82,23 | 76,92 | 82,85 | 6.426 |
| Nemotron | iso | 0.3 | 42 | Test Gold | 53,19 | 49,57 | 51,32 | 41,72 | 49,39 | 8.890 |
| Nemotron | iso | 0.3 | 42 | Benchmark Sintetis | 80,07 | 85,45 | 82,67 | 76,05 | 83,03 | 6.426 |
| Nemotron | iso | 0.3 | 123 | Test Gold | 52,94 | 49,61 | 51,22 | 40,59 | 48,94 | 8.890 |
| Nemotron | iso | 0.3 | 123 | Benchmark Sintetis | 77,40 | 84,42 | 80,76 | 74,09 | 81,53 | 6.426 |
| Nemotron | iso | 0.3 | 2026 | Test Gold | 53,19 | 51,93 | 52,55 | 42,22 | 50,96 | 8.890 |
| Nemotron | iso | 0.3 | 2026 | Benchmark Sintetis | 78,88 | 85,42 | 82,02 | 75,42 | 82,71 | 6.426 |
| Nemotron | iso | 0.5 | 42 | Test Gold | 53,80 | 50,90 | 52,31 | 42,37 | 50,36 | 8.890 |
| Nemotron | iso | 0.5 | 42 | Benchmark Sintetis | 80,18 | 85,25 | 82,64 | 75,75 | 83,16 | 6.426 |
| Nemotron | iso | 0.5 | 123 | Test Gold | 52,27 | 48,46 | 50,29 | 41,05 | 48,25 | 8.890 |
| Nemotron | iso | 0.5 | 123 | Benchmark Sintetis | 77,69 | 85,87 | 81,57 | 75,59 | 82,50 | 6.426 |
| Nemotron | iso | 0.5 | 2026 | Test Gold | 55,56 | 51,07 | 53,22 | 42,55 | 50,84 | 8.890 |
| Nemotron | iso | 0.5 | 2026 | Benchmark Sintetis | 78,96 | 84,97 | 81,85 | 74,82 | 82,66 | 6.426 |
| Nemotron | iso | 0.75 | 42 | Test Gold | 51,91 | 49,27 | 50,55 | 42,27 | 48,56 | 8.890 |
| Nemotron | iso | 0.75 | 42 | Benchmark Sintetis | 76,97 | 84,36 | 80,50 | 75,15 | 80,91 | 6.426 |
| Nemotron | iso | 0.75 | 123 | Test Gold | 52,71 | 48,58 | 50,56 | 41,74 | 48,45 | 8.890 |
| Nemotron | iso | 0.75 | 123 | Benchmark Sintetis | 78,64 | 85,70 | 82,02 | 77,16 | 82,61 | 6.426 |
| Nemotron | iso | 0.75 | 2026 | Test Gold | 53,27 | 48,99 | 51,04 | 41,98 | 48,90 | 8.890 |
| Nemotron | iso | 0.75 | 2026 | Benchmark Sintetis | 80,87 | 85,76 | 83,24 | 76,90 | 83,55 | 6.426 |
| Nemotron | iso | 1.0 | 42 | Test Gold | 52,22 | 47,00 | 49,47 | 41,24 | 47,70 | 8.890 |
| Nemotron | iso | 1.0 | 42 | Benchmark Sintetis | 81,33 | 86,52 | 83,85 | 77,71 | 84,44 | 6.426 |
| Nemotron | iso | 1.0 | 123 | Test Gold | 52,32 | 48,88 | 50,54 | 40,62 | 48,66 | 8.890 |
| Nemotron | iso | 1.0 | 123 | Benchmark Sintetis | 79,12 | 84,91 | 81,91 | 75,75 | 82,40 | 6.426 |
| Nemotron | iso | 1.0 | 2026 | Test Gold | 52,97 | 50,45 | 51,68 | 41,42 | 50,03 | 8.890 |
| Nemotron | iso | 1.0 | 2026 | Benchmark Sintetis | 79,58 | 84,97 | 82,19 | 76,78 | 82,46 | 6.426 |
| Nemotron | iso | 1.25 | 42 | Test Gold | 52,10 | 48,22 | 50,09 | 41,09 | 48,18 | 8.890 |
| Nemotron | iso | 1.25 | 42 | Benchmark Sintetis | 78,24 | 84,73 | 81,36 | 75,59 | 81,87 | 6.426 |
| Nemotron | iso | 1.25 | 123 | Test Gold | 54,13 | 49,36 | 51,64 | 42,16 | 49,58 | 8.890 |
| Nemotron | iso | 1.25 | 123 | Benchmark Sintetis | 79,29 | 85,36 | 82,21 | 76,27 | 82,74 | 6.426 |
| Nemotron | iso | 1.25 | 2026 | Test Gold | 54,43 | 49,72 | 51,97 | 41,89 | 49,86 | 8.890 |
| Nemotron | iso | 1.25 | 2026 | Benchmark Sintetis | 79,97 | 84,95 | 82,39 | 77,07 | 82,72 | 6.426 |
| Nemotron | iso | 1.5 | 42 | Test Gold | 55,03 | 50,57 | 52,71 | 42,13 | 50,52 | 8.890 |
| Nemotron | iso | 1.5 | 42 | Benchmark Sintetis | 81,12 | 86,13 | 83,55 | 76,50 | 84,10 | 6.426 |
| Nemotron | iso | 1.5 | 123 | Test Gold | 55,01 | 50,58 | 52,70 | 41,89 | 50,30 | 8.890 |
| Nemotron | iso | 1.5 | 123 | Benchmark Sintetis | 79,48 | 85,51 | 82,38 | 75,98 | 83,04 | 6.426 |
| Nemotron | iso | 1.5 | 2026 | Test Gold | 54,51 | 51,37 | 52,90 | 42,33 | 51,26 | 8.890 |
| Nemotron | iso | 1.5 | 2026 | Benchmark Sintetis | 81,45 | 86,71 | 84,00 | 78,59 | 84,41 | 6.426 |
| Nemotron | iso | max | 42 | Test Gold | 54,74 | 51,11 | 52,86 | 41,81 | 50,83 | 8.890 |
| Nemotron | iso | max | 42 | Benchmark Sintetis | 77,98 | 84,89 | 81,29 | 75,83 | 81,92 | 6.426 |
| Nemotron | iso | max | 123 | Test Gold | 54,71 | 50,87 | 52,72 | 41,92 | 50,69 | 8.890 |
| Nemotron | iso | max | 123 | Benchmark Sintetis | 78,03 | 84,64 | 81,20 | 75,57 | 81,67 | 6.426 |
| Nemotron | iso | max | 2026 | Test Gold | 52,94 | 49,70 | 51,26 | 41,54 | 49,38 | 8.890 |
| Nemotron | iso | max | 2026 | Benchmark Sintetis | 78,83 | 85,93 | 82,23 | 76,92 | 82,85 | 6.426 |
| Luna | main | max | 42 | Test Gold | 58,70 | 51,44 | 54,83 | 43,59 | 50,95 | 8.890 |
| Luna | main | max | 42 | Benchmark Sintetis | 74,61 | 68,39 | 71,36 | 76,70 | 68,50 | 6.426 |
| Luna | main | max | 123 | Test Gold | 58,41 | 52,51 | 55,30 | 43,69 | 51,79 | 8.890 |
| Luna | main | max | 123 | Benchmark Sintetis | 73,98 | 68,08 | 70,91 | 75,71 | 69,08 | 6.426 |
| Luna | main | max | 2026 | Test Gold | 58,52 | 51,17 | 54,60 | 41,97 | 50,72 | 8.890 |
| Luna | main | max | 2026 | Benchmark Sintetis | 72,65 | 67,58 | 70,03 | 75,26 | 67,56 | 6.426 |
| Luna | iso | 0.3 | 42 | Test Gold | 56,16 | 51,03 | 53,47 | 40,88 | 49,44 | 8.890 |
| Luna | iso | 0.3 | 42 | Benchmark Sintetis | 70,48 | 67,06 | 68,72 | 72,00 | 66,02 | 6.426 |
| Luna | iso | 0.3 | 123 | Test Gold | 56,72 | 51,78 | 54,14 | 41,80 | 50,59 | 8.890 |
| Luna | iso | 0.3 | 123 | Benchmark Sintetis | 74,57 | 73,42 | 73,99 | 74,99 | 72,88 | 6.426 |
| Luna | iso | 0.3 | 2026 | Test Gold | 56,16 | 50,73 | 53,31 | 42,17 | 49,85 | 8.890 |
| Luna | iso | 0.3 | 2026 | Benchmark Sintetis | 73,20 | 68,83 | 70,95 | 73,76 | 68,67 | 6.426 |
| Luna | iso | 0.5 | 42 | Test Gold | 57,73 | 51,30 | 54,33 | 42,46 | 50,49 | 8.890 |
| Luna | iso | 0.5 | 42 | Benchmark Sintetis | 74,50 | 69,92 | 72,14 | 75,58 | 70,30 | 6.426 |
| Luna | iso | 0.5 | 123 | Test Gold | 56,96 | 51,62 | 54,16 | 42,59 | 50,62 | 8.890 |
| Luna | iso | 0.5 | 123 | Benchmark Sintetis | 77,05 | 74,77 | 75,90 | 75,98 | 74,91 | 6.426 |
| Luna | iso | 0.5 | 2026 | Test Gold | 55,68 | 48,29 | 51,72 | 40,63 | 47,98 | 8.890 |
| Luna | iso | 0.5 | 2026 | Benchmark Sintetis | 75,94 | 72,50 | 74,18 | 74,37 | 72,80 | 6.426 |
| Luna | iso | 0.75 | 42 | Test Gold | 56,85 | 50,79 | 53,65 | 42,28 | 49,93 | 8.890 |
| Luna | iso | 0.75 | 42 | Benchmark Sintetis | 73,47 | 68,99 | 71,16 | 73,65 | 69,42 | 6.426 |
| Luna | iso | 0.75 | 123 | Test Gold | 59,25 | 52,06 | 55,42 | 43,91 | 51,45 | 8.890 |
| Luna | iso | 0.75 | 123 | Benchmark Sintetis | 78,58 | 74,88 | 76,69 | 77,74 | 75,55 | 6.426 |
| Luna | iso | 0.75 | 2026 | Test Gold | 56,76 | 49,66 | 52,98 | 42,19 | 49,17 | 8.890 |
| Luna | iso | 0.75 | 2026 | Benchmark Sintetis | 79,07 | 75,83 | 77,42 | 76,85 | 76,60 | 6.426 |
| Luna | iso | 1.0 | 42 | Test Gold | 58,61 | 50,99 | 54,54 | 42,60 | 50,86 | 8.890 |
| Luna | iso | 1.0 | 42 | Benchmark Sintetis | 74,10 | 67,62 | 70,71 | 75,82 | 67,82 | 6.426 |
| Luna | iso | 1.0 | 123 | Test Gold | 58,72 | 50,85 | 54,51 | 42,34 | 50,50 | 8.890 |
| Luna | iso | 1.0 | 123 | Benchmark Sintetis | 75,59 | 70,73 | 73,08 | 74,97 | 71,53 | 6.426 |
| Luna | iso | 1.0 | 2026 | Test Gold | 56,88 | 49,45 | 52,91 | 41,90 | 49,13 | 8.890 |
| Luna | iso | 1.0 | 2026 | Benchmark Sintetis | 73,07 | 68,39 | 70,65 | 75,02 | 68,13 | 6.426 |
| Luna | iso | 1.25 | 42 | Test Gold | 58,09 | 52,07 | 54,92 | 43,31 | 50,75 | 8.890 |
| Luna | iso | 1.25 | 42 | Benchmark Sintetis | 72,56 | 67,93 | 70,17 | 75,25 | 67,92 | 6.426 |
| Luna | iso | 1.25 | 123 | Test Gold | 58,38 | 51,66 | 54,82 | 42,81 | 51,23 | 8.890 |
| Luna | iso | 1.25 | 123 | Benchmark Sintetis | 76,15 | 71,76 | 73,89 | 75,77 | 72,66 | 6.426 |
| Luna | iso | 1.25 | 2026 | Test Gold | 59,59 | 51,81 | 55,43 | 43,78 | 51,43 | 8.890 |
| Luna | iso | 1.25 | 2026 | Benchmark Sintetis | 71,32 | 66,01 | 68,56 | 74,90 | 65,82 | 6.426 |
| Luna | iso | 1.5 | 42 | Test Gold | 59,23 | 50,58 | 54,57 | 43,96 | 50,52 | 8.890 |
| Luna | iso | 1.5 | 42 | Benchmark Sintetis | 74,55 | 69,56 | 71,97 | 75,87 | 70,06 | 6.426 |
| Luna | iso | 1.5 | 123 | Test Gold | 58,55 | 51,23 | 54,64 | 43,52 | 50,92 | 8.890 |
| Luna | iso | 1.5 | 123 | Benchmark Sintetis | 76,75 | 71,13 | 73,83 | 76,05 | 72,34 | 6.426 |
| Luna | iso | 1.5 | 2026 | Test Gold | 58,34 | 51,07 | 54,46 | 42,67 | 50,73 | 8.890 |
| Luna | iso | 1.5 | 2026 | Benchmark Sintetis | 74,02 | 67,23 | 70,46 | 75,16 | 68,00 | 6.426 |
| Luna | iso | max | 42 | Test Gold | 58,70 | 51,44 | 54,83 | 43,59 | 50,95 | 8.890 |
| Luna | iso | max | 42 | Benchmark Sintetis | 74,61 | 68,39 | 71,36 | 76,70 | 68,50 | 6.426 |
| Luna | iso | max | 123 | Test Gold | 58,41 | 52,51 | 55,30 | 43,69 | 51,79 | 8.890 |
| Luna | iso | max | 123 | Benchmark Sintetis | 73,98 | 68,08 | 70,91 | 75,71 | 69,08 | 6.426 |
| Luna | iso | max | 2026 | Test Gold | 58,52 | 51,17 | 54,60 | 41,97 | 50,72 | 8.890 |
| Luna | iso | max | 2026 | Benchmark Sintetis | 72,65 | 67,58 | 70,03 | 75,26 | 67,56 | 6.426 |
| Gemma | main | max | 42 | Test Gold | 55,54 | 50,79 | 53,06 | 42,50 | 50,14 | 8.890 |
| Gemma | main | max | 42 | Benchmark Sintetis | 68,93 | 65,98 | 67,42 | 71,80 | 65,43 | 6.426 |
| Gemma | main | max | 123 | Test Gold | 57,83 | 51,63 | 54,56 | 44,99 | 51,50 | 8.890 |
| Gemma | main | max | 123 | Benchmark Sintetis | 69,32 | 64,53 | 66,84 | 72,11 | 64,30 | 6.426 |
| Gemma | main | max | 2026 | Test Gold | 55,73 | 47,28 | 51,16 | 42,46 | 47,89 | 8.890 |
| Gemma | main | max | 2026 | Benchmark Sintetis | 77,97 | 80,67 | 79,30 | 74,69 | 79,65 | 6.426 |
| Gemma | iso | 0.3 | 42 | Test Gold | 51,25 | 47,82 | 49,48 | 40,66 | 46,88 | 8.890 |
| Gemma | iso | 0.3 | 42 | Benchmark Sintetis | 74,43 | 76,11 | 75,26 | 71,80 | 75,06 | 6.426 |
| Gemma | iso | 0.3 | 123 | Test Gold | 54,50 | 50,21 | 52,27 | 41,45 | 49,47 | 8.890 |
| Gemma | iso | 0.3 | 123 | Benchmark Sintetis | 67,11 | 64,57 | 65,82 | 69,46 | 63,93 | 6.426 |
| Gemma | iso | 0.3 | 2026 | Test Gold | 54,67 | 49,35 | 51,87 | 42,12 | 48,21 | 8.890 |
| Gemma | iso | 0.3 | 2026 | Benchmark Sintetis | 66,14 | 63,88 | 64,99 | 67,89 | 63,32 | 6.426 |
| Gemma | iso | 0.5 | 42 | Test Gold | 55,92 | 50,44 | 53,04 | 44,32 | 50,04 | 8.890 |
| Gemma | iso | 0.5 | 42 | Benchmark Sintetis | 66,63 | 63,23 | 64,88 | 68,47 | 62,20 | 6.426 |
| Gemma | iso | 0.5 | 123 | Test Gold | 55,52 | 48,95 | 52,03 | 40,44 | 48,93 | 8.890 |
| Gemma | iso | 0.5 | 123 | Benchmark Sintetis | 67,53 | 64,01 | 65,72 | 70,28 | 63,26 | 6.426 |
| Gemma | iso | 0.5 | 2026 | Test Gold | 53,80 | 46,21 | 49,72 | 41,46 | 46,58 | 8.890 |
| Gemma | iso | 0.5 | 2026 | Benchmark Sintetis | 67,48 | 63,82 | 65,60 | 69,33 | 63,54 | 6.426 |
| Gemma | iso | 0.75 | 42 | Test Gold | 54,67 | 50,07 | 52,27 | 42,10 | 49,48 | 8.890 |
| Gemma | iso | 0.75 | 42 | Benchmark Sintetis | 70,21 | 68,52 | 69,35 | 72,23 | 68,05 | 6.426 |
| Gemma | iso | 0.75 | 123 | Test Gold | 56,03 | 48,44 | 51,96 | 40,89 | 48,69 | 8.890 |
| Gemma | iso | 0.75 | 123 | Benchmark Sintetis | 69,14 | 64,71 | 66,85 | 71,32 | 64,28 | 6.426 |
| Gemma | iso | 0.75 | 2026 | Test Gold | 54,88 | 48,05 | 51,24 | 42,40 | 48,03 | 8.890 |
| Gemma | iso | 0.75 | 2026 | Benchmark Sintetis | 72,41 | 69,34 | 70,84 | 72,15 | 69,55 | 6.426 |
| Gemma | iso | 1.0 | 42 | Test Gold | 55,90 | 50,28 | 52,94 | 42,58 | 50,07 | 8.890 |
| Gemma | iso | 1.0 | 42 | Benchmark Sintetis | 69,70 | 65,81 | 67,70 | 71,89 | 65,62 | 6.426 |
| Gemma | iso | 1.0 | 123 | Test Gold | 58,27 | 50,55 | 54,13 | 42,50 | 50,67 | 8.890 |
| Gemma | iso | 1.0 | 123 | Benchmark Sintetis | 67,59 | 64,60 | 66,06 | 71,48 | 63,51 | 6.426 |
| Gemma | iso | 1.0 | 2026 | Test Gold | 56,26 | 46,91 | 51,16 | 43,48 | 48,17 | 8.890 |
| Gemma | iso | 1.0 | 2026 | Benchmark Sintetis | 69,88 | 65,38 | 67,55 | 72,13 | 65,49 | 6.426 |
| Gemma | iso | 1.25 | 42 | Test Gold | 55,03 | 48,44 | 51,52 | 42,57 | 48,86 | 8.890 |
| Gemma | iso | 1.25 | 42 | Benchmark Sintetis | 78,59 | 80,53 | 79,55 | 74,71 | 79,69 | 6.426 |
| Gemma | iso | 1.25 | 123 | Test Gold | 55,95 | 47,90 | 51,61 | 41,28 | 48,87 | 8.890 |
| Gemma | iso | 1.25 | 123 | Benchmark Sintetis | 69,07 | 64,99 | 66,97 | 71,35 | 64,83 | 6.426 |
| Gemma | iso | 1.25 | 2026 | Test Gold | 54,96 | 47,81 | 51,13 | 41,16 | 48,14 | 8.890 |
| Gemma | iso | 1.25 | 2026 | Benchmark Sintetis | 78,30 | 82,24 | 80,22 | 75,39 | 80,79 | 6.426 |
| Gemma | iso | max | 42 | Test Gold | 55,54 | 50,79 | 53,06 | 42,50 | 50,14 | 8.890 |
| Gemma | iso | max | 42 | Benchmark Sintetis | 68,93 | 65,98 | 67,42 | 71,80 | 65,43 | 6.426 |
| Gemma | iso | max | 123 | Test Gold | 57,83 | 51,63 | 54,56 | 44,99 | 51,50 | 8.890 |
| Gemma | iso | max | 123 | Benchmark Sintetis | 69,32 | 64,53 | 66,84 | 72,11 | 64,30 | 6.426 |
| Gemma | iso | max | 2026 | Test Gold | 55,73 | 47,28 | 51,16 | 42,46 | 47,89 | 8.890 |
| Gemma | iso | max | 2026 | Benchmark Sintetis | 77,97 | 80,67 | 79,30 | 74,69 | 79,65 | 6.426 |
| GPT-OSS | main | max | 42 | Test Gold | 55,15 | 47,48 | 51,03 | 44,09 | 48,87 | 8.890 |
| GPT-OSS | main | max | 42 | Benchmark Sintetis | 80,45 | 83,78 | 82,09 | 74,26 | 81,92 | 6.426 |
| GPT-OSS | main | max | 123 | Test Gold | 57,94 | 50,66 | 54,06 | 45,41 | 51,58 | 8.890 |
| GPT-OSS | main | max | 123 | Benchmark Sintetis | 78,38 | 82,99 | 80,62 | 74,49 | 81,05 | 6.426 |
| GPT-OSS | main | max | 2026 | Test Gold | 57,79 | 49,98 | 53,60 | 44,90 | 51,31 | 8.890 |
| GPT-OSS | main | max | 2026 | Benchmark Sintetis | 80,05 | 80,30 | 80,17 | 73,45 | 80,06 | 6.426 |
| GPT-OSS | iso | 0.3 | 42 | Test Gold | 53,29 | 46,38 | 49,59 | 40,02 | 47,72 | 8.890 |
| GPT-OSS | iso | 0.3 | 42 | Benchmark Sintetis | 79,15 | 81,90 | 80,50 | 72,07 | 80,48 | 6.426 |
| GPT-OSS | iso | 0.3 | 123 | Test Gold | 54,41 | 45,29 | 49,43 | 39,31 | 47,07 | 8.890 |
| GPT-OSS | iso | 0.3 | 123 | Benchmark Sintetis | 79,51 | 81,36 | 80,42 | 73,06 | 80,30 | 6.426 |
| GPT-OSS | iso | 0.3 | 2026 | Test Gold | 54,11 | 44,16 | 48,63 | 39,00 | 45,95 | 8.890 |
| GPT-OSS | iso | 0.3 | 2026 | Benchmark Sintetis | 79,73 | 80,61 | 80,17 | 70,22 | 79,82 | 6.426 |
| GPT-OSS | iso | 0.5 | 42 | Test Gold | 54,88 | 46,48 | 50,33 | 41,26 | 48,31 | 8.890 |
| GPT-OSS | iso | 0.5 | 42 | Benchmark Sintetis | 80,14 | 83,46 | 81,77 | 73,39 | 81,68 | 6.426 |
| GPT-OSS | iso | 0.5 | 123 | Test Gold | 55,45 | 45,78 | 50,15 | 39,55 | 47,62 | 8.890 |
| GPT-OSS | iso | 0.5 | 123 | Benchmark Sintetis | 80,55 | 82,12 | 81,33 | 73,05 | 81,17 | 6.426 |
| GPT-OSS | iso | 0.5 | 2026 | Test Gold | 55,79 | 46,12 | 50,50 | 42,04 | 48,25 | 8.890 |
| GPT-OSS | iso | 0.5 | 2026 | Benchmark Sintetis | 81,23 | 82,73 | 81,97 | 73,20 | 81,70 | 6.426 |
| GPT-OSS | iso | 0.75 | 42 | Test Gold | 55,20 | 46,58 | 50,52 | 42,88 | 48,60 | 8.890 |
| GPT-OSS | iso | 0.75 | 42 | Benchmark Sintetis | 80,07 | 83,49 | 81,75 | 74,20 | 81,75 | 6.426 |
| GPT-OSS | iso | 0.75 | 123 | Test Gold | 56,06 | 47,12 | 51,20 | 42,52 | 49,09 | 8.890 |
| GPT-OSS | iso | 0.75 | 123 | Benchmark Sintetis | 77,59 | 81,57 | 79,53 | 72,90 | 79,58 | 6.426 |
| GPT-OSS | iso | 0.75 | 2026 | Test Gold | 56,64 | 46,95 | 51,34 | 44,11 | 49,57 | 8.890 |
| GPT-OSS | iso | 0.75 | 2026 | Benchmark Sintetis | 79,59 | 82,45 | 80,99 | 73,09 | 80,99 | 6.426 |
| GPT-OSS | iso | 1.0 | 42 | Test Gold | 55,65 | 46,29 | 50,54 | 43,07 | 48,19 | 8.890 |
| GPT-OSS | iso | 1.0 | 42 | Benchmark Sintetis | 81,30 | 82,68 | 81,98 | 74,75 | 81,78 | 6.426 |
| GPT-OSS | iso | 1.0 | 123 | Test Gold | 55,52 | 47,20 | 51,02 | 43,47 | 48,59 | 8.890 |
| GPT-OSS | iso | 1.0 | 123 | Benchmark Sintetis | 79,79 | 81,65 | 80,71 | 74,60 | 80,71 | 6.426 |
| GPT-OSS | iso | 1.0 | 2026 | Test Gold | 56,67 | 50,27 | 53,28 | 45,20 | 51,37 | 8.890 |
| GPT-OSS | iso | 1.0 | 2026 | Benchmark Sintetis | 79,64 | 81,51 | 80,57 | 73,77 | 80,56 | 6.426 |
| GPT-OSS | iso | 1.25 | 42 | Test Gold | 56,00 | 47,20 | 51,22 | 43,76 | 49,03 | 8.890 |
| GPT-OSS | iso | 1.25 | 42 | Benchmark Sintetis | 81,60 | 82,52 | 82,06 | 74,25 | 81,84 | 6.426 |
| GPT-OSS | iso | 1.25 | 123 | Test Gold | 57,46 | 48,19 | 52,42 | 43,60 | 50,19 | 8.890 |
| GPT-OSS | iso | 1.25 | 123 | Benchmark Sintetis | 80,00 | 81,12 | 80,56 | 74,39 | 80,54 | 6.426 |
| GPT-OSS | iso | 1.25 | 2026 | Test Gold | 56,75 | 47,92 | 51,96 | 44,51 | 49,68 | 8.890 |
| GPT-OSS | iso | 1.25 | 2026 | Benchmark Sintetis | 80,56 | 84,08 | 82,28 | 73,98 | 82,18 | 6.426 |
| GPT-OSS | iso | 1.5 | 42 | Test Gold | 55,82 | 47,55 | 51,35 | 43,04 | 49,45 | 8.890 |
| GPT-OSS | iso | 1.5 | 42 | Benchmark Sintetis | 80,18 | 81,85 | 81,01 | 73,28 | 80,97 | 6.426 |
| GPT-OSS | iso | 1.5 | 123 | Test Gold | 57,06 | 47,41 | 51,79 | 43,06 | 49,18 | 8.890 |
| GPT-OSS | iso | 1.5 | 123 | Benchmark Sintetis | 78,15 | 78,87 | 78,51 | 73,54 | 78,66 | 6.426 |
| GPT-OSS | iso | 1.5 | 2026 | Test Gold | 56,89 | 48,80 | 52,53 | 44,17 | 50,25 | 8.890 |
| GPT-OSS | iso | 1.5 | 2026 | Benchmark Sintetis | 78,56 | 80,24 | 79,39 | 71,94 | 79,46 | 6.426 |
| GPT-OSS | iso | max | 42 | Test Gold | 55,15 | 47,48 | 51,03 | 44,09 | 48,87 | 8.890 |
| GPT-OSS | iso | max | 42 | Benchmark Sintetis | 80,45 | 83,78 | 82,09 | 74,26 | 81,92 | 6.426 |
| GPT-OSS | iso | max | 123 | Test Gold | 57,94 | 50,66 | 54,06 | 45,41 | 51,58 | 8.890 |
| GPT-OSS | iso | max | 123 | Benchmark Sintetis | 78,38 | 82,99 | 80,62 | 74,49 | 81,05 | 6.426 |
| GPT-OSS | iso | max | 2026 | Test Gold | 57,79 | 49,98 | 53,60 | 44,90 | 51,31 | 8.890 |
| GPT-OSS | iso | max | 2026 | Benchmark Sintetis | 80,05 | 80,30 | 80,17 | 73,45 | 80,06 | 6.426 |

## L.3 Evaluasi Transfer Lintas Dataset per Run dan Seed

Tabel L.3 memuat evaluasi transfer lintas domain pada 6 dataset eksternal (IndQNER, IndoLEM UI, IndoLEM UGM, Prosa, Singgalang, WikiANN).

**Tabel L.3 Rincian metrik per-run pada evaluasi transfer lintas domain**

| Korpus Latih | Seed | Dataset Eksternal | Proyeksi Label | Presisi (%) | Recall (%) | Micro-F1 (%) | Support |
| --- | --- | --- | --- | --- | --- | --- | --- |
| NERGRIT (Gold) | 42 | Nergrit | full18 | 83,65 | 84,22 | 83,93 | 8.890 |
| NERGRIT (Gold) | 42 | Indqner | common_PER_LOC | 85,62 | 37,71 | 52,36 | 663 |
| NERGRIT (Gold) | 42 | Indolem Ui | common_PER_LOC | 92,15 | 82,81 | 87,23 | 3.106 |
| NERGRIT (Gold) | 42 | Indolem Ui | additional_ORG | 77,18 | 55,52 | 64,58 | 1.949 |
| NERGRIT (Gold) | 42 | Indolem Ugm | common_PER_LOC | 77,65 | 85,45 | 81,36 | 2.516 |
| NERGRIT (Gold) | 42 | Indolem Ugm | additional_ORG | 48,66 | 22,11 | 30,41 | 823 |
| NERGRIT (Gold) | 42 | Prosa | common_PER_LOC | 86,56 | 81,75 | 84,08 | 10.434 |
| NERGRIT (Gold) | 42 | Singgalang | common_PER_LOC | 41,26 | 53,09 | 46,43 | 90.873 |
| NERGRIT (Gold) | 42 | Singgalang | additional_ORG | 8,21 | 39,38 | 13,59 | 7.336 |
| NERGRIT (Gold) | 42 | Wikiann | common_PER_LOC | 45,67 | 55,51 | 50,11 | 30.988 |
| NERGRIT (Gold) | 42 | Wikiann | additional_ORG | 67,84 | 33,08 | 44,48 | 14.827 |
| NERGRIT (Gold) | 123 | Nergrit | full18 | 83,54 | 84,77 | 84,15 | 8.890 |
| NERGRIT (Gold) | 123 | Indqner | common_PER_LOC | 85,49 | 41,78 | 56,13 | 663 |
| NERGRIT (Gold) | 123 | Indolem Ui | common_PER_LOC | 92,42 | 82,45 | 87,15 | 3.106 |
| NERGRIT (Gold) | 123 | Indolem Ui | additional_ORG | 77,01 | 57,57 | 65,88 | 1.949 |
| NERGRIT (Gold) | 123 | Indolem Ugm | common_PER_LOC | 77,74 | 84,94 | 81,18 | 2.516 |
| NERGRIT (Gold) | 123 | Indolem Ugm | additional_ORG | 46,98 | 22,72 | 30,63 | 823 |
| NERGRIT (Gold) | 123 | Prosa | common_PER_LOC | 86,87 | 81,58 | 84,14 | 10.434 |
| NERGRIT (Gold) | 123 | Singgalang | common_PER_LOC | 42,28 | 53,73 | 47,32 | 90.873 |
| NERGRIT (Gold) | 123 | Singgalang | additional_ORG | 8,47 | 42,69 | 14,14 | 7.336 |
| NERGRIT (Gold) | 123 | Wikiann | common_PER_LOC | 46,13 | 55,14 | 50,24 | 30.988 |
| NERGRIT (Gold) | 123 | Wikiann | additional_ORG | 65,43 | 33,53 | 44,34 | 14.827 |
| NERGRIT (Gold) | 2026 | Nergrit | full18 | 84,26 | 85,19 | 84,72 | 8.890 |
| NERGRIT (Gold) | 2026 | Indqner | common_PER_LOC | 82,19 | 39,67 | 53,51 | 663 |
| NERGRIT (Gold) | 2026 | Indolem Ui | common_PER_LOC | 92,58 | 83,19 | 87,64 | 3.106 |
| NERGRIT (Gold) | 2026 | Indolem Ui | additional_ORG | 78,22 | 58,03 | 66,63 | 1.949 |
| NERGRIT (Gold) | 2026 | Indolem Ugm | common_PER_LOC | 78,30 | 85,17 | 81,59 | 2.516 |
| NERGRIT (Gold) | 2026 | Indolem Ugm | additional_ORG | 51,19 | 23,57 | 32,28 | 823 |
| NERGRIT (Gold) | 2026 | Prosa | common_PER_LOC | 86,91 | 81,23 | 83,97 | 10.434 |
| NERGRIT (Gold) | 2026 | Singgalang | common_PER_LOC | 41,69 | 52,65 | 46,53 | 90.873 |
| NERGRIT (Gold) | 2026 | Singgalang | additional_ORG | 8,63 | 41,93 | 14,32 | 7.336 |
| NERGRIT (Gold) | 2026 | Wikiann | common_PER_LOC | 48,29 | 55,90 | 51,82 | 30.988 |
| NERGRIT (Gold) | 2026 | Wikiann | additional_ORG | 70,90 | 34,72 | 46,61 | 14.827 |
| Nemotron | 42 | Nergrit | full18 | 54,74 | 51,11 | 52,86 | 8.890 |
| Nemotron | 42 | Indqner | common_PER_LOC | 76,92 | 25,64 | 38,46 | 663 |
| Nemotron | 42 | Indolem Ui | common_PER_LOC | 93,58 | 76,43 | 84,14 | 3.106 |
| Nemotron | 42 | Indolem Ui | additional_ORG | 79,59 | 77,42 | 78,49 | 1.949 |
| Nemotron | 42 | Indolem Ugm | common_PER_LOC | 78,26 | 76,27 | 77,25 | 2.516 |
| Nemotron | 42 | Indolem Ugm | additional_ORG | 38,61 | 63,67 | 48,07 | 823 |
| Nemotron | 42 | Prosa | common_PER_LOC | 87,15 | 71,17 | 78,35 | 10.434 |
| Nemotron | 42 | Singgalang | common_PER_LOC | 46,17 | 50,32 | 48,15 | 90.873 |
| Nemotron | 42 | Singgalang | additional_ORG | 9,74 | 54,14 | 16,51 | 7.336 |
| Nemotron | 42 | Wikiann | common_PER_LOC | 41,89 | 45,32 | 43,54 | 30.988 |
| Nemotron | 42 | Wikiann | additional_ORG | 61,57 | 30,82 | 41,08 | 14.827 |
| Nemotron | 123 | Nergrit | full18 | 54,71 | 50,87 | 52,72 | 8.890 |
| Nemotron | 123 | Indqner | common_PER_LOC | 73,91 | 15,38 | 25,47 | 663 |
| Nemotron | 123 | Indolem Ui | common_PER_LOC | 93,34 | 78,56 | 85,31 | 3.106 |
| Nemotron | 123 | Indolem Ui | additional_ORG | 80,70 | 77,68 | 79,16 | 1.949 |
| Nemotron | 123 | Indolem Ugm | common_PER_LOC | 78,04 | 78,82 | 78,43 | 2.516 |
| Nemotron | 123 | Indolem Ugm | additional_ORG | 39,78 | 65,49 | 49,49 | 823 |
| Nemotron | 123 | Prosa | common_PER_LOC | 87,42 | 72,75 | 79,42 | 10.434 |
| Nemotron | 123 | Singgalang | common_PER_LOC | 46,02 | 50,15 | 48,00 | 90.873 |
| Nemotron | 123 | Singgalang | additional_ORG | 9,72 | 52,44 | 16,40 | 7.336 |
| Nemotron | 123 | Wikiann | common_PER_LOC | 44,17 | 43,13 | 43,64 | 30.988 |
| Nemotron | 123 | Wikiann | additional_ORG | 63,17 | 30,64 | 41,26 | 14.827 |
| Nemotron | 2026 | Nergrit | full18 | 52,94 | 49,70 | 51,26 | 8.890 |
| Nemotron | 2026 | Indqner | common_PER_LOC | 54,76 | 6,94 | 12,32 | 663 |
| Nemotron | 2026 | Indolem Ui | common_PER_LOC | 93,62 | 75,53 | 83,61 | 3.106 |
| Nemotron | 2026 | Indolem Ui | additional_ORG | 76,82 | 79,58 | 78,18 | 1.949 |
| Nemotron | 2026 | Indolem Ugm | common_PER_LOC | 77,93 | 74,24 | 76,04 | 2.516 |
| Nemotron | 2026 | Indolem Ugm | additional_ORG | 37,47 | 68,29 | 48,39 | 823 |
| Nemotron | 2026 | Prosa | common_PER_LOC | 87,56 | 69,78 | 77,67 | 10.434 |
| Nemotron | 2026 | Singgalang | common_PER_LOC | 46,68 | 49,97 | 48,27 | 90.873 |
| Nemotron | 2026 | Singgalang | additional_ORG | 9,49 | 56,54 | 16,25 | 7.336 |
| Nemotron | 2026 | Wikiann | common_PER_LOC | 44,72 | 44,39 | 44,56 | 30.988 |
| Nemotron | 2026 | Wikiann | additional_ORG | 51,01 | 33,46 | 40,41 | 14.827 |
| Luna | 42 | Nergrit | full18 | 58,70 | 51,44 | 54,83 | 8.890 |
| Luna | 42 | Indqner | common_PER_LOC | 34,85 | 6,94 | 11,57 | 663 |
| Luna | 42 | Indolem Ui | common_PER_LOC | 93,10 | 72,12 | 81,28 | 3.106 |
| Luna | 42 | Indolem Ui | additional_ORG | 81,39 | 79,43 | 80,39 | 1.949 |
| Luna | 42 | Indolem Ugm | common_PER_LOC | 77,61 | 73,57 | 75,54 | 2.516 |
| Luna | 42 | Indolem Ugm | additional_ORG | 43,07 | 72,54 | 54,05 | 823 |
| Luna | 42 | Prosa | common_PER_LOC | 87,45 | 68,81 | 77,02 | 10.434 |
| Luna | 42 | Singgalang | common_PER_LOC | 45,45 | 49,09 | 47,20 | 90.873 |
| Luna | 42 | Singgalang | additional_ORG | 9,60 | 55,38 | 16,36 | 7.336 |
| Luna | 42 | Wikiann | common_PER_LOC | 32,72 | 38,99 | 35,58 | 30.988 |
| Luna | 42 | Wikiann | additional_ORG | 63,16 | 29,40 | 40,12 | 14.827 |
| Luna | 123 | Nergrit | full18 | 58,41 | 52,51 | 55,30 | 8.890 |
| Luna | 123 | Indqner | common_PER_LOC | 82,69 | 19,46 | 31,50 | 663 |
| Luna | 123 | Indolem Ui | common_PER_LOC | 93,74 | 78,11 | 85,21 | 3.106 |
| Luna | 123 | Indolem Ui | additional_ORG | 79,24 | 77,17 | 78,19 | 1.949 |
| Luna | 123 | Indolem Ugm | common_PER_LOC | 78,55 | 77,58 | 78,06 | 2.516 |
| Luna | 123 | Indolem Ugm | additional_ORG | 42,82 | 73,51 | 54,11 | 823 |
| Luna | 123 | Prosa | common_PER_LOC | 88,87 | 72,96 | 80,14 | 10.434 |
| Luna | 123 | Singgalang | common_PER_LOC | 46,54 | 49,53 | 47,99 | 90.873 |
| Luna | 123 | Singgalang | additional_ORG | 9,18 | 53,61 | 15,68 | 7.336 |
| Luna | 123 | Wikiann | common_PER_LOC | 47,96 | 45,01 | 46,44 | 30.988 |
| Luna | 123 | Wikiann | additional_ORG | 59,13 | 30,57 | 40,30 | 14.827 |
| Luna | 2026 | Nergrit | full18 | 58,52 | 51,17 | 54,60 | 8.890 |
| Luna | 2026 | Indqner | common_PER_LOC | 35,06 | 4,07 | 7,30 | 663 |
| Luna | 2026 | Indolem Ui | common_PER_LOC | 93,33 | 73,86 | 82,46 | 3.106 |
| Luna | 2026 | Indolem Ui | additional_ORG | 80,67 | 80,09 | 80,38 | 1.949 |
| Luna | 2026 | Indolem Ugm | common_PER_LOC | 78,12 | 74,52 | 76,28 | 2.516 |
| Luna | 2026 | Indolem Ugm | additional_ORG | 42,85 | 72,78 | 53,94 | 823 |
| Luna | 2026 | Prosa | common_PER_LOC | 87,91 | 70,50 | 78,25 | 10.434 |
| Luna | 2026 | Singgalang | common_PER_LOC | 46,00 | 50,22 | 48,02 | 90.873 |
| Luna | 2026 | Singgalang | additional_ORG | 9,47 | 59,21 | 16,33 | 7.336 |
| Luna | 2026 | Wikiann | common_PER_LOC | 43,88 | 39,78 | 41,73 | 30.988 |
| Luna | 2026 | Wikiann | additional_ORG | 55,13 | 32,09 | 40,57 | 14.827 |
| Gemma | 42 | Nergrit | full18 | 55,54 | 50,79 | 53,06 | 8.890 |
| Gemma | 42 | Indqner | common_PER_LOC | 76,32 | 8,75 | 15,70 | 663 |
| Gemma | 42 | Indolem Ui | common_PER_LOC | 92,80 | 75,08 | 83,00 | 3.106 |
| Gemma | 42 | Indolem Ui | additional_ORG | 78,96 | 82,81 | 80,84 | 1.949 |
| Gemma | 42 | Indolem Ugm | common_PER_LOC | 77,90 | 76,91 | 77,40 | 2.516 |
| Gemma | 42 | Indolem Ugm | additional_ORG | 39,78 | 74,48 | 51,86 | 823 |
| Gemma | 42 | Prosa | common_PER_LOC | 87,18 | 71,04 | 78,28 | 10.434 |
| Gemma | 42 | Singgalang | common_PER_LOC | 48,22 | 50,36 | 49,27 | 90.873 |
| Gemma | 42 | Singgalang | additional_ORG | 11,22 | 63,88 | 19,09 | 7.336 |
| Gemma | 42 | Wikiann | common_PER_LOC | 34,59 | 39,24 | 36,77 | 30.988 |
| Gemma | 42 | Wikiann | additional_ORG | 47,14 | 22,77 | 30,71 | 14.827 |
| Gemma | 123 | Nergrit | full18 | 57,83 | 51,63 | 54,56 | 8.890 |
| Gemma | 123 | Indqner | common_PER_LOC | 74,04 | 11,61 | 20,08 | 663 |
| Gemma | 123 | Indolem Ui | common_PER_LOC | 92,54 | 79,49 | 85,52 | 3.106 |
| Gemma | 123 | Indolem Ui | additional_ORG | 79,45 | 80,14 | 79,80 | 1.949 |
| Gemma | 123 | Indolem Ugm | common_PER_LOC | 77,86 | 80,37 | 79,09 | 2.516 |
| Gemma | 123 | Indolem Ugm | additional_ORG | 40,76 | 75,33 | 52,90 | 823 |
| Gemma | 123 | Prosa | common_PER_LOC | 86,98 | 74,15 | 80,06 | 10.434 |
| Gemma | 123 | Singgalang | common_PER_LOC | 47,30 | 49,97 | 48,60 | 90.873 |
| Gemma | 123 | Singgalang | additional_ORG | 10,03 | 59,05 | 17,14 | 7.336 |
| Gemma | 123 | Wikiann | common_PER_LOC | 41,79 | 40,65 | 41,21 | 30.988 |
| Gemma | 123 | Wikiann | additional_ORG | 50,10 | 26,15 | 34,36 | 14.827 |
| Gemma | 2026 | Nergrit | full18 | 55,73 | 47,28 | 51,16 | 8.890 |
| Gemma | 2026 | Indqner | common_PER_LOC | 51,02 | 3,77 | 7,02 | 663 |
| Gemma | 2026 | Indolem Ui | common_PER_LOC | 92,29 | 74,34 | 82,35 | 3.106 |
| Gemma | 2026 | Indolem Ui | additional_ORG | 83,43 | 77,27 | 80,23 | 1.949 |
| Gemma | 2026 | Indolem Ugm | common_PER_LOC | 78,07 | 74,40 | 76,19 | 2.516 |
| Gemma | 2026 | Indolem Ugm | additional_ORG | 42,05 | 70,72 | 52,74 | 823 |
| Gemma | 2026 | Prosa | common_PER_LOC | 86,72 | 69,05 | 76,89 | 10.434 |
| Gemma | 2026 | Singgalang | common_PER_LOC | 47,66 | 48,82 | 48,23 | 90.873 |
| Gemma | 2026 | Singgalang | additional_ORG | 11,26 | 58,87 | 18,91 | 7.336 |
| Gemma | 2026 | Wikiann | common_PER_LOC | 39,38 | 36,52 | 37,90 | 30.988 |
| Gemma | 2026 | Wikiann | additional_ORG | 46,79 | 22,79 | 30,65 | 14.827 |
| GPT-OSS | 42 | Nergrit | full18 | 55,15 | 47,48 | 51,03 | 8.890 |
| GPT-OSS | 42 | Indqner | common_PER_LOC | 68,57 | 7,24 | 13,10 | 663 |
| GPT-OSS | 42 | Indolem Ui | common_PER_LOC | 91,77 | 72,18 | 80,81 | 3.106 |
| GPT-OSS | 42 | Indolem Ui | additional_ORG | 80,54 | 78,35 | 79,43 | 1.949 |
| GPT-OSS | 42 | Indolem Ugm | common_PER_LOC | 78,09 | 72,26 | 75,06 | 2.516 |
| GPT-OSS | 42 | Indolem Ugm | additional_ORG | 40,50 | 67,07 | 50,50 | 823 |
| GPT-OSS | 42 | Prosa | common_PER_LOC | 85,40 | 68,11 | 75,78 | 10.434 |
| GPT-OSS | 42 | Singgalang | common_PER_LOC | 47,57 | 51,86 | 49,62 | 90.873 |
| GPT-OSS | 42 | Singgalang | additional_ORG | 10,37 | 57,78 | 17,59 | 7.336 |
| GPT-OSS | 42 | Wikiann | common_PER_LOC | 37,37 | 41,38 | 39,27 | 30.988 |
| GPT-OSS | 42 | Wikiann | additional_ORG | 61,69 | 33,46 | 43,39 | 14.827 |
| GPT-OSS | 123 | Nergrit | full18 | 57,94 | 50,66 | 54,06 | 8.890 |
| GPT-OSS | 123 | Indqner | common_PER_LOC | 76,30 | 15,54 | 25,81 | 663 |
| GPT-OSS | 123 | Indolem Ui | common_PER_LOC | 93,62 | 78,88 | 85,62 | 3.106 |
| GPT-OSS | 123 | Indolem Ui | additional_ORG | 80,35 | 82,66 | 81,49 | 1.949 |
| GPT-OSS | 123 | Indolem Ugm | common_PER_LOC | 79,70 | 79,25 | 79,47 | 2.516 |
| GPT-OSS | 123 | Indolem Ugm | additional_ORG | 40,61 | 71,45 | 51,78 | 823 |
| GPT-OSS | 123 | Prosa | common_PER_LOC | 87,93 | 73,37 | 79,99 | 10.434 |
| GPT-OSS | 123 | Singgalang | common_PER_LOC | 46,87 | 51,22 | 48,95 | 90.873 |
| GPT-OSS | 123 | Singgalang | additional_ORG | 10,03 | 59,38 | 17,17 | 7.336 |
| GPT-OSS | 123 | Wikiann | common_PER_LOC | 41,29 | 43,39 | 42,32 | 30.988 |
| GPT-OSS | 123 | Wikiann | additional_ORG | 61,44 | 31,46 | 41,61 | 14.827 |
| GPT-OSS | 2026 | Nergrit | full18 | 57,79 | 49,98 | 53,60 | 8.890 |
| GPT-OSS | 2026 | Indqner | common_PER_LOC | 62,96 | 7,69 | 13,71 | 663 |
| GPT-OSS | 2026 | Indolem Ui | common_PER_LOC | 93,16 | 76,27 | 83,87 | 3.106 |
| GPT-OSS | 2026 | Indolem Ui | additional_ORG | 79,82 | 78,55 | 79,18 | 1.949 |
| GPT-OSS | 2026 | Indolem Ugm | common_PER_LOC | 78,28 | 76,35 | 77,30 | 2.516 |
| GPT-OSS | 2026 | Indolem Ugm | additional_ORG | 41,75 | 69,14 | 52,06 | 823 |
| GPT-OSS | 2026 | Prosa | common_PER_LOC | 87,43 | 70,81 | 78,25 | 10.434 |
| GPT-OSS | 2026 | Singgalang | common_PER_LOC | 47,63 | 50,85 | 49,19 | 90.873 |
| GPT-OSS | 2026 | Singgalang | additional_ORG | 10,33 | 59,41 | 17,60 | 7.336 |
| GPT-OSS | 2026 | Wikiann | common_PER_LOC | 41,63 | 39,09 | 40,32 | 30.988 |
| GPT-OSS | 2026 | Wikiann | additional_ORG | 61,35 | 33,58 | 43,40 | 14.827 |
