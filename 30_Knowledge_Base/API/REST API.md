2026-04-26


Tags: [[api]], [[http]], [[backend]], [[networking]]

# REST API

> [!info] REST (Representational State Transfer) là một kiến trúc thiết kế API chạy trên HTTP. Client gửi request đến một URL cụ thể, server xử lý và trả về response. Mỗi request là độc lập — server không giữ state giữa các lần gọi.

---

## 1. Nguyên tắc cốt lõi

REST không phải một chuẩn cứng, mà là một tập ràng buộc kiến trúc (architectural constraints):

- **Stateless**: Mỗi request phải chứa đủ thông tin để server xử lý. Server không lưu session giữa các request.
- **Uniform Interface**: Tài nguyên được định danh bằng URL. Thao tác trên tài nguyên thông qua HTTP method chuẩn.
- **Client-Server**: Client và server tách biệt hoàn toàn. Client không biết server lưu dữ liệu thế nào; server không biết client hiển thị thế nào.
- **Cacheable**: Response phải có thông tin cho client biết có cache được không (thông qua header `Cache-Control`).

---

## 2. HTTP Methods

| Method | Mục đích | Idempotent | Body |
|---|---|---|---|
| `GET` | Lấy tài nguyên | Có | Không |
| `POST` | Tạo tài nguyên mới | Không | Có |
| `PUT` | Thay thế toàn bộ tài nguyên | Có | Có |
| `PATCH` | Cập nhật một phần tài nguyên | Không bắt buộc | Có |
| `DELETE` | Xóa tài nguyên | Có | Không |

**Idempotent** có nghĩa là gọi nhiều lần cho kết quả giống nhau. `PUT /users/1` với cùng payload dù gọi 1 lần hay 10 lần thì trạng thái server vẫn như nhau. `POST /users` mỗi lần gọi tạo ra một bản ghi mới.

---

## 3. Cấu trúc URL

URL đại diện cho tài nguyên, không phải hành động:

```
# Đúng — noun
GET  /orders/42
POST /orders
GET  /orders/42/items

# Sai — verb trong URL
POST /createOrder
GET  /getOrderById?id=42
```

Quy tắc phổ biến:
- Collection: `/resources` (số nhiều)
- Single item: `/resources/{id}`
- Nested resource: `/resources/{id}/sub-resources`
- Query params cho filter/sort/page: `/orders?status=pending&page=2`

---

## 4. HTTP Status Codes

| Range | Ý nghĩa |
|---|---|
| 2xx | Thành công |
| 3xx | Redirect |
| 4xx | Lỗi từ phía client |
| 5xx | Lỗi từ phía server |

Các code thường gặp:

| Code | Tên | Khi nào dùng |
|---|---|---|
| 200 | OK | Request thành công, có response body |
| 201 | Created | Tạo tài nguyên thành công (thường dùng với POST) |
| 204 | No Content | Thành công nhưng không có body (thường dùng với DELETE) |
| 400 | Bad Request | Request sai format, thiếu field bắt buộc |
| 401 | Unauthorized | Chưa xác thực (thiếu hoặc sai token) |
| 403 | Forbidden | Đã xác thực nhưng không có quyền |
| 404 | Not Found | Tài nguyên không tồn tại |
| 409 | Conflict | Xung đột trạng thái (VD: tạo user với email đã tồn tại) |
| 422 | Unprocessable Entity | Dữ liệu đúng format nhưng fail validation |
| 429 | Too Many Requests | Rate limit |
| 500 | Internal Server Error | Lỗi không xác định ở server |

---

## 5. Headers quan trọng

**Request headers:**
```
Authorization: Bearer <token>
Content-Type: application/json
Accept: application/json
X-Request-ID: abc-123          # Trace ID để debug
```

**Response headers:**
```
Content-Type: application/json
Cache-Control: max-age=3600
X-RateLimit-Remaining: 42
```

---

## 6. Authentication

**Bearer Token (JWT)**
- Client gửi `Authorization: Bearer <jwt>` trong mỗi request
- Server verify signature của JWT, không cần query DB
- JWT chứa claims (userId, role, exp) — stateless hoàn toàn

**API Key**
- Thường dùng cho server-to-server
- Gửi qua header `X-API-Key: <key>` hoặc query param `?api_key=<key>`

**OAuth 2.0**
- Dùng khi client cần truy cập tài nguyên thay mặt user (third-party access)
- Flow phổ biến: Authorization Code (cho web app), Client Credentials (cho server-to-server)

---

## 7. Ví dụ thực tế

**Luồng user đặt hàng trên e-commerce:**

1. App mobile gửi `POST /orders` với body chứa danh sách sản phẩm và địa chỉ giao hàng
2. Order service validate payload, tạo bản ghi trong DB, trả về `201 Created` với body chứa `orderId`
3. App hiển thị màn hình xác nhận, sau đó gọi `GET /orders/{orderId}` để poll trạng thái
4. Khi user muốn hủy: `PATCH /orders/{orderId}` với body `{"status": "cancelled"}`

**Tại sao REST phù hợp ở đây:** Các thao tác CRUD rõ ràng, client là mobile app cần gọi từng request riêng lẻ, không cần real-time.

---

## 8. Hạn chế của REST

- **Over-fetching**: `GET /users/1` trả về toàn bộ thông tin user dù client chỉ cần `name`. → GraphQL giải quyết bằng cách cho client chỉ định field cần lấy.
- **Under-fetching**: Để hiển thị một trang cần gọi nhiều endpoint: `GET /users/1`, `GET /users/1/orders`, `GET /products/...`. → GraphQL hoặc thiết kế endpoint composite giải quyết.
- **Không phù hợp real-time**: Poll liên tục `GET /messages` rất kém hiệu quả. → WebSocket hoặc SSE phù hợp hơn.
- **Không phù hợp high-performance internal services**: JSON serialization tốn CPU, text-based không compact. → gRPC phù hợp hơn.
