2025-05-02 19:26


Tags:

# Early Detection of Forest Fire Using Mixed Learning Techniques and UAV

### Introduction:
- address cháy rừng ngày càng gia tăng do *nạn phá rừng và biến đổi khí hậu* => nêu ra hệ quả xấu đến môi trường => việc *phát hiện cháy rừng sớm là cần thiết*
	#### Giải pháp đề xuất: 
	- Bài báo đề xuất mô hình deep learning kết hợp giữa: 
		- **YOLOv4 Tiny**: một mô hình nhận diện đối tượng nhẹ, nhanh.
	    - **LiDAR**: công nghệ đo khoảng cách bằng laser để tạo bản đồ 3D.
	- Được tích hợp trên UAV để tuần tra, phát hiện và theo dõi cháy rừng 
	#### Ưu Điểm: 
	- **Tốc độ phân loại nhanh**: chỉ mất khoảng **1.24 giây**.
	- **Độ chính xác cao**: **91%**, với **F1 score là 0.91**.
	- **Phát hiện theo thời gian thực**, có thể truyền dữ liệu về trạm mặt đất.
	- Áp dụng được trong nhiều kiểu rừng: **rừng rậm, rừng mưa**,…
	#### Hạn chế của các phương pháp cũ
	- **Ảnh vệ tinh**: độ phân giải thấp, không theo dõi được theo thời gian thực, cần xử lý trước khi khảo sát lại.
	- **Mạng cảm biến không dây (WSNs)**: bị hạn chế do dễ hỏng khi cháy, cần cơ sở hạ tầng, khó mở rộng và bảo trì.
	#### Tại sao dùng UAV?
	- UAV có **chi phí thấp, linh hoạt, hoạt động độc lập**, và có thể bay qua nhiều khu vực để **phát hiện cháy hiệu quả hơn** các phương pháp truyền thống như máy bay giám sát hoặc tháp canh.
	####  Mục tiêu của nghiên cứu
	- Phát triển một hệ thống UAV tích hợp AI có thể:
		- **Phát hiện cháy rừng và phạm vi cháy**.
		- **Tạo mô hình 3D của khu vực cháy**.
		- **Giám sát cháy ở vùng thấp và rừng rậm**.
### Related Works
- Hiện nay, cháy rừng và khói được phát hiện thông qua **các phương pháp cảm biến từ xa** như:
	- **Ảnh vệ tinh**    
	- **Camera tĩnh độ phân giải cao gắn trên mặt đất**    
	- **Máy bay không người lái (UAV)**
	#### Hạn chế của từng phương pháp:
	-   *Ảnh vệ tinh*:
		- **Độ phân giải thấp**, khó xác định chính xác vị trí cháy.    
		- Không theo dõi **liên tục theo thời gian thực**.
		- **Ảnh hưởng bởi thời tiết**: mây, sương mù làm hình ảnh bị nhiễu.
	-  *Camera + cảm biến mặt đất (nhiệt độ, khói, độ ẩm)*:
		- **Chỉ hiệu quả ở môi trường kín hoặc gần đám cháy**.    
		- **Phạm vi quan sát hạn chế**, muốn mở rộng thì phải lắp thêm cảm biến → **tốn kém**.
	-  *Máy bay không người lái (UAV)*:
		- Có thể bao phủ diện rộng.    
		- Cho ảnh **chất lượng cao theo thời gian thực**.    
		- **Chi phí vận hành thấp hơn nhiều** so với các phương pháp truyền thống.
	#### Các mô hình đã được nghiên cứu và ứng dụng: 
	-  *YOLOv4 + UAV*:
		- Được dùng để nhận dạng cháy từ ảnh trên không.    
		- Tốc độ xử lý khung hình: **3.2 fps**.    
		- **Độ chính xác: 83%** (hiệu quả với đám cháy lớn, nhưng yếu với cháy nhỏ).
	- *YOLOv5 + EfficientDet*:
		- Dùng **NetImage classifier**, tập dữ liệu gồm 10,581 ảnh.
		- Đạt độ chính xác **99.6% với ảnh cháy rõ** và **99.7% với ảnh dễ gây nhầm lẫn**.
		- **Nhược điểm**: **Không phát hiện được khói**, là dấu hiệu sớm của cháy rừng.
	# References
