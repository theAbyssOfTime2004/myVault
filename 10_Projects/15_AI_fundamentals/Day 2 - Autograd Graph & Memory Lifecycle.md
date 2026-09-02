

# Nền tảng

- Khi train model, data đi qua 2 giai đoạn nền tảng: 
	- Forward pass
	- Backward pass
- Để lan truyền ngược, Pytorch sẽ cache các con số tính toán ở forward để sang backword tìm đạo hàm được 1 cách tối ưu đỡ tốn kém, làm bằng cách xây dựng ***Computational Graph*** 

# Vấn đề tích lũy Gradient

![[Pasted image 20260903000650.png]]

