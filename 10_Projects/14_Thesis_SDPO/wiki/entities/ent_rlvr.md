---
type: entity
created: 2026-04-22
updated: 2026-04-22
tags: [rl, training-setting, verifiable-reward]
sources: [src_hubotter2026_self_distillation]
aliases: [Reinforcement Learning with Verifiable Rewards, RLVR]
---

# RLVR — Reinforcement Learning with Verifiable Rewards

Training setting mà reward đến từ **automatic verifier** (unit test, math equality check, theorem prover) thay vì reward model học từ preference hoặc human feedback. Đây là tiêu chuẩn hiện tại để post-train LLM cho code và math.

## Tính chất

- ✅ Ground-truth reward — không cần train RM riêng.
- ✅ Không cần thu thập preference data.
- ❌ Signal chỉ ở outcome level → [[con_credit_assignment]] yếu.
- ❌ Sample-inefficient trên bài khó.

## Liên hệ với [[ent_sdpo]]

Trong [[src_hubotter2026_self_distillation]], SDPO được positioning như successor của RLVR: giữ verifier-based setup nhưng densify signal qua [[con_rich_feedback]] và self-distillation. Nói cách khác, RLVR không bị thay thế mà được *augment*.

## Xuất hiện ở đâu

- [[src_hubotter2026_self_distillation]] — baseline để beat.
