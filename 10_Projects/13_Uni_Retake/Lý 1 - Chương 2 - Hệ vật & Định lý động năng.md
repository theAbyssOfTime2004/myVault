2026-05-06

Tags: [[lý 1]], [[review]], [[công thức]]

# Lý 1 — Chương 2: Hệ vật & Định lý động năng

## Hệ vật — Newton II

### Dạng bài chuẩn: mặt phẳng nghiêng + ròng rọc

**Cấu hình:** vật $m_1$ trên mặt phẳng nghiêng góc $\alpha$, nối dây qua ròng rọc với vật $m_2$ treo thẳng đứng. Hệ số ma sát $\mu$.

**Bước 1 — Xác định chiều chuyển động:**
- Tính lực kéo của $m_2$ xuống: $F_2 = m_2 g$
- Tính thành phần trọng lực của $m_1$ dọc dốc: $F_1 = m_1 g \sin\alpha$
- $m_1 < m_2$ **không có nghĩa** hệ đứng yên — phải so lực kéo thực tế

**Bước 2 — Viết Newton II cho từng vật** (chọn chiều dương = chiều chuyển động):

| Vật | Phương trình |
|---|---|
| $m_1$ (trên dốc) | $T - m_1 g \sin\alpha - \mu m_1 g \cos\alpha = m_1 a$ |
| $m_2$ (treo) | $m_2 g - T = m_2 a$ |

**Bước 3 — Cộng 2 phương trình** (khử $T$):
$$a = \frac{m_2 g - m_1 g \sin\alpha - \mu m_1 g \cos\alpha}{m_1 + m_2}$$

**Bước 4 — Tính lực căng dây** $T$: thay $a$ lại vào 1 trong 2 phương trình.

### Tình huống sau khi dây đứt

Khi dây đứt tại điểm A, vật $m_1$ chuyển động riêng với gia tốc mới:
$$a' = g(\sin\alpha - \mu\cos\alpha)$$

Vận tốc tại A là **liên tục** — lấy vận tốc ngay trước khi đứt làm $v_A$ cho giai đoạn sau.

---

## Động năng

$$W_đ = \frac{1}{2}mv^2$$

- **Đơn vị:** Joule (J) = kg·m²/s²
- Là đại lượng **vô hướng**, luôn $\geq 0$

### Định lý động năng

$$\Delta W_đ = W_{đ\text{(sau)}} - W_{đ\text{(trước)}} = A_{\text{tổng}}$$

Trong đó $A_{\text{tổng}}$ là tổng công của tất cả các ngoại lực tác dụng lên vật.

> **Ý nghĩa:** không cần tính từng lực riêng lẻ — chỉ cần biết vận tốc đầu và cuối là suy ra tổng công, hoặc ngược lại.

---

## Dạng bài: tính $\Delta W_đ$ của một vật trong hệ

**Đề bài dạng:** Cho hệ vật, $m_1$ bắt đầu từ nghỉ, tìm $\Delta W_{đ1}$ sau thời gian $t$.

**Các bước:**

1. Tìm gia tốc $a$ của hệ (Newton II, xem phần trên)
2. Tính vận tốc sau thời gian $t$:
$$v = v_0 + at = at \quad (\text{vì } v_0 = 0)$$
3. Tính $\Delta W_đ$:
$$\Delta W_{đ1} = \frac{1}{2}m_1 v^2 - 0 = \frac{1}{2}m_1 (at)^2$$

---

## Chuyển động cong theo tọa độ tham số

**Dạng bài:** Cho $\vec{r}(t)$ dạng tham số, tìm $|\vec{v}|$ và $|\vec{a}|$ tại $t = t_0$.

**Ví dụ:** $\vec{r} = (b\sin\omega t,\ ct)$ với $b, c, \omega$ cho trước.

**Bước 1 — Tính vận tốc** bằng đạo hàm $\vec{r}$:
$$\vec{v} = \frac{d\vec{r}}{dt} = (b\omega\cos\omega t,\ c)$$
$$|\vec{v}| = \sqrt{b^2\omega^2\cos^2\omega t + c^2}$$

**Bước 2 — Tính gia tốc** bằng đạo hàm $\vec{v}$:
$$\vec{a} = \frac{d\vec{v}}{dt} = (-b\omega^2\sin\omega t,\ 0)$$
$$|\vec{a}| = b\omega^2|\sin\omega t|$$

**Lưu ý về đơn vị $\omega$:**
- $\omega$ thường cho dạng $0{,}5\ \text{s}^{-1}$ — đây là **rad/s** (không phải nghịch đảo, là cùng một đơn vị)
- $0{,}5\ \text{s}^{-1} \neq \frac{1}{0{,}5} = 2$ — đừng nhầm

---

## Mẹo ôn thi

- Hệ vật: **vẽ riêng từng vật** và ghi lực lên từng vật, không gộp chung
- Nhớ chiều dương: chọn theo chiều chuyển động dự đoán, nếu $a < 0$ thì chiều dự đoán sai
- Khi dây đứt: vận tốc **không đổi đột ngột**, chỉ gia tốc thay đổi
- Định lý động năng: hữu ích khi đề hỏi "tính công" mà biết vận tốc đầu/cuối — không cần tính từng lực
- Tọa độ tham số: đạo hàm từng thành phần theo $t$, sau đó lấy module

# References
