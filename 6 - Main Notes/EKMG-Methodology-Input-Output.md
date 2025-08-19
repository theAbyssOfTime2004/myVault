# Multimodal Aspect-Based Sentiment Analysis with External Knowledge and Multi‑granularity Image‑Text Features (EKMG)

## TL;DR
Bài toán: cho **một câu + một ảnh**, mô hình phải tìm **các khía cạnh (aspect terms)** xuất hiện trong câu và **cảm xúc** tương ứng (positive/neutral/negative) cho từng khía cạnh. EKMG làm ba việc chính: (1) mã hoá văn bản và ảnh, đồng thời bổ sung **tri thức ngoài** (AMR cho văn bản, tags cho ảnh); (2) **nâng cao/“lọc nhiễu” ngữ nghĩa** bằng hai nhánh tăng cường dựa trên tri thức; (3) **căn chỉnh đa mức hạt** giữa từ/cụm từ và vùng ảnh bằng đồ thị + GAT và học tương phản, sau đó **BART decoder** sinh chuỗi (aspect, polarity).


### 3 thách thức chính mà paper đặt ra:
1. **Bắt trúng “thông tin quan trọng” trong cả text lẫn image**
    - _Vì sao khó:_ Câu có thể chứa nhiều sắc thái (phủ định, đối lập “but…”, mỉa mai), nhiều từ không liên quan; ảnh cũng nhiều chi tiết thừa. Nếu không lọc, mô hình sẽ chú ý nhầm.        
    - _EKMG làm gì:_ Kéo **external knowledge** để “làm sạch nghĩa” — **AMR** cho văn bản, **image tags** cho ảnh; rồi dùng **mạng tăng cường ngữ nghĩa** (gating/attention) để **giữ phần liên quan** (nhất là danh từ/cụm danh từ – thường là aspect) và **lọc nhiễu** trước khi đem đi căn chỉnh.
2. **Căn chỉnh chữ–hình ở nhiều “mức hạt” (multi-granularity)**    
    - _Vì sao khó:_ Text có các cấp **từ -> cụm từ -> câu**, còn ảnh có **vùng nhỏ -> toàn ảnh**. Ví dụ “staff” phải khớp với vùng nhân viên (fine), còn “environment” cần bối cảnh toàn cảnh (coarse).        
    - _EKMG làm gì:_ Xây **đồ thị dị thể đa góc nhìn** gồm nút **word/phrase/region**, cạnh từ **attention word↔region** và **quan hệ cú pháp**; chạy **GAT** để thông tin chảy đúng giữa các mức, rồi **hợp nhất** đặc trưng fine + coarse thành một biểu diễn chung.
3. **Thu hẹp “khoảng cách ngữ nghĩa” giữa hai modality khi trộn (fusion)**
    -  _Vì sao khó:_ Cùng một ý “không hài lòng về chỗ ngồi ngoài trời” nhưng text là ký hiệu ngôn ngữ, ảnh là tín hiệu thị giác — hai không gian rất khác nhau, trộn thẳng tay dễ lệch nghĩa.
    - _EKMG làm gì:_ Dùng **cross-modal fusion có trọng số theo granularity** (chọn tỉ lệ đóng góp của fine/coarse) và thêm **học tương phản ảnh-văn bản** (đúng cặp kéo gần, sai cặp đẩy xa) để hai modality nằm **gần nhau** trong không gian biểu diễn trước khi **BART decoder** sinh (aspect, polarity).

Tóm lại: *(1)* lọc–làm giàu nghĩa để bắt đúng manh mối, *(2)* nối đúng phần chữ–hình ở từng cấp độ, *(3)* trộn hai modality một cách “ăn rơ” bằng fusion + contrastive learning.

```
1. **Đồ thị dị thể (heterogeneous graph) trong MGCM**
    
    - **Nút** nhiều loại:
        
        - Text: **word**, **phrase**, (và có thể **sentence**).
            
        - Image: **region** (đối tượng/vùng) và **full-image** (toàn ảnh).
            
    - **Cạnh** nhiều “góc nhìn” (multi-view):
        
        - **Text–text**: dependency, constituent (từ↔từ, cụm↔từ).
            
        - **Text–image**: liên hệ **word/phrase ↔ region** (từ attention/correlation).
            
        - **Fine–coarse**: liên kết **region ↔ full-image**, **word/phrase ↔ sentence**.
            
2. **GAT làm gì?**
    
    - Không chỉ “đánh trọng số” mà là **truyền tin có trọng số học được** giữa các nút.
        
    - Mỗi nút iii “nghe” hàng xóm jjj với **trọng số chú ý** αij\alpha_{ij}αij​ (học từ dữ liệu), rồi **tổng hợp** lại để cập nhật biểu diễn của iii.
        
    - Nhờ vậy, cạnh **liên quan** (ví dụ _“staff” ↔ vùng có nhân viên_) sẽ có **trọng số cao**, còn cạnh nhiễu (ví dụ _“staff” ↔ bụi cây_) sẽ **thấp**.
        
    - GAT đặc biệt hợp với **multi-granularity** vì nó cho phép **trao đổi thông tin giữa fine và coarse** (word/phrase/sentence ↔ region/full-image) theo **mức độ quan trọng** học được.
        
3. **Ví dụ “staff” (fine) vs “environment” (coarse)**
    
    - _“staff”_ là **aspect cục bộ** → cần nhìn **vùng ảnh nhỏ** nơi có nhân viên; GAT sẽ đẩy trọng số vào cạnh _word “staff” ↔ region nhân viên_.
        
    - _“environment”_ là **aspect tổng quát** → cần **bối cảnh toàn ảnh** (ánh sáng, bố cục, sạch/đồ đạc) nên cạnh _phrase “environment” ↔ full-image_ sẽ nặng ký hơn.
        
4. **Sau GAT thì gì nữa?**
    
    - Bạn thu được biểu diễn **đã căn chỉnh** giữa các mức fine–coarse và giữa hai kênh **text–image**.
        
    - Tiếp theo là **cross-modal fusion** (hợp nhất có trọng số giữa các mức hạt) để “trộn hai modality cho ăn rơ”, rồi thêm **contrastive learning** (đúng cặp kéo gần, sai cặp đẩy xa) trước khi đưa vào **decoder** sinh _(aspect, polarity)_.
        

Tóm câu ngắn: **Đồ thị dị thể** mô hình hóa đủ loại nút/cạnh (text↔image, fine↔coarse); **GAT** học trọng số chú ý trên các cạnh để **kết nối đúng chỗ, đúng mức chi tiết**; cuối cùng **fusion** + **contrastive** giúp hai modality hòa chung một không gian biểu diễn, phục vụ dự đoán chính xác hơn.
```



## Methodology Overview (EKMG)
EKMG gồm 3 khối lớn, tạo thành một pipeline:

1) **Multimodal Encoding + External Knowledge**  
2) **EKSM – External Knowledge Semantic Enhancement**   
3) **MGCM – Multi‑Granularity Cross‑Modal Alignment + Contrastive Learning** 

### 1. Multimodal Encoding + External Knowledge 
- **Đầu vào**: câu **S**, ảnh **V**, **đồ thị AMR** của S ($G_{amr})$, **image tags** của V ($V_{tag}$).
- **Đầu ra**: Bộ đặc trưng $(H_{cv}, H_s, H_v, H_{noun}, H_{amr}, H_{tag})$
#### a) Image encoder (ảnh):
- Sẽ lấy được đặc trưng toàn cục - *coarse* - biểu diễn toàn ảnh, và đặc trưng cục bộ *fine-grained* để biểu diễn các vùng nhỏ (mà có confidence cao nhất), ta sẽ được $H_{cv}$ nắm bối cảnh toàn ảnh (coarse), còn Ev giữ chi tiết theo vùng/đối tượng (fine).
#### b)  Text - Image encoder (văn bản + projecting các vủng ảnh vào cùng không gian)
- Từ phần `a) Image encoder`, ta được các embedding của các vùng ảnh (gọi là các token ảnh), sau đó projecting chúng vào cùng không gian với các văn bản, dùng các tag `<img>, <BOS>, <EOS>` để đánh dấu vị trí của ảnh và chuỗi/văn bản:
- $$ E_{vs} = <img> + E_v + <img> +  <bos> + E_s + <bos> $$
	- Với $E_v$ là danh sách embedding của 36 vùng ảnh, $E_s$ là embedding của câu thu được từ **BART**   
- Sau đó cho $E_{vs}$ đi qua **BART**, ta được $H_{vs} = [H_v, H_s]$, với:
	- $H_v:$ **đặc trưng vùng ảnh (fine image features)** nhưng đã được đặt trong không gian chữ (mỗi vùng ảnh tương ứng một token ảnh)
	- $H_s$: **đặc trưng văn bản** theo chiều dài câu 
- **Nhấn mạnh danh từ (Noun Mask):**
	- Vì **aspect** thường là danh từ/cụm danh từ, encoder tạo mask danh từ trên $H_s$ rồi lấy: $H_{\text{noun}} = H_s \otimes \text{Mask}_{\text{noun}}$
	=> Để mô hình tập trung hơn vào các vị trí có khả năng là aspect 

- Việc **chèn token ảnh cạnh token chữ** giúp self-attention của BART **nhìn xuyên suốt** ảnh↔chữ, nhờ đó **căn chỉnh** các vùng ảnh với từ/cụm từ **ngay từ encoder** (đưa chúng “về cùng ngôn ngữ” trước khi sang các bước GAT/fusion).

``` css
<img> [region_1] [region_2] ... [region_36] <img> <bos> t_1 t_2 ... t_n <eos>
```





























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
