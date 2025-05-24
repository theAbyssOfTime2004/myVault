2025-05-24 21:32


Tags:

# tóm tắt Deep Learning-Based Forest Fire Risk Research on Monitoring and Early Warning Algorithms

### **Phương pháp đề xuất:**
![[Pasted image 20250524214404.png]]

Thuật toán **tích hợp 3 công nghệ chính**:

- **YOLOv5-EMA**: Mô hình deep learning phát hiện khói từ ảnh nhìn thấy
- **Camera hồng ngoại**: Kiểm tra nhiệt độ vượt ngưỡng cảnh báo
- **FWI Canada**: Tính chỉ số nguy cơ cháy từ dữ liệu khí tượng

### **Thu thập dữ liệu**

- **Camera hai phổ** (visible-infrared bispectral): Chụp đồng thời ảnh thường và ảnh nhiệt
- **Trạm khí tượng**: Thu thập nhiệt độ, độ ẩm, gió, mưa cho tính FWI
- **Tập dữ liệu**: 1,359 ảnh được gán nhãn 4 loại (fire, clouds, fog, other)

### **Xử lý dữ liệu**

- **Ảnh nhìn thấy**: Huấn luyện YOLOv5 → mức độ tin cậy phát hiện khói
- **Ảnh hồng ngoại**: Kiểm tra ngưỡng nhiệt → kết quả nhị phân (0/1)
- **Dữ liệu khí tượng**: Tính FWI → cấp độ nguy hiểm cháy rừng
- **Quyết định cuối**: Kết hợp 3 kết quả theo quy tắc logic

### **Kết quả**

- **Accuracy**: 94.12%
- **Precision**: 96.1%
- **Recall**: 93.67%
- **F1-score**: 94.87%
	- **So sánh**: Vượt trội YOLOv5 đơn lẻ (83.42%) và các phương pháp khác


# References
