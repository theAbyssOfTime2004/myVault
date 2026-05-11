2025-03-25 12:23


Tags: [[Neural Networks]], [[Deep Learning]], [[Common Activation Function In Neural Networks]]

# Tại sao các activation function phải là các hàm phi tuyến?
Nếu mạng nơ-ron **chỉ thực hiện phép biến đổi tuyến tính**, thì nó **không mạnh hơn một mô hình hồi quy tuyến tính đơn giản**. Điều này có nghĩa là:
1. **Không thể học được quan hệ phức tạp**
    - Ví dụ: Nếu bạn muốn phân loại điểm trên một mặt phẳng thành hai nhóm có dạng hình tròn (như phân biệt điểm trong và ngoài một vòng tròn), mô hình tuyến tính sẽ **không thể tách hai nhóm này bằng một đường thẳng**.
    - Một mạng nơ-ron chỉ chứa phép toán tuyến tính vẫn **chỉ có thể học được các đường phân tách tuyến tính**, giống như hồi quy logistic đơn giản.
2. **Nhiều lớp tuyến tính chồng lên nhau không tạo ra điều gì mới**
    - Giả sử ta có hai lớp trong mạng nơ-ron:
$$
\begin{aligned}
\mathbf{h} &= \mathbf{W}_1 \mathbf{x} \\
\mathbf{y} &= \mathbf{W}_2 \mathbf{h}
\end{aligned}
$$

 - Kết hợp lại, ta có:
        $$\mathbf{y} = \mathbf{W}_2 (\mathbf{W}_1 \mathbf{x}) = (\mathbf{W}_2 \mathbf{W}_1) \mathbf{x}$$
- Vì tích hai ma trận vẫn là một ma trận, toàn bộ mạng chỉ tương đương với **một lớp tuyến tính duy nhất**. Dù có thêm bao nhiêu lớp, nó vẫn chỉ là một phép biến đổi tuyến tính đơn giản.
➡ **Nói cách khác, nếu không có hàm kích hoạt phi tuyến, một mạng nơ-ron nhiều lớp cũng chỉ giống như một lớp duy nhất**, và như vậy thì nó không mạnh hơn mô hình tuyến tính thông thường.

### Ví dụ trực quan

Hãy tưởng tượng bạn có một cánh cửa và muốn đi từ phòng này sang phòng khác
- Nếu cửa **chỉ mở theo đường thẳng**, bạn chỉ có thể đi theo một hướng cố định.
- Nhưng nếu cửa **có bản lề xoay tự do (phi tuyến)**, bạn có thể đi theo nhiều hướng khác nhau, giúp bạn đến được nhiều nơi hơn.
Tương tự, nếu mạng nơ-ron chỉ có phép toán tuyến tính, nó bị **giới hạn trong việc học các quan hệ tuyến tính**. Nhưng nếu có hàm kích hoạt phi tuyến, nó có thể học được các **mối quan hệ phức tạp** hơn, giúp xử lý các bài toán khó hơn, như nhận diện ảnh hoặc xử lý ngôn ngữ tự nhiên.
# References
