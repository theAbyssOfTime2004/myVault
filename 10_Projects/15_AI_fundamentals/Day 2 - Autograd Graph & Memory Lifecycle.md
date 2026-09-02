

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

Tóm lại: PyTorch thiết kế phép cộng dồn (`+=`) để có thể linh hoạt gom batch khi thiếu VRAM. Nhưng nếu  không cần gom mà quên xóa rác (`zero_grad`), thì sẽ biến tính năng này thành lỗi nặng.

- Huấn luyện bình thường
```python
optimizer.zero_grad()   # 1. Bắt buộc dọn sạch "rác" của batch trước
output = model(inputs)  # 2. Forward
loss = criterion(output, targets)
loss.backward()         # 3. Tính gradient mới
optimizer.step()        # 4. Cập nhật trọng số
```

- theo batch, gradient accumulation:
```python 
# Giả sử cần gom 4 batch nhỏ (16) để thành batch to (64)
for i, (inputs, targets) in enumerate(dataloader):
    output = model(inputs)
    loss = criterion(output, targets) / 4
    loss.backward()     # Tự động += (tích lũy gradient)

    if (i + 1) % 4 == 0:    # Đủ 4 batch nhỏ
        optimizer.step()    # Cập nhật trọng số
        optimizer.zero_grad() # BÂY GIỜ MỚI ĐƯỢC XÓA để chuẩn bị cho chu kỳ 64 tiếp theo!
```


## `torch.no_grad()_` và `model.eval()`

- `torch.no_grad()`: không cache gradient, không dựng computational graph, giải phỏng các biến teung gian, dùng để tiết kiệm VRAM khi inference vì cơ bản trong inference thì không cần học
- `model.eval()`: tắt các lớp mang tính đóng góp cho quá trình học, như dropout, ngoài ra đổi cách hoạt động batchnorm: 
	- BatchNorm **vẫn chạy và biến đổi dữ liệu**, nhưng nó **đóng băng (freeze)** không tính mean/var của batch hiện tại nữa, mà lấy **running mean / running variance tích lũy từ toàn bộ quá trình train** ra dùng

|                      | **torch.no_grad()**                             | **model.eval()**                                                         |
| -------------------- | ----------------------------------------------- | ------------------------------------------------------------------------ |
| **Phạm vi tác động** | Bộ máy tính toán Autograd (Engine)              | Hành vi của từng Layer trong Model                                       |
| **VRAM & Tốc độ**    | **Tiết kiệm VRAM**, chạy nhanh hơn đáng kể      | **Không** trực tiếp tiết kiệm VRAM hay tăng tốc                          |
| **Kết quả dự đoán**  | Cho ra cùng một con số (chỉ là không lưu graph) | Cho ra **kết quả số học khác** (do Dropout = 0, BatchNorm đổi cách tính) |
