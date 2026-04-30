2025-04-09 18:21
Updated: 2026-05-01

Tags: [[data scientist]], [[review]], [[AI engineer]], [[LLM]], [[deep learning]]

# ôn tập - AI Research/Engineer (Fresher/Junior)
### Tổng hợp các câu hỏi phỏng vấn AI Research/Engineer level fresher/junior

> Note: file này tổng hợp từ JD của VinAI, VinBigData, FPT.AI, các repo GitHub (`amitshekhariitbhu/ai-engineering-interview-questions`, `KalyanKS-NLP/LLM-Interview-Questions-and-Answers-Hub`), DataCamp, InterviewBit, và các bài LinkedIn 2026. Trọng tâm: **modern deep learning + Transformer/LLM + practical AI engineering**.

---

## I. Classic ML / Statistics fundamentals

1. ==Explain how F1-score balances precision and recall. When is F1-score preferred over individual metrics?==
	- Precision = $\frac{TP}{TP + FP}$ : trong tổng số dự đoán positive, có bao nhiêu thật sự đúng (mức độ "chính xác" khi model nói "có")
	- Recall = $\frac{TP}{TP + FN}$ : trong tổng số positive thật sự, ta dự đoán đúng được bao nhiêu (độ phủ)
	- F1-score = $2 \times \frac{\text{precision} \times \text{recall}}{\text{precision} + \text{recall}}$
	- F1-score là **trung bình điều hòa (*harmonic mean*)** của precision và recall → nhạy cảm hơn với sự mất cân bằng vì harmonic mean luôn ≤ arithmetic mean và bị "kéo xuống" mạnh khi 1 trong 2 giá trị nhỏ
	- F1 **không cho phép** 1 trong 2 cái quá cao còn cái còn lại quá thấp (trade-off)
	- **Khi nào dùng F1 thay vì precision/recall riêng lẻ:**
		- Khi cần cân bằng cả 2: spam classification, medical diagnosis (vừa không muốn báo nhầm, vừa không muốn bỏ sót)
		- Khi có **class imbalance** mạnh → accuracy không còn ý nghĩa
		- Khi cần 1 metric duy nhất để so sánh nhiều model (model selection)
	- **Mở rộng (junior level):**
		- **F-beta score** = $(1+\beta^2) \times \frac{P \cdot R}{\beta^2 P + R}$  → $\beta > 1$ ưu tiên recall (vd y tế), $\beta < 1$ ưu tiên precision (vd recommendation)
		- **Macro-F1**: tính F1 từng class rồi trung bình → fair với class nhỏ
		- **Micro-F1**: gộp TP/FP/FN toàn bộ rồi tính F1 → bị thống trị bởi class lớn (≈ accuracy với multiclass single-label)
		- **Weighted-F1**: trung bình F1 các class theo support
		- Khi class imbalance cực mạnh (vd fraud 0.1%) → cân nhắc dùng **PR-AUC** thay vì ROC-AUC vì ROC-AUC bị "lừa" bởi True Negatives quá nhiều

2. ==Bias-Variance tradeoff: định nghĩa, cách phát hiện, cách xử lý==
	- **Tổng error** của model có thể decompose: $\text{Error} = \text{Bias}^2 + \text{Variance} + \text{Irreducible Error}$
	- **Bias**: sai lệch do model **giả định quá đơn giản** so với reality → **underfitting**
		- Vd dùng linear regression cho data dạng cong
	- **Variance**: model **quá nhạy với noise** trong training data → **overfitting**
		- Vd decision tree quá sâu, NN quá nhiều tham số trên ít data
	- **Tradeoff**: tăng độ phức tạp → bias ↓ nhưng variance ↑ (và ngược lại). Mục tiêu là sweet spot tối thiểu total error.
	- **Cách phát hiện**:
		- **High bias**: train accuracy thấp + test accuracy thấp (gần nhau, đều tệ)
		- **High variance**: train accuracy cao nhưng test accuracy thấp (gap lớn)
	- **Cách xử lý**:
		- **Bias cao**: thêm features, dùng model phức tạp hơn (deeper NN), giảm regularization, train lâu hơn
		- **Variance cao**: regularization (L1/L2/Dropout), thêm data, data augmentation, early stopping, ensemble (bagging), giảm độ phức tạp model
	- **Lưu ý modern DL**: với neural network rất lớn (overparameterized), có hiện tượng **double descent** - test error giảm, tăng, rồi giảm lại khi tăng độ phức tạp → phá vỡ U-shape cổ điển

3. ==Cho ví dụ về High Variance Data và regularization xử lý như thế nào?==
	- **High Variance Data**: dữ liệu có khoảng sai số rộng và phân tán lớn quanh mean
	- **Ví dụ**:
		- Dữ liệu thời tiết: nhiệt độ biến thiên lớn theo mùa
		- Dữ liệu giá nhà: từ vài trăm triệu đến vài chục tỷ
		- Stock price, click-through rate
	- **Ảnh hưởng đến generalization**:
		- Model khó tìm pattern chung vì noise lớn
		- Dễ overfit nếu để model học hết mọi điểm dữ liệu
	- **Regularization** = thêm "penalty" vào loss để giảm độ phức tạp:
		- **L2 (Ridge)**: $\mathcal{L}_{new} = \mathcal{L} + \lambda \sum w_i^2$ → kéo weights về gần 0 nhưng không bằng 0, smooth, ổn định
		- **L1 (Lasso)**: $\mathcal{L}_{new} = \mathcal{L} + \lambda \sum |w_i|$ → đẩy weights về **đúng 0** → tự động feature selection, sparse model
		- **Elastic Net**: kết hợp L1 + L2
		- **Dropout** (DL): tắt ngẫu nhiên neurons khi train (tỉ lệ p, thường 0.2–0.5) → ép network học redundant representation, hành vi như ensemble
		- **Early stopping**: dừng khi val loss bắt đầu tăng
		- **Data augmentation**: tạo synthetic data (flip ảnh, mixup, cutmix, paraphrase text)
		- **Weight decay** trong AdamW = L2 nhưng decouple khỏi gradient update

4. ==Imbalanced data: tác dụng của cost-sensitive learning trong real-world scenario==
	- **Cost-sensitive learning**: gán trọng số khác nhau cho lỗi ở mỗi class trong loss function
		- Vd binary classification fraud (1%) vs normal (99%): cost của false negative (bỏ sót fraud) >> cost của false positive
		- Loss: $\mathcal{L} = -\sum_i w_{y_i} \log p(y_i | x_i)$ với $w_{minority} \gg w_{majority}$
	- **Tác dụng**:
		- Buộc model "chú ý" đến minority class thay vì optimize accuracy bằng cách luôn predict majority
		- Tránh degenerate solution (predict all 0)
	- **So sánh với các kỹ thuật khác cho imbalanced data**:
		- **Resampling**:
			- *Oversampling minority* (vd random duplicate, **SMOTE** - tạo synthetic samples bằng interpolation k-NN)
			- *Undersampling majority* (mất thông tin, dùng khi data rất lớn)
		- **Threshold tuning**: train bình thường, sau đó chỉnh threshold ở inference (default 0.5 không phải lúc nào cũng tốt)
		- **Anomaly detection**: xem minority như outlier (Isolation Forest, One-class SVM)
		- **Focal Loss** (Lin et al., RetinaNet 2017): $\mathcal{L} = -(1-p_t)^\gamma \log p_t$ → giảm trọng số cho easy examples, tự động focus vào hard/minority cases. Rất phổ biến trong object detection và LLM training.
	- **Lưu ý**: chỉ resample trên train set, KHÔNG resample val/test (vì test phải phản ánh distribution thực tế)

5. ==Stacking vs Bagging vs Boosting==
	- **Bagging** (**B**ootstrap **Agg**regat**ing**): nhiều model **cùng loại** chạy **song song** trên các bootstrap samples khác nhau, kết quả = vote/average
		- *Bootstrap*: lấy ngẫu nhiên có hoàn lại từ training set
			```python
			D = [A, B, C, D, E]
			Bootstrap 1: [B, A, E, A, D]
			Bootstrap 2: [C, D, D, E, B]
			```
		- **Mục đích**: giảm **variance** (trung bình hóa noise giữa các model)
		- **Ví dụ**: Random Forest = Bagging + random feature subsampling tại mỗi split
	- **Boosting**: nhiều weak learners chạy **tuần tự**, model sau học từ lỗi của model trước
		- Khởi tạo trọng số đều cho samples
		- Mỗi iteration: train weak learner, tăng trọng số sample bị sai, giảm trọng số sample đúng
		- Kết quả = weighted sum các weak learners
		- **Mục đích**: giảm **bias** (và một phần variance)
		- **Ví dụ**: AdaBoost, **Gradient Boosting**, **XGBoost**, **LightGBM**, **CatBoost** (production standard cho tabular data)
	- **Stacking**: nhiều **model khác loại** (heterogeneous) → predictions của chúng làm input cho 1 **meta-model** học cách kết hợp tốt nhất
		- Level-0: base models (vd LR, RF, XGB, NN)
		- Level-1: meta-learner (thường dùng simple model như LogReg để tránh overfit)
		- Cần dùng **out-of-fold predictions** khi tạo training data cho meta-model để tránh leakage
		- **Mục đích**: tận dụng strength của nhiều thuật toán khác nhau
	- **Tóm tắt**:

| | Bagging | Boosting | Stacking |
|---|---|---|---|
| Models | Cùng loại | Cùng loại (weak) | Khác loại |
| Training | Song song | Tuần tự | 2 levels |
| Giảm | Variance | Bias (+ Variance) | Cả 2 |
| Risk overfit | Thấp | Trung bình–cao | Cao nếu không CV |
| Ví dụ | Random Forest | XGBoost, LightGBM | Kaggle ensembles |

---

## II. Deep Learning fundamentals

6. ==Tại sao activation function trong neural networks phải là non-linear?==
	- Nếu không có non-linearity, mạng dù bao nhiêu lớp cũng chỉ là 1 phép biến đổi tuyến tính:
		- $y = W_3(W_2(W_1 x + b_1) + b_2) + b_3 = W' x + b'$
	- → 1000 lớp linear cũng tương đương 1 lớp linear duy nhất → không học được hàm phi tuyến (XOR, image recognition, ngôn ngữ,...)
	- **Universal Approximation Theorem**: NN với 1 hidden layer + non-linear activation có thể xấp xỉ bất kỳ continuous function nào (trên compact set) → phép màu là ở **non-linearity**
	- **Các activation phổ biến**:
		- **Sigmoid** $\sigma(x) = \frac{1}{1+e^{-x}}$ : output (0,1), bị **vanishing gradient** khi |x| lớn, không zero-centered → ít dùng cho hidden layers, vẫn dùng cho binary output
		- **Tanh** $\tanh(x)$: output (-1, 1), zero-centered, vẫn vanishing gradient
		- **ReLU** $\max(0, x)$: đơn giản, không vanishing ở phía dương, **dying ReLU** problem (neuron output luôn 0 không update được)
		- **Leaky ReLU / PReLU**: $\max(\alpha x, x)$ với $\alpha$ nhỏ → fix dying ReLU
		- **GELU** $x \cdot \Phi(x)$: smooth ReLU, dùng trong BERT, GPT-2
		- **SwiGLU**: dùng trong **LLaMA, Mistral, modern LLM 2024+** thay cho FFN ReLU truyền thống
		- **Softmax**: cho output multiclass classification (probabilities tổng = 1)

7. ==Vanishing & Exploding Gradient: nguyên nhân và cách fix==
	- **Vanishing gradient**: gradient nhân qua nhiều layer trở nên rất nhỏ → weights ở layer đầu hầu như không update → network học chậm hoặc không học được
	- **Exploding gradient**: gradient quá lớn → weights nhảy vọt → loss = NaN
	- **Nguyên nhân**:
		- Chain rule: $\frac{\partial \mathcal{L}}{\partial w_1} = \prod_{i} \frac{\partial h_{i+1}}{\partial h_i} \cdot \ldots$
		- Activation như sigmoid/tanh có gradient ≤ 0.25 → tích nhiều layer → vanishing
		- RNN trên sequence dài → exponentially vanishing/exploding theo thời gian
		- Weight init xấu, learning rate quá lớn
	- **Cách fix**:
		- **Activation tốt hơn**: ReLU, GELU thay sigmoid/tanh ở hidden layers
		- **Weight initialization**: **Xavier/Glorot** (cho tanh/sigmoid), **He init** (cho ReLU)
		- **Batch/Layer Normalization**: normalize activations
		- **Residual connections (skip connections)**: $y = F(x) + x$ → gradient có "đường tắt" → ResNet, Transformer
		- **Gradient clipping**: cap gradient norm về threshold (vd 1.0) → fix exploding
		- **LSTM/GRU** thay vanilla RNN: gating mechanism giảm vanishing
		- **Lower learning rate** + warmup schedule

8. ==Batch Normalization vs Layer Normalization vs RMSNorm==
	- **Batch Normalization** (Ioffe & Szegedy, 2015):
		- Normalize **trên batch dimension** cho mỗi feature: $\hat{x} = \frac{x - \mu_B}{\sqrt{\sigma_B^2 + \epsilon}}$, sau đó scale + shift bằng learnable params $\gamma, \beta$
		- Train mode: dùng batch statistics. Eval mode: dùng running mean/var (EMA từ training)
		- **Lợi**: cho phép learning rate lớn hơn, giảm internal covariate shift, có effect như regularization nhẹ
		- **Hạn chế**: phụ thuộc batch size (tệ với batch nhỏ), khó dùng cho RNN/Transformer (mỗi token có thể có length khác nhau), train ≠ eval gây bug
	- **Layer Normalization** (Ba et al., 2016):
		- Normalize **trên feature dimension** trong cùng 1 sample: không phụ thuộc batch
		- Phù hợp với RNN, Transformer (sequence length variable)
		- **Standard cho NLP, Transformer architecture**
	- **RMSNorm** (Zhang & Sennrich, 2019):
		- Đơn giản hóa LayerNorm: chỉ scale theo RMS, không trừ mean
		- $\text{RMSNorm}(x) = \frac{x}{\sqrt{\frac{1}{n}\sum x_i^2 + \epsilon}} \cdot \gamma$
		- Nhanh hơn LayerNorm ~10-50%, performance tương đương
		- **Standard cho LLaMA, Mistral, Qwen, modern LLM 2024+**

9. ==Optimizers: SGD vs Momentum vs Adam vs AdamW==
	- **SGD**: $w_{t+1} = w_t - \eta \nabla \mathcal{L}$
		- Đơn giản, generalize tốt, nhưng converge chậm và nhạy với learning rate
	- **SGD + Momentum**: $v_{t+1} = \beta v_t + \nabla \mathcal{L}$, $w_{t+1} = w_t - \eta v_{t+1}$
		- Tích lũy "momentum" như viên bi lăn dốc → vượt qua local minima nhỏ, smooth update
	- **RMSProp**: chia learning rate cho moving average của $\sqrt{(\nabla\mathcal{L})^2}$ → adaptive per-parameter learning rate
	- **Adam** (Kingma & Ba, 2014): kết hợp Momentum + RMSProp
		- $m_t = \beta_1 m_{t-1} + (1-\beta_1) g_t$  (1st moment - mean)
		- $v_t = \beta_2 v_{t-1} + (1-\beta_2) g_t^2$  (2nd moment - variance)
		- Bias correction: $\hat{m}_t = m_t / (1-\beta_1^t)$
		- Update: $w_{t+1} = w_t - \eta \frac{\hat{m}_t}{\sqrt{\hat{v}_t} + \epsilon}$
		- **Default cho hầu hết DL tasks**
	- **AdamW** (Loshchilov & Hutter, 2017):
		- Decouple weight decay khỏi gradient: $w_{t+1} = w_t - \eta(\frac{\hat{m}_t}{\sqrt{\hat{v}_t}+\epsilon} + \lambda w_t)$
		- Adam gốc gộp L2 vào gradient → không hoạt động đúng với adaptive LR
		- **Standard cho training Transformer/LLM hiện nay**
	- **Khi nào dùng gì**:
		- SGD+Momentum: CNN cho image classification (ResNet), thường generalize tốt hơn Adam
		- AdamW: Transformers, LLM, tasks có sparse gradients
	- **LR scheduling**: warmup + cosine decay là combo phổ biến cho LLM

10. ==Dropout: cơ chế và tại sao hoạt động?==
	- Khi train: với mỗi forward pass, **tắt ngẫu nhiên** mỗi neuron với probability $p$ (vd 0.5)
	- Khi inference: dùng tất cả neurons nhưng scale outputs bởi $(1-p)$ (hoặc inverted dropout: scale lúc training bằng $\frac{1}{1-p}$)
	- **Tại sao hoạt động**:
		- **Ensemble effect**: mỗi forward pass = 1 sub-network khác nhau, inference = trung bình ensemble exponentially nhiều sub-networks
		- **Co-adaptation prevention**: ép neurons không thể "ỷ lại" vào neuron cụ thể nào → mỗi neuron phải học feature hữu ích độc lập
	- **Hyperparams**: $p$ thường 0.2–0.5; cao hơn có thể cho fully-connected layer, thấp hơn cho conv layer
	- **Trong Transformer**: dropout sau attention output, sau FFN, trên embeddings (typical $p = 0.1$)
	- **Lưu ý**: với BatchNorm thì cần cẩn thận thứ tự (Dropout → BatchNorm gây bất ổn vì variance shift)

11. ==Cross-entropy loss và mối liên hệ với Maximum Likelihood, KL divergence==
	- **Binary cross-entropy**: $\mathcal{L} = -[y \log \hat{y} + (1-y) \log(1-\hat{y})]$
	- **Categorical cross-entropy**: $\mathcal{L} = -\sum_i y_i \log \hat{y}_i$
	- **Tại sao dùng CE thay vì MSE cho classification**:
		- Khi sigmoid + MSE → gradient nhỏ khi prediction sai (do $\sigma'(x)$) → học chậm
		- Sigmoid + CE: gradient = $(\hat{y} - y)$ đẹp, không bị vanishing
		- CE convex với softmax/sigmoid output, MSE thì non-convex
	- **Liên hệ với MLE**: minimize CE = maximize log-likelihood của data dưới Bernoulli/Categorical distribution
	- **Liên hệ với KL divergence**:
		- $D_{KL}(P || Q) = \sum P(x) \log \frac{P(x)}{Q(x)} = H(P, Q) - H(P)$
		- Khi $P$ là true distribution (fixed), minimize $H(P, Q)$ (cross-entropy) ≡ minimize $D_{KL}$
	- **Label smoothing**: thay $y = [0,0,1,0]$ bằng $y = [\epsilon/K, \epsilon/K, 1-\epsilon+\epsilon/K, \epsilon/K]$ → giảm overconfidence, regularization, dùng phổ biến trong training Transformer

12. ==CNN: convolution, receptive field, pooling, vì sao hiệu quả cho ảnh==
	- **Convolution**: trượt kernel (filter) qua input, mỗi vị trí compute dot product → feature map
		- Hyperparams: kernel size, stride, padding, số channels
	- **Tại sao tốt cho ảnh**:
		- **Translation equivariance**: detect object bất kể vị trí
		- **Local connectivity**: pixel gần nhau có quan hệ → kernel nhỏ đủ
		- **Parameter sharing**: cùng kernel quét toàn ảnh → giảm tham số drastically vs FC
	- **Receptive field**: vùng input mà 1 neuron output "nhìn thấy"
		- Layer sâu hơn → receptive field lớn hơn → học high-level features (object, scene)
		- Layer nông → low-level features (edge, texture)
	- **Pooling**: downsample (max/average pool) → giảm spatial size, tăng receptive field, translation invariance một phần
		- Modern: thay pooling bằng strided conv (giữ learnable, không mất info)
	- **Modern CNN**: ResNet (residual connections), EfficientNet, ConvNeXt (CNN học từ Transformer design)

---

## III. Sequence Models, Transformers & Attention

13. ==Hạn chế của Seq2Seq truyền thống và tại sao Attention giải quyết được?==
	- **Seq2Seq cổ điển** (Sutskever, 2014): RNN/LSTM encoder nén toàn bộ input sequence thành **1 context vector cố định**, decoder sinh output từ vector đó
	- **Hạn chế**:
		- **Information bottleneck**: 1 vector không đủ chứa thông tin của câu dài
		- **Long-term dependency**: gradient vanish theo thời gian, model "quên" đầu câu
		- **Sequential**: không parallelize được, train chậm
	- **Attention (Bahdanau 2014, Luong 2015)**:
		- Decoder ở mỗi step có thể "nhìn lại" **toàn bộ encoder hidden states** với weights khác nhau
		- $\text{context}_t = \sum_i \alpha_{t,i} h_i$ với $\alpha_{t,i}$ = attention weights softmax
		- Giải quyết bottleneck (không phải nhồi vào 1 vector) và long-term dependency (truy cập trực tiếp)
	- **Self-Attention** (Transformer, 2017): attention trong cùng 1 sequence (Q, K, V đều từ input) → loại bỏ recurrence hoàn toàn → parallelize triệt để
	- **Lưu ý**: *Word2Vec, GloVe* là static word embeddings (1 từ = 1 vector cố định), KHÔNG phải Seq2Seq. Modern: contextual embeddings (BERT, GPT) - 1 từ có vector khác nhau tùy ngữ cảnh.

14. ==Scaled Dot-Product Attention: công thức, vai trò Q/K/V, tại sao chia $\sqrt{d_k}$?==
	- $\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right) V$
	- **Q (Query)**: "tôi đang tìm gì?" - vector của token đang xét
	- **K (Key)**: "tôi chứa cái gì?" - vector của các token được tham chiếu, dùng để so khớp với Q
	- **V (Value)**: "thông tin tôi đem đi nếu được chọn" - vector chứa nội dung thực sự để aggregate
	- $QK^T$ → similarity scores giữa mỗi query và mỗi key
	- Softmax → attention weights (tổng = 1) trên các keys
	- Weighted sum của V theo attention weights → output
	- **Tại sao chia $\sqrt{d_k}$?**
		- Khi $d_k$ lớn, dot product $q \cdot k$ có variance lớn (scale theo $d_k$)
		- Softmax với input lớn → output cực kỳ peaked (gần one-hot) → gradient ≈ 0 → train không được
		- Chia $\sqrt{d_k}$ giữ variance ≈ 1 → softmax mượt → gradient ổn

15. ==Multi-Head Attention: tại sao không dùng 1 head với $d_k$ lớn?==
	- Multi-head: chia $d_{model}$ thành $h$ heads, mỗi head có $d_k = d_{model}/h$ riêng
	- Mỗi head học **một loại quan hệ khác nhau**: syntactic, semantic, coreference, distance,...
	- Nếu 1 head với $d_k$ lớn: chỉ học được 1 loại pattern (1 attention distribution duy nhất) → kém biểu cảm
	- Multi-head ≈ ensemble nhiều "subspace projections" trong attention
	- Output các heads concat → linear projection
	- Cost compute tương đương 1 head với cùng tổng dim
	- **Modern variant**:
		- **MQA (Multi-Query Attention)**: nhiều Q heads chia sẻ 1 K, V → giảm KV cache, tăng inference speed (PaLM)
		- **GQA (Grouped-Query Attention)**: trung gian giữa MHA và MQA → LLaMA-2/3, Mistral

16. ==Positional Encoding: tại sao cần và các phương pháp (sinusoidal vs learned vs RoPE)==
	- Self-attention là **permutation-invariant**: nếu hoán đổi tokens, output cũng hoán đổi → không có thông tin thứ tự
	- → Cần inject positional info vào input embeddings
	- **Sinusoidal PE** (Transformer gốc):
		- $PE(pos, 2i) = \sin(pos / 10000^{2i/d})$
		- $PE(pos, 2i+1) = \cos(pos / 10000^{2i/d})$
		- Cộng vào word embedding: $x = E_{token} + PE$
		- Generalize được cho sequence dài hơn lúc train (về lý thuyết)
	- **Learned absolute PE**: parameter learnable cho mỗi position → BERT, GPT-2
		- Hạn chế: max length cố định, không extrapolate
	- **RoPE (Rotary Position Embedding)**: encode position bằng cách **xoay** Q, K trong không gian phức theo góc tỉ lệ với position
		- Ưu: encode relative position tự nhiên, extrapolate tốt hơn (với base scaling), không thêm params
		- **Standard cho LLaMA, Qwen, Mistral, Gemma 2024+**
	- **ALiBi (Attention with Linear Biases)**: thêm bias linear theo distance vào attention scores → BLOOM, MPT
	- Modern long-context (1M tokens): kết hợp RoPE + scaling tricks (NTK-aware, YaRN)

17. ==Causal mask / Masked self-attention trong decoder==
	- Trong decoder (GPT, Transformer decoder), khi training với teacher forcing, model thấy toàn bộ target sequence cùng lúc
	- Nhưng khi predict token vị trí $t$, chỉ được dùng tokens $1..t-1$ (không được "nhìn tương lai")
	- **Causal mask**: matrix tam giác trên với $-\infty$ trước softmax → các vị trí tương lai có attention weight = 0
	- $\text{mask}_{ij} = -\infty$ nếu $j > i$, ngược lại $0$
	- Cộng mask vào $QK^T / \sqrt{d_k}$ trước softmax
	- Cho phép parallel training: predict tất cả positions cùng lúc, mỗi position chỉ "thấy" prefix của nó
	- **Bidirectional (BERT)** không có causal mask → mỗi token thấy toàn bộ context → tốt cho understanding (NLU), không tự nhiên cho generation

18. ==Encoder-only vs Decoder-only vs Encoder-Decoder Transformer==

| Loại | Ví dụ | Đặc điểm | Use case |
|---|---|---|---|
| Encoder-only | BERT, RoBERTa, DeBERTa | Bidirectional attention, MLM training | Classification, NER, embedding, search |
| Decoder-only | GPT, LLaMA, Mistral, Qwen | Causal attention, next-token prediction | Generation, chat, code (modern LLM standard) |
| Encoder-Decoder | T5, BART, FLAN-T5 | Cross-attention từ decoder sang encoder | Translation, summarization |

- Trend 2024-2026: **decoder-only thống trị** vì scale tốt và đa năng (in-context learning, instruction following)
- BERT-style vẫn dùng nhiều cho embedding/retrieval (BGE, E5, Jina)

---

## IV. LLM, RAG & Modern AI Engineering

19. ==Tokenization: BPE, WordPiece, SentencePiece — sự khác biệt và tại sao subword?==
	- **Tại sao subword (không dùng word/char)**:
		- Word-level: vocab cực lớn, OOV (out-of-vocab) cho từ hiếm
		- Char-level: sequence quá dài, mất ý nghĩa từ
		- Subword: cân bằng — từ phổ biến giữ nguyên, từ hiếm tách thành subwords
	- **BPE (Byte Pair Encoding)** - dùng trong GPT, RoBERTa:
		- Bắt đầu từ chars, lặp lại: tìm cặp xuất hiện nhiều nhất, merge thành token mới
		- Vocab cuối = chars + merged subwords
	- **WordPiece** - dùng trong BERT:
		- Tương tự BPE nhưng merge dựa trên likelihood (chọn cặp tăng likelihood của corpus nhiều nhất), không phải frequency
	- **SentencePiece** - dùng trong T5, LLaMA, ALBERT:
		- Treat input như stream of characters (kể cả spaces) → language-agnostic
		- Unigram LM hoặc BPE backend
	- **tiktoken** (OpenAI): BPE optimized C++, dùng cho GPT-3.5/4
	- **Lưu ý quan trọng**:
		- Cùng 1 từ, tokenizer khác nhau → số tokens khác nhau → ảnh hưởng cost API
		- Tiếng Việt có dấu/Unicode → tokenizer không tối ưu có thể tạo nhiều tokens (~2x English)
		- Token ≠ word, token ≠ char

20. ==Embedding: ý nghĩa, cách tính similarity, dùng ở đâu trong AI engineering==
	- **Embedding**: biểu diễn discrete object (word, sentence, image, user) thành **dense vector** trong không gian liên tục
		- Tính chất: objects "gần nhau về ý nghĩa" thì vector gần nhau
		- Vd: $\text{vec}(king) - \text{vec}(man) + \text{vec}(woman) \approx \text{vec}(queen)$
	- **Loại embeddings**:
		- *Static*: Word2Vec, GloVe, FastText (1 từ = 1 vector)
		- *Contextual*: BERT [CLS], output của sentence transformers (1 từ tùy ngữ cảnh, 1 câu = 1 vector)
		- *Modern dense*: BGE, E5, Cohere, OpenAI text-embedding-3, Jina v3 (multilingual)
		- *Multimodal*: CLIP (text + image cùng không gian)
	- **Similarity metrics**:
		- **Cosine similarity**: $\cos\theta = \frac{a \cdot b}{||a|| \cdot ||b||}$ → most popular cho semantic search
		- **Dot product**: nếu vectors đã normalize thì = cosine
		- **Euclidean (L2)**: ít dùng cho semantic, nhạy với magnitude
	- **Use cases**:
		- Semantic search / retrieval (RAG)
		- Recommendation system
		- Clustering, deduplication
		- Classification (thay vì train model riêng → embed + simple classifier)
		- Anomaly detection

21. ==RAG (Retrieval-Augmented Generation): kiến trúc, ưu điểm, các challenges==
	- **Kiến trúc**:
		1. **Indexing pipeline** (offline):
			- Documents → **chunking** → **embedding** → lưu vào **vector DB** (Pinecone, Weaviate, Qdrant, FAISS, Milvus)
		2. **Query pipeline** (online):
			- User query → embed → vector search top-K → relevant chunks
			- Inject vào prompt: `"Dựa trên context sau: {chunks}, trả lời: {query}"`
			- LLM generate response grounded vào retrieved context
	- **Ưu điểm so với fine-tuning**:
		- Cập nhật knowledge dễ (chỉ update vector DB)
		- Truy ngược source (citation, giảm hallucination)
		- Dùng được với private/proprietary data mà không cần train
		- Rẻ hơn fine-tuning với knowledge thường xuyên thay đổi
	- **Challenges & best practices**:
		- **Chunk size**: quá nhỏ mất context, quá lớn dilute relevance. Thường 256-1024 tokens, có overlap (vd 10-20%)
		- **Chunking strategy**: fixed-size, recursive, semantic (theo câu/đoạn), document-structure-aware
		- **Hybrid search**: dense (embedding) + sparse (BM25) → tốt hơn dense thuần
		- **Reranking**: top-K (vd 100) bằng embedding cheap, rerank top-N (vd 10) bằng cross-encoder mạnh hơn (vd Cohere Rerank, BGE-reranker)
		- **Query rewriting**: HyDE (Hypothetical Document Embeddings), multi-query expansion
		- **Evaluation**: faithfulness, answer relevance, context precision/recall (RAGAs framework)
		- **Failure modes**: retrieved docs irrelevant → LLM hallucinate, context window quá tải, conflict giữa internal knowledge và retrieved context
	- **Advanced**: GraphRAG (Microsoft), Agentic RAG (LLM tự quyết định khi nào search), self-RAG

22. ==Fine-tuning: Full fine-tuning vs LoRA vs QLoRA vs Prompt tuning==
	- **Full fine-tuning**: update toàn bộ params của pretrained model
		- Cần GPU memory rất lớn (vd 7B model FP16 ~ 14GB params + ~3-4x cho gradients/optimizer states/activations ≈ 60-80GB)
		- Risk catastrophic forgetting
		- Tốt nhất về performance nếu đủ data
	- **LoRA (Low-Rank Adaptation)** - Hu et al., 2021:
		- **Freeze** original weights $W$
		- Inject 2 trainable matrices low-rank: $\Delta W = B A$ với $B \in \mathbb{R}^{d \times r}$, $A \in \mathbb{R}^{r \times d}$, $r \ll d$ (typical $r$ = 4–64)
		- Forward: $h = W x + B A x$ (scale bởi $\alpha/r$)
		- Trainable params giảm ~10,000x → fit 7B model trên single GPU
		- Inference: merge $W' = W + BA$ → không thêm latency
		- Có thể swap nhiều LoRA adapters cho cùng base model (multi-tenant)
	- **QLoRA** (Dettmers et al., 2023): LoRA + quantize base model xuống **4-bit** (NF4) → fine-tune 65B model trên 48GB GPU
	- **Adapter**: thêm small bottleneck modules vào mỗi layer (cũ hơn LoRA)
	- **Prompt tuning / Prefix tuning**: chỉ train soft prompts (continuous vectors) prepend vào input, freeze toàn bộ model
		- Rất ít params (vài MB) nhưng performance kém LoRA cho complex tasks
	- **Khi nào dùng gì**:
		- Có tons of data + cần performance max → full FT
		- Limited GPU + task-specific adaptation → LoRA / QLoRA (default)
		- Không có GPU train → prompt engineering / RAG / few-shot

23. ==Prompting techniques: Zero-shot, Few-shot, Chain-of-Thought, ReAct==
	- **Zero-shot**: chỉ task description, không có ví dụ
		- `"Translate this to French: 'Hello world'"`
	- **Few-shot (in-context learning)**: thêm vài examples vào prompt
		- Pattern: `"Q: ... A: ...\nQ: ... A: ...\nQ: {query} A:"`
		- LLM "học" pattern mà không update weights
		- Chỉ work tốt với model đủ lớn (≥ 6B params, GPT-3 paper)
	- **Chain-of-Thought (CoT)** - Wei et al., 2022:
		- Yêu cầu model **giải thích từng bước** trước khi đưa đáp án
		- Cải thiện rõ rệt cho reasoning tasks (math, logic)
		- Trigger: thêm `"Let's think step by step"` (zero-shot CoT, Kojima 2022)
		- Few-shot CoT: cung cấp examples có reasoning chain
	- **Self-Consistency**: sample nhiều CoT với temperature > 0, vote majority answer
	- **ReAct** (Reasoning + Acting): xen kẽ thought, action (tool call), observation → cơ sở của agents
	- **Tree of Thoughts (ToT)**: explore nhiều reasoning paths như tree search
	- **Tips thực tế**:
		- Đặt instructions rõ, output format cụ thể (JSON schema)
		- System prompt vs user prompt: tách role
		- Modern models (GPT-4o, Claude 3.5+, o1) đã internalize CoT → đôi khi không cần nhắc
		- "Reasoning models" (o1, DeepSeek-R1, Claude với extended thinking) có CoT built-in

24. ==Hallucination trong LLM: nguyên nhân và cách giảm==
	- **Hallucination**: LLM sinh ra thông tin sai/bịa, nhưng diễn đạt như thật
	- **Nguyên nhân**:
		- Pretraining objective là **next-token likelihood**, không phải truthfulness
		- Knowledge cutoff (không biết info mới)
		- Training data có sai sót, contradictions
		- Model "compress" knowledge có lossy → chi tiết bị bịa
		- Sampling với temperature cao
	- **Cách giảm**:
		- **RAG**: ground câu trả lời vào nguồn có thật, citation
		- **Lower temperature** (0–0.3) cho factual tasks
		- **Tool use / function calling**: khi cần tính toán, thông tin real-time → call tool thay vì nội suy
		- **Constrained decoding**: JSON mode, structured outputs (Pydantic schema)
		- **Self-consistency / verification**: sinh nhiều câu trả lời, check consistency
		- **Fine-tuning với DPO/RLHF** trên honesty data
		- **Eval framework**: TruthfulQA, FActScore, hallucination detection classifiers
		- **Prompt**: explicitly cho phép model nói "I don't know"
	- **Note**: hallucination là tradeoff cố hữu của generative model — không thể eliminate hoàn toàn

25. ==KV cache: tại sao quan trọng cho LLM inference==
	- Trong autoregressive generation, mỗi step generate 1 token, dùng toàn bộ context tới giờ
	- Naive: mỗi step recompute K, V cho toàn bộ tokens → $O(n^2)$ tổng cost
	- **KV cache**: lưu K, V đã tính cho các tokens cũ, mỗi step mới chỉ tính K, V cho token mới nhất
	- → Mỗi token mới chỉ cost $O(n)$ thay vì $O(n^2)$
	- **Memory cost**: $2 \times L \times h \times d_h \times n$ (2 cho K và V; L = layers, h = heads, $d_h$ = head dim, n = seq length)
		- Vd LLaMA-2-7B với context 4K, FP16: ~2GB chỉ cho KV cache 1 sequence
	- **Tối ưu KV cache**:
		- **MQA/GQA**: shared K, V across heads → giảm KV cache 8-32x
		- **Quantization** KV cache xuống int8/int4
		- **PagedAttention** (vLLM): manage KV cache như virtual memory pages → tránh fragmentation
		- **Sliding window attention** (Mistral): chỉ lưu KV của last $W$ tokens
	- Là bottleneck chính cho long-context inference

26. ==Quantization: int8, int4, GGUF — đánh đổi gì để tăng tốc?==
	- **Quantization**: giảm precision của weights (và optionally activations) từ FP32/FP16 xuống int8/int4
	- **Lợi**:
		- Memory: int8 = 1/2 FP16, int4 = 1/4 FP16 → fit model lớn hơn vào GPU/CPU
		- Speed: int matmul nhanh hơn FP trên hardware support (Tensor Cores, NPUs)
	- **Đánh đổi**: precision loss → quality drop (thường nhỏ với int8, đáng kể với int4 nếu naive)
	- **Phương pháp**:
		- **PTQ (Post-Training Quantization)**: quantize sau khi train, không cần retrain. Vd GPTQ, AWQ
		- **QAT (Quantization-Aware Training)**: simulate quantization khi train → quality cao hơn nhưng tốn compute
		- **GPTQ**: layer-wise, second-order info, int4 với quality drop nhỏ
		- **AWQ (Activation-aware Weight Quantization)**: bảo vệ "salient weights" (kết nối với activation lớn)
	- **Format**:
		- **GGUF** (llama.cpp): format chuẩn cho CPU/Apple Silicon inference, hỗ trợ Q2-Q8
		- **GPTQ/AWQ**: GPU-optimized
		- **bitsandbytes**: integration với HuggingFace, NF4 (QLoRA)
	- **Practical**: Q4_K_M trong GGUF là sweet spot speed/quality cho local inference

---

## V. Practical / MLOps / System

27. ==Train/Val/Test split: tại sao cần và các pitfall thường gặp==
	- **Train**: model học weights
	- **Val**: tune hyperparameters, model selection, early stopping
	- **Test**: đánh giá final, **chỉ dùng 1 lần** ở cuối — nếu dùng để tune → leakage gián tiếp
	- **Tỷ lệ phổ biến**: 70/15/15, 80/10/10, hoặc với data cực lớn 98/1/1
	- **Cross-validation**: k-fold (vd k=5), thay vì 1 val set cố định → estimate ổn định hơn
	- **Pitfall**:
		- **Data leakage**: feature có info từ tương lai (vd target encoding tính trên cả test)
		- **Temporal leakage** với time-series: phải split theo thời gian, KHÔNG random shuffle
		- **Group leakage**: cùng user/patient ở cả train và test → leak. Dùng `GroupKFold`
		- **Distribution shift**: train/test khác distribution thật → metric tốt nhưng prod tệ
		- **Imbalanced**: dùng `StratifiedKFold` để giữ class ratio
	- **Modern**: với LLM evaluation, nguy cơ **test set contamination** trong pretraining data → cần custom held-out eval

28. ==Đánh giá LLM: metrics, eval frameworks, human eval==
	- **Automatic metrics (kinh điển)**:
		- **Perplexity**: $e^{\text{cross-entropy}}$ — đo predictive quality, không đánh giá usefulness
		- **BLEU, ROUGE, METEOR**: n-gram overlap với reference (translation, summarization). Dễ bị fool, không capture semantic
		- **BERTScore**: semantic similarity bằng BERT embeddings
	- **LLM benchmarks**:
		- **MMLU**: multitask academic knowledge (57 subjects)
		- **HumanEval, MBPP**: code generation
		- **GSM8K, MATH**: math reasoning
		- **BBH (Big-Bench Hard)**: reasoning
		- **MT-Bench, AlpacaEval, Arena (LMSYS)**: open-ended chat, preference
		- **IFEval**: instruction following
	- **LLM-as-a-judge**: dùng GPT-4/Claude grade outputs theo rubric
		- Pros: scalable, semantic. Cons: bias (length, position, model preference)
	- **Production eval**:
		- **Online**: A/B testing, user satisfaction, retention
		- **Offline**: golden datasets, regression tests
		- **RAGAs** cho RAG: faithfulness, answer relevance, context precision/recall
		- **Guardrails**: toxicity, PII, hallucination detection
	- **Human eval** vẫn là gold standard cho nuance, nhưng đắt và slow

29. ==Reproducibility trong DL: làm sao đảm bảo experiment lặp lại được?==
	- **Random seeds**: set seed cho `random`, `numpy`, `torch`, `torch.cuda` (mỗi process)
	- **Deterministic ops**: `torch.use_deterministic_algorithms(True)`, `torch.backends.cudnn.deterministic = True` (chậm hơn nhưng repro)
	- **Environment**: pin versions trong `requirements.txt`/`pyproject.toml`, dùng Docker
	- **Data versioning**: DVC, LakeFS, hoặc hash dataset
	- **Experiment tracking**: MLflow, W&B (Weights & Biases), Neptune → log hyperparams, metrics, model artifacts, code commit
	- **Config management**: Hydra, YAML configs thay vì argparse phình to
	- **Lưu ý hardware**: cùng code, khác GPU type/CUDA version → vẫn có thể khác nhỏ. Reproducibility hoàn toàn rất khó với distributed training.

30. ==MLOps pipeline cơ bản: từ notebook đến production==
	1. **Data ingestion + validation**: schema check (Great Expectations, Pandera), drift detection
	2. **Feature engineering**: feature store (Feast, Tecton) để share features train ↔ serve
	3. **Training**: pipeline orchestration (Airflow, Prefect, Kubeflow), reproducible (xem câu 29)
	4. **Model registry**: MLflow, W&B Artifacts → versioning, staging/prod tags
	5. **Serving**:
		- Batch: scheduled jobs, dump predictions
		- Real-time: REST/gRPC (FastAPI, Triton, TorchServe, BentoML)
		- LLM serving: vLLM, TGI, SGLang, TensorRT-LLM
	6. **Monitoring**:
		- *Model performance*: accuracy degradation
		- *Data drift*: input distribution thay đổi (Evidently, WhyLabs)
		- *Concept drift*: relationship X → y thay đổi
		- *Latency, throughput, error rates*
	7. **Retraining**: scheduled hoặc trigger-based khi drift phát hiện
	8. **CI/CD for ML**: test data, test model (smoke test, performance regression), deploy với canary
	- **Khác biệt với software thông thường**: model = code + data + hyperparams, nên cần version cả 3

31. ==Model deployment: latency vs throughput, batching, GPU utilization==
	- **Latency**: thời gian xử lý 1 request (P50, P95, P99)
	- **Throughput**: số requests/giây hệ thống xử lý
	- **Tradeoff**: tăng batch size → throughput cao nhưng latency tăng
	- **Static batching**: chờ đủ batch rồi xử lý → tail latency tệ
	- **Dynamic batching** (Triton): gom requests đến trong cửa sổ ngắn (vd 10ms) → trade nhẹ latency để tăng throughput
	- **Continuous batching** (vLLM, TGI cho LLM): khi 1 request trong batch finish, slot trống được fill ngay bằng request mới → GPU utilization cực cao cho LLM (vì sequences có length khác nhau)
	- **GPU utilization tips**:
		- Mixed precision (FP16/BF16) inference
		- Quantization
		- Compile model: `torch.compile`, ONNX, TensorRT
		- Profile bằng `nvidia-smi`, `nsys`, `torch.profiler`
		- KV cache management cho LLM
	- **Cost calculation**: $/token cho LLM = (GPU $/hour) / (tokens/hour throughput)

---

## VI. Behavioral / Research mindset (AI Research role specific)

32. ==Đọc paper: workflow recommended==
	- **3-pass approach** (Keshav, "How to Read a Paper"):
		1. *Skim*: title, abstract, intro, conclusion, headings, figures (5-10 phút) → quyết định có đọc tiếp không
		2. *Detail*: đọc kỹ, hiểu ý chính, bỏ qua proof. Highlight references quan trọng (~1 giờ)
		3. *Reproduce*: re-derive math, implement core ideas, critique
	- **Tools**: Connected Papers, Semantic Scholar, arXiv-sanity, Papers with Code (cho SOTA + benchmarks)
	- **Track**: Twitter/X (AI researchers), HuggingFace daily papers, AlphaXiv (community comments), Reddit r/MachineLearning
	- **Reproducibility**: ưu tiên paper có code (Papers with Code có "official" tag), check Issues của repo
	- **Note system**: Obsidian/Notion với template (Problem, Method, Results, Critique, My takeaway)
	- **Critical reading**: hỏi "claim này có over-stated không?", "ablation đầy đủ chưa?", "compare baseline có fair không?", "code release không?", "scale có thực tế không?"

33. ==Một AI Engineer khác data scientist như thế nào?==

| | Data Scientist | AI/ML Engineer | AI Researcher |
|---|---|---|---|
| Mục tiêu | Insight, business decision | Production AI systems | Push SOTA, novel methods |
| Output | Reports, dashboards, A/B test | APIs, deployed models, pipelines | Papers, prototypes |
| Skills | Stats, SQL, viz, exp design | SWE + ML, MLOps, system design | DL theory, math, research taste |
| Codebase | Notebooks, scripts | Production code, tests, CI/CD | Research code (often messy) |
| Stakeholders | Business teams | Eng teams, infra | Academic + internal research |

- **AI Engineer hiện đại (2024-2026)** thường overlap mạnh với **LLM/RAG/Agent engineering**: prompt engineering, eval frameworks, vector DB, tool use, multi-agent orchestration, observability cho LLM apps (LangSmith, Langfuse)
- Vietnam market 2026: VinAI, VinBigData, FPT.AI, Zalo AI, Viettel AI, Cinnamon AI → đa phần tìm AI Engineer hybrid (research-aware nhưng ship product được)

34. ==Câu hỏi thường gặp về project cá nhân (behavioral)==
	- **STAR framework**: Situation, Task, Action, Result
	- **Câu hỏi mẫu interviewer hay hỏi**:
		- "Project ML mà em proud nhất, kể end-to-end?"
		- "Bug khó nhất em từng debug trong ML pipeline?"
		- "Khi metric tốt trên val nhưng tệ trên test/prod, em làm gì?"
		- "Trade-off em đã phải đưa ra giữa accuracy và latency?"
		- "Lần em sai trong design choice và đã học được gì?"
		- "Paper gần đây em đọc và muốn áp dụng vào project hiện tại?"
	- **Tips chuẩn bị**:
		- Có 2-3 stories chuẩn bị sẵn, mỗi cái cover được nhiều dimensions (technical depth, teamwork, failure & learning)
		- Số liệu cụ thể: "giảm latency 200ms → 80ms", "tăng F1 từ 0.72 → 0.81"
		- Honest về failure: interviewer thường ấn tượng hơn với câu chuyện thất bại + bài học
		- Hiểu sâu hơn là rộng: 1 project nắm thật chắc > 5 project hời hợt

---

## VII. Coding / Implementation questions (whiteboard)

> Interviewer hay yêu cầu code "from scratch" hoặc "in NumPy/PyTorch only" để check hiểu sâu, không chỉ biết dùng API.

35. ==Implement Scaled Dot-Product Attention from scratch (PyTorch)==
```python
import torch
import torch.nn.functional as F
import math

def scaled_dot_product_attention(Q, K, V, mask=None):
    """
    Q: (batch, seq_q, d_k)
    K: (batch, seq_k, d_k)
    V: (batch, seq_k, d_v)
    mask: (batch, seq_q, seq_k) — bool, True = mask out
    """
    d_k = Q.size(-1)
    # (batch, seq_q, seq_k)
    scores = torch.matmul(Q, K.transpose(-2, -1)) / math.sqrt(d_k)

    if mask is not None:
        scores = scores.masked_fill(mask, float('-inf'))

    attn = F.softmax(scores, dim=-1)            # (batch, seq_q, seq_k)
    out  = torch.matmul(attn, V)                # (batch, seq_q, d_v)
    return out, attn
```
- **Follow-up trap**: tại sao `mask` cộng `-inf` chứ không nhân 0? → vì softmax có $e^x$, $-\infty$ → 0; nếu nhân 0 sau softmax thì các weights còn lại không tổng = 1.
- **Hỏi mở rộng**: extend thành multi-head — split last dim thành `(num_heads, d_head)`, transpose, attention song song trên các heads, concat back, linear projection.

36. ==Implement Multi-Head Attention module==
```python
import torch.nn as nn

class MultiHeadAttention(nn.Module):
    def __init__(self, d_model, num_heads, dropout=0.1):
        super().__init__()
        assert d_model % num_heads == 0
        self.d_model   = d_model
        self.num_heads = num_heads
        self.d_head    = d_model // num_heads

        self.W_q = nn.Linear(d_model, d_model)
        self.W_k = nn.Linear(d_model, d_model)
        self.W_v = nn.Linear(d_model, d_model)
        self.W_o = nn.Linear(d_model, d_model)
        self.dropout = nn.Dropout(dropout)

    def forward(self, x, mask=None):
        B, T, _ = x.shape
        # (B, T, d_model) -> (B, num_heads, T, d_head)
        def split(t): return t.view(B, T, self.num_heads, self.d_head).transpose(1, 2)

        Q, K, V = split(self.W_q(x)), split(self.W_k(x)), split(self.W_v(x))
        scores = (Q @ K.transpose(-2, -1)) / (self.d_head ** 0.5)
        if mask is not None:
            scores = scores.masked_fill(mask, float('-inf'))
        attn = self.dropout(scores.softmax(dim=-1))
        out  = attn @ V                                              # (B, h, T, d_head)
        out  = out.transpose(1, 2).contiguous().view(B, T, self.d_model)
        return self.W_o(out)
```
- **Common bug**: quên `.contiguous()` trước `.view()` sau `transpose` → RuntimeError.

37. ==Implement basic training loop in PyTorch (correct version)==
```python
model.train()
for epoch in range(num_epochs):
    for x, y in train_loader:
        x, y = x.to(device), y.to(device)
        optimizer.zero_grad()              # 1. clear old gradients
        logits = model(x)                  # 2. forward
        loss = criterion(logits, y)        # 3. compute loss
        loss.backward()                    # 4. backward (autograd)
        torch.nn.utils.clip_grad_norm_(    # 5. (optional) clip
            model.parameters(), max_norm=1.0
        )
        optimizer.step()                   # 6. update weights

    # Validation
    model.eval()
    with torch.no_grad():
        for x, y in val_loader:
            ...
    model.train()
```
- **Lỗi kinh điển**: quên `optimizer.zero_grad()` → gradient cộng dồn qua các batch → train sai
- Quên `model.eval()`/`model.train()` → BatchNorm/Dropout hành xử sai trong eval
- Quên `torch.no_grad()` ở val → tốn memory cho computation graph không cần
- `loss.backward()` 2 lần mà không zero_grad → cộng dồn gradients

38. ==Implement Layer Normalization from scratch==
```python
class LayerNorm(nn.Module):
    def __init__(self, d_model, eps=1e-5):
        super().__init__()
        self.gamma = nn.Parameter(torch.ones(d_model))
        self.beta  = nn.Parameter(torch.zeros(d_model))
        self.eps   = eps

    def forward(self, x):
        # x: (..., d_model) — normalize trên feature dim
        mean = x.mean(dim=-1, keepdim=True)
        var  = x.var(dim=-1, keepdim=True, unbiased=False)
        x_hat = (x - mean) / torch.sqrt(var + self.eps)
        return self.gamma * x_hat + self.beta
```
- **Follow-up**: viết RMSNorm — bỏ `mean`, chỉ chia bởi RMS:
```python
def rms_norm(x, gamma, eps=1e-6):
    rms = x.pow(2).mean(dim=-1, keepdim=True).sqrt()
    return gamma * x / (rms + eps)
```

39. ==Implement minimal RAG pipeline (pseudo-code)==
```python
# 1. Indexing (offline)
chunks = []
for doc in documents:
    for chunk in chunk_text(doc, chunk_size=512, overlap=64):
        emb = embedder.encode(chunk)        # vd sentence-transformer
        chunks.append({"text": chunk, "embedding": emb, "doc_id": doc.id})

vector_db.upsert(chunks)

# 2. Query (online)
def answer(query, k=5):
    q_emb       = embedder.encode(query)
    top_chunks  = vector_db.search(q_emb, k=k)               # cosine sim
    context     = "\n\n".join(c["text"] for c in top_chunks)
    prompt = f"""Dựa trên context dưới, trả lời câu hỏi.
Nếu không có thông tin trong context, trả lời "Tôi không biết".

Context:
{context}

Câu hỏi: {query}
Trả lời:"""
    return llm.generate(prompt)
```
- **Follow-up câu hay hỏi**: làm sao handle khi `top_chunks` không relevant? (threshold similarity, reranker, fallback to "không biết"). Làm sao evaluate? (RAGAs: faithfulness, context relevance).

40. ==Implement Cross-Entropy loss from scratch (sanity check hiểu)==
```python
import torch
import torch.nn.functional as F

def cross_entropy_manual(logits, targets):
    """
    logits:  (N, C) — raw scores
    targets: (N,)   — class indices
    """
    # log_softmax = log(softmax(x)) = x - logsumexp(x)
    log_probs = logits - torch.logsumexp(logits, dim=-1, keepdim=True)
    # gather log-prob của class đúng
    nll = -log_probs.gather(1, targets.unsqueeze(1)).squeeze(1)
    return nll.mean()

# Verify
logits  = torch.randn(4, 10)
targets = torch.tensor([3, 1, 7, 2])
print(cross_entropy_manual(logits, targets))
print(F.cross_entropy(logits, targets))    # nên gần bằng nhau
```
- **Trick question**: tại sao dùng `logsumexp` thay vì log(sum(exp))? → **numerical stability**. `exp(large_number)` → inf. `logsumexp` trừ max trước.

41. ==Câu hỏi mẹo / common pitfalls thường gặp==
- **"Train accuracy 99%, test accuracy 60%, em làm gì?"** → overfitting → regularization, more data, simpler model, dropout, augmentation. Đừng nhảy ngay vào "train thêm".
- **"Model dự đoán toàn class 0 trên imbalanced data, accuracy 95%, ổn không?"** → KHÔNG. Accuracy lừa. Check confusion matrix, F1, recall của minority class.
- **"Validation loss giảm nhưng training loss tăng, lý do?"** → có thể do dropout/data augmentation chỉ active khi train + thiếu warmup. Hoặc batch ordering, regularization quá mạnh.
- **"Em đặt batch_size = 1 vs 1024, có gì khác?"** → BS nhỏ: noisy gradient, có thể escape local minima, BatchNorm fail. BS lớn: smooth gradient, throughput cao, có thể overfit/converge kém (sharp minima theo Keskar et al.). Cần adjust LR theo BS (linear scaling rule).
- **"Tại sao model train trên A100 cho kết quả khác V100 dù cùng seed?"** → CUDA non-determinism, mixed precision khác, cuDNN algorithm selection. Repro hoàn toàn rất khó.
- **"Loss = NaN sau vài epoch, debug như thế nào?"** → check exploding gradient (clip), LR quá lớn, division by zero (eps), bad data (NaN/inf trong input), `log(0)` (clamp probabilities), mixed precision overflow.
- **"Embed query xong cosine sim < 0 với mọi doc, sao?"** → một số embedding model output có thể có dim âm; cosine có thể âm. Hoặc query domain khác doc domain. Check normalization.

---

## VIII. Test-Time Training (TTT) — chuyên môn của bạn

> Section này dành cho TTT pipeline bạn đang làm trên LCBv6. Interviewer sẽ đào sâu nếu bạn list nó trong CV.

42. ==Test-Time Training là gì? Khác gì với fine-tuning thông thường?==
- **TTT**: model **update weights tại inference time**, dựa trên test instance hiện tại (hoặc một mini-dataset xung quanh nó), trước khi predict
- **Pipeline điển hình**:
	1. Pretrained model nhận test input $x$
	2. Tạo self-supervised task từ $x$ (vd rotation prediction, masked reconstruction, augmentation invariance)
	3. Update weights vài steps trên loss self-supervised đó
	4. Predict trên $x$ với weights đã update
	5. (Optional) reset weights cho test instance tiếp theo
- **Khác fine-tuning**:
	- FT update 1 lần dùng labeled training set, inference dùng weights cố định
	- TTT update **mỗi test instance** (hoặc cluster), không cần label, adapt với distribution shift
- **Use cases**: domain adaptation, distribution shift, long-tail, in-context learning task mới (Akyürek et al. 2024 chứng minh TTT improve ARC benchmark drastically)
- **Tham khảo**: Sun et al. (2020) "Test-Time Training with Self-Supervision", Akyürek et al. (2024) "The Surprising Effectiveness of Test-Time Training for Abstract Reasoning"

43. ==Trade-off của TTT==
- **Pros**: adapt tốt với distribution shift, no need labels at test time, có thể fix specific instance
- **Cons**:
	- **Latency cao**: phải train mỗi inference → không phù hợp real-time
	- **Compute cost**: train cost mỗi test instance
	- **Catastrophic forgetting**: update weights có thể phá pretrained knowledge nếu không cẩn thận
	- **Self-supervised task design**: chọn aux task phù hợp khó
	- **Stability**: weights drift theo thời gian nếu không reset
- **Mitigation**:
	- LoRA-style adapter cho TTT (chỉ update low-rank, base model frozen)
	- Reset adapters per instance/cluster
	- Học rate rất nhỏ, ít step
	- Cache TTT-adapted weights cho cluster inputs tương tự

44. ==Multi-turn TTT inference loop (mà bạn đang làm)==
- Khái niệm: thay vì 1 lần TTT update + predict, làm **nhiều turns**:
	- Turn 1: TTT update → predict → observe feedback/error signal
	- Turn 2: TTT update lại với info mới → predict tốt hơn
	- ...
- **Câu hỏi interviewer có thể hỏi**:
	- "Stopping criterion cho multi-turn loop là gì?" (convergence của loss, max turns, confidence threshold)
	- "Làm sao tránh oscillation giữa các turns?" (regularization, momentum, weight decay)
	- "Compute scale linearly với số turns?" (yes, đó là cost chính)
	- "Khác gì với iterative refinement của LLM (CoT, self-correct)?" → CoT chỉ generate thêm tokens, weights không đổi. TTT update weights thật.
- **Weight update step bạn chưa thêm**: đây là điểm interviewer sẽ probe — chuẩn bị giải thích plan, lý do chưa add (prioritize stability of inference loop trước), expected behavior khi add (loss curve, accuracy gain).

---

# References

- Vaswani et al. (2017). *Attention is All You Need*. NeurIPS.
- Devlin et al. (2018). *BERT: Pre-training of Deep Bidirectional Transformers*. NAACL.
- Hu et al. (2021). *LoRA: Low-Rank Adaptation of Large Language Models*. arXiv:2106.09685.
- Dettmers et al. (2023). *QLoRA: Efficient Finetuning of Quantized LLMs*. NeurIPS.
- Lewis et al. (2020). *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks*. NeurIPS.
- Wei et al. (2022). *Chain-of-Thought Prompting*. NeurIPS.
- Loshchilov & Hutter (2017). *Decoupled Weight Decay Regularization (AdamW)*. ICLR.
- Su et al. (2021). *RoFormer: Enhanced Transformer with Rotary Position Embedding*.
- Lin et al. (2017). *Focal Loss for Dense Object Detection*. ICCV.
- Sun et al. (2020). *Test-Time Training with Self-Supervision for Generalization under Distribution Shifts*. ICML.
- Akyürek et al. (2024). *The Surprising Effectiveness of Test-Time Training for Abstract Reasoning*. arXiv:2411.07279.
- Keskar et al. (2017). *On Large-Batch Training for Deep Learning: Generalization Gap and Sharp Minima*. ICLR.

**Repos & community resources:**
- [`amitshekhariitbhu/ai-engineering-interview-questions`](https://github.com/amitshekhariitbhu/ai-engineering-interview-questions) — 200+ AI engineering questions
- [`KalyanKS-NLP/LLM-Interview-Questions-and-Answers-Hub`](https://github.com/KalyanKS-NLP/LLM-Interview-Questions-and-Answers-Hub) — 100+ LLM Q&A
- [`Devinterview-io/llms-interview-questions`](https://github.com/Devinterview-io/llms-interview-questions)
- [`andrewekhalel/MLQuestions`](https://github.com/andrewekhalel/MLQuestions) — CV/ML questions
- DataCamp, InterviewBit, Tredence blogs (2026 editions)
- Reddit r/MachineLearning, r/LocalLLaMA cho industry trends
- Papers with Code, HuggingFace daily papers cho SOTA
