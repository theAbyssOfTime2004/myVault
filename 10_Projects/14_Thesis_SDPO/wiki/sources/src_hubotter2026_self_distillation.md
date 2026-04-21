---
type: source
created: 2026-04-22
updated: 2026-04-22
tags: [sdpo, rl, self-distillation, rlvr, code, origin-paper]
cite: "Hübotter et al., 2026"
arxiv: "2601.20802"
url: https://arxiv.org/abs/2601.20802
raw: raw/hubotter2026_sdpo.md
depth: abstract-only
---

# Hübotter et al. 2026 — Reinforcement Learning via Self-Distillation

**Authors**: J. Hübotter, F. Lübeck, L. Behric, A. Baumann, M. Bagatella, D. Marta, I. Hakimi, I. Shenfeld, T. Kleine Buening, C. Guestrin, A. Krause.

**arXiv**: [2601.20802](https://arxiv.org/abs/2601.20802) · submitted 2026-01-28 · revised 2026-02-16 · categories cs.LG, cs.AI.

**Status**: abstract-only ingest. Full PDF needs to be downloaded to [[raw/hubotter2026_sdpo]] and re-ingested for method/results depth.

## TL;DR

RLVR (scalar outcome reward) has weak credit assignment. SDPO densifies the signal by using the model-conditioned-on-feedback as an internal teacher, then distilling those retrospective predictions back into the unconditioned policy. No external teacher or reward model needed. Reported 3× efficiency over best-of-k on hard tasks.

## Problem setting

- Baseline: [[ent_rlvr]] (RL with Verifiable Rewards) — code/math post-training standard.
- Gap: outcome-only reward → sparse signal → poor [[con_credit_assignment]] → sample-inefficient training.

## Key contributions

1. Formalizes **"RL with rich feedback"** as a new problem setting beyond scalar rewards — see [[con_rich_feedback]].
2. **[[ent_sdpo]] method**: model conditioned on textual feedback acts as a [[con_self_teacher]]; its predictions are distilled into the base policy.
3. Empirical wins over RLVR across: scientific reasoning, tool use, competitive programming ([[ent_livecodebench]]).
4. **3× efficiency** vs best-of-k sampling on hard tasks.

## Method (high-level, pending PDF read)

SDPO treats `π(· | state, feedback)` as an internal teacher. Textual feedback conditions the model into producing better next-token predictions, which are then distilled back into `π(· | state)` via self-distillation. Signal becomes dense/per-token instead of sparse/per-episode.

## Results (pending PDF read)

- Scientific reasoning: ✅ (numbers pending)
- Tool use: ✅ (numbers pending)
- Competitive programming on [[ent_livecodebench]]: ✅ (numbers pending)
- 3× compute efficiency vs best-of-k on hard-split tasks.

## Relation to this thesis

- **Origin paper** for the SDPO method the thesis studies.
- Thesis RQ1 explores **test-time** variants of SDPO (reprompt templates) — this paper covers the **train-time** case.
- Thesis RQ2 asks whether the Kim et al. 2026 uncertainty-suppression finding transfers to test-time SDPO on code — a phenomenon this paper does not directly examine.

## Open questions

- Exact distillation objective (KL? token cross-entropy? temperature?) — need PDF.
- Feedback format sensitivity — maps directly onto thesis's [[con_reprompt_template]] taxonomy.
- Does SDPO suppress [[con_epistemic_verbalization]]? (Not reported here; Kim et al. 2026 suggests yes in math domain.)

## Links

- Entities: [[ent_sdpo]] · [[ent_rlvr]] · [[ent_livecodebench]]
- Concepts: [[con_rich_feedback]] · [[con_self_teacher]] · [[con_credit_assignment]]
- Thesis proposal: [[../../SDPO 2026-04-11]]
