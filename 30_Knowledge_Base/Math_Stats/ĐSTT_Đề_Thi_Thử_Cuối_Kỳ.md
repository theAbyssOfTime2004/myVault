---
tags: [linear-algebra, exam, mock-exam, university]
aliases: [ĐSTT Đề Thi Thử, Mock Final LATT]
---

# Đại số tuyến tính – Đề thi thử cuối kỳ (4 câu / 10đ)

> Số liệu tự chế, đúng format đề thi cuối kỳ HCMUS. Liên quan: [[ĐSTT_Chương3_Không_gian_vectơ]], [[ĐSTT_Chương4_Ánh_xạ_tuyến_tính]], [[ĐSTT_Chương5_Chéo_hóa]], [[ĐSTT_Đề_Ôn_Chương3-4_Giải]].
> **Cách dùng:** che phần ĐÁP ÁN, tự làm trong ~75 phút, rồi đối chiếu.

---

# PHẦN I — ĐỀ

## Câu 1 (3,5đ)
Cho hệ phương trình tuyến tính thuần nhất 4 ẩn $x_1,x_2,x_3,x_4$:
$$\begin{cases} x_1 + 2x_2 - x_3 + 3x_4 = 0\\ 2x_1 + 4x_2 - x_3 + 5x_4 = 0\\ x_1 + 2x_2 \phantom{- x_3} + 2x_4 = 0\end{cases}$$
**a)** Tìm một cơ sở và số chiều của không gian nghiệm $W$ của hệ trên.
**b)** Cho $U=\langle u_1,u_2,u_3\rangle$ với $u_1=(1,-1,0,0),\ u_2=(1,0,-1,0),\ u_3=(1,0,0,-1)$. Tìm một cơ sở của $U+W$. Từ đó suy ra $\dim(U\cap W)$ và **xác định** $U\cap W$.

## Câu 2 (3đ)
Cho $B=\{u_1=(1,1,0),\ u_2=(0,1,1),\ u_3=(1,0,1)\}$ là một cơ sở của $\mathbb{R}^3$ và toán tử $f\in L(\mathbb{R}^3)$ có ma trận biểu diễn
$$[f]_B=\begin{pmatrix}1&0&1\\2&1&3\\1&1&2\end{pmatrix}.$$
**a)** Tìm công thức của $f(x,y,z)$.
**b)** Cho $u=(1,2,3)$. Tìm $[f(u)]_B$.
**c)** Tìm số chiều và một cơ sở của $\operatorname{Ker}f$. Từ đó suy ra $\dim\operatorname{Im}f$.

## Câu 3 (2,5đ)
Cho $A=\begin{pmatrix}1&2\\3&2\end{pmatrix}$.
**a)** Chéo hóa $A$.
**b)** Với mọi $n\in\mathbb{N}$, xác định $A^n$.

## Câu 4 (1đ)
Cho $A=\begin{pmatrix}1&2&2\\0&2&1\\0&0&3\end{pmatrix}$. Tìm tất cả các trị riêng và một vectơ riêng ứng với mỗi trị riêng.

---

# PHẦN II — ĐÁP ÁN

## Câu 1

### a) Cơ sở & số chiều của $W$
Khử Gauss ma trận hệ số (xếp dòng):
$$\begin{pmatrix}1&2&-1&3\\2&4&-1&5\\1&2&0&2\end{pmatrix}\xrightarrow{R_2-2R_1,\,R_3-R_1}\begin{pmatrix}1&2&-1&3\\0&0&1&-1\\0&0&1&-1\end{pmatrix}\xrightarrow{R_3-R_2}\begin{pmatrix}1&2&-1&3\\0&0&1&-1\\0&0&0&0\end{pmatrix}$$
Hạng $r=2$ ⇒ $\dim W = n-r = 4-2 = 2$. Ẩn cơ sở: $x_1,x_3$; ẩn tự do: $x_2=s,\ x_4=t$.
- $R_2$: $x_3 - x_4 = 0 \Rightarrow x_3 = t$.
- $R_1$: $x_1 = -2x_2 + x_3 - 3x_4 = -2s + t - 3t = -2s - 2t$.

Nghiệm tổng quát $(x_1,x_2,x_3,x_4)=s(-2,1,0,0)+t(-2,0,1,1)$.
$$\boxed{W=\langle w_1=(-2,1,0,0),\ w_2=(-2,0,1,1)\rangle,\quad \dim W=2.}$$

### b) Cơ sở $U+W$, $\dim(U\cap W)$ và $U\cap W$

**Số chiều $U$:** ma trận $(u_1;u_2;u_3)$ rõ ràng hạng $3$ (ba dòng ĐLTT) ⇒ $\dim U=3$.

**Cơ sở $U+W=\langle u_1,u_2,u_3,w_1,w_2\rangle$:** trước hết mô tả $U$ bằng phương trình. Cho $(a,b,c,d)\in U$:
$$\alpha u_1+\beta u_2+\gamma u_3=(\alpha+\beta+\gamma,\,-\alpha,\,-\beta,\,-\gamma)=(a,b,c,d)$$
⇒ $\alpha=-b,\beta=-c,\gamma=-d$ và $\alpha+\beta+\gamma=a$, tức $-(b+c+d)=a$. Vậy
$$U=\{x\in\mathbb{R}^4 \mid x_1+x_2+x_3+x_4=0\}\quad(\text{siêu phẳng, }\dim U=3).$$
Vì $w_1=(-2,1,0,0)$ có tổng tọa độ $=-1\neq 0$ nên $w_1\notin U$. Thêm một vectơ ngoài siêu phẳng vào $U$ phủ kín $\mathbb{R}^4$:
$$U+W \supseteq U+\langle w_1\rangle = \mathbb{R}^4 \Rightarrow \boxed{U+W=\mathbb{R}^4,\ \dim(U+W)=4,}$$
một cơ sở là cơ sở chính tắc $\{e_1,e_2,e_3,e_4\}$.

**Số chiều giao (Grassmann):**
$$\dim(U\cap W)=\dim U+\dim W-\dim(U+W)=3+2-4=\boxed{1}.$$

**Xác định $U\cap W$:** mỗi $v\in W$ có dạng $v=s w_1+t w_2=(-2s-2t,\ s,\ t,\ t)$. Khi đó $v\in U$
$$\iff x_1+x_2+x_3+x_4=0 \iff (-2s-2t)+s+t+t=0 \iff -s=0 \iff s=0.$$
Vậy $v=t\,w_2$, suy ra
$$\boxed{U\cap W=\langle (-2,0,1,1)\rangle.}$$

---

## Câu 2

Đặt $P=(B_0\to B)=\begin{pmatrix}1&0&1\\1&1&0\\0&1&1\end{pmatrix}$ (cột là $u_1,u_2,u_3$), $\det P=2$, và
$$P^{-1}=\tfrac{1}{2}\begin{pmatrix}1&1&-1\\-1&1&1\\1&-1&1\end{pmatrix}.$$

### a) Công thức $f$
$[f]_{B_0}=P\,[f]_B\,P^{-1}$. Tính $[f]_B P^{-1}=\begin{pmatrix}1&0&0\\2&0&1\\1&0&1\end{pmatrix}$, rồi
$$[f]_{B_0}=P\begin{pmatrix}1&0&0\\2&0&1\\1&0&1\end{pmatrix}=\begin{pmatrix}2&0&1\\3&0&1\\3&0&2\end{pmatrix}.$$
$$\boxed{f(x,y,z)=(2x+z,\ 3x+z,\ 3x+2z).}$$
*(Kiểm: $f(u_1)=f(1,1,0)=(2,3,3)=u_1+2u_2+u_3$ ⇒ cột 1 của $[f]_B$ là $(1,2,1)$ ✓.)*

### b) $[f(u)]_B$ với $u=(1,2,3)$
$[u]_B=P^{-1}u=(0,2,1)$ *(vì $2u_2+u_3=(1,2,3)$ ✓)*. Suy ra
$$[f(u)]_B=[f]_B[u]_B=\begin{pmatrix}1&0&1\\2&1&3\\1&1&2\end{pmatrix}\begin{pmatrix}0\\2\\1\end{pmatrix}=\boxed{\begin{pmatrix}1\\5\\4\end{pmatrix}.}$$
*(Kiểm: $f(1,2,3)=(5,6,9)$, và $1\cdot u_1+5u_2+4u_3=(5,6,9)$ ✓.)*

### c) $\operatorname{Ker}f$ và $\dim\operatorname{Im}f$
Giải $f(x,y,z)=0$: $\begin{cases}2x+z=0\\3x+z=0\\3x+2z=0\end{cases}\Rightarrow x=0,z=0,\ y$ tự do.
$$\boxed{\operatorname{Ker}f=\langle(0,1,0)\rangle,\ \dim\operatorname{Ker}f=1.}$$
Định lý số chiều: $\dim\operatorname{Im}f=\dim\mathbb{R}^3-\dim\operatorname{Ker}f=3-1=\boxed{2}.$

---

## Câu 3

### a) Chéo hóa $A=\begin{pmatrix}1&2\\3&2\end{pmatrix}$
$P_A(\lambda)=(1-\lambda)(2-\lambda)-6=\lambda^2-3\lambda-4=(\lambda-4)(\lambda+1)$ ⇒ trị riêng $\lambda_1=4,\lambda_2=-1$ (phân biệt ⇒ chéo hóa được).
- $E(4):\ (A-4I)X=0:\ -3x+2y=0\Rightarrow$ vectơ riêng $(2,3)$.
- $E(-1):\ (A+I)X=0:\ 2x+2y=0\Rightarrow$ vectơ riêng $(1,-1)$.
$$\boxed{P=\begin{pmatrix}2&1\\3&-1\end{pmatrix},\quad P^{-1}AP=D=\begin{pmatrix}4&0\\0&-1\end{pmatrix}.}$$

### b) $A^n$
$P^{-1}=\tfrac{1}{5}\begin{pmatrix}1&1\\3&-2\end{pmatrix}$, $D^n=\begin{pmatrix}4^n&0\\0&(-1)^n\end{pmatrix}$. Khi đó $A^n=PD^nP^{-1}$:
$$\boxed{A^n=\frac{1}{5}\begin{pmatrix}2\cdot4^n+3(-1)^n & 2\cdot4^n-2(-1)^n\\[2pt] 3\cdot4^n-3(-1)^n & 3\cdot4^n+2(-1)^n\end{pmatrix}.}$$
*(Kiểm $n=1$: $\tfrac15\begin{psmallmatrix}5&10\\15&10\end{psmallmatrix}=\begin{psmallmatrix}1&2\\3&2\end{psmallmatrix}=A$ ✓; $n=0$ ra $I$ ✓.)*

---

## Câu 4
$A=\begin{pmatrix}1&2&2\\0&2&1\\0&0&3\end{pmatrix}$ là ma trận **tam giác trên** ⇒ trị riêng là các phần tử đường chéo:
$$\boxed{\lambda_1=1,\ \lambda_2=2,\ \lambda_3=3.}$$
Vectơ riêng (giải $(A-\lambda I)X=0$):
- $\lambda=1$: $\begin{pmatrix}0&2&2\\0&1&1\\0&0&2\end{pmatrix}X=0\Rightarrow z=0,y=0$ ⇒ $\boxed{(1,0,0)}$.
- $\lambda=2$: $\begin{pmatrix}-1&2&2\\0&0&1\\0&0&1\end{pmatrix}X=0\Rightarrow z=0,\ x=2y$ ⇒ $\boxed{(2,1,0)}$.
- $\lambda=3$: $\begin{pmatrix}-2&2&2\\0&-1&1\\0&0&0\end{pmatrix}X=0\Rightarrow y=z,\ x=2z$ ⇒ $\boxed{(2,1,1)}$.

---

> [!summary] Map đề ↔ chương
> Câu 1 → [[ĐSTT_Chương3_Không_gian_vectơ]] (không gian nghiệm, $U+W$, Grassmann). Câu 2 → [[ĐSTT_Chương4_Ánh_xạ_tuyến_tính]] (đổi cơ sở, Ker/Im). Câu 3–4 → [[ĐSTT_Chương5_Chéo_hóa]] (chéo hóa, $A^n$, trị riêng).
