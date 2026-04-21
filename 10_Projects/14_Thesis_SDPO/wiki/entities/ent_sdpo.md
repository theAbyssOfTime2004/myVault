---
type: entity
created: 2026-04-22
updated: 2026-04-22
tags: [method, rl, self-distillation, core]
sources: [src_hubotter2026_self_distillation]
aliases: [Self-Distillation Policy Optimization, SDPO]
---

# SDPO — Self-Distillation Policy Optimization

Algorithm RL on-policy được giới thiệu trong [[src_hubotter2026_self_distillation]]. Instantiate paradigm [[ent_rlrf]]: chuyển tokenized feedback thành logit-level credit assignment, dùng chính policy (conditioned on feedback) làm [[con_self_teacher]].

## Công thức loss

```
L_SDPO(θ) = Σ_t KL( π_θ(·|x, y<t) || stopgrad(π_θ(·|x, f, y<t)) )
```

- `π_θ(·|x, y<t)`: **student** — next-token distribution tại position `t`.
- `π_θ(·|x, f, y<t)`: **teacher** — cùng model nhưng được condition thêm feedback `f`.
- `stopgrad`: chặn gradient qua teacher → teacher không "collapse" về ignore `f`.

Trong practice dùng **Jensen-Shannon divergence** (symmetric) thay cho plain KL để stability.

## Thuật toán (Algorithm 1 của paper)

```
for each iteration:
  1. Sample question x
  2. Sample G rollouts: {y_i} ~ π_θ(·|x)
  3. Evaluate → feedback f_i
  4. Compute log-probs của self-teacher: log π_θ(y_i,t | x, f_i, y_i,<t)
  5. Gradient descent trên L_SDPO
```

## SDPO vs GRPO (khác biệt cốt lõi)

| | [[ent_grpo]] | SDPO |
|---|---|---|
| Advantage | `r_i − mean{r_j}` | `log π_teacher / π_student` |
| Per token | Constant trong rollout | Khác nhau mỗi position |
| Feedback consumed | Scalar `r` | Tokenized `f` (rich) |
| Signal density | Sequence-level | **Logit-level** |

Nghĩa là SDPO là extension "drop-in" của GRPO: giữ nguyên pipeline, chỉ swap advantages.

## Train-time vs test-time (scope thesis)

| | Train-time SDPO (Hübotter 2026 §3–4) | Test-time SDPO (thesis) |
|---|---|---|
| Cái gì update? | Weights `θ` | Weights — nhưng chỉ cho **1 câu hỏi** |
| Batch | Nhiều questions | 1 hard question, iterate |
| Evaluation | accuracy over test set | [[con_discovery_at_k]] |
| Paper section | §3, §4 | §5 — xem [[con_test_time_self_distillation]] |

Thesis focus regime test-time, nơi §5 mở ra nhưng chưa khảo sát behavioral aspects (RQ1/RQ2).

## Tính chất quan trọng (từ paper)

### Scale emergent (§4.1)

Self-teaching ability là emergent với scale:
- Qwen3-8B ([[ent_qwen3_8b]]): SDPO >> GRPO.
- Qwen3-0.6B: SDPO ≈ GRPO.
- Qwen2.5-1.5B: SDPO < GRPO.

→ SDPO chỉ work khi base model đủ mạnh ở in-context learning.

### Concise reasoning (§3.3)

SDPO generations **ngắn hơn 3×–11×** so với GRPO nhưng accuracy cao hơn. GRPO rơi vào filler ("Hmm", "Wait"), circular reasoning; SDPO concise. Dense credit assignment → learn **how** to reason chứ không phải just how long.

→ Đây là observation Future Work mà thesis RQ1 extend.

### Self-teacher bootstrap (§4.3)

- Teacher không frozen; update cùng student với regularization.
- Teacher accuracy tăng theo time → student có thể vượt initial teacher ("true bootstrapping").
- Best regularization: trust-region (50.6%) > EMA (49.3%) > frozen (48.8%) > unregularized (diverge).

### Feedback content (§4.6, Table 6)

- Env output + own solution: tốt nhất (48.3%).
- Include student's original attempt y trong teacher template: **giảm entropy** (0.23 vs 0.40), kém diversity.
- → Template design matters. Liên hệ trực tiếp RQ1.

### Compute overhead nhẹ (§2.2)

+5.8% (no env) đến +17.1% (with code env) time/step so với GRPO.

## Limitations (thừa nhận trong paper §7)

- Yêu cầu strong in-context learner → không work trên weak models.
- Phụ thuộc chất lượng feedback — misleading/uninformative feedback → không học được.
- Overhead có thể cao hơn trên small models với short generations.

## Open thesis questions

- Train-time SDPO có suppress [[con_epistemic_verbalization]] không? (Kim et al. 2026 nói có trên math.)
- Test-time SDPO có cùng suppression không? → **RQ2** của thesis.
- Biến thể [[con_reprompt_template]] nào help/hurt? → **RQ1**. Paper note template không nhạy syntactically, nhưng *systematic* study chưa có.
- [[con_ctc_metric]] behavior across templates? → **RQ3**.
- Teacher regularization có effect ở test-time không? Paper chỉ test train-time.
