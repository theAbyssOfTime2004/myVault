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
	- *Phương pháp phát hiện chá rừng dựa trên image processing*
		- **1. Xác định các hot objects**
			- Phân tích ảnh để tìm những vùng **có độ sáng cao**.
			- Những vùng này được gọi là **"candidate regions"** 
		- **2. Phân tích chuyển động: Optical Flow**
			- **Tính toán motion vectors** của các candidate regions bằng kỹ thuật **optical flow** – dùng để xác định sự thay đổi vị trí của pixel qua từng khung hình video.
			- Điều này giúp phân biệt **ngọn lửa (chuyển động bất quy tắc)** với các vật thể sáng **nhưng đứng yên** như ánh nắng phản chiếu.
		- **3. Theo dõi ngọn lửa qua ảnh hồng ngoại (IR)**
			- Sử dụng kỹ thuật:
			    - **Blob counter**: Đếm và theo dõi cụm điểm (blob) có hình dạng giống ngọn lửa.
			    - **Morphological operations**: Làm sạch và cải thiện vùng ảnh đã tách (như làm tròn, loại bỏ nhiễu nhỏ).
		 - **4. Phân biệt nền và chuyển động với ViBe**
			- **ViBe (Visual Background Extractor)**: Kỹ thuật trích xuất nền từ video để phân biệt vùng chuyển động mới (tức đám cháy) khỏi vùng nền tĩnh.
			- Phân tích **sự khác biệt giữa các khung hình liên tiếp** để xác định khu vực có chuyển động lạ.
		 - **5. Các kỹ thuật xử lý ảnh hỗ trợ**
			- **Median filtering**: Làm mượt ảnh, loại bỏ nhiễu.
			- **Color space conversion**: Chuyển đổi không gian màu để phân tích tốt hơn (ví dụ từ RGB sang HSV).
			- **Otsu threshold segmentation**: Phân ngưỡng tự động để tách vùng sáng (có thể là lửa).
			- **Morphological operations & Blob counter**: Làm rõ và đếm vùng cháy.
		-  **6. Kết hợp đặc trưng tĩnh và động để phát hiện lửa & khói**
			- **Static features**: Độ sáng, màu sắc.    
			- **Dynamic features**: Vector chuyển động, thay đổi qua khung hình.  
		    => Kết hợp hai loại đặc trưng này giúp hệ thống phát hiện **chính xác cả lửa và khói**, kể cả khi mới bắt đầu.
	 * *Sử dụng Caffemodel - Deep Learning*:
		 - Caffemodel là một mô hình học sâu (deep learning) được sử dụng để **phát hiện vùng cháy và khói**.
		- Ngoài việc nhận diện đơn giản, mô hình còn **phân tích mức độ bất quy tắc** (đặc trưng dao động, mờ ảo) của lửa và khói để tăng độ chính xác.    
		- Mỗi khung hình video được chia thành **lưới 16 × 16**, từ đó ghi lại **tần suất xuất hiện** của các vùng khói/lửa → giúp xác định vị trí gốc của đám cháy và **giảm false alarm**.
	* *Phát hiện khói bằng fuzzy logic + extended version of Kalman filter*
		- Các nghiên cứu khác sử dụng **fuzzy logic** để phân đoạn và phát hiện khói => phù hợp với các tín hiệu **mờ, không rõ ràng** như khói.
		- Để bù trừ ảnh hưởng của **điều kiện môi trường thay đổi** (gió, ánh sáng), **bộ lọc Kalman mở rộng (Extended Kalman Filter)** được dùng để điều chỉnh đầu vào cho fuzzy logic → tăng độ tin cậy trong phát hiện khói.
	- *Phát hiện cháy rừng bằng camera gắn trên UAV*
		- UAV (drone) được gắn **camera thường và camera hồng ngoại** để ghi hình đám cháy từ trên không.
		- Ảnh thu được kết hợp với **thông tin địa hình và dữ liệu thời tiết** → giúp giảm tỷ lệ báo động giả.
		- Đề xuất một chỉ số mới tên là **Forest Fire Detection Index (FFDI)** → dùng để phân biệt rõ vùng có cháy dựa vào phân loại thực vật và màu sắc của lửa/khói.    
		- **Độ chính xác** đạt được là **96.82%**, tốc độ xử lý mỗi ảnh khoảng **0.447 giây**, tốc độ video lên đến **54 khung hình/giây**.
	- *Fire-Net - Mô hình deep learning dùng ảnh vệ tinh*
		- Fire-Net **là một deeplearning framework** được huấn luyện trên ảnh từ vệ tinh **Landsat-8**.
		- Sử dụng cả thông tin **quang học (optical)** và **nhiệt (thermal)** để phát hiện cháy và thực vật bị đốt.    
		- Mô hình này có **khả năng phát hiện cháy nhỏ**, độ chính xác tổng thể đạt **97.35%**.
	- *Hệ thống UAV kép - reducing false alarms*
			- Sử dụng **2 loại UAV**:
			    - **Fixed-wing drone**: bay tầm cao (350–5,500m), phát hiện ban đầu và báo động.
			    - **Rotary-wing drone**: bay thấp hơn, đến kiểm tra lại tại vị trí GPS được cảnh báo → xác nhận có cháy thật hay không.
		- Mục tiêu: **giảm báo động giả nhờ kiểm chứng hai bước**.
	- *Đề xuất mô hình kết hợp 3D modeling + YOLOv4 + Otsu + LiDAR*
		- Mô hình được đề xuất kết hợp nhiều kỹ thuật:
		    - **3D modeling**: Tái dựng không gian 3 chiều giúp phát hiện chính xác hơn.        
		    - **YOLOv4**: Phát hiện vật thể nhanh và mạnh.        
		    - **Otsu thresholding**: Xác định ngưỡng để phân biệt giữa nền và vật thể cháy.        
		    - **LiDAR**: Đo khoảng cách giữa các cây và vật thể để xác định hướng ảnh và định vị đám cháy chính xác.
		- Mục tiêu cuối cùng là **nâng cao độ chính xác và khả năng phát hiện sớm cháy rừng**.
### Proposed Methodology
- Fig 1 trình bày quy trình hoạt động của hệ thống UAV. Khi UAV bay tuần tra, nó sẽ thu thập dữ liệu liên tục từ các sensors: camera RGB để *capture video*, cảm biến hồng ngoại IR để *ghi nhận ảnh/phát xạ nhiệt* của khu rừng, kèm theo *đo vận tốc và hướng gió* từ cảm biến anemometer.
- Tất cả dữ liệu hình ảnh sẽ được đưa vào YOLOv4-Tiny được tích hợp trên onboard cpu của UAV
- YOLOv4-Tiny sẽ phân tích ảnh, phát hiện vị trí có lửa hoặc khói dựa trên bounding box quanh vùng cháy. Nếu **không phát hiện lửa** từ ảnh, hệ thống sẽ kiểm tra xem có các vật liệu dễ cháy hay dấu hiệu nguy cơ nào (như khói mờ) không: nếu có, UAV ước lượng khả năng xảy ra cháy trong khu vực đó và thông báo kết quả cho trạm mặt đất. Nếu **phát hiện lửa**, UAV sẽ tự động điều khiển (visual servoing) tiến đến khu vực cháy và bay lòng vòng quanh nơi có lửa để theo dõi nhiệt độ đám cháy và phạm vi lan rộng

# References
