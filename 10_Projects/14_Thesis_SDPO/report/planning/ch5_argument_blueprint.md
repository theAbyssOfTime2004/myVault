---
type: report-planning
created: 2026-06-26
updated: 2026-06-26
tags: [report, planning, argument-blueprint, cer, discussion]
sources: [syn_report_outline, syn_core_result, syn_math_pilot]
---

# Argument Blueprint — Chapter 5 (Discussion)

Phase 3 (`argument_builder`) artifact. Guides the Ch5 draft. CER = Claim–Evidence–Reasoning. Strength rated Strong/Moderate/Weak per the skill rubric; weak points flagged honestly (calibrated to small n).

## Central thesis

Teacher-first self-distillation escapes the test-time flat-reward trap **precisely when the privileged reference encodes an in-reach *method*, not merely a correct *value*.** Code meets this condition; answer-only AIME math violates it. This single distinction explains the escape / no-escape contrast and bounds the mechanism.

## Sub-arguments

### SA1 — TF beats SF because off-policy injection supplies a correct trajectory where on-policy rollout cannot
- **Evidence**: 8/8 matched TF≥SF (§4.2.2); escape-zero replicated ×3 (idx39 s1, idx64 s1/s2, §4.2.3); idx64 TF 0.422 vs SF 0.047.
- **Reasoning**: on the hard band the bare student rarely rolls correct → flat reward → SF has nothing right to distill; TF's teacher generates a correct trajectory to distill instead.
- **Counter-argument**: TF samples ~2.5× more (`teacher_n=10`) → maybe it is just more compute / best-of-k, not a better mechanism.
- **Rebuttal (concede-and-limit)**: outcome win, not yet compute win — concede openly, defer to CTC (RQ3). But escape-zero is not explained by sampling volume alone: SF also samples 4×/step and still stays at exactly 0, while TF escapes. The *kind* of trajectory distilled differs, which is the controlled variable.
- **Strength**: **Strong** on escape-zero (2 independent problems), **Moderate** overall (not compute-matched).

### SA2 — Escape requires three necessary conditions
1. rich feedback dense enough to densify sparse reward (the SDPO premise);
2. the reference contains a *method*, not just the target;
3. capability is reachable (the model can solve once unblocked).
- **Evidence**: code satisfies all three → escape; AIME too-hard violates (2) and (3) → no escape on 2/2 problems; thinking-ON + 16k tokens still wrong (capability ceiling, §4.5.2).
- **Reasoning**: each condition maps to an observed failure mode when removed.
- **Counter-argument**: only 2 math problems, plus a model confound (Gemma ≠ Qwen) → cannot cleanly attribute non-escape to the conditions rather than to the weaker model.
- **Rebuttal (acknowledge-as-limitation)**: the three conditions are a *hypothesis the boundary supports*, not proves. Future work isolates them (MATH-500 method-reference; Qwen-on-math to remove the model confound, Chapter 6).
- **Strength**: **Moderate** (confounded; presented as characterization, not proof).

### SA3 — Central insight: value-vs-procedure
- **Claim**: code output *is* the method; math output is a *value*.
- **Evidence**: code best_in_batch is a *program* that generalizes to new inputs; an AIME answer is a number that does not; idx9 POST learns a confident reasoning *style* but not the method (form ≠ substance, §4.5.4).
- **Reasoning**: distilling a correct program transfers a reusable algorithm; distilling answer-aware traces transfers style, not capability.
- **Counter-argument**: is this a deep property, or just that AIME happens to lack worked solutions (which MATH-500 has)?
- **Rebuttal (reframe)**: that *is* the testable prediction — the value/procedure distinction predicts MATH-500-with-solution should move toward escape. Stated honestly as a conceptual claim with one falsifiable prediction, not yet tested.
- **Strength**: **Moderate** (compelling, one testable prediction, untested).

### SA4 — Reward landscape reinforces the contrast: cliff vs slope
- **Evidence**: code partial test-pass gives a climbing gradient (0.21 → 1.0); math binary reward is all-or-nothing.
- **Reasoning**: a graded reward offers a hill to climb even before the first full success; a binary reward offers none, worsening the flat-reward trap.
- **Counter-argument**: this is about reward *shape*, distinct from the method/value point — are two explanations being conflated?
- **Rebuttal (concede)**: they are distinct but co-vary with domain in this data (a confound). Presented as *jointly* characterizing the boundary, not as independently isolated causes.
- **Strength**: **Moderate** (co-varies with SA3; confound stated).

### SA5 — Leak is null on code, measurable on math, consistent with Kim; TF's filter is the intended remedy
- **Evidence**: good_bad ≈ good_only on code (leak-null, §4.4); judge catches ~75% copy on math (§4.5.3); fallback can defeat the judge (idx8).
- **Reasoning**: code reference = best_in_batch + public tests (nothing to leak); math reference = the answer (everything to copy).
- **Counter-argument**: the "fallback defeats the judge" finding undermines TF's own anti-leak claim.
- **Rebuttal (acknowledge-as-limitation)**: honest — the remedy holds when the teacher yields ≥1 genuine good, and fails when it yields only copies. A bounded claim, not a universal one.
- **Strength**: **Strong** on code leak-null; **Moderate** on the remedy (fallback caveat).

## Logical flow

Results recap → SA1 (why TF > SF) → SA2 (three conditions) → SA3 (value-vs-procedure, the central claim) → SA4 (reward landscape) → SA5 (leak + Kim) → position relative to Hübotter §5 (what this thesis adds beyond the parent paper).

## Strength assessment

| Sub-argument | Evidence strength | Logic validity | Counter-arg risk |
|---|---|---|---|
| SA1 (TF > SF) | Strong (escape-zero ×3) | Valid | Medium (compute) |
| SA2 (3 conditions) | Moderate (n=2 math, confound) | Qualified | High (confound) |
| SA3 (value-vs-procedure) | Moderate (untested prediction) | Valid | Medium |
| SA4 (reward landscape) | Moderate (co-varies SA3) | Qualified | Medium |
| SA5 (leak) | Strong (code) / Moderate (math remedy) | Valid | Medium |

## Weak-indicator check (skill checklist)

- **Correlation-as-causation**: SA3 and SA4 both co-vary with domain → flagged as a confound, handled by acknowledging it and pointing to the MATH-500 / Qwen-on-math experiments that would separate them.
- **Single-context generalization**: math n=2 → flagged; claims kept at "boundary characterization."
- No circular reasoning, no false dichotomy, no appeal to authority without data. No 2+ weak indicators in any single core argument → safe to draft.

## Notes for the draft

- Lead with the mechanism (SA1), make SA3 the intellectual centerpiece, keep every cross-domain causal claim explicitly confounded.
- Do **not** compound the two sign tests from §4.2.2 and §4.2.3 (they share idx39). State this once.
- Tone: interpret, do not re-report numbers; cite §4.x for evidence rather than repeating tables.
