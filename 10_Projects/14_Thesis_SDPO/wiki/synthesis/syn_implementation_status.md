---
type: synthesis
created: 2026-05-29
updated: 2026-05-29
tags: [implementation, milestone, roadmap, ttt-sdpo, colab]
sources: [src_trl_sdpo_sdft_docs, syn_thesis_proposal, src_lasgroup_sdpo_repo]
---

# Implementation Status & Roadmap — Post Cloud Kickoff (2026-05-29)

Status snapshot + forward plan sau lần đầu chạy TTT-SDPO weight-update thật trên cloud. Bổ sung cho [[syn_thesis_proposal]] (design spec) và `experiments/plans/ttt_sdpo_w2_implementation_plan.md` (W2 spec — một phần superseded, xem mục Divergence).

**Repo**: `theAbyssOfTime2004/thesis-ttt-sdpo` (private, fork-clean từ [[src_lasgroup_sdpo_repo]]). **W&B**: project `ttt-sdpo-thesis`. **Compute**: Colab Pro L4 24GB (~300 units/tháng). **Defense target**: ~25–26/7/2026.

## Milestone — proof-of-mechanism (2026-05-29)

Chứng minh được **lõi SDPO weight-update chạy thật** trên LCBv6 + Qwen2.5-1.5B + LoRA r=32: gen K=4 → evaluate (dense reward = pass ratio) → SDPO self-distillation loss → backprop → save adapter. bf16 stable, không NaN, peak VRAM 7.4/22 GB, ~32s/step.

Kickoff run (3 problem, 2 step mỗi bài):

| problem_id | difficulty | step1 rewards | variance | final_loss | học? |
|---|---|---|---|---|---|
| abc387_a | easy | [1, 1, 0, 1] | 0.234 | 0.0492 | có (lần đầu loss≠0) |
| abc387_b | easy | [0.35, 0, 0, 0] | 0.013 | 0.000 | không |
| abc387_f | hard | [0, 0, 0, 0] | 0.000 | 0.000 | không |

Solvable 2/3, useful SDPO signal (variance>0) 2/3. Qwen 0.5B trước đó all-zero mọi bài → **model size là gating factor**: 1.5B giải được LCBv6 easy.

## Quan trọng — proof-of-mechanism ≠ proof-of-effectiveness

Mới chứng minh **weights thay đổi** (gradient ≠ 0), CHƯA chứng minh **model tốt hơn sau TTT**. abc387_a step 2 còn regress về [0,0,0,0]. → pre/post eval (đo accuracy trước/sau TTT) là gap bắt buộc lấp trước khi viết Results — kéo lên cuối Phase 2.

## SDPO mechanism (traced 2026-05-29, trl.experimental.sdpo)

Chi tiết cơ chế, liên kết với [[con_sdpo_loss_mechanics]], [[con_reprompt_template]], [[con_self_teacher]]:

- **`reprompt_template`** là một config arg trong `SDPOConfig` — string với placeholder `{prompt}` / `{solution}` / `{feedback}`. Đổi string = đổi "approach" cho RQ1, **không cần sửa code**. Đây chính là biến trung tâm RQ1.
- Distillation kích hoạt cho 1 sample iff `has_solution OR use_feedback`:

| Path | Điều kiện | Vai trò |
|---|---|---|
| A `has_solution` | có rollout reward ≥ `success_reward_threshold` (default 1.0) | dùng rollout thành công làm solution demo |
| B `use_feedback` | `include_environment_feedback=True` AND `privileged_context` có feedback | teacher nhận hint kể cả khi không rollout nào perfect |

- Kickoff run chỉ Path A bật (feedback off, context rỗng) → chỉ abc387_a (reward đúng 1.0) học; abc387_b (0.35 < 1.0) loss=0.
- **Path B là chìa khóa bài khó**: đổ test feedback vào `privileged_context` → teacher giải tốt hơn → vẫn có signal distill dù không có lời giải hoàn hảo.
- Teacher = no-grad forward trên context dựng bởi `reprompt_template` + cùng completion; student = grad forward trên prompt gốc + cùng completion; distill student→teacher trên completion tokens.
- Knob khác: `feedback_template`, `environment_feedback_only_without_solution`, `dont_reprompt_on_self_success`.
- Quyết định: **giữ `success_reward_threshold=1.0`** — không hạ xuống 0.5 vì rollout reward 0.5 = code buggy, làm distill target xấu. Bài khó dùng Path B (feedback), không dùng cách hạ threshold.

## Divergence so với W2 plan cũ

W2 plan (`experiments/plans/ttt_sdpo_w2_implementation_plan.md`) giả định **hand-rolled `ttt_sdpo/` module**: tự port `compute_self_distillation_loss` từ `verl/trainer/ppo/core_algos.py:1085` + tự viết `EMATeacher`. Thực tế đã **dùng thẳng `trl.experimental.sdpo.SDPOTrainer`** (theo quyết định switch verl→TRL 2026-05-19 trong [[src_trl_sdpo_sdft_docs]]). TRL lo loss/EMA/teacher-context builder. → phần §3 (component spec), §9 (verbatim port) của W2 plan không còn áp dụng; phần kiến trúc cao (per-question fresh weights, template T1–T7, discovery curve) vẫn giữ.

## 4-Phase forward plan

### Phase 1 — Bật feedback path + template đầu tiên (session kế)
- `include_environment_feedback=True` (mở Path B)
- Viết `reprompt_template` (T2 standard) + `feedback_template`
- `build_feedback()` từ failed **public** test → `privileged_context` (public cho feedback, private cho reward, tránh leak)
- Acceptance: rerun 3 bài kickoff; abc387_b và abc387_f (trước loss=0) giờ loss>0 nhờ feedback → chứng minh tầng reprompt/feedback hoạt động.

### Phase 2 — Multi-turn feedback loop (1–2 session)
- Reuse pattern `baseline_multiturn/multiturn.py` (inference loop đã có)
- Wire SDPO weight-update giữa các turn; public test → feedback, private test → reward
- Termination: pass-all / hết turn budget
- Acceptance: 1 bài qua 3 turn, reward tăng dần ([[con_discovery_at_k]] curve sơ khởi)
- **Kéo pre/post eval vào cuối phase này** (lấp gap effectiveness)

### Phase 3 — So sánh template = research questions (2–3 session)
- T1 baseline (chỉ đề) / T2 standard (đề+feedback) / T3 epistemic (đề+feedback+[[con_epistemic_verbalization]], RQ2)
- Chạy mỗi template trên 10–20 bài, log W&B
- Discovery curve so [[src_hubotter2026_self_distillation]] §5 Fig 13
- (7 template đầy đủ T1–T7 theo [[syn_template_taxonomy_rationale]] khi scale)

### Phase 4 — Scale + final (2–3 session)
- LCBv6 subset 50–100 bài, nhiều seed
- Ablation: num_generations, lora_r, turn budget, α (forward/JSD/reverse KL); có thể Qwen 3B (L4 fit)
- Export biểu đồ cho thesis

## Infra pointers

- Script: `experiments/ttt_trl/05_colab_qwen15b_kickoff.py`
- Notebook + deps: `experiments/ttt_trl/colab/01_qwen15b_kickoff_L4.ipynb`, `requirements_colab.txt`
- Colab deps ngoài requirements.txt: `ray`, `tensordict`, `omegaconf`, `hydra-core`, `pylatexenc`, `torchao>=0.16` (Colab default 0.10 quá cũ, transformers reject)
- Local 1660Ti = smoke test only; mọi run thật trên Colab
