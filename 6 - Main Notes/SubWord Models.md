2025-07-04 21:52


Tags:

# SubWord Models

### Subword Models là gì và tại sao chúng lại quan trọng?
- Subword models là các mô hình xử lý ngôn ngữ ở cấp độ subword thay vì toàn bộ từ. Chúng quan trọng vì các mô hình word embedding truyền thống giả định các từ là nguyên tử (atomic - không thể chia nhỏ ra hơn) và có 1 fix vocabulary. Trong các ứng dụng thực tế, chúng ta thường gặp các từ mà chúng ta không có word embedding cho chúng (out - of -vocab - words). Subword models giải quyết vấn đề này bằng cách cho phép chúng ta xây dựng các biểu diễn cho những từ chưa từng thấy trước đây
### Các loại Subword Models khác nhau là gì?
-  Có 3 loại Subword Models chính:
	- Loại 1: Sử dụng cùng kiến trúc với các mô hình dựa trên từ nhưng áp dụng embedding cho các đơn vị subword (ví dụ: các ký tự)
	- Loại 2: Bổ sung kiến trúc của các mô hình dựa trên từ với các mô hình con (submodels) tổng hợp biểu diễn từ từ các ký tự.
	- Loại 3: Từ bỏ hoàn toàn kiến trúc dựa trên từ và xử lý ngôn ngữ như 1 chuỗi ký tự được kết nối với nhau
### Tokenization WordPiece trong BERT hoạt động như thế nào? 
- WordPiece tokenization là một kỹ thuật được sử dụng trong các mô hình như Bert để chia văn bản thô thành các đơn vị subword. Quá trình này bao gồm việc chia các từ thành các phần nhỏ hơn, đôi khi là các prefix, suffix, hoặc các phần gốc của từ. Ví dụ, trong "morphological", nó có thể được chia thành "m ##or ##phological", với "##" cho biết rằng đó là 1 phần của từ lớn hơn. Điều này giúp mô hình xử lý các từ phức tạp hoặc hiếm gặp bằng cách phân tách chúng thành các đơn vị phổ biến hơn
### Byte Pair Encoding (BPE) là gì?
- BPE là 1 phương pháp phổ biến để tạo các subword units. Nó hoạt động bằng cách:
	- **Khởi tạo**: Bắt đầu từ vựng đơn vị từ 


# References
