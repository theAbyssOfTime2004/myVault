---
tags: [knowledge, data-engineer, distributed-systems, interview-prep, fundamentals]
status: active
created: 2026-08-12
series: DE Fundamentals
part: 3 / Distributed Systems
---

# DE Fundamentals 03 — Distributed Systems

> **Câu bị hỏi hôm 11/8 mà không trả lời được:** *"Distributed system cho storage là như thế nào?"*
> Mục 2 là câu trả lời đó.
>
> **Cách dùng:** đọc xong mỗi mục thì **nói lớn thành tiếng** một lượt.
> Chữ **in đậm** là câu chốt.

---

## Mục lục

1. [[#1 — Ba bài toán gốc]]
2. [[#2 — Distributed storage]] ← *câu bị hỏi*
3. [[#3 — Partitioning chia dữ liệu ra sao]]
4. [[#4 — Replication và quorum]]
5. [[#5 — CAP và consistency]]
6. [[#6 — Consensus vừa đủ]]
7. [[#7 — Xử lý hỏng hóc]]
8. [[#8 — Tự kiểm tra]]

---

# 1 — Ba bài toán gốc

Mọi hệ phân tán, dù là storage, database hay stream processor, đều đang giải **đúng ba bài toán này**. Nắm khung này thì mọi thứ phía sau chỉ là biến thể.

| Bài toán | Câu hỏi | Sinh ra |
|---|---|---|
| **Partition** | Dữ liệu quá lớn cho một máy → chia thế nào? | Sharding, hash/range, consistent hashing |
| **Replicate** | Máy sẽ chết → giữ mấy bản, ở đâu? | Replication factor, quorum, leader/follower |
| **Agree** | Các máy nhìn thấy khác nhau → thống nhất kiểu gì? | Consensus, Raft, CAP, split brain |

> **Câu mở đầu dùng được cho gần như mọi câu hỏi về distributed system:**
> *"Về cơ bản mọi hệ phân tán đều đang giải ba việc: chia dữ liệu ra, nhân bản để chịu lỗi,
> và thống nhất trạng thái giữa các node. Thiết kế khác nhau chỉ là đánh đổi khác nhau ở ba chỗ đó."*

---

# 2 — Distributed storage

> **Ý cốt lõi:** một file quá lớn cho một máy → phải **cắt nhỏ, rải ra, và nhân bản**.
> Ba việc đó sinh ra toàn bộ phần còn lại của thiết kế.

## 2.1 — Mô hình HDFS

Cũ nhưng vẫn là mô hình chuẩn để giải thích. Tách làm hai loại node:

| Thành phần | Giữ cái gì | Đặc điểm |
|---|---|---|
| **NameNode** (master) | *Metadata*: file → gồm block nào → block nằm ở DataNode nào | **Không chứa dữ liệu thật.** Nằm hết trong RAM để tra nhanh |
| **DataNode** (worker) | Block dữ liệu thật | Nhiều, rẻ, được phép hỏng |

### ① Chia block

File bị cắt thành block cố định — mặc định **128 MB**. File 1 GB → 8 block.
**Block là đơn vị của mọi thứ phía sau**: nhân bản, đặt chỗ, giao việc.

### ② Replication

Mỗi block lưu **3 bản** trên 3 DataNode khác nhau. Một máy chết thì dữ liệu vẫn còn ở 2 nơi.

### ③ Rack awareness

3 bản không đặt bừa:

- **Bản 1** — node đang ghi (rẻ nhất, không tốn mạng)
- **Bản 2** — **rack khác** (phòng mất nguyên rack)
- **Bản 3** — cùng rack với bản 2 (rẻ hơn, vì không tốn thêm băng thông liên rack)

**Đây là đánh đổi giữa độ an toàn và chi phí mạng** — nói được ý này là ăn điểm.

### ④ Heartbeat và tự lành

DataNode gửi tín hiệu sống về NameNode định kỳ. Mất tín hiệu quá lâu → NameNode coi node đó chết →
**tự nhân bản lại** các block thiếu bản sao sang node khác cho đủ 3.

### ⑤ Data locality

Vì NameNode biết block nằm ở đâu, compute có thể được **đẩy tới chỗ dữ liệu** thay vì kéo dữ liệu về chỗ compute.

> **Di chuyển code rẻ hơn di chuyển data rất nhiều.** Đây là ý tưởng nền của cả Hadoop lẫn Spark.

### ⚠️ Small file problem

Metadata nằm hết trong RAM của NameNode. Mỗi file/block tốn ~150 byte metadata.
**10 triệu file nhỏ giết NameNode, trong khi 10 file lớn cùng dung lượng thì không sao.**

Câu hỏi phụ hay gặp: *"Vì sao nhiều file nhỏ lại xấu?"* — hai lý do:
metadata phình ở master, và **mỗi file thành một task riêng** ở tầng compute (xem [[DE Fundamentals 01 - Spark Internals]]).

## 2.2 — Object storage (S3 / GCS / ADLS — cái thực tế đang dùng)

Khác biệt then chốt:

| | HDFS | Object storage |
|---|---|---|
| Cấu trúc | Cây thư mục thật | **Kho key–value phẳng** — `/year=2024/` chỉ là tiền tố trong tên key |
| Sửa file | Có append | **Object bất biến** — muốn đổi thì ghi object mới |
| Đổi tên thư mục | Rẻ (đổi metadata) | **Đắt** — phải copy toàn bộ rồi xoá |
| Chịu lỗi | Replication 3× (300% dung lượng) | **Erasure coding** (~150%) |
| Storage & compute | Gắn chặt, có locality | **Tách rời** — scale độc lập, trả tiền theo lượng dùng |

**Erasure coding:** chia dữ liệu thành *k* mảnh + *m* mảnh chẵn lẻ. Mất tối đa *m* mảnh vẫn khôi phục được.
Rẻ hơn nhiều so với giữ 3 bản nguyên vẹn.

## 2.3 — Câu chốt để ăn điểm

> **"Và chính vì object storage bất biến, không có thao tác đổi tên nguyên tử, nên mới cần
> table format như Delta hay Iceberg — tính nguyên tử không đến từ filesystem nữa,
> mà đến từ một transaction log ghi bên cạnh dữ liệu. Commit thực chất là ghi thêm một entry vào log."**

Câu này nối distributed storage sang thứ đã có trong project Lichess. Nói được là chuyển từ
"thuộc bài" sang "hiểu vì sao công cụ tồn tại".

---

# 3 — Partitioning: chia dữ liệu ra sao

## Ba cách chia

| Cách | Làm sao | Ưu | Nhược |
|---|---|---|---|
| **Range** | Chia theo khoảng giá trị (A–F, G–M…) | Query theo khoảng rất nhanh | **Dễ lệch** — dữ liệu theo thời gian dồn hết vào partition cuối |
| **Hash** | `hash(key) % N` | Phân bố đều | Mất tính cục bộ; **query theo khoảng phải quét hết** |
| **Consistent hashing** | Xếp node lên một vòng tròn hash | **Thêm/bớt node chỉ chuyển 1/N dữ liệu** | Phức tạp hơn |

## Vì sao cần consistent hashing

Với `hash(key) % N`, đổi từ 3 node lên 4 node thì **gần như toàn bộ key đổi chỗ** — phải chuyển cả cluster.

Consistent hashing: node và key cùng được ánh xạ lên **một vòng tròn**. Mỗi key thuộc về node đầu tiên
gặp khi đi theo chiều kim đồng hồ. Thêm một node → **chỉ đoạn cung của node đó bị chuyển**, phần còn lại đứng yên.

**Virtual node:** mỗi máy vật lý đăng ký nhiều điểm trên vòng, để phân bố đều hơn và
để khi một máy chết thì tải rải sang nhiều máy chứ không dồn vào một máy kế bên.

Dùng ở: **Cassandra, DynamoDB, Riak.** Redis Cluster dùng hash slot — cùng tinh thần.

## Nối với cái đã biết

**Partition key trong Kafka và partition trong Spark là cùng một khái niệm.**
Và **skew** trong Spark ([[DE Fundamentals 01 - Spark Internals]] mục 4) chính là bài toán
"chọn key phân bố không đều" của partitioning.

---

# 4 — Replication và quorum

## Leader / follower

- **Mọi ghi đi qua leader**, leader phát lại cho follower
- Đọc có thể từ follower (giảm tải) — nhưng **có thể đọc phải dữ liệu cũ**

| Kiểu | Cách | Đánh đổi |
|---|---|---|
| **Đồng bộ** | Leader chờ follower xác nhận rồi mới báo xong | An toàn, **chậm**; follower chết thì ghi bị treo |
| **Bất đồng bộ** | Leader báo xong ngay | Nhanh, nhưng **leader chết là mất dữ liệu chưa kịp truyền** |
| **Bán đồng bộ** | Chờ ít nhất 1 follower | Cân bằng — đa số hệ thật dùng cái này |

> Kafka gọi đây là **ISR (in-sync replicas)** và `acks=all` nghĩa là chờ toàn bộ ISR xác nhận.
> Nối thẳng với phần streaming đã ôn.

## Quorum — công thức phải thuộc

Với **N** bản sao, **W** bản xác nhận khi ghi, **R** bản đọc khi đọc:

> ## W + R > N

Khi đó tập ghi và tập đọc **bắt buộc giao nhau ít nhất một node** → đọc chắc chắn thấy được bản mới nhất.

Cấu hình quen thuộc: **N=3, W=2, R=2** → 2+2 > 3 ✅

Điều chỉnh được theo nhu cầu:

- `W=1, R=3` → ghi nhanh, đọc chậm
- `W=3, R=1` → ghi chậm, đọc nhanh
- `W=1, R=1` → nhanh nhất, **không đảm bảo gì cả** (eventual consistency)

---

# 5 — CAP và consistency

## ⚠️ CAP thường bị nói sai

Cách nói sai phổ biến: *"chọn 2 trong 3"*. Không phải vậy.

> **CAP nói: khi xảy ra network partition (P), phải chọn giữa C và A.**
> Lúc mạng bình thường thì **có cả C lẫn A**, không phải đánh đổi gì cả.

Và **P không phải thứ được chọn** — mạng sẽ đứt, đó là thực tế. Nên thực chất chỉ có hai loại hệ:

| Loại | Khi mạng đứt thì | Ví dụ |
|---|---|---|
| **CP** | Từ chối phục vụ để giữ dữ liệu đúng | HBase, ZooKeeper, etcd |
| **AP** | Vẫn phục vụ, chấp nhận dữ liệu có thể lệch | Cassandra, DynamoDB (mặc định) |

## PACELC — nói được cái này là vượt mặt bằng chung

> **P**artition → chọn **A** hay **C**;
> **E**lse (mạng bình thường) → chọn **L**atency hay **C**onsistency.

Ý nghĩa: **ngay cả khi mạng khoẻ, muốn nhất quán mạnh vẫn phải trả giá bằng độ trễ** —
vì phải chờ đủ số bản sao xác nhận. Đây mới là đánh đổi bạn gặp hằng ngày,
còn partition thì thỉnh thoảng mới xảy ra.

## Các mức consistency

Từ mạnh xuống yếu:

| Mức | Nghĩa |
|---|---|
| **Linearizable** | Như thể chỉ có một bản sao duy nhất. Đắt nhất |
| **Read-your-writes** | Mình ghi thì mình đọc lại thấy ngay (người khác thì chưa chắc) |
| **Monotonic reads** | Đã thấy dữ liệu mới thì không bao giờ thấy lại dữ liệu cũ hơn |
| **Eventual** | Ngừng ghi đủ lâu thì cuối cùng mọi bản sao sẽ giống nhau |

**Ví dụ để trả lời khi bị hỏi "khi nào chấp nhận eventual":**
đếm lượt xem video thì eventual là đủ; **số dư tài khoản thì không**.

---

# 6 — Consensus, vừa đủ

Không cần chứng minh Paxos. Cần biết **vì sao cần** và **nó xuất hiện ở đâu**.

## Vì sao cần

Nhiều node phải thống nhất **một** giá trị — ai là leader, thứ tự các thao tác, cấu hình cluster là gì.
Không thống nhất được thì sinh ra **split brain**: hai node cùng tin mình là leader, cùng nhận ghi, dữ liệu phân nhánh.

## Raft — mức khái niệm

**① Bầu leader.** Mỗi node có bộ đếm thời gian ngẫu nhiên. Hết giờ mà không nghe leader thì tự ứng cử,
xin phiếu. **Ai được quá bán thì thành leader.**

**② Nhân bản log.** Mọi thay đổi đi qua leader, ghi vào log, phát cho follower.

**③ Commit khi quá bán đã ghi.** Chưa quá bán thì chưa tính là xong.

**④ Term.** Mỗi nhiệm kỳ có số thứ tự tăng dần. Node nào nhận tin nhắn với term cũ hơn thì bỏ qua.

> **Vì sao "quá bán" chặn được split brain: một cluster không thể có hai nhóm cùng chiếm quá bán.**
> Đây là câu một dòng đáng thuộc.

## Xuất hiện ở đâu

| Hệ thống | Dùng để |
|---|---|
| **etcd, Consul** | Lưu cấu hình cluster (Kubernetes dùng etcd) |
| **ZooKeeper** | Điều phối; Kafka bản cũ dùng để bầu controller |
| **Kafka KRaft** | Bản mới tự làm consensus, bỏ ZooKeeper |
| **HDFS NameNode HA** | Bầu NameNode nào đang active |

---

# 7 — Xử lý hỏng hóc

## Phát hiện node chết — và vì sao nó khó

**Heartbeat + timeout.** Nhưng đây là chỗ có một sự thật khó chịu:

> **Không thể phân biệt "node đã chết" với "node còn sống nhưng mạng chậm".**

Đó là lý do mọi hệ phân tán đều phải chọn timeout, và mọi timeout đều sai theo một trong hai hướng:

- Timeout ngắn → báo chết nhầm → chuyển leader không cần thiết, gây bất ổn
- Timeout dài → hỏng thật mà lâu mới phát hiện → dịch vụ treo

## Split brain và fencing

Kịch bản: leader cũ bị coi là chết, cluster bầu leader mới. Rồi **leader cũ sống lại** và vẫn tưởng mình là leader.

Hai lớp phòng vệ:

**① Quorum** — leader cũ không còn chiếm được quá bán nên không commit được gì.

**② Fencing token** — mỗi nhiệm kỳ có một số tăng dần. Tầng storage **từ chối mọi ghi mang token cũ**.
Đây là lớp chặn cuối, dùng khi storage nằm ngoài cluster consensus.

## Straggler — node chậm

Không chết hẳn, chỉ chậm. **Một task chậm giữ chân cả job.**

Cách chữa: **speculative execution** — phát hiện task chạy chậm bất thường thì
**chạy song song một bản sao ở node khác**, ai xong trước lấy kết quả người đó.
Spark có `spark.speculation` (mặc định tắt).

> Phân biệt với **skew**: straggler là *máy* chậm, skew là *dữ liệu* lệch.
> Chữa khác nhau hoàn toàn — speculative execution **không** cứu được skew,
> vì bản sao cũng phải xử lý đúng lượng dữ liệu lệch đó.

## Retry và idempotency

Retry là cách chữa mặc định — nhưng chỉ an toàn khi thao tác **idempotent**.

> **Ghi đè là idempotent. Cộng dồn thì không.**

Đã ôn kỹ ở phần streaming. Ở đây chỉ cần nhớ: **mọi hệ phân tán đều retry, nên mọi thao tác đều phải chịu được việc bị chạy hai lần.**

---

# 8 — Tự kiểm tra

**Nói thành tiếng.** Mỗi câu 60–90 giây.

**①** Distributed storage hoạt động thế nào?
*Phải nhắc tới: chia block · replication · rack awareness · metadata tách khỏi dữ liệu · heartbeat.*
→ **Đây là câu đã trượt hôm 11/8. Nói cho tới khi trôi.**

**②** CAP nói gì — và cách phát biểu "chọn 2 trong 3" sai ở đâu?

**③** `W + R > N` nghĩa là gì, và vì sao nó đảm bảo đọc thấy dữ liệu mới nhất?

**④** Split brain là gì, và vì sao "quá bán" chặn được nó?

**⑤** Vì sao nhiều file nhỏ lại là vấn đề — kể cả ở tầng storage lẫn tầng compute?

**⑥** Phân biệt straggler và data skew. Speculative execution chữa được cái nào?

> [!tip] Ấp úng là tín hiệu thật
> Không phải "chưa thuộc bài", mà là **chưa đủ đường dẫn để lôi kiến thức ra dưới áp lực**.
> Quay lại đúng mục đó và nói lại.

---

## Liên quan

- [[DE Fundamentals 01 - Spark Internals]] — partition, shuffle, skew ở tầng compute
- [[DE Fundamentals 02 - SQL nâng cao]] *(chưa có)*
- [[DE Fundamentals 04 - DSA cho DE]] *(chưa có)*
- [[20_KE_HOACH_DE_Fundamentals]] — kế hoạch
