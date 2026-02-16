2025-03-24 18:11


Tags: [[Neural Network]], [[Deep Learning]], [[data scientist]]

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
 ### Feed Forward
 -  trong mạng neuron, tất cả các node được kết nối đôi một với nhau theo 1 chiều duy nhất từ tầng vào đến tầng ra. Tức là mỗi node ở 1 tầng nào đó sẽ nhận đầu vào là tất cả các node ở tầng trước đó mà không suy luận ngược lại:
 $$
z_i^{(l+1)} = \sum_{j=1}^{n^{(l)}} w_{ij}^{(l+1)} a_j^{(l)} + b_i^{(l+1)}
$$
$$
a_j^{(l+1)} = f(z_i^{(l+1)})
$$
- Với 
	- $a_j^{(l)}$​ là đầu ra của lớp $l$ (được tính từ bước trước).
	- $w_{ij}^{(l+1)}$​ là trọng số kết nối từ neuron $j$ (ở lớp $l$) đến neuron $i$ (ở lớp $l+1$).
	- $b_i^{(l+1)}​$ là bias giúp điều chỉnh giá trị.
- Để dễ hình dung thì ta hãy suy nghĩ đến bước tiếp theo là tính $z_i^{l+2}$ và $a_j^{l+2}$ sau khi có đầu ra $a_j^{l+1}$ ở bước trước: 
- thì trước tiên ta sẽ tính $z_i^{(l+2)}$ từ đầu ra $a_j^{(l+1)}$ = $a_i^{(l+1)}$ mà ta tính ở bước trước do đó công thức của $z_i^{(l+2)} = \sum_{j=1}^{n^{(l+1)}} w_{ij}^{(l+2)} a_j^{(l+1)} + b_i^{(l+2)}$ và sau khi có được z_i(l+2) ta sẽ cho vào activation function $f(z_i^{(l+2)})$ và cuối cùng ta được đầu ra $a_i^{(l+2)}$
- Để tiện tính toán, ta coi $a_0^{(l)}$ là một đầu vào và $w_{i0}^{l+1} = b_i^{l+1}$ là tham số trọng lượng của đầu vào này. Lúc đó ta có thể viết lại công thức trên dưới dạng vector:
	$$
\begin{aligned}
\mathbf{z}^{(l+1)} &= \mathbf{W}^{(l+1)} \cdot \mathbf{a}^{(l)} \\
\mathbf{a}^{(l+1)} &= f\bigl(\mathbf{z}^{(l+1)}\bigr)
\end{aligned}
$$
- Giải thích cho việc tại sao ta có thể làm mất đi bias $b_i^{l+1}$, là bởi vì ta đã nhúng bias $b_i^{l+1}$ vào ma trận trọng số $\mathbf{W}^{(l+1)}$
![[Pasted image 20250325160006.png]]
![[Pasted image 20250325160017.png]] 
### Backpropagation
![[Pasted image 20250325172731.png]]
![[Pasted image 20250325174119.png]]
![[Pasted image 20250325174711.png]]
![[Pasted image 20250325174722.png]]
![[Pasted image 20250325174732.png]]
- Khi đến đc lớp cuối, nghĩa là ta đã hoàn thành việc lan truyền ngược sai số nhận được ở lớp L cuối cùng về lớp L đầu tiên 
![[Pasted image 20250325175507.png]]
# References
