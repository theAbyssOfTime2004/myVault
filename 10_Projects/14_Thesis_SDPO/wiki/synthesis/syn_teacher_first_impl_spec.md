---
type: synthesis
created: 2026-06-14
updated: 2026-06-14
tags: [implementation, spec, teacher-first, sdpo, cursor-handoff]
sources: [src_hubotter2026_self_distillation, src_lasgroup_sdpo_repo]
---

# Implementation Spec — Teacher-First Judge-Filtered SDPO (P0: code)

Spec để hand cho Cursor implement, rồi review. Method design ở [[con_teacher_first_judge]].

## 0. Mục tiêu & quyết định kiến trúc

Xây vòng **teacher-first** cho test-time SDPO. KHÔNG sửa `07_discovery_curve.py` (giữ làm student-first baseline). Tạo file mới **`09_teacher_first.py`**.

**Kiến trúc: custom training loop** (KHÔNG dùng `SDPOTrainer` — nó hard-code student-first rollout bên trong, trajectory để distill phải là teacher-generated-filtered nên không nhét vào sạch được).

**Teacher & student dùng CHUNG weight** (cùng 1 model = self-distillation):
- `student` = `model(prompt_only)`
- `teacher` = `model(prompt + feedback + few-shot exemplars)`
- Update weight chỉ qua student forward; teacher forward `.detach()` (stopgrad).

## 1. Tái dùng từ `07_discovery_curve.py`

Import (không copy-paste; import từ module 07 hoặc tách helper chung):
`_prepare_tokenizer`, `_build_messages`, `build_privileged_context`, `build_dynamic_feedback`, `evaluate_model`, `safe_evaluate_model`, `_build_lora_config`, `_extract_text`, `load_lcbv6_split`, `evaluate_solution`.

## 2. Component mới

### 2a. Teacher rollout
```python
@torch.no_grad()
def teacher_generate(model, tokenizer, question_content, feedback_text,
                     good_pool, bad_pool, option, N, temperature, max_new_tokens):
    """
    Teacher prompt = problem + feedback + few-shot exemplars, sample N.
    option="good_only" -> chỉ good_pool ; option="good_bad" -> good_pool + bad_pool kèm label.
    Returns list[str] (N decoded completions).
    """
```
- Few-shot block chèn TRƯỚC directive "Respond with ONLY...".
- Cap exemplar (`max_fewshot=3`) tránh vỡ context. Log token count.

### 2b. Filter / judge
```python
def filter_trajectories(trajectories, row, reference_text, sim_threshold):
    """
    Mỗi traj: score = evaluate_solution(traj,row)["score"]; sim = similarity(traj, reference_text).
    good := score>=1.0 AND sim<sim_threshold   (đúng + độc lập)
    bad  := sim>=sim_threshold                  (copy reference)
    Returns (good_list, bad_list, stats_dict).
    """
```
- `similarity()`: bản đầu `difflib.SequenceMatcher(None,a,b).ratio()` trên code normalize (strip comment/whitespace). Không cần embedding/LLM. Là knob.
- Log mỗi step: `n_good, n_bad, n_total`, mean sim.

### 2c. KL distillation step (lõi)
```python
def teacher_first_step(model, tokenizer, question_content, feedback_text,
                       y_good_list, optimizer, kl_topk, kl_alpha):
    """
    Mỗi y_good:
      student_ids = tokenize(prompt_student + y_good)
      teacher_ids = tokenize(prompt_teacher + y_good)   # teacher_prompt = prompt+feedback(+fewshot)
      student_logits = model(student_ids)               # grad ON
      with no_grad: teacher_logits = model(teacher_ids)  # stopgrad
      # align trên token positions của y_good (prefix length khác nhau 2 bên)
      loss += KL_topk(student_logits@ypos, teacher_logits@ypos, topk=kl_topk, alpha=kl_alpha)
    loss.backward(); optimizer.step(); optimizer.zero_grad()
    """
```
- **kl_alpha=1.0 (reverse KL), kl_topk=20** — match LCBv6 config lasgroup ([[src_lasgroup_sdpo_repo]]).
- ⚠️ **Căn chỉnh token y_good**: prompt_student/prompt_teacher dài khác nhau → phải lấy logits đúng vị trí token y_good ở MỖI bên. Chỗ dễ sai nhất — viết cẩn thận + assert độ dài khớp.
- Trước khi tự viết KL: **kiểm tra `trl/experimental/sdpo/loss_utils.py`** có top-k KL tái dùng được không. Có thì dùng lại; không tiện thì viết thẳng (ổn vì completion ngắn ~400–500 token).

### 2d. Vòng chính
```
load model + LoRA + optimizer (AdamW lr=1e-5)
PRE-eval (student-only)
good_pool=[]; bad_pool=[]
for step in range(max_steps):
    feedback = build_dynamic_feedback(student greedy attempt, row)   # tái dùng 07
    traj = teacher_generate(..., good_pool, bad_pool, option, N, temp)
    good, bad, stats = filter_trajectories(traj, row, reference_text, sim_threshold)
    update good_pool/bad_pool (cap; ưu tiên score cao / mới)
    if good: teacher_first_step(..., good, optimizer, kl_topk, kl_alpha)
    else:    log "no good this step"  (cold-start / collapse signal)
    log step stats -> W&B
POST-eval (student-only)
print effectiveness + discovery curve; write summary.json
```

## 3. CLI args (phong cách 07)
`--problem_index, --model_name (default Qwen/Qwen3-4B), --max_steps, --teacher_n (10), --teacher_temperature (1.0), --sim_threshold (0.8), --fewshot_option {good_only,good_bad} (good_only), --max_fewshot (3), --kl_topk (20), --kl_alpha (1.0), --reprompt_template (presets 07), --eval_samples, --seed, --max_new_tokens, --wandb_project, --no_wandb`.

## 4. ⚠️ QUYẾT ĐỊNH PHẢI HỎI LẠI (Cursor surface, đừng tự đoán)

1. **`reference_text` lấy từ đâu cho CODE?** Load-bearing — không có reference thì filter "copy" vô nghĩa.
   - Math: rõ = `ground_truth`.
   - **Code (LCBv6): CẦN KIỂM TRA** row có field solution mẫu không (`row.keys()`). Có → dùng. Không → quyết: (a) best-scoring trajectory trong batch làm proxy, hay (b) bỏ similarity cho code, chỉ lọc correctness. → **Cursor in `row.keys()` + 1 sample row, hỏi lại.**
2. **`loss_utils` TRL có KL tái dùng không** → đọc file, báo API, rồi mới quyết.

## 5. Phasing
- **P0:** chỉ CODE, 1 bài frontier (idx 23), `good_only`, similarity=difflib. Mục tiêu: vòng chạy + student IMPROVED + n_good hợp lý.
- **P1:** thêm `good_bad` (ablation leak).
- **P2:** math (loader MATH + `feedback.math`, reference=ground_truth, reward binary).

## 6. Logging bắt buộc
- Mỗi step: `n_good/n_bad/n_total`, mean sim, loss, `len(good_pool)`.
- Step 1: in 1 teacher prompt đầy đủ + token count vs `max_prompt_length`.
- In (student_prefix_len, teacher_prefix_len) + assert vị trí token y_good khớp.
- PRE/POST student-only eval (giống 07).

## 7. Review checklist (Claude sẽ check)
- Căn chỉnh token y_good ở 2c (off-by-one → KL sai âm thầm).
- stopgrad teacher (teacher forward `no_grad`/detach).
- Few-shot vào prompt teacher, KHÔNG lọt student/eval.
- reference_text đúng nguồn đã chốt (mục 4.1).
- Cold-start (good_pool rỗng step 1 → teacher feedback-only, không crash).
- KL variant (reverse, top-k) đúng config.

## Links
- [[con_teacher_first_judge]] — method design
- [[src_lasgroup_sdpo_repo]] — verifier code/math, KL config (alpha=1, topk=20)
- [[con_reprompt_template]] — template presets tái dùng
