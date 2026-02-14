MỤC TIÊU

- Tạo hệ thống chat có memory thông minh, persistent và traceable.
- Memory bao gồm: messages, extracted_facts, vector_context, session_metadata.
- Persistence:
    - Checkpoints (snapshot/state timeline) → PostgreSQL (table public.checkpoints) via PostgresSaver.
    - Long‑term key/value store → PostgreSQL (PostgresStore table).
    - Embeddings/vector → vector collection (vecs client) name langgraph_history_cache (pgvector).

KIẾN TRÚC & LUỒNG XỬ LÝ

- StateGraph với nodes (từng bước): init → extract_facts → retrieve_vector → respond → vector_save → summarize → END.
- Mỗi node nhận/đổi state (MemoryState: messages, extracted_facts, vector_context, session_metadata).
- Khi chạy app.invoke(...) node thay đổi các channel; checkpointer ghi checkpoint incremental vào DB; PostgresStore lưu key/value nếu dùng.
- Vectors upsert vào collection (langgraph_history_cache).

CẤU TRÚC STATE / CHECKPOINT (như lưu trong public.checkpoints)

- checkpoint JSON chính gồm:
    - id, ts (timestamp)
    - versions_seen: node → version tokens (ai đã chạy)
    - channel_versions: channel → version token (messages/extracted_facts/vector_context/...)
    - updated_channels: list channel bị cập nhật trong snapshot này
    - channel_values: MAP chứa NHỮNG channel đã thay đổi trong snapshot hiện tại và giá trị thật (ví dụ vector_context hoặc messages nếu được lưu tại lần đó)
- Lưu ý: nhiều row chỉ chứa version tokens cho channel không thay đổi — nội dung thực tế nằm trong channel_values của các checkpoint nơi channel đó được cập nhật.
- DIỄN GIẢI NHANH KHI NHÌN VÀO ROW
	- Nếu trong checkpoint bạn thấy channel_versions là chuỗi số dài → đó là version token, không phải content.
	- Nội dung thật (messages/facts/vector_context) xuất hiện trong channel_values khi channel được cập nhật ở snapshot đó.
	- Để biết state hiện tại, dùng app.get_state() (nó sẽ merge các checkpoint theo version/time).
	- Để xem timeline đầy đủ hoặc replay, dùng app.get_state_history() hoặc đọc các rows theo ts / parent_checkpoint_id và merge channel_values tuần tựKẾT QUẢ / HIỂU KẾT QUẢ

- Kết quả mong muốn: persistent, recoverable memory cho mỗi thread_id.
- public.checkpoints lưu đủ thông tin để:
    - tái tạo state hiện tại (merge),
    - audit / replay từng bước (timeline),
    - debug bởi vì versions_seen chỉ ra node nào đã chạy.
- Embeddings không nằm trong checkpoints — kiểm tra collection langgraph_history_cache để xem records embeddings + metadata.

