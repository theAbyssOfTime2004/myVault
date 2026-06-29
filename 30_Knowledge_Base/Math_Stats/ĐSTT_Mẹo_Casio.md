---
tags: [linear-algebra, casio, exam, university]
aliases: [Mẹo Casio ĐSTT, Casio fx-580VN X LATT]
---

# Đại số tuyến tính – Mẹo bấm Casio (fx-580VN X / fx-880BTG)

> Liên quan: [[ĐSTT_Đề_Thi_Thử_Cuối_Kỳ]], [[ĐSTT_Chương3_Không_gian_vectơ]], [[ĐSTT_Chương5_Chéo_hóa]].

> [!warning] Casio chỉ để KIỂM TRA, không thay lời giải
> Máy **không** khử Gauss / không cho cơ sở / không cho nghiệm tổng quát. Bài vẫn phải trình bày tay (khử Gauss, đọc nghiệm) mới có điểm. Máy giúp **chốt hạng** và **bắt lỗi số học**.

---

## Mẹo 1 — Chốt hạng bằng định thức con

Hạng của ma trận = cấp lớn nhất của **định thức con khác 0**. Casio tính được det tới $4\times4$.

**Kiểm $\dim U=3$:** xếp $u_1,u_2,u_3$ thành ma trận $3\times4$. Lấy một định thức con $3\times3$ (ví dụ bỏ cột 4):

$$\det\begin{pmatrix}1&-1&0\\1&0&-1\\1&0&0\end{pmatrix}=1\neq 0 \Rightarrow \text{hạng}=3.$$

**Kiểm $\dim(U+W)=4$:** ma trận xếp 5 dòng là $5\times4$ — Casio chỉ nhập tối đa $4\times4$, nên **chọn 4 trong 5 dòng** rồi tính det $4\times4$. Ví dụ lấy $u_1,u_2,u_3,w_1$:

$$\det\begin{pmatrix}1&-1&0&0\\1&0&-1&0\\1&0&0&-1\\-2&1&0&0\end{pmatrix}=-1\neq 0 \Rightarrow \text{hạng}=4.$$

> [!note] Quy tắc một chiều
> det $\neq 0$ → chốt được hạng $=4$ (xong). Nếu lỡ chọn 4 dòng cho det $=0$ thì **chưa** kết luận được, phải thử bộ 4 dòng khác. Cứ nhắm bộ "đẹp" để ra $\neq 0$.

**Thao tác:** `Menu → Ma trận` → định nghĩa MatA đúng cỡ → nhập số → thoát, gõ `det(MatA)` (phím `OPTN` có `Det`).

---

## Mẹo 2 — Nhân ma trận để kiểm nghiệm

Sau khi tìm $W=\langle w_1,w_2\rangle$ và $U\cap W=\langle(2,0,-1,-1)\rangle$, kiểm bằng phép nhân: vectơ thuộc $W$ thì nhân với ma trận hệ số phải ra $0$.

Nhập **MatA** = ma trận hệ số $3\times4$, **MatB** = vectơ cột $4\times1$, rồi tính `MatA × MatB`:

$$\text{MatA}\times w_1 = 0,\quad \text{MatA}\times w_2 = 0,\quad \text{MatA}\times(2,0,-1,-1)^\top = 0.$$

Cả ba ra cột $0$ ⇒ chắc chắn nằm trong $W$. Sai một số là lòi ra ngay. *(fx-580VN X nhập ma trận tối đa $4\times4$ nên $3\times4$ và $4\times1$ đều OK.)*

---

## Mẹo 3 — Trị riêng cho Câu 3 & 4 (giải đa thức đặc trưng)

Casio **không** tính trị riêng trực tiếp, nhưng giải được phương trình đa thức:

1. Tính đa thức đặc trưng $P_A(\lambda)=\det(A-\lambda I)$ bằng tay.
2. `Menu → Phương trình → Đa thức`: bậc 2 cho ma trận $2\times2$, bậc 3 cho $3\times3$ → nhập hệ số → ra ngay nghiệm $=$ trị riêng.

Riêng Câu 3 ($A$ cấp 2): char poly bậc 2, bấm ra 2 trị riêng trong vài giây.

---

## Tóm tắt

| Việc | Casio làm được? |
|---|---|
| Khử Gauss, ra cơ sở / nghiệm tổng quát | ❌ làm tay |
| Chốt hạng (det con $\le 4\times4$) | ✅ |
| Kiểm vectơ $\in W$ (nhân $A\cdot v=0$) | ✅ |
| Kiểm ĐLTT / cơ sở (det $\neq 0$) | ✅ |
| Trị riêng (giải đa thức đặc trưng) | ✅ nửa tay nửa máy |

> [!tip] Lưu ý Obsidian
> Block math `$$...$$` phải ở **cột 0**, không thụt trong bullet thì mới render (giống quy tắc bảng).
