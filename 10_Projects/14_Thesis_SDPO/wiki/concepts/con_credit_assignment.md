---
type: concept
created: 2026-04-22
updated: 2026-04-22
tags: [rl, signal, credit-assignment]
sources: [src_hubotter2026_self_distillation]
---

# Credit assignment (RL)

The problem of determining which tokens/actions in a trajectory were responsible for the final reward. Core difficulty of RL; made especially hard by sparse/outcome-only rewards.

## Why it matters for code / math

A correct solution may span dozens of reasoning tokens — which ones mattered? Outcome reward doesn't say. Poor credit assignment → sample-inefficient training → slow learning, noisy gradients.

## [[ent_rlvr]] weakness

Verifiable rewards are binary at episode level. Every token shares the same scalar signal, so the gradient has no per-token discrimination.

## How [[ent_sdpo]] sidesteps it

Converts [[con_rich_feedback]] into per-token signals via the [[con_self_teacher]]. The densified signal gives implicit credit assignment without changing the verifier.

## Links

- [[src_hubotter2026_self_distillation]] — motivation and proposed fix.
