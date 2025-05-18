2025-05-16 16:42


Tags: [[tóm tắt FF detection system using WSN and ML]]

# tóm tắt Early FF Detection System Using WSN and DL

**Tóm tắt nội dung:**

**1. Ý tưởng chính:**  
Hệ thống đề xuất nhằm phát hiện sớm cháy rừng chính xác hơn các phương pháp truyền thống, dựa trên sự kết hợp giữa mạng cảm biến không dây (WSN), mô hình học sâu (Deep Learning - DL) và IoT để giám sát và dự đoán cháy rừng theo thời gian thực.

**2. Cách thức thực hiện:**  
- Sử dụng mạng cảm biến cố định/di động, truyền thông LPWAN (LoRa), kết hợp mô hình học sâu phù hợp.
- Hoạt động qua 3 bước:  
  1. **Ước tính rủi ro chung:** Tính toán Chỉ số thời tiết cháy rừng (FWI) dựa trên dữ liệu thời tiết thực tế từ các trạm trong rừng, dùng phương pháp của Canada để tăng độ chính xác, tốc độ và tiết kiệm năng lượng.
  2. **Thu thập dữ liệu & dự đoán cháy:** Các nút cảm biến đo các chỉ số môi trường (nhiệt độ, độ ẩm, áp suất, CO, CO2, PM2.5, PM10…), gửi dữ liệu về trung tâm qua LoRa, lưu trữ trên nền tảng ThingsBoard. DL (RNN, LSTM, GRU) phân tích dữ liệu cảm biến để dự đoán cháy.
  3. **Phản ứng khi phát hiện cháy:** Nếu dự đoán có cháy, UAV sẽ được triển khai để xác minh tại chỗ, có thể gửi cảnh báo tức thời cho người dùng và kích hoạt phương án chữa cháy.

**3. Thành phần phần cứng & phần mềm:**  
- **Nút cảm biến:** Bộ vi xử lý, cảm biến môi trường (BME280, Nova SDS011, MH-Z14A, ZE07-CO), truyền LoRa, dùng pin năng lượng mặt trời, bo mạch Lora32u4.
- **Mạng truyền thông:** Liên kết hình sao giữa nút cảm biến và gateway, dùng LoRa cho truyền xa.
- **Cổng kết nối (Gateway):** Thu thập và đẩy dữ liệu lên Internet.
- **Máy chủ/nền tảng IoT:** Lưu trữ, xử lý, trực quan hóa dữ liệu, quản lý cảnh báo (dùng ThingsBoard).
- **Mô hình học sâu:** RNN, LSTM, GRU – xây dựng bằng Keras, trực quan hóa bằng Tensorboard.

**4. Kết quả đạt được:**  
- Đã đánh giá trên ~2000 mẫu thử nghiệm.
- Tham số CO, PM2.5, CO2, PM10 ảnh hưởng lớn nhất đến dự đoán cháy.
- Các mô hình học sâu nâng cao độ chính xác và ổn định dự báo; trong đó GRU cho kết quả tốt nhất (99,89% chính xác, loss 0.0088, nhanh hơn LSTM, dễ triển khai thiết bị nhỏ).
- LSTM đạt 99,82% (loss 0.0298), RNN đạt 99,77% (loss 0.0062).
- Hệ thống dự kiến mở rộng với nhiều nút cảm biến hơn để cải thiện dữ liệu và tăng khả năng phối hợp.

**Kết luận:**  
Hệ thống đề xuất giúp phát hiện sớm cháy rừng hiệu quả, đặc biệt nhờ áp dụng mô hình học sâu GRU trên nền tảng IoT với mạng cảm biến không dây, cho kết quả chính xác cao và có thể triển khai trên diện rộng.[]()
# References
