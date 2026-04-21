---
type: concept
created: 2026-04-22
updated: 2026-04-22
tags: [self-distillation, training, teacher-student]
sources: [src_hubotter2026_self_distillation]
aliases: [self-distillation, internal teacher]
---

# Self-teacher

Training setup mà một model đóng cả hai vai trò teacher và student. Trong [[ent_sdpo]], model conditioned on feedback — `π(· | state, feedback)` — là teacher, và predictions của nó được distill ngược về unconditioned policy `π(· | state)`.

## Vì sao hoạt động được

Language models thường "biết" câu trả lời đúng **khi được gợi ý hoặc feedback**, dù không sinh ra được zero-shot. Self-distillation chính là quá trình transfer khả năng *conditional competence* này sang *unconditional generation*. Hay nói cách khác: model học được việc bản thân đã biết gì khi có hint.

## Phân biệt

- **External teacher distillation**: teacher lớn/mạnh hơn dạy student nhỏ. Bắt buộc có teacher.
- **Self-teacher**: không cần external model — chính conditional distribution của student là teacher.
- **Chain-of-thought distillation**: teacher sinh ra reasoning, student mimic. Self-teacher tổng quát hơn (bất kỳ loại feedback nào, không riêng CoT).

## Liên hệ

- [[ent_sdpo]] · [[con_rich_feedback]]
- Classical self-distillation literature (Zhang et al., Mobahi et al.) — chờ ingest source riêng.

## Open / thesis link

- Kim et al. 2026 report rằng self-distillation (trên math) suppress [[con_epistemic_verbalization]]. Đây là thuộc tính **nội tại** của self-teacher setup, hay chỉ xảy ra ở training-time? Thesis **RQ2** target câu hỏi này ở test-time.
