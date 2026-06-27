---
type: report
tags: [report, chapter, discussion, bestcase]
---

# Chapter 5 — Discussion

> **‡ Best-case / projected draft.** The interpretation below assumes the Chapter 4 projections (‡) land in the hypothesized direction. The closing section states what changes if they do not.

## 5.1 Why teacher-first wins, now compute-fair

The mechanism is unchanged from the current draft: on hard problems the bare student rarely rolls a correct attempt, so student-first has nothing correct to distil, while teacher-first injects a correct trajectory generated under feedback. What the full study adds is that the advantage **survives at matched compute** (§4.2.5): at ten generations per step student-first improves but still loses, and the compute-to-correct frontier shows teacher-first reaching discovery with fewer total generations. The current draft could only say "outcome win, not yet compute win"; the best case turns this into a compute-fair claim, which is the single most important upgrade for credibility.

## 5.2 The value-versus-procedure boundary, validated

With the model held fixed and only the reference content varied (MATH-500 worked solution vs AIME answer-only, §4.6), escape appears exactly when the reference encodes an in-reach *method* and not when it encodes only a *value*. This converts the thesis's central idea from a characterization into a tested claim. In code the output is itself a method (a program that generalizes), so distillation installs a procedure; in answer-only math the output is a value that does not generalize, so the teacher can only copy. Supplying the worked solution gives math the missing method, and the boundary moves as predicted.

## 5.3 Epistemic suppression, and what it means here

The thinking-on code result (§4.5) lets us connect to Kim et al. [2]: distillation from feedback-conditioned context suppresses epistemic markers, and the effect accumulates across steps. The nuance the full study can finally state is regime-dependent: on code, where the reference is a correct program, the suppression coincides with genuine improvement (consolidation); in the math leak regime, the same surface suppression coincides with answer-copying and no improvement. Suppression of uncertainty markers is therefore not intrinsically harmful — its meaning depends on whether the reference carries a method.

## 5.4 A cleaner filter

Removing the keep-best-correct fallback means the anti-leak filter is now exact: every distilled trajectory is a genuine, independent solution. This removes the one place in the current draft where the judge could be silently overridden, and makes the math boundary argument airtight — the failure on beyond-capability problems is now demonstrably reference- and capability-bound, not a pipeline artifact.

## 5.5 Position relative to the parent paper

The contribution sharpens: a teacher-first organization of execution-guided self-distillation that accelerates test-time discovery, with a compute-fair advantage, a measured epistemic effect on code, and a validated boundary on *when* the approach helps — the question the parent paper [1] leaves open. This is the form in which the work is suitable for a conference submission.

## 5.6 If the projections do not hold

Honesty requires stating the downside, because each ‡ result could go the other way. If medium-n shrinks the effect, the claim reverts to weak dominance with a real but small margin. If student-first at matched compute closes the gap, the contribution becomes "teacher-first is more sample-efficient" rather than "better" — still publishable, but a different headline. If epistemic suppression does not appear on code, RQ2 stays a math-only observation. If MATH-500 with worked solutions still does not escape, the boundary is about reachable capability more than reference content, and the value-versus-procedure framing weakens to a capability story. The experiments decide; this draft shows the upside, and the real runs will report whichever way they fall.
