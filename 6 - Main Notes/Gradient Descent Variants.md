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

# References
