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


Có 1 lỗi cú pháp — không thể nối "$f\in L(\mathbb{R}^3)$" và "$f(x,y,z)=\dots$" bằng dấu "=".

## Lỗi ở đâu

"$f\in L(\mathbb{R}^3)$" là một **mệnh đề** (khẳng định $f$ **thuộc** một tập hợp) — không phải một con số hay biểu thức, nên **không thể đặt dấu "=" ngay sau nó** để nối với công thức. Viết "$f\in L(\mathbb{R}^3)=f(x,y,z)=\dots$" giống như viết "$x$ là số nguyên $=5$" — sai ngữ pháp toán học.

## Phần sau thì ĐÚNG

$$f(x,y,z)=[f]_{B_0}\cdot(x,y,z)$$

Đây là công thức **chính xác** — ma trận $[f]_{B_0}$ nhân với vectơ tọa độ (viết dạng cột) ra $f(u)$, vì $[u]_{B_0}=u$ (tọa độ chuẩn chính là chính nó).

## Cách viết đúng

Tách thành **hai câu riêng**: $$\text{Cho } f\in L(\mathbb{R}^3).\qquad f(x,y,z)=[f]_{B_0}\begin{pmatrix}x\y\z\end{pmatrix}.$$

Hoặc nếu muốn viết liền mạch trong lời giải: $$f(x,y,z)=[f]_{B_0}\cdot(x,y,z)^\top,\quad\text{với } f\in L(\mathbb{R}^3).$$

## Mẹo phân biệt "$\in$" và "$=$"

|Ký hiệu|Dùng khi nào|
|---|---|
|$\in$|"là phần tử của", nối một **đối tượng** với một **tập hợp**|
|$=$|nối hai **đối tượng cùng loại** (2 số, 2 vectơ, 2 hàm...)|

$f$ và $\mathbb{R}^3$ (hay $L(\mathbb{R}^3)$) không "cùng loại" theo nghĩa đó — $f$ là phần tử, $L(\mathbb{R}^3)$ là tập hợp — nên chỉ dùng $\in$, không dùng $=$.