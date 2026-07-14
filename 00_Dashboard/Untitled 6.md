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