# TTT-SDPO Implementation Plan — W2 Milestone

**Goal**: Implement test-time SDPO POC on 1 LCBv6 hard question with T2 (Standard) template; verify discovery curve qualitatively matches Hübotter §5 Figure 13.

**Target reader**: Cursor agent with no prior context. This document is self-contained.

**Status when this plan starts**:
- ✅ `baseline_multiturn/multiturn.py` works end-to-end on LCBv6 (multi-turn inference, vLLM, no weight update)
- ❌ No TTT-SDPO code exists publicly (verified via search of lasgroup/SDPO, huggingface/trl/experimental/sdpo, beanie00/self-distillation-analysis)
- ✅ Reference loss implementation: `verl/trainer/ppo/core_algos.py:1085` (in lasgroup/SDPO)
- ✅ Reference EMA teacher: `verl/workers/actor/dp_actor.py` (TrustRegionTeacher class + `_update_teacher` method)

**Hardware target**: Colab L4 24GB (free tier with Pro) for pilot. NOT local GTX 1660 Ti (insufficient VRAM).

---

## 0. Repository context

**Working repo**: `/home/theabyssoftime/Repos/SDPO/` (cloned from `https://github.com/lasgroup/SDPO`)

**Files to read before starting** (from working repo):
- `baseline_multiturn/multiturn.py` — reference loop structure (lines 137–272 for `run_question`)
- `verl/trainer/ppo/core_algos.py:1085` — `compute_self_distillation_loss()` reference logic
- `verl/workers/actor/dp_actor.py` — `_update_teacher` EMA method (~lines 130–155)
- `verl/trainer/config/actor/actor.yaml` — default templates (search "reprompt_template")
- `experiments/rich_feedback/run_sdpo.sh` — paper hyperparameters for LCBv6

**External reference** (read-only, for borrowing logic):
- `https://github.com/huggingface/trl/blob/main/trl/experimental/sdpo/sdpo_trainer.py` — `SuccessfulRolloutTeacherContextBuilder`, `EMATeacherSyncCallback`
- `https://arxiv.org/pdf/2601.20802` Hübotter §5 (test-time SDPO formulation, Algorithm in Appendix)

---

## 1. Architecture decisions (locked)

| Decision | Choice | Rationale |
|---|---|---|
| Generation backend | **HuggingFace `model.generate()`** | vLLM doesn't support gradients; using HF for both gen + train avoids weight sync complexity |
| Model | **Qwen3-1.7B** for pilot, Qwen3-8B + LoRA later | Pilot fits L4 24GB without LoRA; 8B requires LoRA |
| Training method | Full FT for 1.7B pilot, **LoRA r=32** for 8B final | LoRA reduces memory ~30× for 8B |
| Optimizer | AdamW (`bitsandbytes` 8-bit when scaling to 8B) | Memory savings |
| Precision | bfloat16 | Standard for Qwen3 |
| Batch size | **1** for POC | Paper uses 16 but 1 is sufficient to verify mechanism; revisit later |
| KL direction | α = 0.5 (JSD) | Default in `verl/trainer/config/actor/actor.yaml`; matches paper |
| Top-K distillation | **Full vocab** for POC simplicity | Top-K=100 optimization can be added later |
| IS clip | 2.0 | Paper default |
| Teacher regularization | EMA with `update_rate=0.05` | Paper default; ablation EMA=0.0 deferred to W4+ |
| Per-question fresh weights | **YES** — reset to base before each new question | Paper §5: TTT-SDPO updates are per-question, not cumulative |

---

## 2. File structure to create

Create new directory `ttt_sdpo/` at repo root:

```
ttt_sdpo/
├── __init__.py
├── config.py             # TTTConfig dataclass
├── templates.py          # T2 template (only T2 for W2; T1,T3-T7 added later)
├── teacher_context.py    # Build teacher prompt from question+feedback+demo
├── sdpo_loss.py          # KL loss computation (port of compute_self_distillation_loss)
├── ema_teacher.py        # EMA teacher manager
├── runner.py             # Main TTT-SDPO loop (the entry point)
├── logging_utils.py      # JSONL + wandb logging
└── run_ttt_q1.sh         # Convenience script: run on q_1 with T2
```

**Do NOT modify**:
- `baseline_multiturn/multiturn.py` (keep as inference baseline)
- Anything under `verl/` (keep upstream verl untouched)
- `experiments/ttt/run_multiturn_all.sh`

---

## 3. Component-by-component spec

### 3.1 `ttt_sdpo/config.py`

```python
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class TTTConfig:
    # Model
    model_name: str = "Qwen/Qwen3-1.7B"
    dtype: str = "bfloat16"
    use_lora: bool = False  # True for 8B
    lora_r: int = 32
    lora_alpha: int = 64
    lora_target_modules: tuple = ("q_proj", "k_proj", "v_proj", "o_proj")
    
    # Generation
    max_response_tokens: int = 8192
    temperature: float = 1.0
    top_p: float = 1.0
    top_k: int = -1
    rollouts_per_turn: int = 1  # batch size 1 for POC
    
    # SDPO loss
    alpha: float = 0.5            # JSD
    is_clip: float = 2.0
    distillation_topk: Optional[int] = None  # None = full vocab for POC
    distillation_add_tail: bool = True
    
    # Teacher
    teacher_update_rate: float = 0.05  # EMA; 0.0 = fixed teacher
    success_reward_threshold: float = 1.0
    environment_feedback_only_without_solution: bool = True
    remove_thinking_from_demonstration: bool = True
    
    # Optimizer
    learning_rate: float = 1e-6  # paper LCBv6 setting
    weight_decay: float = 0.0
    grad_clip: float = 1.0
    
    # Loop
    max_turns: int = 200  # for POC; paper uses 2750
    max_context_len: int = 32000
    template_name: str = "T2"
    
    # Output
    output_dir: str = "outputs/ttt_sdpo"
    wandb_project: str = "ttt-sdpo"
    seed: int = 0
```

### 3.2 `ttt_sdpo/templates.py`

Only T2 (Standard, paper anchor) for W2. Add T1, T3–T7 in W3.

```python
T2_REPROMPT = """{prompt}
{solution_block}
{feedback_block}
Correctly solve the original question."""

T2_SOLUTION_BLOCK = """
Correct solution:

{successful_previous_attempt}
"""

T2_FEEDBACK_BLOCK = """
The following is feedback from your unsuccessful earlier attempt:

{feedback_raw}
"""

def build_teacher_prompt_T2(
    question: str,
    successful_attempt: Optional[str],
    feedback_raw: Optional[str],
    include_environment_feedback: bool = True,
    environment_feedback_only_without_solution: bool = True,
) -> str:
    solution_block = ""
    feedback_block = ""
    
    if successful_attempt is not None:
        solution_block = T2_SOLUTION_BLOCK.format(
            successful_previous_attempt=successful_attempt
        )
    
    use_feedback = include_environment_feedback and feedback_raw is not None
    if environment_feedback_only_without_solution and successful_attempt is not None:
        use_feedback = False
    
    if use_feedback:
        feedback_block = T2_FEEDBACK_BLOCK.format(feedback_raw=feedback_raw)
    
    return T2_REPROMPT.format(
        prompt=question,
        solution_block=solution_block,
        feedback_block=feedback_block,
    )
```

Note: student prompt = `question` (raw, no template). Teacher prompt = output of `build_teacher_prompt_T2(...)`. Both then have the **same** student response appended for log-prob computation.

### 3.3 `ttt_sdpo/sdpo_loss.py`

Port of `verl/trainer/ppo/core_algos.py:1085` (`compute_self_distillation_loss`), simplified for batch=1, full-vocab.

Signature:
```python
def compute_sdpo_loss(
    student_logits: torch.Tensor,    # (1, L, V)
    teacher_logits: torch.Tensor,    # (1, L, V), no_grad
    response_mask: torch.Tensor,     # (1, L), 1 for response tokens, 0 for prompt
    old_log_probs: torch.Tensor,     # (1, L), from generation step (no_grad)
    student_log_probs: torch.Tensor, # (1, L), gathered from student_logits (with grad)
    alpha: float = 0.5,
    is_clip: float = 2.0,
) -> torch.Tensor:
    """Returns scalar loss."""
```

Logic (mirror lasgroup `core_algos.py:1145–1200`):
1. Convert logits to log-probs via `F.log_softmax(logits, dim=-1)`
2. Compute per-position KL:
   - α=0.0: `F.kl_div(student_logp, teacher_logp, reduction='none', log_target=True).sum(-1)`
   - α=1.0: `F.kl_div(teacher_logp, student_logp, reduction='none', log_target=True).sum(-1)`
   - else: JSD via mixture (see verl reference code line 1158–1170)
3. IS correction: `ratio = exp(student_log_probs - old_log_probs).clamp(max=is_clip)`
4. `per_token_loss = kl * ratio * response_mask`
5. Aggregate: `loss = per_token_loss.sum() / response_mask.sum().clamp(min=1.0)`

**Reference for verbatim port**: read `verl/trainer/ppo/core_algos.py` from line 1085 of working repo.

### 3.4 `ttt_sdpo/ema_teacher.py`

```python
import copy
import torch
from torch import nn

class EMATeacher:
    def __init__(self, student: nn.Module, update_rate: float):
        self.update_rate = update_rate
        self.teacher = copy.deepcopy(student)
        for p in self.teacher.parameters():
            p.requires_grad_(False)
        self.teacher.eval()
    
    @torch.no_grad()
    def step(self, student: nn.Module) -> None:
        if self.update_rate == 0.0:
            return  # fixed teacher
        for tp, sp in zip(self.teacher.parameters(), student.parameters()):
            tp.data.mul_(1.0 - self.update_rate).add_(sp.data, alpha=self.update_rate)
    
    def forward_logits(self, input_ids: torch.Tensor, attention_mask: torch.Tensor) -> torch.Tensor:
        with torch.no_grad():
            return self.teacher(input_ids=input_ids, attention_mask=attention_mask).logits
```

For LoRA scenario: teacher copies base + adapter; EMA updates adapter weights only. Defer LoRA EMA logic to W3.

### 3.5 `ttt_sdpo/runner.py` — main loop

This is the **core file**. Skeleton:

```python
def run_ttt_sdpo(cfg: TTTConfig, question: QuestionData) -> dict:
    # 1. Setup
    tokenizer = AutoTokenizer.from_pretrained(cfg.model_name)
    student = AutoModelForCausalLM.from_pretrained(
        cfg.model_name, torch_dtype=torch.bfloat16,
    ).to("cuda")
    if cfg.use_lora:
        from peft import LoraConfig, get_peft_model
        lora_cfg = LoraConfig(r=cfg.lora_r, lora_alpha=cfg.lora_alpha,
                              target_modules=list(cfg.lora_target_modules),
                              task_type="CAUSAL_LM")
        student = get_peft_model(student, lora_cfg)
    
    teacher = EMATeacher(student, cfg.teacher_update_rate)
    optimizer = torch.optim.AdamW(student.parameters(), lr=cfg.learning_rate,
                                   weight_decay=cfg.weight_decay)
    
    # 2. State
    successful_attempts: list[str] = []
    feedback_history: list[str] = []
    response_history: list[str] = []
    history = []
    
    # 3. Loop
    for turn in range(cfg.max_turns):
        # ----- Generate -----
        student_prompt = build_student_prompt(question.prompt, tokenizer)  # raw question + chat template
        student_input_ids = tokenizer(student_prompt, return_tensors="pt").to("cuda")
        
        student.eval()
        with torch.no_grad():
            gen_out = student.generate(
                **student_input_ids,
                max_new_tokens=cfg.max_response_tokens,
                temperature=cfg.temperature,
                top_p=cfg.top_p,
                top_k=cfg.top_k if cfg.top_k > 0 else None,
                do_sample=True,
                return_dict_in_generate=True,
                output_scores=True,
            )
        response_ids = gen_out.sequences[0, student_input_ids["input_ids"].shape[1]:]
        response_text = tokenizer.decode(response_ids, skip_special_tokens=True)
        # Compute old_log_probs from gen_out.scores (per-token logits at gen time)
        old_log_probs = compute_log_probs_from_scores(gen_out.scores, response_ids)
        
        # ----- Evaluate -----
        score = code_reward.compute_score(
            solution=response_text,
            ground_truth=question.tests,
            extra_info={"split": question.split, "truncated": False},
            sparse_rewards=True,
        )
        reward = float(score.get("score", 0.0))
        feedback_raw = score.get("feedback", "")
        
        log_turn(turn, reward, response_text, feedback_raw, ...)
        
        # ----- Termination check -----
        if reward >= cfg.success_reward_threshold:
            successful_attempts.append(response_text)
            break  # discovery achieved
        
        feedback_history.append(feedback_raw)
        response_history.append(response_text)
        
        # ----- SDPO step -----
        teacher_prompt_text = build_teacher_prompt_T2(
            question=question.prompt,
            successful_attempt=successful_attempts[-1] if successful_attempts else None,
            feedback_raw=feedback_raw,
            environment_feedback_only_without_solution=cfg.environment_feedback_only_without_solution,
        )
        # Apply chat template
        teacher_full_text = apply_chat_template_with_response(
            tokenizer, teacher_prompt_text, response_text
        )
        student_full_text = apply_chat_template_with_response(
            tokenizer, question.prompt, response_text
        )
        
        teacher_inputs = tokenizer(teacher_full_text, return_tensors="pt").to("cuda")
        student_inputs = tokenizer(student_full_text, return_tensors="pt").to("cuda")
        
        # Build response mask for both: 1 at positions of response tokens, 0 at prompt
        teacher_response_mask = build_response_mask(teacher_inputs, response_ids)
        student_response_mask = build_response_mask(student_inputs, response_ids)
        
        # Forward passes
        student.train()
        student_out = student(**student_inputs)  # (1, L_s, V)
        with torch.no_grad():
            teacher_logits = teacher.forward_logits(**teacher_inputs)  # (1, L_t, V)
        
        # Align response token logits between student and teacher
        # (response tokens are the SAME ids in both; align by mask positions)
        student_response_logits = gather_response_logits(student_out.logits, student_response_mask)
        teacher_response_logits = gather_response_logits(teacher_logits, teacher_response_mask)
        
        # Get student log_probs at response token positions for IS ratio
        student_lp_for_response = gather_log_probs(student_response_logits, response_ids)
        
        loss = compute_sdpo_loss(
            student_logits=student_response_logits.unsqueeze(0),
            teacher_logits=teacher_response_logits.unsqueeze(0),
            response_mask=torch.ones_like(response_ids).unsqueeze(0),
            old_log_probs=old_log_probs.unsqueeze(0),
            student_log_probs=student_lp_for_response.unsqueeze(0),
            alpha=cfg.alpha,
            is_clip=cfg.is_clip,
        )
        
        optimizer.zero_grad()
        loss.backward()
        torch.nn.utils.clip_grad_norm_(student.parameters(), cfg.grad_clip)
        optimizer.step()
        teacher.step(student)
        
        log_sdpo_step(turn, loss.item(), ...)
    
    return {"history": history, "discovered_at_turn": turn if reward >= 1.0 else None}
```

### 3.6 `ttt_sdpo/run_ttt_q1.sh`

```bash
#!/usr/bin/env bash
set -euo pipefail
python -m ttt_sdpo.runner \
    --data-dir lcb_v6_singles/q_1 \
    --run-name ttt_sdpo_q1_T2_seed0 \
    --template T2 \
    --seed 0
```

---

## 4. Critical implementation pitfalls

### 4.1 Response token alignment between student and teacher

Student prompt and teacher prompt have **different lengths** (teacher has feedback prepended). But the response is the **same token sequence** in both. SDPO loss requires comparing logits at the **same response token positions**.

Implementation:
1. Tokenize student_prompt + response and teacher_prompt + response separately
2. Build a mask that is 1 at response token positions, 0 at prompt positions, for each
3. When computing loss, gather logits only at response positions for both
4. Verify the gathered logit tensors have the **same number of response tokens** (assert)

### 4.2 Logit-to-log-prob shift-by-one

Standard transformer LM: `logits[i]` predicts `token[i+1]`. So when computing log-prob of response tokens:
```python
# response_ids: (L_resp,)
# student_logits: (L_total, V) where L_total includes prompt
# response starts at position prompt_len
# logit at position prompt_len-1 predicts response token 0
# logit at position prompt_len+L_resp-2 predicts response token L_resp-1

response_logits = logits[prompt_len - 1 : prompt_len + L_resp - 1]  # (L_resp, V)
log_probs = F.log_softmax(response_logits, dim=-1)
gathered = log_probs.gather(-1, response_ids.unsqueeze(-1)).squeeze(-1)  # (L_resp,)
```

Verify with a unit test on a tiny example before running full loop.

### 4.3 `old_log_probs` vs current student log_probs

`old_log_probs` = log-probs at generation time (before any weight update).
`student_log_probs` = log-probs computed from current student forward pass.

If you skip IS correction (set `is_clip=None`), you can ignore `old_log_probs`. For POC, **set `is_clip=None` initially** and add IS correction later — simplifies debugging.

### 4.4 Chat template handling

Qwen3 uses chat template with role tags. When building teacher prompt with feedback, the feedback should be part of the **user message** content, NOT a separate role.

Verify with:
```python
messages = [{"role": "user", "content": teacher_prompt_text}]
formatted = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
print(formatted)
```

### 4.5 Memory: forward pass on full context twice

Both student and teacher forward passes process `prompt + response`. For long responses (8K tokens) on Qwen3-1.7B, this is OK on L4 24GB. For Qwen3-8B without LoRA, it will OOM — that's why LoRA is required for 8B.

Enable gradient checkpointing for student:
```python
student.gradient_checkpointing_enable()
```

### 4.6 Numerical stability

For full-vocab KL: `F.kl_div(log_p, log_q, log_target=True, reduction='none').sum(-1)` is numerically stable. **Do not** compute KL by hand with `log(p/q)` — use the F.kl_div API.

For JSD mixture: use `torch.logsumexp` for the mixture log-prob computation (see verl reference code).

---

## 5. Testing & verification

Before running on q_1 (the hard 54-turn case), verify with:

### 5.1 Unit tests (5 minutes)

In `ttt_sdpo/tests/`:
- `test_response_mask.py`: build mask for synthetic prompt+response, verify positions
- `test_log_prob_shift.py`: forward pass on a known sequence, verify log-prob computation matches manual computation
- `test_sdpo_loss.py`: with student==teacher, loss should be ~0; with very different distributions, loss should be large

### 5.2 Smoke test on q_2 (easy, ~15 minutes on L4)

q_2 passes in ~1 turn for baseline. With TTT-SDPO:
- Should pass in 1 turn (no SDPO step needed)
- Verify pipeline runs without crashing
- Verify wandb logs appear

### 5.3 Real test on q_120 (medium, ~30–60 minutes on L4)

q_120 needs ~15–25 turns for baseline. With TTT-SDPO:
- Should converge in **fewer turns** than baseline (this is the W2 success criterion)
- Loss should generally decrease across turns
- Teacher entropy should be < student entropy initially, converge over time

### 5.4 Stretch test on q_1 (hard, may take 1–2 hours on L4)

Baseline needs 54 turns with MemoryError intermediate. With TTT-SDPO target: < 54 turns, ideally 20–40 turns. **This is the W2 milestone evidence.**

---

## 6. Acceptance criteria for W2 done

W2 is complete when:

- [ ] `ttt_sdpo/runner.py` runs end-to-end on q_1 with T2 template without crashing
- [ ] Discovery turn count is **logged** (turn at which reward=1.0 first achieved)
- [ ] Loss curve, reward curve, teacher entropy curve are logged to wandb
- [ ] On q_120 (medium): TTT-SDPO converges in fewer turns than baseline multiturn (sanity)
- [ ] On q_1 (hard): TTT-SDPO converges in ≤ baseline's 54 turns (qualitative match with paper §5 claim of 3× faster)
- [ ] Documentation in `ttt_sdpo/README.md` explaining how to run

W2 NOT required:
- 7 templates (W3)
- LoRA (W3 when scaling to 8B)
- Top-K distillation (W4 optimization)
- Multiple seeds (W5+)
- Full instrumentation for RQ2 epistemic markers (W4)

---

## 7. Compute budget for W2

| Task | Hardware | Estimated time | Cost |
|---|---|---|---|
| Unit tests | Local CPU | 5 min | $0 |
| Smoke test q_2 | Colab L4 | 15 min | ~5 compute units |
| Test q_120 | Colab L4 | 30–60 min | ~10 compute units |
| Test q_1 | Colab L4 | 1–2 hours | ~20 compute units |
| Debug iterations | Colab L4 | 2–4 hours | ~50 compute units |
| **W2 total** | | **4–8 hours wall-clock** | **~85 compute units** |

Stays well within 300 unit Colab Pro budget.

---

## 8. Handoff to W3

Once W2 acceptance criteria pass:

W3 work (next milestone):
1. Add T1, T3–T7 templates to `ttt_sdpo/templates.py`
2. Refactor `runner.py` to take template as parameter
3. Run pilot on Qwen3-1.7B × 2 questions × 7 templates → identify ≥3 templates with measurable behavior difference
4. Add LoRA for scaling to 8B
5. Add epistemic token logging hooks (Component C instrumentation)

---

## 9. Reference snippets to copy verbatim

### From `verl/trainer/ppo/core_algos.py:1145–1200` (in working repo):

This is the production SDPO loss. Read it line-by-line and port to `sdpo_loss.py`. The verl version has more features (rollout correction, sequence-level masking, top-K) — **strip those for POC**, keep only:
- KL computation per α value
- IS clip
- Mean over response tokens

### From `verl/workers/actor/dp_actor.py:130–155`:

The `_update_teacher` method. Already extracted into the spec above as `EMATeacher.step`.

### From HF TRL `trl/experimental/sdpo/sdpo_trainer.py`:

Look at `SuccessfulRolloutTeacherContextBuilder.build()` for inspiration on building teacher context — but **do not import** TRL; the API is for batch training, not per-question TTT.

---

## 10. Out of scope for this implementation

Explicitly **NOT** in this plan:
- Distributed training (single GPU only)
- Multi-question batching
- LiveCodeBench evaluation harness changes (use existing `verl.utils.reward_score.feedback.code`)
- New template variants (T1, T3–T7)
- Epistemic token logging (Component C)
- Teacher-entropy stopping rule (Component D)
- Cross-domain checkpoints (Component B)

These are tracked separately in [[syn_thesis_proposal]].
