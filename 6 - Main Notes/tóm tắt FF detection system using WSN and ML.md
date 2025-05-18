2025-05-19 03:56


Tags: [[tóm tắt Early FF Detection System Using WSN and DL]]

# tóm tắt FF detection system using WSN and ML

**Tóm tắt nội dung:**

**1. Ý tưởng cốt lõi:**  
- Xây dựng hệ thống phát hiện cháy rừng sớm nhằm giảm thiểu thiệt hại, dựa trên mạng cảm biến không dây (WSN) và kết hợp mô hình máy học để tăng độ chính xác.
- Hệ thống hoạt động độc lập dài hạn nhờ dùng pin sạc và năng lượng mặt trời.

**2. Cách thức thực hiện:**  
- **Kiến trúc hệ thống:**  
  - Gồm các nút cảm biến không dây, đầu cụm (cluster head), trạm gốc (base station).
  - Nút cảm biến được bố trí phủ kín rừng (dạng ô), tự cấu hình, giám sát nhiệt độ, độ ẩm, ánh sáng, CO.
  - Đầu cụm thu thập dữ liệu từ các nút cảm biến và truyền tiếp về trạm gốc.
  - Trạm gốc là nơi kết nối mạng cảm biến với quá trình phân tích dữ liệu.

- **Thiết kế và triển khai nút cảm biến:**  
  - Dạng cầu, chịu lực tốt, cảm biến đặt ở mặt dưới tránh thời tiết xấu.
  - Gồm ba lớp: pin, vi điều khiển (Arduino Nano), bộ thu phát (nrf24L01).
  - Phạm vi mỗi nút 5m, đặt cao 1m trên thân cây, cách nhau 8.66m.
  - Đầu cụm bao vùng bán kính 50m, truyền tối đa 100m, cách nhau 86.66m.

- **Nguồn cấp điện:**  
  - Nút cảm biến và đầu cụm dùng pin lithium-ion 18650, bổ sung bằng pin mặt trời; trạm gốc dùng điện lưới.

- **Truyền dữ liệu:**  
  - Dùng topo cây hoặc cụm-cây, truyền từ nút cảm biến → đầu cụm → trạm gốc.
  - Bộ thu phát chính là nrf24L01, có thể thay bằng LoRa, ZigBee, XBee.

- **Phân tích và phát hiện cháy:**  
  - **Tại nút cảm biến:** Phân tích tỷ lệ ngưỡng (so sánh giá trị hiện tại với 30 giây trước, gửi dữ liệu nếu vượt ngưỡng liên tiếp 3 lần).
  - **Tại trạm gốc:** Phân tích bằng mô hình học máy (hồi quy tuyến tính bội), phân loại bằng K-means (cháy/không cháy), huấn luyện trên 7000 mẫu, 80% train, 20% test.
  - Nếu phát hiện cháy, gửi cảnh báo về điện thoại cho cán bộ quản lý.

**3. Kết quả đạt được:**  
- Đã thử nghiệm thực tế ở rừng nhiệt đới Sri Lanka, test nhiều thời điểm trong ngày.
- Xác định ngưỡng từng thông số qua thử nghiệm:
  - Nhiệt độ: 1.05; Độ ẩm: 0.95; Ánh sáng: 1.15; CO: 0.85.
- Độ chính xác mô hình máy học sau huấn luyện: 81%.
- Độ chính xác thực tế qua thử nghiệm:
  - Nút cảm biến: 80% (100% khi có cháy, 64.28% khi không cháy)
  - Mô hình học máy: 86.84% (86.36% khi có cháy, 80% khi không cháy)
  - Tổng thể hệ thống: 90% (86.36% khi có cháy, 92.85% khi không cháy)
- Phân tích thống kê: cả 4 thông số đều có tương quan mạnh với cháy rừng (p < 0.001).
- Hệ thống giúp cảnh báo nhanh hơn, chính xác hơn các hệ thống hiện tại trong điều kiện rừng thực tế.

# References
