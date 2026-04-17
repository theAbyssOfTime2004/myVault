2026-04-17 13:52


Tags: [[K8s]], [[workload]]

# Job và CronJob: Quản lý tác vụ ngắn hạn 

> [!info] : Khi sử dụng Deployment để chạy một tiến trình có điểm dừng (ví dụ: script Python huấn luyện model tự động thoát với mã `exit 0` khi hoàn thành), tiến trình kết thúc sẽ làm Pod dừng hoạt động. Vì mục đích thiết kế của Deployment là duy trì các Pod chạy liên tục (always-on), hệ thống sẽ đánh giá việc Pod dừng là một sự cố và tự động khởi động lại Pod đó theo vòng lặp vô hạn. Để quản lý các tác vụ chỉ thực thi một lần và có trạng thái kết thúc rõ ràng, Kubernetes cung cấp đối tượng Job.


### 1. Job: làm xong là nghỉ 

- Job là 1 object của K8s đảm bảo rằng 1 hoặc nhiều Pod sẽ được thực thi và kết thúc một cách thành công 
**Cơ chế hoạt động**: 
- Khi bạn tạo 1 job, K8s sẽ tạo ra 1 Pod
- Pod này sẽ run code nếu code chạy xong và dump error (Crash/Exit code != 0): Job sẽ ra lệnh cho Kubelet tạo lại một Pod mới để **thử làm lại** (có thể giới hạn số lần thử lại qua thông số `backoffLimit`).
- Nếu code chạy xong và báo thành công (`exit: 0`): Pod sẽ chuyển sang trạng thái `Completed`. Nó **dừng tiêu thụ CPU/RAM**, nhưng xác Pod và log vẫn nằm đó để ta có thể vào xem kết quả.
**Use cases**: 
- *Model Training:*  Một quá trình train model mất 5 tiếng. Đóng gói nó thành Job. Train xong, nó lưu weights vào PVC rồi tự tắt.
- *Migrating database:* Chạy các lệnh cập nhật schema cơ sở dữ liệu trước khi tung ra phiên bản API mới.

### 2. CronJob: Làm việc theo lịch trình

**Cơ chế hoạt động:**
- Định nghĩa một lịch trình bằng Cron format (ví dụ: `0 2 * * *` nghĩa là 2 giờ sáng mỗi ngày). -  có thể lên [Crontab.guru - The cron schedule expression generator](https://crontab.guru/) để xem 
- Cứ đúng giờ đó, K8s Control Plane sẽ tự động **đẻ ra một cái Job mới**.
- Cái Job mới đó lại tiếp tục đẻ ra Pod để làm việc. Làm xong lại nghỉ.
**Use cases**: 
- **Retraining Model:** Cứ 12h đêm Chủ Nhật, tự động kéo dữ liệu mới của tuần qua về để train lại mô hình dự đoán.
- **Backup:** Mỗi 2h sáng tự động dump database và đẩy lên AWS S3.
- **Dọn rác (Garbage Collection):** Dọn dẹp các thư mục log tạm (emptyDir dư thừa) mỗi cuối ngày.
# References
