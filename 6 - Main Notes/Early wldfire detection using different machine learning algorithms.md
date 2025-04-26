2025-04-26 14:28


Tags: [[DeepLearning]], [[Machine Learning]]

# Early wldfire detection using different machine learning algorithms

- **Abstract summary**: Nghiên cứu này đề xuất một hệ thống phát hiện cháy rừng sớm bằng cách sử dụng các nút cảm biến không dây giá rẻ kết hợp với các phương pháp AI detection. Hệ thống gồm các cảm biến đo nhiệt độ, độ ẩm, khói và một module truyền thông không dây. Bốn thuật toán máy học được đánh giá *(bao gồm decision trees, random forests, SVM và KNN),* trong đó Random Forest cho kết quả chính xác cao nhất với độ chính xác 77.95%. Hệ thống này hiệu quả và tiết kiệm chi phí, phù hợp cho việc giám sát cháy rừng trên diện rộng.
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

# References
