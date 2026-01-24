2026-01-24 21:23


Tags: [[seminar HCMUS]]

# FCMF model MABSA

### 1. Tổng quan kiến trúc

```
┌─────────────────────────────────────────────────────────────┐
│              FCMF (Fine-Grained Cross-Modal Fusion)        │
│              Single-Stage End-to-End Approach              │
└─────────────────────────────────────────────────────────────┘

Input: Review Text + Multiple Images (7) + ROIs (4 per image)
  │
  ├─► Text Encoder (XLM-RoBERTa)
  │   └─► Text features: [batch, seq_len, 768]
  │
  ├─► Image Encoder (ResNet-152)
  │   └─► Image features: [batch, 7, 49, 2048]
  │
  ├─► ROI Encoder (ResNet-152)
  │   └─► ROI features: [batch, 7, 4, 2048]
  │
  ├─► Cross-Modal Fusion
  │   ├─► Text-Image Attention
  │   ├─► Text-ROI Attention (Geometric-aware)
  │   └─► Multimodal Encoder
  │
  └─► Classifier
      └─► Output: [batch, 6 aspects, 4 sentiments]
```

# References
