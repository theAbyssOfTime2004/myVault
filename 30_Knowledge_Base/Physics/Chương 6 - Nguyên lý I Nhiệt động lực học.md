---
type: concept
created: 2026-05-31
updated: 2026-05-31
tags: [physics, vat-ly-dai-cuong, nhiet-dong-luc-hoc, nguyen-ly-1, lý 1]
aliases: [Nguyên lý I, First Law of Thermodynamics, Chương 6]
---

# Chương 6 — Nguyên lý I Nhiệt động lực học

> Dùng nội năng $U=\frac{i}{2}nRT$ của khí lý tưởng (xem [[Chương 5 - Khí lý tưởng]]) để áp dụng $\Delta U = Q + W$ cho 4 quá trình.

## 1. Phân biệt Nội năng vs Nhiệt lượng
- **Nội năng U:** năng lượng *bên trong* hệ (động năng tịnh tiến/quay/dao động + thế năng tương tác phân tử…). Là **biến trạng thái** (chỉ phụ thuộc trạng thái, như $P, V, T$).
- **Nhiệt lượng Q:** năng lượng *truyền qua biên* do chênh lệch nhiệt độ. **Không** là biến trạng thái (phụ thuộc đường đi).

## 2. Nội năng khí lý tưởng ⭐
$$U = \frac{i}{2}nRT \qquad \Delta U = \frac{i}{2}nR\,\Delta T$$

Bậc tự do $i$:

| Loại phân tử | $i$ |
|---|---|
| Đơn nguyên tử | 3 |
| 2 nguyên tử | 5 |
| ≥3 nguyên tử | 6 |

U của khí lý tưởng **chỉ phụ thuộc T**.

## 3. Nhiệt dung
- $Q = mc\,\Delta T = nC\,\Delta T$ ; $c$ = nhiệt dung riêng, $C$ = nhiệt dung mol.
- **Phép đo nhiệt lượng (calorimetry):** bảo toàn năng lượng $Q_{thu} = -Q_{tỏa}$.
- Quy ước: $\Delta T>0 \Rightarrow Q>0$ (hệ nhận); $\Delta T<0 \Rightarrow Q<0$ (hệ tỏa).
- $1\ \text{cal} = 4{,}186\ \text{J}$.

## 3b. Nhiệt chuyển pha (nhiệt hóa hơi / nhiệt nóng chảy) ⭐
> Không có trong slide gốc nhưng **xuất hiện trong đề thi thực tế** (VD: đun ấm nước tới khi một phần hóa hơi) — cần nhớ thêm.

Khi vật chuyển pha ở nhiệt độ **không đổi** (VD nước sôi hóa hơi ở 100°C), nhiệt lượng không làm tăng T mà dùng để phá liên kết phân tử:
$$Q = mL$$
- $L$: nhiệt hóa hơi riêng hoặc nhiệt nóng chảy riêng (J/kg). VD nước ở 100°C: $L_v = 2{,}3\times10^6$ J/kg.
- Khác với $Q=mc\Delta T$ (có $\Delta T$); nhiệt chuyển pha thì $\Delta T=0$ trong suốt quá trình.

**Dạng bài mẫu (đun ấm nước bằng bếp điện công suất không đổi):**
1. Tính nhiệt lượng đun ấm + nước từ $t_1$ lên 100°C: $Q_1 = (m_{nước}c_{nước} + m_{ấm}c_{ấm})\Delta T$
2. Tính nhiệt lượng hóa hơi một phần nước ở 100°C: $Q_2 = m_{hơi}L_v$
3. Tổng nhiệt cần: $Q = Q_1 + Q_2$
4. Nếu chỉ x% nhiệt bếp cấp được dùng để đun (phần còn lại thất thoát), và tổng thời gian là $t$: công suất bếp $P = \dfrac{Q}{x\%\cdot t}$

## 4. Công & giản đồ PV
$$W = -\int_{V_i}^{V_f} P\,dV \quad(\text{công môi trường thực hiện lên khí})$$

- **Quy ước của bài giảng:** $V\uparrow \Rightarrow W<0$ (hệ sinh công); $V\downarrow \Rightarrow W>0$ (hệ nhận công); $V=const\Rightarrow W=0$.
- Công = diện tích dưới đường cong PV; **chu trình kín** → công = diện tích hình kín, có thể ≠ 0.

## 5. Nguyên lý I ⭐⭐
$$\boxed{\Delta U = Q + W}$$

- Hệ cô lập: $Q=W=0 \Rightarrow \Delta U=0$, $U=const$.
- Chu trình kín: $\Delta U=0 \Rightarrow W=-Q$.

> [!warning] Lưu ý dấu
> Slide tóm tắt dùng dạng $\Delta U = A + Q$ với **A > 0: hệ nhận công** (cùng quy ước với W ở trên — W>0 khi *nén*). Nhiều SGK VN dùng $\Delta U = Q - A'$ với $A'$ là công hệ *sinh ra*. Bám theo quy ước slide: **W (hay A) > 0 khi nén / hệ nhận công.**

## 6. Áp dụng Nguyên lý I cho 4 quá trình (BẢNG PHẢI THUỘC) ⭐

| Quá trình | Điều kiện | W | Q | ΔU |
|---|---|---|---|---|
| Đẳng tích | $V=const$ | $0$ | $Q=\Delta U = nC_V\Delta T$ | $nC_V\Delta T$ |
| Đẳng áp | $P=const$ | $-P\Delta V$ | $nC_P\Delta T$ | $nC_V\Delta T$ |
| Đẳng nhiệt | $T=const$ | $-nRT\ln\frac{V_f}{V_i}$ | $-W$ | $0$ |
| Đoạn nhiệt | $Q=0$ | $\Delta U=nC_V\Delta T$ | $0$ | $nC_V\Delta T$ |

## 7. Nhiệt dung mol & hệ số Poisson
- $C_V = \dfrac{i}{2}R$ ; $C_P = C_V + R = \dfrac{i+2}{2}R$ (hệ thức **Mayer**).
- **Hệ số Poisson:** $\gamma = \dfrac{C_P}{C_V} = \dfrac{i+2}{i}$ (đơn nguyên tử 1,67 ; lưỡng nguyên tử 1,4).

## 8. Phương trình đoạn nhiệt *(cần biết chứng minh)*
$$PV^\gamma = const,\quad TV^{\gamma-1}=const,\quad T^\gamma P^{1-\gamma}=const$$

Cả 3 biến $P, V, T$ đều thay đổi.

## Các dạng bài tập
1. Chuyển hóa công ↔ nhiệt năng (VD 6.1: nâng tạ tiêu hao calo — đổi cal→J, $W=nmgh$).
2. Calorimetry — tìm $c$ hoặc nhiệt độ cân bằng ($Q_{thu}=-Q_{tỏa}$).
2b. Nhiệt chuyển pha kết hợp calorimetry — đun nước tới khi một phần hóa hơi, tìm công suất bếp (xem mục 3b).
3. Đẳng áp (VD 6.4: bóng He nóng ở P không đổi → tính Q).
4. Đẳng nhiệt (VD 6.5: tính W, Q khi giãn; rồi nén về bằng đẳng áp).
5. Đoạn nhiệt (VD 6.6: nén khí xilanh diesel, $\gamma=1{,}4$ → tìm P, T cuối qua $PV^\gamma$, $TV^{\gamma-1}$).
6. Chu trình kín nhiều giai đoạn trên giản đồ PV → công chu trình = diện tích, $\Delta U_{chu trình}=0$.
7. Chứng minh phương trình đoạn nhiệt (lý thuyết).

## ⚠️ Bẫy thường gặp
- Quên đổi $T$ sang **Kelvin**.
- Nhầm **dấu của công W** — luôn xác định hệ *nhận hay sinh* công trước.

---
**Liên quan:** [[Chương 5 - Khí lý tưởng]]
