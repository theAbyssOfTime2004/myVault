---
tags: [linear-algebra, university, cheo-hoa, tri-rieng]
aliases: [ĐSTT Ch5, Chéo hóa ma trận, Trị riêng, Eigenvalue]
---

# Đại số tuyến tính – Chương 5: Chéo hóa ma trận

> Nguồn: Chuong 5_Cheo hoa ma tran.pdf (ĐH KHTN TP.HCM, LVL©2025). Liên quan: [[ĐSTT_Chương3_Không_gian_vectơ]], [[ĐSTT_Chương4_Ánh_xạ_tuyến_tính]], [[Linear Algebra Review]].

> [!abstract] Bản đồ chương — phủ **Câu 3 (2,5đ) + Câu 4 (1đ)** đề thi cuối kỳ
> **Bài toán gốc:** cho $A$ vuông, tìm $P$ khả nghịch để $P^{-1}AP$ là ma trận **đường chéo**. Sợi chỉ đỏ: **trị riêng → vectơ riêng → không gian riêng $E(\lambda)$ → kiểm điều kiện chéo hóa → lập $P$ từ các cơ sở $E(\lambda_i)$**. Ứng dụng chính: tính $A^n$, giải hệ truy hồi, Fibonacci.
> *Lưu ý: cả chương viết vectơ theo **dạng cột**.*

---

## 1. Trị riêng và vectơ riêng (Câu 4)

### 1.1. Định nghĩa

Cho $A\in M_n(\mathbb{R})$. Vectơ $v\in\mathbb{R}^n$ là **vectơ riêng** của $A$ nếu:
1. $v\neq 0$;
2. tồn tại $\lambda\in\mathbb{R}$ sao cho $\;Av=\lambda v.$

Khi đó $\lambda$ là **trị riêng**, $v$ là vectơ riêng **ứng với** $\lambda$.

> [!note] Nhận xét
> Nếu $v$ là vectơ riêng ứng với $\lambda$ thì $\mu v\ (\mu\neq 0)$ cũng vậy → vectơ riêng không duy nhất (cả một đường thẳng/không gian con).

> [!tip] Cách kiểm "v có là vectơ riêng?"
> Tính $Av$. Nếu $Av=\lambda v$ với một $\lambda$ nào đó → có (đọc luôn $\lambda$). Nếu $Av$ không tỉ lệ với $v$ → không.
> **VD.** $A=\begin{pmatrix}1&6\\5&2\end{pmatrix}$: $A\binom{6}{-5}=\binom{-24}{20}=-4\binom{6}{-5}$ ⇒ $v=(6,-5)$ là vtr ứng $\lambda=-4$. Còn $A\binom{3}{-2}=\binom{-9}{11}$ không tỉ lệ ⇒ không phải vtr.

### 1.2. Đa thức đặc trưng & phương trình đặc trưng

> [!important] Định nghĩa then chốt
> **Đa thức đặc trưng** của $A$: $\quad P_A(\lambda) := \det(A-\lambda I_n).$
> **Mệnh đề:** $\lambda$ là trị riêng của $A\iff P_A(\lambda)=0$ (phương trình đặc trưng).

- $P_A$ có bậc $n$, hệ số đầu $(-1)^n$.
- **VD.** $A=\begin{pmatrix}1&2\\-1&4\end{pmatrix}$: $P_A(\lambda)=\lambda^2-5\lambda+6=(\lambda-2)(\lambda-3)$ ⇒ trị riêng $\lambda_1=2,\lambda_2=3$.

---

## 1.3. Chứng minh thường gặp (Câu 4, 1đ — dạng mệnh đề ngắn)

> [!tip] Ý chính duy nhất cần nhớ
> Mọi chứng minh dưới đây chỉ là **nhân $A$ (hoặc $A^{-1}$) vào hai vế của $Av=\lambda v$** rồi biến đổi. Nắm vững thao tác gốc này là làm được hầu hết dạng bài.

**a) Nhân vô hướng vectơ riêng.** Nếu $v$ là vectơ riêng ứng $\lambda$ thì $\mu v\ (\mu\neq0)$ cũng là vectơ riêng ứng $\lambda$.
> [!note]- Vì sao đúng
> Vectơ riêng chỉ mang tính "hướng" — $A$ tác động lên $v$ bằng cách **kéo giãn theo cùng phương** hệ số $\lambda$. Nếu phóng to/thu nhỏ $v$ thành $\mu v$ (vẫn cùng phương), thì $A$ tác động lên nó cũng phải kéo giãn theo **đúng hệ số $\lambda$ đó** — vì phép nhân ma trận là tuyến tính, "nhân trước hay nhân sau" cho kết quả như nhau. Đây là lý do vectơ riêng **không bao giờ duy nhất** — luôn có cả một đường thẳng (hay không gian) các vectơ riêng cùng $\lambda$.
*Cm:* $A(\mu v)=\mu(Av)=\mu(\lambda v)=\lambda(\mu v)$, và $\mu v\neq0$. $\blacksquare$

**b) Trị riêng của $A^{-1}$.** Nếu $A$ khả nghịch và $\lambda$ là trị riêng của $A$ (vectơ riêng $v$) thì $\lambda\neq0$ và $\dfrac1\lambda$ là trị riêng của $A^{-1}$ (cùng vectơ riêng $v$).
> [!note]- Vì sao đúng
> **Ý 1 ($\lambda\neq0$):** nếu $\lambda=0$ thì $A$ "nuốt" hẳn một vectơ khác $0$ về $0$ ($Av=0$) — nghĩa là $A$ không thể "hoàn tác" được (không đơn ánh), nên không thể khả nghịch. Mà đề cho $A$ khả nghịch $\Rightarrow$ mâu thuẫn $\Rightarrow \lambda\neq0$.
> **Ý 2 ($1/\lambda$):** nếu $A$ kéo giãn $v$ theo hệ số $\lambda$, thì phép ngược $A^{-1}$ phải "kéo giãn ngược lại" theo hệ số $1/\lambda$ để trả $v$ về chỗ cũ — đúng trực giác "nghịch đảo của phóng to là thu nhỏ".
*Cm:* Nếu $\lambda=0$ thì $Av=0,\ v\neq0\Rightarrow A$ không đơn ánh, mâu thuẫn khả nghịch $\Rightarrow\lambda\neq0$. Từ $Av=\lambda v$, nhân $A^{-1}$: $v=\lambda A^{-1}v\Rightarrow A^{-1}v=\dfrac1\lambda v$. $\blacksquare$

**c) Vectơ riêng của 2 trị riêng khác nhau thì độc lập.** Nếu $v_1,v_2$ ứng $\lambda_1\neq\lambda_2$ thì $\{v_1,v_2\}$ ĐLTT.
> [!note]- Vì sao đúng
> $v_1,v_2$ bị $A$ "kéo giãn theo hai tốc độ khác nhau" ($\lambda_1\neq\lambda_2$). Nếu chúng phụ thuộc (cùng phương hoặc một cái là tổ hợp của cái kia), thì áp $A$ vào tổ hợp đó phải cho **cùng một kiểu kéo giãn** cho cả hai — nhưng $\lambda_1\neq\lambda_2$ khiến điều đó không thể xảy ra trừ khi hệ số bằng $0$. Mẹo chứng minh: "nhân $A$ vào một tổ hợp $=0$" tạo ra **hai phương trình khác nhau** (vì mỗi $v_i$ bị nhân với $\lambda_i$ riêng), trừ đi để cô lập từng hệ số.
*Cm:* Giả sử $av_1+bv_2=0$ (*). Nhân $A$: $a\lambda_1v_1+b\lambda_2v_2=0$ (**). Lấy (**) $-\lambda_2\times$(*): $a(\lambda_1-\lambda_2)v_1=0\Rightarrow a=0$ (vì $\lambda_1\neq\lambda_2,v_1\neq0$). Thay vào (*): $b=0$. $\blacksquare$

**d) Trị riêng $0$ $\iff$ không khả nghịch.** $A$ có trị riêng $0$ $\iff \det A=0$.
> [!note]- Vì sao đúng
> Đây thực chất chỉ là **nối 2 định nghĩa đã học lại với nhau**, không có gì mới: "$0$ là trị riêng" nghĩa là có $v\neq0$ với $Av=0v=0$ — tức hệ thuần nhất $AX=0$ có **nghiệm khác 0**. Mà từ Chương 1–2, hệ thuần nhất có nghiệm khác 0 $\iff \det A=0$ (ma trận không khả nghịch). Vậy hai mệnh đề tương đương chỉ vì chúng **cùng diễn tả một điều** theo hai ngôn ngữ khác nhau (trị riêng vs định thức).
*Cm:* $0$ là trị riêng $\iff\exists v\neq0: Av=0\iff$ hệ $AX=0$ có nghiệm không tầm thường $\iff\det A=0$. $\blacksquare$

**e) Trị riêng của $A^k$.** Nếu $\lambda$ là trị riêng của $A$ (vectơ riêng $v$) thì $\lambda^k$ là trị riêng của $A^k$ ($k\in\mathbb{N}^*$), cùng vectơ riêng $v$.
> [!note]- Vì sao đúng
> Mỗi lần áp $A$ vào $v$, nó bị kéo giãn thêm một lần hệ số $\lambda$ — áp $A$ liên tiếp $k$ lần thì kéo giãn dồn lại thành $\lambda\times\lambda\times\cdots\times\lambda=\lambda^k$ ($k$ lần), còn **hướng** ($v$) không đổi vì mỗi bước chỉ scale, không xoay. Quy nạp chỉ là cách viết hình thức cho "làm lại đúng một thao tác $k$ lần".
*Cm (quy nạp):* $k=1$ đúng theo giả thiết. Giả sử $A^kv=\lambda^kv$, khi đó $A^{k+1}v=A(\lambda^kv)=\lambda^k(Av)=\lambda^{k+1}v$. $\blacksquare$

**f) Ma trận tam giác.** Nếu $A$ tam giác (trên/dưới) thì trị riêng $=$ các phần tử đường chéo chính.
> [!note]- Vì sao đúng
> Định thức của ma trận tam giác **luôn** bằng tích các phần tử đường chéo (đã học ở Chương 2) — không cần khai triển phức tạp. Vì $A-\lambda I$ cũng là ma trận tam giác (chỉ trừ $\lambda$ vào đường chéo, không đổi dạng tam giác), nên $\det(A-\lambda I)$ vẫn là tích các phần tử đường chéo của $A-\lambda I$, tức $\prod_i(a_{ii}-\lambda)$. Đa thức này bằng $0$ chính xác khi **một trong các nhân tử** $=0$, tức $\lambda=a_{ii}$ với $i$ nào đó.
*Cm:* $A-\lambda I$ cùng dạng tam giác $\Rightarrow \det(A-\lambda I)=\prod_i(a_{ii}-\lambda)$ (định thức tam giác = tích đường chéo) $\Rightarrow P_A(\lambda)=0\iff\lambda=a_{ii}$. $\blacksquare$ *(đây là mẹo đọc trị riêng trực tiếp đã dùng nhiều ở Câu 4 các đề mẫu.)*

**g) Trị riêng của $A-sI$ (dịch chuyển).** Nếu $\lambda$ là trị riêng của $A$ (vectơ riêng $v$), $s\in\mathbb{R}$, thì $\lambda-s$ là trị riêng của $A-sI$, cùng vectơ riêng $v$.
> [!note]- Vì sao đúng
> $sI$ chỉ đơn giản là "kéo giãn đều mọi hướng theo hệ số $s$" (ma trận vô hướng), nên nó **không làm đổi hướng** $v$ — chỉ trừ bớt $s$ khỏi mức độ kéo giãn ban đầu ($\lambda$) của $A$. Đây chính là "mẹo dịch chuyển" đứng sau công thức $E(\lambda)=\ker(A-\lambda I)$: bản chất $(A-\lambda I)v=0$ nghĩa là $\lambda$ (dịch $s=\lambda$) làm $A-\lambda I$ "triệt tiêu" $v$ — khớp với mệnh đề này khi $s=\lambda$.
*Cm:* $(A-sI)v=Av-sv=\lambda v-sv=(\lambda-s)v$, $v\neq0$. $\blacksquare$

**h) Trị riêng của $sA$ (nhân vô hướng ma trận).** Nếu $\lambda$ là trị riêng của $A$ (vectơ riêng $v$), $s\in\mathbb{R}$, thì $s\lambda$ là trị riêng của $sA$, cùng vectơ riêng $v$.
> [!note]- Vì sao đúng
> Nhân cả ma trận $A$ với $s$ nghĩa là "kéo giãn thêm $s$ lần" lên **mọi** tác động của $A$ — nên mức độ kéo giãn theo hướng $v$ (vốn là $\lambda$) cũng bị nhân thêm $s$, thành $s\lambda$. Đây là mệnh đề **dễ nhất** trong nhóm này — gần như chỉ là đưa số $s$ ra ngoài phép nhân ma trận.
*Cm:* $(sA)v=s(Av)=s(\lambda v)=(s\lambda)v$. $\blacksquare$

**i) Giao hai không gian riêng phân biệt $=\{0\}$.** Nếu $\lambda_1\neq\lambda_2$ thì $E(\lambda_1)\cap E(\lambda_2)=\{0\}$.
> [!note]- Vì sao đúng
> Một vectơ $v\neq0$ nằm trong cả $E(\lambda_1)$ lẫn $E(\lambda_2)$ nghĩa là $A$ **vừa** kéo giãn nó theo hệ số $\lambda_1$ **vừa** theo hệ số $\lambda_2$ cùng lúc — vô lý vì $Av$ chỉ có **một** giá trị duy nhất. Buộc phải có $\lambda_1=\lambda_2$ (trái giả thiết) hoặc $v=0$. Đây thực chất là **cùng một ý tưởng** với mệnh đề (c) (vectơ riêng khác trị riêng thì ĐLTT) — chỉ diễn đạt lại dưới ngôn ngữ "giao hai không gian con".
*Cm:* Giả sử $v\in E(\lambda_1)\cap E(\lambda_2),\ v\neq0$. Khi đó $Av=\lambda_1v$ và $Av=\lambda_2v\Rightarrow(\lambda_1-\lambda_2)v=0$. Vì $\lambda_1\neq\lambda_2\Rightarrow v=0$, mâu thuẫn. Vậy $E(\lambda_1)\cap E(\lambda_2)=\{0\}$. $\blacksquare$

---

## 2. Không gian riêng $E(\lambda)$

> [!important] Định nghĩa
> Nếu $\lambda$ là trị riêng thì
> $$E(\lambda) := \{v\in\mathbb{R}^n \mid Av=\lambda v\}$$
> là **không gian con** của $\mathbb{R}^n$, gọi là **không gian riêng** ứng với $\lambda$.
> **Mấu chốt tính toán:** $E(\lambda)$ chính là **không gian nghiệm** của hệ thuần nhất $\;(A-\lambda I_n)X=0.$

→ Tìm cơ sở & $\dim E(\lambda)$ = giải hệ $(A-\lambda I)X=0$ rồi đọc nghiệm cơ bản (đúng quy trình [[ĐSTT_Chương3_Không_gian_vectơ|Ch3 §5]]). Nhắc lại: $\dim E(\lambda)=n-r(A-\lambda I)$.

> [!important] Mệnh đề chặn số chiều (cực kỳ quan trọng cho chéo hóa)
> Nếu $\lambda$ là trị riêng **bội $m$** (bội đại số, tức bội nghiệm của $P_A$) thì
> $$1\le \dim E(\lambda) \le m.$$
> ($\dim E(\lambda)$ = bội **hình học**.)

---

## 3. Ma trận chéo hóa được (Câu 3a)

> [!important] Định nghĩa
> $A\in M_n(\mathbb{R})$ **chéo hóa được** nếu tồn tại $P$ khả nghịch sao cho $P^{-1}AP$ là ma trận đường chéo.

> [!important] Định lý điều kiện chéo hóa (PHẢI THUỘC)
> $A$ chéo hóa được $\iff$ thỏa **cả hai**:
> 1. $P_A(\lambda)$ **phân rã trên $\mathbb{R}$**: $P_A(\lambda)=(-1)^n(\lambda-\lambda_1)^{m_1}\cdots(\lambda-\lambda_p)^{m_p}$ với $\lambda_i\in\mathbb{R}$, $\sum m_i=n$ (đủ nghiệm thực kể bội).
> 2. $\forall i:\ \dim E(\lambda_i)=m_i$ (bội hình học = bội đại số với **mọi** trị riêng).

> [!tip] Hệ quả loại nhanh
> Nếu $A$ có **đúng $n$ trị riêng phân biệt** thì $A$ chéo hóa được ngay (khỏi kiểm dim, vì mỗi $m_i=1$).

> [!summary] Thuật toán chéo hóa (3 bước)
> **B1.** Tìm $P_A(\lambda)=\det(A-\lambda I)$. Nếu **không phân rã** trên $\mathbb{R}$ → **không** chéo hóa được, dừng.
> **B2.** Tìm các trị riêng $\lambda_i$ và bội $m_i$. Với mỗi $i$ tính $\dim E(\lambda_i)$. Nếu có $\dim E(\lambda_i)<m_i$ → **không** chéo hóa được, dừng.
> **B3.** Với mỗi $i$ tìm cơ sở $\mathcal{B}_i$ của $E(\lambda_i)$. Xếp tất cả vectơ làm **cột** của $P$. Khi đó
> $$P^{-1}AP=\operatorname{diag}(\underbrace{\lambda_1,\dots,\lambda_1}_{m_1},\dots,\underbrace{\lambda_p,\dots,\lambda_p}_{m_p}).$$
> *(Thứ tự trị riêng trên đường chéo khớp thứ tự cột vectơ riêng trong $P$.)*

> [!warning] Hai kiểu "KHÔNG chéo hóa được" hay gặp
> - **Không phân rã:** $P_A=-(\lambda-4)(\lambda^2+4)$ — $\lambda^2+4$ vô nghiệm thực ⇒ không chéo hóa được (trên $\mathbb{R}$).
> - **Thiếu vectơ riêng:** $P_A=-(\lambda-1)^2(\lambda-2)$ nhưng $\dim E(1)=1<2$ ⇒ không chéo hóa được.

---

## 4. Ứng dụng: tính $A^n$ (Câu 3b)

> [!important] Công thức
> $A$ chéo hóa được, $P^{-1}AP=D=\operatorname{diag}(\lambda_1,\dots,\lambda_n)$ ⇒ $A=PDP^{-1}$, do đó
> $$\boxed{A^n=PD^nP^{-1},\qquad D^n=\operatorname{diag}(\lambda_1^n,\dots,\lambda_n^n).}$$

> [!tip] Quy trình Câu 3b
> 1. Chéo hóa được $P, D$ (từ câu a). 2. Viết $D^n$. 3. Tính $P^{-1}$. 4. Nhân $P\,D^n\,P^{-1}$. 5. **Kiểm tra nhanh tại $n=1$** phải ra lại $A$ (và $n=0$ ra $I$).

**VD (cấp 2).** $A=\begin{pmatrix}1&-1\\2&4\end{pmatrix}$: $P_A=(\lambda-2)(\lambda-3)$; $E(2)=\langle(-1,1)\rangle$, $E(3)=\langle(-1,2)\rangle$.
$P=\begin{pmatrix}-1&-1\\1&2\end{pmatrix},\ D=\begin{pmatrix}2&0\\0&3\end{pmatrix},\ P^{-1}=\begin{pmatrix}-2&-1\\1&1\end{pmatrix}$ ⇒
$$A^n=\begin{pmatrix}2^{n+1}-3^n & 2^n-3^n\\ -2^{n+1}+2\cdot 3^n & -2^n+2\cdot 3^n\end{pmatrix}.$$

**Các ứng dụng khác:** hệ truy hồi $X_{n+1}=AX_n\Rightarrow X_n=A^nX_0$; **Fibonacci** với $A=\begin{pmatrix}1&1\\1&0\end{pmatrix}$ cho công thức Binet $F_k=\frac{1}{\sqrt5}\big[(\tfrac{1+\sqrt5}{2})^k-(\tfrac{1-\sqrt5}{2})^k\big]$, tỉ số $F_{k+1}/F_k\to\frac{1+\sqrt5}{2}\approx1{,}618$ (tỉ lệ vàng).

---

## 5. Ví dụ "tự làm" trong slide — đã giải

### VD A (slide 20) — Chéo hóa $A=\begin{pmatrix}1&-4&-4\\8&-11&-8\\-8&8&5\end{pmatrix}$

**B1. Đa thức đặc trưng.** Khai triển $\det(A-\lambda I)$:
$$P_A(\lambda)=(1-\lambda)(\lambda+3)^2 = -(\lambda-1)(\lambda+3)^2.$$
*(Kiểm: vết $=1-11+5=-5=1+(-3)+(-3)$ ✓; $\det A=9=1\cdot(-3)^2$ ✓.)*

**B2. Trị riêng:** $\lambda_1=1$ (bội 1), $\lambda_2=-3$ (bội 2). Phân rã ✓.

- $E(1):\ (A-I)X=0\Rightarrow$ nghiệm $t(-1,-2,2)$. $\dim E(1)=1=m_1$ ✓.
- $E(-3):\ (A+3I)X=0$, mọi dòng tỉ lệ $[1,-1,-1]$ ⇒ $x_1=x_2+x_3$, nghiệm $\langle(1,1,0),(1,0,1)\rangle$. $\dim E(-3)=2=m_2$ ✓.

Cả hai bằng bội ⇒ **$A$ chéo hóa được**.

**B3.**
$$P=\begin{pmatrix}-1&1&1\\-2&1&0\\2&0&1\end{pmatrix},\qquad P^{-1}AP=\operatorname{diag}(1,-3,-3).$$

### VD B (slide 23) — Tìm $A^n$ với $A=\begin{pmatrix}2&-1&-2\\0&5&6\\0&-1&0\end{pmatrix}$

**Đa thức đặc trưng** (khai triển theo cột 1, vì cột 1 $=(2,0,0)$):
$$P_A(\lambda)=(2-\lambda)\big[(5-\lambda)(-\lambda)+6\big]=(2-\lambda)(\lambda-2)(\lambda-3)=-(\lambda-2)^2(\lambda-3).$$

**Trị riêng:** $\lambda=2$ (bội 2), $\lambda=3$ (bội 1).
- $E(2):\ (A-2I)X=0$, hệ rút về $x_2+2x_3=0$ ⇒ $\langle(1,0,0),(0,-2,1)\rangle$, $\dim=2=m$ ✓.
- $E(3):\ \langle(1,-3,1)\rangle$, $\dim=1$ ✓. ⇒ **chéo hóa được**.

$$P=\begin{pmatrix}1&0&1\\0&-2&-3\\0&1&1\end{pmatrix},\quad D=\operatorname{diag}(2,2,3),\quad P^{-1}=\begin{pmatrix}1&1&2\\0&1&3\\0&-1&-2\end{pmatrix}.$$

$A^n=P\,\operatorname{diag}(2^n,2^n,3^n)\,P^{-1}$:
$$\boxed{A^n=\begin{pmatrix}2^n & 2^n-3^n & 2^{n+1}-2\cdot 3^n\\[2pt] 0 & 3^{n+1}-2^{n+1} & 2\cdot 3^{n+1}-3\cdot 2^{n+1}\\[2pt] 0 & 2^n-3^n & 3\cdot 2^n-2\cdot 3^n\end{pmatrix}}$$
*(Kiểm $n=1$ ra đúng $A$, $n=0$ ra $I_3$ ✓.)*

---

## 6. Tổng kết — Bản đồ ôn nhanh (Câu 3 & 4)

| Hỏi gì | Công cụ |
|---|---|
| $v$ có là vectơ riêng? | Tính $Av$, xem có $=\lambda v$ |
| Tìm trị riêng | Giải $P_A(\lambda)=\det(A-\lambda I)=0$ |
| Cơ sở $E(\lambda)$ | Giải hệ thuần nhất $(A-\lambda I)X=0$ → nghiệm cơ bản |
| $A$ có chéo hóa được? | (1) $P_A$ phân rã trên $\mathbb{R}$; (2) $\dim E(\lambda_i)=m_i\ \forall i$ |
| Loại nhanh "được" | Có đủ $n$ trị riêng phân biệt |
| Lập $P, D$ | Cột $P$ = vectơ cơ sở các $E(\lambda_i)$; $D=\operatorname{diag}(\lambda_i)$ cùng thứ tự |
| Tính $A^n$ | $A^n=PD^nP^{-1}$, $D^n=\operatorname{diag}(\lambda_i^n)$ |

> [!note] Công thức/điều kiện phải thuộc
> - $P_A(\lambda)=\det(A-\lambda I)$; trị riêng $\iff P_A=0$.
> - $E(\lambda)=\ker(A-\lambda I)$, $\dim E(\lambda)=n-r(A-\lambda I)$, và $1\le\dim E(\lambda)\le$ bội.
> - Chéo hóa được $\iff$ phân rã **và** mọi bội hình học = bội đại số.
> - $A^n=PD^nP^{-1}$.

> [!warning] Bẫy thường gặp
> - $P_A$ còn nhân tử bậc 2 vô nghiệm thực ($\lambda^2+c,\ c>0$) ⇒ **không** chéo hóa được trên $\mathbb{R}$.
> - Trị riêng bội $\ge 2$ **phải** kiểm $\dim E(\lambda)$ — đừng kết luận "được" vội.
> - $P$ xếp vectơ riêng theo **cột**; thứ tự cột và thứ tự $\lambda$ trên $D$ phải khớp.
> - Tính $A^n$ xong nhớ **thử $n=1$** để bắt lỗi số học.

---
*Ghi chú ôn thi tự động hóa từ slide Chương 5 (28 trang). Đề thi cuối kỳ: xem map tại [[ĐSTT_Đề_Ôn_Chương3-4_Giải]] (Câu 1–2) và chương này (Câu 3–4).*
