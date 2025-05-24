2025-05-19 14:26


Tags:

# tóm tắt bài báo 1.pdf
**Tóm tắt nội dung bài báo:**

**Ý tưởng chính:**
- Bài báo giới thiệu một hệ thống tích hợp Trí tuệ Nhân tạo (AI) với công nghệ IoT năng lượng thấp, nhằm tăng cường giám sát môi trường rừng và đặc biệt là phát hiện, dự báo cháy rừng sớm thông qua phân tích chuỗi thời gian.
- Hệ thống này nhằm thay thế, cải tiến các phương pháp hiện tại, đáp ứng nhu cầu cấp bách về phòng chống cháy rừng.

**Cách thức thực hiện:**
- ![[Pasted image 20250524214301.png]]
- Sử dụng các nút cảm biến *giá rẻ (BME280)* để thu thập dữ liệu nhiệt độ, độ ẩm, áp suất tại rừng xa xôi.
- Dữ liệu được truyền qua công nghệ LoRa (truyền xa, tiết kiệm năng lượng) về gateway, sau đó chuyển lên mạng (The Things Network), truy cập qua giao thức MQTT.
- Đánh giá chất lượng dữ liệu cảm biến thông qua chỉ số *RSSI và SNR*.
- Dữ liệu thực tế liên tục được đối chiếu với dữ liệu khí tượng từ Met Éireann để xác thực và hiệu chỉnh, hỗ trợ phân tích chuỗi thời gian.
- Phân tích chuỗi thời gian được thực hiện bằng mô hình ARIMA (là một kỹ thuật **dự báo chuỗi thời gian** đơn giản, phù hợp triển khai thiết bị biên (edge device), xử lý tốt dữ liệu môi trường không ổn định).
	- Khi phát hiện bất thường trong chuỗi thời gian, hệ thống kích hoạt mô hình cây quyết định (Decision Tree) để đánh giá nguy cơ cháy rừng dựa trên dữ liệu môi trường và bộ dữ liệu rủi ro.
- ![[Pasted image 20250524213547.png]]
**Kết quả đạt được:**
- Hệ thống đã được phát triển và kiểm thử thành công.
- Dữ liệu cảm biến thu thập được đã được xác thực tốt khi so với dữ liệu khí tượng khu vực, đảm bảo độ chính xác.
- Mô hình ARIMA dự báo hiệu quả nhiệt độ và áp suất, kết quả dự đoán sát với thực tế (có khoảng tin cậy 95%).
	- ![[Pasted image 20250524213732.png]]
- Biểu đồ ACF, PACF cho thấy ARIMA ưu tiên dữ liệu gần để dự đoán các mẫu động của môi trường.
	- Biểu đồ ACF và PACF cho thấy rằng **các giá trị trong thời gian gần** (1–2 ngày trước) **liên quan chặt chẽ hơn** đến hiện tại, nên **ARIMA ưu tiên dùng các giá trị này để dự báo**. Điều này đặc biệt quan trọng khi giám sát môi trường, nơi các thay đổi có tính chất **instant and dynamical**.
	- ![[Pasted image 20250524213759.png]]
- Hệ thống đã tích hợp thành công Decision Tree để đánh giá nguy cơ cháy từ dữ liệu thời gian thực.
- Tuy nhiên, việc xác thực hiệu quả dự đoán cháy rừng cuối cùng của toàn hệ thống vẫn là nhiệm vụ tương lai; kết quả hiện tại mới tập trung vào thu thập, xác thực dữ liệu và dự báo các tham số môi trường bằng ARIMA.


# References
