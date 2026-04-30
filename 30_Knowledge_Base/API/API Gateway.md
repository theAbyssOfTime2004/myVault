2026-04-30


Tags: [[api]], [[microservices]], [[backend]], [[networking]]

# API Gateway

> [!info] API Gateway là **một anh gác cổng** đứng trước tất cả service trong hệ thống. Mọi request từ ngoài đều phải qua nó, sau đó nó phân phối vào đúng service xử lý. Client chỉ cần biết một địa chỉ duy nhất.

---

## 1. Vấn đề: khi hệ thống có nhiều service

Giả sử bạn deploy nhiều model AI thành các service riêng:

- Service A: model phân loại ảnh (port 8000)
- Service B: model OCR (port 8001)
- Service C: lưu lịch sử user (port 8002)
- Service D: tính tiền user (port 8003)

Đây gọi là **microservices** — chia hệ thống thành nhiều dịch vụ nhỏ thay vì một app to.

**Nếu không có gateway, app mobile phải tự gọi từng service:**

```
App mobile → server.com:8000/predict   (cho ảnh)
App mobile → server.com:8001/ocr       (cho OCR)
App mobile → server.com:8002/history   (cho lịch sử)
App mobile → server.com:8003/billing   (cho tiền)
```

Vấn đề:
- App phải nhớ 4 địa chỉ, 4 port khác nhau
- Mỗi service phải tự lo auth, HTTPS, chặn spam, ghi log → copy-paste code khắp nơi
- Đổi port hay tách service → app phải sửa code

---

## 2. Giải pháp: thêm một anh gác cổng

```
                    ┌─────────────┐
App mobile ────────►│ API Gateway │────► Service A (ảnh)
                    │             │────► Service B (OCR)
                    │             │────► Service C (history)
                    │             │────► Service D (billing)
                    └─────────────┘
```

App chỉ cần biết **một địa chỉ duy nhất**: `api.example.com`.

Gateway nhìn URL rồi đẩy vào đúng service:
- `api.example.com/predict` → Service A
- `api.example.com/ocr` → Service B
- `api.example.com/history` → Service C

---

## 3. Liên hệ với data/AI

Giống như **Hugging Face Inference API** hay **OpenAI API**.

Bạn gọi `api.openai.com/v1/chat/completions` — bạn không biết bên trong họ chạy bao nhiêu GPU, model nằm ở server nào, có bao nhiêu instance. Họ có **một cổng vào duy nhất** thay mặt cho cả rừng service bên trong.

Đó chính là API Gateway.

---

## 4. Gateway làm hộ những việc gì

Vì mọi request đều đi qua nó, gateway là chỗ tốt nhất để làm các việc chung:

| Việc | Giải thích |
|---|---|
| **Auth** | Kiểm tra token một lần ở cổng → service bên trong khỏi lo |
| **Rate limit** | "User free chỉ được gọi 100 lần/ngày" → chặn ngay tại cổng |
| **HTTPS** | Gateway lo mã hóa, service nội bộ dùng HTTP thường cho nhanh |
| **Logging** | Ghi tất cả request vào một chỗ duy nhất |
| **Load balancing** | Service A có 3 bản sao chạy cùng lúc → gateway chia đều request |
| **Routing** | Nhìn URL để biết đẩy vào service nào |

**Lợi ích lớn nhất:** mỗi service backend chỉ cần lo logic của nó. Mọi việc "ngoại vi" (auth, log, SSL) gateway lo hết.

---

## 5. Các phần mềm gateway phổ biến

API Gateway là **khái niệm**, không phải sản phẩm cụ thể. Có nhiều phần mềm đóng vai trò này:

- **NGINX** — phổ biến nhất, nhẹ, nhanh (xem [[NGINX]])
- **Kong** — built trên NGINX, có thêm plugin
- **Traefik** — tự động phát hiện service trong Docker/K8s
- **HAProxy** — chuyên load balancing
- **AWS API Gateway** — managed service trên AWS

> Quan hệ: "API Gateway" với "NGINX" giống như "model phân loại ảnh" với "ResNet50". Một là khái niệm, một là implementation cụ thể.

---

## 6. Khi nào bạn (data/AI) sẽ đụng tới

- **Deploy model lên production**: phía trước FastAPI/Triton luôn có gateway để lo HTTPS, rate limit, load balancing giữa nhiều GPU instance
- **Build internal AI platform**: nhiều team dùng chung → gateway route request và tính usage
- **Dùng Kubernetes deploy ML pipeline**: "Ingress Controller" trong K8s bản chất là một gateway (xem [[Ingress]])

---

## 7. Tóm gọn 3 dòng

- Hệ thống có nhiều service → cần một anh gác cổng đứng trước
- Anh gác cổng = API Gateway, lo auth + rate limit + HTTPS + log + routing
- Giống cách OpenAI/Hugging Face cho bạn gọi một địa chỉ duy nhất, đằng sau là cả rừng service

---

## 8. Liên hệ

- [[NGINX]] — phần mềm gateway phổ biến nhất
- [[REST API]] — phần lớn traffic qua gateway là REST
- [[Ingress]] — gateway trong thế giới Kubernetes
