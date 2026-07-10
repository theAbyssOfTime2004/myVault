

Giờ đến phần **cách đọc & trình bày hàm loss teacher-first**. Công thức:

$$\mathcal{L}_{\text{TF}}(\theta) = \sum_{y \in \mathcal{G}} \sum_{t=1}^{|y|} \mathrm{KL}\Big(\pi_\theta(\cdot|x, y_{<t}) ,\big|, \mathrm{stopgrad},\pi_\theta(\cdot|x, c, y_{<t})\Big)$$

## Nguyên tắc: nói 1 câu tóm tắt TRƯỚC, rồi mới bóc từng phần

Đừng đọc công thức từ trái sang phải như đọc chữ. Hãy **cho khán giả cái khung trước**:

> "Đây là hàm mất mát của teacher-first. Về bản chất nó **đo student lệch teacher bao nhiêu tại mỗi token**, rồi cộng dồn lại; huấn luyện là cực tiểu hoá nó."

Sau câu đó, bóc theo thứ tự **từ trong ra ngoài** (phần lõi có nghĩa nhất trước, các dấu tổng để sau).

## Thứ tự đọc — 5 bước

**Bước 1 — Hai phân bố bên trong KL (trái tim của công thức).** Chỉ tay vào hai vế trong ngoặc KL:

- $\pi_\theta(\cdot,|,x, y_{<t})$ = **student**: cho đề $x$ và các token đã sinh $y_{<t}$, đây là phân bố xác suất mà mô hình gán cho **token kế tiếp** — bản **không** có context.
- $\pi_\theta(\cdot,|,x, c, y_{<t})$ = **self-teacher**: **cùng mô hình đó, cùng $\theta$**, nhưng được cho thêm **context $c$** (feedback + few-shot) — bản **có** context.
- → Nhấn: _"cùng một mô hình, chỉ khác cái nó được thấy → nên gọi là **self**-distillation."_

**Bước 2 — Dấu KL giữa hai phân bố đó.** $\mathrm{KL}(,\text{student},|,\text{teacher},)$ = "khoảng cách" giữa hai phân bố. Loss muốn nó **nhỏ**, tức **kéo phân bố của student về gần phân bố của teacher**.

- → _"Teacher, nhờ có context, biết token đúng nên là gì; ta ép student bắt chước phân bố đó."_

**Bước 3 — `stopgrad` trên teacher.** Đây là chi tiết kỹ thuật quan trọng nhất: khi tính gradient, **teacher bị đóng băng** — chỉ **student** được cập nhật để tiến về teacher, teacher đứng yên làm "mục tiêu cố định".

- → _"Nếu không chặn, cả hai cùng chạy lại gần nhau, teacher sẽ **sụp vào** student và **bỏ qua context $c$** — mất luôn tác dụng của feedback."_

**Bước 4 — Dấu tổng bên trong $\sum_{t=1}^{|y|}$ (theo token).** Cộng KL trên **từng vị trí token** $t$ của quỹ đạo $y$.

- → _"Không phải một tín hiệu cho cả câu, mà **mỗi token một tín hiệu** — đây là credit assignment **dày** đã nói ở slide trước."_

**Bước 5 — Dấu tổng bên ngoài $\sum_{y \in \mathcal{G}}$ (theo quỹ đạo).** Cộng trên **mọi quỹ đạo tốt $y$ trong good pool $\mathcal{G}$** (các lời giải đúng + độc lập đã lọc).

- → **Đây là chỗ khác duy nhất so với student-first:** student-first cộng trên **một** $y_{\text{student}}$ **sai**; teacher-first cộng trên các $y_{\text{good}}$ **đúng**.

## Câu chốt (nói sau cùng)

> "Cùng một dạng KL như SDPO gốc, nhưng vì ta cộng trên **quỹ đạo đúng của teacher** thay vì attempt sai của student, nên **luôn có tín hiệu đúng để học** — đó chính là cách né flat-reward trap."

---

## Kịch bản đọc thành lời (liền mạch, ~40 giây)

> "Đây là hàm loss teacher-first. Trong ngoặc KL có hai phân bố: bên trái là **student** — mô hình khi chỉ thấy đề bài; bên phải là **self-teacher** — cũng chính mô hình đó nhưng được cho thêm context $c$. KL đo khoảng cách giữa chúng, và ta **kéo student về phía teacher**. Chữ `stopgrad` nghĩa là teacher bị đóng băng, chỉ student học — nếu không, teacher sẽ sụp vào student và bỏ qua feedback. Hai dấu tổng: cái trong cộng trên **từng token**, cái ngoài cộng trên **mọi quỹ đạo tốt trong good pool**. Và điểm khác biệt duy nhất với SDPO gốc chính là ở dấu tổng ngoài này: ta học từ **quỹ đạo đúng đã lọc**, chứ không phải từ attempt sai của student — nhờ vậy thoát được flat-reward trap."

---

## Vài lưu ý khi trình bày

- **Chỉ tay theo thứ tự** đang nói (hai π → KL → stopgrad → hai Σ). Khán giả nhìn theo tay sẽ hiểu nhanh gấp đôi.
- **Đừng sa vào chi tiết** top-K/reverse KL/α trên slide chính — để dành trả lời nếu hội đbàn hỏi (đã có trong Q&A).
- Nếu bị hỏi **"gradient trông thế nào"**: $\partial\mathcal{L}/\partial z_v = \pi_S(v) - \pi_T(v)$ — token nào teacher tin hơn student thì optimizer nâng logit đó lên. (Câu này rất "ăn điểm" nếu nói tự tin.)

Muốn tôi **nhét bản "thứ tự đọc 5 bước" này (rút gọn) vào speaker-note của slide 5** trong script để bạn khỏi phải nhớ không?