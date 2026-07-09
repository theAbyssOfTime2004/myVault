# Bài thuyết trình bảo vệ — kịch bản nói (~15 phút)

**Đề tài:** *Accelerating Test-Time Discovery in Complex Code Generation via Execution-Guided Self-Distillation*
**SV:** Mai Phong Đăng (22280008) · **GVHD:** TS. Ngô Minh Mẫn
**Khớp với:** `slides.pdf` (16 frame) + `main_bestcase.pdf`

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

Điểm khởi đầu là **SDPO** của Hübotter và cộng sự. Ý tưởng: thay vì chỉ dùng reward vô hướng, khai thác **rich feedback** mà môi trường verifiable vốn đã tạo ra — test fail, runtime error. Cùng một mô hình, khi được cho thêm feedback, đóng vai **self-teacher**; phân bố per-token của nó được distill ngược lại vào student. Nhờ vậy **phân bổ tín hiệu học (credit assignment) dày hơn** GRPO
GRPO: một điểm cho cả câu, chia đều. SDPO: mỗi token một phân bố top-K từ teacher  dày hơn T·K lần và có tín hiệu ngay cả khi chưa giải đúng, nên thoát được flat-reward trap.

**Khoảng trống** mà khóa luận nhắm tới: phương pháp gốc là **student-first** — distill chính rollout đã thất bại của student. Trên bài khó, gần như không có gì đúng để học. Đây là điểm phương pháp đề xuất sẽ xử lý.

---

## Slide 4 — Ý tưởng: teacher-first (⏱ 1:00)

Đề xuất trung tâm là **đảo thứ tự**: thay vì học từ rollout sai của student, để **teacher sinh trước**.

Như sơ đồ: cùng một bài toán $x$, student và self-teacher chia sẻ trọng số. Self-teacher (có privileged context) sinh nhiều lời giải; chúng đi qua **verifier + judge** để lọc; những lời giải **đúng và độc lập** tạo thành good pool; rồi student được distill về phía good pool đó — chứ không phải về phía attempt sai của chính nó.

Nói gọn: **teacher-first distill một quỹ đạo đúng đã được lọc** do teacher tạo ra. Về mặt định vị, phương pháp nằm **giữa** on-policy SDPO và off-policy SFT — lấy cái đúng để học, nhưng vẫn trong khung self-distillation.

---

## Slide 5 — Bước teacher-first (⏱ 1:00)

Chi tiết một bước. Privileged context $c$ mà self-teacher nhìn thấy gồm hai phần: **feedback** (test fail, runtime error) và **khối few-shot**. Teacher sample $N$ lời giải dưới context này; **verifier** kiểm tra tính đúng; **judge** kiểm tra `is_copy` — tức lời giải có độc lập hay chỉ sao chép reference. Chỉ những lời giải **vừa đúng vừa độc lập** mới vào good pool, rồi distill student về đó.

**Khối few-shot** là vòng lặp giúp teacher thực hiện in-context learning: các lời giải đã lọc từ good pool được **nạp ngược** vào prompt của teacher ở bước sau làm ví dụ mẫu, để nó dần sinh lời giải tốt và độc lập hơn qua các bước TTT. Có hai biến thể — **good_only** (chỉ đưa ví dụ tốt; sạch, vì good đã lọc nên độc lập với reference) và **good_bad** (thêm cả ví dụ xấu có gắn nhãn; lái mạnh hơn nhưng vì bad ≈ reference nên tái đưa chút nội dung giống-reference vào). So sánh hai biến thể này chính là **ablation leak-vs-no-leak** (kết quả: leak-null trên code).

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

## Slide 15 — Kết luận (⏱ 0:30)

Tóm lại: **teacher-first execution-guided self-distillation** tăng tốc test-time discovery trên sinh mã phức tạp. Nó **thoát flat-reward trap**, lợi thế là **compute-fair**, và đi kèm một **hiệu ứng epistemic phụ thuộc regime**. Quan trọng nhất, **ranh giới value-versus-procedure** giải thích *khi nào* nó hoạt động: cần một phương pháp trong tầm với, không chỉ một đáp án đúng.

---

## Slide 16 — Thank you (⏱ 0:15)

Xin cảm ơn quý thầy cô đã lắng nghe. Rất mong nhận được câu hỏi và góp ý từ hội đồng.

---

## Phụ lục — Câu hỏi có thể gặp (chuẩn bị riêng)

> Nguyên tắc trả lời: (1) trả lời thẳng, ngắn gọn phần cốt lõi trước, rồi mới bổ sung; (2) nếu là câu về *giới hạn/độ tin cậy*, **chủ động thừa nhận** đúng mức rồi nêu cách khắc phục — đừng phòng thủ; (3) tuyệt đối giữ ranh giới calibrated: **code = "significant/Wilcoxon"**, **math = "directional/pilot n=2"**, **epistemic = "co-occurrence/giả thuyết"**.

### A. Phương pháp & lựa chọn thiết kế

- **"Vì sao không so với train-time RLVR / GRPO thông thường?"**
  → Đối tượng nghiên cứu là **test-time discovery trên một bài khó duy nhất** — khác *mục tiêu* với train-time RLVR (vốn nhằm generalize trên cả một phân bố bài). Metric ở đây là **discovery@k** (thời-gian-tới-thành-công đầu tiên), không phải accuracy trên held-out set. So với train-time GRPO sẽ là *so sai loại*: hai bên tối ưu hai hàm mục tiêu khác nhau. Baseline đúng nghĩa là **student-first SDPO** (cùng regime, cùng mục tiêu) — và tôi so trực tiếp với nó, cộng thêm **best-of-k** làm mốc compute.

- **"Vì sao dùng LoRA thay vì full fine-tuning?"**
  → Ba lý do. (a) Test-time training phải **rẻ và có thể reset**: sau mỗi bài tôi reset về base checkpoint, nên một adapter nhẹ (LoRA r=32) vừa khả thi trên compute cá nhân, vừa sạch khi hoàn tác. (b) Full fine-tune một mô hình 4B *cho từng bài* là bất khả thi ở quy mô này. (c) LoRA **khu trú** cập nhật, đúng tinh thần "minimal-change" mà phương pháp chia sẻ với SDFT.

- **"Vì sao chọn Qwen3-4B, không lớn/nhỏ hơn?"**
  → (a) **Compute**: quy mô cá nhân (Colab L4 / A100) — 4B + LoRA là trần để chạy nổi 8×6 quy mô trung bình cộng pilot toán. (b) **SDPO có self-teaching xuất hiện theo scale**: bài báo gốc cho thấy mạnh ở 8B, ngang ở 0.6B, kém ở 1.5B. 4B nằm trong dải mà self-teaching *được kỳ vọng hoạt động*, nhưng bare student vẫn **đủ yếu để bị kẹt** — đúng chỗ teacher-first phát huy nhất. Tôi cũng nói thẳng: trên base mạnh hơn (8B+), biên teacher-first dự kiến **thu hẹp** (đã ghi ở phần giới hạn).

- **"Chọn 8 bài frontier thế nào? Có selection bias không?"**
  → Chọn theo **model pass-rate ∈ (0,1)** — một *frontier do chính mô hình định nghĩa*, không phải nhãn độ khó của kỳ thi. Lý do: reward chỉ có **phương sai** khi mô hình giải được một bài khoảng 30–70% số lần; ngoài dải đó thì mọi phương pháp bão hòa như nhau, không phân biệt được. Quan trọng: **chọn theo độ khó PRE, mù với kết quả TF-vs-SF** — nên đây là lựa chọn vận hành có nguyên tắc, không phải cherry-pick outcome.

- **"Vì sao pass@16, không phải pass@1 hay pass@100?"**
  → pass@k là ước lượng thực nghiệm của xác suất giải được từ `N_eval` sample. 16 (cho code) cân bằng giữa **phương sai ước lượng** và **chi phí per-step** (vocab ~150k). PRE và POST đều đánh giá **student-only, không context** (nếu để context vào lúc eval thì nó leak thẳng vào metric). discovery@k mới là metric chính; pass@16 là số đọc từng bước.

- **"Vì sao dùng reverse KL (α=1)? Có liên quan gì tới suppression không?"**
  → Câu hỏi rất đúng chỗ. Reverse KL là **mode-seeking** → có xu hướng làm nhọn/thu hẹp phân bố, *về mặt lý thuyết* dễ đè nén các epistemic token hơn forward KL (mode-covering). Tôi dùng α=1.0 để **khớp cấu hình LCBv6** của codebase gốc. Còn **liệu α có điều biến suppression hay không** thì tôi **chưa kiểm** — đây là một câu hỏi RO2 còn mở; một sweep forward-KL / JSD là hướng phát triển tự nhiên.

### B. Thống kê, tính vững & tái lập

- **"Vì sao dùng Wilcoxon signed-rank, không dùng t-test? Có hiệu chỉnh đa so sánh không?"**
  → Wilcoxon là **phi tham số** — phù hợp với POST pass-rate ghép cặp vốn bị chặn trong [0,1], không phân phối chuẩn, và có ties; đây là bản nâng cấp đúng của sign test thô. Test chạy trên **các cặp POST đã ghép** (matched PRE theo từng seed đã loại phương sai base/seed). Con số **p<0.01 là *một* test tổng hợp**, không phải nhiều test song song — nên lạm phát đa-so-sánh không phải mối lo chính; các phân rã theo từng bài chỉ mang tính mô tả.

- **"Escape-zero xuất hiện ở bao nhiêu bài/seed? Có vững không?"**
  → Nó **tái lập trên phần lớn các bài khó** trong tập, với hai anchor chuẩn là **idx64** (TF 0.41 vs SF 0.03) và **idx39** (TF 0.17 vs SF 0.09). Định nghĩa vận hành: SF kẹt ở pass=0 suốt các bước trong khi TF cất cánh. Nó được **kiểm chứng tường minh** là *không* phải artifact của bộ lọc (bộ lọc không bao giờ ép một bản copy vào pool). Chính vì **tái lập được** chứ không phải một seed may mắn nên tôi coi đây là đóng góp cơ chế chính.

- **"6 seed đã đủ chưa? Variance thế nào?"**
  → Thiết kế **matched**: cùng base + cùng seed cho cả hai nhánh → PRE khớp theo từng seed, loại được phương sai mức base và mức seed khỏi phép so sánh. 8×6 = 48 quan sát ghép cặp, đủ lực cho Wilcoxon. Tôi ghi thẳng ở §6.1 rằng mở rộng lên **16×16** sẽ nâng lực thống kê thêm. Riêng toán ở **n=2** là *thiếu lực có chủ đích* — nên mọi kết luận toán chỉ ở mức directional.

- **"Judge là một LLM đi chấm output của LLM — có vòng lặp/thiên lệch không?"**
  → Điểm mấu chốt: **judge KHÔNG quyết định tính đúng** — đúng/sai do **verifier** (chạy test thật) quyết, đó là ground truth. Judge chỉ là **cổng độc lập** (`is_copy`), nên dù judge có sai thì nó **không thể để lọt một lời giải sai**. Về rủi ro vòng lặp LLM-chấm-LLM: tôi có **ablation judge-invariance** — difflib (so chuỗi thuần cơ học, *không* dùng LLM) so với LLM judge — và escape-zero **giữ nguyên dưới cả hai**. difflib thuần cơ học loại trừ khả năng kết quả do thiên lệch của LLM judge.

### C. Tính trung thực của các tuyên bố (những câu dễ bị soi nhất)

- **"n nhỏ (nhất là toán) thì kết luận có chắc không?"**
  → Phải **tách bạch hai miền**. **Code là quy mô trung bình**: 48 quan sát ghép cặp, Wilcoxon **p<0.01** — có lực thống kê thật. **Toán là pilot n=2** — tôi **không** tuyên bố ý nghĩa thống kê ở đó; mọi phát biểu toán đều gắn cờ *"directional / sơ bộ"*. Đóng góp chính (RO-method, escape-zero, compute-fair) **hoàn toàn dựa trên kết quả code**.

- **"Suppression có LÀM tăng correctness không?"** *(câu nhạy cảm nhất)*
  → **Không, tôi không khẳng định vậy.** Tôi chỉ quan sát **co-occurrence** (đồng biến). Đồng biến ≠ nhân quả; và chiều nhân quả hợp lý thậm chí có thể **ngược lại hoặc là nguyên nhân chung**: việc *cài được một thủ tục đúng, chạy được* vừa làm tăng held-out correctness, vừa làm bớt hedging (mô hình tự tin vì nó **thật sự biết cách làm**). "Consolidation có lợi" là một **giả thuyết nhất quán với dữ liệu**. Phép kiểm sạch là một **ablation ref-type cùng-domain** (reference chỉ-có-giá-trị vs mang-phương-pháp, cùng trên code, giữ nguyên mọi thứ khác) — tôi **chưa làm**, đây là future work. Ở math leak regime, cùng một suppression bề mặt lại đi cùng việc *chép đáp án* — cho thấy ý nghĩa của suppression **phụ thuộc regime**, đúng như Kim et al. chỉ ra.

- **"Đã cô lập được 'reference type' như biến nhân quả chưa?"**
  → **Chưa.** Việc **dùng cùng một Qwen3-4B** đã loại được confounder *năng lực mô hình*. Nhưng **budget vẫn khác** (code 15 bước / teacher_n=10, toán 3 bước / teacher_n=4) — đây là confounder còn lại. Tôi phát biểu reference-type là biến **chính (primary operative)**, và đọc tương phản code-vs-math theo hướng **directional**. Cách cô lập dứt điểm là **ablation ref-type cùng-domain trên code**.

- **"Tại sao toán thất bại — có phải lỗi pipeline không?"**
  → **Không, đây là kết quả ranh giới, không phải bug.** AIME chỉ cho **một giá trị số tĩnh**, không có lời giải từng bước. Khi base model không tự giải được, privileged context **suy biến**: teacher chỉ chép được con số `\boxed{}`, không trích ra được thủ tục nào để distill. Log verifier-judge (idx8, Phụ lục D.2) xác nhận: **mọi** quỹ đạo teacher đều bị gắn cờ copy → good pool rỗng → **không có tín hiệu học nào**. Bộ lọc hành xử **đúng như thiết kế**; thất bại là **bản chất của feedback chỉ-có-đáp-số**. Con đường gỡ nút là **MATH-500** (có trường `solution`, tức reference mang phương pháp) — future work.

### D. Định vị, tính mới & ý nghĩa

- **"Đóng góp mới thực chất so với SDPO gốc là gì?"**
  → Bốn điểm. (1) **Tổ chức teacher-first**: distill các generation *của teacher* đã lọc, thay vì rollout thất bại của student — nằm giữa SDPO (on-policy) và SFT (off-policy), với bộ lọc anti-copy sạch. (2) **Giao thức đánh giá compute-fair** (compute-matched + compute-to-correct) — biến một lợi thế chỉ-ở-kết-quả thành lợi thế *có ý thức về compute*. (3) **Đo epistemic verbalization trong regime test-time code** — bài báo gốc *chạm* tới test-time nhưng không đo epistemics. (4) **Đặc trưng hóa ranh giới value-versus-procedure**. Nói thẳng về phạm vi: đây là một **đặc trưng hóa thực nghiệm trong một mô hình 4B**, không phải một thuật toán mới tuyên bố tính phổ quát.

- **"Teacher-first chẳng qua là SFT thêm vài bước — khác gì SFT?"**
  → Gần nhưng không đồng nhất. SFT fine-tune trên **demonstration cố định** với **nhãn cứng**. Teacher-first distill một **phân bố mềm per-token** (top-K reverse KL) về phía các quỹ đạo **do chính mô hình sinh, điều kiện hóa trên feedback, đã lọc** — context là **execution feedback kiểu SDPO**, không phải demo cố định; target là phân bố mềm chứ không phải one-hot. Nó giống **SDFT** ở chỗ distill về các generation-tự-sinh-có-điều-kiện, nhưng dùng execution feedback làm context.

- **"Mô hình có chỉ đang *memorize* bài đó không?"**
  → Với code, correctness chấm trên **private test (held-out)**, không phải public test đã đưa trong feedback. Một mức tăng pass@16 ở đó nghĩa là chương trình distill **generalize sang input chưa thấy** — tức một *phương pháp được cài đặt*, không phải output ghi nhớ. Ví dụ idx12 (Phụ lục D.5): PRE tính giai thừa (**hiểu ngược đề**) → POST là thuật toán lặp tìm N, đúng cho **mọi** input. Đây chính là điểm value-versus-procedure được cụ thể hóa.

- **"Sau TTT trên một bài, mô hình có bị hỏng cho bài khác (catastrophic forgetting)?"**
  → Theo giao thức, tôi **reset về base checkpoint sau mỗi bài** — adapter update là *per-problem và bị bỏ đi* — nên **không có forgetting chéo bài** trong quá trình đánh giá. Trong phạm vi một bài, bài báo gốc cho thấy SDPO quên *ít hơn* SFT trên held-out benchmark (nhờ tính on-policy), tuy hơn GRPO một chút. Vì tôi reset, forgetting không phải mối lo cho metric discovery.

- **"Ứng dụng thực tế ở đâu?"**
  → Bất kỳ tình huống nào có **một instance khó, verifiable** và một **ngân sách compute chi tại inference**: một bài competitive-programming cụ thể chưa giải được, agentic coding nơi có thể chạy test, các tác vụ gần formal-verification. Giá trị cốt lõi là **hiệu quả compute-to-correct** — đạt lời giải với ít generation hơn best-of-k. Giới hạn trung thực: mới chứng minh trên LCBv6 với mô hình 4B; muốn triển khai thực tế cần validate ở scale lớn hơn (8B+, benchmark code thứ hai).

- **"discovery@k khác pass@k thế nào — vì sao cần metric riêng?"**
  → pass@k giả định sampling **i.i.d.** (các attempt độc lập). Ở test-time, các attempt **tuần tự, chia sẻ trạng thái và cập nhật trọng số** giữa các bước — nên pass@k i.i.d. không còn áp dụng. discovery@k = $P(T \le k)$ với $T$ là bước đầu tiên giải được, tổng quát hóa pass@k sang thuật toán tuần tự, và **thu về đúng pass@k** khi thuật toán chỉ là best-of-k thuần. Nó cùng dòng dõi với performance profile time-to-termination của Dolan & Moré.

---

### Mẹo trình bày
- 16 slide / 15 phút ≈ **~1 phút/slide** (slide 16 chỉ vài giây); dồn thời gian cho slide 8–9–12 (kết quả chính + insight), lướt nhanh 6–7 (RO + setup).
- Slide 9 (escape-zero) và slide 12 (boundary) là **hai điểm nhớ** — nói chậm, chỉ vào hình.
- Luôn neo vào hình: "đường phẳng vs đường đi lên", "cột xanh cao hơn cột cam".
- **Kỷ luật calibrated:** với code dùng "significant / Wilcoxon"; với toán và epistemic dùng "co-occurs / directional / giả thuyết". Đừng bao giờ nói "suppression giúp tăng correctness" hay "đã cô lập reference type".
