2025-04-26 14:28


Tags: [[DeepLearning]], [[Machine Learning]]

# Early wldfire detection using different machine learning algorithms

- **Abstract summary**: Nghiên cứu này đề xuất một hệ thống phát hiện cháy rừng sớm bằng cách sử dụng các nút cảm biến không dây giá rẻ kết hợp với các phương pháp AI detection. Hệ thống gồm các cảm biến đo nhiệt độ, độ ẩm, khói và một module truyền thông không dây. Bốn thuật toán máy học được đánh giá *(bao gồm decision trees, random forests, SVM và KNN),* trong đó **Random Forest cho kết quả chính xác cao nhất với độ chính xác 77.95%.** Hệ thống này hiệu quả và tiết kiệm chi phí, phù hợp cho việc giám sát cháy rừng trên diện rộng.
### 1.Introduction 
- Trong những năm gần đây, cháy rừng ngày càng xảy ra nhiều và nghiêm trọng hơn do biến đổi khí hậu, thay đổi mục đích sử dụng đất và các hoạt động của con người. 
- Biến đổi khí hậu làm tăng nhiệt độ, thay đổi lượng mưa, khiến đất đai khô hạn hơn, dễ cháy hơn. Hoạt động của con người như đốt phá rừng, đốt lửa trại, bắn pháo hoa cũng làm tăng nguy cơ cháy. 
- Cháy rừng gây ra nhiều hậu quả: 
	- phá hủy môi trường sống, mất đa dạng sinh học, xói mòn đất, ảnh hưởng xấu đến sức khỏe con người và động vật qua khói bụi, gây thiệt hại kinh tế lớn. 
	- Chi phí dập tắt cháy rừng ở Mỹ năm 2020 vượt hơn 2,7 tỷ USD. Vì vậy, cần có các chiến lược phát hiện và giảm thiểu cháy rừng hiệu quả.
### 2.Design of early wildfire detection systems
- **Các cách phát hiện cháy rừng phổ biến:**    
    - **Vệ tinh (satellite-based):** Bao phủ diện rộng nhưng cập nhật dữ liệu chậm.  
    - **UAVs (máy bay không người lái):** Cho hình ảnh chất lượng cao, nhưng hạn chế về thời gian bay và vùng phủ sóng.        
    - **Mạng cảm biến mặt đất (ground-based sensor netwoks):** Theo dõi liên tục, triển khai được ở những điểm then chốt.        
- **Vấn đề với các cách bố trí cũ:**
    - **Dạng đường thẳng hoặc lưới:** Hoạt động kém hiệu quả trong địa hình phức tạp như núi đồi, rừng rậm.
- **Ý nghĩa trong nghiên cứu:** Nghiên cứu này sử dụng mạng cảm biến mặt đất để tận dụng ưu điểm giám sát liên tục, cải thiện khả năng phát hiện cháy sớm trong môi trường thực tế.
### 3.Satellite-based monitoring
- Có độ phủ sóng rất lớn, phù hợp để phát hiện các đám cháy rừng diện rộng
- Tuy nhiên *temporal-resolution hạn chế* (nghĩa là thời gian giữa các lần thu thập dữ liệu khá dài, không liên tục, không cập nhật thường xuyên) khiến cho việc phát hiện bị chậm trệ
- Các nghiên cứu gần đây đã giúp cải thiện temporal-resolutin và độ chính xác của hệ thống này, khiến việc early detection đã dễ dàng hơn
### 4.UAV-based systems
- Có khả năng capture được hình và video *chất lượng cao*, sau đó có thể áp dụng các thuật toán học máy để giúp phát hiện cháy rừng. 
- Có tính linh hoạt cao và có thể deploy dễ dàng. nhưng tầm hoạt đông và thời gian hoạt động hạn chế
### 5.Ground-based sensor networks
- **Mạng cảm biến không dây (WSN)** đang ngày càng được sử dụng nhiều để phát hiện cháy rừng vì khả năng giám sát liên tục theo thời gian thực. Trong nghiên cứu này, cảm biến được bố trí theo **hình tam giác** nhằm tối ưu hóa độ chính xác và độ phân giải không gian, đồng thời tăng khả năng chịu lỗi khi một nút cảm biến bị hỏng.    
- **Phát hiện cháy sớm** rất quan trọng để kiểm soát cháy hiệu quả. Các phương pháp truyền thống (thủ công) thường chậm và thiếu chính xác. Vì thế, **machine learning** và **dữ liệu viễn thám** (như ảnh vệ tinh, UAV) đang được áp dụng rộng rãi để cải thiện khả năng phát hiện.
- Các nghiên cứu trước đây đã dùng nhiều thuật toán như **Random Forest, SVM, CNN, Artificial Neural Networks** để nhận diện cháy, cho kết quả khả quan.
- **WSN kết hợp UAV** và các thuật toán thông minh như **fuzzy logic** cũng được phát triển để theo dõi và cảnh báo cháy kịp thời.    
- **Chỉ số thời tiết cháy (Fire Weather Index - FWI)** được dùng để đánh giá nguy cơ cháy dựa trên độ ẩm, gió, nhiệt độ, lượng mưa,… Có hai cách phổ biến: **phương pháp của Canada** và **phương pháp của Hàn Quốc**. Phương pháp của Canada chính xác hơn, nhanh hơn và tiết kiệm năng lượng nên được ưu tiên sử dụng trong nghiên cứu này.    
	- **Phương pháp Canada:** Được xây dựng trên 6 yếu tố chính liên quan đến điều kiện dễ xảy ra cháy rừng. Các yếu tố này phản ánh khả năng cháy và mức độ nguy hiểm của lửa trong điều kiện thực tế.
	- **Phương pháp Hàn Quốc:** Lấy nền tảng từ phương pháp Canada nhưng được điều chỉnh để phù hợp với đặc điểm địa lý, khí hậu và thảm thực vật của Hàn Quốc, thêm các yếu tố như địa hình và lớp phủ đất.
- Nghiên cứu nhấn mạnh việc **tối ưu hóa cách lắp đặt cảm biến và thu thập dữ liệu tại chỗ**, nhằm nâng cao hiệu quả của các mô hình machine learning khi phát hiện cháy rừng.
### 6.Architecture of the proposed early detection system

![[Pasted image 20250427104403.png]]

- Ba **nút cảm biến** được lắp đặt, mỗi nút có các cảm biến đo: **nhiệt độ, độ ẩm tương đối, CO và CO₂**.
- Các nút cảm biến được bố trí theo **hình tam giác** để tối ưu hóa độ chính xác thu thập dữ liệu và đảm bảo hệ thống vẫn hoạt động nếu một nút bị hỏng.
- *Training data* cho mô hình machine learning được thu thập bằng cách thay đổi vị trí đám cháy và khoảng cách giữa các nút.
- Các nút được đặt ở **độ cao 1 mét** so với mặt đất, tại các đỉnh trên của một **khối lập phương** có chiều cao 1m.    
- Dữ liệu được thu thập:
    - Bắt đầu **30 phút trước khi đốt lửa**.
    - Cứ mỗi **10 giây** ghi một mẫu dữ liệu.
    - Thí nghiệm cháy kéo dài **30 phút**, sau đó tiếp tục thu thêm dữ liệu **30 phút sau khi lửa tắt**.
- Đám cháy thử nghiệm được tạo ra bằng cách đốt **2kg gỗ teak** trong không gian nhỏ (30cm x 30cm).
- Các thông tin khác như **lượng mưa, tốc độ gió** cũng được thu thập từ hệ thống khí tượng.
- Mỗi vụ cháy sẽ tạo ra **3 bộ dữ liệu** từ 3 cảm biến, tất cả dùng để **huấn luyện mô hình machine learning**.
**Note**:
	- **Vì sao dùng nhiều cảm biến (nhiệt độ, độ ẩm, CO, CO₂)?**  
	    → Đám cháy làm tăng nhiệt độ, thay đổi độ ẩm, sinh ra khí CO và CO₂ — nhờ vậy hệ thống dễ dàng nhận diện đám cháy.
	- **Tại sao bố trí hình tam giác?**  
	    → Giúp **khoanh vùng vị trí đám cháy** chính xác hơn (giống như định vị GPS dựa trên nhiều vệ tinh) và tăng độ an toàn nếu 1 nút gặp sự cố.
# References
