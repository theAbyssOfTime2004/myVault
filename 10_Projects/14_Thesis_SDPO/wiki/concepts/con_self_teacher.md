---
type: concept
created: 2026-04-22
updated: 2026-04-22
tags: [self-distillation, training, teacher-student]
sources: [src_hubotter2026_self_distillation]
aliases: [self-distillation, internal teacher]
---

# Self-teacher

A training setup where a single model plays both teacher and student roles. In [[ent_sdpo]], the model conditioned on feedback — `π(· | state, feedback)` — is the teacher, and its predictions are distilled back into the unconditioned policy `π(· | state)`.

## Why it works

Language models often recognize the right answer when *given hints or feedback* even when they cannot produce it zero-shot. Self-distillation transfers that **conditional competence** to unconditional generation.

## Contrast

- **External teacher distillation**: larger/stronger model teaches a smaller one. Requires the teacher.
- **Self-teacher**: no external model — the student's own conditional distribution is the teacher.
- **Chain-of-thought distillation**: teacher produces reasoning, student mimics. Self-teacher is more general (any feedback, not just CoT).

## Related

- [[ent_sdpo]] · [[con_rich_feedback]]
- Classical self-distillation lit (Zhang et al., Mobahi et al.) — pending separate source ingest.

## Open / thesis link

- Kim et al. 2026 reports that self-distillation (on math) suppresses [[con_epistemic_verbalization]]. Is this an intrinsic property of the self-teacher setup, or specific to training-time only? Thesis RQ2 targets the test-time case.
