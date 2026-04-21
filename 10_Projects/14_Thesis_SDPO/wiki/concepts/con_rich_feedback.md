---
type: concept
created: 2026-04-22
updated: 2026-04-22
tags: [rl, signal, feedback]
sources: [src_hubotter2026_self_distillation]
---

# Rich feedback

**Tokenized** feedback từ environment vượt ra khỏi scalar reward. Định nghĩa formal của [[ent_rlrf]] paradigm: `f` có thể là any sequence of tokens representing state của environment sau action.

## So sánh các signal type

| Loại | Ví dụ | Density | Used by |
|---|---|---|---|
| Outcome reward | unit tests pass = 1 | 1 / episode | [[ent_rlvr]] |
| Step reward | +0.2 / subtest | 1 / step | PRM methods |
| **Rich feedback** | "ZeroDivisionError at line 73" | Token-level after condition | [[ent_rlrf]], [[ent_sdpo]] |
| Preference | A > B | Pair / episode | RLHF |

Điểm khác biệt bản chất: rich feedback chỉ "dày" khi có model hiểu được language. Đó chính là lý do SDPO dùng chính policy làm [[con_self_teacher]] — không cần external decoder.

## Nguồn rich feedback (paper §4.6)

Trong code environment, paper phân tích 3 loại:

1. **Environment output**: runtime error, failed test trace, stdout/stderr.
2. **Sample solution**: successful rollout khác trong group (nếu có).
3. **Student's original attempt**: bản thân attempt `y`.

Ablation (Table 6 của paper):

| Feedback combination | Training acc (LCBv6) |
|---|---|
| `output` only | 39.9% |
| `own_solution` only | 42.6% |
| **`output + own_solution`** | **48.3%** ← best |
| `y + output + own_solution` | 44.5% ← biased |

→ Output + solution bổ trợ nhau. Include `y` trong teacher **giảm entropy** (0.40 → 0.23), giảm diversity.

## Format matters (mới chỉ được test syntactically)

Paper claim: *"performance is not sensitive to syntactic variations of the reprompting template"* (§4.6). Nhưng:

- Đây là test của **micro-variation** (wording, format).
- **Macro-variation** (cấu trúc template, what info included, ordering) có thể quan trọng — paper không ablate.
- **Behavior impact** (verbosity, uncertainty) hoàn toàn không được đo.

→ Thesis RQ1 exploit gap này — systematic template taxonomy + measurement.

## Consumers

- [[ent_sdpo]] — primary. Feed feedback qua [[con_reprompt_template]] để form teacher context.
- [[con_self_teacher]] — mechanism dùng feedback.

## Open / thesis link

- Format ảnh hưởng [[con_epistemic_verbalization]] suppression? → RQ2.
- Best format cho discovery efficiency? → RQ1.
- Có cần dynamic format (adapt theo feedback type) không? → follow-up.
