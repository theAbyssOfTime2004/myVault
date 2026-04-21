---
type: entity
created: 2026-04-22
updated: 2026-04-22
tags: [model, base-model, qwen]
sources: [src_hubotter2026_self_distillation]
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

## Gaps

- Chưa ingest Qwen3 technical report → rename to `src_yang2025_qwen3` sau.
- Chưa có deep dive về chat template, stop tokens, sampling params default.
