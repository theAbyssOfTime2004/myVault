2025-05-24 22:09


Tags:

# Globfire Dataset

**GlobFire Database** là một cơ sở dữ liệu **toàn cầu về các sự kiện cháy rừng** đơn lẻ, với mục tiêu:

- Khắc phục hạn chế của dữ liệu vệ tinh hiện tại (chỉ cung cấp diện tích bị cháy mà không có thông tin chi tiết về từng sự kiện).
- Tạo một dữ liệu thống nhất, không phân mảnh và đầy đủ hơn.

---

### **Cách xây dựng GlobFire**

1. **Dữ liệu gốc**: Sử dụng dữ liệu vệ tinh MODIS (MCD64A1) làm đầu vào chính, nhưng có thể kết hợp các nguồn khác.
2. **Phương pháp chính**:
    - Dùng thuật toán **phân cụm DBSCAN** để nhóm các vùng cháy (burnt patches) thành một sự kiện cháy dựa trên **khoảng cách không gian-thời gian**.
    - Không phụ thuộc vào hệ thống chia ô (tiling system), giúp xử lý toàn cầu mà không làm chia nhỏ các đám cháy lớn.
3. **Định nghĩa sự kiện cháy**:
    - Các vùng cháy thuộc cùng một sự kiện nếu chúng **giao nhau** và xảy ra trong vòng **5 ngày**.
    - Đám cháy được coi là kết thúc nếu không có hoạt động mới trong **16 ngày**.

---

### **Nội dung dữ liệu GlobFire**

- Thông tin về các **sự kiện cháy rừng đơn lẻ**, bao gồm:
    - **Ngày bắt đầu và kết thúc** của mỗi đám cháy.
    - **Chu vi và diện tích cháy hàng ngày**.
- Dữ liệu này giúp theo dõi và phân tích diễn biến đám cháy theo thời gian.

---

### **Định dạng và truy cập**

- Dữ liệu được công bố dưới dạng:
    - **ESRI Shapefiles**.
    - **Cơ sở dữ liệu PostgreSQL**.
- Tích hợp với **Hệ thống Thông tin Cháy rừng Toàn cầu (GWIS)**.

---

### **Giá trị và ứng dụng**

- **Nghiên cứu hành vi và chế độ cháy rừng** trên toàn cầu.
- **Phân tích chi tiết** về số lượng, kích thước, và tốc độ lan truyền của các đám cháy.
- **Nghiên cứu cháy rừng cực đoan** và mối liên hệ với biến đổi khí hậu.
- **Tập trung vào đám cháy quan tâm** hoặc phân tích các yếu tố môi trường liên quan.

---

### **Tóm lại**

GlobFire là một cơ sở dữ liệu **độc đáo** và **toàn cầu** về cháy rừng, giúp:

- Nhận diện chi tiết từng sự kiện cháy rừng.
- Cung cấp thông tin sâu hơn về động lực cháy rừng.
- Hỗ trợ nghiên cứu và phân tích cháy rừng trong bối cảnh biến đổi khí hậu.


# References
