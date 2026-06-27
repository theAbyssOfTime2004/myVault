---
type: report
created: 2026-06-26
updated: 2026-06-26
tags: [report, chapter, limitations, future-work, confounds]
sources: [syn_report_outline, syn_core_result, syn_math_pilot, src_kim2026_why_self_distillation_degrades]
---

# Chapter 6 — Limitations and Future Work

The results of this thesis are preliminary and directional. This chapter states the limitations plainly and then lays out the experiments that would address them, organized so that each future experiment isolates a confound named in the discussion.

## 6.1 Limitations

### 6.1.1 Statistical power and scope

The central results rest on small samples: two to three code problems for the escape results, two seeds per template for RQ1, and two problems for the math pilot. Every significance value reported is a crude sign test of the form $0.5^k$ over non-tied matched pairs, which is a descriptive summary, not an inferential test with controlled error rates. The main matched comparison (§4.2.2) and the hard-frontier extension (§4.2.3) also share problem idx39, so their sign-test values are not independent and were never combined. The honest characterization of the main effect is weak dominance: teacher-first is never worse and is often better, but ties are common and the large margins are seed-specific. The W&B export also shows that individual outcomes are **run-dependent**: re-runs of the same seed do not always reproduce the same value, and in particular a stuck-at-zero student-first escape-zero instance (§4.2.3) is not reproduced by every re-run of that seed (Appendix E.3). Aggregate means are stable, but single-seed anecdotes such as a specific escape-zero event should be read as observed instances, not guaranteed outcomes. None of this supports a universal claim; it supports a directional one on one 4B model, one anchor template, and a 15-step budget.

### 6.1.2 The math confounds

The math pilot's non-escape carries two confounds that prevent attributing it to the domain. First, a model confound: code uses Qwen3-4B while math uses Gemma-4-E4B, so the math runs use a different and, on AIME, weaker reasoner. Second, a reference confound: AIME provides only a numeric answer, and the privileged context is hard-coded to return that answer, so the teacher has nothing method-bearing to distill. Either confound alone could produce the observed non-escape. The math result is therefore reported as a boundary characterization, not as a property of mathematics as a domain.

### 6.1.3 Judge reliability on beyond-capability problems

The independence judge degrades exactly where the problems are hardest. On the AIME too-hard problems, the LLM judge catches blatant copying but cannot reliably separate a genuine derivation from an answer-directed confabulation, because both reach the correct number (§4.5.3). The `is_copy` label is thus not fully trustworthy in the beyond-capability regime, which is also the regime where the leak measurement matters most. The 75% copy rate should be read as a lower bound on copying rather than an exact figure.

### 6.1.4 The fallback can defeat the judge

The keep-best-correct fallback, which prevents an empty good pool on a cold start, can override the judge it is meant to support. In the idx8 log (run 463y4fjr) every verdict was `is_copy=true`, so the single trajectory kept as good each step came entirely from the fallback, meaning the good pool was made of copies the judge had already rejected (§4.5.3). The anti-leak filter therefore holds only when the teacher produces at least one genuine, independent solution. When the teacher produces nothing but copies, the filter is silently bypassed.

### 6.1.5 No compute matching

Teacher-first draws roughly 2.5× more generations per step than student-first (`teacher_n=10` versus four). The thesis therefore demonstrates an outcome advantage, not a compute advantage. A fair comparison requires a compute-to-correct view that holds total generation budget fixed, which was not run. The escape-zero events argue that volume alone does not explain the gap (§5.1), but they do not settle the compute question.

### 6.1.6 RQ2 is thin, and forgetting is unmeasured

The epistemic dimension (RQ2) has little data. The code runs use thinking OFF and so produce no reasoning trace to analyze, leaving the math traces as the only RQ2 evidence, and those come from the confounded pilot. Catastrophic forgetting at test time was also not measured; the per-problem reset prevents cross-problem contamination, but a cumulative regime was never tried.

## 6.2 Future Work

The future experiments are ordered by how directly they would resolve the limitations above.

### 6.2.1 Remove the model confound (priority)

The single most informative next experiment is to run Qwen3-4B with thinking ON on *both* code and math. This uses the same reasoner that already escapes on code and asks whether escape appears on math once the model is held fixed. It directly separates the model confound from the reference confound of §6.1.2: if the same reasoner still fails on answer-only math, the reference, not the model, is implicated.

### 6.2.2 Scale to a stronger model

Running Qwen3-8B with thinking could move AIME problems that are currently beyond-capability into the reachable band, where escape becomes possible. This is the strongest lever for flipping the math null. It also tests a prediction that cuts the other way: as the model strengthens, student-first escapes more often on its own, so the teacher-first margin should *narrow*. The escape-zero effect is expected to be sharpest with a model weak enough to stall on its own, and a positive 8B result would likely come with a smaller gap, not a larger one.

### 6.2.3 A method-bearing reference for math

The value-versus-procedure claim (§5.3) makes a falsifiable prediction that this experiment would test. MATH-500 includes a `solution` field, so modifying the math privileged context to inject the worked solution rather than the bare answer would supply a method-bearing reference. If escape then appears on math, the reference, not the domain, was the obstacle, which is exactly what the value-versus-procedure view predicts.

### 6.2.4 Compute-to-correct and more seeds

Two quantitative extensions would strengthen the existing claims rather than open new ones. Logging total generations and reporting a compute-to-correct frontier (RQ3) would convert the outcome advantage of §4.2 into a compute-aware one. Adding problems and seeds, moving from 8-of-8 toward 16-of-16 matched comparisons, would raise the statistical power that §6.1.1 flags as the main weakness.

### 6.2.5 Open RQ2 on code

Running the code arm with thinking ON would, for the first time, produce reasoning traces on the domain where the method works, opening the epistemic-suppression question (RQ2) in a setting free of the math pilot's confounds. This would let the suppression analysis of Kim et al. [2] be applied where teacher-first actually accelerates discovery, rather than only where it stalls.
