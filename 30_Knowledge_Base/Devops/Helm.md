2026-04-26


Tags: [[K8s]], [[devops]], [[helm]], [[infrastructure]]

# Helm — Package Manager cho Kubernetes

> [!info] Helm là "apt/pip" của Kubernetes. Thay vì phải viết và quản lý hàng chục file YAML riêng lẻ, Helm cho phép đóng gói toàn bộ ứng dụng K8s thành một **Chart** duy nhất, có thể cài đặt, cập nhật và gỡ bỏ với một lệnh.

---

## 1. Tại sao cần Helm?

Khi deploy một ứng dụng thực tế lên K8s, bạn cần nhiều object: Deployment, Service, ConfigMap, Secret, Ingress, ServiceAccount, ... Vấn đề phát sinh:

- **Trùng lặp cấu hình:** Tên namespace, image tag, resource limits lặp đi lặp lại ở nhiều file.
- **Khó tái sử dụng:** Deploy lên môi trường `dev` vs `prod` chỉ khác vài giá trị nhưng phải maintain 2 bộ YAML khác nhau.
- **Không có version history:** Không biết đã deploy phiên bản nào, không rollback được.

Helm giải quyết tất cả bằng cách tách **template** (cấu trúc YAML) ra khỏi **values** (các giá trị cụ thể).

---

## 2. Ba khái niệm cốt lõi

### 2.1. Chart

Một **Chart** là gói Helm — một thư mục chứa tất cả các file cần thiết để deploy một ứng dụng:

```
my-app/
├── Chart.yaml          # Metadata: tên, version, description
├── values.yaml         # Giá trị mặc định
├── templates/          # Các file YAML có template
│   ├── deployment.yaml
│   ├── service.yaml
│   └── ingress.yaml
└── charts/             # Dependencies (sub-charts)
```

### 2.2. Release

Mỗi lần bạn `helm install` một Chart vào cluster, Helm tạo ra một **Release** — một instance cụ thể của Chart đang chạy. Bạn có thể install cùng một Chart nhiều lần với tên release khác nhau (ví dụ: `my-app-dev`, `my-app-prod`).

### 2.3. Repository

Nơi lưu trữ và phân phối Chart. Giống như PyPI cho Python hay Docker Hub cho container image. Repository nổi tiếng: [Artifact Hub](https://artifacthub.io).

---

## 3. Templating với Go Template

Helm dùng Go Template syntax để inject values vào YAML:

```yaml
# templates/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ .Release.Name }}-app
spec:
  replicas: {{ .Values.replicaCount }}
  template:
    spec:
      containers:
      - name: {{ .Chart.Name }}
        image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
        resources:
          limits:
            cpu: {{ .Values.resources.limits.cpu }}
```

```yaml
# values.yaml
replicaCount: 2
image:
  repository: my-registry/my-app
  tag: "v1.2.0"
resources:
  limits:
    cpu: "500m"
```

Khi deploy, Helm render template + values thành YAML thuần rồi apply lên K8s.

---

## 4. Các lệnh Helm thiết yếu

```bash
# Thêm repository
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update

# Tìm kiếm chart
helm search repo nginx

# Xem values mặc định của chart
helm show values bitnami/nginx

# Cài đặt (tạo release mới)
helm install my-release bitnami/nginx

# Cài đặt với custom values
helm install my-release bitnami/nginx \
  --values custom-values.yaml \
  --set replicaCount=3 \
  --namespace production

# Xem danh sách release đang chạy
helm list -A

# Cập nhật release
helm upgrade my-release bitnami/nginx --values updated-values.yaml

# Rollback về revision trước
helm rollback my-release 1

# Xem history của release
helm history my-release

# Gỡ bỏ release
helm uninstall my-release
```

---

## 5. Quản lý môi trường với multiple values files

Cách phổ biến để handle dev/staging/prod:

```
values.yaml           # Giá trị base (chung cho mọi env)
values-dev.yaml       # Override cho dev
values-prod.yaml      # Override cho prod
```

```bash
# Deploy lên prod: Helm merge theo thứ tự, file sau override file trước
helm install my-app ./my-chart \
  --values values.yaml \
  --values values-prod.yaml
```

---

## 6. Helm vs Kustomize

| | Helm | Kustomize |
|---|---|---|
| **Approach** | Templating (Go Template) | Patching (overlay trên YAML gốc) |
| **Learning curve** | Cao hơn | Thấp hơn |
| **Tái sử dụng** | Rất cao (Chart có thể share, publish) | Trung bình |
| **Logic phức tạp** | ✅ (if/else, loop, helper functions) | ❌ |
| **Tích hợp K8s** | External tool | Tích hợp sẵn trong `kubectl` |
| **Khi nào dùng** | Deploy ứng dụng phức tạp, share Chart | Customize Chart có sẵn, GitOps đơn giản |

> [!tip] Trong thực tế, nhiều team dùng cả hai: **Helm** để deploy third-party charts (Prometheus, Grafana, cert-manager), **Kustomize** để patch các chart đó cho từng môi trường.

# References
