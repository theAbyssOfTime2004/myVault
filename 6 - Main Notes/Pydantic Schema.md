2026-01-19 22:33


Tags: [[AI Engineering]]

# Pydantic Schema

# Lý thuyết và ứng dụng của lớp Pydantic trong AI Agent system

## 1. Bản chất và Cơ chế của Pydantic

**Pydantic** là một thư viện thực thi **Schema Enforcement** và **Data Validation** dựa trên hệ thống _Type Hinting_ của Python. Thay vì chỉ kiểm tra kiểu dữ liệu một cách thụ động, Pydantic đảm bảo tính toàn vẹn của dữ liệu thông qua cơ chế **Parsing**.

- **Cơ chế chuyển đổi (Type Coercion):** Pydantic không chỉ xác thực mà còn nỗ lực chuyển đổi dữ liệu đầu vào (Input) về đúng kiểu dữ liệu mục tiêu (Target Type) đã được định nghĩa.    
- **Data Integrity:** Đảm bảo dữ liệu chảy qua các thành phần hệ thống luôn nhất quán, giảm thiểu rủi ro lỗi thực thi (Runtime Errors) trong các hệ thống phân tán hoặc vi dịch vụ (Microservices).
- **Vai trò nền tảng:** Là thành phần cốt lõi trong việc ánh xạ giữa dữ liệu phi cấu trúc và các hệ thống quản trị cơ sở dữ liệu (RDBMS/NoSQL) hoặc các giao thức truyền tải (REST/gRPC).

## 2. Pydantic và Giao thức Structured Output

Trong kiến trúc LLM, **Structured Output** là giải pháp cho vấn đề "Tính bất định" (Non-determinism) của ngôn ngữ tự nhiên.

- **Cơ chế chuyển đổi Schema:** Một lớp Pydantic được biên dịch thành một bản đồ **JSON Schema**. Bản đồ này đóng vai trò là một "ràng buộc logic" buộc LLM phải ánh xạ xác suất từ ngữ sang một cấu trúc dữ liệu cố định.
- **Ngữ nghĩa học trong Schema (Semantic Enrichment):** Việc sử dụng thuộc tính `Field(description=...)` cung cấp ngữ cảnh ngữ nghĩa trực tiếp cho mô hình, giúp tối ưu hóa quá trình trích xuất thực thể (Entity Extraction) và phân loại dữ liệu mà không cần Prompt quá dài.
-  Tóm lại, nói 1 cách dễ hiểu thì các lớp Pydantic giúp ta định nghĩa một đầu ra có cấu trúc (strutured output), thường là JSON và điều này rất tốt để dùng làm đầu vào cho các LLM hiện đại         

## 3. Tool Calling và Giao tiếp Liên thành phần

Quy trình gọi hàm (Function Calling) là một bài toán điều phối (Orchestration) dữ liệu giữa LLM và các hệ thống thực thi ngoại vi.

|Giai đoạn|Vai trò kỹ thuật|Ứng dụng của Pydantic|
|---|---|---|
|**Khai báo (Declaration)**|Định nghĩa chữ ký hàm (Function Signature).|Mô tả chính xác kiểu dữ liệu và ràng buộc của các tham số đầu vào.|
|**Định hướng (Routing)**|LLM lựa chọn công cụ phù hợp nhất dựa trên truy vấn.|Cung cấp Metadata thông qua Schema để AI thực hiện ánh xạ logic.|
|**Trích xuất (Extraction)**|Chuyển đổi ngôn ngữ tự nhiên thành tham số hàm.|Đảm bảo tính hợp lệ (Validation) của tham số trước khi thực thi mã nguồn.|
|**Thực thi (Execution)**|Xử lý logic tại Backend.|Ngăn chặn các lỗi Injection hoặc sai lệch kiểu dữ liệu gây sập hệ thống.|

Xuất sang Trang tính

## 4. Phân tích sự khác biệt trong Hiệu năng Tìm kiếm (Search)

Sự chênh lệch giữa Web Search của ChatGPT và các API thô không nằm ở mô hình ngôn ngữ, mà ở **Kiến trúc Điều phối (Orchestration Architecture)**.

- **Raw API (Atomic Search):** Thực hiện một truy vấn duy nhất. Hệ thống này thiếu khả năng tự hiệu chỉnh nếu kết quả tìm kiếm ban đầu không chứa thông tin mục tiêu.
- **Agentic Search (Multi-hop Search):** Sử dụng các chu trình tư duy lặp (Iterative Reasoning). Hệ thống thực hiện phân rã câu hỏi (Query Decomposition), đánh giá mức độ liên quan của thông tin (Relevance Scoring) và tự động tái cấu trúc truy vấn nếu cần thiết.

## 5. Kiến trúc Agentic Workflow tối ưu

Một hệ thống tìm kiếm thông minh cần được vận hành bởi một chuỗi các **Pydantic Models** đóng vai trò là các trạm kiểm soát (Checkpoints):

1. **Query Decomposition Model:** Phân rã một vấn đề phức tạp thành các tiểu mục truy vấn có thể thực thi độc lập.
2. **Context Extraction Model:** Định nghĩa cấu trúc dữ liệu cần trích xuất từ các trang web thô (loại bỏ nhiễu HTML).
3. **Reflection & Critique Model:** Sử dụng một tác nhân AI thứ cấp để kiểm soát chất lượng (Quality Assurance), đối chiếu kết quả tìm kiếm với yêu cầu ban đầu của người dùng.
4. **Recursive Feedback Loop:** Nếu chỉ số tin cậy (Confidence Score) thấp, hệ thống tự động kích hoạt lại chu kỳ tìm kiếm với các tham số đã được tinh chỉnh.


# References
