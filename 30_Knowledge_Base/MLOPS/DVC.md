---
tags:
  - mlops
  - data-versioning
  - dvc
created: 2026-05-15
---

# DVC (Data Version Control)

## Tổng quan

DVC là công cụ **quản lý và versioning các file lớn** (images, audio, video, text dataset, model weights) trong storage. Triết lý: làm cho dataset/model được track giống cách Git track code, nhưng tối ưu cho file lớn mà Git xử lý không hiệu quả.

---

## Vấn đề: Data luôn thay đổi

| Tuần | Thu thập | Dataset size | Train |
| --- | --- | --- | --- |
| Week 1 | 1,000 mẫu | 1,000 | Model v1 |
| Week 2 | 1,000 mẫu nữa | 2,000 (1k cũ + 1k mới) | Model v2 |
| Week 3 | 2,000 mẫu nữa | 5,000 (3k cũ + 2k mới) | Model v3 |
| ... | ... | ... | ... |

Đến tuần `n`, Model v3 drop performance dramatically → muốn **rollback dataset về Week 2** để debug hoặc retrain.

**Không có Data Versioning:** không biết chính xác 3,000 mẫu nào thuộc Week 2 → không thể tái lập, không debug được nguyên nhân drift.

---

## Key Capabilities

- **Version control** cho dataset, model và large artifacts.
- **Đa dạng storage backend:** local filesystem, S3, GCS, Azure Blob, ...
- **Reproducible pipelines:** định nghĩa stage (preprocess → train → evaluate) với dependency tracking tự động — chỉ chạy lại stage có input thay đổi.

---

## Cơ chế hoạt động (tóm tắt)

1. `dvc add data/train.csv` → DVC tính hash file, lưu file thật trong cache, tạo `data/train.csv.dvc` (metadata nhỏ).
2. File `.dvc` được commit vào Git → Git track metadata, DVC track file thật.
3. `dvc push` đẩy file thật lên remote storage (S3, GCS, ...).
4. Khi `git checkout` commit cũ → `dvc checkout` kéo đúng version dataset tương ứng.

→ Lịch sử Git và lịch sử dataset luôn đồng bộ.

---

## DVC Pipeline (`dvc.yaml`)

Định nghĩa stage với deps và outs:

```yaml
stages:
  preprocess:
    cmd: python preprocess.py
    deps: [raw_data/, preprocess.py]
    outs: [processed/]
  train:
    cmd: python train.py
    deps: [processed/, train.py]
    outs: [model.pkl]
    metrics: [metrics.json]
```

`dvc repro` chỉ chạy lại stage có dep thay đổi → reproducible và tiết kiệm thời gian.

---

## Liên hệ

- [[MLflow]] — MLflow lo experiment tracking (params, metrics, runs); DVC lo dataset/model versioning. Kết hợp: MLflow run log lại commit Git + DVC version → tái lập đầy đủ.

---

## Tham khảo

- Installation guide: https://dvc.org/doc/install
