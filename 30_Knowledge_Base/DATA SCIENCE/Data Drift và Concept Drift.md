2026-04-26


Tags: [[mlops]], [[data-science]], [[model-monitoring]], [[drift]]

# Data Drift và Concept Drift

> [!info] Cả hai đều là hiện tượng khiến performance của model suy giảm theo thời gian sau khi deploy — nhưng nguyên nhân gốc rễ khác nhau và cách phát hiện cũng khác nhau.

---

## 1. Data Drift (Input Drift)

Phân phối của input data thay đổi so với lúc model được train — tức là `P(X)` thay đổi.

Model vẫn đúng về mặt logic: nếu được train lại trên data mới, nó vẫn học được. Vấn đề là model hiện tại chưa từng thấy vùng phân phối mới, nên prediction ở đó kém tin cậy.

**Ví dụ:** Model phân loại ảnh sản phẩm được train trên ảnh chụp ban ngày, ánh sáng tốt. Sau khi deploy, user bắt đầu upload ảnh chụp ban đêm, góc nghiêng. Phân phối pixel thay đổi — model predict sai nhiều hơn dù quy tắc phân loại không đổi.

**Phát hiện:** So sánh phân phối feature của production data với training data bằng statistical test:
- **KS Test (Kolmogorov-Smirnov)**: So sánh CDF của hai phân phối, phù hợp với continuous feature.
- **PSI (Population Stability Index)**: Đo mức độ shift giữa hai phân phối dạng bucket. PSI < 0.1 ổn định, 0.1–0.2 cần theo dõi, > 0.2 shift đáng kể.
- **Chi-squared test**: Phù hợp với categorical feature.

Không cần label — chỉ cần input data là đủ để phát hiện.

---

## 2. Concept Drift (Label Drift)

Mối quan hệ giữa input `X` và output `y` thay đổi — tức là `P(y|X)` thay đổi. Bản thân "đáp án đúng" thay đổi theo thời gian, dù input distribution có thể không đổi.

**Ví dụ 1:** Model credit scoring được train năm 2019. Năm 2020 (COVID), hành vi tài chính thay đổi — cùng một profile khách hàng (income, lịch sử tín dụng) nhưng khả năng default cao hơn nhiều. Input `X` không đổi, nhưng `P(y|X)` đã đổi.

**Ví dụ 2:** Model spam filter train năm 2022. Spammer thay đổi chiến thuật, dùng từ ngữ mới. Cùng cấu trúc email nhưng label "spam/not spam" đã khác.

**Phát hiện:** Khó hơn data drift vì **bắt buộc phải có ground truth label từ production**. Cần feedback loop: user report, human labeling, hoặc delayed label (VD: model dự đoán user churn, 30 ngày sau mới biết user có churn thật không).

Nếu không có label, chỉ phát hiện được gián tiếp qua:
- Prediction distribution shift (output của model thay đổi bất thường)
- Business metric degradation (conversion rate, accuracy trên sample nhỏ được label thủ công)

---

## 3. So sánh

| | Data Drift | Concept Drift |
|---|---|---|
| Cái thay đổi | Phân phối input `P(X)` | Quan hệ `P(y\|X)` |
| Nguyên nhân | Thay đổi hành vi user, data source, mùa vụ | Thay đổi thực tế trong thế giới |
| Cần label để phát hiện | Không | Có |
| Phát hiện bằng | Statistical test trên input | Accuracy monitoring, feedback loop |
| Xử lý | Retrain hoặc fine-tune trên data mới | Retrain bắt buộc, có thể cần relabel |

---

## 4. Các dạng Concept Drift

| Dạng | Mô tả |
|---|---|
| **Sudden drift** | Thay đổi đột ngột tại một thời điểm (VD: chính sách thay đổi) |
| **Gradual drift** | Thay đổi dần dần theo thời gian |
| **Recurring drift** | Drift theo chu kỳ (VD: hành vi mua sắm mùa lễ) |
| **Incremental drift** | Thay đổi nhỏ liên tục tích lũy |

---

## 5. Monitoring pipeline thực tế

```
Production data ──► Feature Store
                         │
                    ┌────▼─────┐
                    │  Drift   │  ← so sánh với training distribution
                    │ Monitor  │
                    └────┬─────┘
                         │ drift detected
                         ▼
                      Broker (Knative Eventing / Kafka)
                         │
                         ▼
                    Alert (Webhook → Slack)
                    + Retrain trigger
```

Trong hệ thống dùng KServe, **Drift Prediction Service** đóng vai trò monitor này — nhận inference event từ serving service qua Knative Eventing broker, chạy statistical test, và gửi webhook alert khi phát hiện drift.

---

## 6. Liên quan

- [[Model Serving Patterns]] — kiến trúc hệ thống có tích hợp drift monitoring
- [[KServe và CRD]] — serving framework trên K8s nơi drift monitor được gắn vào
- [[Webhook]] — cơ chế gửi alert khi phát hiện drift
