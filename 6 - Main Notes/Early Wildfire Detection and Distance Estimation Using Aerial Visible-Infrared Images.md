2025-05-05 14:40


Tags:

# Early Wildfire Detection and Distance Estimation Using Aerial Visible-Infrared Images



# References
# **Tóm tắt chi tiết bài báo: Early Wildfire Detection and Distance Estimation Using Aerial Visible-Infrared Images**

## Thông tin bài báo
- **Tiêu đề:** Early Wildfire Detection and Distance Estimation Using Aerial Visible-Infrared Images  
- **Tác giả:** Linhan Qiao, Shun Li, Youmin Zhang, Jun Yan  
- **Ngày xuất bản:** 03/05/2024  
- **Nguồn:** IEEE Transactions on Industrial Electronics  
- **DOI:** [10.1109/TIE.2024.3387089](https://doi.org/10.1109/TIE.2024.3387089)  
- **Github Repository:** [early_wildfire_perception](https://github.com/ConcordiaNAVlab/early_wildfire_perception)  

---

## Mở đầu:
1. Nêu tác hại của cháy rừng và tình hình hiện tại
2. Nhấn mạnh tầm quan trọng của việc phát hiện cháy rừng sớm 
3. Trình bày hạn chế của các phương pháp hiện tại  
	-  Cần giải pháp phát hiện nhanh, linh hoạt, tiết kiệm thời gian và chi phí. UAV là lựa chọn tối ưu.
4. Trình bày ưu điểm của UAV:
	- Linh hoạt về thời gian và không gian.
	-  Chi phí thấp hơn vệ tinh hoặc tháp quan sát.
	-  Có thể gắn nhiều loại cảm biến (hình ảnh, hồng ngoại, đa phổ) để thu thập thông tin.
- Camera hình ảnh (visual), hồng ngoại, và đa phổ trên UAV hoặc vệ tinh được sử dụng rộng rãi để phát hiện cháy rừng, nhưng hầu hết chỉ tập trung vào phân loại hoặc phân đoạn hình ảnh.
- Việc định vị vị trí đám cháy vẫn phụ thuộc nhiều vào thao tác thủ công.
- Các thử nghiệm thực tế về định vị cháy rừng chưa đủ đầy đủ.
---

## Mục tiêu nghiên cứu
Mục tiêu của nghiên cứu là thiết kế và kiểm chứng framework tích hợp trên UAV để hỗ trợ phát hiện cháy rừng sớm thông qua:
1. **Framework design**: 
	- Kết hợp lọc đặc trưng ORB (ORB features) với học sâu (AG U-Net) và kỹ thuật ORB-SLAM2.
	- Giải quyết khoảng trống trong việc phân đoạn khói cháy bằng camera đơn và định vị điểm cháy.
2. **Smoke and suspected flame segmentation:** 
	- Sử dụng AG U-net để phát hiện khói và lửa
	- Hiệu suất cao hơn và giảm false aleart
3. **Distance Estimation:**
	- Sử dụng *SLAM* kết hợp UAV để cung cấp chính xác thông tin vị trí vụ cháy (sử dụng triangulation)
4. **Visual-infrared images registration:**
	- Phát triển một phương pháp images registration  
	- Kết hợp thông tin từ hình ảnh thường và hồng ngoại để giảm báo động sai.
![[Pasted image 20250505153057.png]]
---

## Phương pháp nghiên cứu
- nhấn mạnh sự chuyển dịch từ các phương pháp truyền thống sang sử dụng học sâu, đồng thời giải thích lý do tại sao các mô hình phát hiện đối tượng như YOLO hay SSD lại phù hợp cho phát hiện cháy rừng sớm nhờ tốc độ và khả năng phát hiện khói/ngọn lửa trong điều kiện phức tạp.
### **Yêu cầu đối với mô hình detection**
- Mô hình cần **xử lý hiệu quả thông tin đặc trưng** từ dữ liệu gốc.
- Phân đoạn ngữ nghĩa được ưu tiên hơn so với các mô hình phát hiện đối tượng dựa trên bounding box vì phù hợp hơn để phát hiện khói và ngọn lửa.
- Mô hình cần **đơn giản**, không phụ thuộc nhiều vào kích thước tập dữ liệu hoặc tài nguyên tính toán.
-  U-Net được chọn vì:
    - Cấu trúc nhẹ (light-weight).
    - Hiệu suất phân đoạn tốt ngay cả với tập dữ liệu huấn luyện nhỏ.
    - Dựa vào nghiên cứu [22], cải tiến U-net = cách sử dụng AG
--- 

### **1. Semantic Segmentation**  
![[Pasted image 20250506144221.png]]
- **Mô hình được sử dụng:** Attention Gate (AG) U-Net.  
- **Cải tiến:**  
	- Khác với U-Net gốc chỉ nối thẳng đặc trưng từ phần *encoder (downsampling)* sang phần *decoder (upsampling)*, AG U-Net sử dụng *Attention gates* để "lọc" và "tập trung" vào các đặc trưng quan trọng hơn từ phần encoder.
	- Các *Attention signals* này được truyền qua một đường riêng, giúp các đặc trưng từ phần mã hóa được "quan tâm nhiều hơn".
	- AG ưu tiên các đặc trưng quan trọng và loại bỏ các đặc trưng không liên quan, giúp giảm độ nhạy của mô hình trước các nhiễu động, giảm tỷ lệ báo động sai.  
- **Kiến trúc:**
	- Được thể hiện trong fig2, Attention Gate có thể được formulated bởi công thức sau: 
	- ![[Pasted image 20250506151033.png]]
	- Về cơ bản, Cổng Chú ý kết hợp thông tin từ lớp nông (`x_i^l`) và lớp sâu (`g_i`), học cách tính toán một "trọng số chú ý" (`att_i^l`). Trọng số này sau đó được dùng để điều chỉnh (nhân với) đặc trưng `x_i^l`, làm nổi bật các đặc trưng quan trọng và làm mờ đi các đặc trưng không liên quan trước khi chúng được truyền tới bộ giải mã.
	- các convolutional blocks trong AG U-net *based on ResNet-34* và kế thừa kỹ thuật *residual connection* giữa mỗi hai convolutional blocks, nó cho phép tín hiệu đi tắt qua 1 hoặc nhiều layers. giúp hiệu suất tốt hơn, *hiệu suất dự đoán vẫn có thể được đảm bảo ngay cả khi tập dữ liệu huấn luyện bị hạn chế*
	- loss function của AG U-Net là *Focal Loss* được sử dụng để giúp mô hình tập trung vào mẫu khó, phù hợp với bài toán class imbalance :
	- ![[Pasted image 20250506153015.png]]

- **Quy trình:**  
  1. Sử dụng tập dữ liệu hình ảnh cháy rừng được gán nhãn gồm:  
     - 619 hình ảnh từ Google.  
     - 120 hình ảnh từ các thí nghiệm ngoài trời.  
  2. Gắn nhãn theo 3 lớp: **nền**, **khói**, và **ngọn lửa**.  
  3. Thực hiện huấn luyện bằng Transfer Learning để tinh chỉnh mô hình cho các điều kiện môi trường ngoài trời.
  4. Khi training, không chỉ những khu vực có ngọn lửa rõ ràng mới được gán nhãn là "khu vực cháy". Ngay cả những **khu vực bị nghi ngờ có khả năng cháy (suspected flame area)** cũng được gán nhãn. Điều này được thực hiện để mô hình có thể học cách **dự đoán được khu vực có khả năng phát triển thành đám cháy ngay cả khi chưa có ngọn lửa rõ ràng**

- **Hiệu suất:**  
  - Micro F1-score: **99.464%** (cao hơn hầu hết các mô hình khác như FireNet hoặc U-Net gốc).  
  - AUC-ROC: **89.341%**, thể hiện khả năng giảm báo động sai.  
  - FPS (tốc độ xử lý): **38 FPS**, đáp ứng yêu cầu thời gian thực.  

---

### **2. Distance Estimation**  
- **Công cụ chính:** FAST and BRIEF ORB-SLAM2.  
	- Sử dụng các điểm đặc trưng ORB (Oriented FAST and Rotated BRIEF):
	    - **FAST:** Phát hiện các đặc trưng từ kiểm tra phân đoạn nhanh.
	    - **BRIEF:** Trích xuất các đặc trưng nhị phân mạnh mẽ.
	    - ![[Pasted image 20250507142959.png]]
	    - AG U-Net phân đoạn ảnh để tìm ra đường viền của vùng cháy, một vòng tròn đỏ (vừa khít) và một vòng tròn xanh (lớn hơn 1.5 lần) được xác định dựa trên đường viền này (fig 3a). Vòng tròn xanh là nơi các đặc trưng ORB sẽ được trích xuất.
	    - Từ công thức 4 (hiệu chỉnh quỹ đạo camera) và triangulation tính được d'(trong công thức (5)), sau đó tính phạm vi khoảng cách phản ảnh kích thước và độ sâu vụ cháy.
-  ![[Pasted image 20250507135840.png]]
	- công thức (4) giúp "áp" cái kích thước thật (từ GPS/IMU) vào cái bản đồ hình dáng (được tạo từ SLAM), để chúng ta biết được quỹ đạo di chuyển của camera một cách chính xác cả về hình dáng lẫn kích thước thật ngoài đời. Điều này rất quan trọng để sau đó có thể đo khoảng cách đến đám cháy một cách chính xác. Hiểu đơn giản là `s_i` cho ta biết hệ số tỉ lệ, còn `t_c^*i` cho ta độ dịch chuyển, đc tính từ `s_i`, từ đó ta có được quỹ đạo camera chính xác về mặt tỷ lệ
- ![[Pasted image 20250507144958.png]]
	- 3 công thức (5) lần lượt ước tính khoảng cách từ UAV đến điểm xa nhất của vụ cháy (A), tâm điểm (O), điểm gần nhất (B) 
	- => việc tính như vậy giúp cung cấp 1 phạm vi khoảng cách (A, O, B) có thể hữu ích hơn cho việc lập kế hoạch chữa cháy 
- **Quy trình:**  
  1. Dùng UAV DJI M300 để thu thập hình ảnh với camera DJI ZenMuse H20T.  
  2. Sử dụng ORB-SLAM2 để khôi phục vị trí camera và quỹ đạo di chuyển.  
  3. Tính khoảng cách trung bình giữa UAV và điểm cháy dựa trên các điểm đặc trưng được lọc (ORB features).

- **Kết quả thực nghiệm:**  
  - Độ sai lệch khoảng cách (so với dữ liệu thực tế từ cảm biến laser):  
    - **17.1m:** Sai số 0.44%.  
    - **22.4m:** Sai số 5.78%.  
    - **31.6m:** Sai số 8.76%.  
    - **41.2m:** Sai số 0.15%.  
    - **51.2m:** Sai số 0.68%.  

---

### **3. Image Registration**  
- **Thách thức:**  
  - Camera hồng ngoại DJI ZenMuse H20T không được hiệu chỉnh tham số nội tại và ngoại tại.  
  - Hình ảnh từ camera thường và hồng ngoại không đồng nhất về tỷ lệ và vị trí.  

- **Giải pháp:**  
  - Áp dụng một mô hình hình học dựa trên mối quan hệ giữa hình ảnh thường và hồng ngoại.  
  - Sử dụng thuật toán bình phương tối thiểu (Least Square) để khớp các hình ảnh.  

- **Kết quả:**  
  - Đăng ký chính xác với sai số trung bình dưới **10 pixel** ở khoảng cách trên **15m**.  
  - Giảm thiểu các báo động sai nhờ xác nhận lại thông tin từ ảnh hồng ngoại.  

---

## Kết quả thực nghiệm

### **1. Phân đoạn Semantic**
- **Dữ liệu:** Tổng cộng 739 hình ảnh (619 từ Google và 120 từ thí nghiệm ngoài trời).  
- **Hiệu suất mô hình:**  
  - Micro F1-score: **99.464%**.  
  - AUC-ROC: **89.341%**.  
  - FPS: **38 FPS** (đáp ứng yêu cầu thời gian thực).  

### **2. Ước lượng khoảng cách**
- **Thí nghiệm với 5 khoảng cách:**  
  - **17.1m:** Sai số 0.44%.  
  - **22.4m:** Sai số 5.78%.  
  - **31.6m:** Sai số 8.76%.  
  - **41.2m:** Sai số 0.15%.  
  - **51.2m:** Sai số 0.68%.  

### **3. Đăng ký hình ảnh**
- Sử dụng mô hình hình học để khớp hình ảnh từ camera thường và hồng ngoại.  
- Sai số trung bình dưới **10 pixel** ở khoảng cách trên **15m**.  

---

## Đóng góp nổi bật của nghiên cứu
1. **Phát hiện cháy rừng sớm:**  
   - Phân đoạn chính xác ngọn lửa và khói ngay từ giai đoạn đầu cháy rừng.  

2. **Ước lượng khoảng cách tự động:**  
   - Không cần thao tác thủ công, đáp ứng yêu cầu hoạt động tự động của UAV.  

3. **Ghép khớp ảnh hồng ngoại và thường:**  
   - Tăng độ chính xác và giảm thiểu báo động sai thông qua việc kết hợp dữ liệu từ các loại cảm biến khác nhau.  

---

## Hạn chế và hướng phát triển

### **Hạn chế:**
1. **Thử nghiệm đơn giản:**  
   - Chỉ thử nghiệm với một điểm cháy duy nhất, chưa xử lý các đám cháy phức tạp (nhiều điểm cháy hoặc đường cháy dài).  

2. **Tốc độ tính toán:**  
   - Mặc dù hiệu suất tốt, nhưng cần tối ưu thêm để giảm độ trễ khi triển khai thực tế.  

3. **Dữ liệu huấn luyện:**  
   - Tập dữ liệu còn hạn chế, cần mở rộng để phù hợp với các điều kiện môi trường khác nhau.  

### **Hướng phát triển:**  
1. **Mở rộng thử nghiệm:**  
   - Kiểm tra khả năng xử lý các đám cháy lớn, nhiều điểm cháy, và cháy theo tuyến.  

2. **Cải thiện tính toán thời gian thực:**  
   - Tối ưu hóa thuật toán để giảm độ trễ trong xử lý dữ liệu.  

3. **Tích hợp hệ thống tự động hóa:**  
   - Xây dựng quy trình hoàn toàn tự động cho phát hiện, định vị, và xử lý cháy rừng.  

---

## Kết luận
Nghiên cứu này đã thiết kế và kiểm chứng một framework tích hợp trên UAV, cung cấp giải pháp tự động hóa hiệu quả cho phát hiện cháy rừng sớm. Tuy nhiên, để triển khai thực tế, cần mở rộng quy mô và tối ưu hóa thêm về chi phí và tốc độ xử lý.