---
tags: [knowledge, data-engineer, spark, interview-prep, fundamentals]
status: active
created: 2026-08-12
series: DE Fundamentals
part: 1 / Spark
---

# DE Fundamentals 01 — Spark Internals

> **Vì sao có note này:** phỏng vấn Home Credit vòng manager (2026-08-11) hỏi sâu về Spark
> và distributed system — mảng chưa ôn. Đây là phần bù.
>
> **Cách dùng:** đọc xong mỗi mục thì **nói lớn thành tiếng** một lượt như đang trả lời phỏng vấn.
> Đọc hiểu ≠ nói được. Chỗ thất bại hôm 11/8 là khâu *nói ra dưới áp lực*, không phải khâu *biết*.
>
> Chữ **in đậm** là câu chốt — quên hết thì nhớ mấy câu đó.

---

## Mục lục

1. [[#1 — Spark chia một file cho master và worker thế nào]]
2. [[#2 — Shuffle vì sao nó đắt]]
3. [[#3 — Ba kiểu join và chọn kiểu nào]]
4. [[#4 — Data skew]]
5. [[#5 — Tự kiểm tra]]

---

# 1 — Spark chia một file cho master và worker thế nào

## Nguyên tắc số một

> **Driver không bao giờ đọc dữ liệu. Driver chỉ đọc *metadata* và chia việc.**

Rất nhiều người trả lời sai ở đây — tưởng driver đọc file rồi phát cho worker. Không.
**Dữ liệu đi thẳng từ storage vào executor.**

## Luồng đầy đủ

### ① Driver hỏi metadata

Gọi storage layer lấy danh sách file, kích thước, vị trí block.
Với Parquet thì đọc **footer** — nơi ghi số row group, offset từng row group, thống kê min/max mỗi cột.

### ② Driver tính split (partition)

Mặc định `spark.sql.files.maxPartitionBytes = 128MB`.
File 10GB → khoảng 80 partition. Ranh giới cố gắng khớp block / row-group để không phải đọc chéo node.

### ③ ⚠️ Chỗ chí mạng — file có splittable không

| Định dạng | Splittable | Hệ quả |
|---|---|---|
| Text / CSV / JSON thô | ✅ | Chia theo byte range bình thường |
| Parquet, ORC, Avro | ✅ | Chia theo row group / block |
| bzip2, LZO (có index) | ✅ | Có điểm đồng bộ trong luồng nén |
| **gzip, zstd thường, snappy thô** | ❌ | **Toàn bộ file = 1 partition = 1 core** |

**Lý do:** các codec này nén thành *một luồng liên tục*. Muốn giải mã byte thứ N phải giải mã từ byte 0.
Không có điểm nào nhảy vào giữa được.

> [!important] Đây chính là chuyện đã xảy ra trong project Lichess
> File nén không splittable → Spark cấp đúng 1 task → cả cluster ngồi chơi trong khi 1 core cày
> → **60–75 phút**. Giải nén ra trước rồi mới đọc → chia được thành N partition → chạy song song thật
> → **4 phút**.
>
> Kể được đúng câu chuyện này thì câu hỏi biến thành câu mạnh nhất của buổi phỏng vấn —
> vì nó là **trải nghiệm thật, không phải lý thuyết học thuộc**.

### ④ Ranh giới cắt rơi giữa dòng thì sao

Câu hỏi phụ hay gặp. Quy ước:

- Mỗi task **bỏ qua dòng dở đầu tiên** trong phạm vi của mình
- Và **đọc lấn qua điểm kết thúc** cho tới ký tự xuống dòng tiếp theo

Nhờ vậy mỗi dòng được xử lý **đúng một lần** — không sót, không lặp.

### ⑤ Driver sinh task và xếp lịch

Mỗi partition = 1 task. Khi giao task cho executor, scheduler ưu tiên theo mức độ gần dữ liệu:

`PROCESS_LOCAL` → `NODE_LOCAL` → `RACK_LOCAL` → `ANY`

### ⑥ Executor đọc trực tiếp

Mỗi executor tự lấy đúng byte range của mình từ storage. Với Parquet còn thêm hai tối ưu:

- **Column pruning** — chỉ đọc cột cần
- **Predicate pushdown** — bỏ qua cả row group nếu min/max cho thấy chắc chắn không khớp điều kiện

### ⑦ Stage và shuffle

| Loại phép | Ví dụ | Cần trao đổi dữ liệu | Kết quả |
|---|---|---|---|
| **Narrow** | `map`, `filter`, `select` | ❌ | Gộp chung trong một task, chạy pipeline |
| **Wide** | `groupBy`, `join`, `orderBy` | ✅ | **Shuffle** → ranh giới stage mới |

Shuffle thường là chỗ chậm nhất của cả job.

### ⑧ Kết quả về driver — chỉ khi gọi action

- `count()` → trả về một con số. An toàn.
- **`collect()` → kéo toàn bộ dữ liệu về driver.** Đây là nguyên nhân **OOM driver** kinh điển.

## Câu tóm gọn nếu bị hỏi lại

> "Driver lập kế hoạch dựa trên metadata và chia file thành partition; executor đọc thẳng từ storage
> phần của mình. **Dữ liệu không đi qua driver.** Và chỗ hay hỏng nhất là **file nén không splittable** —
> lúc đó cả file thành một partition duy nhất, cluster to bao nhiêu cũng vô nghĩa."

---

# 2 — Shuffle: vì sao nó đắt

## Vì sao phải shuffle

Để `groupBy("customer_id")` chạy được, **mọi dòng của cùng một customer phải nằm trên cùng một máy**.
Sau khi đọc file thì chúng đang nằm rải rác khắp nơi. **Shuffle là bước sắp xếp lại đó.**

## Chuyện gì xảy ra

**① Phía map.** Mỗi task tính `hash(key) % numPartitions` cho từng dòng, gom theo nhóm,
**ghi xuống đĩa** thành một file dữ liệu + một file index (sort-based shuffle).

**② Phía reduce.** Mỗi reducer kéo phần của nó **từ tất cả** map task.
M map × R reduce = **M×R kết nối mạng**.

**Nên shuffle tốn:** ghi đĩa + serialize + mạng + deserialize.

## Con số cần thuộc

`spark.sql.shuffle.partitions` mặc định **200**. Đây là default sai kinh điển:

| Kích thước dữ liệu | Mỗi partition | Hậu quả |
|---|---|---|
| 10 GB | 50 MB | ✅ Ổn |
| 1 TB | 5 GB | ❌ Spill ra đĩa, chậm khủng khiếp |
| 100 MB | 500 KB | ❌ Chi phí lập lịch > chi phí tính toán |

> **Quy tắc ngón tay cái: nhắm mỗi shuffle partition ~128–200 MB.**

---

# 3 — Ba kiểu join và chọn kiểu nào

Câu hỏi Spark hay gặp thứ nhì sau shuffle.

| Kiểu join | Dùng khi | Có shuffle | Ghi chú |
|---|---|---|---|
| **Broadcast hash join** | Một bên nhỏ (mặc định < 10 MB) | ❌ Không | Nhanh nhất. Bên nhỏ gửi tới mọi executor |
| **Shuffle sort-merge join** | Hai bên đều lớn | ✅ Cả hai bên | Mặc định cho large × large |
| **Shuffle hash join** | Một bên vừa, không đủ nhỏ để broadcast | ✅ Cả hai bên | Dựng hash table trên bên nhỏ hơn ở mỗi partition |

## Broadcast hash join hoạt động ra sao

1. Driver gom bảng nhỏ về (`collect`)
2. Gửi bản sao tới **từng executor**
3. Mỗi executor dựng hash table trong RAM
4. Quét bảng lớn **tại chỗ**, tra hash table

**Bảng lớn không cần di chuyển** — đó là lý do nó nhanh.

> [!warning] Bẫy
> Broadcast một bảng quá lớn → **driver OOM** hoặc executor OOM.
> Ngưỡng `spark.sql.autoBroadcastJoinThreshold` tồn tại chính vì vậy.

## Sort-merge join hoạt động ra sao

1. Shuffle cả hai bảng theo **cùng một key**
2. Mỗi partition **sort** lại
3. Duyệt song song hai luồng đã sort và ghép

Sort là lý do nó tốn. Đổi lại: **không cần nạp bên nào vào RAM toàn bộ** → dữ liệu lớn cỡ nào cũng chạy được.

---

# 4 — Data skew

Bệnh phổ biến nhất trong thực tế.

## Triệu chứng

Câu hỏi kiểu *"job chạy chậm, chẩn đoán đi"*:

> 199 task xong trong 30 giây. **1 task chạy 40 phút.** Cluster gần như rảnh hoàn toàn.

Nhìn ở đâu: **Spark UI → tab Stages → phân bố thời gian task.** Nếu p99 lệch hẳn median thì là skew.

## Nguyên nhân — ba thủ phạm quen mặt

- **`NULL` key** — mọi dòng null dồn vào cùng một partition
- **Giá trị mặc định** — `customer_id = 'UNKNOWN'`, `city = 'N/A'`
- **Khách hàng khổng lồ thật** — một seller chiếm 40% giao dịch

## Cách chữa, theo thứ tự nên thử

### ① Lọc `NULL` ra xử lý riêng

Rẻ nhất, và thường giải quyết xong vấn đề. **Dòng null vốn không join được với gì cả.**

### ② Broadcast nếu bên kia đủ nhỏ

**Không shuffle thì không có skew.**

### ③ Salting — cần biết tên và giải thích được

```python
# Bên lệch: thêm hậu tố ngẫu nhiên vào key
big = big.withColumn("salted_key",
        F.concat(F.col("customer_id"), F.lit("_"),
                 (F.rand() * 10).cast("int")))

# Bên kia: nhân bản mỗi dòng thành 10 bản, một bản cho mỗi salt
small = small.withColumn("salt",
            F.explode(F.array([F.lit(i) for i in range(10)]))) \
         .withColumn("salted_key",
            F.concat(F.col("customer_id"), F.lit("_"), F.col("salt")))

joined = big.join(small, "salted_key")
```

**Ý tưởng: một key nóng bị bẻ thành 10 key → chia được cho 10 task.**

Cái giá: bên nhỏ phồng lên 10 lần → chỉ dùng khi bên nhỏ thật sự nhỏ.

### ④ AQE làm tự động

Adaptive Query Execution (Spark 3+, bật sẵn). Xem thống kê **lúc chạy** rồi:

- Gộp các shuffle partition quá nhỏ lại
- **Tách partition bị lệch** thành nhiều task
- Chuyển sort-merge sang broadcast nếu phát hiện một bên hoá ra nhỏ

> Câu ăn điểm: **"AQE xử lý được nhiều trường hợp, nhưng nó phản ứng *sau khi* đã shuffle — chữa gốc vẫn tốt hơn."**

---

# 5 — Tự kiểm tra

**Nói thành tiếng. Không viết, không đọc thầm.** Mỗi câu nói liền mạch 60–90 giây.

**①** Từ lúc gọi `.groupBy().count()` tới lúc có kết quả, Spark làm những gì?
*Ép mình phải nhắc tới: DAG · stage · shuffle · task · action.*

**②** Job join hai bảng chạy 2 tiếng. Chẩn đoán từ đâu, theo thứ tự nào?
*Gợi ý khung: nhìn Spark UI → phân bố thời gian task → skew hay không → kiểu join có đúng không → số shuffle partition.*

**③** Vì sao broadcast join nhanh hơn sort-merge, và khi nào **không** được dùng nó?

> [!tip] Ấp úng là tín hiệu thật
> Không phải "chưa thuộc bài", mà là **chưa đủ đường dẫn để lôi kiến thức ra dưới áp lực**.
> Quay lại đúng mục đó và nói lại.

---

## Còn thiếu trong Module 1 — để buổi sau

- Memory model (unified memory: execution vs storage), spill
- `cache()` / `persist()` — và khi nào nó **vô ích**
- Catalyst optimizer: parsed → analyzed → optimized logical → physical → codegen
- Bộ triệu chứng → nguyên nhân cho OOM (driver vs executor)

## Liên quan

- [[DE Fundamentals 02 - SQL nâng cao]] *(chưa tạo)*
- [[DE Fundamentals 03 - Distributed Systems]] *(chưa tạo)*
- Project Lichess Feature Store — nguồn của câu chuyện zstd
