---
tags: [project, job-hunt, interview, data-engineer, home-credit, speaking]
status: active
created: 2026-08-10
event: Department Manager interview — 2026-08-11
---

# 16 câu trả lời — bản nói

> Tổng hợp bốn đợt drill. **Đây là bản để ĐỌC TO**, không phải để học thuộc.
> Mục tiêu: cho miệng chạy qua một lần, để lúc bị hỏi thì nó ra được.
> Chữ **in đậm** là câu chốt — nếu quên hết thì nhớ mấy câu đó.

---

# ĐỢT 1 — Mở đầu

## ① "Kể về project feature store trên dữ liệu cờ vua"

*(~90 giây — mở ngắn, hai biển chỉ đường, shred có nhịp riêng)*

> "Đây là một feature store trên dữ liệu cờ vua công khai của Lichess, có hai đường: batch xử lý lịch sử, streaming xử lý ván đang diễn ra, và trên đó là một model nhẹ phát hiện người chơi gian lận.
>
> Sở dĩ chọn cờ vua là vì lúc tìm đề tài em thấy toàn recsys, dữ liệu bệnh viện, thời tiết — không có gì hứng thú. Rồi về quê chơi cờ với em trai thì nghĩ ra. May là Lichess mở toàn bộ dữ liệu, ba mươi triệu ván mỗi tháng, hơn một trăm năm mươi gigabyte khi bung ra.
>
> **Em nói đường batch trước.**
>
> Dữ liệu thô vào MinIO ở tầng bronze, giữ nguyên không đụng gì. Rồi Spark parse lên silver, mỗi ván một dòng.
>
> Chỗ này em vấp một vấn đề đáng nhớ. File nén zstd **không splittable**, nên Spark chỉ chạy được một task — chạy thử thì mất khoảng sáu mươi tới bảy mươi tiếng cho một tháng dữ liệu, cả cluster ngồi không. Em thêm một bước cắt file: đọc một lượt, chỉ giải nén chứ không parse, cắt tại ranh giới ván thành các mảnh khoảng một trăm năm mươi megabyte. Sau đó còn khoảng bốn phút. **Hạ tầng không đổi — chỉ là làm cho dữ liệu chia được.**
>
> Từ silver lên gold em đổi grain, từ một dòng một ván thành một dòng một người chơi, ra được hồ sơ từng người.
>
> Và phần em thấy tinh tế nhất là lúc tạo tập huấn luyện. Với mỗi ván, lịch sử của người chơi **chỉ được lấy từ các ván trước đó** — nếu lỡ gộp cả ván sau thì model nhìn thấy tương lai, lúc train rất đẹp nhưng chạy thật thì vô dụng. Cái đó gọi là data leakage, và **nó đúng bằng bài toán tính điểm rủi ro khách hàng: feature tại thời điểm duyệt vay chỉ được dùng thông tin có tại lúc đó.**
>
> **Đường stream thì ngắn hơn.**
>
> Lichess có một luồng phát trực tiếp ván đang được chiếu. Em đọc luồng đó, đẩy từng nước vào Kafka, đánh khoá theo mã ván để các nước của cùng một ván giữ đúng thứ tự. Flink đọc ra — em chọn Flink vì cần **giữ state theo từng ván**: luồng dữ liệu không cho biết một nước nghĩ bao lâu, phải nhớ đồng hồ của nước trước rồi suy ra. Từ đó tính độ lệch chuẩn thời gian mỗi nước trên cửa sổ trượt, ghi vào Redis. **Độ lệch chuẩn thấp nghĩa là nhịp đều như máy — bắt được tín hiệu gian lận mà không cần chạy engine cờ.**
>
> Hai đường gặp nhau ở Redis, là online store; Delta trên MinIO là offline store. Toàn bộ chạy trên GKE, Terraform dựng hạ tầng, Airflow điều phối batch.
>
> **Về phạm vi:** em làm song song với khoá luận nên dừng ở mức chứng minh kiến trúc — verify trên một tháng có annotation thật, còn lần chạy full-scale là bước cuối."

⚠️ **Đừng nói** *"em dùng Flink để cho latency thấp"* — họ sẽ hỏi *"cần latency thấp để làm gì?"* và bạn không có đáp án tốt.

## ② "Vì sao Spark không tự chia file được?"

> "Không phải Spark không chia được, mà là **file nén zstd không splittable** — không thể bắt đầu giải nén từ một vị trí byte bất kỳ ở giữa. Mà Spark chia việc theo khoảng byte, nên gặp file không chia được thì nó coi cả file là một đơn vị: một file, một task, một máy.
>
> Em sửa bằng một bước đọc một lượt, **chỉ giải nén chứ không parse**, rồi cắt thành nhiều mảnh. Phải cắt **tại ranh giới ván** vì một ván PGN trải trên nhiều dòng — cắt giữa chừng thì hỏng ở cả hai mảnh.
>
> Em nhắm khoảng một trăm năm mươi megabyte mỗi mảnh, là vùng kích thước partition Spark thông thường, tính ra khoảng ba mươi nghìn ván. Chạy thẳng thì mất sáu mươi tới bảy mươi tiếng; cắt ra rồi còn khoảng bốn phút.
>
> Và shred nhanh được là vì nó **chỉ giải nén, không phân tích nội dung** — parse mới là phần đắt. Tách hai việc ra: một lượt rẻ để chia, rồi mới song song hoá phần đắt."

## ③ "Khi nào chọn batch, khi nào chọn streaming?"

> "Em nghĩ câu hỏi quyết định là: **sau khi có kết quả thì ai hành động, và việc đó phải xảy ra nhanh cỡ nào.**
>
> Ví dụ chặn giao dịch gian lận tại điểm bán — quyết định phải xong **trước khi giao dịch hoàn tất**. **Kịp thì mình ngăn chặn được; trễ thì chỉ còn phát hiện để điều tra sau.** Cùng một con số nhưng giá trị nghiệp vụ thấp hơn hẳn, vì tiền đã đi rồi. Cái đó bắt buộc streaming.
>
> Ngược lại, nếu là danh sách khách rủi ro để đội thu hồi nợ gọi điện vào sáng hôm sau, thì cửa sổ hành động là hàng giờ. Batch qua đêm thừa đủ, mà lại đơn giản và rẻ hơn nhiều — streaming ở đó là trả tiền cho độ trễ không ai dùng tới."

---

# ĐỢT 2 — Đào sâu

## ④ "Giờ nghĩ kỹ lại, em cải thiện hệ thống decoy đó thế nào?"

> "Hôm đó em mới nêu được lỗ hổng, chưa nghĩ tới cách chữa. Giờ em thấy có ba tầng.
>
> **Tầng thứ nhất — cần làm rõ cơ chế trước.** Em muốn hỏi lại: sau khi rule kích hoạt và chặn một giao dịch thì **state có được reset không**? Nếu có thì đó chính là lỗ hổng — giao dịch nhỏ đốt sạch ràng buộc rồi giao dịch lớn đi qua. Nếu giao dịch bị chặn vẫn được ghi vào state thì tấn công này khó hơn, nhưng lại mở ra chiều ngược lại: **kẻ gian cố tình làm bị chặn để đầu độc state của nạn nhân** — biến cơ chế phòng thủ thành cách quấy rối khách hàng thật.
>
> **Tầng thứ hai — đưa số tiền vào.** Nếu ngưỡng tính theo **tổn thất kỳ vọng**, tức là rủi ro nhân số tiền, thì giao dịch mồi nhỏ không đủ chạm ngưỡng nên không kích hoạt được phòng thủ, tức là không đốt được gì. Nhưng nói cho công bằng thì nó không triệt tiêu đòn tấn công — kẻ gian có thể làm mồi to hơn. Chỉ là **mồi không còn miễn phí nữa**.
>
> **Tầng thứ ba, và em nghĩ đây mới là điểm chính.** Bất kỳ ngưỡng cố định nào cũng tạo ra một **ranh giới học được**. Nên ngoài việc vá từng lỗ, em sẽ **giám sát phân phối hành vi quanh ngưỡng**. Nếu ngưỡng là năm giao dịch một giờ mà dữ liệu bắt đầu **dồn cụm ở mức bốn**, thì chính cụm đó là bằng chứng có người đang tối ưu ngược lại luật của mình. **Hình dạng phân phối gần ngưỡng tự nó trở thành một tín hiệu phát hiện.**"

## ⑤ "Idempotency là gì, có ví dụ thật không?"

> "Idempotency là chạy lại một job cho ra **cùng một kết quả**, không nhân đôi dữ liệu. Nó là nền tảng của mọi cơ chế retry và backfill — có nó thì job lỗi cứ chạy lại, không có thì mỗi lần lỗi là một lần hồi hộp.
>
> Em gặp đúng chuyện này trong project. Em ghi bảng Delta phân vùng theo tháng, dùng `mode overwrite` mặc định của Spark. Chạy cho tháng mới xong thì phát hiện **dữ liệu tháng cũ biến mất sạch**. Hoá ra mặc định của Spark hiểu 'overwrite' là **xoá cả bảng** rồi ghi lại, chứ không phải thay thế đúng phần mình đang ghi. Chuyển sang `partitionOverwriteMode` dynamic thì mới chỉ ghi đè partition của tháng đang chạy.
>
> Bài học em rút ra là **idempotency phải được thiết kế, nó không tự có** — và mặc định của công cụ thường không phải cái mình tưởng.
>
> Còn cách nhận biết nhanh thì em hay dùng một phép thử: **ghi đè thì idempotent, cộng dồn thì không.** `SET balance = 500` chạy mười lần vẫn ra 500; `balance = balance + 100` thì thành cộng một nghìn. Nhìn phép ghi là biết ngay mình sẽ phải trả giá bao nhiêu cho phần khôi phục."

## ⑥ "Job 20 phút hôm nay chạy 4 tiếng — em kiểm tra gì?"

> "**Em đi từ chỗ rẻ nhất tới chỗ đắt nhất.**
>
> **Đầu tiên là dữ liệu đầu vào.** So số dòng và dung lượng hôm nay với mấy hôm trước. Nếu nguồn đột nhiên gấp mười lần thì job không có lỗi gì cả, chỉ là nhiều việc hơn.
>
> **Thứ hai, mở Spark UI xem phân bố task.** Nếu gần hết task đã xong mà còn **một task vẫn chạy** thì đó là **data skew** — một partition ôm quá nhiều dữ liệu. Hay gặp khi group theo một khoá có giá trị nóng, ví dụ một cửa hàng chiếm bốn mươi phần trăm giao dịch.
>
> **Thứ ba, số lượng và kích thước file.** Nếu upstream bắt đầu sinh ra hàng nghìn file nhỏ thì chi phí mở file át chi phí đọc. Ngược lại nếu gộp thành một file lớn không splittable thì mất song song — em từng gặp đúng chuyện đó với file zstd.
>
> **Thứ tư là tài nguyên.** Có job khác giành CPU không, executor có OOM rồi restart không, node spot có bị thu hồi không.
>
> **Thứ năm là code.** So với lần deploy gần nhất — ai đó vừa thêm một join hay groupBy mới thì đó là nghi phạm đầu tiên, vì shuffle thường là bước đắt nhất."

## ⑦ "Lấy giao dịch gần nhất của mỗi khách — em làm thế nào?"

> "Em dùng **window function** — `ROW_NUMBER` phân vùng theo `customer_id`, sắp theo `transaction_time` giảm dần, rồi lọc lấy những dòng có số thứ tự bằng một.
>
> Lý do không dùng `GROUP BY` là vì **`GROUP BY` gộp các dòng lại** — sau khi gộp thì em chỉ còn một dòng mỗi khách và mất hết thông tin của từng giao dịch. Em lấy được `MAX(transaction_time)` nhưng không lấy được số tiền của đúng giao dịch đó.
>
> **Window function thì không gộp** — nó gán thêm một số thứ tự cho từng dòng trong nhóm, nên em giữ nguyên được cả dòng."

```sql
SELECT * FROM (
    SELECT *, ROW_NUMBER() OVER (
        PARTITION BY customer_id ORDER BY transaction_time DESC) AS rn
    FROM transactions
) t WHERE rn = 1;
```

---

# ĐỢT 3 — Modeling & phán đoán

## ⑧ "Báo cáo tỷ lệ trễ hạn theo tỉnh / sản phẩm / tháng"

> "Trước khi thiết kế bảng em muốn làm rõ hai chỗ.
>
> **Thứ nhất, 'trễ hạn' định nghĩa thế nào?** Trễ một ngày hay trễ ba mươi ngày? Hai định nghĩa cho ra hai con số rất khác nhau.
>
> **Thứ hai, 'tỉnh' là của khách hàng hay của cửa hàng phát sinh khoản vay?** Hai cái này không phải lúc nào cũng trùng.
>
> Giả sử là trễ ba mươi ngày và tỉnh của khách. Em làm **star schema**.
>
> **Grain của bảng fact là một dòng cho một khoản vay trong một tháng** — snapshot hằng tháng. Lý do là báo cáo cần trạng thái *theo từng tháng*; nếu grain là một dòng một khoản vay thì em chỉ có trạng thái hiện tại, không dựng lại được diễn biến.
>
> Mỗi dòng fact có khoá tới khách, khoá tới sản phẩm, tháng, cờ đánh dấu tháng đó có trễ không, và dư nợ. Dimension gồm khách hàng — chứa tỉnh, tuổi, phân khúc thu nhập — sản phẩm vay, và bảng thời gian.
>
> Tỷ lệ trễ hạn khi đó là tổng cờ trễ chia cho số dòng, gom theo tỉnh, sản phẩm, tháng.
>
> Còn một chỗ nữa: **nếu khách chuyển tỉnh thì báo cáo lịch sử tính theo tỉnh cũ hay mới?** Nếu cần đúng theo thời điểm thì dimension khách phải là **kiểu 2** — thêm dòng mới kèm khoảng hiệu lực thay vì ghi đè. Cái này phải chốt với đội rủi ro vì nó đổi cả con số."

## ⑨ "Dịch vụ chấm điểm timeout — chặn hết hay cho qua hết?"

> "Em nghĩ **cả hai lựa chọn thuần đều sai**, nên em tách vấn đề ra.
>
> **Chặn hết** thì an toàn về gian lận, nhưng nó **dừng toàn bộ kinh doanh**. Mọi cửa hàng đối tác không bán được hàng — sự cố kỹ thuật của mình biến thành sự cố doanh thu của họ.
>
> **Cho qua hết** thì kinh doanh chạy, nhưng mở toang cửa. Và điểm đáng lo hơn: **kẻ gian có động cơ chủ động gây quá tải** để tạo ra đúng tình huống đó. Mình vừa biến một điểm yếu kỹ thuật thành một vector tấn công.
>
> Hướng em chọn là **cho qua nhưng suy giảm có kiểm soát**: vẫn duyệt, nhưng **hạ trần số tiền**, báo động ngay, và **gắn cờ toàn bộ giao dịch trong khoảng đó** để rà lại sau. Giao dịch nhỏ vẫn chạy, phần rủi ro lớn bị chặn.
>
> Thêm một chi tiết: nếu dịch vụ đang hỏng thì em dùng **circuit breaker** — sau vài lần lỗi liên tiếp thì ngừng gọi và trả về phương án dự phòng ngay, thay vì để **mọi** giao dịch đứng chờ hết timeout. Không có nó thì một dịch vụ hỏng kéo chậm cả luồng duyệt.
>
> Nhưng chốt cuối cùng **không phải quyết định của kỹ sư**. Đây là câu hỏi về **khẩu vị rủi ro** — chấp nhận mất bao nhiêu tiền gian lận để đổi lấy việc không dừng kinh doanh. Em đưa ra hai ba phương án kèm ước lượng chi phí, rồi để đội rủi ro chốt."

## ⑩ "Làm lại project thì khác gì?"

> "Có ba thứ, ở ba tầng khác nhau.
>
> **Thứ nhất là thiết kế.** Bảng feature ở tầng gold và tập huấn luyện của em được tính **độc lập** từ cùng một nguồn. Cùng một khái niệm được cài đặt ở hai chỗ, và chúng có thể lệch nhau — mà **tránh đúng sự lệch đó lại là lý do feature store tồn tại**. Làm lại em sẽ giữ một bảng feature **có phiên bản theo thời gian** làm nguồn duy nhất: tập huấn luyện lấy từ đó bằng point-in-time join, còn online store chỉ là những dòng mới nhất. Tốn dung lượng hơn nhưng mỗi feature chỉ tính một lần.
>
> **Thứ hai là quy trình, và em nghĩ đây là bài học lớn hơn.** Em chọn một tháng nhỏ làm dữ liệu phát triển cho nhanh, nhưng tháng đó gần như không có chú thích engine — nên toàn bộ logic tính độ chính xác **chưa từng chạy thật một lần nào mà không có lỗi nào báo**. Làm lại em sẽ **đo độ phủ của dữ liệu ngay từ đầu**, trước khi viết logic. Mất nửa buổi, tiết kiệm vài ngày.
>
> **Thứ ba là bật checkpointing và state TTL cho Flink ngay từ đầu**, thay vì để thành nợ kỹ thuật."

## ⑪ "Vì sao Home Credit?"

⚠️ **Câu này phải tự viết.** Khung ba phần:

**① Vì sao loại công ty này** — bạn từng làm ở một công ty nhỏ, môi trường tệ, **không học được gì**. Nên tìm nơi có quy trình, có người giỏi hơn để học, có hệ thống đủ lớn để bài toán thật xuất hiện.

**② Vì sao Home Credit cụ thể** — *(tự điền — tìm MỘT thứ thật, đừng bịa ba thứ)*

**③ Bằng chứng từ chính buổi AC** — bạn đã ngồi làm đề của họ ba tiếng. Nói được rằng bài toán gian lận BNPL là loại vấn đề bạn muốn làm — đó là bằng chứng cụ thể mà rất ít ứng viên có.

**Tránh:** "công ty lớn", "môi trường tốt", "muốn học hỏi".
**Nếu hỏi có nộp nhiều chỗ không:** trả lời thật là có. Điều đáng nói là **vì sao chỗ này khác**.

---

# ĐỢT 4 — Chốt

## ⑫ "Delta khác gì Parquet?"

> "Parquet là **định dạng file** — quy định cách lưu dữ liệu trên đĩa, theo cột, nén tốt. Delta là **định dạng bảng** — nó không thay Parquet mà **phủ một cuốn sổ giao dịch lên trên** các file Parquet.
>
> Cụ thể là một thư mục log ghi từng lần commit: lần này file nào được thêm, file nào bị gỡ, schema là gì. Và điểm cốt lõi: **bảng được định nghĩa bởi cuốn sổ đó, không phải bởi những file đang nằm trong thư mục.**
>
> Từ đó có bốn thứ Parquet thuần không có. **Nguyên tử** — ghi xong hết rồi mới commit, người đọc không thấy trạng thái nửa vời. **Sửa và xoá dòng** — ghi file mới rồi commit 'gỡ cũ, thêm mới' nguyên tử. **Time travel** — đọc lại bảng ở phiên bản bất kỳ. **Bỏ qua dữ liệu không cần đọc** — log lưu min/max từng cột cho từng file.
>
> Trong project em thì thứ dùng nhiều nhất là chế độ ghi đè theo phân vùng — nó là cái làm cho việc chạy lại pipeline trở nên an toàn."

## ⑬ "Báo cáo sai nhưng job chạy xanh — xử lý thế nào?"

> "Câu đầu tiên em hỏi là: **con số đó sai, hay định nghĩa khác nhau?** Rất nhiều lần không phải bug — mà là bên nghiệp vụ hiểu chỉ số theo một cách, pipeline tính theo cách khác. Em sẽ hỏi họ **con số đúng đáng lẽ là bao nhiêu và tính thế nào**. Nếu là lệch định nghĩa thì sửa tài liệu, không sửa code.
>
> Giả sử sai thật. Em **khoanh vùng trước**: sai ở tất cả các dòng hay chỉ một nhóm? **Sai từ bao giờ** — xác định được ngày bắt đầu sai thì có ngay đầu mối để so với lịch deploy hoặc thay đổi phía nguồn.
>
> Rồi **lần ngược theo lineage**: kiểm tra tầng cuối, lùi lên tầng trước, cho tới khi tìm được **tầng đầu tiên mà số đã sai rồi**. Bug nằm ở bước ngay sau tầng đó.
>
> Nghi phạm số một là **join bị fan-out** — phổ biến nhất khi tổng bị thổi phồng. Rồi tới nạp trùng dữ liệu, hoặc phía nguồn đổi ý nghĩa một cột mà không báo.
>
> Và sau khi sửa xong em hỏi thêm: **vì sao mình không phát hiện sớm hơn?** Job chạy xanh nghĩa là không có kiểm tra nào bắt được lỗi này. Em sẽ thêm một data quality check cho đúng loại lỗi đó. **Sửa bug là một việc, bịt lỗ hổng phát hiện là việc khác — và cái thứ hai mới ngăn được lần sau.**"

## ⑭ "Không đặt key cho message Kafka thì sao?"

> "Kafka sẽ phân phối **luân phiên** giữa các partition. Nghĩa là các event **của cùng một thực thể bị rải ra nhiều partition khác nhau**. Và vì Kafka chỉ đảm bảo thứ tự **trong một partition**, nên thứ tự của thực thể đó mất — giữa các partition thì các event xem như không còn liên hệ gì với nhau.
>
> Trong project em hậu quả rất cụ thể. Em tính thời gian mỗi nước cờ bằng hiệu đồng hồ giữa nước này và nước trước — tức là cần **state theo từng ván**. Nếu các nước của một ván nằm ở ba partition khác nhau thì ba consumer xử lý, mỗi con giữ một mảnh state, và **không ai suy ra được thời gian mỗi nước**.
>
> Nên em đặt key bằng mã ván. Nguyên tắc chung: **key phải là thứ mà logic của mình cần gom nhóm theo.**"

## ⑮ "Điểm yếu lớn nhất của em?"

> "Em nghĩ điểm yếu lớn nhất là **chưa từng vận hành một hệ thống chạy thật trong thời gian dài**.
>
> Em xây được kiến trúc, và em hiểu vì sao từng mảnh tồn tại. Nhưng project của em là cluster ephemeral — bật lên làm rồi tắt. Em chưa bao giờ phải trực một hệ thống chạy liên tục, chưa gặp cảnh bị gọi lúc nửa đêm, chưa phải xử lý sự cố khi có người thật đang chờ.
>
> Nó thể hiện ngay trong chính project: em chưa bật checkpointing, chưa đặt TTL cho state, chưa có CI/CD. Em **biết** những thứ đó cần, nhưng chưa từng ở trong tình huống mà thiếu chúng thì trả giá thật.
>
> **Đó cũng là lý do em muốn vào một nơi có hệ thống chạy thật và có người đã làm việc đó lâu năm — phần này em không tự học ở nhà được.**"

⚠️ **Đừng nói:** "em cầu toàn quá" / "em làm việc chăm quá". Và điểm yếu **luôn phải kèm vế hành động**.

## ⑯ Ba câu hỏi ngược nên chuẩn bị

Cuối buổi họ sẽ hỏi *"em có câu hỏi gì không"*. Không hỏi gì là mất điểm. Ba câu an toàn và thật:

- "Đội DE ở đây hiện đang xử lý bài toán gì là chính — nghiêng về xây pipeline mới hay vận hành và mở rộng hệ thống có sẵn?"
- "Một người mới vào thì sáu tháng đầu thường làm gì?"
- "Anh thấy điều gì tạo nên khác biệt giữa một DE tốt và một DE bình thường ở đội mình?"

---

# Sáu câu chốt — nếu quên hết thì nhớ mấy câu này

1. **"Hạ tầng không đổi — em chỉ làm cho dữ liệu chia được."** *(shred)*
2. **"Feature tại thời điểm duyệt vay chỉ được dùng thông tin có tại lúc đó."** *(point-in-time)*
3. **"Kịp thì ngăn chặn, trễ thì chỉ phát hiện."** *(batch vs streaming)*
4. **"Ghi đè thì idempotent, cộng dồn thì không."** *(recovery)*
5. **"Ranh giới cố định là ranh giới học được."** *(chống gaming)*
6. **"Sửa bug là một việc, bịt lỗ hổng phát hiện là việc khác."** *(vận hành)*

---

# Cách dùng file này

**Tối nay:** đọc to **câu ①** ba lần. Đọc lướt phần còn lại một lượt. Viết câu ⑪.

**Sáng mai:** chỉ đọc **sáu câu chốt** ở trên. Không nạp gì mới.

**Trong phòng:** nói **chậm**, có **mốc nghỉ**, và khi không biết thì nói *"em chưa làm cái này, nhưng hướng em nghĩ sẽ là..."* — bịa một câu là mất niềm tin cho mọi câu còn lại.
