2026-04-30


Tags: [[K8s]], [[devops]], [[DNS]]

# CoreDNS

> [!info] **CoreDNS** là DNS server **mặc định** chạy bên trong Kubernetes cluster. Nó là thứ làm cho `redis.production.svc.cluster.local` → resolve thành IP.

Trước Kubernetes 1.13, vai trò này do `kube-dns` đảm nhiệm. Từ 1.13 trở đi, **CoreDNS thay thế kube-dns** làm default — nhanh hơn, plugin-based, ít tài nguyên hơn.

---

## Nó chạy ở đâu?

CoreDNS chạy như một **Deployment** (vài replica để HA) trong namespace `kube-system`:

```bash
$ kubectl -n kube-system get pods -l k8s-app=kube-dns
NAME                       READY   STATUS    AGE
coredns-558bd4d5db-abc12   1/1     Running   3d
coredns-558bd4d5db-xyz45   1/1     Running   3d
```

> Tên Deployment vẫn dùng label `k8s-app=kube-dns` cho tương thích ngược, nhưng image thực tế là `coredns`.

Phía trước nó là một **Service ClusterIP** (thường là `10.96.0.10`) — đây là IP mà Pod nào cũng có trong `/etc/resolv.conf`:

```bash
$ kubectl -n kube-system get svc kube-dns
NAME       TYPE        CLUSTER-IP   PORT(S)
kube-dns   ClusterIP   10.96.0.10   53/UDP,53/TCP
```

---

## Pod tìm CoreDNS bằng cách nào?

Khi kubelet tạo Pod, nó tự inject DNS config vào Pod:

```bash
$ kubectl exec my-pod -- cat /etc/resolv.conf
nameserver 10.96.0.10                                    # ← IP của CoreDNS
search default.svc.cluster.local svc.cluster.local cluster.local
options ndots:5
```

→ Mọi `nslookup`, `getaddrinfo()`, request HTTP từ Pod đều đi qua CoreDNS đầu tiên.

---

## Kiến trúc plugin-based

Đây là điểm mạnh nhất của CoreDNS: cấu hình theo dạng **chuỗi plugin**, mỗi request đi qua từng plugin theo thứ tự (giống middleware). Cấu hình nằm trong **Corefile**, lưu trong ConfigMap `coredns`:

```bash
$ kubectl -n kube-system get configmap coredns -o yaml
```

```
.:53 {
    errors                          # Log lỗi
    health                          # Endpoint /health cho liveness
    ready                           # Endpoint /ready cho readiness
    kubernetes cluster.local in-addr.arpa ip6.arpa {
       pods insecure
       fallthrough in-addr.arpa ip6.arpa
       ttl 30
    }
    prometheus :9153                # Metrics cho Prometheus
    forward . /etc/resolv.conf      # DNS không thuộc cluster → forward ra ngoài
    cache 30                        # Cache 30s
    loop                            # Phát hiện DNS loop
    reload                          # Tự reload khi Corefile đổi
    loadbalance                     # Round-robin các A record
}
```

### Một request đi như thế nào?

Pod hỏi `redis.production.svc.cluster.local`:

1. **`kubernetes` plugin** — nhận ra zone `cluster.local`, tra cứu Service `redis` trong namespace `production` → trả ClusterIP. Xong.

Pod hỏi `google.com`:

1. **`kubernetes` plugin** — không thuộc `cluster.local` → bỏ qua.
2. **`cache` plugin** — chưa có cache → bỏ qua.
3. **`forward` plugin** — forward ra DNS upstream (`/etc/resolv.conf` của Node, thường là DNS của VPC/cloud) → nhận response → trả về Pod. Cache lại 30s cho lần sau.

---

## Những gì CoreDNS làm cho bạn

| Việc | Plugin |
|---|---|
| Resolve Service → ClusterIP | `kubernetes` |
| Resolve Pod (StatefulSet, headless) | `kubernetes` |
| Resolve domain ngoài (google.com) | `forward` |
| Cache để giảm tải | `cache` |
| Reverse DNS (IP → tên) | `kubernetes` |
| Health check cho kubelet | `health`, `ready` |
| Metrics Prometheus | `prometheus` |
| Custom rewrite, alias | `rewrite`, `template` |

---

## Tùy biến phổ biến

### 1. Forward một domain riêng sang DNS server khác

VD: tất cả `*.corp.local` đi sang DNS nội bộ công ty:

```
corp.local:53 {
    forward . 10.0.0.53
}
```

### 2. Stub domain cho dev

Để cluster gọi được API ở máy bạn (`api.local`):

```
api.local:53 {
    hosts {
        192.168.1.100 api.local
    }
}
```

### 3. Tăng cache để giảm latency

```
cache 300        # cache 5 phút thay vì 30s
```

### 4. NodeLocal DNSCache

Một pattern production phổ biến: cài thêm `node-local-dns` (DaemonSet) — mỗi Node có **1 cache CoreDNS local**. Pod hỏi DNS → đi vào local cache trên cùng Node → nhanh hơn nhiều, giảm áp lực lên central CoreDNS, tránh các vấn đề conntrack với UDP.

---

## Khi CoreDNS gặp vấn đề

Triệu chứng thường gặp:
- **Toàn bộ cluster chậm bất thường** → check `kubectl -n kube-system top pods coredns-*`.
- **`nslookup` fail trong Pod** → CoreDNS Pod có chạy không? Service có endpoint không?
- **Resolve domain ngoài fail** → upstream DNS (`forward`) chết hoặc Network Policy chặn.
- **DNS loop** → Corefile forward về chính CoreDNS → plugin `loop` sẽ detect và crash Pod để cảnh báo.

Debug nhanh:

```bash
# Xem log CoreDNS
kubectl -n kube-system logs -l k8s-app=kube-dns

# Test resolve từ Pod debug
kubectl run -it --rm debug --image=nicolaka/netshoot -- bash
nslookup kubernetes.default
dig redis.production.svc.cluster.local
```

---

## Tóm gọn

- **CoreDNS = DNS server nội bộ của cluster**, kế nhiệm kube-dns từ K8s 1.13.
- Chạy như Deployment trong `kube-system`, được expose qua Service `kube-dns` ở IP `10.96.0.10`.
- Mỗi Pod tự động trỏ tới đó qua `/etc/resolv.conf`.
- Kiến trúc **plugin-based** (Corefile) — cực kỳ linh hoạt: forward, cache, rewrite, custom zone, metrics.
- Plugin quan trọng nhất là `kubernetes` — nó **đọc Service/Endpoint từ API server** và sinh DNS records.

# References
- [[k8s Internal DNS - cluster.local]]
- [[k8s DNS - Pod vs Service]]
- [[k8s Services]]
- [[K8s]]
