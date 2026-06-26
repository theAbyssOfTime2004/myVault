---
type: report
created: 2026-06-26
updated: 2026-06-26
tags: [report, chapter, method, sdpo, teacher-first]
sources: [src_hubotter2026_self_distillation, src_kim2026_why_self_distillation_degrades, src_shenfeld2026_sdft, src_lasgroup_sdpo_repo, src_trl_sdpo_sdft_docs]
---

# Chương 3 — Phương pháp

Chương này đặc tả phương pháp ở mức đủ để tái lập (reproduce). Đối tượng nghiên cứu chính là **test-time SDPO** [1, §5]: cố định một bài toán khó, cho mô hình tự cải thiện trong một số bước huấn luyện tại thời điểm suy luận (test-time training, TTT), và đo khả năng *khám phá* (discovery) lời giải. Trong regime đó, luận văn so sánh hai cách tổ chức self-distillation — **student-first** (baseline của paper gốc [1]) và **teacher-first** (biến thể do người hướng dẫn đề xuất) — rồi khảo sát ảnh hưởng của reprompt template (RQ1).

Phạm vi domain: **code generation là lõi** (LiveCodeBench v6 [6]); **math là pilot/contrast** (AIME 2026 [10]), dùng để đặc trưng hoá *biên* của cơ chế chứ không phải để chứng minh nó hoạt động ở mọi nơi. Sự phân vai này được giữ nhất quán xuyên suốt: mọi thiết lập math đều mang theo caveat domain/model tương ứng (xem §3.5 và Chương 6).

Toàn bộ ký hiệu mirror theo paper cha Hübotter et al. [1] để người đọc đối chiếu trực tiếp.

---

## 3.1 Tổng quan pipeline test-time SDPO

### 3.1.1 Ký hiệu và setting

Cho một bài toán $x$ (problem statement). Gọi:

- **Student** $\pi_\theta(\cdot \mid x)$ — policy gốc, chỉ thấy đề bài.
- **Self-teacher** $\pi_\theta(\cdot \mid x, c)$ — *cùng* mô hình (cùng tham số $\theta$), nhưng được condition thêm **privileged context** $c$. Trong SDPO, $c$ đóng vai trò "feedback" $f$ của paper gốc: thông tin retrospective (lỗi runtime, test fail, hoặc lời giải mẫu) cho phép mô hình "nhìn lại" và xác định chỗ sai [1, §2].

Đây là **self**-distillation: teacher và student chia sẻ trọng số; điều duy nhất phân biệt là context đầu vào. Mô hình học bằng cách kéo phân phối next-token của student về phân phối (đã được điều kiện hoá trên $c$) của teacher.

Setting test-time [1, §5]: với mỗi bài $x$, mô hình được reset về checkpoint nền, rồi chạy $K$ bước TTT *chỉ trên bài đó*. Reward là verifiable — graded (code) hoặc binary (math). Mục tiêu không phải generalize sang bài khác mà là **discover** lời giải cho chính $x$ càng sớm càng tốt; metric là discovery@k [1, Def. 5.1] (§3.6).

### 3.1.2 Vòng lặp chung

Hai arm (student-first / teacher-first) chia sẻ cùng một khung; **khác biệt duy nhất là *trajectory nào được đem đi distill***. Khung chung:

```
nạp base model + LoRA + optimizer (AdamW, lr = 1e-5)
PRE-eval (chỉ student π_θ(·|x), N_eval mẫu)         # đo baseline
for step in 1..K:
    feedback ← build_feedback(student attempt, verifier)   # rich feedback
    {trajectories} ← generate(...)                          # arm-specific
    {distill_targets} ← select(...)                         # arm-specific (lõi khác biệt)
    if distill_targets ≠ ∅:
        θ ← θ − lr · ∇_θ  L_KL(distill_targets)             # 1 optimizer step
    log step stats → W&B
POST-eval (chỉ student π_θ(·|x), N_eval mẫu)         # đo sau TTT
report PRE→POST, discovery curve
```

**Figure 3.1** — Sơ đồ hai arm (khác nhau ở khối tô đậm):

```mermaid
flowchart TD
    X[Bài toán x] --> S[Student π_θ·|x]
    X --> T[Self-teacher π_θ·|x,c]
    subgraph SF[Student-first - baseline]
      S -->|rollout on-policy| YS[y_student thường sai]
      YS -->|teacher rescore per-token| KLS[KL distill trên y_student]
    end
    subgraph TF[Teacher-first - đề xuất]
      T -->|sinh N trajectory| YT[y_t1..y_tN]
      YT -->|verifier + judge lọc| G[good pool y_good]
      G -->|KL distill trên y_good| KLT[KL distill trên y_good]
    end
    KLS --> U[update θ]
    KLT --> U
```

Khác biệt cốt lõi giữa hai arm gói gọn ở một câu: **student-first distill trên *attempt thất bại của student*, teacher-first distill trên *trajectory đúng do teacher sinh ra và đã được lọc***. Phần còn lại (loss, model, hyperparam) giữ giống nhau để cô lập đúng biến này.

---

## 3.2 Student-first SDPO (baseline, on-policy)

Đây là thuật toán gốc của Hübotter et al. [1], hiện thực qua `SDPOTrainer` của TRL [5] (script `07_discovery_curve.py`).

**Cơ chế.** Tại mỗi bước, student tự sinh rollout $y \sim \pi_\theta(\cdot \mid x)$ (on-policy). Verifier chấm $y$ và sinh feedback $f$. Self-teacher $\pi_\theta(\cdot \mid x, f)$ rescore *từng token* của chính $y$ đó — tức teacher trả lời câu hỏi "nếu đã biết $f$, thì ở mỗi vị trí token, phân phối đúng đáng lẽ là gì". Student bị kéo về phân phối retrospective này qua KL:

$$
\mathcal{L}_{\text{SDPO}}(\theta) \;=\; \sum_{t=1}^{|y|} \mathrm{KL}\!\Big(\pi_\theta(\cdot \mid x, y_{<t}) \;\big\|\; \mathrm{stopgrad}\,\pi_\theta(\cdot \mid x, f, y_{<t})\Big),
$$

với `stopgrad` chặn gradient qua teacher (ngăn teacher collapse về student để "phớt lờ" $f$) [1, §2]. Chi tiết gradient và xấp xỉ top-K xem §3.3.5 (dùng chung cho cả hai arm).

**Chế độ thất bại trên bài khó (đặt nền cho escape-zero).** Vì rollout là on-policy, trên bài mà student *trần* hiếm khi sinh trúng, hầu hết rollout đều sai → feedback nghèo, tín hiệu distill yếu và kém ổn định. Đây là **flat-reward trap**: không có rollout đúng để học từ đó. Hübotter et al. [1, §5] cho thấy SDPO vẫn iterate được nhờ rich feedback ngay cả khi teacher accuracy ban đầu <1%, nhưng *trên mô hình 4B yếu hơn* (xem §3.5) hiện tượng kẹt-ở-0 vẫn xuất hiện — chính là điểm mà teacher-first nhắm tới.

---

## 3.3 Teacher-first SDPO (đề xuất)

### 3.3.1 Động cơ

Hai vấn đề của student-first thúc đẩy biến thể này:

1. **Flat-reward trap** (§3.2): khi student không tự roll trúng, không có gì "đúng" để distill.
2. **Information leak** [2]: nếu $c$ chứa lời giải mẫu, teacher rescore theo hướng "gần reference" → qua nhiều bước test-time, student converge về *chép* reference thay vì học *cách tư duy*. Kim et al. [2] formalize: khi $I(y; c \mid x)$ (độ giàu thông tin của context) cao, mô hình **suppress epistemic verbalization** và degrade.

**Thay đổi cốt lõi.** Teacher-first **đảo thứ tự**: *teacher sinh trước*, lọc lấy trajectory đúng-và-độc-lập, rồi distill student về *chúng*. KL được tính trên $y_{\text{good}}$ (teacher sinh, đã lọc), không phải $y_{\text{student}}$ (attempt thất bại):

$$
\mathcal{L}_{\text{TF}}(\theta) \;=\; \sum_{y \in \mathcal{G}} \; \sum_{t=1}^{|y|} \mathrm{KL}\!\Big(\pi_\theta(\cdot \mid x, y_{<t}) \;\big\|\; \mathrm{stopgrad}\,\pi_\theta(\cdot \mid x, c, y_{<t})\Big),
$$

với $\mathcal{G}$ = good pool (§3.3.3). Về định vị, teacher-first nằm **giữa SDPO (on-policy) và SFT (off-policy)**: nó giống SDFT [3] ở chỗ distill về generation do chính mô hình (đã được điều kiện hoá) sinh ra, nhưng context là *feedback* kiểu SDPO [1] chứ không phải demonstration cố định.

Vì `SDPOTrainer` hard-code rollout student-first bên trong, teacher-first được hiện thực bằng **custom training loop** (script `09_teacher_first.py`), tái dùng các helper của `07` (`build_privileged_context`, `build_dynamic_feedback`, `evaluate_solution`, eval).

### 3.3.2 Teacher rollout + privileged context

Mỗi bước, teacher sinh $N$ trajectory (`teacher_n`) ở nhiệt độ cao để đa dạng:

$$
\{y_{t_1}, \dots, y_{t_N}\} \sim \pi_\theta(\cdot \mid x, c), \qquad c = \underbrace{f}_{\text{feedback}} \;+\; \underbrace{\text{few-shot exemplars}}_{\text{§3.3.4}}.
$$

`privileged_context` $c$ = hiện thực cụ thể của "feedback" trong [1] (tên gọi là của codebase luận văn; khái niệm là của paper). Nội dung $c$ phụ thuộc domain (§3.5). Few-shot block được chèn *trước* directive cuối ("Respond with ONLY…"), giới hạn `max_fewshot = 3` exemplar để không vỡ context; token count được log mỗi bước.

### 3.3.3 Verifier + LLM judge → good pool

Mỗi trajectory $y_{t_i}$ được gán nhãn qua hai tầng:

**Tầng 1 — Verifier (correctness).**

- **Code** (LCBv6): `evaluate_solution` chạy public/private tests → score = *tỉ lệ test pass* ∈ [0,1] → reward **graded** (có gradient để leo, ví dụ 0.21 → 1.0).
- **Math** (AIME): so khớp đáp án → reward **binary** {0,1}.

**Tầng 2 — Judge (independence / copy-detection).** Đo $y_{t_i}$ có *chép* reference không:

$$
\text{good} := (\text{score} \ge 1.0) \,\wedge\, (\text{independent}), \qquad \text{bad} := (\text{copy reference}).
$$

Hai hiện thực judge (được ablate, §4.4):

| Judge | Cơ chế | Chi phí |
|---|---|---|
| `difflib` | `SequenceMatcher` string-sim trên code đã normalize (strip comment/whitespace); copy nếu sim ≥ ngưỡng (≈0.9) | rẻ, deterministic |
| LLM | groq `llama-3.3-70b` (code) / `glm-4.5-flash` (math), prompt derive-vs-copy → trả `is_copy` + `reasoning_quality` 1–5 | tốn API, semantic |

> **Lưu ý trung thực (không overclaim):** với thinking OFF (code) không có reasoning trace để chấm, `reasoning_quality` bão hoà ở 4–5. Do đó LLM judge ở đây vận hành thuần tuý như **semantic copy-detector**, *không* phải bộ chấm chất lượng suy luận. Luận văn không claim "đo reasoning quality".

**Fallback "keep-best-correct" và rủi ro của nó.** Khi không trajectory nào qua được tầng 2 (mọi bản đều bị gán copy), `filter_trajectories` rơi vào fallback: giữ trajectory *đúng* tốt nhất làm good để vòng lặp không sập (cold-start). Cơ chế này cần thiết để tránh good pool rỗng, nhưng **có thể vô hiệu hoá chính judge** khi teacher chỉ sinh ra bản chép — một bản chép bị judge từ chối vẫn được fallback ép giữ. Đây là một limitation đo được (xác nhận trong log math idx8, §4.5.4 và Chương 6), nêu ở đây để minh bạch về cơ chế.

### 3.3.4 Few-shot teacher steering (good_only vs good_bad)

Các exemplar đã phân loại được đưa *trở lại prompt của teacher* (in-context, **không** train teacher — không gradient) để steer teacher sinh tốt hơn:

| | Option 2 — `good_only` | Option 1 — `good_bad` |
|---|---|---|
| Cơ chế | positive few-shot (chỉ exemplar tốt) | contrastive few-shot (good + bad, kèm nhãn) |
| Sức steer | vừa | mạnh hơn |
| Leak | **sạch** (good đã lọc → độc lập reference) | **rò dư** (bad ≈ reference → đưa nội dung giống reference trở lại context) |

Vì `bad ≈ reference`, đưa bad vào prompt (dù dán nhãn "xấu") nghĩa là teacher *thấy lại* thứ gần reference. Do đó **ablation Option 1 vs Option 2 đồng thời là ablation leak vs no-leak** — kiểm trực tiếp lo ngại của người hướng dẫn (kết quả: leak-null trên data này, §4.4).

### 3.3.5 Bước distillation: top-K reverse KL căn-token

Đây là lõi tính toán, dùng chung cho cả hai arm; chỉ khác *trajectory mục tiêu* ($y_{\text{student}}$ vs $y_{\text{good}}$).

**Phân phối tại mỗi token.** Với logits $z \in \mathbb{R}^V$ ($V \approx 150\text{k}$), $\pi(v) = \mathrm{softmax}(z)_v$. Tại mỗi vị trí $t$ của trajectory mục tiêu, có $\pi_S = \pi_\theta(\cdot\mid x, y_{<t})$ (student) và $\pi_T = \pi_\theta(\cdot \mid x, c, y_{<t})$ (teacher, đã thấy $c$).

**Gradient cốt lõi.** Với teacher `detach()`, đạo hàm loss theo logit student là [1; xem cơ sở ở `con_sdpo_loss_mechanics`]:

$$
\frac{\partial \mathcal{L}}{\partial z_v^{S}} \;=\; \pi_S(v) - \pi_T(v).
$$

Nghĩa: token nào teacher tin hơn student ($\pi_T > \pi_S$) thì optimizer **tăng** logit đó. Target là **phân phối $V$-chiều mỗi token**, không phải một scalar mỗi câu như GRPO [8] — đây là nguồn gốc của credit assignment dày hơn (≈ $T\cdot K$ lần) và sample-efficiency của SDPO [1].

**Hướng KL (α).** Codebase [4] tham số hoá qua $\alpha\in[0,1]$ với mixture $M=(1-\alpha)\pi_S + \alpha\pi_T$: $\alpha=0$ forward KL (mode-covering, giữ epistemic token), $\alpha=1$ reverse KL (mode-seeking, dễ suppress), $\alpha=0.5$ JSD. **Luận văn dùng $\alpha=1.0$** (reverse KL, top-K=20) để khớp config LCBv6 của [4]. (Việc $\alpha$ có modulate suppression hay không là một câu hỏi RQ2 để ngỏ — Chương 6.)

**Xấp xỉ top-K (memory).** KL full-vocab quá tốn với $V\approx150$k; dùng top-K=20 của teacher + 1 tail bucket, student project lên cùng K indices, KL tính trên $(K{+}1)$-chiều [1, §2.2].

**Importance sampling.** Vì sample bằng $\theta_{\text{old}}$ nhưng tính loss với $\theta$ hiện tại, nhân per-token loss với ratio clipped $r_t = \min(\pi_\theta/\pi_{\theta_\text{old}},\, c_{\text{clip}})$, $c_{\text{clip}}=2.0$.

**Căn-token (điểm dễ sai nhất).** Prompt student (`x + y_good`) và prompt teacher (`x + c + y_good`) có độ dài prefix *khác nhau*; phải lấy logits đúng các vị trí token của $y_{\text{good}}$ ở **mỗi** bên rồi mới so KL. Off-by-one ở đây làm KL sai âm thầm → code assert độ dài hai bên khớp và log `(student_prefix_len, teacher_prefix_len)`. Sanity đã verify: token alignment đúng ($L$ khớp hai bên dù prefix khác), `KL(token-mean)` hữu hạn hợp lý.

Hyperparam: AdamW `lr=1e-5`, `kl_topk=20`, `kl_alpha=1.0`, `is_clip=2.0`, teacher luôn stopgrad (self-distillation, shared weights → teacher = student forward với context $c$, no_grad).

---

## 3.4 Reprompt template (T1–T7)

Reprompt template quyết định nội dung $c$ mà teacher nhìn thấy → trực tiếp đổi $\pi_T$ → đổi hướng gradient distill. Đây là biến trung tâm của RQ1. Để defensible ("tại sao là 7 template này?"), không justify từng cái riêng lẻ mà tổ chức không gian thiết kế theo **3 chiều** có grounding từ prior work [1, 2]:

| Template | Tên | Chiều | Vary so với T2 |
|---|---|---|---|
| T1 | Minimal | Information content (thấp) | bỏ structure, chỉ "incorrect, try again" |
| **T2** | **Standard (anchor)** | **baseline** | **failing test + expected + actual + error_type** |
| T3 | Verbose | Information content (cao) | T2 + full stack trace + previous code |
| T4 | Structured JSON | Instruction framing (format) | cùng nội dung T2, mã hoá JSON |
| T5 | Reasoning-inducing | Instruction framing (diagnostic) | T2 + "First, identify root cause, then fix." |
| T6 | First-person | Instruction framing (reframe) | "I attempted this and got X. Let me reconsider." |
| T7 | Cumulative history | Memory depth | tất cả N attempt trước, không chỉ lần cuối |

Ba chiều và nguồn gốc:

- **Information content** (T1→T2→T3): Kim et al. [2] chỉ ra $I(y;c\mid x)$ quyết định mức suppression; luận văn vary *lượng* thông tin trong execution feedback.
- **Instruction framing** (T4, T5, T6): Hübotter et al. [1, §4.6] kết luận biến thể *cú pháp* nhỏ không quan trọng, nhưng biến thể *ngữ nghĩa/chỉ dẫn* thì chưa được test; [1, §7] nêu đây là future work nguyên văn ("how … the reprompt template … influences behavior").
- **Memory depth** (T7): [1, §5] dùng sliding window cố định (1 attempt) chưa ablate; [2] cho thấy suppression *tích luỹ* qua bước → history có thể amplify/dilute.

**T2 là anchor**: mỗi template còn lại vary *đúng một* chiều, giữ nguyên phần còn lại → ablation sạch. Trong thực nghiệm (giới hạn compute), RQ1 chỉ probe **T1/T2/T5** (§4.3); T3/T4/T6/T7 được định nghĩa như không gian thiết kế và để ngỏ (Chương 6). Hai caveat cần acknowledge: T4 (JSON) đồng thời đổi information density (overlap chiều 1–2); T7 tăng context length → confound compute, phải report context length riêng.

---

## 3.5 Domain: code (lõi) và math (pilot)

Khác biệt domain nằm ở **reference_mode** (teacher thấy gì làm "đáp án") và **nội dung privileged_context**, và đây là biến quyết định teacher-first thành/bại (Chương 5).

| | **Code — LCBv6 [6]** (lõi) | **Math — AIME 2026 [10]** (pilot) |
|---|---|---|
| Model | Qwen3-4B [7], LoRA r=32, thinking **OFF** | Gemma-4-E4B, LoRA all-linear, thinking **ON** |
| Verifier | public/private tests → **graded** [0,1] | so đáp án → **binary** {0,1} |
| `reference_mode` | `best_in_batch` (best-scoring trajectory làm proxy) | `ground_truth` (teacher LUÔN thấy đáp án đúng) |
| Leak regime | **null** (reference = best-in-batch + public tests, không phải lời giải mẫu) | **cực đoan** (feedback = "the correct answer is {gt}") |
| `privileged_context` | execution feedback (failing test, expected/actual, error type) + best-in-batch trajectory đúng | đáp án đúng (số) — teacher chỉ việc chép `\boxed{}` |
| Reference CHỨA method? | **Có** (best-in-batch là *chương trình* = thuật toán, tổng quát hoá input mới) | **Không** (chỉ là *giá trị* số, không phải derivation) |

Lưu ý về quyết định `reference_text` cho code: LCBv6 không có field lời giải mẫu tin cậy, nên luận văn dùng **best_in_batch** (trajectory điểm cao nhất trong batch teacher sinh) làm proxy reference để judge đo "độc lập". Hệ quả phụ quan trọng: vì reference *không* phải lời giải tác giả mà là output đúng của chính mô hình + public tests, **code không có leak** — giải thích vì sao ablation good_bad ra leak-null ở code (§4.4) nhưng leak lại đo được ở math (§4.5).

Hai caveat domain của math (giữ kèm mọi kết luận math):

1. **Model confound**: code dùng Qwen3-4B (đã escape), math dùng Gemma-4-E4B — *khác reasoner*. "Math no-escape" có thể một phần là tính chất model, không phải domain.
2. **Reference answer-only**: AIME chỉ có đáp án số, không có worked solution, nên `privileged_context` viết cứng trả về đáp án → teacher chỉ chép được. MATH-500 (có field `solution`) là hướng khử confound này (Chương 6), không nằm trong scope kết quả hiện tại.

Ngân sách TTT cũng khác giữa hai domain (chi tiết đầy đủ ở Phụ lục A): code chạy **15 step, eval 16 mẫu, teacher_n=10**; math chạy **3 step, eval 4 mẫu, teacher_n=4, max_new_tokens=16384** (8192 bị truncate làm mất `\boxed` → score-0 giả). Khác biệt ngân sách này là một biến cần lưu ý khi đối chiếu hai domain, không chỉ model/reference.

Việc chọn bài (problem selection) dùng **model pass-rate** $\in (0,1)$ (frontier theo *mô hình*), không theo nhãn contest, vì reward binary của math chỉ có variance khi mô hình giải đúng ~30–70% (§3.6, §4).

---

## 3.6 Metric và thiết kế so sánh

**pass@k / pass_rate.** Ước lượng empirical của pass@k [9]: với mỗi điều kiện chạy `N_eval` mẫu (code: 16; math: 4), `pass_rate` = tỉ lệ mẫu đúng. Báo PRE (trước TTT) và POST (sau TTT), **chỉ eval student** $\pi_\theta(\cdot\mid x)$ (không cho student thấy $c$ lúc eval — nếu không sẽ là leak vào đánh giá). `greedy` (1 mẫu deterministic) báo kèm như chỉ dấu phụ, nhiễu cao.

**Discovery curve.** Theo discovery@k [1, Def. 5.1] (§3.1): xác suất solve trong $k$ attempt đầu, $P(T\le k)$ với $T=\min\{k: r(y_k)=1\}$. Vì test-time là sinh *tuần tự* (share state, update weight), pass@k i.i.d. không áp dụng; discovery@k là metric đúng. Luận văn log batch pass-rate mỗi bước làm discovery curve thô.

**Escape-zero (bằng chứng cơ chế).** Định nghĩa thao tác: một seed mà **student-first kẹt ở pass = 0** (hoặc tụt về 0) trong khi **teacher-first thoát khỏi 0**. Đây là biểu hiện trực tiếp của flat-reward trap (§3.2): on-policy không có rollout đúng để học, off-policy-leaning bơm được lời giải đúng vào. Escape-zero replicated nhiều lần là contribution cơ chế chính (§4.2).

**Matched comparison.** Hai arm chạy *cùng* base, *cùng* seed → PRE khớp từng seed → so sánh **paired** (matched), khử biến thiên do base/seed. Trên mỗi cặp matched đếm thắng/hoà/thua (TF vs SF).

> **Calibrate trung thực (n nhỏ).** Vì số bài và seed nhỏ ($n=2$–3 bài code, $n=2$ seed cho RQ1, $n=2$ bài math), luận văn chỉ báo **sign test thô** (ví dụ $0.5^k$ trên các cặp không hoà) như *descriptive evidence có hướng*, **không** như inferential proof. Ngôn ngữ giữ ở mức "preliminary / directional / weak dominance"; không dùng "we prove". Mọi p-value đi kèm cảnh báo về $n$ (Chương 4, Chương 6).

---

## Tài liệu trích dẫn trong chương

Đánh số theo master bibliography (`00_references.md`): [1] Hübotter et al. 2026 · [2] Kim et al. 2026 · [3] Shenfeld et al. 2026 · [4] lasgroup SDPO repo · [5] TRL v1.4.0 docs · [6] LiveCodeBench · [7] Qwen3 · [8] GRPO/DeepSeekMath · [9] Chen et al. 2021 (pass@k) · [10] MathArena AIME 2026.
