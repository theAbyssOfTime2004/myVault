## Đề 3 — Câu 2: Lời giải đầy đủ

**Số liệu:** $n=0{,}6$ mol $=6\times10^{-4}$ kmol, $R=8{,}31\times10^3$ J/(kmol.K) → $nR=4{,}986$ J/K; $i=5$ (lưỡng nguyên tử) → $\gamma=\dfrac{i+2}{i}=1{,}4$; $P_1=1{,}8\times10^5$ N/m², $V_1=8\times10^{-3}$ m³; $V_2=V_1$ (đẳng tích 1-2); $V_3=24\times10^{-3}$ m³; $P_3=P_1$ (đẳng áp 3-1).

### a) Tính $P_2$, $T_1$, $T_3$

**$T_1$:** $\quad T_1 = \dfrac{P_1V_1}{nR} = \dfrac{1{,}8\times10^5\times0{,}008}{4{,}986} = \dfrac{1440}{4{,}986} \approx \boxed{288{,}8\ \text{K}}$

**$T_3$:** vì $P_3=P_1$, nên $T_3 = T_1\times\dfrac{V_3}{V_1} = 288{,}8\times3 \approx \boxed{866{,}4\ \text{K}}$

**$P_2$:** dùng phương trình đoạn nhiệt (2→3), với $V_2=V_1$: $$P_2V_2^\gamma = P_3V_3^\gamma \Rightarrow P_2 = P_3\left(\frac{V_3}{V_2}\right)^\gamma = 1{,}8\times10^5\times3^{1{,}4} = 1{,}8\times10^5\times4{,}655$$ $$\boxed{P_2 \approx 8{,}38\times10^5\ \text{N/m}^2 \approx 8{,}38\ \text{atm}}$$

Từ đó: $T_2 = \dfrac{P_2V_2}{nR} = \dfrac{8{,}38\times10^5\times0{,}008}{4{,}986} \approx 1344{,}5\ \text{K}$

### b) Độ biến thiên nội năng cả chu trình

Vì đây là **chu trình kín** (trạng thái đầu = trạng thái cuối), nội năng là hàm trạng thái: $$\boxed{\Delta U_{chu,trình} = 0}$$

_(Kiểm chứng: $\Delta U_{12}=nC_V(T_2-T_1)\approx13160$J; $\Delta U_{23}=nC_V(T_3-T_2)\approx-5960$J; $\Delta U_{31}=nC_V(T_1-T_3)\approx-7200$J → tổng $\approx0$ ✓)_

### c) Công khí thực hiện trong toàn bộ chu trình

**Đẳng tích (1→2):** $A_{12}=0$

**Đoạn nhiệt (2→3):** $Q=0 \Rightarrow A_{23} = -\Delta U_{23} = -(-5960) = +5960\ \text{J}$

**Đẳng áp (3→1):** $A_{31} = P_3(V_1-V_3) = 1{,}8\times10^5\times(0{,}008-0{,}024) = -2880\ \text{J}$

**Tổng công cả chu trình:** $$A = 0+5960-2880 = \boxed{3080\ \text{J}}$$

### d) Hiệu suất động cơ

Tính nhiệt lượng từng quá trình:

- $Q_{12} = \Delta U_{12} \approx 13160$ J (**nhận**)
- $Q_{23} = 0$
- $Q_{31} = nC_P(T_1-T_3) \approx -10080$ J (**thải**)

$$Q_{nhận} = 13160\ \text{J} \qquad Q_{thải}=10080\ \text{J}$$

_(Kiểm tra: $Q_{nhận}-Q_{thải}=13160-10080=3080$J $=A$ ✓ khớp với câu c)_

$$\eta = \frac{A}{Q_{nhận}} = \frac{3080}{13160} \approx \boxed{23{,}4\%}$$



## Đề 4 — Câu 1 (2 điểm)

**Tóm tắt:** mặt phẳng nghiêng dài $L=1{,}0$ m, $\theta=30°$, $g=10$ m/s², quả cầu **đặc** lăn không trượt, thả từ đỉnh ($v_0=0$), $I=\dfrac25mR^2$.

**Tìm:** vận tốc $v$ của quả cầu ở cuối mặt phẳng nghiêng.

## Đề 4 — Câu 2 (4 điểm)

**Tóm tắt:** $m_1=3{,}0$ kg (trên mặt nghiêng $\alpha=30°$, $k=0{,}25$), $m_2=6{,}0$ kg (treo, cách đất $h=5{,}0$m), ròng rọc **vành tròn** $M=2{,}0$ kg (chú ý: khác Đề 3 — vành tròn có $I=MR^2$, không phải $\frac12MR^2$ như đĩa đặc), $g=10$ m/s², hệ khởi hành từ nghỉ.

## Đây là dạng gì?

Vẫn khung τ=Iβ quen thuộc (mặt nghiêng có ma sát + vật treo qua ròng rọc), nhưng có **2 điểm mới**:

1. Ròng rọc là **vành tròn** ($I=MR^2$) — công thức khác đĩa đặc.
2. Câu d) là biến thể mới của "dạng bài tủ dây đứt": ở đây không phải dây đứt, mà là **$m_2$ chạm đất** khiến dây bị chùng — về bản chất xử lý **giống hệt** dạng dây đứt đã học.

## Hướng dẫn

**a) Gia tốc và lực căng dây:**

$$T_1 - m_1g\sin\alpha - km_1g\cos\alpha = m_1a \quad (1)$$ $$m_2g - T_2 = m_2a \quad (2)$$ $$(T_2-T_1)R = I\frac{a}{R} \quad (3)$$

Điểm hay: vì ròng rọc là vành tròn, $I=MR^2$, nên ở (3): $(T_2-T_1)R = MR^2\cdot\dfrac{a}{R} \Rightarrow T_2-T_1 = Ma$ — hệ số $R$ **tự triệt tiêu gọn gàng** (khác đĩa đặc, nơi hệ số còn lại là $\frac12M$).

**b) Thời gian và vận tốc khi $m_2$ chạm đất:**

Chuyển động biến đổi đều từ nghỉ, quãng đường $h=5{,}0$m: $$h = \frac12at^2 \Rightarrow t=\sqrt{\frac{2h}{a}} \qquad v=at$$

**c) Động năng hệ ngay trước khi chạm đất:** $$K=\frac12m_1v^2+\frac12m_2v^2+\frac12I\omega^2, \quad \omega=\frac{v}{R}$$

**d) Sau khi $m_2$ chạm đất — dây chùng:**

$m_1$ đang đi lên với vận tốc $v$ (từ câu b, liên tục tại thời điểm chạm đất), nhưng **mất lực kéo $T_1$** (dây không còn căng vì $m_2$ đã dừng trên đất). Bây giờ $m_1$ chỉ chịu 2 lực dọc dốc, và **cả hai đều cản** vì $m_1$ đang đi lên: $$-m_1g\sin\alpha - km_1g\cos\alpha = m_1a' \Rightarrow a' = -g(\sin\alpha+k\cos\alpha)$$

Dùng $v_f^2=v^2+2a's$ với $v_f=0$ (dừng lại) để tìm $s$.

_(Khác với dạng "dây đứt" ở Đề 3 — ở đó chỉ có ma sát cản; ở đây **cả trọng lực lẫn ma sát đều cản** vì vật đang đi lên dốc, không phải trượt ngang.)_

Bạn thử tự tính các bước nhé — báo lại nếu muốn kiểm tra kết quả hoặc giải chi tiết.

## Đề 4 — Câu 3 (4 điểm)

**Tóm tắt:** $n=2{,}0$ kmol khí **đơn nguyên tử** ($i=3$), chu trình: (1→2) **nén đẳng nhiệt**, (2→3) **dãn nở đẳng áp**, (3→1) **đẳng tích**. $T_1=600$K, $P_1=10^5$ N/m², $\dfrac{V_{max}}{V_{min}}=4$, $R=8{,}31\times10^3$ J/(kmol.K).

## Bước đầu tiên: xác định $V_{max}$, $V_{min}$ là thể tích nào

- $(1\to2)$ nén → $V$ giảm: $V_2<V_1$
- $(2\to3)$ dãn nở → $V$ tăng: $V_3>V_2$
- $(3\to1)$ đẳng tích → $V_3=V_1$ (khép kín về đúng thể tích trạng thái 1)

→ Vậy $V_1=V_3$ (lớn hơn) là $V_{max}$, còn $V_2$ là $V_{min}$: $$\frac{V_1}{V_2}=4$$

## a) Vẽ chu trình (P-V)

Đường (1→2): đường hyperbol đi xuống-sang trái (nén đẳng nhiệt, $V$ giảm, $P$ tăng theo Boyle). Đường (2→3): đường ngang đi sang phải (đẳng áp, $P$ không đổi, $V$ tăng). Đường (3→1): đường thẳng đứng đi xuống (đẳng tích, $V$ không đổi, $P$ giảm về $P_1$).

## b) Tính $V_1, P_2, V_2, T_3$

**$V_1$:** dùng $PV=nRT$ ở trạng thái 1: $V_1 = \dfrac{nRT_1}{P_1}$

**$V_2$:** $V_2 = \dfrac{V_1}{4}$ (từ tỉ lệ đã xác định ở trên)

**$P_2$:** đẳng nhiệt (1→2) nên $P_1V_1=P_2V_2 \Rightarrow P_2 = P_1\dfrac{V_1}{V_2} = 4P_1$

**$T_3$:** đẳng áp (2→3) nên $\dfrac{V_2}{T_2}=\dfrac{V_3}{T_3}$, với $T_2=T_1=600$K (vì 1→2 đẳng nhiệt) và $V_3=V_1=4V_2$: $$T_3 = T_2\times\frac{V_3}{V_2} = 600\times4$$

## c) Nhiệt lượng từng quá trình

- **$(1\to2)$ đẳng nhiệt:** $\Delta U=0 \Rightarrow Q_{12}=A_{12}=nRT_1\ln\dfrac{V_2}{V_1}$ (âm, vì nén nên tỏa nhiệt)
- **$(2\to3)$ đẳng áp:** $Q_{23}=nC_P\Delta T = n\dfrac{i+2}{2}R(T_3-T_2)$ (dương, vì $T$ tăng → nhận nhiệt)
- **$(3\to1)$ đẳng tích:** $Q_{31}=nC_V\Delta T = n\dfrac{i}{2}R(T_1-T_3)$ (âm, vì $T$ giảm → tỏa nhiệt)

## d) Hiệu suất chu trình

Gom $Q_{nhận}$ (chỉ lấy $Q_{23}$, số dương duy nhất), rồi: $$\eta = \frac{A}{Q_{nhận}}, \quad A = A_{12}+A_{23}+A_{31}$$

với $A_{23}=P_2(V_3-V_2)$ (dãn nở, dương), $A_{31}=0$ (đẳng tích).

Bạn thử tự thay số tính từng bước nhé — báo lại nếu muốn kiểm tra kết quả hoặc giải chi tiết.



## Đề 5 — Câu 1 (2 điểm)

**Tóm tắt:** $m=20{,}0$ g $=0{,}020$ kg (viên đạn), $M=10{,}0$ kg (bao cát, treo dây dài $L=1{,}0$ m, ban đầu đứng yên), va chạm **mềm**, sau va chạm dây lệch góc $\theta=20°$.

## Đây là dạng gì?

Đúng "**con lắc đạn**" (bài tủ đã có trong note [Chương 3](https://claude.ai/epitaxy/10_Projects/13_Uni_Retake/L%C3%BD%201%20-%20Ch%C6%B0%C6%A1ng%203%20-%20C%C3%A1c%20%C4%91%E1%BB%8Bnh%20lu%E1%BA%ADt%20b%E1%BA%A3o%20to%C3%A0n.md), mục "Mẹo ôn thi") — 2 giai đoạn:

1. Va chạm mềm (tức thời) → bảo toàn **động lượng**
2. Sau va chạm, hệ (đạn+bao cát dính nhau) đung đưa lên độ cao $h$ → bảo toàn **cơ năng**

**Điểm đặc biệt của bài này:** đề cho **góc lệch** (không cho $v$ trực tiếp) → bạn phải làm **ngược lại thứ tự thông thường** — đi từ góc lệch → tìm $h$ → tìm vận tốc ngay sau va chạm → rồi mới suy ra vận tốc đạn ban đầu.

## Hướng dẫn từng bước

**Bước 1 — Từ góc lệch $\theta$, tìm độ cao $h$ mà hệ lên được:** $$h = L(1-\cos\theta)$$

(đây là công thức hình học quen thuộc của con lắc đơn: độ cao dây treo lệch một góc $\theta$ so với vị trí thấp nhất)

**Bước 2 — Bảo toàn cơ năng (giai đoạn 2), tìm vận tốc $v'$ ngay sau va chạm:** $$\frac12(m+M)v'^2 = (m+M)gh \Rightarrow v' = \sqrt{2gh}$$

(lưu ý: khối lượng dao động lúc này là $m+M$ vì đạn đã dính vào bao cát)

**Bước 3 — Bảo toàn động lượng (giai đoạn 1), tìm vận tốc đạn $v$ trước va chạm:** $$mv = (m+M)v' \Rightarrow v = \frac{(m+M)v'}{m}$$

**Câu b) Phần động năng mất do va chạm:** $$\Delta K = K_{trước} - K_{sau} = \frac12mv^2 - \frac12(m+M)v'^2$$

(hoặc dùng công thức rút gọn đã có trong note: $\dfrac{\Delta K}{K_{trước}}=\dfrac{M}{m+M}$ — vì $M\gg m$ nên gần như toàn bộ động năng đạn bị mất, hợp lý vật lý)

Bạn thử tự thay số tính từng bước nhé — báo lại nếu muốn kiểm tra kết quả hoặc giải chi tiết.

## Đề 6 — Câu 1 (2 điểm)

**Tóm tắt:** $m=2$ kg (quả cầu, treo dây $d=1$m), lệch góc $\theta=60°$ rồi thả, va chạm **hoàn toàn đàn hồi** với $M=5$ kg (đứng yên), $g=9{,}8$ m/s².

## Đây là dạng gì?

Kết hợp **3 công cụ** đã học: bảo toàn cơ năng (con lắc rơi) → va chạm đàn hồi 1D (công thức có sẵn ở note [Chương 3](https://claude.ai/epitaxy/10_Projects/13_Uni_Retake/L%C3%BD%201%20-%20Ch%C6%B0%C6%A1ng%203%20-%20C%C3%A1c%20%C4%91%E1%BB%8Bnh%20lu%E1%BA%ADt%20b%E1%BA%A3o%20to%C3%A0n.md)) → bảo toàn cơ năng lần nữa (M trượt lên cao sau va chạm).

## Hướng dẫn từng bước

**Bước 1 — Vận tốc $m$ ngay TRƯỚC va chạm (bảo toàn cơ năng con lắc):**

Độ cao rơi: $h = d(1-\cos\theta)$ (giống công thức hình học con lắc đã dùng ở Đề 5 Câu 1)

$$mgh = \frac12mv^2 \Rightarrow v = \sqrt{2gd(1-\cos\theta)}$$

**Bước 2 — Vận tốc $m$ và $M$ ngay SAU va chạm (va chạm đàn hồi 1D, $M$ đứng yên ban đầu):**

Dùng thẳng công thức rút gọn đã có trong note (trường hợp vật 2 đứng yên): $$v'_m = \left(\frac{m-M}{m+M}\right)v \qquad v'_M = \left(\frac{2m}{m+M}\right)v$$

_(Lưu ý dấu: vì $M>m$ ở đây, $v'_m$ sẽ **âm** — nghĩa là quả cầu $m$ bật ngược lại sau va chạm, không tiếp tục đi theo chiều cũ.)_

**Bước 3 (câu b) — đã có ở Bước 2:** $v'_M$ chính là đáp số câu b.

**Bước 4 (câu c) — Độ cao cực đại của $M$ sau va chạm (bảo toàn cơ năng, không ma sát):** $$\frac12Mv_M'^2 = Mgh_{max} \Rightarrow h_{max} = \frac{v_M'^2}{2g}$$

Bạn thử tự thay số tính từng bước nhé — báo lại nếu muốn kiểm tra kết quả hoặc giải chi tiết.

## Đề 6 — Câu 2 (4 điểm)

**Tóm tắt:** $m_1=15$ kg (trên mặt nghiêng $\theta=30°$, **KHÔNG ma sát**), $m_2=20$ kg treo (gồm 2 khối dính keo: $m_a=5$kg + $m_b=15$kg), ròng rọc đĩa đặc $R=0{,}25$m, $I=?$ (cần tìm), $a=3$ m/s² (**đã cho sẵn**, không cần tìm), $g=9{,}8$ m/s².

_(Từ câu d "khi m2 chuyển động **xuống**" → suy ra ngay: $m_2$ đi xuống, $m_1$ bị kéo lên dốc — đây là biến thể bài toán ngược giống Đề 2 Câu 1: biết $a$, tìm $T_1,T_2,I$.)_

## a) Phân tích lực và phương trình chuyển động

**$m_1$** (không ma sát, bị kéo lên dốc): chỉ có 2 lực dọc dốc — $T_1$ (kéo lên) và $m_1g\sin\theta$ (kéo xuống, cản): $$T_1 - m_1g\sin\theta = m_1a$$

**$m_2$** (treo, đi xuống): $m_2g$ (xuống) và $T_2$ (lên): $$m_2g - T_2 = m_2a$$

**Ròng rọc** (đĩa đặc, $I$ chưa biết): $\tau=I\beta$, với $\beta=a/R$: $$(T_2-T_1)R = I\frac{a}{R}$$

## b) Tính $T_1$, $T_2$

Vì $a$ đã cho sẵn, thay số trực tiếp: $$T_1 = m_1(a+g\sin\theta) \qquad T_2 = m_2(g-a)$$

## c) Tính $I$

$$I = \frac{(T_2-T_1)R^2}{a}$$

## d) Khi $m_b$ rơi ra khỏi $m_2$ sau 2 giây — đây là câu khó nhất, cần lý luận thêm

**Bước 1:** Tại $t=2$s, hệ đang có vận tốc $v=at=3\times2=6$ m/s (theo chiều cũ: $m_1$ lên, $m_2$ xuống) — vận tốc này **liên tục** ngay khi $m_b$ tách ra.

**Bước 2:** Sau khi $m_b$ rơi ra, khối lượng treo chỉ còn $m_a=5$kg — **phải kiểm tra lại xem chiều chuyển động cũ còn đúng không** (đây chính là bước "so sánh lực chủ động" đã học — vì giờ CẢ 2 bên đều có thể thắng: $m_1$ trên dốc không ma sát có $m_1g\sin\theta$ đầy đủ, còn $m_a$ chỉ còn $m_ag$ nhỏ hơn nhiều so với $m_2g$ ban đầu): $$m_1g\sin\theta \overset{?}{\gtrless} m_ag$$

Thay số: $m_1g\sin\theta = 15\times9{,}8\times0{,}5=73{,}5$N, còn $m_ag=5\times9{,}8=49$N → $m_1g\sin\theta > m_ag$ → **cán cân đã đảo ngược!**

**Bước 3 — Kết luận về chiều chuyển động:** Vì lực "chủ động mới" ($m_1g\sin\theta$) giờ thắng ($m_a g$), hệ **không thể tiếp tục đi theo chiều cũ mãi** — nhưng vì hệ đang có vận tốc $6$m/s theo chiều cũ (quán tính), nó sẽ:

1. Tiếp tục đi theo chiều cũ ($m_1$ lên, $m_a$ xuống) nhưng **giảm tốc dần** (vì lực tổng hợp giờ ngược chiều chuyển động),
2. Dừng lại tức thời,
3. Rồi **đảo chiều**: $m_1$ trượt xuống dốc, $m_a$ bị kéo lên.

Đây là dạng biến thể mới của việc "xác định chiều chuyển động" — áp dụng **sau khi khối lượng thay đổi giữa chừng**, không phải ngay từ đầu bài.

Bạn thử tự tính số các bước a,b,c nhé — phần d) chỉ cần mô tả định tính (không cần tính số) như trên là đủ ý đề hỏi.