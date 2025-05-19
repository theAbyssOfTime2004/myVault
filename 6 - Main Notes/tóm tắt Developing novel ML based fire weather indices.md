2025-05-19 13:46


Tags: [[tóm tắt FF detection system using WSN and ML]], [[tóm tắt Early FF Detection System Using WSN and DL]]

# tóm tắt Developing novel ML based fire weather indices

### 1. Ý tưởng chính
- Mục tiêu là phát triển các chỉ số thời tiết cháy rừng dựa trên học máy (MLFWIs) để ước tính nguy cơ cháy rừng chính xác hơn các chỉ số truyền thống.
- Động lực là do tần suất thời tiết cực đoan và cháy rừng lớn ngày càng tăng, trong khi các chỉ số truyền thống (FWIs) còn nhiều hạn chế: chỉ phù hợp từng vùng, dựa trên thống kê cũ, ít biến số, hiệu quả dự báo kém.
- Học máy được sử dụng vì có thể xử lý dữ liệu lớn, nhiều biến và mối tương tác phức tạp, cho kết quả dự báo chính xác hơn.

### 2. Cách thức thực hiện
- Phát triển các mô hình phân loại để dự đoán nguy cơ cháy rừng mỗi ngày, mỗi khu vực.
- **Biến mục tiêu:** Sự xuất hiện cháy rừng hàng ngày (dữ liệu nhị phân) trên lưới toàn cầu 0.25 độ, dựa trên bộ dữ liệu toàn cầu (Artés et al, 2019).
- **Cân bằng dữ liệu:** Lấy mẫu ngẫu nhiên các quan sát không cháy để cân bằng số lượng với các quan sát cháy.
- **Đặc trưng (biến đầu vào):** Bao gồm nhiều yếu tố khí tượng (nhiệt độ, độ ẩm, lượng mưa, gió, bức xạ mặt trời), địa hình (độ dốc), tải lượng nhiên liệu (NDVI, lịch sử cháy), nhân sinh (mật độ dân số), cùng các chỉ số cháy rừng truyền thống (từ hệ thống Canada, Úc, Mỹ).
- **Mô hình học máy:** Sử dụng 4 mô hình: Random Forest (RF), XGBoost, Multilayer Perceptron (MLP), Logistic Regression (LR).
- **Đánh giá hiệu suất:** Dùng nhiều chỉ số: ROC-AUC (quan trọng nhất), PR-AUC, Accuracy, TPR, TNR.
- **Phân tích đóng góp yếu tố:** Dùng giá trị SHAP và biểu đồ PDPs để xác định và giải thích tác động của các biến đến dự đoán.
- **Dự đoán cháy rừng cực đoan:** Đánh giá năng lực dự đoán 100 vụ cháy lớn nhất bằng cách loại chúng khỏi tập huấn luyện.

### 3. Kết quả đạt được
- Các mô hình học máy (MLFWIs) vượt trội đáng kể so với chỉ số truyền thống và logistic regression trong dự đoán nguy cơ cháy rừng.
- **XGBoost** là tốt nhất (ROC-AUC: 0.98, Accuracy: 0.95), tiếp theo là RF (ROC-AUC: 0.92, Accuracy: 0.85). Các chỉ số truyền thống chỉ đạt ROC-AUC 0.62–0.80.
- Việc thêm các chỉ số FWI truyền thống và lịch sử cháy vào đầu vào giúp cải thiện mô hình (MLFWI-3: ROC-AUC 0.990, Accuracy 0.964), nhưng LR vẫn thua xa MLFWI.
- **Yếu tố quan trọng nhất:** Nhiệt độ, lượng mưa năm trước (liên quan tải nhiên liệu), lượng mưa hàng ngày (hầu như loại trừ nguy cơ bốc cháy), NDVI, độ dốc, mật độ dân số, tốc độ gió (quan hệ phi tuyến).
- Mô hình ML dự đoán các vụ cháy lớn vượt trội so với chỉ số truyền thống.
- MLFWI-1 cho dự đoán gần như hoàn hảo ở mọi khu vực; LR kém hơn rõ rệt và khác biệt giữa các vùng.
  
### 4. Kết luận và ý nghĩa
- MLFWIs vượt trội so với LR và FWI truyền thống, tiềm năng ứng dụng thực tế lớn (cảnh báo cho dân, bản đồ nguy cơ cháy, hỗ trợ quản lý rừng...).
- Xây dựng mô hình từ dữ liệu toàn cầu, các yếu tố đơn giản, dễ tiếp cận, có thể áp dụng rộng rãi.
- Đề xuất từng bước thay thế FWI truyền thống bằng MLFWIs để tăng hiệu quả cảnh báo cháy rừng.



# References
