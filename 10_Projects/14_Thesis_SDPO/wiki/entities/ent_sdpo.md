---
type: entity
created: 2026-04-22
updated: 2026-04-22
tags: [method, rl, self-distillation]
sources: [src_hubotter2026_self_distillation]
aliases: [Self-Distillation Policy Optimization, SDPO]
---

# SDPO — Self-Distillation Policy Optimization

RL post-training method introduced in [[src_hubotter2026_self_distillation]]. Core mechanism: the model, conditioned on textual feedback, acts as an internal teacher; its retrospective predictions are distilled back into the unconditioned policy.

## Why it exists

Solves the [[con_credit_assignment]] weakness of [[ent_rlvr]]: scalar outcome rewards are too sparse for efficient RL on code/math. SDPO turns textual feedback into dense per-token supervision using the model's own [[con_self_teacher]] capability.

## Key properties

- **Self-teacher** — no external teacher or reward model required.
- **Consumes [[con_rich_feedback]]** — textual, not scalar.
- **Dense signal** — per-token, not per-episode.

## Train-time vs test-time (important for thesis)

| | Train-time SDPO (Hübotter 2026) | Test-time SDPO (thesis scope) |
|---|---|---|
| What moves? | Weights | Nothing — frozen model |
| Signal use | Gradient updates | Iterated reprompting at inference |
| Thesis RQs | Background | RQ1 (templates), RQ2 (suppression), RQ3 (CTC) |

## Known results (from origin paper)

- ≥ RLVR baselines on: scientific reasoning, tool use, competitive programming.
- 3× sample efficiency vs best-of-k on hard tasks.
- Evaluated on [[ent_livecodebench]].

## Open thesis questions

- Does train-time SDPO suppress [[con_epistemic_verbalization]]? (Kim et al. 2026 says yes for math; replication on code pending.)
- Does test-time SDPO exhibit the same suppression? → thesis RQ2.
- Which [[con_reprompt_template]] variants help or worsen it? → thesis RQ1.
- How does [[con_ctc_metric]] behave across template variants? → thesis RQ3.
