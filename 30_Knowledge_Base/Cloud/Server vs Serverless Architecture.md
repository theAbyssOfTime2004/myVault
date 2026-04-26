2026-04-26


Tags: [[cloud]], [[devops]], [[serverless]], [[architecture]]

# Server vs Serverless Architecture

---

## 1. Traditional Server Architecture

Bạn **thuê/mua máy chủ**, cài OS, runtime, deploy app lên đó — máy chạy **24/7** dù có request hay không.

```
User → Load Balancer → [Server 1: App luôn chạy]
                     → [Server 2: App luôn chạy]
                     → [Server 3: App luôn chạy]
```

**Bạn phải tự lo:**
- Provisioning máy chủ
- Cài đặt, vá lỗi OS
- Scale khi traffic tăng
- Trả tiền 24/7 kể cả lúc idle

---

## 2. Serverless Architecture

**Không có nghĩa là không có server** — vẫn có server, nhưng bạn không quan tâm đến nó. Bạn chỉ upload **function** (đoạn code), cloud provider lo toàn bộ hạ tầng.

```
User → Cloud Provider → [Spin up function] → Xử lý → Tắt
                      → [Spin up function] → Xử lý → Tắt
                      → [Spin up function] → Xử lý → Tắt
```

Mỗi request = một lần chạy function = trả tiền cho đúng thời gian đó.

**Các dịch vụ phổ biến:** AWS Lambda, Google Cloud Functions, Azure Functions.

---

## 3. So sánh trực tiếp

| | Server (Traditional) | Serverless |
|---|---|---|
| **Đơn vị deploy** | App/Service liên tục chạy | Function chạy theo sự kiện |
| **Scaling** | Manual hoặc cấu hình auto-scale | Tự động, đến hàng nghìn instance |
| **Chi phí** | Trả theo giờ/tháng (24/7) | Trả theo số lần gọi + thời gian chạy |
| **Cold start** | Không có | Có (lần đầu chạy chậm hơn ~100-500ms) |
| **Giới hạn thời gian** | Không giới hạn | Có (AWS Lambda max 15 phút) |
| **State** | Có thể giữ state trong memory | Stateless hoàn toàn |
| **Kiểm soát OS/runtime** | Toàn quyền | Không có |
| **Debug/Observe** | Dễ | Khó hơn (distributed, ephemeral) |

---

## 4. Khi nào chọn gì

**Dùng Server (hoặc K8s) khi:**
- App chạy liên tục, có long-running process (training ML model, WebSocket, streaming)
- Cần kiểm soát runtime, cài thư viện nặng (CUDA, custom binary)
- Latency nhạy cảm — không chấp nhận cold start
- Workload đều đặn — trả tiền 24/7 vẫn rẻ hơn

**Dùng Serverless khi:**
- Workload **không đều** — có lúc 0 request, có lúc đột biến
- Các task ngắn, event-driven (xử lý file upload, gửi email, webhook)
- Muốn **zero ops** — không muốn quản lý server
- Prototype nhanh

---

## 5. Thực tế: thường dùng kết hợp

```
User
 │
 ├── API chính (K8s / Server) ← latency nhạy cảm, chạy liên tục
 │
 ├── Xử lý ảnh upload (Lambda) ← event-driven, spike traffic
 │
 └── Gửi email hàng đêm (Lambda + Cron) ← chạy 1 lần/ngày
```

Không phải "either/or" — chọn đúng tool cho đúng bài toán.

# References
