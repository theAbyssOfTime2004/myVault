---
type: concept
created: 2026-04-22
updated: 2026-04-22
tags: [test-time, discovery, core-thesis]
sources: [src_hubotter2026_self_distillation]
aliases: [Test-Time Self-Distillation, TTT-SDPO, test-time SDPO]
---

# Test-Time Self-Distillation (TTT-SDPO)

Regime đặc biệt của [[ent_sdpo]] được giới thiệu ở §5 paper: model chỉ có **1 câu hỏi khó duy nhất** và phải discover solution càng nhanh càng tốt. Weights update **riêng cho câu đó**, không nhằm generalization.

Đây là **regime scope của thesis**. Mọi RQ (1/2/3) đều sit trong test-time setting này.

## Setting formal

- Input: 1 question `x` (hard, binary reward).
- Goal: minimize **discovery time** — số attempts cho đến khi có 1 solution đúng.
- Metric: [[con_discovery_at_k]] = P(discover trong k attempts).

## Vì sao RLVR không work ở đây

Binary reward = 0 cho đến lần đầu solve → advantage = 0 → không có signal. [[ent_rlvr]] chỉ bắt đầu học *sau khi* đã solve ít nhất 1 lần.

[[ent_rlrf]] (qua SDPO) **nhận feedback mỗi attempt kể cả fail** → bootstrap từ zero success.

## Mechanism (Figure 12 của paper)

Thay vì concat history vào context (multi-turn), TTT-SDPO:

```
Iteration k:
  y_k ~ π_θ_k(· | x)
  f_k = env(y_k)
  θ_{k+1} = SDPO_step(θ_k, x, y_k, f_k)
```

"Compress" interaction history `(y_1, f_1, ..., y_k, f_k)` **vào weights** qua self-distillation. Tránh context window limit (transformer memory bottleneck).

Đây là insight conceptual mạnh: **context → weights** thông qua SDPO loss.

## Kết quả paper (§5.2, Figure 13)

Setup: LCBv6 hard (19 q, pass@64 < 0.5) + very-hard (9 q, pass@64 < 0.03). Qwen3-8B batch size 16.

| Metric | Best-of-k | Multi-turn | SDPO |
|---|---|---|---|
| Very-hard discovery@2750 | 41.5% | 35.6% | **53.2%** |
| Hard discovery@2750 | 72.3% | 68.4% | **78%** |
| Very-hard, to 22% discovery | baseline | baseline | **3× fewer** attempts |
| Hard, to 67% discovery | baseline | baseline | **2.4× fewer** attempts |

- Q3 (very-hard): chỉ SDPO solve được (attempt 321 ≈ 20 SDPO steps × batch 16).
- Multi-turn context limit hit ở step ~837 (hard), ~1007 (very-hard) → diminishing return.

## Observation quan trọng cho RQ2

Paper §5 không measure [[con_epistemic_verbalization]]. Nhưng có hint:

- Initial self-teacher accuracy **< 1%** trên hard questions, **= 0%** trên 78% của chúng.
- Tức là: ngay cả khi có feedback in-context, 1 shot không solve.
- Nhưng credit assignment vẫn đủ tốt → iterate và cuối cùng solve.

Câu hỏi RQ2 đặt ra: trong quá trình iterate, uncertainty language (try/except, "I'm not sure", "maybe") biến đổi thế nào? Có bị suppress giống Kim et al. 2026 observed ở train-time math không?

## Thesis RQs trong regime này

- **RQ1**: template variants nào giúp discovery nhanh hơn? Paper hint template không matter syntactically, nhưng macro structure chưa test.
- **RQ2**: uncertainty suppression xảy ra ở test-time không? Paper không trả lời.
- **RQ3**: [[con_ctc_metric]] (compute vs correctness) cho mỗi template. Paper chỉ đo discovery@k raw count.

## Hyperparameters paper dùng (reference cho thesis)

- Batch size 16 (ablation Figure 19: marginal differences 1/8/16).
- Regularized teacher (EMA hoặc trust-region) — critical.
- 2750 generations budget per question.
- 5 random seeds per question.

## Links

- [[ent_sdpo]] · [[con_discovery_at_k]] · [[ent_livecodebench]] · [[con_reprompt_template]]
