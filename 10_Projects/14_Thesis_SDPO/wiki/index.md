---
type: index
updated: 2026-04-22
---

# Thesis SDPO — Wiki Index

Catalog of all wiki pages. Read this first when answering queries.

## Synthesis

- [[../SDPO 2026-04-11|thesis_proposal_2026-04-11]] — thesis proposal: RQs, contributions, components A–D. *(not yet migrated to `wiki/synthesis/`)*

## Sources (1)

- [[src_hubotter2026_self_distillation]] — Hübotter et al. 2026, arXiv:2601.20802. Origin paper của SDPO. *Abstract-only ingest; PDF đầy đủ còn chờ.*

## Entities (3)

- [[ent_sdpo]] — Self-Distillation Policy Optimization, method trung tâm của thesis.
- [[ent_rlvr]] — Reinforcement Learning with Verifiable Rewards (baseline setting).
- [[ent_livecodebench]] — competitive programming benchmark (v6 hard / very-hard).

## Concepts (3)

- [[con_rich_feedback]] — textual / structured training signal vượt khỏi scalar reward.
- [[con_self_teacher]] — model conditioned on feedback làm internal teacher.
- [[con_credit_assignment]] — bài toán per-token attribution mà SDPO densify.

## Still planned (from thesis proposal)

**Entities**
- `ent_grpo` — Group Relative Policy Optimization (comparison baseline)
- `ent_qwen3_8b` — base model for experiments
- `ent_deepseek_distill_7b` — comparison checkpoint

**Concepts**
- `con_epistemic_verbalization` — uncertainty language in generations (Kim et al. 2026)
- `con_uncertainty_suppression` — the suppression phenomenon itself
- `con_reprompt_template` — test-time prompting format variants (core of RQ1)
- `con_ctc_metric` — compute-to-correct tradeoff (RQ3)
- `con_teacher_entropy_stopping` — proposed early-stop heuristic (Component D)
- `con_code_uncertainty_signals` — try/except, assert, defensive branching as markers

**Sources**
- `src_kim2026_ood_reasoning` — epistemic verbalization suppression finding (cited in proposal)
- `src_livecodebench` — LCB origin paper (contamination protocol details)
