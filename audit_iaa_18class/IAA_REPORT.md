# Independent Dual-Annotator Audit — IAA Report (18-Class NERGRIT)

- Annotator A1: `cx/gpt-6-luna` (reasoning_effort: `high`)
- Annotator A2: `ag/gemini-3.8-flash-high` (reasoning_effort: `high`)
- Samples compared: 300 (7,732 tokens, seed 20261022)
- Consensus rule: dual_agreement: original span overturned only if both annotators reject it; new/replacement span added only if both annotators propose the identical span

## IAA Total (95% Bootstrap CI)

| Metric | Value | Interpretation |
| --- | --- | --- |
| Token Cohen's κ (37 BIO tags) | 0,966 [0,958–0,972] | Hampir sempurna (almost perfect) |
| Token Cohen's κ (18 classes + O) | 0,972 [0,966–0,978] | Hampir sempurna (almost perfect) |
| Entity-decision κ (KEEP/REMOVE/REPLACE) | 0,602 [0,519–0,674] | Substansial (substantial) |
| Entity-decision κ (CORRECT/INCORRECT) | 0,608 [0,522–0,682] | Substansial (substantial) |
| Pairwise exact span-F1 | 0,938 [0,926–0,950] | - |
| Token % agreement (BIO) | 97,53% | - |
| Identical sentences | 70,67% | - |

## IAA per Dataset

| Dataset | κ token BIO | κ token kelas | κ keputusan (3) | Span-F1 IAA | Kalimat identik |
| --- | --- | --- | --- | --- | --- |
| nemotron | 0,959 | 0,967 | 0,707 | 92,86% | 63,00% |
| luna | 0,976 | 0,979 | 0,419 | 95,79% | 79,00% |
| gemma | 0,962 | 0,971 | 0,453 | 92,78% | 70,00% |

## Dataset Annotation Quality vs Dual-Agreement Consensus

| Dataset | Benar | Salah | Terlewat | Presisi | Recall | F1 | Kalimat bermasalah |
| --- | --- | --- | --- | --- | --- | --- | --- |
| nemotron | 634 | 57 | 0 | 91,75% | 91,88% | 91,82% | 42 |
| luna | 549 | 11 | 3 | 98,04% | 98,21% | 98,12% | 11 |
| gemma | 379 | 13 | 7 | 96,68% | 96,44% | 96,56% | 13 |
| TOTAL | 1562 | 81 | 10 | 95,07% | 95,13% | 95,10% | 66 |
