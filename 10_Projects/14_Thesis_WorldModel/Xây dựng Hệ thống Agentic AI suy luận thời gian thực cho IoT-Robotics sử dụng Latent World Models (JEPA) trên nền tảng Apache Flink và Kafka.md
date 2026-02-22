1. **Thiết lập luồng (Data Engineering nhẹ):** Dựng Kafka và Flink cục bộ. Viết script Python giả lập việc phát (publish) một bộ dữ liệu chuỗi thời gian hoặc video cảm biến vào Kafka.

2. **Triển khai World Model (Core Data Science):** Sử dụng PyFlink (Flink API cho Python) để load mô hình pre-trained TS-JEPA hoặc V-JEPA 2. Đóng băng (freeze) phần lớn mô hình, chỉ thực hiện inference (suy luận) hoặc fine-tune một lớp nhỏ (ví dụ: Linear Probe) trên luồng dữ liệu.

3. **Lập kế hoạch và Lấy mẫu (Action/Planning):** Lập trình để khi luồng dữ liệu chảy qua, World Model trong Flink sẽ liên tục tạo ra các "dự đoán tương lai" (rollouts). Nếu hệ thống dự đoán có sự cố (ví dụ: nhiệt độ quá nhiệt, quỹ đạo lệch), Agent sẽ kích hoạt tín hiệu cảnh báo hoặc thay đổi hành động

**Tên đề tài:** Xây dựng Hệ thống Agentic AI suy luận thời gian thực cho tác nhân Embodied AI sử dụng Latent World Models (kiến trúc V-JEPA) trên nền tảng Data Streaming. **Dữ liệu:** Dữ liệu tổng hợp (synthetic data) dạng chuỗi thời gian gồm các cặp (Khung hình ảnh quan sát, Hành động của tác nhân) được sinh ra từ các môi trường mô phỏng vật lý có tính tương tác (như OpenAI Gymnasium), sau đó được giả lập thành các luồng sự kiện (event streams) liên tục để kiểm thử khả năng chịu tải của hệ thống thời gian thực. **Sơ lược về methodology:** Đề tài là sự kết hợp End-to-End giữa nghiên cứu AI cốt lõi và hạ tầng dữ liệu phân tán. Về mặt AI, phương pháp tiếp cận là đóng băng (freeze) mạng V-JEPA pre-trained của Meta để nén khung hình pixel thành vector không gian ẩn zt​, thiết kế và huấn luyện mạng Predictor (Transformer/RNN) nhúng vector hành động at​ vào zt​ để dự đoán trạng thái ẩn tương lai z^t+1​ (năng lực thấu hiểu vật lý được kiểm chứng bằng Linear Probing). Về mặt Kỹ thuật dữ liệu, kiến trúc streaming sử dụng Apache Kafka để hứng luồng dữ liệu giả lập tốc độ cao, kết hợp với Apache Flink để xử lý đồng bộ hóa cửa sổ thời gian (time-windowing), và tích hợp mô hình AI đã đóng gói vào Inference Server nhằm thực hiện suy luận (real-time inference) với độ trễ siêu thấp.


### Giai đoạn 1: Khởi tạo & Thiết lập "Data Contract" (Tuần 1 - 2)

Mục tiêu: Chốt giao thức giao tiếp giữa Model và Hệ thống Streaming.

- **Nhiệm vụ chung (Cả 2 người):** * Thống nhất định dạng dữ liệu truyền tải (JSON hoặc Protobuf).
    
    - Chốt chính xác chiều (shape) của Tensor đầu vào (ví dụ: ảnh 64×64×3, vector hành động 1×3).
        
- **Task của bạn (AI Lead):** * Cài đặt thư viện OpenAI Gymnasium, chọn môi trường `CarRacing-v2`.
    
    - Viết script cho tác nhân chạy ngẫu nhiên để thu thập khoảng 50.000 khung hình và hành động.
        
    - Đóng gói và lưu dataset tĩnh này dưới dạng file `.hdf5` hoặc `.pt`.
        
- **Task của bạn DE:**
    
    - Khởi tạo cụm Apache Kafka (local hoặc cloud).
        
    - Viết script "Mock IoT": Đọc bộ dataset tĩnh của bạn và bắn từng cặp (Frame, Action) vào Kafka topic với tốc độ 30 frames/giây để giả lập luồng dữ liệu thời gian thực.
        

### Giai đoạn 2: Phát triển song song (Tuần 3 - 8)

Mục tiêu: Ai làm việc nấy. Xây dựng hoàn chỉnh "Bộ não" và "Đường ống".

- **Task của bạn (AI Lead):**
    
    - _Tuần 3-4:_ Load pre-trained V-JEPA (đã đóng băng trọng số). Đưa toàn bộ dataset offline qua mô hình để trích xuất ra các latent vectors zt​. Lưu tập latent data này xuống ổ cứng.
        
    - _Tuần 5-7:_ Tận dụng tư duy và kỹ năng của một AI Engineer để viết custom PyTorch `Dataset`/`DataLoader` tối ưu. Thiết kế mạng Predictor (Transformer/RNN), nhúng (embed) vector hành động at​ vào zt​ và huấn luyện mô hình dự đoán z^t+1​.
        
    - _Tuần 8:_ Chạy Linear Probing để đánh giá độ thấu hiểu vật lý của mô hình. Xuất (export) model PyTorch sang định dạng `.onnx` siêu nhẹ và giao cho bạn DE.
        
- **Task của bạn DE:**
    
    - _Tuần 3-5:_ Thiết lập Apache Flink. Viết các job đọc dữ liệu streaming từ Kafka, xử lý cửa sổ thời gian (time-windowing) và gom nhóm dữ liệu (batching).
        
    - _Tuần 6-8:_ Cài đặt Inference Server (Triton Inference Server hoặc TorchServe). Tích hợp một model giả (dummy model) vào trước để test luồng gọi API từ Flink sang Server xem có thông suốt không.
        

### Giai đoạn 3: Tích hợp hệ thống End-to-End (Tuần 9 - 10)

Mục tiêu: Nối luồng dữ liệu, ghép "Bộ não" vào "Đường ống".

- **Nhiệm vụ chung:** * Đưa file `.onnx` thật của bạn vào Triton Server.
    
    - Chạy toàn bộ luồng: _Mock IoT script → Kafka → Flink → Triton Server (chạy V-JEPA Predictor) → Kafka (Topic kết quả)._
        
    - Cùng nhau debug các lỗi phát sinh: Sai lệch shape tensor khi truyền qua mạng, lỗi OOM trên server, hoặc các gói tin bị rớt (data loss).
        

### Giai đoạn 4: Tối ưu hiệu năng thời gian thực (Tuần 11)

Mục tiêu: Đạt chuẩn Real-time (Độ trễ toàn hệ thống < 100ms).

- **Task của bạn (AI Lead):** Kiểm tra lại file `.onnx`, lược bỏ các node tính toán dư thừa hoặc áp dụng lượng tử hóa (quantization) để model dự đoán nhanh hơn nữa nếu hệ thống đang bị nghẽn tại bước inference.
    
- **Task của bạn DE:** Tối ưu hóa bộ nhớ heap của Flink, chỉnh lại kích thước batch size truyền vào Triton Server để đạt thông lượng (throughput) cao nhất mà không làm tăng độ trễ (latency).
    

### Giai đoạn 5: Viết báo cáo & Chuẩn bị bảo vệ (Tuần 12 - 14)

Mục tiêu: Hoàn thiện tài liệu và sẵn sàng trả lời phản biện.

- **Task của bạn (AI Lead):** Viết các chương về Cơ sở lý thuyết (Latent World Models, V-JEPA), kiến trúc mạng Predictor, phương pháp Action Embedding, và phân tích biểu đồ hàm Loss / độ chính xác của Linear Probing.
    
- **Task của bạn DE:** Viết các chương về Kiến trúc hướng sự kiện (Event-driven), cơ chế xử lý của Kafka/Flink, cách giải quyết Backpressure, và các biểu đồ benchmark đo lường Latency/Throughput.
    
- **Nhiệm vụ chung:** Làm slide thuyết trình và quan trọng nhất: **Quay một video demo 3-5 phút** quay lại cảnh hệ thống đang nuốt luồng streaming và liên tục dự đoán trạng thái tương lai trên màn hình console để trình chiếu cho hội đồng xem.