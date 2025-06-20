2025-05-24 21:39


Tags:

# tóm tắt Forest Fire Detection and Notification Method Based on AI and IoT Approaches

### **Phương pháp đề xuất**

Kết hợp **IoT + AI**:

- **Cảm biến MQ-2**: Phát hiện khói/khí → kích hoạt camera
- **Webcam**: Thu thập hình ảnh khi có cảnh báo
- **YOLOv5**: Phân tích ảnh xác nhận có cháy hay không

### **Thu thập dữ liệu**

- **Phần cứng**: Raspberry Pi 4 + cảm biến MQ-2 + webcam Logitech C920
- **Dữ liệu huấn luyện**: Tập ảnh lửa từ nguồn công khai (Robmarkcole, Glenn-Jocher)
- **Tỷ lệ chia**: 75% training / 25% testing

### **Quy trình hoạt động**
![[Pasted image 20250524214954.png]]

1. **MQ-2 phát hiện khói** → kích hoạt camera
2. **Camera chụp ảnh** → gửi lên cloud/máy tính chính
3. **YOLOv5 phân tích** → xác nhận có cháy
4. **Gửi cảnh báo** → bộ phận cứu hỏa xác minh thủ công
5. **Thông báo** → sơ tán trong bán kính 1 dặm nếu xác nhận

### **Triển khai mô hình:**

- **Phần cứng**: Hệ thống sử dụng Raspberry Pi 4 hoặc Arduino làm thiết bị IoT để kết nối và điều khiển cảm biến MQ-2 và camera. Một PC (Windows 10 +  GPU) được sử dụng để chạy mô hình AI (YOLOv5) để phân tích hình ảnh do yêu cầu tính toán. Các thành phần khác bao gồm bộ thu phát, pin, v.v.
- **Mô hình AI (YOLOv5):** Sử dụng mô hình YOLOv5, ban đầu dùng trọng số pre-trained của YOLOv5s, nhưng sau đó đã huấn luyện lại trên tập dữ liệu của riêng họ, sử dụng cả YOLOv5s và YOLOv5x. Việc huấn luyện lại trên YOLOv5x cho kết quả tốt hơn
-  **Truyền dữ liệu**: Dữ liệu từ thiết bị IoT được gửi đến đám mây (cloud) hoặc máy tính. Thông báo và hình ảnh/video được gửi đến bộ phận cứu hỏa qua email (SMTP).
### **Kết quả**

- **Cải thiện** khả năng phát hiện so với YOLOv5 đơn lẻ
- **Giảm báo động sai** nhờ kết hợp cảm biến + AI
- **YOLOv5x** cho kết quả tốt hơn YOLOv5s
- **Phân biệt thành công** cảnh báo giả và cháy thật
- **Hạn chế:** bao gồm thời gian và tài nguyên cần thiết cho việc huấn luyện dữ liệu, cũng như khả năng nhầm lẫn các vật thể màu đỏ (như áo) với lửa.
# References
