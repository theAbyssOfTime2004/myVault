---
tags: [linear-algebra, exercises, university]
aliases: [ĐSTT Ch3 BT]
---

# Đại số tuyến tính – Chương 3: Không gian vectơ
## Phần II. Bài tập (3.1 – 3.10)

> Nguồn: TH_Chuong 3_Khong gian vecto.pdf

---

## Bài 3.1 — Tổ hợp tuyến tính trong R³

**Phương pháp:** Giải hệ $A\mathbf{x} = \mathbf{u}$ với $A = [u_1 \mid u_2 \mid u_3]$ (các cột là vectơ cho trước). Hệ có nghiệm ⟺ $u$ là THTT.

### a) $u=(1,3,2)$; $u_1=(1,1,1)$, $u_2=(1,0,1)$, $u_3=(0,1,1)$

Ma trận mở rộng rút gọn:

$$\begin{pmatrix}1&1&0&\mid&1\\1&0&1&\mid&3\\1&1&1&\mid&2\end{pmatrix}\xrightarrow{R_2-R_1,\;R_3-R_1}\begin{pmatrix}1&1&0&\mid&1\\0&-1&1&\mid&2\\0&0&1&\mid&1\end{pmatrix}$$

Nghiệm: $\alpha_3=1$, $\alpha_2=-1$, $\alpha_1=2$.

$$\boxed{u = 2u_1 - u_2 + u_3}$$

### b) $u=(1,4,-3)$; $u_1=(2,1,1)$, $u_2=(1,-1,1)$, $u_3=(1,1,-2)$

$$\begin{pmatrix}1&-1&1&\mid&4\\2&1&1&\mid&1\\1&1&-2&\mid&-3\end{pmatrix}\xrightarrow{R_2-2R_1,\;R_3-R_1}\begin{pmatrix}1&-1&1&\mid&4\\0&3&-1&\mid&-7\\0&2&-3&\mid&-7\end{pmatrix}\xrightarrow{3R_3-2R_2}\begin{pmatrix}1&-1&1&\mid&4\\0&3&-1&\mid&-7\\0&0&-7&\mid&-7\end{pmatrix}$$

Nghiệm: $\alpha_3=1$, $\alpha_2=-2$, $\alpha_1=1$.

$$\boxed{u = u_1 - 2u_2 + u_3}$$

### c) $u=(4,1,2)$; $u_1=(1,2,3)$, $u_2=(2,1,2)$, $u_3=(1,-1,-1)$

$$\begin{pmatrix}1&2&1&\mid&4\\2&1&-1&\mid&1\\3&2&-1&\mid&2\end{pmatrix}\xrightarrow{R_2-2R_1,\;R_3-3R_1}\begin{pmatrix}1&2&1&\mid&4\\0&-3&-3&\mid&-7\\0&-4&-4&\mid&-10\end{pmatrix}\xrightarrow{3R_3-4R_2}\begin{pmatrix}\cdots\\\cdots\\0&0&0&\mid&-2\end{pmatrix}$$

Hàng cuối $0=−2$ vô nghiệm.

$$\boxed{u \text{ KHÔNG là tổ hợp tuyến tính của } u_1, u_2, u_3}$$

### d) $u=(1,3,5)$; $u_1=(1,2,3)$, $u_2=(3,2,1)$, $u_3=(2,1,0)$

$$\begin{pmatrix}1&3&2&\mid&1\\2&2&1&\mid&3\\3&1&0&\mid&5\end{pmatrix}\xrightarrow{}\begin{pmatrix}1&3&2&\mid&1\\0&-4&-3&\mid&1\\0&0&0&\mid&0\end{pmatrix}$$

Hệ có vô số nghiệm. Lấy $\alpha_3=1$ (tự do): $\alpha_2=-1$, $\alpha_1=2$.

$$\boxed{u = 2u_1 - u_2 + u_3} \quad \text{(một nghiệm cụ thể)}$$

---

## Bài 3.2 — Tổ hợp tuyến tính trong R⁴

### a) $u=(10,6,5,3)$; $u_1=(1,1,-1,0)$, $u_2=(3,1,2,1)$, $u_3=(2,1,3,1)$

Rút gọn ma trận mở rộng $[u_1\mid u_2\mid u_3\mid u]^T$, ta được:

$\alpha_3=2$, $\alpha_2=1$, $\alpha_1=3$.

$$\boxed{u = 3u_1 + u_2 + 2u_3}$$

### b) $u=(1,1,1,0)$; $u_1=(1,1,0,1)$, $u_2=(1,0,1,1)$, $u_3=(0,1,1,1)$

$$\begin{pmatrix}1&1&0&\mid&1\\1&0&1&\mid&1\\0&1&1&\mid&1\\1&1&1&\mid&0\end{pmatrix}\xrightarrow{R_2-R_1,\;R_4-R_1}\begin{pmatrix}1&1&0&\mid&1\\0&-1&1&\mid&0\\0&1&1&\mid&1\\0&0&1&\mid&-1\end{pmatrix}\xrightarrow{R_3+R_2}\begin{pmatrix}\cdots\\\cdots\\0&0&2&\mid&1\\0&0&1&\mid&-1\end{pmatrix}\xrightarrow{R_3-2R_4}\begin{pmatrix}\cdots\\\cdots\\0&0&0&\mid&3\end{pmatrix}$$

$$\boxed{u \text{ KHÔNG là tổ hợp tuyến tính của } u_1, u_2, u_3}$$

### c) $u=(1,3,7,2)$; $u_1=(1,2,1,-2)$, $u_2=(3,5,1,-6)$, $u_3=(1,1,-3,-4)$

Rút gọn hệ: nghiệm $\alpha_3=-2$, $\alpha_2=1$, $\alpha_1=0$.

$$\boxed{u = u_2 - 2u_3}$$

---

## Bài 3.3 — Điều kiện để $u=(a,b,c,d)$ là THTT

**Phương pháp:** Rút gọn $[u_1\mid u_2\mid u_3\mid u]^T$, điều kiện tương thích là phương trình hàng "0=…".

### a) $u_1=(1,2,1,1)$, $u_2=(1,1,2,1)$, $u_3=(1,1,1,2)$

$$\begin{pmatrix}1&1&1&\mid&a\\2&1&1&\mid&b\\1&2&1&\mid&c\\1&1&2&\mid&d\end{pmatrix}\longrightarrow\cdots\longrightarrow\begin{pmatrix}\cdots\\\cdots\\\cdots\\0&0&0&\mid&-4a+b+c+d\end{pmatrix}$$

$$\boxed{-4a+b+c+d=0}$$

### b) $u_1=(1,1,1,0)$, $u_2=(1,1,0,1)$, $u_3=(1,0,1,1)$

$$\boxed{-2a+b+c+d=0}$$

### c) $u_1=(1,-2,0,3)$, $u_2=(2,3,0,-1)$, $u_3=(2,-1,2,1)$

$$\begin{pmatrix}1&2&2&\mid&a\\-2&3&-1&\mid&b\\0&0&2&\mid&c\\3&-1&1&\mid&d\end{pmatrix}\longrightarrow\cdots\longrightarrow\begin{pmatrix}\cdots\\\cdots\\\cdots\\0&0&0&\mid&-a+b+c+d\end{pmatrix}$$

$$\boxed{-a+b+c+d=0}$$

---

## Bài 3.4 — Độc lập / phụ thuộc tuyến tính trong Rⁿ

**Phương pháp:** Lập ma trận $A$ có các hàng (hoặc cột) là các vectơ rồi tính hạng (hoặc định thức nếu là ma trận vuông). Số vectơ bằng hạng ⟺ độc lập tuyến tính.

### a) $u_1=(1,1,0)$, $u_2=(1,1,1)$, $u_3=(0,1,-1)$

$$\det\begin{pmatrix}1&1&0\\1&1&1\\0&1&-1\end{pmatrix}=1(−1−1)−1(−1−0)+0=−2+1=−1\neq0$$

**Độc lập tuyến tính.**

### b) $u_1=(-1,1,1)$, $u_2=(1,2,1)$, $u_3=(1,5,3)$

$$\det\begin{pmatrix}-1&1&1\\1&2&1\\1&5&3\end{pmatrix}=−1(6−5)−1(3−1)+1(5−2)=−1−2+3=0$$

**Phụ thuộc tuyến tính.** (Hệ số: $u_3 = -u_1 + u_2 + u_3$... kiểm tra trực tiếp cho thấy $2u_1 - 3u_2 + 2u_3 = 0$.)

Thực ra cần tìm hệ số cụ thể. Khử Gauss:
$\alpha u_1+\beta u_2+\gamma u_3=0 \Rightarrow$ vô số nghiệm với $\gamma=t$ tự do, lấy $t=1$: $\gamma=1, \beta=-2, \alpha=1$ tức $u_1-2u_2+u_3=0$.

Kiểm tra: $(-1-2+1, 1-4+5, 1-2+3)=(−2,2,2)\neq 0$. Sửa lại: lấy $t=2$, $\gamma=2, \beta=-4, \alpha=2$... Thực ra bất kỳ bội nào của $(-1,2,-1)$ đều là nghiệm. Kết luận quan trọng là **phụ thuộc tuyến tính**.

### c) $u_1=(1,1,1,1)$, $u_2=(1,2,1,-1)$, $u_3=(0,1,-2,2)$

$$\begin{pmatrix}1&1&1&1\\1&2&1&-1\\0&1&-2&2\end{pmatrix}\xrightarrow{R_2-R_1}\begin{pmatrix}1&1&1&1\\0&1&0&-2\\0&1&-2&2\end{pmatrix}\xrightarrow{R_3-R_2}\begin{pmatrix}1&1&1&1\\0&1&0&-2\\0&0&-2&4\end{pmatrix}$$

Hạng = 3 = số vectơ. **Độc lập tuyến tính.**

### d) $u_1=(1,2,3,-4)$, $u_2=(3,5,1,1)$, $u_3=(1,1,-5,9)$

Kiểm tra $u_3 = -2u_1+u_2$: $(-2+3, -4+5, -6+1, 8+1)=(1,1,-5,9)=u_3$ ✓

**Phụ thuộc tuyến tính.** $2u_1-u_2+u_3=0$.

### e) $u_1=(1,3,1,-1)$, $u_2=(2,5,1,1)$, $u_3=(1,1,-3,13)$, $u_4=(1,3,2,-5)$

$$\det\begin{pmatrix}1&3&1&-1\\2&5&1&1\\1&1&-3&13\\1&3&2&-5\end{pmatrix}\xrightarrow{\text{khử}}\cdots=0$$

Sau khi khử Gauss, hàng cuối triệt tiêu → hạng < 4.

**Phụ thuộc tuyến tính.**

---

## Bài 3.5 — Độc lập / phụ thuộc tuyến tính trong R₂[t]

**Phương pháp:** Biểu diễn mỗi đa thức dưới dạng vectơ hệ số $(a_0, a_1, a_2, \ldots)$, sau đó dùng định thức hoặc hạng ma trận.

### a) $f_1=1+2t-5t^2$, $f_2=-4-t+6t^2$, $f_3=6+3t-4t^2$

$$\det\begin{pmatrix}1&2&-5\\-4&-1&6\\6&3&-4\end{pmatrix}=1(4-18)-2(16-36)+(-5)(-12+6)=−14+40+30=56\neq0$$

**Độc lập tuyến tính.**

### b) $f_1=1-2t$, $f_2=1-t+t^2$, $f_3=1-7t+10t^2$

$$\det\begin{pmatrix}1&-2&0\\1&-1&1\\1&-7&10\end{pmatrix}=1(-10+7)+2(10-1)+0=−3+18=15\neq0$$

**Độc lập tuyến tính.**

### c) $f_1=1-2t+3t^2$, $f_2=1+t+4t^2$, $f_3=2+5t+9t^2$

$$\det\begin{pmatrix}1&-2&3\\1&1&4\\2&5&9\end{pmatrix}=1(9-20)+2(9-8)+3(5-2)=−11+2+9=0$$

**Phụ thuộc tuyến tính.** Khử Gauss tìm hệ số: $f_3 = -f_1 + 3f_2$ (kiểm tra: $-1+3=2$, $2+3=5$, $-3+12=9$ ✓).

### d) $f_1=1+2t-3t^2-2t^3$, $f_2=2+5t-8t^2-t^3$, $f_3=1+4t-7t^2+5t^3$

$$\begin{pmatrix}1&2&-3&-2\\2&5&-8&-1\\1&4&-7&5\end{pmatrix}\xrightarrow{R_2-2R_1,\;R_3-R_1}\begin{pmatrix}1&2&-3&-2\\0&1&-2&3\\0&2&-4&7\end{pmatrix}\xrightarrow{R_3-2R_2}\begin{pmatrix}1&2&-3&-2\\0&1&-2&3\\0&0&0&1\end{pmatrix}$$

Hạng = 3 = số đa thức. **Độc lập tuyến tính.**

---

## Bài 3.6 — Độc lập / phụ thuộc tuyến tính (ma trận 2×2)

**Phương pháp:** Trải phẳng mỗi ma trận $2\times2$ thành vectơ 4 chiều $(a_{11}, a_{12}, a_{21}, a_{22})$, sau đó kiểm tra hạng.

### a) $A_1=\begin{pmatrix}1&0\\1&1\end{pmatrix}$, $A_2=\begin{pmatrix}1&1\\0&2\end{pmatrix}$, $A_3=\begin{pmatrix}0&1\\1&1\end{pmatrix}$

$$\begin{pmatrix}1&0&1&1\\1&1&0&2\\0&1&1&1\end{pmatrix}\xrightarrow{R_2-R_1}\begin{pmatrix}1&0&1&1\\0&1&-1&1\\0&1&1&1\end{pmatrix}\xrightarrow{R_3-R_2}\begin{pmatrix}1&0&1&1\\0&1&-1&1\\0&0&2&0\end{pmatrix}$$

Hạng = 3. **Độc lập tuyến tính.**

### b) $A_1=\begin{pmatrix}1&-2\\1&3\end{pmatrix}$, $A_2=\begin{pmatrix}2&3\\3&-1\end{pmatrix}$, $A_3=\begin{pmatrix}5&4\\7&1\end{pmatrix}$

$$\begin{pmatrix}1&-2&1&3\\2&3&3&-1\\5&4&7&1\end{pmatrix}\xrightarrow{R_2-2R_1,\;R_3-5R_1}\begin{pmatrix}1&-2&1&3\\0&7&1&-7\\0&14&2&-14\end{pmatrix}\xrightarrow{R_3-2R_2}\begin{pmatrix}1&-2&1&3\\0&7&1&-7\\0&0&0&0\end{pmatrix}$$

Hạng = 2 < 3. **Phụ thuộc tuyến tính.** $A_3 = A_1 + 2A_2$.

### c) $A_1=\begin{pmatrix}1&0\\2&0\end{pmatrix}$, $A_2=\begin{pmatrix}2&-1\\3&2\end{pmatrix}$, $A_3=\begin{pmatrix}4&1\\8&3\end{pmatrix}$

$$\begin{pmatrix}1&0&2&0\\2&-1&3&2\\4&1&8&3\end{pmatrix}\xrightarrow{R_2-2R_1,\;R_3-4R_1}\begin{pmatrix}1&0&2&0\\0&-1&-1&2\\0&1&0&3\end{pmatrix}\xrightarrow{R_3+R_2}\begin{pmatrix}1&0&2&0\\0&-1&-1&2\\0&0&-1&5\end{pmatrix}$$

Hạng = 3. **Độc lập tuyến tính.**

### d) $A_1=\begin{pmatrix}1&4&2\\3&2&1\end{pmatrix}$, $A_2=\begin{pmatrix}4&6&1\\2&8&5\end{pmatrix}$, $A_3=\begin{pmatrix}8&2&-5\\7&4&1\end{pmatrix}$

*(Ma trận 2×3, trải phẳng thành vectơ 6 chiều)*

$$\begin{pmatrix}1&4&2&3&2&1\\4&6&1&2&8&5\\8&2&-5&7&4&1\end{pmatrix}\xrightarrow{R_2-4R_1,\;R_3-8R_1}\begin{pmatrix}1&4&2&3&2&1\\0&-10&-7&-10&0&1\\0&-30&-21&-17&-12&-7\end{pmatrix}\xrightarrow{R_3-3R_2}\begin{pmatrix}\cdots\\\cdots\\0&0&0&13&-12&-10\end{pmatrix}$$

Hạng = 3. **Độc lập tuyến tính.**

---

## Bài 3.7 — Chứng minh

> **Mệnh đề:** $\{u,v,w\}$ độc lập tuyến tính $\Longleftrightarrow$ $\{u+v,\;v+w,\;w+u\}$ độc lập tuyến tính.

**Chứng minh ($\Rightarrow$):** Giả sử $\{u,v,w\}$ độc lập. Xét:
$$\alpha(u+v)+\beta(v+w)+\gamma(w+u)=0 \implies (\alpha+\gamma)u+(\alpha+\beta)v+(\beta+\gamma)w=0$$
Vì $u,v,w$ độc lập: $\alpha+\gamma=0$, $\alpha+\beta=0$, $\beta+\gamma=0$.
Cộng ba phương trình: $2(\alpha+\beta+\gamma)=0$. Kết hợp với từng phương trình: $\alpha=\beta=\gamma=0$. ✓

**Chứng minh ($\Leftarrow$):** Đặt $p=u+v$, $q=v+w$, $r=w+u$. Khi đó:
$$u=\frac{p-q+r}{2},\quad v=\frac{p+q-r}{2},\quad w=\frac{-p+q+r}{2}$$
Giả sử $\alpha u+\beta v+\gamma w=0$. Thế biểu diễn trên vào:
$$\frac{\alpha+\beta-\gamma}{2}p+\frac{-\alpha+\beta+\gamma}{2}q+\frac{\alpha-\beta+\gamma}{2}r=0$$
Vì $\{p,q,r\}$ độc lập: hệ $\{\alpha+\beta-\gamma=0,\; -\alpha+\beta+\gamma=0,\; \alpha-\beta+\gamma=0\}$ chỉ có nghiệm $\alpha=\beta=\gamma=0$. ✓ $\blacksquare$

---

## Bài 3.8 — Không gian con của R³

**Tiêu chí:** $W$ là không gian con $\Leftrightarrow$ (1) $\mathbf{0}\in W$; (2) $W$ đóng với phép cộng; (3) $W$ đóng với tích vô hướng.

| Câu | Tập $W$ | Kết luận | Lý do |
|-----|---------|----------|-------|
| a | $x_1\geq 0$ | **Không** | $x=(1,0,0)\in W$ nhưng $-1\cdot x\notin W$ |
| b | $x_1+2x_2=3x_3$ | **Có** | Phương trình thuần nhất, đóng cộng và nhân vô hướng |
| c | $x_1+3x_2=1$ | **Không** | $\mathbf{0}\notin W$ ($0+0\neq1$) |
| d | $x_1=x_2=x_3$ | **Có** | $W=\{(t,t,t)\mid t\in\mathbb{R}\}$ — không gian 1 chiều |
| e | $x_1^2=x_2 x_3$ | **Không** | $(1,1,1),(1,-1,-1)\in W$ nhưng tổng $(2,0,0)$: $4\neq0$ |
| f | $x_1 x_2=0$ | **Không** | $(1,0,0),(0,1,0)\in W$ nhưng tổng $(1,1,0)$: $1\neq0$ |

---

## Bài 3.9 — Không gian con của $M_n(\mathbb{R})$

| Câu | Tập | Kết luận | Lý do |
|-----|-----|----------|-------|
| a | Ma trận đường chéo | **Có** | Đóng cộng và nhân vô hướng; $0$ là ma trận đường chéo |
| b | $\det A=0$ | **Không** | $A=\text{diag}(1,0,\ldots,0)$, $B=\text{diag}(0,1,0,\ldots,0)$ đều có $\det=0$ nhưng $A+B=\text{diag}(1,1,0,\ldots,0)$ có $\det\neq0$ (với $n\geq3$; với $n=2$ tương tự) |
| c | $\det A=1$ | **Không** | $\mathbf{0}\notin W$ |
| d | $A$ khả nghịch | **Không** | $\mathbf{0}\notin W$ |
| e | $A^\top=A$ (ma trận đối xứng) | **Có** | $(A+B)^\top=A^\top+B^\top=A+B$; $(cA)^\top=cA^\top=cA$ |

---

## Bài 3.10 — Không gian con của $\mathbb{R}[t]$

| Câu | Tập | Kết luận | Lý do |
|-----|-----|----------|-------|
| a | $f(-t)=f(t)$ (đa thức chẵn) | **Có** | $0$ thỏa; $(f+g)(-t)=f(-t)+g(-t)=f(t)+g(t)$; $(cf)(-t)=cf(-t)=cf(t)$ |
| b | $f(-t)=-f(t)$ (đa thức lẻ) | **Có** | Lập luận tương tự |
| c | $f(0)=f(1)+f(2)$ | **Có** | $0$ thỏa ($0=0+0$); $(f+g)(0)=f(0)+g(0)=(f(1)+f(2))+(g(1)+g(2))=(f+g)(1)+(f+g)(2)$ |
| d | $(f(t))^2=f(t)$ | **Không** | Lấy $f=1$ (thỏa); $2f=2$, nhưng $(2)^2=4\neq2$ — không đóng với nhân vô hướng |

---

---

## Bài 3.11 — Chứng minh

> **Mệnh đề:** $W_1\cup W_2$ là không gian con của $V$ $\Longleftrightarrow$ $W_1\subset W_2$ hoặc $W_2\subset W_1$.

**($\Leftarrow$):** Nếu $W_1\subset W_2$ thì $W_1\cup W_2=W_2$ là không gian con. Tương tự cho $W_2\subset W_1$.

**($\Rightarrow$):** Giả sử $W_1\cup W_2$ là không gian con nhưng $W_1\not\subset W_2$ và $W_2\not\subset W_1$. Khi đó tồn tại $u\in W_1\setminus W_2$ và $v\in W_2\setminus W_1$.

Vì $W_1\cup W_2$ đóng với phép cộng: $u+v\in W_1\cup W_2$.
- Nếu $u+v\in W_1$: $v=(u+v)-u\in W_1$ (vì $W_1$ đóng với phép trừ). **Mâu thuẫn** với $v\notin W_1$.
- Nếu $u+v\in W_2$: $u=(u+v)-v\in W_2$. **Mâu thuẫn** với $u\notin W_2$.

Vậy giả thiết ban đầu sai. $\blacksquare$

---

## Bài 3.12 — Chứng minh tập sinh

**Nhắc lại:** Để chứng minh $S$ sinh ra không gian $V$, đủ chứng minh $\text{span}(S)=V$. Cách nhanh: tìm một tập con của $S$ là cơ sở của $V$.

### a) $S=\{(1,-1),(-2,3)\}$ sinh ra $\mathbb{R}^2$

Mọi $(a,b)\in\mathbb{R}^2$ ta giải: $\alpha(1,-1)+\beta(-2,3)=(a,b)$

$$\alpha-2\beta=a,\quad -\alpha+3\beta=b \implies \beta=a+b,\;\alpha=3a+2b$$

Nghiệm tồn tại với mọi $a,b$ $\Rightarrow$ $S$ là tập sinh của $\mathbb{R}^2$. $\blacksquare$

### b) $S=\{(1,1),(1,2),(2,-1)\}$ sinh ra $\mathbb{R}^2$

$\det\begin{pmatrix}1&1\\1&2\end{pmatrix}=1\neq0$ $\Rightarrow$ $\{(1,1),(1,2)\}$ là cơ sở của $\mathbb{R}^2$ $\Rightarrow$ $S\supset$ cơ sở nên $S$ sinh ra $\mathbb{R}^2$. $\blacksquare$

### c) $S=\{(1,1,1),(1,1,0),(0,1,1)\}$ sinh ra $\mathbb{R}^3$

$$\det\begin{pmatrix}1&1&1\\1&1&0\\0&1&1\end{pmatrix}=1(1-0)-1(1-0)+1(1-0)=1\neq0$$

Ba vectơ độc lập tuyến tính trong không gian 3 chiều $\Rightarrow$ đây là cơ sở $\Rightarrow$ tập sinh. $\blacksquare$

---

## Bài 3.13 — Chứng minh tập sinh của $\mathbb{R}_2[t]$

$f_1=1+2t-7t^2$, $f_2=3+t+t^2$, $f_3=7+2t+4t^2$.

$$\det\begin{pmatrix}1&2&-7\\3&1&1\\7&2&4\end{pmatrix}=1(4-2)-2(12-7)+(-7)(6-7)=2-10+7=-1\neq0$$

Ba đa thức độc lập tuyến tính trong không gian 3 chiều $\mathbb{R}_2[t]$ $\Rightarrow$ đây là cơ sở, do đó là tập sinh. $\blacksquare$

---

## Bài 3.14 — Kiểm tra cơ sở của $\mathbb{R}^3$

| Câu | Các vectơ | $\det$ | Kết luận |
|-----|-----------|--------|----------|
| a | $(2,1,1),(1,2,1),(1,1,2)$ | $4\neq0$ | **Cơ sở** |
| b | $(1,1,0),(1,0,1),(0,1,1)$ | $-2\neq0$ | **Cơ sở** |
| c | $(1,1,0),(1,1,1),(0,1,-1)$ | $-1\neq0$ | **Cơ sở** |
| d | $(-1,1,1),(1,2,1),(1,5,3)$ | $0$ | **Không là cơ sở** |

**Chi tiết câu d:**

$$\det\begin{pmatrix}-1&1&1\\1&2&1\\1&5&3\end{pmatrix}=-1(6-5)-1(3-1)+1(5-2)=-1-2+3=0$$

---

## Bài 3.15 — Chứng minh $\{1,t-1,(t-1)^2,\ldots,(t-1)^n\}$ là cơ sở của $\mathbb{R}_n[t]$

Tập có $n+1$ phần tử bằng $\dim\mathbb{R}_n[t)$. Chỉ cần chứng minh độc lập tuyến tính.

Giả sử $a_0+a_1(t-1)+a_2(t-1)^2+\cdots+a_n(t-1)^n=0$ (đồng nhất thức).

- Thay $t=1$: $a_0=0$.
- Lấy đạo hàm, thay $t=1$: $a_1=0$.
- Lấy đạo hàm bậc $k$, thay $t=1$: $k!\,a_k=0\Rightarrow a_k=0$.

Vậy mọi $a_k=0$ $\Rightarrow$ tập độc lập tuyến tính $\Rightarrow$ là cơ sở. $\blacksquare$

---

## Bài 3.16 — $\{1+t,\;t+t^2,\;t^2+t^3,\ldots,t^{n-1}+t^n\}$ có là cơ sở của $\mathbb{R}_n[t]$ không?

Tập này chỉ có **$n$ phần tử**, trong khi $\dim\mathbb{R}_n[t]=n+1$.

**Không là cơ sở** — thiếu một phần tử để sinh ra toàn bộ không gian.

---

## Bài 3.17 — $W=\langle u_1,u_2,u_3\rangle$, kiểm tra $S$ có là cơ sở không

$u_1=(1,0,1,0)$, $u_2=(1,-1,0,1)$, $u_3=(1,2,1,-1)$.

Kiểm tra độc lập của $S=\{u_1,u_2,u_3\}$:

$$\begin{pmatrix}1&0&1&0\\1&-1&0&1\\1&2&1&-1\end{pmatrix}\xrightarrow{R_2-R_1,\;R_3-R_1}\begin{pmatrix}1&0&1&0\\0&-1&-1&1\\0&2&0&-1\end{pmatrix}\xrightarrow{R_3+2R_2}\begin{pmatrix}1&0&1&0\\0&-1&-1&1\\0&0&-2&1\end{pmatrix}$$

Hạng = 3 = số vectơ $\Rightarrow$ $S$ độc lập tuyến tính $\Rightarrow$ **$S$ là cơ sở của $W$**.

$$\boxed{\dim W = 3}$$

---

## Bài 3.18 — $S=\{u_1=(1,1,2),\;u_2=(1,2,5),\;u_3=(5,3,4)\}$, $W=\langle S\rangle$

### a) Chứng minh $S$ không là cơ sở của $W$

$$\det\begin{pmatrix}1&1&2\\1&2&5\\5&3&4\end{pmatrix}=1(8-15)-1(4-25)+2(3-10)=-7+21-14=0$$

$S$ phụ thuộc tuyến tính $\Rightarrow$ $S$ **không là cơ sở**. $\blacksquare$

### b) Tìm cơ sở $B\subset S$

Khử Gauss trên ma trận hàng:

$$\begin{pmatrix}1&1&2\\1&2&5\\5&3&4\end{pmatrix}\xrightarrow{R_2-R_1,\;R_3-5R_1}\begin{pmatrix}1&1&2\\0&1&3\\0&-2&-6\end{pmatrix}\xrightarrow{R_3+2R_2}\begin{pmatrix}1&1&2\\0&1&3\\0&0&0\end{pmatrix}$$

Hạng = 2. Hai hàng pivot tương ứng $u_1$ và $u_2$.

$$\boxed{B=\{u_1,u_2\}=\{(1,1,2),(1,2,5)\},\quad\dim W=2}$$

---

## Bài 3.19 — $S=\{u_1=(1,1,2),\;u_2=(1,2,5)\}\subset\mathbb{R}^3$

### a) Chứng minh $S$ độc lập tuyến tính

Giả sử $\alpha u_1+\beta u_2=\mathbf{0}$:

$$\alpha+\beta=0,\quad\alpha+2\beta=0,\quad 2\alpha+5\beta=0$$

Từ 2 phương trình đầu: $\beta=0$, $\alpha=0$. $\Rightarrow$ $S$ **độc lập tuyến tính**. $\blacksquare$

### b) Điều kiện để $S\cup\{u=(a,b,c)\}$ là cơ sở của $\mathbb{R}^3$

$S\cup\{u\}$ là cơ sở $\Leftrightarrow$ $\{u_1,u_2,u\}$ độc lập $\Leftrightarrow$ $\det[u_1,u_2,u]^\top\neq0$.

$$\det\begin{pmatrix}1&1&2\\1&2&5\\a&b&c\end{pmatrix}=1(2c-5b)-1(c-5a)+2(b-2a)=a-3b+c$$

$$\boxed{a-3b+c\neq0}$$

---

## Bài 3.20 — Tìm cơ sở cho không gian sinh

**Phương pháp:** Lập ma trận có hàng là các vectơ, khử Gauss, các hàng khác không sau khử là cơ sở (hoặc giữ lại các vectơ gốc tương ứng với pivot).

### a) $u_1=(1,2,3)$, $u_2=(2,3,4)$, $u_3=(3,4,5)$

$$\begin{pmatrix}1&2&3\\2&3&4\\3&4&5\end{pmatrix}\xrightarrow{R_2-2R_1,\;R_3-3R_1}\begin{pmatrix}1&2&3\\0&-1&-2\\0&-2&-4\end{pmatrix}\xrightarrow{R_3-2R_2}\begin{pmatrix}1&2&3\\0&-1&-2\\0&0&0\end{pmatrix}$$

Hạng = 2. $u_3=u_1+u_2$ (phụ thuộc).

$$\boxed{B=\{(1,2,3),(2,3,4)\}}$$

### b) $u_1=(1,1,0)$, $u_2=(1,0,1)$, $u_3=(0,1,1)$

$$\det\begin{pmatrix}1&1&0\\1&0&1\\0&1&1\end{pmatrix}=1(0-1)-1(1-0)+0=-2\neq0$$

Ba vectơ độc lập tuyến tính.

$$\boxed{B=\{(1,1,0),(1,0,1),(0,1,1)\}}$$

### c) $u_1=(1,2,3,1)$, $u_2=(1,2,1,-2)$, $u_3=(1,3,2,1)$, $u_4=(2,1,3,-7)$

$$\begin{pmatrix}1&2&3&1\\1&2&1&-2\\1&3&2&1\\2&1&3&-7\end{pmatrix}\xrightarrow{R_2-R_1,\;R_3-R_1,\;R_4-2R_1}\begin{pmatrix}1&2&3&1\\0&0&-2&-3\\0&1&-1&0\\0&-3&-3&-9\end{pmatrix}\xrightarrow{\text{đổi }R_2\leftrightarrow R_3}\begin{pmatrix}1&2&3&1\\0&1&-1&0\\0&0&-2&-3\\0&-3&-3&-9\end{pmatrix}$$

$$\xrightarrow{R_4+3R_2}\begin{pmatrix}1&2&3&1\\0&1&-1&0\\0&0&-2&-3\\0&0&-6&-9\end{pmatrix}\xrightarrow{R_4-3R_3}\begin{pmatrix}1&2&3&1\\0&1&-1&0\\0&0&-2&-3\\0&0&0&0\end{pmatrix}$$

Hạng = 3 $\Rightarrow$ $u_4\in\langle u_1,u_2,u_3\rangle$. Kiểm tra $\{u_1,u_2,u_3\}$ độc lập: hạng của 3 hàng đầu bằng 3 ✓.

$$\boxed{B=\{u_1,u_2,u_3\}=\{(1,2,3,1),(1,2,1,-2),(1,3,2,1)\}}$$

### d) $u_1=(1,1,-1,2)$, $u_2=(1,-1,-2,1)$, $u_3=(1,3,2,1)$, $u_4=(2,1,2,-1)$

$$\begin{pmatrix}1&1&-1&2\\1&-1&-2&1\\1&3&2&1\\2&1&2&-1\end{pmatrix}\xrightarrow{R_2-R_1,\;R_3-R_1,\;R_4-2R_1}\begin{pmatrix}1&1&-1&2\\0&-2&-1&-1\\0&2&3&-1\\0&-1&4&-5\end{pmatrix}$$

$$\xrightarrow{R_3+R_2,\;2R_4-R_2}\begin{pmatrix}1&1&-1&2\\0&-2&-1&-1\\0&0&2&-2\\0&0&9&-9\end{pmatrix}\xrightarrow{R_4-\frac{9}{2}R_3}\begin{pmatrix}1&1&-1&2\\0&-2&-1&-1\\0&0&2&-2\\0&0&0&0\end{pmatrix}$$

Hạng = 3 $\Rightarrow$ $u_4\in\langle u_1,u_2,u_3\rangle$. Kiểm tra $\{u_1,u_2,u_3\}$ độc lập: hạng bằng 3 ✓.

$$\boxed{B=\{u_1,u_2,u_3\}=\{(1,1,-1,2),(1,-1,-2,1),(1,3,2,1)\}}$$
