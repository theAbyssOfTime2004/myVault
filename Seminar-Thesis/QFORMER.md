[[seminar HCMUS]]
### 1. **Hiểu vai trò của Qformer trong DASCO paper**

- **Qformer là gì?** Đây là một transformer-based module (từ BLIP-2) sử dụng "query-based attention" để bridging (kết nối) và alignment (căn chỉnh) giữa image features (V) và text features. Thay vì chỉ concatenate hoặc average như code hiện tại, Qformer học cách "hỏi" (query) từ text để tương tác với image patches, tạo ra representations chung cho multimodal.
- **Tại sao cần?** Trong mô tả gốc, V là visual features được xử lý qua Qformer để align với text (ví dụ: aspect "camera" được align với visual patches của camera). Code hiện tại thiếu phần này, nên fusion chỉ là cơ bản (average với [CLS] token), không tối ưu cho alignment tinh tế.
- **Lợi ích**: Cải thiện multimodal understanding, giúp model hiểu mối quan hệ giữa text và image tốt hơn, đặc biệt cho ABSA (aspect-based sentiment analysis).

--- 
- Q-former là 1 thành phần đặc biệt của Blip2 (mô hình multimodal), Q-former đóng vai trò như cầu nối giữa ảnh và text encoder
- **Mục tiêu**: học cách liên kết đặc trưng hình ảnh cho phù hợp với ngôn ngữ 
	- Đầu vào: 
		1. `query_embeds`: một tập *learnable query tokens*
			- *Ví dụ: 32 vector query, mỗi vector kích thước 768*
			- dạng `[batch_size, num_query_tokens, hidden_dim]`
		2. `encoder_hidden_states`: đặc trưng ảnh sau khi qua image encoder
			- ví dụ: `[batch_size, num_image_patches, hidden_dim]`
- Trong Blip2, "query" là một **vector truy vấn để hỏi ảnh điều gì đó**, Q-former học cách rút ra các thông tin cần thiết trong ảnh dựa vào các vector truy vấn này, trong mô hình gốc Blip2, query là các *learnable query tokens* (learnable params)
	- **Mục đích:** trích xuất general embedding tống quát của ảnh mà không cần câu hỏi cụ thể 
- Đối với các bài về MABSA (như trong DASCO), ta muốn align **ảnh** với **aspect**, nhưng *learnable query tokens* không linh hoạt cho từng khía cạnh như vậy , nên đã thay thế bằng *text query embeddings* - embedding của từ “food”, “service”, “ambience”, …
- ![[Pasted image 20251004201925.png]]