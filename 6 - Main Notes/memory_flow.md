[[SLZ]]
- Ngày 17/11/2025
- Luồng memory hiện tại:
	- quan tâm đến 2 endpoint `chat/summary` và `/chat-response`
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