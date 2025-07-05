2025-07-06 01:10


Tags:

# Attention Mechanism

## Pipeline cụ thể của **Seq2Seq + Attention với encoder BiGRU và decoder GRU**
---
### 1. Input Preprocessing

- Input sentence (e.g., French) → tokenization
- Convert tokens → word embeddings:  
  $x_1, x_2, ..., x_T$

### 2. Encoder (BiGRU)

- Mỗi input token được đưa vào một BiGRU:
  - GRU đọc xuôi → $\overrightarrow{h}_t$
  - GRU đọc ngược → $\overleftarrow{h}_t$
- Ghép lại:
  - $h_t^{enc} = [\overrightarrow{h}_t ; \overleftarrow{h}_t]$
- Dãy encoder hidden states:
  - $H^{enc} = \{h_1^{enc}, h_2^{enc}, ..., h_T^{enc}\}$

### 3. Khởi tạo Decoder

- Lấy hidden state cuối cùng của backward encoder:
  - $h_0^{dec} = \overleftarrow{h}_1$
- (Có thể đưa qua linear layer nếu cần)

### 4. Decoder - bước đầu tiên

- Input: embedding của token `<START>` → $x_0$
- (Tùy chọn): cộng thêm context vector $c_0$ nếu dùng ở bước đầu

- Tính hidden state đầu tiên:
  - $h_1^{dec} = \text{GRU}([x_0 ; c_0], h_0^{dec})$

### 5. Attention (mỗi bước $t$)

1. Tính attention score giữa $h_t^{dec}$ và từng $h_i^{enc}$:  
   - $\text{score}_i = v^\top \tanh(W_1 h_t^{dec} + W_2 h_i^{enc})$ (*concat*)

2. Dùng softmax để chuẩn hóa:  
   - $\alpha_i = \text{softmax}(\text{score}_i)$

1. Tính context vector (weighted sum):  
   - $c_t = \sum_i \alpha_i \cdot h_i^{enc}$

### 6. Dự đoán từ đầu ra

- Ghép $h_t^{dec}$ và $c_t$:  
  - $o_t = [h_t^{dec} ; c_t]$
- Dự đoán từ:
  - $\hat{y}_t = \text{softmax}(W_o o_t + b_o)$

- Nếu **training**:
  - Dùng ground-truth từ trước đó (teacher forcing)
- Nếu **inference**:
  - Lấy từ có xác suất cao nhất → dùng làm input tiếp theo

### 7. Dừng khi

- Sinh ra token `<END>`, hoặc  
- Đạt đến độ dài tối đa



# References
