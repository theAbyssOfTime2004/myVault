---
type: report
created: 2026-06-26
updated: 2026-06-26
tags: [report, chapter, conclusion]
sources: [syn_report_outline, syn_core_result, syn_math_pilot]
---

# Chapter 7 — Conclusion

This thesis asked how to accelerate test-time discovery in complex code generation via execution-guided self-distillation, and in particular whether reorganizing the self-distillation update, and reformulating the execution feedback it draws on, helps a model discover solutions to hard problems faster.

The method contribution is a teacher-first organization of execution-guided self-distillation. Instead of distilling the student's own failed rollout, as on-policy SDPO does, it has the self-teacher generate trajectories under execution feedback, filters them for correctness and independence with a verifier and a judge, and distills the student toward those. This places the method between on-policy SDPO and off-policy SFT.

The empirical findings are preliminary and directional, bounded by small samples, one 4B model per domain, and a budget that was not compute-matched. Within those bounds they are consistent. On matched comparisons over hard code problems, teacher-first is at least as good as student-first on every seed and never worse, and on the hardest problems it escapes the flat-reward trap that keeps student-first stuck at zero, an escape-zero pattern replicated three times with one roughly ninefold improvement. The reprompt-template formulation of the execution feedback affects discovery, most clearly on hard problems, where a reasoning-inducing template orders above the plain anchor, which orders above a minimal one. The compute question is answered only in part: the teacher-first overhead is quantified, but a compute-matched Pareto comparison remains for future work.

The central finding is a boundary rather than a universal claim. A math pilot on answer-only AIME problems does not escape, and the way it fails is informative. The teacher copies the answer rather than deriving it, at a measured copy rate near 75%, and what transfers to the student is a confident reasoning style rather than a method, so the student stays at zero. Read together with the code results, this characterizes when execution-guided self-distillation accelerates discovery: the privileged reference must encode an in-reach method, not merely a correct value, and the capability must be reachable once the model is unblocked. In code, where the output is itself a method, this holds; in answer-only math, where the output is a value, it does not. This contrast, with leak measurable on math and null on code, says more about the mechanism than a result that worked everywhere would.

The most informative next step follows directly from the boundary. Running the same reasoner on both domains would separate the model from the reference as the cause of the math non-escape, and supplying a method-bearing reference, such as the worked solutions in MATH-500, would test the value-versus-procedure claim head-on. Together with a compute-to-correct comparison and larger samples, these would turn the directional results reported here into a firmer account of when, and at what cost, execution-guided self-distillation accelerates test-time discovery.
