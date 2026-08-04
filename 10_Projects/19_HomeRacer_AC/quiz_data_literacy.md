---
tags: [project, job-hunt, interview, data-engineer, quiz, home-credit]
status: active
created: 2026-07-31
related: "[[prep]] · [[de_concepts]] · [[case_rationale]]"
---

# Quiz — Data Literacy & Thống kê cho DE (36 câu)

> **Cách dùng:** làm hết phần câu hỏi trước, ghi đáp án ra giấy/note, rồi mới kéo xuống phần đáp án. Mỗi đáp án có giải thích ngắn — phần giải thích mới là chỗ học được.
> Mục tiêu không phải điểm cao, mà là **lộ ra chỗ mình tưởng hiểu mà chưa hiểu**.

---

## PHẦN A — Granularity & Cấu trúc dữ liệu (câu 1-7)

**1.** Câu hỏi đầu tiên nên đặt ra khi nhìn một bảng dữ liệu lạ là gì?
- ==A. Bảng có bao nhiêu dòng?==
- B. Mỗi dòng đại diện chính xác cho cái gì?
- C. Cột nào có nhiều NULL nhất?
- D. Dữ liệu được cập nhật lần cuối khi nào?

**2.** Bảng có các cột `account_id`, `snapshot_date`, `balance`. Granularity của bảng này là gì?
- A. Mỗi dòng là một giao dịch
- ==B. Mỗi dòng là một tài khoản==
- C. Mỗi dòng là trạng thái của một tài khoản tại một ngày
- D. Mỗi dòng là một khách hàng

**3.** Sự khác biệt cốt lõi giữa dữ liệu **event-level** và **state-level** là gì?
- A. Event-level luôn nhiều dòng hơn state-level
- ==B. Event-level ghi lại hành động xảy ra; state-level ghi lại trạng thái tại thời điểm==
- C. Event-level dùng cho OLTP, state-level dùng cho OLAP
- D. Không có khác biệt thực chất, chỉ là cách gọi

**4.** Bạn JOIN bảng `customers` (1 dòng/khách) với bảng `transactions` (N dòng/khách) rồi tính `SUM(customers.credit_limit)`. Chuyện gì xảy ra?
- A. Kết quả đúng
- B. Kết quả bị thiếu vì một số khách không có giao dịch
- ==C. `credit_limit` bị nhân bản theo số giao dịch → tổng bị thổi phồng==
- D. Query báo lỗi vì sai kiểu dữ liệu

**5.** Hiện tượng ở câu 4 gọi là gì?
- A. Data skew
- ==B. Fan-out effect==
- C. Cartesian product
- D. Data drift

**6.** Quan hệ N-N (nhiều-nhiều) khi JOIN trực tiếp gây ra vấn đề gì?
- A. Mất dữ liệu
- ==B. Bùng nổ số dòng, dữ liệu bị nhân bản không kiểm soát==
- C. Query luôn trả về NULL
- D. Không có vấn đề nếu có index

**7.** Cách an toàn nhất để tránh fan-out khi cần tổng hợp từ bảng N là gì?
- A. Dùng `SELECT DISTINCT`
- ==B. Tổng hợp bảng N về đúng granularity trước, rồi mới JOIN==
- C. Dùng `LEFT JOIN` thay vì `INNER JOIN`
- D. Thêm index vào khóa ngoại

---

## PHẦN B — Đọc pattern trong bảng nhỏ (câu 8-12)

**8.** Trong Pattern Discovery Matrix, "Logical Dependency" nghĩa là gì?
- A. Cột này phụ thuộc kỹ thuật vào cột kia qua khóa ngoại
- ==B. Quan hệ nghiệp vụ giữa các cột, VD `status='CLOSED'` thì `balance` phải bằng 0==
- C. Thứ tự các cột trong bảng
- D. Cột được tính từ cột khác bằng công thức

**9.** Cột `discount_code` có 80% giá trị NULL. Cách diễn giải đúng nhất là gì?
- A. Dữ liệu bị lỗi, cần loại bỏ cột này
- B. Cần điền giá trị mặc định cho tất cả NULL
- ==C. NULL có thể mang nghĩa nghiệp vụ: đơn hàng không dùng mã giảm giá==
- D. Pipeline nạp dữ liệu đã hỏng

**10.** "Temporal pattern" khi quét dữ liệu thô bao gồm việc kiểm tra điều gì?
- A. Chỉ xu hướng tăng/giảm theo thời gian
- ==B. Xu hướng, tính chu kỳ, và cả **event đến không đúng thứ tự**==
- C. Số lượng cột kiểu timestamp
- D. Timezone của server

**11.** Bảng giao dịch có cột `amount` với `min = -5000`. Phản ứng đúng đầu tiên là gì?
- A. Lọc bỏ mọi dòng âm ngay
- B. Đổi thành giá trị tuyệt đối
- ==C. Hỏi xem giá trị âm có ý nghĩa nghiệp vụ không (hoàn tiền, điều chỉnh?)==
- D. Báo cáo là dữ liệu hỏng

**12.** Vì sao nên xem 10-20 dòng dữ liệu thô trước khi chạy hàm tổng hợp?
- A. Để tiết kiệm chi phí compute
- ==B. Vì hàm tổng hợp che mất cấu trúc, trùng lặp và bất thường ở mức dòng==
- C. Vì quy định bảo mật yêu cầu
- D. Không cần thiết nếu đã có schema

---

## PHẦN C — Sanity-check đơn vị & ngưỡng (câu 13-21)

**13.** Timestamp `1711929600000` có 13 chữ số. Đơn vị là gì?
- A. Giây
- ==B. Mili giây==
- C. Micro giây
- D. Nano giây

**14.** Bạn diễn giải nhầm timestamp mili giây thành giây. Hậu quả?
- A. Thời gian lệch vài phút
- ==B. Thời gian bị đẩy tới tương lai rất xa (hàng nghìn năm)==
- C. Thời gian lùi về năm 1970
- D. Không ảnh hưởng nếu chỉ so sánh tương đối

**15.** Cột `latency` có giá trị `2000`. Trước khi kết luận "hệ thống chậm", cần làm gì?
- A. So sánh với ngưỡng SLA ngay
- B. Xác định đơn vị: 2000ms (2 giây) rất khác 2000 giây
- C. Tính trung bình toàn bộ cột
- D. Kiểm tra xem có NULL không

**16.** Cột `amount = 100000` trong hệ thống tài chính. Rủi ro diễn giải là gì?
- A. Không có rủi ro, rõ ràng là 100.000 đồng
- B. Có thể là đơn vị nhỏ nhất (xu/cents) → thực chất là 1.000,00
- C. Chắc chắn là USD
- D. Cần chia cho 1000 để ra đơn vị chuẩn

**17.** Cột `amount` không có cột `currency_code` đi kèm. Vấn đề là gì?
- A. Không có vấn đề nếu công ty chỉ hoạt động ở một nước
- B. Có thể đang cộng lẫn lộn nhiều loại tiền tệ khác nhau
- C. Chỉ ảnh hưởng báo cáo, không ảnh hưởng pipeline
- D. Có thể suy ra tiền tệ từ độ lớn con số

**18.** Cột `age` có giá trị `1802`. Nguyên nhân khả dĩ nhất?
- A. Lỗi nhập liệu ngẫu nhiên
- B. Cột thực chất chứa **năm sinh**, không phải tuổi
- C. Đơn vị là tháng
- D. Giá trị sentinel đánh dấu dữ liệu thiếu

**19.** Tỷ lệ chuyển đổi tính ra `150%`. Nguyên nhân thường gặp nhất?
- A. Dữ liệu bị nhân bản hoặc sai mẫu số (denominator)
- B. Khách hàng mua nhiều lần
- C. Chuyện bình thường trong marketing
- D. Lỗi làm tròn

**20.** Nguyên tắc "Physical Reality Check" trước khi đặt ngưỡng data quality là gì?
- A. Ngưỡng phải dựa trên percentile của dữ liệu hiện có
- B. Tự hỏi ngưỡng đó có hợp lý trong thực tế không (VD tuổi 0-120)
- C. Ngưỡng phải do business chốt, kỹ sư không được đề xuất
- D. Luôn đặt ngưỡng ở mức 3 độ lệch chuẩn

**21.** Cột `balance` của tài khoản thanh toán có giá trị âm. Câu hỏi đúng cần đặt ra?
- A. Xóa ngay vì số dư không thể âm
- B. Sản phẩm này có cho phép thấu chi (overdraft) không?
- C. Đổi thành 0
- D. Đây chắc chắn là lỗi pipeline

---

## PHẦN D — Nêu giả định rõ ràng (câu 22-27)

**22.** Vai trò cốt lõi của DE/Analyst khi nhận yêu cầu mơ hồ từ business là gì?
- A. Yêu cầu business viết lại cho rõ rồi mới làm
- B. Biến câu hỏi mơ hồ thành logic có giả định được tuyên bố rõ ràng
- C. Chọn cách diễn giải phổ biến nhất và làm luôn
- D. Làm cả mọi cách diễn giải có thể

**23.** Yêu cầu: "tính doanh thu". Bảng có `status` gồm SUCCESS, PENDING, CANCELLED, FAILED. Cách xử lý ĐÚNG?
- A. `SUM(amount)` tất cả các dòng
- B. Tuyên bố rõ: chỉ tính `status='SUCCESS'` và `refund_flag=FALSE`, rồi lọc theo đó
- C. Loại PENDING, giữ lại phần còn lại
- D. Hỏi business rồi ngồi chờ, không làm gì thêm

**24.** Trong Explicit Assumption Framework, bước cuối cùng là gì?
- A. Viết code SQL
- B. Ghi chú vào tài liệu
- C. Định lượng tác động — giả định này loại bỏ/giữ lại bao nhiêu % dữ liệu
- D. Gửi kết quả cho business duyệt

**25.** Vì sao bước "định lượng tác động" quan trọng?
- A. Để tối ưu hiệu năng query
- B. Để biết giả định ảnh hưởng lớn hay nhỏ tới kết quả — lọc mất 2% khác hẳn lọc mất 40%
- C. Vì quy trình bắt buộc
- D. Để tính chi phí lưu trữ

**26.** Giả định NGẦM (implicit) nguy hiểm hơn giả định SAI ở chỗ nào?
- A. Nó luôn dẫn tới kết quả sai
- B. Không ai biết nó tồn tại nên không ai kiểm chứng hay sửa được
- C. Nó làm query chạy chậm
- D. Nó vi phạm quy định tuân thủ

**27.** Báo cáo kế toán cuối ngày nên GROUP BY theo cột nào, và vì sao?
- A. `processing_time`, vì đó là lúc hệ thống ghi nhận
- B. `event_time`, vì phản ánh đúng thời điểm phát sinh tài chính
- C. Cột nào cũng được, chênh lệch không đáng kể
- D. Trung bình của hai cột

---

## PHẦN E — Thống kê mô tả (câu 28-32)

**28.** Bảng giá trị giao dịch có `Mean = 5.000.000`, `Median = 800.000`. Kết luận?
- A. Dữ liệu phân phối chuẩn
- B. Dữ liệu lệch phải — một số giao dịch rất lớn kéo trung bình lên
- C. Dữ liệu lệch trái
- D. Dữ liệu bị lỗi

**29.** Với dữ liệu lệch mạnh như câu 28, nên dùng gì để đặt ngưỡng phát hiện bất thường?
- A. Mean
- B. Median hoặc percentile
- C. Mode
- D. Tổng

**30.** IQR được tính như thế nào?
- A. Max − Min
- B. Q3 − Q1 (P75 − P25)
- C. P99 − P1
- D. 2 × độ lệch chuẩn

**31.** Vì sao đo latency nên dùng P95/P99 thay vì trung bình?
- A. Vì percentile dễ tính hơn
- B. Vì trung bình che mất phần đuôi — nơi người dùng thực sự bị ảnh hưởng nặng
- C. Vì trung bình luôn sai
- D. Vì P99 luôn nhỏ hơn trung bình

**32.** Độ lệch chuẩn của cột `amount` đột ngột tăng gấp 10 lần so với bình thường. Nghi ngờ đầu tiên?
- A. Khách hàng thay đổi hành vi
- B. Dữ liệu bị nhân bản hoặc pipeline dính fan-out
- C. Model machine learning cần train lại
- D. Kích thước cụm compute không đủ

---

## PHẦN F — Thống kê ứng dụng vào Data Quality (câu 33-36)

**33.** Quy tắc Z-score để phát hiện outlier thường dùng ngưỡng nào?
- A. |Z| > 1
- B. |Z| > 2
- C. |Z| > 3 (ngoài khoảng 99.7%)
- D. |Z| > 5

**34.** Xử lý ĐÚNG với các dòng bị đánh dấu outlier trong pipeline production?
- A. Xóa vĩnh viễn
- B. Đưa vào bảng cách ly (quarantine) để người rà soát, không cho vào warehouse
- C. Vẫn nạp bình thường, xử lý sau
- D. Thay bằng giá trị trung bình

**35.** Cách phát hiện data drift/bất thường về khối lượng mà không cần đọc từng dòng?
- A. Kiểm tra thủ công mẫu ngẫu nhiên mỗi ngày
- B. So số dòng và thống kê hôm nay với trung bình động 7 ngày, lệch quá 3σ thì cảnh báo
- C. Đếm số cột trong schema
- D. Kiểm tra log của Airflow

**36.** Định luật Benford dùng để phát hiện điều gì?
- A. Dữ liệu bị thiếu
- B. Dữ liệu có dấu hiệu bị tạo giả/thao túng, qua phân phối chữ số đầu tiên bất thường
- C. Trùng lặp bản ghi
- D. Sai lệch timezone

---
---

# ĐÁP ÁN & GIẢI THÍCH

**1 — B.** Granularity là câu hỏi số 0 của mọi phân tích. Không biết một dòng đại diện cho cái gì thì mọi phép tổng hợp phía sau đều có nguy cơ vô nghĩa.

**2 — C.** Khóa tổ hợp `account_id + snapshot_date` cho biết granularity là "một tài khoản tại một ngày" — đây là bảng snapshot trạng thái, không phải bảng giao dịch.

**3 — B.** Event-level ghi *hành động đã xảy ra* (bất biến, chỉ thêm mới). State-level ghi *trạng thái tại thời điểm* (có thể cập nhật). Nhầm hai loại này dẫn tới đếm sai và diễn giải sai hoàn toàn.

**4 — C.** Sau JOIN, một khách có 50 giao dịch sẽ xuất hiện 50 dòng → `credit_limit` bị cộng 50 lần. Đây là lỗi phổ biến nhất khi làm việc với dữ liệu quan hệ.

**5 — B.** Fan-out effect. (Cartesian product là khi JOIN thiếu điều kiện, khác hiện tượng này.)

**6 — B.** N-N nhân chéo cả hai phía → số dòng bùng nổ. Cần bảng trung gian (bridge table) và tổng hợp cẩn thận.

**7 — B.** Tổng hợp bảng N về đúng granularity của bảng 1 **trước**, rồi JOIN 1-1. `DISTINCT` chỉ che triệu chứng và thường vẫn sai.

**8 — B.** Logical dependency là ràng buộc **nghiệp vụ** giữa các cột. Kiểm tra được nó là một trong những data quality check giá trị nhất, vì nó bắt lỗi mà kiểm tra kiểu dữ liệu không bắt được.

**9 — C.** NULL rất thường mang nghĩa "không áp dụng" chứ không phải "dữ liệu lỗi". Điền bừa giá trị mặc định sẽ bịa ra thông tin không có thật. Luôn hỏi: NULL ở đây nghĩa là gì?

**10 — B.** Bao gồm cả out-of-order — event đến sau khi đã qua thời điểm của nó. Rất quan trọng trong streaming (liên quan watermark).

**11 — C.** Giá trị âm có thể hoàn toàn hợp lệ: hoàn tiền, đảo bút toán, điều chỉnh. Xóa vội là làm mất dữ liệu thật. Hỏi trước.

**12 — B.** `SUM`/`AVG` che mất mọi thứ: trùng lặp, sai granularity, giá trị sentinel, đơn vị lẫn lộn. Nhìn dòng thô là cách rẻ nhất để bắt các lỗi đó.

**13 — B.** 10 chữ số = giây, 13 = mili giây, 16 = micro giây. Đây là mẹo nhận diện nhanh nên nhớ.

**14 — B.** Coi mili giây là giây → nhân giá trị lên 1000 lần → thời gian nhảy tới tương lai xa hàng nghìn năm.

**15 — B.** Đơn vị trước, kết luận sau. 2000ms là bình thường; 2000 giây là thảm họa. Đây đúng là điểm guide của công ty nhấn mạnh.

**16 — B.** Nhiều hệ thống tài chính lưu tiền ở **đơn vị nhỏ nhất** để tránh sai số dấu phẩy động. Phải xác nhận quy ước trước khi tính toán.

**17 — B.** Không có `currency_code` thì `SUM(amount)` là cộng lẫn lộn các loại tiền — con số ra hoàn toàn vô nghĩa. Đây là lỗi nghiêm trọng trong công ty đa quốc gia.

**18 — B.** 1802 quá phi lý cho tuổi nhưng hợp lý cho năm sinh — dấu hiệu cột bị đặt tên sai hoặc trộn hai loại dữ liệu. Physical reality check bắt được ngay.

**19 — A.** Tỷ lệ vượt 100% gần như luôn do sai mẫu số hoặc tử số bị nhân bản (thường lại là fan-out). Tỷ lệ là chỗ dễ lộ lỗi JOIN nhất.

**20 — B.** Ngưỡng phải hợp lý với thực tế vật lý/nghiệp vụ, không chỉ hợp lý về mặt thống kê. Dữ liệu có thể sai một cách rất "ổn định".

**21 — B.** Thấu chi, phí phạt, hoặc bút toán đảo đều tạo số dư âm hợp lệ. Câu hỏi đúng là về **quy tắc sản phẩm**, không phải về dữ liệu.

**22 — B.** Đây là phần giá trị cốt lõi của nghề: biến sự mơ hồ thành logic minh bạch, kiểm chứng được. Không phải chờ người khác làm rõ hộ.

**23 — B.** Tuyên bố giả định rồi lọc theo đó. Vẫn tiến được việc, mà ai đọc cũng biết con số này nghĩa là gì và sửa được nếu quy ước khác.

**24 — C.** Định lượng tác động. Giả định không kèm con số ảnh hưởng là giả định chưa hoàn chỉnh.

**25 — B.** Lọc mất 2% dữ liệu là chi tiết nhỏ; lọc mất 40% là dấu hiệu hiểu sai bài toán. Con số quyết định mức độ cần rà soát lại.

**26 — B.** Giả định sai mà **được nêu ra** thì sẽ có người phát hiện và sửa. Giả định ngầm thì âm thầm sai mãi mãi. Đây chính là lý do guide của công ty nhấn mạnh "state assumptions explicitly".

**27 — B.** Kế toán chốt theo thời điểm giao dịch **thực sự phát sinh** (`event_time`), kèm cửa sổ trễ (watermark) để nhận dữ liệu đến muộn. Dùng `processing_time` sẽ đẩy giao dịch sang sai ngày.

**28 — B.** Mean ≫ Median = lệch phải. Bình thường với dữ liệu tài chính: đa số giao dịch nhỏ, một số ít rất lớn kéo trung bình lên.

**29 — B.** Với phân phối lệch, mean bị outlier kéo đi nên không đại diện. Median/percentile bền vững hơn nhiều.

**30 — B.** IQR = Q3 − Q1. Hàng rào outlier thông dụng: dưới Q1 − 1.5×IQR hoặc trên Q3 + 1.5×IQR.

**31 — B.** Trung bình che phần đuôi. P99 = 5 giây nghĩa là **1% người dùng chờ 5 giây** — dù trung bình chỉ 200ms. Đo hệ thống luôn nhìn đuôi.

**32 — B.** Độ phân tán nhảy vọt mà nghiệp vụ không đổi thường là dấu hiệu dữ liệu bị nhân bản — nghi ngờ pipeline trước, nghi ngờ hành vi khách hàng sau.

**33 — C.** |Z| > 3 tương ứng ngoài khoảng 99.7% của phân phối chuẩn. Lưu ý: Z-score giả định phân phối chuẩn — với dữ liệu lệch mạnh (như số tiền giao dịch) thì IQR hoặc percentile đáng tin hơn.

**34 — B.** Cách ly để rà soát: không làm bẩn warehouse, cũng không mất dữ liệu. Xóa vĩnh viễn là không thể đảo ngược, mà outlier đôi khi lại là dữ liệu thật quan trọng nhất (gian lận!).

**35 — B.** So sánh thống kê tổng hợp với đường cơ sở lịch sử. Đây là nền của data observability — bắt lỗi tự động mà không cần đọc từng dòng.

**36 — B.** Benford: chữ số đầu tiên trong dữ liệu tài chính tự nhiên tuân theo phân phối giảm dần (số 1 ~30%, số 9 ~4.6%). Lệch khỏi phân phối này là tín hiệu dữ liệu bị bịa hoặc thao túng.

---

## Thang tự đánh giá

| Đúng | Ý nghĩa |
|---|---|
| 30-36 | Nắm chắc — chỉ cần lướt lại phần sai trước ngày 6/8 |
| 22-29 | Ổn — đọc kỹ giải thích các câu sai, đủ dùng cho AC |
| < 22 | Đọc lại [[de_concepts]] mục 8 (chất lượng) và phần Data literacy trong [[prep]] |

**Ba câu quan trọng nhất nếu chỉ nhớ được vài thứ:** câu 1 (granularity), câu 4-5 (fan-out), câu 26 (giả định ngầm nguy hiểm hơn giả định sai). Ba ý này bao trùm phần lớn lỗi thực tế trong công việc DE.
