2025-03-24 15:16


Tags: [[DeepLearning]], [[data scientist]], [[NLP]], [[Neural Networks]]

# Recurrent Neural Networks (RNN)

- Mạng hồi quy (RNN) có thể có đầu vào là nhiều input khác nhau 
- Cũng như các mô hình neural networks khác, RNN cũng có các *trọng số*, các *lớp*,  các *biases* và *activation functions*.
- Khác biệt lớn là RNN có *feedback loops*
![[Pasted image 20250324151952.png]]
![[Pasted image 20250324152356.png]]
- giả sử ta có bài toán dự đoán giá trị cổ phiếu tại 1 nơi có tên là StatLand và hình trên là các quy luật cổ phiếu đơn giản
![[Pasted image 20250324152520.png]]
- Giả sử ta đang cố gắng dự đoán giá trị cổ phiếu vào ngày thứ 2 và cổ phiếu đang đi theo quy luật như hình trên, ở phần *Feedback loop* ta sẽ được tổng như hình là $(Today \times w_1)+(y_1 \times w_2)$, nghĩa là *feedback loop* giúp ta tính toán sự ảnh hưởng của giá trị  **hôm qua** và cả **hôm nay** vào dự đoán của ngày **ngày mai**
![[Pasted image 20250324153349.png]]
- Giống như ta đang thực hiện 2 mô hình neural networks với 2 đầu vào là **hôm qua** và **hôm nay** 
![[Pasted image 20250324154010.png]]
- Một vấn đề của RNN là, khi ta càng *unroll (mở rộng)* mô hình thì ta càng khó để train nó, vấn đề này có tên là **Vanishing Gradient/Exploding Gradient Problem** 
 ![[image.png]]
- Khi huấn luyện RNN bằng [[Backpropagation]], ta cần lan truyền các gradient (đạo hàm theo hướng) của từng parameter để minimizing hàm loss bằng [[Gradient Descent]], và khi gradient được lan truyền ngược qua nhiều bước, nếu $W_2$ < 1 thì gradient sẽ dần về 0 khi số bước tăng lên và gradient quá nhỏ sẽ khiến mô hình học rất chậm hoặc gần như không học được và đó được gọi là **Vanishing Gradient**, ngược lại thì nếu $W_2 > 1$ thì gradient sẽ tăng rất nhanh và tiệm cận vô cùng do đó sẽ khiến mô hình học không ổn định, không hội tụ trong quá trình gradient descent và khiến việc training trở nên khó khăn, được gọi là **Exploding Gradient**.
- Cách khắc phục có thể dùng LSTM hoặc GRU
- Dùng activation function là ReLU thay vì sigmoid hoặc tanh
# References
