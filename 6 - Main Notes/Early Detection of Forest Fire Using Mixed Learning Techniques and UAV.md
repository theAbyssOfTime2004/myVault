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
# References
