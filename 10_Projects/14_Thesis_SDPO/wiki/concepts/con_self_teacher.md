---
type: concept
created: 2026-04-22
updated: 2026-04-22
tags: [self-distillation, training, teacher-student, mechanism]
sources: [src_hubotter2026_self_distillation]
aliases: [self-distillation, internal teacher, retrospective teacher]
---

# Self-teacher

Training setup trong [[ent_sdpo]] mà **cùng một model** đóng hai vai trò:

- **Student**: `π_θ(· | x, y<t)` — next-token distribution không có feedback.
- **Teacher**: `π_θ(· | x, f, y<t)` — cùng params `θ`, nhưng condition thêm feedback `f`.

Teacher "nhìn thấy" f trong context → distribution của nó *retrospectively* adjust để phản ánh mistake của attempt gốc. Student học bằng cách minimize KL về teacher.

## Mechanism (paper Figure 4)

1. Student sinh answer `y` (không có feedback).
2. Environment trả về feedback `f` (error, sample solution, v.v.).
3. Re-compute log-prob của **chính `y` đó** dưới teacher `π_θ(·|x, f, y<t)`.
4. Mỗi position `t`: nếu teacher assign xác suất **cao hơn** cho token `y_t` so với student → token đó đúng hướng (keep). Nếu **thấp hơn** → token sai, advantage âm → push student away.
5. Figure 4 visualize: red tokens = teacher disagree, sparse → credit assignment tập trung vào chỗ mistake.

**No sampling overhead**: chỉ cần forward pass để compute log-probs.

## Vì sao hoạt động

LLMs thường "biết" câu trả lời đúng **khi được gợi ý hoặc feedback**, dù không sinh ra được zero-shot. Self-distillation transfer *conditional competence* này thành *unconditional generation*.

Paper note (§4.1): ability này **emergent với scale**. Model yếu (Qwen2.5-1.5B) không hình thành self-teacher tốt.

## Self-teacher bootstrap (§4.3)

Điều quan trọng: teacher **không frozen**. Update cùng student theo thời gian.
- Teacher generation accuracy tăng theo training.
- Student eventually > initial teacher → true bootstrapping.
- Cần [[con_teacher_regularization]] (EMA hoặc trust-region) để tránh teacher collapse về student và ignore `f`.

## Phân biệt với các setup khác

- **External teacher distillation**: teacher lớn/mạnh hơn dạy student nhỏ. Cần teacher.
- **Self-teacher (ours)**: không cần external model — conditional distribution của chính student là teacher.
- **Chain-of-thought distillation**: teacher sinh reasoning, student mimic. Self-teacher tổng quát hơn — feedback dạng gì cũng được.
- **Feedback-conditioned policy** (Liu et al. 2023): học `π(y|x, f)` như goal-conditioned — feedback là goal. Self-teacher thì treat feedback là **state** để credit assignment.

## Quan sát surprising từ §5 (test-time)

Trên hard questions, initial self-teacher accuracy **<1%** — nghĩa là ngay cả conditioned on feedback, 1-shot vẫn không solve. Nhưng **credit assignment vẫn đủ tốt** để iterate. Đây là insight mạnh: không cần teacher solve được → chỉ cần teacher *đánh giá* được.

## Links / thesis

- [[ent_sdpo]] · [[con_rich_feedback]] · [[con_credit_assignment]] · [[con_teacher_regularization]]
- Kim et al. 2026 report self-distillation (math) suppress [[con_epistemic_verbalization]]. Thuộc tính nội tại self-teacher hay chỉ train-time? → **RQ2**.
- Bootstrap property: liệu test-time SDPO có effect bootstrap tương tự? Paper §5 chỉ 1 câu/run → không có signal lên curve teacher-improves. Thesis có thể đo.
