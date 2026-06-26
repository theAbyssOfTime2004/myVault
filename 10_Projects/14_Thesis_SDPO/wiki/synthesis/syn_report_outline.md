---
type: synthesis
created: 2026-06-26
updated: 2026-06-26
tags: [report, outline, discussion, limitations, writing-hub]
sources: [src_hubotter2026_self_distillation, src_kim2026_why_self_distillation_degrades, src_shenfeld2026_sdft]
---

# Report Writing Hub — Outline + Discussion + Limitations

Hub để viết luận văn (min 30 trang). Số liệu lõi ở [[syn_core_result]] (code) + [[syn_math_pilot]] (math). File này chứa **outline chi tiết + lý lẽ Discussion + Limitations/Future Work tinh chỉnh** (phần phát triển trong thảo luận 2026-06-26, chưa nằm chỗ khác).

## Framing tổng: code = lõi, math = "làm thêm"

Report **đứng trên code** (RQ-method + RQ1). Math = pilot/contrast (boundary + leak + epistemic). KHÔNG cần math escape để bảo vệ. Trình bày math như **boundary characterization** ("when does teacher-first work"), KHÔNG phải "thử và thất bại".

## Chuẩn trình bày

- Cấu trúc ML-paper (NeurIPS/ICML): Abstract → Intro(+contributions bullets, RQs) → Related Work → Method → Experiments(setup/results/ablations) → Discussion → Limitations → Conclusion.
- Vỏ ngoài theo format HCMUS (chương, dài, giải thích kỹ). Method/Experiments/Discussion viết theo rigor paper.
- Mirror paper cha Hübotter (notation, metric pass@k/discovery@k, cite dày). PDF gốc trong `raw/`.
- Calibrate claim theo n: n=2 → "preliminary/directional", không "we prove". Limitations tường minh (gần bắt buộc).
- Skill `academic-paper` đã cài ở `.claude/skills/` (12-agent pipeline: IMRaD, APA7, citation-check, LaTeX/PDF). Dùng nó để viết.

## Outline chi tiết (~46 trang, sàn 30 dễ vượt)

### Ch1 Mở đầu (~4tr)
1.1 Bối cảnh (test-time compute, sparse RLVR reward) · 1.2 Bài toán (test-time discovery + reprompt template) · 1.3 RQ1 template / RQ2 epistemic / RQ3 discovery + câu hỏi method TF-vs-SF · 1.4 Đóng góp (bullets) · 1.5 Phạm vi · 1.6 Cấu trúc

### Ch2 Cơ sở & Related Work (~8tr)
2.1 RLVR & GRPO [[ent_rlvr]][[ent_grpo]] · 2.2 SDPO [[ent_sdpo]][[src_hubotter2026_self_distillation]] (2.2.1 self-teacher & rich feedback [[con_self_teacher]][[con_rich_feedback]]; 2.2.2 loss top-k reverse KL + credit assignment [[con_sdpo_loss_mechanics]] có derivation; 2.2.3 ba regime RLVR/RLRF/test-time) · 2.3 Test-time training & discovery@k [[con_test_time_self_distillation]][[con_discovery_at_k]] · 2.4 Reprompt template + taxonomy [[con_reprompt_template]][[syn_template_taxonomy_rationale]] · 2.5 Epistemic verbalization/suppression — Kim [[con_epistemic_verbalization]][[con_uncertainty_suppression]] · 2.6 SDFT + leak [[src_shenfeld2026_sdft]] · 2.7 Định vị gap

### Ch3 Phương pháp (~6tr)
3.1 Pipeline overview (+diagram) · 3.2 Student-first (baseline on-policy) · 3.3 Teacher-first (3.3.1 rollout + privileged_context; 3.3.2 verifier; 3.3.3 LLM judge is_copy+reasoning_quality; 3.3.4 few-shot good_only/good_bad; 3.3.5 KL step token-aligned top-k reverse KL) · 3.4 Templates T1–T7 · 3.5 Domains code(LCBv6)/math(AIME,MATH-500) — reference_mode + nội dung privileged_context · 3.6 Metrics pass@k, discovery curve, escape-zero, matched

### Ch4 Thực nghiệm (~11tr, nặng nhất)
4.1 Setup (Qwen3-4B, Colab/Modal, hyperparams, seeds) · 4.2 RQ-method TF vs SF [[syn_core_result]] (4.2.1 frontier scan; 4.2.2 main matched p≈0.03; 4.2.3 escape-zero hard 9/3/0 p≈0.002; 4.2.4 curves+qualitative) · 4.3 RQ1 template (bảng T5>T2>T1, hard vs easy) · 4.4 Robustness (judge-invariant; Option1≈2 leak null) · 4.5 Math pilot [[syn_math_pilot]] (4.5.1 setup Gemma4/AIME/thinking/infra; 4.5.2 no escape idx9+idx8; 4.5.3 judge bắt leak ~75% + fallback; 4.5.4 epistemic form≠substance)

### Ch5 Thảo luận (~4tr) — xem "Discussion notes" dưới
### Ch6 Limitations + Future Work (~3tr) — xem dưới
### Ch7 Kết luận (~2tr)
### Tài liệu (~2tr)
### Phụ lục (~6tr): A hyperparams · B 7 templates full · C teacher+judge prompt · D ví dụ trajectory good/bad/copy (completion đã có trong chat history/log) · E per-seed tables · F frontier scan (code+AIME 30 bài)

---

## Discussion notes (Ch5 — lý lẽ cốt, viết ra prose)

**Khi nào teacher-first work? — 3 điều kiện cần:**
1. **Rich feedback đủ densify sparse reward** (đúng tiền đề SDPO).
2. **Reference CHỨA method** (không chỉ đích).
3. **Năng lực reachable** (model giải được khi được gỡ).
→ Code thỏa cả 3 → escape. Math (AIME) thiếu (2)+(3) → teacher chỉ chép → no escape.

**Value-vs-procedure (insight trung tâm):**
- Code: output CHÍNH LÀ method (chương trình = thuật toán, tổng quát hóa input mới). Reference đúng = tự động chuyển giao được.
- Math: output = giá trị (số), KHÁC derivation. Đáp án không tổng quát hóa. Method là artifact riêng (worked solution), AIME không có.
- Nối tiền đề SDPO: escape cần feedback đủ giàu để densify reward; code (tests+best_in_batch) giàu, math final-answer nghèo (binary + answer-only). [[con_rich_feedback]][[con_credit_assignment]]

**privileged_context = "feedback" của paper** (Hübotter Table 6 feedback-content ablation). Tên là của code mình; concept là của paper. Teacher-first là biến thể (paper gốc = student-first on-policy).

**Code vs math = reward landscape:** code graded (partial test-pass → có gradient leo, 0.21→1.0); math binary (all-or-nothing, không gradient). "Cliff vs slope."

## Limitations tinh chỉnh (Ch6.1)

- n nhỏ: 2-3 bài code escape, RQ1 n=2 seed, 2 bài math.
- **Math 2-confound**: (a) model — code dùng Qwen3-4B, math dùng **Gemma-4-E4B** (yếu trên AIME, beyond-capability); (b) **reference answer-only** (AIME không có solution + privileged_context viết cứng trả về đáp án). → no-escape có thể là **artifact**, không phải tính chất domain.
- **Judge degrade khi beyond-capability**: glm-4.5-flash bắt được copy trắng trợn nhưng KHÔNG phân biệt nổi "derivation thật" vs "confabulation hướng-đáp-án" (cả hai đều chạm đúng số). → nhãn is_copy không hoàn toàn tin được trên bài quá khó.
- **Fallback ép distill copy** (finding idx8): khi judge gắn TẤT CẢ là is_copy=true, fallback "keep-best-correct" vẫn giữ 1 bản chép làm good → vô hiệu hóa chính judge. Verify được trong log idx8 (run 463y4fjr): mọi verdict is_copy=true, n_good=1 do fallback.
- Chưa compute-matched (TF ~2.5× generation). RQ2 thin (thinking-off code không có trace; math trace = data RQ2 duy nhất).

## Future Work tinh chỉnh (Ch6.2)

- **Khử model confound (ưu tiên #1)**: chạy **Qwen3-4B + thinking trên CẢ code lẫn math** — cùng reasoner đã escape ở code, test có escape ở math không.
- **Scaling**: Qwen3-8B + thinking → bài AIME beyond-capability có thể chuyển reachable → escape có thể xuất hiện (đòn bẩy mạnh nhất lật math null).
- **Method-reference cho math**: **MATH-500** (có field `solution`) + sửa `MathDomain.privileged_context` inject worked solution thay vì chỉ đáp án → test giả thuyết "escape cần method-reference".
- Thinking-on code → mở RQ2 (epistemic trace trên code).
- Thêm bài/seed (power 8/8→16/16); CTC compute-matched (RQ3).
- Dự đoán code+thinking/8B: cơ chế giữ nhưng effect **có thể loãng** (model mạnh → SF tự thoát nhiều hơn → gap TF−SF hẹp lại). Escape-zero sắc nhất với model đủ yếu.

## TODO trước khi viết (free, không tốn $)
- Đọc trực tiếp trajectory "good" idx9 (W&B run fi5m0as1) để xác nhận derivation thật hay confabulation → chốt phần judge-degrade.

## Links
[[syn_core_result]] · [[syn_math_pilot]] · [[syn_thesis_proposal]] · [[con_teacher_first_judge]]
