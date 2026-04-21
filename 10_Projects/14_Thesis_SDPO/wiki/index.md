---
type: index
updated: 2026-04-22
---

# Thesis SDPO — Wiki Index

Catalog of all wiki pages. Read this first when answering queries.

## Synthesis

- [[../SDPO 2026-04-11|thesis_proposal_2026-04-11]] — thesis proposal: RQs, contributions, components A–D. *(not yet migrated to `wiki/synthesis/`)*

## Sources (1)

- [[src_hubotter2026_self_distillation]] — Hübotter et al. 2026, arXiv:2601.20802. Origin paper của SDPO. **Full-PDF ingest** (50 pages, §1–§7 + appendices).

## Entities (6)

- [[ent_sdpo]] — Self-Distillation Policy Optimization, method trung tâm của thesis.
- [[ent_grpo]] — Group Relative Policy Optimization, baseline và hybrid với SDPO.
- [[ent_rlvr]] — Reinforcement Learning with Verifiable Rewards (baseline setting).
- [[ent_rlrf]] — Reinforcement Learning with Rich Feedback (paradigm của SDPO).
- [[ent_livecodebench]] — competitive programming benchmark (v6 hard / very-hard).
- [[ent_qwen3_8b]] — base model chính cho experiments.
- [[ent_olmo3_7b_instruct]] — secondary model (chemistry 6× speedup result).

## Concepts (6)

- [[con_rich_feedback]] — textual / structured training signal vượt khỏi scalar reward.
- [[con_self_teacher]] — model conditioned on feedback làm internal teacher.
- [[con_credit_assignment]] — bài toán per-token attribution mà SDPO densify (3-level ablation).
- [[con_reprompt_template]] — prompt format cho self-teacher. **Trung tâm RQ1.**
- [[con_test_time_self_distillation]] — TTT-SDPO regime §5. **Scope của toàn thesis.**
- [[con_discovery_at_k]] — metric đo discovery time; extend thành CTC (RQ3).

## Still planned (from thesis proposal)

**Concepts**
- `con_epistemic_verbalization` — uncertainty language in generations (Kim et al. 2026)
- `con_uncertainty_suppression` — the suppression phenomenon itself (RQ2)
- `con_ctc_metric` — compute-to-correct tradeoff (RQ3, extend discovery@k)
- `con_teacher_entropy_stopping` — proposed early-stop heuristic (Component D)
- `con_code_uncertainty_signals` — try/except, assert, defensive branching as markers
- `con_teacher_regularization` — EMA / trust-region để tránh teacher collapse

**Entities**
- `ent_deepseek_distill_7b` — comparison checkpoint

**Sources**
- `src_kim2026_ood_reasoning` — epistemic verbalization suppression finding (cited in proposal)
- `src_livecodebench` — LCB origin paper (contamination protocol details)
