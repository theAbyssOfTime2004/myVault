2026-04-26


Tags: [[K8s]], [[devops]], [[security]], [[RBAC]]

# K8s RBAC — ServiceAccount & Role Based Access Control

> [!info] Mọi thứ trong K8s đều đi qua **API Server**. RBAC kiểm soát: **ai** được làm **gì** với **tài nguyên** nào — ngăn Pod/tool leo thang đặc quyền hoặc truy cập dữ liệu không được phép.

---

## 1. ServiceAccount — Danh tính của Pod

**User Account** = indentity của con người (dùng `kubectl`).
**ServiceAccount** = identity của một **Pod/ứng dụng** khi nó gọi K8s API.

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: my-app-sa
  namespace: production
```

Gán vào Pod:
```yaml
spec:
  serviceAccountName: my-app-sa
  containers:
  - name: app
    ...
```

K8s tự động mount token của ServiceAccount vào Pod tại `/var/run/secrets/kubernetes.io/serviceaccount/token`. Ứng dụng dùng token này để xác thực với API Server.

> [!info] Nếu không chỉ định, Pod tự động dùng ServiceAccount `default` của namespace — thường có rất ít quyền.

---

## 2. Bốn object RBAC

```
WHO            CAN DO WHAT        ON WHAT
ServiceAccount + Role/ClusterRole + RoleBinding/ClusterRoleBinding
```

### Role — tập quyền trong một namespace

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: pod-reader
  namespace: production
rules:
- apiGroups: [""]
  resources: ["pods", "pods/logs"]
  verbs: ["get", "list", "watch"]   # Chỉ đọc, không sửa/xóa
```

### ClusterRole — giống Role nhưng áp dụng toàn cluster

Dùng cho tài nguyên không thuộc namespace (Node, PersistentVolume) hoặc khi cần quyền đồng nhất trên mọi namespace.

### RoleBinding — nối ServiceAccount với Role

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: read-pods-binding
  namespace: production
subjects:
- kind: ServiceAccount
  name: my-app-sa
  namespace: production
roleRef:
  kind: Role
  name: pod-reader
  apiGroup: rbac.authorization.k8s.io
```

### ClusterRoleBinding — nối với ClusterRole, có hiệu lực toàn cluster

---

## 3. Verbs — Những gì có thể làm

| Verb | HTTP tương đương | Ý nghĩa |
|---|---|---|
| `get` | GET | Đọc một object cụ thể |
| `list` | GET (collection) | Liệt kê nhiều object |
| `watch` | GET + stream | Lắng nghe thay đổi realtime |
| `create` | POST | Tạo mới |
| `update` | PUT | Cập nhật toàn bộ |
| `patch` | PATCH | Cập nhật một phần |
| `delete` | DELETE | Xóa |

---

## 4. Scope: Role vs ClusterRole

```
Namespace A          Namespace B          Cluster-wide
┌─────────────┐      ┌─────────────┐      ┌──────────────────┐
│ Role        │      │ Role        │      │ ClusterRole      │
│ RoleBinding │      │ RoleBinding │      │ ClusterRoleBinding│
└─────────────┘      └─────────────┘      └──────────────────┘
   Chỉ ảnh             Chỉ ảnh              Ảnh hưởng tất cả
   hưởng NS A          hưởng NS B           namespaces + cluster
                                            resources (Node, PV)
```

> [!tip] Dùng ClusterRole + **RoleBinding** (không phải ClusterRoleBinding) để tái sử dụng tập quyền nhưng vẫn giới hạn scope trong một namespace cụ thể.

---

## 5. Nguyên tắc Least Privilege

Chỉ cấp đúng quyền cần thiết, không hơn:

```yaml
# BAD: cấp toàn quyền
verbs: ["*"]
resources: ["*"]

# GOOD: chỉ đọc Pod trong namespace cụ thể
verbs: ["get", "list"]
resources: ["pods"]
```

**Use case thực tế:**

| Actor | ServiceAccount | Quyền cần |
|---|---|---|
| CI/CD pipeline | `cicd-sa` | `update` Deployment (đổi image tag), không được xóa hay đọc Secret |
| Prometheus | `monitoring-sa` | `get`, `list`, `watch` Pod, Node, Service |
| Ứng dụng thông thường | `default` | Không cần gọi K8s API → zero quyền |
| Argo CD | `argocd-sa` | `get/list/watch/create/patch` hầu hết resources |

---

## 6. Kiểm tra quyền nhanh

```bash
# ServiceAccount X có quyền list pods trong namespace Y không?
kubectl auth can-i list pods \
  --as=system:serviceaccount:production:my-app-sa \
  --namespace production

# Xem toàn bộ quyền của một SA
kubectl get rolebindings,clusterrolebindings -A \
  -o json | jq '... | select(.subjects[]?.name == "my-app-sa")'
```

# References
