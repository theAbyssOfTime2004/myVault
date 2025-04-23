2025-04-23 22:04


Tags: 

# Early Wildfire Detection with CubeSat Images Using Single Image Super-Resolution

- **Abstract summarized**: Bài báo trình bày một phương pháp mới để phát hiện cháy rừng sớm bằng hình ảnh từ vệ tinh CubeSat, kết hợp giữa **deep learning** và **kỹ thuật tăng độ phân giải (super-resolution)**. 
	- Note: **Dữ liệu là ảnh từ vệ tinh Landsat-8**, được xử lý thành ảnh RGB và **giả lập ảnh CubeSat** bằng cách **giảm chất lượng**, rồi **tăng lại độ phân giải bằng Real-ESRGAN**.  **Mục tiêu** là tạo ra một giải pháp có thể áp dụng tốt **cho ảnh CubeSat trong thực tế**
- **Cách tiếp cận:**    
    - Dùng ảnh RGB được tạo từ ảnh Landsat-8 (ban đầu có 10 kênh phổ, sau đó chuyển thành 3 kênh RGB).
    - Ảnh được nâng cấp độ phân giải gấp 4 lần bằng kỹ thuật **Real-ESRGAN**.
    - Áp dụng transfer learning với hai mô hình pre-trained: **MobileNetV2** và **ResNet152V2**.
- **Kết quả:** Việc nâng cấp độ phân giải ảnh giúp tăng độ chính xác, độ nhạy (recall) và f1-score khi phát hiện cháy rừng, tăng khoảng **3–5%** tùy mô hình.
# References
