2026-04-26


Tags: [[K8s]], [[devops]], [[networking]], [[ingress]]

# Kubernetes Ingress

> [!info] Ingress là một K8s object định nghĩa các quy tắc định tuyến HTTP/HTTPS từ bên ngoài vào các Service bên trong cluster. Nó hoạt động như một "API Gateway" hay "Reverse Proxy" ở tầng L7.

---

## 1. Vấn đề Ingress giải quyết

Với `LoadBalancer` Service, mỗi Service cần một Cloud Load Balancer riêng → **tốn kém và khó quản lý** khi có nhiều service.

```
Không có Ingress:
Internet → LoadBalancer ($) → Service A (port 80)
Internet → LoadBalancer ($) → Service B (port 80)
Internet → LoadBalancer ($) → Service C (port 80)

Với Ingress:
Internet → LoadBalancer ($) → Ingress Controller → /api    → Service A
                                                  → /web    → Service B
                                                  → /admin  → Service C
```

Một Load Balancer duy nhất, nhiều Service — tiết kiệm chi phí và tập trung quản lý routing.

---

## 2. Hai thành phần: Ingress Resource vs Ingress Controller

Đây là điểm hay nhầm lẫn nhất:

| | Ingress Resource | Ingress Controller |
|---|---|---|
| **Là gì** | K8s object (YAML) khai báo routing rules | Pod/Deployment chạy trong cluster, thực thi rules |
| **Ai tạo** | Bạn (developer/operator) | Admin (cài đặt một lần) |
| **Ví dụ** | `kind: Ingress` trong YAML | NGINX Ingress Controller, Traefik, HAProxy |
| **Tích hợp sẵn K8s** | ✅ | ❌ (phải cài riêng) |

> [!warning] K8s không tự đi kèm Ingress Controller. Nếu không cài Controller, Ingress Resource chỉ là YAML chết — không có gì xử lý nó.

---

## 3. Cấu trúc Ingress Resource

### 3.1. Path-based routing (cùng domain, khác path)

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: my-app-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  ingressClassName: nginx
  rules:
  - host: myapp.example.com
    http:
      paths:
      - path: /api
        pathType: Prefix
        backend:
          service:
            name: api-service
            port:
              number: 8080
      - path: /web
        pathType: Prefix
        backend:
          service:
            name: frontend-service
            port:
              number: 80
```

### 3.2. Host-based routing (khác domain/subdomain)

```yaml
spec:
  rules:
  - host: api.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: api-service
            port:
              number: 8080
  - host: admin.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: admin-service
            port:
              number: 3000
```

### 3.3. TLS/HTTPS

```yaml
spec:
  tls:
  - hosts:
    - myapp.example.com
    secretName: myapp-tls-secret  # Secret chứa cert + private key
  rules:
  - host: myapp.example.com
    ...
```

Kết hợp với **cert-manager** để tự động issue và renew TLS cert từ Let's Encrypt.

---

## 4. pathType: Exact vs Prefix vs ImplementationSpecific

| pathType | Ý nghĩa |
|---|---|
| `Exact` | Khớp chính xác `/foo` — không match `/foo/bar` |
| `Prefix` | Match `/foo` và mọi thứ bắt đầu bằng `/foo/` |
| `ImplementationSpecific` | Tuỳ Controller (NGINX dùng regex, ...) |

---

## 5. Các Ingress Controller phổ biến

| Controller | Đặc điểm | Khi nào chọn |
|---|---|---|
| **NGINX Ingress** | Phổ biến nhất, stable, nhiều annotation | Mặc định cho hầu hết production |
| **Traefik** | Auto-discover service, dashboard đẹp, hỗ trợ tốt middleware | Microservices, cần dashboard |
| **AWS ALB Controller** | Tích hợp native với AWS ALB | Chạy trên EKS, cần WAF/Shield |
| **Istio Gateway** | Part of service mesh, L7 traffic management | Cần mTLS, circuit breaking, observability |

---

## 6. Annotations phổ biến với NGINX Ingress

```yaml
metadata:
  annotations:
    # Rewrite path trước khi forward đến backend
    nginx.ingress.kubernetes.io/rewrite-target: /$2

    # Rate limiting
    nginx.ingress.kubernetes.io/limit-rps: "10"

    # CORS
    nginx.ingress.kubernetes.io/enable-cors: "true"

    # Upload size limit
    nginx.ingress.kubernetes.io/proxy-body-size: "50m"

    # Sticky session (cho stateful apps)
    nginx.ingress.kubernetes.io/affinity: "cookie"

    # Redirect HTTP → HTTPS
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
```

---

## 7. Ingress vs API Gateway vs Service Mesh

| | Ingress | API Gateway (Kong, AWS API GW) | Service Mesh (Istio) |
|---|---|---|---|
| **Tầng** | L7 (HTTP/HTTPS) | L7 | L4/L7 |
| **Traffic** | North-South (external → cluster) | North-South | East-West (service ↔ service) |
| **Auth/AuthZ** | Cơ bản (annotation) | Đầy đủ (OAuth, JWT, API Key) | mTLS giữa services |
| **Observability** | Hạn chế | Có | Đầy đủ (trace, metric) |
| **Độ phức tạp** | Thấp | Trung bình | Cao |

> [!tip] Production thực tế: **Ingress** cho routing cơ bản + TLS termination. Nếu cần auth, rate limiting nâng cao → thêm **API Gateway**. Nếu cần observability nội bộ + zero-trust → **Service Mesh**.

# References
