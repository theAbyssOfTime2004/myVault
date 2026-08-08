---
tags: [project, job-hunt, interview, data-engineer, home-credit, fraud]
status: active
created: 2026-08-06
event: Department Manager interview — 2026-08-11 (Tue)
---

# BNPL Fraud Case — đào sâu cho vòng Manager

> **Bối cảnh:** đề AC ngày 6/8. Hai người phỏng vấn thứ Ba **đã ngồi trong phòng hôm đó**. Rất có thể họ hỏi lại: *"hôm AC bạn nói về decoy — giờ nghĩ kỹ lại thì sao?"*
> Mục tiêu tài liệu này: **đi xa hơn những gì bạn đã nói hôm 6/8.**
>
> Phần dựng lại đề dựa trên trí nhớ; phần phân tích là mở rộng. Chỗ nào suy đoán mình ghi rõ.

---

## ĐỀ (dựng lại)

**Bối cảnh:** phát hiện gian lận cho giao dịch **Buy Now Pay Later** tại **điểm bán vật lý** (POS), không phải online.

**Grain:** một dòng = một giao dịch của một tài khoản.

**Cột:** `customer_name`, `customer_id`, `seller_id`, `transaction_id`, `transaction_time`, `gps_city`, `longitude`, `latitude`, `amount`, `currency`, `is_fraud`

**Ba phần:**

| Message | Nội dung |
|---|---|
| **1** | Rule **velocity** (thành phố + thời gian) — rule này bỏ sót gì, đã chặt chưa + **data sanity check** |
| **2** | **Sliding window 1 giờ** + **k-means phân cụm centroid theo seller** — kết hợp hai rule được không, nếu được thì đề xuất rule kết hợp |
| **3** | Thiết kế **streaming pipeline**, áp rule của message 1 và 2 vào |

**Ràng buộc:** chỉ streaming, không batch — đề nhắm vào serving độ trễ thấp ngay tại thời điểm giao dịch.

---

# TỔNG HỢP LỖ HỔNG — bản tra nhanh

## A. Dữ liệu & sanity check

- **`is_fraud` được sinh ra từ chính các rule** → nhãn kế thừa toàn bộ điểm mù; train trên đó chỉ học lại rule, không học được gian lận thật
- **Giao dịch bị chặn không bao giờ có nhãn** → dữ liệu train chỉ phản ánh những gì hệ thống cũ cho qua (rejection inference)
- **Nhãn đến muộn** — quyết định 200ms, sự thật vài tuần (chargeback / khiếu nại / không trả kỳ đầu)
- **`gps_city` có thể chỉ là bản nén thô của lat/lon** → dùng city cho velocity là vứt bỏ độ chính xác
- Nếu city và lat/lon độc lập → **độ lệch giữa chúng là feature**; lệch lớn = giả mạo GPS
- **`seller_id` phải có toạ độ ổn định** (POS cố định) → phân tán rộng = POS di động / dữ liệu sai / giả mạo
- **lat/lon null hoặc (0,0)** → rule không kích hoạt = **fail-open thầm lặng**
- **`currency` chưa quy đổi** → mọi ngưỡng theo `amount` vô nghĩa
- **Timezone + clock skew giữa máy POS** → thứ tự sai → "di chuyển bất khả thi" là ảo
- **`transaction_id` trùng** (POS retry) → velocity đếm hai lần → chặn oan khách thật
- **`customer_name` không đủ để nhận diện trùng người** — tên phổ biến, free text, dấu tiếng Việt
- **`amount` lệch phải** → dùng percentile, đừng dùng mean để đặt ngưỡng

## B. Rule velocity

- **Cold start** — giao dịch đầu tiên không có gì để so → **tài khoản mới miễn nhiễm hoàn toàn**
- **Decoy** — giao dịch nhỏ đốt ràng buộc rồi mới đánh lớn *(và chiều ngược: cố tình bị chặn để đầu độc state của nạn nhân)*
- **City quá thô** — 40km trong cùng thành phố, cách 5 phút → không kích hoạt
- ~~Euclid trên độ sai theo hướng đông-tây~~ → **đề đã chốt haversine, lỗ hổng này KHÔNG còn**
- **Ngưỡng tốc độ không phân nấc** — đường bộ hay máy bay? Người đi công tác bị báo động sai
- **Mù hoàn toàn với gian lận trong cùng thành phố** — có lẽ là kịch bản phổ biến nhất
- **Không nhìn số tiền** — 50 nghìn và 50 triệu như nhau
- **Event đến không đúng thứ tự** → sai nếu tính theo processing time
- **Ngưỡng học được** → kẻ gian thăm dò rồi ở ngay bên trong
- **Mù phía seller** — keyed theo customer nên không thấy 40 khách lạ tại một shop trong 1 giờ

## C. Rule phân cụm k-means

- **k-means trên lat/lon thô sai về đo lường** → cụm bị kéo giãn theo hướng đông-tây
- **Centroid + bán kính giả định cụm TRÒN** — khu buôn bán trải dọc đường/sông → **DBSCAN** hợp hơn, lại tự đánh dấu điểm nhiễu
- **Chọn k tuỳ tiện** — k hợp lý ở TP.HCM ≠ ở tỉnh lẻ
- **k-means nhạy với ngoại lệ** — một seller ở xa kéo lệch cả centroid
- **Cửa sổ 1 giờ quá ngắn để fit cụm** → buộc phải train offline → **mâu thuẫn với ràng buộc "chỉ streaming"**
- **Cụm seller ≠ hồ sơ mua sắm của khách** — hai mục tiêu khác nhau, cần làm rõ đề muốn cái nào
- **Bán kính cố định** sai với mật độ khác nhau — 5km ở quận 1 vs ở nông thôn
- **Cold start + du lịch hợp lệ** → chặn oan

## D. Lỗ hổng CẤU TRÚC — sâu nhất

- **Phân mảnh khoá gom nhóm**: một người nhiều tài khoản, hoặc nhiều khách một seller → **mỗi key chỉ 1 giao dịch → không ngưỡng nào chạm được**
- **Chỉnh `amount` không cứu được** — đây là bài toán **trục gom nhóm**, không phải điều kiện lọc
- > **Gian lận nằm ở một mối liên kết mà khoá gom nhóm không nhìn thấy** → cần **entity resolution** + **nhìn theo đồ thị**
- **Mọi ngưỡng đều phá được bằng chia nhỏ** — theo tiền, theo thời gian, hoặc theo **danh tính** (structuring)
- **Ranh giới cố định là ranh giới học được** → làm nhiễu ngưỡng + **giám sát phân phối quanh ngưỡng** (cụm dồn ngay dưới ngưỡng = bằng chứng đang bị dò)

## E. Quyết định BLOCK / REVIEW / ACCEPT

- **Hai ngưỡng, không phải một**
- **Ngưỡng REVIEW do năng lực đội ngũ quyết định**, không do thống kê — vượt năng lực thì hàng đợi âm thầm thành **auto-approve**
- **"Review" nghĩa là gì khi khách đứng ở quầy?** Giao dịch đồng bộ, rà soát bất đồng bộ → phải làm rõ: OTP tại chỗ hay cho qua rồi điều tra
- **Ngưỡng nên đặt trên tổn thất kỳ vọng** (`risk × amount`), không trên risk thuần
- **Không giám sát tỷ lệ ba nhóm** → không phát hiện được fail-open khi feature null hàng loạt

---

# MESSAGE 1 — Velocity rule & sanity check

## 1.1 Sanity check — làm trước khi bàn rule

> Guide của họ nhấn mạnh sanity-check. Và đây là chỗ nhiều người bỏ qua để nhảy thẳng vào rule.

### Vấn đề nghiêm trọng nhất: `is_fraud` được sinh ra TỪ chính các rule này

Đề nói các rule *dùng để gán nhãn fraud*. Vậy nhãn **kế thừa toàn bộ điểm mù của rule**:

- Gian lận mà rule **chưa từng bắt được** → được gán là **không gian lận**
- Train model trên nhãn này → model chỉ học lại **chính các rule đó**, không học được gian lận thật
- Mọi chỉ số precision/recall tính trên nhãn này đều **tự huyễn hoặc**

**Đây là câu đáng nói nhất trong cả message 1.** Nói được:

> "The labels were generated by the rules we're being asked to critique. That means the label set inherits every blind spot the rules have — any fraud the rules never caught is labelled clean. So we can measure how well we reproduce the rules, but not how well we detect fraud. To break that loop we'd need an independent ground truth: confirmed chargebacks, customer disputes, or manual investigation outcomes."

### Nhãn đến muộn (label latency) — HAI chiếc đồng hồ khác nhau

Đừng lẫn hai thứ:

| | Đồng hồ 1 — **QUYẾT ĐỊNH** | Đồng hồ 2 — **SỰ THẬT** |
|---|---|---|
| Là gì | Hệ thống **đoán**: rủi ro, chặn lại | **Xác nhận** giao dịch đó có thật là gian lận không |
| Mất bao lâu | ~200 ms | **Nhiều ngày đến nhiều tuần** |
| Nguồn | Model / rule | Khiếu nại của khách · chargeback · điều tra · BNPL không trả kỳ nào |

Cột `is_fraud` trong dữ liệu đề là **nhãn gắn về sau**, tồn tại vì mọi chuyện đã ngã ngũ. **Lúc giao dịch đang diễn ra thì cột đó không tồn tại** — đó chính là thứ phải đoán.

→ Kéo theo **point-in-time correctness**: feature dùng để train chỉ được lấy từ dữ liệu **trước** thời điểm giao dịch. *(Đúng thứ bạn đã làm trong project Lichess — nối vào được.)*

### Vòng luẩn quẩn: giao dịch bị CHẶN không bao giờ có nhãn ⭐

> Chặn nó → nó không xảy ra → không chargeback, không khiếu nại, **không có gì để xác nhận**.

Bạn chỉ nhận được phản hồi từ những giao dịch **đã cho qua**.

→ Dữ liệu huấn luyện **thiên lệch có hệ thống**: chỉ chứa những gì hệ thống cũ cho là ổn. Trong tín dụng gọi là **rejection inference**.

→ Cách xử lý thực tế: cố tình **cho qua một tỷ lệ nhỏ** giao dịch rủi ro để thu thập nhãn — **chấp nhận mất tiền để mua thông tin**. Cộng với: dùng kết quả điều tra thủ công làm nhãn cho nhóm bị chặn.

> "There's a feedback loop problem: transactions we block never generate a label, because they never happen. So the training data only reflects what the previous system allowed — that's rejection inference. In practice you'd need to deliberately let a small sample of risky transactions through to collect ground truth, and use manual investigation outcomes to label the blocked population."

### `gps_city` vs `longitude/latitude`

*(Cả hai đều là vị trí **khách hàng** tại thời điểm giao dịch.)*

**Kiểm tra 1 — `gps_city` có phải suy ra từ lat/lon không?**
- Nếu **có**: nó là cột thừa, và dùng city cho rule velocity là **tự vứt bỏ độ chính xác** — city là mã hoá cực thô của toạ độ. Làm mạnh thêm lập luận nên dùng haversine.
- Nếu **không** (VD city từ trạm phát sóng, toạ độ từ GPS): chúng có thể lệch hợp lệ, và **mức lệch tự nó là tín hiệu**.

**Kiểm tra 2 — `seller_id` phải có vị trí ỔN ĐỊNH** ⭐

POS là máy **vật lý cố định**; khách phải đứng tại cửa hàng. Suy ra **vị trí khách ≈ vị trí cửa hàng**.

→ Mọi giao dịch của cùng một `seller_id` phải **tụm rất chặt** về toạ độ.

Nếu một `seller_id` có toạ độ **phân tán rộng** → một trong ba:
- Máy POS **di động** (giao hàng tận nơi) — hợp lệ nhưng phải biết
- **Dữ liệu vị trí không đáng tin**
- **Có người giả mạo toạ độ**

→ Đây chính là giả định ngầm mà **rule k-means ở message 2 đang dựa vào**. Kiểm tra giả định đó trước khi dùng rule là đúng tinh thần sanity check.

Đo được bằng: độ lệch chuẩn (hoặc bán kính bao) của toạ độ theo từng `seller_id`. Seller nào phân tán bất thường → cờ đỏ.

### Các kiểm tra khác

| Kiểm tra | Vì sao |
|---|---|
| `lat/lon` = (0,0) | "Null Island" — giá trị sentinel kinh điển khi GPS lỗi |
| `lat/lon` NULL | Rule velocity **im lặng không kích hoạt** → **fail-open**. Kẻ gian chỉ cần vô hiệu hoá GPS |
| Độ chính xác toạ độ | Bị làm tròn còn 2 chữ số thập phân thì sai số ~1km — đủ phá rule khoảng cách |
| `currency` | Có nhiều loại tiền không? Nếu có thì mọi ngưỡng theo `amount` **vô nghĩa** nếu chưa quy đổi |
| `amount` âm / bằng 0 | Hoàn tiền, đảo bút toán — có nên tính vào velocity không? |
| `transaction_time` timezone | UTC hay giờ địa phương? Trộn hai loại là velocity sai hàng loạt |
| **Clock skew giữa các máy POS** | Đồng hồ máy POS lệch nhau vài phút → thứ tự giao dịch sai → "di chuyển bất khả thi" là **ảo** |
| `transaction_id` trùng | Grain có thật sự là một dòng một giao dịch? Retry từ POS có tạo bản ghi trùng? |
| `customer_name` ↔ `customer_id` | Có phải 1-1? **Một người đăng ký hai tài khoản thì velocity mù hoàn toàn** |
| Phân phối `amount` | Lệch phải nặng → dùng percentile, đừng dùng mean để đặt ngưỡng |

> Dòng `customer_name` ↔ `customer_id` là một lỗ hổng lớn: rule velocity keyed theo `customer_id`. Kẻ gian mở hai tài khoản là **thoát hoàn toàn** rule này. Câu hỏi tiếp: có cơ chế phát hiện tài khoản trùng người không (CCCD, số điện thoại, thiết bị)?

## 1.2 Rule velocity — mười lỗ hổng

**Giả định về rule:** cùng `customer_id`, hai giao dịch ở hai thành phố khác nhau trong khoảng thời gian ngắn hơn thời gian di chuyển khả thi → gán fraud.

### 1. Cold start
Giao dịch **đầu tiên** của một khách không có giao dịch trước → rule không thể kích hoạt.
→ Kẻ gian dùng **tài khoản mới**. Toàn bộ rule vô hiệu.

### 2. Tấn công decoy *(insight của bạn hôm AC — nói kỹ hơn)*
Rule chỉ nhìn **cặp giao dịch liên tiếp**. Kẻ gian có thể:
- Bắn một giao dịch nhỏ ở nơi khác để **đốt** ràng buộc velocity
- Giao dịch nhỏ bị chặn → hệ thống coi như đã xử lý xong
- Rồi mới thực hiện giao dịch lớn thật

**Câu hỏi cần đặt để làm rõ cơ chế:** sau khi rule kích hoạt, **state có được reset không?** Nếu có thì đó chính là lỗ hổng. Nếu giao dịch bị chặn vẫn được ghi vào state thì tấn công này khó hơn — nhưng lại sinh ra vấn đề khác: kẻ gian **cố tình làm bị chặn** để đầu độc state của nạn nhân (DoS lên chính khách hàng thật).

*(Đây là hướng mở rộng đáng giá: cùng một lỗ hổng nhìn từ hai phía.)*

### 3. Thành phố là đơn vị quá thô
Hai giao dịch **trong cùng một thành phố** cách nhau 30 giây nhưng ở hai đầu thành phố cũng là bất khả thi — rule không bắt được vì cùng city.

→ **Nên dùng khoảng cách từ lat/lon, không dùng so sánh tên thành phố.** Đây là cải tiến đơn giản nhất và rõ ràng nhất.

### 4. Tính khoảng cách sai
Nếu dùng lat/lon thì **phải dùng haversine**, không dùng Euclid trên đơn vị độ. Một độ kinh tuyến ở vĩ độ 20°N ngắn hơn một độ vĩ tuyến — dùng Euclid là bóp méo khoảng cách theo hướng đông-tây.

### 5. Ngưỡng tốc độ là bao nhiêu?
"Bất khả thi" cần một tốc độ tối đa. Xe máy 40km/h? Ô tô 80? **Máy bay 800?**
→ Hà Nội–TP.HCM trong 2.5 giờ là **hoàn toàn hợp lệ** nếu bay. Rule đặt ngưỡng theo đường bộ sẽ báo động sai hàng loạt với người đi công tác.

### 6. Gian lận trong cùng thành phố hoàn toàn vô hình
Thẻ bị đánh cắp, dùng liên tục trong **một** thành phố → velocity **không bao giờ** kích hoạt. Đây có lẽ là kịch bản gian lận **phổ biến nhất** trong thực tế, và rule này mù hoàn toàn.

### 7. Không nhìn số tiền
Rule đối xử như nhau với giao dịch 50 nghìn và 50 triệu. Rủi ro không nằm ở số lần, mà ở **tiền**.

### 8. Sự kiện đến không đúng thứ tự
Trong streaming, nếu giao dịch B đến trước giao dịch A (mạng trễ), velocity tính theo thứ tự đến sẽ sai.
→ Cần **event time + watermark**, không dùng processing time cho phần tính toán này.

### 9. Ngưỡng học được
Kẻ gian thăm dò để tìm ranh giới thời gian/khoảng cách rồi **ở ngay bên trong**.
→ Xem mục chống gaming ở phần sau.

### 10. Mù phía seller
Velocity keyed theo customer. Một **seller thông đồng** quẹt hàng chục thẻ khác nhau trong một giờ **không bị phát hiện** — vì mỗi customer chỉ có một giao dịch.

→ Đây là hướng bổ sung quan trọng: **cần cả velocity phía seller.**

## 1.3 Cải tiến đề xuất cho message 1

1. Thay so sánh **tên thành phố** bằng **khoảng cách haversine**
2. Tính **tốc độ ngầm định** = khoảng cách / thời gian, so với ngưỡng theo **phương tiện khả dĩ** (có nấc: đường bộ / bay)
3. Chuyển từ **nhị phân** sang **điểm liên tục**: `speed_ratio = implied_speed / max_plausible_speed`
4. Thêm **velocity phía seller**: số customer khác nhau tại một seller trong cửa sổ
5. Xử lý **fail-open**: thiếu lat/lon phải là **tín hiệu rủi ro**, không phải bỏ qua
6. Dùng **event time** cho phép tính, xử lý sự kiện đến trễ
7. Chuẩn hoá **currency** trước mọi ngưỡng theo tiền
8. Kiểm tra **tài khoản trùng người** để bịt lỗ cold start

---

# MESSAGE 2 — Sliding window + k-means, và cách kết hợp

## 2.1 Phê bình rule phân cụm

### Lỗi kỹ thuật rõ nhất: k-means trên lat/lon thô là sai về đo lường

k-means dùng khoảng cách **Euclid**. Trên toạ độ độ (degree), Euclid **không phải khoảng cách thật**:
- 1° vĩ độ ≈ 111 km ở mọi nơi
- 1° kinh độ ≈ 111 km ở xích đạo, nhưng chỉ ≈ **104 km ở vĩ độ 20°N** (Việt Nam)

→ Cụm bị **bóp méo theo hướng đông-tây**. Sai số nhỏ ở quy mô một thành phố nhưng tích luỹ, và sai về mặt nguyên tắc.

**Sửa:** chiếu toạ độ sang hệ mét (UTM) trước khi phân cụm, hoặc dùng thuật toán nhận **haversine** làm metric.

### Centroid + bán kính giả định cụm hình TRÒN

Khu buôn bán thật trải **dọc theo đường, sông, bờ biển** — không tròn. Một hình tròn hoặc bao trùm cả vùng trống, hoặc cắt mất seller thật.

**Thay thế: DBSCAN** — phân cụm theo mật độ, xử lý được hình dạng bất kỳ, và **tự đánh dấu điểm nhiễu** (chính là seller ở vị trí bất thường — đúng thứ ta muốn tìm).

### Chọn k thế nào?

Tuỳ tiện. k quá nhỏ → cụm quá rộng → mọi thứ đều "bình thường". k quá lớn → mỗi seller một cụm → mọi thứ đều "bất thường".
Và k hợp lý ở TP.HCM khác hẳn ở tỉnh lẻ.

### k-means nhạy với ngoại lệ
Một seller ở vị trí xa kéo lệch cả centroid.

### **Cửa sổ 1 giờ quá ngắn để học cụm** ⭐

Đây là mâu thuẫn kiến trúc quan trọng nhất, và là chỗ đáng nêu nhất:

**Không thể học hành vi không gian của khách hàng từ 1 giờ dữ liệu.** Phân cụm cần **lịch sử dài** — hàng tuần, hàng tháng.

→ Suy ra: **mô hình phân cụm phải được huấn luyện ngoài luồng (offline/định kỳ)**, còn tầng streaming chỉ **áp dụng** kết quả đã học.

→ Và điều này **mâu thuẫn với ràng buộc "chỉ streaming, không batch"** của đề. Nêu ra được điểm này là rất mạnh:

> "There's a tension in the brief. Clustering fundamentally requires historical fitting — you can't learn a customer's spatial behaviour from a one-hour window. So while *serving* is streaming-only, the profiles have to be trained periodically offline and pushed to the online store. The streaming layer looks them up; it doesn't fit them."

### Phân cụm SELLER hay phân cụm hành vi CUSTOMER?

Đề nói cụm theo seller. Nhưng cần làm rõ mục đích:
- **Cụm seller** → biết "chợ nằm ở đâu" → phát hiện **seller đăng ký ở vị trí lạ** (merchant giả)
- **Cụm theo customer** → biết "khách này thường mua ở đâu" → phát hiện **giao dịch lệch khỏi thói quen của chính khách**

Hai mục tiêu khác nhau, và cái thứ hai mới bắt được thẻ bị đánh cắp. Đây là **câu hỏi làm rõ** đáng đặt.

### Bán kính cố định là sai với mật độ khác nhau
Bán kính 5km ở quận 1 bao trùm hàng nghìn seller; ở vùng nông thôn thì không bao được gì. → Bán kính nên **thích ứng theo mật độ**.

### Cold start & du lịch hợp lệ
Khách mới không có hồ sơ không gian. Khách đi du lịch giao dịch xa nhà là **hợp lệ** — nếu chỉ dựa vào rule không gian thì sẽ chặn oan.

## 2.2 Kết hợp hai rule — phần đề hỏi thẳng

### Vì sao hai rule BỔ SUNG cho nhau

| Rule | Bắt được gì | Mù chỗ nào |
|---|---|---|
| **Velocity** | Bất khả thi về **thời gian** — một người, hai nơi, quá nhanh | Gian lận **trong cùng khu vực** |
| **Spatial cluster** | Bất thường về **ngữ cảnh** — nơi này lạ với khách này | Gian lận **trong khu vực quen thuộc** |

→ Chúng hỏng theo **hai cách khác nhau**, nên ghép lại phủ được nhiều hơn. Đây là lý do chính đáng để kết hợp, không phải "ghép cho có".

### Vì sao KHÔNG dùng AND hay OR

- **AND** (cả hai cùng kích hoạt): quá chặt. Bỏ sót mọi gian lận chỉ chạm một rule. Precision tăng, **recall sụp**.
- **OR** (một trong hai): quá ồn. False positive bùng nổ, và ở POS thì mỗi false positive là **một khách đứng ở quầy bị từ chối** — chi phí trải nghiệm rất cao.

### Đề xuất: điểm rủi ro có trọng số

Biến mỗi rule từ **nhị phân** thành **điểm liên tục** rồi cộng có trọng số:

```
s1 = velocity_score      = min(1, implied_speed / max_plausible_speed)
s2 = spatial_score       = min(1, distance_to_nearest_normal_cluster / cluster_radius)
s3 = amount_score        = min(1, amount / customer_p95_amount)
s4 = seller_risk         = tỷ lệ fraud lịch sử của seller, LÀM MỊN THEO KHỐI LƯỢNG
s5 = seller_velocity     = số customer khác nhau tại seller này trong cửa sổ 1h

risk = w1·s1 + w2·s2 + w3·s3 + w4·s4 + w5·s5
```

**Lưu ý về `s4`:** phải làm mịn theo khối lượng. Một seller 12 giao dịch với tỷ lệ fraud 100% **không phải bằng chứng**; một seller 800 giao dịch với 15% mới là. *(Đúng bài học S2 vs S4 trong bộ quiz.)*

### Ba hành động: BLOCK / REVIEW / ACCEPT — đề yêu cầu thẳng

Ba lựa chọn nghĩa là **hai ngưỡng**, không phải một:

```
risk  ────────────────────────────────────────────→
      │  ACCEPT  │      REVIEW      │    BLOCK    │
      0        T_low              T_high          1
```

Chỗ đáng nói không phải "có ba bucket", mà là **hai ngưỡng đó đặt bằng cách nào**.

### Điều 1 — Ngưỡng REVIEW do NĂNG LỰC ĐỘI NGŨ quyết định, không do thống kê ⭐

Review nghĩa là **có người thật ngồi xem**. Người thì có giới hạn.

Nếu đội rà soát xử lý được 200 ca/ngày mà ngưỡng của bạn đẩy ra 5.000 ca/ngày thì hàng đợi **vô nghĩa**: ca dồn lại, quá hạn rồi tự động cho qua, hoặc được xem khi đã quá muộn.

→ **`T_low` phải đặt sao cho lượng ca rơi vào dải giữa ≈ năng lực đội, có chừa biên cho ngày cao điểm.**

Đây là ràng buộc **vận hành**, không phải ràng buộc toán học. Rất ít ứng viên fresher nghĩ tới.

> "The review threshold isn't really a statistical choice — it's a capacity constraint. If the analyst team can handle 200 cases a day, the threshold has to produce roughly that volume, with headroom for spikes. Otherwise the queue silently becomes an auto-approve queue."

### Điều 2 — "Review" nghĩa là gì khi khách đang đứng ở quầy? ⭐ *(câu hỏi làm rõ)*

Mâu thuẫn thật: **giao dịch là đồng bộ, rà soát là bất đồng bộ.** Không thể bảo khách đứng chờ 20 phút.

Hai cách hiểu, và **hỏi họ là cách nào** chính là câu hỏi làm rõ đáng giá:

| Cách hiểu | Nghĩa là | Rủi ro |
|---|---|---|
| **Accept-then-review** | Cho qua ngay, gắn cờ điều tra sau | Tiền đã đi rồi; chỉ thu hồi được phần nào |
| **Challenge tại chỗ** | Xác thực bước hai — OTP về điện thoại khách | Chậm ~30 giây, nhưng chặn được gian lận thật |

Với BNPL tại POS, thực tế khả dĩ là **challenge bằng OTP**, hoặc **accept-then-review với trần số tiền**. "Chờ người xem" thuần tuý thì không khả thi trong cửa sổ 200ms.

> "One thing I'd want to clarify: what does 'review' mean operationally at the point of sale? The transaction is synchronous but human review isn't. Realistically it's either step-up authentication in the moment, or accept-with-a-cap and investigate afterwards — those are very different systems."

### Điều 3 — REVIEW chính là nơi SINH RA NHÃN ⭐⭐

Đây là điểm mạnh nhất, vì nó khép lại vòng luẩn quẩn ở mục 1.1:

- Giao dịch **bị chặn** → không có nhãn (không xảy ra nên không có chargeback)
- Giao dịch **cho qua** → có nhãn, nhưng chỉ ở nhóm mà hệ thống đã cho là an toàn
- Giao dịch **được rà soát** → **con người xác nhận trực tiếp** → nhãn sạch, ngay lập tức, đúng ở vùng mơ hồ nhất

→ **Dải REVIEW không chỉ là vùng đệm rủi ro — nó là nhà máy sản xuất nhãn.** Và nó nằm đúng chỗ mô hình cần học nhất: vùng ranh giới.

> "The review band does double duty. It's a risk buffer, but it's also the only place you get clean labels on ambiguous cases — an analyst confirms the outcome directly, immediately, right where the model is most uncertain. That's what breaks the rejection-inference loop."

### Điều 4 — Ngưỡng nên đặt trên TỔN THẤT KỲ VỌNG, không phải trên risk

Rủi ro 0.7 với giao dịch 500 nghìn và rủi ro 0.7 với giao dịch 50 triệu **không thể cùng hành động**.

```
expected_loss = risk_score × amount
```

Đặt ngưỡng trên đại lượng này thay vì trên risk thuần. Kéo theo: giao dịch nhỏ rủi ro cao → cho qua và gắn cờ (chặn không bõ, mà có thể là đòn thăm dò); giao dịch lớn rủi ro trung bình → đẩy sang review.

*Lưu ý cân bằng:* chi phí **chặn nhầm** cũng tăng theo số tiền (mất đơn hàng lớn hơn, cửa hàng đối tác mất doanh thu). Nên công thức đầy đủ phải cân cả hai phía, không chỉ tổn thất do gian lận.

### Điều 5 — Giám sát tỷ lệ ba nhóm

| Tín hiệu | Nghĩa là |
|---|---|
| Tỷ lệ BLOCK nhảy vọt | Gian lận tăng thật, **hoặc** một rule vừa hỏng / dữ liệu đầu vào đổi |
| REVIEW vượt năng lực | Ngưỡng cần chỉnh lại, nếu không hàng đợi thành auto-approve |
| ACCEPT gần 100% | Ngưỡng quá lỏng, hoặc feature đang null hàng loạt (**fail-open thầm lặng**) |

Dòng cuối rất đáng nói: nếu lat/lon bị null hàng loạt thì rule không kích hoạt, mọi thứ được cho qua, và **không có lỗi nào báo**. Tỷ lệ ba nhóm là cách phát hiện.

### Bất đối xứng chi phí — cơ sở để đặt ngưỡng

- **False negative** (bỏ sót): mất tiền, đo được trực tiếp
- **False positive** (chặn nhầm): khách xấu hổ tại quầy, cửa hàng đối tác mất doanh thu, khách có thể bỏ dịch vụ

→ Ngưỡng **không phải quyết định kỹ thuật**. Nó là quyết định kinh doanh dựa trên chi phí kỳ vọng hai loại lỗi. Cần chốt với đội rủi ro.

## 2.3 Chống việc kẻ gian học luật ⭐

Đây là phần mở rộng tự nhiên từ insight decoy của bạn, và gần như chắc chắn không ai khác nói.

**Vấn đề gốc:** rule cố định tạo ra **ranh giới học được**. Kẻ gian thăm dò rồi ở ngay bên trong ranh giới.

**Bốn biện pháp:**

1. **Làm nhiễu ngưỡng** — thêm dao động ngẫu nhiên nhỏ vào ngưỡng, để ranh giới không sắc nét và không xác định được bằng thăm dò.

2. **Thêm thành phần không phải rule** — một model bất thường học từ dữ liệu, không có ranh giới rõ ràng để tìm.

3. **Không tiết lộ lý do chặn** — thông báo cho khách phải mơ hồ, để kẻ gian không biết mình chạm rule nào.

4. **Giám sát META-SIGNAL — điểm mạnh nhất:**

> Nếu ngưỡng là 5 giao dịch/giờ, hãy **theo dõi phân phối số giao dịch mỗi giờ**. Nếu xuất hiện **cụm bất thường ở mức 4**, đó là bằng chứng có người đang **tối ưu ngược lại luật của bạn**.

Nói cách khác: **chính hình dạng phân phối quanh ngưỡng là một tín hiệu phát hiện gian lận.** Đây là loại nhận xét khiến hai người DE nhớ bạn.

> "Any fixed threshold creates a learnable boundary. So I'd monitor the distribution of behaviour *relative to* the thresholds — if transactions start clustering just below a limit, that clustering is itself evidence someone is probing and optimising against the rule. The shape of the distribution near a threshold becomes a detection signal in its own right."

---

# MESSAGE 3 — Streaming pipeline

## 3.1 Kiến trúc

```
POS terminal
   ↓ (HTTPS, đồng bộ — khách đang đứng chờ)
API Gateway / Auth service
   ↓
Kafka  topic: transactions        key = customer_id
   ↓
Flink  (keyed by customer_id)
   ├─ ValueState: giao dịch gần nhất (time, lat, lon)  → tính velocity
   ├─ Sliding window 1h: count, sum(amount), distinct seller
   ├─ Tra Redis: hồ sơ cụm không gian của khách
   ├─ Tra Redis: điểm rủi ro seller
   └─ Tính risk score → quyết định
   ↓
   ├──→ trả quyết định về POS (block / challenge / allow)
   ├──→ ghi state mới vào Redis
   └──→ ghi topic audit (mọi quyết định + lý do)

[Đường huấn luyện định kỳ — offline]
   lịch sử giao dịch → fit cụm không gian per-customer + seller risk
                     → đẩy hồ sơ vào Redis
```

## 3.2 Sáu quyết định thiết kế cần bảo vệ được

### 1. Key theo `customer_id` — và mâu thuẫn với rule phía seller ⭐

Velocity và hồ sơ không gian đều **theo khách**, nên state phải cùng chỗ → key theo `customer_id`.

**Nhưng rule velocity phía seller cần key theo `seller_id`.** Không thể key theo cả hai cùng lúc.

**Giải pháp:** hai luồng keyed song song từ cùng một topic — một keyed theo customer, một keyed theo seller — rồi hợp điểm lại. Hoặc: tính điểm seller ở luồng riêng, ghi vào Redis, luồng customer **tra ra** khi chấm điểm (đơn giản hơn, chấp nhận độ trễ nhỏ).

Nêu được mâu thuẫn này rồi đưa cách xử lý = hiểu sâu về keyed state, không chỉ vẽ hộp.

### 2. Event time hay processing time — câu trả lời KÉP ⭐

Mâu thuẫn thật:
- **Velocity cần event time** — sự kiện đến không đúng thứ tự sẽ tính sai tốc độ
- **Nhưng quyết định chặn không thể chờ watermark** — khách đang đứng ở quầy

**Giải pháp hai đường:**
- **Đường quyết định**: chạy trên **processing time**, quyết trong ngân sách độ trễ, chấp nhận có thể sai với sự kiện đến trễ
- **Đường đối soát**: chạy trên **event time có watermark**, phát hiện những quyết định lẽ ra phải khác, đẩy sang điều tra thủ công và dùng làm phản hồi hiệu chỉnh ngưỡng

Đây là câu trả lời trưởng thành: **không giả vờ rằng chỉ có một lựa chọn đúng.**

### 3. Ngân sách độ trễ — bóc ra thành con số

```
Tổng cửa sổ cho phép     ~300-500 ms
├─ mạng POS → gateway      ~50 ms
├─ gateway → Kafka → Flink ~20 ms
├─ tra Redis (2 lần)       ~5 ms
├─ tính điểm               ~5 ms
└─ trả về POS              ~50 ms
                    còn dư biên an toàn
```
Nói được ngân sách bằng số cho thấy bạn nghĩ như người vận hành.

### 4. Fail-open hay fail-closed — câu hỏi khó nhất ⭐

**Dịch vụ chấm điểm timeout thì làm gì — chặn hết hay cho qua hết?**

- **Fail-closed** (chặn hết): an toàn về gian lận, nhưng **dừng toàn bộ kinh doanh**. Mọi cửa hàng đối tác không bán được.
- **Fail-open** (cho qua hết): kinh doanh chạy, nhưng **mở toang cửa** — và kẻ gian có động cơ gây quá tải hệ thống để tạo ra đúng tình huống đó.

**Câu trả lời thực tế: fail-open có suy giảm.**
- Cho qua, nhưng **hạ trần số tiền** (ví dụ chỉ cho phép dưới 2 triệu)
- Báo động ngay
- Gắn cờ toàn bộ giao dịch trong khoảng thời gian đó để rà lại sau

Nêu được câu hỏi này (và chỉ ra rằng kẻ gian có thể **chủ động tạo ra** sự cố) là mức tư duy rất cao.

### 5. Idempotency
POS retry khi timeout → cùng `transaction_id` gửi hai lần → nếu không khử trùng thì **velocity state bị đếm hai lần**, và khách bị chặn oan.
→ Khử trùng theo `transaction_id` trước khi cập nhật state.

### 6. State TTL và checkpoint
- **State TTL**: keyed theo customer, khách ngừng hoạt động thì state phải được dọn, nếu không state phình vô hạn *(đúng lỗ hổng bạn tự nhận trong project Lichess)*
- **Checkpoint**: mất state nghĩa là mất lịch sử velocity → tạm thời mù. Cần checkpoint xuống object storage
- **Sink idempotent**: ghi quyết định theo `transaction_id` là ghi đè → replay an toàn

## 3.3 Chỗ ràng buộc "không batch" bị vỡ

Nói thẳng và có căn cứ:

> "The brief says streaming only, and for the *decision path* that's right — the answer has to land inside the authorisation window. But two things can't be learned in a stream: the spatial cluster profiles, and the seller risk scores. Both need historical fitting. So I'd separate them: a periodic offline job trains the profiles and pushes them to the online store; the streaming path only looks them up. Serving stays streaming; training doesn't have to be."

Đây là **phản biện đề bài có cơ sở** — đúng thứ đề mời gọi khi ghi "các rule này còn lỗ hổng".

---

# CHUẨN BỊ CHO CÂU HỎI HỌ SẼ HỎI

**"Hôm AC bạn nói về decoy — giờ bạn cải thiện thế nào?"**
→ Mở rộng theo mục 1.2.2: hỏi ngược về cơ chế reset state; chỉ ra lỗ hổng nhìn từ hai phía (kẻ gian đốt ràng buộc, và kẻ gian đầu độc state của nạn nhân); rồi dẫn sang mục chống gaming 2.3 — **ranh giới cố định là ranh giới học được**, và phân phối quanh ngưỡng tự nó là tín hiệu.

**"Bạn thấy rule nào yếu nhất?"**
→ Velocity — vì **mù hoàn toàn với gian lận trong cùng thành phố**, mà đó có lẽ là kịch bản phổ biến nhất. Cộng thêm cold start làm nó vô dụng với tài khoản mới.

**"Nếu chỉ được sửa một thứ?"**
→ Đổi so sánh tên thành phố thành **khoảng cách haversine + tốc độ ngầm định**. Rẻ nhất, bịt được nhiều lỗ nhất, và biến rule nhị phân thành điểm liên tục để kết hợp được với rule khác.

**"Đánh giá hệ thống thế nào?"**
→ Nêu ngay vấn đề nhãn (mục 1.1) — không thể đánh giá tử tế trên nhãn do chính rule sinh ra. Cần ground truth độc lập: chargeback, khiếu nại, kết quả điều tra. Và đo bằng **chi phí kỳ vọng**, không chỉ precision/recall.

**"Scale thì sao?"**
→ Key theo customer_id, số partition đặt theo throughput đỉnh; cẩn thận **skew** nếu có seller/customer siêu hoạt động; state TTL để state không phình; ngân sách độ trễ phải giữ được ở đỉnh, không chỉ ở mức trung bình.
