2026-04-30


Tags: [[devops]], [[networking]], [[api-gateway]], [[reverse-proxy]], [[load-balancing]]

# NGINX

> [!info] NGINX (đọc là "engine-x") là một web server mã nguồn mở, hiệu năng cao, được dùng phổ biến làm **reverse proxy**, **load balancer** và **API Gateway**. Kiến trúc event-driven cho phép xử lý hàng chục nghìn connection cùng lúc trên một máy với footprint rất nhẹ.

---

## 1. NGINX dùng để làm gì

NGINX có 3 vai trò chính, thường chạy đồng thời:

- **Web server**: phục vụ static file (HTML, CSS, JS, ảnh)
- **Reverse proxy**: đứng trước backend app server, nhận request rồi forward vào trong
- **API Gateway / Load balancer**: phân phối traffic đến nhiều service backend

Trong kiến trúc microservices hiện đại, NGINX thường đóng vai [[API Gateway]] — đứng ở biên hệ thống, lo trọn các tác vụ chung như SSL, auth, rate limit, logging trước khi route request vào service.

---

## 2. Vì sao NGINX phổ biến

- **Event-driven, non-blocking**: không tạo thread mới cho mỗi request như Apache cũ → xử lý 10K+ connection đồng thời với RAM thấp
- **Cấu hình bằng file text**: dễ đọc, dễ version control với Git
- **Mã nguồn mở, miễn phí**: bản trả phí (NGINX Plus) chỉ thêm tính năng nâng cao
- **Linh hoạt**: chạy được ở mọi tầng — CDN edge, [[Ingress]] controller K8s, reverse proxy nội bộ
- **Ổn định**: production-tested ở quy mô cực lớn (Netflix, Cloudflare, GitHub đều dùng)

---

## 3. Load Balancing

Khi có nhiều backend instance giống nhau, NGINX phân phối request để không server nào bị quá tải.

**Tầng hoạt động:**
- **Layer 7 (application)**: hiểu HTTP, route theo URL path, header, cookie — linh hoạt
- **Layer 4 (transport)**: chỉ nhìn TCP/UDP — nhanh hơn nhưng kém thông minh

**Thuật toán cân bằng tải:**

| Thuật toán | Cách hoạt động | Khi nào dùng |
|---|---|---|
| **Round Robin** | Chia đều lần lượt cho từng server | Default, các backend đồng đều |
| **Least Connections** | Gửi đến server đang ít kết nối nhất | Request có thời gian xử lý khác nhau |
| **Random** | Chọn ngẫu nhiên | Đơn giản, tránh hot spot |
| **IP Hash** | Cùng client IP → cùng server | Cần session affinity (sticky session) |

---

## 4. Traffic Management

- **A/B testing**: chia % traffic cho nhiều phiên bản backend (VD: 90% v1, 10% v2 để test canary)
- **GeoIP**: nhận diện vị trí client theo IP → chặn theo quốc gia hoặc route đến region gần nhất
- **Rate limiting**: giới hạn số request/giây cho mỗi client
- **Connection limiting**: giới hạn số kết nối đồng thời
- **Bandwidth limiting**: giới hạn tốc độ download cho mỗi client
- **Caching**: cache response để giảm tải backend

Tác dụng chính: **chống abuse, chống DDoS, smooth rollout phiên bản mới**.

---

## 5. Authentication & Security

- **SSL/TLS termination**: NGINX giải mã HTTPS tại edge → traffic vào nội bộ là HTTP, backend không phải tự lo SSL
- **HTTPS redirect**: tự động redirect `http://` → `https://`
- **Basic auth, JWT, OAuth**: tích hợp qua module hoặc Lua script (OpenResty)
- **mTLS**: xác thực hai chiều giữa client và server
- **WAF (Web Application Firewall)**: chặn các pattern tấn công phổ biến (qua ModSecurity hoặc NGINX App Protect)

**Lợi ích tập trung SSL ở gateway:** chỉ phải quản lý một bộ certificate, các service backend không cần biết SSL tồn tại.

---

## 6. Monitoring & Observability

NGINX không chỉ proxy — nó còn là điểm quan sát tốt nhất của hệ thống vì mọi traffic đều đi qua.

- **OpenTelemetry**: thu thập telemetry (trace, metric, log) theo chuẩn mở
- **Log handling**: chia log thành nhiều file (`access.log`, `error.log`) và stream về log server tập trung
- **Metrics exporter**: xuất metric ra [[Prometheus]] để dashboard và alert

**Pipeline điển hình:**

```
NGINX → OpenTelemetry → Prometheus → Grafana
                     → Loki / ELK   → Log dashboard
```

---

## 7. Cấu hình mẫu

Một file `nginx.conf` đơn giản cho reverse proxy + load balancing:

```nginx
upstream backend {
    least_conn;
    server backend1.internal:8080;
    server backend2.internal:8080;
    server backend3.internal:8080;
}

server {
    listen 443 ssl;
    server_name api.example.com;

    ssl_certificate     /etc/nginx/cert.pem;
    ssl_certificate_key /etc/nginx/key.pem;

    # Rate limit: 10 req/s mỗi IP
    limit_req zone=api_limit burst=20 nodelay;

    location /api/ {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## 8. Hình dung tổng thể

```
                  ┌──────────────┐
Client (HTTPS) ─► │    NGINX     │
                  │              │
                  │ • SSL term   │
                  │ • Auth       │
                  │ • Rate limit │
                  │ • Logging    │
                  │ • Routing    │
                  └──────┬───────┘
                         │ (HTTP nội bộ)
            ┌────────────┼────────────┐
            ▼            ▼            ▼
        Backend 1    Backend 2    Backend 3
```

NGINX đứng ở **biên** hệ thống, lo các tác vụ chung trước khi forward request vào service nội bộ.

---

## 9. Khi nào KHÔNG nên dùng NGINX

- **Service mesh phức tạp**: cần mTLS giữa hàng trăm service nội bộ → [[Istio]] / Linkerd phù hợp hơn
- **Traffic gRPC streaming nặng**: NGINX hỗ trợ gRPC nhưng Envoy tối ưu hơn
- **Logic gateway phức tạp**: cần nhiều plugin → Kong (built trên NGINX) hoặc Traefik dễ quản lý hơn

---

## 10. Liên hệ

- [[API Gateway]] — NGINX là một trong các giải pháp gateway phổ biến nhất
- [[Ingress]] — NGINX Ingress Controller là implementation phổ biến nhất cho K8s Ingress
- [[Istio]] — service mesh, đối thủ ở tầng nội bộ
- [[REST API]] — phần lớn traffic NGINX proxy là REST/HTTP
