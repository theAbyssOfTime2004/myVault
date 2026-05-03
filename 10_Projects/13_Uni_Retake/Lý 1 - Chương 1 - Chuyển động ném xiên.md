2026-05-01

Tags: [[lý 1]], [[review]], [[công thức]]

# Lý 1 — Chương 1: Chuyển động ném xiên

## Giả định
- Gốc tọa độ tại điểm ném
- Trục $Oy$ hướng lên, $Ox$ nằm ngang theo hướng ném
- Bỏ qua sức cản không khí
- $\theta$ là góc ném so với phương ngang, $v_0$ là vận tốc đầu

## Vận tốc đầu (phân tích theo trục)
$$v_{0x} = v_0 \cos\theta$$
$$v_{0y} = v_0 \sin\theta$$

## Gia tốc
$$a_x = 0$$
$$a_y = -g$$

## Vị trí ban đầu
$$x_0 = 0, \quad y_0 = 0$$

## Tọa độ tại thời điểm $t$
$$x(t) = v_0 \cos\theta \cdot t$$
$$y(t) = v_0 \sin\theta \cdot t - \tfrac{1}{2} g t^2$$

## Vận tốc tại thời điểm $t$
$$v_x = \frac{dx}{dt} = v_0 \cos\theta$$
$$v_y = \frac{dy}{dt} = v_0 \sin\theta - g t$$

## Một số đại lượng dẫn xuất hay dùng
- **Thời gian đạt độ cao cực đại** ($v_y = 0$):
$$t_{\max} = \frac{v_0 \sin\theta}{g}$$
- **Độ cao cực đại**:
$$H = \frac{v_0^2 \sin^2\theta}{2g}$$
- **Thời gian bay (về lại $y = 0$)**:
$$T = \frac{2 v_0 \sin\theta}{g}$$
- **Tầm xa** (max khi $\theta = 45°$):
$$L = \frac{v_0^2 \sin 2\theta}{g}$$
- **Phương trình quỹ đạo** (khử $t$, quỹ đạo là **parabol**):
$$y = x \tan\theta - \frac{g}{2 v_0^2 \cos^2\theta} x^2$$

## Ném ngang (trường hợp đặc biệt $\theta = 0$)

| | Trục x (ngang) | Trục y (đứng) |
|---|---|---|
| Vận tốc đầu | $v_{0x} = v_0$ | $v_{0y} = 0$ |
| Gia tốc | $a_x = 0$ | $a_y = -g$ |
| Vị trí | $x = v_0 t$ | $y = -\tfrac{1}{2} g t^2$ |
| Vận tốc | $v_x = v_0$ | $v_y = -g t$ |

- Trục x: chuyển động **đều**
- Trục y: **rơi tự do** (bắt đầu từ nghỉ)
- Vận tốc tổng hợp tại t: $v = \sqrt{v_0^2 + g^2 t^2}$

## Mẹo ôn thi

- **Vẽ hình ngay** khi đọc đề — nhất là bài ném xiên/ném ngang để chọn trục và dấu đúng
- **Tách 2 trục độc lập** — trục x và trục y không ảnh hưởng nhau
- Mẹo tìm quỹ đạo: từ $x(t)$ rút $t$ theo $x$, thế vào $y(t)$
- Lý thuyết hay bị hỏi: phân biệt **vận tốc trung bình** vs **tốc độ trung bình**, ý nghĩa $a_t$ và $a_n$, điều kiện các loại chuyển động đặc biệt

# References
