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


## Đề 6 — Câu 2: Lời giải đầy đủ

**Tóm tắt:** $m_1=15$ kg (nghiêng $\theta=30°$, không ma sát), $m_2=20$ kg (treo, $m_a=5$kg+$m_b=15$kg), ròng rọc đĩa đặc $R=0{,}25$m, $a=3$ m/s² (đã cho), $g=9{,}8$ m/s². **Chiều đã chứng minh:** $m_2$ xuống, $m_1$ lên dốc (vì $m_2g=196$N $\gg m_1g\sin\theta=73{,}5$N).

### a) Phương trình chuyển động

$$T_1 - m_1g\sin\theta = m_1a \quad (1)$$ $$m_2g - T_2 = m_2a \quad (2)$$ $$(T_2-T_1)R = I\frac{a}{R} \quad (3)$$

### b) Tính $T_1$, $T_2$

$$T_1 = m_1(a+g\sin\theta) = 15\times(3+4{,}9) = 15\times7{,}9 = \boxed{118{,}5\ \text{N}}$$ $$T_2 = m_2(g-a) = 20\times(9{,}8-3) = 20\times6{,}8 = \boxed{136{,}0\ \text{N}}$$

### c) Tính mô men quán tính ròng rọc

$$I = \frac{(T_2-T_1)R^2}{a} = \frac{(136{,}0-118{,}5)\times(0{,}25)^2}{3} = \frac{17{,}5\times0{,}0625}{3}$$ $$\boxed{I \approx 0{,}365\ \text{kg.m}^2}$$

### d) Khi $m_b$ rơi ra khỏi $m_2$ sau $t=2$s

**Vận tốc hệ tại thời điểm tách (liên tục):** $$v = at = 3\times2 = 6{,}0\ \text{m/s} \quad (\text{theo chiều cũ: } m_1\text{ lên, } m_2\text{ xuống})$$

**Kiểm tra lại cán cân lực chủ động mới** (chỉ còn $m_a=5$kg bên treo): $$m_1g\sin\theta = 73{,}5\ \text{N} \qquad m_ag = 5\times9{,}8=49{,}0\ \text{N}$$

Vì $m_1g\sin\theta > m_ag$ → **cán cân đảo ngược**: giờ $m_1$ có xu hướng thắng, kéo hệ theo chiều **ngược lại** (m_1 xuống dốc, $m_a$ lên).

**Tính gia tốc mới $a'$** (theo chiều mới, dùng lại $I$ vừa tìm ở câu c): $$a' = \frac{m_1g\sin\theta - m_ag}{m_1+m_a+\dfrac{I}{R^2}} = \frac{73{,}5-49{,}0}{15+5+\dfrac{0{,}365}{0{,}0625}} = \frac{24{,}5}{20+5{,}83}$$ $$\boxed{a' \approx 0{,}948\ \text{m/s}^2 \text{ (theo chiều mới: } m_1\text{ xuống, } m_a\text{ lên)}}$$

**Mô tả chuyển động của hệ:** Vì hệ đang có vận tốc $v=6{,}0$m/s theo **chiều cũ**, nhưng lực tổng hợp mới lại đẩy theo **chiều ngược lại** — nên hệ sẽ:

1. Tiếp tục đi theo chiều cũ ($m_1$ lên, $m_a$ xuống) nhưng **giảm tốc dần** với gia tốc $a'\approx0{,}948$m/s²,
2. Dừng lại tức thời sau khoảng $t' = v/a' \approx 6{,}33$s,
3. Sau đó **đảo chiều**: $m_1$ trượt xuống dốc, $m_a$ bị kéo lên — tăng tốc theo chiều mới với cùng gia tốc $a'\approx0{,}948$m/s².

## Đề 6 — Câu 3 (4 điểm)

**Tóm tắt:** $n=2$ mol khí lưỡng nguyên tử ($i=5$), $R=8{,}31$ J/(mol.K). Đọc từ hình: $A(V=10L, P=5atm)$, $B(V=50L, P=1atm)$ — quá trình $A\to B$ **đẳng nhiệt** (giãn nở, đề cho sẵn); $B\to C$: cùng $P=1atm$ → **đẳng áp**; $C\to A$: cùng $V=10L$ → **đẳng tích**.

## Nhận ra ngay: đây là CÙNG một chu trình đã giải ở Đề 2 Câu 2!

Số liệu $P,V$ giống hệt Đề 2 Câu 2 (chỉ đổi tên trạng thái 1→A, 2→B, 3→C) — nên **phương pháp và các bước tính hoàn toàn tương tự**, chỉ khác $n=2$ mol (không cần đổi kmol vì $R$ đã cho theo mol trực tiếp).

## Hướng dẫn

**a) Nhiệt lượng từng quá trình + nhận xét thu/tỏa:**

- $Q_{AB}$ (đẳng nhiệt, giãn nở): $Q_{AB}=nRT_A\ln\dfrac{V_B}{V_A} = P_AV_A\ln\dfrac{V_B}{V_A}$ → dương → **thu nhiệt**
- $Q_{BC}$ (đẳng áp, nén $V$ giảm): $Q_{BC}=n\dfrac{i+2}{2}R\Delta T = \dfrac{i+2}{2}P_B(V_C-V_B)$ → âm → **tỏa nhiệt**
- $Q_{CA}$ (đẳng tích, $P$ tăng): $Q_{CA}=n\dfrac{i}{2}R\Delta T = \dfrac{i}{2}V_A(P_A-P_C)$ → dương → **thu nhiệt**

$Q_{nhận}=Q_{AB}+Q_{CA}$ (cộng 2 số dương), $Q_{tỏa}=|Q_{BC}|$.

**b) Công thực hiện của khí trong 1 chu trình:** $$A = A_{AB}+A_{BC}+A_{CA}, \quad A_{AB}=P_AV_A\ln\frac{V_B}{V_A},\ A_{BC}=P_B(V_C-V_B),\ A_{CA}=0$$

**c) Hiệu suất:** $$\eta = \frac{A}{Q_{nhận}}$$

**d) Nếu $A\to B$ đổi thành đoạn nhiệt — đây là "Dạng 5" đã có trong note [Chương 7](https://claude.ai/epitaxy/10_Projects/13_Uni_Retake/Ch%C6%B0%C6%A1ng%207%20-%20Nguy%C3%AAn%20l%C3%BD%20II%20Nhi%E1%BB%87t%20%C4%91%E1%BB%99ng%20l%E1%BB%B1c%20h%E1%BB%8Dc.md):**

Khi đổi $A\to B$ thành đoạn nhiệt, $Q_{AB}=0$ (không còn thu nhiệt ở đoạn này nữa) → $Q_{nhận}$ chỉ còn lại $Q_{CA}$ (nếu vẫn dương). Cần tính lại toàn bộ 3 trạng thái theo hệ thức đoạn nhiệt (vì $B$ không còn xác định bởi đẳng nhiệt nữa, có thể $V_B$ hoặc $T_B$ sẽ thay đổi tùy đề ràng buộc gì được giữ nguyên — đọc kỹ đề xem giữ nguyên $V_B$ hay $P_B$) rồi tính lại $A$ và $\eta_{mới}$ để so sánh với $\eta$ ở câu c.

Bạn thử tự thay số các bước a,b,c nhé — báo lại nếu muốn giải chi tiết hoặc làm rõ câu d.


## Đề 7 — Câu 1 (4 điểm)

**Tóm tắt:** $m_1=2$ kg (mặt **ngang**), $m_2=10$ kg (mặt **nghiêng** $\theta=45°$), ròng rọc đĩa đặc $M=2$ kg, $k=0{,}1$ (cả 2 mặt), $g=10$ m/s².

## Xác định chiều chuyển động

Theo quy tắc đã chốt: $m_1$ trên mặt **ngang** → hoàn toàn thụ động (không có lực chủ động), chỉ $m_2$ trên nghiêng mới có $m_2g\sin\theta$ chủ động → **không cần so sánh**, chiều chắc chắn là $m_2$ trượt xuống, kéo $m_1$ về phía ròng rọc.

## a) Gia tốc và lực căng dây

$$T_1 - km_1g = m_1a \quad (1)$$ $$m_2g\sin\theta - T_2 - km_2g\cos\theta = m_2a \quad (2)$$ $$(T_2-T_1)R = I\frac{a}{R} \Rightarrow T_2-T_1=\frac{M}{2}a \quad (3,\ \text{vì đĩa đặc } I=\tfrac12MR^2,\ R\text{ tự triệt tiêu})$$

Kết hợp: $\ a = \dfrac{m_2g(\sin\theta-k\cos\theta)-km_1g}{m_1+m_2+\frac{M}{2}}$

## b) Động năng sau $t=3$s (từ nghỉ)

$v=at$, và nhờ $R$ triệt tiêu: $K=\dfrac12v^2\left(m_1+m_2+\dfrac{M}{2}\right)$ (giống mẹo đã dùng ở Đề 5 Câu 2).

## c) Giả sử 1 — đổi ròng rọc, $a_{mới}=1$ m/s², tìm $I_{mới}$

Đây là **bài toán ngược** (biết $a$, tìm $I$) — giống hệt Đề 2 Câu 1 và Đề 6 Câu 2:

1. Tính lại $T_1', T_2'$ từ (1),(2) với $a=1$m/s² (thay vào trực tiếp)
2. $I_{mới} = \dfrac{(T_2'-T_1')R_{mới}^2}{a_{mới}}$, với $R_{mới}=5$cm$=0{,}05$m

## d) Giả sử 2 — thay $m_1$ bằng bánh xe lăn không trượt (cùng khối lượng)

**Điểm mới:** bánh xe không còn "trượt có ma sát" như $m_1$ cũ — nó **lăn không trượt**, nên có thêm phương trình quay cho chính nó (giống dạng "lăn không trượt" đã học), rồi mới nối với ròng rọc và $m_2$ như cũ.

- Bánh xe (tịnh tiến): $T_1 - f_{ms,bánh} = m_1a$
- Bánh xe (quay quanh trục riêng, $I_{bánh}=\frac12m_1R_{bánh}^2$): $f_{ms,bánh}\cdot R_{bánh} = I_{bánh}\dfrac{a}{R_{bánh}} \Rightarrow f_{ms,bánh}=\dfrac12m_1a$

Thay vào phương trình tịnh tiến: $T_1 = m_1a+\dfrac12m_1a = \dfrac32m_1a$ — **bán kính bánh xe cũng tự triệt tiêu**, không cần biết giá trị.

Rồi kết hợp với ròng rọc (3) và $m_2$ (2) như cũ, chỉ thay $T_1=\dfrac32m_1a$ vào: $$a_{mới} = \frac{m_2g(\sin\theta-k\cos\theta)}{\dfrac32m_1+\dfrac{M}{2}+m_2}$$

_(Lưu ý: bánh xe lăn không trượt trên mặt ngang **không có ma sát trượt tiêu hao** như $m_1$ cũ — số hạng $km_1g$ đã biến mất khỏi tử số, vì ma sát nghỉ giữ cho lăn không trượt không sinh công, chỉ đóng vai trò tạo mô men quay.)_

Bạn thử tự tính số các phần nhé — báo lại nếu muốn kiểm tra kết quả hoặc giải chi tiết.


Đây là phương trình **quay** của bánh xe quanh trục của chính nó (khác với ròng rọc — đây là 1 vật rắn MỚI, có chuyển động quay riêng, cần viết phương trình $\tau=I\beta$ cho chính nó).

## Vì sao chỉ có lực ma sát $f_{ms}$ mới tạo ra mô men, không phải $T_1$

Bánh xe chịu 2 lực nằm ngang: $T_1$ (dây kéo, tác dụng **tại tâm trục bánh xe**) và $f_{ms}$ (ma sát nghỉ, tác dụng **tại điểm tiếp xúc với mặt đất**, cách tâm 1 đoạn $R_{bánh}$).

**Mô men lực = lực × cánh tay đòn (khoảng cách vuông góc từ trục quay đến đường tác dụng của lực).** Vì $T_1$ tác dụng **đúng tại tâm** (trục quay), cánh tay đòn của nó $=0$ → $T_1$ **không tạo ra mô men nào cả**, chỉ có $f_{ms}$ (tác dụng tại điểm tiếp xúc, cách tâm $R_{bánh}$) mới tạo mô men làm bánh xe quay.

## Thiết lập phương trình quay

$$\tau = I\beta \Rightarrow f_{ms}\times R_{bánh} = I_{bánh}\times\beta$$

Vì lăn không trượt: $v=\omega R_{bánh} \Rightarrow a=\beta R_{bánh} \Rightarrow \beta = \dfrac{a}{R_{bánh}}$ (điều kiện ràng buộc quen thuộc, giống các bài lăn không trượt đã học).

Thay vào: $$f_{ms}\times R_{bánh} = I_{bánh}\times\frac{a}{R_{bánh}}$$

## Thay $I_{bánh}=\frac12m_1R_{bánh}^2$ (bánh xe là trụ đặc đồng chất)

$$f_{ms}\times R_{bánh} = \frac12m_1R_{bánh}^2\times\frac{a}{R_{bánh}} = \frac12m_1R_{bánh}\times a$$

Chia cả 2 vế cho $R_{bánh}$ (triệt tiêu — đây là lý do bán kính bánh xe không cần biết giá trị): $$f_{ms} = \frac12m_1a$$

## Ý nghĩa vật lý (để hiểu tại sao lực ma sát lại "sinh ra" như vậy)

Nếu bánh xe **không có ma sát**, dây kéo $T_1$ tại tâm sẽ chỉ làm nó **trượt tịnh tiến thuần túy**, không hề quay — nhưng đề yêu cầu **lăn không trượt** (phải vừa tịnh tiến vừa quay đúng tỉ lệ $v=\omega R$). Ma sát nghỉ chính là lực "phụ" xuất hiện để **ép buộc** bánh xe quay đúng theo tỉ lệ đó — nó "mượn" một phần lực kéo để chuyển thành mô men quay, nên làm giảm bớt lực còn lại dùng cho tịnh tiến (đây là lý do sau đó $T_1=\frac32m_1a$ thay vì chỉ $m_1a$ — cần lực kéo lớn hơn để bù cho phần "hao" vào việc quay).


## Đề 7 — Câu 3: Lời giải đầy đủ (Chu trình Otto)

**Số liệu:** $k=V_1/V_2=8$, khí lưỡng nguyên tử $i=5$ → $\gamma=1{,}4$; $T_1=293$K, $T_3=1023$K, $P_1=10^5$ Pa, $V_1=0{,}5\times10^{-3}$ m³, $R=8{,}31\times10^3$ J/(kmol.K).

**Tính $n$:** $n=\dfrac{P_1V_1}{RT_1}=\dfrac{50}{8{,}31\times10^3\times293}\approx2{,}054\times10^{-5}$ kmol $\Rightarrow nR\approx0{,}1706$ J/K

### a) $P_2, T_2$ và $P_4, T_4$

**Đoạn nhiệt (1→2), nén:** $T_2 = T_1\times k^{\gamma-1} = 293\times8^{0{,}4} \approx 293\times2{,}297$ $$\boxed{T_2\approx673{,}1\ \text{K}} \qquad P_2 = P_1\times k^\gamma = 10^5\times8^{1{,}4} \approx \boxed{1{,}838\times10^6\ \text{Pa}}$$

**Đoạn nhiệt (3→4), giãn:** vì $V_4=V_1, V_3=V_2$ nên $T_4=T_3/k^{\gamma-1}=1023/2{,}297$ $$\boxed{T_4\approx445{,}3\ \text{K}} \qquad P_4 = \frac{nRT_4}{V_1}\approx\boxed{1{,}520\times10^5\ \text{Pa}}$$

### b) Công và nhiệt lượng từng quá trình

**$(1\to2)$ đoạn nhiệt:** $Q_{12}=0$ $$\Delta U_{12}=nR\frac{i}{2}(T_2-T_1)=0{,}1706\times2{,}5\times380{,}1\approx162{,}2\ \text{J} \Rightarrow A_{12}=-162{,}2\ \text{J (nhận công)}$$

**$(2\to3)$ đẳng tích:** $A_{23}=0$ $$Q_{23}=nR\frac{i}{2}(T_3-T_2)=0{,}1706\times2{,}5\times349{,}9\approx\boxed{149{,}3\ \text{J (thu nhiệt)}}$$

**$(3\to4)$ đoạn nhiệt:** $Q_{34}=0$ $$\Delta U_{34}=nR\frac{i}{2}(T_4-T_3)=0{,}1706\times2{,}5\times(-577{,}7)\approx-246{,}5\ \text{J} \Rightarrow A_{34}=+246{,}5\ \text{J (sinh công)}$$

**$(4\to1)$ đẳng tích:** $A_{41}=0$ $$Q_{41}=nR\frac{i}{2}(T_1-T_4)=0{,}1706\times2{,}5\times(-152{,}3)\approx\boxed{-65{,}0\ \text{J (tỏa nhiệt)}}$$

### c) Hiệu suất động cơ

$$A_{total}=A_{12}+A_{34}=-162{,}2+246{,}5\approx84{,}3\ \text{J} \qquad Q_{nhận}=Q_{23}\approx149{,}3\ \text{J}$$ $$\eta=\frac{A}{Q_{nhận}}=\frac{84{,}3}{149{,}3}\approx\boxed{56{,}5\%}$$

### d) Công thức hiệu suất Otto tổng quát theo $k,\gamma$

Từ hệ thức đoạn nhiệt: $T_2=T_1k^{\gamma-1}$, $T_3=T_4k^{\gamma-1}$, thay vào $\eta=1-\dfrac{|Q_{41}|}{Q_{23}}=1-\dfrac{T_4-T_1}{T_3-T_2}$:

$$\eta = 1-\frac{T_4-T_1}{k^{\gamma-1}(T_4-T_1)}$$ $$\boxed{\eta_{Otto} = 1-\frac{1}{k^{\gamma-1}}}$$

_(Kiểm tra: thay $k=8,\gamma=1{,}4$: $\eta=1-1/8^{0{,}4}=1-1/2{,}297\approx56{,}5\%$ ✓ khớp câu c)_


Không sao — bài này **không cần** $n$ hay $R$ luôn, vì có thể giải hoàn toàn bằng mẹo "$PV$ thay cho $nRT$" đã dùng nhiều lần trước đó (Đề 2 Câu 2, Đề 6 Câu 3, Đề 5 Câu 3...).

## Vì sao không cần $n$, $R$

Mọi công thức công/nhiệt cho 4 loại quá trình đều có thể viết **thuần túy bằng $P,V$**, không cần tách riêng $n$ hay $R$:

- Đẳng nhiệt: $A=P_1V_1\ln\dfrac{V_2}{V_1}$
- Đẳng áp: $A=P\Delta V$, $Q=\dfrac{i+2}{2}\Delta(PV)$
- Đẳng tích: $A=0$, $Q=\dfrac{i}{2}\Delta(PV)$
- Đoạn nhiệt: $\Delta U=\dfrac{i}{2}\Delta(PV)$ (vì $Q=0$)

→ Tất cả đều chỉ cần biết $P,V$ tại mỗi trạng thái — không cần biết $n$, $R$, hay thậm chí $T$ tuyệt đối.

## Vấn đề thực sự cần giải quyết: xác định đủ $P,V$ ở cả 4 trạng thái

Đề cho: $P_1=P_0=10^5$, $V_1=V_0=3\times10^{-3}$; $V_2=3V_0$; $P_3=P_0/5$. Bạn cần tìm nốt $P_2, V_3, P_4, V_4$ bằng cách dùng **đúng loại quá trình nối giữa 2 trạng thái liên tiếp**:

1. **$P_2$:** từ đẳng nhiệt (1→2), $P_1V_1=P_2V_2 \Rightarrow P_2=\dfrac{P_1V_1}{V_2}=\dfrac{P_0}{3}$
2. **$V_3$:** từ đoạn nhiệt (2→3), $P_2V_2^\gamma=P_3V_3^\gamma \Rightarrow V_3=V_2\left(\dfrac{P_2}{P_3}\right)^{1/\gamma}$ (với $\gamma=\frac{i+2}{i}=\frac75$)
3. **$P_4$:** từ đẳng áp (3→4), $P_4=P_3=\dfrac{P_0}{5}$
4. **$V_4$:** từ đẳng tích (4→1), $V_4=V_1=V_0$

Sau khi có đủ $(P,V)$ ở cả 4 trạng thái, áp dụng công thức tương ứng cho từng quá trình như bảng ở trên — hoàn toàn không cần đụng đến $n$ hay $R$ ở bất kỳ bước nào.

Bạn thử tự tính $P_2, V_3$ trước nhé — báo lại nếu muốn kiểm tra hoặc giải chi tiết cả bài.

## Đề 9 — Câu 1 (5 điểm)

**Tóm tắt:** $m_1$ (A) $=2$kg (treo), $m_2$ (B) $=5$kg (mặt nghiêng $\alpha=60°$, $k=0{,}1$), ròng rọc đĩa đặc $M=1$kg, $g=9{,}8$m/s².

## Xác định chiều chuyển động (lần này đọc kỹ hình trước khi giả định)

Từ hình: ròng rọc ở **đỉnh**, $m_1$ treo bên trái (có mũi tên "↑" trong hình gợi ý $m_1$ đi lên), $m_2$ trên mặt nghiêng bên phải — đây là cấu hình "tug-of-war" chuẩn (khác với Đề 8 vừa sửa). Kiểm chứng bằng so sánh: $$m_2g\sin\alpha = 5\times9{,}8\times\sin60°\approx42{,}4\ \text{N} \qquad m_1g=2\times9{,}8=19{,}6\ \text{N}$$

$m_2g\sin\alpha \gg m_1g$ → $m_2$ thắng → **$m_2$ trượt xuống dốc, kéo $m_1$ lên** — khớp với mũi tên trong hình.

## a) Gia tốc (dùng Newton)

$$T_1 - m_1g = m_1a \quad (1)$$ $$m_2g\sin\alpha - T_2 - km_2g\cos\alpha = m_2a \quad (2)$$ $$T_2-T_1 = \frac{M}{2}a \quad (3,\ \text{đĩa đặc, } R \text{ triệt tiêu})$$

$$a = \frac{m_2g(\sin\alpha-k\cos\alpha)-m_1g}{m_1+m_2+\frac{M}{2}}$$

## b) Lực căng dây

Thay $a$ vào (1), (2) để ra $T_1, T_2$.

## Đề 9 — Câu 1c: Trình bày chi tiết (dùng $W$)

**Định lý động năng (Chương 3):** tổng công của các ngoại lực tác dụng lên hệ bằng độ biến thiên động năng của hệ: $$W_{ngoại} = \Delta K = K_{sau} - K_{trước}$$

_(Ở đây $W$ = công mà hệ **nhận** được từ các lực bên ngoài — nếu dương, động năng hệ tăng; nếu âm, động năng hệ giảm. Đây chính là quy ước "$W$ = công nhận" đã thống nhất trước đó.)_

## Bước 1 — Xác định "hệ" đang xét

Lấy **cả 3 vật** làm một hệ thống chung: $m_1$ (treo) + $m_2$ (trên nghiêng) + ròng rọc (đang quay). Vì dây không giãn và ròng rọc lý tưởng (trục quay không ma sát), **lực căng dây $T_1, T_2$ là NỘI LỰC** của hệ này — không tính vào $W_{ngoại}$ (chúng chỉ truyền năng lượng qua lại giữa các phần trong hệ, không thêm/bớt năng lượng tổng).

## Bước 2 — Liệt kê các ngoại lực thực sự sinh công

Xét hệ di chuyển một quãng đường $s$ bất kỳ (kể từ nghỉ):

**Trọng lực $m_1$** (đi lên $s$, trọng lực hướng xuống → cản trở): $$W_1 = -m_1gs$$

**Trọng lực $m_2$** (đi xuống dốc $s$, thành phần dọc dốc $m_2g\sin\alpha$ cùng hướng chuyển động → hỗ trợ): $$W_2 = +m_2g\sin\alpha\cdot s$$

**Ma sát trên $m_2$** (luôn cản trở chuyển động thực tế): $$W_{ms} = -F_{ms}\cdot s = -km_2g\cos\alpha\cdot s$$

_(Phản lực pháp tuyến $N$ trên $m_2$ và trọng lực ròng rọc không sinh công, vì luôn vuông góc với chuyển động hoặc điểm đặt không di chuyển.)_

## Bước 3 — Tính $\Delta K$ của hệ

Từ nghỉ ($K_{trước}=0$), dùng $\omega=v/R$ và $I=\frac12MR^2$ (đĩa đặc, $R$ triệt tiêu): $$\Delta K = \frac12m_1v^2+\frac12m_2v^2+\frac12I\omega^2 = \frac12v^2\left(m_1+m_2+\frac{M}{2}\right)$$

## Bước 4 — Áp dụng định lý động năng

$$W_1+W_2+W_{ms} = \Delta K$$ $$s\left[m_2g\sin\alpha - m_1g - km_2g\cos\alpha\right] = \frac12v^2\left(m_1+m_2+\frac{M}{2}\right)$$

Dùng $v^2=2as$ (chuyển động biến đổi đều), thay vào và **chia cả 2 vế cho $s$** (triệt tiêu): $$m_2g\sin\alpha - m_1g - km_2g\cos\alpha = a\left(m_1+m_2+\frac{M}{2}\right)$$

$$\boxed{a = \frac{m_2g(\sin\alpha-k\cos\alpha) - m_1g}{m_1+m_2+\frac{M}{2}}}$$

## Kết luận

Kết quả **giống hệt** công thức đã tìm ở câu a (dùng $\tau=I\beta$ trực tiếp cho từng vật) — đây chính là ý nghĩa của câu c: **2 con đường khác nhau** (Newton từng vật riêng lẻ, vs. định lý động năng cho cả hệ) dẫn đến **cùng một kết quả**, xác nhận tính đúng đắn của bài toán.


Không — $W_1, W_2$ là **công của trọng lực**, không phải chính thế năng. Chúng có liên hệ chặt chẽ nhưng là 2 đại lượng khác nhau.

## Mối liên hệ đúng: công trọng lực = ÂM của biến thiên thế năng

Từ note [Chương 3](https://claude.ai/epitaxy/10_Projects/13_Uni_Retake/L%C3%BD%201%20-%20Ch%C6%B0%C6%A1ng%203%20-%20C%C3%A1c%20%C4%91%E1%BB%8Bnh%20lu%E1%BA%ADt%20b%E1%BA%A3o%20to%C3%A0n.md), công thức đã có: $$A_g = -mg\Delta y = -(U_{sau}-U_{trước}) = -\Delta U$$

Nghĩa là: **công của trọng lực = $-\Delta U$**, chứ không phải $U$.

## Kiểm chứng với $W_1$, $W_2$ trong bài này

**$W_1$** ($m_1$ đi **lên** $s$, độ cao tăng thêm $s$): $$\Delta U_1 = +m_1gs \ (\text{thế năng } m_1 \text{ TĂNG}) \quad\Rightarrow\quad W_1 = -\Delta U_1 = -m_1gs \ ✓$$

**$W_2$** ($m_2$ đi **xuống dốc** $s$, độ cao giảm $s\sin\alpha$): $$\Delta U_2 = -m_2g\sin\alpha\cdot s \ (\text{thế năng } m_2 \text{ GIẢM}) \quad\Rightarrow\quad W_2 = -\Delta U_2 = +m_2g\sin\alpha\cdot s \ ✓$$

Khớp đúng với công thức tôi đã dùng.

## Vì sao phân biệt điều này lại quan trọng

Nếu thay $W_1=-\Delta U_1$, $W_2=-\Delta U_2$ vào định lý động năng $W_{ngoại}=\Delta K$: $$-\Delta U_1 - \Delta U_2 + W_{ms} = \Delta K \quad\Rightarrow\quad \Delta K + \Delta U = W_{ms} \quad\Rightarrow\quad \Delta(K+U) = W_{ms}$$

Đây chính là dạng **"cơ năng không bảo toàn khi có ma sát"** — độ biến thiên cơ năng ($K+U$) bằng đúng công của ma sát (luôn âm, vì ma sát luôn lấy bớt năng lượng ra khỏi hệ). Nếu không có ma sát ($W_{ms}=0$), sẽ trở về đúng **bảo toàn cơ năng thuần túy** ($\Delta(K+U)=0$) — đây là lý do vì sao dùng công của trọng lực (không phải thế năng trực tiếp) mới là cách viết "gốc", còn "bảo toàn cơ năng" chỉ là **trường hợp đặc biệt** khi không có lực ma sát/lực cản nào khác.


## Đề 9 — Câu 2 (5 điểm)

**Tóm tắt:** $n=3$ mol khí lưỡng nguyên tử ($i=5$, $\gamma=1{,}4$), $R=8{,}31$ J/(mol.K) (giả định, đề không ghi rõ nhưng chuẩn SI).

**Đọc từ hình:** $A(P=5\times10^5$ Pa$)$, $B(P=1\times10^5$ Pa$)$ — $A\to B$ **đoạn nhiệt** giãn nở; $B\to C$ **đẳng áp** (nén, cùng $P=1\times10^5$), $V_C=30$L; $C\to A$ khép kín về $P_A=5\times10^5$.

**Lưu ý:** từ vị trí $A$ và $C$ trên đồ thị (cùng thẳng hàng theo trục $V$), có vẻ $C\to A$ là **đẳng tích** ($V_A=V_C=30$L) — bạn kiểm tra lại hình xem có đúng vậy không, vì đây là điểm mấu chốt quyết định cách giải. Tôi sẽ hướng dẫn theo giả định này.

## Hướng dẫn

**a) Tìm $V_B$ và nhiệt độ từng trạng thái:**

Với $V_A=V_C=0{,}03$ m³ (giả định đẳng tích C→A):

**$V_B$** (từ đoạn nhiệt A→B): $P_AV_A^\gamma=P_BV_B^\gamma \Rightarrow V_B=V_A\left(\dfrac{P_A}{P_B}\right)^{1/\gamma}=V_A\times5^{1/1{,}4}$

**$T_A$**: $T_A=\dfrac{P_AV_A}{nR}$

**$T_C$**: $T_C=\dfrac{P_CV_C}{nR}=\dfrac{P_CV_A}{nR}$ (vì $V_C=V_A$)

**$T_B$**: từ đẳng áp B→C, $\dfrac{V_B}{T_B}=\dfrac{V_C}{T_C} \Rightarrow T_B=T_C\times\dfrac{V_B}{V_C}$

**b) Công và nhiệt mỗi quá trình:**

- $(A\to B)$ đoạn nhiệt: $Q_{AB}=0$; $A_{AB}=\dfrac{P_AV_A-P_BV_B}{\gamma-1}$ (công thức đoạn nhiệt đã có trong bảng công thức)
- $(B\to C)$ đẳng áp: $A_{BC}=P_B(V_C-V_B)$; $Q_{BC}=\dfrac{i+2}{2}(P_CV_C-P_BV_B)$
- $(C\to A)$ đẳng tích: $A_{CA}=0$; $Q_{CA}=\dfrac{i}{2}(P_AV_A-P_CV_C)$

**c) Hiệu suất:** xác định $Q_{nhận}$ (số dương), rồi $\eta=\dfrac{A_{total}}{Q_{nhận}}$ (đây là động cơ nhiệt, vì đề chỉ hỏi hiệu suất chu trình, không nhắc máy lạnh).

Bạn xác nhận lại quá trình $C\to A$ có đúng là đẳng tích không, rồi thử tính từng bước — báo lại nếu muốn kiểm tra hoặc giải chi tiết.


## Đề 10 — Câu 1 (3 điểm)

**Tóm tắt:** $m_A=1$kg, $v_A=10$m/s tại A, đường A→C **không ma sát**, $h_1=6$m (độ cao A so với đáy B), $h_2=2$m (độ cao C so với đáy B), $g=9{,}8$m/s².

## a) Vận tốc tại B và C

Vì A→C không ma sát → **bảo toàn cơ năng**, chọn gốc thế năng tại đáy (điểm B):

$$\frac12v_A^2+gh_1 = \frac12v_B^2 \Rightarrow v_B=\sqrt{v_A^2+2gh_1}$$

$$\frac12v_A^2+gh_1 = \frac12v_C^2+gh_2 \Rightarrow v_C=\sqrt{v_A^2+2g(h_1-h_2)}$$

## b) Va chạm đàn hồi tại C

$m_A=1$kg (vận tốc $v_C$ vừa tính) va chạm đàn hồi với $m_C=0{,}2$kg (đứng yên) — dùng thẳng công thức đã học (Chương 3): $$v'_A = \left(\frac{m_A-m_C}{m_A+m_C}\right)v_C \qquad v'_C = \left(\frac{2m_A}{m_A+m_C}\right)v_C$$

Vì $m_A>m_C$ (1kg > 0,2kg), $v'_A$ sẽ **dương** (cùng chiều cũ) — $m_A$ tiếp tục đi tới, không bật ngược; $v'_C$ sẽ **lớn hơn** $v_C$ ban đầu (vật nhẹ bị bắn đi nhanh hơn, kiểu "đầu gậy đánh bóng golf").

## c) Đoạn CD = 15m có ma sát $k=0{,}7$

Sau va chạm, **cả 2 vật đều tiếp tục di chuyển về phía D** (vì cả $v'_A$ và $v'_C$ đều dương, cùng chiều). Với **mỗi vật riêng biệt**, kiểm tra bằng định lý động năng (công của ma sát = biến thiên động năng): $$-kmgs = 0 - \frac12mv'^2 \Rightarrow s_{max} = \frac{v'^2}{2kg}$$

- Nếu $s_{max} \ge 15$m → vật **đến được D**, tính $v_D$ bằng $v_D^2=v'^2-2kg\times15$
- Nếu $s_{max} < 15$m → vật **dừng lại** ở quãng đường $s=s_{max}$ (tính từ C), chưa tới D

Cần làm bước này **riêng cho cả $m_A$ và $m_C$** (vì có 2 vật với 2 vận tốc khác nhau sau va chạm).

Bạn thử tự tính từng bước nhé — báo lại nếu muốn kiểm tra kết quả hoặc giải chi tiết.