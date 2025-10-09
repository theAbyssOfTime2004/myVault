pipeline:
```python
input -> provider -> builder -> processor -> renderer -> markdown
```
### provider: 
- **PDFProvider cung cấp đầu vào đầy đủ cho giai đoạn Builder**: toàn bộ text và hình ảnh của tài liệu, kèm thông tin bố cục cơ bản. Quá trình này kết hợp _“text gốc + OCR bổ sung”_ để đạt độ chính xác cao và tốc độ tối ưu
thực hiện các  bước sau:
- **Mở file pdf**
- **Duyệt qua các trang pdf**: 
	- Lấy text: sử dụng `page.get_text()` hoặc `TextPage` API để lấy từng đoạn/ký tự cùng bounding box
	- Lấy ảnh: render toàn bộ trang ra bitmap rồi cắt ảnh theo toạ độ, hoặc trực tiếp trích xuất bytes ảnh nếu có. Mỗi ảnh sẽ được lưu ra file (ví dụ đặt tên theo trang: `page_0_image_1.png`, …) và một block _Image_ tương ứng được tạo, chứa đường dẫn đến file ảnh đã lưu.
	- lấy thông tin font, kích thước
	- raw structure của trang: các **block thô**, chỉ cần cung cấp danh sách **dòng chữ rời rạc** (lines) và **đối tượng phi chữ** (như images), kèm tọa độ cho tất cả những thành phần này.
- **OCR (nếu cần thiết)**: 
	- nếu toàn bộ text là scan img, hoặc bị encrypted -> gọi **Surya OCR**
	- nếu flag `--force_ocr`: sẽ bỏ qua hoàn toàn text PDF và OCR tất cả các trang để đảm bảo không bỏ sót (dùng trong trường hợp text gốc bị lỗi encoding)
- Tạo đối tượng **Document** gồm:
	- `page.text_blocks`
	- `image.text_blocks`
	- Có thể có `page.figure_blocks`, `page.table_blocks` thô nếu Provider bước đầu nhận diện được (ví dụ bằng cách nhìn hình ảnh đường kẻ bảng), nhưng thường việc xác định block loại gì sẽ do Builder làm.
	- Thông tin khác: chiều rộng/cao trang, số trang,..