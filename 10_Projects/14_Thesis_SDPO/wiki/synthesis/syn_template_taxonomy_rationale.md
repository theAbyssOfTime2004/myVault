---
type: synthesis
created: 2026-05-02
updated: 2026-05-02
tags: [template, taxonomy, rq1, rationale, methodology]
sources: [src_hubotter2026_self_distillation, src_kim2026_why_self_distillation_degrades]
---

# Template Taxonomy — Rationale & Nguồn gốc

Giải thích tại sao thesis chọn 7 templates này, không phải 7 templates khác. Dùng khi viết methodology section của thesis.

## Vấn đề

7 templates trong [[syn_thesis_proposal]] (T1–T7) được propose ban đầu mà không có explicit grounding. Cần principled justification để defensible với advisor/reviewer.

**Câu hỏi reviewer sẽ hỏi**: *"Tại sao là 7 templates này?"*

## Cách trả lời: Principled Dimension Framework

Thay vì justify từng template riêng lẻ, thesis identify **3 dimensions** mà reprompt template có thể vary. 7 templates là sample đại diện trải trên 3 dimensions đó.

Khi reviewer chấp nhận 3 dimensions là important → 7 templates tự nhiên follow.

---

## 3 Dimensions và nguồn gốc

### Dimension 1 — Information content

**Định nghĩa**: Lượng thông tin trong teacher context `c` — từ tối thiểu (chỉ thông báo sai) đến tối đa (error + stack trace + code cũ).

**Grounding**: [[src_kim2026_why_self_distillation_degrades]] — Kim et al. chứng minh `I(y;c|x)` (information richness của teacher context) **quyết định mức độ suppression**. Họ test 4 điểm trên spectrum:
- `c = ∅` (không có gì)
- `c = s\think` (solution stripped thinking)
- `c = ỹ` (regenerated)
- `c = s` (full solution)

**Thesis extension**: Kim vary *loại* thông tin. Thesis vary *lượng* thông tin trong execution feedback — từ minimal đến verbose. Đây là natural extension của Kim's dimension.

**Templates cover dimension này**: T1 (Minimal) → T2 (Standard) → T3 (Verbose)

---

### Dimension 2 — Instruction framing

**Định nghĩa**: Cách prompt hướng dẫn model xử lý feedback — từ neutral ("solve it") đến diagnostic ("identify root cause first") đến reframing ("first-person reflection").

**Grounding**: [[src_hubotter2026_self_distillation]] §4.6 + §7:
- §4.6: paper test *nội dung* `c` (có solution hay không, có feedback hay không) và kết luận syntactic variation nhỏ không matter. Nhưng **semantic/instructional variation chưa được test**.
- §7 explicit: *"future work should systematically study how individual aspects, such as the reprompt template, influence behavior."*

**Thesis contribution**: fill gap §7 bằng cách vary instruction framing — dimension mà paper acknowledge là open nhưng không test.

**Templates cover dimension này**: T4 (JSON — format/structure), T5 (Reasoning-inducing — "identify root cause first"), T6 (First-person — reframe as self-reflection)

---

### Dimension 3 — Memory depth

**Định nghĩa**: Bao nhiêu lần thử trước được đưa vào teacher context — chỉ lần cuối (default) hay toàn bộ history.

**Grounding**: Hai sources:
1. [[src_hubotter2026_self_distillation]] §5: paper dùng fixed sliding window (chỉ 1 previous attempt), không ablate memory depth. Đây là implementation choice chưa được justify empirically.
2. [[src_kim2026_why_self_distillation_degrades]]: suppression **accumulate qua nhiều steps** — tức là history có thể amplify hoặc dilute suppression effect. Câu hỏi tự nhiên: nếu model thấy toàn bộ history thay vì chỉ lần cuối, behavior thay đổi thế nào?

**Templates cover dimension này**: T7 (Cumulative history — all N previous attempts)

---

## Mapping đầy đủ

| Template | Tên | Dimension | Vary gì so với T2 |
|---|---|---|---|
| T1 | Minimal | Information content (thấp) | Bỏ hết structure, chỉ "incorrect, try again" |
| **T2** | **Standard (anchor)** | **baseline** | **Failing test + expected + actual + error_type** |
| T3 | Verbose | Information content (cao) | T2 + full stack trace + previous code |
| T4 | Structured JSON | Instruction framing (format) | Same content T2, JSON-encoded |
| T5 | Reasoning-inducing | Instruction framing (diagnostic) | T2 + "First, identify root cause, then fix." |
| T6 | First-person | Instruction framing (reframe) | "I attempted this and got X. Let me reconsider." |
| T7 | Cumulative history | Memory depth | All N previous attempts, not just latest |

**T2 là anchor**: mọi template vary đúng 1 dimension, giữ nguyên dimensions còn lại → clean ablation.

---

## Cách viết trong thesis (methodology section)

> *"We organize the template design space along three dimensions motivated by prior work: (1) **information content**, following Kim et al.'s finding that `I(y;c|x)` determines suppression magnitude; (2) **instruction framing**, addressing the open question raised by Hübotter et al. §7 regarding semantic formulation variation; and (3) **memory depth**, motivated by the sequential nature of test-time SDPO and Kim et al.'s observation that suppression accumulates across steps. The seven templates (T1–T7) sample distinct points across these dimensions, with T2 (paper default) serving as the anchor."*

---

## Limitations để acknowledge

- **T4 (JSON)** cover instruction framing nhưng cũng thay đổi information density — không hoàn toàn isolate 1 dimension. Có thể argue T4 overlap cả dimension 1 và 2.
- **T7 (Cumulative)** tăng context length đáng kể → confound với compute cost tăng. Cần report context length separately.
- Taxonomy cover 3 dimensions nhưng không exhaustive — ví dụ không test code-specific uncertainty elicitation ("if unsure, add try/except"). Acknowledge as future work.

---

## Links

- [[syn_thesis_proposal]] — 7 templates trong context thesis plan đầy đủ
- [[con_reprompt_template]] — template mechanics + dimensions đã brainstorm
- [[src_kim2026_why_self_distillation_degrades]] — grounding dimension 1
- [[src_hubotter2026_self_distillation]] — grounding dimension 2 + 3
- [[con_uncertainty_suppression]] — motivation cho dimension 1 + 3
