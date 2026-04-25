2026-04-26


Tags: [[kubernetes]], [[devops]], [[autoscaling]], [[KEDA]], [[HPA]]

# K8s Autoscaling — HPA và KEDA

---

## 1. Vấn đề Scale: "to zero" vs "from 1"

Khi nói đến autoscaling trong K8s, có hai chiến lược cơ bản:

| Chiến lược | Ý nghĩa | Trade-off |
|---|---|---|
| **Scale to zero** | Khi không có traffic, giảm replica về 0 | Tiết kiệm hoàn toàn chi phí, nhưng gặp **cold start latency** khi request đầu tiên đến |
| **Scale from 1** | Luôn giữ tối thiểu 1 replica chạy | Không có cold start, nhưng tốn chi phí kể cả khi idle |

> [!tip] Chọn gì?
> - Workload **không đòi hỏi latency thấp** (batch job, background worker): scale to zero.  
> - Workload **phục vụ user trực tiếp** (inference endpoint, API): giữ từ 1 replica trở lên, dùng KEDA + CronScaler để warm up trước giờ cao điểm.

---

## 2. HPA (Horizontal Pod Autoscaler)

**HPA** là cơ chế autoscaling tích hợp sẵn trong K8s, hoạt động theo vòng lặp điều khiển (control loop) mặc định mỗi 15 giây.

### 2.1. Ba tầng metrics mà HPA hỗ trợ

```
┌────────────────────────────────────────────────┐
│  Tầng 1: Resource Metrics (metrics-server)     │
│          CPU, Memory của Pod                    │
├────────────────────────────────────────────────┤
│  Tầng 2: Custom Metrics (custom.metrics API)   │
│          Prometheus Adapter → expose metric     │
│          vào K8s API                            │
├────────────────────────────────────────────────┤
│  Tầng 3: External Metrics (external.metrics)   │
│          Metric từ ngoài cluster                │
│          (SQS queue depth, Datadog, ...)        │
└────────────────────────────────────────────────┘
```

### 2.2. Giới hạn của HPA

- **Không scale về 0:** `minReplicas` nhỏ nhất là 1.
- **Custom metrics cần stack phức tạp:** Để HPA đọc được metric từ Prometheus, phải deploy thêm **Prometheus Adapter** và cấu hình `APIService` — nhiều bước, dễ lỗi.
- Chỉ scale dựa trên **giá trị metric tại thời điểm hiện tại**, không có cơ chế schedule hay event-driven.

---

## 3. KEDA (Kubernetes Event-Driven Autoscaler)

**KEDA** là một operator mở rộng, được thiết kế để lấp đầy những điểm yếu của HPA.

> [!info] Bản chất KEDA
> KEDA **không thay thế HPA** — nó tạo và quản lý HPA object ở phía sau. KEDA là lớp trừu tượng ở trên, giúp đơn giản hóa cấu hình và bổ sung thêm khả năng.

### 3.1. Những gì KEDA bổ sung

| Tính năng | HPA thuần | KEDA |
|---|---|---|
| Scale to zero | ❌ | ✅ |
| Số lượng scalers tích hợp | 3 tầng (cần adapter) | **50+ scalers** (Kafka, SQS, Redis, Prometheus, Cron, ...) |
| Cấu hình | Phức tạp (cần Prometheus Adapter) | Đơn giản, khai báo trong `ScaledObject` |
| Event-driven | ❌ | ✅ |
| Schedule-based | ❌ | ✅ (CronScaler) |

### 3.2. Cấu hình KEDA với Prometheus scaler

```yaml
apiVersion: keda.sh/v1alpha1
kind: ScaledObject
metadata:
  name: inference-scaler
spec:
  scaleTargetRef:
    name: inference-deployment
  minReplicaCount: 0      # scale to zero được
  maxReplicaCount: 10
  triggers:
  - type: prometheus
    metadata:
      serverAddress: http://prometheus:9090
      metricName: http_requests_total
      threshold: "100"
      query: sum(rate(http_requests_total[1m]))
```

---

## 4. So sánh & Khi nào chọn

> [!warning] Đính chính quan trọng
> HPA không "nhìn sai" metric. HPA hoàn toàn có thể đọc custom metric từ Prometheus — nhưng phải cấu hình thêm Prometheus Adapter khá phức tạp. KEDA tiện hơn vì nó tích hợp sẵn Prometheus scaler, không cần adapter riêng.

### Khi nào chọn HPA thuần?
- Chỉ cần scale theo **CPU/Memory** đơn giản.
- Không có yêu cầu scale to zero.
- Muốn giảm số lượng component trong cluster.

### Khi nào chọn KEDA?
- Cần **scale to zero** để tiết kiệm chi phí.
- Metric phức tạp hơn CPU/RAM: queue depth, request rate, custom business metric.
- Cần **schedule-based scaling** (warm up trước giờ cao điểm).
- Muốn cấu hình đơn giản, tập trung tất cả trong một `ScaledObject`.

---

## 5. Pattern thực tế: Prometheus + CronScaler kết hợp

Kết hợp hai trigger trong một `ScaledObject` để giải quyết cả hai bài toán:

```yaml
triggers:
# Trigger 1: Scale theo metric thực tế
- type: prometheus
  metadata:
    query: sum(rate(http_requests_total[1m]))
    threshold: "50"

# Trigger 2: Pre-warm trước giờ cao điểm (tránh cold start)
- type: cron
  metadata:
    timezone: Asia/Ho_Chi_Minh
    start: "0 8 * * 1-5"   # 8:00 sáng thứ 2-6
    end:   "0 20 * * 1-5"  # 8:00 tối thứ 2-6
    desiredReplicas: "2"
```

**Cách hoạt động:**
- Ban ngày (giờ hành chính): CronScaler giữ tối thiểu 2 replica → không cold start.
- Ngoài giờ: replica về 0 → tiết kiệm chi phí.
- Nếu metric tăng đột biến bất kỳ lúc nào: Prometheus trigger kích hoạt scale up.

KEDA lấy `max` của tất cả các trigger để quyết định số replica cuối cùng.

---

## References
