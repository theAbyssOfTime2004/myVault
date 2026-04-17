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

# References
