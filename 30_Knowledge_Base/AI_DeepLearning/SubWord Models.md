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
### Các Subword Models cải thiện việc xử lý ngôn ngữ tự nhiên như thế nào?
 - Subword Models cải thiện việc xử lý ngôn ngữ tự nhiên bằng cách:
	 - **Giải quyết vấn đề với OOV:** Cho phép mô hình xử lý các từ mới hoặc hiếm gặp mà không có trong từ vựng ban đầu
	 - **Xử lý các lỗi chính tả và biến thể:** Bằng cách phân tích ở cấp độ subword, mô hình có thể xử lý tốt hơn các lỗi chính tả nhỏ hoặc các biển thể hình thái của từ
	 - N**ắm bắt ngữ nghĩa phong phú hơn:** Đối với các ngôn ngữ có hình thái phức tạp, các subword có thể giúp nắm bắt các sắc thái ngữ nghĩa và mối quan hệ giữa các từ tốt hơn
	 - **Giảm kích thước từ vựng:** Thay vì một từ vựng khổng lồ gồm tất cả các từ, Subword models có thể hoạt động hiệu quả hơn với một từ vựng nhỏ hơn gồm các đơn vị dưới từ.
### CNNs và RNNs được sử dụng như thế nào để biểu diễn từ cấp ký tự
- CNNs và RNNs là 2 kiến trúc neural network chính được sử dụng để tạo biểu diễn từ cấp ký tự:
	- **CNNs:** Thường được sử dụng để trích xuất các đặc trưng cục bộ từ chuỗi ký tự. Chúng có thể nhận diện các mẫu (n-grams ký tự) và kết hợp chúng thành một biểu diễn tổng thể theo từ.
	- **RNNs:** Đặc biệt hiệu quả trong việc xử lý các chuỗi tuần tự (sequential string). Chúng có thể đọc từng ký tự một và duy trì hidden state để ghi nhớ context của các ký tự trước đó, từ đó tạo ra một representation tổng hợp cho toàn bộ từ. 
	- Cả 2 đều cho phép mô hình học cách tổng hợp thông tin từ các ký tự riêng lẻ để tạo ra một biểu diễn có ý nghĩa cho từ đầy đủ
### Tóm lại: 
#### Types of Subword Models
| Type       | Description                                                       | Example                                                        |
| ---------- | ----------------------------------------------------------------- | -------------------------------------------------------------- |
| **Type 1** | Reuse word-level architectures, but apply them to subword tokens. | Replace word input with BPE or WordPiece                       |
| **Type 2** | Add character-level modules to word-based models.                 | Use CNN/RNN over characters to compose word vectors            |
| **Type 3** | Fully character-level modeling.                                   | Treat input as a character sequence (e.g., Char-CNN, Char-RNN) |
# References
