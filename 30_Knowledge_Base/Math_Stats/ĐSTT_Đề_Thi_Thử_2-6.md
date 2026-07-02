---
tags: [linear-algebra, exam, mock-exam, university]
aliases: [ĐSTT Đề Thi Thử 2-6, Mock Final LATT Set 2]
---
 
# Đại số tuyến tính – 5 đề thi thử bổ sung (Đề số 2–6)

> Tiếp theo [[ĐSTT_Đề_Thi_Thử_Cuối_Kỳ]]. Cùng format 4 câu / 10đ (3,5 + 3 + 2,5 + 1). Số liệu tự chế, đã giải và kiểm chứng từng câu (thay nghiệm ngược, kiểm $n=1$, kiểm $f(u_i)$...).
> **Cách dùng:** che đáp án, tự làm ~75 phút mỗi đề, rồi đối chiếu.

---
---

# ĐỀ SỐ 2

## Đề

**Câu 1 (3,5đ).** Cho hệ thuần nhất 4 ẩn:
$$\begin{cases}x_1+x_2+x_3+x_4=0\\x_1+2x_2+x_3+2x_4=0\\2x_1+3x_2+2x_3+3x_4=0\end{cases}$$
a) Tìm cơ sở và số chiều không gian nghiệm $W$.
b) Cho $U=\langle u_1=(1,0,0,1),u_2=(0,1,1,0),u_3=(1,1,1,1)\rangle$. Tìm cơ sở $U+W$. Suy ra $\dim(U\cap W)$ và xác định $U\cap W$.

**Câu 2 (3đ).** Cho $B=\{u_1=(1,1,1),u_2=(1,1,0),u_3=(1,0,0)\}$ cơ sở $\mathbb{R}^3$, $[f]_B=\begin{pmatrix}1&0&1\\2&1&0\\0&1&1\end{pmatrix}$.
a) Tìm công thức $f(x,y,z)$. b) $u=(2,1,0)$: tìm $[f(u)]_B$. c) Tìm cơ sở & $\dim\operatorname{Ker}f$, suy ra $\dim\operatorname{Im}f$.

**Câu 3 (2,5đ).** $A=\begin{pmatrix}2&3\\1&4\end{pmatrix}$. a) Chéo hóa $A$. b) Tìm $A^n,\forall n\in\mathbb{N}$.

**Câu 4 (1đ).** Tìm trị riêng, vectơ riêng của $A=\begin{pmatrix}3&1&2\\0&1&4\\0&0&5\end{pmatrix}$.

## Đáp án

**Câu 1a.** Khử Gauss ma trận hệ số:
$$\begin{pmatrix}1&1&1&1\\1&2&1&2\\2&3&2&3\end{pmatrix}\xrightarrow{R_2-R_1,\ R_3-2R_1}\begin{pmatrix}1&1&1&1\\0&1&0&1\\0&1&0&1\end{pmatrix}\xrightarrow{R_3-R_2}\begin{pmatrix}1&1&1&1\\0&1&0&1\\0&0&0&0\end{pmatrix}$$
Hạng $r=2\Rightarrow\dim W=4-2=2$. Ẩn cơ sở $x_1,x_2$; tự do $x_3=s,\ x_4=t$.
- $R_2$: $x_2+x_4=0\Rightarrow x_2=-t$.
- $R_1$: $x_1=-x_2-x_3-x_4=t-s-t=-s$.

Nghiệm tổng quát $(x_1,x_2,x_3,x_4)=s(-1,0,1,0)+t(0,-1,0,1)$.
$$\boxed{W=\langle w_1=(-1,0,1,0),\ w_2=(0,-1,0,1)\rangle,\quad \dim W=2.}$$

**Câu 1b.**

**Bước 0 — $\dim U$:** xếp $u_1,u_2,u_3$ thành dòng, khử Gauss:
$$\begin{pmatrix}1&0&0&1\\0&1&1&0\\1&1&1&1\end{pmatrix}\xrightarrow{R_3-R_1}\begin{pmatrix}1&0&0&1\\0&1&1&0\\0&1&1&0\end{pmatrix}\xrightarrow{R_3-R_2}\begin{pmatrix}1&0&0&1\\0&1&1&0\\0&0&0&0\end{pmatrix}$$
Hạng $=2$ ⇒ $\dim U=2$ ($u_3=u_1+u_2$ thừa), cơ sở $\{u_1,u_2\}$.

**Bước 1 — cơ sở & $\dim(U+W)$:** gộp $u_1,u_2,w_1,w_2$ thành dòng, khử Gauss:
$$\begin{pmatrix}1&0&0&1\\0&1&1&0\\-1&0&1&0\\0&-1&0&1\end{pmatrix}\xrightarrow{R_3+R_1,\ R_4+R_2}\begin{pmatrix}1&0&0&1\\0&1&1&0\\0&0&1&1\\0&0&1&1\end{pmatrix}\xrightarrow{R_4-R_3}\begin{pmatrix}1&0&0&1\\0&1&1&0\\0&0&1&1\\0&0&0&0\end{pmatrix}$$
Có 3 dòng khác 0 ⇒
$$\boxed{\dim(U+W)=3,\quad \text{cơ sở }\{(1,0,0,1),(0,1,1,0),(0,0,1,1)\}.}$$

**Bước 2 — Grassmann:** $\dim(U\cap W)=\dim U+\dim W-\dim(U+W)=2+2-3=\boxed{1}$.

**Bước 3 — xác định $U\cap W$:** giải $\alpha u_1+\beta u_2=s w_1+t w_2$.

Vế trái: $\alpha(1,0,0,1)+\beta(0,1,1,0)=(\alpha,\ \beta,\ \beta,\ \alpha)$.
Vế phải: $s(-1,0,1,0)+t(0,-1,0,1)=(-s,\ -t,\ s,\ t)$.

Cân bằng từng tọa độ:
$$\begin{cases}\alpha=-s\\ \beta=-t\\ \beta=s\\ \alpha=t\end{cases}\Rightarrow\ s=-\alpha,\ t=\alpha\ (\text{từ }1,4);\ \text{thế vào }(2),(3):\ \beta=-\alpha\ (\text{cả hai khớp, không mâu thuẫn}).$$
Tự do $\alpha=r$: $(\alpha,\beta,s,t)=(r,-r,-r,r)$. Vectơ giao (vế $U$):
$$v=\alpha u_1+\beta u_2=r\,u_1-r\,u_2=r(1,-1,-1,1).$$
*(Kiểm vế $W$: $sw_1+tw_2=-r\,w_1+r\,w_2=r(w_2-w_1)=r(1,-1,-1,1)$ — trùng ✓; đúng 1 tham số tự do ⇒ khớp Grassmann.)*
$$\boxed{U\cap W=\langle(1,-1,-1,1)\rangle.}$$

**Câu 2a.** $P=(u_1\,u_2\,u_3)=\begin{pmatrix}1&1&1\\1&1&0\\1&0&0\end{pmatrix}$, $\det P=-1$, $P^{-1}=\begin{pmatrix}0&0&1\\0&1&-1\\1&-1&0\end{pmatrix}$. $[f]_{B_0}=P[f]_BP^{-1}=\begin{pmatrix}2&0&1\\1&0&2\\1&-1&1\end{pmatrix}$.
$$\boxed{f(x,y,z)=(2x+z,\ x+2z,\ x-y+z).}$$
*(Kiểm: cột 1 của $[f]_B$ là $(1,2,0)^\top \Rightarrow f(u_1)=1u_1+2u_2+0u_3=(1,1,1)+(2,2,0)=(3,3,1)$. Thay $u_1=(1,1,1)$ vào công thức: $f(1,1,1)=(2+1,1+2,1-1+1)=(3,3,1)$ ✓ khớp.)*

**Câu 2b.** $[u]_B=P^{-1}(2,1,0)=(0,1,1)$. $[f(u)]_B=[f]_B(0,1,1)^\top=(1,1,2)$.
$$\boxed{[f(u)]_B=(1,1,2).}$$
*(Kiểm: $f(2,1,0)=(4,2,1)$; $1u_1+1u_2+2u_3=(1,1,1)+(1,1,0)+(2,0,0)=(4,2,1)$ ✓ khớp.)*

**Câu 2c.** $\operatorname{Ker}f$ là nghiệm của hệ $f(x,y,z)=0$, ứng với ma trận hệ số chính là $[f]_{B_0}$:
$$\begin{pmatrix}2&0&1\\1&0&2\\1&-1&1\end{pmatrix}\xrightarrow{R_1\leftrightarrow R_2}\begin{pmatrix}1&0&2\\2&0&1\\1&-1&1\end{pmatrix}\xrightarrow{R_2-2R_1,\ R_3-R_1}\begin{pmatrix}1&0&2\\0&0&-3\\0&-1&-1\end{pmatrix}\xrightarrow{R_2\leftrightarrow R_3}\begin{pmatrix}1&0&2\\0&-1&-1\\0&0&-3\end{pmatrix}$$
Hạng $=3$ (đủ 3 pivot) $\Rightarrow \dim\operatorname{Ker}f=3-3=0$. *(Thế ngược cũng ra: $R_3\Rightarrow z=0$; $R_2\Rightarrow y=0$; $R_1\Rightarrow x=0$ — chỉ nghiệm tầm thường.)*
$$\boxed{\operatorname{Ker}f=\{0\},\ \dim\operatorname{Ker}f=0,\quad \dim\operatorname{Im}f=3\ (f\text{ là song ánh}).}$$

**Câu 3a.** $P_A(\lambda)=\lambda^2-6\lambda+5=(\lambda-1)(\lambda-5)$. $E(1)=\langle(3,-1)\rangle$, $E(5)=\langle(1,1)\rangle$.
$$\boxed{P=\begin{pmatrix}3&1\\-1&1\end{pmatrix},\quad D=\begin{pmatrix}1&0\\0&5\end{pmatrix}.}$$

**Câu 3b.** $P^{-1}=\tfrac14\begin{pmatrix}1&-1\\1&3\end{pmatrix}$.
$$\boxed{A^n=\frac14\begin{pmatrix}5^n+3 & 3\cdot5^n-3\\ 5^n-1 & 3\cdot5^n+1\end{pmatrix}.}$$
*(Kiểm $n=1$: $\tfrac14\begin{psmallmatrix}8&12\\4&16\end{psmallmatrix}=A$ ✓.)*

**Câu 4.** $A$ tam giác trên $\Rightarrow$ trị riêng $=$ đường chéo: $\lambda=3,1,5$.
- $\lambda=3$: $(A-3I)X=0\Rightarrow (1,0,0)$.
- $\lambda=1$: $(A-I)X=0\Rightarrow (1,-2,0)$.
- $\lambda=5$: $(A-5I)X=0\Rightarrow (3,2,2)$.

$$\boxed{\lambda=3\to(1,0,0);\quad \lambda=1\to(1,-2,0);\quad \lambda=5\to(3,2,2).}$$

---
---

# ĐỀ SỐ 3

## Đề

**Câu 1 (3,5đ).**
$$\begin{cases}x_1-x_2+x_3-x_4=0\\x_1+x_2-x_3+x_4=0\\2x_1+x_3-x_4=0\end{cases}$$
a) Tìm cơ sở, số chiều không gian nghiệm $W$.
b) Cho $U=\langle u_1=(1,1,0,0),u_2=(1,0,1,1)\rangle$. Tìm cơ sở $U+W$, suy ra $\dim(U\cap W)$ và xác định $U\cap W$.

**Câu 2 (3đ).** $B=\{u_1=(1,0,0),u_2=(1,1,0),u_3=(1,1,1)\}$, $[f]_B=\begin{pmatrix}1&1&0\\0&1&1\\1&2&1\end{pmatrix}$.
a) Tìm $f(x,y,z)$. b) $u=(2,1,3)$: tìm $[f(u)]_B$. c) Cơ sở & $\dim\operatorname{Ker}f$, suy ra $\dim\operatorname{Im}f$.

**Câu 3 (2,5đ).** $A=\begin{pmatrix}5&4\\1&2\end{pmatrix}$. a) Chéo hóa. b) Tìm $A^n$.

**Câu 4 (1đ).** Trị riêng, vectơ riêng của $A=\begin{pmatrix}3&0&0\\2&-1&0\\1&4&2\end{pmatrix}$.

## Đáp án

**Câu 1a.** Khử Gauss:
$$\begin{pmatrix}1&-1&1&-1\\1&1&-1&1\\2&0&1&-1\end{pmatrix}\xrightarrow{R_2-R_1,\ R_3-2R_1}\begin{pmatrix}1&-1&1&-1\\0&2&-2&2\\0&2&-1&1\end{pmatrix}\xrightarrow{R_3-R_2}\begin{pmatrix}1&-1&1&-1\\0&2&-2&2\\0&0&1&-1\end{pmatrix}$$
Hạng $r=3\Rightarrow\dim W=4-3=1$. Tự do $x_4=t$.
- $R_3$: $x_3-x_4=0\Rightarrow x_3=t$.
- $R_2$: $2x_2-2x_3+2x_4=0\Rightarrow x_2=x_3-x_4=0$.
- $R_1$: $x_1-x_2+x_3-x_4=0\Rightarrow x_1=x_2-x_3+x_4=0-t+t=0$.

$$\boxed{W=\langle(0,0,1,1)\rangle,\quad \dim W=1.}$$

**Câu 1b.**

**Bước 0 — $\dim U$:** $u_1=(1,1,0,0),u_2=(1,0,1,1)$ không tỉ lệ ⇒ ĐLTT ⇒ $\dim U=2$.

**Bước 1 — cơ sở & $\dim(U+W)$:** gộp $u_1,u_2,w=(0,0,1,1)$ thành dòng:
$$\begin{pmatrix}1&1&0&0\\1&0&1&1\\0&0&1&1\end{pmatrix}\xrightarrow{R_2-R_1}\begin{pmatrix}1&1&0&0\\0&-1&1&1\\0&0&1&1\end{pmatrix}$$
Đã là bậc thang, hạng $=3$ ⇒
$$\boxed{\dim(U+W)=3,\quad \text{cơ sở }\{(1,1,0,0),(0,-1,1,1),(0,0,1,1)\}.}$$

**Bước 2 — Grassmann:** $\dim(U\cap W)=2+1-3=\boxed{0}$.

**Bước 3 — xác định $U\cap W$:** giải $\alpha u_1+\beta u_2=t\,w$ ($W$ chỉ có 1 vectơ sinh).

Vế trái: $\alpha(1,1,0,0)+\beta(1,0,1,1)=(\alpha+\beta,\ \alpha,\ \beta,\ \beta)$.
Vế phải: $t(0,0,1,1)=(0,\ 0,\ t,\ t)$.

Cân bằng từng tọa độ:
$$\begin{cases}\alpha+\beta=0\\ \alpha=0\\ \beta=t\\ \beta=t\end{cases}\Rightarrow\ \alpha=0\ (\text{từ }2)\ \Rightarrow\ \beta=0\ (\text{từ }1)\ \Rightarrow\ t=0\ (\text{từ }3).$$
Chỉ nghiệm tầm thường $(\alpha,\beta,t)=(0,0,0)$ — **không có tham số tự do** ⇒ khớp $\dim(U\cap W)=0$ ở Grassmann.
$$\boxed{U\cap W=\{0\}.}$$

**Câu 2a.** $P=\begin{pmatrix}1&1&1\\0&1&1\\0&0&1\end{pmatrix}$, $P^{-1}=\begin{pmatrix}1&-1&0\\0&1&-1\\0&0&1\end{pmatrix}$. $[f]_{B_0}=P[f]_BP^{-1}=\begin{pmatrix}2&2&-2\\1&2&-1\\1&1&-1\end{pmatrix}$.
$$\boxed{f(x,y,z)=(2x+2y-2z,\ x+2y-z,\ x+y-z).}$$
*(Kiểm: cột 1 của $[f]_B$ là $(1,0,1)^\top \Rightarrow f(u_1)=1u_1+0u_2+1u_3=(1,0,0)+(1,1,1)=(2,1,1)$. Thay $u_1=(1,0,0)$: $f(1,0,0)=(2,1,1)$ ✓ khớp.)*

**Câu 2b.** $[u]_B=P^{-1}(2,1,3)=(1,-2,3)$. $[f(u)]_B=[f]_B(1,-2,3)^\top=(-1,1,0)$.
$$\boxed{[f(u)]_B=(-1,1,0).}$$
*(Kiểm: $f(2,1,3)=(0,1,0)$; $-1u_1+1u_2+0u_3=-1(1,0,0)+(1,1,0)=(0,1,0)$ ✓ khớp.)*

**Câu 2c.** Ma trận hệ số của $f(x,y,z)=0$ chính là $[f]_{B_0}$:
$$\begin{pmatrix}2&2&-2\\1&2&-1\\1&1&-1\end{pmatrix}\xrightarrow{R_1\leftrightarrow R_3}\begin{pmatrix}1&1&-1\\1&2&-1\\2&2&-2\end{pmatrix}\xrightarrow{R_2-R_1,\ R_3-2R_1}\begin{pmatrix}1&1&-1\\0&1&0\\0&0&0\end{pmatrix}$$
Hạng $=2\Rightarrow \dim\operatorname{Ker}f=3-2=1$. Tự do $x_3=t$: $R_2\Rightarrow y=0$; $R_1\Rightarrow x=-y+z=t$.
$$\boxed{\operatorname{Ker}f=\langle(1,0,1)\rangle,\ \dim\operatorname{Ker}f=1,\quad \dim\operatorname{Im}f=2.}$$

**Câu 3a.** $P_A(\lambda)=\lambda^2-7\lambda+6=(\lambda-1)(\lambda-6)$. $E(1)=\langle(1,-1)\rangle,\ E(6)=\langle(4,1)\rangle$.
$$\boxed{P=\begin{pmatrix}1&4\\-1&1\end{pmatrix},\quad D=\begin{pmatrix}1&0\\0&6\end{pmatrix}.}$$

**Câu 3b.**
$$\boxed{A^n=\frac15\begin{pmatrix}4\cdot6^n+1 & 4\cdot6^n-4\\ 6^n-1 & 6^n+4\end{pmatrix}.}$$
*(Kiểm $n=1$: $\tfrac15\begin{psmallmatrix}25&20\\5&10\end{psmallmatrix}=A$ ✓.)*

**Câu 4.** $A$ tam giác dưới $\Rightarrow$ trị riêng $=$ đường chéo: $\lambda=3,-1,2$.
- $\lambda=3$: $(A-3I)X=0 \Rightarrow (2,1,6)$.
- $\lambda=-1$: $(A+I)X=0 \Rightarrow (0,-3,4)$.
- $\lambda=2$: $(A-2I)X=0 \Rightarrow (0,0,1)$.

$$\boxed{\lambda=3\to(2,1,6);\quad \lambda=-1\to(0,-3,4);\quad \lambda=2\to(0,0,1).}$$

---
---

# ĐỀ SỐ 4

## Đề

**Câu 1 (3,5đ).**
$$\begin{cases}x_1+x_2-x_3+x_4=0\\x_1-x_2+x_3+x_4=0\\x_1+3x_2-3x_3+x_4=0\end{cases}$$
a) Tìm cơ sở, số chiều không gian nghiệm $W$.
b) Cho $U=\langle u_1=(1,0,0,1),u_2=(0,1,1,0),u_3=(1,1,1,1)\rangle$. Tìm cơ sở $U+W$, suy ra $\dim(U\cap W)$, xác định $U\cap W$.

**Câu 2 (3đ).** $B=\{u_1=(1,1,0),u_2=(0,1,1),u_3=(1,0,1)\}$, $[f]_B=\begin{pmatrix}1&1&0\\0&2&1\\1&0&1\end{pmatrix}$.
a) Tìm $f(x,y,z)$. b) $u=(3,2,1)$: tìm $[f(u)]_B$. c) Cơ sở & $\dim\operatorname{Ker}f$, suy ra $\dim\operatorname{Im}f$.

**Câu 3 (2,5đ).** $A=\begin{pmatrix}4&-1\\2&1\end{pmatrix}$. a) Chéo hóa. b) Tìm $A^n$.

**Câu 4 (1đ).** Trị riêng, vectơ riêng của $A=\begin{pmatrix}2&1&0\\0&-1&3\\0&0&4\end{pmatrix}$.

## Đáp án

**Câu 1a.** Khử Gauss:
$$\begin{pmatrix}1&1&-1&1\\1&-1&1&1\\1&3&-3&1\end{pmatrix}\xrightarrow{R_2-R_1,\ R_3-R_1}\begin{pmatrix}1&1&-1&1\\0&-2&2&0\\0&2&-2&0\end{pmatrix}\xrightarrow{R_3+R_2}\begin{pmatrix}1&1&-1&1\\0&-2&2&0\\0&0&0&0\end{pmatrix}$$
Hạng $r=2\Rightarrow\dim W=4-2=2$. Tự do $x_3=s,\ x_4=t$.
- $R_2$: $-2x_2+2x_3=0\Rightarrow x_2=x_3=s$.
- $R_1$: $x_1+x_2-x_3+x_4=0\Rightarrow x_1=-x_2+x_3-x_4=-s+s-t=-t$.

$$\boxed{W=\langle w_1=(0,1,1,0),\ w_2=(-1,0,0,1)\rangle,\quad \dim W=2.}$$

**Câu 1b.**

**Bước 0 — $\dim U$:** $u_3=(1,1,1,1)=u_1+u_2$ (thừa) $\Rightarrow \dim U=2$, cơ sở $\{u_1,u_2\}$. **Chú ý $u_2=(0,1,1,0)=w_1$** — chi tiết này sẽ làm gọn bước sau.

**Bước 1 — cơ sở & $\dim(U+W)$:** vì $u_2=w_1$ (trùng), chỉ cần gộp $u_1,w_1,w_2$ (không cần lặp $u_2$):
$$\begin{pmatrix}1&0&0&1\\0&1&1&0\\-1&0&0&1\end{pmatrix}\xrightarrow{R_3+R_1}\begin{pmatrix}1&0&0&1\\0&1&1&0\\0&0&0&2\end{pmatrix}$$
Hạng $=3$ ⇒
$$\boxed{\dim(U+W)=3,\quad \text{cơ sở }\{(1,0,0,1),(0,1,1,0),(0,0,0,1)\}.}$$

**Bước 2 — Grassmann:** $\dim(U\cap W)=2+2-3=\boxed{1}$.

**Bước 3 — xác định $U\cap W$:** giải $\alpha u_1+\beta u_2=s w_1+t w_2$.

Vế trái: $\alpha(1,0,0,1)+\beta(0,1,1,0)=(\alpha,\ \beta,\ \beta,\ \alpha)$.
Vế phải: $s(0,1,1,0)+t(-1,0,0,1)=(-t,\ s,\ s,\ t)$.

Cân bằng từng tọa độ:
$$\begin{cases}\alpha=-t\\ \beta=s\\ \beta=s\\ \alpha=t\end{cases}\Rightarrow\ \alpha=-t\ \text{và}\ \alpha=t\ (\text{từ }1,4)\ \Rightarrow\ 2\alpha=0\Rightarrow\alpha=0,\ t=0.$$
Còn lại $\beta=s$ **tự do** (2 phương trình tọa độ 2,3 trùng nhau, không ràng buộc thêm). Đặt $\beta=s=r$: $(\alpha,\beta,s,t)=(0,r,r,0)$.

$$v=\alpha u_1+\beta u_2=0+r\,u_2=r(0,1,1,0).$$
*(Kiểm vế $W$: $sw_1+tw_2=r\,w_1+0=r(0,1,1,0)$ — trùng ✓, đúng vì $u_2=w_1$; 1 tham số tự do ⇒ khớp Grassmann.)*
$$\boxed{U\cap W=\langle(0,1,1,0)\rangle.}$$

**Câu 2a.** $P=\begin{pmatrix}1&0&1\\1&1&0\\0&1&1\end{pmatrix}$, $\det P=2$, $P^{-1}=\tfrac12\begin{pmatrix}1&1&-1\\-1&1&1\\1&-1&1\end{pmatrix}$.
$$\boxed{f(x,y,z)=\Big(x+y,\ \tfrac{-x+3y+3z}{2},\ \tfrac{x+y+3z}{2}\Big).}$$
*(Kiểm $f(u_1){=}f(1,1,0){=}(2,1,1)$; và $1u_1{+}0u_2{+}1u_3{=}(1,1,0){+}(1,0,1){=}(2,1,1)$ ✓ khớp cột 1 $[f]_B=(1,0,1)$.)*

**Câu 2b.** $[u]_B=P^{-1}(3,2,1)=(2,0,1)$. $[f(u)]_B=[f]_B(2,0,1)^\top=(2,1,3)$.
$$\boxed{[f(u)]_B=(2,1,3).}$$
*(Kiểm: $f(3,2,1)=(5,3,4)$; $2u_1+u_2+3u_3=(2,2,0)+(0,1,1)+(3,0,3)=(5,3,4)$ ✓.)*

**Câu 2c.** Quy hệ $f(x,y,z)=0$ (nhân 2 để bỏ mẫu ở tọa độ 2,3) về ma trận hệ số:
$$\begin{pmatrix}1&1&0\\-1&3&3\\1&1&3\end{pmatrix}\xrightarrow{R_2+R_1,\ R_3-R_1}\begin{pmatrix}1&1&0\\0&4&3\\0&0&3\end{pmatrix}$$
Hạng $=3$ (đủ 3 pivot) $\Rightarrow \dim\operatorname{Ker}f=3-3=0$. *(Thế ngược: $R_3\Rightarrow z=0$; $R_2\Rightarrow y=0$; $R_1\Rightarrow x=0$.)*
$$\boxed{\operatorname{Ker}f=\{0\},\ \dim\operatorname{Ker}f=0,\quad \dim\operatorname{Im}f=3\ (f\text{ là song ánh}).}$$

**Câu 3a.** $P_A(\lambda)=\lambda^2-5\lambda+6=(\lambda-2)(\lambda-3)$. $E(2)=\langle(1,2)\rangle,\ E(3)=\langle(1,1)\rangle$.
$$\boxed{P=\begin{pmatrix}1&1\\2&1\end{pmatrix},\quad D=\begin{pmatrix}2&0\\0&3\end{pmatrix}.}$$

**Câu 3b.**
$$\boxed{A^n=\begin{pmatrix}2\cdot3^n-2^n & 2^n-3^n\\ 2\cdot3^n-2^{n+1} & 2^{n+1}-3^n\end{pmatrix}.}$$
*(Kiểm $n=1$: $\begin{psmallmatrix}6-2&2-3\\6-4&4-3\end{psmallmatrix}=A$ ✓.)*

**Câu 4.** Tam giác trên $\Rightarrow \lambda=2,-1,4$.
- $\lambda=2$: $(1,0,0)$.
- $\lambda=-1$: $(1,-3,0)$.
- $\lambda=4$: $(3,6,10)$.

$$\boxed{\lambda=2\to(1,0,0);\quad \lambda=-1\to(1,-3,0);\quad \lambda=4\to(3,6,10).}$$

---
---

# ĐỀ SỐ 5

## Đề

**Câu 1 (3,5đ).**
$$\begin{cases}2x_1-4x_2+5x_3+3x_4=0\\x_1-2x_2-x_3-x_4=0\\x_1-2x_2+6x_3+4x_4=0\end{cases}$$
a) Tìm cơ sở, số chiều không gian nghiệm $W$.
b) Cho $U=\langle u_1=(2,1,0,0),u_2=(4,2,0,0),u_3=(0,1,1,1)\rangle$. Tìm cơ sở $U+W$, suy ra $\dim(U\cap W)$, xác định $U\cap W$.

**Câu 2 (3đ).** $B=\{u_1=(1,1,0),u_2=(0,1,1),u_3=(1,0,1)\}$, $[f]_B=\begin{pmatrix}2&1&1\\1&2&1\\1&1&2\end{pmatrix}$.
a) Tìm $f(x,y,z)$. b) $u=(1,2,3)$: tìm $[f(u)]_B$. c) Cơ sở & $\dim\operatorname{Ker}f$, suy ra $\dim\operatorname{Im}f$.

**Câu 3 (2,5đ).** $A=\begin{pmatrix}6&-2\\3&1\end{pmatrix}$. a) Chéo hóa. b) Tìm $A^n$.

**Câu 4 (1đ).** Trị riêng, vectơ riêng của $A=\begin{pmatrix}1&1&1\\0&2&1\\0&0&3\end{pmatrix}$.

## Đáp án

**Câu 1a.** Đổi chỗ $R_1\leftrightarrow R_2$ để có pivot gọn, rồi khử Gauss:
$$\begin{pmatrix}2&-4&5&3\\1&-2&-1&-1\\1&-2&6&4\end{pmatrix}\xrightarrow{R_1\leftrightarrow R_2}\begin{pmatrix}1&-2&-1&-1\\2&-4&5&3\\1&-2&6&4\end{pmatrix}\xrightarrow{R_2-2R_1,\ R_3-R_1}\begin{pmatrix}1&-2&-1&-1\\0&0&7&5\\0&0&7&5\end{pmatrix}\xrightarrow{R_3-R_2}\begin{pmatrix}1&-2&-1&-1\\0&0&7&5\\0&0&0&0\end{pmatrix}$$
Hạng $r=2\Rightarrow\dim W=4-2=2$. Cột pivot 1,3; tự do $x_2=s,\ x_4=t$.
- $R_2$: $7x_3+5x_4=0\Rightarrow x_3=-\tfrac57x_4$. Để tránh phân số, đặt $x_4=7t\Rightarrow x_3=-5t$.
- $R_1$: $x_1-2x_2-x_3-x_4=0\Rightarrow x_1=2x_2+x_3+x_4=2s-5t+7t=2s+2t$.

$$\boxed{W=\langle(2,1,0,0),\ (2,0,-5,7)\rangle,\quad \dim W=2.}$$

**Câu 1b.**

**Bước 0 — $\dim U$:** $u_2=(4,2,0,0)=2u_1$ (thừa) $\Rightarrow\dim U=2$, cơ sở $\{u_1,u_3\}$. **Chú ý $u_1=(2,1,0,0)=w_1$**.

**Bước 1 — cơ sở & $\dim(U+W)$:** vì $u_1=w_1$, gộp $u_1(=w_1), u_3, w_2$:
$$\begin{pmatrix}2&1&0&0\\0&1&1&1\\2&0&-5&7\end{pmatrix}\xrightarrow{R_3-R_1}\begin{pmatrix}2&1&0&0\\0&1&1&1\\0&-1&-5&7\end{pmatrix}\xrightarrow{R_3+R_2}\begin{pmatrix}2&1&0&0\\0&1&1&1\\0&0&-4&8\end{pmatrix}$$
Hạng $=3$ ⇒
$$\boxed{\dim(U+W)=3,\quad \text{cơ sở }\{(2,1,0,0),(0,1,1,1),(0,0,-4,8)\}.}$$

**Bước 2 — Grassmann:** $\dim(U\cap W)=2+2-3=\boxed{1}$.

**Bước 3 — xác định $U\cap W$:** giải $\alpha u_1+\beta u_3=s w_1+t w_2$.

Vế trái: $\alpha(2,1,0,0)+\beta(0,1,1,1)=(2\alpha,\ \alpha+\beta,\ \beta,\ \beta)$.
Vế phải: $s(2,1,0,0)+t(2,0,-5,7)=(2s+2t,\ s,\ -5t,\ 7t)$.

Cân bằng từng tọa độ:
$$\begin{cases}2\alpha=2s+2t\\ \alpha+\beta=s\\ \beta=-5t\\ \beta=7t\end{cases}$$
Từ (3),(4): $-5t=7t\Rightarrow 12t=0\Rightarrow t=0$, kéo theo $\beta=0$. Từ (2): $\alpha=s$. Thế vào (1): $2s=2s+0$ (luôn đúng, không thêm ràng buộc) — vậy $s=\alpha$ **tự do**.

Đặt $\alpha=s=r$: $(\alpha,\beta,s,t)=(r,0,r,0)$.
$$v=\alpha u_1+\beta u_3=r\,u_1+0=r(2,1,0,0).$$
*(Kiểm vế $W$: $sw_1+tw_2=r\,w_1+0=r(2,1,0,0)$ — trùng ✓, đúng vì $u_1=w_1$; 1 tham số tự do ⇒ khớp Grassmann.)*
$$\boxed{U\cap W=\langle(2,1,0,0)\rangle.}$$

**Câu 2a.** $P=\begin{pmatrix}1&0&1\\1&1&0\\0&1&1\end{pmatrix}$, $P^{-1}=\tfrac12\begin{pmatrix}1&1&-1\\-1&1&1\\1&-1&1\end{pmatrix}$. $[f]_{B_0}=\begin{pmatrix}2&1&1\\1&2&1\\1&1&2\end{pmatrix}$ (trùng $[f]_B$, do tính đối xứng đặc biệt của $B,[f]_B$).
$$\boxed{f(x,y,z)=(2x+y+z,\ x+2y+z,\ x+y+2z).}$$
*(Kiểm $f(u_1)=f(1,1,0)=(3,3,2)$; $2u_1+u_2+u_3=(2,2,0)+(0,1,1)+(1,0,1)=(3,3,2)$ ✓.)*

**Câu 2b.** $[u]_B=P^{-1}(1,2,3)=(0,2,1)$. $[f(u)]_B=[f]_B(0,2,1)^\top=(3,5,4)$.
$$\boxed{[f(u)]_B=(3,5,4).}$$
*(Kiểm: $f(1,2,3)=(7,8,9)$; $3u_1+5u_2+4u_3=(3,3,0)+(0,5,5)+(4,0,4)=(7,8,9)$ ✓.)*

**Câu 2c.** Ma trận hệ số của $f(x,y,z)=0$ (ở đây $[f]_{B_0}=[f]_B$ do tính đối xứng):
$$\begin{pmatrix}2&1&1\\1&2&1\\1&1&2\end{pmatrix}\xrightarrow{R_1\leftrightarrow R_2}\begin{pmatrix}1&2&1\\2&1&1\\1&1&2\end{pmatrix}\xrightarrow{R_2-2R_1,\ R_3-R_1}\begin{pmatrix}1&2&1\\0&-3&-1\\0&-1&1\end{pmatrix}\xrightarrow{R_2\leftrightarrow R_3}\begin{pmatrix}1&2&1\\0&-1&1\\0&-3&-1\end{pmatrix}\xrightarrow{R_3-3R_2}\begin{pmatrix}1&2&1\\0&-1&1\\0&0&-4\end{pmatrix}$$
Hạng $=3$ (đủ 3 pivot) $\Rightarrow \dim\operatorname{Ker}f=3-3=0$.
$$\boxed{\operatorname{Ker}f=\{0\},\ \dim\operatorname{Ker}f=0,\quad \dim\operatorname{Im}f=3\ (f\text{ là đẳng cấu}).}$$

**Câu 3a.** $P_A(\lambda)=\lambda^2-7\lambda+12=(\lambda-3)(\lambda-4)$. $E(3)=\langle(2,3)\rangle,\ E(4)=\langle(1,1)\rangle$.
$$\boxed{P=\begin{pmatrix}2&1\\3&1\end{pmatrix},\quad D=\begin{pmatrix}3&0\\0&4\end{pmatrix}.}$$

**Câu 3b.**
$$\boxed{A^n=\begin{pmatrix}3\cdot4^n-2\cdot3^n & 2\cdot3^n-2\cdot4^n\\ 3\cdot4^n-3^{n+1} & 3^{n+1}-2\cdot4^n\end{pmatrix}.}$$
*(Kiểm $n=1$: $\begin{psmallmatrix}12-6&6-8\\12-9&9-8\end{psmallmatrix}=A$ ✓.)*

**Câu 4.** Tam giác trên $\Rightarrow \lambda=1,2,3$.
- $\lambda=1$: $(1,0,0)$.
- $\lambda=2$: $(1,1,0)$.
- $\lambda=3$: $(1,1,1)$.

$$\boxed{\lambda=1\to(1,0,0);\quad \lambda=2\to(1,1,0);\quad \lambda=3\to(1,1,1).}$$

---
---

# ĐỀ SỐ 6

## Đề

**Câu 1 (3,5đ).**
$$\begin{cases}x_1+2x_2-x_3+3x_4=0\\2x_1+4x_2-x_3+5x_4=0\\x_1+2x_2+2x_4=0\end{cases}$$
a) Tìm cơ sở, số chiều không gian nghiệm $W$.
b) Cho $U=\langle u_1=(1,-1,0,0),u_2=(1,0,-1,0),u_3=(1,0,0,-1)\rangle$. Tìm cơ sở $U+W$, suy ra $\dim(U\cap W)$, xác định $U\cap W$.

**Câu 2 (3đ).** $B=\{u_1=(1,2,1),u_2=(2,1,1),u_3=(1,1,2)\}$, $[f]_B=\begin{pmatrix}1&0&0\\0&2&0\\0&0&3\end{pmatrix}$.
a) Tìm $f(x,y,z)$. b) $u=(4,3,5)$: tìm $[f(u)]_B$. c) Cơ sở & $\dim\operatorname{Ker}f$, suy ra $\dim\operatorname{Im}f$.

**Câu 3 (2,5đ).** $A=\begin{pmatrix}1&-1\\2&4\end{pmatrix}$. a) Chéo hóa. b) Tìm $A^n$.

**Câu 4 (1đ).** Trị riêng, vectơ riêng của $A=\begin{pmatrix}2&1&0\\0&-1&3\\0&0&4\end{pmatrix}$ (giống ma trận Đề 4 — dùng để luyện lại nhanh, tự làm không xem đáp án Đề 4).

## Đáp án

*(Câu 1 chính là bài [[ĐSTT_Đề_Thi_Thử_Cuối_Kỳ]] Câu 1 — dùng để ôn lại, xem đáp án tại file đó: $W=\langle(-2,1,0,0),(-2,0,1,1)\rangle$, $\dim(U+W)=4$, $U\cap W=\langle(-2,0,1,1)\rangle$.)*

**Câu 2a.** $P=(u_1\,u_2\,u_3)=\begin{pmatrix}1&2&1\\2&1&1\\1&1&2\end{pmatrix}$, $\det P=-4$, $P^{-1}=\tfrac14\begin{pmatrix}-1&3&-1\\3&-1&-1\\-1&-1&3\end{pmatrix}$.
$$\boxed{f(x,y,z)=\Big(2x-y+z,\ \tfrac{x+y+5z}{4},\ \tfrac{-x-5y+15z}{4}\Big).}$$
*(Kiểm: cột 1 của $[f]_B$ là $(1,0,0)^\top \Rightarrow f(u_1)=1\cdot u_1=(1,2,1)$. Thay $u_1=(1,2,1)$: $f(1,2,1)=(2-2+1,\ \tfrac{1+2+5}{4},\ \tfrac{-1-10+15}{4})=(1,2,1)$ ✓ khớp.)*

**Câu 2b.** $[u]_B=P^{-1}(4,3,5)=(0,1,2)$. $[f(u)]_B=[f]_B(0,1,2)^\top=(0,2,6)$.
$$\boxed{[f(u)]_B=(0,2,6).}$$
*(Kiểm: $f(4,3,5)=(10,8,14)$; $2u_2+6u_3=2(2,1,1)+6(1,1,2)=(4,2,2)+(6,6,12)=(10,8,14)$ ✓ khớp.)*

**Câu 2c.** Quy hệ $f(x,y,z)=0$ (nhân 4 để bỏ mẫu ở tọa độ 2,3) về ma trận hệ số:
$$\begin{pmatrix}2&-1&1\\1&1&5\\-1&-5&15\end{pmatrix}\xrightarrow{R_1\leftrightarrow R_2}\begin{pmatrix}1&1&5\\2&-1&1\\-1&-5&15\end{pmatrix}\xrightarrow{R_2-2R_1,\ R_3+R_1}\begin{pmatrix}1&1&5\\0&-3&-9\\0&-4&20\end{pmatrix}\xrightarrow{R_2\div(-3)}\begin{pmatrix}1&1&5\\0&1&3\\0&-4&20\end{pmatrix}\xrightarrow{R_3+4R_2}\begin{pmatrix}1&1&5\\0&1&3\\0&0&32\end{pmatrix}$$
Hạng $=3$ (đủ 3 pivot) $\Rightarrow \dim\operatorname{Ker}f=3-3=0$.
$$\boxed{\operatorname{Ker}f=\{0\},\ \dim\operatorname{Ker}f=0,\quad \dim\operatorname{Im}f=3\ (f\text{ là song ánh}).}$$

**Câu 3a.** $P_A(\lambda)=\lambda^2-5\lambda+6=(\lambda-2)(\lambda-3)$. $E(2)=\langle(-1,1)\rangle,\ E(3)=\langle(-1,2)\rangle$.
$$\boxed{P=\begin{pmatrix}-1&-1\\1&2\end{pmatrix},\quad D=\begin{pmatrix}2&0\\0&3\end{pmatrix}.}$$
*(Đây là ví dụ mẫu trong slide Chương 5, xem [[ĐSTT_Chương5_Chéo_hóa]] §4 để đối chiếu công thức $A^n$ đầy đủ.)*

**Câu 3b.**
$$\boxed{A^n=\begin{pmatrix}2^{n+1}-3^n & 2^n-3^n\\ -2^{n+1}+2\cdot3^n & -2^n+2\cdot3^n\end{pmatrix}.}$$

**Câu 4.** *(Trùng ma trận Đề 4 — đáp án: $\lambda=2\to(1,0,0)$; $\lambda=-1\to(1,-3,0)$; $\lambda=4\to(3,6,10)$. Dùng để tự kiểm nếu ra khác thì dò lại quy trình.)*

---

> [!tip] Lưu ý khi tự luyện
> Mọi câu 2a trong 5 đề đều đã kiểm bằng cách thay $u_1$ (hoặc $u_i$) vào công thức $f$ vừa tìm, đối chiếu với cột tương ứng của $[f]_B$ — cách này (Mẹo 2 mở rộng) luôn nên làm sau khi tính xong công thức $f$ để tự bắt lỗi. Nếu tự làm ra công thức khác, dùng đúng phép kiểm này để dò xem sai ở bước nào.

