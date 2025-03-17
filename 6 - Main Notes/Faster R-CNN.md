2025-03-17 23:01


Tags: [[DeepLearning]], 

# Mask R-CNN

![[Pasted image 20250317230226.png]]

### **1. Đầu vào (Input Image)**

- Hình ảnh đầu vào chứa các đối tượng (ví dụ: người chơi bóng đá).
- Hệ thống sẽ phát hiện và khoanh vùng các đối tượng quan trọng.

### **2. Faster R-CNN - Phát hiện đối tượng**

- **Faster R-CNN** là một mô hình phát hiện đối tượng (object detection).
- Nó sử dụng một phần tử gọi là **RoIAlign** (Region of Interest Align) để trích xuất đặc trưng của các vùng chứa đối tượng.
- Mô hình xác định **hộp giới hạn (bounding box)** và nhãn lớp (**class box**) cho từng đối tượng.

### **3. FCN on RoI - Phân đoạn đối tượng**

- Sau khi phát hiện vùng chứa đối tượng, một mạng **Fully Convolutional Network (FCN)** được áp dụng trên từng vùng.
- FCN giúp phân đoạn chính xác từng pixel thuộc về đối tượng, thay vì chỉ xác định hộp giới hạn.

### **4. Đầu ra (Output Image)**

- Hình ảnh đầu ra chứa các đối tượng được phân đoạn riêng biệt bằng các màu sắc khác nhau.
- Điều này giúp mô hình không chỉ nhận diện mà còn tách biệt chính xác từng phần của đối tượng.

### **Tóm tắt**

- **Faster R-CNN** phát hiện hộp giới hạn đối tượng.
- **Mask R-CNN** mở rộng bằng cách thêm bước **phân đoạn đối tượng**, giúp xác định chính xác đường viền của từng đối tượng.
- Ứng dụng phổ biến: xe tự hành, y tế (phân tích hình ảnh X-quang), nhận diện khuôn mặt, xử lý ảnh tự động.

# References
