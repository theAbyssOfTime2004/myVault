---
type: entity
created: 2026-04-22
updated: 2026-04-22
tags: [method, rl, baseline]
sources: [src_hubotter2026_self_distillation]
aliases: [Group Relative Policy Optimization, GRPO]
---

# GRPO — Group Relative Policy Optimization

RLVR algorithm giới thiệu bởi Shao et al. 2024 (DeepSeek). Ước lượng advantage từ outcome reward **tương đối trong group** các rollout cùng question, không cần value network.

Là **baseline chính** của [[src_hubotter2026_self_distillation]]. Thesis cũng dùng GRPO cho comparison (thesis proposal mentioned).

## Advantage formula

Cho group G rollouts `{y_i}` của cùng question `x`, reward `r_i`:

```
A_GRPO_{i,t} = r_i − mean{r_j}_{j=1..G}
```

Properties:
- **Constant across tokens** trong một rollout (không per-token).
- **Unbiased** với objective `J(θ) = E[r(y|x)]`.
- Monte Carlo estimate — variance cao.
- Nếu cả group cùng reward (thường là 0 trên hard task) → advantage = 0, learning **stall**.

## So với SDPO

Xem bảng chi tiết ở [[ent_sdpo]]. Tóm tắt:
- GRPO: Monte Carlo, unbiased, sequence-level, consumes scalar reward.
- SDPO: bootstrapped (via self-teacher), biased, logit-level, consumes [[con_rich_feedback]].

Trade-off quen thuộc trong RL: MC unbiased-high-variance vs bootstrapped biased-low-variance (Sutton & Barto).

## Improved GRPO variant dùng trong paper

Paper dùng GRPO với several modern mods (§3.1):
- Asymmetric clipping (Yu et al. 2025)
- Avoid biased normalization (Liu et al. 2025b)
- Off-policy correction cho efficient inference (Yao et al. 2025)
- PPO-style importance weighting để off-policy training

Đây là "strong baseline" paper so sánh với.

## Hybrid SDPO + GRPO (§4.5)

```
A_hybrid = λ·A_GRPO + (1−λ)·A_SDPO,  λ ∈ [0,1]
```

- λ=0.9: tốt hơn SDPO trên Qwen3-0.6B (weak model), kém trên Qwen3-8B.
- → GRPO signal có thể **harmful** trên strong model.

## Thesis relevance

- Baseline để so với test-time SDPO ở cả RQ1 và RQ3.
- Có thể dùng như reference point khi đo [[con_epistemic_verbalization]] — RQ2: liệu GRPO giữ uncertainty tốt hơn SDPO trên code?
