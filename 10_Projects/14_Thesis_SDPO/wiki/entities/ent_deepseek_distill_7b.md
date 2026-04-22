---
type: entity
created: 2026-04-22
updated: 2026-04-22
tags: [model, reasoning-model, deepseek]
sources: [src_kim2026_why_self_distillation_degrades]
aliases: [DeepSeek-R1-Distill-Qwen-7B, DS-R1-Distill-7B]
---

# DeepSeek-R1-Distill-Qwen-7B

Checkpoint 7B distilled từ DeepSeek-R1 (Guo et al. 2025) xuống Qwen-7B base. Strong reasoning model với **high baseline epistemic verbalization**.

## Đặc điểm quan trọng

- **Thinking tag built-in**: response bao trong `<think>...</think>`.
- **Verbose**: response length base ~13,000 tokens trên DAPO-Math questions.
- **High epistemic density**: 182.5 epistemic tokens/response (unguided, §3 Table 1).
- Reasoning performance mạnh base: AIME24 54.79, MATH500 92.19.

## Primary model trong Kim et al. 2026

[[src_kim2026_why_self_distillation_degrades]] dùng làm primary model vì:
- Epistemic baseline cao → có space để measure suppression.
- Strong reasoning → degradation khi suppress rõ ràng.

### Kết quả chính trên model này

**SFT (§4, Table 2)**:
- `D_ug` (unguided correct): AIME24 51.0 (≈ base 54.8).
- `D_sg` (solution-guided correct): AIME24 **20.2** (drop 40%).

**On-policy (§5.1, Figure 3)**:
- GRPO: AIME24 54.7 → 56.0 (modest gain).
- SDPO `c=s`: **drop 40% AIME24, 15% AMC23**.
- SDPO `c=s\think`: drop attenuated but still below base.
- Epistemic token changes on AIME24: `wait` -60.8, `maybe` -17.1, `perhaps` -17.1.

**Teacher regime (§5.4, Figure 6)**:
- SDPO EMA 0.0 > SDPO EMA 0.05 (fixed teacher better).

## Thesis relevance

### Option: secondary model
- Base model default của thesis vẫn là [[ent_qwen3_8b]].
- DS-R1-Distill-7B có thể dùng làm **third model** cho RQ2 robustness check:
  - High epistemic baseline → signal-to-noise cao nhất để detect suppression.
  - Paper Kim đã đo baseline → thesis có reference numbers.

### Gap để thesis fill
- Kim et al. test DS-R1-Distill-7B ở train-time math.
- Thesis test (potentially) ở **test-time code**: LCBv6 behavior chưa có data.
- DS-R1-Distill-7B có được train trên code data không? → cần check, ảnh hưởng validity.

## Links

- [[src_kim2026_why_self_distillation_degrades]]
- [[con_epistemic_verbalization]] (đo nhiều nhất trên model này)
- [[ent_qwen3_8b]] · [[ent_olmo3_7b_instruct]]

## Gaps

- Chưa ingest DeepSeek-R1 paper (Guo et al. 2025, arXiv:2501.12948).
- Chat template / stop tokens specifics chưa document.
