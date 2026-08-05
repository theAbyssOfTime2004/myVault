---
tags: [project, job-hunt, interview, data-engineer, streaming, home-credit]
status: active
created: 2026-07-31
related: "[[quiz_streaming]] · [[de_concepts]] · [[lichess_mapping]]"
---

# Bốn khái niệm streaming — đào sâu

> Bốn thứ này hay bị nói kiểu học thuộc. Hiểu được **cơ chế bên dưới** thì trả lời câu nào cũng ra, và nghe rất khác so với đọc định nghĩa.

---

## 1. Kafka Streams — "chỉ là thư viện, không cần cụm riêng"

### Khác biệt gốc: framework vs library

**Flink và Spark là framework:** bạn viết job rồi **nộp nó cho một cụm**. Cụm đó có bộ điều phối riêng (JobManager của Flink, Driver của Spark) chịu trách nhiệm chia task xuống các worker, theo dõi, khởi động lại khi lỗi. Cụm này là **một hệ thống riêng bạn phải dựng và vận hành**.

**Kafka Streams là thư viện:** bạn `import` nó vào code Java/Scala, viết logic, build ra một file `.jar`. Chạy nó lên là xong — nó chỉ là **một tiến trình JVM bình thường**. Đóng Docker, deploy như một microservice trên K8s, EC2, hay bất cứ đâu.

```
Flink:          [code job] ──submit──> [Flink Cluster: JobManager + TaskManagers]
                                        ↑ bạn phải dựng và nuôi cụm này

Kafka Streams:  [code + thư viện] ──build──> [app.jar] ──run──> chỉ là một process
                                                                không có cụm nào cả
```

### Vậy nó scale kiểu gì nếu không có cụm?

Đây là chỗ thiết kế thông minh: **nó mượn cơ chế consumer group của Kafka**.

- Chạy 3 instance của cùng ứng dụng, đặt cùng `application.id`.
- Kafka group coordinator tự chia các partition cho 3 instance đó.
- Muốn scale? **Chạy thêm instance** — Kafka tự rebalance.
- Một instance chết? Kafka chia lại partition cho các instance còn sống.

→ Nó không cần bộ điều phối riêng vì **Kafka chính là bộ điều phối**.

### State thì sao?

- State lưu local bằng **RocksDB** trong từng instance.
- Đồng thời được sao lưu vào một **changelog topic** trong Kafka.
- Instance chết → instance mới đọc lại changelog topic để dựng lại state.

→ Khả năng chịu lỗi cũng đến từ Kafka. Toàn bộ "phần khó" được đẩy sang Kafka.

### Cái giá phải trả

**Chỉ đọc từ Kafka, chỉ ghi ra Kafka.** Muốn ghi thẳng vào Postgres hay Redis thì phải thêm Kafka Connect như một mảnh riêng. Với Flink thì connector nguồn/đích là chuyện bình thường.

### Vì sao điều này quan trọng trong thực tế

Với một đội đã chạy microservice trên K8s, Kafka Streams là **"thêm một service nữa"** — không có nền tảng mới nào phải học và nuôi. Còn một cụm Flink là **một hệ thống cần người trực**.

**Nối vào trải nghiệm thật của bạn (rất mạnh khi kể):** trong project Lichess bạn phải dựng Flink K8s Operator + cert-manager, và gặp bug operator crashloop trên K8s 1.35 phải dò phiên bản tương thích. **Đó chính xác là chi phí vận hành mà Kafka Streams tránh được.** Nói được câu này nghĩa là bạn hiểu đánh đổi bằng trải nghiệm, không phải bằng bảng so sánh đọc được.

> **Câu trả lời gọn:** *"Flink và Spark là framework — phải nộp job cho một cụm mình dựng. Kafka Streams chỉ là thư viện: build ra jar rồi chạy như một app thường, scale bằng cách chạy thêm instance vì nó mượn consumer group của Kafka làm bộ điều phối. Đổi lại nó chỉ đọc ghi được với Kafka."*

---

## 2. Checkpointing & thuật toán Chandy-Lamport

### Bài toán: chụp ảnh một hệ đang chạy mà không dừng nó

Job Flink có nhiều operator nằm trên nhiều máy, mỗi cái giữ state riêng. Muốn khôi phục sau sự cố thì phải lưu lại **trạng thái nhất quán của toàn bộ job tại cùng một thời điểm logic**.

Cách ngây thơ: dừng hết mọi thứ → chụp → chạy tiếp. Giết chết thông lượng, không dùng được cho hệ chạy 24/7.

### Lời giải: barrier trôi theo dòng dữ liệu

Flink dùng biến thể của **Chandy-Lamport**, gọi là *asynchronous barrier snapshotting*:

1. **JobManager chèn một dấu hiệu đặc biệt gọi là barrier** vào luồng dữ liệu tại nguồn — nó nằm **giữa bản ghi thứ n và n+1**.
2. Barrier **trôi theo dòng dữ liệu** qua đồ thị xử lý, y như một bản ghi bình thường.
3. Operator nào nhận được barrier trên **tất cả** đầu vào của nó → **chụp state của chính mình** → đẩy barrier tiếp xuống dưới.
4. Ảnh chụp được ghi ra storage bền vững (S3/MinIO/HDFS).

```
Nguồn ──[r5][r4][B][r3][r2][r1]──> Operator A ──> Operator B ──> Sink
                    ↑
              barrier trôi cùng dữ liệu
              mọi thứ TRƯỚC nó nằm trong ảnh chụp
              mọi thứ SAU nó thì không
```

**Vì sao cách này cho ảnh nhất quán:** vì barrier đi cùng dữ liệu, nó cắt dòng chảy thành "trước" và "sau" một cách rõ ràng ở **mọi** operator — mà **không cần dừng xử lý**. Dữ liệu vẫn chảy trong lúc chụp.

**Barrier alignment:** nếu một operator có 2 đầu vào và barrier tới đầu này trước, nó **giữ tạm** đầu vào đó lại cho tới khi barrier tới nốt đầu kia — để đảm bảo không trộn dữ liệu trước và sau barrier. (Sau này Flink có thêm *unaligned checkpoint* để giảm độ trễ do chờ này.)

### Khôi phục sau sự cố

Khởi động lại toàn bộ operator từ ảnh chụp thứ N, **đồng thời** đặt lại offset Kafka về đúng vị trí đã ghi trong ảnh chụp đó. State và vị trí đọc khớp nhau → xử lý tiếp như chưa từng có sự cố.

→ Điểm mấu chốt: **checkpoint lưu cả state lẫn offset**. Lưu mỗi state mà không lưu offset thì vô nghĩa.

### Nhưng checkpoint MỘT MÌNH chưa đủ cho exactly-once

Checkpoint đảm bảo **state bên trong** đúng. Nhưng thế giới bên ngoài **không tự quay ngược**: nếu bạn đã ghi ra sink giữa checkpoint N và lúc crash, rồi replay từ N, thì những lần ghi đó **xảy ra hai lần**.

→ Đây là ranh giới giữa **exactly-once state** và **exactly-once end-to-end**. Sink phải hợp tác. Xem mục 4.

> **Câu trả lời gọn:** *"Flink chèn barrier vào luồng dữ liệu; operator nào nhận đủ barrier trên mọi đầu vào thì chụp state của mình rồi chuyển barrier xuống dưới — nên chụp được ảnh nhất quán của cả job mà không phải dừng xử lý. Checkpoint lưu cả state lẫn offset, khôi phục là khởi động lại từ đó. Nhưng checkpoint chỉ đảm bảo state; muốn exactly-once đến tận đầu ra thì sink cũng phải transactional hoặc idempotent."*

---

## 3. Poison pill & Dead Letter Queue

### Vì sao gọi là "viên thuốc độc"

Không phải vì bản ghi đó xấu, mà vì nó **giết consumer theo vòng lặp**:

```
1. Consumer đọc message ở offset N
2. Parse lỗi → ném exception → consumer chết
3. Offset N CHƯA được commit
4. Consumer khởi động lại → đọc lại đúng offset N
5. Lại chết → quay về bước 3 → VÒNG LẶP VÔ TẬN
```

**Hậu quả nặng hơn nhiều so với mất một bản ghi:** pipeline **kẹt cứng tại offset N**. Mọi message phía sau — có thể là hàng triệu bản ghi hoàn toàn hợp lệ — **không bao giờ được xử lý**. Một bản ghi hỏng làm chết cả luồng.

### Vì sao không đơn giản bỏ qua nó?

Bỏ qua được — đó chính là `try/except: continue`. Nhưng khi đó bạn **âm thầm mất dữ liệu mà không biết mất bao nhiêu**. Ba tháng sau phát hiện thiếu 2% giao dịch mà không truy được gì.

**DLQ = bỏ qua + giữ lại + nhìn thấy được.**

### Mẫu DLQ đầy đủ

1. Bắt exception.
2. Đẩy **message gốc + metadata lỗi** sang topic riêng, ví dụ `lichess.tv.moves.dlq`. Metadata gồm: nội dung exception, thời điểm, topic/partition/offset gốc, số lần đã thử lại.
3. **Commit offset** → luồng chính chạy tiếp.
4. **Cảnh báo theo độ sâu DLQ** — DLQ có 5 message là chuyện thường; có 50.000 message nghĩa là schema nguồn vừa đổi.
5. Sửa bug xong thì **replay lại từ DLQ**.

### Phân biệt hai loại lỗi — chỗ tinh tế

| Loại lỗi | Ví dụ | Cách xử lý |
|---|---|---|
| **Tạm thời** (transient) | Mạng timeout, DB đang restart | **Retry có backoff** — thử lại sẽ thành công |
| **Vĩnh viễn** (permanent) | JSON hỏng, sai schema, thiếu trường bắt buộc | **DLQ ngay** — thử lại một tỷ lần vẫn hỏng |

→ Retry một lỗi vĩnh viễn chính là cách tạo ra vòng lặp poison pill. Quy tắc thực tế: **retry N lần có backoff → vẫn hỏng thì coi là vĩnh viễn → đẩy DLQ**.

### Trong project của bạn — và lời tự phê đáng nói

Parser bọc `try/except: continue` cho từng ván → đã có **cô lập bản ghi lỗi** ở mức nhẹ nhất, đủ để một ván hỏng (đuôi zstd bị cắt) không giết cả job.

**Nhưng chưa có DLQ** → ván hỏng **biến mất im lặng**, không đếm được bao nhiêu ván bị bỏ.

> **Câu đáng nói khi phỏng vấn:** *"Em có cô lập bản ghi lỗi bằng try/except từng ván nên một ván hỏng không giết cả job, nhưng chưa có DLQ — nghĩa là em không đếm được bao nhiêu ván bị bỏ qua. Lên production thì tối thiểu phải đếm và giữ lại bản ghi lỗi để còn biết mà điều tra."*
→ Tự nhận đúng lỗ hổng, kèm cách sửa. Đây là loại câu khiến người phỏng vấn tin phần còn lại bạn nói.

---

## 4. Exactly-once — và vì sao cái tên này gây hiểu nhầm

### Hiểu nhầm phổ biến nhất

**Exactly-once KHÔNG có nghĩa mỗi message được xử lý đúng một lần về mặt vật lý.** Sau sự cố, message **chắc chắn bị xử lý lại**. Cái được đảm bảo là **kết quả cuối cùng giống như thể nó chỉ được xử lý một lần**.

→ Tên chính xác hơn là **exactly-once semantics** hoặc **effectively-once**. Nói được ý này là dấu hiệu hiểu thật.

### Ba mảnh phải có đủ

| Mảnh | Vai trò | Thiếu thì sao |
|---|---|---|
| **1. Nguồn tua lại được** | Kafka với offset | Không replay được thì không thể khôi phục đúng |
| **2. Ảnh chụp state nhất quán** | Checkpointing | State và offset lệch nhau → tính sai |
| **3. Đầu ra không nhân đôi** | 2PC hoặc sink idempotent | Ghi lặp ra ngoài, dữ liệu bị đúp |

Thiếu **bất kỳ** mảnh nào là mất đảm bảo. Đây là lý do câu trả lời "chỉ cần bật checkpoint" là sai.

### Cách A — Two-phase commit (2PC)

- **Pha 1 (pre-commit):** khi barrier checkpoint đi qua, sink **ghi dữ liệu nhưng chưa commit** transaction.
- **Pha 2 (commit):** khi JobManager xác nhận **mọi** operator đã checkpoint xong, nó báo cho sink → sink mới commit.
- Crash trước khi commit → transaction bị hủy, dữ liệu **không hiện ra ngoài** → replay từ checkpoint an toàn.

**Cái giá ít người nói tới:** đầu ra chỉ hiện ra **tại mốc checkpoint**. Nếu checkpoint mỗi 30 giây thì **độ trễ thực tế của hệ thống là 30 giây**, dù mỗi event xử lý trong 2ms. → *Exactly-once bằng 2PC biến độ trễ của bạn thành chu kỳ checkpoint.* Đây là đánh đổi rất đáng nêu.

### Cách B — Sink idempotent (rẻ hơn nhiều, phổ biến hơn nhiều)

Ghi theo kiểu **ghi lại bao nhiêu lần cũng ra cùng kết quả**: upsert theo khóa nghiệp vụ, hoặc khử trùng theo id.

**At-least-once + sink idempotent ≈ exactly-once về mặt hiệu quả** — mà không tốn chi phí 2PC, không bị phạt độ trễ. **Đa số hệ thống thật chọn cách này.**

### Phân biệt then chốt: ghi đè thì idempotent, cộng dồn thì không

```
balance = 500          → ghi 10 lần vẫn ra 500     ✅ idempotent
balance = balance + 100 → ghi 10 lần ra +1000      ❌ KHÔNG idempotent
```

→ Đây chính là ranh giới quyết định **khi nào buộc phải dùng 2PC thật**: khi mỗi lần ghi là một phép **cộng dồn** không thể suy ra từ khóa.

### Áp vào Home Credit

| Bài toán | Bản chất phép ghi | Cần gì |
|---|---|---|
| Cập nhật **điểm rủi ro** của khách | Ghi đè giá trị mới | Sink idempotent là đủ |
| Ghi **sổ cái giao dịch** / chuyển tiền | Cộng dồn từng bút toán | Cần exactly-once thật (2PC) |

### Trong project của bạn

Sink Redis là `hset` — **ghi đè**, nên **idempotent tự nhiên**. Đó chính là lý do bạn né được exactly-once mà vẫn đúng: replay lại một cửa sổ thì kết quả ghi đè lên vẫn ra giá trị đúng.

> **Câu trả lời gọn:** *"Exactly-once không có nghĩa message chỉ được xử lý một lần — nó vẫn bị xử lý lại sau sự cố, chỉ là kết quả cuối giống như xử lý một lần. Cần đủ ba thứ: nguồn tua lại được, checkpoint để state và offset khớp nhau, và đầu ra không nhân đôi — bằng two-phase commit hoặc sink idempotent. Thực tế đa số dùng at-least-once cộng sink idempotent vì rẻ hơn nhiều; 2PC chỉ cần khi phép ghi là cộng dồn, như sổ cái tài chính."*

---

## Bốn câu chốt nếu chỉ nhớ được vài thứ

1. **Kafka Streams** không có cụm vì nó mượn consumer group của Kafka làm bộ điều phối.
2. **Checkpoint** = barrier trôi theo dữ liệu → ảnh chụp nhất quán mà không dừng job; lưu **cả state lẫn offset**.
3. **Poison pill** nguy hiểm vì làm **kẹt cả luồng**, không phải vì mất một bản ghi. DLQ = bỏ qua + giữ lại + nhìn thấy được.
4. **Exactly-once** = effectively-once. **Ghi đè thì idempotent, cộng dồn thì không** — đó là ranh giới quyết định có cần 2PC hay không.
