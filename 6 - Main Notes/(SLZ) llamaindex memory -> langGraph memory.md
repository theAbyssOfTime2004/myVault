
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