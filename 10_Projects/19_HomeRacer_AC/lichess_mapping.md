---
tags: [project, job-hunt, interview, data-engineer, home-credit, lichess]
status: active
created: 2026-07-31
related: "[[prep]] · [[de_concepts]] · [[case_rationale]]"
source: "[[18_DE_FeatureStore/end_to_end_walkthrough]]"
---

# Ánh xạ guide AC ↔ Lichess Feature Store

> Mục đích: mỗi bullet trong prep guide của Home Credit → **thứ bạn đã thực sự xây** → **câu nói ra được**.
> Nguyên tắc xuyên suốt: nói đúng những gì đã làm, nêu rõ chỗ đã cố tình đơn giản hoá. **Không overclaim** — xem Phần 5.

---

## PHẦN 0 — Bản 60 giây nối cả 4 bullet

> "Em có làm một feature store trên dữ liệu cờ vua Lichess, có cả đường batch và đường streaming. Đường stream đúng hình dạng chuẩn: Lichess TV feed → collector → **Kafka** → **Flink** windowed aggregation → **Redis** làm online store, FastAPI đọc Redis trả feature. Đường batch thì Spark parse PGN → Delta lakehouse trên MinIO theo medallion, rồi materialize sang Redis.
>
> Chỗ em học được nhiều nhất là về **latency và throughput**: file dump nén zstd không splittable nên một tháng dữ liệu mất 60-75 tiếng vì Spark chỉ chạy được 1 task; em thêm bước shred cắt file theo ranh giới ván thành nhiều shard để chạy song song, xuống còn khoảng 4 phút. Còn về **recovery**, job Flink của em cố tình đơn giản hoá — processing-time không watermark, chấp nhận at-most-once vì ghi Redis là overwrite có TTL — nhưng em biết rõ lên production thì phải thêm checkpointing và state TTL."

Đoạn này chạm cả 4 bullet: shape ✅ · landscape ✅ · latency/throughput ✅ · failure/recovery ✅.

---

## PHẦN 1 — "General shape of a streaming pipeline"

### Sơ đồ chuẩn ↔ project của bạn

| Tầng chuẩn | Trong Lichess FS | Chi tiết thật |
|---|---|---|
| **Source** | Lichess TV feed (NDJSON) | `GET /api/tv/feed`, long-lived stream, event `featured` (ván mới) + `fen` (mỗi nước, kèm clock `wc`/`bc`) |
| **Ingestion / collector** | `stream/collector/collect_tv.py` | `requests(stream=True)`, theo dõi `current_game_id`, có **reconnect** khi stream đóng |
| **Message broker** | **Kafka** (Strimzi trên GKE) | topic `lichess.tv.moves`, **key = game_id** (đảm bảo cùng ván vào cùng partition → giữ thứ tự) |
| **Stream processor** | **Flink** (PyFlink DataStream) | `flink/jobs/tv_movetime.py` — keyed state + sliding window |
| **Online serving store** | **Redis** | `online:movetime:<game_id>` (hash: count/avg/stddev/updated_ts), **TTL 3600s** |
| **Consumer** | FastAPI Feature API | `GET /features/movetime/{game_id}` |

**Vẽ lên whiteboard đúng thế này:**
```
Lichess TV (NDJSON) → collector → Kafka (lichess.tv.moves, key=game_id)
                                     → Flink (keyed state → sliding window 30s/10s)
                                     → Redis (online:movetime:*, TTL 1h)
                                     → FastAPI /features/movetime
```

**Chi tiết đắt giá — logic bên trong Flink** (nói được là rất mạnh):
1. `flat_map` parse message → `(game_id, lm, wc, bc, event_ts)`
2. `key_by(game_id)` → `KeyedProcessFunction` giữ **ValueState** `last_wc`/`last_bc` → suy ra thời gian mỗi nước từ **độ tụt của đồng hồ** (bên nào clock giảm thì bên đó vừa đi)
3. `key_by(game_id)` → **SlidingProcessingTimeWindows(30s, slide 10s)** → aggregate bằng **thuật toán Welford** (tính mean/variance online, một pass, không giữ toàn bộ mẫu)
4. Ghi Redis + TTL

→ Điểm nghiệp vụ: `stddev` move-time quá thấp = nhịp đánh đều như máy = tín hiệu gian lận, **không cần chạy engine cờ**.

**Vì sao dùng key_by game_id:** cùng một ván luôn về cùng partition/task → state đúng và thứ tự trong ván được giữ. Đây là câu trả lời chuẩn cho "làm sao đảm bảo thứ tự trong stream".

---

## PHẦN 2 — "Open-source landscape awareness"

### 2.1 Message brokers → bạn dùng Kafka

| Nói gì | Nội dung |
|---|---|
| Đã dùng | **Kafka**, deploy bằng **Strimzi operator** trên GKE |
| Vì sao Kafka | Retention + replay theo offset; nhiều consumer đọc cùng nguồn; tách producer/consumer để hai bên chạy khác tốc độ |
| Biết cái khác | RabbitMQ (queue truyền thống — message tiêu thụ xong là mất, không replay được), Pulsar, Kinesis/Pub-Sub (managed trên cloud) |
| Chi tiết thật | `key=game_id` để phân vùng theo ván; consumer đọc từ `offsets.latest()` |

### 2.2 Stream processors → bạn dùng Flink

| Nói gì | Nội dung |
|---|---|
| Đã dùng | **Flink** (PyFlink DataStream API), qua **Flink K8s Operator 1.10.0** + cert-manager |
| Vì sao Flink | True streaming — xử lý từng event, có keyed state, windowing gốc |
| Đối chiếu | **Spark Structured Streaming** là micro-batch (bạn dùng Spark cho **batch** trong cùng project → nói được sự khác biệt từ trải nghiệm thật); Kafka Streams là thư viện nhúng, không cần cụm riêng |
| Trung thực | `parallelism=1` — chưa kiểm chứng scale ngang |

### 2.3 Online serving stores → bạn dùng Redis

| Nói gì | Nội dung |
|---|---|
| Đã dùng | **Redis** làm online store |
| Vì sao cần | Delta trên MinIO query mất **vài giây** — quá chậm cho API. Redis in-memory trả về **mili giây** |
| Kiến trúc 2 tầng | **Offline store** = Delta trên MinIO (đầy đủ, chậm, để train) · **Online store** = Redis (nhanh, để serving). Cùng feature, hai nơi, hai mục đích |
| Keys thật | `offline:player:<player>:<speed>` · `online:cheat:<player>:<speed>` · `online:movetime:<game_id>` |
| Biết cái khác | Cassandra, DynamoDB, ScyllaDB — cùng nhóm key-value low-latency |

### 2.4 Phần còn lại của stack (nếu được hỏi rộng)

| Nhóm | Bạn dùng |
|---|---|
| Object storage | **MinIO** (S3-compatible) |
| Table format | **Delta Lake** (ACID, versioning, dynamic partition overwrite) |
| Batch engine | **Spark 3.5.2** (Spark Operator trên GKE) |
| Query engine | **Trino** + Hive Metastore — query, DQ check, và **transform bằng SQL** (CTAS ra bảng Delta mới) |
| Orchestration | **Airflow 2.10.5**, KubernetesExecutor (mỗi task = 1 pod) |
| Infra | GKE + **Terraform**, Prometheus + Grafana |

---

## PHẦN 3 — "Latency vs Throughput vs Concurrency"

> Đây là bullet bạn có **câu chuyện mạnh nhất**, vì có số liệu thật.

### 3.1 Throughput & Concurrency — câu chuyện shred (kể được thành chuyện)

**Vấn đề:** file dump `.pgn.zst` **không splittable** — Spark không chia được một file nén zstd cho nhiều máy. Một file = **một task** = một máy đọc tuần tự → **~62-75 tiếng** cho một tháng dữ liệu.

**Chẩn đoán:** đây là bài toán **concurrency**, không phải bài toán máy yếu. Thêm máy vô ích khi chỉ có 1 task.

**Giải pháp — bước shred:** đọc file một lần, **chỉ giải nén** (không parse — nên rất nhanh), cắt theo **ranh giới ván** (mỗi ván mới bắt đầu bằng `[Event ...]`), gom ~30.000 ván thành một shard `.pgn.gz`.

**Kết quả:** N shard → N task chạy song song → **~75 phút xuống ~4 phút**.

**Câu chốt ăn điểm:** *"Đây là ví dụ rõ nhất về concurrency quyết định throughput: hạ tầng không đổi, chỉ tăng số đơn vị song song bằng cách làm dữ liệu chia được."*

### 3.2 Latency — câu chuyện materialize sang Redis

- Delta trên MinIO: đầy đủ nhưng query mất **vài giây** → không dùng được cho API cần trả lời tức thì.
- Giải pháp: job **materialize** copy feature từ Gold Delta → Redis hash.
- Kết quả: lookup xuống **mili giây**.

**Đánh đổi thật sự nằm ở đâu — nói cho chính xác:**

Redis giữ một **bản sao đã tính sẵn**, không phải khung nhìn sống. Delta là nguồn sự thật; Redis là **ảnh chụp** tại thời điểm materialize, và nó **không tự cập nhật** khi nguồn đổi.

| Cách làm | Độ trễ | Độ tươi |
|---|---|---|
| Tính lúc được hỏi (query thẳng Delta) | vài giây | luôn bằng nguồn |
| Tính trước rồi cất (materialize → Redis) | mili giây | bằng lần tính lại gần nhất |

→ **Nguyên nhân gây cũ là việc TÍNH TRƯỚC, không phải Redis.** Đổi Redis sang Cassandra cũng không khác. Nguyên tắc: *bất kỳ giá trị nào được tính trước đều là ảnh chụp của một khoảnh khắc — độ tươi bị chặn bởi tần suất tính lại.*

**Lưu ý về chính project này:** materialize là bước cuối của DAG batch, nên Redis **không cũ hơn Delta Gold** một cách đáng kể — cả hai cùng tươi bằng lần chạy pipeline gần nhất. Muốn tươi hơn thì phải chạy **cả pipeline** dày hơn, chứ không phải chỉ materialize dày hơn.

### 3.2b Vì sao hai đường cùng ghi vào Redis — nhịp làm tươi theo loại feature

| Key | Nguồn | Nhịp làm tươi | Vì sao đủ / vì sao cần |
|---|---|---|---|
| `offline:player:*` · `online:cheat:*` | Batch | theo lần chạy pipeline (ngày) | Hồ sơ tổng thể người chơi không đổi trong vài giờ |
| `online:movetime:*` | Stream (Flink) | mỗi 10 giây | Ván cờ chỉ kéo dài vài phút — dữ liệu cũ 1 ngày là vô nghĩa |

→ Cùng một online store, **hai nhịp làm tươi khác nhau tùy feature đó hỏng đi nhanh cỡ nào**. Đây chính là lý do kiến trúc lai batch + stream tồn tại.

**Câu nối sang Home Credit:** *"Feature lịch sử như số lần trễ hạn 6 tháng qua thì batch hằng ngày là đủ. Nhưng feature kiểu 'khách vừa quẹt thẻ 5 lần trong 10 phút' thì phải qua stream. Hai loại cùng ghi vào online store, model đọc cả hai lúc chấm điểm."*

### 3.3 Latency trong stream — đánh đổi của cửa sổ trượt

`SlidingProcessingTimeWindows(size=30s, slide=10s)`:
- **Slide 10s** → kết quả cập nhật mỗi 10 giây ⇒ đây chính là **độ trễ** của feature.
- **Size 30s** → mỗi kết quả thống kê trên 30 giây dữ liệu ⇒ cửa sổ lớn thì số liệu **mượt hơn nhưng cũ hơn**.
- Nói được: *"Chọn 30s/10s là cân giữa độ mượt của thống kê và độ tươi của tín hiệu."*

### 3.4 Bảng tóm ba khái niệm bằng chính project

| Khái niệm | Trong project | Con số |
|---|---|---|
| **Latency** | Thời gian trả một lượt tra feature | Delta ~vài giây → Redis ~ms |
| **Throughput** | Lượng ván parse được mỗi đơn vị thời gian | 1 tháng: 75 phút → 4 phút |
| **Concurrency** | Số task Spark chạy song song | 1 task (1 file) → N task (N shard) |

→ Và mối quan hệ: **tăng concurrency làm tăng throughput, nhưng không giảm latency của một request đơn lẻ** — đó là lý do vẫn cần Redis cho serving.

---

## PHẦN 4 — "Failure / recovery handling"

> Phần này bạn có lợi thế đặc biệt: **biết rõ mình đã né cái gì và vì sao**. Đó là câu trả lời trưởng thành hơn nhiều so với liệt kê lý thuyết.

### 4.1 Những cơ chế bạn ĐÃ có

| Cơ chế | Trong project | Ý nghĩa |
|---|---|---|
| **Idempotent ingest** | `mc stat` trước khi tải, đã có thì skip | Chạy lại DAG không tải lại 30GB |
| **Idempotent write** | `partitionOverwriteMode=dynamic` | Ghi lại tháng đang chạy, **không xoá tháng khác** (chính là bug B8 đã sửa) |
| **Bronze bất biến** | Lưu `.zst` gốc, không parse, không sửa | Logic parse sai vẫn **replay/backfill** được, khỏi tải lại từ nguồn |
| **Cô lập bản ghi lỗi** | `parse_games`: mỗi ván bọc `try/except: continue` | Một ván hỏng (đuôi zstd bị cắt) không giết cả job — tư duy giống **DLQ** ở mức nhẹ |
| **Reconnect** | Collector tự kết nối lại khi TV feed đóng | Nguồn long-lived chắc chắn sẽ rớt |
| **TTL** | Redis `expire 3600s` cho `online:movetime:*` | Ván cũ tự dọn, không phình bộ nhớ |
| **Unit test cho code path quan trọng** | `tests/test_pgn_parse.py` | Vì dev month không có eval/clock nên logic ACPL chưa từng chạy thật → test riêng |
| **Retry / monitoring** | Airflow (KubernetesExecutor) + Prometheus/Grafana | Điều phối có retry, có quan sát |

### 4.2 Những cái bạn CỐ TÌNH né — và lý do (đây là phần ăn điểm)

| Bài toán | Xử lý | Lý do né được |
|---|---|---|
| **Watermark / late data** | `no_watermarks()` + **processing-time** window | Use case là thống kê nhịp đánh trong ván đang diễn ra, không cần chính xác theo event-time |
| **Exactly-once** | Chấp nhận **at-most-once** (`offsets.latest()`, Redis sink không transactional) | Ghi Redis là **hset overwrite + TTL** → mất vài lần cập nhật lúc restart không ảnh hưởng kết quả |
| **Checkpointing** | Chưa làm (`NO checkpointing yet`) | Trade-off có ý thức trong phạm vi project học tập |

### 4.3 Những lỗ hổng bạn TỰ NHẬN — nói ra trước khi bị hỏi

- **Flink state phình vô hạn**: keyed theo `game_id` nhưng **không có state TTL/cleanup** cho ván đã kết thúc. Redis có TTL, nhưng *Flink state* thì không → chạy lâu sẽ tích tụ.
- **Không checkpoint = không recovery**: Flink restart là **mất sạch state**.
- **parallelism = 1**: chưa kiểm chứng scale ngang.

### 4.4 CÂU TRẢ LỜI CHUẨN — học thuộc mạch này

> "Job Flink của em cố tình đơn giản hoá theo use case: dùng **processing-time, không watermark** để né phần phức tạp của event-time; chấp nhận **at-most-once** vì sink là Redis overwrite có TTL nên mất vài cập nhật lúc restart không ảnh hưởng; và hoãn checkpointing.
>
> Lên production thì em sẽ thêm ba thứ: **state TTL** để state không phình theo số ván, **checkpoint xuống MinIO** để recovery được sau sự cố, và cân nhắc **exactly-once sink** nếu nghiệp vụ đòi con số chính xác tuyệt đối."

→ Cấu trúc: *đã né gì → vì sao né được → production cần thêm gì*. Đây là cách trả lời của người hiểu hệ thống, không phải người học thuộc.

### 4.5 Ba câu chuyện sự cố kể được (nếu được hỏi "gặp bug khó nhất là gì")

**1. Bug Flink prune — hay nhất, kể cái này.**
`RedisMovetimeWriter` là một `MapFunction` không có downstream sink → **optimizer của Flink cắt bỏ nó khỏi execution graph** → job báo RUNNING, không lỗi gì, nhưng **không có gì được ghi vào Redis**. Fix: thêm terminal sink `.print()` để giữ nó trong graph.
→ Bài học: *loại lỗi nguy hiểm nhất không phải lỗi làm sập hệ thống, mà là lỗi "chạy bình thường nhưng không có tác dụng"* — không có exception nào để mà bắt.

**2. Dev data không kích hoạt code path quan trọng.**
Dùng tháng `2013-01` để dev vì nhỏ, nhưng tháng đó hầu như không có `%eval`/`%clk` → **toàn bộ logic ACPL và move-time chưa từng chạy thật**. Fix: chạy lại trên `2024-12` để đo coverage thật + viết unit test với PGN tự chế có giá trị biết trước.
→ Bài học: *dev data ≠ production data; nếu dev data không chạm tới code path quan trọng thì phải test riêng code path đó.*

**3. Ghi đè xoá mất dữ liệu tháng khác.**
`mode("overwrite")` mặc định của Spark wipe **toàn bộ** bảng, không chỉ partition đang ghi. Fix: `partitionOverwriteMode=dynamic`.
→ Bài học: *idempotency phải được thiết kế, không tự có* — và mặc định của công cụ thường không phải cái mình tưởng.

---

## PHẦN 5 — Ranh giới trung thực (đọc kỹ trước khi vào phòng)

Repo doc của chính bạn đã cảnh báo, giữ đúng kỷ luật này:

| ĐỪNG nói | NÓI thế này |
|---|---|
| "Em đã chạy 120GB" | "Kiến trúc và pipeline đã verify trên một tháng thật có eval/clock; **lần chạy full-scale là bước cuối**, em đã thiết kế shred + spot autoscale để gánh" |
| "Hệ thống chạy 24/7" | "Cluster là **ephemeral** — bật lúc dev và demo rồi tear down, để giữ trong $300 free credit" |
| "Streaming production-grade" | "Stream path chạy được end-to-end, nhưng **cố tình đơn giản hoá**: chưa checkpoint, chưa state TTL, parallelism 1" |
| "Có CI/CD đầy đủ" | "CI/CD và DAG chạy theo lịch thật vẫn còn **TODO**, hiện trigger thủ công" |

→ Trung thực về giới hạn **làm tăng** độ tin cậy, không giảm. Người phỏng vấn có kinh nghiệm nhận ra ngay ai đang thổi phồng — và một câu nói quá sẽ khiến họ nghi ngờ mọi câu còn lại.

---

## PHẦN 6 — Câu hỏi đào sâu có thể gặp & hướng trả lời

**"Vì sao chọn Flink mà không dùng Spark Streaming?"**
→ Cần true streaming từng event và keyed state theo ván; Spark Structured Streaming là micro-batch. Trong cùng project em vẫn dùng Spark cho batch, nên chọn theo đúng việc chứ không theo thói quen.

**"Làm sao đảm bảo thứ tự event trong một ván?"**
→ `key=game_id` khi produce vào Kafka → cùng ván vào cùng partition (Kafka chỉ đảm bảo thứ tự **trong** partition), rồi `key_by(game_id)` bên Flink để state và window đúng theo từng ván.

**"Nếu Flink chết giữa chừng thì sao?"**
→ Hiện tại mất state vì chưa checkpoint; chấp nhận được vì Redis là overwrite + TTL và feature sẽ được tính lại từ cửa sổ kế tiếp. Production thì bật checkpoint xuống MinIO + state TTL.

**"Vì sao tách online store riêng, không đọc thẳng lake?"**
→ Query Delta trên MinIO mất vài giây, API cần mili giây. Nên tách hai tầng: offline (Delta) để train, online (Redis) để serve — và đây cũng là cách chống **training-serving skew**.

**"Xử lý dữ liệu bẩn thế nào?"**
→ Ba tầng: parser bọc `try/except` từng ván để không chết job; DQ check bằng SQL trên Trino (null `game_id`, `win_rate ∈ [0,1]`, `popularity > 0`); unit test cho phần tính ACPL/move-time.

**"Point-in-time correctness là gì, làm thế nào?"**
→ Khi tạo tập train, feature lịch sử của người chơi ở ván X chỉ được tính từ các ván **trước** X. Code: `Window.partitionBy(player, speed).orderBy(game_datetime).rowsBetween(unboundedPreceding, -1)` — số `-1` chính là chỗ loại ván hiện tại ra khỏi cửa sổ, chống **data leakage**.

**"Nếu phải làm lại, làm khác gì?"**
→ Đo coverage dữ liệu (tỷ lệ có eval/clock) **ngay từ Phase 0** thay vì phát hiện muộn; và bật checkpointing cho Flink sớm hơn thay vì để thành nợ kỹ thuật.

---

## Nối sang case Home Credit

Khi thảo luận case gian lận POS hay cảnh báo trễ hạn, dùng chính kinh nghiệm này:

- **Kiến trúc hai tầng batch + stream** — bạn đã làm thật, không phải lý thuyết.
- **Tầng nào cần realtime** — timing features realtime qua Flink; feature lịch sử theo batch. Ánh xạ thẳng sang: chặn hồ sơ gian lận realtime + rà soát cửa hàng đối tác theo batch.
- **Point-in-time correctness** — cực kỳ liên quan trong tín dụng: tính feature rủi ro khách hàng chỉ được dùng dữ liệu có tại thời điểm đó.
- **Online store cho quyết định nhanh** — Redis phục vụ điểm rủi ro cho hệ thống duyệt vay trong mili giây.

Câu mở lời tự nhiên: *"Cái này giống hệ thống em từng làm — có một đường batch tính feature lịch sử và một đường stream tính feature realtime, hai bên gặp nhau ở online store..."*
