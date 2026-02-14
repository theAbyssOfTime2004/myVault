[[SLZ]]


- có 2 lọai tóm tắt:
	- **thứ 1 là:** `summarize_history_node():` tóm tắt và cắt bớt message khi số lượng tin nhắn > `MAX_MESSAGES` (đang set là 20), sau tóm tắt -> xóa bớt tin nhắn cũ chỉ giữ lại 10 tn -> kết quả tóm tắt được lưu vào `state["summary"]`
		- Tóm tắt này sẽ xuất hiện trong phần `🕒 Tóm tắt hội thoại trước:` ở cuối `memory_content`.
	- **thứ 2 là:** `trong get_memory_content_from_state():` tóm tắt 5 tin gần nhất nếu chúng vượt quá `SHORT_TERM_TOKEN_THRESHOLD` (đang set là 200 tokens), **không xóa tin nhắn**, chỉ tóm tắt để hiển thị.
		- Tóm tắt này xuất hiện trong phần `🕒 Tóm tắt lịch sử gần nhất:` (ở **đầu** `memory_content`).
	
- **lg_memory.py**: có 7 thay đổi quan trọng:
1. ✅ **XÓA vecs** - Chỉ dùng PostgresStore
2. ✅ **Enable semantic search** - Tự động embedding
3. ✅ **Refactor vector ops** - Dùng Store API thay SQL
4. ✅ **RemoveMessage** - LangGraph best practice
5. ✅ **Better fact extraction** - Ưu tiên tên chính xác
6. ✅ **Smart reconnection** - Error handling tốt hơn
7. ✅ **Smart summarization** - Tiết kiệm tokens

refactored lại dựa trên [docs langgraph memory](https://docs.langchain.com/oss/python/langgraph/add-memory) 