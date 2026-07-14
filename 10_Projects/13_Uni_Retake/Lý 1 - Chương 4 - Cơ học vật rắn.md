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

## Dạng bài tủ: Dây đứt giữa chừng

**Đề mẫu:** hệ vật + ròng rọc chuyển động từ nghỉ trong t giây, sau đó dây đứt → hỏi chuyển động tiếp theo của 1 vật (quãng đường đi được đến khi dừng, vận tốc chạm đất...).

**Các bước:**
1. Dùng gia tốc $a$ đã tính ở pha 1 (khi còn hệ 2 vật + ròng rọc) để tìm vận tốc tại đúng thời điểm đứt dây: $v = at$ (vì bắt đầu từ nghỉ).
2. **Vận tốc liên tục qua thời điểm đứt dây** — dùng $v$ này làm vận tốc đầu cho pha 2. Chỉ gia tốc thay đổi đột ngột (không còn lực căng dây/đối trọng).
3. Viết lại phương trình Newton **chỉ cho vật đang xét** ở pha 2 (không còn T, không còn ràng buộc với ròng rọc) — chú ý vật có thể đổi từ "đi lên chậm dần" hoặc "trượt có ma sát đến khi dừng" tùy hướng chuyển động lúc đứt dây.
4. Nếu hỏi quãng đường đến khi dừng: dùng $v^2 = v_0^2 + 2a's$ với $a'$ là gia tốc mới (thường ngược dấu vận tốc, do chỉ còn ma sát/trọng lực cản).

## Dạng bài tủ: Lăn không trượt (vật rắn vừa tịnh tiến vừa quay)

**Điều kiện không trượt:** $v = \omega R$ (vận tốc khối tâm liên hệ trực tiếp với vận tốc góc).

**Công cụ 1 — Bảo toàn cơ năng** (khi ma sát là ma sát nghỉ, không sinh công, dùng khi đề hỏi *vận tốc* ở cuối dốc):
$$mgh = \frac{1}{2}mv^2 + \frac{1}{2}I\omega^2 = \frac{1}{2}mv^2\left(1+\frac{I}{mR^2}\right) \quad\Rightarrow\quad v = \sqrt{\dfrac{2gh}{1+I/(mR^2)}}$$

| Vật | $I/(mR^2)$ | $v$ ở cuối dốc cao h |
|---|---|---|
| Trụ đặc | $1/2$ | $\sqrt{4gh/3}$ |
| Trụ rỗng (vành mỏng) | $1$ | $\sqrt{gh}$ |
| Cầu đặc | $2/5$ | $\sqrt{10gh/7}$ |
| Cầu rỗng | $2/3$ | $\sqrt{6gh/5}$ |

> **So sánh tốc độ lăn:** $I/(mR^2)$ càng nhỏ → càng ít năng lượng "trích" sang động năng quay → tới đích **nhanh hơn**. Thứ tự nhanh dần: trụ rỗng < cầu rỗng < trụ đặc < cầu đặc.

**Công cụ 2 — Newton tịnh tiến + quay** (bắt buộc dùng khi đề hỏi **độ lớn lực ma sát**, vì bảo toàn năng lượng không cho ra lực):
$$mg\sin\alpha - f = ma \qquad fR = I\beta \qquad a = R\beta$$
Giải hệ 3 phương trình ra $a$ và $f$.

## Mẹo ôn thi

- Luôn phân biệt: bài **không có** khối lượng ròng rọc (dây lý tưởng, ròng rọc lý tưởng) → $T$ như nhau 2 bên, dùng Newton II thường (xem [[Lý 1 - Chương 2 - Hệ vật & Định lý động năng]]); bài **có I ròng rọc** → 2 bên dây có lực căng khác nhau, phải viết riêng phương trình cho từng đoạn dây + phương trình quay.
- Khi đề cho "ròng rọc dạng đặc/dạng mỏng" — đó là gợi ý để chọn $I=\tfrac12 mr^2$ hay $I=mr^2$.
- Bài hỏi "gia tốc, lực căng" → Newton II + τ=Iβ. Bài hỏi "vận tốc sau khi đi được đoạn/độ cao h" → ưu tiên bảo toàn năng lượng (nhanh hơn tích phân gia tốc).
- Ròng rọc "kép" (2 bán kính R và r trên cùng trục, dây quấn khác bán kính mỗi bên) — mômen lực mỗi bên tính riêng theo bán kính tương ứng: $\tau = R T_1 - r T_2$, rồi mới áp $\tau = I\beta$.

---

## 1. Ròng rọc đơn, 2 lực căng khác nhau (bài vừa làm)

$$(T_2-T_1)R = I\beta, \quad a=R\beta \quad\Rightarrow\quad T_2-T_1=\frac{I}{R^2}a$$

Đặc điểm: chỉ 1 bán kính $R$ cho cả 2 đoạn dây, nên tốc độ 2 vật bằng nhau.

## 2. Ròng rọc "kép" — 2 bán kính khác nhau ($R$ và $r$) trên cùng 1 trục (Đề 2, 14, 19)

$$T_1R - T_2r = I\beta$$

**Điểm khác biệt quan trọng:** ràng buộc vận tốc/gia tốc **không còn giống nhau cho 2 vật** vì chúng nằm ở 2 bán kính khác nhau: $$a_1 = R\beta \qquad a_2 = r\beta \quad\Rightarrow\quad a_1 \neq a_2$$

Đây là bẫy hay gặp nhất — nhiều bạn quen dùng $a_1=a_2$ từ bài đơn giản rồi áp nhầm sang bài này.

## 3. Hai ròng rọc riêng biệt nối tiếp nhau (Đề 6 câu 1, Đề 19 câu 2)

Dây đi qua 2 ròng rọc khác nhau → có **3 đoạn dây với 3 lực căng khác nhau** ($T_1, T_2, T_3$), mỗi ròng rọc viết 1 phương trình $I\beta$ riêng: $$(T_1-T_2)R_1 = I_1\beta_1 \qquad (T_2-T_3)R_2 = I_2\beta_2$$

Nếu 2 ròng rọc có cùng bán kính và dây không trượt thì $\beta_1=\beta_2$, cộng 2 phương trình lại để khử $T_2$ (đây là mẹo hay dùng, xem lại ví dụ "Động cơ Atwood" ở note Chương 4).

## 4. Vật lăn không trượt (Đề 4, 13, 41) — KHÔNG phải bài ròng rọc

Ở đây chỉ có **1 lực duy nhất tạo mômen** là lực ma sát nghỉ $f$ (không phải lực căng dây), vì trọng lực và phản lực đi qua tâm khối nên không có cánh tay đòn:

$$fR = I\beta, \quad a=R\beta$$

Kết hợp với Newton tịnh tiến $mg\sin\alpha - f = ma$ → giải ra $a$ và $f$ (xem "Dạng bài tủ: Lăn không trượt" ở note Chương 4).

## 5. Vật vừa rơi vừa tự quay (kiểu con quay yo-yo, Đề 31 câu 2 — "trụ rỗng cuộn dây")

Vật rơi tự do trong khi dây cuộn quanh nó tự nhả ra, chỉ có **1 lực căng** (không phải 2 vật kéo nhau qua ròng rọc): $$mg - T = ma \quad \text{(tịnh tiến)} \qquad TR = I\beta \quad \text{(quay quanh trục của chính vật đó)}$$

## Cách nhận diện nhanh khi đọc đề

|Dấu hiệu trong đề|Dạng|Số lực căng|
|---|---|---|
|"ròng rọc" nối 2 vật, 1 bán kính|Dạng 1|2 ($T_1, T_2$)|
|"bán kính lớn $r_1$, bán kính nhỏ $r_2$" cùng 1 ròng rọc|Dạng 2|2, nhưng $a_1\neq a_2$|
|2 ròng rọc riêng, dây vắt qua cả 2|Dạng 3|3 ($T_1,T_2,T_3$)|
|"lăn không trượt", "quả cầu/trụ lăn xuống dốc"|Dạng 4|0 (chỉ có $f$)|
|"cuộn dây quanh trụ", 1 đầu dây cố định|Dạng 5|1 ($T$)|
# References
- [[Lý 1 - Chương 3 - Các định luật bảo toàn]]
