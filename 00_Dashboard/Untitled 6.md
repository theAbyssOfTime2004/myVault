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

## Đây là dạng gì?

Đúng "Dạng bài tủ: Lăn không trượt" đã có trong note [Lý 1 - Chương 4](https://claude.ai/epitaxy/10_Projects/13_Uni_Retake/L%C3%BD%201%20-%20Ch%C6%B0%C6%A1ng%204%20-%20C%C6%A1%20h%E1%BB%8Dc%20v%E1%BA%ADt%20r%E1%BA%AFn.md) — đề **không cho hệ số ma sát**, chỉ nói "lăn không trượt" → dùng **công cụ 1: bảo toàn cơ năng** (ma sát nghỉ trong lăn không trượt không sinh công, nên cơ năng vẫn bảo toàn dù có "ma sát").

## Hướng dẫn

**Bước 1 — Tìm độ cao rơi tương ứng:** $$h = L\sin\theta$$

**Bước 2 — Bảo toàn cơ năng** (từ đỉnh, $v_0=0$, đến chân dốc): $$mgh = \frac12mv^2 + \frac12I\omega^2$$

Vì lăn không trượt: $\omega = v/R$. Thay $I=\dfrac25mR^2$: $$mgh = \frac12mv^2 + \frac12\left(\frac25mR^2\right)\left(\frac{v}{R}\right)^2 = \frac12mv^2\left(1+\frac25\right) = \frac12mv^2\cdot\frac75$$

**Bước 3 — Rút ra $v$:** $$v^2 = \frac{2gh}{1+\frac25} = \frac{10}{7}gh \quad\Rightarrow\quad v = \sqrt{\frac{10gh}{7}}$$

Chú ý: khối lượng $m$ và bán kính $R$ **tự triệt tiêu** hoàn toàn khỏi công thức cuối — kết quả chỉ phụ thuộc $g$, $h$ (và hệ số $2/5$ đặc trưng cho quả cầu đặc). Đây là điểm mấu chốt của dạng "lăn không trượt": vận tốc cuối không phụ thuộc khối lượng hay kích thước vật, chỉ phụ thuộc **hình dạng** (qua tỉ số $I/(mR^2)$).

Bạn thử thay số tính $v$ nhé — báo lại nếu muốn kiểm tra kết quả hoặc giải chi tiết.