---
tags: [knowledge, data-engineer, spark, interview-prep, fundamentals]
status: active
created: 2026-08-12
updated: 2026-08-13
series: Job Fundamentals
part: 1 / Spark
---

# Job Fundamentals 01 — Apache Spark

> **Tài liệu tham chiếu đầy đủ, không phải bản vá cho một buổi phỏng vấn cụ thể.**
> Mục tiêu: hiểu Spark đủ để trả lời được câu **chưa gặp bao giờ**, không chỉ câu đã gặp.
>
> **Cách dùng:** Phần I–III đọc một lượt để có khung. Phần IV–V là ruột, đọc kỹ.
> Phần VII–VIII là thứ phân biệt người dùng Spark với người hiểu Spark.
> Mỗi phần đọc xong thì **nói lớn thành tiếng** một lượt.

---

## Mục lục

**I.** [[#I — Bối cảnh Spark ra đời để giải quyết cái gì]]
**II.** [[#II — Kiến trúc và thành phần]]
**III.** [[#III — Mô hình lập trình]]
**IV.** [[#IV — Bộ máy thực thi]]
**V.** [[#V — Bộ nhớ và chịu lỗi]]
**VI.** [[#VI — Hệ sinh thái module]]
**VII.** [[#VII — Dùng khi nào và không dùng khi nào]]
**VIII.** [[#VIII — Ưu nhược điểm và bối cảnh cạnh tranh]]
**IX.** [[#IX — Vận hành và tuning thực tế]]
**X.** [[#X — Khung trả lời câu hỏi chưa gặp]]
**XI.** [[#XI — Tự kiểm tra]]

---
---

# I — Bối cảnh: Spark ra đời để giải quyết cái gì

## 1.1 — Thế giới trước Spark

**2003–2004, Google công bố hai bài báo** làm nền cho toàn bộ ngành: **GFS** (hệ tệp phân tán) và **MapReduce** (mô hình tính toán phân tán). Ý tưởng chung: **thay vì mua một siêu máy tính, ghép hàng nghìn máy rẻ lại và chấp nhận chúng sẽ hỏng liên tục.**

**2006, Hadoop ra đời** (Doug Cutting, tách từ dự án Nutch, được Yahoo hậu thuẫn) — bản mã nguồn mở của hai ý tưởng đó. Lần đầu tiên xử lý petabyte trở nên khả thi với công ty bình thường.

## 1.2 — Chỗ MapReduce bế tắc

MapReduce có một ràng buộc thiết kế cứng: **giữa mỗi giai đoạn Map và Reduce, dữ liệu phải ghi xuống đĩa.**

Đó là lựa chọn có lý — ghi xuống đĩa nghĩa là máy chết thì đọc lại được, không phải tính lại từ đầu. Nhưng nó sinh ra ba vấn đề không chữa được:

**① Thuật toán lặp thì thảm hoạ.** Machine learning, thuật toán đồ thị (PageRank), tối ưu — tất cả đều lặp đi lặp lại trên **cùng một tập dữ liệu**. Với MapReduce, **mỗi vòng lặp phải đọc lại toàn bộ dữ liệu từ đĩa**. Chạy 100 vòng = đọc 100 lần cùng một thứ.

**② Truy vấn tương tác là không thể.** Nhà phân tích muốn hỏi một câu, xem kết quả, rồi hỏi câu tiếp — mỗi câu mất vài chục phút thì không còn là tương tác nữa.

**③ Mô hình lập trình quá thô.** Mọi thứ phải bẻ về `map` và `reduce`. Một phép join đơn giản trở thành nhiều chục dòng code khó đọc, và phải tự tay tối ưu.

## 1.3 — Ý tưởng cốt lõi của Spark

**2009, phòng thí nghiệm AMPLab tại UC Berkeley**, Matei Zaharia bắt đầu dự án Spark. Mã nguồn mở năm 2010, chuyển cho Apache năm 2013, thành dự án cấp cao nhất **tháng 2/2014**.

Bài báo nền tảng: ***Resilient Distributed Datasets: A Fault-Tolerant Abstraction for In-Memory Cluster Computing*** (NSDI 2012).

Câu hỏi mà bài báo giải:

> **Làm sao giữ dữ liệu trong RAM giữa các bước tính toán, mà vẫn chịu được lỗi
> — nhưng không phải trả giá bằng việc nhân bản dữ liệu?**

Nhân bản dữ liệu trong RAM thì quá đắt. **Lời giải: đừng lưu dữ liệu, lưu *cách tạo ra* dữ liệu.**

Đó là **lineage** (phả hệ). Mỗi RDD ghi nhớ nó được sinh ra từ RDD nào qua phép biến đổi nào. Một partition mất → **tính lại đúng partition đó** từ cha của nó. Không cần bản sao nào cả.

> **Đây là đóng góp trí tuệ trung tâm của Spark.** Mọi thứ khác — API đẹp, tốc độ, hệ sinh thái —
> đều là hệ quả. Bị hỏi *"Spark khác Hadoop chỗ nào"* mà chỉ trả lời "Spark chạy trên RAM nên nhanh hơn"
> là trả lời ở mức bề mặt. **Câu đúng là: Spark chịu lỗi bằng lineage thay vì bằng nhân bản,
> nhờ đó mới dám giữ dữ liệu trong RAM.**

## 1.4 — Con số làm nên tên tuổi

**2014, Daytona GraySort** — cuộc thi sắp xếp dữ liệu quy mô lớn:

| | Thời gian | Số máy |
|---|---|---|
| Kỷ lục cũ (Hadoop MapReduce) | 72 phút | 2100 |
| **Spark** | **23 phút** | **206** |

Nhanh hơn ~3 lần với **1/10 số máy**. Và đáng chú ý: bài toán sắp xếp là **thuần I/O đĩa**, không phải bài toán lặp trong RAM — nghĩa là Spark thắng cả ở sân nhà của MapReduce.

## 1.5 — Dòng thời gian tiến hoá

| Năm | Cột mốc | Ý nghĩa |
|---|---|---|
| 2009 | Khởi động tại AMPLab | |
| 2012 | Bài báo RDD | Nền tảng lý thuyết |
| 2014 | Apache top-level · Spark 1.0 · Databricks thành lập | Chính thức trưởng thành |
| 2015 | **DataFrame** (1.3) | Có schema → **Catalyst tối ưu được** |
| 2016 | **Spark 2.0** — hợp nhất Dataset/DataFrame, **Tungsten**, Structured Streaming | Bước nhảy lớn nhất về hiệu năng |
| 2018 | Spark 2.3 — hỗ trợ **Kubernetes** | Thoát khỏi ràng buộc YARN |
| 2020 | **Spark 3.0** — **AQE**, dynamic partition pruning | Tối ưu dựa trên thống kê lúc chạy |
| 2023 | Spark 3.4 — **Spark Connect** | Tách client khỏi cluster, kiến trúc kiểu client mỏng |
| 2025 | Spark 4.0 | ANSI SQL mặc định, kiểu VARIANT, Python data source API |

> **Mạch xuyên suốt: từ "API cho lập trình viên tự tối ưu" → "khai báo ý định, để máy tối ưu".**
> RDD bắt bạn tự nghĩ cách. DataFrame + Catalyst + AQE thì bạn mô tả *muốn gì*, hệ thống lo *làm thế nào*.
> Đây là cùng một mạch tiến hoá mà SQL đã đi qua 30 năm trước.

---
---

# II — Kiến trúc và thành phần

## 2.1 — Ba khối chính

```
┌─────────────────────────────────────────────┐
│                  DRIVER                     │
│  • Chạy hàm main()                          │
│  • Dựng DAG, chia stage, sinh task          │
│  • Giữ SparkContext / SparkSession          │
│  • KHÔNG đọc dữ liệu                        │
└──────────────────┬──────────────────────────┘
                   │ xin tài nguyên
                   ▼
┌─────────────────────────────────────────────┐
│            CLUSTER MANAGER                  │
│  Standalone · YARN · Kubernetes · Mesos(cũ) │
│  • Cấp phát máy và tài nguyên               │
└──────────────────┬──────────────────────────┘
                   │ khởi tạo
                   ▼
┌─────────────────────────────────────────────┐
│              EXECUTOR × N                   │
│  • Chạy task                                │
│  • Đọc dữ liệu TRỰC TIẾP từ storage         │
│  • Giữ dữ liệu cache trong RAM              │
│  • Báo cáo kết quả về driver                │
└─────────────────────────────────────────────┘
```

### Driver

Bộ não. Giữ `SparkSession`, dựng kế hoạch, chia việc, theo dõi tiến độ.

**Driver chết = cả ứng dụng chết.** Và driver là điểm nghẽn khi:
- Gọi `collect()` trên dữ liệu lớn → **OOM driver**
- Broadcast một bảng quá to
- Số task quá lớn (hàng trăm nghìn) → riêng việc lập lịch đã tắc

### Executor

Tiến trình JVM chạy trên worker node. Mỗi executor có:
- **Số core** (`spark.executor.cores`) → số task chạy song song trong cùng executor
- **Bộ nhớ** (`spark.executor.memory`)
- **Block manager** — quản lý dữ liệu cache và file shuffle

**Executor sống suốt vòng đời ứng dụng** (trừ khi bật dynamic allocation). Đây là khác biệt lớn so với MapReduce, nơi mỗi task là một JVM mới → chi phí khởi động khổng lồ.

### Cluster manager

| Loại | Đặc điểm | Dùng khi |
|---|---|---|
| **Standalone** | Có sẵn trong Spark, đơn giản | Cluster chỉ chạy Spark |
| **YARN** | Chuẩn của hệ sinh thái Hadoop | Đang có sẵn Hadoop |
| **Kubernetes** | Đóng gói container, co giãn linh hoạt | **Hạ tầng hiện đại — hướng đi chính** |
| **Mesos** | Đã ngừng phát triển | Hệ thống cũ |

## 2.2 — Client mode vs Cluster mode

| | Driver chạy ở đâu | Dùng khi |
|---|---|---|
| **Client** | Máy nộp job (laptop, edge node) | Phát triển, notebook, cần xem output trực tiếp |
| **Cluster** | Bên trong cluster | **Production** — tắt máy cá nhân job vẫn chạy |

> Câu hỏi phụ hay gặp: *"Sao chạy notebook thì được mà submit lên production thì OOM driver?"*
> — Vì client mode driver dùng RAM máy cá nhân (thường lớn), cluster mode dùng cấu hình đã đặt (thường nhỏ hơn).

## 2.3 — Tầng module

```
┌──────────┬──────────────┬────────┬─────────┐
│ Spark SQL│  Structured  │ MLlib  │ GraphX  │
│ DataFrame│  Streaming   │        │         │
├──────────┴──────────────┴────────┴─────────┤
│              SPARK CORE                     │
│        RDD · lập lịch · shuffle             │
├─────────────────────────────────────────────┤
│  Standalone │ YARN │ Kubernetes │ Mesos     │
└─────────────────────────────────────────────┘
```

**Điểm bán hàng lớn nhất của Spark: một engine, nhiều loại tải.** Batch, SQL, streaming, ML dùng chung một bộ máy thực thi và một API. Trước Spark phải ghép Hadoop + Hive + Storm + Mahout, mỗi thứ một mô hình.

---
---

# III — Mô hình lập trình

## 3.1 — Ba tầng trừu tượng

| | RDD | DataFrame | Dataset |
|---|---|---|---|
| Ra đời | 2011 | 2015 | 2016 |
| Có schema | ❌ | ✅ | ✅ |
| Catalyst tối ưu | ❌ | ✅ | ✅ |
| Kiểm tra kiểu lúc biên dịch | ✅ | ❌ | ✅ |
| Ngôn ngữ | Mọi ngôn ngữ | Mọi ngôn ngữ | **Chỉ Scala/Java** |
| Khi nào dùng | Dữ liệu phi cấu trúc, cần điều khiển tay | **Mặc định** | Scala, cần an toàn kiểu |

### Vì sao DataFrame nhanh hơn RDD

RDD với Spark chỉ là **một đống object không rõ bên trong là gì**. Không biết cấu trúc → không tối ưu được gì cả, chỉ chạy đúng thứ tự bạn viết.

DataFrame **có schema** → Spark biết cột nào kiểu gì → **Catalyst có thể viết lại truy vấn**: đẩy điều kiện lọc xuống sát nguồn, bỏ cột không dùng, đổi thứ tự join, gộp phép toán.

> **Với PySpark, khác biệt còn lớn hơn nhiều.** RDD trong Python phải serialize dữ liệu qua lại
> giữa JVM và tiến trình Python cho **từng dòng**. DataFrame thì mọi phép toán chạy trong JVM,
> Python chỉ gửi *mô tả* việc cần làm.
>
> **Đây là lý do quy tắc "đừng dùng RDD trong PySpark" tồn tại** — không phải vì phong cách,
> mà vì chênh lệch hiệu năng có thể tới hàng chục lần.

## 3.2 — Lazy evaluation

Spark **không chạy gì cả** cho tới khi gặp một **action**.

| Loại | Ví dụ | Hành vi |
|---|---|---|
| **Transformation** | `select`, `filter`, `join`, `groupBy`, `map` | Chỉ **ghi thêm vào kế hoạch**, không chạy |
| **Action** | `count`, `collect`, `show`, `write`, `take` | **Kích hoạt chạy thật** |

**Vì sao thiết kế như vậy:** biết trước toàn bộ chuỗi phép toán thì mới tối ưu được cả chuỗi. Nếu chạy ngay từng lệnh thì không còn cơ hội gộp hay đổi thứ tự.

```python
df = spark.read.parquet("...")     # chưa đọc gì
df2 = df.filter(col("x") > 10)     # chưa chạy
df3 = df2.select("a", "b")         # chưa chạy
df3.count()                        # ← BÂY GIỜ mới chạy
```

Và Spark sẽ **đẩy `filter` xuống tận lúc đọc file**, **chỉ đọc cột `a`, `b`** — dù bạn viết theo thứ tự ngược lại.

> ⚠️ **Hệ quả khó chịu:** lỗi không xuất hiện ở dòng gây lỗi, mà ở dòng gọi action.
> Đây là nguyên nhân chính khiến debug Spark khó.

## 3.3 — Lineage và DAG

Mỗi DataFrame nhớ **nó sinh ra từ đâu**. Chuỗi đó tạo thành một **DAG** (đồ thị có hướng không chu trình).

Dùng để:
- **Tối ưu** — nhìn toàn cảnh trước khi chạy
- **Chịu lỗi** — mất partition thì tính lại từ cha
- **Gỡ lỗi** — `df.explain()` in ra kế hoạch

## 3.4 — Narrow vs Wide — ranh giới quan trọng nhất

| | **Narrow** | **Wide** |
|---|---|---|
| Nghĩa | Mỗi partition cha đóng góp cho **đúng một** partition con | Partition con cần dữ liệu từ **nhiều** partition cha |
| Ví dụ | `map`, `filter`, `select`, `union` | `groupBy`, `join`, `distinct`, `orderBy`, `repartition` |
| Cần shuffle | ❌ | ✅ |
| Chi phí | Rẻ, gộp chung một task | **Đắt nhất trong Spark** |
| Mất partition thì | Tính lại 1 partition cha | **Có thể phải tính lại nhiều partition** |

> **Đây là khái niệm sinh ra mọi thứ khác.** Stage được chia tại ranh giới wide.
> Skew chỉ xảy ra ở wide. Tối ưu Spark = **giảm số lần shuffle, và làm mỗi lần shuffle rẻ đi**.

---
---

# IV — Bộ máy thực thi

## 4.1 — Từ code tới task

```
Code (DataFrame / SQL)
   ↓  Catalyst phân tích + tối ưu
Kế hoạch logic đã tối ưu
   ↓  lập kế hoạch vật lý + sinh mã
DAG các RDD
   ↓  cắt tại ranh giới shuffle
STAGE
   ↓  mỗi partition một task
TASK  →  giao cho executor
```

**Thuật ngữ phải phân biệt được:**

| Từ | Nghĩa |
|---|---|
| **Job** | Một action sinh ra một job |
| **Stage** | Đoạn giữa hai lần shuffle |
| **Task** | Một đơn vị việc trên **một partition**. Task = đơn vị nhỏ nhất |
| **Partition** | Một mảnh dữ liệu |

**Số task của một stage = số partition.** Quan hệ này là chìa khoá để hiểu song song hoá.

## 4.2 — Đọc file: driver chia việc thế nào

### Nguyên tắc số một

> **Driver không bao giờ đọc dữ liệu. Driver chỉ đọc *metadata* và chia việc.**

Nhiều người trả lời sai chỗ này — tưởng driver đọc file rồi phát cho worker. Không. **Dữ liệu đi thẳng từ storage vào executor.**

### ① Driver hỏi metadata

Lấy danh sách file, kích thước, vị trí block. Với Parquet thì đọc **footer** — nơi ghi số row group, offset từng row group, thống kê min/max mỗi cột.

### ② Driver tính split

`spark.sql.files.maxPartitionBytes` mặc định **128 MB**. File 10 GB → khoảng 80 partition.

### ③ ⚠️ Chỗ chí mạng: file có splittable không

| Định dạng | Splittable | Hệ quả |
|---|---|---|
| Text / CSV / JSON thô | ✅ | Chia theo byte range |
| Parquet, ORC, Avro | ✅ | Chia theo row group / block |
| bzip2, LZO (có index) | ✅ | Có điểm đồng bộ trong luồng nén |
| **gzip, zstd thường, snappy thô** | ❌ | **Cả file = 1 partition = 1 core** |

**Lý do:** các codec này nén thành *một luồng liên tục*. Muốn giải mã byte thứ N phải giải mã từ byte 0.

> [!important] Chuyện đã xảy ra trong project Lichess
> File nén không splittable → Spark cấp đúng 1 task → cả cluster ngồi chơi trong khi 1 core cày
> → **60–75 phút**. Giải nén trước rồi mới đọc → chia thành N partition → **4 phút**.
>
> Kể được chuyện này là **trải nghiệm thật**, khác hẳn lý thuyết học thuộc.

### ④ Ranh giới cắt rơi giữa dòng

Quy ước: mỗi task **bỏ qua dòng dở đầu tiên**, và **đọc lấn qua điểm kết thúc** tới ký tự xuống dòng tiếp theo. Nhờ vậy mỗi dòng được xử lý **đúng một lần**.

### ⑤ Xếp lịch theo data locality

`PROCESS_LOCAL` → `NODE_LOCAL` → `RACK_LOCAL` → `ANY`

> Với object storage (S3/GCS), **locality gần như không còn ý nghĩa** — mọi thứ đều qua mạng.
> Đây là đánh đổi khi tách storage khỏi compute.

### ⑥ Executor đọc trực tiếp

Với Parquet có thêm: **column pruning** (chỉ đọc cột cần) và **predicate pushdown** (bỏ qua cả row group nếu min/max cho thấy không khớp).

## 4.3 — Shuffle: chỗ đắt nhất

### Vì sao cần

Để `groupBy("customer_id")` chạy được, **mọi dòng của cùng một customer phải nằm trên cùng một máy**.

### Diễn biến

**① Phía map.** Mỗi task tính `hash(key) % numPartitions`, gom theo nhóm, **ghi xuống đĩa** thành một file dữ liệu + một file index.

**② Phía reduce.** Mỗi reducer kéo phần của nó **từ tất cả** map task → **M×R kết nối mạng**.

**Chi phí:** ghi đĩa + serialize + mạng + deserialize. Gần như luôn là chỗ chậm nhất.

### Con số phải thuộc

`spark.sql.shuffle.partitions` mặc định **200** — default sai kinh điển:

| Dữ liệu | Mỗi partition | Hậu quả |
|---|---|---|
| 10 GB | 50 MB | ✅ Ổn |
| 1 TB | 5 GB | ❌ Spill ra đĩa, rất chậm |
| 100 MB | 500 KB | ❌ Chi phí lập lịch > chi phí tính toán |

> **Quy tắc: nhắm mỗi shuffle partition ~128–200 MB.** (AQE bật thì tự gộp partition nhỏ, đỡ được vế dưới.)

## 4.4 — Ba kiểu join

| Kiểu | Dùng khi | Shuffle | Ghi chú |
|---|---|---|---|
| **Broadcast hash join** | Một bên nhỏ (mặc định < 10 MB) | ❌ | Nhanh nhất |
| **Shuffle sort-merge join** | Hai bên đều lớn | ✅ Cả hai | Mặc định cho large × large |
| **Shuffle hash join** | Một bên vừa | ✅ Cả hai | Dựng hash table trên bên nhỏ hơn mỗi partition |

**Broadcast:** driver gom bảng nhỏ, gửi tới **từng executor**, mỗi executor dựng hash table, quét bảng lớn tại chỗ. **Bảng lớn không di chuyển** → nhanh.
⚠️ Broadcast bảng quá lớn → **OOM driver hoặc executor**.

**Sort-merge:** shuffle cả hai theo cùng key → sort mỗi partition → duyệt song song và ghép.
Sort là chỗ tốn, đổi lại **không cần nạp bên nào vào RAM toàn bộ** → dữ liệu lớn cỡ nào cũng chạy.

## 4.5 — Data skew

**Triệu chứng:** 199 task xong trong 30 giây, **1 task chạy 40 phút**. Cluster rảnh.
Nhìn ở: **Spark UI → Stages → phân bố thời gian task**. p99 lệch hẳn median = skew.

**Ba thủ phạm:** key `NULL` · giá trị mặc định (`'UNKNOWN'`, `'N/A'`) · khách hàng khổng lồ thật.

**Cách chữa theo thứ tự:**

**① Lọc `NULL` ra xử lý riêng** — rẻ nhất, thường xong luôn. Dòng null vốn không join được với gì.

**② Broadcast nếu bên kia đủ nhỏ** — không shuffle thì không có skew.

**③ Salting:**

```python
# Bên lệch: thêm hậu tố ngẫu nhiên
big = big.withColumn("salted_key",
        F.concat(F.col("customer_id"), F.lit("_"),
                 (F.rand() * 10).cast("int")))

# Bên kia: nhân bản mỗi dòng thành 10 bản
small = small.withColumn("salt",
            F.explode(F.array([F.lit(i) for i in range(10)]))) \
         .withColumn("salted_key",
            F.concat(F.col("customer_id"), F.lit("_"), F.col("salt")))

joined = big.join(small, "salted_key")
```

**Một key nóng bẻ thành 10 key → chia cho 10 task.** Giá: bên nhỏ phồng 10 lần.

**④ AQE tự xử lý** — xem mục 4.7.

## 4.6 — Catalyst optimizer

Bộ tối ưu truy vấn của Spark. Năm bước:

```
SQL / DataFrame API
   ↓
① Unresolved Logical Plan     — cú pháp đúng, chưa biết cột có thật không
   ↓  đối chiếu catalog
② Logical Plan                 — đã phân giải tên bảng, tên cột, kiểu
   ↓  áp luật tối ưu
③ Optimized Logical Plan
   ↓  sinh nhiều phương án
④ Physical Plans → mô hình chi phí chọn một
   ↓  whole-stage codegen
⑤ Java bytecode → RDD
```

**Các luật tối ưu quan trọng ở bước ③:**

| Luật | Làm gì |
|---|---|
| **Predicate pushdown** | Đẩy `WHERE` xuống sát nguồn đọc — lọc trước khi đưa vào join |
| **Projection pruning** | Bỏ cột không dùng — với Parquet nghĩa là **không đọc từ đĩa luôn** |
| **Constant folding** | `WHERE x > 2 + 3` → `WHERE x > 5` |
| **Join reordering** | Đổi thứ tự join dựa trên thống kê |
| **Dynamic partition pruning** (3.0+) | Dùng kết quả bảng nhỏ để bỏ qua partition của bảng lớn lúc chạy |

> **Đây là lý do DataFrame nhanh hơn RDD**, và là lý do *"viết SQL cho gọn"* thường cũng nhanh hơn
> code tay — bộ tối ưu nhìn được toàn cảnh, còn bạn thì không.

## 4.7 — Tungsten và AQE

### Tungsten (Spark 1.6 → 2.x)

Dự án tối ưu tầng thực thi, ba mũi:

**① Quản lý bộ nhớ nhị phân.** Dữ liệu lưu ở định dạng nhị phân gọn (`UnsafeRow`) thay vì object Java. Một `String` trong JVM tốn ~40+ byte overhead; ở dạng nhị phân thì gần bằng đúng độ dài thật. **Giảm bộ nhớ và giảm áp lực GC.**

**② Whole-stage code generation.** Thay vì mỗi phép toán là một hàm gọi nhau qua interface (mỗi dòng dữ liệu tốn vài lần gọi hàm ảo), Spark **sinh ra một hàm Java duy nhất** gộp cả stage. Giảm mạnh chi phí gọi hàm, và tận dụng được cache CPU.

**③ Đọc theo vector.** Parquet reader đọc theo lô cột thay vì từng dòng.

### AQE — Adaptive Query Execution (Spark 3.0+, bật sẵn)

Catalyst tối ưu **trước khi chạy**, dựa trên thống kê có thể sai. AQE tối ưu lại **trong lúc chạy**, dựa trên số liệu thật sau mỗi shuffle:

| Làm gì | Ý nghĩa |
|---|---|
| **Gộp shuffle partition nhỏ** | 200 partition mà dữ liệu bé → tự gộp lại, đỡ chi phí lập lịch |
| **Đổi sort-merge sang broadcast** | Sau khi lọc, một bên hoá ra nhỏ → chuyển kiểu join |
| **Tách partition bị lệch** | Tự chia nhỏ partition skew thành nhiều task |

> **Câu ăn điểm:** *"AQE xử lý được nhiều trường hợp, nhưng nó phản ứng **sau khi** đã shuffle —
> chữa gốc vẫn tốt hơn."*

---
---

# V — Bộ nhớ và chịu lỗi

## 5.1 — Mô hình bộ nhớ

Bộ nhớ mỗi executor (heap JVM) chia như sau:

```
┌──────────────────────────────────────┐
│ Reserved (~300 MB)                   │  Spark tự giữ
├──────────────────────────────────────┤
│ Unified Memory                       │  spark.memory.fraction = 0.6
│ ┌──────────────┬───────────────────┐ │
│ │  Execution   │     Storage       │ │  storageFraction = 0.5
│ │  shuffle,    │     cache,        │ │
│ │  sort, join, │     broadcast     │ │
│ │  aggregation │                   │ │
│ └──────────────┴───────────────────┘ │
├──────────────────────────────────────┤
│ User Memory                          │  ~40% — cấu trúc dữ liệu của bạn, UDF
└──────────────────────────────────────┘
```

**Luật quan trọng nhất — quan hệ bất đối xứng:**

> **Execution có thể chiếm chỗ của Storage (đuổi cache đi).**
> **Storage KHÔNG thể chiếm chỗ của Execution.**

Lý do: cache mất thì tính lại được. Execution thiếu bộ nhớ thì **job chết**.

Đây là "unified memory" (từ Spark 1.6). Trước đó hai vùng cố định, và chuyện *"cache chiếm hết chỗ khiến join không chạy nổi"* là bệnh kinh niên.

## 5.2 — Spill

Khi execution memory không đủ, Spark **ghi tạm ra đĩa** thay vì chết. Đây là hành vi cứu mạng nhưng rất chậm.

**Nhìn spill ở Spark UI:** cột *Spill (Memory)* và *Spill (Disk)* trong chi tiết stage.

**Có spill nghĩa là:** partition quá to → tăng số partition, hoặc tăng bộ nhớ executor, hoặc giảm dữ liệu đi vào (lọc sớm hơn).

## 5.3 — Cache và persist

```python
df.cache()                                    # = MEMORY_AND_DISK cho DataFrame
df.persist(StorageLevel.MEMORY_ONLY)
df.unpersist()                                # nhớ giải phóng
```

| Mức | Đặc điểm |
|---|---|
| `MEMORY_ONLY` | Nhanh nhất; không đủ chỗ thì **tính lại** phần thiếu |
| `MEMORY_AND_DISK` | Không đủ RAM thì ghi đĩa. **Mặc định của `df.cache()`** |
| `MEMORY_ONLY_SER` | Nén thành mảng byte — tốn CPU, tiết kiệm RAM |
| `DISK_ONLY` | Chỉ đĩa |
| `*_2` | Nhân đôi bản sao trên node khác |

> ⚠️ **Bẫy nhỏ:** `RDD.cache()` là `MEMORY_ONLY`, còn `DataFrame.cache()` là `MEMORY_AND_DISK`. Khác nhau.

### Khi nào cache là VÔ ÍCH — hoặc có hại

**① Dữ liệu chỉ dùng một lần.** Cache rồi dùng một lần = tốn công lưu, không thu lại được gì.

**② Tính lại rẻ hơn giữ.** Nếu chuỗi phép toán ngắn và dữ liệu to, tính lại có khi rẻ hơn là chiếm RAM.

**③ Cache đẩy execution memory xuống** → sinh spill → **chậm hơn là không cache**. Đây là trường hợp cache thực sự gây hại.

**④ Cache rồi lọc.** `df.cache()` rồi `df.filter(...)` → đã lưu cả bảng trong khi chỉ cần một phần. Lọc trước rồi mới cache.

> **Quy tắc: chỉ cache khi một DataFrame được dùng lại từ 2 action trở lên, và đã lọc gọn.**

## 5.4 — Chịu lỗi

### Batch: tính lại theo lineage

Executor chết → driver biết partition nào mất → **tính lại từ cha theo lineage**. Không cần nhân bản.

**Điều kiện để cơ chế này đúng: phép biến đổi phải tất định.** Dùng `rand()` không đặt seed, hoặc phụ thuộc thời gian hệ thống, thì tính lại ra kết quả khác → sai lặng lẽ.

**Task thất bại được thử lại** `spark.task.maxFailures` lần (mặc định 4) trước khi giết cả stage.

### Checkpoint

Với chuỗi lineage rất dài (thường do vòng lặp), lineage tự nó trở thành gánh nặng — mất một partition phải tính lại hàng trăm bước.

`df.checkpoint()` **ghi dữ liệu xuống storage bền và cắt đứt lineage**. Đổi chi phí ghi lấy việc không phải tính lại dài.

**Phân biệt với cache:** cache giữ trong RAM và **vẫn giữ lineage**; checkpoint ghi bền và **xoá lineage**.

### Streaming: checkpoint bắt buộc

Structured Streaming ghi vào thư mục checkpoint: **offset đã đọc tới đâu** + **state của các phép có trạng thái**. Đây là thứ cho phép khởi động lại mà không mất dữ liệu và không xử lý lại từ đầu.

## 5.5 — Chẩn đoán OOM

| Hiện tượng | Nguyên nhân thường gặp | Chữa |
|---|---|---|
| **OOM ở driver** | `collect()` dữ liệu lớn · broadcast bảng to · quá nhiều task | Đừng `collect`, dùng `write` · hạ ngưỡng broadcast · giảm số partition |
| **OOM ở executor** | Partition quá to · skew · UDF giữ dữ liệu trong RAM | Tăng số partition · chữa skew · viết lại UDF |
| **GC chiếm phần lớn thời gian** | Quá nhiều object nhỏ trong JVM | Dùng DataFrame thay RDD · tăng RAM · chỉnh GC |
| **Spill rất nhiều** | Execution memory thiếu | Tăng partition · giảm cache · lọc sớm |

> **Khung trả lời khi bị hỏi "job OOM thì làm sao":**
> *"Trước hết xác định OOM ở driver hay executor — hai nguyên nhân hoàn toàn khác nhau.
> Driver thì thường là `collect` hoặc broadcast. Executor thì thường là partition quá to hoặc skew.
> Rồi mới mở Spark UI xem phân bố thời gian và dung lượng task."*
>
> **Nói được bước phân loại trước khi nói giải pháp là dấu hiệu người đã làm thật.**

---
---

# VI — Hệ sinh thái module

## 6.1 — Spark SQL

Không chỉ là "chạy được câu SQL". Đây là **tầng nền của DataFrame** — mọi thao tác DataFrame đều đi qua Catalyst giống hệt SQL.

**Thành phần:**
- **Catalyst** — bộ tối ưu (mục 4.6)
- **Catalog** — siêu dữ liệu bảng; kết nối được với Hive Metastore, AWS Glue, Unity Catalog
- **Data Source API** — giao diện đọc/ghi; nhờ nó Spark nói chuyện được với Parquet, JDBC, Delta, Iceberg, Kafka…
- **Thrift Server** — cho công cụ BI cắm vào qua JDBC/ODBC

**Điểm cần nhớ: SQL và DataFrame API là hoàn toàn tương đương về hiệu năng** — cùng đi qua Catalyst, cùng ra một physical plan. Chọn cái nào là chuyện phong cách và khả năng bảo trì.

## 6.2 — Structured Streaming

Ý tưởng nền: **coi luồng dữ liệu như một bảng không ngừng dài ra.** Cùng API với batch.

```python
df = (spark.readStream.format("kafka")
        .option("subscribe", "transactions").load())

(df.groupBy(window("event_time", "1 hour"), "customer_id")
   .count()
   .writeStream
   .outputMode("update")
   .option("checkpointLocation", "/ckpt")
   .start())
```

### Hai chế độ chạy

| | **Micro-batch** (mặc định) | **Continuous** (thử nghiệm) |
|---|---|---|
| Cách chạy | Gom thành lô nhỏ, chạy như batch | Xử lý từng bản ghi |
| Độ trễ | ~100 ms – vài giây | ~1 ms |
| Đảm bảo | **Exactly-once** | Chỉ at-least-once |
| Thực tế | Gần như luôn dùng cái này | Hiếm khi dùng |

### Thời gian sự kiện và watermark

**Event time** = lúc việc xảy ra. **Processing time** = lúc Spark thấy nó. Dữ liệu tới trễ và lệch thứ tự là chuyện thường.

**Watermark** trả lời: *"trễ tới mức nào thì bỏ?"*

```python
df.withWatermark("event_time", "10 minutes")
```

Nghĩa: sự kiện trễ hơn 10 phút so với mốc lớn nhất đã thấy thì bỏ qua. **Đây cũng là cơ chế cho phép Spark dọn state cũ** — không có watermark thì state phình vô hạn.

### Output mode

| Mode | Ghi gì | Dùng khi |
|---|---|---|
| **Append** | Chỉ dòng mới, không sửa lại | Có watermark, kết quả đã chốt |
| **Update** | Dòng nào đổi thì ghi lại | Tổng hợp đang chạy |
| **Complete** | Ghi lại toàn bộ bảng kết quả | Bảng kết quả nhỏ |

### So với Flink — câu hỏi hay gặp

| | Spark Structured Streaming | Flink |
|---|---|---|
| Mô hình | Micro-batch | **Streaming thật** |
| Độ trễ | ~vài trăm ms trở lên | ~vài ms |
| Xử lý state | Được, nhưng đơn giản hơn | **Mạnh và linh hoạt hơn** |
| Batch + stream chung | ✅ Cùng API, cùng engine | ✅ Có, nhưng batch yếu hơn |
| Khi nào chọn | **Đã dùng Spark cho batch, độ trễ giây là đủ** | **Cần dưới 100 ms, hoặc state phức tạp** |

## 6.3 — MLlib

Thư viện ML phân tán. Có `Pipeline`, `Transformer`, `Estimator` — mô phỏng scikit-learn.

**Nói thẳng về tình hình hiện tại:** MLlib **đang mất dần vai trò**. Deep learning thì dùng PyTorch/TensorFlow; ML dạng bảng thì XGBoost/LightGBM mạnh hơn và thường chạy vừa trên một máy.

**Chỗ Spark vẫn thắng trong ML: chuẩn bị dữ liệu và feature engineering ở quy mô lớn** — rồi giao dữ liệu đã gọn cho framework khác huấn luyện. Đây chính là mô hình project Lichess.

## 6.4 — GraphX / GraphFrames

Tính toán trên đồ thị — PageRank, connected components, đường đi ngắn nhất. **Ít dùng trong thực tế**, phần lớn nhu cầu đồ thị nay đi bằng database chuyên dụng (Neo4j) hoặc thư viện riêng.

Biết là có, không cần đào sâu.

---
---

# VII — Dùng khi nào và không dùng khi nào

## 7.1 — Loại bài toán Spark giải tốt

| Loại | Ví dụ cụ thể |
|---|---|
| **ETL/ELT quy mô lớn** | Đọc raw → làm sạch → chuẩn hoá → ghi vào lakehouse |
| **Xử lý dữ liệu bán cấu trúc** | JSON lồng nhau, log, clickstream — thứ SQL thuần khó xử |
| **Join dữ liệu lớn** | Ghép nhiều bảng hàng tỉ dòng |
| **Feature engineering** | Tính đặc trưng theo thời gian, cửa sổ trượt, point-in-time |
| **Xử lý theo lô định kỳ** | Job hằng đêm, tổng hợp, báo cáo |
| **Streaming độ trễ giây** | Bảng điều khiển gần thời gian thực, cảnh báo |
| **Xử lý file lộn xộn** | Hàng nghìn file với schema hơi khác nhau |

## 7.2 — Ứng dụng phổ biến nhất trên thực tế

Nếu chỉ được nói một câu:

> **Đại đa số job Spark trên thế giới là ETL theo lô.**
> Không phải machine learning, không phải streaming, không phải đồ thị.
> **Đọc file thô, làm sạch, join, tổng hợp, ghi ra dạng có cấu trúc.**

Xếp theo tần suất thực tế:

1. **ETL/ELT theo lô** — áp đảo
2. **Truy vấn phân tích SQL** trên data lake
3. **Chuẩn bị dữ liệu cho ML** (không phải huấn luyện)
4. **Structured Streaming**
5. **MLlib huấn luyện mô hình** — nhỏ và đang thu hẹp

> Trả lời được câu này một cách thẳng thắn (thay vì kể một danh sách hoành tráng gồm cả GraphX)
> cho thấy bạn nhìn thực tế chứ không nhìn tài liệu quảng cáo.

## 7.3 — ⚠️ Khi KHÔNG nên dùng Spark

Đây là phần **phân biệt rõ nhất người hiểu Spark với người chỉ biết Spark.**

| Tình huống | Vì sao không | Dùng gì thay |
|---|---|---|
| **Dữ liệu vừa một máy** (dưới ~vài trăm GB) | Chi phí cluster + shuffle qua mạng lớn hơn lợi ích | **DuckDB, Polars**, pandas |
| **Truy vấn điểm, độ trễ ms** | Spark tối thiểu vài trăm ms chỉ để khởi động job | PostgreSQL, Redis, Cassandra |
| **Streaming dưới 100 ms** | Micro-batch không xuống thấp hơn được | **Flink** |
| **Dữ liệu đã nằm trong warehouse** | Kéo ra rồi đẩy vào là thừa | **SQL + dbt ngay trong warehouse** |
| **Job nhỏ chạy rất thường xuyên** | Chi phí khởi động JVM lấn át việc thật | Script thường, hàm serverless |
| **Giao dịch OLTP** | Spark không phải database, không có transaction dạng đó | Database thật |

> **Câu đáng nói trong phỏng vấn:**
> *"Câu hỏi đầu tiên với một bài toán dữ liệu không phải là tune Spark thế nào,
> mà là bài này có thực sự cần Spark không. Rất nhiều thứ gọi là big data
> thực ra chạy vừa trên một máy, và lúc đó DuckDB hay Polars nhanh hơn hẳn
> vì không phải trả giá cho việc phối hợp giữa các máy."*
>
> **Đây là loại câu làm người phỏng vấn ngồi thẳng lên.** Nó cho thấy bạn tối ưu cho bài toán,
> không phải cho công cụ.

---
---

# VIII — Ưu nhược điểm và bối cảnh cạnh tranh

## 8.1 — Ưu điểm

**① Một engine cho nhiều loại tải.** Batch, SQL, streaming, ML chung một API và một bộ máy. Không phải nuôi bốn hệ thống.

**② Trưởng thành và phổ biến.** Ra đời hơn 10 năm, gần như mọi nền tảng dữ liệu đều hỗ trợ. **Tuyển người biết Spark dễ**, tài liệu và lời giải cho lỗi thì đầy.

**③ Đa ngôn ngữ.** Scala, Java, Python, R, SQL — cùng hiệu năng nếu dùng DataFrame.

**④ Bộ tối ưu làm hộ rất nhiều.** Catalyst + AQE che được kha khá sai lầm của người viết.

**⑤ Chịu lỗi tự động.** Máy chết giữa chừng thì job vẫn xong, không cần code gì thêm.

**⑥ Co giãn thật.** Cùng một đoạn code chạy được trên laptop lẫn trên cluster nghìn node.

## 8.2 — Nhược điểm

**① Chi phí cố định lớn.** Khởi động vài giây tới vài phút. **Không dùng cho truy vấn tương tác nhỏ.**

**② Gánh nặng JVM.** GC là nguồn bất ổn kinh niên. Tungsten giảm bớt chứ không xoá được.

**③ Debug khó.** Lazy evaluation khiến lỗi hiện ra ở chỗ khác nơi gây lỗi. Stack trace phân tán, dài, khó đọc.

**④ Tuning là nghề riêng.** Hàng trăm tham số, mặc định thường không hợp, và cùng một job cần cấu hình khác nhau khi dữ liệu đổi.

**⑤ Python UDF đắt.** Mỗi dòng phải qua lại giữa JVM và Python. Pandas UDF (dùng Arrow) đỡ hơn nhiều nhưng vẫn không bằng hàm dựng sẵn.
→ **Quy tắc: luôn ưu tiên hàm có sẵn của Spark; UDF là phương án cuối.**

**⑥ Tốn tiền.** Cluster đòi nhiều RAM. Với dữ liệu vừa, chi phí thường không đáng.

**⑦ Quá tay cho việc nhỏ.** Và đây là lỗi phổ biến nhất — dùng Spark cho thứ mà một script Python xử lý xong trong 2 phút.

## 8.3 — Bối cảnh hiện tại

| Đối thủ | Cạnh tranh ở đâu | Đánh giá thẳng |
|---|---|---|
| **Flink** | Streaming | Flink thắng rõ ở độ trễ thấp và state phức tạp. Spark thắng khi đã có sẵn hạ tầng batch |
| **dbt + warehouse** (Snowflake, BigQuery) | Biến đổi dữ liệu | Dữ liệu đã ở trong warehouse thì SQL tại chỗ đơn giản hơn nhiều. **Đây là nơi Spark mất thị phần nhiều nhất** |
| **DuckDB, Polars** | Dữ liệu vừa và nhỏ | Một máy hiện đại xử lý được hàng trăm GB. **Rất nhiều bài toán "big data" thực ra không big** |
| **Ray** | Tải AI/ML | Thuần Python, hợp với deep learning hơn |
| **Trino / Presto** | Truy vấn tương tác | Nhanh hơn cho SQL kiểu khám phá |

### Spark có đang đi xuống không

Trả lời trung thực: **không, nhưng phạm vi đã thu hẹp.**

- **Mất phần dưới** cho DuckDB/Polars — dữ liệu vừa không cần cluster nữa
- **Mất phần SQL** cho warehouse + dbt — nếu dữ liệu vốn đã ở trong đó
- **Mất phần streaming độ trễ thấp** cho Flink
- **Vẫn giữ vững**: ETL quy mô rất lớn, dữ liệu bán cấu trúc, lakehouse, mọi thứ chạy trên Databricks

Và Spark vẫn đang tiến hoá: **Photon** (engine viết bằng C++ của Databricks), **Spark Connect** (client mỏng), **Comet/Gluten** (tăng tốc bằng engine gốc qua Arrow) — đều nhằm gỡ đúng điểm yếu JVM.

> **Nếu bị hỏi "Spark còn đáng học không":**
> *"Phạm vi có hẹp lại, nhưng ở mảng ETL quy mô lớn thì chưa có thứ thay thế.
> Và quan trọng hơn: các khái niệm của Spark — partition, shuffle, skew, lazy evaluation,
> tối ưu theo kế hoạch — là chung cho mọi engine phân tán. Học Spark là học cách nghĩ đó."*

---
---

# IX — Vận hành và tuning thực tế

## 9.1 — Đọc Spark UI

Công cụ chẩn đoán số một. Bốn tab hay dùng:

| Tab | Nhìn gì |
|---|---|
| **Jobs** | Job nào lâu; job có bị chạy lại không |
| **Stages** | **Phân bố thời gian task** (median vs max → skew) · lượng đọc/ghi shuffle · spill |
| **SQL** | Kế hoạch thực thi dạng đồ thị — kiểu join thật sự được chọn, số dòng ở mỗi bước |
| **Executors** | Thời gian GC · dung lượng bộ nhớ · executor nào chết |

> **Thói quen đúng: mọi chẩn đoán bắt đầu từ tab Stages, xem bảng tóm tắt thời gian task
> (min / 25th / median / 75th / max). Chênh lệch median với max nói gần hết câu chuyện.**

## 9.2 — Các tham số đáng nhớ

```python
spark.sql.shuffle.partitions          # 200 — chỉnh theo dung lượng dữ liệu
spark.sql.files.maxPartitionBytes     # 128MB — kích thước partition khi đọc
spark.sql.autoBroadcastJoinThreshold  # 10MB — ngưỡng broadcast (-1 để tắt)
spark.sql.adaptive.enabled            # true từ 3.0 — AQE
spark.sql.adaptive.skewJoin.enabled   # true — tự tách partition lệch
spark.executor.memory                 # RAM mỗi executor
spark.executor.cores                  # số task song song / executor
spark.memory.fraction                 # 0.6 — phần dành cho execution+storage
spark.speculation                     # false — bật để chống straggler
spark.dynamicAllocation.enabled       # tự co giãn số executor
```

## 9.3 — Bảng triệu chứng → nguyên nhân

| Triệu chứng | Nguyên nhân thường gặp |
|---|---|
| Một task chạy rất lâu, còn lại xong nhanh | **Skew** |
| Mọi task đều chậm đều nhau | Thiếu tài nguyên, hoặc partition quá to |
| Chỉ một task duy nhất chạy | **File nén không splittable**, hoặc `coalesce(1)` |
| Spill rất lớn | Execution memory thiếu → tăng partition |
| Thời gian GC cao | Quá nhiều object → dùng DataFrame, tăng RAM |
| Shuffle read khổng lồ | Join không cần thiết, hoặc bỏ lỡ cơ hội broadcast |
| Job chạy lại nhiều lần | Executor chết → xem tab Executors |
| Nhanh khi test, chậm khi chạy thật | Dữ liệu thật bị skew mà mẫu test thì không |

## 9.4 — Nguyên tắc luôn đúng

**① Lọc sớm nhất có thể.** Mỗi dòng loại bỏ được trước join là tiết kiệm ở mọi bước sau.

**② Giảm số lần shuffle.** Gộp nhiều phép gom thành một; tránh `orderBy` nếu không thật sự cần thứ tự toàn cục.

**③ Broadcast bảng nhỏ.** Kiểm tra kế hoạch xem Spark có tự làm chưa; chưa thì gợi ý bằng `broadcast()`.

**④ Chọn định dạng cột (Parquet/ORC) và nén splittable.** Đây là thứ rẻ nhất mà lợi nhất.

**⑤ Phân vùng dữ liệu theo cột hay lọc** — nhưng đừng phân vùng quá mịn, sẽ đẻ ra hàng nghìn file bé.

**⑥ Tránh UDF Python.** Dùng hàm có sẵn; buộc phải viết thì dùng pandas UDF.

**⑦ Đo trước khi chỉnh.** Mở UI, tìm stage chậm nhất, chữa đúng chỗ đó. Chỉnh tham số theo cảm tính là cách nhanh nhất để tốn một ngày mà không cải thiện gì.

---
---

# X — Khung trả lời câu hỏi chưa gặp

Đây là phần quan trọng nhất của note này. **Không thể học thuộc mọi câu hỏi Spark.** Nhưng gần như mọi câu đều rơi vào một trong bốn khung dưới.

## Khung ① — "X hoạt động thế nào?"

Trả lời theo **luồng dữ liệu**, không theo danh sách tính năng:

> **Ai lập kế hoạch → dữ liệu đi đâu → chia việc thế nào → chuyện gì xảy ra khi hỏng.**

Áp cho bất kỳ thành phần nào: đọc file, shuffle, broadcast, streaming.

## Khung ② — "Vì sao chậm / chẩn đoán đi"

> **① Phân loại trước.** Một task chậm hay mọi task chậm? Driver hay executor?
> **② Chỉ ra chỗ nhìn.** Spark UI tab Stages, phân bố thời gian task.
> **③ Nêu 2–3 nguyên nhân xác suất cao nhất** theo thứ tự.
> **④ Nói cách kiểm chứng từng cái.**

**Người phỏng vấn quan tâm quy trình chẩn đoán hơn là đáp án.** Nói "tôi sẽ mở UI xem phân bố thời gian task trước" mạnh hơn là đoán bừa một nguyên nhân đúng.

## Khung ③ — "So sánh A và B"

> **① Chúng khác nhau ở chiều nào** (không phải liệt kê hai danh sách rời)
> **② Đánh đổi là gì**
> **③ Chọn cái nào trong tình huống nào**

Ví dụ: *"Sort-merge và broadcast khác nhau ở chỗ có phải di chuyển bảng lớn hay không. Broadcast tránh được shuffle nhưng đòi một bên đủ nhỏ để nhét vừa RAM mỗi executor. Nên broadcast khi bên nhỏ dưới vài trăm MB, còn lại thì sort-merge."*

## Khung ④ — "Thiết kế một pipeline cho…"

> **① Hỏi lại đã.** Dữ liệu bao lớn? Cần độ trễ bao nhiêu? Chạy bao lâu một lần? Đã có hạ tầng gì?
> **② Nói xem có cần Spark không.** Ăn điểm rất mạnh.
> **③ Vẽ luồng: nguồn → thô → sạch → phục vụ.**
> **④ Nói rõ chỗ nào có thể hỏng** và xử lý ra sao.

## Ba câu vạn năng

Bí thì vẫn nói được thứ có nội dung:

> **"Về cơ bản Spark chia dữ liệu thành partition, mỗi partition là một task chạy song song. Chỗ nào cần trao đổi dữ liệu giữa các partition thì phải shuffle, và shuffle là chỗ đắt nhất."**

> **"Câu hỏi tôi hỏi trước tiên là dữ liệu bao lớn và cần độ trễ bao nhiêu — vì hai con số đó quyết định gần hết kiến trúc."**

> **"Cái này tôi chưa làm trực tiếp, nhưng theo cách Spark xử lý những thứ tương tự thì tôi đoán là…"**

Câu thứ ba là câu **nên dùng thay vì im lặng**. Thành thật về giới hạn nhưng vẫn thể hiện được cách suy luận — và đó là thứ đang được chấm.

---
---

# XI — Tự kiểm tra

**Nói thành tiếng, không mở note.**

## Nhóm nền tảng

**①** Spark ra đời để giải quyết vấn đề gì của MapReduce? *(3 vấn đề)*
**②** RDD lineage là gì, và vì sao nó cho phép giữ dữ liệu trong RAM mà vẫn chịu lỗi?
**③** Vì sao DataFrame nhanh hơn RDD? Trong PySpark thì chênh lệch còn lớn hơn — vì sao?
**④** Narrow và wide transformation khác nhau thế nào, và vì sao ranh giới đó quan trọng?

## Nhóm thực thi

**⑤** Từ `.groupBy().count()` tới lúc có kết quả, Spark làm những gì?
*Phải nhắc: DAG · Catalyst · stage · shuffle · task · action.*
**⑥** Driver chia một file cho các executor thế nào? Chuyện gì xảy ra nếu file nén bằng gzip?
**⑦** Ba kiểu join — cơ chế và khi nào chọn cái nào?
**⑧** Catalyst gồm những bước nào, và ba luật tối ưu quan trọng nhất là gì?
**⑨** AQE làm gì mà Catalyst không làm được?

## Nhóm bộ nhớ và lỗi

**⑩** Execution memory và storage memory — quan hệ bất đối xứng giữa chúng là gì? Vì sao?
**⑪** Khi nào cache là vô ích, và khi nào cache còn **có hại**?
**⑫** Job OOM — chẩn đoán từ đâu, theo thứ tự nào?
**⑬** Cache và checkpoint khác nhau chỗ nào?

## Nhóm phán đoán — quan trọng nhất

**⑭** **Khi nào KHÔNG nên dùng Spark?** Nêu ít nhất 4 tình huống và lý do.
**⑮** Ứng dụng phổ biến nhất của Spark trong thực tế là gì?
**⑯** Spark so với Flink — chọn cái nào trong hoàn cảnh nào?
**⑰** Nêu ba nhược điểm thật của Spark.
**⑱** Một job join hai bảng chạy 2 tiếng. Chẩn đoán theo trình tự nào?

> [!tip] Chuẩn để coi là xong
> Nhóm **phán đoán** quan trọng hơn nhóm thực thi. Ai đọc tài liệu cũng nói được Spark làm gì;
> **rất ít người nói được khi nào không nên dùng nó.** Đó là chỗ tạo khác biệt.

> [!warning] Ấp úng là tín hiệu thật
> Không phải "chưa thuộc bài", mà là **chưa đủ đường dẫn để lôi kiến thức ra dưới áp lực**.
> Quay lại đúng mục đó và nói lại.

---

## Liên quan

- [[Job Fundamentals 02 - SQL nâng cao]] — Catalyst tối ưu SQL; window function
- [[Job Fundamentals 03 - Distributed Systems]] — partition, replication, consensus ở tầng dưới
- [[Job Fundamentals 04 - DSA]] *(chưa có)*
- [[20_KE_HOACH_Job_Fundamentals]] — kế hoạch
