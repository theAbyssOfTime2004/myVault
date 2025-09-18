2025-07-06 01:10


Tags: [[NLP]], [[DeepLearning]], [[Neural Networks]]

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
## Image Captioning with Attention – Full Summary


### Mục tiêu bài toán

**Input**: Một bức ảnh  
**Output**: Một chuỗi từ mô tả bức ảnh (caption) Ví dụ:

- Ảnh: chim đang bay trên mặt nước
- Caption: "A bird flying over a body of water"


### Ý tưởng cốt lõi

Image captioning là một bài toán cross-domain giữa:

- NLP (chuỗi từ)
- Computer Vision (hình ảnh) Mô hình học cách "dịch" từ ảnh sang ngôn ngữ tự nhiên.


### Pipeline tổng quát

#### 1. Input image

- Một bức ảnh kích thước tùy ý.

#### 2. CNN trích đặc trưng

- Dùng CNN (VD: Inception, ResNet) để biến ảnh thành tập các vùng (regions).
- Ví dụ: $$14 \times 14 = 196$$ vùng, mỗi vùng là một vector $$h_i$$
#### 3. Attention + Decoder (RNN/LSTM)

Tại mỗi bước sinh từ:

- Tính attention scores giữa hidden state hiện tại $$h_t^{dec}$$ và từng $$h_i$$
- Dùng softmax để chuẩn hóa → trọng số $$\alpha_i$$
- Tính context vector:  
    $$c_t = \sum_i \alpha_i h_i$$
- Dùng $$c_t$$ để sinh từ tiếp theo qua RNN

#### 4. Caption generation

- Bắt đầu từ token `<START>`
- Sinh từng từ cho đến khi gặp `<END>` hoặc đạt độ dài tối đa

### Công thức quan trọng

- **Attention score (additive)**: $$\text{score}_i = v^\top \tanh(W_1 h_t^{dec} + W_2 h_i)$$
- **Softmax attention weight**: $$\alpha_i = \frac{\exp(\text{score}_i)}{\sum_j \exp(\text{score}_j)}$$
- **Context vector**: $$c_t = \sum_i \alpha_i h_i$$
- **Dự đoán từ tiếp theo**: $$\hat{y}_t = \text{softmax}(W_o [h_t^{dec}; c_t] + b_o)$$


### Attention hoạt động như thế nào?

Tại mỗi bước sinh từ:

- Mô hình sẽ "nhìn vào" vùng ảnh quan trọng thông qua attention Ví dụ:
- Khi sinh từ `"bird"` → attention tập trung vào vùng có chim
- Khi sinh từ `"water"` → attention chuyển sang vùng có mặt nước


### Làm sao mô hình biết "bird" là chim?

Câu hỏi: **Mô hình có được dạy trước rằng "chim là bird" không?**  
→ Không! Thay vào đó, mô hình học từ dữ liệu gồm nhiều ảnh và caption:

- Từ ảnh → CNN trích đặc trưng thành các vector vùng
- Khi những ảnh có chim luôn đi kèm caption chứa từ `"bird"`  
    → Mô hình học được mối liên hệ giữa vùng ảnh và từ mô tả Toàn bộ quá trình này được tối ưu hóa thông qua hàm mất mát (loss) và lan truyền ngược (backpropagation).


### Ví dụ Attention từ bài báo _Show, Attend and Tell_

|Caption|Attention nhìn vào vùng|
|---|---|
|A stop sign on a road|Biển báo đỏ|
|A giraffe standing in a forest|Con hươu cao cổ|
|A little girl blowing a bubble|Mặt và bong bóng|
|A group of people on a boat|Người và thuyền|


### Slide minh họa

#### Slide 1: Attention trên vùng ảnh

- Mỗi vùng ảnh là một vector $$h_i$$
- Ví dụ context vector:  
    $$c_1 = 0.5 \cdot h_3 + 0.5 \cdot h_4$$
- Dùng để sinh từ `"learning"`

#### Slide 2: Pipeline tổng quát

- Ảnh → CNN → vectors
- Vectors → Attention
- Decoder → sinh từ theo từng bước

#### Slide 3: Ví dụ attention

- Hiển thị rõ mô hình "nhìn" vào đúng vùng ảnh khi sinh từ tương ứng trong caption


### Kết luận

Attention chính là chìa khóa giúp mô hình Image Captioning:

- Không còn cần phải nén toàn ảnh thành 1 vector cố định
- Thay vào đó, mô hình có thể "tập trung" vào từng vùng ảnh khác nhau theo từng thời điểm sinh từ
- Nhờ đó caption chính xác và tự nhiên hơn, gần với cách con người mô tả ảnh

---

## Self-Attention Pipeline (trên từng token)

### Mục tiêu

Tạo biểu diễn mới có ngữ cảnh cho mỗi token bằng cách cho nó "nhìn" các token khác trong chuỗi.

### Bước 1: Chuẩn bị input và tạo Query, Key, Value

Input là các vector embedding, có shape `[seq_len, d_model]`. Mỗi token được ánh xạ thành ba vector:

- **Query** = Input × W_Q (shape: [d_k])
- **Key** = Input × W_K (shape: [d_k])
- **Value** = Input × W_V (shape: [d_v])

W_Q, W_K, W_V là ma trận trọng số có thể học được (learnable parameters). Key và Query phải có cùng shape (để dot product được), còn Value có thể khác.

#### Ví dụ (Input #1):

- Input vector: `[1, 0, 1, 0]`
- Query = `[1, 0, 2]`
- Key = `[0, 1, 1]`
- Value = `[1, 2, 3]`

### Bước 2: Tính Attention Scores

Với mỗi token đang xét (Input #1), tính dot product giữa query của nó và tất cả các key (kể cả của chính nó):

$$\text{score} = \text{dot}(\text{query}_{\text{input1}}, \text{key}_j)$$

#### Ví dụ:

Query của Input #1 là `[1, 0, 2]`

Các key:

- Input #1: `[0, 1, 1]`
- Input #2: `[4, 4, 0]`
- Input #3: `[2, 3, 1]`

Tính tích vô hướng:

$$[1,0,2] \cdot [0,1,1] = 1 \times 0 + 0 \times 1 + 2 \times 1 = 2$$

$$[1,0,2] \cdot [4,4,0] = 1 \times 4 + 0 \times 4 + 2 \times 0 = 4$$

$$[1,0,2] \cdot [2,3,1] = 1 \times 2 + 0 \times 3 + 2 \times 1 = 4$$

→ Attention scores = `[2, 4, 4]`

### Bước 3: Chuẩn hóa Attention Scores bằng Softmax

Dùng softmax để biến các attention scores thành xác suất (trọng số attention):

$$\text{softmax}([2, 4, 4]) = [0.0, 0.5, 0.5]$$

→ Điều này cho thấy Input #1 chủ yếu chú ý vào Input #2 và Input #3.

### Bước 4: Tính Weighted Sum của các Value

Lấy từng value vector nhân với trọng số tương ứng và cộng lại:

#### Các value tương ứng:

- Input #1: `[1, 2, 3]`
- Input #2: `[2, 8, 0]`
- Input #3: `[2, 6, 3]`

#### Weighted sum:

$$\text{output} = 0.0 \times [1, 2, 3] + 0.5 \times [2, 8, 0] + 0.5 \times [2, 6, 3]$$

$$= [0, 0, 0] + [1, 4, 0] + [1, 3, 1.5] = [2.0, 7.0, 1.5]$$

→ Đây là **embedding đầu ra mới của Input #1**, sau khi đã "chú ý" đến toàn bộ chuỗi, tiếp theo hãy lặp lại việc tính toán cho các Input #2 và #3

### Kết quả

Output của mỗi token là một vector mới có ngữ cảnh, tổng hợp từ các value khác theo trọng số attention. Quá trình được lặp lại cho từng token trong chuỗi.

### Ghi chú quan trọng

- Query và Key phải có cùng chiều để thực hiện dot product
- Value có thể có chiều khác; chiều của đầu ra sẽ bằng chiều của Value
- Output là embedding "mới" của token, đã được cập nhật bằng thông tin từ các token khác

### Công thức tổng quát

$$\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V$$

Trong đó:

- Q: Ma trận queries [seq_len, d_k]
- K: Ma trận keys [seq_len, d_k]
- V: Ma trận values [seq_len, d_v]
- $$\sqrt{d_k}$$: Hệ số scaled để tránh gradient vanishing

### Ý nghĩa trực quan

Self-attention cho phép mỗi token "hỏi" (query) tất cả các token khác trong chuỗi để tìm hiểu ngữ cảnh. Token nào có "chìa khóa" (key) phù hợp với câu hỏi sẽ được chú ý nhiều hơn, và "giá trị" (value) của chúng sẽ được kết hợp để tạo ra biểu diễn mới cho token đang xét.

Trong ví dụ trên, Input #1 gần như bỏ qua chính nó (weight = 0.0) và tập trung vào Input #2 và #3 (mỗi cái weight = 0.5), tạo ra một embedding mới phản ánh thông tin từ cả hai token này.

---

## Multi-Head Self-Attention

### Khái niệm cơ bản

**Multi-head self-attention** là thành phần cốt lõi trong **Transformer Network**. Nó có cấu trúc gồm một block self-attention, trong đó chứa **nhiều attention heads** chạy **song song**.

### Cấu trúc và hoạt động

#### Input chung cho tất cả heads

**Tất cả các heads nhận cùng một input**: tức là cùng 1 tập các vector embedding ban đầu của các token (làm `query`, `key`, `value`).

#### Điểm khác biệt quan trọng

**Điểm khác biệt nằm ở trọng số**: mỗi head sử dụng **bộ trọng số riêng biệt** $$W_Q^{(i)}, W_K^{(i)}, W_V^{(i)}$$, nên tạo ra các `Q`, `K`, `V` khác nhau → dẫn đến **cách tính attention khác nhau**.

#### Công thức cho mỗi head

Đối với head thứ i:

$$Q^{(i)} = X \cdot W_Q^{(i)}$$ $$K^{(i)} = X \cdot W_K^{(i)}$$ $$V^{(i)} = X \cdot W_V^{(i)}$$

$$\text{head}_i = \text{Attention}(Q^{(i)}, K^{(i)}, V^{(i)}) = \text{softmax}\left(\frac{Q^{(i)}K^{(i)T}}{\sqrt{d_k}}\right)V^{(i)}$$

### Ý nghĩa và lợi ích

#### Học nhiều góc nhìn khác nhau

**Mỗi head học được một góc nhìn khác nhau** về mối quan hệ giữa các token trong chuỗi:

- **Head 1**: Tập trung vào ngữ pháp (subject-verb, noun-adjective)
- **Head 2**: Học đồng tham chiếu (pronoun resolution)
- **Head 3**: Chú ý đến vị trí tương đối của các từ
- **Head 4**: Nắm bắt logic và quan hệ nhân quả
- **Head 5**: Phân tích cảm xúc và tone
- **Head 6**: Hiểu ngữ cảnh và domain-specific knowledge

#### Tăng khả năng biểu diễn

Thay vì chỉ có một cách nhìn duy nhất, multi-head attention cho phép mô hình:

- Nắm bắt **nhiều loại quan hệ** cùng lúc
- Học **các pattern phức tạp** mà single-head không thể học được
- Tăng **khả năng tổng quát hóa** cho nhiều tác vụ khác nhau

### Tổng hợp output

Các output từ tất cả các heads sẽ được **nối lại (concatenate)** và **tổng hợp** thành biểu diễn đầu ra cuối cùng:

$$\text{MultiHead}(Q, K, V) = \text{Concat}(\text{head}_1, \text{head}_2, ..., \text{head}_h) \cdot W_O$$

Trong đó:

- $$h$$: số lượng heads
- $$W_O$$: ma trận trọng số để project concatenated output về chiều mong muốn

### Ví dụ minh họa

#### Giả sử có 3 heads cho câu "The cat sat on the mat"

**Head 1 (Syntax)**: Tập trung vào quan hệ chủ-vị

- "cat" → "sat" (high attention)
- "mat" → "on" (high attention)

**Head 2 (Coreference)**: Học đồng tham chiếu

- "cat" → "the" (moderate attention)
- "mat" → "the" (moderate attention)

**Head 3 (Position)**: Chú ý đến vị trí

- "sat" → "on" (high attention)
- "on" → "mat" (high attention)

#### Kết quả cuối cùng

Concatenate tất cả outputs từ 3 heads và project qua $W_O$ để có biểu diễn cuối cùng chứa đựng thông tin từ cả 3 góc nhìn.

---
## Transformer Architecture
### Encoder and Decoder 
- Encoding component là *Stack của N encoders*. Các encoder có structure giống nhau nhưng weights thì khác nhau. Đầu ra của encoder thứ $i$ là đầu vào của encoder thứ $i+1$
-  Edcoding component cũng là *Stack của N decoders*. Cũng tương tự như encoder, các decoder có structure giống nhau nhưng weights khác nhau

### 1. Từ → Vector
- Mỗi token (ví dụ `"I"`) được gán một **vector embedding** có chiều $d_{\text{model}}$​, thường là 512 hoặc 768.
- Vector này được lấy từ một **bảng tra cứu** (`Embedding matrix`) và được **học trong quá trình huấn luyện**.
- Vector 512 chiều này **không mô tả nghĩa cụ thể từng số**, mà tổng thể nó **mã hóa mối quan hệ ngữ nghĩa của từ đó với các từ khác** trong corpus.
###  2. Positional Encoding

- Vì Transformer không có cấu trúc tuần tự như RNN, nên cần **thêm positional encoding** vào embedding.
- Positional Encoding giúp mô hình **phân biệt vị trí các từ trong câu**.
### 3. Multi-head Attention

- Thay vì chỉ có 1 attention head, ta có **nhiều head chạy song song** (ví dụ: 8 heads).
- Tất cả các head dùng **cùng 1 input**, nhưng **trọng số Q/K/V khác nhau** (khởi tạo khác, học khác).
- Mỗi head học được **kiểu quan hệ ngữ nghĩa khác nhau** → giúp mô hình hiểu ngữ cảnh tốt hơn.
- Kết quả từ các head được **nối lại (concatenate)** và đưa qua một lớp tuyến tính chung để feed-forward layer hiểu được.
![[Pasted image 20250707004950.png]]

### 4. Các Mask trong Attention

| Mask loại gì             | Dùng ở đâu               | Để làm gì                                 |
| ------------------------ | ------------------------ | ----------------------------------------- |
| Padding mask             | Encoder + Decoder        | Bỏ qua `[PAD]` token (không có ý nghĩa)   |
| Causal (look-ahead) mask | Decoder (self-attention) | Không cho nhìn về “tương lai” khi sinh từ |
### 5. Residual Connections
- Giúp mô hình **giữ lại thông tin gốc** của đầu vào $X$ qua mỗi layer.
- Tránh tình trạng thông tin bị **làm mờ hoặc biến mất** do nhiều phép biến đổi liên tiếp (self-attention, FFN).
- **Mỗi encoder block gồm 2 sublayers:**
	1. *Multi-head self-attention*
	2. *Feed-forward network (FFN)*
	=> Mỗi sublayer **đều được bọc bởi một residual connection và LayerNorm**.
### 6. Feed Forward Network
- Là một **mạng con (sub-layer)** nằm sau lớp **Multi-head self-attention** trong mỗi encoder.****
- FFN là một **mạng gồm 2 lớp fully connected (linear layers)** và một hàm kích hoạt **ReLU** ở giữa.
#### Công thức:
$$FFN(x) = \max(0, xW_1 + b_1)W_2 + b_2 $$

- $x$: đầu vào của FFN (mỗi token đã qua attention)
    
- $W_1, b_1$​: trọng số và bias của lớp ẩn
- $W_2, b_2$​: trọng số và bias của lớp output
- $\max(0, \cdot)$: chính là **hàm ReLU**
#### Tóm lại: 
- Trong mỗi encoder layer, sau khi các token đã "nhìn nhau" qua self-attention, thì **mỗi token lại được xử lý riêng biệt bởi một FFN để học thêm biểu diễn ngữ nghĩa mạnh hơn.**
---
# References
