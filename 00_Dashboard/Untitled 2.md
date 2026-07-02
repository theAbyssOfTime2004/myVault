Ví dụ dùng **Đề số 2, Câu 1b** — vì $U$ cho bằng hệ sinh, còn $W$ vốn cho bằng **hệ phương trình** (chỉ là ta đã giải nó ra thành $w_1,w_2$ ở câu a). Dùng lại **chính hệ phương trình gốc** của $W$ thay vì cơ sở $w_1,w_2$.

## Nhắc lại đề

$W={x_1+x_2+x_3+x_4=0,\ x_1+2x_2+x_3+2x_4=0,\ 2x_1+3x_2+2x_3+3x_4=0}$. Từ câu a, khử Gauss ra hệ **rút gọn tương đương**: $$\begin{cases}x_1+x_2+x_3+x_4=0\ x_2+x_4=0\end{cases}\quad(\text{2 phương trình độc lập, đây chính là "phương trình của }W\text{"})$$

$U=\langle u_1=(1,0,0,1),\ u_2=(0,1,1,0)\rangle$ (đã bỏ $u_3$ thừa).

## Cách cũ (TH1, đã làm) — 4 ẩn

Đặt $\alpha u_1+\beta u_2=sw_1+tw_2$, cân bằng 4 tọa độ, giải hệ 4 ẩn $\alpha,\beta,s,t$.

## Cách mới (TH2 shortcut) — chỉ 2 ẩn, nhanh hơn hẳn

**Bước 1 — Phần tử tổng quát của $U$:** $$x=\alpha u_1+\beta u_2=(\alpha,\ \beta,\ \beta,\ \alpha)$$

**Bước 2 — Thay thẳng vào 2 phương trình của $W$ (không cần $w_1,w_2$):** $$\begin{cases}x_1+x_2+x_3+x_4=0 \ \Rightarrow\ \alpha+\beta+\beta+\alpha=0 \ \Rightarrow\ 2\alpha+2\beta=0\ \Rightarrow\ \alpha+\beta=0\ x_2+x_4=0 \ \Rightarrow\ \beta+\alpha=0\ \Rightarrow\ \alpha+\beta=0\end{cases}$$

**Cả hai phương trình cho CÙNG một ràng buộc** $\alpha+\beta=0$ — chỉ **2 ẩn**, giải ngay tại chỗ, khỏi lập bảng hay khử Gauss thêm.

**Bước 3 — Tự do $\alpha=r\Rightarrow\beta=-r$:** $$x=\alpha u_1+\beta u_2=r,u_1-r,u_2=r(1,-1,-1,1)$$

$$\boxed{U\cap W=\langle(1,-1,-1,1)\rangle}$$

**Trùng chính xác** kết quả cũ, nhưng chỉ mất **2 ẩn thay vì 4**, và khỏi cần bảng cân bằng tọa độ + không cần dùng $w_1,w_2$ ở bước này.

## So sánh tốc độ

||Cách cũ (TH1)|Cách mới (TH2 shortcut)|
|---|---|---|
|Số ẩn|4 ($\alpha,\beta,s,t$)|2 ($\alpha,\beta$)|
|Cần $w_1,w_2$?|Có|Không — dùng thẳng phương trình gốc|
|Số phương trình phải cân bằng|4 tọa độ|Bằng số phương trình của $W$ (ở đây 2)|

## Lưu ý quan trọng — khi nào dùng được

Cách này áp dụng được vì **$U$ vốn cho bằng hệ sinh và $W$ vốn cho bằng phương trình** (dù đề bắt bạn giải $W$ ra cơ sở ở câu a, nhưng hệ phương trình gốc/rút gọn vẫn dùng lại được ở bước xác định $U\cap W$). Còn **cơ sở $U+W$** (đề vẫn bắt tìm) thì **vẫn phải** gộp $u_1,u_2,w_1,w_2$ khử Gauss như cũ — TH2 chỉ giúp tiết kiệm ở **bước cuối** (xác định $U\cap W$), không thay được toàn bộ Câu 1b.