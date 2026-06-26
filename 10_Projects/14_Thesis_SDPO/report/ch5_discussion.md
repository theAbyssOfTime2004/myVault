---
type: report
created: 2026-06-26
updated: 2026-06-26
tags: [report, chapter, discussion, teacher-first, value-vs-procedure, boundary]
sources: [syn_report_outline, syn_core_result, syn_math_pilot, src_hubotter2026_self_distillation, src_kim2026_why_self_distillation_degrades, src_shenfeld2026_sdft]
---

# Chapter 5 — Discussion

This chapter interprets the results of Chapter 4 rather than re-reporting them; evidence is cited back to §4.x. The argument builds toward one claim: teacher-first self-distillation escapes the test-time flat-reward trap when the privileged reference encodes an in-reach *method*, and fails when it encodes only a *value*. Code meets that condition and math, as run here, does not, which is what the escape and no-escape results jointly characterize.

## 5.1 Why teacher-first beats student-first

The matched results (§4.2.2) and the hard-frontier extension (§4.2.3) point to a single mechanism. On a hard problem the bare student rarely produces a correct rollout, so student-first has nothing correct to distill and the reward stays flat. Teacher-first removes that dependence: the teacher, conditioned on feedback and steered by good exemplars, can generate a correct trajectory even when the unaided student cannot, and the student is distilled toward that trajectory. The controlled variable across the two arms is exactly *which* trajectory is distilled (§3.1), so the gap is attributable to that choice rather than to model, loss, or hyperparameters.

The escape-zero events are the cleanest evidence. In three seed-instances (idx39 s1, idx64 s1 and s2) student-first stays at or returns to pass = 0 while teacher-first lifts off zero. The obvious alternative explanation is compute: teacher-first draws roughly 2.5× more samples per step, so perhaps it simply finds a solution by volume. That objection is conceded in part and bounded. The thesis claims an *outcome* win, not yet a *compute* win, and defers a compute-matched comparison to the compute-to-correct metric (Chapter 6). But sampling volume alone does not explain escape-zero: student-first also samples several rollouts per step and still never escapes 0 on those instances, whereas teacher-first does. The difference is the *kind* of trajectory available to learn from, not merely the count.

The result should be read at its real strength. It is weak dominance, with many ties and modest typical margins, sharpened into a clear effect on the hardest problems where there is room to separate the arms. One further caution applies to the statistics. The main matched comparison (§4.2.2) and the hard-frontier extension (§4.2.3) share problem idx39, so their two sign-test values are not independent and must not be multiplied together into a stronger combined claim. Each is reported as a separate descriptive signal over a small sample.

## 5.2 Three conditions for escape

Reading the escape and no-escape cases together suggests three conditions that appear jointly necessary for teacher-first to lift a problem off zero.

First, the feedback must be rich enough to densify the sparse reward, which is the original premise of SDPO [1]. Second, the reference the teacher draws on must contain a *method*, not just the target. Third, the capability must be reachable: the model has to be able to produce the solution once unblocked, even if it cannot find it unaided. Code satisfies all three and escapes. The AIME too-hard problems violate the second and third: the reference is a bare number, and the model answers wrong with confidence even after reasoning to completion with thinking ON and a 16k-token budget (§4.5.2), which indicates a genuine capability ceiling rather than a compute shortfall.

This decomposition is a hypothesis the boundary supports, not a proven law. Two problems is a thin basis, and the math runs carry a model confound (Gemma-4-E4B for math versus Qwen3-4B for code), so non-escape cannot be cleanly attributed to the missing conditions rather than to the weaker reasoner. The conditions are stated as a characterization, with the experiments that would isolate them set out in Chapter 6.

## 5.3 Value versus procedure

The second condition deserves a sharper statement, because it is the intellectual center of the thesis. In code, the model's output *is* the method. A correct program is an algorithm; it generalizes to new inputs, and best_in_batch validated by public tests is therefore a transferable artifact. Distilling toward it installs a reusable procedure. In math as run here, the output is a *value*. An AIME answer is a single number that does not generalize, and the derivation that would generalize, the worked solution, is a separate artifact that AIME does not provide. The teacher conditioned on the answer can copy the number but has no procedure to transfer.

The idx9 traces make this concrete (§4.5.4). After test-time training the student produces a more confident reasoning *style* learned from the answer-aware teacher, but not a correct method, and it does not even memorize the target 156. Form transfers; substance does not. This is what distilling a value rather than a procedure looks like from the inside.

A fair objection is that this may be an artifact of AIME specifically, since MATH-500 does include worked solutions. That objection is welcome, because it is precisely the prediction the value-versus-procedure view makes: supplying a method-bearing reference should move math toward escape. The claim is conceptual and carries one falsifiable test, which Chapter 6 names. It is not yet established.

## 5.4 Reward landscape: a cliff and a slope

A second domain difference compounds the first. Code uses a graded reward, the fraction of tests passed, so even a partially correct program earns a gradient to climb, and runs show that climb in practice (for example 0.21 toward 1.0). Math uses a binary reward, correct or not, with nothing in between. A graded reward is a slope that can be ascended before the first full success; a binary reward is a cliff that gives no foothold until the answer is exactly right, which deepens the flat-reward trap that teacher-first is meant to relieve.

Reward shape and the value-versus-procedure distinction are conceptually separate, but in this data they co-vary with the domain: code is both graded and method-bearing, math is both binary and value-only. They cannot be disentangled here, so they are offered together as a joint characterization of the boundary rather than as two independently isolated causes. Separating them would require, for instance, a graded math reward or an answer-only code task, neither of which was run.

## 5.5 Leak: null on code, measurable on math

The leak picture is consistent with the same reference distinction. On code the leak ablation is null: feeding the teacher labeled "bad/copy" exemplars (good_bad) changes nothing relative to good_only (§4.4). This follows from the code reference being best_in_batch plus public tests rather than an author solution, so there is little reference content to leak in the first place. On math the leak is directly measurable: with the answer in context, the teacher mostly copies, and the judge flags roughly 75% of trajectories as copies (§4.5.3). This is the degradation-from-rich-context that Kim et al. [2] describe, observed here as a concrete copy rate.

Teacher-first's filter is the intended remedy, and its limit is stated honestly. The keep-best-correct fallback can defeat the judge: when every trajectory is a copy, the fallback still forces one copy into the good pool, as the idx8 log shows (§4.5.3). The remedy therefore holds when the teacher yields at least one genuine, independent solution and fails when it yields only copies. That is a bounded claim about a filter, not a guarantee that teacher-first prevents leak in all regimes.

## 5.6 The reprompt template

The template result (§4.3) speaks to the titular question and interprets cleanly through the formal mechanism of §3.4. The template sets the content of the privileged context, which sets the teacher distribution $\pi_T$, which sets the per-token gradient target $\pi_S - \pi_T$ (§3.3.5). Changing the template is therefore a direct way to steer what the teacher demonstrates. The data show a monotone ordering on the hard problem, T5 > T2 > T1, and saturation on the easy one. The reading is that a reasoning-inducing reprompt ("identify the root cause, then fix") gives the teacher a diagnostic context that yields better corrections exactly where corrections are hard to find, while on an easy problem any adequate template suffices and the differences wash out.

This addresses, in miniature, the open question Hübotter et al. [1, §7] raise about how the reprompt template influences behavior, and it aligns with Kim et al.'s [2] information-content axis, since T1 through T5 vary how much diagnostic structure the context carries. The evidence is directional only: the probe is on the student-first arm, at two seeds, with small absolute counts, and the template by teacher-first interaction is untested (Chapter 6). The template matters, and it matters most in the hard regime, but the strength of that statement is bounded by the same small n as the rest of the study.

## 5.7 Position relative to the parent paper

The privileged context used throughout is the same object Hübotter et al. [1] call feedback; the name is local to this codebase, the concept is theirs, and their feedback-content ablation (Table 6) studies the same lever. The parent paper studies student-first, on-policy test-time SDPO. This thesis contributes a teacher-first organization of execution-guided self-distillation that distills filtered teacher generations, places it between SDPO and SFT (it resembles SDFT [3] but with execution feedback rather than a fixed demonstration as context), and characterizes the regime where reorganizing the update this way *accelerates* test-time discovery. The escape-zero result extends the parent paper's §5 observation that SDPO can iterate from rich feedback before the first success, by showing a concrete setting where the on-policy version stalls at zero and the teacher-first version does not. The value-versus-procedure boundary is the thesis's own framing of *when* that acceleration should and should not appear, and it is the question the parent paper leaves open.

## In-chapter citations

Numbered per the master bibliography (`00_references.md`): [1] Hübotter et al. 2026 · [2] Kim et al. 2026 · [3] Shenfeld et al. 2026. (Evidence cited back to Chapter 4; metric and method definitions in Chapter 3.)
