---
type: concept
created: 2026-06-14
updated: 2026-06-14
tags: [sdpo, teacher-first, information-leak, few-shot, judge, rq2, method, advisor-idea]
sources: [src_hubotter2026_self_distillation, src_kim2026_why_self_distillation_degrades]
---

# Teacher-First Judge-Filtered Self-Distillation

Idea method do **advisor đề xuất 2026-06-14**, trong buổi gặp + trao đổi sau đó. Đây là một biến thể của [[ent_sdpo]] nhằm tránh **information leak** — bổ sung một *method contribution* cho thesis vốn đang thiên về empirical (RQ1 template). Nối thẳng vào vấn đề degradation mà [[src_kim2026_why_self_distillation_degrades]] chẩn đoán.

## Vấn đề: information leak trong SDPO gốc

SDPO gốc (student-first): student sinh `y_student` (thường sai) → teacher `π(·|x, f)` (với `f` = feedback, có thể chứa **sample solution**) rescore từng token của `y_student` → student bị kéo về teacher qua KL.

Nếu `f` chứa reference solution, teacher rescore theo hướng "gần reference" → student học **chép reference** thay vì học **tư duy**. Qua nhiều test-time step → student converge về copy → "chả còn gì để học" (lời advisor). Đây chính là degradation từ rich context mà Kim et al. mô tả (`I(y;c|x)` cao → suppression).

## Flow teacher-first (chốt 2026-06-14)

```
1. Teacher(x, f) → sinh N trajectory {y_t1...y_tN}   [temperature cao → diverse]
2. Judge / verifier → gán nhãn good / bad cho mỗi y_ti:
      bad : y_ti ≈ sample_sol (chỉ copy reference)
      good: y_ti đúng (pass) VÀ độc lập với reference
3. Few-shot: đưa exemplar trở lại PROMPT của teacher (in-context, KHÔNG train teacher):
      Option 1: good + bad (kèm label) — contrastive ("đừng như bad, hãy như good")
      Option 2: chỉ good               — positive-only
4. Teacher (đã few-shot steer) → sinh trajectory tốt hơn
5. Student học bằng KL divergence trên y_good:
      KL( π_student(·|x, y<t) || stopgrad π_teacher(·|x, f, y<t) )   trên y_good
6. Lặp — pool good tích lũy dần qua step
```

**Thay đổi cốt lõi so với SDPO gốc:** KL tính trên `y_good` (teacher tự sinh, đã lọc), **không** phải `y_student` (attempt thất bại của student).

**Xác nhận với advisor:**
- Student **vẫn** học bằng KL distillation từ distribution của teacher (không đổi).
- Few-shot chỉ để **cải thiện teacher** (in-context), không thay cơ chế học của student.
- **Thử cả Option 1 và Option 2** (thành một ablation).

## Few-shot teacher improvement = "dạy teacher thế nào là đúng"

Đưa trajectory đã phân loại vào prompt teacher kiểu [[con_reprompt_template|few-shot]] để steer teacher generation. Đây **không** train teacher (không gradient) — chỉ in-context learning.

| | Option 2 (good only) | Option 1 (good + bad + label) |
|---|---|---|
| Cơ chế | positive few-shot | contrastive few-shot |
| Sức steer | vừa | mạnh hơn |
| **Leak** | **sạch** ✅ | **rò dư** ⚠️ |

**Phân tích leak (quan trọng):**
- `good` đã qua lọc = độc lập reference → đưa vào prompt **không** mang reference vào context → no-leak. Đây tương đương **Variant A** (clean).
- `bad ≈ reference` → Option 1 đưa bad vào prompt = đưa nội dung giống reference trở lại context (dù dán nhãn "bad") → teacher *thấy* reference → **leak dư**.

→ Option 2 = no-leak; Option 1 = steer mạnh hơn nhưng đánh đổi leak. Ablation Option 1 vs 2 đồng thời là ablation **leak vs no-leak**.

## Hai domain: code + math

| | Verifier có sẵn? | Reward | Feedback "giàu" |
|---|---|---|---|
| **Code** (LCBv6) | ✅ `verl...reward_score.feedback.code` | **partial** (tỉ lệ test pass) | execution trace, test fail |
| **Math** (MATH) | ✅ `verl...reward_score.feedback.math` (drop-in sibling) | **binary** (0/1) | mỏng — mặc định chỉ format error |

**2 phát hiện về math (đọc từ `feedback/math.py`):**

1. **Reward nhị phân (0/1).** `reward = 1.0 if correct else 0.0`. → flat-reward/collapse nặng hơn code; **chỉ có variance khi bài model giải đúng ~30–70%** → problem selection ở math khắt khe hơn.

2. **"Rich feedback" math = đọc luôn đáp án.** Khi `correctness_feedback=True`: `feedback = "...The correct answer is {ground_truth}."` → leak ở dạng cực đoan nhất (chỉ việc chép `\boxed{}`). → **math là case mạnh nhất để chứng minh cả vấn đề leak lẫn cách chữa** (teacher-first + filter). Baseline student-first + correctness_feedback sẽ copy đáp án rõ ràng → "có bệnh" để chứng minh teacher-first "chữa" → điều kiện cần cho claim contribution tới [[src_kim2026_why_self_distillation_degrades|Kim]].

## Ma trận thí nghiệm

| | Student-first (baseline) | Teacher-first (contribution) |
|---|---|---|
| **Code** | ✅ pilot xong (idx 19/23) | ⬜ build |
| **Math** | ⬜ baseline tối thiểu (cần cho claim Kim) | ⬜ build |

- Student-first math = "có bệnh" (degrading baseline) để đối chứng — **bắt buộc** nếu muốn claim contribution Kim, không chỉ "teacher-first chạy được".
- Teacher-first chạy **cả 2 domain** → chứng minh method generalize cross-domain.

## Metrics (nối RQ2 / Kim)

- **pass-rate / discovery@k** — hiệu năng ([[con_discovery_at_k]]).
- **similarity-to-reference** — đo "có chép không" (độc lập = thấp). Đây là cách *measure* được "copy=bad" của advisor.
- **uncertainty markers** — [[con_uncertainty_suppression]] / [[con_epistemic_verbalization]], đo suppression qua step.

→ "copy=bad" đo bằng similarity; suppression đo bằng markers → cả hai = **RQ2**.

## Implementation gotchas

1. **Cold-start (chicken-egg):** step 1 chưa có good nào → pool few-shot rỗng → cần vòng "mồi" (sinh trần, lọc) trước. Trên bài khó model hiếm ra good → pool có thể mãi rỗng → sập. Rủi ro same-model-on-hard (giống bức tường idx 9).
2. **Context length:** trajectory (code ~400–500 token, math+thinking dài hơn) nhét vào prompt few-shot → ngốn budget nhanh → canh `max_prompt_length` / số exemplar.
3. **Problem selection:** chọn bài model giải đúng ~30–70% (frontier) — nhất là math (binary reward).
4. **Similarity threshold + log survivor count:** ngưỡng lọc phải điều chỉnh được; log "bao nhiêu good sống sót mỗi step" để phát hiện pool rỗng sớm.

## Liên hệ với phần đã có

- **RQ1 template không mất:** teacher vẫn nhận `f` để sinh → [[con_reprompt_template]] vẫn áp cho teacher rollout. Pool good tích lũy = đúng dimension **memory depth** (T7) trong [[syn_template_taxonomy_rationale]].
- **Pipeline tái dùng:** script `07_discovery_curve.py` (student-first) làm baseline; teacher-first cần custom loop (TRL `SDPOTrainer` làm student-first ở trong → phải tự wrap hoặc hack).

## Quyết định đã chốt vs còn treo

**Chốt (2026-06-14):**
- Student học bằng KL (không đổi); few-shot chỉ cải thiện teacher.
- Thử cả Option 1 (good+bad+label) và Option 2 (good only).
- Teacher-first chạy cả code + math; student-first math làm baseline đối chứng.

**Còn cân nhắc khi build:**
- Judge = LLM judge thật, hay thay bằng **verifier (đúng/sai) + similarity (độc lập)** cho rẻ & sạch? (nghiêng cái sau vì code/math đã có verifier; LLM judge chỉ cần nếu muốn chấm "reasoning quality").
- Variant A (teacher KHÔNG thấy reference lúc distill) đã được Option 2 đáp ứng tự nhiên.

## Scope / timeline

Còn ~4 tuần tới submission (2026-07-11). Đây là **3 trục mới cùng lúc** (teacher-first method + math domain + RQ2 metric) chồng lên RQ1. Ưu tiên:
- **P0:** teacher-first vs student-first trên **code**, 1–2 bài frontier, vài seed.
- **P1:** một dataset math (MATH level 3–4), so sánh 2 arm → cross-domain + claim Kim.
- **P2:** template grid × 2 arm, RQ2 suppression đầy đủ.

## First result — P0 idx23 (2026-06-14)

Pipeline verified end-to-end (Qwen3-4B, A100, 15 steps, T2, good_only, best_in_batch). KL-sanity `KL(token-mean)=0.200`, token alignment correct (L=469 hai bên dù prefix khác nhau).

| | pass_rate | mean_score |
|---|---|---|
| **Teacher-first** (09) | 0.500 → **1.000** (+0.500) | 0.819 → **1.000** (+0.181) |
| Student-first (07, T2) | 0.500 → 0.750 (+0.250) | 0.819 → 0.909 (+0.091) |

→ Teacher-first ~gấp đôi Δ, nhưng **chưa kết luận được** (xem caveat).

**4 caveat (quan trọng, đừng overclaim):**
1. 1 seed / 1 bài / eval n=8 → chưa có ý nghĩa thống kê.
2. **Không compute-matched** — teacher_n=10 → ~2.5× generations vs 07 (num_generations=4); một phần "thắng" có thể do nhiều mẫu hơn → cần **CTC (RQ3)**.
3. **Hội tụ nhanh** — từ step 2: batch_r=1.0, mean_sim≈0.9, n_good kẹt ở 1 (diversity collapse) → anti-copy filter gần như không bị thử; idx23 quá dễ.
4. greedy không đổi (1.0→1.0) → cải thiện là **độ tin cậy**, không phải **discovery**.

→ Hệ quả: comparison nghiêm túc cần **bài frontier khó hơn** (pass ~0.15–0.45, không hội tụ step 2) + **≥2 seed** + **log total generations cho CTC**. idx23 chạm trần, chỉ dùng để verify pipeline.

## Matched result — idx39 hard (2026-06-16) ⭐ core result

Frontier problem idx39 (abc393_d, hard, base pass≈0.1). **Both arms × 4 seeds × eval16** on L4, Qwen3-4B, 15 steps, T2. PRE khớp từng seed (cùng base+seed) → so sánh sạch.

| seed | PRE | TF POST | SF POST | TF−SF |
|---|---|---|---|---|
| 0 | 0.000 | **0.438** | 0.188 | +0.250 |
| 1 | 0.000 | 0.062 | 0.000 | +0.062 |
| 2 | 0.062 | 0.125 | 0.125 | 0 |
| 3 | 0.188 | 0.062 | 0.062 | 0 |
| **TB** | | **0.172** | **0.094** | **+0.078** |

- **Teacher-first ≥ student-first ở CẢ 4 seed**, strictly > 2/4. Mean POST ~1.8×, mean Δ ~3.5× (TF +0.109 vs SF +0.031). → **weak dominance, có hướng, không phải noise.**
- **seed3 (PRE cao 0.188): CẢ HAI degrade** y hệt → over-distillation khi base đã khá, áp cho cả hai arm như nhau (không phải lỗi riêng TF).
- Caveat: **1 bài**, gain khiêm tốn + nhiễu → cần ≥1 bài hard nữa để confirm generalize. Đây là "weak dominance" không phải blowout.

## Matched result — idx12 (2026-06-16) + tổng 2 bài

idx12 (abc389_b, nhãn "easy" nhưng **model pass=0.12** → model-hard). 4 seed × eval16, PRE khớp.

| seed | PRE | TF POST | SF POST | TF−SF |
|---|---|---|---|---|
| 0 | 0.000 | 1.000 | 0.938 | +0.062 |
| 1 | 0.062 | 1.000 | 0.500 | +0.500 |
| 2 | 0.062 | 1.000 | 1.000 | 0 |
| 3 | 0.125 | 1.000 | 0.938 | +0.062 |
| **TB** | | **1.000** | **0.844** | +0.156 |

→ TF **1.0 mọi seed** (rock-solid); SF dao động (seed1=0.5). TF ≥ SF cả 4, strictly > 3/4.

### Tổng hợp 2 bài × 4 seed = 8 so sánh matched

| | TF≥SF | TF>SF | tie | TF<SF |
|---|---|---|---|---|
| idx39 (hard) | 4/4 | 2 | 2 | 0 |
| idx12 (model-hard) | 4/4 | 3 | 1 | 0 |
| **Tổng** | **8/8** | **5** | **3** | **0** |

→ **Teacher-first ≥ student-first ở CẢ 8 seed, strictly > 5/8, KHÔNG bao giờ thua** + ổn định hơn (variance thấp). Pattern **lặp qua 2 bài độc lập** → không phải nhiễu (sign test thô 5–0, p≈0.03).

**Core conclusion thesis:** *"Teacher-first weakly dominates student-first SDPO ở test-time discovery — ≥ mọi seed/bài, thường hơn, không bao giờ tệ hơn, variance thấp hơn."* Cơ chế: TF off-policy-leaning bơm solution đúng từ teacher → student học chắc/ổn hơn SF (on-policy, kém ổn khi rollout hiếm trúng).

**Caveat:** weak dominance (nhiều hòa, margin nhỏ); 2 bài / 4B / chỉ T2; TF tốn ~2.5× generation (CTC caveat — thắng *outcome* không phải *compute*); idx12 nghiêng fixable-bug → margin nhỏ.

## Judge ablation — difflib vs LLM (2026-06-16)

LLM-judge implemented (provider chain: groq `llama-3.3-70b` primary + gemini fallback + difflib final; cache, retry, key-presence filter). **Gemini free tier = 20 req/DAY** → quá thấp cho matrix → groq làm primary. All 8 runs clean (`judge_fallbacks=0` = toàn groq).

**good_only, mean POST pass (4 seed):**

| Bài | Student-first | TF difflib | TF LLM(groq) |
|---|---|---|---|
| idx39 | 0.094 | 0.172 | 0.266 |
| idx12 | 0.844 | 1.000 | 0.984 |

- **TF ≥ SF ở cả 2 bài, cả 2 judge** → core result **robust với judge choice**.
- difflib vs LLM: POST student ~như nhau (idx12 ~1.0 cả hai; idx39 cùng ballpark, LLM nhỉnh trong nhiễu). → **judge-invariant**.
- **Nhưng 2 judge dán nhãn KHÁC nhau rõ:** LLM (ngữ nghĩa) gọi ÍT copy hơn difflib (chuỗi sim≥0.9) → idx12 LLM giữ `n_good` tới 10 vs difflib `n_good=1`. Labeling khác nhưng outcome không đổi (distill bị chi phối bởi correctness + collapse, không phải ranh giới copy).
- `reasoning_quality` luôn 4–5 (cả gemini lẫn groq) + thinking off → judge = **semantic copy-detector**, KHÔNG đo reasoning. Đừng claim "đo reasoning quality" khi viết.

**Kết luận ablation:** kết quả teacher-first bất biến với (a) judge choice (difflib/LLM) — chưa test good_bad nhưng kỳ vọng cũng invariant. Đây là robustness finding, 1 đoạn trong thesis.

## Links

- [[ent_sdpo]] · [[con_self_teacher]] · [[con_reprompt_template]] · [[con_test_time_self_distillation]]
- [[con_uncertainty_suppression]] · [[con_epistemic_verbalization]] · [[con_discovery_at_k]]
- [[src_hubotter2026_self_distillation]] (§7 future work: behavioral differences; §4.6 feedback type) · [[src_kim2026_why_self_distillation_degrades]] (degradation từ rich context)
- [[syn_template_taxonomy_rationale]] (memory depth = pool good) · [[syn_implementation_status]]
- [[src_lasgroup_sdpo_repo]] (verifier code/math; teacher loop tự build)
