2025-01-15 01:02


Tags: [[Neural Network]], [[DeepLearning]], 

# Neural Network

### Tổng quan về neural network
- Artificial Neural Network là mô hình xử lý thông tin được mô phỏng dựa trên hoạt động của hệ thần kinh sinh vật
- Bao gồm số lượng lớn các neural được gắn kết để xử lý thông tin
- Artificial Neural Network giống như não người, được học bởi kinh nghiệm thông qua huấn luyện, có khả năng lưu trữ tri thức và sử dụng chúng trong việc dự đoán những dữ liệu chưa biết
### Natural Neurons 
- Natural neurons nhận tín hiệu thông qua các khớp thần kinh (synapses) trên các cấu trúc hình cây (dendrites) hoặc các màng (membrane) của tế bào thần kinh (neuron).
- Khi các tín hiệu nhận được đủ mạnh (vượt qua  1 ngưỡng nào đó), các neuron sẽ được kích hoạt và truyền 1 tín hiệu thông qua axon (nerve fibre).
- Tín hiệu này có thể truyền đến synapse khác và có kích hoạt tiếp những neuron khác.
![[Pasted image 20250115011452.png]]
### Cấu trúc của 1 neuron nhân tạo
- Một neurn nhân tạo (artificial neuron) bao gồm 3 thành phần chính:
	- Input (giống như synapses): được nhân bởi các trọng số (weights), mô tả độ lớn của tín hiệu.
	- Các inputs sau đó được tính toán thông qua một hàm toán học để xác định sự kích hoạt của neuron.
	- Mạng neuron nhân tạo sẽ kết hợp nhiều artificial neuron như thế để tiến hành xử lý thông tin. Kết quả xử lý của một neuron có thể làm input cho một neuron khác.
	![[Pasted image 20250115011659.png]]
- Các đơn vị xử lý (processing elements) của một artificial neuron network là những neuron.
- Một artificial neuron network bao gồm 3 thành phần chính: input layer, hidden layer và output layer
![[Pasted image 20250115011805.png]]

### Quá trình xử lý thông tin của ANN.
![[Pasted image 20250115012132.png]]

- Ví dụ: xét hệ thống đánh giá mức độ rủi ro cho vay trong ngân hàng
-  **Inputs**: Là các thuộc tính của dữ liệu, ví dụ: thu nhập, nghề nghiệp, giới tính (trong đánh giá rủi ro cho vay).
- **Outputs**: Kết quả từ mạng neuron, ví dụ: quyết định "cho vay" hay "không cho vay".
- **Trọng số liên kết**: Biểu thị mức độ quan trọng của mỗi input đối với quá trình xử lý dữ liệu qua các layer trong mạng neuron.
- **Hàm tổng**: Tính tổng các input nhân với trọng số của chúng. Công thức:
$$
Y_{j} = \sum_{i=1}^{n} w_{ij} x_{i}
$$
- **Hàm chuyển đổi (transformation function)**: Xác định mối quan hệ giữa **kích hoạt bên trong (internal activation)** và **output** của neuron.
- **Chức năng**: Quyết định liệu output của neuron có được truyền đến layer tiếp theo hay không.
- **Hàm phổ biến**:
    - Hàm **sigmoid**: Chuẩn hóa output về khoảng [0,1], thường dùng vì tính phi tuyến.
    - Xử lý các giá trị kích hoạt lớn trước khi truyền tiếp.
- **Giá trị ngưỡng (threshold)**: Kiểm soát output của neuron. Nếu nhỏ hơn ngưỡng, neuron không truyền output đến layer tiếp theo.

# References
