2025-04-21 11:54


Tags: [[data scientist]], [[beginner]], [[DeepLearning]], [[Machine Learning]]

# Vanishing and Exploding Gradient

#### **Vanishing/Exploding Gradients là gì?**
Là hiện tượng:
- **Vanishing**: Gradient trở nên **rất nhỏ** → mô hình **học chậm hoặc không học được**.
- **Exploding**: Gradient trở nên **rất lớn** → mô hình **không ổn định**, dễ "exploding".

![[Pasted image 20250421115533.png]]
- Xét mạng neural đơn giản không có bias và activation như ảnh trên với 2 đầu vào (`x₁`, `x₂`) → nhiều lớp ẩn → đầu ra `ŷ`.
- với `ŷ` được tính theo công thức forward propagation như sau:
$$\hat{y} = W^{[L]} W^{[L-1]} \cdots W^{[1]} x$$
với:
	- $x$ là vector inputs 
	- $W^{[l]}$ là ma trận weights của tầng $l$ trong mạng
- Lưu ý rằng trong công thức trên ảnh nên có activation function cho mỗi layer (được viết ở dưới nhưng không viết tường minh trên công thức), chính là $a^{[l]} = g(z^{[l]})$ với $g()$ chính là activation function
- Ví dụ nếu mỗi $W = 1.5$ thì $\hat{y} \approx (1.5)^L x$ => rất lớn, khiến cho gradient bị exploding
- Ngược lại nếu $W = 0.5$ thì gradient sẽ rất nhỏ, giảm theo cấp số nhân và tiến về 0
# References
