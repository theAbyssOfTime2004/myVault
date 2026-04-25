2026-04-26


Tags: [[K8s]], [[devops]], [[configuration]]

# K8s ConfigMap và Secret

> [!info] Nguyên tắc: tách cấu hình ra khỏi container image. Image chứa code — ConfigMap/Secret chứa config. Cùng image, khác config = deploy lên nhiều môi trường.

---

## 1. ConfigMap — Cấu hình không nhạy cảm

Lưu trữ dữ liệu dạng key-value hoặc toàn bộ file config (không mã hóa).

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  APP_ENV: "production"
  LOG_LEVEL: "info"
  config.yaml: |
    server:
      port: 8080
      timeout: 30s
```

### Cách inject vào Pod

**Cách 1 — Biến môi trường:**
```yaml
spec:
  containers:
  - name: app
    envFrom:
    - configMapRef:
        name: app-config
    # hoặc chọn từng key
    env:
    - name: LOG_LEVEL
      valueFrom:
        configMapKeyRef:
          name: app-config
          key: LOG_LEVEL
```

**Cách 2 — Mount như file:**
```yaml
    volumeMounts:
    - name: config-vol
      mountPath: /etc/config
  volumes:
  - name: config-vol
    configMap:
      name: app-config
# → file /etc/config/config.yaml sẽ có nội dung từ ConfigMap
```

---

## 2. Secret — Dữ liệu nhạy cảm

Giống ConfigMap nhưng dữ liệu được encode **base64** và K8s có cơ chế hạn chế access (RBAC, encryption at rest).

> [!warning] Base64 **không phải** mã hóa. Secret mặc định chỉ khó đọc hơn, không an toàn hơn về bản chất. Để bảo mật thực sự: bật **Encryption at Rest** hoặc dùng external secret manager (Vault, AWS Secrets Manager).

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: db-secret
type: Opaque
data:
  DB_PASSWORD: cGFzc3dvcmQxMjM=   # base64("password123")
  API_KEY: c2VjcmV0a2V5          # base64("secretkey")
```

Tạo nhanh bằng kubectl (tự encode base64):
```bash
kubectl create secret generic db-secret \
  --from-literal=DB_PASSWORD=password123 \
  --from-literal=API_KEY=secretkey
```

Inject vào Pod (giống ConfigMap, dùng `secretRef` / `secretKeyRef`):
```yaml
    envFrom:
    - secretRef:
        name: db-secret
```

---

## 3. So sánh & Khi nào dùng gì

| | ConfigMap | Secret |
|---|---|---|
| **Dữ liệu** | Plain text | Base64 encoded |
| **Encryption at rest** | ❌ | ✅ (nếu bật) |
| **RBAC riêng** | ❌ | ✅ |
| **Hiện trong logs** | Có thể | K8s cố gắng che |
| **Dùng cho** | App config, feature flags, env vars không nhạy cảm | Password, API key, token, TLS cert, SSH key |

---

## 4. Hạn chế cần biết

- **Size limit:** Cả hai giới hạn **1MB** per object.
- **Không tự reload:** Khi update ConfigMap/Secret, Pod đang chạy **không tự nhận giá trị mới** nếu inject qua env vars — phải restart Pod. Nếu mount như file thì K8s sẽ tự cập nhật file sau vài phút (eventual consistency).
- **Secret không đủ cho production nghiêm túc** — cần tích hợp với **External Secrets Operator** + Vault/AWS SSM để sync secret từ bên ngoài vào K8s tự động.

# References
