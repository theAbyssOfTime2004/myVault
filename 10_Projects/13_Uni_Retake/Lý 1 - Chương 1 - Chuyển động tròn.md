2026-05-03

Tags: [[lý 1]], [[review]], [[công thức]]

# Lý 1 — Chương 1: Chuyển động tròn

## Gia tốc trong chuyển động tròn

Vật chuyển động cong có vận tốc thay đổi theo **2 cách**:
1. Thay đổi về **độ lớn** → đặc trưng bởi gia tốc tiếp tuyến $a_t$
2. Thay đổi về **hướng** → đặc trưng bởi gia tốc pháp tuyến $a_n$

### Gia tốc tiếp tuyến $\vec{a}_t$ — "nhanh hay chậm lại"

$$a_t = \frac{dv}{dt}$$

- **Phương:** dọc theo quỹ đạo (tiếp tuyến), cùng phương với $\vec{v}$
- **Chiều:** cùng chiều $\vec{v}$ → vật nhanh dần; ngược chiều $\vec{v}$ → vật chậm dần

### Gia tốc pháp tuyến $\vec{a}_n$ — "rẽ nhanh hay chậm"

$$a_n = \frac{v^2}{R}$$

- **Phương:** vuông góc quỹ đạo, hướng vào tâm cong
- Kể cả vật đi đều (v = const) mà đi cong thì vẫn có $a_n \neq 0$
- $v$ trong công thức là **vận tốc tức thời tại thời điểm đang xét** (không phải hằng số)

### Gia tốc toàn phần $\vec{a}$

$$\vec{a} = \vec{a}_t + \vec{a}_n$$

Vì $\vec{a}_t \perp \vec{a}_n$:

$$a = \sqrt{a_t^2 + a_n^2}$$

## Nhận dạng loại chuyển động

| Điều kiện | Loại chuyển động |
|---|---|
| $a_n = 0,\ a_t \neq 0$ | Thẳng biến đổi |
| $a_n = 0,\ a_t = \text{const}$ | Thẳng biến đổi đều |
| $a_n \neq 0,\ a_t = 0$ | Cong đều |
| $a_n = \text{const},\ a_t = 0$ | Tròn đều |
| $a = 0$ | Thẳng đều |

## Chuyển động tròn biến đổi đều

Công thức tương tự CĐ thẳng biến đổi đều, chỉ thay:
$x \to \theta$, $v \to \omega$, $a \to \beta$

| CĐ thẳng | CĐ tròn |
|---|---|
| $v = v_0 + at$ | $\omega = \omega_0 + \beta t$ |
| $x = x_0 + v_0 t + \tfrac{1}{2}at^2$ | $\theta = \theta_0 + \omega_0 t + \tfrac{1}{2}\beta t^2$ |
| $v^2 - v_0^2 = 2a\Delta x$ | $\omega^2 - \omega_0^2 = 2\beta\Delta\theta$ |

## Chuyển động tròn đều

$$T = \frac{2\pi}{\omega}, \quad f = \frac{1}{T}, \quad \omega = 2\pi f$$

- $a_t = 0$ (tốc độ không đổi)
- $a_n = \frac{v^2}{R} = \omega^2 R$ (luôn hướng vào tâm)

## Dạng bài: Tính $a_t$, $a_n$, $a$ từ $s(t)$

**Đề bài dạng:** Cho $s(t)$, bán kính $R$, tìm gia tốc tại $t = t_0$.

**Các bước:**

1. **Tìm $a_t$:** Lấy đạo hàm bậc 2 của $s(t)$ theo $t$
$$a_t = \frac{d^2s}{dt^2}$$

2. **Tìm $v(t)$:** Lấy đạo hàm bậc nhất của $s(t)$
$$v(t) = \frac{ds}{dt}$$

3. **Thay $t = t_0$** vào $v(t)$ để tính $v(t_0)$

4. **Tính $a_n$:**
$$a_n = \frac{v(t_0)^2}{R}$$

> **Lưu ý quan trọng:** Nếu $v$ âm thì lấy $|v|$ để tính $a_n$, vì $a_n = v^2/R$ dùng độ lớn vận tốc.

5. **Tính $a$ toàn phần:**
$$a = \sqrt{a_t^2 + a_n^2}$$

**Tại sao phải thay $t = t_0$ vào $v(t)$?**
Vì $v$ phụ thuộc $t$ → tại mỗi thời điểm $v$ khác nhau → $a_n$ cũng khác nhau. Đề hỏi tại $t = t_0$ nên mọi đại lượng phải lấy giá trị tại thời điểm đó.

# References
