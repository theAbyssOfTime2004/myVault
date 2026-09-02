

# Nền tảng

- Khi train model, data đi qua 2 giai đoạn nền tảng: 
	- Forward pass
	- Backward pass
- Để lan truyền ngược, Pytorch sẽ cache các con số tính toán ở forward để sang backword tìm đạo hàm được 1 cách tối ưu đỡ tốn kém, làm bằng cách xây dựng ***Computational Graph*** 

# Vấn đề tích lũy Gradient

![[Pasted image 20260903000650.png]]

- mỗi khi gọi `loss.backward()` pytorch không ghi đè gradient mới mà sẽ cộng dồn, vấn đề để giải quyết bài toán thiếu VRAM:
	- ví dụ muốn `batch_size = 64` nhưng VRAM nhỏ, chỉ vừa `batch_size = 16`:
	- Chạy batch 1 (size 16) $\rightarrow$ gọi `loss.backward()` (lưu gradient 1).
	- Chạy batch 2 (size 16) $\rightarrow$ gọi `loss.backward()` (gradient tự cộng dồn vào gradient 1).
	- Chạy batch 3, batch 4 $\rightarrow$ cộng dồn tiếp.
	- Đủ 4 lần (tổng cộng 64 mẫu) $\rightarrow$ mới gọi `optimizer.step()` để cập nhật trọng số 1 lần duy nhất