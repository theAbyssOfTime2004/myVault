---
type: report
tags: [report, chapter, conclusion, bestcase]
---

# Chapter 7 — Conclusion

> **‡ Best-case / projected draft.** Conclusions stated as established here rest on the Chapter 4 projections (‡); the current real draft remains the factual baseline.

This thesis asked how to accelerate test-time discovery in complex code generation via execution-guided self-distillation. The method contribution is a teacher-first organization: the self-teacher generates trajectories under execution feedback, a verifier and a judge filter them for correctness and independence (with the fallback removed, so a copy is never distilled), and the student is distilled toward those filtered trajectories, between on-policy SDPO and off-policy SFT.

In the full study the empirical picture is strong and, importantly, compute-fair. On a medium matched evaluation teacher-first significantly outperforms student-first‡ and escapes the flat-reward trap on the hardest problems; at a matched generation budget, and on a compute-to-correct frontier, the advantage holds‡, so it is not a sampling-volume artifact. The reprompt-template formulation of the feedback affects discovery, most clearly on hard problems. With reasoning enabled, distillation from feedback-conditioned context measurably suppresses epistemic verbalization on code‡, and the meaning of that suppression turns out to be regime-dependent. Most decisively, holding the model fixed and supplying a method-bearing reference lets the model escape on math where an answer-only reference does not‡, validating the central value-versus-procedure boundary: escape requires the reference to encode an in-reach method, not merely a value.

Even in this best case the work is an empirical characterization in one model family at a personal compute scale, and a stronger model is expected to narrow the margin. But with the projected results in hand, the contribution is a compute-fair, mechanistically explained, and boundary-validated account of when execution-guided self-distillation accelerates test-time discovery — the form in which it is ready for publication. The immediate next step is to run the experiments this draft projects, and to report whichever way they fall.
