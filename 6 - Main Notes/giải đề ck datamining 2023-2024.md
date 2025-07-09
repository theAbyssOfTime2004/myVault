![[Pasted image 20250709183047.png]]

# Bài giải
### Câu 1: 
- **Câu 1a**: Các bước quan trọng trong quá trình tiền xử lý dữ liệu (data preparation) cho một dự án khai thác dữ liệu thực tế có thể bao gồm:
	- Feature Extraction: là chuyển đổi dữ liệu thô không có cấu trúc hoặc có cấu trúc phức tạp thành các thuộc tính có ý nghĩa, phù hợp cho việc xử lý bằng các thuật toán data mining
	- Data Cleaning: Quy trình làm sạch dữ liệu là thiết yếu vì các lỗi và sự không nhất quán có thể xảy ra trong quá trình thu thập dữ liệu. Các tác vụ data cleaning cơ bản và quan trọng nhất bao gồm: 
		- Handling Missing Data
		- Detecting Outlier 
		- Normalization
	- Feature Selection and Transform: Chọn lọc và biến đổi là hai tác vụ quan trọng cần thực hiện sau khi thu thập được data và trước khi đưa vào mô hình, trước tiên đối với việc chọn lọc, mục tiêu chung của tác vụ này là giảm kích cỡ dữ liệu và sàng lọc ra được những dữ liệu có ích, mang lại nhiều ý nghĩa cho quá trình học (build model) và cũng như giúp các thuật toán chạy nhanh hơn, hiệu quả hơn. Còn biến đổi là việc chuyển đổi kiểu dữ liệu này sang dữ liệu khác, và việc này cũng sẽ diễn ra trước khi dữ liệu đi vào mô hình, mục tiêu của là để đảm bảo rằng dữ liệu đầu vào tương thích với yêu cầu của mô hình
		- Một vài phép chọn lọc và biến đổi có thể kể đến là:
			- Chọn lọc:
				- Unsupervised feature selection
				- Supervised feature selection
			- Biến đổi:
				- Discretization
				- Binarization
