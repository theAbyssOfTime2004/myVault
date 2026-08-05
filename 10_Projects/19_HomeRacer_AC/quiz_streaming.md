---
tags: [project, job-hunt, interview, data-engineer, quiz, home-credit, streaming]
status: active
created: 2026-07-31
related: "[[prep]] · [[de_concepts]] · [[lichess_mapping]]"
---

# Quiz — Streaming Systems & Failure Handling (40 câu)

> **Cách dùng:** làm hết phần câu hỏi, ghi đáp án ra chỗ khác, rồi mới dò. Phần giải thích mới là chỗ học.
> **Lưu ý:** đáp án đúng được phân bố đều A/B/C/D — không đoán theo vị trí được.
> Một số câu gắn thẳng vào project Lichess của bạn (đánh dấu 🎯) — đó là những câu dễ bị hỏi trong Q&A ngày 6/8.

---

## PHẦN A — Hình dạng pipeline streaming (câu 1-8)

**1.** Bốn tầng cốt lõi của một streaming pipeline theo đúng thứ tự là gì?
- ==A. Source → Stream Processor → Message Broker → Serving Store==
- B. Message Broker → Source → Serving Store → Stream Processor
- C. Source → Message Broker → Stream Processor → Serving Store
- D. Source → Serving Store → Message Broker → Stream Processor

**2.** Vai trò cốt lõi của message broker trong kiến trúc streaming là gì?
- ==A. Làm bộ đệm và tách rời producer khỏi consumer để hai bên chạy độc lập tốc độ==
- B. Biến đổi dữ liệu trước khi lưu
- C. Phục vụ truy vấn độ trễ thấp cho ứng dụng
- D. Nén dữ liệu để tiết kiệm dung lượng

**3.** Kafka lưu dữ liệu dưới dạng nào?
- A. Cây B-tree có index
- B. Bảng quan hệ có khóa chính
- C. Hàng đợi xóa message sau khi tiêu thụ
- ==D. Log chỉ ghi nối đuôi, bất biến (append-only immutable log)==

**4.** CDC (Change Data Capture) hoạt động bằng cách nào?
- A. Chạy `SELECT *` định kỳ trên bảng nguồn
- ==B. Đọc transaction log của DB (WAL của Postgres, binlog của MySQL)==
- C. Đặt trigger trên mọi bảng cần theo dõi
- D. So sánh snapshot hôm nay với snapshot hôm qua

**5.** Vì sao CDC được ưa dùng hơn việc query trực tiếp DB vận hành để lấy dữ liệu?
- ==A. Vì đọc transaction log không tạo thêm tải truy vấn lên DB đang phục vụ khách==
- B. Vì CDC luôn nhanh hơn về mặt thông lượng
- C. Vì CDC không cần quyền truy cập vào DB
- D. Vì CDC tự động làm sạch dữ liệu

**6.** Yêu cầu đặc trưng của tầng online serving store là gì?
- A. Dung lượng lưu trữ lớn với chi phí thấp nhất
- B. Hỗ trợ truy vấn SQL phức tạp nhiều bảng
- C. Nén dữ liệu tối đa
- ==D. Độ trễ đọc rất thấp, thường dưới 10ms==

**7.** 🎯 Trong project Lichess, tại sao message Kafka được đặt `key = game_id`?
- A. Để nén message tốt hơn
- B. Để tiết kiệm dung lượng lưu trữ trên broker
- ==C. Để mọi message của cùng một ván vào cùng partition, giữ đúng thứ tự và state==
- D. Vì Kafka bắt buộc phải có key cho mọi message

**8.** Kiến trúc chỉ dùng một nhánh streaming duy nhất, muốn tính lại lịch sử thì replay lại stream, gọi là gì?
- A. Lambda architecture
- ==B. Kappa architecture==
- C. Medallion architecture
- D. Data mesh

---

## PHẦN B — Hệ sinh thái open-source (câu 9-17)

**9.** Điểm khác biệt cốt lõi giữa Kafka và RabbitMQ là gì?
- A. Kafka nhanh hơn RabbitMQ trong mọi tình huống
- B. RabbitMQ không hỗ trợ nhiều consumer
- C. Kafka chỉ chạy trên Java, RabbitMQ chạy đa nền tảng
- ==D. Kafka giữ message theo retention nên replay được; RabbitMQ là queue, message tiêu thụ xong là mất==

**10.** Đặc điểm kiến trúc nổi bật của Apache Pulsar so với Kafka là gì?
- A. Tách biệt tầng compute và tầng storage
- B. Không cần message broker
- C. Chỉ hỗ trợ at-most-once
- D. Viết bằng C++ nên không có JVM overhead

**11.** Redpanda khác Kafka chủ yếu ở điểm nào?
- A. Dùng mô hình pub/sub khác hoàn toàn
- B. Không hỗ trợ partition
- C. Tương thích API Kafka nhưng viết bằng C++, không có overhead của JVM
- D. Chỉ chạy được trên cloud, không self-host được

**12.** Trong Kafka, thứ tự message được đảm bảo ở phạm vi nào?
- ==A. Toàn bộ topic==
- B. Trong từng partition
- C. Trong từng consumer group
- D. Toàn cluster nếu bật cấu hình ordering

**13.** ClickHouse và Apache Pinot thuộc nhóm nào và mạnh ở đâu?
- A. Message broker, mạnh về retention dài
- B. Stream processor, mạnh về windowing
- C. Object storage, mạnh về chi phí thấp
- D. OLAP real-time, tổng hợp hàng tỷ dòng trong vài mili giây

**14.** Cassandra thường được chọn làm serving store khi nào?
- A. Khi cần thông lượng ghi rất cao và khả năng scale ngang
- B. Khi cần join nhiều bảng phức tạp
- C. Khi dữ liệu nhỏ và cần transaction ACID chặt
- D. Khi cần lưu trữ file nhị phân lớn

**15.** Debezium là công cụ thuộc nhóm nào?
- A. Stream processor
- B. Online serving store
- ==C. CDC — bắt thay đổi từ DB đẩy vào stream==
- D. Orchestration

**16.** 🎯 Trong project Lichess, Strimzi đóng vai trò gì?
- A. Thư viện xử lý stream nhúng trong ứng dụng
- ==B. Kubernetes operator để triển khai và vận hành Kafka trên cluster==
- C. Table format cho Delta Lake
- D. Công cụ điều phối thay thế Airflow

**17.** Vì sao Redis phù hợp làm online store cho feature store hơn là query thẳng data lake?
- A. Vì Redis lưu được nhiều dữ liệu hơn
- B. Vì Redis hỗ trợ SQL đầy đủ
- C. Vì Redis rẻ hơn object storage
- ==D. Vì Redis in-memory trả về mili giây, còn query Delta trên object storage mất vài giây==

---

## PHẦN C — Flink vs Spark Streaming vs Kafka Streams (câu 18-25)

**18.** Mô hình xử lý của Apache Flink là gì?
- ==A. Record-at-a-time — xử lý từng event ngay khi đến==
- B. Micro-batching theo chu kỳ cố định
- C. Batch theo lịch hằng giờ
- D. Chỉ xử lý khi được gọi qua API

**19.** Spark Structured Streaming về bản chất hoạt động thế nào?
- A. True streaming từng event
- B. Chỉ chạy được trên dữ liệu tĩnh
- ==C. Chia luồng liên tục thành các micro-batch rồi dùng engine batch xử lý==
- D. Dựa hoàn toàn vào Kafka Consumer Group

**20.** Độ trễ điển hình của Spark Structured Streaming so với Flink?
- A. Thấp hơn Flink đáng kể
- B. Bằng nhau
- C. Chỉ khác khi dữ liệu lớn hơn 1TB
- ==D. Cao hơn — khoảng 100ms đến 1 giây, so với vài ms của Flink==

**21.** Khác biệt hạ tầng lớn nhất của Kafka Streams so với Flink và Spark?
- A. Kafka Streams cần cluster lớn hơn
- ==B. Kafka Streams chỉ là thư viện, không cần cụm xử lý riêng — deploy như một ứng dụng thường==
- C. Kafka Streams chạy trên GPU
- D. Kafka Streams không hỗ trợ state

**22.** Ràng buộc đáng chú ý nhất của Kafka Streams là gì?
- ==A. Chỉ đọc từ Kafka và ghi ra Kafka==
- B. Không hỗ trợ windowing
- C. Không chạy được trên Kubernetes
- D. Độ trễ cao hơn Spark

**23.** Flink dùng cơ chế nào để đảm bảo exactly-once khi có sự cố?
- A. Ghi log mọi event ra file rồi so sánh khi khởi động lại
- B. Chạy song song hai job rồi đối chiếu kết quả
- ==C. Checkpoint state định kỳ (thuật toán Chandy-Lamport) + sink có transaction==
- D. Dựa vào retention của Kafka để phát hiện trùng lặp

**24.** Khi nào chọn Spark Structured Streaming thay vì Flink?
- A. Khi cần độ trễ dưới 10ms
- B. Khi cần complex event processing
- C. Khi cần xử lý từng event riêng lẻ tức thì
- ==D. Khi ưu tiên thông lượng lớn, dùng chung API với batch, và hệ đã dựng sẵn trên Spark/Delta==

**25.** 🎯 Vì sao project Lichess chọn Flink cho stream nhưng Spark cho batch?
- A. Vì Flink không xử lý được dữ liệu lớn
- ==B. Vì cần true streaming và keyed state cho từng ván, còn batch thì cần thông lượng cao trên khối dữ liệu lớn==
- C. Vì Spark không hỗ trợ streaming
- D. Vì Flink rẻ hơn khi chạy trên GKE

---

## PHẦN D — Latency, Throughput, Concurrency (câu 26-32)

**26.** Latency đo cái gì?
- A. Thời gian một event đi từ nguồn tới đích
- ==B. Số event xử lý được mỗi giây==
- C. Số kết nối đồng thời hệ thống chịu được
- D. Dung lượng dữ liệu xử lý mỗi ngày

**27.** Gom nhiều event lại thành lô rồi mới xử lý sẽ dẫn tới điều gì?
- A. Giảm cả latency và throughput
- B. Tăng cả latency và giảm throughput
- C. Giảm latency và tăng throughput
- ==D. Tăng throughput nhưng cũng tăng latency==

**28.** Concurrency khác throughput ở chỗ nào?
- A. Không khác, chỉ là hai cách gọi
- B. Concurrency đo tốc độ, throughput đo số kết nối
- ==C. Concurrency là số việc chạy song song; throughput là số việc hoàn thành mỗi đơn vị thời gian==
- D. Concurrency chỉ áp dụng cho batch, throughput chỉ cho streaming

**29.** Hệ thống phát hiện gian lận thẻ tại điểm bán nên ưu tiên chỉ số nào?
- A. Throughput cao nhất có thể
- ==B. Latency thấp — phải quyết định trước khi giao dịch hoàn tất==
- C. Dung lượng lưu trữ
- D. Chi phí hạ tầng thấp nhất

**30.** 🎯 Trong project Lichess, file `.pgn.zst` không splittable khiến Spark chỉ chạy được 1 task. Đây là vấn đề về gì?
- ==A. Concurrency — không thể chia việc ra chạy song song==
- B. Latency — mỗi bản ghi xử lý quá lâu
- C. Chất lượng dữ liệu
- D. Dung lượng bộ nhớ

**31.** 🎯 Bước shred (cắt file thành nhiều shard theo ranh giới ván) giúp cải thiện điều gì, và bằng cách nào?
- A. Giảm latency của từng request tra cứu, bằng cách cache kết quả
- B. Giảm dung lượng lưu trữ, bằng cách nén tốt hơn
- C. Tăng độ chính xác dữ liệu, bằng cách loại ván lỗi
- ==D. Tăng throughput, bằng cách tăng số task chạy song song trên cùng hạ tầng==

**32.** Tăng concurrency có làm giảm latency của một request đơn lẻ không?
- A. Có, luôn luôn giảm tỷ lệ thuận
- B. Có, nếu tăng đủ số node
- ==C. Không — nó tăng tổng thông lượng, còn độ trễ một request vẫn phụ thuộc đường xử lý của chính nó==
- D. Không xác định được, phụ thuộc ngôn ngữ lập trình

---

## PHẦN E — Đảm bảo giao nhận (câu 33-36)

**33.** At-most-once nghĩa là gì?
- A. Không mất dữ liệu, có thể trùng
- B. Có thể mất dữ liệu, không bao giờ trùng
- C. Không mất, không trùng
- ==D. Mỗi message được xử lý đúng một lần trong mọi tình huống==

**34.** At-least-once đạt được bằng cơ chế nào, và hệ quả là gì?
- ==A. Retry khi không nhận được ack — không mất dữ liệu nhưng có thể trùng==
- B. Commit offset ngay khi gửi — có thể mất dữ liệu
- C. Two-phase commit — không mất không trùng
- D. Ghi đè theo khóa — luôn cho kết quả cuối đúng

**35.** Vì sao at-least-once thường đi kèm yêu cầu idempotency ở phía sink?
- A. Vì at-least-once làm giảm throughput
- B. Vì cần nén dữ liệu trước khi ghi
- C. Vì cần giữ thứ tự message
- ==D. Vì message có thể được xử lý lặp, nên sink phải cho kết quả như nhau dù ghi nhiều lần==

**36.** Exactly-once thường đạt được bằng cách nào?
- A. Chỉ cần bật retry ở producer
- B. Tăng retention của Kafka lên đủ dài
- ==C. Stateful processing + checkpoint, kết hợp two-phase commit hoặc sink idempotent==
- D. Dùng at-least-once rồi xóa trùng thủ công định kỳ

---

## PHẦN F — Kỹ thuật khôi phục sự cố (câu 37-40)

**37.** "Poison pill" trong streaming là gì và xử lý thế nào?
- A. Message quá lớn — cần chia nhỏ trước khi gửi
- ==B. Message lỗi format làm consumer crash lặp lại — đẩy vào DLQ và cho luồng chính chạy tiếp==
- C. Message trùng lặp — cần khử trùng theo id
- D. Message đến trễ — cần watermark để xử lý

**38.** Checkpointing trong Flink hoạt động thế nào?
- ==A. Định kỳ chụp snapshot state và offset, lưu ra storage bền vững để khôi phục sau sự cố==
- B. Ghi mọi event ra log file trên máy local
- C. Sao chép toàn bộ cluster sang vùng dự phòng
- D. Nén state để tiết kiệm bộ nhớ

**39.** 🎯 Job Flink trong project Lichess hiện chưa bật checkpointing. Hệ quả trực tiếp là gì?
- A. Job không chạy được quá 24 giờ
- B. Kết quả ghi vào Redis bị sai số
- C. Không dùng được sliding window
- ==D. Flink restart là mất sạch state, phải tính lại từ cửa sổ kế tiếp==

**40.** 🎯 Job Flink đó keyed theo `game_id` nhưng không có state TTL. Rủi ro là gì?
- A. Thứ tự message trong ván bị đảo lộn
- B. Redis bị đầy vì key không hết hạn
- ==C. State của các ván đã kết thúc không bao giờ được dọn, chạy lâu thì phình vô hạn==
- D. Không tính được stddev chính xác

---
---

# ĐÁP ÁN & GIẢI THÍCH

**1 — C.** Source → Broker → Processor → Serving Store. Nhớ mạch này là vẽ được whiteboard cho mọi bài streaming.

**2 — A.** Broker là bộ đệm và là ranh giới tách rời. Nhờ nó producer có thể phát nhanh hơn consumer xử lý mà không sập, và nhiều consumer khác nhau cùng đọc một nguồn.

**3 — D.** Append-only immutable log. Đây là lý do Kafka replay được — message không bị xóa khi tiêu thụ, chỉ hết hạn theo retention.

**4 — B.** Đọc transaction log (WAL/binlog). Trigger và polling đều là cách cũ, tạo tải lên DB nguồn.

**5 — A.** Không thêm tải truy vấn lên DB đang phục vụ khách — điểm mấu chốt trong hệ tài chính, vì query phân tích nặng có thể làm chậm hệ thống vận hành. (Lưu ý: CDC không tự làm sạch dữ liệu, và vẫn cần quyền truy cập.)

**6 — D.** Độ trễ đọc rất thấp (thường <10ms). Đây là tầng phục vụ quyết định tức thì, không phải tầng phân tích.

**7 — C.** Kafka chỉ đảm bảo thứ tự **trong** partition, nên key quyết định phân vùng. `key=game_id` → mọi nước của cùng ván về cùng partition → state và thứ tự đúng. Đây là câu trả lời chuẩn cho "làm sao đảm bảo thứ tự trong stream".

**8 — B.** Kappa. (Lambda là chạy song song hai nhánh batch + stream rồi hợp nhất — đơn giản hơn về khái niệm nhưng phải duy trì hai codebase.)

**9 — D.** Kafka giữ message theo retention → replay được từ offset. RabbitMQ là queue truyền thống, message tiêu thụ xong là mất. Khác biệt này quyết định khả năng chạy lại khi pipeline lỗi.

**10 — A.** Pulsar tách compute (broker) khỏi storage (BookKeeper), nên scale hai tầng độc lập. (Đáp án D là mô tả của Redpanda.)

**11 — C.** Redpanda tương thích API Kafka nhưng viết bằng C++, bỏ được overhead của JVM.

**12 — B.** Chỉ trong từng partition. Đây là một trong những điều bị hiểu nhầm nhiều nhất về Kafka — không có "thứ tự toàn topic".

**13 — D.** OLAP real-time. Khác Redis ở chỗ: Redis tra cứu theo khóa, còn ClickHouse/Pinot tổng hợp trên khối lớn cực nhanh — hai nhu cầu khác nhau.

**14 — A.** Cassandra mạnh về write throughput và scale ngang. Đổi lại: không hợp cho join phức tạp hay transaction chặt.

**15 — C.** Debezium là công cụ CDC phổ biến nhất, đọc log của Postgres/MySQL đẩy vào Kafka.

**16 — B.** Strimzi là Kubernetes operator cho Kafka — lo việc triển khai, cấu hình, vận hành Kafka trên K8s.

**17 — D.** Delta trên object storage mất vài giây; API cần mili giây. Đây chính là lý do tồn tại của bước materialize và của kiến trúc feature store hai tầng.

**18 — A.** Record-at-a-time, xử lý ngay khi event đến. Đây là định nghĩa của "true streaming".

**19 — C.** Micro-batching: chia luồng thành lô nhỏ rồi dùng engine batch. Về bản chất Spark Structured Streaming **không** phải true streaming.

**20 — D.** ~100ms-1s so với vài ms của Flink. Chênh lệch này bắt nguồn từ mô hình micro-batch.

**21 — B.** Kafka Streams chỉ là thư viện — đóng gói vào ứng dụng rồi deploy như một service thường, không cần dựng cụm xử lý. Đây là ưu điểm vận hành lớn nhất của nó.

**22 — A.** Chỉ đọc từ Kafka và ghi ra Kafka — gắn chặt với hệ sinh thái Kafka. Nếu cần đọc/ghi nguồn khác thì phải dùng Flink hoặc Spark.

**23 — C.** Checkpoint state định kỳ (Chandy-Lamport) lưu ra storage bền vững, kết hợp sink có transaction. Chỉ checkpoint thôi chưa đủ cho exactly-once end-to-end — sink cũng phải hợp tác.

**24 — D.** Khi ưu tiên throughput, muốn dùng chung API DataFrame cho cả batch lẫn stream, và hệ đã dựng trên Spark/Delta. Chọn công cụ theo bối cảnh, không theo "cái nào hiện đại hơn".

**25 — B.** Stream cần true streaming + keyed state theo từng ván; batch cần thông lượng cao trên khối dữ liệu lớn. Nói được lý do chọn theo **việc** chứ không theo thói quen là điểm cộng.

**26 — A.** Thời gian một event đi từ nguồn tới đích, đo bằng ms/µs.

**27 — D.** Gom lô → throughput tăng (ít overhead I/O hơn trên mỗi event) nhưng latency tăng (event phải nằm chờ đủ lô). Đây là đánh đổi kinh điển nhất trong streaming.

**28 — C.** Concurrency = số việc chạy **song song**; throughput = số việc **hoàn thành** mỗi đơn vị thời gian. Concurrency là phương tiện, throughput là kết quả.

**29 — B.** Latency thấp — quyết định phải xong trước khi giao dịch hoàn tất. Đây là ví dụ chuẩn cho câu hỏi "hành động phía sau có cần realtime không".

**30 — A.** Vấn đề concurrency: chỉ có 1 đơn vị công việc nên thêm máy vô ích. Chẩn đoán đúng loại nút thắt mới chọn đúng cách sửa.

**31 — D.** Tăng throughput bằng cách tăng số task song song, **hạ tầng không đổi**. 75 phút → 4 phút. Chú ý: nó không giảm latency của việc parse một ván đơn lẻ.

**32 — C.** Không. Tăng concurrency tăng tổng thông lượng, nhưng độ trễ một request vẫn do đường xử lý của chính nó quyết định. Đây là lý do vẫn cần Redis cho serving dù batch đã chạy nhanh.

**33 — B.** Có thể mất, không bao giờ trùng. Hợp với dữ liệu mà mất vài bản ghi không ảnh hưởng (log cảm biến, tracking chuột).

**34 — A.** Retry khi thiếu ack → không mất nhưng có thể trùng. Đây là mức mặc định phổ biến nhất trong thực tế.

**35 — D.** Vì message có thể được xử lý lặp lại, sink phải idempotent (upsert theo khóa, dedup theo id) để kết quả cuối vẫn đúng. **At-least-once + idempotent sink ≈ exactly-once về mặt hiệu quả** — và rẻ hơn nhiều so với 2PC thật.

**36 — C.** Stateful processing + checkpoint, kết hợp 2PC hoặc sink idempotent. Đắt nhất về độ phức tạp và hiệu năng — chỉ dùng khi nghiệp vụ thực sự đòi (chuyển tiền, kế toán).

**37 — B.** Message lỗi format làm consumer crash lặp vô hạn. Xử lý: bắt exception, đẩy vào DLQ, luồng chính chạy tiếp. Nguyên tắc: **một bản ghi hỏng không được phép giết cả pipeline**.

**38 — A.** Snapshot state + offset lưu ra storage bền vững (S3/MinIO/HDFS). Khi crash: khởi động lại, kéo checkpoint gần nhất, đọc tiếp từ offset tương ứng.

**39 — D.** Restart là mất sạch state. Chấp nhận được trong project này vì Redis là ghi đè + TTL và cửa sổ kế tiếp sẽ tính lại — nhưng phải nói rõ đây là **trade-off có ý thức**, không phải sơ suất.

**40 — C.** State của ván đã kết thúc không bao giờ được dọn → phình vô hạn theo thời gian. Lưu ý phân biệt: **Redis có TTL, nhưng Flink state thì không** — đây đúng là lỗ hổng bạn tự nhận trong doc, và nói ra trước khi bị hỏi sẽ ghi điểm.

---

## Thang tự đánh giá

| Đúng | Ý nghĩa |
|---|---|
| 34-40 | Nắm chắc — đủ tự tin cho phần Q&A với assessors |
| 26-33 | Ổn — đọc kỹ giải thích câu sai, tập trung phần D và E |
| < 26 | Đọc lại [[de_concepts]] mục 2, 4, 8 và [[lichess_mapping]] phần 3-4 |

**Sáu câu 🎯 gắn với project Lichess (7, 16, 25, 30, 31, 39, 40) là quan trọng nhất** — đó là những câu nếu assessor hỏi thì bạn phải trả lời được ngay, vì chúng nói về thứ chính bạn đã xây.

**Ba ý cốt lõi nếu chỉ nhớ được vài thứ:**
1. Gom lô → throughput tăng, latency tăng (đánh đổi kinh điển)
2. At-least-once + idempotent sink ≈ exactly-once, rẻ hơn nhiều
3. Một bản ghi hỏng không được giết cả pipeline → DLQ
