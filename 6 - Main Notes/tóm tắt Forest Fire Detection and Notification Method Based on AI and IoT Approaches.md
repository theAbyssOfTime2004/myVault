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

1. **MQ-2 phát hiện khói** → kích hoạt camera
2. **Camera chụp ảnh** → gửi lên cloud/máy tính chính
3. **YOLOv5 phân tích** → xác nhận có cháy
4. **Gửi cảnh báo** → bộ phận cứu hỏa xác minh thủ công
5. **Thông báo** → sơ tán trong bán kính 1 dặm nếu xác nhận

### **Kết quả**

- **Cải thiện** khả năng phát hiện so với YOLOv5 đơn lẻ
- **Giảm báo động sai** nhờ kết hợp cảm biến + AI
- **YOLOv5x** cho kết quả tốt hơn YOLOv5s
- **Phân biệt thành công** cảnh báo giả và cháy thật

# References
