---
type: entity
created: 2026-04-22
updated: 2026-04-22
tags: [model, base-model, olmo]
sources: [src_hubotter2026_self_distillation]
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

## Gaps

- Chưa ingest Olmo3 tech report. Open source nên có thể access checkpoint và paper.
