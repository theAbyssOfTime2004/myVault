---
type: report-planning
created: 2026-06-26
updated: 2026-06-26
tags: [report, planning, argument-blueprint, cer, introduction]
sources: [syn_report_outline, syn_core_result, syn_math_pilot, src_hubotter2026_self_distillation]
---

# Argument Blueprint — Chapter 1 (Introduction)

Phase 3 artifact for the Introduction. Focus: calibrated contribution claims, each with evidence + counter + rebuttal. The deep mechanism argument lives in Ch5; here the job is to state contributions at the strength the data supports.

## Central thesis (paper-level)

A teacher-first organization of execution-guided self-distillation **accelerates test-time discovery in complex code generation**: it escapes the flat-reward trap that stalls on-policy SDPO on hard problems, and the regime where it helps is characterized by whether the privileged reference encodes an in-reach method rather than only a value.

## Research questions

- **RQ-method**: At test time, does teacher-first (distill filtered teacher generations) beat student-first (distill the student's own failed rollout) at discovering solutions to hard code problems?
- **RQ1**: Does the reprompt-template formulation of the execution feedback affect discovery, and in which regime?
- **RQ2 (epistemic)**: Does self-distillation from rich context suppress epistemic verbalization at test time? (Thin: only the math pilot carries trace data.)
- **RQ3 (efficiency)**: How does discovery trade off against compute (compute-to-correct)? (Largely future work; outcome-only here.)

## Contributions (claims, calibrated)

### C1 — A teacher-first variant of execution-guided self-distillation
- **Evidence**: method (Ch3), implemented as a custom loop distilling verifier+judge-filtered teacher trajectories.
- **Counter**: it is a variant, not a new algorithm.
- **Rebuttal (concede-and-limit)**: framed as a variant positioned between SDPO and SFT, not as a new paradigm.
- **Strength**: Strong (it is a clear, implemented method contribution).

### C2 — Empirical evidence that teacher-first accelerates discovery where on-policy SDPO stalls
- **Evidence**: 8/8 matched TF≥SF; escape-zero replicated ×3; idx64 TF 0.422 vs SF 0.047 (§4.2).
- **Counter**: small n; not compute-matched (~2.5× generations).
- **Rebuttal (concede-and-limit)**: stated as weak/directional dominance with escape-zero as the sharp signal; compute deferred to RQ3.
- **Strength**: Strong on escape-zero, Moderate overall.

### C3 — The reprompt-template formulation of execution feedback affects discovery
- **Evidence**: monotone T5 > T2 > T1 on the hard problem (§4.3).
- **Counter**: 2 seeds, SF arm only, small absolute counts.
- **Rebuttal (acknowledge-as-limitation)**: directional; template × teacher-first interaction untested.
- **Strength**: Moderate.

### C4 — A value-versus-procedure boundary characterization
- **Evidence**: code escapes; answer-only AIME math does not (2/2), with measured ~75% copy and form-not-substance traces (§4.5, §5.3).
- **Counter**: math n=2 with a model + reference confound.
- **Rebuttal (acknowledge + reframe)**: presented as boundary characterization with one falsifiable prediction (MATH-500 method-reference), not as a domain law.
- **Strength**: Moderate.

## Logical flow (Introduction)

Background (test-time compute; sparse RLVR reward; SDPO and rich feedback) → problem (discovery stalls on hard code; how to formulate and organize execution feedback) → RQs → contributions (C1–C4) → scope (TTT, LoRA, code core / math pilot) → thesis structure.

## Weak-indicator check

- No overclaiming: every contribution carries its counter and a concede/acknowledge rebuttal.
- Single-context generalization (math n=2) flagged in C4.
- No false dichotomy (teacher-first is positioned on a spectrum, not as the only option).

## Notes for the draft

- Lead the opening with the title's verb: *accelerate test-time discovery … via execution-guided self-distillation*.
- Keep contribution bullets calibrated; no "we prove."
- Name the boundary (C4) as a strength of the work, not as a failed math experiment.
