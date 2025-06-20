2025-03-20 17:54


Tags: [[Linear Regression]], [[beginner]], [[Machine Learning]]

# Linear Regression for more complex models

![[Pasted image 20250320175511.png]]

- Mặc dù các phép biến đổi đầu vào có thể là phi tuyến tính như đã liệt kê ở trên (logarithm, polynomial, interaction between variables,...) nhưng mô hình hồi quy vẫn áp dụng được vì:
	- **Sự tuyến tính trong tham số $(\theta)$**
		- Phương trình hồi quy vẫn có dạng tuyến tính đối với các **hệ số $\theta$**: $$h_{\theta}(x) = \sum_{j=0}^d \theta_j\phi_j(x)$$
		- với $\theta_j$ là trọng số (*weights*) cần học của mô hình
		- $\phi_j(x)$ là *basis function*, dùng để biến đổi đặc trưng đầu vào $x$.
	- **Ý nghĩa**:
		**1. Bias $\theta_0$ và hàm cơ sở đặc biệt $\phi_0(x)=1$**
	- Thường ta đặt $\phi_0(x)=1$ để **tạo ra một hạng tử bias** trong mô hình.
	- Khi đó, $\theta_0$ hoạt động như một hằng số, giúp mô hình dịch chuyển đường hồi quy mà không làm thay đổi độ dốc.
		**2. Hàm cơ sở $\phi_j(x)$ quyết định kiểu mô hình**
	- Nếu ta chọn $\phi_j(x)$ (hàm tuyến tính), ta có **hồi quy tuyến tính chuẩn**.
	- Nếu ta chọn $\phi_j(x)=x_j^2,x_j^3,sin(x_j),e^{x_j},x_1x_2,...$, mô hình có thể học được các quan hệ **phi tuyến** nhưng vẫn là hồi quy tuyến tính (vì vẫn tuyến tính theo $\theta_j$​).
![[Pasted image 20250320181312.png]]
- Mặc dù hồi quy tuyến tính gốc chỉ có thể mô tả mối quan hệ tuyến tính, nhưng bằng cách **biến đổi đặc trưng đầu vào thành đa thức** $(x^2,x^3,...)$ mô hình có thể học được **mối quan hệ phi tuyến**.
- Do đó, dù ta đang thực hiện **hồi quy tuyến tính** trên tham số, ta vẫn có thể mô hình hóa dữ liệu có quan hệ phi tuyến.
![[Pasted image 20250320181413.png]]
- M là bậc của đa thức
# References
