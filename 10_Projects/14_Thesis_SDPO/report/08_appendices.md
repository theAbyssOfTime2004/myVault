---
type: report
created: 2026-06-26
updated: 2026-06-26
tags: [report, appendices]
sources: [syn_core_result, syn_math_pilot, con_teacher_first_judge, syn_teacher_first_impl_spec]
---

# Appendices

Appendices A, B, C, E, and F are complete, with B and C reproduced verbatim from the codebase (`07_discovery_curve.py`, `09_teacher_first.py`) and the rest from the experiment records. Appendix D is complete for the math pilot (verbatim from the W&B logs); its code exemplars and the full idx0–90 / per-seed tables (Appendix E/F notes) await further log export.

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

## Appendix B — Reprompt templates (verbatim)

Each preset overrides the SDPO template *slots* only; the model, the feedback content (the privileged context), and the hyperparameters are held fixed for a clean ablation. The TRL 1.6.0 slots are `reprompt_template → {prompt}{solution}{feedback}`, `feedback_template → {feedback_raw}` (this `{feedback_raw}` is the privileged context), and `solution_template → {successful_previous_attempt}`. T2 is the TRL/paper default verbatim.

**Honest scope note.** The codebase (`07_discovery_curve.py`, `REPROMPT_TEMPLATES`) implements **four** presets, reproduced below: T1, T2, T5, T6. The taxonomy of §3.4 also names T3 (verbose), T4 (structured JSON), and T7 (cumulative history); these three are conceptual points in the design space and were **not** implemented. Of the four implemented, the experiments probe T1/T2/T5 (§4.3); T6 is implemented but unprobed.

```python
# T1 - Minimal: teacher is told the attempt was wrong but NOT why
#   (feedback_template drops the {feedback_raw} test/error detail).
"T1_minimal": {
    "reprompt_template": "{prompt}{solution}{feedback}\n\nProvide a corrected solution.\n",
    "feedback_template": "\nYour previous attempt was incorrect.\n\n",
},
# T2 - Standard / anchor: exact TRL + paper defaults (rich feedback included).
"T2_standard": {
    "reprompt_template": "{prompt}{solution}{feedback}\n\nCorrectly solve the original question.\n",
    "feedback_template": "\nThe following is feedback from your unsuccessful earlier attempt:\n\n{feedback_raw}\n\n",
},
# T5 - Reasoning-inducing: SAME rich feedback as T2, trailing instruction asks
#   for root-cause analysis first.
"T5_reasoning": {
    "reprompt_template": "{prompt}{solution}{feedback}\n\nFirst, identify the root cause of the failure, then provide a corrected solution.\n",
    "feedback_template": "\nThe following is feedback from your unsuccessful earlier attempt:\n\n{feedback_raw}\n\n",
},
# T6 - First-person: SAME rich feedback, reframed as the model's own reflection.
"T6_first_person": {
    "reprompt_template": "{prompt}{solution}{feedback}\n\nI attempted this problem and my solution was incorrect. Let me reconsider and write a correct solution.\n",
    "feedback_template": "\nHere is the feedback from my unsuccessful earlier attempt:\n\n{feedback_raw}\n\n",
},
```

---

## Appendix C — Teacher and judge prompts (verbatim)

### C.1 Teacher prompt and few-shot block

The teacher prompt is `question + few-shot block + feedback + trailing instruction`, where the feedback and trailing instruction come from the selected reprompt preset (Appendix B). A worked instance of the assembled prompt (with the leaked math reference) is shown in Appendix D.1. The few-shot block (`09_teacher_first.py`, `_build_fewshot_block`) is assembled as follows; exemplars are stripped of their thinking traces and capped at 1500 characters:

```
Here are correct, independent example solutions:

Correct example 1:
```python
<good trajectory, post-think solution only>
```

[good_bad option only:]
Here are INCORRECT or copied attempts to avoid:

Bad example 1 (do not imitate):
```python
<bad / copied trajectory>
```
```

Under `good_only` (Option 2) only the "Correct example" exemplars appear; under `good_bad` (Option 1) the "Bad example" block is appended, which is what re-introduces reference-like content (§3.3.4).

### C.2 LLM judge prompt — code (groq `llama-3.3-70b`)

```
You are judging a CANDIDATE solution to a competitive-programming problem.

You are given the PROBLEM, a REFERENCE solution, and a CANDIDATE solution. The
candidate is ALREADY known to be correct (it passes the test cases), so do NOT
re-check correctness. Decide only two things:

  1. is_copy: Is the candidate essentially a copy of the reference solution --
     i.e. the same algorithm, structure and control/data flow, ignoring trivial
     renaming, comments, or formatting? true if it is essentially a copy, false
     if it is an independent solution (different approach/structure).
  2. reasoning_quality: How clear and self-contained is the candidate's logic,
     on an integer scale 1-5 (1 = obfuscated/unclear, 5 = clean, clearly reasoned).

PROBLEM: {problem}
REFERENCE SOLUTION: {reference}
CANDIDATE SOLUTION: {candidate}

Return ONLY JSON with keys: is_copy (boolean) and reasoning_quality (integer 1-5).
```

### C.3 LLM judge prompt — math (`glm-4.5-flash`)

```
You are judging a CANDIDATE solution to a math problem.

You are given the PROBLEM, the KNOWN CORRECT ANSWER, and the CANDIDATE's full
output (which may include a <think>...</think> reasoning block followed by a final
\boxed{answer}). The candidate was ALREADY shown the correct answer as feedback,
so it is trivial for it to simply restate it. Decide only two things:

  1. is_copy: Did the candidate just COPY/state the given correct answer WITHOUT
     genuine step-by-step derivation? true if it merely asserted the answer (no
     real working, or working that does not actually lead to the answer). false if
     the candidate DERIVED the answer through genuine step-by-step reasoning.
  2. reasoning_quality: How sound and self-contained is the candidate's
     derivation, on an integer scale 1-5 (1 = no/incoherent reasoning, 5 = clear,
     correct, complete derivation).

PROBLEM: {problem}
KNOWN CORRECT ANSWER: {reference}
CANDIDATE OUTPUT (including any <think> reasoning): {candidate}

Return ONLY JSON with keys: is_copy (boolean) and reasoning_quality (integer 1-5).
```

The judge returns structured JSON (`is_copy`: boolean, `reasoning_quality`: integer). Note the code judge is explicitly told the candidate is already correct and to judge only copying and clarity, which is why with thinking OFF it functions as a semantic copy-detector rather than a reasoning scorer (§3.3.3).

---

## Appendix D — Example trajectories (math pilot)

Excerpts are verbatim from the W&B logs; long completions are trimmed with `[...]`. What the logs record per run: the teacher prompt, the per-step judge verdicts, and the student PRE/POST eval completions. The teacher-generated trajectories that the judge scored are *not* stored as text (only their verdicts), so copying is evidenced here by the verdicts, not by the copied text. Code exemplars (e.g., idx12 learning to iterate after a `math.factorial` runtime error) are not yet exported and remain to be added.

### D.1 Teacher prompt with the leaked reference (idx9, run `fi5m0as1`)

```
<|turn>user
Let △ABC have side lengths AB = 13, BC = 14, and CA = 15. Triangle △A'B'C'
is obtained by rotating △ABC about its circumcenter so that AC is
perpendicular BC, with A' and B not on the same side of line B'C'. Find the
integer closest to the area of hexagon AA'CC'BB'.

The following is feedback from your unsuccessful earlier attempt:

Reference: the correct final answer is 156.

Correctly solve the original question.
[...]
```

The reference is the bare answer 156; there is no worked solution to distill, only the number to copy (§3.5).

### D.2 Judge verdict sequences

idx9 (run `fi5m0as1`), correct answer 156; batch reward 1.0 every step, so all 12 trajectories are nominally correct:

| step | verdicts (is_copy / reasoning_quality) | n_good / n_bad |
|---|---|---|
| 1 | (T,1) (T,2) (F,2) (F,4) | 1 / 3 |
| 2 | (T,2) (T,2) (T,2) (T,3) | 1 / 3 |
| 3 | (T,2) (T,2) (T,1) (T,3) | 1 / 3 |

The only genuine derivation (F,4) is at step 1; steps 2–3 are all copies, so the kept "good" comes from the fallback. idx8 (run `463y4fjr`), correct answer 29:

| step | verdicts | n_good / n_bad | batch reward |
|---|---|---|---|
| 1 | (T,1) (T,3) | 1 / 1 | 0.50 |
| 2 | (T,3) (T,2) (T,1) | 1 / 2 | 0.75 |
| 3 | (T,4) (T,3) (T,2) (F,2) | 1 / 3 | 1.00 |

Every idx8 verdict is `is_copy=true` (the lone `F` has reasoning_quality 2 < 3), so every kept "good" is a fallback-retained copy.

### D.3 Form changes, substance does not (idx9 student eval, PRE vs POST)

**PRE** (23,920 chars, boxed **148**). The model recognizes the configuration is contradictory, then satisfices toward a clean angle:

> "But $AC \perp BC$ is impossible in $\triangle ABC$ [...] **Crucial Insight Check:** [...] This seems overly complex for a calculation intended to yield a clean integer answer nearby. Let's pivot and assume $\theta$ is a 'nice' angle, like $90^\circ$ or $180^\circ$ [...]"

It computes 315.5 under one reading, reinterprets the hexagon as a union (147.5), and boxes 148.

**POST** (11,951 chars, about half the length, boxed **168**). After TTT the setup is better — it now derives $\cos C = 3/5$ and $\theta = 90^\circ \pm C$ — but it gives up earlier and shortcuts to twice the triangle area:

> "[...] unless the overlap is significant [...] the area is often closely approximated by the sum of the individual areas [...] the most straightforward interpretation leading to a clean integer answer is that the intended area calculation ignores the slight overlap [...] $\text{Area}(H) \approx 84 + 84 = 168$."

Both are wrong (correct 156); the model never reaches or memorizes the leaked answer. TTT changed the reasoning style (more confident, more willing to shortcut), not the capability.

### D.4 The opposite stylistic drift (idx8 student eval, PRE vs POST)

idx8 drifts the other way. **PRE** (boxed **40201**) treats the rolls as independent and computes $p = 2^{13}\cdot 3 / 5^6$, giving $m+n = 24576 + 15625 = 40201$. **POST** (boxed **17**) is *more* rigorous — it does casework on $R_2 = R_4$ versus $R_2 \neq R_4$, counts $N_B = 11700$ and $N_{A\cap B} = 3600$, and simplifies $p = 4/13$ to $m+n = 17$. POST is longer and more careful, yet still wrong (correct 29). Across the two problems, then, TTT moves the reasoning style in opposite directions (idx9 lazier, idx8 more rigorous) while leaving correctness unchanged.

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
