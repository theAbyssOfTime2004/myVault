---
source_type: arxiv_paper
clipped: 2026-04-22
url: https://arxiv.org/abs/2601.20802
pdf: https://arxiv.org/pdf/2601.20802
arxiv_id: 2601.20802
---

# Reinforcement Learning via Self-Distillation

Hübotter, Lübeck, Behric, Baumann, Bagatella, Marta, Hakimi, Shenfeld, Kleine Buening, Guestrin, Krause. arXiv:2601.20802 — submitted 2026-01-28, revised 2026-02-16.

> NOTE: Current clip is metadata + abstract + contribution summary only (via WebFetch on arxiv abstract page). Full PDF not yet downloaded to this folder. To deepen the wiki source page, download the PDF here and re-run ingest.

## Abstract (paraphrased)

RL in verifiable-reward domains (code, math) suffers from poor credit assignment because scalar outcome rewards provide sparse signals. The paper proposes **Self-Distillation Policy Optimization (SDPO)**, which transforms tokenized textual feedback into dense learning signals. Instead of requiring an external teacher or reward model, SDPO leverages the model's own capability to recognize mistakes when conditioned on feedback — the model conditioned on feedback acts as an internal teacher whose retrospective predictions are distilled back into the unconditioned policy.

## Key contributions (from abstract)

1. Formalizes "RL with rich feedback" as a new problem setting beyond scalar rewards.
2. SDPO method — converts tokenized textual feedback into training signals via self-teaching.
3. Empirical improvement over RLVR baselines on scientific reasoning, tool use, competitive programming.
4. 3× efficiency vs best-of-k on difficult tasks.

## Named entities

- **Method**: SDPO (Self-Distillation Policy Optimization)
- **Setting**: RLVR (Reinforcement Learning with Verifiable Rewards)
- **Benchmark**: LiveCodeBench v6
