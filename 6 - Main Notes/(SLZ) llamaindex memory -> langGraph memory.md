
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

- `FactExtractionMemoryBlock` cùng với `fact_extraction_prompt_template` có chức năng trích xuất các fact và thông tin quan trọng từ hội thoại 
	-> Có thể thay thế được với `ConversationEntityMemory` cùng `entity_extraction_prompt` từ langchain (nhưng hiện tại đã deprecated và đã được migrating qua langGraph)

- `VectorMemoryBlock` để lữu trữ và tìm kiếm context hội thoại bằng vector
	-> Có thể thay thế bằng `VectorStoreRetrieverMemory`

- `StaticMemoryBlock` hiện không dùng nên sẽ bỏ đi 

- Cần viết lại hàm `summarize_history()` để phù hợp với input từ langGraph memory, dùng cho việc tạo *full_question* từ *memory + input_query*   
- viết lại hàm `get_memory_content()` với memory của langGraph, dùng cho việc xem các thông tin quan trọng trong `ConversationEntityMemory`, và in ra short_term_memory + long_term_memory