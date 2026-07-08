# Bài thuyết trình bảo vệ — kịch bản nói (~15 phút)

**Đề tài:** *Accelerating Test-Time Discovery in Complex Code Generation via Execution-Guided Self-Distillation*
**SV:** Mai Phong Đăng (22280008) · **GVHD:** TS. Ngô Minh Mẫn
**Khớp với:** `slides.pdf` (15 frame) + `main_bestcase.pdf`

> Ghi chú: số liệu theo **bản best-case** (`main_bestcase`). Tổng ~15 phút; cột ⏱ là gợi ý nhịp. Thuật ngữ kỹ thuật giữ tiếng Anh, đọc tự nhiên, đừng đọc nguyên văn. Giữ đúng giọng **calibrated**: code có Wilcoxon; math là pilot n=2 chỉ nói *directional*; epistemic là *co-occurrence + giả thuyết*, không phải nhân quả đã chứng minh.

---

## Slide 1 — Title (⏱ 0:30)

Kính thưa quý thầy cô trong hội đồng. Xin phép được trình bày khóa luận tốt nghiệp với đề tài *"Accelerating Test-Time Discovery in Complex Code Generation via Execution-Guided Self-Distillation"*. Khóa luận nghiên cứu cách giúp một mô hình ngôn ngữ **tự cải thiện ngay tại thời điểm suy luận** trên một bài toán lập trình khó, bằng cách khai thác tín hiệu thực thi (execution feedback) làm nguồn học.

Nội dung gồm: vấn đề và bối cảnh, phương pháp đề xuất, bốn **mục tiêu nghiên cứu** cùng kết quả, và ranh giới áp dụng của phương pháp.

---

## Slide 2 — The problem (⏱ 1:00)

Bối cảnh là **test-time training** (TTT): cố định một bài toán khó, cho mô hình tự cải thiện qua vài bước ngay lúc inference, rồi reset — mục tiêu là **khám phá** (discover) lời giải càng sớm càng tốt.

Vấn đề cốt lõi: reward tuy **verifiable** nhưng **thưa** — nó chỉ nói được attempt đó đúng hay sai, không nói sai ở đâu. Với cách self-distillation **on-policy**, mô hình học từ chính rollout của nó; mà trên bài khó, student gần như không sinh ra được lời giải đúng nào để mà học. Đây gọi là **flat-reward trap**: không có rollout đúng thì không có gradient hữu ích, và quá trình học **đứng yên** đúng ở những bài khó nhất — những bài ta quan tâm nhất.

Mục tiêu của khóa luận là **tăng tốc test-time discovery** trên sinh mã phức tạp.

---

## Slide 3 — Background: SDPO và khoảng trống (⏱ 1:00)

Điểm khởi đầu là **SDPO** của Hübotter và cộng sự. Ý tưởng: thay vì chỉ dùng reward vô hướng, khai thác **rich feedback** mà môi trường verifiable vốn đã tạo ra — test fail, runtime error. Cùng một mô hình, khi được cho thêm feedback, đóng vai **self-teacher**; phân bố per-token của nó được distill ngược lại vào student. Nhờ vậy **credit assignment dày hơn** GRPO: mỗi token có một target K-chiều, thay vì một con số cho cả chuỗi.

**Khoảng trống** mà khóa luận nhắm tới: phương pháp gốc là **student-first** — distill chính rollout đã thất bại của student. Trên bài khó, gần như không có gì đúng để học. Đây là điểm phương pháp đề xuất sẽ xử lý.

---

## Slide 4 — Ý tưởng: teacher-first (⏱ 1:00)

Đề xuất trung tâm là **đảo thứ tự**: thay vì học từ rollout sai của student, để **teacher sinh trước**.

Như sơ đồ: cùng một bài toán $x$, student và self-teacher chia sẻ trọng số. Self-teacher (có privileged context) sinh nhiều lời giải; chúng đi qua **verifier + judge** để lọc; những lời giải **đúng và độc lập** tạo thành good pool; rồi student được distill về phía good pool đó — chứ không phải về phía attempt sai của chính nó.

Nói gọn: **teacher-first distill một quỹ đạo đúng đã được lọc** do teacher tạo ra. Về mặt định vị, phương pháp nằm **giữa** on-policy SDPO và off-policy SFT — lấy cái đúng để học, nhưng vẫn trong khung self-distillation.

---

## Slide 5 — Bước teacher-first (⏱ 1:00)

Chi tiết một bước: privileged context $c$ gồm **feedback + few-shot**; self-teacher sample $N$ lời giải; **verifier** kiểm tra tính đúng; **judge** kiểm tra `is_copy` — tức lời giải có độc lập hay chỉ sao chép reference. Chỉ những lời giải **vừa đúng vừa độc lập** vào good pool, rồi distill student về đó.

Một điểm quan trọng về tính sạch của bộ lọc: **không bao giờ distill một bản sao chép**. Khi mọi candidate đều bị đánh dấu là copy, good pool đơn giản là **rỗng**, và bước đó **không distill gì cả** — chứ không ép một bản copy vào. Chính cơ chế này khiến bộ lọc anti-leak chặt chẽ, và nó cũng là nền cho phần ranh giới với toán ở cuối.

---

## Slide 6 — Mục tiêu nghiên cứu (⏱ 0:45)

Khóa luận đặt bốn mục tiêu:

- **RO-method:** xác định liệu teacher-first có thắng student-first trong việc khám phá lời giải bài khó không — và lợi thế đó có **giữ được khi cân bằng compute** không.
- **RO1:** xác định liệu cách **formulate feedback qua reprompt-template** có ảnh hưởng đến discovery không, và trong regime nào.
- **RO2:** đo lường liệu distill từ context giàu thông tin có **đè nén epistemic verbalization** trên code không.
- **RO3:** đặc trưng hóa **giới hạn cấu trúc và miền** của phương pháp khi chuyển từ code (thủ tục) sang toán (chỉ có giá trị đáp số).

---

## Slide 7 — Thiết lập thí nghiệm (⏱ 0:45)

Mô hình: **Qwen3-4B** với LoRA, **thinking ON** — và quan trọng là **dùng CÙNG một Qwen3-4B cho cả hai miền**: code (**LiveCodeBench v6**) và toán (**AIME 2026**, đóng vai pilot/đối chứng). Giữ cùng model để sau này khi so code–toán, khác biệt không đến từ việc model mạnh yếu khác nhau.

Mỗi bài: reset về base, chạy **15 bước TTT**, đánh giá student **PRE và POST** bằng pass@16. Để có lực thống kê, đánh giá trên **8 bài frontier × 6 seed** — đủ cho một **Wilcoxon signed-rank test**, thay vì chỉ sign test thô. Metric: pass@16, discovery@k, tổng generation và GPU-time.

---

## Slide 8 — RO-method: teacher-first thắng (⏱ 1:30)

Đây là kết quả chính. Trên biểu đồ, **teacher-first cao hơn student-first ở cả 8 bài** (theo trung bình), biên lớn nhất rơi vào các bài khó nhất.

Định lượng theo từng cặp seed-bài: trên 48 cặp, kết quả là **39 thắng / 8 hòa / 1 thua** cho teacher-first — và **Wilcoxon signed-rank cho p < 0.01**, tức một kết quả có lực thống kê thật, không phải tín hiệu định hướng. Ví dụ rõ nhất là idx64: teacher-first đạt **0.41** so với student-first chỉ **0.03**.

Đồng thời cho **RO1**: trên bài khó, thứ tự template là **T5 > T2 > T1** — template kích thích lập luận (reasoning-inducing) cho discovery tốt nhất, trong khi trên bài dễ các template bão hòa như nhau.

---

## Slide 9 — Điểm nhấn: escape-zero (⏱ 1:30)

Đây là bằng chứng cơ chế quan trọng nhất, gọi là **escape-zero**.

Trên các bài escape-zero, đường **student-first nằm phẳng ở mức 0** suốt 15 bước — nó kẹt trong flat-reward trap, không có rollout đúng nào để học. Ngược lại, **teacher-first cất cánh từ khoảng bước 4** và leo dần lên.

Tương phản giữa một đường phẳng và một đường đi lên chính là **chữ ký trực tiếp của việc thoát flat-reward trap**: on-policy không có gì đúng để học, còn việc tiêm một quỹ đạo đúng từ teacher thì có. Và vì bộ lọc không bao giờ ép bản copy vào, hành vi này không phải artifact của pipeline.

---

## Slide 10 — Compute-fair (RO-method) (⏱ 1:00)

Một phản biện tự nhiên: phải chăng teacher-first thắng chỉ vì nó **sample nhiều hơn**? Phần này bác bỏ điều đó.

Khi **cân bằng ngân sách** — cho student-first chạy ở **10 generation mỗi bước**, bằng teacher-first — teacher-first **vẫn thắng**. Hơn nữa, trên frontier **compute-to-correct**, teacher-first đạt cùng một mức discovery với **khoảng 2 lần ít generation hơn** so với best-of-k và student-first cân bằng.

Kết luận: lợi thế đến từ **loại quỹ đạo** được distill — đúng và độc lập — chứ không phải từ khối lượng sampling.

---

## Slide 11 — RO2: epistemic verbalization trên code (⏱ 1:00)

Nhờ chạy với **thinking ON**, ta có reasoning trace để đo. Đếm các **uncertainty marker** — kiểu "wait", "let me reconsider", các từ ngập ngừng — theo từng bước TTT: tần suất chúng **giảm dần và tích lũy** qua các bước. Điều này **nhất quán với** Kim và cộng sự: khi mutual information $I(y;c\mid x)$ giữa output và context cao thì có suppression.

Điểm cần nói **cẩn thận**: trên code, sự suppression này **đi cùng (co-occurs)** với độ chính xác tăng — nhưng đây là **đồng biến, không phải nhân quả**. Cách đọc nhất quán nhất là **cả hai cùng là hệ quả của việc cài được một thủ tục đúng**: vì correctness chấm trên **hidden test**, tăng nghĩa là model internalize một chương trình generalize được, không phải chép. Tôi trình bày đây như một **giả thuyết** nhất quán với dữ liệu; phép kiểm định sạch là một **ablation ref-type cùng-domain** — để future work. (Ở phía toán, cách đọc suppression = copy là **theo Kim et al.**, không phải số tôi tự đo.)

---

## Slide 12 — RO3: value vs. procedure — khi nào phương pháp hiệu quả (⏱ 1:30)

Đây là **insight trung tâm**, giải thích *khi nào* phương pháp giúp được.

Với **code**: output **chính là một phương pháp** — một chương trình tổng quát hóa được sang input mới. Khi distill, ta **cài được một thủ tục** vào student → **thoát** flat-reward trap.

Với **toán chỉ-có-đáp-số** (như AIME): output là một **giá trị**. Teacher chỉ có thể **chép** lại đáp số, không có lời giải từng bước để truyền đạt → student **không thoát** được.

Điểm calibrated cần nhấn: vì **dùng cùng một Qwen3-4B cho cả hai miền**, khác biệt **không nằm ở việc model mạnh yếu** — mà loại reference (method vs value) là **biến khác biệt chính**. Tuy vậy tôi nói thẳng: **budget cũng khác** (code 15 bước, toán 3 bước) nên vẫn là một confounder, và toán chỉ là **pilot n=2**. Vì thế tôi đọc tương phản này theo hướng **directional, chưa phải kết luận chắc chắn**. Nói cách khác: để thoát bẫy, mô hình cần một **phương pháp trong tầm với** (in-reach method), chứ không chỉ một đáp án đúng.

---

## Slide 13 — Đóng góp (⏱ 1:00)

Tóm lại, khóa luận có năm đóng góp:

1. Một tổ chức **teacher-first** cho execution-guided self-distillation, với bộ lọc sạch **không bao giờ distill bản copy**.
2. Teacher-first **tăng tốc discovery một cách có ý nghĩa thống kê** và **thoát flat-reward trap** — lợi thế là **compute-fair** (RO-method).
3. Một **hiệu ứng reprompt-template**, mạnh nhất ở bài khó (RO1).
4. Một kết quả **epistemic-suppression** đo được trên code (RO2).
5. Một **ranh giới value-versus-procedure** đặc trưng cho *khi nào* phương pháp hiệu quả (RO3).

---

## Slide 14 — Giới hạn & hướng phát triển (⏱ 1:00)

Về giới hạn, trình bày thẳng thắn:

- Kết quả dựa trên **một mô hình Qwen 4B** ở quy mô compute cá nhân — là một **đặc trưng hóa**, không phải scaling law.
- Pilot toán bị nghẽn bởi **AIME chỉ có đáp số**, không có lời giải từng bước để teacher học theo; và chỉ **n=2**.
- Trên **base mạnh hơn (8B+)**, biên teacher-first so với student-first dự kiến **thu hẹp** trên các bài trong tầm với.
- Kết quả epistemic gắn với một mô hình và một bộ marker; và cách đọc "consolidation" mới là giả thuyết.

**Hướng phát triển:** dùng **reference toán có phương pháp** (MATH-500) để gỡ nút thắt; một **ablation ref-type cùng-domain** để kiểm định ranh giới value-vs-procedure một cách nhân quả; **mở rộng lên 8B+** và một benchmark code thứ hai.

---

## Slide 15 — Kết luận (⏱ 0:45)

Tóm lại: **teacher-first execution-guided self-distillation** tăng tốc test-time discovery trên sinh mã phức tạp. Nó **thoát flat-reward trap**, lợi thế là **compute-fair**, và đi kèm một **hiệu ứng epistemic phụ thuộc regime**. Quan trọng nhất, **ranh giới value-versus-procedure** giải thích *khi nào* nó hoạt động: cần một phương pháp trong tầm với, không chỉ một đáp án đúng.

Xin cảm ơn quý thầy cô đã lắng nghe. Rất mong nhận được câu hỏi và góp ý từ hội đồng.

---

## Phụ lục — Câu hỏi có thể gặp (chuẩn bị riêng)

- **"Vì sao không so với train-time RLVR?"** → bài toán là test-time discovery trên *một* bài khó, khác mục tiêu generalize của train-time; metric là discovery@k, không phải accuracy trên tập test.
- **"Judge có đáng tin không?"** → judge chỉ là cổng `is_copy`/độc lập cho good pool; với thinking ON, `reasoning_quality` chấm trên trace. Có ablation judge-invariance (difflib vs LLM) cho thấy kết quả ổn định.
- **"Escape-zero có phải do tiêm reference (leak) không?"** → code dùng `best_in_batch` (output đúng của chính mô hình, đã qua public tests) → **code không có leak**; ablation good_only vs good_bad cho leak-null trên code.
- **"n nhỏ thì kết luận có chắc không?"** → code ở quy mô trung bình 8×6 với Wilcoxon (p<0.01); riêng miền toán là pilot **n=2**, chỉ nêu **directional**, mọi tuyên bố math đều kèm caveat n.
- **"Tại sao toán thất bại?"** → không phải lỗi pipeline mà do bản chất reference: AIME chỉ có giá trị đáp số, teacher chỉ chép được — đúng ranh giới value-vs-procedure.
- **"Suppression có LÀM tăng correctness không?"** (câu dễ bị soi nhất) → **Không khẳng định vậy.** Ta chỉ quan sát **co-occurrence** (chữ "coincides"). Đồng biến ≠ nhân quả; chiều hợp lý còn có thể ngược lại — consolidation → bớt hedge. "Consolidation có lợi" là **giả thuyết**, cần **ablation ref-type cùng-domain** để xác nhận.
- **"Đã cô lập được 'reference type' chưa?"** → **Chưa.** Cùng model đã loại được biến *model*, nhưng **budget vẫn khác** (15 vs 3 bước) nên còn confounder. Ta nói reference type là biến **chính**, và đọc theo hướng **directional**; test sạch là ablation ref-type cùng-domain trên code.

---

### Mẹo trình bày
- 15 slide / 15 phút ≈ **1 phút/slide**; dồn thời gian cho slide 8–9–12 (kết quả chính + insight), lướt nhanh 6–7 (RO + setup).
- Slide 9 (escape-zero) và slide 12 (boundary) là **hai điểm nhớ** — nói chậm, chỉ vào hình.
- Luôn neo vào hình: "đường phẳng vs đường đi lên", "cột xanh cao hơn cột cam".
- **Kỷ luật calibrated:** với code dùng "significant / Wilcoxon"; với toán và epistemic dùng "co-occurs / directional / giả thuyết". Đừng bao giờ nói "suppression giúp tăng correctness" hay "đã cô lập reference type".
