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

# References
