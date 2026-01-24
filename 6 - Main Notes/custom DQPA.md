2026-01-24 20:13


Tags: [[seminar HCMUS]]
 
# custom DQPA

**DEQA (Gốc):**
```
3 Experts riêng biệt:
├── Text-Only Expert (DeBERTa)
├── Text+Description Expert (DeBERTa + GPT-4 caption)
└── Text+Vision Expert (CLIP)
→ Ensemble: Weighted voting/averaging
```

**custom-DEQA**: 
```
Single Unified Model:
├── Text Encoder (mDeBERTa-v3) - term + context
├── Image Encoder (SigLIP/ResNet-152)
└── Gated-Attention Fusion
→ Direct classification
```

**Image Processing**:
**DEQA gốc**: 
```
Image → GPT-4 API → Text Description → DeBERTa Encoder
```

**DEQA custom**:

```
Image → SigLIP/ResNet Encoder → Features
+ Image Caption (có sẵn - ở phần xử lý data) → Text Encoder → Features
→ Gated Fusion
```

Lý do:
- Không phụ thuộc GPT-4 API (chi phí, latency)
- Tận dụng photo_caption có sẵn trong dataset
- Kết hợp cả vision features và caption text

Advantage:
- Chi phí thấp hơn (không cần GPT-4)
- Nhanh hơn (không cần API call)
- Vẫn có semantic information từ caption

**C. Fusion Mechanism: Ensemble vs Gated-Attention**
**DEQA gốc**: 
```
# Ensemble: Simple averaging or weighted voting
final_pred = α * pred_text + β * pred_text_desc + γ * pred_text_vision
```

**DEQA custom**:
```
# Gated-Attention: Learnable relevance weighting
gate = σ(W · [text_features; image_features])  # [0, 1]
fused = gate * image_features + (1 - gate) * text_features
```

Lý do:
- Học được: Gate tự động học mức độ liên quan của image
- Linh hoạt: Tự động bỏ qua image khi không liên quan
- End-to-end: Tối ưu cùng với classification

Advantage:
- Tự động điều chỉnh theo từng sample
- Không cần hand-tune ensemble weights
- Có residual connection để bảo toàn text information
**D. Input Format: Multi-turn QA vs Direct Input**
**DEQA gốc**:
```
Stage 1:
  Input: "[Q_e] What aspect terms? [Review text]"
  → Extract candidates
  Input: "[Q_v] Is 'service' correct? [Review text]"
  → Validate

Stage 2:
  Input: "[Q_c] Sentiment of <target>service</target>? [Review text]"
  → Classify
```

**DEQA custom**:
```
Stage 1:
  Input: term + context (review) + image
  → Direct classification

Stage 2:
  Input: term + aspect + context + image
  → Direct classification
```

Lý do:
- Đơn giản: Không cần format queries
- Hiệu quả: Model học trực tiếp từ term + context
- Phù hợp: Dataset đã có term annotations sẵn

Trade-off:
- Mất tính hướng dẫn của QA format
- Nhưng vẫn đạt performance tốt (83.76% F1)

| Improvement                   | Mô tả                                   | Lợi ích                                     |
| ----------------------------- | --------------------------------------- | ------------------------------------------- |
| 1. Gated-Attention Fusion     | Thay ensemble bằng learnable gate       | Tự động điều chỉnh, end-to-end trainable    |
| 2. Dual Text Encoding         | Separate term encoder + context encoder | Capture cả local (term) và global (context) |
| 3. SigLIP Image Encoder       | Vision Transformer với Sigmoid Loss     | Fine-grained features tốt hơn ResNet        |
| 4. Class-Balanced Focal Loss  | Kết hợp Focal Loss + Class Balancing    | Xử lý class imbalance tốt hơn               |
| 5. No External API Dependency | Không cần GPT-4                         | Chi phí thấp, deploy dễ, nhanh hơn          |
#### Key Differences

1. Single Model Architecture → Đơn giản, hiệu quả
2. Gated-Attention Fusion → Tự động điều chỉnh
3. Pre-existing Captions → Không cần GPT-4
4. Direct Input Format → Không cần QA queries
5. Class-Balanced Focal Loss → Xử lý imbalance tốt hơn

### Potential Questions & Answers

Q: Tại sao không dùng Multi-Expert Ensemble như DEQA?
A: Single model đơn giản hơn, dễ train, và Gated-Attention đã đạt performance tương đương (83.76% F1).
Q: Tại sao không dùng GPT-4 cho image descriptions?
A: Dataset đã có photo_caption, không cần GPT-4, giảm chi phí và latency.
Q: Gated-Attention có tốt hơn Ensemble không?
A: Ensemble đa dạng hơn, nhưng Gated-Attention học được và tự động điều chỉnh, phù hợp với single model architecture.

# References
