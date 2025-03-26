
# So Sánh Chi Tiết Các Thuật Toán PCA, LSA và SVD

## I. Phân Tích Thành Phần Chính (PCA - Principal Component Analysis)

### 1. Nguyên Lý Cơ Bản

- Áp dụng mean centering cho dữ liệu: mỗi điểm được trừ đi trung bình của tập dữ liệu
- Có thể áp dụng ngay cả khi trung bình dữ liệu được lưu riêng

### 2. Mục Tiêu Chính

- Xoay dữ liệu về một hệ trục sao cho lượng phương sai lớn nhất có thể được biểu diễn bởi số chiều nhỏ nhất

### 3. Đặc Điểm Toán Học

- Phương sai của tập dữ liệu theo một hướng cụ thể được thể hiện qua ma trận phương sai
- Ma trận phương sai là đối xứng và nửa xác định dương
- Các vector riêng với giá trị riêng lớn thể hiện các principal components (trục chính)

## II. Phân Rã Giá Trị Riêng (SVD - Singular Value Decomposition)

### 1. Mối Quan Hệ với PCA

- Có mối liên hệ gần gũi với PCA
- Cung cấp 2 bộ vector cơ sở tương tự PCA
- Cho cùng vector cơ sở với PCA nếu dữ liệu có trung bình bằng 0

## III. Phân Tích Ngữ Nghĩa Tiềm Ẩn (LSA - Latent Semantic Analysis)

### 1. Bản Chất

- Một ứng dụng cụ thể của SVD cho dữ liệu văn bản
- Mỗi dòng ma trận đại diện cho một văn bản
- Mỗi cột thể hiện tần suất xuất hiện của từ

### 2. Đặc Điểm Xử Lý

- Ma trận thưa, trung bình các cột gần 0
- Tính thưa của ma trận dẫn đến khả năng giảm chiều mạnh mẽ

## IV. So Sánh Chi Tiết

### 1. Điểm Tương Đồng

- Đều là các phương pháp giảm chiều
- Đều sử dụng kỹ thuật phân rã ma trận
- Mục tiêu: Giảm thiểu số chiều mà không mất mát nhiều thông tin

### 2. Điểm Khác Biệt

- PCA: Tập trung vào phương sai, phù hợp với dữ liệu số
- SVD: Phương pháp phân rã ma trận tổng quát
- LSA: Chuyên biệt cho dữ liệu văn bản, khai thác mối quan hệ ngữ nghĩa ẩn

### 3. Ưu Điểm Từng Phương Pháp

- PCA: Giảm nhiễu, trích xuất đặc trưng chính
- SVD: Linh hoạt, áp dụng được cho nhiều loại dữ liệu
- LSA: Phát hiện mối quan hệ ngữ nghĩa tiềm ẩn trong văn bản

## V. Kết Luận

Mỗi phương pháp đều có điểm mạnh riêng và phù hợp với các loại dữ liệu và bài toán khác nhau. Việc lựa chọn phụ thuộc vào bản chất dữ liệu và mục tiêu cụ thể của phân tích.

| **Tiêu chí**                     | **PCA**                                                                                                                                                                                                              | **SVD**                                                                                                                                                                                                                                                                                     | **LSA**                                                                                                                                                                                                                                                                                     |
| -------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Mục đích**                     | - Tìm các thành phần chính (principal components) nhằm giảm chiều dữ liệu.<br>- Giữ lại thông tin phương sai lớn nhất của dữ liệu.                                                                                   | - Phân rã ma trận thành ba ma trận $\\(U, \\Sigma, V^T\\).$<br>- Có thể dùng cho nhiều mục đích, trong đó có giảm chiều dữ liệu (tương tự PCA).                                                                                                                                             | - Áp dụng SVD vào dữ liệu văn bản (ma trận thuật ngữ – văn bản) để trích xuất ngữ nghĩa tiềm ẩn.<br>- Giảm chiều dữ liệu văn bản.                                                                                                                                                           |
| **Nguyên lý cốt lõi**            | - Dịch dữ liệu về trung bình (mean centering), tính ma trận hiệp phương sai (covariance), tìm trị riêng và vector riêng.<br>- Các vector riêng (eigenvectors) ứng với phương sai lớn nhất là các “thành phần chính”. | - Thực hiện phân rã ma trận bất kỳ (có thể là dữ liệu, ma trận hiệp phương sai, v.v.) thành $\\(U \\,Sigma, V^T\\).$<br>- PCA cũng có thể được thực hiện qua SVD của ma trận dữ liệu đã được chuẩn hoá.                                                                                     | - Thực chất là ứng dụng SVD lên ma trận thuật ngữ – văn bản (term-document matrix).<br>- Giữ lại các thành phần có giá trị kỳ dị (singular values) lớn để biểu diễn không gian ngữ nghĩa.                                                                                                   |
| **Quy trình (tóm tắt)**          | 1. Trừ trung bình (center) dữ liệu.<br>2. Tính ma trận hiệp phương sai.<br>3. Tìm trị riêng (eigenvalues) & vector riêng (eigenvectors).<br>4. Chọn các thành phần chính có phương sai cao nhất.                     | 1. Cho ma trận dữ liệu $\\(A\\)$ (có thể chuẩn hoá hoặc không).<br>2. Thực hiện $\\(A = U \times\\ Sigma \times V^T\\)$.<br>3. Chọn số chiều k bằng cách lấy k giá trị kỳ dị lớn nhất trong $\\(\\Sigma\\).$<br>4. Ma trận xấp xỉ hạng k: $\\(A_k = U_k \times \\ Sigma_k \times V_k^T\\).$ | 1. Xây dựng ma trận thuật ngữ – văn bản (term-document matrix).<br>2. Thực hiện SVD trên ma trận này: $\\(A = U \times \\ Sigma \times V^T\\).$<br>3. Chọn k giá trị kỳ dị lớn nhất để tạo không gian ngữ nghĩa k chiều.<br>4. Biểu diễn văn bản/thuật ngữ trong không gian giảm chiều này. |
| **Loại dữ liệu**                 | - Thường dùng cho dữ liệu số (vector).<br>- Đặc biệt hữu ích khi dữ liệu có tương quan cao giữa các chiều.                                                                                                           | - Áp dụng được trên nhiều loại dữ liệu: hình ảnh, văn bản, chuỗi thời gian... miễn là biểu diễn được dưới dạng ma trận.                                                                                                                                                                     | - Thường dùng cho dữ liệu văn bản, ma trận thuật ngữ – văn bản.<br>- Đôi khi cũng áp dụng cho dữ liệu khác nhưng tên gọi phổ biến nhất là LSA trong xử lý ngôn ngữ tự nhiên.                                                                                                                |
| **Khi nào nên dùng**             | - Khi muốn giảm chiều và vẫn giữ lại tối đa phương sai của dữ liệu.<br>- Thường là bước tiền xử lý trong Machine Learning.                                                                                           | - Khi cần phân rã ma trận để hiểu cấu trúc ẩn của dữ liệu.<br>- Khi muốn thực hiện PCA mà không trực tiếp tính ma trận hiệp phương sai.                                                                                                                                                     | - Khi muốn rút trích ngữ nghĩa tiềm ẩn từ dữ liệu văn bản (LSA).<br>- Khi muốn giảm nhiễu, nén thông tin trong văn bản.                                                                                                                                                                     |
| **Kết quả**                      | - Ma trận dữ liệu được chiếu lên không gian ít chiều (các principal components).<br>- Giữ lại thông tin quan trọng nhất (phương sai lớn).                                                                            | - Ba ma trận $\\(U, \\Sigma, V^T\\).$<br>- Có thể xấp xỉ dữ liệu bằng cách bỏ bớt các giá trị kỳ dị nhỏ trong $\\(\\Sigma\\)$.                                                                                                                                                              | - Không gian ngữ nghĩa k chiều (LSA space).<br>- Các văn bản/thuật ngữ được biểu diễn trong không gian này.                                                                                                                                                                                 |
| **Ưu điểm**                      | - Dễ hiểu về mặt toán học.<br>- Giảm chiều hiệu quả khi dữ liệu có tương quan.<br>- Thường được hỗ trợ trong các thư viện ML.                                                                                        | - Linh hoạt, áp dụng cho nhiều bài toán (bao gồm PCA).<br>- Công cụ mạnh để phân rã ma trận, xử lý nhiễu, xấp xỉ hạng thấp.                                                                                                                                                                 | - Giúp phát hiện mối quan hệ ngữ nghĩa tiềm ẩn giữa các từ và văn bản.<br>- Giảm chiều và giảm nhiễu cho dữ liệu văn bản.                                                                                                                                                                   |
| **Hạn chế**                      | - Chỉ xét quan hệ tuyến tính, bỏ qua phi tuyến.<br>- Cần chuẩn hoá (center) dữ liệu trước.                                                                                                                           | - SVD cho dữ liệu lớn có thể tốn chi phí tính toán cao.<br>- Cần xác định số thành phần k tối ưu (tương tự PCA).                                                                                                                                                                            | - Dữ liệu văn bản có thể rất lớn, chi phí tính SVD cao.<br>- Không xử lý tốt các ngữ nghĩa phức tạp (phi tuyến).                                                                                                                                                                            |
| **Liên hệ giữa các phương pháp** | - PCA có thể được xem là SVD của ma trận dữ liệu đã chuẩn hoá (hoặc ma trận hiệp phương sai).                                                                                                                        | - SVD là kỹ thuật tổng quát; PCA là trường hợp riêng khi áp dụng SVD lên dữ liệu chuẩn hoá.                                                                                                                                                                                                 | - LSA thực chất là SVD trên ma trận thuật ngữ – văn bản.                                                                                                                                                                                                                                    |
