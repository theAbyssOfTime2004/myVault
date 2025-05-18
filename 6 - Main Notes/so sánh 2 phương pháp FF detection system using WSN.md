2025-05-19 03:57


Tags: [[tóm tắt FF detection system using WSN and ML]], [[tóm tắt Early FF Detection System Using WSN and DL]]

# so sánh 2 phương pháp FF detection system using WSN

### So sánh hai phương pháp phát hiện cháy rừng

#### 1. Điểm giống nhau

- **Mục tiêu chung:**
  - Cả hai đều hướng tới phát hiện cháy rừng sớm nhằm giảm thiểu thiệt hại.
- **Công nghệ nền tảng:**
  - Đều sử dụng mạng cảm biến không dây (WSN) để giám sát các thông số môi trường trong rừng.
  - Hệ thống cảm biến đều có khả năng hoạt động dài hạn nhờ sử dụng pin sạc kết hợp năng lượng mặt trời.
- **Các thông số môi trường giám sát:**
  - Đều đo các chỉ số như nhiệt độ, độ ẩm, khí CO (và ánh sáng ở phương pháp 2, PM2.5/PM10, CO2 ở phương pháp 1).
- **Tự động cảnh báo:**
  - Hệ thống đều có khả năng gửi cảnh báo đến các đơn vị/cá nhân có trách nhiệm khi phát hiện cháy.
- **Có phân tích dữ liệu cảm biến, không chỉ dựa vào giá trị ngưỡng mà còn ứng dụng phân tích/học máy để tăng độ chính xác phát hiện.

#### 2. Khác biệt chính

| Tiêu chí                       | Phương pháp 1 (DL, IoT, GRU)                                                                | Phương pháp 2 (Threshold + ML truyền thống)                                                          |
| ------------------------------ | ------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| **Giải thuật phân tích**       | Học sâu (Deep Learning: GRU, LSTM, RNN)                                                     | ML truyền thống (Linear Regression, K-means)                                                         |
| **Chỉ số cảm biến**            | Đa dạng hơn: nhiệt độ, độ ẩm, áp suất, CO, CO2, PM2.5, PM10, bức xạ mặt trời, tốc độ gió... | Ít hơn: nhiệt độ, độ ẩm, ánh sáng, CO                                                                |
| **Kiến trúc truyền thông**     | Dùng LoRa, LPWAN, gateways, kết nối Internet (IoT, ThingsBoard)                             | nrf24L01, ZigBee, LoRa, XBee, topo cây/cụm-cây, chỉ cần trạm gốc (không nhất thiết phải có Internet) |
| **Phân tích dữ liệu cảm biến** | Tập trung xử lý tập trung trên server, mô hình DL huấn luyện với dữ liệu lớn (2000 mẫu)     | Phân tích sơ bộ tại nút (dựa ngưỡng); gửi lên trạm gốc để phân tích ML (7000 mẫu)                    |
| **Khả năng mở rộng**           | Thiết kế cho triển khai quy mô lớn, phối hợp nhiều nút và UAV                               | Phù hợp cho quy mô nhỏ hoặc trung bình, không nhấn mạnh UAV hoặc mở rộng                             |
| **Tính năng bổ sung**          | Có UAV hỗ trợ xác minh cháy, lập bản đồ nhiệt                                               | Không đề cập UAV, chủ yếu cảnh báo qua tin nhắn                                                      |
| **Độ chính xác đạt được**      | GRU: 99.89%, LSTM: 99.82%, RNN: 99.77%                                                      | ~90% tổng thể (86.84% khi có cháy, 92.85% khi không cháy)                                            |
| **Phản hồi dữ liệu**           | Dashboard trực quan, cảnh báo real-time, tích hợp IoT                                       | Chủ yếu cảnh báo cho cán bộ qua tin nhắn                                                             |

#### 3. Hạn chế của từng phương pháp

- **Phương pháp 1 (DL, IoT, GRU):**
  - Đòi hỏi hạ tầng IoT, gateway, máy chủ Internet ⇒ chi phí đầu tư, vận hành cao hơn.
  - Cần kết nối Internet ổn định, có thể gặp khó khăn ở rừng sâu hẻo lánh.
  - Đào tạo mô hình học sâu cần tập dữ liệu lớn và tài nguyên tính toán mạnh.
  - Cảm biến đa dạng hơn nên chi phí phần cứng cao.

- **Phương pháp 2 (Threshold + ML truyền thống):**
  - Độ chính xác thấp hơn, dễ nhầm lẫn khi điều kiện môi trường thay đổi bất thường (độ chính xác nút cảm biến khi không cháy chỉ đạt ~64%).
  - Phân tích ML chỉ dùng Linear Regression, K-means – không tận dụng được sức mạnh của DL cho các quan hệ phức tạp.
  - Không có cơ chế xác minh lại (như UAV), dễ bị báo động giả.
  - Chủ yếu cảnh báo cho cán bộ, thiếu dashboard trực quan và khả năng mở rộng IoT.
  - Chỉ đo được ít tham số môi trường, dễ bỏ sót các yếu tố quan trọng khác (như bụi mịn, CO2…).

#### 4. Tổng kết

- Phương pháp 1 hiện đại hơn, độ chính xác cao, khả năng mở rộng tốt, tích hợp nhiều công nghệ (IoT, DL, UAV), nhưng chi phí đầu tư và vận hành cao hơn.
- Phương pháp 2 đơn giản hơn, dễ triển khai ở vùng sâu vùng xa, chi phí thấp, nhưng độ chính xác chưa cao, ít tính năng bổ sung, khó mở rộng hoặc tích hợp thêm công nghệ mới.


# References
