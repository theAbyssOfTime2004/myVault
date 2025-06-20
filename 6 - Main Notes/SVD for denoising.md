2025-06-20 11:19


Tags:

# SVD for denoising

### Các bước làm: 
- ***Bước 1***: Đọc file âm thành bằng librosa (Đã thực hiện)
	- kết quả mẫu: 
	- ![[Pasted image 20250620112520.png]]
- ***Bước 2***: Biến đổi tín hiệu âm thanh thành ma trận
	- Giải thích: lấy ví dụ với file đầu tiên là `noisy1_SNRdb_0.0_clnsp1.wav`, sau khi đọc ta có được các thông số sampling rate là 16000 và số lượng mẫu là 161058 và do đó file âm thanh này có độ dài khoảng 10s, ta có thể hiểu rằng tín hiệu này có thể biểu diễn bằng 1 mảng 1 chiều `s = [s1,s2,s3,...sL]` với `L = 161058` và s1, `s2 ,s3, ... sL` lần lượt là các giá trị tương ứng cho biên độ của sóng âm tại thời điểm đó
	- Việc biểu diễn tín hiệu âm thanh thành 1 mảng 1D  `s = [s1,s2,s3,...sL]` chính là biểu diễn theo miền thời gian. Bởi vì mỗi giá trị trong mảng là **biên độ của sóng âm tại một thời điểm cụ thể** do đó khi plot mảng `s` ra ta sẽ được 1 đồ thị biên độ - thời gian 
	- vói sampling rate = 16000hz  = 16kHz nghĩa là mỗi giây ta sẽ lấy mẫu 16000 lần, do đó khoảng cách thời gian giữa  2 mẫu liên tiếp (hay khoảng các thời gian giữa $s_{i}$ và $s_{i+1}$ trong mảng `s`) là: $$
\Delta t = \frac{1}{f_s} = \frac{1}{16000} = 0.0000625 \text{ giây} = 62.5 \text{ micro giây}
$$
-  Vậy thì giờ ta đã hiểu rằng tín hiệu âm thanh sẽ được đọc thành 1 mảng 1 chiều có dạng `s = [s1,s2,s3,...sL]` và có thể plot trên 1 miền thời gian, tiếp theo ta sẽ làm cách nào để chuyển đổi nó thành 1 ma trận để có thể sử dụng cho SVD
	- Ta sẽ chuyển tín hiệu 1 chiều này thành 1 ma trận 2 chiều $A \in \mathbb{R}^{M \times N}$, Với:
		- $M$ là số lượng *frame* (số hàng)
		-  $N$ là chiều dài mỗi *frame* (số cột)
		- *H* là overlapping, thông thường = 1/2 độ dài *frame* = $\frac{N}{2}$
	=> Tín hiệu âm thanh 1 chiều `s` được chia thành nhiều *frame* overlapping nhau, xếp thành các hàng trong ma trận `A`. Mỗi hàng có độ dài `N`, các frame cách nhau `H`. Đây là **frame matrix** sẽ dùng cho **SVD**.

- ***Bước 3***: Sử dụng frame matrix vừa chuyển đổi được làm đầu vào cho SVD
	- Mục tiêu là để phân rã ma trận $A \in \mathbb{R}^{M \times N}$ ra thành các thành phần 
# References
