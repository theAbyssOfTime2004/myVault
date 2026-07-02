Đúng — chính xác là tìm $f(x,y,z)$.

## Giải nghĩa ký hiệu

$L(\mathbb{R}^3)$ = tập hợp **mọi ánh xạ tuyến tính** từ $\mathbb{R}^3$ vào chính nó (gọi là **toán tử tuyến tính**, xem [[ĐSTT_Chương4_Ánh_xạ_tuyến_tính]] §1). "$f\in L(\mathbb{R}^3)$" chỉ là cách nói gọn: "$f$ là một toán tử tuyến tính trên $\mathbb{R}^3$".

**"Tìm công thức của $f$"** = viết ra biểu thức tường minh: $$f(x,y,z)=(\dots,\ \dots,\ \dots)$$ — đúng cái mà Câu 2a trong mọi đề mẫu yêu cầu.

## Vì sao cần "tìm" chứ không cho sẵn

Đề chỉ cho $[f]_B$ (ma trận biểu diễn theo cơ sở $B$ **lạ**, không phải $B_0$), nên chưa đọc trực tiếp ra công thức được — phải **đổi sang $[f]_{B_0}$** trước:

$$[f]_{B_0}=P,[f]_B,P^{-1}\qquad (P=(B_0\to B),\text{ xếp cột } u_1,u_2,u_3)$$

Sau đó **đọc từng dòng** của $[f]_{B_0}$ ra công thức: dòng $i$ cho tọa độ thứ $i$ của $f(x,y,z)$.

## Ví dụ (Câu 2 Đề số 2)

$[f]_{B_0}=\begin{pmatrix}2&0&1\1&0&2\1&-1&1\end{pmatrix}$ → đọc trực tiếp: $$f(x,y,z)=(2x+z,\ x+2z,\ x-y+z)$$

Đây chính là "công thức của $f$" mà đề hỏi.