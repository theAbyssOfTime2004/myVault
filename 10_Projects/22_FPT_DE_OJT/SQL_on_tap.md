---
tags: [job-hunt, interview, fpt, ojt, data-engineer, sql, interview-prep]
status: active
created: 2026-09-29
role: Data Engineer OJT — FPT
---

# FPT DE OJT — Ôn SQL

> **Note này bổ sung, không thay thế** [[Job Fundamentals 02 - SQL nâng cao]].
> Note 02 lo phần *window, gap-island, sessionization, NULL, fan-out, hiệu năng*.
> Note này lo phần **OJT/fresher hay bị hỏi mà note 02 chưa có**:
> lý thuyết cơ sở dữ liệu (nói bằng lời), khác biệt cú pháp SQL Server, và **một bộ bài tập có dữ liệu thật để gõ**.
>
> **Cách dùng:** dán schema ở mục C vào [db-fiddle](https://www.db-fiddle.com) (chọn PostgreSQL) hoặc Postgres local,
> rồi tự gõ từng bài. Đáp án nằm trong ô gập — **chỉ mở sau khi đã chạy ra kết quả**.
> Mọi đáp án và kết quả dưới đây đã chạy thật trên PostgreSQL 16.

---

## Mục lục

**A.** [[#A — Lý thuyết hay hỏi (trả lời bằng lời)]]
**B.** [[#B — SQL Server vs PostgreSQL vs MySQL]]
**C.** [[#C — Schema luyện tập]]
**D.** [[#D — 22 bài tập]]
**E.** [[#E — Lịch 7 buổi]]

---

# A — Lý thuyết hay hỏi (trả lời bằng lời)

Vòng OJT thường có một đoạn **hỏi-đáp miệng** trước khi cho viết query. Mỗi câu dưới đây nói trôi được trong 30–60 giây là đạt.

## A1 — Phân loại lệnh

| Nhóm | Lệnh | Ghi nhớ |
|---|---|---|
| **DDL** — định nghĩa | `CREATE`, `ALTER`, `DROP`, `TRUNCATE` | Đổi **cấu trúc** |
| **DML** — thao tác | `SELECT`, `INSERT`, `UPDATE`, `DELETE`, `MERGE` | Đổi **dữ liệu** |
| **DCL** — quyền | `GRANT`, `REVOKE` | Ai được làm gì |
| **TCL** — giao dịch | `BEGIN`, `COMMIT`, `ROLLBACK`, `SAVEPOINT` | Gói nhiều lệnh thành một |

## A2 — `DELETE` vs `TRUNCATE` vs `DROP` ⭐

| | `DELETE` | `TRUNCATE` | `DROP` |
|---|---|---|---|
| Xoá gì | Dòng (có `WHERE`) | **Mọi** dòng | Cả bảng + cấu trúc |
| Tốc độ | Chậm — ghi log từng dòng | Nhanh — giải phóng cả trang dữ liệu | Nhanh |
| Trigger `DELETE` | Chạy | Không chạy | Không |
| Reset identity | Không | Có (SQL Server) | — |
| Rollback | Được | Được **trong transaction** ở SQL Server/Postgres; MySQL thì không | Tuỳ DB |

> Bẫy: nhiều người nói "`TRUNCATE` không rollback được" — **sai với SQL Server và Postgres**. Nói được điều này là ăn điểm.

## A3 — Khoá và ràng buộc

- **Primary key** — duy nhất + không `NULL`, mỗi bảng một cái (có thể gồm nhiều cột = *composite key*, như `order_items(order_id, product_id)`)
- **Candidate key** — mọi tập cột có thể làm PK; chọn một làm PK, còn lại là *alternate key*
- **Foreign key** — trỏ sang PK bảng khác, đảm bảo **toàn vẹn tham chiếu** (không có đơn hàng của khách không tồn tại)
- **Unique** — duy nhất nhưng **cho phép `NULL`** (SQL Server chỉ cho *một* `NULL`, Postgres cho nhiều)
- **Surrogate key** (id tự tăng, không mang nghĩa) vs **natural key** (email, CCCD) — kho dữ liệu gần như luôn dùng surrogate vì natural key có thể đổi

## A4 — Chuẩn hoá ⭐

| Dạng | Điều kiện | Ví dụ vi phạm |
|---|---|---|
| **1NF** | Mỗi ô một giá trị nguyên tử, không nhóm lặp | Cột `phones = '090..., 091...'` |
| **2NF** | 1NF + không phụ thuộc **một phần** vào khoá ghép | `order_items(order_id, product_id, product_name)` — `product_name` chỉ phụ thuộc `product_id` |
| **3NF** | 2NF + không phụ thuộc **bắc cầu** | `employees(emp_id, dept_id, dept_name)` — `dept_name` phụ thuộc `dept_id`, không phụ thuộc `emp_id` |
| **BCNF** | Mọi phụ thuộc hàm đều có vế trái là siêu khoá | Hiếm hỏi sâu, biết tên là đủ |

**Câu nối sang DE:** OLTP chuẩn hoá để **ghi đúng, không dư thừa**. Kho dữ liệu (OLAP) **cố tình phi chuẩn hoá** (star schema) để **đọc nhanh, ít join**. Nói được *vì sao* mỗi bên chọn ngược nhau là trả lời tốt.

## A5 — Transaction & ACID ⭐

| | Nghĩa | Ví dụ chuyển khoản A → B |
|---|---|---|
| **A**tomicity | Tất cả hoặc không gì | Trừ A mà chưa cộng B thì rollback cả hai |
| **C**onsistency | Luôn thoả ràng buộc | Tổng tiền hệ thống không đổi, số dư không âm |
| **I**solation | Giao dịch song song không thấy trạng thái dở của nhau | Người khác không thấy lúc A đã trừ, B chưa cộng |
| **D**urability | Commit rồi thì mất điện vẫn còn | Nhờ write-ahead log |

### Isolation level và hiện tượng

| Level | Dirty read | Non-repeatable read | Phantom |
|---|---|---|---|
| Read Uncommitted | có thể | có thể | có thể |
| **Read Committed** (mặc định SQL Server, Postgres) | ✗ | có thể | có thể |
| Repeatable Read (mặc định MySQL InnoDB) | ✗ | ✗ | có thể* |
| Serializable | ✗ | ✗ | ✗ |

\* *Postgres và InnoDB thực tế chặn phần lớn phantom ở Repeatable Read — nhắc thêm câu này nếu người hỏi đào sâu.*

- **Dirty read** — đọc dữ liệu người khác chưa commit
- **Non-repeatable read** — đọc cùng *một dòng* hai lần, ra hai giá trị
- **Phantom** — chạy cùng *một điều kiện* hai lần, **số dòng** khác nhau

## A6 — Index ⭐

- **Là gì:** cấu trúc phụ (thường là **B-tree**) giúp tìm dòng không cần quét cả bảng — như mục lục sách
- **Clustered vs Non-clustered** (SQL Server hỏi rất nhiều):
  - **Clustered** — dữ liệu bảng *được sắp xếp vật lý* theo khoá này → **mỗi bảng chỉ một**; PK mặc định là clustered
  - **Non-clustered** — cấu trúc riêng, trỏ về dòng → **có nhiều cái**
- **Composite index `(a, b)`** dùng được cho `WHERE a = ?` và `WHERE a = ? AND b = ?`, **không dùng được** cho `WHERE b = ?` (quy tắc *leftmost prefix*)
- **Covering index** — index chứa đủ mọi cột query cần → không phải quay lại bảng
- **Khi index có hại:** bảng ghi nhiều (mỗi `INSERT`/`UPDATE` phải cập nhật index), cột ít giá trị khác nhau (giới tính), bảng quá nhỏ
- Bọc hàm quanh cột làm mất index → xem *sargability* ở [[Job Fundamentals 02 - SQL nâng cao#7 — Hiệu năng|note 02 mục 7]]

## A7 — View, CTE, temp table, subquery

| | Lưu gì | Sống bao lâu | Dùng khi |
|---|---|---|---|
| **Subquery** | Không | Trong 1 câu | Logic ngắn, dùng 1 lần |
| **CTE** (`WITH`) | Không | Trong 1 câu | Tách query dài thành bước dễ đọc; **đệ quy** (cây quản lý) |
| **Temp table** | Có, dữ liệu thật | Trong session | Kết quả trung gian dùng lại nhiều lần, cần index |
| **View** | Chỉ lưu **câu query** | Vĩnh viễn | Che độ phức tạp, phân quyền |
| **Materialized view** | Lưu **kết quả** | Vĩnh viễn, phải refresh | Báo cáo nặng, chấp nhận dữ liệu hơi cũ |

## A8 — Stored procedure vs Function vs Trigger

| | Stored procedure | Function | Trigger |
|---|---|---|---|
| Gọi thế nào | `EXEC` / `CALL` | Trong `SELECT` | **Tự chạy** khi `INSERT/UPDATE/DELETE` |
| Trả về | 0..n result set, tham số `OUTPUT` | Bắt buộc 1 giá trị hoặc 1 bảng | — |
| Sửa dữ liệu | Được | Không (SQL Server) | Được |
| Transaction | Quản lý được | Không | Chạy trong transaction của lệnh gây ra nó |

> Trigger là "ma thuật ẩn" — debug khó, nên nói thêm: *"em sẽ hạn chế trigger, ưu tiên logic ở tầng ETL cho dễ theo dõi."*

## A9 — Kiểu dữ liệu (quan trọng với tiếng Việt)

- `CHAR(n)` — độ dài **cố định**, đệm khoảng trắng. `VARCHAR(n)` — độ dài **thay đổi**
- **SQL Server:** `VARCHAR` không lưu đúng dấu tiếng Việt với collation mặc định → dùng **`NVARCHAR`** và chuỗi có tiền tố **`N'Hà Nội'`**. Quên `N` là ra `H? N?i`
- Tiền: **`DECIMAL/NUMERIC`**, không bao giờ `FLOAT` (sai số làm tròn)
- Thời gian: `DATE`, `DATETIME2` (SQL Server), `TIMESTAMP` / `TIMESTAMPTZ` (Postgres) — nhắc được múi giờ là điểm cộng với DE

## A10 — Phần "Data Engineer" của SQL

- **OLTP vs OLAP** — nhiều giao dịch nhỏ, ghi nhiều, chuẩn hoá ↔ ít truy vấn lớn, đọc nhiều, phi chuẩn hoá, thường lưu theo **cột**
- **Star schema** — 1 bảng **fact** (sự kiện, số đo: `order_items`) ở giữa + nhiều bảng **dimension** (ngữ cảnh: khách, sản phẩm, ngày). **Snowflake** = dimension được chuẩn hoá tiếp
- **Grain** của fact — "một dòng đại diện cho cái gì" — phải nói ra đầu tiên khi thiết kế
- **SCD (Slowly Changing Dimension)**:
  - **Type 1** — ghi đè, mất lịch sử
  - **Type 2** — thêm dòng mới với `valid_from`, `valid_to`, `is_current` → giữ lịch sử (hay hỏi nhất)
  - **Type 3** — thêm cột `previous_value`, giữ được 1 bước
- **ETL vs ELT** — biến đổi trước khi nạp ↔ nạp thô vào kho rồi biến đổi bằng SQL trong kho (xu hướng hiện nay, nhờ kho cột mạnh)
- **Idempotent load** — chạy lại job không sinh dữ liệu trùng → dùng `MERGE` / upsert thay vì `INSERT` mù (bài 21)
- **Incremental load** — chỉ nạp dữ liệu mới bằng watermark (`updated_at > last_run`)

---

# B — SQL Server vs PostgreSQL vs MySQL

Nhiều dự án và chương trình đào tạo trong hệ sinh thái FPT dùng **SQL Server**. Không cần thuộc hết — nhưng gặp đề T-SQL thì không được khựng.

| Việc | SQL Server (T-SQL) | PostgreSQL | MySQL |
|---|---|---|---|
| Lấy N dòng | `SELECT TOP 5 ...` | `LIMIT 5` | `LIMIT 5` |
| Phân trang | `OFFSET 10 ROWS FETCH NEXT 5 ROWS ONLY` | `LIMIT 5 OFFSET 10` | `LIMIT 10, 5` |
| Thay `NULL` | `ISNULL(x, 0)` / `COALESCE` | `COALESCE` | `IFNULL` / `COALESCE` |
| Giờ hiện tại | `GETDATE()` | `NOW()` | `NOW()` |
| Cộng ngày | `DATEADD(day, 30, d)` | `d + INTERVAL '30 days'` | `DATE_ADD(d, INTERVAL 30 DAY)` |
| Hiệu ngày | `DATEDIFF(day, a, b)` | `b - a` | `DATEDIFF(b, a)` |
| Đầu tháng | `DATEFROMPARTS(YEAR(d), MONTH(d), 1)` | `DATE_TRUNC('month', d)` | `DATE_FORMAT(d, '%Y-%m-01')` |
| Nối chuỗi | `a + b` / `CONCAT` | `a \|\| b` / `CONCAT` | `CONCAT` |
| Tự tăng | `INT IDENTITY(1,1)` | `GENERATED ALWAYS AS IDENTITY` / `SERIAL` | `AUTO_INCREMENT` |
| Upsert | `MERGE` | `INSERT ... ON CONFLICT` / `MERGE` (≥15) | `INSERT ... ON DUPLICATE KEY UPDATE` |
| Gộp chuỗi theo nhóm | `STRING_AGG(x, ',')` | `STRING_AGG(x, ',')` | `GROUP_CONCAT(x)` |
| Tạo bảng từ query | `SELECT ... INTO new_tbl FROM ...` | `CREATE TABLE new_tbl AS SELECT ...` | `CREATE TABLE ... AS SELECT ...` |

> **Chiến thuật khi đề không nói hệ quản trị:** hỏi lại một câu *"anh/chị muốn em viết theo SQL Server hay Postgres ạ?"*.
> Không biết thì viết SQL chuẩn (`ROW_NUMBER`, `COALESCE`, `CASE WHEN`) — chạy được gần như mọi nơi.

---

# C — Schema luyện tập

Mô hình bán hàng nhỏ + nhân sự. **Dữ liệu được cài sẵn bẫy** (ghi chú bên phải) — nhiều bài sai là vì những dòng này.

```sql
DROP TABLE IF EXISTS order_items, orders, products, customers, employees, departments CASCADE;

CREATE TABLE departments (
    dept_id   INT PRIMARY KEY,
    dept_name VARCHAR(50) NOT NULL
);

CREATE TABLE employees (
    emp_id     INT PRIMARY KEY,
    name       VARCHAR(50) NOT NULL,
    dept_id    INT REFERENCES departments(dept_id),
    manager_id INT REFERENCES employees(emp_id),
    salary     NUMERIC(10,2) NOT NULL,
    hire_date  DATE NOT NULL
);

CREATE TABLE customers (
    customer_id INT PRIMARY KEY,
    name        VARCHAR(50) NOT NULL,
    email       VARCHAR(100),
    city        VARCHAR(50),
    signup_date DATE NOT NULL
);

CREATE TABLE products (
    product_id INT PRIMARY KEY,
    name       VARCHAR(50) NOT NULL,
    category   VARCHAR(30) NOT NULL,
    price      NUMERIC(10,2) NOT NULL
);

CREATE TABLE orders (
    order_id    INT PRIMARY KEY,
    customer_id INT REFERENCES customers(customer_id),
    order_date  DATE NOT NULL,
    status      VARCHAR(20) NOT NULL   -- 'completed' | 'cancelled' | 'pending'
);

CREATE TABLE order_items (
    order_id   INT REFERENCES orders(order_id),
    product_id INT REFERENCES products(product_id),
    quantity   INT NOT NULL,
    unit_price NUMERIC(10,2) NOT NULL,
    PRIMARY KEY (order_id, product_id)
);

INSERT INTO departments VALUES
 (1,'Data'),(2,'Backend'),(3,'HR'),(4,'Legal');          -- Legal: không có ai

INSERT INTO employees VALUES
 (1,'An',   1,NULL,5000,'2020-01-10'),                    -- giám đốc Data, không có quản lý
 (2,'Bình', 1,1,   3000,'2021-03-01'),
 (3,'Chi',  1,1,   3000,'2021-06-15'),                    -- đồng lương với Bình
 (4,'Dũng', 1,2,   2000,'2023-02-01'),
 (5,'Hà',   2,NULL,4000,'2019-11-20'),
 (6,'Khoa', 2,5,   4500,'2022-01-05'),                    -- lương cao hơn quản lý
 (7,'Lan',  2,5,   2500,'2024-04-01'),
 (8,'Minh', 3,NULL,2800,'2020-08-08'),
 (9,'Nam',  NULL,1,1800,'2025-01-15');                    -- chưa xếp phòng

INSERT INTO customers VALUES
 (1,'Tuấn','tuan@mail.com','Hà Nội','2024-01-05'),
 (2,'Linh','linh@mail.com','HCM',   '2024-01-20'),
 (3,'Phúc','phuc@mail.com','Đà Nẵng','2024-02-11'),
 (4,'Mai', NULL,           'HCM',   '2024-03-02'),
 (5,'Quân','quan@mail.com','Hà Nội','2024-03-15'),       -- chưa mua gì
 (6,'Tuấn','tuan@mail.com','Hà Nội','2024-04-01');       -- trùng với khách 1

INSERT INTO products VALUES
 (1,'Laptop',  'Electronics',1000),
 (2,'Phone',   'Electronics', 600),
 (3,'Earbuds', 'Electronics', 100),
 (4,'Tablet',  'Electronics', 400),
 (5,'SQL Book','Books',        30),
 (6,'DE Book', 'Books',        40),
 (7,'Desk',    'Furniture',   200);                      -- chưa bán được

INSERT INTO orders VALUES
 (101,1,'2024-01-10','completed'),
 (102,2,'2024-01-25','completed'),
 (103,1,'2024-02-02','completed'),
 (104,3,'2024-02-15','cancelled'),
 (105,2,'2024-02-20','completed'),
 (106,4,'2024-03-05','completed'),
 (107,1,'2024-03-20','pending'),
 (108,3,'2024-03-22','completed'),
 (109,6,'2024-04-03','completed'),
 (110,2,'2024-04-10','completed');

INSERT INTO order_items VALUES
 (101,1,1,1000),(101,5,2,30),
 (102,2,1,600),
 (103,3,2,100),(103,6,1,40),
 (104,1,1,1000),
 (105,4,1,400),(105,5,1,30),(105,6,1,40),
 (106,2,2,550),
 (107,7,1,200),
 (108,5,3,30),
 (109,3,1,100),
 (110,1,1,950),(110,3,1,100);
```

**Doanh thu** trong mọi bài = `SUM(quantity * unit_price)` **chỉ tính đơn `completed`**, trừ khi đề nói khác.

---

# D — 22 bài tập

Ba mức: 🟢 cơ bản (phải làm được không do dự) · 🟡 trung bình (mức OJT hay ra) · 🔴 nâng cao (điểm cộng).

## 🟢 Cơ bản

### Bài 1 — Nhân viên lương cao hơn trung bình toàn công ty

> [!success]- Đáp án
> ```sql
> SELECT name, salary
> FROM employees
> WHERE salary > (SELECT AVG(salary) FROM employees)
> ORDER BY salary DESC;
> ```
> Kết quả: **An 5000, Khoa 4500, Hà 4000**.
> Không viết được `WHERE salary > AVG(salary)` — hàm tổng hợp không dùng trong `WHERE` (xem thứ tự thực thi, note 02 mục 1).

### Bài 2 — Mức lương cao thứ 2 ⭐ (câu kinh điển)

> [!success]- Đáp án — biết ít nhất 2 cách
> ```sql
> -- Cách 1: subquery — chạy mọi nơi
> SELECT MAX(salary) FROM employees
> WHERE salary < (SELECT MAX(salary) FROM employees);
>
> -- Cách 2: DISTINCT + OFFSET
> SELECT DISTINCT salary FROM employees
> ORDER BY salary DESC
> LIMIT 1 OFFSET 1;          -- SQL Server: OFFSET 1 ROWS FETCH NEXT 1 ROWS ONLY
>
> -- Cách 3: DENSE_RANK — tổng quát cho "cao thứ N"
> SELECT DISTINCT salary FROM (
>     SELECT salary, DENSE_RANK() OVER (ORDER BY salary DESC) AS dr
>     FROM employees
> ) t
> WHERE dr = 2;
> ```
> Kết quả: **4500**.
> **Follow-up hay gặp:** *"Nếu không có lương thứ 2 thì sao?"* → cách 1 trả về `NULL` (1 dòng), cách 2 và 3 trả về 0 dòng.
> *"Sao dùng `DENSE_RANK` mà không phải `RANK`?"* → với `5000, 5000, 4500`, `RANK` cho 4500 hạng 3, không có hạng 2.

### Bài 3 — Số nhân viên mỗi phòng, **kể cả phòng không có ai**

> [!success]- Đáp án
> ```sql
> SELECT d.dept_name, COUNT(e.emp_id) AS n
> FROM departments d
> LEFT JOIN employees e ON e.dept_id = d.dept_id
> GROUP BY d.dept_id, d.dept_name
> ORDER BY d.dept_id;
> ```
> Kết quả: Data 4 · Backend 3 · HR 1 · **Legal 0**.
> **Bẫy:** viết `COUNT(*)` thì Legal ra **1** — vì `LEFT JOIN` vẫn sinh ra một dòng (toàn `NULL` bên phải) và `COUNT(*)` đếm dòng. `COUNT(e.emp_id)` bỏ qua `NULL` nên ra 0.

### Bài 4 — Phòng có lương trung bình trên 3000

> [!success]- Đáp án
> ```sql
> SELECT d.dept_name, ROUND(AVG(e.salary), 2) AS avg_salary
> FROM employees e
> JOIN departments d ON d.dept_id = e.dept_id
> GROUP BY d.dept_name
> HAVING AVG(e.salary) > 3000;
> ```
> Kết quả: **Backend 3666.67, Data 3250.00**. Lọc trên nhóm → `HAVING`, không phải `WHERE`.

### Bài 5 — Tên nhân viên kèm tên quản lý (người không có quản lý vẫn hiện)

> [!success]- Đáp án
> ```sql
> SELECT e.name, m.name AS manager
> FROM employees e
> LEFT JOIN employees m ON m.emp_id = e.manager_id;
> ```
> **Self join** — cùng một bảng đóng hai vai. `LEFT` để An, Hà, Minh (không có quản lý) không bị mất.

### Bài 6 — Nhân viên có lương cao hơn quản lý trực tiếp

> [!success]- Đáp án
> ```sql
> SELECT e.name, e.salary, m.name AS manager, m.salary AS manager_salary
> FROM employees e
> JOIN employees m ON m.emp_id = e.manager_id
> WHERE e.salary > m.salary;
> ```
> Kết quả: **Khoa 4500 > Hà 4000**.

### Bài 7 — Khách hàng chưa từng đặt đơn

> [!success]- Đáp án
> ```sql
> SELECT c.customer_id, c.name
> FROM customers c
> WHERE NOT EXISTS (
>     SELECT 1 FROM orders o WHERE o.customer_id = c.customer_id
> );
> ```
> Kết quả: **Quân (5)**. Cách `LEFT JOIN ... WHERE o.order_id IS NULL` cũng đúng. **Tránh `NOT IN`** — xem bài 19.

### Bài 8 — Email bị trùng

> [!success]- Đáp án
> ```sql
> SELECT email, COUNT(*) AS n
> FROM customers
> WHERE email IS NOT NULL
> GROUP BY email
> HAVING COUNT(*) > 1;
> ```
> Kết quả: **tuan@mail.com — 2**.

## 🟡 Trung bình

### Bài 9 — Doanh thu theo tháng

> [!success]- Đáp án
> ```sql
> SELECT DATE_TRUNC('month', o.order_date)::date AS month,
>        SUM(oi.quantity * oi.unit_price)       AS revenue
> FROM orders o
> JOIN order_items oi ON oi.order_id = o.order_id
> WHERE o.status = 'completed'
> GROUP BY 1
> ORDER BY 1;
> ```
> Kết quả: 01 → **1660** · 02 → **710** · 03 → **1190** · 04 → **1150**.
> SQL Server: thay `DATE_TRUNC` bằng `DATEFROMPARTS(YEAR(o.order_date), MONTH(o.order_date), 1)` và phải `GROUP BY` lại nguyên biểu thức (không dùng `GROUP BY 1`).

### Bài 10 — Tăng trưởng doanh thu so với tháng trước (%)

> [!success]- Đáp án
> ```sql
> WITH m AS (
>     SELECT DATE_TRUNC('month', o.order_date)::date AS month,
>            SUM(oi.quantity * oi.unit_price)       AS revenue
>     FROM orders o
>     JOIN order_items oi ON oi.order_id = o.order_id
>     WHERE o.status = 'completed'
>     GROUP BY 1
> )
> SELECT month, revenue,
>        LAG(revenue) OVER (ORDER BY month) AS prev,
>        ROUND(100.0 * (revenue - LAG(revenue) OVER (ORDER BY month))
>              / NULLIF(LAG(revenue) OVER (ORDER BY month), 0), 1) AS pct
> FROM m
> ORDER BY month;
> ```
> Kết quả `pct`: `NULL`, **-57.2**, **67.6**, **-3.4**.
> Hai chi tiết đáng nói: `NULLIF(..., 0)` chống chia cho 0; `100.0` (không phải `100`) để tránh **chia số nguyên** ra 0.

### Bài 11 — Lương cao nhất mỗi phòng, giữ cả người đồng hạng

> [!success]- Đáp án
> ```sql
> SELECT dept_id, name, salary
> FROM (
>     SELECT *, RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS r
>     FROM employees
>     WHERE dept_id IS NOT NULL
> ) t
> WHERE r = 1;
> ```
> Kết quả: Data **An** · Backend **Khoa** · HR **Minh**.
> **Biến thể:** *lương cao thứ 2 mỗi phòng* → `DENSE_RANK`, `= 2` → Data ra **cả Bình và Chi (3000)**, Backend ra **Hà**. Dùng `ROW_NUMBER` sẽ mất một trong hai người Data — sai.

### Bài 12 — Top 2 sản phẩm doanh thu cao nhất mỗi danh mục

> [!success]- Đáp án
> ```sql
> WITH r AS (
>     SELECT p.category, p.name, SUM(oi.quantity * oi.unit_price) AS rev
>     FROM order_items oi
>     JOIN orders o   ON o.order_id = oi.order_id AND o.status = 'completed'
>     JOIN products p ON p.product_id = oi.product_id
>     GROUP BY p.category, p.name
> )
> SELECT category, name, rev
> FROM (
>     SELECT *, ROW_NUMBER() OVER (PARTITION BY category ORDER BY rev DESC) AS rn
>     FROM r
> ) t
> WHERE rn <= 2;
> ```
> Kết quả: Books — **SQL Book 180, DE Book 80** · Electronics — **Laptop 1950, Phone 1700**.
> Laptop không phải 3000: đơn 104 (1000) bị huỷ, đơn 110 bán giá 950.

### Bài 13 — Pivot: doanh thu Electronics và Books theo từng tháng thành 2 cột

> [!success]- Đáp án — conditional aggregation
> ```sql
> SELECT DATE_TRUNC('month', o.order_date)::date AS month,
>        SUM(CASE WHEN p.category = 'Electronics' THEN oi.quantity * oi.unit_price ELSE 0 END) AS electronics,
>        SUM(CASE WHEN p.category = 'Books'       THEN oi.quantity * oi.unit_price ELSE 0 END) AS books
> FROM orders o
> JOIN order_items oi ON oi.order_id = o.order_id
> JOIN products p     ON p.product_id = oi.product_id
> WHERE o.status = 'completed'
> GROUP BY 1
> ORDER BY 1;
> ```
> Kết quả: 01 → 1600 / 60 · 02 → 600 / 110 · 03 → 1100 / 90 · 04 → 1150 / 0.
> **`SUM(CASE WHEN ...)` là mẫu phải thuộc** — chạy mọi DB, thay được `PIVOT` của SQL Server, và dùng lại cho mọi bài "đếm/tổng có điều kiện".

### Bài 14 — Tỷ lệ đơn bị huỷ theo thành phố

> [!success]- Đáp án
> ```sql
> SELECT c.city,
>        COUNT(*) AS n_orders,
>        ROUND(100.0 * SUM(CASE WHEN o.status = 'cancelled' THEN 1 ELSE 0 END) / COUNT(*), 1) AS cancel_pct
> FROM orders o
> JOIN customers c ON c.customer_id = o.customer_id
> GROUP BY c.city;
> ```
> Kết quả: Đà Nẵng **50.0%**, HCM và Hà Nội 0%. Lại là `SUM(CASE ...)`.

### Bài 15 — Khách đã mua **cả** Electronics **lẫn** Books

> [!success]- Đáp án
> ```sql
> SELECT o.customer_id
> FROM orders o
> JOIN order_items oi ON oi.order_id = o.order_id
> JOIN products p     ON p.product_id = oi.product_id
> WHERE o.status = 'completed'
>   AND p.category IN ('Electronics', 'Books')
> GROUP BY o.customer_id
> HAVING COUNT(DISTINCT p.category) = 2;
> ```
> Kết quả: **1, 2**.
> Sai hay gặp: `WHERE category = 'Electronics' AND category = 'Books'` — một dòng không thể có hai giá trị, ra rỗng.

### Bài 16 — Doanh thu cộng dồn theo ngày

> [!success]- Đáp án
> ```sql
> WITH d AS (
>     SELECT o.order_date, SUM(oi.quantity * oi.unit_price) AS rev
>     FROM orders o
>     JOIN order_items oi ON oi.order_id = o.order_id
>     WHERE o.status = 'completed'
>     GROUP BY o.order_date
> )
> SELECT order_date, rev,
>        SUM(rev) OVER (ORDER BY order_date
>                       ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_total
> FROM d;
> ```
> Dòng cuối: **4710** (= 1660 + 710 + 1190 + 1150, khớp bài 9 — tự kiểm chéo như vậy là thói quen tốt).
> Vì sao ghi `ROWS` tường minh → note 02 mục 3.3.

### Bài 17 — Đếm số đơn mỗi khách sau khi đã join `order_items` (bắt lỗi fan-out)

Có người viết:

```sql
SELECT o.customer_id, COUNT(o.order_id)
FROM orders o JOIN order_items oi ON oi.order_id = o.order_id
GROUP BY o.customer_id;
```

Kết quả sai ở đâu, sửa thế nào?

> [!success]- Đáp án
> Khách 1 ra **5**, khách 2 ra **6** — nhưng mỗi người thật ra chỉ có **3 đơn**.
> Join sang `order_items` làm mỗi đơn nhân lên theo số món → **fan-out**.
> Sửa nhanh: `COUNT(DISTINCT o.order_id)`. Sửa đúng bản chất: **gom trước rồi mới join**, hoặc đừng join bảng không cần.
> Giải thích đầy đủ → note 02 mục 6.

### Bài 18 — Khách quay lại mua trong vòng 30 ngày sau đơn hoàn thành đầu tiên

> [!success]- Đáp án
> ```sql
> WITH f AS (
>     SELECT customer_id, MIN(order_date) AS first_date
>     FROM orders
>     WHERE status = 'completed'
>     GROUP BY customer_id
> )
> SELECT f.customer_id, f.first_date
> FROM f
> WHERE EXISTS (
>     SELECT 1 FROM orders o
>     WHERE o.customer_id = f.customer_id
>       AND o.status = 'completed'
>       AND o.order_date >  f.first_date
>       AND o.order_date <= f.first_date + 30      -- SQL Server: DATEADD(day, 30, f.first_date)
> );
> ```
> Kết quả: **1** (10/01 → 02/02) và **2** (25/01 → 20/02). Đây là dạng **retention** — rất hay gặp ở bài DE/analytics.

## 🔴 Nâng cao

### Bài 19 — Đếm nhân viên **không** quản lý ai

Chạy thử câu này trước, giải thích kết quả:

```sql
SELECT COUNT(*) FROM employees
WHERE emp_id NOT IN (SELECT manager_id FROM employees);
```

> [!success]- Đáp án
> Ra **0** — sai. `manager_id` có `NULL` (An, Hà, Minh) → `x NOT IN (1, 2, 5, NULL)` là `UNKNOWN` với **mọi** dòng.
> ```sql
> SELECT COUNT(*) FROM employees e
> WHERE NOT EXISTS (
>     SELECT 1 FROM employees x WHERE x.manager_id = e.emp_id
> );
> ```
> Đúng: **6**. Chi tiết → note 02 mẫu ⑥.

### Bài 20 — `LEFT JOIN` bị biến thành `INNER JOIN`

Liệt kê **mọi** khách 3 và 5 kèm đơn `completed` của họ (không có đơn thì vẫn hiện tên). Câu dưới sai chỗ nào?

```sql
SELECT c.name, o.order_id
FROM customers c
LEFT JOIN orders o ON o.customer_id = c.customer_id
WHERE o.status = 'completed' AND c.customer_id IN (3, 5);
```

> [!success]- Đáp án
> Chỉ ra **Phúc 108** — mất Quân. Điều kiện trên bảng bên phải phải nằm trong `ON`:
> ```sql
> SELECT c.name, o.order_id
> FROM customers c
> LEFT JOIN orders o
>        ON o.customer_id = c.customer_id
>       AND o.status = 'completed'
> WHERE c.customer_id IN (3, 5);
> ```
> Đúng: **Phúc 108, Quân NULL**. Điều kiện trên bảng **bên trái** (`c.customer_id`) thì để ở `WHERE` là đúng.

### Bài 21 — Khử trùng lặp và upsert (bài "đúng chất DE")

**a)** Trong một bảng staging copy từ `customers`, xoá các dòng trùng `email`, giữ dòng có `customer_id` nhỏ nhất.
**b)** Nạp dữ liệu mới vào bảng `dim_product` sao cho **chạy lại nhiều lần không bị trùng**: sản phẩm đã có thì cập nhật giá, chưa có thì thêm.

> [!success]- Đáp án
> ```sql
> -- a) Dedup — Postgres
> CREATE TEMP TABLE stg_customers AS SELECT * FROM customers;
>
> DELETE FROM stg_customers s
> USING (
>     SELECT customer_id,
>            ROW_NUMBER() OVER (PARTITION BY email ORDER BY customer_id) AS rn
>     FROM stg_customers
>     WHERE email IS NOT NULL
> ) d
> WHERE s.customer_id = d.customer_id
>   AND d.rn > 1;
> -- → xoá đúng 1 dòng (customer_id 6)
>
> -- SQL Server có cách gọn: xoá thẳng qua CTE
> -- WITH d AS (SELECT *, ROW_NUMBER() OVER (PARTITION BY email ORDER BY customer_id) rn
> --            FROM stg_customers WHERE email IS NOT NULL)
> -- DELETE FROM d WHERE rn > 1;
>
> -- b) Chuẩn bị: bảng đích và bảng nguồn (dữ liệu mới về)
> CREATE TEMP TABLE dim_product AS SELECT product_id, name, price FROM products;
> ALTER TABLE dim_product ADD PRIMARY KEY (product_id);
> CREATE TEMP TABLE src (product_id INT, name TEXT, price NUMERIC);
> INSERT INTO src VALUES (3, 'Earbuds', 80), (9, 'Lamp', 25);
>
> -- Upsert — MERGE (SQL Server, Postgres ≥ 15)
> MERGE INTO dim_product t
> USING src s ON t.product_id = s.product_id
> WHEN MATCHED THEN
>     UPDATE SET price = s.price
> WHEN NOT MATCHED THEN
>     INSERT (product_id, name, price) VALUES (s.product_id, s.name, s.price);
>
> -- Postgres cách phổ biến hơn
> INSERT INTO dim_product (product_id, name, price)
> VALUES (3, 'Earbuds', 90), (8, 'Chair', 150)
> ON CONFLICT (product_id) DO UPDATE
>     SET name = EXCLUDED.name, price = EXCLUDED.price;
> ```
> **Câu nói kèm:** *"Job ETL có thể bị chạy lại do lỗi hoặc retry, nên em dùng MERGE/upsert để load là idempotent — chạy 1 lần hay 3 lần kết quả như nhau."*

### Bài 22 — Kiểm tra chất lượng dữ liệu

Viết các câu kiểm tra: số dòng, số `NULL` ở `email`, số `email` khác nhau, và `order_items` nào trỏ tới sản phẩm không tồn tại.

> [!success]- Đáp án
> ```sql
> SELECT COUNT(*)                AS total,
>        COUNT(email)            AS has_email,
>        COUNT(*) - COUNT(email) AS null_email,
>        COUNT(DISTINCT email)   AS distinct_email
> FROM customers;
> -- → 6 | 5 | 1 | 4   → có 1 NULL và 1 cặp trùng
>
> -- Orphan: khoá ngoại "mồ côi"
> SELECT oi.*
> FROM order_items oi
> LEFT JOIN products p ON p.product_id = oi.product_id
> WHERE p.product_id IS NULL;
> -- → 0 dòng (FK đã chặn), nhưng ở kho dữ liệu thường KHÔNG có FK → phải tự kiểm
> ```
> Bốn con số `total / non-null / null / distinct` là bộ kiểm tra đầu tiên nên chạy trên **mọi** bảng mới nhận về.

---

## Còn lại: đã có trong note 02

Mấy dạng này **chắc chắn nên luyện** nhưng đã viết kỹ ở [[Job Fundamentals 02 - SQL nâng cao]], không lặp lại:

- Dòng mới nhất mỗi nhóm (`ROW_NUMBER` + `rn = 1`) — **câu đã trượt ở Home Credit**
- Chuỗi ngày liên tiếp (gap & island)
- Sessionization
- Moving average loại trừ dòng hiện tại

---

# E — Lịch 7 buổi

Theo đúng luật của [[20_KE_HOACH_Job_Fundamentals]]: **sàn 20 phút**, dừng ở chỗ trọn vẹn.

| Buổi | Làm | Xong khi |
|---|---|---|
| 1 | Dựng schema mục C · bài 1–4 | Chạy ra đúng kết quả không mở đáp án |
| 2 | Bài 5–8 · nói lại A1, A2, A3 | Nói được `DELETE/TRUNCATE/DROP` trong 30 giây |
| 3 | Bài 9–12 · đọc mục B | Viết lại bài 9 bằng cú pháp SQL Server |
| 4 | Bài 13–16 · nói lại A4, A5 | Giải thích 3NF bằng ví dụ `employees/departments` |
| 5 | Bài 17–20 · nói lại A6 | Tự giải thích được vì sao bài 19 ra 0 |
| 6 | Bài 21–22 · nói lại A7–A10 | Nói được SCD type 2 và vì sao cần idempotent |
| 7 | Note 02 mẫu ①④⑤ · làm lại bài sai nhiều nhất | Gõ mẫu ① không do dự |

> [!tip] Câu hỏi tự vấn trước khi viết bất kỳ query nào
> **"Một dòng kết quả đại diện cho cái gì?"** — trả lời xong câu này thì phần lớn lỗi fan-out, `GROUP BY` sai, `COUNT` sai tự biến mất.
> Và nói câu này **thành tiếng** khi phỏng vấn — người phỏng vấn nghe được cách mình nghĩ, không chỉ thấy đáp án.

---

## Liên quan

- [[Job Fundamentals 02 - SQL nâng cao]]
- [[Job Fundamentals 01 - Apache Spark]]
- [[20_KE_HOACH_Job_Fundamentals]]
