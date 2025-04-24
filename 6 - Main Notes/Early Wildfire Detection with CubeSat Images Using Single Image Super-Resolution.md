2025-04-23 22:04


Tags: 

# Early Wildfire Detection with CubeSat Images Using Single Image Super-Resolution

- **Abstract summary**: Bài báo trình bày một phương pháp mới để phát hiện cháy rừng sớm bằng hình ảnh từ vệ tinh CubeSat, kết hợp giữa **deep learning** và **kỹ thuật tăng độ phân giải (super-resolution)**. 
	- Note: **Dữ liệu là ảnh từ vệ tinh Landsat-8**, được xử lý thành ảnh RGB và **giả lập ảnh CubeSat** bằng cách **giảm chất lượng**, rồi **tăng lại độ phân giải bằng Real-ESRGAN**.  **Mục tiêu** là tạo ra một giải pháp có thể áp dụng tốt **cho ảnh CubeSat trong thực tế**
- **Cách tiếp cận:**    
    - Dùng ảnh RGB được tạo từ ảnh Landsat-8 (ban đầu có 10 kênh phổ, sau đó chuyển thành 3 kênh RGB).
    - Ảnh được nâng cấp độ phân giải gấp 4 lần bằng kỹ thuật **Real-ESRGAN**.
    - Áp dụng transfer learning với hai mô hình pre-trained: **MobileNetV2** và **ResNet152V2**.
- **Kết quả:** Việc nâng cấp độ phân giải ảnh giúp tăng độ chính xác, độ nhạy (recall) và f1-score khi phát hiện cháy rừng, tăng khoảng **3–5%** tùy mô hình.
### Introduction Summary
- Nhắc lại về các tác hại của cháy rừng và tính cấp thiết của việc phát triển mô hình phát hiện cháy rừng
- Trình bày lại các phương pháp phát hiện cháy rừng trong quá khứ, có 3 loại:
	- *dựa trên mặt đất (terrestrial-based), trên không (aerial-based) và vệ tinh (satellite-based)*
	- Dạng mặt đất và trên không phổ biến hơn vì chi phí ban đầu và kỹ thuật đơn giản hơn.
	- Tuy nhiên, do số lượng vệ tinh phóng lên tăng mạnh và chi phí giảm, nghiên cứu về vệ tinh đang được đẩy mạnh.
- Trình bày về các ưu điểm của việc sử dụng vệ tinh:
	- Có thể giám sát những khu vực xa xôi, khó tiếp cận.
	- Quan sát liên tục cả vào ban đêm hoặc trong thời tiết xấu.
	- Về lâu dài tiết kiệm chi phí bảo trì so với các phương pháp khác.
- Trình bày cụ thể về những ưu điểm của **CubeSat**:
	 - Giá rẻ, dễ triển khai, mở rộng vùng quan sát trên toàn cầu.
	- Có thể chọn quỹ đạo để theo dõi nhiều nơi hoặc giám sát liên tục một khu vực.
	- Có thể dùng nhiều CubeSat để vượt qua hạn chế về băng thông truyền tín hiệu.
- Những hạn chế của CubeSat: 
- Kích thước nhỏ nên camera payload capacity nhỏ → không thể sử dụng thuật toán so sánh nhiều băng tần như các vệ tinh lớn.
- Khả năng xử lý phần mềm giới hạn → không thể implementing các mô hình deep learning nặng.
- Do đó, cần giải pháp nhẹ, hiệu quả và dùng ít dữ liệu đầu vào.
	- => Bài báo đề xuất dùng kỹ thuật **super-resolution** để cải thiện hiệu quả phát hiện cháy rừng từ ảnh CubeSat, dù bị giới hạn về số băng tần và bộ nhớ.
### Super-resolution technique:
- Kỹ thuật super-resolution sẽ được thực hiện tại trạm ở mặt đất, mà không cần phải thay đổi bất kỳ phần cứng nào của CubeSat
 - Mục tiêu là giúp hệ thống **phát hiện cháy rừng thời gian thực trên toàn cầu bằng CubeSat**.    
- Ưu điểm:    
    - Khắc phục các giới hạn của CubeSat (kích thước nhỏ, băng thông thấp, tải trọng hạn chế).
    - Ảnh RGB từ CubeSat được xử lý nâng cao độ phân giải ở mặt đất → cải thiện chất lượng ảnh.
    - Khi so sánh mô hình học sâu trên ảnh gốc và ảnh đã enhanced, kết quả cho thấy:
        - **Tốc độ học nhanh hơn**
        - **Hiệu suất phát hiện cháy tốt hơn**
### Materials
- Dữ liệu dùng cho training được tiền xử lý từ data Landsat-8
	- Ảnh Landsat-8 có 11 băng tần (multispectral), nhưng loại bỏ band 8 (panchromatic), còn lại 10 band → lưu dưới định dạng TIFF.
- Trong nghiên cứu trước đó:
	- Ảnh được *resize về kích thước 256x256*, với spatial resolution là 30m thì 1 bức ảnh sẽ tương ứng với $59km^2$ diện tích mặt đất 
	![[Pasted image 20250424124416.png]]
	- Dùng kỹ thuật segmentation để tạo fire masks cho ảnh (xem rằng liệu có đang xảy ra 1 vụ cháy nào trong từng pixel không) 
	- Tuy nhiên, gán nhãn thủ công rất khó và tốn thời gian → họ dùng **3 thuật toán phát hiện cháy có sẵn** để tự động tạo nhãn:
		- Schroeder et al.
		- Murphy et al.    
		- Kumar & Roy
	- "Since the three algorithms are not ground truth, they sometimes produce slightly different results", nên họ **xác định một pixel là “cháy” nếu ít nhất 2 thuật toán đồng ý.**
### Preprocessing

# References
