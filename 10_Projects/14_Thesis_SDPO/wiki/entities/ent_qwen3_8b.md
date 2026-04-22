---
type: entity
created: 2026-04-22
updated: 2026-04-22
tags: [model, base-model, qwen]
sources: [src_hubotter2026_self_distillation, src_kim2026_why_self_distillation_degrades]
aliases: [Qwen3-8B]
---

# Qwen3-8B

Base model (8B params) của Qwen3 family (Yang et al. 2025a / Alibaba). Dùng làm **default checkpoint** cho experiments SDPO trên [[ent_livecodebench]] và là base model mặc định của thesis.

## Vì sao paper (và thesis) chọn Qwen3-8B

- In-context learning ability đủ mạnh để self-teaching work (§4.1 scaling study).
- SDPO gain nổi bật nhất ở scale này trong Qwen3 family:
  - Qwen3-0.6B, 1.7B, 4B: SDPO ~= GRPO (marginal).
  - **Qwen3-8B**: SDPO >> GRPO (48.8% vs 41.2% trên LCBv6).
- Có sẵn public checkpoint và tương thích với verl training framework.

## Dùng ở đâu trong thesis

- **Component A** (RQ1): base model cho 7 template variants × test-time SDPO ablation.
- **Component C** (RQ2): measure uncertainty signal evolution qua iterations.
- **Component D** (RQ3): teacher entropy stopping heuristic.

## Checkpoint variants liên quan

- Qwen3-8B (base) — scope hiện tại của thesis.
- Qwen3-8B + math-SDPO (bởi beanie00) — potential cross-domain checkpoint cho **Component B** (RQ2 bonus).
- Qwen3-8B + GRPO → reference cho behavior comparison.

## Practical

- Context length default 40k tokens (§5 multi-turn baseline dùng sliding window 32k).
- Multi-GPU training dùng verl library, 4× NVIDIA GH200 trong paper setup.

## Behavior under SDPO (Kim et al. 2026 findings)

[[src_kim2026_why_self_distillation_degrades]] test Qwen3-8B hai chế độ:

### Thinking Mode: ON (§5.2)
- Base response rất dài (~10k tokens) + nhiều epistemic tokens.
- GRPO và SDPO đều giảm length + epistemic, nhưng **SDPO aggressive hơn**.
- AIME24 OOD: SDPO `c=s` falls below base; `c=s\think` degrade progressive.
- Insight: base Qwen3-8B "over-express" uncertainty → GRPO trim OK, SDPO trim too much.

### Thinking Mode: OFF (§5.3)
- Base response ngắn hơn, performance thấp hơn.
- **GRPO tự tăng** epistemic verbalization → training score 0.4 → 0.8.
- SDPO giảm length, training improve chậm, AIME24 slight drop (0.25 → 0.23).
- → GRPO dùng epistemic verbalization như tool để improve; SDPO triệt tiêu tool đó.

### Thesis implication
- Thesis đang planning dùng Qwen3-8B (mode chưa specify trong proposal).
- **Quyết định mode = quyết định baseline epistemic density** → ảnh hưởng signal-to-noise để measure suppression ở RQ2.
- Recommendation: thesis fix **Thinking ON** cho hard code (matching Hübotter §5 setup LCBv6) nhưng note explicitly.

## Gaps

- Chưa ingest Qwen3 technical report → rename to `src_yang2025_qwen3` sau.
- Chưa có deep dive về chat template, stop tokens, sampling params default.
- Thinking ON/OFF behavior trên **code** (vs math Kim đã test) chưa có data.
