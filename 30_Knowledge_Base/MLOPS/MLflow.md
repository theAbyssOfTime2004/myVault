---
tags:
  - mlops
  - experiment-tracking
  - mlflow
created: 2026-05-15
---

# MLflow

## Tổng quan

MLflow là nền tảng mã nguồn mở để quản lý vòng đời ML, trọng tâm là **experiment tracking** — ghi lại có hệ thống các lần train model để so sánh, tái lập và lựa chọn baseline.

**Vấn đề cần giải quyết:** Quy trình CRISP-DM yêu cầu lặp đi lặp lại Preprocess → Choose Model → Train → Evaluate nhiều lần (đổi feature, đổi kiến trúc, tune hyperparameter) trước khi chọn được baseline để deploy. Không có công cụ tracking, các lần thử nghiệm sẽ thất lạc, không so sánh được, không tái lập được.

---

## Vai trò trong CRISP-DM

```
Raw Data → Preprocessed Data → Choose Model → Train → Evaluate → Baseline → Deploy
                ↑                    ↑              ↓
                └── đổi method ──────┴── đổi arch / tune HP ──┘
```

Mỗi vòng lặp là một **experiment run** — MLflow ghi lại để biết run nào ra baseline.

---

## Core Capabilities

### I. Performance Comparison
- **Baseline vs new experiments:** so sánh model mới với baseline hoặc version trước bằng metric chuẩn (Accuracy, MAPE, R2, AUC/PR).
- **Metric dashboards:** visualize trend performance theo thời gian / theo dataset → phát hiện overfitting hoặc performance drop sớm.
- **Hyperparameter impact analysis:** track xem learning rate, batch size, kiến trúc, regularization ảnh hưởng final performance ra sao.
- **Cross-dataset evaluation:** đánh giá model trên nhiều domain / cohort khác nhau.

### Các thành phần thường dùng
- **Tracking:** log params, metrics, artifacts, source code version cho mỗi run.
- **Projects:** đóng gói code dạng reproducible (conda/pip env + entry points).
- **Models:** format chuẩn để serve nhiều framework (sklearn, pytorch, ...).
- **Model Registry:** quản lý stage (Staging / Production / Archived) và version của model.

---

## Khái niệm chính

- **Experiment:** nhóm các run cùng mục tiêu (ví dụ "tune XGBoost cho churn").
- **Run:** một lần execute training với params cụ thể, sinh ra metrics và artifacts.
- **Params:** input cấu hình (hyperparameter, config).
- **Metrics:** output đo lường (loss, accuracy, ...), có thể log theo step.
- **Artifacts:** file output (model, plot, confusion matrix, ...).

---

## Liên hệ

- [[DVC]] — MLflow track experiments + metrics; DVC version dataset/model file lớn. Hai công cụ bổ trợ nhau.
- [[Model Serving Patterns]] — sau khi chọn baseline qua MLflow, model được đẩy sang serving.
