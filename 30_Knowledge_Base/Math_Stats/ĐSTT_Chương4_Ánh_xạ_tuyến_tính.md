---
tags: [linear-algebra, university, anh-xa-tuyen-tinh]
aliases: [ĐSTT Ch4, Ánh xạ tuyến tính]
---

# Đại số tuyến tính – Chương 4: Ánh xạ tuyến tính

> Nguồn: Chuong 4_Anh xa tuyen tinh.pdf (ĐH KHTN TP.HCM). Liên quan: [[ĐSTT_Chương3_Bài_Tập]], [[Linear Algebra Review]].

---

## 1. Tóm tắt lý thuyết

### 4.1. Định nghĩa

**Ánh xạ** $f: X \to Y$: mỗi $x \in X$ liên kết **duy nhất** một $y = f(x) \in Y$. ($X$ = tập nguồn, $Y$ = tập đích.)

**Ánh xạ tuyến tính** $f: V \to W$ ($V, W$ là KGVT trên $\mathbb{R}$) thỏa:

$$\text{i) } f(u+v) = f(u)+f(v); \qquad \text{ii) } f(\alpha u) = \alpha f(u).$$

Gộp một điều kiện: $f(\alpha u + v) = \alpha f(u) + f(v),\ \forall \alpha \in \mathbb{R},\ \forall u,v \in V$.

- $L(V,W)$ = tập ánh xạ tuyến tính từ $V$ vào $W$.
- $f \in L(V,V) = L(V)$ gọi là **toán tử tuyến tính**.

**Tính chất** (suy từ định nghĩa):

1. $f(0) = 0$ — *mẹo loại nhanh: nếu $f(0)\neq 0$ thì không tuyến tính.*
2. $f(-u) = -f(u)$.
3. Bảo toàn THTT: $f\!\left(\sum \alpha_i u_i\right) = \sum \alpha_i f(u_i)$.

**Định lý xác định qua cơ sở:** nếu $B=\{u_1,\dots,u_n\}$ là cơ sở của $V$ và cho trước bộ ảnh $\{v_1,\dots,v_n\}$ trong $W$, thì **tồn tại duy nhất** $f$ tuyến tính với $f(u_i)=v_i$.

**Tiêu chuẩn ma trận** ($f:\mathbb{R}^n\to\mathbb{R}^m$): $f$ tuyến tính $\iff \exists A$ sao cho $f(u)=uA$. → Cách nhanh để chứng minh tuyến tính: chỉ ra mỗi tọa độ output là tổ hợp bậc nhất **thuần nhất** của input (không có hằng số tự do).

### 4.2. Nhân và ảnh

| Khái niệm | Định nghĩa | Là KGC của | Cách tìm cơ sở |
|---|---|---|---|
| Nhân $\mathrm{Ker}\,f$ | $\{u\in V \mid f(u)=0\}$ | $V$ (nguồn) | Giải hệ thuần nhất $f(u)=0$ → nghiệm cơ bản |
| Ảnh $\mathrm{Im}\,f$ | $\{f(u)\mid u\in V\}$ | $W$ (đích) | Ảnh cơ sở chính tắc $\{f(e_i)\}$ → khử Gauss |

**Định lý số chiều (Rank–Nullity):**

$$\boxed{\dim\mathrm{Im}\,f + \dim\mathrm{Ker}\,f = \dim V}$$

(Dùng $\dim V$ = chiều **tập nguồn**.)

### 4.3. Ma trận biểu diễn

Với $B=(u_1,\dots,u_n)$ cơ sở $V$, $C=(v_1,\dots,v_m)$ cơ sở $W$:

$$[f]_{B,C} = \big([f(u_1)]_C\ \ [f(u_2)]_C\ \dots\ [f(u_n)]_C\big) \quad(\text{mỗi cột} = \text{tọa độ ảnh theo } C).$$

Toán tử ($V=W$, $B=C$): viết gọn $[f]_B$.

**Phương pháp tìm $[f]_{B,C}$:** lập $M=(v_1^\top\dots v_m^\top \mid f(u_1)^\top\dots f(u_n)^\top)$, Gauss–Jordan đưa về $(I_m \mid P)$, khi đó $[f]_{B,C}=P$.

**Hai công thức then chốt:**

$$[f(u)]_C = [f]_{B,C}\,[u]_B$$
$$[f]_{B',C'} = (C\to C')^{-1}\,[f]_{B,C}\,(B\to B') \qquad\Big([f]_{B'} = (B\to B')^{-1}[f]_B(B\to B') \text{ cho toán tử}\Big)$$

trong đó $(B_0\to B) = (u_1^\top\ u_2^\top\ \dots)$ là ma trận xếp các vectơ cơ sở $B$ thành **cột**.

---

## 2. Lời giải các ví dụ "(tự làm)"

### VD1 (4.1) — Chứng minh tuyến tính bằng ma trận

$f:\mathbb{R}^3\to\mathbb{R}^3,\ f(x,y,z)=(x+y+z,\ x-2y,\ y-3z)$.

Mỗi tọa độ output thuần nhất bậc nhất ⇒ $f(u)=uA$ với

$$A=\begin{pmatrix}1&1&0\\1&-2&1\\0&0&-3\end{pmatrix} \quad\Rightarrow\quad \boxed{f \text{ là ánh xạ tuyến tính.}}$$

### VD2 (4.1) — Tìm công thức $f$ khi biết ảnh cơ sở

$B=(u_1=(1,-2,2),\,u_2=(-2,5,-4),\,u_3=(0,-1,1))$; $f(u_1)=(1,1,-2),\,f(u_2)=(1,-2,1),\,f(u_3)=(1,2,-1)$.

Tìm $[u]_B$ cho $u=(x,y,z)$ (giải $\alpha_1u_1+\alpha_2u_2+\alpha_3u_3=u$):

$$[u]_B = (x+2y+2z,\ \ y+z,\ \ -2x+z).$$

$$f(u)=(x+2y+2z)(1,1,-2)+(y+z)(1,-2,1)+(-2x+z)(1,2,-1)$$
$$\boxed{f(x,y,z) = (-x+3y+4z,\ -3x+2z,\ -3y-4z)}$$

### VD3 (4.1) — Chứng minh tuyến tính

$f(x,y,z)=(-x+5y+2z,\ -2x+5z,\ x-3y-4z)$. Có $f(u)=uA$ với

$$A=\begin{pmatrix}-1&-2&1\\5&0&-3\\2&5&-4\end{pmatrix} \quad\Rightarrow\quad \boxed{f \text{ tuyến tính.}}$$

### VD4 (4.2) — Cơ sở của $\mathrm{Ker}\,f$

$f:\mathbb{R}^4\to\mathbb{R}^3,\ f(x,y,z,t)=(x+2y+3z+2t,\ x+3y+3z-t,\ 2x+3y+6z+7t)$.

Giải hệ thuần nhất:

$$\tilde A=\begin{pmatrix}1&2&3&2\\1&3&3&-1\\2&3&6&7\end{pmatrix}\sim\begin{pmatrix}1&0&3&8\\0&1&0&-3\\0&0&0&0\end{pmatrix}$$

Nghiệm $(x,y,z,t)=(-3a-8b,\ 3b,\ a,\ b)$. Cơ sở:

$$\boxed{\mathrm{Ker}\,f = \langle\, u_1=(-3,0,1,0),\ u_2=(-8,3,0,1)\,\rangle, \quad \dim\mathrm{Ker}\,f = 2}$$

### VD5 (4.2) — Cơ sở của $\mathrm{Im}\,f$

$f:\mathbb{R}^3\to\mathbb{R}^4,\ f(x,y,z)=(x+2y-3z,\ 3x+2y,\ 2x+2y-z,\ 4x-y+5z)$.

Ảnh cơ sở chính tắc: $f(e_1)=(1,3,2,4),\ f(e_2)=(2,2,2,-1),\ f(e_3)=(-3,0,-1,5)$.

$$\begin{pmatrix}1&3&2&4\\2&2&2&-1\\-3&0&-1&5\end{pmatrix}\xrightarrow{R_2-2R_1,\,R_3+3R_1}\begin{pmatrix}1&3&2&4\\0&-4&-2&-9\\0&0&2&-13\end{pmatrix}$$

Ba hàng khác 0 ⇒

$$\boxed{\mathrm{Im}\,f = \langle (1,3,2,4),\ (0,-4,-2,-9),\ (0,0,2,-13)\rangle,\quad \dim\mathrm{Im}\,f=3}$$

Kiểm tra: $\dim\mathrm{Ker}\,f = \dim\mathbb{R}^3 - \dim\mathrm{Im}\,f = 3-3 = 0$ ⇒ $f$ đơn ánh.

### VD6 (4.3) — $[f]_{B,C}$ qua cặp cơ sở

$f:\mathbb{R}^3\to\mathbb{R}^2,\ f(x,y,z)=(2x+y-z,\ -y+2z)$; $B=\{u_1=(1,1,0),u_2=(1,0,1),u_3=(0,1,1)\}$, $C=\{v_1=(1,2),v_2=(3,5)\}$.

$f(u_1)=(3,-1),\ f(u_2)=(1,2),\ f(u_3)=(0,1)$. Với $[w]_C$: $a=-5w_1+3w_2,\ b=2w_1-w_2$.

$$\boxed{[f]_{B,C}=\begin{pmatrix}-18&1&3\\7&0&-1\end{pmatrix}}$$

### VD7 (4.3) — $[f]$ theo cơ sở chính tắc

$f:\mathbb{R}^4\to\mathbb{R}^3,\ f(x,y,z,t)=(x-2y+z-t,\ x+2y+z+t,\ 2x+2z)$. Đọc thẳng hệ số:

$$\boxed{[f]_{B_0,B_0'}=\begin{pmatrix}1&-2&1&-1\\1&2&1&1\\2&0&2&0\end{pmatrix}}$$

### VD8 (4.3) — $[f]_{B_0}$ của toán tử

$f(x,y,z)=(2x+y+z,\ x-4y+3z,\ 2x-y-z)$:

$$\boxed{[f]_{B_0}=\begin{pmatrix}2&1&1\\1&-4&3\\2&-1&-1\end{pmatrix}}$$

### VD9 (4.3) — $[f]_B$ theo cơ sở bất kỳ

$u_1=(1,1,0),u_2=(0,2,1),u_3=(2,3,1)$; $f(x_1,x_2,x_3)=(2x_1+x_2-x_3,\ x_1+2x_2-x_3,\ 2x_1-x_2+3x_3)$.

a) $\det(u_1^\top u_2^\top u_3^\top)\neq 0$ ⇒ $B$ là cơ sở. b) Dùng $[f]_B=(B_0\to B)^{-1}[f]_{B_0}(B_0\to B)$ (giống hệt ví dụ giải mẫu slide 30–31):

$$\boxed{[f]_B=\begin{pmatrix}-1&1&-8\\-1&1&-3\\2&0&7\end{pmatrix}}$$

### VD10 (4.3) — Đổi cơ sở + tính ảnh

$f:\mathbb{R}^3\to\mathbb{R}^2$, $[f]_{B,C}=\begin{pmatrix}4&1&2\\1&3&2\end{pmatrix}$; $B=\{(1,2,1),(2,1,1),(0,2,1)\}$, $C=\{v_1=(2,1),v_2=(3,1)\}$.

$(C_0\to C)=\begin{pmatrix}2&3\\1&1\end{pmatrix}$, $(B\to B_0)=(B_0\to B)^{-1}=\begin{pmatrix}1&2&-4\\0&-1&2\\-1&-1&3\end{pmatrix}$.

a) $[f]_{B_0,C_0}=(C_0\to C)\,[f]_{B,C}\,(B\to B_0)$:

$$\boxed{[f]_{B_0,C_0}=\begin{pmatrix}1&1&8\\1&2&0\end{pmatrix}}\quad\Rightarrow\quad f(x,y,z)=(x+y+8z,\ x+2y)$$

b) $\boxed{f(3,4,1)=(15,\ 11)}$

### VD11 (4.3) — Hai ma trận biểu diễn của một toán tử

$f(x_1,x_2,x_3)=(x_1+3x_2,\ -2x_2+x_3,\ 4x_1-x_2+2x_3)$; $B=(u_1=(-1,2,1),u_2=(0,1,1),u_3=(0,-3,-2))$.

a) $\boxed{[f]_{B_0}=\begin{pmatrix}1&3&0\\0&-2&1\\4&-1&2\end{pmatrix}}$

b) $(B_0\to B)=\begin{pmatrix}-1&0&0\\2&1&-3\\1&1&-2\end{pmatrix}$, $(B_0\to B)^{-1}=\begin{pmatrix}-1&0&0\\-1&-2&3\\-1&-1&1\end{pmatrix}$. Áp dụng $[f]_B=(B_0\to B)^{-1}[f]_{B_0}(B_0\to B)$:

$$\boxed{[f]_B=\begin{pmatrix}-5&-3&9\\-11&2&-2\\-6&-1&4\end{pmatrix}}$$

*(Kiểm chứng: cột $j$ của $[f]_B$ đúng bằng $[f(u_j)]_B$.)*

### VD12 (4.3) — $f(B)$, cơ sở $\mathrm{Im}\,f$, và biểu thức $f$

$f:\mathbb{R}^3\to\mathbb{R}^3$, $[f]_{B,C}=\begin{pmatrix}-2&-2&-1\\-3&-2&0\\4&4&2\end{pmatrix}$; $B=\{(1,2,1),(2,1,1),(1,1,1)\}$, $C=\{v_1=(1,0,1),v_2=(1,1,0),v_3=(2,2,1)\}$.

a) Mỗi cột là $[f(u_j)]_C$ ⇒ $f(u_j)=$ tổ hợp $v_i$:

$$f(u_1)=(3,5,2),\quad f(u_2)=(4,6,2),\quad f(u_3)=(3,4,1).$$

Xếp thành ma trận, rút gọn ⇒ hạng 2 (vector thứ 3 phụ thuộc):

$$\boxed{\text{Cơ sở } \mathrm{Im}\,f = \{(3,5,2),\ (4,6,2)\}, \quad \dim\mathrm{Im}\,f=2}$$

b) $[u]_B=(B_0\to B)^{-1}u = (y-z,\ x-z,\ -x-y+3z)$. Ráp $f(u)=\sum [u]_{B,i}\,f(u_i)$:

$$\boxed{f(x,y,z) = (x+2z,\ \ 2x+y+z,\ \ x+y-z)}$$

---

## 3. Bản đồ ôn nhanh

| Hỏi gì | Công cụ |
|---|---|
| Có tuyến tính không? | Định nghĩa gộp / tìm $A$ với $f(u)=uA$; mẹo $f(0)=0$ |
| Tính $f$ tại điểm khi biết ảnh cơ sở | Phân tích THTT, dùng tính chất 3 |
| Tìm công thức $f$ | Tìm $[u]_B$ → $f(u)=\sum\alpha_i f(u_i)$ |
| Cơ sở $\mathrm{Ker}\,f$ | Giải hệ thuần nhất $f(u)=0$ |
| Cơ sở $\mathrm{Im}\,f$ | Ảnh cơ sở chính tắc → khử Gauss |
| Số chiều còn lại | $\dim\mathrm{Im}+\dim\mathrm{Ker}=\dim V$ |
| Ma trận biểu diễn | Cột = $[f(u_i)]_C$; Gauss–Jordan $(C\mid f(B))\to(I\mid P)$ |
| Đổi cơ sở | $[f]_{B',C'}=(C\to C')^{-1}[f]_{B,C}(B\to B')$ |
