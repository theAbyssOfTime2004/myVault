---
type: synthesis
created: 2026-06-24
updated: 2026-06-24
tags: [results, teacher-first, math, aime, epistemic, leak, pilot]
sources: [src_kim2026_why_self_distillation_degrades, src_hubotter2026_self_distillation]
---

# Math Pilot — Teacher-First trên AIME2026 (Gemma-4-E4B, thinking ON)

Pilot mở rộng [[syn_core_result]] (code escape-zero) sang **math domain** — nơi advisor và [[src_kim2026_why_self_distillation_degrades|Kim]] dự đoán **information-leak/epistemic** mạnh nhất. Chạy trên Modal A100-80GB (Colab CU hết). Method: [[con_teacher_first_judge]].

## Setup

| | |
|---|---|
| Model | google/gemma-4-E4B-it + LoRA all-linear, **thinking ON** |
| Data | MathArena/aime_2026 (30 bài, đáp án integer) |
| reference_mode | `ground_truth` (teacher LUÔN thấy đáp án đúng = **leak regime**) |
| Judge | LLM `zai:glm-4.5-flash`, prompt derive-vs-copy (is_copy + reasoning_quality 1–5) |
| max_new_tokens | **16384** (8192 bị truncate → mất `\boxed` → score 0 giả) |
| Steps / eval | 3 TTT step, eval 4 sample, teacher_n=4, top_p 0.95 top_k 64 |

## Frontier scan (30 bài AIME2026, n_samples=2)

- **Frontier (0<pass<1):** idx 8, 11, 21, 25
- **Too hard (pass=0):** idx 2,3,9,10,12,13,14,16,17,22,24,26,27,28,29 (15 bài)
- **Ceiling (pass=1):** idx 0,1,4,5,6,7,15,18,19,20,23

→ Độ khó **rải rác**, không đơn điệu. Gemma4-thinking giải được nhiều bài AIME2026.

## Run idx9 (aime2026_10, too-hard) — clean run đầu tiên, KHÔNG escape

Bài: tam giác 13-14-15, xoay quanh circumcenter, diện tích hexagon. Đáp án đúng **156**.

| | PRE | POST |
|---|---|---|
| pass_rate | 0.000 | 0.000 |
| greedy | 0.000 | 0.000 |
| boxed answer | 148 | 168 |

`discovery curve: 1.00→1.00→1.00` · mỗi step `n_good=1 n_bad=3` · `judge_calls=4` · không crash.

> **EFFECTIVENESS: NO IMPROVEMENT** — teacher-first KHÔNG kéo bài too-hard thoát 0.

## Phát hiện 1 — Judge bắt được leak (positive, on-thesis)

Teacher có leaked answer 156 → **cả 4 trajectory đều "đúng"** (`batch_mean_r=1.0`). Nhưng judge bóc ra **xuyên suốt 3 step**:

| | is_copy=true (chỉ khẳng định 156) | genuine derive |
|---|---|---|
| tỉ lệ | **~3/4 (75%)** | ~1/4 |

→ **Privileged teacher chủ yếu CHÉP đáp án, không derive.** LLM judge phát hiện đúng (`n_good=1/n_bad=3` ổn định). Đây là **information-leak đo được** — đúng lo ngại của [[con_teacher_first_judge]] và [[src_kim2026_why_self_distillation_degrades]]. (Khác code: ở code leak null vì reference=best_in_batch + public tests, xem [[syn_core_result]] ablation.)

## Phát hiện 2 — Tại sao không escape: regime sai + leak truyền form ≠ substance

1. **idx9 vượt năng lực thật của Gemma4.** Thinking ON + 16384 token (không cụt) → model nghĩ trọn vẹn, **vẫn ra sai tự tin** (148, 168). Loại bỏ giả thuyết "nghĩ chưa đủ" → đây là **capability ceiling**, không phải thiếu compute.
2. **Reference chỉ là số "156"** → teacher chỉ copy được, không có "method-trong-tầm-với" để distill. Distill vài trace answer-aware **không cài được năng lực model vốn không có**.
3. **"Too hard" ≠ regime escape-zero của code.** Code "hard" = **reachable-but-stuck** (model giải được khi được gỡ bằng feedback/best_in_batch). AIME "too hard" = **beyond-capability**. Chọn sai regime.

## Phát hiện 3 — Epistemic pathology (qualitative, đọc full thinking trace)

- **Satisficing về "số đẹp"**: khi bí, model giả định bừa (PRE: θ=90°; POST: Area=2K=168) rồi tự biện minh *"in problems of this nature, the intended answer is usually clean"* → **đoán theo convention đề thi thay vì derive**.
- **Epistemic suppression** ([[con_uncertainty_suppression]]): model BIẾT đề mơ hồ (*"this is impossible", "contradiction"*) nhưng **không thừa nhận bất lực**, xuất đáp án dứt khoát.
- **"Self-correction theater"**: đầy nhãn *"Crucial Insight Check", "Self-Correction"* nhưng correction **chạy vòng tròn, không hội tụ**. PRE tự mâu thuẫn (thinking ra 316, clean-solution ra 148).
- **TTT đổi FORM không đổi SUBSTANCE**: POST ngắn nửa (24k→12k char), setup tốt hơn (biết cos C=3/5, θ=90°±C) nhưng **bỏ cuộc sớm hơn** → tự tin cắt góc tới sai (168). Student học **phong cách reasoning tự tin** từ teacher answer-aware, **không học method** → đây là **vegetative/epistemic mimicry** hiện hình. Thậm chí không memorize được 156.

## Run idx8 (aime2026_9, "frontier" theo scan, đáp án 29) — replication, cũng KHÔNG escape

Bài xác suất xúc xắc/sticker. Nhãn frontier (pass 0.5 ở scan n_samples=2) nhưng thực tế **PRE pass=0 (4 sample), greedy=0** → cũng beyond-capability (scan n=2 quá noise). PRE boxed 40201, POST boxed 17 (đúng 29) → đều sai. `discovery curve 0.50→0.75→1.00`, `n_good=1` mỗi step (teacher chủ yếu `is_copy=true`). **PRE 0 → POST 0, NO IMPROVEMENT.**

> **Nuance POST**: idx8 đi NGƯỢC idx9 — POST **rigorous hơn** (casework R2=R4 / R2≠R4, đếm N_B=11700 → p=4/13). idx9 POST thì **lười đi** (shortcut 2K). Cả hai vẫn sai. → TTT đổi **phong cách** reasoning (bất định) nhưng **không sửa correctness** = "form ≠ substance" replicated qua 2 bài.

(Vận hành: idx8 chạy trọn 4.1h sau khi thêm `retries=2` + monitoring sạch — các crash trước là preempt/cancel ngắt quãng, không phải bug.)

## Phát hiện 4 — Fallback ép distill copy + judge degrade (verify trong log idx8)

Đọc log idx8 (run 463y4fjr): **mọi verdict judge = is_copy=true** (cái duy nhất is_copy=false thì rq=2 <3 → cũng bad). Vậy `n_good=1` mỗi step **đến từ FALLBACK** (`filter_trajectories` ~line782: "không có good nhưng có trajectory đúng → giữ cái đúng tốt nhất"). → **good_pool idx8 = các bản chép mà judge ĐÃ từ chối, fallback ép giữ.** Fallback "keep-best-correct" **vô hiệu hóa chính judge** khi teacher chỉ sinh copy.

Đối lập idx9 (run fi5m0as1): có 1 verdict is_copy=false rq=4 (genuine-label) ở step1. → **judge degrade khi beyond-capability**: bắt được copy trắng trợn nhưng không phân biệt nổi "derivation thật" vs "confabulation hướng-đáp-án" (cả hai chạm đúng số). TODO: đọc trực tiếp trajectory good idx9 để xác nhận.

→ Discussion/Limitations/Future Work đầy đủ + outline report: xem [[syn_report_outline]].

## Kết luận pilot (2 bài: idx9, idx8 — đều KHÔNG escape)

> Teacher-first **escape khi reference cho method-trong-tầm-với** (code, [[syn_core_result]]) nhưng **fail khi teacher chỉ có đáp án trên bài beyond-capability** (AIME too-hard, **2/2 bài**): teacher copy đáp án (judge bắt ~75%), leak truyền **form ≠ substance** (replicated 2 bài), student không thoát 0. **Contrast này mạnh hơn "work everywhere"** — nó characterize cơ chế: escape cần *reachable capability*, không phải chỉ *đáp án đúng*.

## Hướng tiếp (nếu còn budget ~$50)

- **Frontier idx8/21/25** (reachable, pass 0.5) = regime đúng để thử TF>SF improvement. Nếu lên → SF matched. Nếu không → chốt report với contrast trên.
- Report khả dụng **không cần math escape**: lõi = code escape-zero; math = (judge bắt leak 75%) + (epistemic mimicry) làm pilot/contrast.

## Hạ tầng (đã giải quyết, ghi để khỏi lặp)

- Modal wrapper `modal_run.py`: `.spawn()` + `--detach` (miễn nhiễm crash máy), `PYTHONUNBUFFERED=1` (live log), full `requirements.txt` (khớp Colab, khỏi cascade dep).
- Bug đã fix: `get_reference_text` nhận int answer (judge bị skip nếu không); judge `TimeoutError` không catch → crash (cap candidate `[-10000:]` + timeout 180s); 8192→16384 chống truncate.
- z.ai key hết hạn → verify bằng `modal run modal_run.py::verify_zai` trước khi đốt GPU.

## Links

- [[syn_core_result]] — code escape-zero (lõi, contrast)
- [[con_teacher_first_judge]] · [[con_uncertainty_suppression]] · [[con_epistemic_verbalization]]
- [[src_kim2026_why_self_distillation_degrades]] (epistemic degradation) · [[src_hubotter2026_self_distillation]]
