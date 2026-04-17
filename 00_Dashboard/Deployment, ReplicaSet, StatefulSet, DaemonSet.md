2026-04-17 14:32


Tags: [[K8s]], [[devops]], [[workload]], [[infrastructure]]

# ReplicaSet, Deployment, StatefulSet, DaemonSet

### 1. ReplicaSet

- **Mục đích:** Đảm bảo hệ thống luôn duy trì một số lượng bản sao (replicas) của Pod đang hoạt động khớp với cấu hình đã khai báo tại bất kỳ thời điểm nào.
- **Cơ chế hoạt động:** ReplicaSet liên tục giám sát trạng thái của các Pod thông qua các nhãn (labels). Nếu số lượng Pod thực tế ít hơn số lượng cấu hình (do lỗi gì đó), hệ thống sẽ tự động khởi tạo thêm Pod. Nếu số lượng vượt quá mức khai báo, hệ thống sẽ tự động chấm dứt các Pod dư thừa.
- **Đặc điểm:** ReplicaSet không hỗ trợ tích hợp các chiến lược cập nhật phiên bản ứng dụng. Kubernetes khuyến cáo không nên khởi tạo trực tiếp ReplicaSet, mà nên quản lý chúng thông qua Deployment.

### 2. Deployment

- **Mục đích:** Quản lý vòng đời của các ứng dụng phi trạng thái (stateless), bao gồm việc triển khai, cập nhật phiên bản (update) và khôi phục phiên bản cũ (rollback).
> [!info] stateless là là một giao thức hoặc quy trình thiết kế mà tại đó hệ thống không lưu trữ bất kỳ dữ liệu (trạng thái) nào của các phiên làm việc trước đó giữa các lần tương tác.
- **Cơ chế hoạt động:** Deployment hoạt động ở mức độ cao hơn và trực tiếp quản lý các ReplicaSet. Khi có yêu cầu thay đổi cấu hình (ví dụ: thay đổi phiên bản image của container), Deployment sẽ khởi tạo một ReplicaSet mới. Quá trình chuyển đổi (Rolling Update) diễn ra bằng cách tăng dần số lượng Pod ở ReplicaSet mới, đồng thời giảm số lượng Pod ở ReplicaSet cũ.
- **Đặc điểm:** Đảm bảo ứng dụng được cập nhật không gây gián đoạn dịch vụ (zero downtime) và cung cấp khả năng tự động khôi phục nhanh chóng nếu quá trình triển khai gặp lỗi.

### 3. StatefulSet

- **Mục đích:** Quản lý việc triển khai và mở rộng quy mô của các ứng dụng có trạng thái (stateful), nơi mỗi bản sao yêu cầu một định danh duy nhất và dữ liệu lưu trữ bền vững.
- **Cơ chế hoạt động:**
    - **Định danh cố định:** Khác với Deployment (Pod được gán tên ngẫu nhiên), StatefulSet cấp phát một định danh cố định theo thứ tự cho từng Pod (ví dụ: `app-0`, `app-1`). Khi bị khởi động lại, Pod vẫn giữ nguyên tên và định danh mạng (hostname).
    - **Khởi tạo và kết thúc có thứ tự:** Các Pod được khởi tạo tuần tự từ `0` đến `N-1`. Pod sau chỉ được khởi tạo khi Pod trước đó đã ở trạng thái sẵn sàng. Khi thu hồi, hệ thống xóa Pod theo thứ tự ngược lại (từ `N-1` về `0`).
    - **Lưu trữ độc lập:** Mỗi Pod được liên kết với một PersistentVolumeClaim (PVC) riêng. Nếu Pod bị điều phối sang Node khác, cấu hình lưu trữ cũ vẫn được tự động gắn lại vào Pod để bảo toàn dữ liệu.
- **Ứng dụng:** Triển khai các hệ thống cơ sở dữ liệu phân tán hoặc công cụ trung gian (message broker) như MongoDB, MySQL Cluster, Elasticsearch, Kafka.
# References
