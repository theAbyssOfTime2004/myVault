---
type: entity
created: 2026-04-22
updated: 2026-04-22
tags: [method, rl, self-distillation]
sources: [src_hubotter2026_self_distillation]
aliases: [Self-Distillation Policy Optimization, SDPO]
---

# SDPO — Self-Distillation Policy Optimization

Phương pháp RL post-training được giới thiệu trong [[src_hubotter2026_self_distillation]]. Cơ chế cốt lõi: model khi được condition trên textual feedback đóng vai trò *internal teacher*; retrospective predictions của nó được distill ngược về unconditioned policy.

## Vì sao cần SDPO

Giải quyết điểm yếu [[con_credit_assignment]] của [[ent_rlvr]]: outcome-only reward quá sparse để train hiệu quả trên code/math. SDPO biến [[con_rich_feedback]] thành per-token supervision bằng cách tận dụng khả năng [[con_self_teacher]] của chính model.

## Tính chất chính

- **Self-teacher** — không cần external teacher hay reward model riêng.
- **Consumes [[con_rich_feedback]]** — textual, không phải scalar.
- **Dense signal** — per-token, không phải per-episode.

## Train-time vs test-time (quan trọng với thesis)

| | Train-time SDPO (Hübotter 2026) | Test-time SDPO (scope thesis) |
|---|---|---|
| Cái gì di chuyển? | Weights | Không gì cả — model frozen |
| Dùng signal thế nào? | Gradient update | Iterated reprompting lúc inference |
| RQs của thesis | Background | RQ1 (templates), RQ2 (suppression), RQ3 (CTC) |

Phân biệt này là lằn ranh của thesis — origin paper làm train-time, thesis làm test-time và nghiên cứu behavior chứ không train weights.

## Known results (từ origin paper)

- ≥ RLVR baselines trên: scientific reasoning, tool use, competitive programming.
- 3× sample efficiency vs best-of-k trên hard tasks.
- Eval trên [[ent_livecodebench]].

## Open questions (thesis)

- Train-time SDPO có suppress [[con_epistemic_verbalization]] không? (Kim et al. 2026 nói có trên math; replication trên code chưa ai làm.)
- Test-time SDPO có cùng hiện tượng suppression đó không? → thesis **RQ2**.
- Biến thể [[con_reprompt_template]] nào giúp / làm tệ hơn? → thesis **RQ1**.
- [[con_ctc_metric]] thay đổi ra sao giữa các template? → thesis **RQ3**.
