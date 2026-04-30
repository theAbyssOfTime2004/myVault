2026-04-30


Tags: [[api]], [[microservices]], [[backend]], [[networking]], [[infrastructure]]

# API Gateway

> [!info] API Gateway là một **cổng vào duy nhất** (single entry point) đứng giữa client và hệ thống microservices. Mọi request từ client đều đi qua gateway, sau đó được định tuyến đến đúng service xử lý. Client không cần biết bên trong có bao nhiêu service hay chúng nằm ở đâu.

---

## 1. Tại sao cần API Gateway

Trong kiến trúc microservices, hệ thống bị chia nhỏ thành hàng chục service. Nếu client gọi trực tiếp từng service:

- Client phải biết địa chỉ của tất cả service → coupling chặt
- Mỗi service phải tự xử lý auth, rate limit, SSL → trùng lặp logic
- Mỗi service public ra internet → diện tấn công lớn
- Đổi vị trí hay tách service → client phải sửa code

API Gateway giải quyết bằng cách trở thành **lớp trung gian duy nhất**: client chỉ nói chuyện với gateway, gateway lo phần còn lại.

**Hình dung:** Gateway giống như **lễ tân của một tòa nhà văn phòng**. Khách không cần biết công ty nào ở tầng nào — chỉ cần đến quầy lễ tân, lễ tân sẽ hướng dẫn hoặc gọi giúp người cần gặp.

---

## 2. Cách hoạt động

```
Client  ─►  API Gateway  ─►  Service A (REST)
                        ─►  Service B (REST)
                        ─►  Service C (REST) ─► Database
```

1. Client gửi request đến địa chỉ duy nhất của gateway
2. Gateway xác thực, kiểm tra rate limit, đọc URL
3. Gateway forward (proxy) request đến service phù hợp
4. Service xử lý xong → trả response qua gateway → về client

Backend service có thể đổi địa chỉ, đổi công nghệ, tách thành nhiều instance — client không bị ảnh hưởng vì gateway che hết.

---

## 3. Các tính năng chính

| Tính năng | Mô tả |
|---|---|
| **Authentication** | Verify token (JWT, API key, OAuth) tập trung tại gateway |
| **IP allowlist/blocklist** | Chặn hoặc cho phép theo IP |
| **Rate limiting** | Giới hạn số request mỗi client để chống abuse |
| **Logging & monitoring** | Ghi lại mọi request — một chỗ duy nhất để quan sát traffic |
| **Traffic routing** | Định tuyến request đến service đúng dựa trên URL path |
| **SSL termination** | Giải mã HTTPS tại gateway, traffic nội bộ có thể là HTTP |
| **Service discovery** | Giấu vị trí thật của service instance |
| **Request aggregation** | Gọi song song nhiều service rồi gộp kết quả trả cho client |

**Ví dụ aggregation:** Client cần load dashboard với data từ `user-service`, `order-service`, `notification-service`. Thay vì client gọi 3 lần, gateway gọi song song 3 service nội bộ rồi gộp thành một response duy nhất.

---

## 4. Lợi ích chính

- **Reverse proxy**: ẩn cấu trúc nội bộ, client không thấy được có bao nhiêu service
- **Cross-cutting concerns tập trung**: auth, logging, rate limit chỉ làm một chỗ thay vì lặp ở mỗi service
- **Giảm bề mặt tấn công**: chỉ một endpoint public ra internet
- **Decoupling**: backend đổi cấu trúc không ảnh hưởng client
- **Performance**: caching, request aggregation, compression đều có thể làm tại gateway

---

## 5. Các giải pháp phổ biến

**Reverse proxy server** (nhẹ, tự build logic):
- **NGINX** — phổ biến nhất, hiệu năng cao, cấu hình bằng file
- **HAProxy** — chuyên load balancing, rất ổn định
- **Traefik** — auto-discovery với Docker/Kubernetes
- **Kong** — built trên NGINX, có plugin ecosystem cho auth/rate limit

**Service mesh ingress controller** (cho Kubernetes):
- **Istio** — service mesh đầy đủ, có ingress gateway
- **Ambassador** — Kubernetes-native, dựa trên Envoy
- **Linkerd** — service mesh nhẹ, ưu tiên đơn giản

**Managed cloud:**
- AWS API Gateway, Google Cloud API Gateway, Azure API Management

---

## 6. Hạn chế cần lưu ý

- **Single point of failure**: gateway chết là cả hệ thống chết → cần chạy nhiều instance, có load balancer phía trước
- **Latency**: thêm một hop trong đường đi của request
- **Bottleneck**: mọi traffic đi qua gateway → cần scale tốt
- **Phức tạp khi cấu hình**: routing rule, plugin, retry policy có thể trở nên rối

---

## 7. Khi nào KHÔNG cần API Gateway

- Hệ thống monolith — chỉ có một backend, không cần định tuyến
- Hệ thống nhỏ với 2–3 service và client nội bộ — overhead không đáng
- Internal service-to-service communication — service mesh phù hợp hơn

---

## 8. Liên hệ

- [[REST API]] — phần lớn traffic qua gateway là REST
- [[gRPC]] — gateway có thể proxy gRPC hoặc làm gRPC-to-REST translation
- [[WebSocket]] — một số gateway hỗ trợ WebSocket passthrough
