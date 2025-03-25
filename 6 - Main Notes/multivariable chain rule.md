2025-03-25 16:14


Tags: [[Backpropagation]], [[data scientist]], [[DeepLearning]], [[beginner]]

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
$$ \ {a+b}
$$

# References
