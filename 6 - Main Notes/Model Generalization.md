2025-03-20 18:14


Tags: [[Machine Learning]], [[data scientist]], [[beginner]]

# Model Generalization
### Training, validation and test split
![[Pasted image 20250320182002.png]]
- **Bậc 1**: Mô hình quá đơn giản  (underfitting) → lỗi cao trên tập validation.
- **Bậc 3**: Mô hình phù hợp nhất (best generalization) → lỗi trên validation và test tương đồng, thấp.
- **Bậc 10**: Mô hình quá phức tạp (overfitting) → lỗi rất thấp trên training nhưng cao trên validation, không tổng quát tốt.
**Tỷ lệ phổ biến để chia dữ liệu thành training, validation, test là:**
- **80% - 10% - 10%**
- **70% - 15% - 15%**
- **60% - 20% - 20%**
Tùy vào số lượng dữ liệu, nếu dữ liệu lớn có thể dùng 80%-10%-10%, còn nếu dữ liệu nhỏ hơn có thể dùng 70%-15%-15% để có đủ dữ liệu kiểm tra.
# References
