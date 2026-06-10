---
tags: [linear-algebra, exercises, university]
aliases: [ĐSTT Đề Ôn Ch3-4]
---

# Đại số tuyến tính – Đề ôn tập (Chương 3 + 4)

> Nguồn: file.pdf (Downloads, 2026-06-10). Liên quan: [[ĐSTT_Chương3_Không_gian_vectơ]], [[ĐSTT_Chương4_Ánh_xạ_tuyến_tính]]

---

## Câu 1 — Độc lập / phụ thuộc tuyến tính trong R⁴

Cho $v_1=(1,-1,3,-2)$, $v_2=(2,-1,0,4)$, $v_3=(6,-7,24,m)$.

**Phương pháp:** Xếp các vectơ thành hàng của ma trận, khử Gauss. Hệ ĐLTT ⟺ hạng ma trận $= 3$.

$$\begin{pmatrix}1&-1&3&-2\\2&-1&0&4\\6&-7&24&m\end{pmatrix}\xrightarrow{R_2-2R_1,\;R_3-6R_1}\begin{pmatrix}1&-1&3&-2\\0&1&-6&8\\0&-1&6&m+12\end{pmatrix}\xrightarrow{R_3+R_2}\begin{pmatrix}1&-1&3&-2\\0&1&-6&8\\0&0&0&m+20\end{pmatrix}$$

Hạng $=3$ ⟺ $m+20\neq 0$ ⟺ $m\neq -20$.

### a) Với $m=6$

$m+20=26\neq 0$ nên hạng $=3$ = số vectơ.

$$\boxed{\{v_1,v_2,v_3\} \text{ độc lập tuyến tính khi } m=6}$$

### b) Giá trị $m$ để phụ thuộc tuyến tính

$$\boxed{m=-20}$$

Khi đó kiểm tra trực tiếp: $v_3 = 8v_1 - v_2$ (hệ số tìm từ 3 tọa độ đầu: $3a=24\Rightarrow a=8$, $-8-b=-7\Rightarrow b=-1$; tọa độ thứ tư $-2(8)+4(-1)=-20$ ✓).

---

## Câu 2 — Kiểm tra ánh xạ tuyến tính

Cho $f:\mathbb{R}^3\to\mathbb{R}^2$, $f(x_1,x_2,x_3)=(|x_1-3x_2|,\,6x_3)$.

**Phương pháp:** Nghi ngờ dấu giá trị tuyệt đối → thử tính thuần nhất $f(\alpha u)=\alpha f(u)$ với $\alpha=-1$.

Lấy $u=(1,0,0)$:

- $f(u)=(|1|,0)=(1,0)$, suy ra $-f(u)=(-1,0)$
- $f(-u)=f(-1,0,0)=(|-1|,0)=(1,0)$

Vì $f(-u)=(1,0)\neq(-1,0)=-f(u)$ nên $f$ vi phạm tính thuần nhất.

$$\boxed{f \text{ KHÔNG là ánh xạ tuyến tính}}$$

---

## Câu 3 — Cơ sở của không gian con sinh bởi hệ vectơ

Cho $L=\langle u_1,u_2,u_3\rangle\subset\mathbb{R}^4$ với $u_1=(1,-1,5,8)$, $u_2=(3,-3,21,13)$, $u_3=(-1,1,13,-41)$.

### a) Tìm cơ sở của $L$

$$\begin{pmatrix}1&-1&5&8\\3&-3&21&13\\-1&1&13&-41\end{pmatrix}\xrightarrow{R_2-3R_1,\;R_3+R_1}\begin{pmatrix}1&-1&5&8\\0&0&6&-11\\0&0&18&-33\end{pmatrix}\xrightarrow{R_3-3R_2}\begin{pmatrix}1&-1&5&8\\0&0&6&-11\\0&0&0&0\end{pmatrix}$$

Hạng $=2$, vậy $\dim L = 2$.

$$\boxed{\text{Cơ sở của } L:\ \{w_1=(1,-1,5,8),\ w_2=(0,0,6,-11)\}}$$

(Cũng có thể lấy $\{u_1,u_2\}$ vì hai vectơ này ĐLTT.)

### b) Xác định $m$ để $v=(5,m,31,m+34)\in L$

Tìm $a,b$ sao cho $v=a\,w_1+b\,w_2$:

| Tọa độ | Phương trình | Kết quả |
|---|---|---|
| 1 | $a=5$ | $a=5$ |
| 2 | $-a=m$ | $m=-5$ |
| 3 | $5a+6b=31$ | $b=1$ |
| 4 | $8a-11b=m+34$ | $40-11=29=m+34$ ⟹ $m=-5$ ✓ |

Hai phương trình chứa $m$ cho cùng giá trị, hệ tương thích.

$$\boxed{m=-5,\quad v = 5w_1 + w_2}$$

---

## Câu 4 — Chứng minh B là cơ sở của R³

Cho $B=\{u_1=(1,1,1),\,u_2=(2,3,8),\,u_3=(1,1,0)\}$ (toán tử $f$ kèm theo trong đề dùng cho phần sau).

**Phương pháp:** $3$ vectơ trong $\mathbb{R}^3$ là cơ sở ⟺ định thức ma trận cột khác $0$.

$$\det\begin{pmatrix}1&2&1\\1&3&1\\1&8&0\end{pmatrix} = 1(3\cdot 0-1\cdot 8) - 2(1\cdot 0-1\cdot 1) + 1(1\cdot 8-3\cdot 1) = -8+2+5 = -1 \neq 0$$

Vì định thức khác $0$, ba vectơ ĐLTT; mà $\dim\mathbb{R}^3=3$ nên:

$$\boxed{B \text{ là cơ sở của } \mathbb{R}^3}$$

---

## Câu 5 — Cơ sở của Ker f và Im f

Cho $f:\mathbb{R}^3\to\mathbb{R}^3$, $f(x_1,x_2,x_3)=(x_1+2x_3,\;5x_1+2x_2+4x_3,\;7x_1+3x_2+5x_3)$.

Ma trận chính tắc:

$$A=\begin{pmatrix}1&0&2\\5&2&4\\7&3&5\end{pmatrix}$$

### Ker f — giải $Ax=0$

- Hàng 1: $x_1+2x_3=0 \Rightarrow x_1=-2x_3$
- Hàng 2: $5(-2x_3)+2x_2+4x_3=0 \Rightarrow 2x_2=6x_3 \Rightarrow x_2=3x_3$
- Hàng 3 (kiểm tra): $7(-2x_3)+3(3x_3)+5x_3=-14x_3+9x_3+5x_3=0$ ✓

Đặt $x_3=t$: nghiệm $(x_1,x_2,x_3)=t(-2,3,1)$.

$$\boxed{\operatorname{Ker}f = \langle(-2,3,1)\rangle,\quad \dim\operatorname{Ker}f=1}$$

### Im f — không gian cột của A

$\operatorname{rank}A = 3-\dim\operatorname{Ker}f = 2$. Cột 3 phụ thuộc: $c_3 = 2c_1 - 3c_2$ (kiểm: $2(1,5,7)-3(0,2,3)=(2,4,5)$ ✓). Hai cột đầu ĐLTT.

$$\boxed{\operatorname{Im}f = \langle(1,5,7),\,(0,2,3)\rangle,\quad \dim\operatorname{Im}f=2}$$

**Kiểm tra định lý số chiều:** $\dim\operatorname{Ker}f+\dim\operatorname{Im}f = 1+2 = 3 = \dim\mathbb{R}^3$ ✓
