---
type: concept
created: 2026-07-14
updated: 2026-07-14
tags: [physics, vat-ly-dai-cuong, nhiet-dong-luc-hoc, nguyen-ly-2, lý 1]
aliases: [Nguyên lý II, Second Law of Thermodynamics, Chương 7, Entropy]
---

# Chương 7 — Nguyên lý II Nhiệt động lực học

> Nguyên lý I không phân biệt được công và nhiệt, không giải thích được vì sao một số quá trình tuân theo NL I nhưng không bao giờ xảy ra trong tự nhiên (VD: nhiệt tự đi từ vật lạnh sang vật nóng). Nguyên lý II lấp khoảng trống đó. Xem nền tảng ở [[Chương 6 - Nguyên lý I Nhiệt động lực học]].

## 1. Hạn chế của Nguyên lý I
- NL I chỉ cho biết ΔU, không phân biệt được đóng góp của Q và W.
- Theo NL I, công và nhiệt hoàn toàn tương đương (đổi qua lại được), nhưng **thực tế công có thể biến hoàn toàn thành nhiệt, còn nhiệt chỉ biến được một phần thành công**.
- NL I không giải thích được "chất lượng" nhiệt lượng — nhiệt lấy từ nguồn nhiệt độ cao chuyển hóa thành công nhiều hơn nhiệt lấy từ nguồn nhiệt độ thấp.

## 2. Quá trình thuận nghịch vs không thuận nghịch
- **Thuận nghịch:** hệ có thể quay lại trạng thái đầu theo đúng đường cũ trên giản đồ PV, mọi điểm trên đường đều là trạng thái cân bằng nhiệt. Chỉ là mô hình lý tưởng.
- **Không thuận nghịch:** mọi quá trình thực tế trong tự nhiên (có ma sát, lực cản...). Không có quá trình không thuận nghịch nào tự đảo chiều được.

## 3. Hai phát biểu của Nguyên lý II ⭐

| Phát biểu | Nội dung |
|---|---|
| **Clausius** | Nhiệt lượng không bao giờ tự đi từ vật lạnh hơn sang vật nóng hơn. |
| **Kelvin–Planck** | Không thể chế tạo động cơ nhiệt chuyển hóa hoàn toàn nhiệt lượng nhận từ nguồn nóng thành công trong một chu trình (không thể có động cơ vĩnh cửu loại 2). |

## 4. Động cơ nhiệt (Heat Engine)

Hoạt động theo chu trình kín ($\Delta U = 0$): nhận $Q_h$ từ nguồn nóng $T_h$, sinh công $W_{eng}$, thải $Q_c$ ra nguồn lạnh $T_c$.

$$W_{eng} = |Q_h| - |Q_c|$$

$$\eta = \frac{W_{eng}}{|Q_h|} = 1 - \frac{|Q_c|}{|Q_h|}$$

- $\eta = 1$ (100%) chỉ khi $Q_c=0$ — **không thể xảy ra** (đây chính là nội dung Kelvin–Planck).
- Động cơ xăng thực tế: η ≈ 20%; động cơ diesel: η ≈ 35–40%.

## 5. Máy làm lạnh – Bơm nhiệt (Refrigerator / Heat Pump)

Ngược chiều động cơ nhiệt: tốn công W để lấy $Q_c$ từ nguồn lạnh, thải $Q_h$ ra nguồn nóng.

$$|Q_h| = |W| + |Q_c|$$

**Hệ số hiệu quả (COP):**
$$\text{COP}_{\text{làm lạnh}} = \frac{|Q_c|}{W} = \frac{|Q_c|}{|Q_h|-|Q_c|} \qquad \text{COP}_{\text{sưởi}} = \frac{|Q_h|}{W} = \frac{|Q_h|}{|Q_h|-|Q_c|}$$

- Không thể có thiết bị chuyển nhiệt từ nơi lạnh sang nơi nóng mà **không tốn công** (đây là hệ quả trực tiếp của phát biểu Clausius).

## 6. Định lý Carnot & Chu trình Carnot ⭐⭐

**Định lý Carnot:** không động cơ nào hoạt động giữa 2 nguồn nhiệt $T_h, T_c$ có hiệu suất cao hơn động cơ Carnot (chu trình thuận nghịch) hoạt động giữa 2 nguồn đó.

**Chu trình Carnot** = 2 quá trình đẳng nhiệt + 2 quá trình đoạn nhiệt xen kẽ:
1. $A\to B$: giãn đẳng nhiệt ở $T_h$ — nhận $Q_h$
2. $B\to C$: giãn đoạn nhiệt — $T_h \to T_c$
3. $C\to D$: nén đẳng nhiệt ở $T_c$ — thải $Q_c$
4. $D\to A$: nén đoạn nhiệt — $T_c \to T_h$

**Hiệu suất Carnot (chỉ phụ thuộc nhiệt độ 2 nguồn):**
$$\eta_C = 1 - \frac{T_c}{T_h}$$

**Hệ số làm lạnh Carnot:**
$$\text{COP}_{lc} = \frac{T_c}{T_h - T_c}$$

> [!tip] Muốn tăng hiệu suất động cơ
> So sánh cùng một lượng $\Delta T$: **giảm $T_c$ hiệu quả hơn tăng $T_h$** (vì $T_c$ nằm ở tử số của $T_c/T_h$, ảnh hưởng phi tuyến mạnh hơn). Nhưng thực tế giảm $T_c$ khó thực hiện hơn nên người ta thường tăng $T_h$.

## 7. Entropy (S) & Nguyên lý tăng Entropy ⭐

$$\Delta S = \frac{Q}{T} \quad (T = \text{const, quá trình thuận nghịch})$$

- Đơn vị: J/K. S là **biến trạng thái** (như U, P, V, T).
- Q vào hệ → S tăng ($\Delta S>0$); Q ra khỏi hệ → S giảm ($\Delta S<0$).
- Nhiệt truyền từ vật nóng $T_h$ sang vật lạnh $T_c$ (không thuận nghịch):
$$\Delta S_{tot} = -\frac{Q}{T_h} + \frac{Q}{T_c} > 0 \quad (\text{vì } T_h > T_c)$$

**Nguyên lý tăng Entropy (dạng phát biểu khác của NL II):**
$$\Delta S_{vũ trụ} \ge 0$$
- Dấu "=" chỉ xảy ra với quá trình thuận nghịch (lý tưởng, không có thật).
- Entropy **không bảo toàn** (khác với năng lượng) — luôn có xu hướng tăng theo thời gian đối với hệ cô lập.

## 8. Hệ thức thống nhất Nguyên lý I & II

Kết hợp $\Delta U = Q+W$ với $\Delta S = Q/T$ (quá trình thuận nghịch, $W=-PdV$):
$$T\,dS = dU + P\,dV$$

## Các dạng bài tập thường gặp
1. Tính hiệu suất động cơ / công suất tỏa nhiệt từ $Q_h, Q_c$ (VD 7.1, 7.2).
2. Chu trình gồm nhiều quá trình (đẳng nhiệt + đoạn nhiệt xen kẽ) trên giản đồ PV: tính P, V, T tại từng điểm bằng $PV=const$ (đẳng nhiệt) và $PV^\gamma=const$, $TV^{\gamma-1}=const$ (đoạn nhiệt), sau đó tính W, Q từng chặng rồi tổng hợp η (VD 7.4, 7.5 — xem lại bảng công thức W, Q theo từng quá trình ở [[Chương 6 - Nguyên lý I Nhiệt động lực học]]).
3. Hiệu suất Carnot cực đại $\eta_C = 1-T_c/T_h$ — so sánh tăng $T_h$ vs giảm $T_c$.
4. Tính độ biến thiên entropy khi truyền nhiệt giữa 2 vật nhiệt độ khác nhau.
5. **So sánh hiệu suất khi thay đổi loại 1 quá trình trong chu trình** (rất hay gặp trong đề thi, VD: "nếu quá trình A→B là đoạn nhiệt thay vì đẳng nhiệt thì η bằng bao nhiêu? So sánh").

### Dạng 5 chi tiết — Đổi loại quá trình, tính lại hiệu suất

Đây **không phải bài tính lại thuần túy** — phải hiểu quan hệ P-V-T thay đổi ra sao:
1. Nếu 2 trạng thái đầu/cuối của quá trình bị đổi vẫn giữ nguyên (cùng $V_i, V_f$ hoặc cùng $P_i$) thì trạng thái ở đầu kia của quá trình **có thể thay đổi khác với đề gốc**, vì đẳng nhiệt ($PV=const$) và đoạn nhiệt ($PV^\gamma=const$) cho quan hệ P-V khác nhau — phải tính lại toàn bộ điểm nối tiếp theo, không chỉ riêng quá trình đó.
2. Tính lại W và Q của **đúng quá trình bị đổi loại**:
   - Đẳng nhiệt: $W=-nRT\ln(V_f/V_i)$, $Q=-W$
   - Đoạn nhiệt: $Q=0$, $W=\Delta U=nC_V\Delta T$
3. Cộng dồn lại tổng W, Q của cả chu trình (các quá trình còn lại giữ nguyên nếu trạng thái biên của chúng không đổi) → tính lại $\eta = W_{eng}/|Q_h|$.
4. So sánh về mặt định tính: chu trình có quá trình đoạn nhiệt thường cho đường cong dốc hơn đẳng nhiệt trên giản đồ PV → diện tích (công) khác đi, nên **η sau khi đổi luôn khác** η ban đầu — đề thường muốn thấy nhận xét này chứ không chỉ đưa ra số.

## ⚠️ Bẫy thường gặp
- Nhầm chiều bất đẳng thức entropy: $\Delta S_{vũ trụ} \ge 0$, không phải $\le 0$.
- $\eta_C$ và COP Carnot dùng nhiệt độ tuyệt đối (Kelvin), không dùng °C.
- Công thức chu trình nhiều giai đoạn: phải xác định đúng quá trình nào đẳng nhiệt/đoạn nhiệt trước khi áp W tương ứng — không áp nhầm công thức đẳng nhiệt cho đoạn nhiệt.

---
**Liên quan:** [[Chương 6 - Nguyên lý I Nhiệt động lực học]], [[Chương 5 - Khí lý tưởng]]
