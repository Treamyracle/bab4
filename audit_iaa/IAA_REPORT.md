# Independent Dual-Annotator Audit — IAA Report

- Annotator A1: Arif Athaya Harahap
- Annotator A2: Muhammad Faiz Fauzan
- Samples compared: 400 kalimat (4 korpus sintetis terstratifikasi: nemotron, luna, gemma, gpt_oss; 10.812 token; seed 20261022)
- Consensus rule: dual_agreement: original span overturned only if both annotators reject it; new/replacement span added only if both annotators propose the identical span

## IAA total (4 Korpus Sintetis — 95% bootstrap CI)

| Metric | Value | Interpretation |
| --- | --- | --- |
| Token Cohen's κ (37 BIO tags) | 0,987 [0,983–0,991] | Hampir sempurna (almost perfect) |
| Token Cohen's κ (18 classes + O) | 0,989 [0,985–0,993] | Hampir sempurna (almost perfect) |
| Entity-decision κ (KEEP/REMOVE/REPLACE) | 0,923 [0,895–0,947] | Hampir sempurna (almost perfect) |
| Entity-decision κ (CORRECT/INCORRECT) | 0,928 [0,899–0,952] | Hampir sempurna (almost perfect) |
| Pairwise exact span-F1 | 0,976 [0,968–0,983] (97,63%) | Konsistensi batas rentang sangat tinggi |
| Token % agreement (BIO) | 99,13% | 10.718 / 10.812 token identik |
| Identical sentences | 89,75% | 359 / 400 kalimat identik tanpa selisih |

## IAA per dataset sintetis

| Dataset | κ token BIO | κ token kelas | κ keputusan (3) | Span-F1 IAA | Kalimat identik |
| --- | --- | --- | --- | --- | --- |
| nemotron | 0,977 | 0,981 | 0,886 | 95,93% | 82,00% |
| luna | 0,992 | 0,992 | 0,911 | 98,46% | 92,00% |
| gemma | 0,988 | 0,989 | 0,927 | 97,60% | 92,00% |
| gpt_oss | 0,994 | 0,995 | 0,965 | 98,72% | 93,00% |
| **Total Gabungan** | **0,987** | **0,989** | **0,923** | **97,63%** | **89,75%** |

## Dataset annotation quality vs dual-agreement consensus

| Dataset | Benar | Salah | Terlewat | Presisi | Recall | F1 | Kalimat bermasalah |
| --- | --- | --- | --- | --- | --- | --- | --- |
| nemotron | 517 | 118 | 21 | 81,42% | 86,17% | 83,72% | 73 |
| luna | 493 | 27 | 12 | 94,81% | 95,17% | 94,99% | 28 |
| gemma | 297 | 78 | 14 | 79,20% | 83,90% | 81,48% | 62 |
| gpt_oss | 451 | 97 | 36 | 82,30% | 82,90% | 82,60% | 75 |
| **TOTAL** | **1.758** | **320** | **83** | **84,60%** | **87,20%** | **85,88%** | **238** |
