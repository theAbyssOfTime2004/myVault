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
	- **Khởi tạo**: Bắt đầu với từng ký tự riêng biệt là một đơn vị trong từ vựng (a, b, c, ..., z, etc.). Mỗi từ được biểu diễn bằng một chuỗi ký tự cộng với ký hiệu kết thúc `$` để phân biệt từ với từ khác có cùng tiền tố.
	- **Tạo word unit mới**: Đếm tất cả các cặp ký tự liền kề (bigram) trong corpus hiện tại. Tìm cặp xuất hiện **nhiều nhất** (most frequent) và gộp chúng lại thành một đơn vị mới trong từ vựng.
	- **Lặp lại**: cho đến khi kích thước từ vựng không vượt quá kích thước tối đa đã giả định.
### Composing word representations from characters 
- Các biểu word representation from characters thường được xây dựng bằng cách sử dụng CNNs hoặc RNNs. Các mạng này có thể xử lý chuỗi ký tự trong một từ và tổng hợp chúng thành 1 biểu diễn vector duy nhât cho từ đó, nắm bắt được ngữ nghĩa và cấu trúc của nó dựa trên các ký tự tạo nên nó.
### Tại sao chúng ta cần Subword Models khi đã có Word Embeddings?
 - Word embeddings truyền thống xử lý mỗi từ như một đơn vị riêng biệt và yêu cầu một từ vựng cố định. Điều này dẫn đến vấn đề out-of-vocabulary (OOV) khi gặp các từ mới hoặc hiếm gặp mà không có trong từ vựng huấn luyện. Subword models giải quyết vấn đề này bằng cách phân tách các từ thành các thành phần nhỏ hơn (ký tự hoặc subword units), cho phép mô hình xây dựng biểu diễn cho các từ OOV dựa trên các thành phần đã biết của chúng. Điều này giúp cải thiện khả năng tổng quát hóa và tính mạnh mẽ của chúng 
# References
