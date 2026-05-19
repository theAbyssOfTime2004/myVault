---
type: source
created: 2026-05-19
updated: 2026-05-19
tags: [implementation, trl, huggingface, sdpo, sdft, peft, lora, decision]
sources: [src_trl_sdpo_sdft_docs]
url: https://huggingface.co/docs/trl/en/sdpo_trainer
code: https://github.com/huggingface/trl/tree/main/trl/experimental/sdpo
version: "trl==1.4.0"
depth: docs+example-script
aliases: [TRL SDPO integration, HuggingFace TRL self-distillation]
---

# HuggingFace TRL — SDPO + SDFT Trainer Integration

Implementation reference page cho việc thesis switch từ verl ([[src_lasgroup_sdpo_repo]]) sang TRL. Document findings sau khi WebFetch docs + example script ngày 2026-05-19.

**Source**: 
- Docs: https://huggingface.co/docs/trl/en/sdpo_trainer + https://huggingface.co/docs/trl/sdft_trainer
- Code: https://github.com/huggingface/trl/tree/main/trl/experimental/sdpo
- PR: huggingface/trl#4929 (SDPO), #4940 (SDFT)
- Confirmed merge từ [[src_youtube_hubotter_shenfeld_discussion]] (line 2055-2064).

## TL;DR — Decision

**Switch verl → TRL** cho thesis implementation. Tiết kiệm ~1-2 tuần infrastructure work. Trade-off duy nhất: mất trust-region teacher mode (chấp nhận được, ablate trong limitation section).

[[src_lasgroup_sdpo_repo]] giữ vai trò **scientific reference** (paper code, canonical hyperparam) chứ không phải implementation base.

## 5 Finding chính

### Finding 1: SDPOTrainer là class Python độc lập

```python
from trl.experimental.sdpo import SDPOTrainer, SDPOConfig

trainer = SDPOTrainer(
    model="Qwen/Qwen3-8B",
    args=SDPOConfig(...),
    train_dataset=ds,
    peft_config=lora_cfg,
)
trainer.train()
```

**Ý nghĩa**:
- Install: `pip install trl==1.4.0` (so với verl: clone ~50k-line repo, setup ray, FSDP)
- Debug: standard Python stack trace (so với verl: ray actor logs khó trace)
- Status: `trl.experimental.*` namespace → API có thể đổi giữa version → **must pin version** trong `requirements.txt`

**Cost saved**: ~1 tuần infrastructure setup.

### Finding 2: LoRA/PEFT built-in

```bash
--use_peft \
--lora_target_modules q_proj k_proj v_proj o_proj gate_proj up_proj down_proj
```

**Ý nghĩa**:
- Compute reality: GTX 1660 Ti 6GB chỉ đủ 0.5-1.5B; Modal A100-40GB không fit Qwen3-8B full FT
- Với LoRA r=32: VRAM training ~24GB, fit A100-40GB
- Không có LoRA = không làm được Phase 3 Qwen3-8B trong budget 30h A100
- → **must-have**, không phải nice-to-have

**Verl path**: phải tự wire up PEFT, không có example LoRA cho SDPO trong lasgroup repo.

### Finding 3: Reprompt template configurable qua Python dict

SDPO config có 3 template slots:
- `reprompt_template`: wrap toàn bộ context
- `solution_template`: format successful rollout (nếu có)
- `feedback_template`: format environment feedback

**Ý nghĩa cho RQ1**:
7 template ablation = 7 dict Python literals, không fork code. Workflow:

```python
TEMPLATES = {
    "T1_minimal": dict(reprompt_template="...", feedback_template="..."),
    "T2_standard": dict(...),  # anchor = Hübotter Table 2 default
    "T3_verbose": dict(...),
    "T4_json": dict(...),
    "T5_reasoning_inducing": dict(...),
    "T6_first_person": dict(...),
    "T7_cumulative": dict(...),
}

for name, tmpl in TEMPLATES.items():
    cfg = SDPOConfig(output_dir=f"sdpo-{name}", **tmpl, **shared_cfg)
    trainer = SDPOTrainer(model=base, args=cfg, train_dataset=ds, peft_config=lora_cfg)
    trainer.train()
```

→ Clean ablation matrix, không confound do hidden config drift.

### Finding 4: Hyperparam knobs match debate Hübotter vs Kim

| Knob | TRL config | Range | Maps tới |
|---|---|---|---|
| α (KL type) | `distillation_alpha` | 0.0 (forward) / 0.5 (JSD) / 1.0 (reverse) | Hübotter §4 default JSD; lasgroup LCBv6 = 1.0 |
| Teacher EMA | `teacher_update_rate` qua `ema` mode | 0.05 (Hübotter) / 0.0 (Kim recommend) | Direct ablation |
| Top-K | `distillation_topk` | 20 (LCBv6) / 100 (general) | Match lasgroup |
| Loss mode | `sdpo_policy_loss_mode` | `distillation_only` / `hybrid` | Hybrid match Hübotter §4.5 (`λ·A_GRPO + (1−λ)·A_SDPO`) |
| Full logit | `full_logit_distillation` | True / False | True = logit-level (Hübotter best); False = token-level reverse KL |

**Ý nghĩa**:
- Ablation Hübotter vs Kim contradiction (EMA 0.05 vs 0.0) trở thành 1 config swap, không phải code change.
- α ablation cho RQ2 (forward/JSD/reverse KL) làm trực tiếp qua flag.

### Finding 5: Dataset interface chỉ cần 2 column

```python
Dataset.from_dict({
    "prompt": [[{"role": "user", "content": question}]],
    "privileged_context": [feedback_text_from_evaluator],
})
```

**Ý nghĩa**:
- POC hiện tại có rich feedback từ unit test evaluator → map thẳng vào `privileged_context`
- Không phải restructure data pipeline
- TTT per-turn dataset = construct ad-hoc, 1 row per turn

## 3 Caveat cần biết

### Caveat 1: ⚠️ Test-time loop KHÔNG có sẵn

TRL trainer thiết kế **epoch-based** trên dataset cố định. TTT regime (1 câu, multi-turn, update per turn) phải tự wrap.

**Pseudo-code TTT loop**:

```python
def ttt_sdpo_one_question(question, max_turns=2750):
    trainer = SDPOTrainer(model=base, args=cfg, peft_config=lora_cfg)
    
    for turn in range(max_turns):
        # Generate với current weights
        response = trainer.model.generate(question)
        
        # Evaluate
        passed, feedback = evaluator(response, question)
        if passed:
            return turn, response
        
        # Build per-turn dataset
        trainer.train_dataset = Dataset.from_dict({
            "prompt": [[{"role": "user", "content": question}]],
            "privileged_context": [format_feedback(feedback)],
        })
        
        # 1 SDPO gradient step
        trainer.train()
    
    return max_turns, None  # discovery failed
```

**Risk** (load-bearing cho thesis):
- Weight có thật sự persist giữa các turn? (`trainer.model` reference vs new instance)
- LoRA adapter có save/restore đúng qua `.train()` calls?
- Generation có dùng updated weight không hay dùng base?

→ **Test ngay ở Stage 1 sanity check trên 0.5B local**. Bug ở đây sẽ kill toàn bộ pipeline.

### Caveat 2: Trust-region teacher KHÔNG support

TRL chỉ implement `"ema"` và `"none"` mode. Mất trust-region của Hübotter §4.3 (báo cáo +1.8% vs EMA).

**Impact**: trade-off ~1-2% performance. Thesis quan tâm template ablation + EMA vs frozen hơn → drop khỏi ablation, document trong limitation section.

**Limitation framing đề xuất**: *"Trust-region teacher regularization (Hübotter §4.3) không được include trong ablation vì TRL implementation chỉ hỗ trợ EMA và frozen mode. Chúng tôi ablate EMA vs frozen vì đây là core của contradiction Hübotter-Kim."*

### Caveat 3: vLLM support unclear

SDFT docs explicit: *"does not support `use_vllm=True`"*. SDPO docs không khẳng định nhưng có thể tương tự (cùng base trainer).

**Impact**: generation chậm hơn HF transformers default. POC hiện tại dùng vLLM → migration TRL có thể bottleneck ở generation throughput.

**Mitigation options**:
1. `torch.compile` trên HF generate + aggressive KV cache
2. Batch nhiều câu nếu independent (TTT mỗi câu có thể parallel)
3. **Decouple**: generate bằng vLLM riêng → save logprobs → feed vào TRL trainer riêng → đánh đổi complexity nhưng giữ tốc độ vLLM

**Action**: verify SDPO vLLM support bằng cách đọc source code hoặc test thực tế trước khi commit migration full.

## Implementation roadmap (post-migration)

### Stage 1 — Verify TRL functional (1-2 ngày, local)
- `pip install trl==1.4.0 peft datasets accelerate`
- Copy example script từ `trl/experimental/sdpo/sdpo.py`
- Chạy minimal SDPO trên Qwen2.5-0.5B với 1 câu LCBv6, 1 turn (không loop)
- Verify: loss compute, gradient step, model save/reload

### Stage 2 — TTT wrap (3-5 ngày, local)
- Implement `ttt_sdpo_one_question` loop (Caveat 1)
- Test 1 câu, 10 turn, verify weight update giữa các turn
- Edge case: LoRA persist, generation use latest weight, no memory leak

### Stage 3 — Define 7 templates (parallel với Stage 2)
- Blocker cho RQ1 — define dimension taxonomy trước
- 7 Python dict literals trong `templates.py`

### Stage 4 — Pilot trên Colab L4 (5h budget)
- Qwen2.5-1.5B + LoRA r=16
- 2 câu × 7 template × 1 seed = 14 run
- Down-select 4 template tốt nhất

### Stage 5 — Phase 3 final trên Modal A100 (30h budget)
- Qwen3-8B + LoRA r=32
- 4 template × 5 câu × 2 seed = 40 run
- Hoặc Wave 2 split: 4 template × EMA 0.05 (12 run) + top 2 template × EMA 0.0 (6 run) = 18 run

## Code mẫu Phase 3

```bash
python trl/experimental/sdpo/sdpo.py \
    --model_name_or_path Qwen/Qwen3-8B \
    --use_peft \
    --lora_r 32 \
    --lora_target_modules q_proj k_proj v_proj o_proj gate_proj up_proj down_proj \
    --learning_rate 1e-6 \
    --dtype bfloat16 \
    --bf16 true \
    --per_device_train_batch_size 1 \
    --gradient_accumulation_steps 1 \
    --distillation_alpha 1.0 \
    --distillation_topk 20 \
    --full_logit_distillation true \
    --sdpo_policy_loss_mode distillation_only \
    --include_environment_feedback true
```

Setting match `experiments/rich_feedback/run_sdpo.sh` của [[src_lasgroup_sdpo_repo]] (LCBv6 hyperparams: LR=1e-6, α=1.0, mini_batch=1, topk=20).

## So sánh paths

| Aspect | verl ([[src_lasgroup_sdpo_repo]]) | TRL (this page) | OpenClaw-RL |
|---|---|---|---|
| Scientific authority | ✅ paper code | ⚠️ adaptation | ⚠️ variant (PPO-clipped) |
| LoRA/PEFT | manual | built-in flag | not mentioned |
| Template ablation | YAML config | Python dict | hardcoded |
| Trust-region teacher | ✅ | ✗ | ? |
| EMA / frozen teacher | ✅ | ✅ | ? |
| TTT loop | có baseline script (no weight update) | phải tự wrap | có (production loop) |
| vLLM | ✅ | ✗ (SDFT confirm) | ✅ |
| Code base size | ~50k lines verl | vài trăm lines | full Megatron-LM stack |
| Hardware | flexible | flexible | 8× GPU, CUDA 12.9 |
| Documentation | sparse | docs + example | partial |
| Status | research code | experimental flag | research demo |
| **Verdict cho thesis** | scientific reference | ⭐ **implementation** | citation only |

## Open questions

- vLLM cho SDPO confirm hay không support? → action: fetch source code `trl/experimental/sdpo/sdpo_trainer.py` line ~239
- TRL có cleanup `optimizer.state` giữa các `.train()` call không? Ảnh hưởng TTT loop với LoRA.
- `peft_config` có persist correct qua multiple `.train()` calls hay reset adapter mỗi lần?

## Links

- [[src_lasgroup_sdpo_repo]] — scientific reference (paper code)
- [[src_hubotter2026_self_distillation]] — origin paper (hyperparam source)
- [[src_kim2026_why_self_distillation_degrades]] — EMA vs frozen ablation motivation
- [[src_youtube_hubotter_shenfeld_discussion]] — confirm TRL merge timeline
- [[src_shenfeld2026_sdft]] — sister algorithm, SDFTTrainer cũng available
- [[con_reprompt_template]] · [[con_test_time_self_distillation]] · [[con_self_teacher]] · [[con_sdpo_loss_mechanics]]
- [[syn_thesis_proposal]] — overall plan (cần update timeline với TRL migration savings)
