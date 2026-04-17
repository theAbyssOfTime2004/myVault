2026-04-16 18:39


Tags: [[kubernetes]], [[devops]], [[Docker]], [[infrastructure]]

# K8s

---

# Nhập môn Kubernetes (K8s) - Kiến trúc & Khái niệm cốt lõi

> [!info] Tổng quan Kubernetes (K8s) là một Container Orchestration System mã nguồn mở. Nó tự động hóa deployment, scaling và quản lý vận hành các ứng dụng được containerized trên một cụm (cluster) máy chủ.

## 1. Bản chất của Kubernetes

K8s không chạy mã nguồn trực tiếp. Nó quản lý các môi trường thực thi (như Docker, containerd) dựa trên hai nguyên lý cốt lõi:

1. **Trạng thái khai báo (Declarative State):** Người dùng định nghĩa trạng thái mong muốn của hệ thống thông qua các tệp cấu hình (YAML/JSON). K8s sẽ liên tục giám sát và tự động điều chỉnh hệ thống thực tế để khớp với trạng thái khai báo này (Reconciliation Loop).
2. **Quản lý hạ tầng theo cụm (Cluster-based Infrastructure):** K8s gộp tài nguyên tính toán, mạng và lưu trữ của nhiều máy chủ vật lý/ảo thành một "hồ chứa" (pool) tài nguyên duy nhất và phân bổ chúng dựa trên nhu cầu của ứng dụng.

## 2. Kiến trúc cụm Kubernetes (Cluster Architecture)

Một cụm K8s bao gồm hai thành phần chính: **Control Plane** (Bộ não điều khiển) và các **Worker Nodes** (Nơi chạy ứng dụng).

### 2.1. Control Plane (Các Node Quản lý)

Đây là các tiến trình cốt lõi đưa ra quyết định toàn cục cho cụm:

- **`kube-apiserver`:** Trái tim của K8s. Đây là cổng giao tiếp duy nhất. Mọi lệnh từ người dùng (qua `kubectl`) hay các thành phần khác đều phải đi qua API Server.
    
- **`etcd`:** Cơ sở dữ liệu key-value phân tán, lưu trữ toàn bộ cấu hình và trạng thái hiện tại của cụm. K8s dùng `etcd` làm "nguồn chân lý" (source of truth).
    
- **`kube-scheduler`:** Quản lý việc cấp phát tài nguyên. Khi có một ứng dụng mới cần chạy, scheduler sẽ tính toán xem Worker Node nào đang có đủ CPU/RAM và phù hợp nhất để đặt ứng dụng đó lên.
    
- **`kube-controller-manager`:** Chạy các tiến trình vòng lặp kiểm soát (Control Loops). Nó phát hiện sự sai lệch giữa trạng thái hiện tại và trạng thái khai báo, sau đó kích hoạt các hành động để đưa hệ thống về đúng quỹ đạo (ví dụ: khởi động lại app bị lỗi).
    

### 2.2. Worker Nodes (Các Node Thực thi)

Nơi các container thực tế hoạt động. Mỗi Worker Node có các thành phần:

- **`kubelet`:** Một agent chạy trên mỗi node. Nó lắng nghe lệnh từ Control Plane và ra lệnh cho Container Runtime khởi tạo/xóa container.
    
- **`kube-proxy`:** Quản lý các quy tắc mạng (iptables/IPVS) trên node, cho phép các container giao tiếp với nhau hoặc với mạng bên ngoài.
    
- **Container Runtime:** Phần mềm chạy container thực tế (thường là `containerd` hoặc `CRI-O`, trước đây là Docker).
    


## 3. Các Object cơ bản trong K8s (Core Resources)

Trong K8s, mọi thứ đều là Object. Dưới đây là các Object nền tảng nhất:

> [!abstract] 3.1. Pod Đơn vị nhỏ nhất và cơ bản nhất trong K8s. Một Pod chứa một hoặc nhiều container chia sẻ chung Network (chung địa chỉ IP) và Storage. Bạn hiếm khi tạo Pod trực tiếp, mà sẽ tạo thông qua Deployment.

> [!abstract] 3.2. Deployment Object dùng để quản lý Pod. Bạn định nghĩa số lượng Pod (replicas) mong muốn trong Deployment.
> 
> - **Tính năng:** Cung cấp cơ chế cập nhật không gián đoạn (Rolling Update) và khả năng khôi phục phiên bản cũ (Rollback).
>     

> [!abstract] 3.3. Service Pod có thể bị xóa và tạo lại liên tục, dẫn đến địa chỉ IP thay đổi. Service cung cấp một địa chỉ IP và DNS tĩnh, đồng thời đóng vai trò là một Load Balancer nội bộ để phân phối lưu lượng mạng đến các Pod đang hoạt động.
> 
> - Các loại chính: `ClusterIP` (chỉ mạng nội bộ), `NodePort` (mở port trên mỗi node), `LoadBalancer` (tích hợp với Cloud Provider).
>     

> [!abstract] 3.4. ConfigMap & Secret Tách biệt cấu hình khỏi mã nguồn.
> 
> - **ConfigMap:** Lưu trữ các biến môi trường, file cấu hình (không mã hóa).
>     
> - **Secret:** Lưu trữ dữ liệu nhạy cảm (password, token, ssh keys) dưới dạng base64.
>     

> [!abstract] 3.5. Persistent Volume (PV) & Persistent Volume Claim (PVC) K8s quản lý lưu trữ (Storage). Container có tính stateless (mất dữ liệu khi khởi động lại).
> 
> - **PV:** Là phân vùng lưu trữ vật lý (NFS, Cloud Disk).
>     
> - **PVC:** Là yêu cầu sử dụng dung lượng lưu trữ từ Pod.
>     


## 4. Tương tác với K8s: Workflow cơ bản

Cách tiếp cận chuẩn khi làm việc với K8s:

1. **Viết file cấu hình (YAML):** Định nghĩa Object.
    
    YAML
    
    ```
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: my-ml-app
    spec:
      replicas: 3
      template:
        spec:
          containers:
          - name: inference-container
            image: my-repo/inference:v1
    ```
    
2. **Áp dụng cấu hình:** Sử dụng CLI tool là `kubectl`.
    
    Bash
    
    ```
    kubectl apply -f deployment.yaml
    ```
    
1. **K8s xử lý:** API Server nhận YAML -> Lưu vào `etcd` -> Controller phát hiện cần 3 replicas -> Scheduler tìm Node trống -> Kubelet trên Node đó tải Image và chạy Container.

## 5. Tại sao AI/Data Science Engineer cần K8s?

Mặc dù xuất phát từ giới Software Engineering, K8s hiện nay là xương sống cho MLOps:

- **Tính toán phân tán:** K8s tối ưu cho việc điều phối các workload nặng song song. Thay vì chạy thủ công trên nhiều máy, K8s tự động phân phối các tiến trình training hoặc các framework tối ưu hóa phân tán (như SDPO) ra toàn bộ cụm.
    
- **Quản lý GPU chuẩn xác:** K8s có khả năng cấp phát (schedule) tài nguyên phần cứng chuyên biệt như GPU/TPU cho từng Pod cụ thể thông qua _Device Plugins_.
    
- **Mở rộng linh hoạt (Auto-scaling):** Có thể tự động tăng số lượng container khi lưu lượng suy luận (Inference request) của model tăng đột biến, và giảm xuống để tiết kiệm chi phí tính toán khi rảnh rỗi.

# References
