

ta biết rằng Quantization ban đầu chỉ đơn giản là tìm 1 scale factor rồi lấy toàn bộ giá trị số thực trong dãy giá trị chia cho scale factor để được 1 dãy số nguyên rời rạc (vì đơn giản là số nguyên cần ít bit để biểu diễn -> ít bytes để chứa hơn -> giảm bộ nhớ -> tăng tốc độ), tuy nhiên ta không thể naive mà đem toàn bộ dãy số thực chia cho scale factor được 


Các kỹ thuật Quantization hiện đại (AWQ, GPTQ, SmoothQuant, GGUF) phải giải quyết **3 vấn đề gai góc** sau:

### 1. Outlier Problem

Trong các mô hình Transformer lớn (từ 6B tham số trở lên), có một hiện tượng kỳ lạ: $99.9\%$ các số có giá trị rất nhỏ (khoảng $-1$ đến $+1$), nhưng thỉnh thoảng lại xuất hiện vài outiers vọt lên tới $+100$ hoặc $-100$ 

- Nếu bạn scale ngây thơ:
    
    $$\text{scale} = \frac{100}{127} \approx 0.787$$
    
- Hậu quả: $99.9\%$ các con số nằm trong khoảng $[-1, 1]$ khi chia cho $0.787$ sẽ chỉ ra các giá trị lẻ như $0.2, -0.4, 0.8...$ Khi qua hàm `round()`, **toàn bộ $99.9\%$ dữ liệu bị trimmed về $-1, 0, 1$**. Toàn bộ cấu trúc tinh vi của mô hình bị phá hủy.

### 2. Granularity

Thay vì dùng 1 con số `scale` cho cả ma trận hàng triệu phần tử, người ta chia nhỏ ra:

- **Per-channel / Per-row:** Mỗi hàng hoặc mỗi cột trong ma trận trọng số có một cây thước `scale` riêng.
- **Group-wise (Block-wise):** Chia ma trận thành từng khối nhỏ (ví dụ cứ 128 số thì gộp thành 1 nhóm và tính 1 `scale` riêng). Cách này cô lập các số ngoại lai, không để một con số cực đoan làm hỏng độ mịn của các số lân cận.

### 3. Smarter Rounding

Làm tròn thông thường (`round(x)`) nhìn từng số riêng lẻ. Nhưng các phương pháp hiện đại làm thông minh hơn nhiều:

- **GPTQ (Second-Order Optimization):** Khi làm tròn một trọng số (gây ra một sai số $\Delta$), thuật toán lập tức điều chỉnh nhẹ các trọng số còn lại chưa làm tròn xung quanh nó để bù đắp lại tổng sai số của cả tầng.
- **AWQ (Activation-aware Weight Quantization):** Nó nhận ra rằng không phải trọng số nào cũng quan trọng như nhau. Trọng số nào kích hoạt các đặc trưng lớn trong dữ liệu thì giữ nguyên độ chính xác hoặc nhân hệ số bảo vệ, chỉ ép mạnh những trọng số ít quan trọng.