2025-07-21 10:41


Tags:

# Workflow của agent
- Ta có agent với định danh là `agent_id` và một danh sách các URL cần crawl `url`, cùng với `crawl_id`. Khi người dùng gọi API thì trạng thái của từng url trong `url` sẽ được chuyển đổi sang processing trong bảng `web_crawl_sources` từ backend, đồng thời một tin nhắn sẽ được push lên SQS để worker xử lý
### Training_worker() method:
- Tiếp đó ở backend sẽ có một method `training_worker()`  có nhiệm vụ liên tục nhận các message từ SQS để xử lý (với *wait_time=20s*), nghĩa là sau 20s không có tin nhắn nào từ SQS thì trả về `None`. Nếu có tin nhắn thì tạo các task song song `asyncio task` để xử lý bằng một method tên là `process_message`. Tiếp đó dùng `asyncio.gather` để đợi toàn bộ task chạy xong, lấy kết quả và log ra các task bị failed.
### process_message() method:
- Parse message từ SQS để lấy các `agent_id, crawl_id, url`
- Gọi hàm `create_trained_url_datasource` để xử lý crawl URL đó: 
	- Kiểm tra agent đã có `collection` và `datasource type` phù hợp chưa 
	- Nếu url đã từng train -> trả về `already_trained`
	- Nếu chưa, gọi `crawl_selected_link` -> crawl nội dung
	- Sau đó gọi `process_website()` -> tóm tắt và nhúng embedding
	- Update status về `Trained` hoặc `Error` 
### crawl_selected_link() method:
- Mở trang web bằng *playwright*, sau đó tạo browser, context và page với `user-agent` giả lập như người dùng thật 
-  `goto_with_retry()`: cố gắng truy cập lại trang web tối đa 3 lần nếu lỗi 
- Sau đấy sử dụng `process_html()` để làm sạch html:
	- Bỏ các thẻ không cần thiết
	- Trích xuất text, image, url bằng `_extract()` thành định dạng dễ hiểu cho AI 
- Dùng *LLM(OpenAI)* để tóm tắt nội dung:
	- prompt template như sau: 
```python
clean_prompt = f"""\
                                ###Role
                                Bạn là trợ lý tóm tắt nội dung văn bản, đảm bảo tóm tắt đầy đủ và chính xác.

                                ###Constraints
                                1. Nếu có đoạn **ví dụ** (bắt đầu bằng "Ví dụ" hoặc "Example"), hãy nhấn mạnh đó là phần ví dụ, giữ nguyên ý và không bỏ sót.
                                2. Nếu có các trường **Tên sản phẩm**, **Giá**, **SKU**, **Link ảnh**, **Link sản phẩm**, hãy nhấn mạnh và giữ nguyên các thông tin này khi tóm tắt.
                                3. Không thay đổi hay rút gọn bất kỳ URL nào.
                                4. Không bỏ qua hoặc lược bớt bất kỳ thông tin quan trọng nào trong văn bản.
                                5. Tuyệt đối không bịa, không suy diễn
                                Input cần format:
                                {cleaned_text}
                                """
```

### process_website()
- Data crawl xong sẽ được gửi qua phần RAG để chunking và lưu vector db.
- Nếu crawl content rỗng -> báo error, ngược lại gọi hàm `process_website` để lưu vào vector db
- Cuối cùng update status về Trained bằng `update_web_crawling_training_status()`
### extract() method
- 
# References
