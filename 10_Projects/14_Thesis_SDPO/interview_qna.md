---
type: prep
created: 2026-08-22
tags: [interview, thesis, qna, prep]
---

# Interview Q&A — Thesis SDPO (test-time)

Script ôn phỏng vấn. Câu trả lời viết theo lối **nói**, không phải lối viết. Mỗi câu 20–40 giây là đủ; họ muốn nghe tiếp thì sẽ hỏi đuổi.

---

## 0. Ba thứ phải thuộc lòng

**Pitch 30 giây:**
> Em nghiên cứu cách một LLM tự cải thiện ngay lúc suy luận trên một bài lập trình khó, bằng cách học từ phản hồi khi chạy code — test nào fail, lỗi gì. Phương pháp gốc gọi là SDPO: model khi được cho thêm feedback đóng vai "thầy" của chính nó, và phân bố dự đoán của thầy được distill ngược vào "trò". Vấn đề là bản gốc học từ chính bài làm sai của trò, mà trên bài khó thì trò gần như không bao giờ làm đúng — nên chẳng có gì đúng để học. Em đảo lại: để thầy sinh lời giải trước, lọc lấy cái đúng và độc lập, rồi mới cho trò học theo.

**Một con số:** trên bài khó nhất, phương pháp của em đạt **0.41 pass@16 so với 0.05** của baseline.

**Một hạn chế tự nêu:** *"Hiện tại compute chưa được cân bằng — phương pháp của em sinh nhiều mẫu hơn baseline khoảng 2.5 lần. Em đang chạy phiên bản cân bằng compute để kiểm chứng."*

---

## A. Tổng quan

**Q: Kể ngắn gọn về đồ án của em.**
→ Dùng pitch 30 giây ở trên.

**Q: Tại sao em chọn đề tài này?**
→ Nó xuất phát từ phần Future Work của paper gốc — họ viết thẳng rằng cần nghiên cứu có hệ thống xem cách trình bày feedback ảnh hưởng hành vi model thế nào. Cùng lúc có một paper khác phản biện rằng self-distillation làm model mất khả năng thể hiện sự không chắc chắn. Hai hướng đó chưa ai kiểm ở regime test-time trên code, nên đó là khoảng trống rõ ràng và vừa sức làm trong một đồ án.

**Q: Test-time training là gì? Giải thích cho người ngoài ngành.**
→ Bình thường model được train xong rồi đem đi dùng, trọng số cố định. Test-time training là: khi gặp một bài khó cụ thể, mình cho model tự cập nhật trọng số ngay tại chỗ để giải riêng bài đó — như một sinh viên được phép ôn lại đúng dạng bài đang làm. Giải xong thì reset về ban đầu.

**Q: Ứng dụng thực tế ở đâu?**
→ Bất kỳ chỗ nào có **một bài khó và có cách kiểm tra tự động**: một bài competitive programming chưa giải được, agent viết code có thể chạy test, các tác vụ gần formal verification. Giá trị là đổi compute lấy lời giải cho đúng bài đang cần.

---

## B. Nền tảng

**Q: SDPO là gì?**
→ Self-Distillation Policy Optimization. Ý chính: cùng một model, khi được cho thêm feedback vào context, sẽ dự đoán tốt hơn phiên bản không có feedback. Ta lấy phân bố next-token của phiên bản "có feedback" làm mục tiêu, rồi kéo phiên bản "không feedback" về phía đó bằng KL divergence. Cả hai dùng chung trọng số nên gọi là *self*-distillation.

**Q: Khác gì GRPO?**
→ GRPO chỉ có một con số reward cho cả câu, và mọi token trong câu chia nhau đúng con số đó — tín hiệu rất thưa. SDPO cho mỗi token một **phân bố** mục tiêu, nên thông tin dày hơn nhiều. Quan trọng hơn: nếu cả nhóm rollout đều sai thì advantage của GRPO về 0 và không học được gì, còn SDPO vẫn có tín hiệu từ feedback.

**Q: SDPO có phải là DPO không?** *(bẫy tên gọi)*
→ Không. DPO học từ **cặp so sánh do người đánh giá** (A tốt hơn B). SDPO không có preference nào cả — nó là **distillation**, học bằng cách khớp phân bố xác suất giữa hai phiên bản của cùng một model.

**Q: Sao không dùng một model lớn hơn làm thầy?**
→ Vì mục tiêu là **nâng trần năng lực**, không phải nén một model có sẵn. Nếu đã có model mạnh hơn thì bài toán khác rồi. Ở đây "thầy" chỉ là chính model đó nhưng được nhìn thêm feedback — nên không cần model ngoài.

**Q: pass@k và discovery@k khác nhau chỗ nào?**
→ pass@k giả định các lần thử **độc lập** với nhau. Ở test-time, các lần thử **nối tiếp và có cập nhật trọng số** giữa chừng, nên không còn độc lập. discovery@k là xác suất giải được trong k lần thử đầu, dùng được cho thuật toán tuần tự. Khi thuật toán chỉ là sampling thuần thì hai cái trùng nhau.

---

## C. Phương pháp

**Q: Teacher-first là gì? Khác bản gốc chỗ nào?**
→ Bản gốc (student-first): trò làm bài → thường sai → thầy chấm lại từng token của **chính bài sai đó** → trò học theo. Vấn đề: trên bài khó, bài sai vẫn cứ là bài sai, không có gì đúng để học.
Của em (teacher-first): **thầy sinh trước** vài lời giải dưới feedback → verifier chạy test kiểm đúng/sai → judge kiểm xem có phải chép reference không → chỉ những lời giải **vừa đúng vừa độc lập** mới được đưa cho trò học.
Điểm khác duy nhất là **học theo quỹ đạo nào** — loss, model, hyperparameter giữ nguyên hết để so sánh sạch.

**Q: "Flat-reward trap" là gì?**
→ Trên bài khó, mọi lần thử đều sai → mọi reward đều bằng 0 → không có chênh lệch nào để tạo gradient → model đứng im. Nó kẹt ở đúng những bài mình quan tâm nhất.

**Q: Judge để làm gì?**
→ Để tránh chuyện thầy chỉ **chép** reference thay vì thực sự nghĩ. Nếu cứ thế distill thì trò học cách chép, không học được cách giải. Em thử hai loại judge: một cái so chuỗi thuần (difflib), một cái dùng LLM so ngữ nghĩa.

**Q: Sao dùng LoRA mà không full fine-tune?**
→ Ba lý do. Một, test-time training phải rẻ và **reset được** — sau mỗi bài em reset về checkpoint gốc. Hai, full fine-tune một model 4B cho **từng bài** là bất khả thi với compute cá nhân. Ba, LoRA khu trú cập nhật lại, đúng tinh thần "thay đổi tối thiểu".

**Q: Sao chọn Qwen3-4B?**
→ Paper gốc cho thấy khả năng tự làm thầy **xuất hiện theo scale**: mạnh ở 8B, ngang ở 0.6B, kém hơn ở 1.5B. 4B nằm trong dải mà tự-làm-thầy đã hoạt động, nhưng model trần vẫn **đủ yếu để bị kẹt** — đúng chỗ phương pháp của em phát huy. Cộng thêm giới hạn compute cá nhân.

**Q: Loss cụ thể là gì?**
→ KL divergence theo từng token giữa phân bố của trò và phân bố của thầy, cộng dồn trên các lời giải đã lọc. Thầy được `stopgrad` — không cho gradient chảy qua, nếu không thầy sẽ tự sụp về trò và bỏ qua feedback. Dùng top-K = 20 để tiết kiệm bộ nhớ (vocab ~150k), reverse KL, importance-sampling clip 2.0, AdamW lr 1e-5.

---

## D. Thực nghiệm & kết quả

**Q: Setup thế nào?**
→ Qwen3-4B + LoRA, LiveCodeBench v6. Mỗi bài: reset về base, chạy 15 bước test-time training, đánh giá trò bằng pass@16 trước và sau. 4 bài, 4 seed. Chạy trên Colab L4 và Modal A100.

**Q: Chọn bài thế nào? Có cherry-pick không?**
→ Chọn theo **tỉ lệ pass của chính model**, giữ những bài model giải được nhưng không ổn định — pass nằm giữa 0 và 1. Lý do: bài luôn giải được hoặc không bao giờ giải được thì reward **không có phương sai**, mọi phương pháp đều như nhau, không phân biệt được gì.
Quan trọng: chọn **theo độ khó đo trước khi chạy**, không nhìn kết quả so sánh. Nên không phải cherry-pick.

**Q: Kết quả chính?**
→ Thiết kế **matched**: hai phương pháp chạy cùng base, cùng seed, nên điểm trước khi train khớp nhau từng seed — loại được nhiễu do seed. Teacher-first **bằng hoặc hơn baseline ở mọi seed**, không bao giờ thua. Trên nhóm bài khó là 9 thắng, 3 hoà, 0 thua. Bài mạnh nhất là 0.41 so với 0.05.

**Q: "Escape-zero" là gì?**
→ Có những seed mà baseline đứng nguyên ở **đúng 0** suốt 15 bước, trong khi phương pháp của em nhấc lên khỏi 0. Đó là dấu hiệu trực tiếp của flat-reward trap: on-policy không có gì đúng để học, còn tiêm một lời giải đúng từ thầy thì có.
*Tự nêu thêm:* một vài instance này **không tái lập khi chạy lại cùng seed** — em có ghi rõ trong phụ lục.

**Q: Kết quả về template thì sao?**
→ Có hướng: template ép model phân tích nguyên nhân trước rồi sửa cho kết quả tốt hơn template chuẩn, tốt hơn template tối giản. **Nhưng em nói thẳng là số tuyệt đối quá nhỏ** — chênh nhau cỡ 1 đến 4 mẫu đúng trên 32 — nên nó nằm trong ngưỡng nhiễu. Em trình bày như một quan sát định hướng, không phải kết luận.

**Q: Phần math thì sao?**
→ Em thử mở rộng sang AIME. Kết quả là **không thoát** — model vẫn 0 điểm sau khi train. Nhưng cách nó thất bại lại có ích: judge bắt được khoảng 75–80% quỹ đạo của thầy chỉ là **chép đáp án** chứ không phải suy ra. Với code, "lời giải" chính là **một chương trình**, tức là một phương pháp dùng lại được cho input mới. Với AIME, đáp án chỉ là **một con số** — chép xong cũng không học được gì.
*Tự nêu:* phần math có nhiều confound — khác model, khác budget, khác kiểu reference — nên em trình bày như **giả thuyết**, không phải kết luận.

---

## E. Câu khó — soi tính trung thực

**Q: Có phải phương pháp của em thắng chỉ vì sinh nhiều mẫu hơn không?**
→ *(Chủ động nói trước khi bị hỏi)* Đúng là hiện tại chưa cân bằng compute — em sinh khoảng 2.5 lần nhiều hơn. Nhưng lợi thế không nằm ở **số mẫu** mà ở **tỉ lệ trúng mỗi mẫu**: baseline cần **trò trần** làm đúng, còn em cần **thầy có feedback** làm đúng — hai tỉ lệ này cách nhau rất xa. Log cho thấy thầy đạt reward 1.0 từ bước thứ hai, còn trò trước khi train thường 0/16. Cân bằng số mẫu không xoá được chênh lệch về chất lượng phân phối. Và em đang chạy phiên bản cân bằng compute để kiểm chứng đúng câu hỏi này.

**Q: n nhỏ như vậy thì kết luận có đáng tin không?**
→ Em không tuyên bố chứng minh. Em dùng từ "có hướng" và "weak dominance". Cái đáng tin là **tính nhất quán về hướng**: 4 bài độc lập, không bài nào thua. Cái chưa đáng tin là độ lớn và mức ý nghĩa thống kê. Em đang mở rộng quy mô để xử lý đúng điểm này.

**Q: Sao không so với GRPO?**
→ Khác mục tiêu. GRPO train-time nhắm generalize trên cả một phân bố bài; em nhắm giải **một bài cụ thể** nhanh nhất. Metric khác, hàm mục tiêu khác — so sẽ là so nhầm loại. Baseline đúng cùng regime là student-first SDPO, và em so trực tiếp với nó.

**Q: Model có đang học vẹt đúng bài đó không?**
→ Không. Điểm được chấm trên **test riêng (private)**, không nằm trong feedback đưa cho model. Ví dụ cụ thể: trước khi train, model tính giai thừa của X — tức hiểu ngược đề. Sau khi train, nó viết vòng lặp tìm N sao cho N! = X, đúng cho **mọi** input. Đó là một thuật toán, không phải đáp án ghi nhớ.

**Q: Dùng LLM để chấm LLM có bị thiên lệch không?**
→ Judge **không quyết định đúng/sai** — cái đó do verifier chạy test thật quyết, đó là ground truth. Judge chỉ kiểm "có chép không". Nên judge sai cũng **không thể để lọt một lời giải sai**. Và em có ablation: so difflib (thuần so chuỗi, không dùng LLM) với LLM judge — kết quả không đổi. Cái thuần cơ học đó loại trừ khả năng thiên lệch của LLM.

**Q: Điểm yếu lớn nhất của đồ án là gì?**
→ Quy mô mẫu. 4 bài, 4 seed là quá nhỏ để nói mạnh. Thứ hai là chưa cân bằng compute. Cả hai em đều biết rõ và đang xử lý. Điểm yếu thứ ba là phần math có nhiều confound nên em chỉ dám để ở mức giả thuyết.

**Q: Nếu chạy lại từ đầu, em làm khác gì?**
→ Em sẽ cân bằng compute **ngay từ đầu** thay vì để thành lỗ hổng phải vá sau. Và em sẽ dùng **cùng một model cho cả code lẫn math** — hiện tại hai domain dùng hai model khác nhau nên không quy kết được nguyên nhân.

---

## F. Kỹ thuật & debugging

**Q: Kể một bug khó em từng gặp.**
→ Model cứ sinh ra văn bản lảm nhảm thay vì code, reward 0 mọi bước. Em in completion ra qua hàm reward, thấy nó đang **viết tiếp đề bài**. In tiếp prompt mà trainer thực nhận, rồi đếm token: 644 token, trong khi TRL mặc định `max_prompt_length = 512` — nó **âm thầm cắt cụt đề bài trong lúc training**, còn code eval của em thì không cắt, nên eval trông vẫn bình thường. Sửa lên 4096 là hết.
Bài học: bug này **làm mất hiệu lực mấy kết luận trước đó** của em, nên em phải chạy lại và ghi rõ trong log.

**Q: Chỗ nào trong code dễ sai nhất?**
→ Căn chỉnh token. Prompt của trò là `đề + lời giải`, prompt của thầy là `đề + feedback + lời giải` — **prefix dài khác nhau**, nên phải lấy logits đúng vị trí của phần lời giải ở **mỗi bên riêng**. Lệch một token là KL sai mà không báo lỗi gì cả. Em thêm assert kiểm tra hai lát cắt bằng độ dài và log cả hai prefix length ra.

**Q: Xử lý giới hạn API của judge thế nào?**
→ groq giới hạn 100 nghìn token/ngày, tính ra chỉ khoảng **4 run/ngày** — không đủ. Em làm chuỗi provider: groq chính, gemini dự phòng, difflib chốt cuối; cộng thêm cache để không chấm lại cùng một candidate. Sau khi có ablation chứng minh kết quả không phụ thuộc judge, em chuyển hẳn sang difflib cho các run chính vì nó **tái lập được** và miễn phí.

**Q: Chạy trên hạ tầng gì?**
→ Colab L4 22GB cho các run nhẹ, Modal A100-80GB cho run nặng. Trên Modal em dùng `.spawn()` với `--detach` để run không chết khi máy em mất kết nối, và bật retry để chống preempt. Log toàn bộ lên W&B: số lời giải tốt/xấu mỗi bước, similarity trung bình, loss, verdict của judge.

---

## G. Định vị & hướng tiếp

**Q: Đóng góp mới so với paper gốc là gì?**
→ Ba thứ. Một, **tổ chức teacher-first** — distill lời giải đã lọc do thầy sinh, thay vì bài sai của trò. Hai, bằng chứng cho thấy ở scale 4B thì **tiền đề của paper gốc bị yếu đi**: họ nói không cần lời giải đúng vẫn học được, em thấy trên model nhỏ thì cần. Ba, đặc trưng hoá **khi nào** phương pháp hoạt động — cần reference chứa phương pháp, không chỉ đáp án.
Em nói rõ phạm vi: đây là một **nghiên cứu thực nghiệm trên một model 4B**, không phải một thuật toán mới tuyên bố tính phổ quát.

**Q: Nó chẳng qua là SFT thôi phải không?**
→ Gần nhưng khác. SFT học bằng **nhãn cứng** trên demonstration cố định. Ở đây mục tiêu là **phân bố mềm theo từng token**, và quỹ đạo là do **chính model sinh ra dưới feedback**, không phải demo bên ngoài. Nó nằm giữa on-policy SDPO và off-policy SFT.

**Q: Hướng tiếp theo?**
→ Chuyển sang **train-time**: dataset nhiều bài, có baseline GRPO thật, có eval trên tập ngoài phân bố — ở đó câu hỏi về quên kiến thức và độ phủ tác vụ mới đo được đúng nghĩa. Và khử confound bằng cách dùng **cùng một model cho cả hai domain**, với reference mang phương pháp (MATH-500 có sẵn lời giải từng bước) thay vì chỉ đáp số.

**Q: Em học được gì lớn nhất từ đồ án này?**
→ Cách **hiệu chỉnh kết luận theo đúng mức bằng chứng**. Ban đầu em có kết quả trông rất đẹp trên 1 seed, nhưng khi tăng lên 4 seed với eval 16 mẫu thì hoá ra một phần là nhiễu. Từ đó em học cách thiết kế so sánh matched, tự đi tìm confound của chính mình, và viết ra những chỗ mình chưa chắc thay vì giấu đi.

---

## H. Không nên nói

- ❌ "distributed training" — em chạy **một GPU mỗi run**, song song nhiều run. Không phải DDP/FSDP.
- ❌ "preference optimization" — SDPO là **distillation**, không có preference.
- ❌ "em chứng minh được..." — dùng "kết quả có hướng", "sơ bộ".
- ❌ Bất kỳ con số nào từ bản best-case (Wilcoxon p<0.01, 16 bài × 6 seed, math escape) — **những cái đó chưa chạy**.
- ❌ "suppression giúp tăng correctness" — chỉ là đồng biến, chưa phải nhân quả.

## Mẹo

- Câu về **giới hạn**: thừa nhận thẳng trước, rồi mới nói cách khắc phục. Đừng phòng thủ.
- Không biết thì nói **"cái đó em chưa kiểm"** — mạnh hơn đoán bừa rất nhiều.
- Luôn neo vào **một con số cụ thể** (0.41 vs 0.05) rồi mới mở rộng.
- Nếu bí, quay về: *"bản chất là học từ lời giải đúng do thầy sinh, thay vì học từ bài sai của trò."*
