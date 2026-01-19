2026-01-19 14:20


Tags: [[TigerTribe]], [[HNK-SMARTAP-BREWBUDDY]]

# Overview Architecture

```mermaid
graph TD
    Main[main.py] --> API[API Layer]
    API --> Workflow[BeerOrderingWorkflow]
    
    Workflow --> Prepare[Prepare]
    Prepare --> Parallel{Parallel}
    Parallel -->|1| Compliance[Compliance]
    Parallel -->|2| Extract[Extraction]
    
    Compliance --> Decision[Decision]
    Extract --> Decision
    Decision --> Finalize[Finalize]
    
    Compliance --> CompSvc[Compliance Service]
    Extract --> ExtrSvc[Extraction Service]
    Decision --> StateSvc[State Service]
    
    CompSvc --> Agent[Agent Service]
    ExtrSvc --> Agent
    StateSvc --> Agent
    
    Agent --> Redis[(Redis)]
    Agent --> Blob[(Azure Blob)]
    
    style Workflow fill:#e1f5fe
    style Agent fill:#fff3e0
    style Redis fill:#ffebee
    style Blob fill:#ffebee
```

## Detailed Workflow with Classes/Methods Mapping:

```mermaid
graph TD
    Start[POST /api/v1/chat/beer-ordering] --> Verify[verify_api_key]
    Verify --> BeerOrderingChat[beer_ordering_chat]
    
    BeerOrderingChat --> ValidateULID[_is_valid_ulid]
    BeerOrderingChat --> ValidatePayload[_validate_payload]
    
    BeerOrderingChat --> GetSession[chat_service.get_chat_session]
    GetSession --> GetSessionRepo[chat_session_repository.get_session]
    
    GetSession --> WorkflowRun[beer_ordering_workflow.run]
    
    WorkflowRun --> Prepare[_prepare_step_executor]
    Prepare --> GetLastMsg[state_management_service.get_last_assistant_message]
    
    Prepare --> Parallel{Parallel Analysis}
    
    Parallel -->|1| ComplianceStep[_check_compliance_step_executor]
    Parallel -->|2| ExtractStep[_extraction_step_executor]
    
    ComplianceStep --> CheckCompliance[compliance_service.check_compliance]
    ExtractStep --> ExtractInfo[information_extraction_service.extract_information]
    
    CheckCompliance --> CompAgent[agent_service.run_async]
    ExtractInfo --> ExtrAgent[agent_service.run_async]
    
    Parallel --> Router[compliance_router]
    
    Router -->|violated| InvalidStep[_invalid_compliance_step_executor]
    Router -->|passed| DecisionStep[_decision_step_executor]
    
    InvalidStep --> EndSession[chat_service.end_chat_session]
    InvalidStep --> SaveHistory1[chat_service.save_chat_history]
    
    DecisionStep --> DecideNext[state_management_service.decide_next_step]
    DecideNext --> StateAgent[agent_service.run_async]
    
    DecisionStep --> InverseMap[inverse_map_mood_occasion]
    
    DecisionStep --> Finalize[_finalize_step_executor]
    
    Finalize --> SetSession[chat_service.set_chat_session]
    Finalize --> SaveHistory2[chat_service.save_chat_history]
    
    SetSession --> UpsertSession[chat_session_repository.upsert_session]
    SaveHistory2 --> SaveHistoryRepo[chat_history_session_repository.save_session]
    
    CompAgent & ExtrAgent & StateAgent --> Redis[(Redis DB)]
    UpsertSession & SaveHistoryRepo --> Blob[(Azure Blob Storage)]
    
    Finalize --> Response[ChatBeerOrderingResponse]
    
    style WorkflowRun fill:#e1f5fe
    style Parallel fill:#fff3e0
    style CompAgent fill:#ffebee
    style ExtrAgent fill:#ffebee
    style StateAgent fill:#ffebee
    style Redis fill:#e8f5e9
    style Blob fill:#e8f5e9
```


- Vị trí chính xác trong repo:
```python
beer_ordering_chat() → app/api/chat.py:48

_is_valid_ulid() → app/api/chat.py:191

_validate_payload() → app/api/chat.py:198

get_chat_session() → app/services/chat_services/chat_service.py:26
 beer_ordering_workflow.run() → app/services/workflows/beer_ordering_workflow.py:67

_prepare_step_executor() → app/services/workflows/beer_ordering_workflow.py:124
 _check_compliance_step_executor() → app/services/workflows/beer_ordering_workflow.py:164
 _extraction_step_executor() → app/services/workflows/beer_ordering_workflow.py:180

check_compliance() → app/services/chat_services/compliance_service.py:17

extract_information() → app/services/chat_services/information_extraction.py:20

compliance_router() → app/services/workflows/beer_ordering_workflow.py:407

 _decision_step_executor() → app/services/workflows/beer_ordering_workflow.py:198

decide_next_step() → app/services/chat_services/state_management.py:39

 _finalize_step_executor() → app/services/workflows/beer_ordering_workflow.py:332

set_chat_session() → app/services/chat_services/chat_service.py:51

save_chat_history() → app/services/chat_services/chat_service.py:114
```

1. Trigger Workflow:
	- Sau khi `beer_ordering_chat (API)` thực hiện xong validate và lấy session state.
	- Hàm` BeerOrderingWorkflow.run()` được gọi.
	- `self.workflow.arun()` kích hoạt workflow engine.
2. Execution Chain:
	- Bước 1: *prepare_step*: (`_prepare_step_executor`): Chuẩn bị input, merge state hiện tại và request mới.
	- Bước 2: Parallel:
		- *compliance_step*: (`_check_compliance_step_executor`): Kiểm tra compliance -> gọi `compliance_service.check_compliance `  -> Trả về `compliance_result`.
		- *extraction_step*: (`_extraction_step_executor`): Trích xuất thông tin (mood, flavor, etc.) -> Trả về `extracted_info`.
	- Bước 3: Router:
		- `compliance_router`: Nhận input từ Parallel trước đó.
		- Kiểm tra `compliance_result.`
		- Nếu Vi phạm (`is_violated`): -> Gọi i`nvalid_compliance_step`.
		- Nếu An toàn: -> Gọi `decision_step`.
3. Violation Path:
	- invalid_compliance_step (_invalid_compliance_step_executor):
	- Lưu lịch sử chat.
	- Kết thúc session (`end_chat_session`).
	- Trả về response với `renderingType="chat-terminated"`.
4. Happy Path - Decision:
	- decision_step (_decision_step_executor):
		- Tổng hợp kết quả từ extraction và compliance.
		- Cập nhật logic nghiệp vụ (ví dụ: state mapping, intent count).
		- Gọi AI (`state_management_service`) để quyết định câu trả lời tiếp theo.
	- finalize_step (_finalize_step_executor):
		- Lưu state mới vào DB.
		- Trả về response cuối cùng cho API.
# References
