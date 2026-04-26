2026-04-26


Tags: [[mlops]], [[model-serving]], [[deployment]], [[infrastructure]], [[knative]]

# Model Serving Patterns

---

## 1. Hai pattern deploy ML model

### Model-as-a-Service

Model được deploy thành một service độc lập, expose inference API. Backend application gọi vào API đó để lấy prediction — backend không load model trực tiếp và không phụ thuộc vào ML framework.

```
UI → Backend App Service → (HTTP/gRPC) → Serving Model Service → prediction
```

**Lợi ích:**

- **Decouple backend và model**: Backend không cần biết model được viết bằng PyTorch hay TensorFlow. Có thể swap model hoặc upgrade version mà không cần redeploy toàn bộ hệ thống.
- **A/B testing dễ hơn**: Route một phần traffic sang model version mới mà không ảnh hưởng backend.
- **Scale độc lập**: Model server (thường cần GPU) được scale riêng biệt với backend server (CPU). GPU/TPU được tập trung thay vì mỗi instance backend phải load model riêng.
- **Tái sử dụng**: Nhiều backend service khác nhau có thể gọi cùng một serving model service.

**Nhược điểm:**

- Thêm network hop → latency cao hơn
- Hệ thống phức tạp hơn: cần quản lý thêm một service, monitoring, versioning

---

### Model-as-a-Dependency

Model được package cùng với application, chạy trong cùng process hoặc container. Backend load model trực tiếp vào memory và gọi inference locally.

```
UI → Backend App + Serving Model → prediction
```

**Lợi ích:**

- Không có network hop → latency thấp hơn
- Đơn giản hơn về infrastructure: chỉ có một service để deploy và quản lý

**Nhược điểm:**

- Backend phụ thuộc vào ML framework (PyTorch, TensorFlow, ...) — build image nặng hơn
- Upgrade model đồng nghĩa phải redeploy toàn bộ application
- Không tái sử dụng được model cho nhiều service
- GPU phải gắn với từng instance backend — kém hiệu quả nếu có nhiều instance

---

## 2. Khi nào dùng cái nào

| Tiêu chí | Model-as-a-Service | Model-as-a-Dependency |
|---|---|---|
| Latency yêu cầu | Không cực thấp | Cực thấp (sub-millisecond) |
| Nhiều service cần cùng model | Có | Không |
| Cần A/B testing model | Có | Không |
| Team ML và backend tách biệt | Có | Không |
| Quy mô | Lớn | Nhỏ hoặc edge |

---

## 3. Ví dụ kiến trúc kết hợp

Diagram dưới mô tả một hệ thống production dùng cả hai pattern đồng thời, tích hợp thêm pipeline phát hiện drift:

```
                     ┌─────────────────────────────┐
                     │  backend app service         │
User → UI ──────────►│         ↓                   │──── prediction
                     │  serving model service       │
                     └─────────────────────────────┘
                              │
                              │ Knative Eventing
                              ▼
User → UI ──────────► backend app + serving model ──── prediction
                              │
                              │ emit event
                              ▼
                           Broker
                              │
                           Trigger
                              │
                              ▼
                    Drift Prediction Service
                              │
                           Webhook
                              │
                              ▼
                         Chat Channel
                      (Slack, Teams, ...)
```

**Luồng hoạt động:**

1. Cả hai pattern (model-as-service ở trên và model-as-dependency ở dưới) đều emit inference event vào **Knative Eventing broker** sau mỗi prediction.
2. Broker route event đến **Trigger**, Trigger forward đến **Drift Prediction Service**.
3. Drift Prediction Service phân tích phân phối input/output theo thời gian để phát hiện data drift.
4. Khi phát hiện drift vượt threshold, service gửi **webhook** đến chat channel để alert team.

**Knative Eventing** ở đây đóng vai trò event bus: decouples producer (serving services) khỏi consumer (drift detection). Thêm consumer mới (VD: logging service, retraining trigger) không cần sửa code serving service.

---

## 4. Liên quan

- [[KServe và CRD]] — framework deploy model-as-a-service trên Kubernetes
- [[Webhook]] — cơ chế alert từ drift detection service đến chat channel
- [[k8s Autoscaling - HPA và KEDA]] — scale serving service theo request load
