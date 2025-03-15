2025-03-15 22:44


Tags: [[data mining]]

# The Basic Data Types and Major Building Blocks

### The basic data types
- có 2 loại dữ liệu chính với độ phức tạp đa dạng là 
	- Dữ liệu định hướng không phụ thuộc 
	- Dữ liệu định hướng phụ thuộc
![[Pasted image 20250315225022.png]]
- Có thể hiểu rằng:
	-  **Dữ liệu không phụ thuộc (Nondependency-oriented data):**
	    - Dữ liệu đơn giản, không có mối quan hệ giữa các mục hoặc thuộc tính.
	    - Ví dụ: Hồ sơ nhân khẩu học gồm tuổi, giới tính, mã ZIP.
	- **Dữ liệu có phụ thuộc (Dependency-oriented data):**
	    - Có mối quan hệ rõ ràng hoặc ẩn giữa các mục dữ liệu.
	    - Ví dụ:
	        - **Mạng xã hội:** Các người dùng (đỉnh) liên kết với nhau qua mối quan hệ (cạnh).
	        - **Dữ liệu chuỗi thời gian:** Các giá trị liên tiếp từ cảm biến có liên quan đến nhau theo thời gian.
- Dữ liệu định hướng phụ thuộc có 2 kiểu phụ thuộc:
	- Phụ thuộc ngầm: 
		- Không được chỉ định rõ ràng nhưng có tồn tại:
			- Ví dụ:
			- **Dữ liệu cảm biến nhiệt độ:** Các giá trị đo liên tiếp thường có sự tương đồng. Nếu có sự thay đổi đột ngột, điều đó có thể là bất thường và cần được phân tích.
			- **Dữ liệu chuỗi thời gian:** Giá trị của một thời điểm thường liên quan đến giá trị của thời điểm kế tiếp.
	- Phụ thuộc tường minh:
		- Được biểu diễn rõ bằng các mối quan hệ, thường sử dụng graph
		- Ví dụ:
			- **Mạng xã hội:** Người dùng kết nối với nhau qua mối quan hệ bạn bè.
			- **Hệ thống giao thông:** Các nút giao thông kết nối với nhau bằng đường đi.
			- **Dữ liệu liên kết web:** Các trang web có liên kết đến nhau.
- Dữ liệu định hướng phụ thuộc có 4 loại:
	-  Time-series Data
	- Discrete Sequences and Strings
	- Spartial Data
	- Network and Graph Data
### Major Building Blocks
- Khai phá mẫu liên hệ (*Association Pattern Mining*)
	- 
# References
