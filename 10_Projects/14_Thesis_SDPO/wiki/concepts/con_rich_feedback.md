---
type: concept
created: 2026-04-22
updated: 2026-04-22
tags: [rl, signal, feedback]
sources: [src_hubotter2026_self_distillation]
---

# Rich feedback (trong RL training)

Training signal chứa nhiều thông tin hơn scalar reward — ví dụ: natural-language critique, structured error message, tokenized explanation về chỗ sai. Được formalize hoá thành problem setting *"RL with rich feedback"* trong [[src_hubotter2026_self_distillation]].

## So sánh

| Loại signal | Ví dụ | Density |
|---|---|---|
| Outcome reward ([[ent_rlvr]]) | 1 nếu test pass, 0 nếu không | 1 / episode |
| Step reward | +0.2 mỗi subtest pass | 1 / step |
| **Rich feedback** | "Line 12 trả về sai type vì..." | Token-level sau khi condition |

Điểm khác biệt bản chất: rich feedback chỉ "dày" được khi có model hiểu được ngôn ngữ — đó chính là lý do SDPO dùng chính model làm teacher.

## Ai consume

- [[ent_sdpo]] — đưa rich feedback vào làm teacher-side conditioning, rồi distill ngược.

## Liên hệ thesis

- **Format** của feedback nào hữu dụng nhất? → map thẳng vào thesis **RQ1** và [[con_reprompt_template]] taxonomy.
- Format có ảnh hưởng tới [[con_epistemic_verbalization]] suppression không? → thesis **RQ2**.
