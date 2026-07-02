---
tags: [linear-algebra, university, khong-gian-vecto]
aliases: [ĐSTT Ch3, Không gian vectơ, Vector Space]
---

# Đại số tuyến tính – Chương 3: Không gian vectơ

> Nguồn: Chuong 3_Khong gian vecto.pdf (ĐH KHTN TP.HCM). Liên quan: [[ĐSTT_Chương3_Bài_Tập]], [[ĐSTT_Chương4_Ánh_xạ_tuyến_tính]], [[Linear Algebra Review]].

> [!abstract] Bản đồ chương
> Chương này xây dựng khái niệm **không gian vectơ** (KGVT) từ các tiên đề, rồi phát triển bộ công cụ để "đo" và "mô tả" một không gian: **tổ hợp tuyến tính → độc lập/phụ thuộc → tập sinh → cơ sở → số chiều**. Phần sau áp dụng vào **không gian con**, **không gian nghiệm** của hệ thuần nhất, và cuối cùng là **tọa độ & ma trận chuyển cơ sở**. Sợi chỉ đỏ xuyên suốt: **mọi câu hỏi đều quy về giải một hệ phương trình tuyến tính rồi đọc hạng $r(A)$**.

---

## 1. Không gian vectơ

### 1.1. Định nghĩa (8 tiên đề)

Cho tập $V$ với phép cộng $+$ và phép nhân vô hướng $\cdot$ của $\mathbb{R}$ với $V$. $V$ là **không gian vectơ trên $\mathbb{R}$** nếu $\forall u,v,w \in V$ và $\forall \alpha,\beta \in \mathbb{R}$ thỏa 8 tính chất:

| # | Tính chất | Ý nghĩa |
|---|---|---|
| 1 | $u+v = v+u$ | Cộng giao hoán |
| 2 | $(u+v)+w = u+(v+w)$ | Cộng kết hợp |
| 3 | $\exists\, 0 \in V: u+0 = u$ | Có vectơ **không** |
| 4 | $\exists\, u' \in V: u'+u = 0$ | Có vectơ **đối** |
| 5 | $(\alpha\beta)u = \alpha(\beta u)$ | Nhân vô hướng kết hợp |
| 6 | $(\alpha+\beta)u = \alpha u + \beta u$ | Phân phối theo vô hướng |
| 7 | $\alpha(u+v) = \alpha u + \alpha v$ | Phân phối theo vectơ |
| 8 | $1\cdot u = u$ | Đơn vị vô hướng |

Khi đó: mỗi $u\in V$ là một **vectơ**; $0$ là **vectơ không**; $u'$ là **vectơ đối** của $u$.

### 1.2. Các ví dụ kinh điển về KGVT

- $\mathbb{R}^n = \{(x_1,\dots,x_n)\mid x_i\in\mathbb{R}\}$ với cộng và nhân vô hướng theo từng tọa độ. Vectơ không $0=(0,\dots,0)$, đối của $u$ là $-u$.
- $M_{m\times n}(\mathbb{R})$ — ma trận, với cộng ma trận và nhân số. Vectơ không = ma trận không.
- $\mathbb{R}[x]$ — đa thức hệ số thực (bậc tùy ý); và $\mathbb{R}_n[x]$ — đa thức **bậc $\le n$**.
- Ví dụ "lạ" (tự làm): $V=(0,+\infty)$ với $u\oplus v = uv$ và $\alpha\odot u = u^\alpha$ vẫn là KGVT trên $\mathbb{R}$ → **bản chất KGVT nằm ở 8 tiên đề, không nằm ở ký hiệu phép toán.**

> [!warning] Mẹo loại nhanh — kiểm tra vectơ $0$
> Tập định bởi một **phương trình thuần nhất** thì là KGVT:
> $V=\{(x_1,x_2,x_3)\mid 2x_1+3x_2+x_3=0\}$ ✅
> Tập định bởi phương trình có **hằng số tự do** thì **không** là KGVT vì $0\notin W$:
> $W=\{x_1+x_2-2x_3=1\}$ ❌ (do $0=(0,0,0)\notin W$).

### 1.3. Mệnh đề cơ bản

Với mọi $u\in V,\ \alpha\in\mathbb{R}$:
1. $\alpha u = 0 \iff (\alpha=0 \text{ hoặc } u=0)$.
2. $(-1)u = u'$ → vì vậy ký hiệu $-u$ thay cho vectơ đối $u'$.

---

## 2. Tổ hợp tuyến tính

### 2.1. Định nghĩa

Một **tổ hợp tuyến tính** (THTT) của $u_1,\dots,u_m \in V$ là vectơ

$$u = \alpha_1 u_1 + \alpha_2 u_2 + \cdots + \alpha_m u_m, \qquad \alpha_i \in \mathbb{R}.$$

Đẳng thức này gọi là **dạng biểu diễn** của $u$. *Lưu ý:* vectơ $0$ **luôn** là THTT (lấy mọi $\alpha_i=0$).

### 2.2. Phương pháp kiểm tra "u có là THTT của $u_1,\dots,u_m$?"

$u$ là THTT $\iff$ phương trình $u = \alpha_1 u_1 + \cdots + \alpha_m u_m$ **có nghiệm**.

> [!tip] Thuật toán trong $\mathbb{R}^n$ (xếp **cột**)
> **Bước 1.** Lập ma trận mở rộng $\big(u_1^\top\ u_2^\top\ \dots\ u_m^\top \mid u^\top\big)$ (mỗi vectơ là một cột).
> **Bước 2.** Giải hệ bằng khử Gauss:
> - **Vô nghiệm** → $u$ **không** là THTT.
> - **Có nghiệm** $(\alpha_1,\dots,\alpha_m)$ → $u$ là THTT, đọc luôn dạng biểu diễn.

**Ví dụ.** $u=(-3,1,4)$ với $u_1=(1,2,1), u_2=(-1,-1,1), u_3=(-2,1,1)$ → nghiệm duy nhất $(1,2,1)$, nên $u=u_1+2u_2+u_3$.

**Ví dụ (vô nghiệm).** $u=(4,3,5)$ với $u_1=(1,2,5),u_2=(1,3,7),u_3=(-2,3,4)$ → dòng cuối $0=−5$ ⇒ **không** là THTT.

**Ví dụ (vô số nghiệm).** Đổi tọa độ cuối của $u$ thành $(4,3,10)$ → nghiệm $(\alpha_1,\alpha_2,\alpha_3)=(9+9t,-5-7t,t)$ ⇒ vẫn là THTT, biểu diễn không duy nhất.

**Dạng "tìm điều kiện".** Để $u=(a,b,c,d)$ là THTT của một họ, ép hệ có nghiệm → ràng buộc trên $a,b,c,d$ (ví dụ $a-b-c+d=0$). Đây chính là cách mô tả không gian sinh ở mục 4.

### 2.3. Độc lập & phụ thuộc tuyến tính

Xét phương trình thuần nhất $\;\alpha_1 u_1 + \cdots + \alpha_m u_m = 0\;$ $(\star)$:

- Chỉ có **nghiệm tầm thường** ($\alpha_i=0$ hết) → $\{u_i\}$ **độc lập tuyến tính (ĐLTT)**.
- Có **nghiệm không tầm thường** (vô số nghiệm) → **phụ thuộc tuyến tính (PTTT)**.

> [!note] Hiểu bản chất
> $\{u_i\}$ **PTTT** $\iff$ **tồn tại một vectơ là THTT của các vectơ còn lại**. (Phụ thuộc = có vectơ "thừa", suy ra được từ các vectơ kia.)

**Liên hệ hạng (Kronecker–Capelli) cho hệ thuần nhất $AX=0$ với $m$ ẩn:**
- $r(A)=m$ → chỉ nghiệm tầm thường → **ĐLTT**.
- $r(A)<m$ → vô số nghiệm → **PTTT**.

> [!tip] Thuật toán kiểm tra ĐLTT trong $\mathbb{R}^n$
> Xếp $u_1,\dots,u_m$ thành **dòng hoặc cột** của ma trận $A$, tính hạng:
> - $r(A)=m$ → **ĐLTT**.
> - $r(A)<m$ → **PTTT**.
>
> **Khi $m=n$ (ma trận vuông):** dùng định thức cho nhanh — $\det A\neq 0 \Rightarrow$ ĐLTT; $\det A = 0 \Rightarrow$ PTTT.

**Ví dụ tìm biểu diễn khi PTTT.** $u_1,u_2,u_3,u_4\in\mathbb{R}^4$ cho $r(A)=3<4$, nghiệm $(-t,-t,-t,t)$. Chọn $t=-1$: $u_1+u_2+u_3-u_4=0 \Rightarrow u_4=u_1+u_2+u_3$.

**Ví dụ tham số.** Với họ phụ thuộc $m$, thường $\det A = m(m-1)(m+1)$ → ĐLTT $\iff m\neq 0, \pm 1$.

> [!info] Mệnh đề kế thừa
> - $S$ PTTT ⇒ **mọi tập chứa $S$** đều PTTT.
> - $S$ ĐLTT ⇒ **mọi tập con của $S$** đều ĐLTT.

---

## 3. Cơ sở và số chiều

### 3.1. Tập sinh

$S\subseteq V$ là **tập sinh** của $V$ nếu **mọi** vectơ của $V$ đều là THTT của $S$. Ký hiệu $V=\langle S\rangle$.

**Kiểm tra:** $S=\{u_i\}$ sinh $\mathbb{R}^n$ $\iff$ hệ $\big(u_1^\top\dots u_m^\top\mid u^\top\big)$ có nghiệm với **mọi** $u=(x,y,z,\dots)$. Nếu xuất hiện dòng kiểu $0 = (\text{biểu thức của } x,y,z)$ ≠ 0 cho một $u_0$ nào đó → $S$ **không** sinh.

### 3.2. Cơ sở & số chiều

> [!important] Định nghĩa then chốt
> $B\subseteq V$ là **cơ sở** của $V$ nếu **(i)** $B$ là tập sinh **và (ii)** $B$ độc lập tuyến tính.
> **Số chiều** $\dim V$ = số vectơ của một cơ sở bất kỳ của $V$.

- **Hệ quả:** mọi cơ sở của $V$ có **cùng số phần tử** → $\dim V$ định nghĩa tốt.
- **Cơ sở chính tắc** của $\mathbb{R}^n$: $B_0=\{e_1,\dots,e_n\}$ với $e_i$ có $1$ ở vị trí $i$. Suy ra $\boxed{\dim\mathbb{R}^n = n}$.

**Mệnh đề chặn (rất hay dùng để loại nhanh), với $\dim V = n$:**

| Số vectơ của tập con $S$ | Kết luận chắc chắn |
|---|---|
| $> n$ | $S$ **PTTT** (không thể ĐLTT) |
| $< n$ | $S$ **không** là tập sinh |
| $= n$ | $S$ cơ sở $\iff$ $S$ ĐLTT $\iff$ $S$ là tập sinh |

> [!tip] Mẹo vàng khi số vectơ $= \dim V$
> Chỉ cần kiểm **một trong hai** điều kiện (ĐLTT *hoặc* sinh) là đủ kết luận cơ sở — thường kiểm ĐLTT qua $\det A \neq 0$ là nhanh nhất.

**Mệnh đề mở rộng cơ sở:** nếu $S$ ĐLTT và $u$ **không** là THTT của $S$ thì $S\cup\{u\}$ vẫn ĐLTT. (Nền tảng của "định lý cơ sở không toàn vẹn" — xem 4.2.)

---

## 4. Không gian vectơ con

### 4.1. Định nghĩa & tiêu chuẩn

$W\neq\varnothing$, $W\subseteq V$ là **không gian con** ($W\le V$) nếu $W$ với phép toán hạn chế từ $V$ cũng là KGVT.

> [!important] Tiêu chuẩn không gian con (dùng cái này, đừng kiểm 8 tiên đề!)
> $W\le V \iff \forall u,v\in W,\ \forall\alpha\in\mathbb{R}:\quad \alpha u + v \in W.$
> (Tương đương: $W$ đóng với phép cộng **và** nhân vô hướng.)

> [!tip] Quy trình kiểm tra
> **Bước 1.** Kiểm $0\in W$. Nếu $0\notin W$ → **kết luận ngay không phải KGC, dừng.**
> **Bước 2.** Lấy $u,v\in W,\ \alpha\in\mathbb{R}$ tổng quát, kiểm $\alpha u+v\in W$. Nếu đúng → $W\le V$; nếu sai → chỉ ra **một phản ví dụ cụ thể**.

- ✅ $W=\{2x_1+x_2-x_3=0\}$ là KGC (phương trình thuần nhất).
- ❌ $W=\{x_1+3x_2+x_3=1\}$ không phải ($0\notin W$).
- ❌ $W=\{x_1=2x_2x_3\}$ không phải — phản ví dụ $u=(2,1,1),v=(4,2,1)\in W$ nhưng $u+v=(6,3,2)\notin W$ (phi tuyến).

**Hai phép toán bảo toàn KGC:** nếu $W_1,W_2\le V$ thì
- **Giao** $W_1\cap W_2 \le V$.
- **Tổng** $W_1+W_2=\{w_1+w_2\mid w_i\in W_i\}\le V$.

### 4.2. Không gian con sinh bởi tập hợp

$W=\langle S\rangle$ = tập **mọi THTT** của $S$ = **không gian con nhỏ nhất** chứa $S$. Quy ước $\langle\varnothing\rangle=\{0\}$.

- Mô tả $W$ dạng tham số → tách thành tổ hợp để **đọc ra tập sinh**. VD $W=\{(a+2b,\,a-b,\,-a+2b)\} = \langle (1,1,-1),(2,-1,2)\rangle$.
- **Điều kiện thuộc $\langle S\rangle$:** ép hệ THTT có nghiệm → ràng buộc tuyến tính trên tọa độ (VD $-2x+y=0$ và $x-2z+t=0$).
- **Bằng nhau:** $\langle S_1\rangle=\langle S_2\rangle \iff$ mỗi vectơ của $S_1$ là THTT của $S_2$ và ngược lại.

> [!note] Hai định lý "chỉnh" cơ sở
> - **Cơ sở không toàn vẹn:** $S$ ĐLTT nhưng chưa là cơ sở ⇒ **thêm** vectơ để được cơ sở.
> - **Rút gọn tập sinh:** $S$ sinh $V$ nhưng chưa là cơ sở ⇒ **bỏ bớt** vectơ (các vectơ phụ thuộc) để được cơ sở.

### 4.3. Không gian dòng của ma trận ⭐ (công cụ tính cơ sở mạnh nhất)

Các **vectơ dòng** $u_1,\dots,u_m$ của $A$ sinh ra **không gian dòng** $W_A=\langle u_1,\dots,u_m\rangle$.

> [!important] Định lý nền
> - Hai ma trận **tương đương dòng** ⇒ **cùng** không gian dòng.
> - $\dim W_A = r(A)$, và **các dòng khác $0$ trong dạng bậc thang của $A$ tạo thành một cơ sở** của $W_A$.

> [!tip] Thuật toán tìm cơ sở & số chiều của $W=\langle u_1,\dots,u_m\rangle\le\mathbb{R}^n$
> **Bước 1.** Xếp $u_1,\dots,u_m$ thành các **dòng** của $A$.
> **Bước 2.** Khử Gauss đưa $A$ về **dạng bậc thang** $R_A$.
> **Bước 3.** $\dim W$ = số dòng khác $0$ của $R_A$; các dòng khác $0$ là **một cơ sở** của $W$.

*Nhận xét hữu ích:* nếu $r(A)=$ số vectơ ban đầu thì **các vectơ gốc** $u_1,\dots,u_m$ cũng là một cơ sở (chúng ĐLTT).

### 4.4. Không gian tổng

Nếu $W_1=\langle S_1\rangle,\ W_2=\langle S_2\rangle$ thì $\;W_1+W_2=\langle S_1\cup S_2\rangle$.

→ **Cách tính:** gộp tất cả vectơ sinh của $W_1$ và $W_2$ thành các dòng, khử Gauss, đọc cơ sở như mục 4.3.

---

## 5. Không gian nghiệm của hệ thuần nhất

> [!important] Định lý
> Tập nghiệm $W=\{u\in\mathbb{R}^n \mid Au^\top = 0\}$ của hệ thuần nhất là **không gian con của $\mathbb{R}^n$**, và
> $$\dim W = \text{số ẩn tự do} = n - r(A).$$

> [!tip] Thuật toán tìm cơ sở không gian nghiệm
> **Bước 1.** Giải hệ → nghiệm tổng quát theo các tham số (ẩn tự do) $t,s,\dots$
> **Bước 2.** Lần lượt cho bộ ẩn tự do các giá trị $(1,0,\dots,0),\dots,(0,\dots,0,1)$ → các **nghiệm cơ bản** $u_1,\dots,u_k$.
> **Bước 3.** $\{u_1,\dots,u_k\}$ là **cơ sở** của không gian nghiệm.

**Ví dụ.** Hệ 4 phương trình với nghiệm $(-17t+29s,\,10t-17s,\,t,\,s)$ → cơ sở $\{(-17,10,1,0),(29,-17,0,1)\}$, $\dim W = 2$.

### 5.1. Không gian giao $U\cap W$ — 3 trường hợp

$x\in U\cap W \iff x\in U$ **và** $x\in W$. Cách làm tùy **$U,W$ được cho dưới dạng gì**.

> [!important] Công thức số chiều (Grassmann) — dùng chung cho cả 3 trường hợp
> $$\boxed{\dim(U+W) = \dim U + \dim W - \dim(U\cap W)}$$
> Cho **số chiều** giao ngay (không cần giải thêm). Nhưng muốn **xác định** (viết cơ sở) $U\cap W$ thì vẫn phải làm tiếp theo 1 trong 3 cách dưới, và số tham số tự do tìm được phải khớp con số Grassmann này.

**TH1 — Cả hai cho bằng HỆ SINH** ($U=\langle u_1,\dots,u_p\rangle$, $W=\langle v_1,\dots,v_q\rangle$):
1. Rút gọn về cơ sở của $U$, $W$ (bỏ vectơ thừa).
2. Đặt $\alpha_1u_1+\cdots+\alpha_pu_p = \beta_1v_1+\cdots+\beta_qv_q$ (xếp **cột**).
3. Cân bằng từng tọa độ → hệ thuần nhất ẩn $\alpha_i,\beta_j$, giải ra quan hệ.
4. Thế nghiệm vào **một vế** (vế gọn hơn) → cơ sở $U\cap W$.

*VD:* $U=\langle(1,1,0),(0,1,1)\rangle$, $W=\langle(1,0,1),(1,2,1)\rangle$. Đặt $a(1,1,0)+b(0,1,1)=c(1,0,1)+d(1,2,1)$ → giải ra $a=b=d,\ c=0$, tự do $a$ → $U\cap W=\langle(1,2,1)\rangle$.

**TH2 — MỘT bên hệ sinh, MỘT bên phương trình** ($U=\langle u_1,\dots,u_p\rangle$, $W=\{$ hệ thuần nhất $=0\}$):
1. Viết phần tử tổng quát của $U$: $x=\alpha_1u_1+\cdots+\alpha_pu_p$.
2. Thay tọa độ của $x$ vào **phương trình của $W$** → ràng buộc tuyến tính trên $\alpha_i$.
3. Giải ràng buộc, tìm ẩn tự do.
4. Thế ngược vào $x=\sum\alpha_iu_i$ → cơ sở $U\cap W$.

*VD (bài 3.25):* $U=\langle u,v,w\rangle$, $W=\{x_1+x_2-x_3+2x_4=0\}$. $\alpha u+\beta v+\gamma w=(\alpha{+}\beta{+}\gamma,\alpha,-\gamma,-\alpha{-}\beta)$, thay vào pt $W$ ra $\beta=2\gamma$ → $U\cap W=\langle u,\ 2v+w\rangle$.

**TH3 — Cả hai cho bằng PHƯƠNG TRÌNH** ($U=\{$hệ 1$=0\}$, $W=\{$hệ 2$=0\}$):
1. **Gộp** mọi phương trình của cả 2 hệ thành **một hệ lớn**.
2. Khử Gauss, tìm hạng $r$ → $\dim(U\cap W)=n-r$.
3. Giải nghiệm tổng quát → nghiệm cơ bản = cơ sở $U\cap W$ (đúng thuật toán mục 5 ở trên).

*VD:* $U=\{x_1+x_2-x_3=0\}$, $W=\{x_2-x_4=0\}$ (trong $\mathbb{R}^4$) → gộp 2 pt, hạng 2, $\dim=2$, $U\cap W=\langle(1,0,1,0),(-1,1,0,1)\rangle$.

> [!tip] Bảng chọn nhanh
>
> | $U$ dạng | $W$ dạng | Dùng | Thao tác |
> |---|---|---|---|
> | Hệ sinh | Hệ sinh | TH1 | $\sum\alpha_iu_i=\sum\beta_jv_j$, giải, thế 1 vế |
> | Hệ sinh | Phương trình | TH2 | Phần tử tổng quát $U$ → thay vào pt $W$ |
> | Phương trình | Phương trình | TH3 | Gộp phương trình, giải 1 hệ |

> [!warning] Chốt kiểm luôn áp dụng
> 1. Số tham số tự do tìm được phải **khớp Grassmann**.
> 2. Vectơ cơ sở tìm được phải **kiểm được cả hai điều kiện** (thay vào phương trình ra 0, và/hoặc là tổ hợp đúng của cơ sở kia) — dùng phép nhân ma trận / thay số để tự bắt lỗi trước khi chốt đáp án.

---

## 6. Tọa độ và ma trận chuyển cơ sở

### 6.1. Tọa độ theo cơ sở

**Cơ sở được sắp** $B=(u_1,\dots,u_n)$: cố định thứ tự các vectơ. Khi đó mọi $u\in V$ biểu diễn **duy nhất** $u=\alpha_1 u_1+\cdots+\alpha_n u_n$, và

$$[u]_B = \begin{pmatrix}\alpha_1\\ \vdots\\ \alpha_n\end{pmatrix} \quad(\text{vectơ tọa độ của } u \text{ theo } B).$$

- Với **cơ sở chính tắc** $B_0$ của $\mathbb{R}^n$: $[u]_{B_0} = u^\top$ (tọa độ chính là các thành phần).
- **Tuyến tính của tọa độ:** $[u+v]_B=[u]_B+[v]_B$ và $[\alpha u]_B=\alpha[u]_B$.

> [!tip] Tìm $[u]_B$ trong $\mathbb{R}^m$
> Lập $\big(u_1^\top\ u_2^\top\ \dots\ u_n^\top \mid u^\top\big)$ → Gauss–Jordan → nghiệm $(c_1,\dots,c_n)$ chính là $[u]_B$.

### 6.2. Ma trận chuyển cơ sở

> [!important] Định nghĩa
> Với hai cơ sở $B_1=(u_1,\dots,u_n)$, $B_2=(v_1,\dots,v_n)$ của $V$:
> $$(B_1\to B_2) = P = \big([v_1]_{B_1}\ \ [v_2]_{B_1}\ \dots\ [v_n]_{B_1}\big)$$
> Mỗi **cột** $P$ = tọa độ của vectơ cơ sở **mới** $v_j$ theo cơ sở **cũ** $B_1$.

> [!tip] Cách tìm $(B_1\to B_2)$ nhanh trong $\mathbb{R}^n$
> Lập ma trận mở rộng $\big(u_1^\top\dots u_n^\top \mid v_1^\top\dots v_n^\top\big)$, biến đổi sơ cấp dòng về dạng $(I_n \mid P)$. Khi đó $(B_1\to B_2)=P$.

> [!important] Bốn tính chất "vàng"
> 1. $(B\to B) = I_n$.
> 2. $[u]_{B_1} = (B_1\to B_2)\,[u]_{B_2}$ — **đổi tọa độ** từ $B_2$ sang $B_1$.
> 3. $(B_2\to B_1) = (B_1\to B_2)^{-1}$ — nghịch đảo.
> 4. $(B_1\to B_3) = (B_1\to B_2)(B_2\to B_3)$ — bắc cầu.

**Liên hệ với cơ sở chính tắc** (cực kỳ tiện trong $\mathbb{R}^n$):
- $(B_0\to B) = \big(u_1^\top\ u_2^\top\ \dots\ u_n^\top\big)$ — chỉ cần xếp các vectơ cơ sở thành cột.
- $(B\to B_0) = (B_0\to B)^{-1}$.
- $(B_1\to B_2) = (B_0\to B_1)^{-1}(B_0\to B_2)$.

**Ví dụ áp dụng tính chất 2.** Biết $(S\to T)$ và $[u]_T$ → $[u]_S = (S\to T)[u]_T$ (nhân ma trận với vectơ tọa độ).

---

## 7. Tổng kết — Sơ đồ tư duy & checklist ôn thi

> [!summary] Mọi bài toán Chương 3 quy về 3 bước
> 1. **Lập ma trận** (xếp vectơ thành dòng hoặc cột — tùy mục đích).
> 2. **Khử Gauss** đưa về bậc thang, đọc **hạng $r(A)$**.
> 3. **Dịch $r(A)$ ra kết luận** theo bảng dưới.

| Câu hỏi | Cách làm | Kết luận theo $r(A)$ |
|---|---|---|
| $u$ là THTT của họ? | Xếp **cột** + cột $u$, giải hệ | Có nghiệm ⇒ có; vô nghiệm ⇒ không |
| Họ ĐLTT hay PTTT? | Xếp dòng/cột, tính $r(A)$ | $r=m$ ⇒ ĐLTT; $r<m$ ⇒ PTTT |
| $S$ có sinh $\mathbb{R}^n$? | Hệ có nghiệm với mọi $u$ | $r=n$ ⇒ sinh |
| $S$ có là cơ sở $\mathbb{R}^n$? | Số vectơ $=n$ **và** ĐLTT ($\det\neq 0$) | thỏa cả hai ⇒ cơ sở |
| Cơ sở & $\dim$ của $\langle S\rangle$? | Xếp **dòng** → bậc thang | dòng khác $0$ = cơ sở; số đó = $\dim$ |
| Cơ sở không gian nghiệm $AX=0$? | Giải hệ → nghiệm cơ bản | $\dim = n - r(A)$ |
| $W$ có là KGC? | Kiểm $0\in W$ rồi $\alpha u+v\in W$ | — |
| Tọa độ $[u]_B$? | $(u_i^\top\mid u^\top)$ → Gauss–Jordan | nghiệm = $[u]_B$ |
| Ma trận chuyển $(B_1\to B_2)$? | $(u_i^\top\mid v_j^\top)\to(I_n\mid P)$ | $P$ = ma trận chuyển |

> [!note] Các công thức phải thuộc lòng
> - $\dim\mathbb{R}^n = n$, $\dim M_{m\times n}=mn$, $\dim\mathbb{R}_n[x]=n+1$.
> - $\dim W_A = r(A)$ (không gian dòng).
> - $\dim(\text{nghiệm } AX=0) = n - r(A)$.
> - **Grassmann:** $\dim(W_1+W_2)=\dim W_1+\dim W_2-\dim(W_1\cap W_2)$.
> - $[u]_{B_1}=(B_1\to B_2)[u]_{B_2}$ và $(B_2\to B_1)=(B_1\to B_2)^{-1}$.

> [!warning] Bẫy thường gặp
> - **Phương trình có hằng số ≠ 0** ($=1$) ⇒ KHÔNG là KGC/KGVT (vì $0$ không thuộc).
> - **Quan hệ phi tuyến** ($x_1=2x_2x_3$, $u^\alpha$...) ⇒ kiểm kỹ, thường KHÔNG đóng.
> - "$u$ là THTT" có **vô số cách biểu diễn** khi họ PTTT — đừng nhầm với "duy nhất" (chỉ duy nhất khi là **cơ sở**).
> - Xếp **dòng** để tìm cơ sở không gian dòng; xếp **cột** để kiểm THTT/tọa độ. Đừng lẫn lộn.

---
*Ghi chú ôn tập tự động hóa từ slide Chương 3 (99 trang). Xem bài tập áp dụng tại [[ĐSTT_Chương3_Bài_Tập]].*
