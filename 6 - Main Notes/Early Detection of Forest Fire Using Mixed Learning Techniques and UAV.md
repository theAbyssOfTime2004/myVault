2025-05-02 19:26


Tags:

# Early Detection of Forest Fire Using Mixed Learning Techniques and UAV

### 1. Introduction:
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
### 2. Related Works
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
### 3. Proposed Methodology
**3.1 Autonomous Drone Routing**
- Fig 1 trình bày quy trình hoạt động của hệ thống UAV. Khi UAV bay tuần tra, nó sẽ thu thập dữ liệu liên tục từ các sensors: camera RGB để *capture video*, cảm biến hồng ngoại IR để *ghi nhận ảnh/phát xạ nhiệt* của khu rừng, kèm theo *đo vận tốc và hướng gió* từ cảm biến anemometer.
- Tất cả dữ liệu hình ảnh sẽ được đưa vào YOLOv4-Tiny được tích hợp trên onboard cpu của UAV
- *fig 1: proposed architecture flow*![[Pasted image 20250503135255.png]]
	1. **Bắt đầu & Thu thập Dữ liệu:** UAV bắt đầu tuần tra rừng, thu thập dữ liệu hình ảnh, nhiệt độ (IR), và tốc độ/hướng gió.
	2. **Xử lý Ban đầu:** Dữ liệu được xử lý bằng mô hình Deep Learning để giám sát và gửi thông tin về trạm mặt đất.
	3. **Phát hiện Cháy? :**
	    - **Nếu KHÔNG có cháy:** UAV kiểm tra xem có vật liệu dễ cháy không.
	        - Nếu CÓ vật liệu dễ cháy: Dự đoán nguy cơ cháy, thông báo cho trạm mặt đất, rồi tiếp tục tuần tra.
	        - Nếu KHÔNG có vật liệu dễ cháy: Tiếp tục tuần tra.
	    - **Nếu CÓ cháy:**
	        - **Thông báo Ngay:** Gửi cảnh báo phát hiện cháy đến trạm mặt đất.
	        - **Quyết định Chế độ Bay:** Chọn bay tự động (Autonomous) hay điều khiển từ xa (RC).
	            - **Bay Tự động:** UAV tự phân tích, chia vùng cháy (lõi, giữa, rìa), tạo mô hình 3D của khu vực cháy để mô phỏng, và liên tục giám sát (bay lượn, đo nhiệt độ).
	            - **Bay RC:** Người điều khiển lái UAV đến vị trí cháy và thực hiện các biện pháp nghiệp vụ.
	        - **Truyền Dữ liệu Chi tiết:** Gửi toàn bộ dữ liệu (phân vùng, mô hình 3D, dự báo thời gian thực) về trạm mặt đất.
	4. **Lưu trữ:** Toàn bộ dữ liệu thu thập và xử lý trong quá trình được lưu vào cơ sở dữ liệu.
	**Tóm lại:** UAV tuần tra rừng, dùng AI để phát hiện cháy hoặc nguy cơ cháy. Nếu không có cháy, nó đánh giá rủi ro và tiếp tục tuần tra. Nếu có cháy, nó thông báo ngay, sau đó (thường là tự động) phân tích chi tiết đám cháy (vùng, 3D), liên tục gửi dữ liệu cập nhật về trạm mặt đất, và cuối cùng lưu trữ mọi thông tin.
- *fig 2: Categorization of navigation features of UAV* ![[Pasted image 20250503135710.png]]
	- Hệ thống định vị điều hướng của UAV được phân thành ba nhóm tính năng chính (Awareness, Basic Navigation, Expanded Navigation) như sơ đồ phân cấp ở *fig2* 
		- **Awareness (Nhận thức)**: UAV liên tục thu thập thông tin về môi trường xung quanh (các chướng ngại, khoảng cách đến vật cản) bằng các cảm biến nội bộ. Ví dụ, “semantic evaluation” giúp nhận biết loại chướng ngại (cây cối, chim, khói, v.v.), “block detection” và “block distinction” xác định và phân biệt các vật cản ngay gần UAV) 
		- **Basic Navigation (Điều hướng cơ bản)**: cung cấp chức năng bay tự động tối thiểu để tránh va chạm và di chuyển an toàn. Các tính năng này gồm điều khiển drift tự động (autonomous drift), né tránh va chạm (collision evasion) với chim, cây, cột điện…, và tự động cất cánh/hạ cánh (auto take-off/landing) khi cần.
		- **Expanded Navigation (Điều hướng mở rộng)**: bao gồm các kỹ thuật tiên tiến như lập lộ trình bay (pathway generation) và đánh giá môi trường xung quanh (neighbourhood detection) nhằm xây dựng bản đồ bay ảo. Ví dụ, nó có thể tạo đường bay tối ưu qua các khu rừng phức tạp, cân nhắc địa hình cao độ (depth deployment) hoặc các chuyển động bay phi tuyến (non-linear drift) cho nhiệm vụ tuần tra nhiều ngày. 
	=> Tóm lại, ba nhóm này bổ sung lẫn nhau: nhóm Awareness cho *surrouding awareness tại chỗ*, Basic đảm bảo *bay an toàn* , Expanded *nâng cao khả năng tự chủ và lập kế hoạch bay phức tạp*.
	- **Đối với việc navigating trong khu vực không có GPS**: 
		- Trong rừng rậm, UAV dùng thuật toán **SLAM** để vừa tự xây dựng bản đồ môi trường xung quanh, vừa xác định vị trí của mình trên bản đồ đó bằng cách nhận diện các điểm mốc (landmarks), giúp nó điều hướng mà không cần tín hiệu GPS.
- *fig3: Structure of main modules* ![[Pasted image 20250503142817.png]]
- Hệ thống định vị bằng hình ảnh của UAV hoạt động qua hai giai đoạn chính, dựa trên ba modules:
	- **Hybrid Feature Extraction:** Module này kết hợp hai phương pháp trích xuất đặc trưng khác nhau (ví dụ từ các thang đo hoặc thuật toán khác nhau) để xác định các điểm đặc trưng từ hình ảnh cảm biến ở hai cấp độ khác nhau. Ví dụ, có thể dùng phối hợp các bộ phát hiện corner và phát hiện texture, nhằm thu được thông tin cả vi mô và vĩ mô của cảnh vật. Kết quả là các hybrid features thu được.
	- **Generating Map:** Các hybrid features thu được được nén và đánh giá trong initial hybrid map và cuối cùng thành final hybrid map. Cụ thể, hệ thống sử dụng info-theoretic filter để chọn ra những đặc trưng có ý nghĩa nhất trong môi trường. Sau đó, thuật toán mã feature compression sẽ mã hóa những đặc trưng này thành các code words và lưu trữ dưới dạng bản đồ đặc trưng của khu vực.    
	- **Hybrid Localization:** Trong pha định vị, UAV so sánh các đặc trưng quan sát (từ dữ liệu cảm biến hiện tại) với bản đồ đã tạo. Nó thực hiện topological matching giữa các điểm ảnh quan sát và node của hybrid map, kết hợp với phương pháp nội suy/tam giác (feature triangulation) để suy toán vị trí chính xác của UAV. Nhờ đó, ngay cả khi GPS không khả dụng, UAV vẫn có thể xác định vị trí tương đối so với các mốc đã trích xuất trong bản đồ. Nói chung, hệ thống kết hợp đồng thời dữ liệu cảm biến (thị giác, cảm biến quán tính, v.v.) với bản đồ đặc trưng để định vị UAV theo hybrid localization.
	- **Tóm lại:** Luồng hoạt động là: UAV bay, quan sát, trích xuất đặc trưng, đánh giá, nén và xây dựng một bản đồ đặc trưng của môi trường. Sau đó, khi cần biết vị trí, nó lại quan sát, trích xuất đặc trưng, so sánh với bản đồ đã xây dựng, và từ đó tính ra vị trí hiện tại của mình.
*fig 4 and table 1: Technical information of UAV* ![[Pasted image 20250503182447.png]] ![[Pasted image 20250503182515.png]]
 - Phần này trình bày các thông số kỹ thuật chính của UAV, tập trung vào hiệu suất bay và khả năng mang tải:
	- **Trọng lượng cất cánh tối đa (MTOW):** Được dùng để đánh giá khả năng mang tải ở các độ cao.
	- **Tải trọng (Payload):** UAV có thể mang 6,825 gram thiết bị.
	- **Thời gian bay:** Hoạt động được 107 phút khi có GPS và 87 phút khi không có GPS.
	- **Cảm biến & Phần cứng:** Trang bị máy đo gió, CPU, cảm biến hồng ngoại (IR) và camera 12K.
	- **Lực đẩy (Thrust - τ):** Là lực nâng do cánh quạt tạo ra, đủ để nâng 7,000 gram. Công thức (1) tính lực đẩy dựa trên kích thước cánh quạt, mật độ không khí, và vận tốc gió qua quạt.
	- **Công suất (Power - P):** Năng lượng cần thiết cho hoạt động bay. Công thức (2) tính công suất dựa trên lực đẩy, tốc độ quay, và đặc tính cánh quạt.
	- **Khối lượng nâng được (m):** Tổng khối lượng UAV có thể nhấc lên. Công thức (3) tính toán dựa trên lực đẩy hoặc công suất.
- Tóm lại, mục này cung cấp thông tin về khả năng hoạt động (tải trọng, thời gian bay), trang bị cảm biến và các công thức vật lý cơ bản để tính toán hiệu suất bay (lực đẩy, công suất, khối lượng nâng).
**3.2 Fire Detection and Fire Region Prediction** 
- Mô tả cách UAV phát hiện đám cháy trong rừng và sau đó phân tích, dự đoán **vùng lan rộng** của đám cháy dựa vào ảnh và thông tin cảm biến thu được.
	1. **Trang bị & Giao tiếp:** UAV dùng cảm biến hồng ngoại (IR), camera 12K và CPU trên bo mạch. Nó gửi video thời gian thực về trạm mặt đất. Trạm mặt đất phân tích, quyết định hành động và có thể điều khiển UAV.
	2. **Phát hiện bằng AI:** CPU trên UAV đủ mạnh để chạy mô hình **YOLOv4 tiny**, giúp phát hiện lửa nhanh và chính xác.
- Sử dụng mô hình YOLOv4 Tiny:
- ![[Pasted image 20250503202534.png]]
	- cấu trúc gồm 2 layers:
		- *feature extraction layer (DarkNet + ResNet)*: Nhiệm vụ nhận diện các đặc điểm hình ảnh quan trọng.
			- Gồm có các khối CBL và CBM với hàm kích hoạt Leaky ReLU/Mish (trong Fig5). 
		- *processing layer*: Xử lý các đặc trưng đã trích xuất để đưa ra dự đoán cuối cùng.
		- Mạng còn có 5 lớp max-pooling (kích thước 2×2, stride 2) để giảm kích thước ảnh đặc trưng còn 1/32 lần ban đầu. Do lửa và khói không có hình dạng cố định, mô hình sử dụng lớp YOLO cuối (logistic regression) để dự đoán xem có vật cháy ở vị trí nào, đồng thời tính toán bounding box dựa trên 2 chỉ số *RPN* và *IoU*. Trong quá trình huấn luyện, hệ thống đã được cung cấp tập ảnh lửa và khói thực tế, cho phép YOLOv4-Tiny học được đặc trưng thị giác của đám cháy.
		- *Note*: IoU là một chỉ số đo lường mức độ trùng khớp giữa hai khung: khung giới hạn _dự đoán_ bởi mô hình và khung giới hạn _thực tế_ 
			- **Cách tính:** IoU = (Diện tích phần giao nhau của 2 khung) / (Diện tích phần hợp lại của 2 khung).
			- **Giá trị:** Từ 0 (không trùng khớp) đến 1 (trùng khớp hoàn hảo)
	-  phương trình (5) được dùng để phân nhóm các bounding boxs theo các nhóm khác nhau 
	- còn phương trình (6) là để tính grounding box dựa trên tâm của đám cháy thu dc từ camera
		- 1. **`BBx`, `BBy`:** Là tọa độ **điểm chính giữa (tâm)** của cái khung đó trên ảnh.
		    - `BBx`: Tâm khung nằm ở đâu theo chiều **ngang**.
		    - `BBy`: Tâm khung nằm ở đâu theo chiều **dọc**.
		- 2. **`BBwidth`, `BBheight`:** Là **kích thước** của cái khung đó.
		    - `BBwidth`: Khung **rộng** bao nhiêu.
		    - `BBheight`: Khung **cao** bao nhiêu.
	- **Tóm lại:** `BBx, BBy` cho biết **vị trí tâm**, còn `BBwidth, BBheight` cho biết **kích thước** của khung hình chữ nhật bao quanh đám cháy. Có 4 thông số này sẽ vẽ được chính xác cái khung đó lên ảnh.
- **Phân chia các pixel trong ảnh thành 2 vùng cháy và không cháy dựa trên độ histogram độ sáng/nhiệt độ dùng phương pháp Otsu**
	- **Mục tiêu:** Otsu tìm một giá trị ngưỡng `k` để phân loại 2 lớp 
	- **Tiêu chí "Tốt nhất":** Ngưỡng `k` được coi là "tốt nhất" nếu nó làm cho sự khác biệt (phương sai - variance) _bên trong mỗi lớp_ là nhỏ nhất có thể. Nói cách khác, Otsu cố gắng tìm ngưỡng `k` sao cho:
	- **Cách hoạt động của Otsu:**
		1. Tính histogram độ sáng của ảnh. Chuẩn hóa histogram để có `p(j)`.
		2. **Thử từng giá trị ngưỡng `k`** có thể (từ 1 đến h-1).
		3. Với mỗi `k`:
		    - Tính `ω_a(k)` và `ω_b(k)` bằng công thức (8).
		    - Tính giá trị trung bình độ sáng cho từng lớp (không ghi trong công thức nhưng cần để tính phương sai).
		    - Tính phương sai `σ_a^2(k)` và `σ_b^2(k)` cho từng lớp.
		    - Tính tổng phương sai nội lớp có trọng số `σ_w^2(k)` bằng công thức (7).
		4. Chọn giá trị `k` nào mà cho ra `σ_w^2(k)` **nhỏ nhất**. Ngưỡng `k` tối ưu này sẽ phân chia ảnh thành hai lớp một cách tốt nhất theo tiêu chí của Otsu.
*fig 6: YOLOv4 Tiny architecture*: ![[Pasted image 20250503215146.png]]

**Prediction of the Possibility of Forest fire**: 
- UAV không chỉ phát hiện đám cháy đang xảy ra mà còn có nhiệm vụ **dự đoán nguy cơ cháy rừng** ngay cả khi chưa có lửa.
	- **Khi không thấy cháy:** UAV sẽ tìm kiếm các yếu tố có thể gây cháy trong tương lai.
	- **Cách tìm:** Nó dựa vào việc xác định các nguyên nhân gây cháy (do người hoặc tự nhiên) và đặc biệt là tìm kiếm sự hiện diện của 3 yếu tố trong **"Tam giác Lửa"**:![[Pasted image 20250503215703.png]]
	    1. **Oxy** (có sẵn)
	    2. **Nhiên liệu** (cây cỏ khô, vật liệu dễ cháy)
	    3. **Nguồn nhiệt** (tàn lửa, điểm nóng bất thường)
- **Hành động:** Nếu UAV phát hiện thấy có đủ Nhiên liệu và Nguồn nhiệt tiềm ẩn ở một khu vực, nó sẽ đánh giá đó là nơi có nguy cơ cháy cao và **gửi cảnh báo** về trạm mặt đất để có biện pháp phòng ngừa sớm.
- **3.3 3D Modelling of Forest Fire**
	- **Construction of 3D Forest Fire Modeling:** Mục này tập trung vào việc thu thập dữ liệu và thiết lập cơ sở cho mô hình 3D. Nó mô tả việc sử dụng kỹ thuật *photogrammetry*, cụ thể là spatial resection, để **ước tính vị trí 3D của cây cối** bằng cách đo đạc các feature points phân bố trên nhiều ảnh 2D chụp từ các góc độ khác nhau (quá trình "*relative orientation*"). Tuy nhiên, phương pháp này gặp khó khăn trong môi trường rừng ngoài trời phức tạp. Do đó, công nghệ **LiDAR** được tích hợp và đóng vai trò then chốt: nó cung cấp **dữ liệu định hướng và khoảng cách cực kỳ chính xác** giữa các vật thể (cây cối), giúp khắc phục hạn chế của việc lấy mẫu bề mặt bằng phương pháp truyền thống và xử lý sự không nhất quán của dữ liệu (ví dụ, do che khuất). LiDAR cho phép thu thập dữ liệu điểm 3D liên tục và nhanh chóng ngay cả khi UAV đang bay tốc độ cao trong khu vực rừng.
	- **Terrestrial Image-Based 3D Modeling:** Sau khi có dữ liệu ảnh và/hoặc LiDAR, mục này mô tả các bước xử lý để tinh chỉnh và tạo ra sản phẩm cuối cùng. Quá trình bắt đầu bằng việc **căn chỉnh chính xác các ảnh** với nhau, sử dụng các phương pháp định hướng đã có (từ LiDAR hoặc đo ảnh), kết hợp với việc đo các *tie points* - các điểm tương đồng trên nhiều ảnh. Bước quan trọng tiếp theo là *bundle adjustment*, một kỹ thuật tối ưu hóa phức tạp giúp tinh chỉnh đồng thời vị trí/góc chụp của camera (UAV) và tọa độ 3D của các điểm đặc trưng, nhằm đạt độ chính xác hình học cao nhất và cho phép **hiệu chỉnh cảm biến (sensor calibration)**. Cuối cùng, các **thuật toán đối sánh ảnh tự động (automatic photogrammetric matching)** tiên tiến, có khả năng xử lý nhiều ảnh đầu vào, được áp dụng để thực hiện đo đạc bề mặt và tạo ra kết quả là một *3D dense point cloud* mô tả chi tiết bề mặt địa hình và thảm thực vật của khu vực rừng bị cháy.
### 4. Experiments and Results:
- *Training và deploy:* Mô hình được train trước trên desktop với 100 ảnh và 50,000 training steps cho mỗi ảnh sau đó mới được nạp vào bộ xử lý của UAV (UAV-CPU) để thử nghiệm thực tế.
- *Hiệu năng:*
	-  Mô hình YOLOv4 tiny đạt tốc độ xử lý (FPS) đủ tốt trên CPU của UAV để phát hiện và phân tích theo thời gian thực.
	- Các chỉ số đánh giá hiệu năng được trình bày trong Bảng 2 (ví dụ: mAP@0.5 là 85.36%, F1-score là 0.91).
	- Bảng 3 so sánh mô hình đề xuất với các công trình trước đó, cho thấy mô hình này vượt trội hơn hẳn (ví dụ: Độ chính xác - Accuracy đạt 93.3% so với 87%, 86.7%, 89% của các mô hình khác).
	- ![[Pasted image 20250504193128.png]]
- Các kỹ thuật augmentation như Mix-up và Mosaic được dùng để tạo thêm dữ liệu huấn luyện đa dạng. Lớp tích chập (convolution layer) trong mạng hoạt động tốt trong việc phát hiện các phần nhỏ của ảnh (như đốm lửa nhỏ).
- **Phát hiện trong điều kiện khó:**
    - Mô hình có thể phát hiện lửa ngay cả ở vùng ánh sáng yếu (nhờ phương pháp Otsu đã đề cập trước đó để phân đoạn ảnh nhiệt).
    - **Hạn chế:** Mô hình gặp khó khăn ở những vùng có **khói dày đặc**, vì khói bị **nhầm lẫn với sương mù dày**, dẫn đến không phát hiện được lửa.
    - Mô hình được huấn luyện với dữ liệu đa dạng (nắng, mưa, tuyết,...) để hoạt động tốt trong nhiều điều kiện môi trường.
# References
