2025-04-07 22:28


Tags: [[DeepLearning]], [[Convolutional Neural Networks]], [[Machine Learning]]

# CNN review

- Cách tính ma trận đầu ra
![[Pasted image 20250407223608.png]]
- Ước lượng ma trận đầu ra, ví dụ xét 1 mạng neuron tích chập, có ảnh input 28x28 với filter 7x7:
	- Với ảnh 28×28, filter 7×7, không padding, stride = 1:
		- Filter có thể di chuyển từ vị trí 0 đến vị trí 21 theo chiều ngang (tổng 22 vị trí)
		- Filter có thể di chuyển từ vị trí 0 đến vị trí 21 theo chiều dọc (tổng 22 vị trí)
		- Ma trận đầu ra: 22×22
	- Với ảnh 28×28, filter 7×7, padding = 1, stride = 1:
		- Ảnh sau padding: 30×30
		- Filter có thể di chuyển từ vị trí 0 đến vị trí 23 theo chiều ngang (tổng 24 vị trí)
		- Filter có thể di chuyển từ vị trí 0 đến vị trí 23 theo chiều dọc (tổng 24 vị trí)
		- Ma trận đầu ra: 24×24
- Output_size = [(Input_size + 2 × Padding - Filter_size) / Stride] + 1
# References
