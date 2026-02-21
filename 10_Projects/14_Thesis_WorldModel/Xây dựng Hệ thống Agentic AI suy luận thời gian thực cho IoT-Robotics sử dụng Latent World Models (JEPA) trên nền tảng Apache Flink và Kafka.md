1. **Thiết lập luồng (Data Engineering nhẹ):** Dựng Kafka và Flink cục bộ. Viết script Python giả lập việc phát (publish) một bộ dữ liệu chuỗi thời gian hoặc video cảm biến vào Kafka.

2. **Triển khai World Model (Core Data Science):** Sử dụng PyFlink (Flink API cho Python) để load mô hình pre-trained TS-JEPA hoặc V-JEPA 2. Đóng băng (freeze) phần lớn mô hình, chỉ thực hiện inference (suy luận) hoặc fine-tune một lớp nhỏ (ví dụ: Linear Probe) trên luồng dữ liệu.

3. **Lập kế hoạch và Lấy mẫu (Action/Planning):** Lập trình để khi luồng dữ liệu chảy qua, World Model trong Flink sẽ liên tục tạo ra các "dự đoán tương lai" (rollouts). Nếu hệ thống dự đoán có sự cố (ví dụ: nhiệt độ quá nhiệt, quỹ đạo lệch), Agent sẽ kích hoạt tín hiệu cảnh báo hoặc thay đổi hành động