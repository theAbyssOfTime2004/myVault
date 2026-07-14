---
type: concept
created: 2026-05-31
updated: 2026-05-31
tags: [physics, vat-ly-dai-cuong, khi-ly-tuong, nhiet-dong-luc-hoc, lý 1]
aliases: [Khí lý tưởng, Ideal Gas, Chương 5]
---

# Chương 5 — Khí lý tưởng

> Mô hình khí lý tưởng nối **vĩ mô** ($PV=nRT$) với **vi mô** ($\frac12 m\overline{v^2}=\frac32 k_BT$). Là nền tảng cho [[Chương 6 - Nguyên lý I Nhiệt động lực học]].

## 1. Nhiệt độ & thang đo
- **Nguyên lý số 0:** hai vật cân bằng nhiệt thì có cùng nhiệt độ → cơ sở để định nghĩa và đo nhiệt độ.
- Đổi thang đo (phải thuộc):
	- $T(K) = t(°C) + 273{,}15$
	- $t(°F) = \frac{9}{5}t(°C) + 32$
- **0 K = không độ tuyệt đối**, không có nhiệt độ nào thấp hơn.

## 2. Sự nở vì nhiệt

| Loại | Công thức | Ghi nhớ |
|---|---|---|
| Nở dài | $\Delta L = \alpha L_0 \Delta T$ | $\alpha$ [K⁻¹] hệ số nở dài |
| Nở mặt | $\Delta A = 2\alpha A_0 \Delta T$ | hệ số "2" do nở 2 chiều |
| Nở khối | $\Delta V = \beta V_0 \Delta T$ | vật rắn đẳng hướng: $\beta = 3\alpha$ |

## 3. Áp suất
- $P = \dfrac{F_\perp}{A}$, đơn vị **Pa = N/m²**.
- $1\ \text{atm} = 1{,}013\times10^5\ \text{Pa} = 760\ \text{mmHg (torr)} = 1{,}013\ \text{bar}$.

## 4. Phương trình trạng thái khí lý tưởng ⭐
$$PV = nRT = \frac{M}{\mu}RT = N k_B T$$

- $R = 8{,}314\ \text{J/(mol·K)}$ ; $k_B = R/N_A = 1{,}38\times10^{-23}$ J/K ; $N_A = 6{,}022\times10^{23}$ mol⁻¹.
- $n = N/N_A = M/\mu$ (số mol).
- **Đẳng quá trình (2 trạng thái):** $\dfrac{P_1V_1}{T_1} = \dfrac{P_2V_2}{T_2}$

| Quá trình | Điều kiện | Định luật |
|---|---|---|
| Đẳng nhiệt | $T=const$ | Boyle: $PV=const$ |
| Đẳng áp | $P=const$ | Charles: $V/T=const$ |
| Đẳng tích | $V=const$ | Gay-Lussac: $P/T=const$ |

## 5. Thuyết động học phân tử — 5 giả thiết
1. Số phân tử lớn, khoảng cách trung bình ≫ kích thước phân tử.
2. Chuyển động theo định luật Newton, độc lập, ngẫu nhiên, mọi hướng.
3. Chỉ tương tác khi **va chạm đàn hồi** với nhau.
4. Va chạm đàn hồi với thành bình.
5. Các phân tử cùng một loại.

## 6. Cơ sở vi mô của áp suất & nhiệt độ ⭐
$$PV = \frac{2}{3}N\left(\tfrac{1}{2}m\overline{v^2}\right) \quad\Rightarrow\quad \boxed{\tfrac{1}{2}m\overline{v^2} = \tfrac{3}{2}k_BT}$$

- Nhiệt độ ↔ động năng tịnh tiến trung bình của phân tử.
- Mỗi bậc tự do tịnh tiến góp $\frac{1}{2}k_BT$ (3 chiều → hệ số 3).
- **Vận tốc quân phương:** $v_{rms} = \sqrt{\overline{v^2}} = \sqrt{\dfrac{3k_BT}{m}} = \sqrt{\dfrac{3RT}{\mu}}$

## 7. Phân bố & định luật khí quyển *(đọc thêm)*
- Phân bố **Maxwell–Boltzmann** theo năng lượng.
- Định luật khí quyển: $n(y) = n_0\, e^{-mgy/k_BT}$ — mật độ/áp suất giảm theo hàm mũ theo độ cao.

## 8. Định luật Dalton (áp suất riêng phần)
$$P_{hh} = P_A + P_B + P_C + \dots \quad(\text{cùng } V, T)$$

## Các dạng bài tập
1. Đổi đơn vị nhiệt độ / áp suất.
2. Nở vì nhiệt (khe đường ray, ống nước, lỗ tròn nở…).
3. Tính áp suất $P=F/A$ (VD 5.1: giày cao gót vs tennis).
4. Tìm $n, V, P, T$ từ $PV=nRT$ (VD 5.2).
5. Đẳng quá trình / 2 trạng thái $\frac{P_1V_1}{T_1}=\frac{P_2V_2}{T_2}$ (VD 5.3 bình khí lặn; bình xịt ném vào lửa — câu b có nở thể tích vỏ).
6. Động năng & $v_{rms}$ (VD 5.5: tổng $=\frac32 nRT$, một phân tử $=\frac32 k_BT$).
7. Mật độ khí theo độ cao (định luật khí quyển).
8. Hỗn hợp khí — Dalton.

## ⚠️ Bẫy thường gặp
- Luôn đổi $T$ sang **Kelvin** trước khi thay vào công thức.

---
**Liên quan:** [[Chương 6 - Nguyên lý I Nhiệt động lực học]]
