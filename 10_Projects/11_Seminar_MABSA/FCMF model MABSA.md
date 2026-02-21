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

Tóm lại, quy trình bắt đầu từ dataset gốc, ta chạy prepare_image_roi_labels.py để trích xuất bounding box và aspect labels, kết quả được lưu vào file roi_labels.csv.

Trong quá trình chuẩn bị dữ liệu cho training (Dataset class), ta thực hiện hai việc song song:

Thứ nhất, đối với văn bản, ta tạo thêm các câu phụ trợ (auxiliary sentences) chứa thông tin aspect của ảnh và ROI, sau đó tokenize toàn bộ bằng XLM-RoBERTa.

Thứ hai, đối với hình ảnh, ta thực hiện cắt (crop) và chuẩn hóa (normalize) các vùng ROI dựa trên tọa độ từ file CSV đã chuẩn bị.

Bước vào vòng lặp training (training loop), ta sử dụng mạng ResNet-152 (pretrained trên ImageNet) để trích xuất đặc trưng thị giác. Cụ thể là trích xuất đặc trưng toàn cục cho 7 ảnh và đặc trưng cục bộ cho 28 vùng ROI (4 ROI mỗi ảnh).

Các đặc trưng này sau đó được đưa vào mô hình FCMF. Tại đây, luồng xử lý diễn ra song song cho từng aspect category. Đầu tiên, mô hình dùng XLM-RoBERTa để mã hóa đặc trưng văn bản. Tiếp theo, ta sử dụng cơ chế Attention đa tầng: lớp đầu tiên cầu nối (bridge) giữa đặc trưng văn bản và đặc trưng toàn cục của ảnh; lớp thứ hai là Geometric ROI-aware Attention giúp liên kết văn bản với từng vùng ROI cụ thể, có tính đến cả vị trí không gian của chúng. Cuối cùng, tất cả thông tin được tổng hợp qua bộ mã hóa đa phương thức (Multimodal Encoder) để đưa ra dự đoán đồng thời về cả aspect và sentiment trong một lần chạy duy nhất.
![[Pasted image 20260124221623.png]]

# References
