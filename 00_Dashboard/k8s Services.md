2026-04-16 22:21


Tags: [[K8s]], [[devops]]

# k8s Services: ClusterIP, NodePort, LoadBalancer

> [!info] Ba loại Service này không hoạt động độc lập mà **nằm chồng lên nhau**. Loại thứ 2 (NodePort) bao gồm luôn tính năng của loại 1. Loại thứ 3 (LoadBalancer) bao gồm luôn tính năng của loại 1 và 2.

### 1. ClusterIP (Internal)

- Là loại service cơ bản nhất, K8s sẽ tạo 1 virtual IP chỉ có thể truy cập từ internal network của cụm 
	=> **Không thể** truy cập ClusterIP từ mạng bên ngoài 
- **Use case**: 
- Dùng cho giao tiếp nội bộ giữa các microservices
- _Ví dụ trong AI:_ Bạn có một Pod chạy Database (Redis/PostgreSQL) lưu trữ cache cho mô hình ngôn ngữ lớn (LLM). Bạn sẽ dùng ClusterIP cho Database này, để chỉ có các Pod chạy code Inference mới gọi được DB, còn bên ngoài internet tuyệt đối không thể chạm tới DB.

### 2. NodePort (mở cổng ra ngoài ở mức cơ bản)

- K8s sẽ mở 1 port trên tất cả các Nodes trong cụm, có thể truy cập bằng cách: `Địa_chỉ_IP_của_Node:NodePort`

**Bản chất kỹ thuật:**
- NodePort nằm đè lên ClusterIP.
- Khi bạn tạo NodePort, K8s tự động chọn một cổng ngẫu nhiên trong dải từ **30000 đến 32767** (hoặc bạn tự chỉ định).
- Bất cứ ai truy cập vào cổng này trên _bất kỳ Node nào_, traffic sẽ tự động được đẩy vào ClusterIP nội bộ, rồi đẩy tiếp xuống Pod.

### 3. LoadBalancer (Cổng giao tiếp chuẩn mực - Mức Production)

**Bản chất kỹ thuật:**
- LoadBalancer nằm đè lên NodePort.
- Khi bạn khai báo type là LoadBalancer, K8s sẽ tự động gửi API call đến nhà cung cấp Cloud mà bạn đang dùng (như AWS, Google Cloud, Azure).
- Nhà cung cấp Cloud sẽ cấp phát một Load Balancer thực sự bên ngoài cụm K8s (ví dụ: AWS ALB). Load Balancer này sẽ có một IP Public hoặc Domain.
- Traffic đi từ Internet -> Trúng Cloud Load Balancer -> Phân phát vào các NodePort trên các máy chủ K8s -> Đẩy vào ClusterIP -> Vào Pod.

### Tóm tắt luồng đi của dữ liệu (Traffic Flow)

Nếu ta có một hệ thống lớn đang chạy LoadBalancer, thì đường đi của một gói tin (packet) từ trình duyệt của người dùng đến được cái ứng dụng AI của ta sẽ đi qua tất cả các lớp này:

**Internet** `-->` **Cloud LoadBalancer** (IP Public) `-->` **NodePort** (Cổng 3xxxx trên Máy chủ) `-->` **ClusterIP** (Mạng ảo nội bộ) `-->` **Container Port** (Port 80 của Nginx/FastAPI).
# References
