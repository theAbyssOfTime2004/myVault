2026-07-14

Tags: [[lý 1]], [[review]], [[công thức]], [[ôn thi cuối kỳ]]

# Lý 1 — Chương 3: Các định luật bảo toàn trong cơ học

## Công của lực – Công suất

$$dA = \vec{F}\cdot d\vec{s} = F\,ds\cos\theta$$

- A > 0: lực sinh/nhận công dương; 
- A < 0: công cản (tiêu hao); 
- A = 0: lực vuông góc với chuyển động (VD: trọng lực & phản lực trên mặt phẳng ngang)
- Tổng công: $A = A_1 + A_2 + \dots + A_N$ (cộng đại số công của từng lực)

$$P = \frac{dA}{dt} = \vec{F}\cdot\vec{v} \qquad P_{tb} = \frac{A}{\Delta t}$$

- Đơn vị công suất: $1\,W = 1\,J/s = 1\,kg.m^2/s^3$

## Động năng – Định lý động năng

$$K = \frac{1}{2}mv^2$$

$$A_{12} = K_2 - K_1 = \frac{1}{2}mv_2^2 - \frac{1}{2}mv_1^2$$

> Công của tổng ngoại lực dọc theo quãng đường = độ biến thiên động năng trên quãng đường đó. Hữu ích khi đề cho vận tốc đầu/cuối và hỏi công (không cần tính từng lực).

## Thế năng – Định lý thế năng

$$U = mgy$$

$$A_g = -mg\Delta y = -(U_2 - U_1) = -\Delta U$$

- Dấu "−" nghĩa là: nâng vật lên ($\Delta y > 0$) thì trọng lực sinh công âm, thế năng tăng.

## Cơ năng – Bảo toàn cơ năng

$$E = K + U = \text{const} \quad\Leftrightarrow\quad K_i + U_i = K_f + U_f$$

- Chỉ đúng khi **hệ cô lập** (không có lực ma sát/lực cản sinh công, hoặc bỏ qua các lực đó).
- Dạng bài chuẩn: vật rơi/ném có vận tốc đầu bất kỳ — chọn gốc thế năng hợp lý rồi cân bằng $K_i+U_i=K_f+U_f$.

## Động lượng – Bảo toàn động lượng

$$\vec{p} = m\vec{v} \qquad \vec{F} = \frac{d\vec{p}}{dt}$$

- Động lượng hệ nhiều vật: $\vec{p} = \sum_i \vec{p}_i = \sum_i m_i\vec{v}_i$
- **Định luật bảo toàn động lượng:** nếu $\sum \vec{F}_{ext} = 0$ (hệ cô lập) thì $\vec{p} = \text{const}$ tại mọi thời điểm.
- Định lý xung lượng – động lượng: $\vec{F}\Delta t = \Delta\vec{p} = m\Delta\vec{v}$ (dùng cho bài va chạm/dừng đột ngột, VD: túi khí ô tô).

### Súng giật lùi (bảo toàn động lượng khi hệ ban đầu đứng yên)

$$0 = m\vec{v} + M\vec{V} \quad\Rightarrow\quad \vec{V} = -\frac{m\vec{v}}{M}$$

## Bài toán va chạm

**Nguyên tắc chung:** động lượng luôn bảo toàn trong va chạm (hệ cô lập); động năng chỉ bảo toàn trong va chạm **đàn hồi**.

### Va chạm mềm (không đàn hồi) — 2 vật dính vào nhau

$$\vec{v} = \frac{m_1\vec{v}_1 + m_2\vec{v}_2}{m_1+m_2}$$

- Năng lượng "mất" (chuyển thành nhiệt/biến dạng), giả sử $m_2$ đứng yên ban đầu:
$$Q = K - K' = \frac{1}{2}\frac{m_1m_2}{m_1+m_2}v_1^2 \qquad \frac{Q}{K} = \frac{m_2}{m_1+m_2}$$
  - $m_2 \gg m_1$: $Q/K \approx 1$ (gần như toàn bộ động năng biến thành dạng khác — VD búa đóng đinh vào tường)
  - $m_2 \ll m_1$: $Q/K \approx 0$ (gần như không mất năng lượng)

### Va chạm đàn hồi 1 chiều

$$\vec{v}'_1 = \left(\frac{m_1-m_2}{m_1+m_2}\right)\vec{v}_1 + \left(\frac{2m_2}{m_1+m_2}\right)\vec{v}_2$$
$$\vec{v}'_2 = \left(\frac{2m_1}{m_1+m_2}\right)\vec{v}_1 + \left(\frac{m_2-m_1}{m_1+m_2}\right)\vec{v}_2$$

**Trường hợp đặc biệt** (giả sử $m_2$ đứng yên, $v_2=0$):
- $m_1 \gg m_2$: $v'_1 \approx v_1$, $v'_2 \approx 2v_1$
- $m_1 = m_2$: $v'_1 = v_2 = 0$, $v'_2 = v_1$ → **2 vật trao đổi vận tốc cho nhau**

### Va chạm 2 chiều

Bảo toàn động lượng theo từng trục x, y riêng biệt:
$$m_1v_1 = m_1v'_1\cos\theta + m_2v'_2\cos\phi \qquad 0 = m_1v'_1\sin\theta - m_2v'_2\sin\phi$$

Nếu đàn hồi, thêm phương trình bảo toàn động năng: $\frac{1}{2}m_1v_1^2 = \frac{1}{2}m_1v_1'^2 + \frac{1}{2}m_2v_2'^2$. Va chạm không đàn hồi thì **không** dùng được bảo toàn động năng.

## Mẹo ôn thi

- Xác định trước: va chạm đàn hồi hay mềm? → quyết định có dùng bảo toàn động năng hay không (động lượng luôn bảo toàn).
- Bài "con lắc đạn" (đạn bắn vào khối gỗ treo dây rồi cùng bay lên độ cao h): 2 giai đoạn — (1) va chạm mềm bảo toàn động lượng tìm $v$ sau va chạm, (2) bảo toàn cơ năng từ lúc va chạm đến lúc lên độ cao h.
- Khi bài cho "vật đứng yên ban đầu" → luôn dùng công thức rút gọn (thế $v_2=0$).
- Công thức tổng công $A = \Delta K$ và định lý thế năng $A_g=-\Delta U$ là 2 công cụ độc lập — kết hợp chúng ra bảo toàn cơ năng.

# References
