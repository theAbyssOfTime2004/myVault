---
type: concept
created: 2026-04-22
updated: 2026-04-22
tags: [rl, signal, feedback]
sources: [src_hubotter2026_self_distillation]
---

# Rich feedback (in RL training)

A training signal that carries more information than a scalar reward — e.g. natural-language critique, structured error messages, tokenized explanations of what went wrong. Formalized as a problem setting ("RL with rich feedback") in [[src_hubotter2026_self_distillation]].

## Contrast

| Signal type | Example | Density |
|---|---|---|
| Outcome reward ([[ent_rlvr]]) | 1 if tests pass else 0 | 1 / episode |
| Step reward | +0.2 per passed subtest | 1 / step |
| **Rich feedback** | "Line 12 returns wrong type because..." | Token-level once conditioned |

## Consumers

- [[ent_sdpo]] — feeds rich feedback into the model as teacher-side conditioning, then distills back.

## Open / links to thesis

- What feedback **formats** are most useful? → directly maps onto thesis RQ1 and [[con_reprompt_template]] taxonomy.
- Does feedback format affect [[con_epistemic_verbalization]] suppression? → thesis RQ2.
