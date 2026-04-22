---
type: concept
created: 2026-04-22
updated: 2026-04-22
tags: [training, generalization, self-distillation]
sources: [src_kim2026_why_self_distillation_degrades]
aliases: [task coverage, distribution breadth]
---

# Task coverage

Quy mô và diversity của problem distribution trong training set. [[src_kim2026_why_self_distillation_degrades]] identify đây là **modulating factor** quyết định khi nào self-distillation win vs lose.

## Operational definition

Paper vary `|D|` (số training questions) ∈ {1, 8, 64, 128, 512, 14000}. Nhưng coverage ≠ chỉ `|D|`:

| Dataset | `|D|` | Unique types | Coverage qualitative |
|---|---|---|---|
| Chemistry (SciKnowEval) | 2,400 | **6** | Narrow (surface variants) |
| LCBv6 | 131 | diverse | Narrow (train == eval) |
| DAPO-Math-17k | 14,000 | broad | Broad (OOD eval) |

→ Coverage = `|D|` × type diversity × train/eval distributional distance.

## Tương tác với [[con_uncertainty_suppression]]

**Finding central** của paper (§6):

| Coverage | SDPO vs GRPO | Suppression effect |
|---|---|---|
| Narrow | SDPO win (fast, efficient) | OK, thậm chí helpful |
| Broad | **SDPO lose OOD** | Hurt |

Visualization (Figure 7–8):
- `|D|=1`: SDPO dominate instantly.
- `|D|=128`: SDPO still competitive in-domain, weaker OOD.
- `|D|=512+`: SDPO training score OK nhưng OOD AIME24 drop mạnh.
- `|D|=DAPO (14k)`: SDPO dưới base model ở AIME24.

GRPO ngược lại: càng rộng `|D|`, càng tăng epistemic verbalization, càng improve OOD.

## Vì sao coverage matter

Intuition:
- **Narrow `|D|`**: model gặp pattern tương tự nhiều lần → có thể compress reasoning thành shortcut → confident style OK.
- **Broad `|D|`**: model phải generalize → uncertainty signals giúp maintain alternative hypotheses khi gặp unseen problem → needed.

Paper frame như Bayesian reasoning argument: nếu task pattern đã familiar, prior mạnh, ít cần update belief → epistemic redundant. Ngược lại → epistemic critical.

## Thesis implication

### Regime scope của thesis nằm ở đâu trên axis này?

Test-time SDPO trên LCBv6 hard (19 questions) + very-hard (9 questions):
- `|D| = 1` (mỗi run 1 question).
- Nhưng problem chính nó có *implicit* coverage — solution space của 1 hard code problem rộng.
- Theo Kim framework: nên là regime SDPO win (narrow).

**But**: thesis measure khác với Kim et al. Thesis quan tâm **discovery time** không phải OOD eval. Khác metric khác framework.

### Hypothesis
- H1: Suppression xảy ra (vì task effectively `|D|=1`).
- H2: Suppression **không hurt** discovery trên chính câu đó (consistent with Kim narrow regime).
- H3: Suppression **có thể hurt** nếu evaluate cross-question generalization — thesis có thể thêm "leave-one-out discovery" làm OOD proxy.

### RQ3 connection

Coverage effect khiến **CTC curve** shape khác:
- Narrow: suppression → fewer tokens → lower compute → same correctness → CTC favorable.
- Broad: suppression → fewer tokens → wrong → CTC unfavorable.

[[con_ctc_metric]] phải capture cả hai regime.

## Open questions

- Code task coverage inherent narrower hay broader hơn math? (paper claim code narrow vì LCB 131 only — nhưng LCB mỗi câu có implicit broad solution space.)
- Multi-question test-time SDPO (train 1 câu, test câu khác) — coverage axis thứ 2.
- Template variation có đóng vai trò proxy cho coverage variation? (unclear, probably not — different axis.)

## Links

- [[con_uncertainty_suppression]] · [[con_epistemic_verbalization]]
- [[src_kim2026_why_self_distillation_degrades]]
- [[ent_livecodebench]] (narrow theo Kim framework)
- [[con_test_time_self_distillation]] (1-question regime)
