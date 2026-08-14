---
tags: [knowledge, backend, fastapi, docker, api, ai-engineering, fundamentals]
status: active
created: 2026-08-13
series: Job Fundamentals
part: 5 / Backend cho AI-DE
---

# Job Fundamentals 05 — Backend cho AI/DE

> **Đây không phải "học backend engineering".** Không có microservice, không có thiết kế hệ thống
> quy mô lớn, không tự cài OAuth. Đây là **danh sách ngắn** mà một AI/Data Engineer thật sự cần.
>
> **Phần tay nghề — HTTP anatomy, đọc API docs, debug, log, production —
> nằm ở [[Job Fundamentals 06 - Nghề dev thực chiến]].** Note này lo phần kỹ thuật.
>
> **Cách dùng:** đọc rồi **ship một thứ**. Backend không học được bằng cách đọc.
> Mục XII là bản đặc tả artifact cụ thể.

---

## Mục lục

**I.** [[#I — Vì sao AI-DE cần backend và cần tới mức nào]]
**II.** [[#II — Thiết kế REST]]
**III.** [[#III — Routing hiểu cho hết]]
**IV.** [[#IV — FastAPI]]
**V.** [[#V — Async vs sync cái bẫy lớn nhất]]
**VI.** [[#VI — Serving mô hình]]
**VII.** [[#VII — Gọi API bên ngoài]]
**VIII.** [[#VIII — Database từ phía ứng dụng]]
**IX.** [[#IX — Docker]]
**X.** [[#X — Deploy]]
**XI.** [[#XI — Auth vừa đủ]]
**XII.** [[#XII — Artifact nâng cấp RAG demo]]
**XIII.** [[#XIII — Tự kiểm tra]]

---
---

# I — Vì sao AI/DE cần backend, và cần tới mức nào

## 1.1 — Thực tế công việc ở VN

**AI Engineer** ở phần lớn công ty = **bọc mô hình thành dịch vụ**. Phần "AI" thường là gọi API hoặc tinh chỉnh nhẹ; phần lớn thời gian là code như một backend dev.

**Data Engineer** = viết pipeline, mà pipeline là **phần mềm** — có Git, PR, test, CI, on-call. Cộng thêm việc thường xuyên phải **gọi API bên ngoài để nạp dữ liệu**.

Nên backend ở đây không phải kiến thức phụ trợ. **Nó là công việc.**

## 1.2 — Ranh giới: học gì và KHÔNG học gì

| ✅ Học | ❌ Không học ở giai đoạn này |
|---|---|
| Thiết kế REST cơ bản | GraphQL, gRPC |
| FastAPI | Django, Spring, NestJS |
| Docker + compose | Kubernetes chuyên sâu, Helm |
| Deploy lên một PaaS | Terraform, hạ tầng tự quản |
| API key / hiểu JWT | Tự cài OAuth2, SSO |
| Connection pool, migration | Tối ưu database chuyên sâu |
| Health check, log | Prometheus, Grafana, tracing phân tán |

> **Vượt quá cột trái là học thứ mà vị trí fresher/junior không dùng tới**,
> và thời gian đó nên dồn cho SQL/DSA.

---
---

# II — Thiết kế REST

## 2.1 — Tài nguyên là danh từ, method là động từ

```
❌  POST /getUserById
❌  POST /createNewOrder
❌  GET  /deleteUser?id=5

✅  GET    /users/5
✅  POST   /orders
✅  DELETE /users/5
```

**Quy tắc:** URL mô tả **cái gì**, method mô tả **làm gì với nó**. Dùng **danh từ số nhiều** cho tập hợp.

## 2.2 — Ngữ nghĩa của từng method

| Method | Làm gì | Idempotent | Có body |
|---|---|---|---|
| `GET` | Đọc | ✅ | ❌ |
| `POST` | Tạo mới | ❌ | ✅ |
| `PUT` | Thay thế **toàn bộ** | ✅ | ✅ |
| `PATCH` | Sửa **một phần** | ⚠️ Tuỳ | ✅ |
| `DELETE` | Xoá | ✅ | ❌ |

> **Idempotent = gọi 10 lần cho kết quả giống gọi 1 lần.**
> Bạn đã hiểu khái niệm này từ phần streaming — ở đây **đúng cùng một thứ**, chỉ khác ngữ cảnh.
>
> `PUT /users/5 {name: "A"}` gọi 100 lần → vẫn một user tên A.
> `POST /orders` gọi 100 lần → **100 đơn hàng**.

### Idempotency-Key — mẫu thiết kế đáng biết

Với thao tác `POST` mà lặp lại là tai hoạ (thanh toán, tạo đơn), quy ước phổ biến:

```http
POST /payments
Idempotency-Key: 7f3a9b21-...

→ Server lưu key này cùng kết quả.
→ Request thứ hai với cùng key → trả về kết quả cũ, KHÔNG thực hiện lại.
```

Client bị timeout rồi retry cũng không bị trừ tiền hai lần. **Đây là cách Stripe làm**, và là câu trả lời tốt khi bị hỏi *"làm sao retry an toàn"*.

## 2.3 — Path param vs query param vs body

| | Dùng cho | Ví dụ |
|---|---|---|
| **Path param** | Định danh **một** tài nguyên cụ thể | `/users/5` |
| **Query param** | Lọc, sắp xếp, phân trang | `/users?role=admin&limit=20` |
| **Body** | Dữ liệu tạo/sửa | `POST /users` + JSON |

⚠️ **Không bao giờ đặt thông tin nhạy cảm vào query param** — nó nằm trong log server, lịch sử trình duyệt, và header `Referer`.

## 2.4 — Lồng tài nguyên: chỉ một cấp

```
✅  GET /users/5/orders
❌  GET /users/5/orders/12/items/3/reviews
```

Lồng quá sâu thì URL giòn và khó đổi. Sau một cấp thì dùng tài nguyên phẳng: `GET /reviews?item_id=3`.

## 2.5 — Phân trang: offset vs cursor

| | Cách | Ưu | Nhược |
|---|---|---|---|
| **Offset** | `?limit=20&offset=40` | Dễ hiểu, nhảy trang được | ⚠️ **Có bản ghi mới chèn vào là lệch** — bị lặp hoặc sót |
| **Cursor** | `?limit=20&after=abc123` | Ổn định khi dữ liệu đang đổi | Không nhảy tới trang N được |

**Dữ liệu tĩnh → offset. Dữ liệu đang thay đổi liên tục → cursor.**

## 2.6 — Versioning

```
/api/v1/chat
```

Đặt version vào path ngay từ đầu. Rẻ lúc này, **rất đắt khi phải thêm sau** — vì lúc đó đã có client đang gọi.

---
---

# III — Routing, hiểu cho hết

## 3.1 — Mô hình còn thiếu

Framework web thực chất chỉ là **một bảng tra**:

```python
routes = {
    ("GET",  "/users/{id}"): get_user,
    ("POST", "/chat"):       chat_handler,
}
```

Request tới → so **method + path** với bảng → rút tham số trong path → **gọi hàm của bạn** → giá trị trả về thành response body.

> **`@app.get("/users/{id}")` chỉ làm đúng một việc: ghi vào bảng đó.**
> Nó không gọi hàm, không làm gì khác. Hiểu vậy là hết bí ẩn.

## 3.2 — Bốn nguyên nhân của gần như mọi vụ 404

### ① Prefix của router

```python
router = APIRouter(prefix="/api/v1")

@router.post("/chat")      # path thật là /api/v1/chat
def chat(): ...

app.include_router(router)
```

Path bạn viết **không phải** path thật. Kiểm tra bằng `/docs` — FastAPI liệt kê toàn bộ route thật.

### ② Thứ tự đăng ký

```python
@app.get("/users/{user_id}")    # đăng ký TRƯỚC
def get_user(user_id: str): ...

@app.get("/users/me")            # ❌ KHÔNG BAO GIỜ chạy tới
def get_me(): ...
```

`/users/me` khớp vào `{user_id}` mất rồi — `user_id` nhận giá trị `"me"`.

> **Route cụ thể phải đăng ký TRƯỚC route có tham số.**

### ③ Dấu `/` cuối

`/chat` và `/chat/` có thể là hai thứ khác nhau. FastAPI mặc định redirect (307), nhưng **một số client làm mất method POST khi redirect** → biến thành GET → 405.

### ④ Reverse proxy sửa path

Nginx nuốt `/api` rồi mới chuyển tiếp → app nhận `/chat` trong khi bạn gõ `/api/chat`. Kiểm tra bằng cách log path mà app **thực sự** nhận được.

## 3.3 — Middleware: chạy trước và sau mọi request

```python
@app.middleware("http")
async def add_request_id(request: Request, call_next):
    rid = str(uuid.uuid4())
    request.state.request_id = rid
    response = await call_next(request)      # ← handler chạy ở đây
    response.headers["X-Request-ID"] = rid
    return response
```

Dùng cho: request id, logging, CORS, đo thời gian, xác thực chung.

**Thứ tự quan trọng:** middleware đăng ký sau chạy *ngoài cùng*. Nếu authentication nằm sai vị trí thì có thể bị bỏ qua.

---
---

# IV — FastAPI

## 4.1 — Vì sao FastAPI hợp với AI/DE

**① Pydantic tự validate.** Sai định dạng → trả 422 kèm mô tả rõ trường nào sai. Không phải tự viết kiểm tra.

**② `/docs` tự sinh.** Swagger UI có sẵn, thử API ngay trên trình duyệt. Cực tiện khi demo và khi debug.

**③ Type hint là hợp đồng.** Code Python bình thường, không cú pháp lạ.

**④ Async có sẵn** — quan trọng khi phải chờ mô hình hoặc API bên ngoài.

## 4.2 — Bộ khung tối thiểu nhưng đúng

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Depends, Request
from pydantic import BaseModel, Field
import logging

logger = logging.getLogger(__name__)


# ---------- Vòng đời: nạp model MỘT LẦN ----------
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Đang nạp model...")
    app.state.retriever = load_retriever()      # tốn vài giây
    app.state.llm = load_llm()
    logger.info("Sẵn sàng")
    yield
    # dọn dẹp khi tắt
    app.state.retriever = None


app = FastAPI(title="RAG Service", version="1.0.0", lifespan=lifespan)


# ---------- Schema: hợp đồng vào/ra ----------
class ChatRequest(BaseModel):
    question: str = Field(min_length=1, max_length=2000)
    top_k: int = Field(default=5, ge=1, le=20)


class ChatResponse(BaseModel):
    answer: str
    sources: list[str]


# ---------- Dependency ----------
def get_retriever(request: Request):
    if request.app.state.retriever is None:
        raise HTTPException(status_code=503, detail="Service chưa sẵn sàng")
    return request.app.state.retriever


# ---------- Endpoint ----------
@app.post("/api/v1/chat", response_model=ChatResponse)
def chat(req: ChatRequest, retriever=Depends(get_retriever)):
    try:
        docs = retriever.search(req.question, k=req.top_k)
    except Exception as e:
        logger.exception("Truy xuất thất bại", extra={"question": req.question})
        raise HTTPException(status_code=500, detail="Lỗi truy xuất tài liệu")

    if not docs:
        raise HTTPException(status_code=404, detail="Không tìm thấy tài liệu liên quan")

    answer = generate(req.question, docs)
    return ChatResponse(answer=answer, sources=[d.source for d in docs])


# ---------- Health check ----------
@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/ready")
def ready(request: Request):
    if request.app.state.retriever is None:
        raise HTTPException(status_code=503, detail="model chưa nạp xong")
    return {"status": "ready"}
```

**Sáu điểm đáng chú ý trong đoạn trên** — đây là thứ phân biệt code demo với code chạy được thật:

**①** Model nạp trong `lifespan`, **không nạp trong hàm xử lý**
**②** `Field(...)` đặt ràng buộc — chặn input rác ngay ở cửa
**③** `response_model` → response cũng được validate và tự vào tài liệu
**④** Bắt lỗi rồi **ném `HTTPException` với mã đúng**, không để traceback lọt ra ngoài
**⑤** `logger.exception` giữ nguyên stack trace, kèm ngữ cảnh
**⑥** **Tách `/health` và `/ready`** — xem mục 4.4

## 4.3 — Dependency injection

`Depends()` cho phép tách phần "lấy tài nguyên" khỏi phần "xử lý logic". Lợi ích thật:

- **Test dễ** — thay dependency bằng bản giả, không cần dựng cả app
- **Không lặp code** — xác thực, kết nối DB dùng chung
- FastAPI **tự dọn dẹp** nếu dependency dùng `yield`

```python
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()          # luôn chạy, kể cả khi handler ném lỗi
```

## 4.4 — Health check: `/health` khác `/ready`

| | Trả lời câu hỏi | Nền tảng dùng để |
|---|---|---|
| **`/health`** (liveness) | *Tiến trình còn sống không?* | Chết thì **khởi động lại** |
| **`/ready`** (readiness) | *Đã sẵn sàng nhận request chưa?* | Chưa sẵn sàng thì **chưa gửi traffic tới** |

⚠️ **Rất quan trọng với dịch vụ ML:** model mất 30–60 giây để nạp. Nếu chỉ có `/health` trả 200 ngay, nền tảng sẽ đẩy traffic vào **trước khi model nạp xong** → hàng loạt lỗi 500 mỗi lần deploy.

## 4.5 — Cấu trúc thư mục

```
app/
  main.py            # tạo app, đăng ký router, lifespan
  config.py          # đọc biến môi trường, một chỗ duy nhất
  api/
    v1/
      chat.py        # router
  schemas/           # model Pydantic
  services/          # logic nghiệp vụ — KHÔNG biết gì về HTTP
  core/
    logging.py
tests/
Dockerfile
requirements.txt
.dockerignore
```

> **Nguyên tắc quan trọng nhất: `services/` không được biết gì về HTTP.**
> Không import `Request`, không ném `HTTPException`. Nhờ vậy logic **test được mà không cần dựng server**,
> và tái dùng được cho batch job hay CLI.

---
---

# V — Async vs sync: cái bẫy lớn nhất

Đây là chỗ AI engineer hay sai nhất, và hậu quả rất khó chẩn đoán.

## 5.1 — Hai loại endpoint

```python
@app.post("/a")
def sync_endpoint():        # def thường
    ...

@app.post("/b")
async def async_endpoint(): # async def
    ...
```

| | Chạy ở đâu | Nghẽn thì sao |
|---|---|---|
| **`def`** | FastAPI đẩy sang **threadpool** | Chỉ chiếm một thread, request khác vẫn chạy |
| **`async def`** | Chạy thẳng trên **event loop** | ⚠️ **Nghẽn là cả server đứng** |

## 5.2 — ⚠️ Lỗi kinh điển

```python
# ❌ THẢM HOẠ
@app.post("/chat")
async def chat(req: ChatRequest):
    result = model.generate(req.question)   # blocking, mất 3 giây
    return result
```

`model.generate()` là **CPU-bound và blocking**. Đặt nó trong `async def` → nó **chiếm event loop suốt 3 giây** → **toàn bộ server đứng hình**, kể cả `/health` cũng không trả lời được.

Triệu chứng ngoài đời: *"chạy một mình thì nhanh, hai người dùng cùng lúc là timeout hết"*.

### Ba cách sửa

```python
# ✅ Cách 1 — đơn giản nhất: dùng def thường
@app.post("/chat")
def chat(req: ChatRequest):
    return model.generate(req.question)     # FastAPI tự đưa vào threadpool
```

```python
# ✅ Cách 2 — cần async cho việc khác thì đẩy phần blocking ra executor
@app.post("/chat")
async def chat(req: ChatRequest):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, model.generate, req.question)
```

```python
# ✅ Cách 3 — việc quá lâu thì trả về ngay, xử lý nền
@app.post("/jobs")
def create_job(req: JobRequest, bg: BackgroundTasks):
    job_id = str(uuid.uuid4())
    bg.add_task(run_heavy_job, job_id, req)
    return {"job_id": job_id, "status": "queued"}   # 202 Accepted
```

## 5.3 — Quy tắc quyết định

> **Chờ I/O (gọi API, đọc DB có driver async) → `async def` + `await`.**
> **Tính toán nặng hoặc thư viện blocking (model inference) → `def` thường.**
> **Không bao giờ gọi hàm blocking trong `async def` mà không bọc executor.**

Thư viện blocking hay gặp: `requests`, đa số SDK model, `time.sleep`, phần lớn driver DB đồng bộ.
*(Bản async tương ứng: `httpx`, `asyncio.sleep`, `asyncpg`.)*

---
---

# VI — Serving mô hình

Phần này là chỗ AI engineer khác backend dev thuần.

## 6.1 — Nạp model một lần, không nạp mỗi request

```python
# ❌ Nạp lại mỗi request → chậm khủng khiếp, và RAM nổ
@app.post("/chat")
def chat(req):
    model = load_model()        # 30 giây!
    return model.predict(req)

# ✅ Nạp lúc khởi động, giữ trong app.state
```

## 6.2 — ⚠️ Số worker × kích thước model = RAM thật

```bash
uvicorn app.main:app --workers 4
```

**Mỗi worker là một tiến trình riêng và nạp bản model riêng.**

`4 worker × model 2GB = 8GB RAM`

Đây là nguyên nhân số một của việc **container bị OOM-kill ngay khi khởi động** mà không hiểu vì sao.

| Loại tải | Cấu hình hợp lý |
|---|---|
| Model lớn, chạy trên CPU | **1 worker**, tăng thread nội bộ |
| Model nhỏ | Nhiều worker được |
| Chủ yếu gọi API bên ngoài (như RAG dùng Gemini) | Nhiều worker / async — model không nằm trong RAM |

## 6.3 — Warmup

Lần suy luận đầu tiên thường chậm hơn nhiều (cấp phát bộ nhớ, biên dịch kernel, nạp lười). **Chạy một lần suy luận giả lúc khởi động**, trước khi `/ready` trả OK:

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.model = load_model()
    app.state.model.predict("warmup")     # ← nuốt cú chậm đầu tiên
    yield
```

## 6.4 — Timeout ở mọi tầng

Sinh văn bản có thể chạy rất lâu, hoặc không bao giờ dừng. **Phải có giới hạn ở từng tầng:**

- Tham số `max_tokens` của model
- Timeout khi gọi API bên ngoài
- Timeout của server (`--timeout-keep-alive`)
- Timeout của reverse proxy / nền tảng *(Cloud Run mặc định 300 giây)*

**Thiếu một tầng là cả chuỗi treo.**

## 6.5 — Chọn kiểu giao tiếp

| Kiểu | Khi nào | Ghi chú |
|---|---|---|
| **Đồng bộ** — chờ rồi trả | Dưới ~10 giây | Đơn giản nhất, mặc định |
| **Streaming (SSE)** | Sinh văn bản dài | Người dùng thấy chữ chạy ra, cảm giác nhanh hơn nhiều |
| **Job bất đồng bộ** | Trên ~30 giây | `POST /jobs` → `GET /jobs/{id}` để hỏi trạng thái |

```python
# Streaming bằng Server-Sent Events
from fastapi.responses import StreamingResponse

@app.post("/chat/stream")
def chat_stream(req: ChatRequest):
    def gen():
        for token in model.stream(req.question):
            yield f"data: {token}\n\n"
    return StreamingResponse(gen(), media_type="text/event-stream")
```

---
---

# VII — Gọi API bên ngoài

Phần này DE dùng nhiều hơn AI — nạp dữ liệu từ API là công việc thường ngày.

## 7.1 — ⚠️ Luôn đặt timeout

```python
# ❌ requests MẶC ĐỊNH KHÔNG CÓ TIMEOUT → treo vĩnh viễn
r = requests.get(url)

# ✅
r = requests.get(url, timeout=(3, 30))    # (kết nối, đọc)
```

**Đây là bug production kinh điển:** API đối tác chậm → tiến trình của bạn treo → hết luồng → dịch vụ chết. Không phải lỗi của họ, là **lỗi của bạn vì không đặt timeout**.

## 7.2 — Retry có kỷ luật

**Hai điều kiện phải thoả trước khi retry:**

**① Thao tác phải idempotent.** `GET` retry thoải mái. `POST /payments` thì **không**, trừ khi có Idempotency-Key.

**② Lỗi phải là lỗi tạm thời.**

| Loại lỗi | Retry? |
|---|---|
| Timeout, lỗi kết nối | ✅ |
| `429` quá tải, `503` | ✅ — và **tôn trọng header `Retry-After`** |
| `500` | ⚠️ Một hai lần |
| `400`, `401`, `404`, `422` | ❌ **Retry vô nghĩa** — request sai thì lần nào cũng sai |

### Exponential backoff + jitter

```python
import random, time

def call_with_retry(fn, max_attempts=5):
    for attempt in range(max_attempts):
        try:
            return fn()
        except TransientError:
            if attempt == max_attempts - 1:
                raise
            delay = (2 ** attempt) + random.uniform(0, 1)   # 1, 2, 4, 8... + nhiễu
            time.sleep(delay)
```

**Vì sao cần jitter:** không có nó thì mọi client cùng retry **đúng cùng một thời điểm** — đập sập server ngay khi nó vừa hồi phục. Gọi là *thundering herd*.

## 7.3 — Tái dùng kết nối

```python
# ❌ Mỗi lần gọi lại bắt tay TCP + TLS từ đầu
for url in urls:
    requests.get(url)

# ✅ Dùng chung session → giữ kết nối sống
session = requests.Session()
for url in urls:
    session.get(url, timeout=10)
```

Với hàng nghìn lời gọi, khác biệt là **rất lớn**.

## 7.4 — Phân trang và giới hạn tốc độ

```python
def fetch_all(session, url):
    cursor = None
    while True:
        params = {"limit": 100}
        if cursor:
            params["after"] = cursor
        data = session.get(url, params=params, timeout=30).json()
        yield from data["results"]              # generator, không nạp hết vào RAM
        cursor = data.get("next_cursor")
        if not cursor:
            break
```

**Dùng generator** để không phải giữ toàn bộ kết quả trong bộ nhớ — quan trọng khi API trả về hàng triệu bản ghi.

---
---

# VIII — Database từ phía ứng dụng

## 8.1 — Connection pool

Mở một kết nối DB **tốn hàng chục mili giây** (bắt tay TCP, xác thực). Pool giữ sẵn một số kết nối và tái dùng.

```python
# ❌ Tạo engine trong hàm xử lý → pool mới mỗi request, vô nghĩa
@app.get("/users")
def get_users():
    engine = create_engine(DB_URL)      # SAI

# ✅ Tạo một lần ở cấp module hoặc trong lifespan
engine = create_engine(DB_URL, pool_size=5, max_overflow=10, pool_pre_ping=True)
```

`pool_pre_ping=True` kiểm tra kết nối còn sống trước khi dùng — tránh lỗi *"MySQL server has gone away"* sau khi nhàn rỗi lâu.

⚠️ **`pool_size` × số worker = tổng kết nối tới DB.** Database có giới hạn (Postgres mặc định 100). 10 worker × pool 20 = 200 → **quá giới hạn, app không kết nối được**.

## 8.2 — Vấn đề N+1

```python
# ❌ 1 + N truy vấn
users = db.query(User).all()             # 1 truy vấn
for u in users:
    print(u.orders)                       # +1 truy vấn cho MỖI user

# ✅ 1 truy vấn
users = db.query(User).options(joinedload(User.orders)).all()
```

100 user → **101 truy vấn thay vì 1**. Đây là nguyên nhân chậm phổ biến nhất của ứng dụng dùng ORM, và là câu hỏi phỏng vấn rất hay gặp.

**Cách phát hiện:** bật log SQL và đếm số truy vấn cho một request.

## 8.3 — Migration

**Không bao giờ sửa schema bằng tay trên production.** Dùng công cụ migration (Alembic cho SQLAlchemy) — mọi thay đổi là một file có version, chạy được lại, và revert được.

**Quy tắc an toàn — trong lúc deploy, code cũ và code mới cùng chạy:**

| Thao tác | An toàn |
|---|---|
| Thêm cột cho phép NULL | ✅ |
| Thêm bảng | ✅ |
| **Xoá cột** | ❌ Code cũ vẫn đang đọc nó |
| **Đổi tên cột** | ❌ Tương đương xoá + thêm |
| Thêm NOT NULL vào cột đã có | ❌ Dữ liệu cũ vi phạm |

**Cách đúng để xoá/đổi tên — ba bước, ba lần deploy:**
① thêm cột mới → ② chuyển code sang dùng cột mới → ③ *sau đó* mới xoá cột cũ.

---
---

# IX — Docker

Món giá trị nhất trong cả note này. Học một lần, dùng ở mọi vị trí.

## 9.1 — Image vs container

| | Là gì | Ví von |
|---|---|---|
| **Image** | Khuôn đóng gói bất biến — code + thư viện + hệ điều hành nền | **Class** |
| **Container** | Một tiến trình đang chạy từ image đó | **Instance** |

Một image → chạy được nhiều container. **Container chết là mất hết dữ liệu bên trong** (trừ volume) — đó là chủ ý, không phải nhược điểm.

## 9.2 — Dockerfile đúng cách

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# ⭐ requirements TRƯỚC, code SAU — xem 9.3
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app ./app

# không chạy bằng root
RUN useradd -m appuser
USER appuser

ENV PYTHONUNBUFFERED=1

EXPOSE 8080
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
```

**Hai dòng dễ bỏ sót:**

`PYTHONUNBUFFERED=1` — không có nó thì **log Python bị đệm lại và không hiện ra** trong `docker logs`. Bạn sẽ tưởng app im lặng trong khi nó đang chạy bình thường.

`--host 0.0.0.0` — mặc định uvicorn nghe `127.0.0.1`, nghĩa là **chỉ nghe bên trong container**. Từ ngoài không vào được. Đây là lỗi số một của người mới dùng Docker.

## 9.3 — ⭐ Layer caching: sai lầm phổ biến nhất

Mỗi lệnh trong Dockerfile tạo một **layer** được cache. Layer đổi → **mọi layer sau nó đều phải build lại**.

```dockerfile
# ❌ SAI — đổi một dòng code là cài lại toàn bộ thư viện (3 phút mỗi lần)
COPY . .
RUN pip install -r requirements.txt

# ✅ ĐÚNG — requirements ít đổi, nằm ở layer trước
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
```

**Nguyên tắc: thứ ít thay đổi đặt lên trên, thứ hay thay đổi đặt xuống dưới.**

## 9.4 — `.dockerignore` — đừng quên

```
.git
__pycache__/
*.pyc
.venv/
data/
*.ipynb
.env
```

Không có file này thì `COPY . .` nuốt luôn `.git`, môi trường ảo, dữ liệu — **image phồng từ 200 MB lên vài GB**, và tệ hơn: `.env` chứa secret bị đóng gói vào image.

## 9.5 — Multi-stage build

Khi cần biên dịch thứ gì đó nhưng không muốn công cụ biên dịch nằm trong image cuối:

```dockerfile
FROM python:3.11 AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY ./app ./app
ENV PATH=/root/.local/bin:$PATH
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
```

## 9.6 — docker-compose cho môi trường local

```yaml
services:
  api:
    build: .
    ports:
      - "8080:8080"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/app
    depends_on:
      - db
    volumes:
      - ./app:/app/app          # sửa code là thấy ngay, khỏi build lại

  db:
    image: postgres:16
    environment:
      - POSTGRES_PASSWORD=pass
    volumes:
      - pgdata:/var/lib/postgresql/data

volumes:
  pgdata:
```

**Điểm đáng nhớ: trong compose, các service gọi nhau bằng *tên service*** — `db:5432`, không phải `localhost:5432`. Mỗi container có mạng riêng, `localhost` là chính nó.

## 9.7 — Lệnh dùng hằng ngày

```bash
docker build -t myapp:dev .
docker run -p 8080:8080 --env-file .env myapp:dev
docker ps                          # container đang chạy
docker logs -f <id>                # xem log
docker exec -it <id> /bin/bash     # chui vào trong container
docker compose up --build
docker compose logs -f api
docker system prune -a             # dọn rác, giải phóng ổ đĩa
```

> **`docker exec -it <id> /bin/bash` là chiêu debug quan trọng nhất.**
> Vào bên trong container xem file có đúng không, biến môi trường có được truyền vào không,
> thư viện có cài đủ không. Rất nhiều vụ *"chạy local ngon mà trong Docker thì hỏng"*
> giải quyết xong trong 30 giây bằng lệnh này.

---
---

# X — Deploy

## 10.1 — Chọn nền tảng

| Nền tảng | Ưu | Hợp với |
|---|---|---|
| **Cloud Run** (Google) | Có bậc miễn phí rộng, tự co giãn về 0 | **Khuyến nghị** — trả tiền theo request |
| **Railway / Render** | Dựng nhanh nhất, ít cấu hình | Demo, portfolio |
| **Fly.io** | Nhiều vùng, có volume | Cần lưu trạng thái |
| **HF Spaces** | Miễn phí, cộng đồng AI | Demo ML thuần |

**Đề xuất: Cloud Run** — vì nó dùng đúng Docker image bạn đã build, và trải nghiệm gần với môi trường doanh nghiệp thật nhất.

## 10.2 — Quy trình

```bash
# ① build cho đúng kiến trúc CPU của nền tảng (Mac M-series hay quên chỗ này)
docker build --platform linux/amd64 -t gcr.io/<project>/ragapp:v1 .

# ② đẩy image lên registry
docker push gcr.io/<project>/ragapp:v1

# ③ deploy
gcloud run deploy ragapp \
  --image gcr.io/<project>/ragapp:v1 \
  --region asia-southeast1 \
  --memory 2Gi \
  --set-env-vars "LOG_LEVEL=INFO" \
  --set-secrets "GEMINI_API_KEY=gemini-key:latest"
```

⚠️ **`--platform linux/amd64`**: build trên Mac M1/M2 ra image ARM, nền tảng chạy AMD64 → container khởi động rồi chết ngay với lỗi khó hiểu. **Bẫy này tốn của rất nhiều người cả buổi.**

## 10.3 — Cấu hình và secret

```python
# config.py — một chỗ duy nhất
import os

class Settings:
    api_key: str = os.environ["GEMINI_API_KEY"]      # thiếu là chết ngay lúc khởi động
    log_level: str = os.getenv("LOG_LEVEL", "INFO")  # có mặc định
    max_tokens: int = int(os.getenv("MAX_TOKENS", "1000"))

settings = Settings()
```

**Ba quy tắc:**

**①** Secret **không bao giờ** vào Git. `.env` phải nằm trong `.gitignore`.
**②** Biến bắt buộc dùng `os.environ[...]` để **chết ngay lúc khởi động** nếu thiếu — thay vì chết giữa chừng lúc có người dùng thật.
**③** Đọc cấu hình ở **một chỗ duy nhất**, không rải `os.getenv` khắp code.

> Nếu đã lỡ commit secret lên Git: **xoá khỏi lịch sử là chưa đủ — phải huỷ và cấp lại key đó.**
> Coi như nó đã bị lộ.

## 10.4 — Danh sách kiểm tra trước khi deploy

- [ ] Health check + readiness đã có, và readiness **chờ model nạp xong**
- [ ] Mọi cấu hình đi qua biến môi trường, không hardcode
- [ ] `.dockerignore` có `.env`, `.git`, `data/`
- [ ] Đã đặt timeout ở mọi lời gọi ra ngoài
- [ ] Log có mức và có ngữ cảnh — *(xem [[Job Fundamentals 06 - Nghề dev thực chiến]] mục VIII)*
- [ ] Đã chạy thử **image** ở local, không chỉ chạy code
- [ ] Giới hạn bộ nhớ đủ cho **số worker × kích thước model**
- [ ] Biết cách quay lại bản trước

---
---

# XI — Auth vừa đủ

**Không tự cài OAuth. Không tự viết thuật toán mã hoá.** Chỉ cần hiểu ba thứ:

## 11.1 — API key

Đơn giản nhất, đủ cho dịch vụ nội bộ và portfolio:

```python
from fastapi import Security, HTTPException
from fastapi.security import APIKeyHeader

api_key_header = APIKeyHeader(name="X-API-Key")

def verify_key(key: str = Security(api_key_header)):
    if key != settings.api_key:
        raise HTTPException(status_code=401, detail="API key không hợp lệ")

@app.post("/api/v1/chat", dependencies=[Depends(verify_key)])
def chat(...): ...
```

## 11.2 — JWT — hiểu, không cần tự cài

Một chuỗi gồm ba phần ngăn bởi dấu chấm: `header.payload.signature`

- **Payload chứa thông tin** (user id, quyền, hạn dùng) và **chỉ được mã hoá base64 — ai cũng đọc được**. ⚠️ **Không bao giờ để dữ liệu nhạy cảm trong payload.**
- **Signature** chứng minh token không bị sửa, ký bằng khoá bí mật của server.
- **Stateless** — server không cần lưu phiên, chỉ cần kiểm chữ ký. Đó là ưu điểm chính, và cũng là nhược điểm: **không thu hồi được token trước hạn** trừ khi thêm danh sách đen.

## 11.3 — Vài quy tắc bất di bất dịch

**Luôn dùng HTTPS.** Không có nó thì mọi thứ trên là vô nghĩa.
**Không tự viết hàm băm mật khẩu.** Dùng `bcrypt` hoặc `argon2`.
**Không log token.** *(Xem note 06 mục 8.4.)*
**Đặt hạn dùng ngắn cho access token.**

---
---

# XII — Artifact: nâng cấp RAG demo

Đây là sản phẩm của tuần 2 trong [[20_KE_HOACH_Job_Fundamentals]].

> **Ranh giới phải giữ: KHÔNG thêm tính năng cho con RAG.**
> Chỉ thêm lớp phục vụ. Thêm tính năng là mở mặt trận mới — đúng thứ mà danh sách
> *KHÔNG làm* trong kế hoạch được dựng ra để chặn.

## Phạm vi

```
RAG demo hiện tại
  ├── FastAPI
  │     ├── POST /api/v1/chat        (Pydantic validate)
  │     ├── GET  /health             (liveness)
  │     ├── GET  /ready              (readiness — chờ index nạp xong)
  │     └── /docs                    (tự sinh)
  ├── Model/index nạp trong lifespan, KHÔNG nạp mỗi request
  ├── Cấu hình + secret qua biến môi trường
  ├── Log có mức, có request id
  ├── Xử lý lỗi → mã trạng thái đúng, không lộ traceback
  ├── Dockerfile (đúng thứ tự layer) + .dockerignore
  ├── docker-compose cho local
  ├── Deploy lên Cloud Run — có URL truy cập được
  └── README: kiến trúc, cách chạy, cách gọi thử
```

## Thứ tự làm — mỗi bước một buổi

**Buổi 1** — Bọc FastAPI: một endpoint chạy được, Pydantic validate, `/docs` xem được
**Buổi 2** — Lifespan nạp model, `/health` + `/ready`, xử lý lỗi tử tế
**Buổi 3** — Cấu hình qua biến môi trường, log có ngữ cảnh, request id qua middleware
**Buổi 4** — Dockerfile + `.dockerignore`, chạy được bằng `docker run` ở local
**Buổi 5** — Deploy lên Cloud Run, sửa cho tới khi URL thật trả lời được
**Buổi 6** — README + tự đọc lại toàn bộ diff

## Vì sao artifact này đáng giá gấp đôi

**① Với CV:** nói được *"đã đóng gói và deploy một dịch vụ"* — thứ gần như mọi JD AI Engineer đòi.

**② Với phản xạ production:** deploy thật **ép** bạn phải đưa secret ra biến môi trường (vì không thể commit key), **debug khi không gắn được debugger** (chỉ có log), đọc log của dịch vụ chạy ở nơi khác, và sửa một deploy hỏng.

**Đó là production thu nhỏ.** Không thay được kinh nghiệm đi làm, nhưng đủ để phản xạ quay lại sau thời gian nghỉ.

---
---

# XIII — Tự kiểm tra

## Nói thành tiếng

**①** Vì sao không được gọi hàm blocking trong `async def`? Triệu chứng khi làm sai là gì?
**②** `/health` và `/ready` khác nhau thế nào? Vì sao dịch vụ ML **bắt buộc** phải tách hai cái?
**③** Bốn nguyên nhân phổ biến của lỗi 404 khi routing?
**④** Vì sao `COPY requirements.txt` phải đứng trước `COPY . .` trong Dockerfile?
**⑤** Khi nào được retry một request, khi nào không? Vì sao cần jitter?
**⑥** Idempotent nghĩa là gì? Method nào idempotent, method nào không?
**⑦** Vấn đề N+1 là gì, phát hiện bằng cách nào?
**⑧** 4 worker × model 2GB thì tốn bao nhiêu RAM? Vì sao?
**⑨** Migration nào an toàn khi deploy, migration nào không? Xoá một cột thì làm ba bước ra sao?

## Làm thật

**⑩** Viết một FastAPI có `/health`, một POST endpoint dùng Pydantic, và chạy được `/docs`.
**⑪** Đóng gói nó vào Docker, chạy bằng `docker run`, gọi được từ máy thật.
**⑫** Cố tình làm hỏng: bỏ `--host 0.0.0.0` đi rồi thử gọi. Quan sát lỗi, hiểu vì sao.
**⑬** `docker exec -it` chui vào container đang chạy, kiểm tra biến môi trường bằng `env`.
**⑭** Deploy lên Cloud Run hoặc Railway. **Có URL công khai gọi được.**

> [!tip] Chuẩn để coi là xong
> Câu **①②④⑧** là bốn câu hay được hỏi nhất, và cũng là bốn lỗi hay gặp nhất khi làm thật.
> Bài **⑭** là mốc của tuần 2 — chưa có URL chạy được thì chưa xong.

---

## Liên quan

- [[Job Fundamentals 06 - Nghề dev thực chiến]] — HTTP anatomy, đọc API docs, debug, log, production
- [[Job Fundamentals 03 - Distributed Systems]] — idempotency, retry, chịu lỗi ở tầng hệ thống
- [[Job Fundamentals 01 - Apache Spark]]
- [[Job Fundamentals 02 - SQL nâng cao]]
- [[20_KE_HOACH_Job_Fundamentals]] — kế hoạch
