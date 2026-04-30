2026-04-30


Tags: [[devops]], [[networking]], [[api-gateway]], [[reverse-proxy]]

# NGINX

> [!info] NGINX (đọc là "engine-x") là **một phần mềm** đóng vai [[API Gateway]]. Nó nhận hết request từ ngoài internet, rồi đẩy vào đúng service bên trong. Là giải pháp gateway phổ biến nhất hiện nay — kiểu như PyTorch trong thế giới deep learning.

---

## 1. NGINX là cái gì

**Đơn giản nhất:** NGINX là một phần mềm chạy trên server, đứng giữa user và app của bạn.

```
User (internet) ──► NGINX ──► App của bạn (FastAPI, Flask, Node...)
```

**Quan hệ với "API Gateway":**
- "API Gateway" = khái niệm, vai trò
- "NGINX" = một sản phẩm cụ thể đóng vai trò đó

> Giống như "model phân loại ảnh" (khái niệm) vs "ResNet50" (sản phẩm cụ thể).

Có nhiều phần mềm khác cũng làm gateway: Kong, Traefik, HAProxy. Nhưng NGINX phổ biến nhất.

---

## 2. NGINX làm được những gì

### Vai trò 1 — Web server (phục vụ file tĩnh)

User gõ `example.com` → NGINX trả về file `index.html`, `style.css`, ảnh. Vai trò gốc của NGINX, đơn giản nhất.

### Vai trò 2 — Reverse proxy (đẩy request vào app)

User gõ `example.com/api/predict` → NGINX đẩy request vào FastAPI đang chạy ở `localhost:8000`.

> "Reverse proxy" = một thằng đứng trước app, nhận request thay app rồi đẩy vào trong.

### Vai trò 3 — API Gateway / Load Balancer

User gọi → NGINX phân phối request đến nhiều instance giống nhau để không server nào quá tải:

```
                ┌─► FastAPI instance 1 (GPU 1)
User ─► NGINX ──┼─► FastAPI instance 2 (GPU 2)
                └─► FastAPI instance 3 (GPU 3)
```

Đây là cách deploy model AI điển hình ở production.

---

## 3. NGINX dùng như thế nào

Bạn **không code NGINX bằng Python**. Bạn viết một **file config** rồi chạy NGINX với file đó.

Ví dụ file config đơn giản:

```nginx
# Khi có request đến /predict → đẩy về FastAPI ở port 8000
location /predict {
    proxy_pass http://localhost:8000;
}

# Khi có request đến /ocr → đẩy về FastAPI khác ở port 8001
location /ocr {
    proxy_pass http://localhost:8001;
}
```

Chạy `nginx -c config.conf` → xong, bạn vừa có một API Gateway.

---

## 4. 4 nhóm tính năng chính (theo slides)

### a. Load Balancing — chia tải

Khi có nhiều bản sao của cùng một service, NGINX chia request đều cho các bản sao. Các thuật toán:

- **Round Robin** — chia lần lượt, đều như chia bài
- **Least Connections** — gửi cho server đang ít kết nối nhất
- **Random** — chọn ngẫu nhiên
- **IP Hash** — cùng một user IP luôn vào cùng server (giữ session)

**Liên hệ data/AI:** Giả sử bạn có 4 GPU mỗi GPU chạy 1 instance model. NGINX chia request inference đều cho 4 GPU.

### b. Traffic Management — quản lý lưu lượng

- **A/B testing**: chia 90% traffic sang model v1, 10% sang model v2 để test
- **GeoIP**: chặn theo quốc gia, hoặc route user Việt Nam sang server Singapore
- **Rate limiting**: "user free chỉ được gọi 100 lần/ngày"

### c. Authentication & Security

- **SSL/TLS**: NGINX lo mã hóa HTTPS — backend của bạn không phải tự cài SSL
- **HTTPS redirect**: user gõ `http://...` tự động chuyển sang `https://...`

### d. Monitoring — giám sát

Vì mọi request đi qua NGINX, đây là chỗ tốt nhất để thu thập số liệu:

- **OpenTelemetry**: gửi trace/metric ra hệ thống quan sát
- **Logging**: ghi mọi request vào file
- **Prometheus exporter**: xuất metric (số request/giây, latency...) cho Prometheus → Grafana vẽ biểu đồ

---

## 5. Tại sao NGINX phổ biến đến vậy

- **Nhẹ, nhanh**: xử lý hàng chục nghìn user cùng lúc trên một máy — RAM thấp
- **Cấu hình đơn giản**: một file text, có thể commit Git
- **Miễn phí, mã nguồn mở**
- **Production-tested**: Netflix, Cloudflare, GitHub đều dùng

---

## 6. Khi nào bạn (data/AI) sẽ đụng tới NGINX

| Tình huống | NGINX làm gì |
|---|---|
| Deploy FastAPI model lên server | Đứng trước FastAPI, lo HTTPS + rate limit |
| Có nhiều GPU instance chạy cùng model | Chia request đều cho các GPU |
| Deploy ML trên Kubernetes | "NGINX Ingress Controller" — bản chất là NGINX (xem [[Ingress]]) |
| Build platform cho team data nội bộ | Gateway để route request, log usage |

---

## 7. Tóm gọn 3 dòng

- NGINX = phần mềm đóng vai API Gateway, đứng trước app của bạn
- Bạn không code NGINX, bạn viết file config kiểu "URL này đẩy vào port kia"
- Production deploy AI gần như chắc chắn có NGINX ở phía trước

---

## 8. Liên hệ

- [[API Gateway]] — khái niệm, NGINX là một implementation
- [[Ingress]] — NGINX trong thế giới Kubernetes
- [[REST API]] — phần lớn traffic NGINX proxy là REST/HTTP
