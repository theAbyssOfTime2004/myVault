---
type: source
created: 2026-04-23
updated: 2026-04-23
tags: [codebase, implementation, verl, reference]
sources: [src_lasgroup_sdpo_repo]
aliases: [lasgroup/SDPO, SDPO repo, official SDPO code]
---

# lasgroup/SDPO — Official codebase

Repo: https://github.com/lasgroup/SDPO — verl fork implementing SDPO paper ([[src_hubotter2026_self_distillation]]). Ingest dựa trên read các file cấu hình + loss + experiment scripts qua GitHub raw API (không clone).

## Cấu trúc repo

```
SDPO/
├── verl/                          # verl fork (RL training framework)
│   ├── trainer/
│   │   ├── config/
│   │   │   ├── sdpo.yaml          # entrypoint config cho SDPO runs
│   │   │   ├── actor/actor.yaml   # default actor config + templates
│   │   │   └── user.yaml          # user paths (dir/log_dir/ckpt_dir)
│   │   └── ppo/core_algos.py      # compute_self_distillation_loss() (line 1085)
│   └── workers/actor/
│       ├── dp_actor.py            # DataParallelPPOActor + TrustRegionTeacher + _update_teacher (EMA)
│       └── megatron_actor.py
├── experiments/
│   ├── generalization/            # §3 no-rich-feedback (sciknoweval, tooluse)
│   │   └── run_sdpo_all.sh
│   ├── rich_feedback/             # §4 LCBv6 rich feedback
│   │   └── run_sdpo.sh
│   └── ttt/                       # §5 test-time — chỉ có multiturn baseline
│       └── run_multiturn_all.sh
├── baseline_multiturn/multiturn.py  # TTT multi-turn baseline (không phải SDPO)
├── data/{split_tests.py, preprocess.py}
├── datasets/lcb_v6.json
├── run_local_sdpo.sh              # local smoke-test
└── requirements*.txt, Dockerfile.gh200
```

**Key insight #1**: **Không có dedicated TTT-SDPO script**. `experiments/ttt/` chỉ chứa multi-turn baseline. TTT-SDPO kết quả trong paper §5 chưa được released as reproducible script — thesis nếu muốn replicate phải tự wire lên từ SDPO trainer + single-question data loader. Đây là **infrastructure gap** thesis cần bridge.

## Default SDPO config (`verl/trainer/config/sdpo.yaml`)

```yaml
max_model_len: 18944  # = 512 template + 2048 prompt + 8192 feedback + 8192 response
actor_rollout_ref:
  actor:
    ppo_mini_batch_size: 32
    policy_loss:
      loss_mode: sdpo
    self_distillation:
      max_reprompt_len: 10240
      is_clip: 2.0
    optim:
      lr: 1e-5
  rollout:
    n: 8
    calculate_log_probs: True
algorithm:
  adv_estimator: grpo            # no critic
  norm_adv_by_std_in_grpo: False
  rollout_correction:
    rollout_is: token
    rollout_is_threshold: 2.0
data:
  train_batch_size: 32
trainer:
  val_before_train: False
```

## Full self-distillation config surface (`actor/actor.yaml`)

| Key | Default | Meaning |
|---|---|---|
| `loss_mode` | `vanilla` | Set `sdpo` để bật distillation |
| `full_logit_distillation` | `True` | Full logit KL thay vì reverse KL on sampled |
| `alpha` | `0.5` | **0.0=forward KL, 1.0=reverse KL, 0.5=JSD** |
| `success_reward_threshold` | `1.0` | Reward ≥ threshold = successful demo |
| `teacher_regularization` | `ema` | `ema` \| `trust-region` |
| `teacher_update_rate` | `0.05` | EMA rate (Hübotter default) hoặc trust-region mixing coef |
| `distillation_topk` | `100` | Top-K logits dùng cho KL (K=None → full vocab) |
| `distillation_add_tail` | `True` | Thêm tail bucket cho mass ngoài top-K |
| `is_clip` | `2.0` | IS ratio clip (None = off) |
| `max_reprompt_len` | `10240` | Truncate reprompted prompt tokens |
| `reprompt_truncation` | `right` | `left` \| `right` \| `error` |
| `dont_reprompt_on_self_success` | `True` | Skip nếu sample đã pass |
| `remove_thinking_from_demonstration` | `True` | Strip `<think>...</think>` — **= Kim's `c=s\think`** |
| `include_environment_feedback` | `True` | Rich feedback on/off |
| `environment_feedback_only_without_solution` | `True` | Dùng feedback chỉ khi không có successful solution |

**Key insight #2**: `remove_thinking_from_demonstration=True` **trùng khớp với Kim et al.'s `c=s\think` condition** — setting default đã là "strip thinking". Kim paper khảo sát `c=s` (full solution incl. thinking) vs `c=s\think`; Hübotter default chọn `c=s\think`. [[con_reprompt_template]] RQ1 có thể ablate thẳng flag này.

**Key insight #3**: Chỉ 2 teacher regularization modes: `ema` (reference worker updated as EMA) hoặc `trust-region` (teacher = `lerp(ref, student, mix_coef)`). Fixed teacher (EMA 0.0) = dùng `ema` với `teacher_update_rate=0.0`. Xem [[con_self_teacher]].

## Default templates (`actor/actor.yaml`)

```
reprompt_template: "{prompt}{solution}{feedback}\n\nCorrectly solve the original question."

solution_template: "\n\nCorrect solution:\n\n{successful_previous_attempt}"

feedback_template: "\n\nThe following is feedback from your unsuccessful earlier attempt:\n\n{feedback_raw}"
```

**Key insight #4**: **Đây là default template baseline cho RQ1**. Template taxonomy thesis sẽ vary:
- Negative instruction: thêm "Do not repeat the mistake you made"
- Confidence elicitation: "Rate your confidence first, then solve"
- Ordering: feedback-first vs solution-first
- Uncertainty preservation: "Use 'wait/hmm/perhaps' if unsure"

Templates là plain strings với `{prompt}`, `{solution}`, `{feedback}`, `{feedback_raw}`, `{successful_previous_attempt}` placeholders — trivial to edit.

## `compute_self_distillation_loss()` — core logic (`core_algos.py:1085`)

Flow:
1. **Distill targets**: nếu `distillation_topk` → dùng top-K logits + optional tail bucket; else full logits.
2. **KL direction**:
   - `alpha=0.0`: `KL(student || teacher)` (forward)
   - `alpha=1.0`: `KL(teacher || student)` (reverse)
   - `0<alpha<1`: **Generalized JSD** với mixture `m = (1-α)·π_s + α·π_t`, loss = `lerp(KL(m||s), KL(m||t), α)`.
3. **IS correction**: `ratio = exp(log π_s - log π_old).clamp(max=is_clip)`, multiplied vào per-token loss.
4. **Rollout correction**: optional token-level IS weights.
5. **Aggregate**: `token-mean` / `seq-mean-*`.

Non-full-logit path chỉ hỗ trợ reverse KL (`alpha=1.0`) dạng `log_ratio.detach() * student_log_probs`.

**Key insight #5**: JSD default (`α=0.5`) khác với typical self-distillation literature dùng forward hoặc reverse KL. Thesis RQ2 cần **kiểm tra α có modulate suppression không** — α=1.0 (reverse) có thể aggressive hơn về mode-seeking → suppression mạnh hơn; α=0.0 (forward) mode-covering → có thể preserve epistemic tokens. Kim 2026 không test dimension này.

## `_update_teacher()` EMA (`dp_actor.py`)

```python
if teacher_regularization != "ema": return
if update_rate == 0.0: return  # no-op = fixed teacher
for tp, sp in zip(teacher.params(), actor.params()):
    tp.data.mul_(1 - update_rate).add_(sp.data, alpha=update_rate)
```

`teacher_update_rate=0.0` ⇒ EMA update skipped ⇒ **teacher frozen tại ref checkpoint**. Đây là cách bật fixed-teacher mà Kim et al. recommend — setting đã có sẵn, chỉ cần override flag. Không cần code change.

## Experiment script diff — hyperparam quan trọng

| Param | Default sdpo.yaml | `generalization/run_sdpo_all.sh` (§3) | `rich_feedback/run_sdpo.sh` (§4 LCBv6) |
|---|---|---|---|
| DATA | — | sciknoweval {bio,chem,mat,phys} + tooluse | datasets/lcb_v6 |
| MODEL | — | Qwen3-8B, Olmo-3-7B-Instruct | Qwen3-8B |
| LR | 1e-5 | 1e-5 | **1e-6** (10× nhỏ hơn) |
| ALPHA | 0.5 (JSD) | 0.5 (JSD) | **1.0 (reverse KL)** |
| `distillation_topk` | 100 | 100 | **20** (K nhỏ hơn) |
| `teacher_update_rate` | 0.05 | 0.05 | **0.01** (5× chậm hơn) |
| `include_environment_feedback` | True | **False** (no rich feedback setting) | True |
| `ppo_mini_batch_size` | 32 | 32 | **1** (extreme on-policy) |
| `val_kwargs.n` | — | — | 4 |

**Key insight #6**: Rich-feedback LCBv6 config dùng hyperparams **rất khác default** — reverse KL, 10× smaller LR, 5× slower teacher EMA, aggressive on-policy (mini_batch=1). Cho thấy LCBv6 regime cần tuning mạnh. Thesis test-time code regime có thể khởi đầu từ rich_feedback hyperparams, không phải từ default.

**Key insight #7**: `ALPHA=1.0` (reverse KL) ở LCBv6 + Kim 2026 finding rằng reverse KL nổi tiếng là mode-seeking → **reverse KL có thể là nguyên nhân structural của suppression ở code regime**. Thesis RQ2 hypothesis mới: *suppression ở code có thể weaker khi chuyển sang forward KL hoặc JSD*. Đây là ablation specific chưa ai làm.

## TTT multi-turn baseline (`experiments/ttt/run_multiturn_all.sh`)

```bash
QUESTION_IDS=(1 3 10 43 46 59 69 74 86 91 92 95 100 103 111 120 125 127 129)
for qid in "${QUESTION_IDS[@]}"; do
  python baseline_multiturn/multiturn.py \
      --data-dir="lcb_v6_singles/q_${qid}" \
      --run-name="multiturn_q${qid}" --seed=0
done
```

**Key insight #8**: Danh sách 19 câu LCBv6 hard cho reproducibility thesis. IDs chính xác để thesis có thể chạy trên cùng subset và so sánh trực tiếp với bảng paper:
`{1, 3, 10, 43, 46, 59, 69, 74, 86, 91, 92, 95, 100, 103, 111, 120, 125, 127, 129}`

## `baseline_multiturn/multiturn.py` — TTT baseline (không phải SDPO)

Config:
- `MODEL = "Qwen/Qwen3-8B"`, `MAX_TOKENS=8192`, `MAX_TURNS=2880`, `MAX_CONTEXT_LEN=32000`
- `template_name = "feedback_only"` (alt: `"attempt_and_feedback"`)
- Feedback prefix: `"The following is feedback from your unsuccessful earlier attempt:\n\n"`
- Feedback suffix: `"\n\nCorrectly solve the original question."`
- Context overflow: drop earliest feedback khi vượt MAX_CONTEXT_LEN
- vLLM inference + `verl.utils.reward_score.multi_source_reward`
- Log wandb + jsonl

**Key insight #9**: Multi-turn = TTT without weight update. SDPO adds weight update. Thesis TTT-SDPO có thể lấy multiturn loop này làm skeleton, chèn gradient step per turn sau khi có successful attempt. **Không có skeleton sẵn cho TTT-SDPO trong repo** — thesis implementation effort thật sự.

## `run_local_sdpo.sh` — local smoke-test (có bug sensitive)

- `MODEL_PATH="Qwen/Qwen2.5-7B-Instruct"` ← **NOT Qwen3-8B** như paper
- `TRAIN_BATCH_SIZE=32`, `ROLLOUT_BATCH_SIZE=8`, `LR=1e-5`, `ALPHA=0.5`
- `DONT_REPROMPT_ON_SELF_SUCCESS=True`

**Key insight #10**: Local smoke test dùng Qwen2.5-7B-Instruct — nếu thesis replicate paper phải nhớ override về Qwen3-8B. Pitfall dễ miss.

## Implications cho thesis

### Infrastructure checklist

- [x] SDPO trainer có sẵn, config surface đầy đủ.
- [x] Templates là plain strings, trivial để taxonomy (RQ1).
- [x] α ablation (forward/JSD/reverse KL) có sẵn qua flag.
- [x] Fixed teacher qua `teacher_update_rate=0.0`.
- [x] Top-K distillation để save memory.
- [ ] **TTT-SDPO loop**: phải tự implement. Lấy `baseline_multiturn/multiturn.py` làm skeleton + chèn SDPO gradient step.
- [ ] **Single-question dataset format**: `lcb_v6_singles/q_{id}/` — cần verify format qua `data/split_tests.py` và `preprocess.py`.
- [ ] **Epistemic token logging hook**: chưa có trong verl — thesis cần thêm metric callback đếm tokens wait/hmm/... per step.

### Knobs trực tiếp relevant cho thesis RQs

| RQ | Knob | Code location |
|---|---|---|
| RQ1 (template) | `reprompt_template`, `solution_template`, `feedback_template` | `actor/actor.yaml` |
| RQ1 | `remove_thinking_from_demonstration` | ibid |
| RQ1 | `environment_feedback_only_without_solution` | ibid |
| RQ2 (suppression) | `alpha` (KL direction) | `core_algos.py:1085` |
| RQ2 | `teacher_update_rate` (0.0 vs 0.05) | `dp_actor._update_teacher` |
| RQ2 | `distillation_topk` (100 vs 20 vs None) | `core_algos.py:1085` |
| RQ3 (CTC) | `max_turns` (in multiturn), `rollout.n`, `ppo_mini_batch_size` | various |

## Follow-up actions

- Clone repo locally vào `experiments/` (user-owned area) để chạy.
- Verify `lcb_v6_singles/` format qua `data/split_tests.py`.
- Prototype TTT-SDPO bằng cách ghép `multiturn.py` skeleton + SDPO trainer call per-turn.
- Add epistemic token counter callback vào verl reward/metric pipeline.
- Khi có ý định chạy: query W&B logs của authors tại https://wandb.ai/jonhue/SDPO để xem metrics họ đã log → học format.

## Links

- [[src_hubotter2026_self_distillation]] — paper this repo implements.
- [[ent_sdpo]] · [[con_self_teacher]] · [[con_reprompt_template]] · [[con_test_time_self_distillation]]
- [[con_credit_assignment]] (logit/token/sequence knob = `full_logit_distillation` + `distillation_topk`)
- [[syn_kim2026_thesis_impact]] (ties to EMA/α ablation plan)
