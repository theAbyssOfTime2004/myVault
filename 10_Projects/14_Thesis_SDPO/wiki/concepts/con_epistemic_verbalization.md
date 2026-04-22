---
type: concept
created: 2026-04-22
updated: 2026-04-22
tags: [reasoning, uncertainty, behavior, core-thesis, rq2]
sources: [src_kim2026_why_self_distillation_degrades, src_kim2026_strategic_info_allocation]
aliases: [epistemic verbalization, uncertainty expression, epistemic tokens]
---

# Epistemic verbalization

Hiện tượng LLM **verbal hóa uncertainty** trong quá trình reasoning bằng các tokens/phrase đặc trưng. Từ Kim et al. 2026 ([[src_kim2026_strategic_info_allocation]], original). Applied to SD analysis trong [[src_kim2026_why_self_distillation_degrades]].

Đây là **central variable của RQ2**.

## Definition operational (Kim et al. 2026)

10 epistemic markers tracked:
```
T = {wait, hmm, perhaps, maybe, actually, alternatively,
     seems, might, likely, check}
```

Metric: `E(y) = Σ_{t ∈ T} count(t, y)` — đếm occurrences trong response.

Tokens này không trực tiếp advance reasoning nhưng **signal rằng model đang giữ alternative hypotheses** hoặc doubt current direction.

## Vì sao quan trọng

### Self-Bayesian reasoning framing

LLM reasoning = iterative belief update. Mỗi step condition trên problem + previous tokens, model update belief over intermediate hypotheses.

- Không có epistemic verbalization → **commit sớm** vào hypothesis sai, ít cơ hội recover.
- Có epistemic verbalization → **maintain alternatives**, gradual uncertainty reduction.

### Evidence empirical

DeepSeek-R1 và các reasoning model mạnh **thường xuyên** express uncertainty. Ablation remove những token này → performance drop significant (Kim et al. 2026 strategic info paper).

Figure 2 của [[src_kim2026_why_self_distillation_degrades]]: "Reasoning without signals leads to premature commitment."

## Suppression qua self-distillation

Phát hiện chính của [[src_kim2026_why_self_distillation_degrades]]:

Teacher có access rich context `c` (solution) → không cần express uncertainty → generate concise confident responses. Student minimize KL với teacher → học imitate confident style → suppress epistemic verbalization.

Đặc biệt xấu khi:
- Student không có `c` lúc inference.
- Task coverage rộng (diverse OOD problems).

→ Xem [[con_uncertainty_suppression]] cho mechanism, [[con_task_coverage]] cho scaling.

## Quantitative findings (Table 1, §3)

Response length và epistemic count tỉ lệ nghịch với `I(y;c|x)`:

| Context `c` | Avg epistemic count |
|---|---|
| ∅ (unguided) | **182.5** |
| `s\think` | 159.8 |
| `ỹ` (regeneration) | 24.1 |
| `s` (full solution) | **8.8** |

Drop 20× khi teacher có full context.

## Test-time code bối cảnh (RQ2)

Thesis cần:
1. **Define epistemic tokens cho code**: "wait/hmm" generic hay code-specific như try/except, assert, `# verify`, defensive branching? Xem [[con_code_uncertainty_signals]] (stub).
2. **Measure evolution** qua iterations của test-time SDPO: monotonic suppress hay non-monotonic?
3. **Connect to discovery**: responses ít epistemic có discover faster không? Hay discover fewer?

## Open questions cho thesis

- Kim et al. đo trên math (AIME/MATH500). Code có pattern khác không — có thể structured syntax đã "implicit uncertainty" qua guard clauses.
- Test-time 1-question setup: suppression có xảy ra không khi chỉ train 1 câu? Hay loop quá ngắn để manifest?
- Template có thể **preserve** epistemic verbalization? (RQ1 × RQ2 intersection)

## Links

- [[con_uncertainty_suppression]] · [[con_task_coverage]] · [[con_code_uncertainty_signals]]
- [[src_kim2026_why_self_distillation_degrades]] · [[src_kim2026_strategic_info_allocation]]
- [[ent_sdpo]] (method nơi suppression xảy ra)
