2025-10-25 16:16


Tags: [[AI engineer]]

# AI Engineering

#### 1. What is the difference between fine-tuning and prompt-engineering 
- **Fine-tuning** là quá trình adapt model bằng cách update model weights của foundation model. Đòi hỏi sự đầu tư lớn về mặt dữ liệu và tài nguyên tính toán
- **Prompt Engineering** là kỹ thuật adapt model bằng cách cung cấp instruction và context phù hợp trong prompt, **mà không cần phải thay đổi trọng số mô hình**. Đây là kỹ thuật dễ và phổ biến nhất để bắt đầu
th
#### 2. How does RAG improve over standard LLM inference?
- RAG cải thiện suy luận của standard LLM inference bằng cách cung cấp context cần thiết, giải quyết các hạn chế chính của foundation model:
	- **Reduce Hallucination:** Bằng cách bổ sung thông tin liên quan từ nguồn bên ngoài, RAG giúp mô hình tạo ra phản hồi dựa trên thực tế documented facts và hạn chế việc tạo ra thông tin sai lệch
	- **Xử lý kiến thức outdated:** RAG cho phép mô hình truy cập và sử dụng thông tin mới nhất từ các nguồn dữ liệu bên ngoài
	- **Vượt qua giới hạn context length**: Khi dữ liệu cần thiết vượt quá context length của model, RAG chỉ cần truy xuất  các *chunks* liên quan nhất

#### 3. Explain what embeddings are used for in a retrieval system
- *Embeddings* là numerical representation (thường là các dense vectors) của dữ liệu gốc - nhằm mục đích nắm bắt ý nghĩa (semantics). Trong retrieval system based on embeddings, chúng được sử dụng để:
	- **Data Transformation**: Chuyển đổi documents (hoặc các chunks) và query của user thành các vector embedding
	- **Đo lường độ liên quan**: Cho phép so sánh semantic similarity giữa query và documents. Các documents có embedding gần với embedding của query (thường đo bằng cosine similarity) được coi là liên quan nhất và sẽ được truy vấn
#### 4. How would you mitigate hallucination in an LLM pipeline?
- Có vài phương án ví dụ như sau:
- **RAG để xây dựng context**: Cung cấp context đầy đủ để mô hình tham khảo khi response 
- **Prompting**: viết prompt phù hợp - ví dụ như: yêu cầu mô hình trả lời thành thật (trả lời không biết nếu không chắc chắn), chỉ dựa vào facts, không bịa đặt, tạo ra các constraints liên quan đến hallucination, việc yêu cầu mô hình tạo ra *phản hồi ngắn gọn* cũng giúp giảm hallucination
- **Evaluate**: Sử dụng _Knowledge-augmented verification_ như SAFE (*Search-Augmented Factuality Evaluator*) để kiểm tra tính xác thực của từng statement trong phản hồ 
- **Finetuning**: có thể sử dụng preference finetuning

#### 5. What's the difference between few-shot learning vs fine-tuning
- Sự khác biệt chính nằm ở mechanic và resource:
- **Few-shot Learning:** Là một dạng *in-context learning*. Hoạt động bằng cách cung cấp các ví dụ (shots) trong prompt mà không cần cập nhật model weights. Few-shot Learning bị giới hạn bởi context length 
- **Fine-tuning**: là quá trình update weights của model bằng cách tiếp tục training trên data cụ thể, đòi hỏi data và tài nguyên tính toán lớn hơn nhưng cho phép mô hình chuyên môn hóa cao hơn 
#### 6. Core components of a RAG pipeline
- Gồm có:
	- **Data Loading & Chunking**
	- **Embedding**
	- **Indexing & Storage**
	- **Retrieval**
	- **Augmentation & Generation**
#### 7. Làm thế nào để tối ưu hóa một ứng dụng LLM về độ trễ (latency) và chi phí (cost)?
- Các phương án có thể bao gồm: 
	- **Model Selection:** Chọn model nhỏ hơn, nhanh hơn nhưng vẫn đủ tốt cho tác vụ
	- **Quantization**: Giảm độ chính xác của mô hình để giảm kích thước và tăng tốc độ suy luận
	- **Caching**: Lưu lại kết qủa cho các câu hỏi thường gặp
	- **Prompt Optimize**: Viết prompt ngắn gọn hơn, yêu cầu câu trả lời ngắn hơn.
	- 
# References
