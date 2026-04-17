2026-04-16 22:42


Tags: [[K8s]], [[devops]]

# k8s Storage: emptyDir, PV và PVC


### 1. emptyDir (lưu trữ tạm thời - ephemeral)

- Như tên gọi, nó là 1 thư mục trống, khi 1 Pod được initialized ở 1 Node, K8s sẽ tạo ra 1 thư mục tên `emptyDir` trên ổ cứng của node đó và cho phép Pod ghi dữ liệu vào
	- Nếu Pod bị xóa bằng bất kỳ lý do gì thì emptyDir cũng sẽ bay màu vĩnh viễn cùng Pod 
	- **Chia sẻ nội bộ:** Nếu Pod của có 2 container, cả 2 container này có thể cùng đọc/ghi vào chung một cái `emptyDir`.

### 2. PV - PersistentVolume 

**Khái niệm:** Đây là một "Khối lưu trữ vật lý" thực sự nằm trên cụm hoặc ngoài mạng Cloud (Ví dụ: Một ổ cứng SSD 100GB, một phân vùng AWS EBS, hay một thư mục Share mạng NFS).

**Bản chất & Vòng đời:**

- **Độc lập hoàn toàn với Pod:** Pod sinh ra hay chết đi không hề ảnh hưởng đến PV. Dữ liệu trên PV là vĩnh viễn.
- **Do Admin quản lý:** Thông thường, SysAdmin sẽ là người đi mua ổ cứng và cấu hình các PV này vào cụm K8s.

### 3. PVC - PersistentVolumeClaim 

- **Khái niệm:** K8s không cho phép Pod kết nối thẳng thẳng trực tiếp vào cái PV (ổ cứng). Thay vào đó, nó dùng PVC. **PVC là một lời yêu cầu (Claim) xin cấp phát lưu trữ.**

- **Cơ chế hoạt động:**

	1. Lập trình viên viết file `pvc.yaml` yêu cầu: _"Tôi cần một ổ cứng 5GB, quyền Đọc/Ghi"_.
    
	2. K8s nhận tờ đơn PVC này, chạy đi tìm trong kho xem có cái **PV** nào dung lượng >= 5GB đang rảnh không.
    
	3. Nếu có, K8s sẽ **Bind (Trói/Kết nối)** cái PVC đó với cái PV kia.
    
	4. Cuối cùng, Pod của bạn sẽ "Mount" cái PVC này vào để dùng.
# References
