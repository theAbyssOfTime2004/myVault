---
type: index
updated: 2026-04-22
---

# Thesis SDPO — Wiki Index

Catalog of all wiki pages. Read this first when answering queries.

## Synthesis

- [[../SDPO 2026-04-11|thesis_proposal_2026-04-11]] — thesis proposal: RQs, contributions, components A–D. *(not yet migrated to `wiki/synthesis/`)*

## Sources (3)

- [[src_hubotter2026_self_distillation]] — Hübotter et al. 2026, arXiv:2601.20802. Origin paper của SDPO. **Full-PDF ingest.**
- [[src_kim2026_why_self_distillation_degrades]] — Kim et al. 2026, arXiv:2603.24472. Paper critique SDPO về suppression of epistemic verbalization. **Full-PDF ingest.**
- [[src_kim2026_strategic_info_allocation]] — Kim et al. 2026 (original). Nguồn của epistemic verbalization concept. **STUB.**

## Entities (7)

- [[ent_sdpo]] — Self-Distillation Policy Optimization, method trung tâm của thesis.
- [[ent_grpo]] — Group Relative Policy Optimization, baseline và hybrid với SDPO.
- [[ent_rlvr]] — Reinforcement Learning with Verifiable Rewards (baseline setting).
- [[ent_rlrf]] — Reinforcement Learning with Rich Feedback (paradigm của SDPO).
- [[ent_livecodebench]] — competitive programming benchmark (v6 hard / very-hard).
- [[ent_qwen3_8b]] — base model chính cho experiments.
- [[ent_olmo3_7b_instruct]] — secondary model (chemistry 6× speedup result).
- [[ent_deepseek_distill_7b]] — high-reasoning checkpoint, primary test model của Kim et al.

## Concepts (9)

- [[con_rich_feedback]] — textual / structured training signal vượt khỏi scalar reward.
- [[con_self_teacher]] — model conditioned on feedback làm internal teacher (fixed vs moving regime).
- [[con_credit_assignment]] — bài toán per-token attribution mà SDPO densify.
- [[con_reprompt_template]] — prompt format cho self-teacher. **Trung tâm RQ1.**
- [[con_test_time_self_distillation]] — TTT-SDPO regime §5. **Scope của toàn thesis.**
- [[con_discovery_at_k]] — metric đo discovery time; extend thành CTC (RQ3).
- [[con_epistemic_verbalization]] — uncertainty tokens (wait/hmm/maybe...). **Core của RQ2.**
- [[con_uncertainty_suppression]] — hiện tượng SD suppress epistemic tokens. **Core RQ2.**
- [[con_task_coverage]] — modulating factor: narrow OK, broad harmful.

## Still planned (from thesis proposal)

**Concepts**
- `con_ctc_metric` — compute-to-correct tradeoff (RQ3, extend discovery@k)
- `con_teacher_entropy_stopping` — proposed early-stop heuristic (Component D)
- `con_code_uncertainty_signals` — try/except, assert, defensive branching as markers
- `con_teacher_regularization` — EMA / trust-region / fixed teacher comparison

**Sources**
- `src_livecodebench` — LCB origin paper (contamination protocol details)
- `src_yang2025_qwen3` — Qwen3 tech report
