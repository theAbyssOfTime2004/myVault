2025-05-16 16:42


Tags:

# tóm tắt Early FF Detection System Using WSN and DL

### **Tóm tắt methodology**:
- Các công trình liên quan (Background and Related Work):
	- Fire Weather Index - FWI 
		- Chỉ số ước tính mức độ rủi ro xảy ra cháy rừng cho một khu vực dựa trên ngữ cảnh thời tiết
		- Có hai phương pháp chính được sử dụng phổ biến: phương pháp của Hàn Quốc và phương pháp của Canada. 
		- phương pháp của Canada được lựa chọn trong nghiên cứu này vì nó được chứng minh là chính xác hơn, nhanh hơn và tiêu thụ ít năng lượng hơn
		- FWI của Canada gồm sáu thành phần, tính toán dựa trên các quan sát hàng ngày liên tiếp về nhiệt độ, độ ẩm tương đối, tốc độ gió và lượng mưa trong 24 giờ trước đó
		- Dữ liệu thời tiết cần được thu thập liên tục
	- Wireless Sensor Network (WSN)
	- Hệ thống IoT + LoRa:
		- Hệ thống IoT bao gồm nhiều thành phần như thiết bị kết nối, mạng không dây, nền tảng thu thập/xử lý dữ liệu, các ứng dụng và hệ thống giám sát - bảo mật
		- thiết bị kết nối thu thập data từ sensors -> xử lý data -> truyền qua mạng không dây -> thực hiện hành động, diễn ra trực tiếp trên các thiết bị và yêu cầu nguồn điện
		- bởi vì mạng đô thị (urban network) không phủ sóng khắp các rừng -> gây khó khăn cho việc thiết lập hệ thống IoT
			- => để giải quyết -> sử dụng LoRa là công nghệ truyền thông tầm xa với mức tiêu thụ năng lượng thấp
		- Dữ liệu từ gateway được gửi lên Internet qua MQTT, lưu trữ trên ThingsBoard và hiển thị trên dashboard. Khi phát hiện cháy, hệ thống sẽ gửi cảnh báo ngay lập tức cho người dùng qua Telegram.

# References
