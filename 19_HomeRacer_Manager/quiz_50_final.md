---
tags: [project, job-hunt, interview, data-engineer, home-credit, quiz]
status: active
created: 2026-08-10
event: Department Manager interview — 2026-08-11
---

# 50 câu tổng hợp — vòng Manager

> Bao trọn những gì đã ôn cho vòng này: project Lichess, đề fraud AC, streaming & failure, lưu trữ, modeling & SQL, và phán đoán nghề nghiệp.
> Đáp án + giải thích ở cuối. Đáp án phân bố đều A/B/C/D.
> Đây là vòng **Q&A nói**, nên với mỗi câu sai hãy tự hỏi thêm: *"nếu bị hỏi câu này, mình sẽ NÓI thế nào?"*

---

## PHẦN A — Project Lichess (1-12)

**1.** File dump `.pgn.zst` khiến Spark chỉ chạy được một task, vì:
- A. File quá lớn so với bộ nhớ executor
- ==B. Định dạng nén zstd không splittable nên không chia được theo khoảng byte==
- C. Spark không hỗ trợ đọc định dạng PGN
- D. Cluster không đủ node

**2.** Bước shred phải cắt tại ranh giới ván cờ, vì:
- A. Để mỗi mảnh có kích thước bằng nhau
- B. Để nén tốt hơn
- C. Vì Spark yêu cầu như vậy
- ==D. Vì một ván PGN trải trên nhiều dòng — cắt giữa chừng làm hỏng ván ở cả hai mảnh==

**3.** Shard được ghi ra dạng `.gz`, cũng không splittable. Điều này có tái tạo vấn đề cũ không?
- ==A. Không — bài toán đã đổi từ một file lớn thành N file, mỗi file đọc trọn bởi một task==
- B. Có — vẫn không chia được nên vẫn chậm
- C. Có, trừ khi đổi sang bzip2
- D. Không xác định được nếu chưa đo

**4.** Bước shred chạy nhanh vì:
- A. Nó chạy trên spot node
- B. Nó dùng nhiều executor
- ==C. Nó chỉ giải nén, không phân tích nội dung — parse mới là phần đắt==
- D. File đã được cache sẵn

**5.** Con số ~30.000 ván mỗi shard nên được giải thích thế nào?
- A. Là con số tối ưu tuyệt đối cho Spark
- ==B. Là hệ quả của việc nhắm ~150MB mỗi shard, vùng kích thước partition Spark thông thường==
- C. Là số ván trung bình mỗi ngày trên Lichess
- D. Được chọn ngẫu nhiên rồi giữ nguyên

**6.** Trong `build_training_set`, `rowsBetween(unboundedPreceding, -1)` có tác dụng:
- ==A. Loại ván hiện tại khỏi lịch sử, chống data leakage==
- B. Giới hạn cửa sổ còn một dòng
- C. Sắp xếp ván theo thời gian
- D. Bỏ qua ván đầu tiên của mỗi người chơi

**7.** Nếu tính lịch sử người chơi mà gộp cả các ván sau, hậu quả là:
- A. Job chạy chậm hơn
- B. Kết quả không đổi vì trung bình vẫn thế
- C. Model báo lỗi khi train
- ==D. Model học từ thông tin không tồn tại lúc dự đoán — đẹp lúc train, vô dụng lúc chạy thật==

**8.** Job Flink báo RUNNING, đọc Kafka bình thường, nhưng Redis trống. Nguyên nhân:
- A. Redis hết bộ nhớ
- B. Kafka topic rỗng
- ==C. `MapFunction` ghi Redis không có sink phía sau nên bị optimizer cắt khỏi execution graph==
- D. Sai cấu hình kết nối Redis

**9.** Bài học rút ra từ bug đó là:
- ==A. Lỗi nguy hiểm nhất là lỗi chạy bình thường nhưng không có tác dụng — không có exception để bắt==
- B. Nên dùng Spark thay vì Flink
- C. Phải luôn bật checkpointing
- D. Redis không phù hợp làm sink

**10.** `mode("overwrite")` mặc định của Spark khi ghi bảng Delta phân vùng:
- A. Chỉ ghi đè partition có trong DataFrame
- ==B. Xoá toàn bộ bảng rồi ghi lại — làm mất dữ liệu các partition khác==
- C. Báo lỗi nếu bảng đã tồn tại
- D. Thêm dữ liệu vào cuối bảng

**11.** Trong job Flink, thuật toán Welford được dùng thay vì cộng dồn `sum` và `sum²` vì:
- A. Nó chạy nhanh hơn
- B. Nó tốn ít bộ nhớ hơn đáng kể
- C. Flink không hỗ trợ luỹ thừa
- ==D. Cách ngây thơ mất chính xác số học — trừ hai số lớn gần bằng nhau có thể ra phương sai âm==

**12.** Đường stream trong project chạy khi nào?
- A. Khi DAG `batch_pipeline` được trigger
- B. Sau khi `materialize_redis` chạy xong
- ==C. Liên tục và độc lập với DAG — collector và Flink là deployment thường trực==
- D. Theo lịch cron mỗi giờ

---

## PHẦN B — Đề fraud AC (13-22)

**13.** Lỗ hổng nghiêm trọng nhất của cột `is_fraud` trong đề là:
- ==A. Nhãn được sinh ra từ chính các rule đang bị phê bình, nên kế thừa mọi điểm mù của chúng==
- B. Nhãn bị thiếu ở nhiều dòng
- C. Nhãn không cân bằng
- D. Nhãn ở sai kiểu dữ liệu

**14.** Giao dịch bị **chặn** thì:
- A. Vẫn có nhãn sau vài ngày
- B. Được gán nhãn gian lận tự động
- ==C. Không bao giờ có nhãn, vì nó không xảy ra nên không có chargeback hay khiếu nại==
- D. Được đội review gán nhãn ngay

**15.** Rule velocity theo thành phố mù hoàn toàn với kịch bản nào?
- A. Thẻ bị nhân bản dùng ở hai tỉnh cùng lúc
- ==B. Thẻ trộm dùng ở nhiều cửa hàng trong cùng một thành phố==
- C. Giao dịch số tiền lớn bất thường
- D. Tài khoản mới mở

**16.** Lý do velocity theo tốc độ di chuyển không bắt được thẻ trộm dùng tại chỗ:
- A. Do độ chính xác GPS kém
- B. Do ngưỡng đặt sai
- C. Do thiếu dữ liệu lịch sử
- ==D. Vì kẻ trộm cầm thẻ đi bộ — di chuyển hoàn toàn khả thi, nên rule không có gì để bắt==

**17.** Một seller thông đồng quẹt 40 thẻ khác nhau trong một giờ không bị phát hiện, vì:
- A. Số tiền mỗi giao dịch quá nhỏ
- B. Cửa hàng đã được whitelist
- ==C. Rule keyed theo customer, mà mỗi customer chỉ có một giao dịch==
- D. Cửa sổ một giờ quá ngắn

**18.** Thêm điều kiện về `amount` có sửa được lỗ hổng mù phía seller không?
- ==A. Không — đó là bài toán về trục gom nhóm, không phải về điều kiện lọc==
- B. Có, nếu ngưỡng đủ thấp
- C. Có, kết hợp với velocity
- D. Chỉ với giao dịch trên 10 triệu

**19.** k-means trên lat/lon thô vẫn sai dù đề đã chốt dùng haversine, vì:
- A. Haversine chậm hơn Euclid
- B. Lat/lon cần chuẩn hoá về [0,1] trước
- C. k-means không hỗ trợ dữ liệu địa lý
- ==D. k-means định nghĩa trong không gian Euclid — centroid là trung bình cộng, không hoán đổi metric được==

**20.** Centroid + bán kính giả định cụm hình tròn. Vấn đề với khu buôn bán dọc quốc lộ là:
- A. Bán kính phải lớn hơn
- ==B. Vòng tròn vừa bao thừa vùng trống vừa cắt mất shop thật — không bán kính nào đúng==
- C. Cần tăng số cụm k
- D. Cần dùng toạ độ chính xác hơn

**21.** Với ba hành động BLOCK / REVIEW / ACCEPT, ngưỡng đẩy vào REVIEW nên đặt theo:
- A. Phân vị 95 của điểm rủi ro
- B. Ngưỡng thống kê ba sigma
- ==C. Năng lực xử lý của đội rà soát — vượt quá thì hàng đợi âm thầm thành auto-approve==
- D. Số tiền giao dịch

**22.** Dải REVIEW có một giá trị đặc biệt ngoài việc giảm rủi ro:
- ==A. Nó là nơi duy nhất sinh ra nhãn sạch, ngay lập tức, ở đúng vùng mơ hồ nhất==
- B. Nó giảm tải cho hệ thống streaming
- C. Nó cho phép bỏ qua bước huấn luyện lại
- D. Nó thay thế được kiểm toán

---

## PHẦN C — Streaming & failure (23-32)

**23.** Không đặt key cho message Kafka thì:
- A. Message bị mất
- B. Kafka báo lỗi
- C. Thứ tự toàn topic được đảm bảo
- ==D. Message rải luân phiên, event của cùng thực thể văng ra nhiều partition và mất thứ tự==

**24.** Kafka đảm bảo thứ tự message ở phạm vi:
- A. Toàn bộ topic
- ==B. Trong từng partition==
- C. Trong từng consumer group
- D. Toàn cluster nếu bật cấu hình

**25.** Với quyết định chặn giao dịch tại chỗ, dùng sliding window có nhược điểm gì?
- A. Cửa sổ chỉ phát kết quả tại mốc slide, nên luôn trễ tới một khoảng slide
- B. Cửa sổ không tính được số đếm
- C. Cửa sổ tốn quá nhiều CPU
- D. Cửa sổ không hỗ trợ keyed state

**26.** Giải pháp thay thế phù hợp hơn cho đường quyết định:
- A. Rút ngắn slide xuống 1 giây
- B. Dùng tumbling window
- C. Giữ danh sách timestamp trong keyed state và đếm ngay khi event tới — trễ bằng 0
- D. Chuyển sang Spark Structured Streaming

**27.** At-least-once đạt được bằng:
- A. Commit offset trước khi xử lý
- ==B. Xử lý trước, commit offset sau — nên có thể xử lý lại khi crash==
- C. Two-phase commit
- D. Tắt retry

**28.** Exactly-once nghĩa là:
- A. Message chỉ đi qua code đúng một lần
- B. Hệ thống không bao giờ crash
- C. Retry bị vô hiệu hoá
- ==D. Kết quả cuối như thể mỗi message được xử lý một lần — message vẫn bị xử lý lại sau sự cố==

**29.** Checkpointing bảo vệ được gì và không bảo vệ được gì?
- ==A. Bảo vệ state bên trong job; không bảo vệ những gì job đã ghi ra ngoài==
- B. Bảo vệ cả state lẫn mọi thứ đã ghi ra sink
- C. Chỉ bảo vệ offset Kafka
- D. Bảo vệ khỏi mọi loại lỗi

**30.** Phép ghi nào là idempotent?
- A. `INSERT INTO ledger VALUES (...)`
- B. `balance = balance + 100`
- ==C. `SET balance = 500`==
- D. Cả ba

**31.** Một message lỗi format làm consumer chết lặp lại. Vấn đề nghiêm trọng nhất là:
- A. Mất một bản ghi
- ==B. Pipeline kẹt tại offset đó, mọi message phía sau không được xử lý==
- C. Kafka bị đầy
- D. Consumer group bị rebalance liên tục

**32.** Phân biệt lỗi tạm thời và lỗi vĩnh viễn quan trọng vì:
- A. Lỗi vĩnh viễn nén tốt hơn
- B. Chỉ lỗi tạm thời mới cần ghi log
- C. Lỗi tạm thời cần DLQ
- ==D. Retry một lỗi vĩnh viễn vô hạn chính là cách tạo ra vòng lặp kẹt==

---

## PHẦN D — Lưu trữ & Delta (33-38)

**33.** Delta Lake khác Parquet ở chỗ:
- A. Delta nén tốt hơn
- B. Delta lưu theo dòng, Parquet lưu theo cột
- ==C. Parquet là định dạng file; Delta phủ một transaction log lên trên các file Parquet==
- D. Delta chỉ chạy trên Databricks

**34.** "Bảng Delta ở phiên bản N" được xác định bởi:
- ==A. Replay log từ 0 tới N để cộng dồn tập file đang hoạt động==
- B. Danh sách file có trong thư mục
- C. Metadata trong Hive Metastore
- D. Tên file Parquet

**35.** Trong project, Redis đóng vai trò gì so với Delta trên MinIO?
- A. Nguồn sự thật, Delta chỉ là backup
- B. Nơi lưu trữ dài hạn
- C. Nơi chạy truy vấn phân tích
- ==D. Bản sao phái sinh phục vụ tra cứu nhanh — xoá đi chạy lại materialize là có lại==

**36.** "Tính trước rồi cất vào Redis" đánh đổi cái gì?
- A. Đổi độ chính xác lấy tốc độ
- ==B. Đổi độ tươi lấy độ trễ — giá trị chỉ mới đến lần materialize gần nhất==
- C. Đổi dung lượng lấy tốc độ
- D. Không đánh đổi gì

**37.** Vì sao đường stream ghi thẳng Redis thay vì chờ materialize theo lô?
- A. Vì feature nhịp đánh trong ván đang diễn ra hỏng đi rất nhanh, dữ liệu cũ một ngày là vô nghĩa
- B. Vì Flink không ghi được Delta
- C. Vì Redis rẻ hơn
- D. Vì batch job chạy quá lâu

**38.** `OPTIMIZE` trong Delta dùng để:
- A. Xoá file không còn tham chiếu
- B. Nén dữ liệu mạnh hơn
- C. Gộp nhiều file nhỏ thành file lớn hơn — chữa small file problem
- D. Tạo index

---

## PHẦN E — Modeling & SQL (39-46)

**39.** Báo cáo tỷ lệ trễ hạn theo tỉnh/sản phẩm/tháng. Grain phù hợp cho bảng fact là:
- A. Một dòng một khách hàng
- ==B. Một dòng một khoản vay trong một tháng==
- C. Một dòng một khoản vay
- D. Một dòng một tỉnh một tháng

**40.** Vì sao không chọn grain "một dòng một khoản vay"?
- A. Vì bảng sẽ quá lớn
- B. Vì thiếu khoá ngoại
- C. Vì không join được với dimension
- ==D. Vì chỉ có trạng thái hiện tại, không dựng lại được diễn biến theo từng tháng==

**41.** Khách chuyển tỉnh. Muốn báo cáo lịch sử vẫn tính theo tỉnh **tại thời điểm đó**, cần:
- A. SCD type 2 — thêm dòng mới kèm khoảng hiệu lực thay vì ghi đè
- B. SCD type 1 — ghi đè giá trị mới
- C. Lưu tỉnh trong bảng fact
- D. Không cần làm gì, dimension tự xử lý

**42.** Lấy giao dịch **gần nhất** của mỗi khách, giữ nguyên cả dòng. Cách đúng:
- A. `GROUP BY customer_id ORDER BY transaction_time`
- B. `SELECT DISTINCT customer_id, MAX(transaction_time)`
- C. `ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY transaction_time DESC)` rồi lọc `= 1`
- D. `LIMIT 1` với `ORDER BY`

**43.** Vì sao `GROUP BY` không dùng được cho câu trên?
- A. Vì nó chậm hơn
- B. Vì nó không hỗ trợ ORDER BY
- C. Vì nó cần index
- D. Vì nó gộp các dòng lại — mất thông tin từng giao dịch, chỉ lấy được hàm tổng hợp

**44.** Join `customers` (1 dòng/khách) với `payments` (N dòng/khách) rồi `SUM(credit_limit)`:
- A. Cho kết quả đúng
- B. Bị thổi phồng vì credit_limit lặp lại theo số dòng payment
- C. Bị thiếu vì khách chưa thanh toán bị loại
- D. Báo lỗi kiểu dữ liệu

**45.** Cách xử lý an toàn cho trường hợp trên:
- A. Dùng `SELECT DISTINCT`
- B. Đổi sang `LEFT JOIN`
- C. Gom bảng N về đúng grain của bảng 1 trước, rồi join 1-1
- D. Thêm index vào khoá ngoại

**46.** Trong star schema, bảng nào chứa các số đo để cộng/trung bình?
- A. Fact table
- B. Dimension table
- C. Bridge table
- D. Cả hai như nhau

---

## PHẦN F — Phán đoán & vận hành (47-50)

**47.** Job batch bình thường 20 phút, hôm nay 4 tiếng. Bước kiểm tra ĐẦU TIÊN nên là:
- A. Tăng số executor
- B. Restart job
- C. Đọc lại code
- D. So khối lượng dữ liệu đầu vào hôm nay với những hôm trước

**48.** Trong Spark UI, hầu hết task đã xong nhưng một task vẫn chạy. Đây là dấu hiệu của:
- A. Thiếu bộ nhớ
- B. Data skew — một partition ôm quá nhiều dữ liệu
- C. Lỗi mạng
- D. Sai cấu hình checkpoint

**49.** Đội nghiệp vụ báo con số trên báo cáo sai, nhưng job chạy xanh. Việc đầu tiên nên làm:
- A. Chạy lại pipeline
- B. Kiểm tra log Airflow
- C. Xác nhận xem là bug thật hay là hai bên đang định nghĩa chỉ số khác nhau
- D. Rollback bản deploy gần nhất

**50.** Dịch vụ chấm điểm gian lận timeout. Hướng xử lý hợp lý nhất:
- A. Cho qua nhưng hạ trần số tiền, báo động ngay, gắn cờ rà soát sau — và để đội rủi ro chốt khẩu vị
- B. Chặn toàn bộ giao dịch cho tới khi khôi phục
- C. Cho qua toàn bộ, xử lý sau
- D. Tự động chuyển sang model dự phòng không cần thông báo

---
---

# ĐÁP ÁN & GIẢI THÍCH

**A — Project Lichess**

**1 — B.** zstd dạng stream không cho bắt đầu giải nén từ vị trí byte bất kỳ, mà Spark chia việc theo khoảng byte → một file = một split = một task.

**2 — D.** Một ván PGN trải nhiều dòng. Cắt giữa chừng thì parser không đọc được ván đó ở cả hai mảnh.

**3 — A.** Bài toán đã đổi. Trước là *một* file không chia được; giờ là *N* file, mỗi file đọc trọn bởi một task. Song song đến từ **số lượng file**, không cần splittable nữa.

**4 — C.** Shred chỉ giải nén, không parse. Parse PGN mới là phần tốn. Tách hai việc: một lượt rẻ để chia, rồi song song hoá phần đắt.

**5 — B.** Nói theo **mục tiêu kích thước** (~150MB, vùng partition Spark chuẩn) mạnh hơn nhiều so với "cắt 30k thì tình cờ ra 150MB".

**6 — A.** `-1` nghĩa là tới dòng **trước** dòng hiện tại → loại ván đang xét khỏi lịch sử của chính nó.

**7 — D.** Đây là data leakage. Nguy hiểm vì **chỉ số lúc train rất đẹp** — nó trông như thành công.

**8 — C.** Flink dựng execution graph ngược từ sink; operator không dẫn tới sink nào bị coi là code chết và bị cắt.

**9 — A.** Không có exception để bắt, không có gì để grep. Phải mở job graph mới thấy operator biến mất.

**10 — B.** Chế độ mặc định là `static` → wipe cả bảng. Phải đặt `partitionOverwriteMode=dynamic`.

**11 — D.** Khi phương sai nhỏ so với trung bình, trừ hai số lớn gần bằng nhau làm mất chữ số có nghĩa. Welford tính online, ổn định hơn.

**12 — C.** Collector và Flink là deployment thường trực, **không phải task trong DAG**. Đây là chỗ dễ trả lời sai nếu chỉ nhớ sơ đồ.

**B — Đề fraud**

**13 — A.** Gian lận mà rule chưa từng bắt được thì được gán là sạch. Train trên nhãn đó chỉ học lại chính rule.

**14 — C.** Chặn nó → nó không xảy ra → không có gì xác nhận. Đây là **rejection inference**: dữ liệu train chỉ phản ánh những gì hệ thống cũ cho qua.

**15 — B.** Cùng thành phố thì rule không kích hoạt, dù hai điểm cách nhau 40km và chỉ 5 phút.

**16 — D.** Đây là vấn đề về **tiền đề của rule**, không phải độ phân giải dữ liệu. Tăng độ chính xác GPS không cứu được.

**17 — C.** Mỗi nạn nhân chỉ có một giao dịch → không có gì để so. Cần thêm tổng hợp keyed theo seller.

**18 — A.** Điều kiện lọc và trục gom nhóm là hai thứ khác nhau. Muốn thấy mẫu hình ở thực thể nào thì phải gom nhóm theo thực thể đó.

**19 — D.** Centroid là trung bình cộng, và trung bình cộng là điểm cực tiểu tổng bình phương khoảng cách **Euclid**. Đổi metric thì điểm tối ưu cũng đổi. Sửa: chiếu sang hệ mét, hoặc dùng k-medoids / DBSCAN.

**20 — B.** Sai theo cả hai chiều cùng lúc — nới rộng thì phủ thêm vùng trống, thu hẹp thì cắt mất shop. Vì **hình dạng** sai, không phải kích thước.

**21 — C.** Đây là ràng buộc **vận hành**, không phải thống kê. Rất ít ứng viên nghĩ tới.

**22 — A.** BLOCK không có nhãn, ACCEPT chỉ có nhãn ở vùng đã cho là an toàn. Chỉ REVIEW cho nhãn sạch ở đúng vùng model cần học nhất.

**C — Streaming & failure**

**23 — D.** Không key thì Kafka rải round-robin. Vấn đề không phải "thứ lạ nằm chung" mà là **thứ liên quan bị tách rời**.

**24 — B.** Chỉ trong partition. Không có khái niệm thứ tự toàn topic.

**25 — A.** Cửa sổ chỉ phát khi đóng, nên độ trễ tối đa bằng một khoảng slide. Trong khoảng đó cả đợt tấn công có thể hoàn thành.

**26 — C.** Bỏ timestamp cũ hơn cửa sổ, đếm số còn lại, tính ngay khi event tới. Chính xác, không trễ, state nhỏ.

**27 — B.** Retry khi thiếu ack → không mất nhưng có thể trùng. Đây là mức mặc định thực tế phổ biến nhất.

**28 — D.** Tên chính xác hơn là *effectively-once*. Nói được ý này là dấu hiệu hiểu thật.

**29 — A.** Flink tua ngược được chính nó, **không tua ngược được thế giới bên ngoài**. Sink phải idempotent hoặc transactional.

**30 — C.** Ghi đè thì idempotent; cộng dồn và insert thuần thì không. Đây là ranh giới quyết định chiến lược khôi phục.

**31 — B.** Không phải mất một bản ghi — mà là **kẹt cả luồng**. Hàng triệu message phía sau không bao giờ được xử lý.

**32 — D.** Retry lỗi vĩnh viễn chính là cơ chế tạo ra vòng lặp poison pill. Lỗi tạm thời → retry có backoff; lỗi vĩnh viễn → DLQ ngay.

**D — Lưu trữ & Delta**

**33 — C.** Parquet là định dạng **file**; Delta là định dạng **bảng**. Delta không thay Parquet.

**34 — A.** Bảng được định nghĩa bởi **log**, không phải bởi file có trong thư mục. File không có trong log thì không thuộc về bảng.

**35 — D.** Redis là bản phái sinh. Nói được điều này cho thấy hiểu đúng vai trò từng tầng.

**36 — B.** Nguyên nhân gây cũ là **việc tính trước**, không phải Redis. Đổi Redis sang Cassandra cũng vậy.

**37 — A.** Feature khác nhau hỏng đi với tốc độ khác nhau — đó là lý do một online store có hai nhịp làm tươi.

**38 — C.** `VACUUM` mới là xoá file không tham chiếu (và vacuum quá tay thì mất time travel).

**E — Modeling & SQL**

**39 — B.** Báo cáo cần trạng thái **theo từng tháng** → fact phải có grain theo tháng.

**40 — D.** Một dòng một khoản vay chỉ cho trạng thái hiện tại. Lịch sử đã mất.

**41 — A.** Type 2 thêm dòng mới với khoảng hiệu lực; fact của tháng cũ trỏ tới khoá cũ nên lịch sử giữ nguyên đúng.

**42 — C.** Window function **không gộp dòng** — nó gán số thứ tự cho từng dòng trong nhóm, nên giữ nguyên được cả dòng.

**43 — D.** Sau `GROUP BY` chỉ còn một dòng mỗi khách. `MAX(transaction_time)` cho **thời điểm**, không cho **cả dòng**.

**44 — B.** Fan-out. Khách có 50 payment thì credit_limit bị cộng 50 lần.

**45 — C.** Pre-aggregate về đúng grain rồi join 1-1. `DISTINCT` chỉ che triệu chứng.

**46 — A.** Fact chứa số đo + khoá ngoại; dimension chứa thuộc tính để lọc và nhóm.

**F — Phán đoán & vận hành**

**47 — D.** Rẻ nhất và loại được nguyên nhân phổ biến nhất: nguồn đột nhiên gấp nhiều lần thì job không có lỗi gì cả.

**48 — B.** Một straggler cạnh các task đã xong là dấu hiệu kinh điển của skew.

**49 — C.** Rất nhiều lần không phải bug mà là lệch định nghĩa. Hỏi con số đúng đáng lẽ là bao nhiêu và tính thế nào.

**50 — A.** Không chọn một chiều. Và câu chốt là: **khẩu vị rủi ro không phải quyết định của kỹ sư** — đưa phương án kèm ước lượng chi phí rồi để nghiệp vụ chốt.

---

## Thang tự đánh giá

| Đúng | Ý nghĩa |
|---|---|
| 43-50 | Sẵn sàng |
| 35-42 | Ổn — đọc kỹ giải thích các câu sai |
| < 35 | Tập trung phần sai nhiều nhất, đừng ôn dàn trải |

**Sáu câu quan trọng nhất nếu chỉ nhớ được vài thứ:** 6 (point-in-time), 9 (lỗi im lặng), 18 (trục gom nhóm), 29 (checkpoint không đủ), 30 (ghi đè vs cộng dồn), 42 (window vs GROUP BY).

**Và nhớ:** đây là vòng **nói**. Làm xong quiz, với mỗi câu sai hãy tự hỏi *"nếu bị hỏi, mình sẽ nói thành câu thế nào?"* — biết đáp án và nói ra được là hai chuyện khác nhau.
