2025-03-18 13:47


Tags: [[Machine Learning]], [[beginner]], 

# Linear Regression

![[Pasted image 20250318134846.png]]
- Ta có 1 ví dụ về data giá nhà ở theo đặc trưng size in feet^2 như trên
![[Pasted image 20250318134941.png]]
- Mục đích là tìm 1 đường thẳng (1 hàm số) có thể thể hiện được mối liên hệ giữa đặc trưng của data và nhãn của data 
![[Pasted image 20250318135213.png]]
- Giả thuyết về dữ liệu sẽ được biểu diễn theo hàm số $y \approx h_{\theta}(x) = \theta_{0} + \theta_{1}x$ 
- Trong đó:
	- $y$ là giá trị đầu ra (giá nhà).
	- $x$ là đặc điểm của nhà (ví dụ: diện tích).
	- $\theta_{0}$​ là hệ số chặn (intercept).
	- $\theta_{1}$ là hệ số góc (slope), xác định mức độ ảnh hưởng của đặc điểm $x$ đến $y$.
-  Thuật toán học máy sẽ tìm ra bộ tham số tối ưu $\theta$ dựa trên tập huấn luyện.
- Khi có mô hình, ta có thể sử dụng nó để dự đoán giá trị yyy cho dữ liệu mới.
- Nếu $h_{\theta}(x)$ là một hàm tuyến tính, phương pháp này được gọi là **hồi quy tuyến tính (linear regression)**.
- Ta cần tối ưu $\theta$ là bởi vì mô hình học máy dự đoán một giá trị $h_{\theta}(x)$ nhưng có thể lệch so với giá trị thực tế $y$. Độ lệch này được đo bằng **hàm mất mát (loss function)**.![[Pasted image 20250318140703.png]]
- Tối ưu $\theta$ giúp giảm giá trị $J(\theta)$ do đó giúp mô hình hoạt động chính xác hơn
![[Pasted image 20250318141141.png]]
- Visualize hàm hồi quy với các giá trị $\theta_{0}$ và $\theta_{1}$  ngẫu nhiên
![[Pasted image 20250318141315.png]]
- Cách để chọn giá trị $\theta_{0}$ và $\theta_{1}$ hợp lý là chọn làm sao cho $\theta_{0}$ và $\theta_{1}$ **gần** với y trong mẫu huấn luyện $(x,y)$, và ở đây ta có câu hỏi: "Như thế nào là **gần**?"

![[Pasted image 20250318141629.png]]
![[Pasted image 20250318141644.png]]
- Hình trên minh họa cách mô hình tìm đường thẳng tốt nhất để giảm thiểu các sai số giữa giá trị thực $y(i)$ và giá trị dự đoán $h_{\theta}(x_{i})$
- Đường nét đứt màu đỏ là đường hồi quy còn các điểm dữ liệu khoanh tròn màu xanh là giá trị thực tế, khoảng cách từ các điểm dữ liệu thực tế đến đường dự đoán là sai số dự đoán $(y_{i}-h_{\theta}(x_{i}))$ 
- dòng ![[Pasted image 20250318142825.png]] này nghĩa là min của tổng bình phương sai số (SSE)
- Sau đó ta sẽ muốn tìm trung bình của tổng bình phương sai số là từ (SSE) -> (MSE):
$$
\text{MSE} = \frac{1}{m} \sum_{i=1}^{m} (h_{\theta}(x_{i})-y_{i})^2
$$
- Và để thuận tiện cho việc đạo hàm trong *gradient descent* sau đó, ta sẽ muốn thêm hệ số 1/2, do đó MSE sẽ trở thành: 
 $$
J(\theta) = \frac{1}{2m} \sum_{i=1}^{m} (h_{\theta}(x_{i})-y_{i})^2
$$
và đây cũng chính là hàm loss mà ta sẽ muốn **minimize** để tối ưu hóa mô hình hồi quy tuyến tính của mình
**NOTE**: Việc chuyển ta chọn hàm loss là MSE thay vì SSE là vì:
- Tránh phụ thuộc vào số lượng dữ liệu
- Dễ so sánh giữa các mô hình khác nhau 
- Định nghĩa chính xác hơn về sai số:
	- SSE cho thấy tổng sai số nhưng không phản ánh mức độ sai số trung bình trên mỗi điểm dữ liệu.
	- MSE giúp ta hiểu rõ **một điểm dữ liệu trung bình bị dự đoán lệch bao nhiêu (bình phương sai số)**.
- Hỗ trợ các thuật toán tối ưu hóa một cách dễ dàng hơn
	- MSE giúp Gradient descent hoạt động ổn định hơn và hội tụ nhanh hơn vì lượng dữ liệu sẽ không quá nhiều SSE nếu mẫu quá lớn 

![[Pasted image 20250318144522.png]]
![[Pasted image 20250318144744.png]]

- 🔹 Mục tiêu của Linear Regression là tìm vector trọng số θ\thetaθ sao cho hàm dự đoán hθ(x)h_\theta(x)hθ​(x) khớp với giá trị thực yyy nhất, bằng cách **tối thiểu hóa MSE**.
# References
