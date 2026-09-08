-  in general thì hàm sinh (generating func là 1 dãy tổng vô hạn kiểu A(x) = a_0 + a_1x+ a_2x^2 + a_3x^3 +... và có thể được biễu diễn ở dạng rút gọn (ví dụ như là 1/1-x) và mục đích tồn tại của hàm sinh này là vì nó có thể dùng để mô hình hóa một số bài toán tổ hợp và giúp ta giải các bài toán đấy một cách dễ dàng thay vì các phương pháp đếm thủ công
- Ví dụ ta có 1 bài toán: cần chọn ra **$r$ viên bi** từ một rổ gồm: 3 bi Xanh, 3 bi Trắng, 3 bi Đỏ, 3 bi Vàng. _(Giới hạn: Mỗi màu chỉ có tối đa 3 viên)_.
- Nếu đểm thủ công
	-  _Trường hợp 1:_ 3 Xanh, 3 Trắng, 3 Đỏ, 1 Vàng.
	- _Trường hợp 2:_ 3 Xanh, 2 Trắng, 2 Đỏ, 3 Vàng.
	- _Trường hợp 3:_ ... (Rất dễ sót hoặc trùng lặp).

- Dùng hàm sinh để mô hình hóa:
	-  $$A(x) = (1 + x + x^2 + x^3) \cdot (1 + x + x^2 + x^3) \cdot (1 + x + x^2 + x^3) \cdot (1 + x + x^2 + x^3)$$
$$A(x) = (1 + x + x^2 + x^3)^4$$
=> Ví dụ r = 10, ta chỉ cần tìm hệ số của $x^{10}$ trong khai triển và được đáp án 

- 1 ví dụ mang tính trực giác về việc tại sao hệ số đứng trước $x^e$ lại đại diện cho số cách chọn của $e$:
	Hãy thử bài toán: Chọn 2 viên bi từ 2 màu (Xanh, Trắng), mỗi màu tối đa 1 viên.
	- Xanh: $(1 + x)$ (chọn 0 hoặc 1)
	- Trắng: $(1 + x)$ (chọn 0 hoặc 1)
	Phép nhân:
	
	$$(1 + x) \cdot (1 + x) = 1 \cdot 1 + 1 \cdot x + x \cdot 1 + x \cdot x$$
	$$= 1 + x + x + x^2$$
	$$= 1 + \mathbf{2}x + x^2$$
	Tại sao hệ số của $x^1$ (tổng 1 viên) lại là 2?
	
	Vì lúc nhân, ta có 2 trường hợp tạo ra $x^1$:
	
	1. Chọn 1 Xanh ($x$), 0 Trắng ($1$) $\rightarrow x \cdot 1 = x$
	2. Chọn 0 Xanh ($1$), 1 Trắng ($x$) $\rightarrow 1 \cdot x = x$
	
	Cộng lại ta có $2x$. Vậy có 2 cách chọn 1 viên.
	$\rightarrow$ **Kết luận:** Hệ số của $x^{10}$ trong bài toán lớn chính là tổng số lần các bộ $(e_1, e_2, e_3, e_4)$ cộng lại bằng 10

- Một giải thích có hệ thống hơn thì về bản chất đó là sự đẳng cấu (*Isomorphism*) giữa đại số và tổ hợp
- **Trong Đại số:** Khi nhân hai lũy thừa cùng cơ số, ta **cộng** số mũ.
- **Trong Tổ hợp:** Khi ta gộp (kết hợp) một nhóm $n$ vật thể với một nhóm $m$ vật thể, tổng kích thước (số lượng) của chúng được **cộng** lại ($n+m$).
$\rightarrow$ Vì phép nhân đại số kích hoạt việc cộng số mũ, nó trở thành công cụ hoàn hảo để mô phỏng việc "cộng dồn" số lượng các vật thể được chọn.

- Tính chất phân phối giúp ta liệt kê ra tất cả các trường hợp (cases) mà không bị sót. Mỗi đơn thức sau khi nhân tung ra (ví dụ $1 \cdot x^2$) chính là một "kịch bản" lựa chọn cụ thể.