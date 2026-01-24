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


**FLOW**:

```
┌─────────────────────────────────────────────────────────────┐
│  PHASE 0: Prepare Image/ROI Aspect Labels                 │
│  prepare_image_roi_labels.py + Train classifiers          │
│  └─► Extract image/ROI aspects từ dataset                  │
│  └─► Train image/ROI classifiers                           │
│  └─► Generate: resnet152_image_label.json                  │
│  └─► Generate: resnet152_roi_label.json                    │
└─────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│  PHASE 1: Prepare ROI Labels                                │
│  prepare_image_roi_labels.py                               │
│  └─► Extract bbox + aspect từ dataset                       │
│  └─► Tạo CSV: roi_labels.csv                                │
└─────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│  PHASE 2: Training Dataset                                  │
│  vimacsa_dataset.py                                         │
│  ├─► Text Processing:                                       │
│  │   └─► Format: "[aspect] </s></s> review </s></s>        │
│  │              image_aspects </s></s> roi_aspects"        │
│  │   └─► Tokenize: [batch, 6, seq_len] (6 aspects)         │
│  ├─► Image Processing:                                      │
│  │   └─► Load 7 images: [batch, 7, 3, 224, 224]            │
│  └─► ROI Processing:                                       │
│      └─► Crop ROI từ bbox: [batch, 7, 4, 3, 224, 224]      │
│      └─► Normalize coords: [batch, 7, 4, 4]                │
└─────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│  PHASE 3: Extract Visual Features                           │
│  run_multimodal_fcmf.py (Training Loop)                     │
│  ├─► Image Features:                                        │
│  │   └─► ResNet-152: [batch, 7, 3, 224, 224]               │
│  │   └─► Output: [batch, 7, 49, 2048]                      │
│  └─► ROI Features:                                          │
│      └─► ResNet-152: [batch, 7, 4, 3, 224, 224]            │
│      └─► Output: [batch, 7, 4, 2048]                       │
└─────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│  PHASE 4: FCMF Model (Per-Aspect Processing)               │
│  fcmf_framework/fcmf_modeling.py                            │
│  └─► For each aspect (6 aspects):                          │
│      ├─► Text Encoder: [batch, seq_len, 768]                │
│      ├─► Text-Image Attention: [batch, 768]                │
│      ├─► Text-ROI Attention (Geometric): [batch, 768]      │
│      ├─► Multimodal Fusion: [batch, 768]                   │
│      └─► Classify: [batch, 4] (None/Neg/Neu/Pos)           │
│  └─► Final: [batch, 6, 4] (6 aspects × 4 sentiments)        │
└─────────────────────────────────────────────────────────────┘
```



# References
