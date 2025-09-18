



```python
from langchain.memory import (
BaseMemory, 
ConversationEntityMemory,
ConversationSummaryBufferMemory, 
VectorStoreRetrieverMemory, 
CombinedMemory)

-> 
from llama_index.core.memory import (
Memory, 
FactExtractionMemoryBlock, 
VectorMemoryBlock)
```


- `Memory` trong llamaindex có thể được thay thế bằng các class `CombinedMemory`(dùng kết hợp nhiều memory nhỏ) và `ConversationSummaryBufferMemory`, cùng các class phía dưới 
- `FactExtractionMemoryBlock` cùng với `fact_extraction_prompt_template` có chức năng trích xuất các fact và thông tin quan trọng từ hội thoại 
	-> Có thể thay thế được với `ConversationEntityMemory` cùng `entity_extraction_prompt` từ langchain (nhưng hiện tại đã deprecated và đã được migrating qua langGraph)

- `VectorMemoryBlock` để lữu trữ và tìm kiếm context hội thoại bằng vector
	-> Có thể thay thế bằng `VectorStoreRetrieverMemory` (Store the conversation history in a vector store and retrieves the relevant parts of past conversation based on the input.)

- `StaticMemoryBlock` hiện không dùng nên sẽ bỏ đi 

- Cần viết lại hàm `summarize_history()` để phù hợp với input từ langGraph memory, dùng cho việc tạo *full_question* từ *memory + input_query*   
- viết lại hàm `get_memory_content()` với memory của langGraph, dùng cho việc xem các thông tin quan trọng trong `ConversationEntityMemory`, và in ra short_term_memory + long_term_memory

- thay đổi cơ chế *persistance memory* vào supabase sang langGraph
```python
# persistence code hiện tại:
memory = Memory.from_defaults(
    session_id="user_001",
    token_limit=10000,
    chat_history_token_ratio=0.05,
    token_flush_size=300,
    memory_blocks=blocks,
    insert_method="system",
    async_database_uri=postgres_connection_str,  # ← Async PostgreSQL
    table_name="history_cache",                  # ← Table lưu memory
)

def save_to_memory(role: str, content: str) -> None:
    if memory is not None:
        try:
            msg = ChatMessage(role=role, content=content)
            memory.put(msg)  # ← Tự động lưu vào Supabase
        except Exception as e:
            print(f"Lỗi khi lưu vào memory: {str(e)}")

```

- **Lưu ý:** các class `ConversationEntityMemory`, `VectorStoreRetrieverMemory`, `ConversationSummaryBufferMemory`, `CombinedMemory` của langchain đã deprecated và sẽ cần được thay đổi sang langgraph

- `ConversationSummaryBufferMemory` ->  [summarize messages LangGraph](https://langchain-ai.github.io/langgraph/how-tos/memory/add-memory/#delete-messages)
- `VectorStoreRetrieverMemory` ->  [A Long-Term Memory Agent](https://python.langchain.com/docs/versions/migrating_memory/long_term_memory_agent/)
- `ConversationEntityMemory` -> [A Long-Term Memory Agent](https://python.langchain.com/docs/versions/migrating_memory/long_term_memory_agent/)