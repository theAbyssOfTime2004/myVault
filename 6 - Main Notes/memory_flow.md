[[SLZ]]
- Ngày 17/11/2025
- Luồng memory hiện tại:
	- quan tâm đến endpoint `chat/summary` 
	- Với `chat/summary`:
		- **Đầu vào**: Nó nhận tin nhắn mới của người dùng và bản tóm tắt cũ.
		- **Xử lý**: Nó gọi AI để tạo ra một bản tóm tắt mới, cập nhật hơn.
		- **Đầu ra**: Nó trả về một đối tượng JSON, trong đó có một trường quan trọng là [sum_history](vscode-file://vscode-app/usr/share/code/resources/app/out/vs/code/electron-browser/workbench/workbench.html). Giá trị của [sum_history](vscode-file://vscode-app/usr/share/code/resources/app/out/vs/code/electron-browser/workbench/workbench.html) chính là **chuỗi tóm tắt mới** của cuộc trò chuyện.

- Đi chi tiết vào `chat/summary`, để biết đã làm gì trong đó:
	- hàm xử lý endpoint này là `create_stateless_summary`, mọi thông tin cần thiết cho hàm này đều phải được cung cấp trong `payload: SummaryRequest`  
		- **Bước 1**: gọi hàm `handle_chat_and_build_prompt_stateless` và hàm này  sẽ nhận các thông tin sau: 
	```python
	history_result, usage_metadata = await handle_chat_and_build_prompt_stateless(
	user_input=payload.user_input, # tin nhấn mới nhất của người dùng
	ad_content=payload.ad_content, # Nội dung ads (nếu có)
	recent_messages=payload.recent_messages or "", # Một vài tin nhắn gần nhất
	previous_summary=payload.previous_summary or "", # summary của cuộc trò chuyện trước khi có tin nhắn mới
	conversation_id=payload.conversation_id,
)
	```
	- Hàm này sẽ gọi đến LLM và yêu cầu nó: "Dựa vào bản tóm tắt cũ, các tin nhắn gần đây và tin nhắn mới này, hãy tạo ra một bản tóm tắt mới", output từ hàm này sẽ là 1 object `history_result` chứa: 
		- sum_history: **Chuỗi tóm tắt mới đã được cập nhật**.
		- full_question
		- language
	- **Bước 2:** thêm thông tin khách hàng bằng cách gửi query tìm `customer_id` lên database, có được `customer_id` thì tiếp tục truy vấn trong bảng `customers` để tìm `customer_info`:
	```python
	if customer_id:
		try:
			customer_info = (supabase_client
				.table("customers")
				.select("name, phone, email, address", "gender", "pronoun")
				.eq("customer_id", customer_id)
				.execute()
			).data[0]
	```
	- Sau đó sử dụng hàm `format_input_with_context` để chèn `customer_info` vào vào bản tóm tắt `sum_history_text`: 
```python
context_kwargs = {
	"user_info": customer_info
}
sum_history_text = history_result.sum_history
sum_history_text = format_input_with_context(sum_history_text, **context_kwargs)
```
- **Bước 3:** trả về kết quả 
```python
return SummaryResponse(
	sum_history=sum_history_text,
	full_question=history_result.full_question,
	language=history_result.language,
	usage=usage_metadata,
)
```


- **Luồng hoạt động của hàm `handle_chat_and_build_prompt_stateless()`:
	- phần đầu tiên là fetch prompt từ db - theo 2 cách có hoặc không có previous_summary - để tạo system_prompt tạo full_question bằng user_messages(gồm previous_summary (nếu có), ad_content, recent_messages và user_input. 
	- phần thứ 2 là fetch system_prompt đó cùng user_message, truyền HistoryModel vào để đảm bảo output sẽ là dạng: class HistoryModel(BaseModel): sum_history: str full_question: str language: str 
	- cuối cùng trả về output + `usage_metadata`
	- `usage_metadata` là **thông tin chi tiết về việc sử dụng tokens của LLM call**, được OpenAI API trả về sau mỗi lần gọi. (mục đích quản lý chi phí, caching và monitoring)

- còn 1 implementation thứ 2 không được sử dụng(là file `langmem_process.py`), file này làm những việc sau: 
```
┌─────────────────────────────────────────────────────────┐
│  1. EXTRACT PHASE                                     │
├─────────────────────────────────────────────────────────┤
│  Input: Conversation messages                          │
│     ↓                                                 │
│  LLM Extract (3 parallel calls)                        │
│     ├─ Semantic Manager → [Triple1, Triple2, ...]      │
│     ├─ Episodic Manager → [Episode1, Episode2, ...]    │
│     └─ Profile Manager → UserProfile                   │
└────────────────────┬────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────┐
│  2. EMBEDDING PHASE                                   │
├─────────────────────────────────────────────────────────┤
│  For each extracted item:                              │
│     Triple1 → embed("User thích màu đỏ")               │
│         → [0.123, -0.456, ..., 0.789]  (1536 dims)      │
│     Triple2 → embed("User có budget 30 triệu")          │
│         → [0.321, 0.654, ..., -0.987]  (1536 dims)      │
│     Episode1 → embed("Tình huống: ... Suy nghĩ: ...")   │
│         → [0.111, 0.222, ..., 0.333]  (1536 dims)       │
│     UserProfile → embed("Tên: A, Sở thích: gaming")     │
│         → [0.444, 0.555, ..., 0.666]  (1536 dims)       │
└────────────────────┬────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────┐
│  3. STORAGE PHASE (InMemoryStore - RAM)                │
├─────────────────────────────────────────────────────────┤
│  Namespace Structure:                                  │
│                                                       │
│  ("memories", "user_001", "semantic")                  │
│    ├─ id_1: {value: Triple1, embedding: [...]}         │
│    ├─ id_2: {value: Triple2, embedding: [...]}         │
│    └─ ...                                             │
│                                                       │
│  ("memories", "user_001", "episodic")                  │
│    ├─ id_1: {value: Episode1, embedding: [...]}        │
│    └─ ...                                             │
│                                                       │
│  ("users", "user_001", "profile")                      │
│    └─ id_1: {value: UserProfile, embedding: [...]}     │
└────────────────────┬────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────┐
│  4. RETRIEVAL PHASE                                   │
├─────────────────────────────────────────────────────────┤
│  User Query: "sở thích người dùng"                     │
│     ↓                                                 │
│  Embed Query:                                         │
│     query_embedding = embed("sở thích người dùng")     │
│         → [0.234, 0.567, ..., 0.890]                   │
│     ↓                                                 │
│  Search InMemoryStore:                                 │
│     For each namespace (semantic, episodic, profile):   │
│         For each item in namespace:                    │
│             similarity = cosine_similarity(            │
│                 query_embedding,                      │
│                 item.embedding                        │
│             )                                         │
│         Sort by similarity DESC                       │
│         Return top K items                            │
│     ↓                                                 │
│  Results (Top 3 example):                              │
│     1. Triple1: "User thích màu đỏ" (similarity: 0.92)  │
│     2. UserProfile (similarity: 0.87)                   │
│     3. Episode1 (similarity: 0.81)                      │
└────────────────────┬────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────┐
│  5. FORMATTING PHASE                                  │
├─────────────────────────────────────────────────────────┤
│  Format results as context string:                     │
│                                                       │
│  === THÔNG TIN NGƯỜI DÙNG ===                          │
│  Tên: Nguyễn Văn A                                     │
│  Sở thích: gaming                                      │
│                                                       │
│  === KÝ ỨC NGỮ NGHĨA ===                               │
│  - User thích màu đỏ                                   │
│  - User có budget 30 triệu                             │
│                                                       │
│  === KÝ ỨC SỰ KIỆN ===                                 │
│  Tình huống: Khách hỏi PC gaming...                    │
│  Suy nghĩ: Tôi nghĩ nên recommend i5...                │
│  ...                                                  │
└─────────────────────────────────────────────────────────┘
```

- Drawback: với implementation `langmem_process.py` này thì còn gặp lỗi bị lặp memory 
- Implementation thứ 3 là `lg_memory.py` với langgraph memory