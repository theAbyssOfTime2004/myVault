---
tags: [knowledge, software-engineering, testing, qa, automation, fundamentals]
status: active
created: 2026-09-07
series: Job Fundamentals
part: 7 / Testing
---

# Job Fundamentals 07 — Testing

> **Note này viết cho một người sắp phỏng vấn ở công ty bán công cụ test — nhưng không viết theo đề phỏng vấn.**
> Mục tiêu là hiểu testing như một ngành: nó ra đời để giải quyết cái gì, các tầng của nó,
> chỗ nó thất bại, và khi nào **không** nên test.
>
> **Câu quan trọng nhất trong cả note, đọc trước rồi hãy đọc tiếp:**
> Test không tồn tại để *tìm bug*. Test tồn tại để **cho phép thay đổi code mà không sợ**.
> Ai hiểu điều này thì mọi câu hỏi còn lại đều suy ra được; ai không hiểu thì sẽ đi đếm coverage.
>
> Phần VIII (test hệ thống không tất định) là phần khác biệt nhất — nó là chỗ testing gặp AI,
> và là phần ít người trả lời được.

---

## Mục lục

**I.** [[#I — Vì sao testing tồn tại]]
**II.** [[#II — Từ vựng phải chuẩn]]
**III.** [[#III — Kim tự tháp và các biến thể]]
**IV.** [[#IV — Thế nào là một test tốt]]
**V.** [[#V — pytest, công cụ thực tế]]
**VI.** [[#VI — Coverage đo được gì và không đo được gì]]
**VII.** [[#VII — Flaky test, kẻ thù số một]]
**VIII.** [[#VIII — Test hệ thống không tất định]]
**IX.** [[#IX — Test trong CI/CD]]
**X.** [[#X — E2E và test automation như một ngành]]
**XI.** [[#XI — Khi nào KHÔNG nên test]]
**XII.** [[#XII — Khung trả lời câu chưa gặp]]
**XIII.** [[#XIII — Tự kiểm tra]]

---
---

# I — Vì sao testing tồn tại

## 1.1 — Thế giới trước test tự động

Phần mềm được kiểm bằng người. Có hẳn một vai trò gọi là **manual QA**: đọc bản đặc tả, thao tác tay theo kịch bản, ghi lại chỗ sai.

Cách này hoạt động được với phần mềm phát hành mỗi năm một lần. Nó sụp đổ khi phần mềm bắt đầu **thay đổi liên tục**.

## 1.2 — Hai áp lực làm nảy sinh test tự động

**① Chi phí của lỗi tăng theo thời gian phát hiện.**

| Phát hiện lúc | Chi phí tương đối |
|---|---|
| Đang viết code | 1× |
| Code review | ~5× |
| QA trước phát hành | ~10× |
| Trên production | 30–100× |

Con số cụ thể tuỳ nghiên cứu và đừng trích như chân lý, nhưng **hình dạng của nó thì luôn đúng**: càng muộn càng đắt, vì càng muộn thì càng nhiều thứ đã xây chồng lên chỗ sai.

**② Bài toán hồi quy (regression).**

Sửa một chỗ có thể làm hỏng một chỗ khác không liên quan. Với hệ thống có 500 chức năng, sau mỗi lần sửa mà kiểm tay lại cả 500 thì không ai làm nổi. Nên hoặc là **không kiểm** (và cầu may), hoặc là **không sửa** (và hệ thống chết dần).

Test tự động phá thế lưỡng nan đó. Đây là lý do tồn tại thật sự của nó.

> [!important] Hệ quả cần nhớ
> Giá trị của một bộ test **không nằm ở số bug nó tìm ra hôm nay**, mà ở chỗ nó cho phép
> refactor, nâng thư viện, đổi kiến trúc — những việc mà không có test thì không ai dám chạm vào.
>
> Một codebase không có test không phải là codebase "chưa được kiểm tra".
> Nó là codebase **đã đóng băng**.

## 1.3 — Dòng thời gian

| Mốc | Việc xảy ra |
|---|---|
| 1994 | Kent Beck viết SUnit cho Smalltalk — khai sinh họ xUnit |
| 1997 | JUnit (Beck + Gamma) — test tự động thành phổ thông |
| ~2000 | TDD được đặt tên và cổ vũ cùng phong trào Agile |
| 2000s | Continuous Integration (Fowler) — test chạy tự động mỗi lần commit |
| 2004 | Selenium — điều khiển trình duyệt thật, mở ra ngành test automation cho web |
| 2010s | Selenium WebDriver thành chuẩn W3C; hệ sinh thái công cụ thương mại mọc lên quanh nó |
| 2018+ | Cypress, Playwright — kiến trúc mới, auto-wait, bớt flaky |
| 2023+ | Agent LLM sinh và sửa test; đồng thời xuất hiện bài toán ngược: **test chính hệ thống LLM** |

> [!note] Vì sao mốc 2004 đáng nhớ
> Cả một ngành công cụ test thương mại — bao gồm Katalon — mọc lên trên nền Selenium và Appium.
> Bài toán họ giải không phải "làm sao điều khiển trình duyệt" (Selenium làm được rồi),
> mà là **làm sao để người không phải lập trình viên cũng viết và bảo trì được test**,
> và **làm sao để bộ test không mục ruỗng theo thời gian**. Bài toán thứ hai mới là bài toán khó.

---
---

# II — Từ vựng phải chuẩn

Đây là phần dễ mất điểm nhất vì ai cũng nghĩ mình biết.

## 2.1 — Phân loại theo phạm vi

| Loại | Phạm vi | Tốc độ | Test cái gì |
|---|---|---|---|
| **Unit** | Một hàm / một lớp, tách khỏi phụ thuộc | mili-giây | Logic thuần |
| **Integration** | Vài thành phần thật ghép với nhau (code + DB thật) | trăm mili-giây → giây | Ranh giới giữa các phần |
| **Component / service** | Một service, phụ thuộc ngoài bị giả lập | giây | Hợp đồng của service |
| **Contract** | Thoả thuận giữa bên gọi và bên bị gọi | giây | Hai bên còn khớp nhau không |
| **End-to-end (E2E)** | Toàn hệ thống qua giao diện thật | chục giây → phút | Luồng người dùng thật |

Ranh giới unit/integration **không có định nghĩa phổ quát** — cãi nhau về nó là dấu hiệu của một cuộc phỏng vấn đi lạc. Điều thật sự quan trọng: *test này chạy nhanh hay chậm, và khi đỏ thì có chỉ ra được chỗ hỏng không.*

## 2.2 — Phân loại theo mục đích

**Smoke test** — tập rất nhỏ, chạy trước tiên, trả lời "hệ thống có sống không". Đỏ ở đây thì khỏi chạy tiếp.
**Regression test** — tập tích luỹ, đảm bảo cái từng chạy vẫn chạy. Phần lớn bộ test lâu năm là loại này.
**Acceptance test** — viết theo góc nhìn nghiệp vụ, trả lời "có đúng thứ khách cần không".
**Exploratory test** — người thật dùng thật, không theo kịch bản, đi tìm thứ chưa ai nghĩ tới.

> [!important] Ranh giới hay bị hỏi
> **Test tự động xác nhận cái ta ĐÃ BIẾT phải đúng. Người tìm ra cái ta CHƯA NGHĨ TỚI.**
> Hai thứ này không thay thế nhau. Công ty nào tự động hoá 100% rồi cắt hết exploratory
> sẽ ngừng phát hiện được loại lỗi mới.

## 2.3 — Phân loại theo phi chức năng

Performance · load · stress · soak · security · accessibility · usability · compatibility (trình duyệt, thiết bị, hệ điều hành).

Chỗ hay quên: **những thứ này cũng cần được tự động hoá và đưa vào CI**, không chỉ chạy một lần trước khi phát hành.

## 2.4 — Test double — bảng phải thuộc

Từ vựng chuẩn là của Gerard Meszaros. Người phỏng vấn hỏi "mock khác stub thế nào" rất hay, và phần lớn ứng viên trả lời sai vì gọi mọi thứ là "mock".

| Tên | Là gì | Dùng khi |
|---|---|---|
| **Dummy** | Chỉ để lấp chỗ tham số, không bao giờ được dùng tới | Hàm bắt buộc truyền đối số mà test không quan tâm |
| **Stub** | Trả về giá trị định sẵn | Cần đưa hệ thống vào một trạng thái nhất định |
| **Spy** | Là stub, nhưng ghi lại nó bị gọi thế nào | Muốn kiểm tra sau khi chạy |
| **Mock** | Được lập trình sẵn **kỳ vọng**, tự fail nếu kỳ vọng không thoả | Cần khẳng định một tương tác **phải** xảy ra |
| **Fake** | Bản cài đặt thật nhưng rút gọn | DB trong bộ nhớ, kho lưu bằng dict |

Câu chốt phân biệt:

> **Stub phục vụ kiểm tra trạng thái — "sau khi chạy, kết quả có đúng không".**
> **Mock phục vụ kiểm tra tương tác — "nó có gọi đúng thứ cần gọi không".**

Và câu nói thêm để lộ kinh nghiệm:

> "Tôi ưu tiên fake và stub. Mock kiểm tra tương tác nên nó gắn chặt vào *cách* code làm việc — refactor không đổi hành vi vẫn làm test đỏ. Mock chỉ xứng đáng khi bản thân tương tác mới là thứ cần bảo đảm, ví dụ *phải* gửi đúng một email chứ không phải hai."

---
---

# III — Kim tự tháp và các biến thể

## 3.1 — Kim tự tháp gốc (Mike Cohn)

```
        /\        E2E        — ít, chậm, đắt, sát thực tế nhất
       /  \
      /----\     Integration — vừa
     /      \
    /--------\   Unit        — nhiều, nhanh, rẻ
```

Lý lẽ đằng sau nó **không phải là về số lượng**, mà là về **chi phí trên mỗi đơn vị niềm tin**:

| Tiêu chí | Unit | E2E |
|---|---|---|
| Thời gian phản hồi | mili-giây | phút |
| Chi phí bảo trì | thấp | cao |
| Khi đỏ, biết hỏng ở đâu | ngay lập tức | phải điều tra |
| Độ giống thực tế | thấp | cao |
| Xu hướng flaky | gần như không | cao |

Kim tự tháp là một **kinh nghiệm về kinh tế**, không phải một định luật.

## 3.2 — Phản mẫu: ly kem úp ngược

```
    \--------/   E2E nhiều
     \      /
      \----/     Integration ít
       \  /
        \/       Unit gần như không có
```

Xảy ra khi đội không viết unit test, chỉ dựng một rừng test giao diện. Hậu quả: bộ test chạy 40 phút, đỏ liên miên vì flaky, không ai tin, và cuối cùng bị tắt.

Đây là **cách chết phổ biến nhất của một bộ test**, và cũng là bài toán mà công cụ test thương mại phải đối mặt: khách hàng của họ rất dễ rơi vào hình dạng này.

## 3.3 — Testing Trophy (Kent C. Dodds)

Lập luận: với ứng dụng web hiện đại, **integration test cho tỉ lệ giá trị trên chi phí cao nhất**, còn kiểm tra kiểu tĩnh (type checker, linter) bắt được một lớp lỗi mà không tốn test nào.

```
     ___
    /   \    E2E
   /-----\
  |       |  Integration  ← phình to nhất
   \-----/
    |___|    Unit
   =======   Static (types, lint)
```

Không mâu thuẫn với kim tự tháp — nó chỉ nói rằng khi phần lớn rủi ro nằm ở **chỗ ghép nối** chứ không ở logic thuần, thì nên dồn về tầng giữa.

**Cách nói ở phỏng vấn:** không tuyên bố trung thành với hình nào. Nói theo rủi ro:

> "Hình dạng đúng phụ thuộc vào chỗ rủi ro nằm ở đâu. Code nhiều logic tính toán thì đáy unit phải rộng. Service chủ yếu là ghép API và ghi DB thì unit test gần như chỉ test mock, integration mới có giá trị thật."

---
---

# IV — Thế nào là một test tốt

## 4.1 — Cấu trúc: AAA

```python
def test_discount_applies_to_orders_over_threshold():
    # Arrange — dựng bối cảnh
    order = Order(items=[Item(price=100), Item(price=60)])

    # Act — làm đúng MỘT việc
    total = order.total_with_discount()

    # Assert — khẳng định kết quả
    assert total == 144  # 160 - 10%
```

Biến thể trong BDD là **Given–When–Then**, cùng ý tưởng, khác từ vựng.

## 4.2 — Nguyên tắc FIRST

| Chữ | Nghĩa | Vi phạm điển hình |
|---|---|---|
| **F**ast | Nhanh | Gọi mạng thật, `sleep(2)` |
| **I**solated | Độc lập, không phụ thuộc test khác | Test B chỉ chạy được sau test A |
| **R**epeatable | Chạy lại cho cùng kết quả, ở mọi máy | Phụ thuộc `datetime.now()`, múi giờ, random không seed |
| **S**elf-validating | Tự pass/fail, không cần người đọc log | `print()` rồi tự nhìn |
| **T**imely | Viết gần lúc viết code | Để dồn "sau này viết test" |

## 4.3 — Test hành vi, đừng test cách cài đặt

Đây là **nguyên nhân gốc của phần lớn bộ test bị ghét**.

```python
# ❌ Gắn chặt vào cách cài đặt — đổi tên hàm nội bộ là đỏ
def test_bad():
    svc = PriceService()
    svc._compute_base = Mock(return_value=100)
    svc._apply_tax = Mock(return_value=110)
    assert svc.price() == 110      # test đang mô tả lại code, không kiểm gì cả

# ✅ Gắn vào hành vi — refactor thoải mái, test vẫn có nghĩa
def test_good():
    svc = PriceService(tax_rate=0.1)
    assert svc.price_for(base=100) == 110
```

> [!important] Phép thử một dòng
> **Refactor mà không đổi hành vi thì test có được phép đỏ không?**
> Nếu có → test đó đang test sai thứ. Nó không bảo vệ bạn, nó trói bạn.

## 4.4 — Một test, một lý do để fail

Test đúng thì tên nó đã nói ra chuyện gì hỏng. Đặt tên theo mẫu:

```
test_<đối tượng>_<điều kiện>_<kết quả mong đợi>

test_login_with_expired_token_returns_401
test_chunker_on_empty_document_returns_empty_list
test_retry_stops_after_max_attempts
```

Khi CI đỏ lúc 11 giờ đêm, **cái duy nhất người ta nhìn thấy đầu tiên là tên test**. Tên tốt tiết kiệm hàng giờ.

## 4.5 — Không có logic trong test

Có `if`, `for`, `try` trong test là dấu hiệu test đang cần được test. Thay bằng bảng tham số:

```python
@pytest.mark.parametrize("text, size, expected_chunks", [
    ("",            100, 0),
    ("a" * 50,      100, 1),
    ("a" * 150,     100, 2),
    ("a" * 100,     100, 1),   # đúng biên
])
def test_chunking(text, size, expected_chunks):
    assert len(chunk(text, size)) == expected_chunks
```

## 4.6 — Ca biên phải quét

Rỗng · null/None · đúng một phần tử · rất lớn · unicode và emoji · số âm và số 0 · trùng lặp · sai kiểu · vượt giới hạn · gọi đồng thời · thứ tự đảo.

*(Danh sách ngắn hơn đã có ở [[Job Fundamentals 06 - Nghề dev thực chiến]] mục VII — đây là bản đầy đủ.)*

---
---

# V — pytest, công cụ thực tế

## 5.1 — Vì sao pytest thắng unittest

`assert` trần thay vì `assertEqual` · fixture thay vì `setUp` · parametrize sẵn · hệ plugin lớn · báo lỗi diễn giải được (`assert x == y` in ra chênh lệch cụ thể).

## 5.2 — Fixture

```python
# conftest.py — dùng chung cho cả thư mục, không cần import
import pytest

@pytest.fixture
def sample_docs():
    return [{"id": 1, "text": "hello"}, {"id": 2, "text": "world"}]

@pytest.fixture(scope="session")   # dựng một lần cho cả phiên chạy
def db_engine():
    engine = create_engine("postgresql://localhost/test")
    yield engine                    # phần sau yield là dọn dẹp
    engine.dispose()

@pytest.fixture
def db_session(db_engine):          # fixture dùng được fixture khác
    conn = db_engine.connect()
    tx = conn.begin()
    yield Session(bind=conn)
    tx.rollback()                   # mỗi test tự cuốn lại — test độc lập
    conn.close()
```

| Scope | Dựng lại khi nào |
|---|---|
| `function` (mặc định) | Mỗi test |
| `class` | Mỗi lớp test |
| `module` | Mỗi file |
| `session` | Một lần cho cả lần chạy |

> [!warning] Bẫy scope
> Fixture scope rộng mà **có trạng thái thay đổi được** sẽ làm test phụ thuộc lẫn nhau —
> nguồn gốc kinh điển của "chạy riêng thì xanh, chạy cả bộ thì đỏ".
> Scope rộng chỉ nên dùng cho thứ đắt tiền và **chỉ đọc**.

## 5.3 — Mock: bẫy lớn nhất

```python
# app/service.py
from app.client import fetch_user      # import vào không gian tên của service

# ❌ SAI — patch chỗ nó được ĐỊNH NGHĨA
mock.patch("app.client.fetch_user")

# ✅ ĐÚNG — patch chỗ nó được DÙNG
mock.patch("app.service.fetch_user")
```

**Quy tắc: patch nơi tên được tra cứu, không phải nơi nó được tạo ra.** Đây là câu hỏi phỏng vấn Python rất hay gặp và rất hay bị sai.

## 5.4 — Bộ lệnh dùng hằng ngày

```bash
pytest -x
pytest --lf
pytest -k "retriev and not slow"
pytest -m integration
pytest -q --tb=short
pytest -n auto
pytest -p no:randomly
```

`-x` dừng ở lỗi đầu · `--lf` chỉ chạy lại cái đã fail · `-k` lọc theo tên · `-m` lọc theo marker · `-n auto` chạy song song · `-p no:randomly` tắt xáo thứ tự khi cần điều tra.

## 5.5 — Plugin đáng biết

| Plugin | Giải quyết |
|---|---|
| `pytest-cov` | Đo coverage |
| `pytest-xdist` | Chạy song song |
| `pytest-asyncio` | Test hàm `async` |
| `pytest-randomly` | Xáo thứ tự → phát hiện test phụ thuộc nhau |
| `freezegun` | Đóng băng thời gian |
| `respx` / `responses` | Giả lập tầng HTTP thay vì mock hàm |
| `testcontainers` | Dựng Postgres/Redis thật trong Docker cho integration test |
| `hypothesis` | Property-based testing — sinh input ngẫu nhiên tìm phản ví dụ |

> [!tip] Hypothesis đáng nói riêng
> Thay vì tự nghĩ ca biên, khai báo **tính chất luôn phải đúng** rồi để thư viện đi tìm phản ví dụ:
> ```python
> @given(st.text())
> def test_chunk_then_join_preserves_content(text):
>     assert "".join(chunk(text, 100)) == text
> ```
> Nhắc tới property-based testing ở phỏng vấn là tín hiệu rõ ràng rằng bạn đọc quá mức tối thiểu.

---
---

# VI — Coverage đo được gì và không đo được gì

## 6.1 — Các mức

| Mức | Đo gì |
|---|---|
| **Line** | Dòng nào đã được thực thi |
| **Branch** | Mỗi nhánh `if` đã đi qua cả hai chiều chưa |
| **Path** | Mọi tổ hợp đường đi — bùng nổ tổ hợp, thực tế không dùng |
| **Mutation** | Sửa nhỏ code rồi xem test có bắt được không |

Branch coverage có ích hơn line coverage rõ rệt và nên bật mặc định (`--cov-branch`).

## 6.2 — Điều coverage KHÔNG nói

```python
def test_meaningless():
    result = complicated_function(data)   # coverage 100%
    # ... và không có assert nào
```

**Coverage đo dòng nào đã CHẠY, không đo dòng nào đã được KHẲNG ĐỊNH.**

Nó cũng không nói: đã nghĩ tới ca biên nào chưa · assert có đúng thứ cần không · phần chưa phủ có phải phần rủi ro nhất không.

## 6.3 — Định luật Goodhart

> Khi một thước đo trở thành mục tiêu, nó thôi làm một thước đo tốt.

Ép KPI "coverage 90%" thì đội sẽ đạt 90% — bằng cách test getter/setter và viết test không assert. Con số đẹp lên, chất lượng không đổi.

**Chính sách hợp lý hơn:**
- Đo **diff coverage** (code mới trong PR này) thay vì con số toàn cục
- Quy tắc "không được làm tụt" thay vì một ngưỡng tuyệt đối
- Dùng coverage như **bản đồ tìm chỗ chưa nghĩ tới**, không dùng như điểm số

## 6.4 — Mutation testing: thước đo thật

Công cụ tự sửa code (`>` thành `>=`, xoá một dòng, đổi `True` thành `False`) rồi chạy test. Test không đỏ nghĩa là **đột biến sống sót** → chỗ đó test rỗng nghĩa dù coverage 100%.

Chậm nên không chạy mỗi commit, nhưng chạy một lần trên module quan trọng là cách nhanh nhất để biết bộ test có thật hay không. Công cụ Python: `mutmut`, `cosmic-ray`.

---
---

# VII — Flaky test, kẻ thù số một

## 7.1 — Vì sao nó nguy hiểm hơn test thiếu

Test flaky = lúc xanh lúc đỏ trên cùng một code.

Chuỗi hậu quả: đội quen với chuyện đỏ → chạy lại cho tới khi xanh → **không ai đọc CI đỏ nữa** → một lỗi thật lọt qua giữa đám nhiễu → bộ test mất hoàn toàn công dụng.

> [!important]
> **Một bộ test flaky tệ hơn không có test.** Không có test thì người ta cẩn thận.
> Có test flaky thì người ta tưởng mình được bảo vệ, và bấm chạy lại.

## 7.2 — Bảng nguyên nhân

| Nguyên nhân | Dấu hiệu | Cách chữa |
|---|---|---|
| Thời gian thật | Đỏ lúc nửa đêm, đỏ khi đổi múi giờ | Tiêm đồng hồ, `freezegun`, luôn dùng UTC |
| Ngẫu nhiên không seed | Đỏ ngẫu nhiên, không lặp lại được | Cố định seed, ghi seed vào log |
| Trạng thái dùng chung | Chạy riêng xanh, chạy cả bộ đỏ | Dọn sạch giữa các test, transaction rollback |
| Phụ thuộc thứ tự | Đổi thứ tự là đỏ | `pytest-randomly` để phát hiện, rồi cắt phụ thuộc |
| Mạng thật | Đỏ khi mạng chậm hoặc dịch vụ ngoài lỗi | Mock, hoặc tách sang lane riêng ngoài CI chính |
| Đua bất đồng bộ | Chỉ đỏ khi chạy song song | Chờ theo điều kiện, không chờ theo thời gian |
| `sleep()` cứng | Đỏ trên máy CI yếu | Thay bằng chờ tới khi điều kiện thoả, có timeout |
| Rò tài nguyên | Càng về cuối bộ test càng hay đỏ | Đóng file/connection trong teardown |

## 7.3 — Quy trình xử lý đúng

1. **Phát hiện** — chạy lặp và xáo thứ tự định kỳ; theo dõi tỉ lệ flaky như một chỉ số thật
2. **Cách ly** — chuyển test flaky sang lane riêng để CI chính sạch trở lại
3. **Có vé theo dõi và có hạn** — cách ly là tạm thời, không phải chỗ chôn
4. **Sửa gốc, không retry mù**

> [!warning] Về retry tự động
> Có `--reruns 3` là hợp lý như **lưới an toàn tạm thời**, nhưng nếu nó thành chính sách mặc định
> thì đội vừa mua quyền không bao giờ sửa nguyên nhân. Retry phải được **đếm và báo cáo**,
> chứ không được im lặng.

Đây cũng là câu hỏi rất dễ gặp: *"Team có 200 test, 15 cái flaky, bạn làm gì?"* Trả lời theo đúng bốn bước trên, và **nói rõ rằng bước tốn tiền nhất là bước 4 và không được bỏ**.

---
---

# VIII — Test hệ thống không tất định

Phần khác biệt nhất của note này. Đây là chỗ testing gặp AI, và là câu hỏi mà rất ít ứng viên trả lời có cấu trúc.

## 8.1 — Nhận thức nền: cái vỏ tất định bọc lấy lõi ngẫu nhiên

Một ứng dụng LLM **không** phải là một hộp ngẫu nhiên. Nó là một hệ thống phần mềm bình thường trong đó **một lời gọi hàm** trả về kết quả không tất định.

```
[ HTTP / auth / validate ]   ← tất định
[ routing, phân luồng     ]   ← tất định
[ retrieval, chunk, rank  ]   ← tất định
[ dựng prompt             ]   ← tất định
[ >>> GỌI MODEL <<<       ]   ← KHÔNG tất định
[ parse, validate schema  ]   ← tất định
[ hậu xử lý, ghi DB       ]   ← tất định
```

**Kết luận quan trọng: 80–90% codebase test được bằng cách thông thường.** Câu trả lời bắt đầu bằng việc chỉ ra điều này là câu trả lời của người đã thật sự xây hệ thống loại đó.

## 8.2 — Bốn tầng chiến lược

**Tầng 1 — Phần tất định: test như mọi phần mềm khác.**
Chunker, parser, router, validator, retry logic đều là hàm thuần. Unit test bình thường, không có gì đặc biệt.

**Tầng 2 — Ranh giới với model: mock trong CI.**
CI không được gọi model thật: chậm, tốn tiền, không lặp lại được, và hỏng khi nhà cung cấp gặp sự cố. Mock ở tầng HTTP (`respx`) tốt hơn mock hàm SDK, vì nó vẫn kiểm được phần dựng request.
Ghi lại phản hồi thật một lần rồi phát lại (kiểu VCR) là cách rẻ để có dữ liệu thực tế mà vẫn tất định.

**Tầng 3 — Assert theo tính chất, không theo bằng nhau.**
Với output sinh ra, không so sánh chuỗi. Khẳng định **bất biến**:

| Tính chất | Cách kiểm |
|---|---|
| Đúng schema | Parse bằng Pydantic |
| Có trích nguồn | Mọi câu khẳng định phải map về context đã lấy |
| Không rò dữ liệu | Không chứa PII, không lộ system prompt |
| Trong ngân sách | Số token, độ trễ, chi phí dưới ngưỡng |
| Từ chối đúng lúc | Câu ngoài phạm vi phải nhận được lời từ chối |
| Ổn định | Chạy n lần, tỉ lệ biến thiên dưới ngưỡng |

**Tầng 4 — Chất lượng: eval suite, tách khỏi CI.**
Chất lượng câu trả lời **không phải pass/fail** mà là phân phối. Cần golden set có nhãn, chạy định kỳ (nightly, hoặc khi đổi prompt/model), theo dõi **xu hướng** và đặt **ngưỡng hồi quy** ("không được tụt quá 3% so với bản trước") thay vì một cổng nhị phân.

> [!important] Câu chốt để nói ra
> **"Correctness thì gate được trong CI. Quality thì chỉ theo dõi được theo thời gian.**
> **Nhét quality vào CI như một cổng pass/fail sẽ tạo ra một cổng flaky — mà flaky thì sẽ bị tắt."**

## 8.3 — Bộ chỉ số RAG cần gọi đúng tên

JD của Katalon nêu đích danh **Ragas** và **DeepEval**, nên phải biết chúng đo gì. Nguyên tắc chung: **tách chỉ số của retrieval khỏi chỉ số của generation** — hai chỗ này hỏng vì lý do khác nhau và chữa bằng cách khác nhau.

| Nhóm | Chỉ số | Trả lời câu hỏi |
|---|---|---|
| Retrieval | Context recall | Context lấy về có chứa đủ thông tin để trả lời không |
| Retrieval | Context precision | Phần lấy về có bị loãng bởi đoạn vô quan không |
| Retrieval | recall@k, nDCG, MRR | Xếp hạng có đưa đoạn đúng lên đầu không |
| Generation | Faithfulness / groundedness | Câu trả lời có bịa ngoài context không |
| Generation | Answer relevance | Có trả lời đúng câu được hỏi không |
| Generation | Answer correctness | So với đáp án chuẩn thì đúng tới đâu |

> [!important] Chẩn đoán theo cặp chỉ số
> **Context recall thấp** → lỗi ở retrieval: chunking, embedding, hoặc top-k.
> **Context recall cao nhưng faithfulness thấp** → retrieval ổn, model bịa: lỗi ở prompt hoặc ở model.
> Nói được cặp chẩn đoán này là chứng minh hiểu vì sao phải tách hai nhóm, chứ không chỉ thuộc tên chỉ số.

Cần biết thêm: phần lớn các chỉ số trên **được tính bằng LLM**, nên chúng thừa hưởng mọi giới hạn ở mục 8.4 — kể cả chi phí và độ ổn định.

## 8.4 — LLM-as-judge và giới hạn của nó

Dùng model chấm output của model là công cụ hữu ích, nhưng phải biết nó hỏng ở đâu:

| Thiên lệch | Biểu hiện |
|---|---|
| Position bias | Ưu ái phương án đặt trước trong so sánh cặp |
| Verbosity bias | Chấm câu dài cao hơn câu ngắn đúng |
| Self-preference | Ưu ái văn phong của chính họ model đó |
| Thiếu ổn định | Cùng input, chạy lại ra điểm khác |

Cách dùng có trách nhiệm: **cố định phiên bản model chấm và phiên bản prompt chấm** · temperature 0 · đảo thứ tự khi so sánh cặp rồi lấy trung bình · và quan trọng nhất — **hiệu chuẩn với nhãn người trên một tập con**, báo cáo mức đồng thuận. Judge chưa hiệu chuẩn là một cái thước chưa biết đơn vị.

## 8.5 — Temperature 0 không cho tất định

Cần biết để không nói sai: `temperature=0` giảm ngẫu nhiên lấy mẫu nhưng **không đảm bảo tái lập**. Batching phía nhà cung cấp, thứ tự cộng dồn số thực trên GPU, và việc model được cập nhật ngầm đều làm output đổi. Nên bản thân model phải bị coi là **một phụ thuộc có phiên bản**.

## 8.6 — Nâng model là một lần nâng dependency

Đổi sang bản model mới, hay đổi nhà cung cấp, tương đương nâng một thư viện lõi:
ghim phiên bản model trong cấu hình · chạy toàn bộ eval suite trước khi đổi · so sánh theo từng phân khúc dữ liệu chứ không chỉ điểm tổng · có đường lùi.

Prompt cũng vậy — **prompt là code**: phải nằm trong Git, có phiên bản, đi qua review, và mỗi lần đổi phải chạy lại eval.

## 8.7 — Chỗ nối với test automation

> Phần lớn eval của agent phải viện tới LLM-as-judge **vì không có chân lý nền**.
> Trong test automation thì có: **test chạy pass hay fail là một oracle tất định.**
> Agent sinh ra một test case — có chạy được không, có bắt được bug đã cấy vào không,
> có còn xanh khi giao diện đổi nhẹ không. Đó là tín hiệu mạnh hơn hẳn việc nhờ một model đi chấm.

Cùng nguyên lý với execution-guided evaluation trong khoá luận: **lấy kết quả thực thi làm tín hiệu, thay vì lấy phán đoán của model.**

---
---

# IX — Test trong CI/CD

## 9.1 — Cái gì chạy lúc nào

| Giai đoạn | Chạy gì | Ngân sách thời gian |
|---|---|---|
| Pre-commit hook (máy dev) | Lint, format, type check | vài giây |
| Mỗi push / PR | Unit + integration nhanh | **< 10 phút** |
| Trước khi merge | Thêm contract test, diff coverage | < 15 phút |
| Nightly | E2E đầy đủ, eval suite, performance | không giới hạn |
| Trước khi phát hành | Smoke trên staging | vài phút |

> [!important] Ngưỡng 10 phút
> Bộ test PR vượt quá khoảng 10 phút thì người ta bắt đầu **push rồi bỏ đi làm việc khác**,
> vòng phản hồi đứt, và test mất phần lớn công dụng.
> Giữ nó nhanh quan trọng hơn giữ nó đầy đủ — phần đầy đủ đẩy sang nightly.

## 9.2 — Dữ liệu test

Ba cách, theo thứ tự ưu tiên:
1. **Transaction rollback** — mỗi test chạy trong một transaction rồi cuốn lại. Nhanh và sạch nhất.
2. **Factory** (`factory_boy`) — sinh đối tượng theo nhu cầu, chỉ khai báo trường mình quan tâm. Tốt hơn fixture cứng vì test tự nói lên nó phụ thuộc vào cái gì.
3. **Testcontainers** — dựng Postgres/Redis thật trong Docker. Thật hơn mock, chậm hơn, đáng cho integration test.

Tuyệt đối không: dùng chung một DB dev cho test, hoặc dựa vào dữ liệu có sẵn trong DB.

## 9.3 — Cổng chất lượng hợp lý

Bắt buộc: test xanh · lint và type check sạch · diff coverage không tụt · không có secret trong diff.
Không nên bắt buộc: coverage toàn cục đạt một số cụ thể · e2e đầy đủ trên mỗi PR · điểm eval của LLM.

---
---

# X — E2E và test automation như một ngành

Phần này quan trọng riêng khi phỏng vấn ở công ty làm công cụ test.

## 10.1 — Kiến trúc hai thế hệ

**Selenium/WebDriver** — điều khiển trình duyệt qua một giao thức chuẩn, từ một tiến trình bên ngoài. Ưu: chuẩn W3C, mọi trình duyệt, mọi ngôn ngữ. Nhược: **mọi lệnh là một chuyến đi mạng**, không biết trang "xong" lúc nào → sinh ra văn hoá `sleep()` → flaky.

**Playwright / Cypress** — chạy sát trình duyệt hơn, có **auto-wait** dựng sẵn: chờ phần tử tồn tại, hiện hữu, ổn định, nhận được sự kiện, rồi mới thao tác. Đây là lý do kỹ thuật khiến thế hệ mới bớt flaky hẳn, không phải vì "viết tốt hơn".

## 10.2 — Chiến lược chọn phần tử — nguồn gốc chính của bảo trì

| Cách chọn | Độ bền | Ghi chú |
|---|---|---|
| Theo vai trò + tên (`getByRole("button", name="Submit")`) | Cao | Đồng thời kiểm luôn accessibility |
| Theo text người dùng nhìn thấy | Cao | Vỡ khi đổi ngôn ngữ |
| `data-testid` | Cao | Cần frontend hợp tác thêm thuộc tính |
| CSS class | Thấp | Vỡ khi đổi style |
| XPath tuyệt đối | Rất thấp | Vỡ khi thêm một thẻ `div` |

**Nguyên tắc: chọn theo thứ người dùng nhận biết, không theo cấu trúc DOM.**

## 10.3 — Page Object Model và lời phê bình nó

POM gói mỗi trang thành một lớp, để khi giao diện đổi thì chỉ sửa một chỗ.

Phê bình: POM dễ phình thành lớp khổng lồ và **mô tả trang thay vì mô tả việc người dùng làm**. Screenplay pattern là câu trả lời cho việc đó — tổ chức quanh *actor* và *task* thay vì quanh *trang*.

Biết cả hai và nói được đánh đổi là đủ; không cần theo phe nào.

## 10.4 — Vì sao E2E đắt

Chậm (chục giây mỗi ca) · flaky theo bản chất (mạng, animation, thời gian) · khó chẩn đoán khi đỏ (chỉ biết "luồng hỏng", không biết hỏng ở đâu) · bảo trì nặng (giao diện đổi thường xuyên hơn logic).

**Kết luận thực dụng: E2E chỉ dành cho những luồng mà nếu hỏng thì mất tiền.** Đăng nhập, thanh toán, luồng nghiệp vụ chính. Không dùng E2E để kiểm validate form.

## 10.5 — Bài toán thật của ngành công cụ test

Đây là chỗ nên thể hiện là đã suy nghĩ về sản phẩm của họ:

- **Bảo trì**: test tự động hỏng vì giao diện đổi, chứ không phải vì phần mềm sai — chi phí lớn nhất của cả ngành nằm ở đây
- **Selector tự chữa lành**: khi selector cũ hỏng, tự tìm phần tử tương ứng — hữu ích và cũng nguy hiểm, vì nó có thể che một hồi quy thật
- **Ngưỡng người không lập trình**: low-code để QA thủ công dùng được, mà không tạo ra thứ không bảo trì nổi
- **Thời gian chạy**: hàng nghìn ca E2E cần sharding, chạy song song, và chọn lọc test theo vùng code đã đổi
- **Agent LLM sinh test**: hứa hẹn giảm chi phí viết, nhưng đẩy vấn đề sang **thẩm định** — ai xác nhận test do máy sinh là đúng, và bằng gì

---
---

# XI — Khi nào KHÔNG nên test

Mục này phân biệt người hiểu công cụ với người sùng bái công cụ.

## 11.1 — Không viết test cho

- **Code thăm dò sắp vứt** — prototype để trả lời một câu hỏi rồi bỏ
- **Getter/setter, DTO thuần, hằng số cấu hình** — không có logic thì không có gì để hỏng
- **Thư viện bên thứ ba** — họ tự test rồi; chỉ test **cách mình dùng** nó
- **Framework** — không test rằng FastAPI biết định tuyến
- **Giao diện đang thay đổi mỗi ngày** — tự động hoá sớm là bảo trì ngay điều chưa ổn định

## 11.2 — Khi test có giá trị âm

- Test gắn vào cách cài đặt: cản refactor, không bắt được lỗi thật
- Test flaky không ai sửa: dạy cả đội bỏ qua màu đỏ
- Test viết ra chỉ để nâng coverage: tốn thời gian chạy, tốn thời gian bảo trì, không bảo vệ gì
- Test lặp lại y hệt nhau ở nhiều tầng: sửa một hành vi phải sửa mười chỗ

## 11.3 — Khi người làm tốt hơn máy

Exploratory testing thắng ở: sản phẩm mới chưa rõ hành vi đúng · vấn đề trải nghiệm và thẩm mỹ · lỗi loại "không ai từng nghĩ tới" · usability.

**Tự động hoá xác nhận điều đã biết. Người phát hiện điều chưa biết.**

## 11.4 — Phép tính quyết định

> Tự động hoá một ca test là **một khoản đầu tư có chi phí bảo trì**, không phải một lần chi.
>
> Đáng làm khi: ca đó chạy nhiều lần · hậu quả nếu hỏng lớn · phần đang kiểm đủ ổn định.
> Không đáng khi: chạy một lần · dễ kiểm bằng mắt · phần đang kiểm còn đổi mỗi tuần.

Câu nói được ở phỏng vấn:

> "Tôi không cố tự động hoá mọi thứ. Mỗi test tự động là một tài sản phải nuôi. Nếu chi phí nuôi nó lớn hơn cái nó bảo vệ thì nên xoá — và biết lúc nào nên xoá test cũng là một phần của việc giữ bộ test còn dùng được."

---
---

# XII — Khung trả lời câu chưa gặp

Khi bị hỏi *"bạn sẽ test cái X thế nào"* — X có thể là bất cứ gì — chạy theo sáu bước này. Trả lời có cấu trúc quan trọng hơn trả lời đúng.

**① Hỏi lại cho rõ: hỏng nghĩa là gì.**
> "Trước hết tôi muốn rõ thế nào là hỏng ở đây — sai kết quả, chậm, hay không nhất quán? Vì mỗi loại kiểm bằng cách khác nhau."

**② Tách phần tất định khỏi phần không tất định.**
Nêu ra rằng phần lớn hệ thống là tất định và test bình thường được.

**③ Chọn tầng theo chi phí phản hồi.**
Cái gì unit test được thì đừng đẩy lên E2E. Nêu lý do bằng tốc độ phản hồi và khả năng chỉ ra chỗ hỏng.

**④ Nói rõ cái mình sẽ KHÔNG test.**
Đây là bước phân biệt rõ nhất. Người có kinh nghiệm luôn nêu ranh giới.

**⑤ Nêu cách biết bộ test còn khoẻ.**
Tỉ lệ flaky · thời gian chạy · số lỗi lọt ra production · thời gian trung bình để chẩn đoán một lần đỏ.

**⑥ Nêu đánh đổi mình đang chấp nhận.**
> "Cách này bỏ sót loại lỗi Y. Tôi chấp nhận vì bắt được Y sẽ tốn gấp ba, và Y hiếm."

> [!tip] Khi thật sự không biết
> Nói ra cách mình sẽ tìm hiểu, đừng bịa: *"Tôi chưa làm cái này. Cách tôi sẽ tiếp cận là…
> và thứ tôi sẽ đọc trước là…"* Với vị trí intern, thể hiện được đường đi có giá trị
> gần bằng biết sẵn đáp án.

---
---

# XIII — Tự kiểm tra

Chuẩn: **nói trôi 90 giây, không nhìn note.** Ghi âm lại và nghe — chỗ ngập ngừng chính là chỗ chưa hiểu.

**Nền tảng**
1. Test tồn tại để làm gì, nếu không phải để tìm bug?
2. Tại sao chi phí sửa lỗi tăng theo thời gian phát hiện?
3. Kim tự tháp test dựa trên lập luận kinh tế nào?
4. Ly kem úp ngược hỏng ở đâu, và vì sao nó tự nhiên hình thành?

**Từ vựng**
5. Mock khác stub thế nào? Khi nào nên chọn fake thay cả hai?
6. Vì sao ưu tiên kiểm tra trạng thái hơn kiểm tra tương tác?
7. `mock.patch` phải trỏ vào đâu, và vì sao?

**Chất lượng test**
8. "Test hành vi, không test cách cài đặt" — cho một ví dụ cụ thể của việc làm sai.
9. Có thể đạt coverage 100% mà bộ test vô giá trị không? Bằng cách nào?
10. Mutation testing đo được cái mà coverage không đo được — là cái gì?

**Vận hành**
11. Team có 15 test flaky. Bốn bước xử lý?
12. Vì sao retry tự động là chính sách nguy hiểm?
13. Cái gì chạy trên mỗi PR, cái gì đẩy sang nightly, và vì sao lấy mốc 10 phút?

**Không tất định**
14. Test một hệ thống có output không tất định — trình bày bốn tầng.
15. Context recall thấp và faithfulness thấp chỉ ra hai lỗi khác nhau ở đâu?
16. Vì sao không nên đặt điểm eval của LLM làm cổng pass/fail trong CI?
17. LLM-as-judge có những thiên lệch nào, và hiệu chuẩn nó bằng cách nào?
18. `temperature=0` có cho tái lập hoàn toàn không? Vì sao không?

**Phán đoán**
19. Kể ba trường hợp **không** nên viết test.
20. Khi nào một test có giá trị âm?
21. Người vẫn hơn máy ở loại kiểm thử nào, và vì sao?

---

## Liên quan

- [[Job Fundamentals 06 - Nghề dev thực chiến]] — mục VII là bản rút gọn của note này
- [[Job Fundamentals 05 - Backend cho AI-DE]] — FastAPI, async, serving; test tầng service nối vào đây
- [[Job Fundamentals 03 - Distributed Systems]] — retry, idempotency, xử lý hỏng hóc
- [[20_KE_HOACH_Job_Fundamentals]] — kế hoạch tổng
