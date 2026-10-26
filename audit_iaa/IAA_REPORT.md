# Independent Dual-Annotator Audit — IAA Report

- Annotator A1: Arif Athaya Harahap
- Annotator A2: Muhammad Faiz Fauzan
- Samples compared: 600 (seed 20261022)
- Consensus rule: dual_agreement: original span overturned only if both annotators reject it; new/replacement span added only if both annotators propose the identical span

## IAA total (95% bootstrap CI)

| Metric | Value | Interpretation |
| --- | --- | --- |
| Token Cohen's κ (37 BIO tags) | 0,988 [0,984–0,991] | Hampir sempurna (almost perfect) |
| Token Cohen's κ (18 classes + O) | 0,990 [0,987–0,993] | Hampir sempurna (almost perfect) |
| Entity-decision κ (KEEP/REMOVE/REPLACE) | 0,932 [0,909–0,952] | Hampir sempurna (almost perfect) |
| Entity-decision κ (CORRECT/INCORRECT) | 0,936 [0,912–0,955] | Hampir sempurna (almost perfect) |
| Pairwise exact span-F1 | 0,978 [0,972–0,984] | - |
| Token % agreement (BIO) | 99,19% | - |
| Identical sentences | 90,83% | - |

## IAA per dataset

| Dataset | κ token BIO | κ token kelas | κ keputusan (3) | Span-F1 IAA | Kalimat identik |
| --- | --- | --- | --- | --- | --- |
| gold | 0,969 | 0,976 | 0,929 | 95,41% | 89,00% |
| nemotron | 0,977 | 0,981 | 0,886 | 95,93% | 82,00% |
| luna | 0,992 | 0,992 | 0,911 | 98,46% | 92,00% |
| gemma | 0,988 | 0,989 | 0,927 | 97,60% | 92,00% |
| gpt_oss | 0,994 | 0,995 | 0,965 | 98,72% | 93,00% |
| benchmark | 0,998 | 0,998 | 0,970 | 99,53% | 97,00% |

## Dataset annotation quality vs dual-agreement consensus

| Dataset | Benar | Salah | Terlewat | Presisi | Recall | F1 | Kalimat bermasalah |
| --- | --- | --- | --- | --- | --- | --- | --- |
| gold | 213 | 102 | 14 | 67,62% | 70,76% | 69,16% | 57 |
| nemotron | 517 | 118 | 21 | 81,42% | 86,17% | 83,72% | 73 |
| luna | 493 | 27 | 12 | 94,81% | 95,17% | 94,99% | 28 |
| gemma | 297 | 78 | 14 | 79,20% | 83,90% | 81,48% | 62 |
| gpt_oss | 451 | 97 | 36 | 82,30% | 82,90% | 82,60% | 75 |
| benchmark | 582 | 53 | 10 | 91,65% | 90,65% | 91,15% | 46 |
| TOTAL | 2553 | 475 | 107 | 84,31% | 86,28% | 85,28% | 341 |
