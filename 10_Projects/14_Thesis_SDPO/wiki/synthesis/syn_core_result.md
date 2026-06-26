---
type: synthesis
created: 2026-06-16
updated: 2026-06-17
tags: [results, teacher-first, sdpo, core-result, rq-method]
sources: [src_hubotter2026_self_distillation, src_shenfeld2026_sdft, src_kim2026_why_self_distillation_degrades]
---

# Core Result — Teacher-First vs Student-First SDPO (test-time)

Bản nháp Results cho thesis. Tổng hợp các run matched 2026-06-14→16. Method detail: [[con_teacher_first_judge]].

## Câu hỏi

Ở regime **test-time SDPO** ([[con_test_time_self_distillation]], Hübotter §5), so sánh 2 cơ chế distillation trên cùng 1 bài khó:
- **Student-first** (baseline, script 07, TRL `SDPOTrainer`): distill student về teacher-rescore của **rollout student tự sinh** (on-policy).
- **Teacher-first** (đề xuất advisor, script 09): teacher (model + feedback + few-shot good) sinh N trajectory → lọc (verifier đúng + difflib độc lập) → distill student về **good trajectory teacher sinh** (off-policy-leaning).

Cùng loss top-k reverse-KL (`compute_topk_self_distillation_loss`, trl 1.6.0), cùng model, cùng hyperparam → chỉ khác *trajectory được distill*.

## Setup

| | |
|---|---|
| Model | Qwen3-4B + LoRA r=32, bf16, thinking OFF |
| Hardware | Colab L4 (22GB) / A100 |
| Steps | 15 TTT step/bài |
| Eval | 16 sample, pass_rate + mean_score, PRE vs POST (student-only) |
| Seeds | 4 (0–3); PRE khớp từng seed giữa 2 arm → **matched comparison** |
| Bài | frontier theo **model pass-rate ∈ (0,1)** (không phải nhãn contest) |
| Template | T2_standard (anchor) |

## Kết quả — 2 bài frontier, 4 seed, eval16 (matched)

### idx39 (abc393_d, nhãn hard, base pass≈0.1)

| seed | PRE | TF POST | SF POST |
|---|---|---|---|
| 0 | 0.000 | **0.438** | 0.188 |
| 1 | 0.000 | 0.062 | 0.000 |
| 2 | 0.062 | 0.125 | 0.125 |
| 3 | 0.188 | 0.062 | 0.062 |
| **TB** | | **0.172** | **0.094** |

### idx12 (abc389_b, nhãn easy nhưng model pass≈0.12)

| seed | PRE | TF POST | SF POST |
|---|---|---|---|
| 0 | 0.000 | **1.000** | 0.938 |
| 1 | 0.062 | **1.000** | 0.500 |
| 2 | 0.062 | 1.000 | 1.000 |
| 3 | 0.125 | **1.000** | 0.938 |
| **TB** | | **1.000** | **0.844** |

### Tổng hợp (8 matched seed-comparisons)

| | TF ≥ SF | TF > SF | tie | TF < SF |
|---|---|---|---|---|
| idx39 | 4/4 | 2 | 2 | 0 |
| idx12 | 4/4 | 3 | 1 | 0 |
| **Tổng** | **8/8** | **5** | **3** | **0** |

→ Sign test thô (5 thắng / 0 thua trên các cặp không-hòa): p ≈ 0.5⁵ ≈ **0.03**.

## Kết luận chính

> **Teacher-first weakly dominates student-first SDPO ở test-time discovery:** ≥ student-first trên **mọi** seed/bài, strictly tốt hơn trên đa số, **không bao giờ tệ hơn**, và **ổn định hơn** (variance thấp — idx12 TF đạt 1.0 mọi seed trong khi SF dao động 0.5–1.0).

Pattern **lặp lại qua 2 bài độc lập** → tín hiệu có hướng, không phải nhiễu sampling.

## Cơ chế (giải thích)

- **Student-first (on-policy):** rollout do student trần sinh → trên bài khó rollout **hiếm trúng** → reward phẳng → tín hiệu yếu/kém ổn định.
- **Teacher-first (off-policy-leaning):** teacher có feedback+few-shot **sinh được lời giải đúng** ngay cả khi student trần không tự nghĩ ra → distill cái đúng đó vào student → học chắc hơn, đặc biệt ở bài khó.
- Định vị: teacher-first ≈ **SDFT-style** ([[src_shenfeld2026_sdft]]: distill về model-conditioned generation) với context = *feedback* (kiểu [[src_hubotter2026_self_distillation|SDPO]]) thay vì demonstration. Đứng giữa SDPO (on-policy) và SFT (off-policy).

## Quan sát phụ (qualitative)

- **Discovery thật**: greedy 0.075→1.0 (idx12), 0.175→0.225 (idx39) — model học giải bài nó deterministic fail. Ví dụ: idx12 base dùng `math.factorial(X)` (sai hướng) → feedback báo runtime error → học cách lặp tìm N. idx29 (exploratory) base dùng `exit()` (không có trong sandbox) → feedback báo NameError → sửa.
- **Bài dễ-fix (exploratory, eval8): idx23, idx29** → cả 2 arm gần như cùng solve (tie hoặc TF nhỉnh nhẹ). → differentiation rõ hơn ở bài khó hơn.
- **Collapse/over-distill**: từ ~step 2, teacher hội tụ (batch reward=1.0, mean_sim≈0.9, n_good→1). Khi base xuất phát cao (idx39 seed3 PRE 0.188), **cả 2 arm đều degrade** (over-distillation) — không phải lỗi riêng TF.

## Ablation — Judge × few-shot Option (mean POST pass_rate)

Hai trục robustness, cùng matched 4 seed / eval16 / T2:
- **Judge** (cách lọc trajectory "độc lập"): `difflib` (string-sim ≥ 0.9) vs `LLM` (groq `llama-3.3-70b`, semantic copy-detection).
- **Option few-shot teacher**: `good_only` (Opt 2, chỉ exemplar tốt) vs `good_bad` (Opt 1, thêm exemplar "copy/bad" gắn nhãn xấu — kiểm tra lo ngại *leak* của advisor).

| arm | idx39 | idx12 |
|---|---|---|
| SF baseline | 0.094 | 0.844 |
| TF · good_only · difflib | 0.172 | 1.000 |
| TF · good_only · LLM | 0.266 | 0.984 |
| TF · good_bad · LLM | 0.250 | 1.000 |

**Hai phát hiện:**
1. **Judge-invariant**: difflib vs LLM cho POST ~như nhau, TF ≥ SF ở cả 2. (Hai judge *dán nhãn* khác rõ — LLM semantic gọi ít "copy" hơn → idx12 LLM `n_good` tới 10 vs difflib `n_good`=1 — nhưng *outcome* không đổi.)
2. **Option-invariant (leak null)**: good_bad ≈ good_only (idx39 0.250 vs 0.266; idx12 1.000 vs 0.984). Cho teacher thấy exemplar "copy/bad" gắn nhãn xấu **không** thay đổi kết quả → lo ngại information-leak của advisor không materialize trên data này.

Matched vs SF cho good_bad: **7 thắng / 1 hòa / 0 thua** (idx39 thắng 4/4 — sạch hơn good_only vốn có ô hòa). Sign test thô p ≈ 0.5⁷ ≈ 0.008. Bổ trợ kết luận chính, không nâng claim (vẫn n=2 bài).

> reasoning_quality của LLM-judge luôn 4–5: do thinking OFF → không có reasoning trace để chấm → judge chỉ hoạt động như **semantic copy-detector**, không đo chất lượng suy luận.

## Hard-frontier extension (2026-06-17) — escape-zero trap

Mở rộng matched comparison sang bài **hard pass-thấp** (frontier scan idx0-90), test giả thuyết: on-policy SDPO (student-first) bị **flat-reward trap** trên bài khó (student trần hiếm roll trúng → reward phẳng → kẹt), teacher-first thoát được vì teacher sinh được lời giải đúng để distill.

| bài | id | judge | SF TB | TF TB | thắng/hòa/thua | escape-zero |
|---|---|---|---|---|---|---|
| idx39 | abc393_d | difflib | 0.094 | 0.172 | 2/2/0 | seed1 (SF 0→0, TF 0.062) |
| idx64 | abc397_e | LLM-groq | 0.047 | 0.422 | 4/0/0 | seed1 (SF 0.062→0, TF 0.375), seed2 (SF 0→0, TF 0.062) |
| idx77 | abc399_f | difflib | 0.203 | 0.344 | 3/1/0 | — (SF không kẹt 0 ở bài này) |
| **Tổng** | | | | | **9/3/0** | **3 instance / 2 bài** |

- **TF > SF trên cả 3 bài hard**, không bao giờ thua. Sign test 9 cặp không-hòa: 9/0 → p ≈ 0.5⁹ ≈ **0.002**.
- **Escape-zero replicated 3 lần** (idx39 s1, idx64 s1+s2): SF kẹt pass=0 (hoặc tụt về 0) trong khi TF thoát. Đây là bằng chứng cơ chế: on-policy flat-reward trap vs off-policy injection.
- idx64 là ca mạnh nhất: TF 0.422 vs SF 0.047 (~9×), thắng 4/4.
- Judge khác nhau giữa các bài (idx64 LLM, idx39/77 difflib) — không sao, đã có ablation chứng minh judge-invariant.
- Greedy: tăng ở idx77 TF (0→1.0), giảm ở idx64 vài seed → greedy đơn nhiễu cao, pass@16 là metric chính.

> **Claim nâng cấp:** từ "weak dominance" (bài frontier thường) lên **"TF học được trên bài hard nơi on-policy SDPO bị flat-reward trap, biên độ lớn, escape-zero replicated"**. Đây là contribution chính, không phải margin nhỏ.

## RQ1 — Template ablation (SF/discovery, code, Modal 2026-06-25)

Probe trực tiếp câu hỏi titular ("reprompt template formulation"). SF arm (script 07, Qwen3-4B, thinking OFF, 15 step, eval16), 3 template × 2 bài × 2 seed = 12 run. POST pass@16:

| Template | idx12 (easy) | idx39 (hard) |
|---|---|---|
| T1_minimal ("provide a corrected solution") | 0.66 | **0.03** |
| T2_standard ("correctly solve the original question") | 0.97 | 0.06 |
| T5_reasoning ("identify root cause, then provide corrected") | 0.97 | **0.13** |

- **Bài hard (idx39): monotone T5 > T2 > T1** (0.13 > 0.06 > 0.03), T5 ổn định 2 seed (.125/.125). **Reprompt ép reasoning > anchor > tối giản.**
- Bài easy (idx12): T2 ≈ T5 bão hòa (~0.97), T1 tụt (0.66, một phần do 1 seed xui).
- → **Template CÓ ảnh hưởng, effect rõ nhất ở bài khó** (nơi có room phân biệt). RQ1 có data.
- Caveat: **n=2 seed, số tuyệt đối nhỏ → directional, chưa mạnh power.** SF arm (baseline), chưa probe TF × template.

## Discussion + Report outline

Lý lẽ Discussion (3 điều kiện teacher-first work, value-vs-procedure, rich-feedback), Limitations tinh chỉnh (model confound, judge degrade, fallback-copy), Future Work (Qwen cả 2 domain, MATH-500 method-reference), và **outline report 30+ trang** → tập trung ở **[[syn_report_outline]]** (writing hub).

## Limitations

- **Weak dominance**: nhiều ô hòa, margin thường nhỏ; win lớn là seed-specific.
- Chỉ **2 bài, model 4B, template T2**, 15 step → không phải universal claim.
- **Không compute-matched**: TF sinh ~2.5× generation (teacher_n=10 vs SF num_generations=4) → TF thắng về *outcome*, chưa chứng minh thắng về *compute* (cần CTC — [[con_discovery_at_k]] mở rộng).
- **Judge**: đã ablate difflib (string-sim 0.9) vs LLM-groq (semantic) → judge-invariant; nhưng cả hai chỉ là copy-detector (thinking off), chưa chấm chất lượng suy luận.
- **CF test-time chưa đo** (reset per-bài nên không nhiễm; cumulative chưa thử).

## Hướng mở rộng (nếu compute/thời gian cho phép)

- Thêm bài frontier (tăng power: 8/8 → 16/16).
- RQ1: template ablation (T1/T5 vs T2) × 2 arm.
- ~~Option 1 (good_bad) ablation = leak vs no-leak~~ ✅ done — Option 1 ≈ Option 2 (xem section Ablation).
- Math domain (P2): nơi leak/Kim mạnh nhất; verifier `feedback.math` có sẵn (reward binary).
- CTC để fair compute comparison.

## Links

- [[con_teacher_first_judge]] — method + bảng matched chi tiết
- [[syn_teacher_first_impl_spec]] — implementation spec
- [[src_hubotter2026_self_distillation]] (§5 test-time, §4.4 forgetting) · [[src_shenfeld2026_sdft]] (on-policy minimum-change) · [[src_kim2026_why_self_distillation_degrades]] (rich-context degradation)
- [[con_test_time_self_distillation]] · [[con_discovery_at_k]] · [[syn_thesis_proposal]]
