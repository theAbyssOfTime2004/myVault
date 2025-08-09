# Multimodal Aspect-Based Sentiment Analysis with External Knowledge and Multi‑granularity Image‑Text Features (EKMG)

## TL;DR
Bài toán: cho **một câu + một ảnh**, mô hình phải tìm **các khía cạnh (aspect terms)** xuất hiện trong câu và **cảm xúc** tương ứng (positive/neutral/negative) cho từng khía cạnh. EKMG làm ba việc chính: (1) mã hoá văn bản và ảnh, đồng thời bổ sung **tri thức ngoài** (AMR cho văn bản, tags cho ảnh); (2) **nâng cao/“lọc nhiễu” ngữ nghĩa** bằng hai nhánh tăng cường dựa trên tri thức; (3) **căn chỉnh đa mức hạt** giữa từ/cụm từ và vùng ảnh bằng đồ thị + GAT và học tương phản, sau đó **BART decoder** sinh chuỗi (aspect, polarity).

---

## Problem Setup (Input → Output)
- **Input**: cặp (S, V) gồm **câu văn bản S** và **ảnh V** đi kèm.
- **Output**: mô hình sinh ra **danh sách các aspect** xuất hiện trong S và **nhãn cảm xúc** cho từng aspect. Trong kiến trúc này, output được **linearize** thành một **chuỗi** để **BART decoder** sinh ra, ví dụ:  
  `aspect_1 <POS> ; aspect_2 <NEG> ; ...`

---

## Methodology Overview (EKMG)
EKMG gồm 3 khối lớn, tạo thành một pipeline:

1) **Multimodal Encoding + External Knowledge**  
2) **EKSM – External Knowledge Semantic Enhancement**   
3) **MGCM – Multi‑Granularity Cross‑Modal Alignment + Contrastive Learning** 
Cuối cùng, **BART decoder** sinh chuỗi (aspect, polarity).

### 1) Multimodal Encoding + External Knowledge

**Ảnh**
- **Coarse features**: trích từ backbone CNN (ví dụ ResNet‑101) cho toàn ảnh.
- **Fine‑grained region features**: trích từ **Faster R‑CNN** (các vùng/objects có score cao).

**Văn bản**
- Mã hoá bằng **BART encoder** để lấy **biểu diễn ngữ cảnh hai chiều** cho từng token.
- **Noun mask**: nhấn mạnh vào **danh từ/cụm danh từ** vì phần lớn aspect rơi vào nhóm này.

**Tri thức ngoài**
- **AMR graph** cho văn bản: nắm **quan hệ nghĩa cấp cao** (semantic roles, predicate‑argument…), giúp “sạch” hơn so với phụ thuộc cú pháp thuần tuý.
- **Image tags**: tên đối tượng/cảnh trong ảnh (tự động suy ra) và **mã hoá bằng BART** để đặt trong cùng không gian ngôn ngữ với văn bản.

### 2) EKSM – External Knowledge Semantic Enhancement

**Nhánh văn bản (Text branch)**
- **Semantic Purify Network**:
  - Đưa **AMR** qua **GNN** để gộp thông tin toàn cục.
  - **Attention** giữa **AMR features** và **noun‑focused text features** để **lấy phần liên quan** đến aspect.
  - **Gating/MLP** để **lọc nhiễu** từ AMR và trộn **động** vào đặc trưng văn bản.

**Nhánh ảnh (Image branch)**
- Tính **trọng số tag‑theo‑danh‑từ** (liên hệ giữa tags và noun features).
- **Heterogeneity Resolution Network**: ánh xạ, pooling, và cơ chế **khử lệch modality** giữa tags (ngôn ngữ) và ảnh (thị giác).
- **Gating** để trộn kết quả vào **region features** của ảnh.

**Kết quả của EKSM**: thu được **text features** và **image features** đã **được tăng cường ngữ nghĩa**, có tính liên quan cao hơn đến các khía cạnh tiềm năng.

### 3) MGCM – Multi‑Granularity Cross‑Modal Alignment + Contrastive Learning

**multi-view heterogeneous graph**
- Kết hợp:
  - **Ma trận liên hệ từ ↔ vùng ảnh** (attention hai chiều word→region và region→word).
  - **Đồ thị cú pháp hỗn hợp** ở phía văn bản (kết hợp **dependency tree** ở mức từ và **constituent tree** ở mức cụm/câu).

**Lan truyền và hợp nhất**
- Chạy **graph attention network** qua đồ thị để **trao đổi thông tin** giữa các **mức hạt** (fine ↔ coarse) của văn bản và ảnh.
- **Fuse** sâu với **coarse image features** bằng **cơ chế hợp nhất có trọng số theo granularity** để thu được **biểu diễn ảnh‑văn bản hợp nhất**.

**Mục tiêu học (Loss)**
- **Học tương phản ảnh‑văn bản** để **khép khoảng cách** giữa hai modality.
- **Cross‑entropy** cho tác vụ sinh/nhãn cảm xúc ở decoder.
- Hàm mất tổng quát:  
  $$L = (1 - \alpha)\,L_{\text{contrastive}} + \alpha\,L_{\text{CE}}. $$

### Decoder và Suy luận

- **BART decoder** nhận các đặc trưng đã căn chỉnh/tăng cường để **sinh chuỗi** biểu diễn **(aspect, polarity)**.  
- Đầu ra chuỗi có thể dễ dàng **parse** lại thành danh sách các cặp (aspect, sentiment).

## Datasets và Metrics (Tóm tắt nhanh)

- **Datasets**: Twitter15, Twitter17 (mỗi mẫu gồm **text + image**; một câu có thể có **nhiều aspect**).
- **Metrics**: tuỳ biến thể tác vụ (nhận diện aspect, gán sentiment, chuỗi hợp nhất), dùng **Precision / Recall / F1** (và đôi khi **Accuracy**).

## Intuition – Tại sao EKMG hiệu quả?

1. **Tri thức ngoài làm sạch/ngữ nghĩa hoá**: AMR và tags giúp mô hình bám đúng **thực thể/quan hệ** liên quan đến aspect, hạn chế nhiễu bối cảnh.
2. **Căn chỉnh đa mức hạt**: aspect như “staff” gắn với **vùng ảnh nhỏ**; aspect như “environment” cần **ngữ cảnh rộng** (cụm từ + bố cục ảnh). MGCM trao đổi thông tin ở **nhiều tầng** để phù hợp cả hai.
3. **Học tương phản**: ép **ảnh** và **văn bản** về gần nhau ở mức biểu diễn, khiến decoder sinh chuỗi ổn định và chính xác hơn.

## Ghi chú nhanh về BART encoder (so với BERT encoder)

- Kế thừa BERT và GPT
- **BART encoder** là encoder **hai chiều** kiểu Transformer, **rất gần** với **BERT encoder** về kiến trúc.
- Khác biệt chính ở **mục tiêu tiền huấn luyện**: BART dùng **denoising seq2seq** (phục hồi văn bản bị làm hỏng), nên **ăn khớp tự nhiên** với **decoder sinh chuỗi** cho output dạng linearized của EKMG.
