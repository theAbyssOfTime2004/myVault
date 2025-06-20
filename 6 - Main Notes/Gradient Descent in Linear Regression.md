2025-03-18 14:54


Tags: [[Machine Learning]], [[beginner]]

# Gradient Descent in Linear Regression

### Problems

![[Pasted image 20250318145428.png]]
- Sau khi học về [[Linear Regression]], ta biết rằng mình sẽ phải lập giả thuyết về hàm hồi quy và từ đó có được hàm loss $J(\theta_{0},\theta_{1})$ và ta sẽ muốn minimize loss function $J(\theta_{0},\theta_{1})$ bằng cách thay đổi các giá trị $\theta_{0},\theta_{1}$
- Vấn đề là làm sao để ta có thể thay đổi các giá trị  $\theta_{0},\theta_{1}$ làm sao để minimize  $J(\theta_{0},\theta_{1})$ một cách hợp lý nhất
![[Pasted image 20250318150154.png]]
- Bắt đầu với một initial value của $J(\theta_{0},\theta_{1})$, thuật toán tối ưu sẽ dịch chuyển giá trị đó theo hướng mà sẽ giúp lower the value of  $J(\theta_{0},\theta_{1})$ => **Gradient Descent**
### Gradient Descent

![[Pasted image 20250318150509.png]]

![[Pasted image 20250318150714.png]]
- Khởi tạo $\theta$
- Lặp lại thuật toán đến khi hội tụ: $$\theta_{j} = \theta_{j} - \alpha \frac{\partial}{\partial \theta_j}J(\theta) $$
- ![[Pasted image 20250318151209.png]]
- Hàm mất mát $J(\theta)$ là một hàm lồi (hình parabol), và mục tiêu của chúng ta là tìm giá trị $\theta_j$​ tối ưu sao cho $J(\theta)$ nhỏ nhất. Gradient Descent thực hiện việc này bằng cách **di chuyển ngược hướng gradient** để giảm giá trị $J(\theta)$. Biểu thức đạo hàm riêng của $J(\theta)$ theo biến $\theta$:
$$
\frac{\partial J(\theta)}{\partial \theta_j} = \lim_{\epsilon \to 0} \frac{J(\theta \mid \theta_j + \epsilon) - J(\theta \mid \theta_j)}{\epsilon}
$$
- Ta có 2 trường hợp:
- Gradient dương ($\epsilon > 0$)  thì giảm $\theta_j$
- Gradient âm ($\epsilon < 0$) thì tăng $\theta_j$
- Luôn cập nhật theo hướng **ngược với gradient** (cũng có nghĩa là ngược dấu với đạo hàm) để giảm hàm mất mát.
![[Pasted image 20250318152333.png]]
- Dấu = đầu tiên, khai triển $J(\theta)$, ta được  $J(\theta) = \frac{1}{2n} \sum_{i=1}^{n} (h_{\theta}(x_{i})-y_{i})^2$
- Dấu = thứ 2 tiếp tục khai triển $h_{\theta}(x_{i})$ trong ngoặc, ta được $\sum_{k=0}^{d} \theta_k x_k^{(i)}$ 
- Dấu = thứ 3 khai triển đạo hàm riêng theo biến $\theta_j$ cho cả cụm $J(\theta) = \frac{1}{2n} \sum_{i=1}^{n} (\sum_{k=0}^{d} \theta_k x_k^{(i)}-y_{i})^2$, áp dụng quy tắc đạo hàm $(u^2)' = 2uu'$ trong phần reminder ta được kết quả như trên, xem $(\sum_{k=0}^{d} \theta_k x_k^{(i)}-y_{i})^2$ như là u
- Dấu = thứ 4  là kết quả sau khi rút gọn, tiếp tục đạo hàm u, ta được như trên vì $h_{\theta}(x_{i}) = \sum_{k=0}^{d} \theta_k x_k^{(i)}$, nên đạo hàm của nó theo $\theta_j$ là: $\frac{\partial}{\partial \theta_j} h_{\theta}(x_{i}) = x_j^{(i)}$, và đạo hàm riêng theo $\theta_j$ cho biến $y^{(i)}=0$, do đó ta có được kết quả cuối cùng 
![[Pasted image 20250318160249.png]]
- Thuật toán gradient descent hội tụ khi các tiêu chí sau được thỏa mãn:
	- hàm mất mát $J(\theta)$ đủ nhỏ: $J(\theta)$ bé hơn 1 số $\epsilon$ cực nhỏ thì ta xem rằng thuật toán hội tụ
	- khoảng cách giữa giá trị $\theta$ mới và cũ đủ nhỏ: $$ \|θ_{new} - θ_{old}\|_2 < ε $$
	- Nếu sự thay đổi trong giá trị $\theta$ giữa 2 lần cập nhật nhỏ hơn 1 số $\epsilon$ (cực nhỏ) thì có nghĩa là thuật toán không còn cải thiện đáng kể và có thể dừng
	- Độ chính xác của mô hình là đủ tốt trên tập kiểm tra
![[Pasted image 20250318212833.png]]
### **1. Đồ thị bên trái: Hàm hồi quy $h(x)=-900-0.1x$**

- Trục hoành: **Kích thước nhà (square feet, $x$)**
- Trục tung: **Giá nhà (price, $y$)**
- Các dấu **x đỏ**: **Dữ liệu huấn luyện (Training data)**
- Đường **xanh dương**: **Đường hồi quy hiện tại** dựa trên tham số $\theta_0$ và $\theta_1$ 
- Phương trình hiển thị: $h(x)=-900-0.1x$ 
→ Đây là phương trình của mô hình hồi quy tuyến tính hiện tại.

📌 **Ý nghĩa:**
- Đồ thị này cho thấy mô hình hiện tại chưa phù hợp với dữ liệu.
- Đường hồi quy đang có hệ số góc âm ($\theta_1 = -0.1$), có thể chưa phải là giá trị tối ưu.
- Cần tiếp tục cập nhật tham số để đường hồi quy phù hợp hơn với dữ liệu thực tế.
### **2. Đồ thị bên phải: Hàm mất mát $J(\theta_0,\theta_1)$
- Đây là **đồ thị đường đồng mức (contour map)** thể hiện giá trị của hàm mất mát $J(\theta_0,\theta_1)$
- Trục hoành: **$\theta_0$ (hệ số chặn - bias term)**
- Trục tung: **$\theta_1$​ (hệ số góc - slope)**
- Các đường contour thể hiện các mức giá trị của hàm mất mát $J(\theta_0,\theta_1)$, với giá trị càng nhỏ khi tiến về tâm của hình elip.
- Dấu **x đỏ**: Vị trí hiện tại của các tham số $(\theta_0,\theta_1)$

📌 **Ý nghĩa:**
- Mục tiêu của Gradient Descent là tìm điểm thấp nhất (global minimum) của hàm mất mát $J(\theta_0,\theta_1)$.
- Nếu điểm đỏ chưa nằm ở trung tâm của đường đồng mức, nghĩa là mô hình chưa tối ưu và cdần tiếp tục cập nhật $(\theta_0,\theta_1)$​ bằng Gradient Descent.
![[Pasted image 20250318212816.png]]
- **Mục tiêu của Gradient Descent**: **Tìm giá trị tối ưu của $(\theta_0,\theta_1)$ sao cho hàm mất mát $J(\theta_0,\theta_1)$ nhỏ nhất.**  
- **Các dấu "×" đỏ thể hiện quá trình cập nhật tham số dần dần về điểm tối ưu.**  
-  **Khi Gradient Descent hội tụ, tham số $(\theta_0,\theta_1)$ sẽ nằm gần trung tâm các đường đồng mức.**
-  **Hiểu đơn giản**: Đồ thị này giống như một bản đồ địa hình, trong đó thuật toán Gradient Descent giống như một người leo núi, luôn tìm đường đi nhanh nhất xuống thung lũng nơi hàm mất mát nhỏ nhất. 

# References
