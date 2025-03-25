2025-03-24 18:11


Tags: [[Neural Network]], [[DeepLearning]], [[data scientist]]

# Neural networks foundation
### Perceptron
- Một mạng neural được cấu thành từ các neural đơn lẻ được gọi là *perceptron*. 
- ![[Pasted image 20250324181315.png]]
- 1 perceptron sẽ nhận 1 hoặc nhiều đầu vào dạng nhị phân và cho ra output $o$ dạng nhị phân duy nhất, các đầu vào bị ảnh hưởng bởi tham số $w$ tương ứng của nó, còn kết quả đầu ra được quyết định dựa vào 1 ngưỡng quyết định $b$ nào đó: 
- $$ o = \begin{cases} 0 &\text{if }\displaystyle\sum_iw_ix_i \le \text{threshold} \cr 1 &\text{if }\displaystyle\sum_iw_ix_i > \text{threshold} \end{cases} $$
- Đặt $b=-\text{threshold}$, ta có thể viết lại thành: $$ o = \begin{cases} 0 &\text{if }\displaystyle\sum_iw_ix_i + b \le 0 \cr 1 &\text{if }\displaystyle\sum_iw_ix_i + b > 0 \end{cases} $$
- Để dễ hình dung, ta lấy ví dụ việc đi nhậu hay không phụ thuộc vào 4 yếu tố sau:
	- 1. Trời có nắng hay không?
	- 2. Có hẹn trước hay không?
	- 3. Vợ có vui hay không?
	- 4. Bạn nhậu có ít khi gặp được hay không?

Thì ta coi 4 yếu tố đầu vào là $x_1, x_2, x_3, x_4$ và nếu $o=0$ thì ta không đi nhậu còn $o=1$ thì ta đi nhậu. Giả sử mức độ quan trọng của 4 yếu tố trên lần lượt là $w_1=0.05, w_2=0.5, w_3=0.2, w_4=0.25$ và chọn ngưỡng $b=-0.5$ thì ta có thể thấy rằng việc trời nắng có ảnh hưởng chỉ 5% tới quyết định đi nhậu và việc có hẹn từ trước ảnh hưởng tới 50% quyết định đi nhậu của ta.

Nếu gắn $x_0=1$ và $w_0=b$, ta còn có thể viết gọn lại thành: $$ o = \begin{cases} 0 &\text{if }\mathbf{w}^{\intercal}\mathbf{x} \le 0 \cr 1 &\text{if }\mathbf{w}^{\intercal}\mathbf{x} > 0 \end{cases} $$
### Sigmoid Neurons
- Với đầu vào và đầu ra dạng nhị phân, ta rất khó có thể điều chỉnh một lượng nhỏ đầu vào để đầu ra thay đổi chút ít vì tính không liên tục , nên để linh động ta có thể mở rộng chúng thay vì chỉ 0 hoặc 1 thì sẽ là khoảng $[0;1]$. Lúc này đầu ra sẽ được quyết định bởi 1 hàm (activation function) sigmoid $\sigma(\mathbf{w}^{\intercal}\mathbf{x})$ và hàm sigmoid này có công thức là: $$ \sigma(z) = \dfrac{1}{1+e^{-z}} $$
![[Pasted image 20250324182121.png]]
- Đặt $z = \mathbf{w}^{\intercal}\mathbf{x}$ thì công thức của perceptron lúc này sẽ có dạng: $$ o = \sigma(z) = \dfrac{1}{1+\exp(-\mathbf{w}^{\intercal}\mathbf{x})} $$
- Một cách tổng quát , hàm perceptron được biểu diễn qua một activation function $f(z)$ như sau: $$ o = f(z) = f(\mathbf{w}^{\intercal}\mathbf{x}) $$
- Bằng cách biểu diễn như vậy ta có thể coi neuron sinh học được biểu diễn như sau:![[Pasted image 20250325121459.png]]
- So với ban đầu: ![[Pasted image 20250325121527.png]]
- một điểm cần lưu ý là các activation function phải là [[hàm phi tuyến]]. vì nếu nó là hàm tuyến tính thì khi kết hợp các phép toán tuyến tính $\mathbf{w}^{\intercal}\mathbf{x}$ thì kết quả thu đc cũng chỉ là một phép biến đổi tuyến tính dẫn tới chuyện nó trở nên vô nghĩa
# References
