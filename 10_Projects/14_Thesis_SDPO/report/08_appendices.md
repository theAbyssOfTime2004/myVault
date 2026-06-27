---
type: report
created: 2026-06-26
updated: 2026-06-26
tags: [report, appendices]
sources: [syn_core_result, syn_math_pilot, con_teacher_first_judge, syn_teacher_first_impl_spec]
---

# Appendices

Appendices A, E, and F are filled from the experiment records. Appendices B, C, and D require verbatim source text (template strings, prompt text, full trajectories) and are marked as stubs to be filled from the codebase and logs, so that nothing here is reconstructed from memory.

---

## Appendix A — Hyperparameters

### A.1 Code (LiveCodeBench v6, core)

| Setting | Value |
|---|---|
| Model | Qwen3-4B, LoRA r=32, bf16, thinking OFF |
| Optimizer | AdamW, lr = 1e-5 |
| TTT steps $K$ | 15 |
| Teacher samples `teacher_n` (TF) | 10 |
| `num_generations` (SF baseline) | 4 |
| Teacher temperature | ~1.0 |
| Eval samples $N_{\text{eval}}$ | 16 (student-only, PRE and POST) |
| Seeds | 0, 1, 2, 3 (matched PRE per seed) |
| Template | T2 (anchor) for the main comparison; T1/T2/T5 for RQ1 |
| KL top-K | 20 |
| KL direction $\alpha$ | 1.0 (reverse KL) |
| Importance-sampling clip | 2.0 |
| Similarity threshold (difflib judge) | ~0.9 |
| Few-shot exemplars `max_fewshot` | 3 |
| Few-shot option | good_only (main); good_bad (leak ablation) |
| Judge | difflib (string-sim) or groq `llama-3.3-70b` (semantic) |
| `reference_mode` | best_in_batch |
| Hardware | Colab L4 (22 GB) / A100 |

### A.2 Math (AIME 2026, pilot)

| Setting | Value |
|---|---|
| Model | google/gemma-4-E4B-it, LoRA all-linear, thinking ON |
| TTT steps $K$ | 3 |
| Teacher samples `teacher_n` | 4 |
| Eval samples | 4 |
| `max_new_tokens` | 16384 (8192 truncated `\boxed`, producing spurious zeros) |
| Sampling | top_p 0.95, top_k 64 |
| `reference_mode` | ground_truth (leak regime) |
| Judge | `zai:glm-4.5-flash`, derive-vs-copy (`is_copy` + `reasoning_quality` 1–5) |
| Data | MathArena/aime_2026 (30 problems, integer answers) |
| Hardware | Modal A100-80GB |

Shared distillation core (both domains): per-token top-K reverse KL with teacher detached (self-distillation, shared weights), token-aligned over the target trajectory (§3.3.5).

---

## Appendix B — Reprompt templates T1–T7 (STUB)

> **To be filled from the codebase** (reprompt-template presets in script `07`). The taxonomy and the role of each template are given in §3.4; this appendix should reproduce the **verbatim template strings** for T1–T7. Required text: the exact slot layout for each of T1 (minimal), T2 (standard anchor), T3 (verbose), T4 (JSON), T5 (reasoning-inducing), T6 (first-person), T7 (cumulative history). Not reconstructed here to avoid paraphrase drift.

---

## Appendix C — Teacher and judge prompts (STUB)

> **To be filled from the codebase.** Required verbatim text: (1) the teacher rollout prompt including the few-shot exemplar block layout (good_only and good_bad variants); (2) the LLM-judge prompt that returns `is_copy` and `reasoning_quality` (the code/groq variant and the math/glm-4.5-flash variant). Described in §3.3.2–§3.3.4; exact strings pending.

---

## Appendix D — Example trajectories (STUB)

> **To be filled from W&B logs.** Required: one good, one bad/copy, and one borderline trajectory per domain, copied verbatim. Candidate runs noted in the records: code idx12 (base uses `math.factorial` in the wrong direction, then learns to iterate); math idx9 (W&B run `fi5m0as1`, boxed 148→168 against correct 156, "in problems of this nature, the intended answer is usually clean"); math idx8 (run `463y4fjr`, all verdicts `is_copy=true`). Full completions pending.

---

## Appendix E — Per-seed results

### E.1 idx39 (abc393_d, hard, base pass ≈ 0.1), eval-16, difflib judge

| seed | PRE | TF POST | SF POST |
|---|---|---|---|
| 0 | 0.000 | 0.438 | 0.188 |
| 1 | 0.000 | 0.062 | 0.000 |
| 2 | 0.062 | 0.125 | 0.125 |
| 3 | 0.188 | 0.062 | 0.062 |
| mean | | 0.172 | 0.094 |

### E.2 idx12 (abc389_b, model-hard, model pass ≈ 0.12), eval-16

| seed | PRE | TF POST | SF POST |
|---|---|---|---|
| 0 | 0.000 | 1.000 | 0.938 |
| 1 | 0.062 | 1.000 | 0.500 |
| 2 | 0.062 | 1.000 | 1.000 |
| 3 | 0.125 | 1.000 | 0.938 |
| mean | | 1.000 | 0.844 |

### E.3 Hard-frontier means and escape-zero instances

| problem | id | judge | SF mean | TF mean | win/tie/loss | escape-zero seeds |
|---|---|---|---|---|---|---|
| idx39 | abc393_d | difflib | 0.094 | 0.172 | 2/2/0 | s1 (SF 0→0, TF 0.062) |
| idx64 | abc397_e | LLM-groq | 0.047 | 0.422 | 4/0/0 | s1 (SF 0.062→0, TF 0.375), s2 (SF 0→0, TF 0.062) |
| idx77 | abc399_f | difflib | 0.203 | 0.344 | 3/1/0 | — |

> Full per-seed tables for idx64 and idx77 are in the W&B logs; only means and the escape-zero seeds are reproduced here.

### E.4 RQ1 template (SF arm, 2 seeds), POST pass@16

| Template | idx12 (easy) | idx39 (hard) |
|---|---|---|
| T1_minimal | 0.66 | 0.03 |
| T2_standard | 0.97 | 0.06 |
| T5_reasoning | 0.97 | 0.13 |

T5 on idx39 is stable across its two seeds (.125 / .125).

### E.5 Judge × few-shot ablation, mean POST pass (4 seeds)

| arm | idx39 | idx12 |
|---|---|---|
| SF baseline | 0.094 | 0.844 |
| TF · good_only · difflib | 0.172 | 1.000 |
| TF · good_only · LLM | 0.266 | 0.984 |
| TF · good_bad · LLM | 0.250 | 1.000 |

---

## Appendix F — Frontier scans

### F.1 Math (AIME 2026, Gemma-4-E4B thinking ON, n_samples = 2)

| Band | Problem indices |
|---|---|
| Frontier (0 < pass < 1) | 8, 11, 21, 25 |
| Too-hard (pass = 0) | 2, 3, 9, 10, 12, 13, 14, 16, 17, 22, 24, 26, 27, 28, 29 |
| Ceiling (pass = 1) | 0, 1, 4, 5, 6, 7, 15, 18, 19, 20, 23 |

The two pilot problems (idx9, idx8) are drawn from the too-hard band; idx8 was labeled frontier by the noisy 2-sample scan but is actually pass = 0 at 4 samples.

### F.2 Code (LiveCodeBench v6, Qwen3-4B)

Problems for the matched comparisons were selected by *model* pass-rate $\in (0,1)$ over a scan of idx0–90. The problems used are idx12 (abc389_b), idx39 (abc393_d), idx64 (abc397_e), and idx77 (abc399_f).

> **To be completed:** the full idx0–90 model-pass-rate scan table is in the logs and should be reproduced here for completeness.
