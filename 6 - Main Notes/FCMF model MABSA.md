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
┌─────────────────────────────────────────────────────────┐
│  Dataset (vimacsa_dataset.py)                          │
│  └─► Crop ROI từ image: image[:, y1:y2, x1:x2]         │
│  └─► Transform: Resize + Normalize                     │
│  └─► Output: roi_img_features [batch, 7, 4, 3, 224, 224]│
└─────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────┐
│  Training Loop (run_multimodal_fcmf.py)                │
│  └─► For each image (7 images):                        │
│      └─► For each ROI (4 ROIs):                        │
│          └─► Extract features: resnet_roi(roi_image)    │
│              └─► ResNet-152 forward pass               │
│              └─► Output: [batch, 2048]                 │
│  └─► Stack: [batch, 7, 4, 2048]                        │ 
└─────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────┐
│  FCMF Model                                             │
│  └─► Input: encoded_roi [batch, 7, 4, 2048]            │
│  └─► Project: [2048] → [768]                            │
│  └─► Geometric attention                                │
│  └─► Multimodal fusion                                  │
└─────────────────────────────────────────────────────────┘
```



# References
