2025-12-15 09:57


Tags: [[Deep Learning]], [[Machine Learning]], [[Gradient Descent]]

# FGSM

- FGSM viết tắt của Fast Gradient Sign Method, là 1 phương pháp tạo *adversarial noise*, thường được dùng để kiểm tra độ nhạy của deep learning model với nhiễu rất nhỏ
- FGSM không thêm random noise mà thêm nhiễu có hướng dựa trên gradient của loss, nhiễu này đánh vào điểm yếu của model 
### Cách hoạt động:

### Bước 1 – Có một loss function

Ví dụ:

- Classifier: cross-entropy
- CLIP: cosine similarity loss
- Diffusion (indirect): embedding alignment loss

### Bước 2 – Tính gradient của loss theo ảnh

$\nabla_x L(x, y)$

Gradient này trả lời:

> “Nếu tôi tăng từng pixel một chút, loss sẽ tăng hay giảm?”

### Bước 3 – Lấy **dấu** của gradient

FGSM không quan tâm độ lớn chính xác, chỉ quan tâm:

- Pixel này nên tăng hay giảm?

$sign(\nabla_x L(x, y))$


### Bước 4 – Cộng nhiễu nhỏ theo hướng đó

$x_{adv} = x + \epsilon \cdot sign(\nabla_x L(x, y))$

- `ε` (epsilon): rất nhỏ (ví dụ 1/255)
- Với mắt người: ảnh gần như không đổi
- Với model: **loss tăng mạnh**

# References
