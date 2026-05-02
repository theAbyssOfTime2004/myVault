---
tags:
  - deep-learning
  - training
  - debugging
  - methodology
  - karpathy
source: https://karpathy.github.io/2019/04/25/recipe/
created: 2026-05-02
---

# A Recipe for Training Neural Networks — Karpathy

> *"Neural net training is a leaky abstraction... a 'fast and furious' approach to training neural networks does not work and only leads to suffering."*

Bài viết của Andrej Karpathy (2019) được xem là **kinh điển về phương pháp luận training neural network**. Đây không phải về kiến trúc hay thuật toán mới — đây là về **quy trình** để không bị cuốn vào vòng xoáy debug trong vô vọng.

---

## Hai sự thật khó chịu về NN training

### 1. Neural Net Training is a Leaky Abstraction

Sách vở và tutorial khiến NN trông như "plug and play" — import thư viện, gọi `model.fit()`, xong. Karpathy phản bác: NN **không phải off-the-shelf technology** ngay khi bạn lệch khỏi bài toán ImageNet classification chuẩn.

Mỗi component (BatchNorm, RNN, RL framework) có những giả định, edge case, và tương tác mà bạn buộc phải hiểu sâu — nếu không sẽ "hoạt động" nhưng cho kết quả tệ một cách bí ẩn.

### 2. Neural Net Training Fails Silently

Trong software thông thường, bug → exception → bạn fix. Trong NN training, bug → **model vẫn train, vẫn cho output, chỉ là kết quả tệ hơn mức nó nên đạt**. Một vài ví dụ:

- Quên flip label khi flip ảnh trong augmentation
- Off-by-one trong autoregressive model (token t nhìn thấy token t thay vì chỉ 1..t-1)
- Clip loss thay vì clip gradient
- Load pretrained weight nhưng quên `model.load_state_dict()`, vẫn dùng random init

→ Không có exception, training vẫn chạy, loss vẫn giảm — bug ẩn đến khi bạn để ý sai sót về performance.

**Hệ quả:** training NN đòi hỏi **kiên nhẫn và để ý chi tiết** — đối lập hoàn toàn với phong cách "code thật nhanh rồi xem kết quả".

---

## Recipe — 6 bước

### Bước 1: Become One With The Data

> Đừng động vào model trước khi hiểu data.

Dành **hàng giờ** đọc qua hàng nghìn examples, không viết code NN nào. Mục tiêu: hiểu phân phối, tìm pattern, phát hiện duplicate, label noise, imbalance, bias.

**Cụ thể cần làm:**
- Tự phân loại bằng tay vài chục example → hỏi bản thân: tôi đang nhìn vào đặc trưng gì? Local hay global context? Kiến trúc nào phù hợp với cách tôi suy nghĩ?
- Đo độ noise của label
- Tìm các spurious variation (nhiễu không liên quan) → cân nhắc preprocessing để loại
- Spatial position có quan trọng không? Cần invariance gì?
- Viết script search/filter/sort theo mọi thuộc tính
- Plot phân phối trên mọi axis, **đặc biệt chú ý outliers** — outlier hầu như luôn lộ ra bug data hoặc preprocessing

**Insight cốt lõi:** NN là một dạng nén dataset. Khi nó predict sai, lỗi đó *thường nói nhiều về data hơn về model*.

---

### Bước 2: End-to-End Skeleton + Dumb Baselines

Trước khi nghĩ đến SOTA, dựng một pipeline **đầu cuối** với model đơn giản nhất có thể (linear classifier hoặc tiny ConvNet). Mục tiêu là loop train → eval → visualize chạy ổn, không phải accuracy cao.

**13 tips của Karpathy ở bước này:**

#### 1. Fix random seed
Reproducibility loại bỏ một biến nhiễu khi debug. Bạn cần tách "kết quả thay đổi vì code mới" khỏi "kết quả thay đổi vì seed khác".

#### 2. Simplify
Tắt mọi thứ không cần thiết. **Đặc biệt là tắt data augmentation** — augmentation thường là nguồn bug, để sau.

#### 3. Add significant digits to evaluation
Đừng chỉ nhìn loss của batch trên Tensorboard với smoothing. Chạy eval trên **toàn bộ test set** để có số chính xác.

#### 4. Verify loss @ init
Loss ban đầu có khớp lý thuyết không?  
Softmax với `n` class, model uniform output → loss = `-log(1/n)`.  
Ví dụ 10 class → expected initial loss ≈ 2.302. Nếu loss init ≠ giá trị này → **bug ngay từ đầu**.

#### 5. Initialize well
- Last layer bias = mean của data (regression với target mean=50 → init bias=50)
- Imbalanced classification (1:10 positive:negative) → init logit bias sao cho sigmoid output ≈ 0.1
- Loại bỏ "hockey stick" loss curve — model không phải dùng vài epoch đầu chỉ để học mean

#### 6. Human baseline
Bạn (hoặc annotator) làm task này được bao nhiêu accuracy? Nếu human làm được 90% mà model đạt 95% → có thể có data leak. Nếu human làm được 60% mà bạn target 95% → có vấn đề về tham vọng.

Trick: annotate test set 2 lần, dùng 1 lần làm "prediction", 1 lần làm "ground truth" → đo human-level performance.

#### 7. Input-independent baseline
Train với **input bị zero hoàn toàn**. Model phải tệ hơn so với khi có input thật. Nếu performance bằng nhau → model đang không trích xuất thông tin gì từ input → bug.

#### 8. Overfit one batch
Lấy 2-3 example, tăng capacity model, train cho đến khi loss → 0.  
Visualize prediction vs label tại loss tối thiểu → phải khớp **hoàn hảo**. Nếu không overfit nổi 2 example → có bug structural.

#### 9. Verify decreasing training loss
Tăng nhẹ capacity → training loss phải giảm tương ứng. Nếu không → bug optimizer/data flow.

#### 10. Visualize just before the net
**Quy tắc vàng:** plot data ngay trước dòng `y_hat = model(x)`. Đó là source of truth duy nhất về cái thực sự vào network. Augmentation/preprocessing có thể làm hỏng data theo cách bạn không ngờ tới — chỉ visualize ở cuối pipeline mới thấy.

#### 11. Visualize prediction dynamics
Cố định 1 batch test → plot prediction qua training. Cách prediction "nhảy" tiết lộ:
- Wiggle quá mức → learning rate quá cao
- Stuck → learning rate quá thấp / dead ReLU
- Instability → batch norm / numerical issue

#### 12. Use backprop to chart dependencies
Test data leak across batch/time:  
Set `loss = output[i].sum()`, gọi `backward()`, kiểm tra `input.grad`.  
- Chỉ `input[i]` được có gradient ≠ 0
- Áp cho autoregressive model: `output[t]` chỉ được phụ thuộc `input[1..t-1]`

Nếu sai → đang có information leak qua broadcasting/masking sai.

#### 13. Generalize a special case
Viết code cho case cụ thể trước (full loop, hard-coded), verify đúng, **rồi mới** vectorize từng phần. Mỗi bước vectorize phải giữ nguyên kết quả. Đảo ngược thứ tự này = bug ẩn không tránh khỏi.

---

### Bước 3: Overfit

Triết lý hai pha của Karpathy:
1. **Pha 1:** chọn model **đủ lớn để overfit training set** (training loss thấp).
2. **Pha 2:** regularize lại (đánh đổi training loss lấy validation loss).

Lý do: nếu không overfit nổi → có bug/misconfig sâu → regularize sớm sẽ che mất bug đó.

**4 nguyên tắc ở bước này:**

#### 1. Picking the model — "Don't be a hero"
Đừng thiết kế kiến trúc exotic. Tìm paper gần nhất với bài toán của bạn, copy kiến trúc đơn giản nhất hoạt động được. Image classification → ResNet-50. Custom hóa **sau** khi đã chạy được.

#### 2. Adam is safe
**Default đáng tin cậy: Adam, lr=3e-4.** Adam tha thứ cho hyperparameter tệ tốt hơn SGD. SGD tuned tốt thì hơn Adam một chút, nhưng "tốt" cần tuning kỹ và hẹp. Với RNN/sequence, theo paper, đừng tự sáng tạo.

#### 3. Complexify only one at a time
Có nhiều signal/feature để add → thêm **từng cái một**, verify từng bước cải thiện như kỳ vọng. Nhảy thẳng vào "all features at once" = không debug được khi performance không như mong đợi.

Ví dụ: train trên ảnh nhỏ trước, rồi tăng resolution sau khi pipeline ổn.

#### 4. Don't trust LR decay defaults
Đây là **bug ngầm phổ biến nhất** khi copy code. LR decay schedule thường tied vào epoch number, mà epoch number lại tùy thuộc vào dataset size. ImageNet decay 10x ở epoch 30 — copy sang dataset khác có thể đẩy LR về 0 sớm và bạn không biết.

**Khuyến nghị Karpathy:** ban đầu **tắt decay hoàn toàn**, dùng LR hằng số. Tune decay ở bước cuối cùng.

---

### Bước 4: Regularize

Đã có model overfit → giờ "đổi training accuracy lấy validation accuracy". Karpathy xếp các kỹ thuật **theo hiệu quả thực tế**:

#### 1. Get more data (mạnh nhất, vượt xa các kỹ thuật khác)
> *"By far the best and preferred way to regularize."*

Sai lầm phổ biến: tốn engineering cycle để optimize trên dataset nhỏ thay vì collect thêm data thật. Data thật gần như **đảm bảo monotonic improvement**.

#### 2. Data augment
Augmentation aggressive (half-fake data). Cheap so với collect data thật.

#### 3. Creative augmentation
Đi xa hơn flip/crop:
- Domain randomization
- Simulation
- Hybrid (paste object vào scene thật)
- GAN-generated data

#### 4. Pretrain
Dùng pretrained weight gần như **không bao giờ hại**, kể cả khi data đủ.

#### 5. Stick with supervised learning
Unsupervised pretraining trong CV hiện tại (2019) chưa cho kết quả mạnh. (Lưu ý: NLP với BERT là exception, do text deliberate hơn, signal-to-noise cao hơn.)

#### 6. Smaller input dimensionality
Loại bỏ feature mang signal giả. Giảm resolution nếu chi tiết low-level không quan trọng. Ít feature giả → ít overfit.

#### 7. Smaller model size
Dùng domain knowledge. Ví dụ: thay FC layer ở top của ImageNet classifier bằng global average pooling — giảm hàng triệu parameter mà vẫn giữ accuracy.

#### 8. Decrease batch size
Batch nhỏ → BatchNorm dùng mean/std batch ít chính xác hơn → "wiggle" trong scale/offset → regularization tự nhiên.

#### 9. Drop (dropout)
Dùng có chừng mực. **Dropout2d (spatial dropout) cho ConvNet.** Cảnh báo: dropout **không hợp với BatchNorm**, kết hợp cẩn thận.

#### 10. Weight decay
Tăng weight decay coefficient.

#### 11. Early stopping
Stop dựa trên validation loss. Đơn giản, hiệu quả.

#### 12. Try a larger model
Đặt cuối danh sách. Counterintuitive: model lớn hơn cuối cùng overfit nhiều hơn, **nhưng** performance early-stopped của nó thường vượt model nhỏ.

**Sanity check:** visualize first-layer weights. Filters phải có cấu trúc (edges, gradients) — nếu nhiễu hết → có vấn đề. Check internal activations xem có artifact lạ không.

---

### Bước 5: Tune

Khám phá rộng không gian hyperparameter sau khi đã có pipeline tin cậy.

#### 1. Random over grid search
Grid search **trông** an toàn nhưng kém hơn random search. Lý do: NN nhạy với một số hyperparameter và gần như không nhạy với số khác. Grid lãng phí evaluation vào parameter không quan trọng. Random phủ rộng hơn theo chiều quan trọng.

#### 2. Hyperparameter optimization
Bayesian optimization toolbox tồn tại và có người dùng thành công, nhưng Karpathy nửa đùa: dùng intern.

---

### Bước 6: Squeeze Out the Juice

Sau khi có config tốt nhất, vắt thêm performance.

#### 1. Ensembles
~5 model ensemble → +~2% accuracy gần như đảm bảo. Nếu deploy bị giới hạn compute, **distill ensemble vào 1 network** (dark knowledge — soft label từ ensemble làm target).

#### 2. Leave it training
Network train **lâu hơn intuition của bạn**. Karpathy kể chuyện vô tình để model train suốt kỳ nghỉ đông → quay lại thấy kết quả SOTA.

---

## Tinh thần cốt lõi của recipe

> *"From simple to complex, and at every step of the way we make concrete hypotheses about what will happen and then either validate them with an experiment or investigate until we find some issue."*

Bốn nguyên tắc xuyên suốt:

1. **Đi từ đơn giản đến phức tạp**, mỗi bước có hypothesis cụ thể.
2. **Verify mỗi assumption bằng experiment**, đừng giả định.
3. **Mỗi component mới phải được test riêng** trước khi tích hợp.
4. **Khi confused → simplify, đừng add thêm complexity.**

---

## Checklist thực dụng

```
Trước khi viết code model:
[ ] Đã đọc qua >100 example bằng tay
[ ] Đã visualize phân phối, outliers
[ ] Đã ước lượng được human baseline
[ ] Đã có script filter/sort/search dataset

Trước khi train serious:
[ ] Random seed fixed
[ ] Augmentation tắt
[ ] Loss @ init khớp lý thuyết
[ ] Last layer bias init theo mean/prior
[ ] Input-independent baseline kém hơn baseline thường
[ ] Overfit được 2-batch về loss ≈ 0
[ ] Visualize data ngay trước model(x)
[ ] LR decay tắt (dùng const lr)
[ ] Optimizer = Adam, lr=3e-4

Khi đã overfit:
[ ] Get more data (ưu tiên trước mọi technique khác)
[ ] Augmentation aggressive
[ ] Pretrain weights
[ ] Early stopping với validation loss
[ ] Random search hyperparameter, không grid

Trước khi nộp/deploy:
[ ] Ensemble 5 model
[ ] Train lâu hơn bạn nghĩ là cần
[ ] First-layer filter visualize có cấu trúc
```

---

## Liên kết

- [[Backpropagation]]
- [[Vanishing and Exploding Gradient]]
- [[Common Activation Function In Neural Networks]]
- [[PyTorch Autograd]]
- [[PyTorch Data Pipeline]]
- [[Adamw and Adam (optimizer)]]
