2026-07-14

Tags: [[lý 1]], [[review]], [[công thức]], [[ôn thi cuối kỳ]]

# Lý 1 — Chương 4: Cơ học vật rắn

## Khối tâm (CM)

$$x_{CM} = \frac{\sum_i m_i x_i}{M} \qquad \vec{r}_{CM} = \frac{\sum_i m_i \vec{r}_i}{M} = \frac{1}{M}\int \vec{r}\,dm$$

- Vật đối xứng → khối tâm nằm trên trục/mặt đối xứng.
- Khối tâm **không nhất thiết nằm trong vật** (VD: boomerang, vòng khuyên).
- Thanh đồng nhất dài L: $x_{CM} = L/2$ (tính từ 1 đầu). Thanh mật độ $\lambda = \alpha x$ (tăng dần): $x_{CM} = \tfrac{2}{3}L$.
- Chuyển động khối tâm: $M\vec{a}_{CM} = \sum \vec{F}_{ext}$ — khối tâm chuyển động như 1 chất điểm khối lượng M chịu tổng ngoại lực. Nếu $F_{ext}=0$ thì $\vec{p}_{CM}=$ const (bảo toàn động lượng hệ, kể cả khi hệ nổ/vỡ thành nhiều mảnh).

## Mômen lực (τ) & Mômen động lượng (L)

$$\vec{\tau} = \vec{r}\times\vec{F} \qquad \tau = Fd \text{ (d: cánh tay đòn, } d\perp F)$$

$$\vec{L} = \vec{r}\times\vec{p} \qquad L = mvr\sin\phi$$

- Hướng của $\vec\tau$, $\vec L$: quy tắc bàn tay phải, vuông góc mặt phẳng $(\vec r,\vec F)$ hoặc $(\vec r,\vec p)$.
- Vật chuyển động tròn ($\vec r \perp \vec p$): $L = mvr = m\omega r^2$.
- Nhiều lực/mômen: cộng đại số theo chiều dương đã chọn (chú ý dấu ngược chiều kim đồng hồ / cùng chiều).

## Mômen quán tính (I)

$$I = \int r^2\,dm = \sum_i m_i r_i^2$$

**Bảng công thức cần nhớ** (trục qua khối tâm):

| Vật | I |
|---|---|
| Vòng tròn/trụ rỗng mỏng | $MR^2$ |
| Trụ đặc (đĩa đặc) | $\tfrac{1}{2}MR^2$ |
| Thanh mảnh, trục qua giữa | $\tfrac{1}{12}ML^2$ |
| Thanh mảnh, trục qua đầu | $\tfrac{1}{3}ML^2$ |
| Cầu đặc | $\tfrac{2}{5}MR^2$ |
| Cầu rỗng (vỏ cầu) | $\tfrac{2}{3}MR^2$ |
| Ròng rọc dạng mỏng (vòng) | $mr^2$ |
| Ròng rọc dạng đặc | $\tfrac{1}{2}mr^2$ |

### Định lý trục song song (Steiner–Huygens)

$$I = I_{CM} + MD^2$$

với D là khoảng cách từ trục mới đến trục qua khối tâm (song song).

## Định luật 2 Newton cho chuyển động quay

$$\tau = I\beta$$

Tương đương chuyển động quay ↔ tịnh tiến: $F\to\tau$, $m\to I$, $a\to\beta$, $v\to\omega$, $p=mv \to L=I\omega$.

### Dạng bài ròng rọc có khối lượng (KHÔNG bỏ qua I)

Các bước giải chuẩn:
1. Vật treo m: $mg - T = ma$ (Newton II tịnh tiến)
2. Ròng rọc: $\tau = RT = I\beta$
3. Ràng buộc dây không trượt: $a = R\beta$
4. Giải hệ 3 phương trình → $a = \dfrac{g}{1 + I/(mR^2)}$, $T = \dfrac{mg}{1+mR^2/I}$

**Atwood có ròng rọc khối lượng** (2 vật $m_1, m_2$ qua ròng rọc mômen quán tính I, bán kính R):
$$a = \frac{(m_1-m_2)g}{m_1+m_2+\dfrac{2I}{R^2}}$$
(nếu 2 ròng rọc giống nhau; nếu 1 ròng rọc thì mẫu số có $I/R^2$ thay vì $2I/R^2$ — luôn dựng lại từ 3 bước trên, đừng học thuộc máy móc.)

## Cơ năng vật rắn quay

$$K_R = \frac{1}{2}I\omega^2 \qquad \text{(động năng quay)}$$

- Vật rắn vừa tịnh tiến vừa quay (VD: lăn không trượt): $K = \tfrac{1}{2}Mv_{CM}^2 + \tfrac{1}{2}I_{CM}\omega^2$
- Định lý công – động năng quay: $A = \tfrac{1}{2}I\omega_f^2 - \tfrac{1}{2}I\omega_i^2$
- Bài ròng rọc + vật treo, hỏi vận tốc sau khi rơi đoạn h → dùng **bảo toàn cơ năng cho cả hệ** (gồm cả động năng quay ròng rọc $\tfrac12 I\omega^2$), không dùng Newton nếu đề không hỏi lực căng dây.

## Mômen động lượng & bảo toàn (mở rộng từ τ = dL/dt)

$$\sum\tau = \frac{dL}{dt} \quad\Rightarrow\quad \tau_{ext}=0 \Rightarrow L = \text{const}$$

- Tương tự bảo toàn động lượng tuyến tính nhưng cho chuyển động quay: nếu tổng mômen ngoại lực = 0 thì mômen động lượng của hệ không đổi.
- Ứng dụng kinh điển: vận động viên trượt băng xoay tròn, kéo tay vào (giảm I) → $\omega$ tăng để giữ $L=I\omega$ không đổi.

## Mẹo ôn thi

- Luôn phân biệt: bài **không có** khối lượng ròng rọc (dây lý tưởng, ròng rọc lý tưởng) → $T$ như nhau 2 bên, dùng Newton II thường (xem [[Lý 1 - Chương 2 - Hệ vật & Định lý động năng]]); bài **có I ròng rọc** → 2 bên dây có lực căng khác nhau, phải viết riêng phương trình cho từng đoạn dây + phương trình quay.
- Khi đề cho "ròng rọc dạng đặc/dạng mỏng" — đó là gợi ý để chọn $I=\tfrac12 mr^2$ hay $I=mr^2$.
- Bài hỏi "gia tốc, lực căng" → Newton II + τ=Iβ. Bài hỏi "vận tốc sau khi đi được đoạn/độ cao h" → ưu tiên bảo toàn năng lượng (nhanh hơn tích phân gia tốc).

# References
- [[Lý 1 - Chương 3 - Các định luật bảo toàn]]
