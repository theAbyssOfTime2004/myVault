---
tags: [knowledge, data-engineer, sql, interview-prep, fundamentals]
status: active
created: 2026-08-12
series: Job Fundamentals
part: 2 / SQL
---

# Job Fundamentals 02 — SQL nâng cao

> **Đây là module dài nhất (tuần 2–5)** và là mảng bị hỏi nhiều thứ hai sau Spark.
> Lỗ hổng đã xác nhận: **lấy giao dịch mới nhất của mỗi khách** — trả lời bằng `GROUP BY`, sai.
> Mục 2 và Mẫu ① là chỗ đó.
>
> **Cách dùng:** đọc mục, rồi **tự gõ lại truy vấn từ đầu** — không copy. SQL là kỹ năng, không phải kiến thức.

---

## Mục lục

1. [[#1 — Thứ tự thực thi mô hình giải thích mọi thứ]]
2. [[#2 — GROUP BY vs Window]] ← *chỗ đã sai*
3. [[#3 — Window function đầy đủ]]
4. [[#4 — Sáu mẫu phải thuộc]]
5. [[#5 — NULL những cái bẫy]]
6. [[#6 — Join và fan-out]]
7. [[#7 — Hiệu năng]]
8. [[#8 — Tự kiểm tra]]

---

# 1 — Thứ tự thực thi: mô hình giải thích mọi thứ

SQL **không chạy theo thứ tự bạn viết**. Thứ tự logic là:

```
FROM / JOIN
  ↓
WHERE
  ↓
GROUP BY
  ↓
HAVING
  ↓
SELECT   ← window function tính ở đây
  ↓
DISTINCT
  ↓
ORDER BY
  ↓
LIMIT
```

Nắm cái này thì ba câu hỏi kinh điển tự trả lời:

| Câu hỏi | Vì sao |
|---|---|
| Sao không dùng được alias của `SELECT` trong `WHERE`? | `WHERE` chạy **trước** `SELECT`, lúc đó alias chưa tồn tại |
| `WHERE` khác `HAVING` chỗ nào? | `WHERE` lọc **dòng thô**, `HAVING` lọc **nhóm đã gom** |
| Sao không lọc được `WHERE rn = 1`? | Window function tính ở bước `SELECT`, **sau** `WHERE` → phải bọc vào subquery/CTE |

> **Câu cuối chính là lý do tồn tại của mẫu `ROW_NUMBER` bọc subquery.**
> Không phải quy ước tuỳ tiện — nó là hệ quả trực tiếp của thứ tự thực thi.

---

# 2 — GROUP BY vs Window

Đây là ranh giới quan trọng nhất trong toàn bộ SQL nâng cao.

|  | `GROUP BY` | Window function |
|---|---|---|
| Số dòng | **N vào → M ra** (gom lại) | **N vào → N ra** (chú thích thêm) |
| Giữ được cột khác | ❌ Chỉ giữ được cột trong `GROUP BY` và hàm tổng hợp | ✅ Giữ nguyên mọi cột |
| Dùng khi | Cần **một dòng cho mỗi nhóm** | Cần **giữ chi tiết** nhưng thêm thông tin ngữ cảnh |

## Vì sao `GROUP BY` sai ở bài "giao dịch mới nhất mỗi khách"

```sql
-- ❌ SAI
SELECT customer_id, MAX(transaction_time), amount
FROM transactions
GROUP BY customer_id;
```

**Vấn đề:** `MAX(transaction_time)` cho đúng *thời điểm*, nhưng `amount` thì **không có gì buộc nó phải thuộc về đúng dòng đó**.

- Postgres / SQL Server → **báo lỗi** (`amount` không nằm trong `GROUP BY`)
- MySQL (chế độ lỏng) → **chạy được và trả về sai** — lấy `amount` của một dòng bất kỳ trong nhóm

> **Đây là loại lỗi tệ nhất: chạy trót lọt, không báo gì, và số ra sai.**

**Cách nghĩ đúng:** câu hỏi không phải *"giá trị lớn nhất là bao nhiêu"* mà là *"**dòng nào** là dòng mới nhất"*.
`GROUP BY` trả lời câu thứ nhất. Muốn trả lời câu thứ hai thì cần **xếp hạng rồi lấy dòng hạng 1** → window function.

---

# 3 — Window function đầy đủ

## Cú pháp

```sql
<hàm>() OVER (
    PARTITION BY <chia nhóm>
    ORDER BY    <sắp xếp trong nhóm>
    <khung>
)
```

Cả ba phần đều tuỳ chọn. Không có `PARTITION BY` → cả bảng là một nhóm.

## 3.1 — Nhóm xếp hạng

| Hàm | Với giá trị `100, 100, 90` | Dùng khi |
|---|---|---|
| `ROW_NUMBER()` | `1, 2, 3` | **Khử trùng lặp** — luôn cho đúng 1 dòng mỗi nhóm |
| `RANK()` | `1, 1, 3` | Xếp hạng thật, đồng hạng thì nhảy số |
| `DENSE_RANK()` | `1, 1, 2` | Xếp hạng, không nhảy số |
| `NTILE(4)` | Chia đều thành 4 phần | Chia tứ phân vị |

> **Bị hỏi "khác nhau chỗ nào" thì đừng định nghĩa — đưa luôn ví dụ `100, 100, 90`.**
> Nhanh hơn và không thể hiểu nhầm.

**Chọn cái nào:** cần *đúng một dòng* → `ROW_NUMBER`. Cần *tất cả dòng đồng hạng* → `RANK` / `DENSE_RANK`.

## 3.2 — Nhóm lệch dòng

```sql
LAG(amount, 1)  OVER (PARTITION BY customer_id ORDER BY txn_time)  -- dòng trước
LEAD(amount, 1) OVER (PARTITION BY customer_id ORDER BY txn_time)  -- dòng sau
FIRST_VALUE(amount) OVER (...)
LAST_VALUE(amount)  OVER (...)   -- ⚠️ xem cảnh báo ở 3.3
```

Dùng cho: so sánh với kỳ trước, tính chênh lệch, đo khoảng cách giữa hai sự kiện.

## 3.3 — Khung (frame) — chỗ hay sai nhất

```sql
ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW    -- từ đầu nhóm tới dòng hiện tại
ROWS BETWEEN 6 PRECEDING AND CURRENT ROW           -- 7 dòng gần nhất
ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING    -- ⭐ LOẠI TRỪ dòng hiện tại
ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING  -- toàn bộ nhóm
```

### ⚠️ `ROWS` vs `RANGE`

| | Nghĩa |
|---|---|
| **`ROWS`** | Đếm **số dòng vật lý** |
| **`RANGE`** | Gộp mọi dòng có **cùng giá trị `ORDER BY`** (peers) vào chung |

**Mặc định khi có `ORDER BY` là `RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`** — không phải `ROWS`.

Hậu quả: nếu có **timestamp trùng nhau**, running total dùng mặc định sẽ **cộng luôn cả các dòng cùng thời điểm**, kể cả những dòng "phía sau". Số ra không sai về mặt định nghĩa nhưng thường không phải cái bạn muốn.

> **Ghi `ROWS` một cách tường minh khi ý bạn là "n dòng gần nhất".** Đừng để mặc định quyết hộ.

### ⚠️ `LAST_VALUE` gần như luôn trả về sai

Vì khung mặc định dừng ở `CURRENT ROW` → "giá trị cuối" hoá ra là chính dòng hiện tại. Phải mở khung:

```sql
LAST_VALUE(amount) OVER (
    PARTITION BY customer_id ORDER BY txn_time
    ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
)
```

### ⭐ Khung loại trừ dòng hiện tại — point-in-time correctness

```sql
AVG(amount) OVER (
    PARTITION BY customer_id ORDER BY txn_time
    ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING
)
```

**Đây chính là `rowsBetween(Window.unboundedPreceding, -1)` trong project Lichess.**

Ý nghĩa: đặc trưng tại thời điểm T **chỉ được tính từ dữ liệu trước T**. Tính cả dòng hiện tại là
**data leakage** — model đẹp lúc huấn luyện, sập lúc chạy thật, và **không có lỗi nào báo cả**.

> Kể được chỗ này trong phỏng vấn là chuyển từ "biết cú pháp" sang "hiểu vì sao cần cú pháp đó".

---

# 4 — Sáu mẫu phải thuộc

## Mẫu ① — Dòng mới nhất mỗi nhóm ⭐

**Bài đã trượt hôm 11/8.**

```sql
SELECT *
FROM (
    SELECT *,
           ROW_NUMBER() OVER (
               PARTITION BY customer_id
               ORDER BY transaction_time DESC
           ) AS rn
    FROM transactions
) t
WHERE rn = 1;
```

**Vì sao phải bọc subquery:** `WHERE` chạy trước `SELECT`, mà `rn` sinh ra ở `SELECT` → không lọc trực tiếp được.

### Các cách khác

**Correlated subquery** — chạy được nhưng thường chậm, và **trả về nhiều dòng nếu có đồng hạng**:

```sql
SELECT * FROM transactions t
WHERE transaction_time = (
    SELECT MAX(transaction_time) FROM transactions t2
    WHERE t2.customer_id = t.customer_id
);
```

**`DISTINCT ON`** — gọn nhất nhưng **chỉ Postgres**:

```sql
SELECT DISTINCT ON (customer_id) *
FROM transactions
ORDER BY customer_id, transaction_time DESC;
```

> **Nói trong phỏng vấn:** đưa `ROW_NUMBER` trước (chuẩn, chạy mọi nơi),
> rồi nhắc `DISTINCT ON` như một lựa chọn nếu là Postgres. **Nhắc được lựa chọn thứ hai luôn ăn điểm.**

### Xử lý đồng hạng

Nếu hai giao dịch cùng `transaction_time`, `ROW_NUMBER` vẫn chọn một dòng — nhưng **chọn dòng nào là không xác định**.
Muốn ổn định thì thêm khoá phụ:

```sql
ORDER BY transaction_time DESC, transaction_id DESC
```

**Đây là chi tiết người phỏng vấn hay dò.** Nói ra chủ động thì rất được điểm.

---

## Mẫu ② — Top N mỗi nhóm

Y hệt mẫu ①, chỉ đổi điều kiện lọc:

```sql
SELECT * FROM (
    SELECT *,
           ROW_NUMBER() OVER (PARTITION BY category ORDER BY revenue DESC) AS rn
    FROM products
) t
WHERE rn <= 3;
```

Muốn giữ **mọi sản phẩm đồng hạng 3** thì đổi sang `DENSE_RANK()`.

---

## Mẫu ③ — Running total và moving average

```sql
SELECT
    txn_date,
    amount,

    -- cộng dồn từ đầu
    SUM(amount) OVER (
        PARTITION BY customer_id ORDER BY txn_date
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS running_total,

    -- trung bình trượt 7 dòng
    AVG(amount) OVER (
        PARTITION BY customer_id ORDER BY txn_date
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) AS ma7

FROM transactions;
```

Nối với phần fraud đã ôn: **phát hiện bất thường theo 3σ** dựa trên `AVG` và `STDDEV` trượt, kết hợp khung loại trừ dòng hiện tại để không cho giao dịch đang xét ảnh hưởng tới chính ngưỡng của nó.

---

## Mẫu ④ — Gap and island ⭐

Bài toán: **chuỗi ngày liên tiếp** (streak đăng nhập, ngày hoạt động liên tục).

**Mẹo:** với các ngày liên tiếp, `ngày − số thứ tự dòng` là **hằng số**. Dùng nó làm khoá nhóm.

```sql
WITH d AS (
    SELECT DISTINCT user_id, login_date FROM logins
),
g AS (
    SELECT *,
           login_date - (ROW_NUMBER() OVER (
               PARTITION BY user_id ORDER BY login_date
           ) * INTERVAL '1 day') AS grp
    FROM d
)
SELECT user_id,
       MIN(login_date) AS streak_start,
       MAX(login_date) AS streak_end,
       COUNT(*)        AS streak_length
FROM g
GROUP BY user_id, grp;
```

Kiểm tra bằng tay để thấy vì sao nó chạy:

| login_date | rn | date − rn ngày |
|---|---|---|
| 01-01 | 1 | 2023-12-31 |
| 01-02 | 2 | 2023-12-31 |
| 01-03 | 3 | 2023-12-31 |
| **01-07** | 4 | **2024-01-03** ← đứt chuỗi, nhóm mới |
| 01-08 | 5 | 2024-01-03 |

---

## Mẫu ⑤ — Sessionization ⭐

Bài toán: gom event thành phiên, **cách nhau quá 30 phút thì tính phiên mới**.

**Mẹo:** đánh dấu 0/1 chỗ bắt đầu phiên, rồi **cộng dồn cờ đó** → ra id phiên.

```sql
WITH marked AS (
    SELECT *,
           CASE
               WHEN event_time - LAG(event_time) OVER (
                        PARTITION BY user_id ORDER BY event_time
                    ) > INTERVAL '30 minutes'
                 OR LAG(event_time) OVER (
                        PARTITION BY user_id ORDER BY event_time
                    ) IS NULL
               THEN 1 ELSE 0
           END AS is_new_session
    FROM events
),
sessioned AS (
    SELECT *,
           SUM(is_new_session) OVER (
               PARTITION BY user_id ORDER BY event_time
               ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
           ) AS session_id
    FROM marked
)
SELECT user_id, session_id,
       MIN(event_time) AS started,
       MAX(event_time) AS ended,
       COUNT(*)        AS events
FROM sessioned
GROUP BY user_id, session_id;
```

> **`SUM` cộng dồn trên cờ 0/1 để sinh khoá nhóm** là một trong những thủ thuật SQL đáng giá nhất.
> Nó giải được cả một họ bài toán "gom các dòng liền kề theo điều kiện nào đó".

---

## Mẫu ⑥ — Anti-join: tìm cái không tồn tại

Bài toán: khách hàng **chưa từng** giao dịch.

```sql
-- ✅ Cách tốt
SELECT c.*
FROM customers c
WHERE NOT EXISTS (
    SELECT 1 FROM transactions t WHERE t.customer_id = c.customer_id
);

-- ✅ Cũng được
SELECT c.*
FROM customers c
LEFT JOIN transactions t ON t.customer_id = c.customer_id
WHERE t.customer_id IS NULL;

-- ❌ NGUY HIỂM
SELECT * FROM customers
WHERE customer_id NOT IN (SELECT customer_id FROM transactions);
```

**Vì sao `NOT IN` nguy hiểm:** nếu subquery trả về **dù chỉ một `NULL`**, toàn bộ truy vấn trả về **không dòng nào**.
Vì `x NOT IN (1, 2, NULL)` được đánh giá là `UNKNOWN`, không phải `TRUE`.

> **Đây là bẫy phỏng vấn cực kỳ phổ biến. Dùng `NOT EXISTS` làm mặc định.**

---

# 5 — NULL: những cái bẫy

| Bẫy | Sai ở đâu | Cách đúng |
|---|---|---|
| `NOT IN` với `NULL` | Trả về rỗng | `NOT EXISTS` |
| `NULL = NULL` | Ra `UNKNOWN`, không phải `TRUE` | `IS NULL` / `IS NOT DISTINCT FROM` |
| `COUNT(col)` | **Bỏ qua `NULL`** | `COUNT(*)` nếu muốn đếm dòng |
| `AVG(col)` | Chia cho số dòng **không NULL** | `AVG(COALESCE(col, 0))` nếu `NULL` nghĩa là 0 |
| `SUM` trên tập rỗng | Ra `NULL`, không phải `0` | `COALESCE(SUM(x), 0)` |
| `LEFT JOIN` + điều kiện ở `WHERE` | **Biến thành `INNER JOIN`** | Đưa điều kiện vào `ON` |

## Cái cuối đáng nói riêng

```sql
-- ❌ Không còn là LEFT JOIN nữa
SELECT * FROM customers c
LEFT JOIN transactions t ON t.customer_id = c.customer_id
WHERE t.amount > 100;

-- ✅ Giữ đúng ngữ nghĩa LEFT JOIN
SELECT * FROM customers c
LEFT JOIN transactions t
       ON t.customer_id = c.customer_id
      AND t.amount > 100;
```

**Vì sao:** `LEFT JOIN` sinh ra dòng có `t.*` toàn `NULL` cho khách không khớp.
Rồi `WHERE t.amount > 100` đánh giá `NULL > 100` = `UNKNOWN` → **loại luôn các dòng đó**.
Kết quả đúng bằng `INNER JOIN`.

> Câu chốt: **điều kiện lọc bảng bên phải phải nằm ở `ON`, không nằm ở `WHERE`.**

---

# 6 — Join và fan-out

## Fan-out là gì

Join trên khoá **không duy nhất** ở phía bên kia thì **số dòng nhân lên**.

Khách A có 3 địa chỉ. `customers ⋈ addresses` → A xuất hiện **3 lần**.
Rồi `SUM(amount)` → **số tiền bị đếm gấp 3**.

> **Đây là nguyên nhân số một khiến báo cáo ra số sai mà không ai phát hiện.**

## Cách phòng

**① Khai báo grain trước khi viết.** *"Một dòng của kết quả này đại diện cho cái gì?"*
Không trả lời được thì chưa nên viết truy vấn.

**② Kiểm tra số dòng trước và sau join.** Tăng bất thường = fan-out.

**③ Gom trước rồi mới join** thay vì join rồi mới gom:

```sql
-- ✅ An toàn
SELECT c.customer_id, c.name, a.total
FROM customers c
LEFT JOIN (
    SELECT customer_id, SUM(amount) AS total
    FROM transactions
    GROUP BY customer_id
) a ON a.customer_id = c.customer_id;
```

Cách này **giữ được grain là một dòng một khách** — join với bảng đã gom sẵn thì không thể fan-out.

---

# 7 — Hiệu năng

## Sargability — điều kiện có dùng được index không

```sql
-- ❌ Bọc hàm quanh cột → index vô dụng, phải quét toàn bảng
WHERE DATE(created_at) = '2024-01-01'
WHERE UPPER(email) = 'A@B.COM'
WHERE amount * 100 > 5000

-- ✅ Để cột trần một bên
WHERE created_at >= '2024-01-01' AND created_at < '2024-01-02'
WHERE email = 'a@b.com'
WHERE amount > 50
```

> **Nguyên tắc: cột phải đứng trần một bên phép so sánh.** Bọc hàm vào là mất index.

## Đọc `EXPLAIN`

Ba thứ cần nhìn:

| Nhìn gì | Dấu hiệu xấu |
|---|---|
| **Kiểu quét** | `Seq Scan` trên bảng lớn có index |
| **Kiểu join** | `Nested Loop` với số dòng lớn ở cả hai bên |
| **Ước lượng vs thật** | Lệch nhiều lần → thống kê cũ, cần `ANALYZE` |

## Vài quy tắc luôn đúng

- **Lọc sớm.** Đẩy `WHERE` xuống càng sâu càng tốt — ít dòng đi vào join thì mọi thứ phía sau rẻ hơn
- **Gom trước khi join** khi có thể (xem mục 6)
- **Tránh `SELECT *`** — đặc biệt với định dạng cột (Parquet), vì mất luôn column pruning
- **`EXISTS` thường nhanh hơn `IN`** với subquery lớn — `EXISTS` dừng ngay khi tìm thấy dòng đầu tiên

---

# 8 — Tự kiểm tra

Không nhìn note. **Tự gõ lại truy vấn từ đầu**, không copy.

**①** Lấy giao dịch **mới nhất của mỗi khách hàng**, giữ đủ mọi cột.
Giải thích vì sao `GROUP BY` không làm được.
→ **Đây là câu đã trượt hôm 11/8.**

**②** `ROW_NUMBER` / `RANK` / `DENSE_RANK` khác nhau thế nào — trả lời bằng ví dụ số.

**③** Vì sao `WHERE rn = 1` không dùng trực tiếp được, phải bọc subquery?

**④** `NOT IN (subquery)` sai chỗ nào khi subquery có `NULL`?

**⑤** Viết truy vấn tìm **chuỗi ngày đăng nhập liên tiếp** dài nhất của mỗi user.

**⑥** Viết truy vấn **gom event thành phiên**, cách nhau > 30 phút là phiên mới.

**⑦** `LEFT JOIN` mà đặt điều kiện ở `WHERE` thì chuyện gì xảy ra? Vì sao?

**⑧** Trung bình trượt 7 ngày **không tính ngày hiện tại** — viết khung cửa sổ.
Vì sao lại cần loại trừ dòng hiện tại?

> [!tip] Chuẩn để coi là xong
> Câu ① và ⑧ phải gõ được **không do dự**. Đó là hai câu có xác suất bị hỏi cao nhất,
> và câu ⑧ nối thẳng sang project của mình.

---

## Liên quan

- [[Job Fundamentals 01 - Apache Spark]]
- [[Job Fundamentals 03 - Distributed Systems]]
- [[Job Fundamentals 04 - DSA]] *(chưa có)*
- [[20_KE_HOACH_Job_Fundamentals]] — kế hoạch
