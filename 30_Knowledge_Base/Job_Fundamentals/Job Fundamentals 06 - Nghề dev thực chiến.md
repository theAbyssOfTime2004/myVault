---
tags: [knowledge, software-engineering, debugging, devtools, workflow, fundamentals]
status: active
created: 2026-08-13
series: Job Fundamentals
part: 6 / Nghề dev thực chiến
---

# Job Fundamentals 06 — Nghề dev thực chiến

> **Đây không phải note về công nghệ. Đây là note về *cách làm việc*.**
>
> Toàn bộ nội dung dưới đây là **tri thức ngầm** — thứ người ta học bằng cách ngồi cạnh
> đồng nghiệp có kinh nghiệm, không phải bằng cách đọc sách. Đi thực tập ngắn thì chưa kịp hấp thụ,
> và không ai nghĩ phải dạy vì với họ nó đã hiển nhiên.
>
> **Tin tốt:** đây là phần **học nhanh nhất và hoàn vốn cao nhất** trong cả series.
> Spark cần vài tuần, DSA cần vài tháng. Mấy thứ ở đây đọc hiểu trong một buổi,
> thành phản xạ sau vài lần dùng thật.
>
> **Cách dùng:** khác các note kia — **không đọc để nhớ, mà đọc rồi làm ngay.**
> Phần XI là bài tập thực hành, không phải câu hỏi lý thuyết.

---

## Mục lục

**I.** [[#I — DevTools điều tra qua trình duyệt]]
**II.** [[#II — Đọc một codebase lạ]]
**III.** [[#III — Git như công cụ điều tra]]
**IV.** [[#IV — Quy trình debug]]
**V.** [[#V — Vòng đời một task]]
**VI.** [[#VI — Pull request và code review]]
**VII.** [[#VII — Test ở mức thực dụng]]
**VIII.** [[#VIII — Log và quan sát hệ thống]]
**IX.** [[#IX — Môi trường và production]]
**X.** [[#X — Giao tiếp phần có đòn bẩy cao nhất]]
**XI.** [[#XI — Bài tập thực hành]]

---
---

# I — DevTools: điều tra qua trình duyệt

Đây là kỹ thuật trung tâm của debug web, và là thứ bạn hay thấy dev có kinh nghiệm làm.

## 1.1 — Quy trình từng bước

**①** Mở **F12** → tab **Network**

**②** Lọc **`Fetch/XHR`** ⭐
Bước quan trọng nhất và hay bị bỏ qua. Không lọc thì thấy hàng trăm request ảnh/CSS/font — nhiễu hoàn toàn. Lọc rồi thì **chỉ còn lệnh gọi API**, thường chỉ vài cái.

**③** Bấm **xoá log** (🚫) để dọn sạch

**④** **Thực hiện đúng hành động đang lỗi** — bấm nút, submit form, load trang

**⑤** Nhìn request nào vừa bắn ra. Cái nào **đỏ (4xx/5xx)** là ứng viên số một

**⑥** Bấm vào request đó:

| Tab | Cho biết gì |
|---|---|
| **Headers** | URL đầy đủ · method · **mã trạng thái** · token xác thực |
| **Payload** | Frontend **gửi lên** cái gì |
| **Response** | Server **trả về** cái gì (thô) |
| **Preview** | JSON đã format cho dễ đọc |
| **Timing** | Thời gian nằm ở đâu — dùng khi điều tra *"sao chậm"* |
| **Initiator** | ⭐ **Đoạn code frontend nào đã gọi request này** |

**⑦** Chuột phải → **Copy as cURL** → chạy lại độc lập trong terminal hoặc Postman

## 1.2 — Vì sao nó tìm ra được code

Chỗ mấu chốt mà không ai nói ra:

> **Ba lớp: giao diện người dùng ↔ URL của API ↔ code backend.**
> **URL chính là cây cầu nối hai đầu.**

**Tìm code frontend:** cột **Initiator** hiện ngăn xếp lời gọi đã kích hoạt request. Bấm vào → nhảy thẳng tới file JS và số dòng.

**Tìm code backend:** đã biết `POST /api/v1/orders/123/cancel` → vào repo backend **grep `orders` + `cancel`** trong thư mục routes → ra đúng hàm xử lý.

**Đó là toàn bộ trick.** Người không biết phải đọc mò cả repo; người biết đi thẳng tới nơi trong 30 giây.

## 1.3 — Bảng phân loại nhanh: lỗi nằm ở đâu

Đây là thứ tiết kiệm nhiều giờ nhất — **cắt bài toán làm đôi trước khi bắt đầu tìm**:

| Quan sát ở tab Network | Kết luận |
|---|---|
| **Request không hề bắn ra** | Lỗi **frontend** — chưa tới server. Kiểm tra event handler, validation phía client |
| Bắn ra, trả về **4xx** | **Frontend gửi sai** — thiếu trường, sai định dạng, thiếu/hết hạn token |
| Bắn ra, trả về **5xx** | **Backend hỏng** — không phải lỗi bạn nhìn thấy trên giao diện |
| **200 nhưng dữ liệu sai** | Lỗi **logic backend** |
| **200, dữ liệu đúng, màn hình vẫn sai** | Lỗi **hiển thị frontend** |

## 1.4 — Các chiêu DevTools khác

**• `Preserve log`** — giữ log qua các lần chuyển trang.
**Bắt buộc khi debug luồng đăng nhập** — trang redirect là log bị xoá sạch.

**• Lọc theo mã trạng thái** — gõ `status-code:500` vào ô filter.

**• Console: chạy `fetch()` trực tiếp** — thử endpoint ngay trong trang, **cookie phiên đã có sẵn**, không phải dựng lại đăng nhập trong Postman:

```javascript
fetch('/api/v1/orders', {method: 'GET'})
  .then(r => r.json()).then(console.log)
```

**• Application → Local Storage / Cookies** — nơi token thật nằm.
Dùng khi điều tra *"sao tự nhiên bị đăng xuất"*.

**• Sources → XHR breakpoint** — dừng chương trình **ngay khi** có request tới URL chứa chuỗi nào đó. Rất mạnh khi không biết code nào gọi nó.

**• Throttling** — giả lập mạng chậm, tái hiện bug chỉ xuất hiện khi mạng yếu.

**• Disable cache** — loại trừ nguyên nhân "trình duyệt vẫn dùng bản cũ".

## 1.5 — Postman và cURL: chỉ là bốn thứ

Rối Postman gần như luôn là **chưa có mô hình về HTTP request**. Một request chỉ gồm **đúng bốn thứ**:

| | Là gì | Hay sai chỗ nào |
|---|---|---|
| **Method** | GET / POST / PUT / PATCH / DELETE | Gửi POST vào route chỉ nhận GET |
| **URL** | Địa chỉ + query param `?limit=10` | Nhầm query param với path param |
| **Headers** | `Content-Type`, `Authorization`, `Accept` | **Gửi JSON nhưng quên `Content-Type: application/json`** |
| **Body** | JSON / form-data / raw | Chọn `form-data` khi server đợi JSON → 422 |

**Postman là cái form có bốn ô đó. cURL cũng vậy. `requests` của Python cũng vậy.**
Ba thứ khác vỏ, cùng ruột.

### Mã trạng thái phải phân biệt được

| Mã | Nghĩa | Hành động |
|---|---|---|
| **401** | Chưa xác thực | Kiểm tra token có gửi không, có hết hạn không |
| **403** | Đã xác thực nhưng **không có quyền** | Vấn đề phân quyền, không phải đăng nhập |
| **404** | Không có route, hoặc không có tài nguyên | Kiểm tra path, prefix, dấu `/` cuối |
| **422** | Dữ liệu gửi lên sai định dạng | **FastAPI trả về body nói rõ sai ở trường nào** — hầu hết người mới không đọc |
| **429** | Vượt giới hạn tốc độ | Cần backoff |
| **500** | Lỗi phía server | **Lỗi của bạn** — đi xem log server |
| **502 / 504** | Gateway lỗi / hết giờ | Service phía sau chết hoặc chạy quá lâu |

## 1.6 — Đọc API docs: checklist 7 điểm

Mở bất kỳ tài liệu API nào, tìm **đúng 7 thứ này theo thứ tự**:

**①** Base URL — có môi trường sandbox không
**②** Xác thực — kiểu gì, đặt vào đâu, tên header là gì
**③** Endpoint cần dùng — method + path
**④** Hình dạng request — trường nào bắt buộc
**⑤** Hình dạng response — **dữ liệu thật thường lồng trong `data` hoặc `results`**
**⑥** Lỗi — mã trạng thái và định dạng body lỗi
**⑦** Giới hạn — rate limit, phân trang, kích thước trang tối đa

> **Quy tắc quan trọng nhất: tìm ví dụ cURL trong quickstart, chạy y nguyên trước đã.**
> Có **một** lần gọi thành công rồi mới sửa dần thành cái mình cần.
>
> Đa số cảnh rối là do viết cả trăm dòng code rồi mới gọi lần đầu — hỏng thì không biết hỏng ở tầng nào.

---
---

# II — Đọc một codebase lạ

Ngày đầu đi làm: một repo 200 nghìn dòng và một task. **Không ai đọc từ đầu tới cuối.**

## 2.1 — Bắt đầu từ điểm vào, không từ đầu file

**Điểm vào** là chỗ chương trình thật sự bắt đầu chạy:

- Một **route** (web app)
- Một câu lệnh **CLI**
- Một **job** trong scheduler
- Hàm **`main()`**
- Hoặc — thường tốt nhất — **một bài test**

## 2.2 — Ba đường tìm nhanh nhất

| Có gì trong tay | Grep cái gì |
|---|---|
| Thấy lỗi trên màn hình | **Copy nguyên văn câu lỗi** rồi grep cả repo |
| Biết URL từ tab Network | Grep đoạn path |
| Thấy một nhãn trên giao diện | Grep chuỗi đó |

> **Grep nguyên văn câu thông báo lỗi** hiệu quả đến mức bất ngờ.
> Chuỗi đó thường chỉ xuất hiện **đúng một chỗ** trong toàn bộ mã nguồn — và đó là chỗ bạn cần.

## 2.3 — Lần theo *một* luồng từ đầu đến cuối

Chọn **một** chức năng, đi trọn vẹn:

```
route → handler → service → repository → truy vấn DB
```

**Hiểu một luồng trọn vẹn có giá trị hơn đọc lướt hai mươi file.** Vì kiến trúc lặp lại — hiểu một luồng là hiểu khuôn mẫu của cả hệ thống.

## 2.4 — Bốn file đọc trước tiên

| File | Cho biết |
|---|---|
| **`README.md`** | Cách chạy, ít nhất là ý định của tác giả |
| **`docker-compose.yml`** | ⭐ **Hệ thống gồm những dịch vụ nào** — bản đồ kiến trúc trong 20 dòng |
| **`requirements.txt` / `package.json`** | Dùng thư viện gì → đoán được app làm gì |
| **Thư mục `tests/`** | Code **nên** làm gì — rõ hơn comment, không lỗi thời như tài liệu |

## 2.5 — Đọc test để hiểu ý định

Test nói cho bạn biết hành vi mong muốn, và **luôn cập nhật** (vì test sai thì CI đỏ). Tài liệu thì có thể đã lỗi thời từ hai năm trước.

---
---

# III — Git như công cụ điều tra

Ai cũng biết `commit` / `push`. Ba lệnh dưới mới là thứ dev có kinh nghiệm dùng.

## 3.1 — `git blame` — vì sao code lại viết như vậy

```bash
git blame path/to/file.py
git blame -L 40,60 path/to/file.py     # chỉ dòng 40-60
```

Ai sửa dòng này, lúc nào, ở commit nào → mở commit đó đọc mô tả → **hiểu vì sao code lại kỳ cục như vậy**.

**Rất hay cứu bạn khỏi việc "sửa" một thứ vốn cố ý.** Đoạn code trông thừa thãi đó có khi là bản vá cho một sự cố production năm ngoái.

## 3.2 — `git log -S` — truy nguồn một đoạn logic

```bash
git log -S "tên_hàm_nào_đó" --oneline
git log -S "MAGIC_NUMBER" -p          # kèm diff
```

Tìm **commit nào đã thêm hoặc xoá** chuỗi đó. Dùng khi muốn biết một đoạn logic xuất hiện từ đâu và vì lý do gì.

## 3.3 — `git bisect` — tìm commit làm hỏng

```bash
git bisect start
git bisect bad                  # bản hiện tại hỏng
git bisect good v1.2            # bản này còn chạy tốt
# git tự checkout commit giữa → bạn test → trả lời:
git bisect good     # hoặc: git bisect bad
# lặp lại tới khi git chỉ ra thủ phạm
git bisect reset
```

Git **tự chia đôi lịch sử**. 1000 commit → khoảng **10 lần thử**.

> **Đây là binary search áp dụng vào công việc thật** — và là chiêu rất ít người mới biết.
> Nếu có script test tự động, dùng `git bisect run ./test.sh` để git tự chạy hết.

## 3.4 — Vài lệnh điều tra khác

```bash
git log --oneline -- path/to/file.py    # lịch sử của riêng một file
git show <commit>                        # xem trọn một commit
git diff main...HEAD                     # những gì nhánh mình đã đổi
git stash                                # cất dở dang để nhảy sang việc khác
```

## 3.5 — Nếp làm việc chuẩn

**① Một nhánh cho một task.** Không làm trực tiếp trên `main`.

**② Commit nhỏ, thông điệp có nghĩa.**
`fix bug` thì vô dụng. `fix: xử lý null customer_id trong pipeline fraud` thì sáu tháng sau vẫn hiểu.

**③ `pull --rebase` trước khi push.** Giữ lịch sử thẳng, tránh commit merge rác.

**④ Đọc lại diff của mình trước khi mở PR.** *(Xem mục VI.)*

---
---

# IV — Quy trình debug

## 4.1 — Kỷ luật cốt lõi

> **Một giả thuyết tại một thời điểm, và luôn biết điều gì sẽ chứng minh mình sai.**

Kiểu hỏng phổ biến — **debug kiểu bắn shotgun**: sửa 5 chỗ cùng lúc, chạy được, **không biết chỗ nào đã sửa**. Tuần sau hỏng lại từ đầu, và lần này còn thêm 4 thay đổi vô nghĩa nằm trong code.

## 4.2 — Sáu bước

### ① Tái hiện cho ổn định

**Không tái hiện được thì không debug được.** Lúc được lúc không → tìm quy luật trước đã: có phải chỉ với người dùng nào đó? Chỉ khi dữ liệu rỗng? Chỉ sau khi để lâu (token hết hạn)?

### ② Đọc lỗi cho kỹ

Đọc **câu thông báo thật**, tìm **dòng đầu tiên trong stack trace thuộc code của bạn** — phần còn lại là ruột thư viện. Đa số người lướt qua bước này rồi đi đoán.

### ③ Chia đôi đường ống

Chuỗi thường là:

```
client → mạng → routing → handler → logic → DB / API ngoài
```

**Hỏng nằm ở đâu giữa "chạy được" và "không chạy"?**
Log ở chính giữa, rồi chia đôi tiếp. Mỗi lần chia đôi là loại được nửa không gian tìm kiếm.

### ④ Cô lập từng biến

| Thử | Loại trừ được |
|---|---|
| Chạy bằng cURL có hỏng không? | Code client |
| Đưa input cứng vào có hỏng không? | Dữ liệu |
| Chạy local có hỏng không? | Môi trường |
| Bản commit cũ có hỏng không? | Thay đổi gần đây |

### ⑤ Sửa một thứ một lần

### ⑥ Kiểm chứng: bản sửa có giải thích được triệu chứng không?

**Sửa xong mà không nói được vì sao trước đó hỏng thì bạn chưa sửa — bạn chỉ đẩy nó đi chỗ khác.**

Đây là bước hay bị bỏ nhất, và là lý do nhiều bug "đã sửa" quay lại sau vài tuần.

## 4.3 — Với lỗi liên quan API: câu hỏi tách nhanh nhất

> **Lỗi ở request của mình, hay ở response của họ?**

**Copy as cURL** rồi chạy trần:

- **cURL cũng hỏng** → lỗi ở **request** của bạn
- **cURL chạy được** → lỗi ở **code** của bạn

Một thao tác, cắt đôi không gian tìm kiếm.

## 4.4 — Khi bí hẳn

**• Giải thích cho vịt cao su.** Nói to bài toán như đang giải thích cho người khác. Nghe ngớ ngẩn nhưng hiệu quả thật — vì phải diễn đạt thành lời buộc bạn kiểm tra lại các giả định ngầm.

**• Nghi ngờ giả định, không nghi ngờ code.** Bug thường nằm ở chỗ bạn *chắc chắn* là đúng nên không kiểm tra. In ra xem giá trị thật là gì.

**• Đứng dậy đi chỗ khác.** Chuyện sáo nhưng đúng — bế tắc thường là do bám vào một hướng sai.

---
---

# V — Vòng đời một task

## 5.1 — Hỏi cho rõ TRƯỚC khi code

Ticket viết mơ hồ là chuyện thường. **Làm ba ngày theo cách hiểu sai tệ hơn nhiều so với hỏi một câu ở đầu.**

Ba câu nên hỏi khi ticket không rõ:

- *"Kết quả mong đợi cụ thể trông như thế nào?"*
- *"Trường hợp X thì xử lý ra sao?"* (nêu một ca biên cụ thể)
- *"Cái này có phụ thuộc vào việc gì đang làm dở không?"*

## 5.2 — Chia nhỏ và ước lượng

Task nghe như "2 ngày" thì thực tế thường là **4**. Không sao — miễn là **báo sớm khi thấy sẽ trễ**.

> **Người ta không sợ chậm. Người ta sợ chậm mà tới hạn mới biết.**

## 5.3 — Báo tắc nghẽn ngay

Tắc 2 tiếng thì nói. Đừng im lặng đợi tới standup hôm sau.

## 5.4 — Thế nào là xong

"Xong" **không phải** là "code chạy trên máy tôi". Danh sách tối thiểu:

- [ ] Chạy đúng với ca thường **và** vài ca biên
- [ ] Test cũ không vỡ
- [ ] Đã tự đọc lại diff
- [ ] Không còn code debug, biến thừa, `print` bỏ quên
- [ ] Không hardcode thứ đáng lẽ phải là cấu hình
- [ ] Đã cập nhật tài liệu/README nếu có thay đổi cách chạy

---
---

# VI — Pull request và code review

## 6.1 — PR nhỏ

**200 dòng được review kỹ. 2000 dòng nhận một chữ "LGTM"** và mọi lỗi lọt qua.

Task lớn thì chia thành nhiều PR nối tiếp.

## 6.2 — Tự đọc lại diff trước khi mở PR

**Bạn sẽ tự bắt được ~80% góp ý:** code debug bỏ quên, biến không dùng, tên đặt ẩu, file thừa lỡ commit, secret lỡ tay đưa vào.

Đây là thói quen rẻ nhất mà tạo ấn tượng tốt nhất.

## 6.3 — Mô tả PR nói *vì sao*, không nói *cái gì*

Diff đã cho biết *cái gì* rồi.

```markdown
## Vấn đề
Job fraud detection bỏ sót giao dịch có customer_id null,
làm sai ~3% số liệu báo cáo hằng ngày.

## Cách xử lý
Tách dòng null ra nhánh riêng thay vì để chúng dồn vào một partition.

## Đã kiểm chứng thế nào
Chạy lại dữ liệu ngày 2026-08-01, số khớp với bản đối chiếu thủ công.

## Lưu ý cho người review
Chưa xử lý trường hợp seller_id cũng null — đã tạo ticket riêng.
```

## 6.4 — Nhận góp ý

**Review là bàn về code, không phải về bạn.** Chỗ này người mới hay nhạy cảm quá mức, và nó cản việc học.

- Không đồng ý thì **hỏi lý do**, đừng im lặng làm theo, cũng đừng cãi cùn
- Góp ý mà bạn thấy đúng → sửa và **cảm ơn**, không cần xin lỗi dài dòng
- Cùng một góp ý lặp lại nhiều lần → đó là một thói quen cần đổi, ghi lại

---
---

# VII — Test ở mức thực dụng

Fresher không cần TDD, không cần độ phủ 100%. **Ba thứ là đủ:**

**① Chạy test có sẵn TRƯỚC khi sửa gì.**
Để biết cái gì đang hỏng sẵn — **không phải do bạn**. Bỏ bước này thì nửa tiếng sau bạn sẽ ngồi debug một lỗi có từ trước.

**② Viết test cho hàm có logic rắc rối.**
Nơi bạn không chắc mọi trường hợp biên. Không cần test cho getter/setter.

**③ Mỗi bug đã sửa → thêm một test.**
Để nó không quay lại. Đây là loại test có giá trị cao nhất, vì nó chứng minh bug từng tồn tại thật.

**Ca biên hay quên:** rỗng · null · một phần tử · rất lớn · ký tự unicode · số âm · trùng lặp.

---
---

# VIII — Log và quan sát hệ thống

## 8.1 — Log vô dụng vs log debug được

```python
# ❌ Vô dụng
print("here")
print(data)
logger.info("error")

# ✅ Debug được
logger.error("Thanh toán thất bại", extra={
    "request_id": rid,
    "user_id": uid,
    "amount": amount,
    "error": str(e),
})
```

`print("here")` là vô dụng khi nó nằm giữa mười nghìn dòng log của mười người dùng đồng thời.

## 8.2 — Mức log

| Mức | Dùng khi | Có bật ở production không |
|---|---|---|
| `DEBUG` | Chi tiết lúc phát triển | ❌ Thường tắt |
| `INFO` | Sự kiện bình thường — job bắt đầu/kết thúc | ✅ |
| `WARNING` | Bất thường nhưng vẫn chạy — retry, dữ liệu thiếu | ✅ |
| `ERROR` | Hỏng thật, cần người xem | ✅ + cảnh báo |

## 8.3 — Request id

Thứ cho phép **nối các dòng log rời rạc của cùng một request** lại với nhau. Không có nó, log production là một mớ hỗn độn không lần được — vì hàng trăm request đang chạy xen kẽ.

## 8.4 — ⚠️ Không bao giờ log

**Mật khẩu · token · số thẻ · thông tin cá nhân.**

Log thường được gửi sang hệ thống khác, lưu nhiều tháng, và nhiều người xem được. Đây là lỗi bảo mật rất phổ biến và rất dễ tránh.

---
---

# IX — Môi trường và production

## 9.1 — Khác nhau ở đâu

| | Local | Production |
|---|---|---|
| **Cấu hình** | Ghi cứng, file `.env` | **Biến môi trường tiêm vào**, secret ở nơi quản lý riêng |
| **Lỗi** | Traceback hiện ngay màn hình | **Chui vào log, phải đi tìm** |
| **Debugger** | Gắn thoải mái | **Không có. Log là con mắt duy nhất** |
| **Dữ liệu** | Nhỏ, giả | Lớn, thật, có thông tin cá nhân |
| **Triển khai** | Chạy script | Build image → đẩy → deploy → health check → **rollback nếu hỏng** |
| **Hỏng thì** | Bực mình | **Ảnh hưởng người dùng thật** |

## 9.2 — Bốn thói quen sinh ra từ bảng trên

Đây chính là thứ người ta gọi là **"tư duy production"**:

**① Không bao giờ ghi cứng cấu hình.**
Mọi thứ khác nhau giữa các môi trường đều đi qua biến môi trường. Đây là nguyên tắc **12-factor**.

```python
# ❌
DB_URL = "postgres://user:pass@prod-db:5432/app"

# ✅
DB_URL = os.environ["DATABASE_URL"]
```

**② Log phải đủ ngữ cảnh để debug mà không cần debugger.**

**③ Mọi thay đổi phải đảo ngược được.**
Deploy hỏng thì quay về bản cũ trong một phút, không phải ngồi vá dưới áp lực.

**④ Không chạy thứ chưa test lên dữ liệu thật.**
Nghe hiển nhiên. Vẫn là nguồn sự cố số một.

## 9.3 — Vài quy tắc về schema và migration

**• Migration phải tương thích ngược trong lúc triển khai.**
Trong vài phút deploy, code cũ và code mới **cùng chạy**. Xoá cột ngay là code cũ sập.

**• Thêm cột thì an toàn. Xoá hoặc đổi tên thì không.**
Cách đúng là ba bước: thêm cột mới → chuyển dần sang dùng cột mới → *sau đó* mới xoá cột cũ.

**• Job dữ liệu phải chạy lại được (idempotent).**
Chạy hai lần phải ra cùng kết quả. **Ghi đè thì idempotent, cộng dồn thì không.**
Vì mọi job rồi sẽ có lúc phải chạy lại.

---
---

# X — Giao tiếp: phần có đòn bẩy cao nhất

Nghe không giống kỹ thuật. Nhưng đây là thứ quyết định người ta đánh giá bạn thế nào trong **ba tháng đầu** — nhiều hơn cả chất lượng code.

## 10.1 — Biết cách hỏi

**Đặt giới hạn thời gian: tự vật lộn 30–60 phút, rồi hỏi.**

- Hỏi sớm quá → bị coi là không tự xoay xở
- Hỏi muộn quá → **tệ hơn nhiều** — bạn đốt cả ngày cho thứ người khác gỡ trong hai phút

### Khung bốn phần

> **① Tôi đang cố làm X**
> **② Tôi đã thử A, B, C**
> **③ Tôi mong đợi Y nhưng nhận được Z**
> **④ Tôi nghĩ nguyên nhân có thể là W**

Hỏi kiểu này → người trả lời mất 30 giây.
Hỏi *"anh ơi cái này lỗi"* → họ phải khai thác ngược từ đầu. **Đó mới là điều gây khó chịu, không phải việc bạn hỏi.**

**Phần ④ quan trọng nhất** — nó cho thấy bạn có suy nghĩ, kể cả khi đoán sai.

## 10.2 — Nói "tôi không biết"

**Nói thẳng rồi nói tiếp bạn sẽ tìm hiểu thế nào.** Đoán bừa rồi để người khác phát hiện sai mới là thứ làm mất uy tín.

> *"Cái này em chưa làm bao giờ. Em nghĩ hướng tiếp cận sẽ là… — anh thấy có hợp lý không?"*

## 10.3 — Cập nhật chủ động

Task kéo dài vài ngày → **báo tiến độ mà không cần ai hỏi**. Im lặng làm người khác lo, và họ sẽ bắt đầu hỏi — lúc đó bạn đã ở thế bị động.

## 10.4 — Ghi lại

Mọi thứ mất hơn 30 phút để tìm ra thì **ghi lại**. Ba tháng sau bạn sẽ gặp lại nó, và bạn sẽ không nhớ.

---
---

# XI — Bài tập thực hành

> **Note này không kiểm tra bằng cách nói lớn — kiểm tra bằng cách LÀM.**
> Mỗi bài dưới đây làm thật, không đọc rồi gật đầu.

## Nhóm DevTools

**①** Mở một trang web bất kỳ có đăng nhập (Facebook, GitHub, một trang thương mại điện tử).
Lọc `Fetch/XHR`, tìm **request nào tải nội dung chính** của trang. Xem Payload và Response.

**②** Chuột phải request đó → **Copy as cURL** → dán vào terminal và chạy.
Nó có chạy được không? Nếu không thì **thiếu cái gì** — cookie, header, token?

**③** Tìm một trang có nút bấm gọi API. Bấm nút, rồi dùng cột **Initiator** để nhảy tới đoạn code JS đã gọi nó.

**④** Vào tab **Application**, tìm xem token đăng nhập của trang đó được lưu ở đâu.

## Nhóm codebase

**⑤** Lấy một repo mã nguồn mở bạn chưa từng đọc *(gợi ý: một project FastAPI nhỏ trên GitHub)*.
Trong **15 phút**, trả lời: nó gồm những dịch vụ nào · điểm vào ở đâu · một request đi qua những file nào.

**⑥** Trong repo đó, chọn một câu thông báo lỗi bất kỳ trong code, **grep nó**, và xem nó được ném ra từ đâu.

## Nhóm Git

**⑦** Trong repo `myVault` hoặc bất kỳ repo nào của bạn, chạy `git blame` lên một file, mở commit gần nhất và đọc mô tả.

**⑧** Chạy thử `git bisect` một lần cho biết — kể cả khi không có bug thật, cứ chọn một commit cũ làm mốc "good" để đi qua quy trình.

**⑨** Dùng `git log -S "<một chuỗi trong code>"` để tìm commit đã đưa nó vào.

## Nhóm production

**⑩** Lấy một script bất kỳ của bạn đang hardcode đường dẫn hoặc key → **chuyển hết sang biến môi trường**.

**⑪** Thay toàn bộ `print()` debug trong một file bằng `logger` có mức và có ngữ cảnh.

> [!tip] Chuẩn để coi là xong
> Bài **①②③** phải thành phản xạ — làm được trong 2 phút mà không cần nghĩ.
> Đó là thao tác bạn sẽ dùng gần như mỗi ngày khi đi làm.

---

## Liên quan

- [[Job Fundamentals 05 - Backend cho AI-DE]] *(chưa có)* — FastAPI, Docker, deploy
- [[Job Fundamentals 01 - Apache Spark]]
- [[Job Fundamentals 02 - SQL nâng cao]]
- [[Job Fundamentals 03 - Distributed Systems]]
- [[20_KE_HOACH_Job_Fundamentals]] — kế hoạch
