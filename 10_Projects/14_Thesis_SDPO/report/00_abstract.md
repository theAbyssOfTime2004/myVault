---
type: report
created: 2026-06-26
updated: 2026-06-26
tags: [report, abstract]
sources: [syn_core_result, syn_math_pilot, syn_report_outline]
---

# Abstract

Test-time training lets a language model improve on a single hard problem at inference time, but on-policy self-distillation stalls when the model rarely produces a correct attempt to learn from. This thesis studies how to accelerate test-time discovery in complex code generation via *execution-guided self-distillation*, where execution feedback (failing tests, runtime errors) is the privileged context that drives the update. We propose a *teacher-first* organization: rather than distilling the student's own failed rollout, the self-teacher generates trajectories under feedback, a verifier and a judge filter them for correctness and independence, and the student is distilled toward those filtered trajectories, placing the method between on-policy SDPO and off-policy SFT. On matched comparisons over hard LiveCodeBench problems with a 4B model, teacher-first is at least as good as the student-first baseline on every seed and never worse, and on the hardest problems it escapes the flat-reward trap that keeps student-first stuck at zero, an escape-zero pattern replicated three times. The reprompt-template formulation of the feedback affects discovery, most clearly on hard problems. A math pilot on answer-only AIME problems does not escape, and its failure is informative: the teacher copies the answer (the judge flags most trajectories as copies, roughly four in five) and transfers reasoning style rather than method. Together these results characterize a boundary, escape requires the reference to encode an in-reach method rather than only a value. Findings are preliminary and directional, bounded by small samples and outcome-only (not compute-matched) comparisons.

**Keywords:** test-time training, self-distillation, code generation, execution feedback, discovery@k, information leak.
