Bạn đúng, và mình xin nhận sai — đây là lỗi dấu quan trọng, để mình sửa lại cho chuẩn.

## Quy tắc đúng (đã bị mình nói ngược ở vài tin trước)

Trong dạng từ vựng ta đang dùng ($w_i = b_i + d_{ij}x_j$, tức $w_i$ = hằng số + hệ số), **biến vào phải có hệ số DƯƠNG** trên dòng biến ra, không phải âm. Lý do: $w_4 = -4+x_1-4x_2$ đang âm, muốn kéo nó về 0 (tăng lên) thì cần tăng biến nào làm $w_4$ **tăng theo** — tức hệ số dương ($x_1$: $+1$). Hệ số âm ($x_2$: $-4$) sẽ kéo $w_4$ càng âm hơn, không dùng được.

Đối chiếu lại: đây khớp với mọi bước đối ngẫu đã làm đúng trước đó (ví dụ $w_1=-2+4x_1-x_2$ từng chọn $x_1$ hệ số $+4$, không chọn $x_2$ hệ số $-1$) — quy tắc đó vốn đúng, chỉ là 2-3 tin gần đây mình lỡ phát biểu ngược lại. Cảm ơn bạn đã bắt lỗi.

## Sửa lại phép xoay: $x_1$ vào, $w_4$ ra

Từ $w_4=-4+x_1-4x_2$, giải $x_1$: $$x_1 = 4+4x_2+w_4$$

_(Lưu ý nhỏ: bạn viết $x_1=4+4x_2-w_4$ — dấu $w_4$ bị lệch, phải là $+w_4$. Kiểm tra ngược: thế vào $w_4=x_1-4-4x_2$ ra đúng $-4+x_1-4x_2$ ✓ chỉ khi hệ số là $+w_4$.)_

Thế vào các dòng còn lại:

$$\begin{aligned} 
z' &= 9x_1+x_2 = 36+37x_2+9w_4\ 
w_1 &= 10-6x_1-5x_2 = -14-29x_2-6w_4\ w_2 &= 8-3x_1+2x_2 = -4-10x_2-3w_4\ w_3 &= 3-2x_1-x_2 = -5-9x_2-2w_4 \end{aligned}$$

## Kiểm tra: có xoay tiếp được không?

$b$ âm nhất bây giờ là $w_1=-14$. Xét dòng $w_1 = -14-29x_2-6w_4$: hệ số $x_2$ là $-29$, hệ số $w_4$ là $-6$ — **cả hai đều âm**, không còn cột dương nào để chọn biến vào.

Theo đúng quy tắc (nay đã sửa lại): **không có ứng viên vào → bài toán vô nghiệm.** Kết luận cuối cùng không đổi so với trước (vẫn vô nghiệm, khớp với chứng minh đại số $x_1\ge4$ mâu thuẫn $x_1\le\tfrac53$), nhưng bây giờ lộ ra **ngay sau đúng 1 bước xoay**, gọn hơn hẳn so với lập luận "vòng lặp 2 bước" mình đưa ra trước — lập luận đó dựa trên quy tắc sai nên không cần dùng nữa.

## Quy tắc tổng hợp cần sửa lại trong bảng bạn tóm tắt trước đó

> Đơn hình đối ngẫu — biến vào: trên dòng biến ra, chỉ xét cột có hệ số **DƯƠNG** _(không phải âm)_; tỉ số = (hệ số dòng $z$) ÷ (hệ số dòng đang xét), chọn tỉ số dương nhỏ nhất.

Mọi chỗ khác trong bảng tổng hợp của bạn (biến ra, điều kiện dừng, hai pha...) vẫn đúng nguyên, chỉ riêng dấu của điều kiện chọn cột này cần sửa lại như trên.