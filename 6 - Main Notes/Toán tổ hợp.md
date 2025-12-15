-  in general thì hàm sinh là 1 dãy tổng vô hạn kiểu A(x) = a_0 + a_1x+ a_2x^2 + a_3x^3 +... và có thể được biễu diễn ở dạng rút gọn (ví dụ như là 1/1-x) và mục đích tồn tại của hàm sinh này là vì nó có thể dùng để mô hình hóa một số bài toán tổ hợp và giúp ta giải các bài toán đấy một cách dễ dàng thay vì các phương pháp đếm thủ công
- Ví dụ ta có 1 bài toán: cần chọn ra **$r$ viên bi** từ một rổ gồm: 3 bi Xanh, 3 bi Trắng, 3 bi Đỏ, 3 bi Vàng. _(Giới hạn: Mỗi màu chỉ có tối đa 3 viên)_.
- Nếu đểm thủ công
	-  _Trường hợp 1:_ 3 Xanh, 3 Trắng, 3 Đỏ, 1 Vàng.
	- _Trường hợp 2:_ 3 Xanh, 2 Trắng, 2 Đỏ, 3 Vàng.
	- _Trường hợp 3:_ ... (Rất dễ sót hoặc trùng lặp).

- Dùng hàm sinh để mô hình hóa:
	-  $$A(x) = (1 + x + x^2 + x^3) \cdot (1 + x + x^2 + x^3) \cdot (1 + x + x^2 + x^3) \cdot (1 + x + x^2 + x^3)$$
$$A(x) = (1 + x + x^2 + x^3)^4$$
=> Ví dụ r = 10, ta chỉ cần tìm hệ số của $x^{10}$ trong khai triển và được đáp án 