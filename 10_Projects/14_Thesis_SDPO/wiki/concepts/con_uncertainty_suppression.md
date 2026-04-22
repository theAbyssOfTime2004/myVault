---
type: concept
created: 2026-04-22
updated: 2026-04-22
tags: [phenomenon, self-distillation, behavior, rq2]
sources: [src_kim2026_why_self_distillation_degrades]
aliases: [epistemic suppression, uncertainty collapse]
---

# Uncertainty suppression

Hiện tượng self-distillation (và các post-training method tương tự) **giảm [[con_epistemic_verbalization]]** của student model, dẫn đến confident reasoning style có thể hurt OOD performance.

Đây là **phenomenon chính của RQ2**. Paper nguồn: [[src_kim2026_why_self_distillation_degrades]].

## Mechanism

```
Teacher condition trên rich context c
  → teacher generate concise confident reasoning
  → student KL-minimize với teacher
  → student học imitate style
  → suppress "wait/hmm/maybe/..." tokens
```

Vấn đề: tại inference time, student **không có `c`** → phải reason from scratch → nhưng đã bị train để không express uncertainty → premature commit errors.

## Conditions suppression xảy ra

Theo [[src_kim2026_why_self_distillation_degrades]], hai factors quyết định:

### 1. Information richness `I(y; c|x)`

Càng giàu context càng suppress mạnh:
- `c = s` (full solution): suppress aggressive nhất.
- `c = s\think` (solution no CoT): suppress ít hơn.
- `c = ỹ` (regenerated): intermediate.
- `c = ∅`: không suppress (không có teacher gap).

### 2. Task coverage

Xem [[con_task_coverage]]:
- Narrow coverage (Chemistry 6 types, LCB 131 q): suppression OK, accuracy up.
- Broad coverage (DAPO-Math 14k): suppression **hurt** OOD.

## Evidence empirical

### Off-policy SFT (Table 2)

DeepSeek-R1-Distill-Qwen-7B SFT trên 800 **correct** responses:

| Dataset | Epistemic density | AIME24 |
|---|---|---|
| Unguided responses | High | 51.0 (~base) |
| Solution-guided responses | Low | **20.2** (drop 40%) |

Cả hai đều correct answers — chênh duy nhất ở epistemic density.

### On-policy ([[ent_sdpo]] vs [[ent_grpo]])

DeepSeek-R1-Distill-Qwen-7B trên DAPO-Math:
- GRPO: +epistemic, AIME24 54.7 → 56.0.
- SDPO `c=s`: −60.8 `wait` tokens, AIME24 drop ~40%.

### Feedback loop với moving teacher

EMA 0.05 teacher **amplify** suppression qua iterations (Figure 6). Fixed teacher (EMA 0.0) mitigate.

→ Update [[con_self_teacher]] section fixed vs moving.

## Không chỉ stylistic

Key paper claim: "Even when the training objective faithfully guides the model toward correct reasoning traces, the resulting reasoning style can quietly shift in ways that hurt generalization."

Suppression **không penalize bởi standard objective** (KL to teacher, correct reward). Hidden regression.

## Mối quan hệ với "concise reasoning" claim của SDPO

Hübotter 2026 (§3.3) tự hào SDPO responses 3×–11× ngắn hơn GRPO mà accuracy cao hơn. Kim et al. 2026 phản biện: claim này đúng *trong task coverage hẹp*. Rộng ra → concise = suppress = hurt.

→ Hai papers không direct contradict — complementary: Hübotter show gain in-domain narrow, Kim show cost OOD broad.

## Thesis implications

### RQ2 formal claim
Thesis RQ2: **đo epistemic suppression trong test-time SDPO trên code** (LCBv6 hard/very-hard). Paper chưa cover setting này.

### Predictions testable
- H1: Suppression xảy ra ở test-time SDPO (monotonic decrease qua iterations).
- H2: Magnitude nhỏ hơn math vì code base có ít epistemic tokens tự nhiên.
- H3: Template design ([[con_reprompt_template]]) modulate suppression rate.

### Mitigation ideas (future work seed)
- Template với explicit uncertainty elicitation (vary RQ1).
- Teacher regularization đặc biệt penalize epistemic token suppression — xem [[con_teacher_regularization]] (stub).
- Entropy floor / constrain KL theo epistemic token positions.

## Links

- [[con_epistemic_verbalization]] — the thing being suppressed.
- [[con_task_coverage]] — the modulating factor.
- [[con_self_teacher]] · [[con_reprompt_template]] · [[ent_sdpo]]
