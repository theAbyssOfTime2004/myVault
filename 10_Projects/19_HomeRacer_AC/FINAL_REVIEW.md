---
tags: [project, job-hunt, interview, data-engineer, home-credit, final]
status: active
created: 2026-08-05
event: AC 2026-08-06, 9:30 — Home Credit VN, 20 Nguyễn Đăng Giai, Thủ Đức
---

# TỔNG DUYỆT — AC 6/8

> Đây là file duy nhất cần mở sáng mai. Mọi thứ khác là tài liệu tham chiếu.

---

## 0. NGÀY MAI

- **9:30 check-in** (đến trễ có thể không được vào) · 20 Nguyễn Đăng Giai, Thủ Đức · **đi sớm, giờ cao điểm**
- **Smart casual** · **laptop sạc đầy + sạc** · số Mr. Khang **0938.368.316**
- 10:00-10:30 chia nhóm · **10:30-11:30 thảo luận** · **11:30-11:40 present** · 11:40-11:50 Q&A · 11:50 kết thúc
- Nhóm **6 người**, bị quan sát suốt · **present bằng tiếng Anh**
- **10 phút present cho 6 người = ~1.5 phút/người**

### Ba tiêu chí chấm (từ email của họ)
- **Speak up** — im lặng = không có gì để chấm. Phát biểu trong 5 phút đầu, dù chỉ là một câu hỏi
- **Be collaborative** — hỏi làm rõ, xây trên ý người khác, giúp nhóm tiến lên
- **Stay calm under time pressure** — không cần đáp án hoàn hảo, cần thấy cách tiếp cận

### Nước đi mở màn (nói trong 2 phút đầu)
> "We have 60 minutes and only 10 to present for six people. Should we plan the time — 10 minutes to understand the problem, 10 for ideas, 25 to design, and keep the last 15 to assemble the presentation?"

- **Bẫy chết người:** bàn 55 phút rồi hoảng 5 phút cuối → present rời rạc → **cả nhóm cùng mất điểm**
- Vai **timekeeper/synthesizer** = dễ nổi bật nhất, ít ai giành nhất

### Nếu nhóm nhiều role (product, DA...)
- Bạn là người **duy nhất** hiểu hệ thống → lợi thế mặc định
- Vai: **phiên dịch + tổng hợp**. Hỏi product về mục tiêu, hỏi DA về data, bạn lo luồng dữ liệu
- **Rủi ro:** đè người khác bằng thuật ngữ → nói bằng lời thường

### Nếu nhóm toàn DE
- Ai cũng biết Kafka → **không có lợi thế mặc định**
- **Bẫy:** đua khoe công nghệ. Không được điểm gì
- Đánh vào 4 trục bỏ trống: **hỏi câu nghiệp vụ** · **giữ giờ** · **nói vận hành/sự cố** · **nói chi phí**
- Nước đi: *"We all agree on the stack — can I ask something more basic? What does the system actually do when it flags something?"*
- **Chọn phương án đơn giản và bảo vệ nó** — chín chắn hơn mọi kiến trúc phức tạp

---

## 1. KHUNG CASE

### 5 câu hỏi làm rõ (nói ra miệng, trong 10 phút đầu)
1. **Mục tiêu & metric** — giải quyết vấn đề gì, đo thành công bằng gì
2. **Hành động phía sau** — sau khi có kết quả thì AI làm GÌ ← **câu quan trọng nhất**
3. **Người dùng** — ai dùng output, quyết định gì
4. **Dữ liệu** — có gì, chất lượng ra sao, **có nhãn không**
5. **Ràng buộc + nêu giả định** — "Em giả định X, nếu sai thì Y đổi"

### Present 3 nhịp (~1.5 phút)
1. **Vấn đề + giả định** (20s)
2. **Giải pháp** — đi theo dòng dữ liệu trái→phải, vừa vẽ vừa nói (40s)
3. **Đánh đổi + bước tiếp** (30s) ← **nhịp phân loại ứng viên**

- Nhịp 3 chứng minh bạn **đã cân nhắc phương án khác** rồi mới chọn
- Câu cuối *"align features with the DA, confirm thresholds with product"* = ghi điểm teamwork

---

## 2. DATA LITERACY

### Grain — câu hỏi số 0
- **"Một dòng đại diện cho cái gì?"** — hỏi TRƯỚC mọi thứ
- `customer_id + month` → một khách trong một tháng, **không phải** một khách
- Chưa chốt grain thì mọi phép tổng hợp phía sau đều có nguy cơ vô nghĩa

### Fan-out
- JOIN bảng 1 với bảng N → giá trị bên 1 bị **nhân bản** theo số dòng bên N
- **Không có lỗi nào báo.** Ra số trông hợp lý mà sai
- > **Số sai im lặng nguy hiểm hơn job chết ồn ào** — crash sửa trong 1 giờ, số sai vào thẳng báo cáo
- **Sửa:** gom bảng N về đúng grain trước (`GROUP BY`), rồi `LEFT JOIN` 1-1
- Dùng LEFT không INNER, kẻo mất khách chưa phát sinh giao dịch

### Đơn vị & tính hợp lý
- Timestamp: **10 chữ số = giây · 13 = mili giây · 16 = micro giây**
- Tiền: có thể lưu **đơn vị nhỏ nhất** (xu) → 100000 có thể là 1000.00
- **Không có `currency_code` → `SUM(amount)` vô nghĩa**
- `age = 1987` → là **năm sinh**, không phải tuổi
- Tỷ lệ > 100% → mẫu số sai hoặc tử số bị nhân bản (thường do fan-out)
- Số âm ở latency → clock skew hoặc trừ ngược
- NULL thường **mang nghĩa** ("không áp dụng"), không phải lỗi
- Không có NULL ≠ sạch — có thể bị mã hoá thành 0, chuỗi rỗng, ngày giả

### Nêu giả định
- Ba cách phản ứng khi thiếu thông tin: đứng im (mất điểm) · giả định ngầm (nguy hiểm nhất) · **nêu ra rồi tiến (đúng)**
- > **Giả định ngầm nguy hiểm hơn giả định sai** — không ai biết nó tồn tại nên không ai sửa được
- Luôn **định lượng tác động**: lọc mất 2% là chi tiết, mất 40% là hiểu sai đề

### Thống kê nhanh
- **Mean ≫ Median** → lệch phải → dùng **percentile**, đừng dùng mean để đặt ngưỡng
- **σ**: bình phương độ lệch → trung bình → căn bậc hai. Khoảng bình thường **μ ± 3σ** (99.7%)
- **z = (x − μ)/σ**, báo động nếu |z| > 3
- **IQR = Q3 − Q1 = P75 − P25**. Hàng rào: Q1 − 1.5·IQR, Q3 + 1.5·IQR
- Percentile chia 100 phần; tứ phân vị chỉ là Q1=P25, Q2=P50, Q3=P75
- **Lệch mạnh → percentile. Chuẩn → σ.** Tiền, latency, thu nhập đều lệch
- Đường cơ sở phải **loại ngày hiện tại ra** (`ROWS BETWEEN 7 PRECEDING AND 1 PRECEDING`)

---

## 3. STREAMING PIPELINE

```
Source → Message Broker → Stream Processor → Serving Store
```

- **Source**: app, IoT, hoặc **CDC** từ DB vận hành (đọc WAL/binlog — **không query trực tiếp**, vì DB đang phục vụ khách thật)
- **Broker**: bộ đệm + tách rời producer/consumer. Kafka = **append-only log**, giữ message theo retention → **replay được**
- **Processor**: lọc, biến đổi, tổng hợp. Stateless vs **stateful** (cần nhớ dữ liệu trước)
- **Serving store**: đọc mili giây. Tra **theo khóa**, không SQL tự do

### Kafka
- **Topic** = kênh theo chủ đề · **Partition** = topic chẻ nhỏ để chạy song song
- **Thứ tự chỉ đảm bảo TRONG một partition**, không phải toàn topic
- **Key quyết định partition** → không đặt key thì event của **cùng một thực thể bị văng ra nhiều partition** → mất thứ tự
- **Offset** = vị trí đọc trong partition · **Commit offset** = báo "đã xử lý tới đây"
- **Consumer group**: trong cùng group = **chia việc**; khác group = **ai cũng nhận đủ**
- **Trần song song = số partition**. Consumer thừa ngồi không

### Window — vì sao cần
- Stream **vô hạn** → không tính được `AVG`/`COUNT` (chờ đến bao giờ?)
- → cắt thành khúc hữu hạn. **Window trượt trên trục thời gian**
- **Tumbling** = liền nhau, không chồng lấn (báo cáo theo giờ)
- **Sliding** = chồng lấn — *size* = phủ bao lâu, *slide* = bao lâu ra kết quả một lần
- **Session** = đóng khi im lặng đủ lâu

### Event time vs Processing time
- Event time = lúc xảy ra · Processing time = lúc nhận được
- **Watermark** = "tôi tin đã nhận đủ event trước T" → đóng cửa sổ
- Tính động: `max event time đã thấy − độ trễ cho phép`
- Đánh đổi duy nhất: cho phép trễ **nhiều** = chính xác hơn nhưng chậm hơn
- > Watermark không giải quyết vấn đề — nó biến vấn đề ngầm thành **tham số bạn chọn**

---

## 4. LANDSCAPE

| Nhóm | Lựa chọn |
|---|---|
| **Broker** | **Kafka** (mặc định, replay) · Pulsar (tách compute/storage) · Redpanda (C++, không JVM) · RabbitMQ (queue, không replay) |
| **Processor** | **Flink** (true streaming, ms) · **Spark SS** (micro-batch, 100ms-1s) · **Kafka Streams** (thư viện, không cần cụm) |
| **Serving** | **Redis** (in-memory, key lookup) · Cassandra (write throughput) · ClickHouse/Pinot (OLAP realtime) |

### Điểm phân biệt
- **Kafka vs RabbitMQ**: Kafka = **event** ("đã xảy ra", replay có ích) · RabbitMQ = **command** ("làm giúp tôi", làm xong là hết)
- RabbitMQ đúng khi: task queue, cần ack từng message, có priority, **replay là có hại**, và tránh **head-of-line blocking** (Kafka: một task chậm chặn cả partition)
- **Spark micro-batch**: gom ~500ms rồi chạy batch engine. **State vẫn giữ qua các lô** — không phải job độc lập
- **Kafka Streams**: thư viện, scale bằng chạy thêm instance (mượn consumer group làm điều phối), state ở RocksDB + changelog topic. **Vẫn cần cụm Kafka** — chỉ không cần cụm *xử lý*
- Chọn Spark khi: ~1 giây là đủ, đã có sẵn Spark, muốn một API chung batch+stream

### OLTP vs OLAP
- **OLTP**: chạm **ít dòng rất nhiều lần**, lưu theo dòng, chạy nghiệp vụ (Postgres/MySQL)
- **OLAP**: chạm **rất nhiều dòng ít lần**, lưu theo cột, phân tích (BigQuery/ClickHouse)
- **Trong pipeline: OLTP ở ĐẦU (nguồn, qua CDC) · OLAP ở CUỐI (đích phân tích) · Serving store là thứ THỨ BA**
- > Pipeline tồn tại để **bắc cầu giữa OLTP và OLAP**

### Serving store — điều dễ hiểu nhầm
- **Không trả lời câu hỏi tự do.** Nó trả về **giá trị tính sẵn theo một khóa**
- Danh sách feature được **chốt từ lúc thiết kế** = **quyết định nghiệp vụ**, không phải kỹ thuật
- Câu hỏi tự do → về lake/Trino, chấp nhận chậm
- **Tính trước = đổi độ tươi lấy độ trễ.** Giá trị tính sẵn là **ảnh chụp một khoảnh khắc**
- Hỏi đúng không phải "làm sao cho nhanh" mà **"con số này cũ đi nhanh cỡ nào?"**
- Feature chậm đổi → batch · Feature nhanh đổi → stream · **cùng một store, hai nhịp**

---

## 5. LATENCY / THROUGHPUT / CONCURRENCY

- **Latency** = thời gian **một** bản ghi đi hết đường
- **Throughput** = số bản ghi **mỗi giây**
- **Concurrency** = số việc chạy **song song**
- **Gom lô → throughput TĂNG, latency TĂNG** (bản ghi đầu phải chờ đủ lô)
- Concurrency bên trong lô **không cứu được latency** — sàn latency do **thời gian chờ đầy lô** quyết định
- **Tăng concurrency → tăng throughput, KHÔNG giảm latency một request**
- **Đo bằng P95/P99, không dùng trung bình** — trung bình che phần đuôi

### Câu quyết định batch hay streaming
> **"Sau khi có kết quả thì AI làm GÌ, và việc đó phải xảy ra nhanh cỡ nào?"**

- **Cửa sổ hành động** quyết định latency budget, không phải kỹ thuật
- Kịp cửa sổ → **NGĂN CHẶN** · Trễ → **chỉ PHÁT HIỆN** (cùng con số, giá trị thấp hơn hẳn)
- Collections gọi điện hôm sau → cửa sổ hàng giờ → **batch thừa đủ**
- Chặn giao dịch tại quầy → cửa sổ ~200ms-2s → **buộc streaming**

---

## 6. FAILURE / RECOVERY

### Delivery semantics — do THỨ TỰ quyết định
```
commit trước, xử lý sau  →  at-most-once   →  có thể MẤT
xử lý trước, commit sau  →  at-least-once  →  có thể TRÙNG   ← mặc định thực tế
gộp cả hai thành một khối →  exactly-once  →  đắt
```
- **Exactly-once KHÔNG có nghĩa xử lý một lần** — vẫn xử lý lại, chỉ là **kết quả cuối như thể một lần**
- Cần đủ **ba mảnh**: nguồn tua lại được + checkpoint + đầu ra không nhân đôi

### Idempotent vs Transactional — giải HAI bài toán khác nhau
- **Idempotent** trả lời: *"nếu ghi hai lần thì sao?"* → rẻ, không phạt độ trễ → **luôn thử cái này trước**
- **Transactional** trả lời: *"nếu chỉ MỘT NỬA số phép ghi xảy ra thì sao?"* → **atomicity**, đây mới là lý do thật
- Chuyển tiền cần transaction vì **trừ A + cộng B phải cùng xảy ra**, không phải vì chống trùng
- Ghi sổ cái **vẫn idempotent được** nếu có `txn_id` làm khóa (`ON CONFLICT DO NOTHING`)

```
SET balance = 500            → ghi 10 lần vẫn 500      ✅ ghi đè = idempotent
SET balance = balance + 100  → ghi 10 lần thành +1000  ❌ cộng dồn = không
```
- **Upsert không tự cứu bạn — cái quyết định là bạn SET gì**
- `ON CONFLICT (col)` **chỉ chạy nếu cột đó có UNIQUE/PRIMARY KEY**

### Checkpoint
- **Chụp state + offset**, lưu ra storage bền vững (S3/MinIO). **Thiếu offset là vô nghĩa**
- Chụp bằng **barrier trôi theo dòng dữ liệu** → ảnh nhất quán **mà không dừng job**
- Khôi phục = nạp ảnh chụp + đặt lại offset → **xử lý lại phần từ checkpoint tới lúc crash**
- > **Checkpoint bảo vệ trí nhớ của job. KHÔNG bảo vệ những gì job đã làm ra bên ngoài**
- DB không biết có crash — dòng đã commit vẫn nằm đó. Flink tua ngược được chính nó, **không tua ngược được thế giới**
- → sink phải **idempotent hoặc transactional**
- Side-effect không đảo ngược được (gửi SMS, gọi API) → cần **idempotency key** riêng

### Poison pill & DLQ
- Message lỗi → consumer chết → restart → đọc lại đúng nó → chết tiếp → **vòng lặp vô tận**
- **Nguy hiểm không phải mất một bản ghi — mà là KẸT CẢ LUỒNG.** Hàng triệu message phía sau không bao giờ được xử lý
- **DLQ**: bắt lỗi → đẩy message + metadata sang topic riêng → **commit offset** → luồng chính chạy tiếp
- **Cảnh báo theo độ sâu DLQ** — không có nó thì chỉ là đổi chỗ sự im lặng
- **Lỗi tạm thời** (mạng) → retry có backoff · **Lỗi vĩnh viễn** (JSON hỏng) → DLQ ngay
- > Retry lỗi vĩnh viễn **chính là cách tạo ra** vòng lặp đó

---

## 7. GOVERNANCE (điểm cộng ở công ty tài chính)

- **Data contract** — thoả thuận schema + ngữ nghĩa + SLA + chính sách đổi. Giải nguyên nhân số 1 gây gãy pipeline: **nguồn đổi mà không báo**. Thực thi bằng schema registry
- **Lineage** — dữ liệu từ đâu, qua gì, tới đâu. **Ngược lên** để debug, **xuôi xuống** để biết đổi cột này thì ai gãy. **Bắt buộc cho audit**
- **Data quality** — assertion cố định (null, unique, range) bắt lỗi **đã nghĩ tới**; giám sát thống kê bắt lỗi **chưa nghĩ tới**
- **PII / RBAC / masking / retention / audit trail** — retention mâu thuẫn cố hữu: audit đòi giữ, quyền riêng tư đòi xoá
- **Explainability** — quyết định tín dụng phải **giải thích được vì sao từ chối**. Ràng buộc luôn việc chọn model

---

## 8. PROJECT CỦA BẠN

### Batch
`dump .pgn.zst (30GB) → MinIO bronze (thô, bất biến) → shred → Spark parse → Delta silver (1 dòng/ván) → Spark aggregate → gold features → point-in-time training set → IsolationForest → materialize → Redis`

### Stream
`Lichess TV (NDJSON) → collector → Kafka (key=game_id) → Flink (ValueState clock → sliding 30s/10s → Welford) → Redis (TTL 1h) → FastAPI`

**Hai đường gặp nhau ở Redis** = online store. Delta trên MinIO = offline store.

### Bốn câu chuyện — thả MỘT câu đúng lúc
- **Shred** (nói về scale): zstd không splittable → 1 task → **62-75h**. Cắt theo ranh giới ván → song song → **4 phút**. *"Same infrastructure — I just made the data divisible."*
- **Partition overwrite** (nói về idempotency): `mode("overwrite")` mặc định **wipe cả bảng**, xoá mất tháng khác → `partitionOverwriteMode=dynamic`
- **Dev month không có eval** (nói về data quality): tháng 2013-01 không có annotation → logic ACPL **chưa từng chạy thật** → đo coverage lại + viết unit test
- **Flink prune** (khi bị hỏi "bug khó nhất"): map ghi Redis không có sink phía sau → optimizer **cắt khỏi execution graph** → job RUNNING, không lỗi, **không ghi gì**. *"The most dangerous bug isn't the one that crashes — it's the one that runs fine and does nothing."*

### Point-in-time correctness (rất liên quan tín dụng)
- `rowsBetween(unboundedPreceding, -1)` — số **−1** loại ván hiện tại ra → chống **data leakage**
- Nối sang: *"feature của khách tại thời điểm duyệt vay chỉ được dùng thông tin có tại lúc đó"*

### Ranh giới trung thực — KHÔNG overclaim
| Đừng nói | Nói |
|---|---|
| "Đã chạy 120GB" | "Verified on a real month with eval/clock; the full-scale run is the last step" |
| "Chạy 24/7" | "Ephemeral cluster — spun up for dev and demo, torn down after" |
| "Production-grade streaming" | "Deliberately simplified: no checkpointing, no state TTL, parallelism 1" |
| "Có CI/CD đầy đủ" | "CI/CD and scheduled DAGs are still TODO" |

> Trung thực về giới hạn **làm tăng** độ tin cậy. Một câu nói quá khiến họ nghi ngờ **mọi** câu còn lại.

---

## 9. CÂU TIẾNG ANH DÙNG NGAY

**Hỏi làm rõ**
- "What problem are we solving, and how would we measure success?"
- "What happens after the system produces an output — who acts on it?"
- "Does this need to be real-time, or is a daily batch enough?"
- "Let me state an assumption: I'm assuming X. If that's wrong, Y changes."

**Teamwork**
- "Building on what X just said..."
- "That's a good point. My only concern is..."
- "So to summarise where we are: we've agreed on X, we're still deciding Y."
- "Should we pick one and move on?"

**Đọc bảng số**
- "What does one row represent here?"
- "What unit is this column in — milliseconds or seconds?"
- "That doesn't look physically plausible — is this age or year of birth?"

**Không biết**
- "I haven't worked with that specifically, but my thinking would be..."
- "That's a good question — I'd want to check that rather than guess."

**Present**
- "The main trade-off was batch versus streaming. Batch is simpler and enough if the action happens daily — and this design upgrades to streaming without a rebuild."
- "Next steps: align on feature definitions with the analyst, confirm thresholds with product."

---

## 10. MƯỜI CÂU MANG VÀO PHÒNG

1. **Hỏi trước khi giải.** Câu đầu tiên nói ra là một câu hỏi, không phải một giải pháp
2. **"Một dòng đại diện cho cái gì?"** — câu số 0 với mọi bảng
3. **Số sai im lặng nguy hiểm hơn crash ồn ào**
4. **Đơn vị trước, kết luận sau**
5. **Giả định ngầm nguy hiểm hơn giả định sai** — nêu ra rồi tiến
6. **Hành động phía sau quyết định batch hay streaming** — không phải công nghệ nghe hay
7. **Gom lô: throughput tăng, latency tăng.** Concurrency tăng throughput, không giảm latency một request
8. **Ghi đè thì idempotent, cộng dồn thì không** — đây là ranh giới quyết định chiến lược khôi phục
9. **Checkpoint không đủ — sink phải hợp tác**
10. **Một bản ghi hỏng không được giết cả pipeline** → DLQ

---

## Sáng mai

- Chỉ đọc: **mục 0** (nước đi mở màn) + **mục 1** (5 câu hỏi) + **mục 10**
- **Không nạp thêm gì mới**
- Nói **chậm, rõ, tự tin**. Tiếng Anh của bạn tốt hơn mặt bằng phòng đó
- Assessor không chấm bạn **so với** nhóm — họ chấm **bạn làm nhóm tốt lên bao nhiêu**
