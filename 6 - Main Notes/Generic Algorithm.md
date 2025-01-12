2025-01-13 02:23


Tags: [[Local Search Algorithm]], [[search algorithm]], [[Machine Learning]]

# Generic Algorithm
### Giới thiệu:
- Dựa trên (bắt chước) quá trình tiến hóa tự nhiên trong sinh học
- Áp dụng phương pháp tìm kiếm ngẫu nhiên  (stochastic search) để tìm được lời giải (vd: một hàm mục tiêu, một mô hình phân lớp, ...) tối ưu.
- Giải thuật di truy di truyền (Generic Algorithm (Generic Algorithm – GA) có khả năng tìm được các lời giải tốt thậm chí ngay cả với các không gian tìm kiếm (lời giải) không liên tục rất phức tạp
- Mỗi khả năng của lời giải được biểu diễn bằng một chuỗi nhị phân (vd: 100101101) – được gọi là nhiễm sắc thể (chromosome).
	- việc biểu diễn này phụ thuộc vào từng bài toán cụ thể.
- GA cũng đc xem như 1 bài toán học máy, dựa trên quá trình optimization
#### Mô tả:
- Xây dựng (khởi tạo) quần thể (population) ban đầu
	- Tạo nên một số các giả thiết (khả năng của lời giải) ban đầu
	- Mỗi giả thiết khác các gi khác các giả thiết khác (vd: khác nhau đối với các giá trị của một số tham số nào đó của bài toán)
- Đánh giá quần thể
	- Đánh giá (cho ánh giá (cho điểm) mỗi giả thiết (vd: bằng cách kiểm tra độ chính xác của hệ thống trên một tập dữ liệu kiểm thử)
	- Trong lĩnh vực sinh học, điểm đánh giá này của mỗi giả thiết được gọi là *độ phù hợp (fitness)* của giả thiết đó
	-  Xếp hạng các giả thiết theo mức độ phù hợp của chúng, và chỉ giữ lại các giả thiết tốt nhất (gọi là *các giả thiết phù hợp nhất – survival of the fittest)*
- Sản sinh ra sinh ra *thế hệ tiếp theo (next generation)*
	-  Thay đổi ngẫu nhiên các giả thiết để sản sinh ra thế hệ tiếp theo (gọi là *các con cháu – offspring)*
- Lặp lại quá trình trên cho đến khi ở một thế hệ nào đó có giả thiết tốt nhất có độ phù hợp cao hơn giá tri phù hợp mong muốn (định trước)
![[Pasted image 20250113022943.png]]
![[Pasted image 20250113022951.png]]

#### GA - Minh họa
![[Pasted image 20250113023010.png]]

#### Các toán tử di truyền:
- 3 toán tử di truyền được sử dụng để sinh ra các cá thể con cháu (offspring) trong thế hệ tiếp theo
	- Nhưng chỉ có 2 toán tử lai ghép (crossover) và đột biến (mutation) tạo nên sự thay đổi

 - **Tái sản xuất (Reproduction)**
	-  Một giả thiết được giữ lại (không thay đổi)
 - **Lai ghép (Crossover)** ==để sinh ra 2 cá thể mới==
	- Ghép ("phối hợp") của hai cá thể cha mẹ
	- Điểm lai ghép được chọn ngẫu nhiên (trên chiều dài của nhiễm sắc thể)
	- Phần đầu tiên của nhiễm sắc thể $hi$ được ghép với phần sau của nhiễm sắc thể $hj$ và ngược lại để sinh ra 2 nhiễm sắc thể mới, và ngược lại, để sinh ra 2 nhiễm sắc thể mới

 - **Đột biến (Mutation)** ==để sinh ra 1 cá thể mới==
	- Chọn ngẫu nhiên một bit của nhiễm sắc thể, và đổi giá trị (0→1 / 1→0)
	-  Chỉ tạo nên một thay đổi nhỏ và ngẫu nhiên đối với một cá thể cha mẹ
	![[Pasted image 20250113023318.png]]
	![[Pasted image 20250113023350.png]]
	
# References
