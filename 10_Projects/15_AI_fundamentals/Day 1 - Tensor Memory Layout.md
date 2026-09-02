


# Cấu tạo cốt lõi của 1 Tensor



một `torch.Tensor` gồm 2 phần là ***Storage*** và ***Metadata***
1. Storage:
	- là mảng 1D lưu giá trị liên tục trên RAM, không biết hay có thông tin gì về dim, row, col của ma trận 
2. Metadata:
	- chứa thông tin mô tả cách biểu diễn mảng 1D kia:
		- **Shape:** Kích thước các chiều (ví dụ: `[2, 3]`).
		-  **Stride:** Số bước nhảy trong Storage để đi tiếp 1 đơn vị theo từng chiều (ví dụ: `(3, 1)`).
		- **Offset:** Vị trí bắt đầu đọc trong Storage.
	    - **Dtype & Device:** Kiểu dữ liệu (`int32`, `float32`) và thiết bị (`cpu`, `cuda`).



x = torch.tensor([[1, 2, 3],

[4, 5, 6]], dtype=torch.int32)

thì x mặc định là row-major và trong pytorch thì nó contiguous, tuy nhiên khi dùng phép transpose vào x: 

t = x.t() 

thì nó sẽ thành non-contiguous 

tuy nhiên cách các phần tử của tensor t được sắp xếp trong ram không khác gì x, nó chỉ đổi stride để khi in ra, nó là chuyển vị của x? 
và gọi view trên t thì sẽ xảy ra lỗi vì t là non-contagious

và ý chính là, cái giúp xác định 1 tensor là contiguous hay non contiguous là dựa vào STRIDE của nó, nếu với stride đó mà cách đọc trên ram là theo hàng -> contiguous, không theo hàng mà nhảy lung tung -> non-contiguous


khi dùng method .contiguous() thì pytorch sẽ cấp phát 1 vùng mới trong ram, rồi đem cái tensor mà đang non contiguous đấy quăng vào theo thứ tự theo hàng để nó trở thành contiguous

.view() tạo 1 bộ metadata khác để xem tensor theo cách khác, xài được cho contiguous

.reshape() cũng là tạo 1 bộ metadata khác để xem tensor theo cách khác, xài được co cả contiguous và non contiguous, với non contiguous thì đơn giản là .contiguou() rồi .view()

tương tự thay cho .t() thì .permute() cũng sẽ tạo ra một non-contiguous tensor 

các method này hoạt động trên metadata chứ không phải storage, vì việc thay đổi quy tắc đọc/xem thì nhanh hơn thay đổi chính bản thân dữ liệu

## Pitching script: 

**Problem:** Operations like `transpose()` or `permute()` are zero-copy in PyTorch; they change the tensor's `stride` metadata without reallocating physical memory, making the tensor **non-contiguous** (the logical row-major order no longer matches the 1D physical memory layout).

**Mechanism:** When a tensor is non-contiguous, calling `.view()` fails because it requires contiguous memory to safely reinterpret shapes without copying. Calling `.contiguous()` explicitly allocates a new memory buffer and rearranges elements sequentially so that the last dimension has a stride of 1.

**Trade-off:** Zero-copy transforms are $O(1)$ and instant, but downstream operators requiring contiguous memory will force a `.contiguous()` call, which incurs memory allocation and copy overhead ($O(N)$).