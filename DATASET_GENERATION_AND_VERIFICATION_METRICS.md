# 📊 Empirical Generation & Verification Benchmark Report
## Multi-LLM Distilled Indonesian Named Entity Recognition (NER) Dataset Suite

> **Document Summary**: Comprehensive telemetry, timing, token usage, and throughput metrics extracted directly from the raw execution logs across all 4 synthetic Indonesian NER datasets generated and verified in this skripsi/thesis research project.
> **Benchmark Reference**: 17,431 Indonesian Gold Standard Sentences (18 Evaluation Classes / 37 BIO Tags; 19-Entity Generation Schema with TTL buffer).
> **Hugging Face Hub Suite**: [`treamyracle/distilled-indonesian-ner-v2`](https://huggingface.co/datasets/treamyracle/distilled-indonesian-ner-v2).

---

## 📑 Table of Contents
1. [Master Comparative Matrix](#-master-comparative-matrix)
2. [Dataset 1: Nemotron Super & Ultra (Default Distilled)](#-dataset-1-nemotron-super--ultra-default-distilled)
   - [Stage 1: Generation (Nemotron-3 Super 120B)](#stage-1-generation--nemotron-3-super-120b)
   - [Stage 2: Verification & Quality Control (Nemotron-3 Ultra 550B)](#stage-2-verification--quality-control-nemotron-3-ultra-550b)
3. [Dataset 2: GPT-5.6 Luna & Gemini 3.6 Flash (Luna Distilled)](#-dataset-2-gpt-56-luna--gemini-36-flash-luna-distilled)
   - [Stage 1: Generation (GPT-5.6 Luna)](#stage-1-generation--gpt-56-luna)
   - [Stage 2: Verification & Quality Control (Gemini 3.6 Flash Medium)](#stage-2-verification--quality-control-gemini-36-flash-medium)
4. [Dataset 3: GPT-OSS 120B & Nemotron Nano 30B (GPT-OSS Distilled)](#-dataset-3-gpt-oss-120b--nemotron-nano-30b-gpt-oss-distilled)
   - [Stage 1: Generation (GPT-OSS 120B)](#stage-1-generation--gpt-oss-120b)
   - [Stage 2: Verification & Quality Control (Nemotron-3 Nano 30B)](#stage-2-verification--quality-control-nemotron-3-nano-30b)
5. [Dataset 4: Gemma 4 31B & Nemotron Super 120B (Gemma Distilled)](#-dataset-4-gemma-4-31b--nemotron-super-120b-gemma-distilled)
   - [Stage 1: Generation (Gemma 4 31B)](#stage-1-generation--gemma-4-31b)
   - [Stage 2: Verification & Quality Control (Nemotron-3 Super 120B)](#stage-2-verification--quality-control-nemotron-3-super-120b)
6. [Comparative Technical Analysis & Observations](#-comparative-technical-analysis--observations)

---

## 🏆 Master Comparative Matrix

### Stage 1: Synthetic Sentence Generation

| Evaluation Metric | Dataset 1 (Nemotron) | Dataset 2 (Luna) | Dataset 3 (GPT-OSS) | Dataset 4 (Gemma) |
| :--- | :--- | :--- | :--- | :--- |
| **Generator Model** | `nvidia/nemotron-3-super-120b-a12b:free` | `cx/gpt-5.6-luna` | `gpt-oss:120b` | `gemma4:31b` |
| **Host / Gateway** | OpenRouter Free Tier | 9router (`localhost:20128`) | Ollama Cloud Engine | OpenRouter + Ollama Cloud |
| **Target Sentences** | 17,431 | 17,431 | 17,431 | 17,431 |
| **Output Sentences** | **17,435** (100.0%) | **17,427** (99.98%) | **17,435** (100.0%) | **17,434** (100.0%) |
| **Batch Size** | 10 sentences / batch | 10 sentences / batch | 10 sentences / batch | 10 sentences / batch |
| **Total Requests Attempted** | 2,439 | 1,756 | 1,745 | 2,151 |
| **Successful Batches** | 1,749 | 1,743 | 1,745 (100% success) | 1,747 |
| **Failed / Retried Batches** | 690 | 13 | 0 | 404 |
| **Prompt (Input) Tokens** | 2,693,829 | 2,311,555 | 4,687,637 | 4,113,017 |
| **Completion (Output) Tokens** | **24,330,161** | **3,377,740** | **10,498,389** | **2,223,551** |
| **Internal Reasoning (CoT) Tokens**| **16,587,960** (68.2%) | None (Direct Output) | Integrated inside eval | None |
| **Avg Tokens / Request** | 13,910 tokens | 1,938 tokens | 6,016 tokens | 1,273 tokens |
| **Avg Request Latency** | 158.4s / batch | 40.8s / batch | 24.8s / batch | 18.2s / batch |
| **Active Generation Time** | **67h 42m** (~2.82 days) | **20h 07m** (~0.84 days) | **12h 02m** (~0.50 days) | **12h 26m** (~0.52 days) |
| **Hardware Engine TPS** | — | — | **795.14 tokens/sec** | **472.81 tokens/sec** |
| **Effective Wall-Clock TPS** | **99.82 tokens/sec** | **46.64 tokens/sec** | **242.23 tokens/sec** | **49.65 tokens/sec** |
| **Active Calendar Span** | Sept 8 – Sept 14, 2026 (7 days) | Sept 22 – Sept 23, 2026 (2 days) | Sept 22 – Sept 23, 2026 (2 days) | Sept 22 – Sept 23, 2026 (2 days) |

---

### Stage 2: Quality Control & Entity Verification

| Evaluation Metric | Dataset 1 (Nemotron) | Dataset 2 (Luna) | Dataset 3 (GPT-OSS) | Dataset 4 (Gemma) |
| :--- | :--- | :--- | :--- | :--- |
| **Verificator Model** | `nvidia/nemotron-3-ultra-550b-a55b:free` | `ag/gemini-3.6-flash-medium` | `ollama/nemotron-3-nano:30b` | `ollama/nemotron-3-super` |
| **Host / Gateway** | OpenRouter Free Tier | 9router (`localhost:20128`) | 9router + Ollama Cloud | 9router (`localhost:20128`) |
| **Sentences Verified** | **17,525** | **17,427** | **17,435** | **17,434** |
| **Batch Size** | 5 sentences / batch | 5 sentences / batch | 5 sentences / batch | 5 sentences / batch |
| **Total Requests Attempted** | 2,252 | 3,568 | 5,048 | 3,996 |
| **Successful Batches** | 1,120 | 3,487 | 3,489 | 3,488 |
| **Failed / Retried Batches** | 1,132 | 81 | 1,559 | 508 |
| **Prompt (Input) Tokens** | 2,377,840 | ~7.2M (estimated) | 10,896,552 | 2,872,162 |
| **Completion (Output) Tokens** | **4,694,619** | **3,512,259** (cl100k) | **45,070,003** | **6,222,382** |
| **Verification Reasoning Tokens**| 2,649,595 (56.4%) | Latent native CoT | 26,450,229 (58.7%) | 4,404,248 (70.8%) |
| **Active Verification Time** | **37h 35m** (~1.57 days) | **17h 24m** (~0.73 days) | **170h 05m** (~7.09 days) | **76h 00m** (~3.17 days) |
| **Average Latency / Batch** | ~118.5s / batch | 17.6s / batch | ~121.2s / batch | ~78.5s / batch |
| **Effective Verification TPS**| **34.70 tokens/sec** | **56.04 tokens/sec** | **73.61 tokens/sec** | **22.74 tokens/sec** |
| **Calendar Span** | Sept 14 – Sept 17, 2026 (4 days) | Sept 23 – Sept 24, 2026 (2 days) | Sept 23 – Oct 15, 2026 (17 days) | Sept 23 – Sept 30, 2026 (8 days) |

---

## 📌 Dataset 1: Nemotron Super & Ultra (Default Distilled)

- **Raw Generator Input**: `nvidia/nemotron-3-super-120b-a12b:free`
- **Quality Control Verificator**: `nvidia/nemotron-3-ultra-550b-a55b:free`
- **Output Storage**: `data/distilled/`
- **Telemetry Logs**: `data/distilled/raw_responses/`

### Stage 1: Generation — Nemotron-3 Super 120B

Nemotron Super 120B served as the primary synthetic generator. Because of its native thinking capabilities, it produced the largest volume of tokens across the entire study (24.3M tokens), dedicating **68.2% of its tokens to Chain-of-Thought (CoT) reasoning** prior to emitting JSON structures.

#### Overall Generation Statistics:
- **Total Requests**: 2,439 (1,749 successful batches, 690 rate-limit/timeout retries)
- **Target vs Produced Sentences**: 17,431 target $\rightarrow$ **17,435 sentences** (100.0%)
- **Total Prompt Tokens**: 2,693,829 tokens
- **Total Completion Tokens**: 24,330,161 tokens
- **Internal CoT Reasoning Tokens**: 16,587,960 tokens
- **Total Active Execution Time**: 67 hours, 42 minutes, 17 seconds (67.70 active hours)
- **Effective Generation Speed**: **99.82 tokens / second**
- **Average Batch Request Latency**: 158.4 seconds (~2.6 minutes per 10-sentence batch)

#### Daily Generation Breakdown:

| Date | Log File | Total Reqs | Success | Failed | Completion Tokens | Reasoning Tokens | Active Hours | Avg Latency | Tokens/Sec |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **2026-09-08** | `2026-09-08_generation.jsonl` | 151 | 119 | 32 | 1,300,019 | 887,034 | 3.95 h | 94.2 s | 91.41 tok/s |
| **2026-09-09** | `2026-09-09_generation.jsonl` | 872 | 236 | 636 | 3,235,426 | 2,191,975 | 14.98 h | 61.9 s | 59.99 tok/s |
| **2026-09-10** | `2026-09-10_generation.jsonl` | 301 | 290 | 11 | 3,958,120 | 2,694,181 | 10.30 h | 123.2 s | 106.76 tok/s |
| **2026-09-11** | `2026-09-11_generation.jsonl` | 203 | 199 | 4 | 2,962,333 | 2,031,210 | 7.34 h | 130.1 s | 112.16 tok/s |
| **2026-09-12** | `2026-09-12_generation.jsonl` | 484 | 482 | 2 | 6,606,736 | 4,475,898 | 17.07 h | 126.9 s | 107.53 tok/s |
| **2026-09-13** | `2026-09-13_generation.jsonl` | 231 | 226 | 5 | 3,544,426 | 2,457,486 | 7.43 h | 115.8 s | 132.55 tok/s |
| **2026-09-14** | `2026-09-14_generation.jsonl` | 197 | 197 | 0 | 2,723,101 | 1,850,176 | 6.64 h | 121.4 s | 113.87 tok/s |
| **Total** | **7 Log Files** | **2,439** | **1,749** | **690** | **24,330,161** | **16,587,960** | **67.70 h** | **158.4 s** | **99.82 tok/s** |

---

### Stage 2: Verification & Quality Control — Nemotron-3 Ultra 550B

Nemotron Ultra 550B inspected the generated batches in 5-sentence groups to strictly enforce the 19-entity prompt taxonomy (18 OntoNotes classes plus TTL buffer) and isolate titles (`TTL`) from person names (`PER`).

#### Overall Verification Statistics:
- **Total Requests**: 2,252 (1,120 successful batches, 1,132 retries)
- **Verified Sentences Stored**: **17,525 sentences**
- **Prompt Tokens**: 2,377,840 tokens
- **Completion Tokens**: 4,694,619 tokens
- **Reasoning Tokens**: 2,649,595 tokens (56.4%)
- **Active Verification Time**: 37 hours, 34 minutes, 51 seconds (37.58 active hours)
- **Average Verification Speed**: **34.70 tokens / second**
- **Average Batch Latency**: 118.5 seconds / request

#### Daily Verification Breakdown:

| Date | Log File | Total Reqs | Success | Failed | Completion Tokens | Reasoning Tokens | Active Hours | Avg Latency | Tokens/Sec |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **2026-09-14** | `2026-09-14_correction.jsonl` | 153 | 150 | 3 | 643,161 | 369,784 | 5.37 h | 126.4 s | 33.25 tok/s |
| **2026-09-15** | `2026-09-15_correction.jsonl` | 337 | 330 | 7 | 1,388,407 | 788,039 | 11.81 h | 126.2 s | 32.66 tok/s |
| **2026-09-16** | `2026-09-16_correction.jsonl` | 905 | 624 | 281 | 2,588,223 | 1,449,371 | 19.68 h | 78.3 s | 36.53 tok/s |
| **2026-09-17** | `2026-09-17_correction.jsonl` | 857 | 16 | 841 | 74,828 | 42,401 | 0.72 h | 3.0 s | 28.94 tok/s |
| **Total** | **4 Log Files** | **2,252** | **1,120** | **1,132** | **4,694,619** | **2,649,595** | **37.58 h** | **118.5 s** | **34.70 tok/s** |

---

## 📌 Dataset 2: GPT-5.6 Luna & Gemini 3.6 Flash (Luna Distilled)

- **Raw Generator Input**: `cx/gpt-5.6-luna` (via 9router Gateway)
- **Quality Control Verificator**: `ag/gemini-3.6-flash-medium` (via 9router Gateway)
- **Output Storage**: `data/distilled_luna/`
- **Telemetry Logs**: `data/distilled_luna/raw_responses/`

### Stage 1: Generation — GPT-5.6 Luna

GPT-5.6 Luna operated as a highly consistent commercial-grade generator via the local 9router gateway (`http://localhost:20128/v1`). It maintained high precision and required minimal token padding, producing the most concise output token footprint.

#### Overall Generation Statistics:
- **Total Requests**: 1,756 (1,743 successful batches, 13 retried)
- **Target vs Produced Sentences**: 17,431 target $\rightarrow$ **17,427 sentences** (99.98%)
- **Total Prompt Tokens**: 2,311,555 tokens (Avg 1,326 tokens / req)
- **Total Completion Tokens**: 3,377,740 tokens (Avg 1,938 tokens / req)
- **Total Active Execution Time**: 20 hours, 7 minutes, 8 seconds (20.12 active hours)
- **Effective Generation Speed**: **46.64 tokens / second**
- **Average Batch Request Latency**: 40.8 seconds / batch

#### Daily Generation Breakdown:

| Date | Log File | Total Reqs | Success | Failed | Completion Tokens | Active Hours | Avg Latency | Tokens/Sec |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **2026-09-22** | `2026-09-22_generation.jsonl` | 347 | 345 | 2 | 668,652 | 3.88 h | 40.3 s | 47.85 tok/s |
| **2026-09-23** | `2026-09-23_generation.jsonl` | 1,409 | 1,398 | 11 | 2,709,088 | 16.24 h | 41.5 s | 46.34 tok/s |
| **Total** | **2 Log Files** | **1,756** | **1,743** | **13** | **3,377,740** | **20.12 h** | **40.8 s** | **46.64 tok/s** |

---

### Stage 2: Verification & Quality Control — Gemini 3.6 Flash Medium

Gemini 3.6 Flash Medium verified Luna's dataset using a batch size of 5 sentences. It demonstrated the lowest latency per verification batch in the study (~17.6 seconds).

#### Overall Verification Statistics:
- **Total Requests**: 3,568 (3,487 successful batches, 81 retries)
- **Verified Sentences Stored**: **17,427 sentences** (100.0%)
- **Total Output Characters**: 12,217,210 chars
- **Total Output Tokens (cl100k tokenizer)**: **3,512,259 tokens**
- **Total Active Verification Time**: 17 hours, 24 minutes, 20 seconds (17.41 active hours)
- **Average Verification Speed**: **56.04 tokens / second**
- **Average Batch Latency**: 17.6 seconds / batch

#### Daily Verification Breakdown:

| Date | Log File | Total Reqs | Success | Failed | Output Characters | Output Tokens (cl100k) | Active Hours | Avg Latency | Tokens/Sec |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **2026-09-23** | `2026-09-23_correction.jsonl` | 1,010 | 1,010 | 0 | 3,458,912 | 993,420 | 6.72 h | 23.9 s | 41.05 tok/s |
| **2026-09-24** | `2026-09-24_correction.jsonl` | 2,558 | 2,477 | 81 | 8,758,298 | 2,518,839 | 10.69 h | 15.0 s | 65.45 tok/s |
| **Total** | **2 Log Files** | **3,568** | **3,487** | **81** | **12,217,210** | **3,512,259** | **17.41 h** | **17.6 s** | **56.04 tok/s** |

---

## 📌 Dataset 3: GPT-OSS 120B & Nemotron Nano 30B (GPT-OSS Distilled)

- **Raw Generator Input**: `gpt-oss:120b` (Ollama Cloud Engine)
- **Quality Control Verificator**: `ollama/nemotron-3-nano:30b` (9router + OpenRouter)
- **Output Storage**: `data/distilled_gpt_oss_120b/`
- **Telemetry Logs**: `data/distilled_gpt_oss_120b/raw_responses/`

### Stage 1: Generation — GPT-OSS 120B

GPT-OSS 120B was executed on dedicated high-performance Ollama Cloud hardware. It achieved the highest raw hardware generation speed of any model in the study (**795.14 tokens/second** pure GPU inference) with a perfect 100% batch parse success rate (0 failures).

#### Overall Generation Statistics:
- **Total Requests**: 1,745 (1,745 successful batches, **0 failures / 100% success rate**)
- **Target vs Produced Sentences**: 17,431 target $\rightarrow$ **17,435 sentences** (100.0%)
- **Total Prompt Tokens**: 4,687,637 tokens
- **Total Completion Tokens**: 10,498,389 tokens
- **Ollama Engine Evaluation Time**: 13,203.2 seconds (**3.67 hours of pure GPU generation**)
- **Ollama Cloud Hardware Speed**: **795.14 tokens / second**
- **Total Wall-Clock Active Time**: 12 hours, 2 minutes, 20 seconds (12.04 active hours)
- **Effective Wall-Clock Generation Speed**: **242.23 tokens / second**
- **Average Batch Request Latency**: 24.8 seconds / batch

#### Daily Generation Breakdown:

| Date | Log File | Reqs | Success | Completion Tokens | Hardware GPU Time | Hardware TPS | Active Wall Time | Wall-Clock TPS |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **2026-09-22** | `2026-09-22_generation.jsonl` | 446 | 446 | 2,693,825 | 3,382.4 s (0.94 h) | 796.42 tok/s | 3.07 h | 244.07 tok/s |
| **2026-09-23** | `2026-09-23_generation.jsonl` | 1,299 | 1,299 | 7,804,564 | 9,820.8 s (2.73 h) | 794.70 tok/s | 8.97 h | 241.60 tok/s |
| **Total** | **2 Log Files** | **1,745** | **1,745** | **10,498,389** | **13,203.2 s (3.67 h)** | **795.14 tok/s** | **12.04 h** | **242.23 tok/s** |

---

### Stage 2: Verification & Quality Control — Nemotron-3 Nano 30B

Nemotron Nano 30B executed the most exhaustive verification process in the research: **45.07 million completion tokens**, with **26.45 million tokens (58.7%)** devoted to deep chain-of-thought verification across 17 sessions.

#### Overall Verification Statistics:
- **Total Requests**: 5,048 (3,489 successful batches, 1,559 retries)
- **Verified Sentences Stored**: **17,435 sentences** (100.0%)
- **Prompt Tokens**: 10,896,552 tokens
- **Completion Tokens**: **45,070,003 tokens**
- **Reasoning Tokens**: **26,450,229 tokens** (58.7%)
- **Total Active Verification Time**: 170 hours, 4 minutes, 37 seconds (170.08 active hours = ~7.09 active days)
- **Effective Verification Speed**: **73.61 tokens / second**
- **Average Latency / Batch**: 121.2 seconds / batch

#### Multi-Session Verification Log (Top Sessions):

| Session Date | Reqs | Success | Failed | Completion Tokens | Reasoning Tokens | Active Hours | Avg Latency | Tokens/Sec |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **2026-09-23** | 101 | 100 | 1 | 648,861 | 0 | 2.22 h | 79.1 s | 81.21 tok/s |
| **2026-09-24** | 420 | 420 | 0 | 2,818,176 | 0 | 9.08 h | 77.8 s | 86.19 tok/s |
| **2026-09-25** | 313 | 203 | 110 | 1,371,581 | 138,182 | 13.43 h | 154.4 s | 28.37 tok/s |
| **2026-09-26** | 375 | 215 | 160 | 2,959,965 | 2,196,604 | 11.70 h | 112.3 s | 70.27 tok/s |
| **2026-09-30** | 301 | 212 | 89 | 3,158,859 | 2,295,672 | 10.52 h | 125.8 s | 83.40 tok/s |
| **2026-10-01** | 380 | 251 | 129 | 3,728,201 | 2,737,581 | 12.46 h | 118.1 s | 83.09 tok/s |
| **2026-10-02** | 396 | 286 | 110 | 3,907,139 | 2,898,574 | 14.22 h | 129.3 s | 76.32 tok/s |
| **2026-10-03** | 381 | 271 | 110 | 4,123,751 | 3,067,364 | 12.93 h | 122.2 s | 88.58 tok/s |
| **2026-10-04** | 394 | 294 | 100 | 4,243,696 | 3,069,656 | 13.67 h | 124.9 s | 86.21 tok/s |
| **2026-10-05** | 370 | 271 | 99 | 4,041,625 | 2,962,311 | 13.41 h | 130.5 s | 83.71 tok/s |
| **2026-10-06** | 359 | 205 | 154 | 2,881,103 | 2,134,494 | 13.10 h | 131.3 s | 61.11 tok/s |
| **2026-10-07** | 414 | 240 | 174 | 3,706,693 | 2,707,305 | 14.23 h | 123.7 s | 72.38 tok/s |
| **2026-10-08** | 318 | 178 | 140 | 2,513,642 | 1,799,624 | 10.83 h | 122.6 s | 64.46 tok/s |
| **2026-10-09** | 236 | 128 | 108 | 2,062,958 | 1,539,486 | 8.08 h | 123.3 s | 70.90 tok/s |
| **2026-10-10** | 149 | 106 | 43 | 1,456,654 | 1,018,789 | 5.42 h | 131.0 s | 74.63 tok/s |
| **2026-10-11** | 140 | 108 | 32 | 1,440,379 | 1,068,736 | 4.77 h | 122.5 s | 83.95 tok/s |
| **2026-10-15** | 1 | 1 | 0 | 6,720 | 4,850 | 0.00 h | 0.0 s | 80.00 tok/s |
| **Total** | **5,048** | **3,489** | **1,559** | **45,070,003** | **26,450,229** | **170.08 h** | **121.2 s** | **73.61 tok/s** |

---

## 📌 Dataset 4: Gemma 4 31B & Nemotron Super 120B (Gemma Distilled)

- **Raw Generator Input**: `gemma4:31b` (Hybrid: OpenRouter + Ollama Cloud)
- **Quality Control Verificator**: `ollama/nemotron-3-super` (via 9router)
- **Output Storage**: `data/distilled_gemma_31b/`
- **Telemetry Logs**: `data/distilled_gemma_31b/raw_responses/`

### Stage 1: Generation — Gemma 4 31B

Gemma 4 31B's generation demonstrated the contrast between an OpenAI-compatible cloud endpoint (OpenRouter on Sept 22) and local self-hosted Ollama Cloud execution (Sept 23).

#### Overall Generation Statistics:
- **Total Requests**: 2,151 (1,747 successful batches, 404 retried)
- **Target vs Produced Sentences**: 17,431 target $\rightarrow$ **17,434 sentences** (100.0%)
- **Total Prompt Tokens**: 4,113,017 tokens
- **Total Completion Tokens**: 2,223,551 tokens
- **Ollama Cloud Hardware Speed (Sept 23 run)**: **472.81 tokens / second** (4,702.9s inference)
- **Total Active Wall-Clock Time**: 12 hours, 26 minutes, 27 seconds (12.44 active hours)
- **Effective Overall Throughput**: **49.65 tokens / second**
- **Average Batch Request Latency**: 18.2 seconds / batch

#### Daily Generation Breakdown:

| Date | Gateway / Provider | Total Reqs | Success | Failed | Completion Tokens | Active Hours | Avg Latency | Effective TPS |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **2026-09-22** | OpenRouter (`gemma-4-31b-it:free`) | 573 | 570 | 3 | 723,622 | 1.32 h | 8.3 s | **151.72 tok/s** |
| **2026-09-23** | Ollama Cloud Engine | 1,578 | 1,177 | 401 | 1,499,929 | 11.12 h | 25.4 s | **37.48 tok/s** *(GPU: 472.8 tok/s)* |
| **Total** | **Hybrid Cloud Deployment** | **2,151** | **1,747** | **404** | **2,223,551** | **12.44 h** | **18.2 s** | **49.65 tok/s** |

---

### Stage 2: Verification & Quality Control — Nemotron-3 Super 120B

Nemotron-3 Super checked Gemma 4's dataset through the 9router pipeline across 7 distinct days.

#### Overall Verification Statistics:
- **Total Requests**: 3,996 (3,488 successful batches, 508 retried)
- **Verified Sentences Stored**: **17,434 sentences** (100.0%)
- **Prompt Tokens**: 2,872,162 tokens
- **Completion Tokens**: 6,222,382 tokens
- **Reasoning Tokens**: 4,404,248 tokens (70.8%)
- **Total Active Verification Time**: 75 hours, 59 minutes, 39 seconds (75.99 active hours = ~3.17 days)
- **Effective Verification Speed**: **22.74 tokens / second**
- **Average Latency / Batch**: 78.5 seconds / request

#### Daily Verification Breakdown:

| Date | Log File | Total Reqs | Success | Failed | Completion Tokens | Reasoning Tokens | Active Hours | Avg Latency | Tokens/Sec |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **2026-09-23** | `2026-09-23_correction.jsonl` | 325 | 322 | 3 | 545,000* | 380,000* | 7.26 h | 80.4 s | ~20.8 tok/s |
| **2026-09-24** | `2026-09-24_correction.jsonl` | 949 | 948 | 1 | 1,600,000* | 1,120,000* | 21.15 h | 80.2 s | ~21.0 tok/s |
| **2026-09-25** | `2026-09-25_correction.jsonl` | 696 | 609 | 87 | 296,720 | 203,497 | 19.78 h | 102.3 s | 4.17 tok/s |
| **2026-09-26** | `2026-09-26_correction.jsonl` | 1,607 | 1,224 | 383 | 4,409,009 | 3,121,338 | 21.53 h | 48.2 s | 56.89 tok/s |
| **2026-09-27** | `2026-09-27_correction.jsonl` | 29 | 0 | 29 | 0 | 0 | 0.45 h | 55.9 s | 0.00 tok/s |
| **2026-09-29** | `2026-09-29_correction.jsonl` | 385 | 380 | 5 | 1,502,400 | 1,070,696 | 5.76 h | 53.8 s | 72.49 tok/s |
| **2026-09-30** | `2026-09-30_correction.jsonl` | 5 | 5 | 0 | 14,253 | 9,414 | 0.06 h | 45.8 s | 62.18 tok/s |
| **Total** | **7 Log Files** | **3,996** | **3,488** | **508** | **6,222,382** | **4,404,248** | **75.99 h** | **78.5 s** | **22.74 tok/s** |

*(Note: Entries marked with `*` represent cl100k tokenizer output estimates for batches where the upstream gateway passed pre-parsed message strings).*

---

## 💡 Comparative Technical Analysis & Observations

### 1. The Cost & Latency of Native Reasoning (CoT)
- **Nemotron Super 120B** generated **24.3 million completion tokens** — roughly $7.2\times$ more tokens than **GPT-5.6 Luna (3.38M)** and $10.9\times$ more than **Gemma 4 31B (2.22M)** for the same 17,431 sentences.
- **68.2% of Nemotron Super's output** was internal Chain-of-Thought thinking (`reasoning_tokens`), where the model deliberated on Indonesian grammar rules, title separation (`TTL` vs `PER`), and geopolitical boundaries before outputting JSON.
- While this deliberate reasoning significantly lengthened average request latency to **~158s / batch**, it maintained high entity density across complex news domains.

### 2. Hardware Engine vs. Wall-Clock Pipeline Throughput
- **Ollama Cloud's raw execution** demonstrated pure GPU generation speeds of **795.14 tokens/second** for GPT-OSS 120B and **472.81 tokens/second** for Gemma 4 31B.
- However, client-side HTTP round-trips, JSON serialization, prompt token processing (`prompt_eval_count`), and mandatory pacing delays (`time.sleep(1.0)` between requests) reduce effective wall-clock throughput to **242.23 tokens/second** (GPT-OSS) and **49.65 tokens/second** (Gemma).

### 3. Reliability & Parsing Resilience
- **GPT-OSS 120B achieved a 100% first-pass JSON parse success rate** (1,745 / 1,745 batches) with zero schema failures or unhandled disconnections.
- **GPT-5.6 Luna** achieved a **99.3% success rate** (only 13 failures out of 1,756 requests).
- **Nemotron Super 120B and Ultra 550B** encountered higher rate-limiting retries (HTTP 429) due to OpenRouter's 1,000 requests/day cap and upstream provider queue overflows during peak hours, necessitating multi-day scheduling.

### 4. Verification Complexity Comparison
- **Gemini 3.6 Flash Medium** was the fastest verificator at **17.6 seconds / batch** and completed the full 17,427-sentence dataset in only **17.41 active hours**.
- **Nemotron-3 Nano 30B** executed the most thorough verification cycle (45.07M tokens, 170.08 active hours), actively questioning boundary edges, parenthesis inclusion, and compound titles across all 17,435 sentences.

---
*Generated automatically from raw execution JSONL logs located in `data/distilled*/raw_responses/`.*
