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
## Image Caption Generation with Attention

### Tổng quan

**Image Captioning** là bài toán:
> Input: một hình ảnh  
> Output: một chuỗi từ mô tả nội dung ảnh

Ví dụ:
-  Hình ảnh: con chim đang bay trên mặt nước  
- Caption sinh ra: `"A bird flying over a body of water"`

### Pipeline tổng quát (Slide 2)

1. **Input Image**: ảnh đầu vào.
2. **Convolutional Feature Extraction**:
   - Dùng CNN (VD: Inception, ResNet) để chia ảnh thành nhiều vùng (regions) → mỗi vùng là 1 vector đặc trưng.
   - Ví dụ: ảnh → `14×14 = 196` vectors (feature map).
3. **RNN with Attention**:
   - Dùng LSTM để sinh từ từng bước.
   - Mỗi bước, attention sẽ quyết định nên "nhìn" vùng ảnh nào.
4. **Caption Generation**:
   - Sinh từng từ, ví dụ:
     - `"A"` → `"bird"` → `"flying"` → `"over"` → `"a"` → `"body"` → `"of"` → `"water"`

### Cơ chế Attention (Slide 1)

Giống như Attention trong NLP nhưng thay vì từ → mô hình chú ý vào **vùng ảnh**.

#### Diễn giải:

- Mỗi vùng ảnh sau CNN có vector đặc trưng:  
  `h¹, h², ..., h⁴` (VD: 4 vùng ảnh tương ứng với 4 ký tự Hán trong ví dụ `"機器學習"`)

- Khi LSTM đang sinh từ `"learning"`:
  - Nó tính attention scores $\alpha^i_1$ giữa $h_t^{dec}$ và từng $h^i$
  - Softmax chuẩn hóa:  
    - $\tilde{\alpha}_1^1 = 0.0$,  
    - $\tilde{\alpha}_1^2 = 0.0$,  
    - $\tilde{\alpha}_1^3 = 0.5$,  
    - $\tilde{\alpha}_1^4 = 0.5$

- Tính context vector:
  - $c^1 = \sum_i \tilde{\alpha}_1^i h^i = 0.5 h^3 + 0.5 h^4$

- Context vector $c^1$ được đưa vào RNN để sinh ra từ `"learning"`

---

## 🧠 Học được "chim là bird" như thế nào?

> ❓ Làm sao mô hình biết hình con chim thì caption nên là `"bird"`?

- Không được lập trình sẵn!
- Mô hình học từ **dữ liệu huấn luyện**:
  - Mỗi ảnh có 5 caption thật (con người viết)
  - Qua huấn luyện:
    - Khi vector đặc trưng giống chim → mô hình học rằng `"bird"` thường được sinh ra
    - Attention học được vùng ảnh liên quan đến từ cụ thể
- Toàn bộ được tối ưu qua **backpropagation**, tối thiểu hóa loss giữa caption dự đoán và caption thật

---

## 🖼️ Slide 3 – Attention đúng chỗ

Một số ví dụ trong bài báo "Show, Attend and Tell":

| Caption                              | Attention nhìn vào…                      |
|--------------------------------------|------------------------------------------|
| A woman is throwing a frisbee       | tay và vật thể bay                       |
| A stop sign on a road               | biển báo đỏ                              |
| A giraffe standing in a forest      | vùng chứa hươu cao cổ                    |
| A group of people sitting in a boat | vùng có người và thuyền                  |
| A little girl is blowing a bubble   | mặt và bong bóng                         |

➡️ Attention giúp caption không bị mơ hồ — chọn đúng vùng ảnh tại đúng thời điểm sinh từ.

---

## ✍️ Tổng kết kỹ thuật

| Thành phần      | Vai trò |
|-----------------|--------|
| **CNN**         | Chia ảnh thành nhiều vùng, mỗi vùng thành vector đặc trưng |
| **Attention**   | Ở mỗi bước sinh từ, tính softmax score giữa decoder state và từng vùng ảnh |
| **Context Vector** | Tổng trọng số các vùng ảnh → truyền vào RNN |
| **RNN (LSTM)**  | Sinh từng từ dựa vào context + từ trước đó |
| **Loss**        | So sánh caption dự đoán với ground truth → backpropagation |

---

## 📌 Công thức chính

- **Attention Score**:
  - $\text{score}_i = v^\top \tanh(W_1 h_t^{dec} + W_2 h_i^{enc})$
- **Softmax Attention Weights**:
  - $\alpha_i = \text{softmax}(\text{score}_i)$
- **Context Vector**:
  - $c_t = \sum_i \alpha_i \cdot h_i^{enc}$
- **Output Word**:
  - $\hat{y}_t = \text{softmax}(W_o [h_t^{dec}; c_t] + b_o)$

---

## 🧠 Ghi nhớ

> "Attention giúp mô hình không nhìn toàn ảnh một cách mù quáng — mà chọn đúng vùng để sinh đúng từ."

---

## 📚 Tài liệu tham khảo

**Show, Attend and Tell: Neural Image Caption Generation with Visual Attention**  
Kelvin Xu et al., ICML 2015  
https://arxiv.org/abs/1502.03044


# References
