2025-03-18 21:37


Tags:[[Machine Learning]], [[beginner]], [[Gradient Descent in Linear Regression]]

# Gradient Descent Variants

- There are three variants of gradient descent
	- **Batch** gradient descent
	- **Stochastic** gradient descent
	- **Mini-batch** gradient descent
![[Pasted image 20250318222744.png]]

### Iteration vs. Epoch
- 1 *Iteration* = when a *batch of data* samples is fed to the model for training
- 1 *epoch* = when the *entire dataset* is fed to the model for training
![[Pasted image 20250318223214.png]]
$=>$ 1 *epoch gồm nhiều iteration*, số lượng iteration phụ thuộc vào batch size (là số mẫu dữ liệu được xử lý trong mỗi epoch)
- dựa vào hình:
	- training set gồm $N$ mẫu dữ liệu.
	- Nếu **batch size** = 2, mỗi batch chứa 2 mẫu dữ liệu.
	- Vì toàn bộ tập dữ liệu có $N$ mẫu, số iteration trong 1 epoch là: $$\frac{N}{\text{batch size}} = \frac{N}2$$
- Ví dụ với một dataset có 1024 datasamples và batch size = 64 thì ta sẽ có 1 epoch = 1024/64 = 16 iterations
### Batch Gradient Descent
![[Pasted image 20250320164833.png]]
- Batch Gradient Descent dùng toàn bộ dữ liệu trên tập dữ liệu để tính gradient 
- **Ưu điểm**: 
	- *Cập nhật chính xác*: Việc sử dụng toàn bộ dataset, sẽ giúp tính gradient chính xác hơn do đó giúp ước lượng hướng tối ưu được chính xác hơn
	- *Hội tụ dễ dàng hơn*: các lần cập nhật trọng số sẽ ổn định hơn và do đó giúp tiến về minimum dễ dàng hơn
- **Nhược điểm**:
	- *Chậm đối với các dataset lớn*: bởi vì yêu cầu phải sử dụng toàn bộ dataset trong mỗi traning iteration, do đó dẫn đến thời gian training rất lâu đối với dữ liệu lớn
	- *Yêu cầu bộ nhớ cao*: là 1 thử thách khó khăn đối với các dataset lớn
### Stochastic gradient descent
![[Pasted image 20250320170245.png]]

- Stochastic gradient descent sử dụng *từng mẫu dữ liệu riêng lẻ* để tính gradient
- Cập nhật lại trọng số $\theta_j$ ngay lập tức sau mỗi lần tính gradient
- **Ưu điểm**:
	- *Nhanh*: chỉ xử lý duy nhất 1 điểm dữ liệu tại 1 thời điểm, nên việc xử lý là rất nhanh đối với kể cả các dataset lớn
	- *Ít đặt nặng bộ nhớ*: chỉ cần store 1 điểm dữ liệu duy nhất trong bộ nhớ tại 1 thời điểm.
	- *Có thể thoát khỏi local minima*: Nhiễu trong từng điểm dữ liệu đơn lẻ đôi khi có thể giúp thoát khỏi local minima
		- Do nhiễu từ SGD, thuật toán không luôn luôn đi theo hướng dốc xuống một cách hoàn toàn chính xác và đôi khi điều này giúp cho SGD có thể thoát khỏi các điểm local minima "nông" và tìm kiếm các điểm thấp hơn
- **Nhược điểm**:
	- *Noisy Updates*: Các update từ chỉ 1 điểm dữ liệu duy nhất thì noisy hơn cả dataset do đó dẫn đến hội tụ không mượt mà và dễ xảy ra dao động (oscillations) quanh điểm cực tiểu
	- *Hội tụ kém ổn định*: Do sự biến động lớn trong mỗi lần cập nhật, SGD có thể không ổn định bằng Batch GD, nếu không điều chỉnh *learning rate* hợp lý sẽ dễ bị kẹt trong các local minima xấu hoặc dao động xung quanh minimum mà không hội tụ
### Mini-batch gradient descent
![[Pasted image 20250320172337.png]]
- Sử dụng một **subset of the data** (mini-batch) để tính gradient. Mini-batch size k là một tham số ta có thể tune cho mô hình 
![[Pasted image 20250320172638.png]]
- Làm sao để chọn ra được số `batch_size` hợp lý?
![[Pasted image 20250320172757.png]]

### Model hyper-parameters
- In machine learning, a hyperparameter is essentially a control knob you **adjust before training** a model. It determines the learning process itself, rather than being learned from the data.
![[Pasted image 20250320173029.png]]
### Learning rate:
- Là một siêu tham số (hyperparameter). 
# References
