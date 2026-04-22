---
type: concept
created: 2026-04-22
updated: 2026-04-22
tags: [template, prompting, core-thesis, rq1]
sources: [src_hubotter2026_self_distillation, src_kim2026_why_self_distillation_degrades]
aliases: [teacher reprompt template, SDPO template]
---

# Reprompt template

Cấu trúc prompt dùng để build context cho [[con_self_teacher]]. Quyết định **feedback nào** được include và **cách trình bày** để teacher retrospectively evaluate student's attempt.

Đây là **trung tâm RQ1 của thesis** — paper chỉ test syntactic variation, thesis làm systematic template taxonomy.

## Template gốc của paper (Table 2)

```
User: <prompt>
Correct solution:
<successful_previous_rollout>     # [optional] nếu có sample solution
The following is feedback from your unsuccessful earlier attempt:
<environment_output>               # [optional] nếu attempt fail
Correctly solve the original question.
Assistant: <original_response>     # dùng để re-evaluate log-probs
```

Các slot:
- `prompt` — question gốc.
- `successful_previous_rollout` — nếu batch có success cùng question. Skip nếu không.
- `environment_output` — runtime output từ attempt. Skip nếu success.
- `original_response` — **luôn là student's attempt** để teacher compute log-prob trên đúng token đó.

## Paper findings về template

### §4.6 (feedback ablation — Table 6)

Đã discuss ở [[con_rich_feedback]]. Tóm:
- Env output + own solution: **tốt nhất** (48.3%).
- Include `y` trong teacher context: giảm diversity, biased toward student's attempt.

### §4.6 note quan trọng

> *"performance is not sensitive to syntactic variations of the reprompting template"*

→ Paper test wording/format microvariation, không tìm thấy khác biệt lớn. NHƯNG:

## Những gì paper **không** test (= opening cho thesis)

1. **Structural variation** (macro): thứ tự slots, số lượng feedback included, format (JSON vs markdown vs XML), v.v.
2. **Instruction variation**: "Correctly solve..." vs "Identify your mistake..." vs "Explain why...".
3. **Chain-of-thought prompt** trong teacher context.
4. **Negative instruction** ("Do not repeat the mistake above").
5. **Uncertainty elicitation** ("Rate confidence before answering").
6. **Behavior impact**: template có thay đổi [[con_epistemic_verbalization]], response length, hedging language không?
7. **Test-time context**: paper chỉ test train-time templates.

## Template là suppression lever (Kim et al. 2026 framing)

[[src_kim2026_why_self_distillation_degrades]] cho thấy `I(y; c|x)` — information richness của teacher context — quyết định mức độ [[con_uncertainty_suppression]].

Template **là cái chứa `c`** → template design = knob trực tiếp điều khiển suppression.

Kim et al. test 4 điểm trên spectrum `I`:
- `c = ∅` (no suppression).
- `c = s\think` (mid).
- `c = ỹ` (mid-high).
- `c = s` (max suppression).

**Gap**: họ chỉ vary *what goes into c*, không vary *how c is formatted/framed*. Thesis taxonomy có thể giữ content roughly constant nhưng vary:
- **Phrasing**: "Correctly solve" vs "Identify your mistake" vs "Rate your confidence first".
- **Ordering**: feedback-first vs solution-first.
- **Explicit uncertainty elicitation**: "Before answering, note any uncertainty."

→ Nếu template có thể **preserve epistemic tokens** mà vẫn deliver credit signal, đó là contribution đáng kể.

## Thesis RQ1 scope

Thesis sẽ:
1. Build **template taxonomy** (7 variants theo thesis proposal).
2. Test test-time discovery efficiency trên [[ent_livecodebench]] hard/very-hard.
3. Measure không chỉ accuracy mà còn [[con_code_uncertainty_signals]], response length, iteration count.
4. Connect to RQ2 (suppression) và RQ3 ([[con_ctc_metric]]).

## Dimensions để design taxonomy

Gợi ý initial taxonomy:

| Dimension | Options |
|---|---|
| Feedback ordering | output first / solution first / interleaved |
| Instruction framing | neutral / diagnostic / confidence-elicit |
| Solution present | yes / no / partial |
| Student attempt visibility | yes / no / masked |
| Reasoning scaffold | none / CoT / "think step by step" |

## Links

- [[ent_sdpo]] · [[con_self_teacher]] · [[con_rich_feedback]]
- Thesis RQs: RQ1 primary, RQ2 secondary (template × suppression), RQ3 secondary (template × CTC).
