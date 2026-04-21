---
type: entity
created: 2026-04-22
updated: 2026-04-22
tags: [rl, training-setting, verifiable-reward]
sources: [src_hubotter2026_self_distillation]
aliases: [Reinforcement Learning with Verifiable Rewards, RLVR]
---

# RLVR — Reinforcement Learning with Verifiable Rewards

Training setting where rewards come from an automatic verifier (unit tests, math equality check, theorem prover) rather than a learned reward model or human preferences. Current standard for post-training LLMs on code and math.

## Properties

- ✅ Ground-truth reward without RM training.
- ✅ No preference data collection.
- ❌ Scalar/outcome-only signal → weak [[con_credit_assignment]].
- ❌ Sample-inefficient on hard problems.

## Relation to [[ent_sdpo]]

SDPO is positioned in [[src_hubotter2026_self_distillation]] as a successor to RLVR: keeps the verifier-based setup but densifies the signal via [[con_rich_feedback]] and self-distillation.

## Where it appears

- [[src_hubotter2026_self_distillation]] — baseline to beat.
