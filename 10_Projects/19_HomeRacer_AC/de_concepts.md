---
tags: [project, job-hunt, interview, data-engineer, reference, home-credit]
status: active
created: 2026-07-31
related: "[[prep]]"
---

# Từ điển khái niệm Data Engineering — cho AC 6/8

> Sắp theo **đường đi của dữ liệu**: nguồn → nạp → lưu → xử lý → điều phối → mô hình hóa → phục vụ → chất lượng → quy mô → kiến trúc → quản trị.
> Mỗi mục: **khái niệm — giải thích ngắn — vì sao xuất hiện trong case**.
> Mức độ: 🟢 căn bản (phải biết) · 🟡 trung cấp (nên biết) · 🔴 nâng cao (biết để ghi điểm)

---

## 1. Nền tảng — khung tư duy

**🟢 Data pipeline** — chuỗi bước đưa dữ liệu từ nguồn đến nơi dùng được (lấy → biến đổi → lưu → phục vụ). Mọi case DE đều là thiết kế một pipeline.

**🟢 ETL vs ELT** — *ETL*: biến đổi **trước** khi load vào kho. *ELT*: load thô vào kho/lake **rồi** mới biến đổi. Ngày nay ELT phổ biến hơn vì lưu trữ rẻ và compute co giãn. Nói được lý do chọn là ăn điểm.

**🟢 Batch vs Streaming** — *Batch*: xử lý theo lô định kỳ (hằng giờ/ngày), đơn giản, rẻ, độ trễ cao. *Streaming*: xử lý liên tục từng event, phức tạp, tốn kém, độ trễ thấp.
→ **Câu hỏi quyết định: hành động phía sau có cần realtime không?** Nếu collections gọi điện vào hôm sau thì batch là đủ. Nếu phải chặn giao dịch gian lận ngay lúc quẹt thẻ thì bắt buộc streaming.

**🟢 Micro-batch** — trung gian: gom event thành lô rất nhỏ (vài giây) rồi xử lý. Spark Structured Streaming hoạt động kiểu này.

**🟢 OLTP vs OLAP** — *OLTP*: DB vận hành, nhiều giao dịch nhỏ, ghi/đọc theo dòng (PostgreSQL, MySQL — nơi hồ sơ vay được tạo). *OLAP*: DB phân tích, quét lượng lớn để tổng hợp (BigQuery, Snowflake, ClickHouse).
→ Nguyên tắc vàng: **không chạy truy vấn phân tích nặng trên DB vận hành** — sẽ làm sập hệ thống đang phục vụ khách.

**🟡 Data product** — dữ liệu/đầu ra được đóng gói như một sản phẩm có người dùng, SLA, chủ sở hữu rõ ràng (không chỉ là một bảng ai đó tạo rồi bỏ quên).

---

## 2. Nạp dữ liệu (Ingestion)

**🟢 Batch load** — kéo dữ liệu theo lô định kỳ: dump toàn bộ bảng, hoặc **incremental** (chỉ lấy bản ghi mới/đổi từ lần trước, dựa vào cột timestamp hoặc id tăng dần).

**🟡 CDC (Change Data Capture)** — bắt **từng thay đổi** (insert/update/delete) từ DB vận hành bằng cách đọc transaction log, đẩy sang lake/stream. Ưu điểm: gần realtime, không làm nặng DB nguồn. Công cụ: Debezium.
→ Rất hay dùng trong case tài chính: đưa dữ liệu khoản vay/thanh toán từ core banking sang hệ phân tích.

**🟢 Message broker** — hàng đợi/log trung gian nhận event, tách **producer** (bên gửi) khỏi **consumer** (bên nhận). Cho phép hai bên chạy với tốc độ khác nhau, và nhiều consumer cùng đọc một nguồn.

**🟢 Kafka** — broker mặc định của ngành. Các khái niệm phải biết:
- **Topic**: kênh chứa event theo chủ đề.
- **Partition**: topic chia nhiều phần để xử lý song song; thứ tự chỉ được đảm bảo **trong** một partition.
- **Offset**: số thứ tự của message trong partition — consumer lưu offset để biết đọc tới đâu, và có thể **tua lại** (replay).
- **Consumer group**: nhóm consumer chia nhau các partition để xử lý song song.
- **Retention**: Kafka **giữ** message một thời gian (VD 7 ngày) → đọc lại được, đây là điểm khác queue truyền thống.

**🟡 Pulsar / RabbitMQ / Kinesis / Pub/Sub** — các lựa chọn khác. RabbitMQ là queue truyền thống (message tiêu thụ xong là mất). Kinesis (AWS), Pub/Sub (GCP) là bản managed trên cloud.

**🟡 Webhook / API polling** — nạp từ hệ thống bên thứ ba: webhook (họ đẩy sang mình) hoặc polling (mình định kỳ hỏi họ).

---

## 3. Lưu trữ

**🟢 Data lake** — kho lưu dữ liệu **thô**, đủ loại định dạng, rẻ, linh hoạt (S3, GCS, ADLS). Nhược: dễ thành "data swamp" nếu không quản trị.

**🟢 Data warehouse** — kho dữ liệu **đã cấu trúc**, tối ưu cho truy vấn phân tích (BigQuery, Snowflake, Redshift). Nhược: kém linh hoạt với dữ liệu phi cấu trúc, đắt hơn.

**🟢 Lakehouse** — kết hợp: lưu file rẻ như lake nhưng có tính năng kiểu warehouse (transaction ACID, schema, time travel) nhờ **table format**. Đây là kiến trúc hiện đại phổ biến — và là kiến trúc project Lichess của bạn.

**🟡 Table format: Delta Lake / Apache Iceberg / Hudi** — lớp metadata phủ lên các file Parquet, cho phép: ACID transaction, cập nhật/xóa dòng, **time travel** (đọc lại trạng thái bảng ở thời điểm quá khứ), schema evolution.
 
**🟢 Định dạng file:**
- **CSV** — theo dòng, dễ đọc, nhưng cồng kềnh, không có kiểu dữ liệu, chậm.
- **JSON** — linh hoạt, lồng nhau được, nhưng nặng và chậm.
- **Parquet** — **theo cột**, nén tốt, đọc nhanh cho phân tích. Mặc định của lake/lakehouse.
- **Avro** — theo dòng, mạnh về schema evolution, hay dùng cho message trong Kafka.
- **ORC** — theo cột, tương tự Parquet, phổ biến trong hệ Hive.

**🟢 Vì sao lưu theo cột (columnar) nhanh hơn** — truy vấn phân tích thường chỉ đọc vài cột trong hàng trăm cột. Lưu theo cột cho phép **chỉ đọc đúng cột cần**, và nén tốt hơn vì dữ liệu cùng cột giống nhau. Giải thích được ý này là ghi điểm.

**🟡 Partitioning (phân vùng lưu trữ)** — chia dữ liệu thành thư mục theo cột (VD `/date=2026-08-06/`), để truy vấn chỉ quét đúng phần cần → nhanh và rẻ hơn. Thường phân vùng theo ngày.

**🟡 Object storage vs HDFS** — ngày nay dùng object storage trên cloud (S3/GCS) thay cho HDFS truyền thống: tách biệt **storage** và **compute**, co giãn độc lập.

---

## 4. Xử lý (Processing)

**🟢 Spark** — engine xử lý phân tán phổ biến nhất cho batch (và micro-batch streaming). Chia dữ liệu ra nhiều máy xử lý song song.

**🟢 Flink** — engine **true streaming**, xử lý từng event, mạnh về state và event-time, hỗ trợ exactly-once. Chọn Flink khi cần độ trễ thật thấp.

**🟡 Kafka Streams / ksqlDB** — xử lý stream nhẹ, chạy như thư viện trong ứng dụng, không cần cụm riêng.

**🟡 dbt** — công cụ biến đổi dữ liệu **trong warehouse** bằng SQL, có version control, test, tài liệu. Trụ cột của ELT hiện đại.

**🟡 Stateless vs stateful processing** — *stateless*: mỗi event xử lý độc lập (lọc, đổi định dạng). *stateful*: cần nhớ dữ liệu trước đó (đếm số giao dịch của khách trong 1 giờ) → cần lưu state và checkpoint.

**🟡 Windowing (cửa sổ thời gian)** — gom event theo khoảng thời gian để tổng hợp:
- **Tumbling**: cửa sổ liền nhau, không chồng lấn (mỗi 5 phút một cửa sổ).
- **Sliding**: chồng lấn (5 phút gần nhất, cập nhật mỗi 1 phút).
- **Session**: gom theo phiên hoạt động, kết thúc khi im lặng đủ lâu.

**🔴 Event time vs Processing time** — *event time*: lúc sự việc **thực sự xảy ra**. *processing time*: lúc hệ thống **nhận được**. Chúng lệch nhau vì mạng trễ. Tính toán đúng phải dựa trên event time.

**🔴 Watermark** — cơ chế báo "đã nhận đủ event tới mốc thời gian T, có thể chốt cửa sổ", để xử lý event đến trễ mà không chờ vô hạn.

---

## 5. Điều phối (Orchestration)

**🟢 Orchestration** — điều phối thứ tự và lịch chạy của các bước trong pipeline, xử lý phụ thuộc, retry khi lỗi, cảnh báo. Không có nó thì pipeline là mớ cron rời rạc không ai kiểm soát.

**🟢 Airflow** — công cụ điều phối phổ biến nhất. Alternatives: Dagster, Prefect, Mage.

**🟢 DAG (Directed Acyclic Graph)** — đồ thị các task có hướng, không vòng lặp: task B chạy sau khi task A xong. Cách biểu diễn pipeline trong Airflow.

**🟢 Idempotency (tính bất biến khi chạy lại)** — **TỪ KHÓA VÀNG.** Chạy cùng một job hai lần cho **cùng một kết quả**, không nhân đôi dữ liệu. Đạt được bằng: ghi đè theo partition, **upsert/merge theo khóa**, khử trùng theo id.
→ Đây là nền tảng của mọi cơ chế retry và recovery. Nhắc được từ này trong case là điểm cộng rõ rệt.

**🟢 Backfill** — chạy lại pipeline cho dữ liệu quá khứ (vì sửa lỗi logic, hoặc mới thêm feature). Pipeline thiết kế tốt phải backfill được dễ dàng — và điều đó đòi hỏi idempotency.

**🟡 Retry & alerting** — tự thử lại khi lỗi tạm thời (mạng, timeout), báo động khi lỗi thật. Cần phân biệt hai loại lỗi.

**🟡 SLA (Service Level Agreement)** — cam kết: dữ liệu phải sẵn sàng trước 7h sáng. Biến kỳ vọng mơ hồ thành cam kết đo được.

---

## 6. Mô hình hóa dữ liệu (Data Modeling)

**🟢 Star schema** — mô hình kinh điển cho phân tích: một **fact table** ở giữa nối tới nhiều **dimension table** xung quanh (hình sao).

**🟢 Fact vs Dimension** —
- **Fact**: sự kiện/giao dịch có số đo, nhiều dòng (mỗi khoản giải ngân, mỗi lần thanh toán). Chứa số liệu + khóa ngoại.
- **Dimension**: thực thể mô tả, ít dòng hơn (khách hàng, cửa hàng, sản phẩm, ngày). Chứa thuộc tính để lọc/nhóm.
→ Câu hay hỏi: "Bảng này là fact hay dimension?" — hỏi ngược: nó ghi *sự kiện* hay mô tả *thực thể*?

**🟡 Snowflake schema** — star schema với dimension được chuẩn hóa thêm (tách nhỏ). Ít trùng lặp hơn nhưng phải join nhiều hơn.

**🟢 Grain (độ hạt)** — "một dòng trong bảng này đại diện cho cái gì?" VD: một dòng = một lần thanh toán, hay = một khách một tháng? **Chốt grain trước khi thiết kế bảng** — nhầm grain là hỏng cả mô hình. Nói được từ này rất chuyên nghiệp.

**🟡 SCD (Slowly Changing Dimension)** — xử lý thuộc tính thay đổi theo thời gian (khách đổi địa chỉ):
- **Type 1**: ghi đè, mất lịch sử.
- **Type 2**: thêm dòng mới với khoảng hiệu lực (valid_from/valid_to) → **giữ được lịch sử**, phổ biến nhất.

**🟡 Normalization vs Denormalization** — chuẩn hóa (tách bảng, ít trùng lặp, tốt cho OLTP) vs phi chuẩn hóa (gộp bảng, ít join, nhanh cho OLAP).

**🟡 Medallion architecture (Bronze/Silver/Gold)** — tổ chức lake theo 3 tầng: **Bronze** = dữ liệu thô nguyên trạng; **Silver** = đã làm sạch, chuẩn hóa, khử trùng; **Gold** = đã tổng hợp, sẵn sàng cho báo cáo/model. Rất dễ vẽ lên whiteboard và rất được ưa dùng khi trình bày.

**🟡 Data mart** — tập dữ liệu con phục vụ một phòng ban cụ thể (mart cho rủi ro, mart cho marketing).

---

## 7. Phục vụ (Serving)

**🟢 Online serving store** — nơi lưu kết quả để đọc **độ trễ thấp** (mili giây) khi ứng dụng cần ngay: **Redis** (in-memory, nhanh nhất), Cassandra, DynamoDB, ScyllaDB.
→ Trong case: điểm rủi ro tính sẵn được ghi vào đây để hệ thống duyệt vay đọc trong tích tắc.

**🟡 Feature store** — nơi lưu trữ và phục vụ **feature** cho ML, với hai mặt:
- **Offline store**: dữ liệu lịch sử để train model (lưu trong lake/warehouse).
- **Online store**: feature mới nhất để suy luận realtime (lưu trong Redis/Cassandra).
- **Training-serving skew**: vấn đề feature lúc train khác lúc phục vụ → feature store sinh ra để chống điều này.
→ Đây chính là project Lichess của bạn — nói được cả hai mặt là rất mạnh.

**🟡 Point-in-time correctness / Data leakage** — khi tạo dữ liệu train, chỉ được dùng thông tin **có tại thời điểm đó**, không dùng dữ liệu tương lai. Vi phạm = model đẹp trên giấy, sập trong thực tế. Cực kỳ quan trọng trong tín dụng.

**🟡 Caching** — lưu tạm kết quả hay dùng để giảm tải và giảm độ trễ.

**🟡 Reverse ETL** — đẩy dữ liệu từ warehouse **ngược lại** vào hệ thống vận hành (CRM, công cụ gửi SMS) để hành động.

---

## 8. Chất lượng & Độ tin cậy

**🟢 Data quality checks** — kiểm tra tự động: không null ở cột bắt buộc, giá trị trong khoảng hợp lệ, khóa duy nhất, số dòng không sụt bất thường, tổng khớp với nguồn. Công cụ: Great Expectations, dbt tests.

**🟢 Delivery semantics (đảm bảo giao nhận)** —
- **At-most-once**: có thể mất, không bao giờ trùng.
- **At-least-once**: không mất, **có thể trùng** → phải khử trùng bằng idempotency. Mặc định thực tế phổ biến nhất.
- **Exactly-once**: không mất, không trùng. Đạt bằng checkpoint + transactional sink (Flink + Kafka transactions). Đắt và phức tạp nhất.

**🟢 Checkpointing** — định kỳ chụp lại state + offset đang xử lý. Khi sập, khởi động lại từ checkpoint gần nhất thay vì làm lại từ đầu.

**🟢 Dead-letter queue (DLQ)** — message lỗi lặp lại nhiều lần được đẩy sang hàng đợi phụ để điều tra sau, **thay vì chặn nghẽn cả pipeline**.

**🟡 Backpressure** — khi consumer xử lý chậm hơn producer, hệ thống phát tín hiệu ngược để giảm tốc độ nạp, tránh tràn bộ nhớ và sập.

**🟡 Schema evolution** — schema nguồn thay đổi (thêm/xóa/đổi kiểu cột) mà không làm gãy pipeline. Avro/Parquet + table format hỗ trợ việc này.

**🟡 Data contract** — thỏa thuận giữa bên tạo dữ liệu và bên dùng: schema, ý nghĩa, SLA, cam kết không đổi đột ngột. Giải pháp cho gốc rễ của phần lớn sự cố pipeline.

**🟡 Data lineage** — truy vết dữ liệu đi từ đâu, qua những biến đổi nào, tới đâu. Cần khi debug và khi audit (bắt buộc trong tài chính).

**🟡 Data observability** — giám sát sức khỏe dữ liệu: độ tươi (freshness), khối lượng, phân phối, schema. Phát hiện sự cố **trước khi** người dùng phát hiện.

**🔴 Data drift** — phân phối dữ liệu thay đổi theo thời gian làm model xuống cấp. Cần giám sát và train lại.

---

## 9. Quy mô & Hiệu năng

**🟢 Latency vs Throughput vs Concurrency** —
- **Latency**: thời gian xử lý **một** bản ghi (ms).
- **Throughput**: số bản ghi **mỗi giây**.
- **Concurrency**: số việc chạy **song song**.
- **Đánh đổi**: gom lô lớn → throughput tăng nhưng latency **tăng**. Đây là câu hỏi rất hay gặp, đừng lẫn ba khái niệm.

**🟡 Horizontal vs Vertical scaling** — mở rộng ngang (thêm máy) vs mở rộng dọc (máy mạnh hơn). Hệ dữ liệu lớn gần như luôn chọn ngang.

**🟡 Shuffle** — bước dữ liệu phải di chuyển giữa các máy trong Spark (khi join hoặc groupBy). **Đắt nhất trong xử lý phân tán** — tối ưu Spark chủ yếu là giảm shuffle.

**🟡 Data skew (lệch dữ liệu)** — một partition chứa quá nhiều dữ liệu (VD một cửa hàng chiếm 40% giao dịch) → một máy làm mãi không xong trong khi các máy khác rảnh. Xử lý: salting key, tách riêng key nóng.

**🟡 Small file problem** — quá nhiều file nhỏ làm chậm nghiêm trọng (chi phí mở file lớn hơn chi phí đọc). Xử lý: **compaction** — gộp định kỳ thành file lớn hơn.

**🔴 Predicate pushdown** — đẩy điều kiện lọc xuống tầng đọc file để chỉ đọc phần cần, thay vì đọc hết rồi lọc. Parquet hỗ trợ tốt.

**🔴 Broadcast join** — khi một bảng đủ nhỏ, gửi nguyên bản sao tới mọi máy để join tại chỗ, **tránh shuffle**. Kỹ thuật tối ưu Spark kinh điển.

---

## 10. Kiến trúc

**🟡 Lambda architecture** — chạy **song song** hai nhánh: batch (chính xác, chậm) + streaming (nhanh, gần đúng), rồi hợp nhất khi phục vụ. Nhược: phải duy trì **hai** codebase cho cùng một logic.

**🟡 Kappa architecture** — chỉ một nhánh **streaming** duy nhất; muốn tính lại lịch sử thì replay lại stream. Đơn giản hơn về vận hành.

**🟡 Medallion** — xem mục 6, là cách tổ chức tầng dữ liệu trong lakehouse.

**🔴 Data mesh** — phi tập trung hóa: mỗi domain (tín dụng, thu hồi nợ, marketing) sở hữu và vận hành dữ liệu của mình như một sản phẩm, thay vì một đội trung tâm ôm hết.

**🔴 CAP theorem** — hệ phân tán chỉ đạt được 2 trong 3: **C**onsistency, **A**vailability, **P**artition tolerance. Vì phân vùng mạng là điều không tránh được, thực tế là chọn giữa C và A.

**🔴 Sharding & Replication** — *sharding*: chia dữ liệu ra nhiều node để mở rộng. *replication*: nhân bản để chịu lỗi và tăng khả năng đọc.

---

## 11. Quản trị & Tuân thủ (quan trọng vì đây là công ty tài chính)

**🟢 PII (Personally Identifiable Information)** — dữ liệu định danh cá nhân: CMND/CCCD, số điện thoại, địa chỉ, thu nhập. Trong tài chính đây là dữ liệu nhạy cảm bậc nhất.

**🟡 Masking / Anonymization / Encryption** — che dữ liệu nhạy cảm khi hiển thị; ẩn danh khi phân tích; mã hóa khi lưu và khi truyền.

**🟡 Access control (RBAC)** — phân quyền theo vai trò: không phải ai cũng được xem cột thu nhập hay CCCD.

**🟡 Data retention** — chính sách giữ dữ liệu bao lâu rồi xóa. Ngành tài chính bị luật ràng buộc (vừa buộc giữ để audit, vừa buộc xóa theo quyền riêng tư).

**🟡 Audit trail** — nhật ký ai truy cập/thay đổi cái gì, khi nào. Bắt buộc với tổ chức tín dụng.

**🔴 Model governance / Explainability** — với quyết định tín dụng, phải giải thích được **vì sao** từ chối một khách. Model hộp đen thuần túy có rủi ro pháp lý.

---

## 12. Bộ câu trả lời nhanh — nếu bị hỏi bất ngờ

| Câu hỏi | Trả lời gọn |
|---|---|
| Batch hay streaming? | Tùy **hành động phía sau có cần realtime không**. Chặn giao dịch → streaming. Gọi điện hôm sau → batch. |
| Vì sao Parquet? | Lưu theo cột: chỉ đọc cột cần, nén tốt → nhanh và rẻ cho phân tích. |
| Xử lý trùng lặp thế nào? | Thiết kế **idempotent**: upsert theo khóa nghiệp vụ, khử trùng theo event id. |
| Pipeline sập giữa chừng? | Khởi động lại từ **checkpoint**, replay từ Kafka offset, chạy lại an toàn nhờ idempotency. |
| Dữ liệu bẩn/lỗi? | Data quality checks tự động + **DLQ** cho bản ghi lỗi, không chặn cả luồng. |
| Truy vấn quá chậm? | Phân vùng, nén thành file lớn hơn (compaction), định dạng cột, giảm shuffle. |
| Scale ra sao? | Mở rộng ngang: phân vùng dữ liệu, thêm consumer/executor, chú ý **skew**. |
| Bắt đầu từ đâu? | Từ **quyết định kinh doanh** cần hỗ trợ, đi ngược về dữ liệu cần có. Không bắt đầu từ công nghệ. |

---

## 13. Nếu chỉ kịp nhớ 10 từ

1. **Idempotency** — chạy lại không nhân đôi
2. **Checkpointing** — khôi phục sau sự cố
3. **CDC** — bắt thay đổi từ DB nguồn
4. **Partition** — chia để xử lý song song / quét ít hơn
5. **Fact & Dimension** — xương sống mô hình phân tích
6. **Grain** — một dòng đại diện cho cái gì
7. **At-least-once** — mặc định thực tế, nên cần idempotency
8. **DLQ** — cách ly bản ghi lỗi
9. **Latency ≠ Throughput** — trễ một bản ghi vs số bản ghi/giây
10. **Batch vs Streaming quyết định bởi hành động phía sau**, không phải bởi công nghệ nghe hay
