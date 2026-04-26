2026-04-26


Tags: [[api]], [[webhook]], [[backend]], [[event-driven]]

# Webhook

> [!info] Webhook là cơ chế một server gửi HTTP POST đến một URL của server khác khi có sự kiện xảy ra. Thay vì client liên tục hỏi "có gì mới không?" (polling), server chủ động gửi dữ liệu ngay khi có sự kiện.

---

## 1. Vấn đề webhook giải quyết

**Polling — cách làm không hiệu quả:**

App cần biết khi nào thanh toán hoàn tất. Nếu dùng polling:

```
App → GET /payments/123/status  → {"status": "pending"}   # lần 1
App → GET /payments/123/status  → {"status": "pending"}   # lần 2
App → GET /payments/123/status  → {"status": "pending"}   # lần 3, ...
App → GET /payments/123/status  → {"status": "completed"} # lần N, cuối cùng có kết quả
```

Vấn đề: Phần lớn request là vô ích. Nếu có 10,000 đơn hàng đang chờ, load lên payment service rất lớn. Độ trễ phát hiện phụ thuộc vào interval polling.

**Webhook — server push:**

```
Payment service → POST /your-server/webhooks/payment  với body {"event": "payment.completed", "payment_id": 123}
```

App nhận ngay khi sự kiện xảy ra. Không có request thừa.

---

## 2. Luồng hoạt động

```
1. Developer đăng ký webhook URL với service bên ngoài
   (VD: vào Stripe dashboard, điền URL: https://yourapp.com/webhooks/stripe)
        │
        ▼
2. Sự kiện xảy ra ở service bên ngoài
   (VD: user thanh toán thành công)
        │
        ▼
3. Service bên ngoài gửi HTTP POST đến URL đã đăng ký
   Header: Content-Type: application/json
   Body: JSON payload mô tả sự kiện
        │
        ▼
4. Server của bạn nhận request, xử lý, trả về 2xx
        │
        ▼
5. Nếu không nhận được 2xx, service bên ngoài retry theo policy của họ
```

---

## 3. Cấu trúc payload

Không có chuẩn chung — mỗi service có format riêng. Ví dụ Stripe:

```json
{
  "id": "evt_1abc...",
  "type": "payment_intent.succeeded",
  "created": 1714123456,
  "data": {
    "object": {
      "id": "pi_1abc...",
      "amount": 150000,
      "currency": "vnd",
      "status": "succeeded",
      "metadata": {
        "order_id": "ORD-42"
      }
    }
  }
}
```

---

## 4. Bảo mật — Signature Verification

> [!warning] Bất kỳ ai biết webhook URL đều có thể gửi POST giả mạo đến endpoint đó. Không verify signature là lỗ hổng bảo mật nghiêm trọng.

**Cơ chế phổ biến — HMAC signature:**

1. Service bên ngoài (VD: Stripe) cung cấp một `webhook_secret` khi bạn đăng ký
2. Khi gửi webhook, họ tính `HMAC-SHA256(payload, webhook_secret)` và đặt vào header
3. Server của bạn tính lại HMAC từ raw payload nhận được, so sánh với giá trị trong header

```python
import hmac
import hashlib

def verify_stripe_webhook(payload_bytes: bytes, sig_header: str, secret: str) -> bool:
    timestamp, signature = parse_stripe_header(sig_header)
    signed_payload = f"{timestamp}.{payload_bytes.decode()}"
    expected = hmac.new(secret.encode(), signed_payload.encode(), hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature)
```

> [!important] Luôn dùng `hmac.compare_digest` thay vì `==` để tránh timing attack.

---

## 5. Idempotency

Service bên ngoài có thể gửi cùng một webhook nhiều lần (network timeout, retry). Server phải xử lý idempotent:

```python
def handle_payment_webhook(event: dict):
    event_id = event["id"]

    # Kiểm tra đã xử lý chưa
    if db.processed_events.exists(event_id):
        return  # Bỏ qua duplicate

    # Xử lý
    process_payment(event["data"])

    # Đánh dấu đã xử lý
    db.processed_events.insert(event_id)
```

---

## 6. Retry và Dead Letter

Khi server trả về non-2xx (hoặc timeout), service bên ngoài sẽ retry. Policy thường theo exponential backoff:

```
Attempt 1: ngay lập tức
Attempt 2: sau 5 phút
Attempt 3: sau 30 phút
Attempt 4: sau 2 giờ
Attempt 5: sau 1 ngày
→ Sau đó mark là failed, gửi alert cho developer
```

Vì vậy endpoint webhook phải:
- Respond nhanh (trong vòng vài giây) — xử lý nặng thì đẩy vào queue
- Luôn trả về 2xx nếu đã nhận được payload (dù chưa xử lý xong)

---

## 7. Ví dụ thực tế

**Stripe payment flow:**

1. User bấm "Thanh toán" trên app → app gọi API tạo `PaymentIntent` trên Stripe
2. Stripe xử lý thanh toán bất đồng bộ (có thể mất vài giây đến vài phút với 3D Secure)
3. Khi hoàn tất, Stripe gửi `POST https://yourapp.com/webhooks/stripe` với event `payment_intent.succeeded`
4. Server verify signature, đọc `metadata.order_id`, update trạng thái đơn hàng trong DB, gửi email xác nhận cho user

**GitHub Actions trigger:**

1. Developer push code lên GitHub
2. GitHub gửi webhook đến CI/CD server (Jenkins, internal service) với payload chứa commit info
3. CI/CD server nhận, trigger pipeline build/test/deploy

---

## 8. Webhook vs Polling vs WebSocket

| | Polling | Webhook | WebSocket |
|---|---|---|---|
| Ai khởi tạo kết nối | Client | Server (gửi HTTP) | Client (upgrade) |
| Kết nối | Stateless, mỗi lần mới | Stateless, mỗi event mới | Persistent |
| Phù hợp | Đơn giản, tần suất thấp | Server-to-server async events | Real-time 2 chiều |
| Cần expose endpoint | Không | Có (server phải có public URL) | Không |
| Browser support | Tốt | N/A (server-side) | Tốt |
