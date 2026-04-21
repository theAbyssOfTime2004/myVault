---
type: entity
created: 2026-04-22
updated: 2026-04-22
tags: [rl, training-setting, verifiable-reward, baseline]
sources: [src_hubotter2026_self_distillation]
aliases: [Reinforcement Learning with Verifiable Rewards, RLVR]
---

# RLVR — Reinforcement Learning with Verifiable Rewards

Training setting mà reward đến từ **automatic verifier** (unit test, math equality check, theorem prover). Current standard cho post-training LLM trên code, math, reasoning.

Paper [[src_hubotter2026_self_distillation]] position [[ent_rlrf]] như generalization của RLVR; [[ent_sdpo]] là algorithm instantiate RLRF.

## Properties

- ✅ Ground-truth reward, không cần preference data hay RM.
- ❌ Signal ở outcome level → [[con_credit_assignment]] yếu.
- ❌ Sample-inefficient trên hard task.
- ❌ Khi cả group rollout cùng 0 reward → [[ent_grpo]] advantage collapse → stall.
- ❌ Outcome reward = information bottleneck che state (paper Figure 2).

## Landscape RLVR

Các algorithm chủ đạo:
- [[ent_grpo]] (Shao et al. 2024 / DeepSeek): group-relative MC advantage.
- STaR (Zelikman et al. 2022): iterative self-improvement với MC reward.
- Variants: REINFORCE++, RLOO, Dr.GRPO.
- PPO-based với clipped importance sampling cho off-policy.

## Tại sao thesis vẫn quan tâm

- Test-time SDPO cần GRPO làm reference — so sánh behavior.
- RQ2 đặt câu hỏi liệu [[con_epistemic_verbalization]] được preserve tốt hơn trong RLVR (scalar only) vs RLRF (rich feedback) không.

## Liên hệ với [[ent_rlrf]]

RLRF strictly generalize: RLVR = RLRF với `f = tokenize(r)`. Paper chứng minh ngay cả không có rich feedback thật (§3), dùng **successful rollout làm feedback proxy** cho failed rollouts cũng giúp SDPO > GRPO.
