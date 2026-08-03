---
tags: [project, job-hunt, interview, data-engineer, home-credit, active]
status: active
created: 2026-07-31
event: Assessment Center — 2026-08-06 (Thu)
role: Data Engineer — HomeRacer / Home Credit
---

# HomeRacer AC Prep — Data Engineer (6/8/2026)

> **Đọc dòng này trước khi hoảng:** AC không phải bài thi kiến thức hóc búa hay live-coding cạnh tranh. Nó chấm **cách bạn hỏi để hiểu đề, cách bạn phối hợp nhóm, cách bạn trình bày**. Bạn không cần biết mọi thứ — bạn cần biết cách nghĩ có cấu trúc và nói ra thành lời. Tài liệu này cho bạn đủ nội dung để không bao giờ "trắng đầu".

---

## PHẦN 0 — Cheat sheet (đọc sáng 6/8, 5 phút)

**Khung 5 câu hỏi làm rõ đề (dùng cho MỌI case):**
1. **Mục tiêu & metric** — Giải quyết vấn đề gì? Đo thành công bằng gì? Sau đó ai làm gì với kết quả?
2. **Người dùng & quyết định** — Ai dùng output? Nó phục vụ quyết định nào?
3. **Dữ liệu** — Ta có data gì? Chất lượng ra sao?
4. **Ràng buộc** — Realtime hay batch? Quy mô? Latency? Ngân sách?
5. **Giả định** — Nói thành lời: "Em giả định X, nếu sai thì điều chỉnh."

**Streaming pipeline — vẽ được sơ đồ này:**
`Source → Ingestion → Message Broker → Stream Processor → Sink (serving store / lake / warehouse)`

**Present 3 nhịp:** Vấn đề + giả định → Giải pháp (vẽ flow) → Đánh đổi + bước tiếp theo.

**3 từ khóa ăn điểm:** *idempotency*, *checkpointing*, *state assumptions explicitly*.

**Teamwork một câu:** Hỏi product về mục tiêu, hỏi DA về data, mình lo hệ thống/pipeline, rồi tổng hợp lại. Kéo người vào, đừng đè bằng thuật ngữ.

---

## PHẦN 1 — Group Case (cấu phần chấm nặng nhất)

### 1.1 Chuyện gì xảy ra
Ghép nhóm với ứng viên khác (product, DA...). Cùng giải một bài toán / thiết kế một data product. **Chỉ design plan, không build.** Ai cũng present. Chấm: đặt câu hỏi hiểu đề, teamwork, present.

### 1.2 Home Credit làm gì (để đoán đề)
Tài chính tiêu dùng: vay trả góp, vay tại điểm bán (POS), thẻ tín dụng. Đề DE thường quanh:
- Dự đoán/cảnh báo khách **trễ hạn thanh toán** (collections)
- **Phát hiện gian lận** giao dịch
- **Chấm điểm rủi ro tín dụng** (credit scoring)
- **Gợi ý sản phẩm** vay/thẻ
- **Giám sát giao dịch realtime**

### 1.3 Khung 5 câu hỏi — giải thích
Dân tech hay lao vào giải ngay → mất điểm. Người được chấm cao **hỏi trước khi giải**. Với mỗi đề, chạy tuần tự:

1. **Mục tiêu & metric.** "Cái này giải quyết vấn đề gì, đo thành công bằng metric nào?" → Ví dụ giảm tỷ lệ default? Tăng precision cảnh báo? Quan trọng: **sau khi có kết quả thì AI/người làm gì với nó** (gọi điện, gửi SMS, cơ cấu lại nợ).
2. **Người dùng & quyết định.** Ai dùng — team collections? Tự động? Quyết định gì được đưa ra?
3. **Dữ liệu có sẵn.** Lịch sử thanh toán? Giao dịch? Nhân khẩu học? Dữ liệu bureau ngoài? Chất lượng/độ đầy đủ?
4. **Ràng buộc.** Cần realtime hay batch hằng ngày là đủ? Bao nhiêu khách? Yêu cầu latency? Ngân sách hạ tầng?
5. **Nêu giả định.** Khi thiếu thông tin, KHÔNG đoán ngầm — nói ra: *"Em giả định scoring batch hằng ngày là đủ vì collections hành động vào hôm sau."*

### 1.4 Teamwork — nước đi cụ thể
Nhóm hỗn hợp (product, DA). Hai cái chết: **im lặng** hoặc **đè mọi người bằng jargon DE**.

Nước đi đúng — bạn là người **kéo mọi người vào rồi tổng hợp**:
- Hỏi **product**: "Quyết định/hành động nào đến từ cái này? Metric kinh doanh là gì?"
- Hỏi **DA**: "Ta có data gì, phân phối trông thế nào?"
- Bạn đóng góp: thiết kế hệ thống/pipeline, tính khả thi, luồng dữ liệu.
- **Tổng hợp**: gom các luồng lại, đề xuất plan, mời phản biện.
- Giải thích bằng lời dễ hiểu, không thuật ngữ hóa. Nền DE dùng để **dẫn dắt nhẹ**, không phải để áp đảo.

### 1.5 Present — cấu trúc 3 nhịp
1. **Vấn đề + giả định** — tóm tắt bài toán và các giả định đã nêu.
2. **Giải pháp** — vẽ flow, đi từ nguồn data đến output.
3. **Đánh đổi + bước tiếp theo** — batch vs streaming, cái gì làm trước, rủi ro gì.
Ngắn, rõ, có cấu trúc là đủ ăn điểm.

### 1.6 CASE MẪU CÓ LỜI GIẢI — học thuộc mạch này
**Đề:** "Thiết kế hệ thống cảnh báo khách có nguy cơ trễ kỳ thanh toán tới."

**Bước 1 — Hỏi (chạy khung 5 câu):**
- Metric: giảm tỷ lệ trễ hạn; đo bằng precision/recall của cảnh báo. Hành động sau cảnh báo: collections gọi/nhắn nhắc.
- Người dùng: team collections, dùng danh sách khách rủi ro mỗi sáng.
- Data: lịch sử thanh toán, thông tin khoản vay, giao dịch, (có thể) bureau.
- Ràng buộc: collections hành động theo ngày → **batch hằng ngày là đủ**, chưa cần streaming.
- Giả định (nói ra): có 12 tháng lịch sử thanh toán; scoring chạy 1 lần/ngày lúc rạng sáng.

**Bước 2 — Thiết kế (góc nhìn DE, tập trung pipeline không phải model):**
- **Nguồn:** core banking DB (thanh toán, khoản vay), luồng giao dịch, bureau (batch).
- **Ingestion:** CDC từ DB vận hành → data lake; batch load bureau.
- **Xử lý:** pipeline feature batch (Spark) tính đặc trưng hằng ngày → feature store.
- **Scoring:** model đọc feature, ghi điểm rủi ro vào serving store.
- **Serving:** dashboard collections đọc điểm; hoặc đẩy khách rủi ro cao vào queue.
- **Chất lượng & phục hồi:** chạy idempotent (chạy lại không nhân đôi), data quality checks, khả năng backfill.

**Bước 3 — Present:**
"Vấn đề là cảnh báo sớm khách sắp trễ, để collections can thiệp. Em giả định batch hằng ngày đủ vì hành động theo ngày. Luồng: CDC từ core banking → lake → feature pipeline hằng ngày → model scoring → serving store cho dashboard. Đánh đổi chính là batch vs streaming — batch đơn giản và đủ nếu can thiệp theo ngày; chỉ cần streaming nếu muốn chặn ngay trong ngày. Bước tiếp: chốt feature với DA, chốt ngưỡng cảnh báo với product."

---

## PHẦN 2 — Technical concepts (guide công ty đưa)

> "Whiteboard hoặc chỉ ý tưởng/flow" = họ muốn nghe bạn **nghĩ**, không đòi code chạy. Vừa vẽ vừa nói to.

### 2.1 Data literacy
- **Đọc bảng nhỏ tìm pattern:** xu hướng (tăng/giảm), ngoại lệ (outlier), tương quan giữa cột.
- **Sanity-check số & đơn vị TRƯỚC khi tin:** ngưỡng có hợp lý vật lý không? VD "latency 5000" — ms hay giây? "amount 50" — đơn vị tiền nào? Con số vô lý = nghi ngờ data.
- **Nêu giả định thành lời khi suy luận từ cột thô** — đây là dòng in đậm trong guide, họ sẽ để ý.

### 2.2 Streaming pipeline — shape
`Source → Ingestion → Message Broker → Stream Processor → Sink`
- **Source:** app, giao dịch, IoT, CDC từ DB.
- **Message broker:** đệm & phân phối event, tách producer khỏi consumer.
- **Stream processor:** biến đổi/tổng hợp/làm giàu event, giữ state.
- **Sink / serving store:** nơi ghi kết quả để phục vụ đọc nhanh, hoặc lake/warehouse để phân tích.

### 2.3 Open-source landscape (thuộc vài tên mỗi nhóm)
- **Message brokers:** **Kafka** (mặc định — log phân vùng, replay bằng offset), Pulsar, RabbitMQ (queue truyền thống), Kinesis / Pub/Sub (cloud).
- **Stream processors:** **Flink** (true streaming, event-time, stateful, exactly-once), **Spark Structured Streaming** (micro-batch), Kafka Streams (thư viện), ksqlDB.
- **Online serving stores:** **Redis** (in-memory, nhanh nhất), Cassandra, DynamoDB, ScyllaDB — đọc key-value độ trễ thấp để serving.

### 2.4 Latency vs Throughput vs Concurrency (đừng lẫn)
- **Latency:** thời gian xử lý **một** bản ghi. Đơn vị ms.
- **Throughput:** số bản ghi xử lý **trên giây**. records/sec.
- **Concurrency:** số việc chạy **song song** cùng lúc.
- **Đánh đổi:** gom batch → tăng throughput nhưng **tăng** latency. Tăng concurrency → có thể tăng throughput nhưng thêm chi phí phối hợp.

### 2.5 Delivery semantics (đảm bảo giao nhận)
- **At-most-once:** có thể mất, không bao giờ trùng.
- **At-least-once:** không mất, có thể trùng → **cần idempotency** để khử trùng.
- **Exactly-once:** không mất, không trùng — đạt bằng **checkpointing + transactional sink** (VD Flink + Kafka transactions). Đắt nhất.

### 2.6 Failure / recovery (guide để riêng = chắc chắn hỏi)
- **Checkpointing:** định kỳ snapshot state + offset. Lỗi thì khởi động lại từ checkpoint gần nhất, không mất dữ liệu.
- **Replay:** Kafka giữ message; consumer đọc lại từ một offset khi cần xử lý lại.
- **Dead-letter queue (DLQ):** message lỗi lặp lại → đẩy sang queue phụ để xem sau, thay vì chặn cả pipeline.
- **Idempotency (từ khóa vàng):** xử lý cùng một message hai lần cho **cùng kết quả** (VD upsert theo key, dedup theo id). Cho phép retry an toàn.
- **Backpressure:** consumer chậm hơn producer → hệ thống báo ngược lên để giảm tốc, tránh sập.
- **Watermark:** xử lý event đến trễ / không đúng thứ tự trong event-time.

### 2.7 Bonus — khái niệm DE nền hay bị hỏi
- **Batch vs streaming:** batch = xử lý theo lô định kỳ (đơn giản, rẻ, độ trễ cao); streaming = xử lý liên tục (phức tạp, cho realtime). Chọn theo **hành động có cần realtime không**.
- **Data lake vs warehouse vs lakehouse:** lake = raw đủ loại (rẻ, linh hoạt); warehouse = có cấu trúc cho analytics (nhanh query); lakehouse = kết hợp cả hai.
- **Parquet vs CSV:** Parquet = cột, nén tốt, đọc nhanh cho analytics; CSV = hàng, đơn giản nhưng chậm & cồng kềnh.
- **ETL vs ELT:** ETL biến đổi trước khi load; ELT load thô rồi biến đổi trong warehouse (phổ biến hơn với lakehouse).
- **Idempotent pipeline:** chạy lại không nhân đôi dữ liệu — nền của recovery.

---

## PHẦN 3 — Neo vào project của bạn
Feature Store Lichess (batch/stream lakehouse) là material thật để nói. Khi được hỏi kinh nghiệm streaming/pipeline, kể từ đó: nguồn → ingestion → xử lý batch+stream → feature store → serving. Nói từ đồ mình đã làm luôn thuyết phục hơn lý thuyết.

---

## PHẦN 4 — Checklist tối 5/8
- [ ] Đọc lại Phần 0 cheat sheet đến mức đọc thuộc khung 5 câu hỏi
- [ ] Vẽ lại được sơ đồ streaming từ trí nhớ
- [ ] Nói trôi được case mẫu (Phần 1.6) như kể chuyện
- [ ] Nhớ 3 từ khóa: idempotency, checkpointing, state assumptions
- [ ] **Ngủ trước 12h** — sáng 6/8 tỉnh táo quan trọng hơn 1 giờ ôn thêm
