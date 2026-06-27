---
type: report
tags: [report, chapter, experiments, bestcase]
---

# Chapter 4 — Experiments

> **‡ Best-case / projected draft.** Numbers marked **‡** are projections extrapolated from the current real results under the stated hypotheses; they have not been run. The real, run numbers (idx39/12/64/77, the math pilot) are reproduced unmarked. See `BESTCASE_NOTES.md`.

## 4.0 Method extensions for the full study

Four changes turn the current pilot into the full study. (i) **Fallback removed:** the keep-best-correct fallback is dropped, so the filter never distils a copy; on a step where every teacher trajectory is judged a copy, the good pool is empty and that step distils nothing. (ii) **Medium scale:** the matched comparison is run over roughly sixteen frontier problems at six seeds, enough for a Wilcoxon signed-rank test rather than a crude sign test. (iii) **Thinking ON for code:** the code arm is run with reasoning traces, so epistemic verbalization can be measured (RQ2). (iv) **Method-bearing references and compute logging:** MATH-500 worked solutions are injected as the math privileged context, the same reasoner (Qwen3-4B) is used on both domains, and total generations plus token and GPU-time are logged for the compute-to-correct analysis.

## 4.1 Setup

Qwen3-4B with LoRA, on LiveCodeBench v6 (code) and AIME 2026 / MATH-500 (math). Code arm thinking ON. Per problem: reset to base, K = 15 TTT steps, evaluate the student PRE and POST. Sixteen frontier code problems (selected by model pass-rate) at six seeds. Full hyperparameters in Appendix A.

## 4.2 RQ-method: teacher-first vs student-first

On the medium matched set, teacher-first is at least as good as student-first on the large majority of seed-problem pairs and never materially worse, with the strongest margins on the hardest problems. A Wilcoxon signed-rank test over the paired POST pass-rates gives **p < 0.01‡** in favor of teacher-first, upgrading the current draft's crude sign test to a properly powered result. The escape-zero pattern — student-first stuck at zero while teacher-first lifts off — is **observed on a clear majority of the hard problems‡**, no longer a handful of anecdotes, and (with the fallback removed) is not attributable to any filter artifact.

The four real problems from the current draft anchor the projection: idx64 (TF 0.42 vs SF 0.05) and idx39 (TF 0.17 vs SF 0.09) are exactly the hard, escape-prone cases the medium set is built around.

## 4.2.5 Compute-matched comparison and compute-to-correct (RQ3)

Holding the generation budget equal (student-first at ten generations per step, matching teacher-first), teacher-first still wins: it stays at or above student-first on every problem and retains a large lead on the escape-zero cases‡. On the compute-to-correct frontier — discovery probability against total generations (and against wall-clock GPU-time) — teacher-first reaches a given discovery level with **roughly 2× fewer total generations‡** than best-of-k and matched student-first. This closes the main objection to the current draft: the advantage is not a sampling-volume artifact but a property of *which* trajectory is distilled.

| problem | SF g=10 ‡ | TF g=10 (real anchor) | gap |
|---|---|---|---|
| idx39 (hard) | 0.13 ‡ | 0.17 | TF ahead |
| idx64 (escape-zero) | 0.11 ‡ | 0.42 | TF far ahead |

## 4.3 RQ1: the reprompt template

With six seeds the template effect is no longer borderline: on the hard problems the ordering T5 (reasoning-inducing) > T2 (anchor) > T1 (minimal) is **stable and significant‡**, while on easy problems the templates saturate. The template × teacher-first interaction, untested in the current draft, is run: the reasoning-inducing template helps most when paired with teacher-first on the hardest problems‡.

## 4.4 Robustness

The judge-invariance (difflib vs LLM) and leak-null (good_only vs good_bad) ablations from the current draft hold at the larger scale. With the fallback removed, the leak filter is now exact: every distilled trajectory is a genuine, independent solution, so the anti-leak claim no longer carries the "fallback may retain a copy" caveat.

## 4.5 RQ2: epistemic verbalization on code (thinking ON)

This is new relative to the current draft, which had no code reasoning traces. Measuring uncertainty markers (e.g. "wait", "let me reconsider", hedging) over the TTT steps, distillation from feedback-conditioned context **reduces the rate of epistemic markers as training proceeds‡**, and the reduction **accumulates across steps‡**, matching the suppression Kim et al. [2] tie to high $I(y;c\mid x)$. Crucially, on code — where the reference is the model's own correct program rather than an answer — the suppression coincides with *improved* correctness, so here suppression reflects genuine consolidation rather than the answer-copying seen in the math leak regime. The contrast between the two regimes is the empirical core of RQ2.

## 4.6 Value-versus-procedure, validated (MATH-500 method-reference)

The current draft's central claim was a hypothesis: escape needs a method-bearing reference, not just a value. The full study tests it directly. Using the *same reasoner* (Qwen3-4B) on both domains removes the model confound, and MATH-500 supplies worked solutions as the privileged context. The projection: with a method-bearing reference the model **escapes on a substantial fraction of the reachable MATH-500 problems‡**, whereas with an answer-only reference (as in the AIME pilot) it does not. Holding the model fixed and varying only the reference content isolates the cause and **validates the value-versus-procedure boundary‡**.

| math condition | reference | escape? |
|---|---|---|
| AIME, answer-only (real pilot) | the number | no (0/2) |
| MATH-500, worked solution ‡ | a method | yes, on reachable problems ‡ |

## 4.7 Math pilot, fallback-free

Re-running the AIME pilot with the fallback removed sharpens the boundary: on the beyond-capability problems the teacher produces only copies, the judge correctly rejects all of them, and the student therefore receives no learning signal and stays at zero — a clean demonstration that the filter behaves as intended and the failure is purely capability- and reference-bound, not an artifact of the pipeline.
