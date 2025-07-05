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
---

## Tổng quan kiến trúc và pipeline cụ thể của **seq2seq with 2-layer stacked encoder + attention**

| Thành phần       | Mô tả                                                                 |
|------------------|----------------------------------------------------------------------|
| **Encoder**      | 2-layer stacked LSTM                                                 |
| **Decoder**      | 2-layer stacked LSTM, khởi tạo từ final hidden + cell states của encoder |
| **Attention**    | Tính giữa decoder hidden state hiện tại $h_t^{dec}$ và toàn bộ encoder hidden states $h_i^{enc}$ |
| **Output step**  | Ghép context vector $c_t$ + decoder output $h_t^{dec}$ → đưa qua feed-forward layer để sinh từ |

### 1. Encoder: 2-layer stacked LSTM

- Mỗi từ đầu vào $x_t$ được xử lý qua **2 tầng LSTM liên tiếp**:

  - LSTM layer 1: $x_t \rightarrow h_t^{(1)}$
  - LSTM layer 2: $h_t^{(1)} \rightarrow h_t^{(2)}$

- Tầng trên nhận hidden state từ tầng dưới tại cùng timestep.
- Tầng cuối của encoder trả về:
  - Hidden state cuối cùng: $h_T^{(2)}$
  - Cell state cuối cùng: $c_T^{(2)}$

➡️ Sử dụng $h_T^{(2)}$ và $c_T^{(2)}$ để **khởi tạo decoder**.


### 2. Decoder: 2-layer stacked LSTM

- Cũng gồm **2 tầng như encoder**.
- Khởi tạo từ:
  - Hidden states: $h_0^{dec} = h_T^{(2)}$
  - Cell states: $c_0^{dec} = c_T^{(2)}$

- Tại mỗi timestep $t$:
  - Nhận embedding từ từ trước: $x_t$
  - Tính hidden state: $h_t^{dec} = \text{LSTM}(x_t, h_{t-1}^{dec}, c_{t-1}^{dec})$
  - Tính context vector $c_t$ từ attention

### 3. Attention Score Functions được dùng

### Mục tiêu:
Tính điểm attention score giữa $h_t^{dec}$ và từng $h_i^{enc}$ để biết nên tập trung vào phần nào của đầu vào.

| Tên hàm           | Công thức                                                        | Ghi chú              |
|-------------------|------------------------------------------------------------------|----------------------|
| **Additive**      | $\text{score}_i = v^\top \tanh(W_1 h_t^{dec} + W_2 h_i^{enc})$   | Bahdanau (concat)    |
| **Dot Product**   | $\text{score}_i = h_t^{dec} \cdot h_i^{enc}$                     | Luong                |
| **General**       | $\text{score}_i = h_t^{dec^\top} W h_i^{enc}$                    | Luong (general)      |
| **Location-based**| $\text{score}_i = W h_t^{dec}$ (không dùng $h_i^{enc}$)         | Dựa trên vị trí      |

Sau đó:

- Chuẩn hóa scores bằng softmax:
  - $\alpha_i = \text{softmax}(\text{score}_i)$
- Tính context vector:
  - $c_t = \sum_i \alpha_i \cdot h_i^{enc}$


### 4. Sinh từ tiếp theo

- Ghép context vector và decoder hidden state:
  - $o_t = [h_t^{dec} ; c_t]$
- Đưa qua feedforward layer + softmax:
  - $\hat{y}_t = \text{softmax}(W_o o_t + b_o)$

- Nếu đang **training**:
  - Sử dụng ground truth $y_{t-1}$ làm input tiếp theo (teacher forcing)

- Nếu đang **inference**:
  - Lấy từ có xác suất cao nhất từ $\hat{y}_t$ làm input tiếp theo


### Ghi chú

- $h_t^{dec}$: decoder hidden state tại thời điểm $t$
- $h_i^{enc}$: encoder hidden state tại thời điểm $i$
- $c_t$: context vector tại thời điểm $t$
- $\alpha_i$: attention weight tại vị trí $i$
- $o_t$: vector tổng hợp từ decoder + attention
- $\hat{y}_t$: xác suất phân phối từ vựng ở bước $t$

---
# Image Captioning with Attention – Full Summary


## Mục tiêu bài toán

**Input**: Một bức ảnh  
**Output**: Một chuỗi từ mô tả bức ảnh (caption) Ví dụ:

- Ảnh: chim đang bay trên mặt nước
- Caption: "A bird flying over a body of water"


## Ý tưởng cốt lõi

Image captioning là một bài toán cross-domain giữa:

- NLP (chuỗi từ)
- Computer Vision (hình ảnh) Mô hình học cách "dịch" từ ảnh sang ngôn ngữ tự nhiên.


## Pipeline tổng quát

### 1. Input image

- Một bức ảnh kích thước tùy ý.

### 2. CNN trích đặc trưng

- Dùng CNN (VD: Inception, ResNet) để biến ảnh thành tập các vùng (regions).
- Ví dụ: $$14 \times 14 = 196$$ vùng, mỗi vùng là một vector $$h_i$$

### 3. Attention + Decoder (RNN/LSTM)

Tại mỗi bước sinh từ:

- Tính attention scores giữa hidden state hiện tại $$h_t^{dec}$$ và từng $$h_i$$
- Dùng softmax để chuẩn hóa → trọng số $$\alpha_i$$
- Tính context vector:  
    $$c_t = \sum_i \alpha_i h_i$$
- Dùng $$c_t$$ để sinh từ tiếp theo qua RNN

### 4. Caption generation

- Bắt đầu từ token `<START>`
- Sinh từng từ cho đến khi gặp `<END>` hoặc đạt độ dài tối đa

## Công thức quan trọng

- **Attention score (additive)**: $$\text{score}_i = v^\top \tanh(W_1 h_t^{dec} + W_2 h_i)$$
- **Softmax attention weight**: $$\alpha_i = \frac{\exp(\text{score}_i)}{\sum_j \exp(\text{score}_j)}$$
- **Context vector**: $$c_t = \sum_i \alpha_i h_i$$
- **Dự đoán từ tiếp theo**: $$\hat{y}_t = \text{softmax}(W_o [h_t^{dec}; c_t] + b_o)$$


## Attention hoạt động như thế nào?

Tại mỗi bước sinh từ:

- Mô hình sẽ "nhìn vào" vùng ảnh quan trọng thông qua attention Ví dụ:
- Khi sinh từ `"bird"` → attention tập trung vào vùng có chim
- Khi sinh từ `"water"` → attention chuyển sang vùng có mặt nước


## Làm sao mô hình biết "bird" là chim?

Câu hỏi: **Mô hình có được dạy trước rằng "chim là bird" không?**  
→ Không! Thay vào đó, mô hình học từ dữ liệu gồm nhiều ảnh và caption:

- Từ ảnh → CNN trích đặc trưng thành các vector vùng
- Khi những ảnh có chim luôn đi kèm caption chứa từ `"bird"`  
    → Mô hình học được mối liên hệ giữa vùng ảnh và từ mô tả Toàn bộ quá trình này được tối ưu hóa thông qua hàm mất mát (loss) và lan truyền ngược (backpropagation).


## Ví dụ Attention từ bài báo _Show, Attend and Tell_

|Caption|Attention nhìn vào vùng|
|---|---|
|A stop sign on a road|Biển báo đỏ|
|A giraffe standing in a forest|Con hươu cao cổ|
|A little girl blowing a bubble|Mặt và bong bóng|
|A group of people on a boat|Người và thuyền|


## Slide minh họa

### Slide 1: Attention trên vùng ảnh

- Mỗi vùng ảnh là một vector $$h_i$$
- Ví dụ context vector:  
    $$c_1 = 0.5 \cdot h_3 + 0.5 \cdot h_4$$
- Dùng để sinh từ `"learning"`

### Slide 2: Pipeline tổng quát

- Ảnh → CNN → vectors
- Vectors → Attention
- Decoder → sinh từ theo từng bước

### Slide 3: Ví dụ attention

- Hiển thị rõ mô hình "nhìn" vào đúng vùng ảnh khi sinh từ tương ứng trong caption


## Kết luận

Attention chính là chìa khóa giúp mô hình Image Captioning:

- Không còn cần phải nén toàn ảnh thành 1 vector cố định
- Thay vào đó, mô hình có thể "tập trung" vào từng vùng ảnh khác nhau theo từng thời điểm sinh từ
- Nhờ đó caption chính xác và tự nhiên hơn, gần với cách con người mô tả ảnh

---

# References
