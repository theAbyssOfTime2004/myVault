2026-04-30


Tags: [[K8s]], [[devops]], [[CoreDNS]]

# Internal DNS của Kubernetes (`*.svc.cluster.local`)

> [!info] Đây là **DNS nội bộ** của cluster — không phải DNS public ngoài Internet. Mỗi Service tự động được cấp một tên DNS theo format dưới đây, và bất kỳ Pod nào trong cluster có thể gọi tên này để truy cập Service mà **không cần biết IP**.

```
<service-name>.<namespace>.svc.cluster.local
```

---

## Ai cấp DNS này?

**CoreDNS** (trước đây là kube-dns) — chạy như một Deployment trong namespace `kube-system`. Mọi Pod khi khởi tạo đều được cấu hình `/etc/resolv.conf` trỏ tới CoreDNS:

```bash
$ kubectl exec -it my-pod -- cat /etc/resolv.conf
nameserver 10.96.0.10                    # IP của CoreDNS
search default.svc.cluster.local svc.cluster.local cluster.local
options ndots:5
```

→ Vì thế Pod có thể gọi tên ngắn gọn, không cần FQDN đầy đủ.

---

## Phân tích từng phần

```
my-app.production.svc.cluster.local
  │       │       │      │
  │       │       │      └── Cluster domain (mặc định, có thể đổi)
  │       │       └── "svc" = đây là Service (phân biệt với pod, node...)
  │       └── Namespace mà Service đang sống
  └── Tên Service
```

---

## Các mức rút gọn (nhờ `search` domains)

Pod ở **cùng namespace** với Service → gọi cực ngắn:

| Pod gọi từ đâu | Cú pháp dùng được |
|---|---|
| Cùng namespace `production` | `my-app` ✅ ngắn nhất |
| Cùng namespace | `my-app.production` |
| Khác namespace | `my-app.production.svc` |
| Bất kỳ đâu, đầy đủ FQDN | `my-app.production.svc.cluster.local` |

```python
# Pod backend ở namespace "production" gọi Redis cùng namespace
redis_client = Redis(host="redis", port=6379)

# Gọi service ở namespace khác
analytics = httpx.get("http://api.analytics.svc.cluster.local/stats")
```

---

## Với từng loại Service

| Service type | DNS resolve về |
|---|---|
| `ClusterIP` | IP ảo của Service (kube-proxy LB sang Pod) |
| `NodePort` | Cũng là ClusterIP (nội bộ vẫn dùng được) |
| `LoadBalancer` | Cũng là ClusterIP nội bộ (bên ngoài thì là External-IP) |
| `Headless` (`clusterIP: None`) | Trả về **IP của từng Pod** → dùng cho StatefulSet, database cluster |

Ví dụ headless service cho Postgres cluster:
```
postgres-0.postgres.production.svc.cluster.local  → Pod 0
postgres-1.postgres.production.svc.cluster.local  → Pod 1
postgres-2.postgres.production.svc.cluster.local  → Pod 2
```

---

## Khác nhau với domain public

| | Internal DNS (`*.cluster.local`) | Public DNS (`api.example.com`) |
|---|---|---|
| Ai resolve | CoreDNS trong cluster | DNS provider (Route53, Cloudflare…) |
| Truy cập từ đâu | **Chỉ trong cluster** | Internet |
| Dùng cho | Service-to-service nội bộ | Client/người dùng cuối |
| Service type | ClusterIP đủ rồi | LoadBalancer hoặc Ingress |

→ Chốt: khi 2 microservice trong cluster nói chuyện với nhau, **luôn dùng internal DNS**, không bao giờ đi vòng ra Internet (chậm, tốn tiền egress, không bảo mật).

---

## Test thử trong cluster

```bash
# Tạo pod debug tạm thời
kubectl run -it --rm debug --image=busybox --restart=Never -- sh

# Bên trong pod:
nslookup kubernetes.default.svc.cluster.local
# → resolve về ClusterIP của API server

nslookup my-app                               # ngắn (cùng namespace)
nslookup my-app.production.svc.cluster.local  # đầy đủ FQDN
```

---

## Lưu ý nhỏ

- **`ndots:5`** trong `resolv.conf` nghĩa là: nếu tên có ít hơn 5 dấu chấm, resolver sẽ thử ghép với từng `search` domain trước. Vì vậy `redis` sẽ được thử lần lượt: `redis.default.svc.cluster.local` → `redis.svc.cluster.local` → `redis.cluster.local` → cuối cùng mới ra Internet. Có thể gây **chậm** khi gọi domain ngoài → cân nhắc dùng FQDN có dấu chấm cuối (`google.com.`) để bypass.
- Cluster domain mặc định là `cluster.local` nhưng có thể đổi khi setup cluster (kubelet flag `--cluster-domain`).
- CoreDNS có thể được mở rộng (rewrite, forward sang DNS server khác, custom zones) qua ConfigMap `coredns` trong `kube-system`.

# References
- [[k8s Services]]
- [[k8s Service Exposure - NodePort vs Ingress vs LoadBalancer]]
- [[K8s]]
