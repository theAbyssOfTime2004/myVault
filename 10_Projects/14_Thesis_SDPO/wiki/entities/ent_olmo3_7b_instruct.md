---
type: entity
created: 2026-04-22
updated: 2026-04-22
tags: [model, base-model, olmo]
sources: [src_hubotter2026_self_distillation, src_kim2026_why_self_distillation_degrades]
aliases: [Olmo3-7B-Instruct]
---

# Olmo3-7B-Instruct

Instruction-tuned model 7B params từ AllenAI (Olmo et al. 2025). Dùng làm **second base model** trong [[src_hubotter2026_self_distillation]] §3 cho science reasoning và tool use experiments.

## Key result với SDPO

- Trên Chemistry (SciKnowEval L3), Olmo3-7B-Instruct + SDPO đạt accuracy 5h-GRPO chỉ trong **50 phút → 6× wall-clock speedup**.
- Response length **11× ngắn hơn** GRPO trên cùng task.
- Final 5h accuracy hơn GRPO >10 percentage points.

## Thesis relevance

- Chưa phải base model default của thesis (đã chọn [[ent_qwen3_8b]]).
- Có thể dùng làm **secondary** cho generalization test ở Component A (RQ1), nếu compute cho phép.
- Hữu ích để confirm behavior của template không phải chỉ Qwen-specific.

## Counterpoint từ Kim et al. 2026

Chemistry 6× speedup (Hübotter §3) có context quan trọng từ [[src_kim2026_why_self_distillation_degrades]]:

- SciKnowEval Chemistry = **6 problem types** cố định, 2,400 questions toàn variant bề mặt.
- Theo framework [[con_task_coverage]]: narrow → suppression không hurt, thậm chí giúp.
- Kim et al. test Olmo3-7B-Instruct ở Appendix D.2, confirm behavior tương tự DS-R1-Distill-7B trên math.

→ 6× speedup **không phải chiến thắng phổ quát của SDPO** — nó là artifact của task coverage hẹp. Thesis trên LCBv6 hard/very-hard cũng là narrow coverage, nên expect SDPO win tương tự ở accuracy nhưng phải check suppression.

## Gaps

- Chưa ingest Olmo3 tech report. Open source nên có thể access checkpoint và paper.
- Appendix D.2 của Kim paper chưa đọc sâu — có numbers chi tiết cho Olmo3 trên AIME.
