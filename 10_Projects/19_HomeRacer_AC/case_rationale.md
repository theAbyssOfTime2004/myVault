---
tags: [project, job-hunt, interview, data-engineer, home-credit, reference]
status: active
created: 2026-07-31
related: "[[prep]] · [[de_concepts]]"
---

# Giải phẫu case mẫu — vì sao mỗi nước đi

> Mục tiêu: không học thuộc lời giải, mà hiểu **logic sinh ra lời giải** để áp vào bất kỳ đề nào.
> Đề gốc: *"Thiết kế hệ thống cảnh báo khách có nguy cơ trễ kỳ thanh toán tới."*

---

## PHẦN A — Tại sao HỎI trước khi GIẢI

### A.0 Lý do sâu hơn "vì họ chấm điểm phần này"

Đúng là tiêu chí chấm có mục "biết đặt câu hỏi hiểu đề". Nhưng lý do thật sự nằm ở nghề:

Trong công việc DE thật, **hiểu sai yêu cầu = mất cả quý**. Bạn xây một pipeline streaming 3 tháng, rồi phát hiện nghiệp vụ chỉ cần báo cáo mỗi sáng — batch 2 tuần là xong. Không ai đánh giá kỹ sư giỏi qua việc gõ code nhanh; người ta đánh giá qua việc **xây đúng thứ cần xây**.

Vì vậy khi bạn hỏi trước, người chấm không nghĩ "bạn này chưa biết làm". Họ nghĩ **"bạn này từng bị đau vì làm sai yêu cầu"** — tức là có kinh nghiệm thật. Đó là tín hiệu mạnh hơn mọi thuật ngữ kỹ thuật.

Ngược lại, lao vào vẽ kiến trúc ngay phát tín hiệu: quen làm bài tập có đề rõ (môi trường trường học), chưa quen làm sản phẩm thật (môi trường công ty).

### A.1 Câu hỏi 1 — Mục tiêu & Metric. **Vì sao hỏi đầu tiên?**

> *Metric: giảm tỷ lệ trễ hạn; đo bằng precision/recall. Hành động sau cảnh báo: collections gọi/nhắn nhắc.*

**Vì mọi quyết định thiết kế phía sau đều bắt nguồn từ đây.** Không biết đo thành công bằng gì thì không có cơ sở nào để chọn giữa hai phương án.

Nhưng phần giá trị nhất nằm ở chỗ ít người nói ra: **precision và recall ánh xạ thẳng sang chi phí kinh doanh, và hai loại sai lầm KHÔNG cân nhau.**

- **False positive** (báo động nhầm khách tốt): tốn thời gian nhân viên gọi điện, và tệ hơn — **làm phiền khách hàng đang trả tốt**, ảnh hưởng trải nghiệm. Chi phí vừa phải.
- **False negative** (bỏ sót khách sắp vỡ nợ): mất trắng khoản nợ. Chi phí **lớn hơn nhiều**.

→ Suy ra: nên **ưu tiên recall hơn precision**, chấp nhận báo động thừa. Và ngưỡng cảnh báo không do kỹ sư chọn — nó là **quyết định kinh doanh**, phải chốt với product/rủi ro.

Nói được đoạn này là bạn vượt hẳn mức "fresher biết thuật ngữ": bạn đang nối kỹ thuật với tiền.

**Vế thứ hai còn quan trọng hơn: "sau cảnh báo thì ai làm gì?"**

Một cảnh báo không ai hành động là một cảnh báo vô giá trị — dù model có đẹp đến đâu. Và câu trả lời ở đây (*collections gọi điện*) chính là thứ **quyết định toàn bộ kiến trúc**: con người gọi điện trong giờ hành chính → không cần realtime → batch. Xem A.4.

### A.2 Câu hỏi 2 — Người dùng & Quyết định

> *Team collections, dùng danh sách khách rủi ro mỗi sáng.*

Câu này quyết định **hình dạng tầng phục vụ (serving layer)**. Ba kiểu người dùng cho ba kiến trúc hoàn toàn khác nhau:

| Người dùng | Cách tiêu thụ | Hệ quả kiến trúc |
|---|---|---|
| Nhân viên collections | Danh sách mỗi sáng | Dashboard/bảng → **batch, warehouse là đủ** |
| Hệ thống duyệt vay tự động | Gọi API lúc khách đăng ký | **Online serving store** (Redis), độ trễ ms |
| Hệ thống chặn giao dịch | Chặn ngay lúc quẹt | **Streaming**, độ trễ dưới giây |

Cùng một bài toán "chấm điểm rủi ro", nhưng ba câu trả lời trên cho ra ba hệ thống khác nhau về độ phức tạp và chi phí gấp nhiều lần. Đó là lý do không được đoán.

### A.3 Câu hỏi 3 — Dữ liệu

> *Lịch sử thanh toán, thông tin khoản vay, giao dịch, (có thể) bureau.*

Hai lớp ý nghĩa:

**Lớp 1 — Tính khả thi.** Không có dữ liệu thì không có hệ thống. Hỏi sớm để biết mình đang thiết kế trên nền có thật hay đang vẽ tưởng tượng.

**Lớp 2 — Vấn đề NHÃN (label), chỗ này rất ít fresher nghĩ tới.** Muốn train model có giám sát, cần biết trong quá khứ **ai đã thực sự trễ hạn**. Câu hỏi kèm theo rất "chuyên nghiệp":

- Trễ hạn định nghĩa thế nào? Trễ 1 ngày hay 30 ngày (DPD 30)? — mỗi định nghĩa cho một bài toán khác nhau.
- Có đủ mẫu dương không? Nếu chỉ 2% khách trễ hạn → **imbalanced data**, cần xử lý riêng.
- Có bao nhiêu lịch sử? Đủ để bao trọn một chu kỳ khoản vay chưa?

Và một khái niệm cực quan trọng trong tín dụng — **point-in-time correctness**: khi tạo dữ liệu train, chỉ được dùng thông tin **có tại thời điểm đó**. Nếu vô tình dùng dữ liệu tương lai (VD: dùng trạng thái thanh toán tháng sau để dự đoán tháng này) thì model đẹp trên giấy và **sập hoàn toàn khi chạy thật**. Đây gọi là **data leakage**, và nó là lý do chính khiến feature store tồn tại.

*Nhắc được "point-in-time correctness" hoặc "data leakage" trong case tài chính là một trong những điểm cộng lớn nhất có thể ghi.*

### A.4 Câu hỏi 4 — Ràng buộc. **Câu quan trọng nhất với vai trò DE**

> *Collections hành động theo ngày → batch hằng ngày là đủ, chưa cần streaming.*

Đây là **quyết định lớn nhất trong cả bài**, vì batch và streaming chênh nhau rất xa về:

| | Batch | Streaming |
|---|---|---|
| Độ phức tạp | Thấp | Cao (state, watermark, exactly-once) |
| Chi phí hạ tầng | Thấp (chạy rồi tắt) | Cao (cụm chạy 24/7) |
| Vận hành/debug | Dễ, chạy lại được | Khó, lỗi khó tái hiện |
| Nhân sự cần | Ít | Nhiều, kỹ năng cao |

**Nguyên tắc:** độ trễ của hệ thống chỉ cần nhanh hơn **tốc độ hành động của con người/hệ thống phía sau**. Collections gọi điện trong giờ làm việc → dữ liệu sẵn lúc 6h sáng là thừa đủ. Xây streaming ở đây là **đốt tiền và công sức để lấy độ trễ không ai dùng đến**.

Đây chính là dấu hiệu phân biệt kỹ sư non và kỹ sư chín:
- Non: chọn công nghệ nghe hiện đại nhất → "mình sẽ dùng Kafka + Flink".
- Chín: chọn công nghệ **đơn giản nhất đủ đáp ứng yêu cầu**, và **nói rõ khi nào thì cần nâng cấp**.

Câu nói ăn điểm: *"Batch hằng ngày là đủ cho use case này. Nếu sau này nghiệp vụ muốn can thiệp ngay trong ngày, kiến trúc này nâng lên streaming được mà không phải làm lại từ đầu."*

### A.5 Câu hỏi 5 — Nêu giả định thành lời

> *Giả định: có 12 tháng lịch sử thanh toán; scoring chạy 1 lần/ngày lúc rạng sáng.*

Trong AC, **luôn luôn thiếu thông tin** — đó là cố ý. Họ muốn xem bạn xử lý sự mơ hồ thế nào. Có ba cách phản ứng:

1. **Đứng im chờ đủ thông tin** → mất điểm, trông thụ động.
2. **Ngầm giả định rồi cứ thế giải** → nguy hiểm nhất: nếu giả định sai thì cả lời giải sai, mà không ai kịp phát hiện.
3. **Nêu giả định thành lời rồi tiếp tục** → đúng. Vừa tiến được, vừa mở đường sửa.

Câu mẫu: *"Em giả định X. Nếu thực tế không phải vậy thì phần Y sẽ thay đổi."* — vế sau mới là vế ăn điểm, vì nó cho thấy bạn hiểu giả định đó ảnh hưởng tới đâu.

Guide của công ty ghi thẳng *"stating assumptions explicitly"* trong phần data literacy → đây là thứ họ **chủ động tìm kiếm** ở ứng viên.

---

## PHẦN B — Tại sao THIẾT KẾ như vậy

> Nguyên tắc xuyên suốt: **bạn là DE, không phải data scientist.** Đừng sa đà vào chọn model (XGBoost hay neural net). Giá trị của bạn nằm ở **đường đi của dữ liệu**: lấy từ đâu, biến đổi thế nào, lưu ở đâu, phục vụ ra sao, hỏng thì làm gì. Trong nhóm có DA/DS rồi — để phần model cho họ, đó cũng là teamwork tốt.

### B.1 Nguồn: core banking DB, luồng giao dịch, bureau

Nhận diện đúng **ba loại nguồn khác nhau**, mỗi loại nạp một kiểu:
- **DB vận hành** (khoản vay, thanh toán) — dữ liệu quan hệ, thay đổi liên tục → CDC.
- **Luồng sự kiện** (giao dịch) — khối lượng lớn, chỉ thêm mới → stream hoặc batch dump.
- **Bên thứ ba** (credit bureau) — cập nhật chậm, lấy qua API/file, thường tính phí mỗi lần gọi → batch định kỳ, và **cache lại** để không gọi lặp.

### B.2 Ingestion: **CDC** từ DB vận hành → lake

**Vì sao không truy vấn thẳng vào DB core banking?** Đây là lỗi kinh điển của người mới, và tránh được nó là điểm cộng lớn:

1. **Core banking là hệ thống OLTP đang phục vụ khách thật.** Chạy một query phân tích quét cả bảng lịch sử thanh toán có thể làm chậm hoặc treo hệ thống — nghĩa là khách không vay được, cửa hàng không bán được. **Rủi ro nghiệp vụ, không chỉ rủi ro kỹ thuật.**
2. OLTP tối ưu cho đọc/ghi từng dòng, **không** tối ưu cho quét lớn → query phân tích chạy chậm khủng khiếp.
3. Truy vấn trực tiếp tạo **coupling chặt**: schema bên vận hành đổi là pipeline gãy.

CDC giải quyết cả ba: đọc từ transaction log (**không đụng vào tải của DB**), đưa thay đổi sang lake gần realtime, và tách biệt hai hệ thống.

**Vì sao đổ vào data lake trước, không đi thẳng vào model?**
- **Lưu bản thô** → sau này đổi logic feature thì **backfill lại được** từ dữ liệu gốc. Nếu chỉ lưu kết quả đã xử lý, dữ liệu gốc mất là mất vĩnh viễn.
- **Một nguồn, nhiều người dùng**: cùng dữ liệu đó, đội rủi ro, marketing, báo cáo đều dùng được. Không phải mỗi đội tự kéo một đường từ core banking.
- **Rẻ**: object storage rẻ hơn nhiều so với lưu trong DB vận hành.

### B.3 Xử lý: pipeline feature batch (Spark) → feature store

**Vì sao cần feature store, không tính feature trực tiếp lúc train?**

- **Tái sử dụng**: "số lần trễ hạn 6 tháng qua" dùng được cho model trễ hạn, model gian lận, model duyệt vay. Tính một lần, dùng nhiều nơi.
- **Chống training-serving skew**: nếu feature lúc train tính bằng SQL, lúc chạy thật tính lại bằng Python, hai bên lệch nhau → model chạy thật kém hơn hẳn lúc thử nghiệm. Feature store đảm bảo **một định nghĩa duy nhất**.
- **Point-in-time correctness** (nối lại A.3): feature store lưu feature kèm mốc thời gian, nên tạo tập train là lấy đúng giá trị feature **tại thời điểm quá khứ đó**, không lẫn dữ liệu tương lai.

Đây cũng chính là project Feature Store Lichess của bạn → khi trình bày, nói *"em có làm một feature store cho dữ liệu cờ vua, kiến trúc batch + stream, nên phần này em hình dung được"* → material thật, cực kỳ thuyết phục.

### B.4 Scoring: model đọc feature → ghi điểm vào serving store

Tách **tính điểm** khỏi **phục vụ điểm** vì:
- Dashboard cần đọc **nhanh và ổn định**, không thể chờ model chạy.
- Model đổi/nâng cấp mà tầng phục vụ không phải thay đổi.
- Điểm ghi ra là bảng đơn giản (`customer_id, risk_score, scored_at`) → ai cũng dùng được.

**Lưu ý về `scored_at`**: luôn ghi kèm mốc thời gian chấm điểm. Không có nó thì không ai biết điểm đang xem là của hôm nay hay của tuần trước — và trong tài chính, điểm cũ dẫn tới quyết định sai.

### B.5 Serving: dashboard hoặc queue

Hai kiểu tiêu thụ, phản ánh hai kiểu hành động:
- **Dashboard**: người xem danh sách rồi tự quyết định gọi ai trước.
- **Queue/worklist**: khách rủi ro cao được đẩy thẳng vào hàng đợi công việc của nhân viên → tự động hơn, ít phụ thuộc người chủ động vào xem.

Nêu được cả hai và nói *"tùy quy trình làm việc của collections"* = cho thấy bạn thiết kế theo **con người dùng nó**, không chỉ theo kỹ thuật.

### B.6 Chất lượng & phục hồi — phần khiến bạn khác fresher khác

Đa số ứng viên trình bày xong đường đi "sạch" rồi dừng. Người có tư duy vận hành nói tiếp: **"và khi nó hỏng thì sao?"**

- **Idempotent**: job chạy lại cho cùng kết quả, không nhân đôi dữ liệu. Kỹ thuật: ghi đè theo partition ngày, hoặc upsert theo khóa `(customer_id, date)`. → **Bắt buộc**, vì pipeline chắc chắn sẽ có ngày lỗi và phải chạy lại.
- **Data quality checks**: số dòng hôm nay có sụt bất thường không? Tỷ lệ null có tăng vọt? Điểm rủi ro trung bình có nhảy đột ngột (dấu hiệu pipeline lỗi hoặc dữ liệu đầu vào đổi)?
→ Trong tài chính, **dữ liệu sai còn nguy hiểm hơn không có dữ liệu**: không có thì biết mà chờ, sai thì cứ thế ra quyết định sai hàng loạt.
- **Backfill**: sửa logic feature xong phải tính lại được lịch sử. Chỉ khả thi nếu đã lưu dữ liệu thô (B.2) và pipeline idempotent.
- **SLA**: dữ liệu phải sẵn sàng trước 7h sáng, vì collections bắt đầu làm lúc 8h. Có cam kết đo được → có cái để báo động khi trễ.

---

## PHẦN C — Tại sao TRÌNH BÀY theo cấu trúc đó

Cấu trúc: **Vấn đề + giả định → Giải pháp → Đánh đổi + bước tiếp**

**Nhịp 1 — Vấn đề + giả định.** Chứng minh bạn *hiểu đề* trước khi phô giải pháp. Nêu giả định ngay đầu cũng là "bảo hiểm": nếu giả định sai, người nghe sửa ngay, cả phần sau vẫn còn giá trị.

**Nhịp 2 — Giải pháp, vừa vẽ vừa nói.** Đi theo dòng chảy dữ liệu từ trái sang phải (nguồn → xử lý → phục vụ) vì đó là thứ tự não người theo dõi dễ nhất. Guide ghi *"whiteboard hoặc chỉ ý tưởng/flow"* → **họ muốn thấy bạn nghĩ ra tiếng**, nên đừng im lặng vẽ rồi mới nói.

**Nhịp 3 — Đánh đổi + bước tiếp. Đây là nhịp phân loại ứng viên.**

Nói được đánh đổi chứng minh bạn **đã cân nhắc phương án khác** rồi mới chọn — chứ không phải chỉ biết mỗi một cách. Người mới trình bày như thể giải pháp của mình là duy nhất đúng; người có kinh nghiệm luôn nói *"em chọn A vì X, đánh đổi là Y; nếu điều kiện đổi thì B hợp hơn."*

Và câu cuối — *"bước tiếp: chốt feature với DA, chốt ngưỡng cảnh báo với product"* — không phải câu xã giao. Nó ghi điểm **teamwork**: bạn thể hiện mình biết ranh giới chuyên môn của mình ở đâu, và tôn trọng phần việc của người khác trong nhóm. Trong AC có cả product và DA ngồi đó, đây là tín hiệu rất mạnh.

---

## PHẦN D — Bộ khung chuyển sang đề khác

Mạch trên áp được cho gần như mọi case dữ liệu. Rút gọn thành 6 bước:

1. **Hành động phía sau là gì?** → quyết định batch hay streaming (câu quan trọng nhất)
2. **Ai dùng, dùng thế nào?** → quyết định tầng phục vụ
3. **Dữ liệu ở đâu, thuộc loại nguồn nào?** → quyết định cách nạp (CDC / batch / stream)
4. **Lưu thô trước, xử lý sau** → luôn đúng, cho phép backfill và nhiều người dùng chung
5. **Tách tính toán khỏi phục vụ** → mỗi bên tối ưu cho việc của mình
6. **Hỏng thì sao?** → idempotency, quality checks, backfill, SLA

Áp thử vào đề gian lận POS (đề đang treo trong buổi mock):
- Hành động phía sau: chặn hồ sơ ngay tại quầy? → **cần realtime** → streaming. Hay rà soát cửa hàng đối tác hằng tuần? → **batch**. *(Ở đề này rất có thể là cả hai: chặn hồ sơ realtime + giám sát cửa hàng theo batch — nói được cả hai tầng là rất mạnh.)*
- Ai dùng: hệ thống duyệt vay tự động (API, độ trễ ms) + đội quản lý đối tác (dashboard).
- Nguồn: hồ sơ vay (CDC), sự kiện giao dịch (stream), dữ liệu cửa hàng đối tác, thiết bị/vị trí.
- ... phần còn lại tự chạy theo khung.

---

## PHẦN E — Những cái bẫy nên tránh

| Bẫy | Vì sao mất điểm | Thay bằng |
|---|---|---|
| Lao vào vẽ kiến trúc ngay | Bỏ qua đúng tiêu chí được chấm nặng nhất | Chạy khung 5 câu hỏi trước |
| Chọn công nghệ "nghe hiện đại" | Cho thấy chọn theo hype, không theo yêu cầu | Chọn đơn giản nhất đủ dùng, nói rõ khi nào cần nâng cấp |
| Sa đà vào model/thuật toán | Đó là phần của DS, không phải giá trị của DE | Tập trung đường đi dữ liệu, nhường model cho DA/DS |
| Chỉ trình bày đường đi "sạch" | Thiếu tư duy vận hành | Thêm phần hỏng-thì-sao (idempotency, DLQ, backfill) |
| Đè nhóm bằng thuật ngữ | Mất điểm teamwork | Giải thích bằng lời dễ hiểu, hỏi ý người khác |
| Im lặng vì sợ sai | Không có gì để chấm | Nêu giả định rồi tiến, sai thì sửa |
