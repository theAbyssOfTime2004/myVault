---
type: report
tags: [report, chapter, limitations, future, bestcase]
---

# Chapter 6 — Limitations and Publication Roadmap

> **‡ Best-case / projected draft.** This chapter shows how the limitations of the current real draft are resolved, and what remains.

## 6.1 Limitations resolved relative to the current draft

The full study addresses the main limitations of the current real draft:

- **Statistical power.** Medium scale (≈16 problems × 6 seeds) and a Wilcoxon signed-rank test replace the crude $0.5^k$ sign test, so the main effect is reported with controlled error rather than as a directional signal (§4.2).
- **Compute matching.** A matched-budget comparison and a compute-to-correct frontier replace the outcome-only result, so the advantage is shown to be compute-fair, not a sampling-volume artifact (§4.2.5).
- **RQ2 thinness.** Running the code arm with thinking ON produces reasoning traces on the domain where the method works, turning the epistemic question from a confounded math-only pilot into a measured result (§4.5).
- **The fallback.** Removing the keep-best-correct fallback makes the leak filter exact; the judge is never silently overridden (§4.4, §4.7).
- **The model and reference confounds.** Using the same reasoner on both domains and supplying MATH-500 worked solutions isolates the cause of the math non-escape and validates the value-versus-procedure boundary (§4.6).

## 6.2 Limitations that remain even in the best case

Honesty requires naming what more compute and time do *not* fix:

- **One model family, one scale.** All results are on a 4B-scale Qwen model at a personal compute scale. The findings are an empirical characterization in one setting, not a universal law, and not an industry-scale evaluation.
- **Effect size under scale.** A stronger model (8B and up) is expected to escape more on its own, so the teacher-first margin should *narrow*; the effect is expected to be most pronounced on models weak enough to stall unaided. Best case means the effect is well-measured and compute-fair, not necessarily large.
- **Reward shape vs reference content.** Code is both graded and method-bearing while answer-only math is both binary and value-only; even with MATH-500 these two factors co-vary unless a graded math reward (or an answer-only code task) is constructed.
- **Generalization of the epistemic result.** The suppression measurement is on one model with one marker lexicon; its generality across models and reasoning styles is untested.

## 6.3 Publication roadmap

The work is positioned for a conference submission a few months after graduation. The path: (1) run the medium-scale matched comparison and the compute-to-correct frontier (the headline result); (2) run the thinking-on code arm for the epistemic-suppression measurement; (3) run MATH-500 with worked-solution references and the same reasoner to validate the boundary; (4) scale to 8B to characterize how the margin changes with model strength; (5) extend to a second code benchmark to test cross-benchmark robustness. Steps 1–3 are the minimum for a paper; steps 4–5 strengthen it. Each is sized to a personal compute budget rather than an industry one.
