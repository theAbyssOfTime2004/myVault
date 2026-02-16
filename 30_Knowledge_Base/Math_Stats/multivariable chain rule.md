2025-03-25 16:14


Tags: [[Backpropagation]], [[data scientist]], [[Deep Learning]], [[beginner]]

# multivariable chain rule
### Đồ thị tính toán
- Là 1 cách hay để hiểu các biểu thức toán học. Ví dụ với biểu thức $e = (a+b)*(b+1)$, ta có 3 phép toán bao gồm 2 phép cộng và 1 phép nhân. Ta có thể biến đổi thành đồ thị như sau:
![[Pasted image 20250325161721.png]]
- Với $c$ và $d$ là 2 biến được tạo thêm để chứa 2 phép tính $a+b$ và $b+1$
- Ta có thể thực hiện các phép toán bằng cách gắn giá trị cho các biến đầu vào bằng các giá trị cụ thể nào đó và tính dần lên các nút ở phía trên của đồ thị:
![[Pasted image 20250325161856.png]]
### Đạo hàm với đồ thị tính toán
- Nếu muốn hiểu đạo hàm trong đồ thị tính toán, thì chìa khóa là cần hiểu được đạo hàm trên các cạnh của đồ thị. Nếu $a$ ảnh hưởng trực tiếp đến $c$ thì ta muốn biết nó ảnh hưởng đến $c$ như thế nào. Nếu $a$ thay đổi một chút thì $c$ sẽ thay đổi ra sao? Ta gọi đó là *đạo hàm riêng* của c theo a.
- Các đạo hàm riêng trên đồ thị có thể được tính đơn giản như sau:
$$ \frac{\partial}{\partial{a}} (a+b) = \frac{\partial a}{\partial a} + \frac{\partial b}{\partial a} = 1
$$
$$
\frac{\partial}{\partial u} uv = u \frac{\partial v}{\partial u} + v \frac{\partial u}{\partial u} = v
$$
- Các đạo hàm trên mỗi cạnh đc thể hiện trên đồ thị dưới đây:
![[Pasted image 20250325162933.png]]
- Ví dụ ta muốn biết nút $e$ bị ảnh hưởng như thế nào bởi $a$. Nếu ta thay đổi $a$ 1 đơn vị thì, $c$ cũng thay đổi 1 đơn vị, và nếu $c$ thay đổi 1 đơn vị thì $e$ bị thay đổi 2 đơn vị. Vì vậy, $e$ thay đổi $1*2$ đơn vị theo sự thay đổi của $a$.
- Quy tắc chung là lấy tổng tất cả các đường từ một nút tới nút khác và nhân với đạo hàm trên mỗi cạnh tương ứng. Ví dụ để tính đạo hàm của $e$ theo $b$, ta có:
$$
\frac {\partial e}{\partial b} = 1*2+1*3
$$
- Điều này có nghĩa rằng $b$ ảnh hưởng thế nào đến $e$ thông qua $c$ (tích: $\frac{\partial e}{\partial c} \frac{\partial c}{\partial b}$) và $d$ (tích: $\frac{\partial e}{\partial d} \frac{\partial d}{\partial b}$)
### Chain forward and Chain backward
![[Pasted image 20250325164431.png]]

![[Pasted image 20250325164444.png]]
- Đạo hàm tiến theo dõi môt nút đầu vào ảnh hưởng tới tất cả các nút ra sao, còn đạo hàm ngược thể hiện tất cả các nút ảnh hưởng tới 1 nút đầu vào thế nào. Nói cách khác đạo hàm tiến áp dụng phép toán $\frac{\partial}{\partial X}$ cho tất cả các nút, còn đạo hàm ngược áp dụng phép toán $\frac{\partial}{\partial Z}$ cho tất cả các nút.
- **NOTE**: Đạo hàm tiến cho ta đạo hàm của đầu ra theo một đầu vào, nhưng đạo hàm ngược cho ta tất cả theo đầu vào luôn.
- Khi huấn luyện một mạng nơ-ron nhân tạo (NN - Neural Network), ta cần tối ưu hóa nó sao cho hoạt động hiệu quả nhất. Để làm được điều này, ta cần một chỉ số để đánh giá hiệu suất của mạng, gọi là **hàm chi phí (cost function)**.
- Hàm chi phí là một hàm phụ thuộc vào các tham số (weights và biases) của mạng nơ-ron. Mục tiêu của quá trình huấn luyện là **giảm giá trị của hàm chi phí**, tức là làm cho mạng dự đoán tốt hơn.
- Để tối ưu hóa, ta cần **tính đạo hàm của hàm chi phí** theo các tham số của mạng. Điều này giúp ta biết cần điều chỉnh tham số theo hướng nào để giảm chi phí. Phương pháp **gradient descent** được sử dụng để cập nhật tham số bằng cách dịch chuyển chúng theo hướng giảm nhanh nhất của hàm chi phí.
- Tuy nhiên, vì số lượng tham số của một mạng NN có thể rất lớn (hàng triệu hoặc hàng chục triệu), việc tính toán tất cả các đạo hàm này một cách trực tiếp sẽ rất tốn thời gian. Để giải quyết vấn đề này, ta sử dụng **thuật toán lan truyền ngược (backpropagation) hay là đạo hàm ngược**.
- Backpropagation giúp ta **tính toán đạo hàm hiệu quả hơn**, bằng cách sử dụng quy tắc chuỗi để truyền lỗi từ đầu ra ngược trở lại các lớp trước đó. Điều này giúp cập nhật trọng số nhanh hơn và tối ưu mạng một cách hiệu quả hơn.
# References
