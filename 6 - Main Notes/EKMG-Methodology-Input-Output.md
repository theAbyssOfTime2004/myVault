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


## Methodology Overview (EKMG)
EKMG gồm 3 khối lớn, tạo thành một pipeline:

1) **Multimodal Encoding + External Knowledge**  
2) **External Knowledge Enhanced Semantic Extraction**   
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

### c) External Knowledge encoder
- Có nhiệm vụ lấy thêm *external knowledge* cho text và image, cụ thể là: 
	- **AMR graph** của câu (đồ thị nghĩa trừu tượng)
	- **Image tags** của ảnh (nhãn từ ImageNet)
	=> Rồi mã hóa cả 2 vào cùng không gian biểu diễn với text bằng **BART**, thu được 2 knowledge tensor: $H_{amr}$ và $H_{tag}$ 
![[Pasted image 20250819094205.png]]


- Cụ thể hơn: 
	- Với đồ thị **AMR**: Nút = **concept/entity/event/attribute**, cạnh = **quan hệ ngữ nghĩa** 
	- BART mã hóa $G_{amr}$ -> $H_{amr}$ (số nút $l_{amr}$ = tổng số **concept/entity/event/attribute** trong câu)
	- Với **Image tags**: Dùng **ResNet - 101** suy ra **10 tags** từ bộ **ImageNet** cho mỗi ảnh
	- Bart mã hóa dãy tags -> $H_{tag}$
- Nói dễ hiểu: External Knowledge encoder cung cấp **2 nguồn tri thức** — AMR cho **text** và tags cho **image** — được **BART** đưa vào **cùng chuẩn biểu diễn**. Các bước tiếp theo dùng chúng để **lọc nhiễu** và **làm đậm ý nghĩa** trước khi căn chỉnh đa mức và hợp nhất cross-modal.
 
	
### 2. External Knowledge Enhanced Semantic Extraction

- **Dùng external knowledge** — **AMR** cho text, **image tags** cho ảnh — để **tăng cường/“làm sạch” ngữ nghĩa** rồi **rút ra** biểu diễn đã tăng cường cho **text** và **image**.
- **Đầu vào**: 
	- Text: $H_s$ (đặc trưng câu), $H_{noun}$ (nhấn mạnh danh từ), $H_{amr}$ (AMR đã mã hóa)
	- Image: $H_v$ (đặc trưng vùng ảnh), $H_{tag}$ (tags đã mã hóa), $H_{noun}$. 
-  **A. Text (AMR-guided "semantic purify" + gating)**	 
	- Dùng $H_{noun}$ "purifying" $H_{unit}$ để lấy phần AMR liên quan, rồi gate trộn vào $H_s$:

$$H_{es} = \text{Gate}(H_s, \text{Attn}(H_{noun}, H_{amr}))$$
- **B. Image (tag-guided + heterogeneity resolution + gating)**
	- Dùng $H_{noun}$​ "purifying" $H_{tag}​$, qua khối HR (giảm lệch modality), rồi gate trộn vào $H_v$ ​:
**Ký hiệu:**
- $\text{Attn}(\cdot, \cdot)$: attention để chọn phần tri thức liên quan.
- $\text{HR}(\cdot)$: _heterogeneity resolution_ (đưa tag về không gian hòa hợp với vùng ảnh).
- $\text{Gate}(\cdot, \cdot)$: cổng trộn có kiểm soát (học được).
- **Đầu ra**: 
	- $H_{es}:$ text enhanced
	- $H_{ev}:$ image enhanced 
**Note:** **“Giảm lệch modality”** = làm cho **đặc trưng của hai modality khác nhau** (ở đây là **text** và **image**) **trở nên tương thích** để có thể so khớp, cộng/trộn và suy luận chung.

### 3. MGCM – Multi‑Granularity Cross‑Modal Alignment + Contrastive Learning 

#### MGCM:

- **MGCM làm gì?**  
    - Căn chỉnh **chữ ↔ hình** ở **nhiều mức chi tiết** (fine ↔ coarse), rồi **trộn** chúng thành một biểu diễn chung và dùng **contrastive learning** để kéo hai kênh lại gần nhau.
- **Bước 1 – Nối đúng chỗ (multi-granularity alignment):**  
    - Tạo “mạng liên kết” giữa:
	    - **Text–text**: quan hệ cú pháp (word ↔ word, phrase ↔ word).
	    - **Text–image**: từ/cụm từ ↔ **vùng ảnh** liên quan.
	    - **Fine–coarse**: vùng ↔ **toàn ảnh**, word/phrase ↔ **câu**.  
        - Mục tiêu: có connection cho cả chi tiết và bối cảnh.
- **Bước 2 – Chọn liên kết quan trọng (GAT):**  
    - Dùng **Graph Attention Network** để “truyền tin có trọng số” trên mạng liên kết.  
    Ví dụ: _“staff”_ sẽ nhận nhiều thông tin từ **vùng có nhân viên** (fine); _“environment”_ ưu tiên **toàn ảnh** (coarse).
- **Bước 3 – Trộn fine & coarse (fusion có trọng số):**  
	-     Học một **tỉ lệ pha trộn** giữa **chi tiết vùng** và **bối cảnh toàn ảnh**.  
    - Aspect “tổng quát” (environment) → bối cảnh nặng hơn; aspect “cục bộ” (staff, dish) → chi tiết vùng nặng hơn.
- **Bước 4 – Kéo chữ–hình về cùng không gian (contrastive learning):**  
    - Cặp **đúng** (text–image của cùng mẫu) bị **kéo gần**, cặp **sai** bị **đẩy xa** → giảm “lệch modality”, fusion ổn định hơn.
- **Kết quả:**  
    - Thu được biểu diễn **đã căn chỉnh & hợp nhất** để **decoder** sinh ra các cặp _(aspect, polarity)_ chính xác hơn.

#### Image-Text Contrastive Learning:

- **Mục tiêu:** kéo **biểu diễn ảnh** và **biểu diễn chữ** (của cùng một mẫu) **lại gần**, và đẩy các cặp **không khớp** ra xa → giảm “lệch modality”.    
- **Cách làm:**
    - Từ đặc trưng đã tăng cường/căn chỉnh, lấy **vector ảnh** và **vector text** ở mức toàn cục (sau fusion).
    - Tính **độ tương đồng** (thường cosine), dùng **loss kiểu InfoNCE** với **dương** = cặp cùng mẫu trong batch, **âm** = các mẫu khác trong batch.
    - Có thể tính hai chiều (image→text và text→image) để ổn định hơn.
- **Tác dụng:** làm không gian chung “dễ sống” cho cả hai kênh, giúp fusion và decoder ổn định, giảm sai lệch khi ảnh và chữ diễn đạt khác nhau

#### Prediction (Decoder) & Training Objective"

- **Decoder:** dùng **BART decoder** để **sinh chuỗi** biểu diễn danh sách **(aspect, polarity)**. Họ thêm các **token cảm xúc** như `<POS>/<NEU>/<NEG>`.
- **Training:** **cross-entropy** cho chuỗi sinh + **contrastive loss** ở trên. **Tổng loss**:
  $$L = (1 - \alpha)\,L_{\text{contrastive}} + \alpha\,L_{\text{CE}}. $$
- (α được chọn thực nghiệm; trong bài α ≈ 0.8 cho kết quả tốt.)
- **Suy luận:** decode chuỗi (thường beam search đơn giản), rồi **parse** về danh sách cặp _(aspect, sentiment)_.

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

## Về heterogeneous graph
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
    - Mỗi nút $i$ “nghe” hàng xóm $j$ với **trọng số chú ý** $\alpha_{ij}$​ (học từ dữ liệu), rồi **tổng hợp** lại để cập nhật biểu diễn của $i$.
    - Nhờ vậy, cạnh **liên quan** (ví dụ _“staff” ↔ vùng có nhân viên_) sẽ có **trọng số cao**, còn cạnh nhiễu (ví dụ _“staff” ↔ bụi cây_) sẽ **thấp**.
    - GAT đặc biệt hợp với **multi-granularity** vì nó cho phép **trao đổi thông tin giữa fine và coarse** (word/phrase/sentence ↔ region/full-image) theo **mức độ quan trọng** học được.
3. **Ví dụ “staff” (fine) vs “environment” (coarse)**
    - _“staff”_ là **aspect cục bộ** → cần nhìn **vùng ảnh nhỏ** nơi có nhân viên; GAT sẽ đẩy trọng số vào cạnh _word “staff” ↔ region nhân viên_.
    - _“environment”_ là **aspect tổng quát** → cần **bối cảnh toàn ảnh** (ánh sáng, bố cục, sạch/đồ đạc) nên cạnh _phrase “environment” ↔ full-image_ sẽ nặng ký hơn.
4. **Sau GAT thì gì nữa?**
    - Bạn thu được biểu diễn **đã căn chỉnh** giữa các mức fine–coarse và giữa hai kênh **text–image**.
    - Tiếp theo là **cross-modal fusion** (hợp nhất có trọng số giữa các mức hạt) để “trộn hai modality cho ăn rơ”, rồi thêm **contrastive learning** (đúng cặp kéo gần, sai cặp đẩy xa) trước khi đưa vào **decoder** sinh _(aspect, polarity)_.
Tóm lại: **Đồ thị dị thể** mô hình hóa đủ loại nút/cạnh (text↔image, fine↔coarse); **GAT** học trọng số chú ý trên các cạnh để **kết nối đúng chỗ, đúng mức chi tiết**; cuối cùng **fusion** + **contrastive** giúp hai modality hòa chung một không gian biểu diễn, phục vụ dự đoán chính xác hơn.