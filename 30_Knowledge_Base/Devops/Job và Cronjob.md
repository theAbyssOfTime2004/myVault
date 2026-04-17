2026-04-17 13:52


Tags: [[K8s]], [[workload]]

# Job và Cronjob: Quản lý tác vụ ngắn hạn 

> [!info] : Khi sử dụng Deployment để chạy một tiến trình có điểm dừng (ví dụ: script Python huấn luyện model tự động thoát với mã `exit 0` khi hoàn thành), tiến trình kết thúc sẽ làm Pod dừng hoạt động. Vì mục đích thiết kế của Deployment là duy trì các Pod chạy liên tục (always-on), hệ thống sẽ đánh giá việc Pod dừng là một sự cố và tự động khởi động lại Pod đó theo vòng lặp vô hạn. Để quản lý các tác vụ chỉ thực thi một lần và có trạng thái kết thúc rõ ràng, Kubernetes cung cấp đối tượng Job.


### 1. Job: làm xong là nghỉ 

- Job là 1 object của K8s đảm bảo rằng 1 hoặc nhiều Pod sẽ được thực thi và kết thúc một cách thành công 
**Cơ chế hoạt động**: 
- Khi bạn tạo 1 job, K8s sẽ tạo ra 1 Pod
- Pod này sẽ run code nếu code chạy xong và dump error (Crash/Exit code != 0): Job sẽ ra lệnh cho Kubelet tạo lại một Pod mới để **thử làm lại** (có thể giới hạn số lần thử lại qua thông số `backoffLimit`).
- Nếu code chạy xong và báo thành công (`exit: 0`): Pod sẽ chuyển sang trạng thái `Completed`. Nó **dừng tiêu thụ CPU/RAM**, nhưng xác Pod và log vẫn nằm đó để ta có thể vào xem kết quả.
# References
