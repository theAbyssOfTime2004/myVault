2026-05-02


Tags: [[devops]], [[ci-cd]], [[automation]], [[deployment]], [[mlops]]

# CI/CD

---

## 1. Continuous Integration (CI)

**CI** = lập trình viên thường xuyên merge code vào repo trung tâm, sau đó hệ thống **tự động build và test**.

```
Build → Test
```

- **Build**: biên dịch / đóng gói code
- **Test**: chạy unit test, integration test

**Mục tiêu**: phát hiện lỗi sớm khi code vừa được merge, tránh tích tụ bug và hạn chế "merge hell".

---

## 2. Continuous Delivery (CD - Delivery)

Mở rộng CI: **tự động deploy code đã test sang môi trường staging**, sẵn sàng để lên production — nhưng bước cuối **cần người duyệt thủ công**.

```
Build → Test → Acceptance tests → Deploy to staging → [Manual] Deploy to production → Smoke tests
```

- Code lúc nào cũng ở trạng thái **"có thể release"** bất cứ lúc nào.
- Quyết định *khi nào* release vẫn nằm ở con người (release manager, product owner).

---

## 3. Continuous Deployment (CD - Deployment)

Đi xa hơn Delivery: **tự động luôn cả bước deploy lên production**, không có bước duyệt tay.

```
Build → Test → Acceptance tests → Deploy to staging → [Auto] Deploy to production → Smoke tests
```

- Mọi commit pass hết test sẽ **tự động ra production**.
- Yêu cầu **test coverage cao** và **monitoring tốt**, vì không có "lưới an toàn" là con người.

---

## 4. So sánh 3 cấp

| Cấp | Phạm vi tự động | Bước cần người |
|---|---|---|
| CI | Build + Test | Merge, deploy |
| CD (Delivery) | + Acceptance test + Deploy staging | Duyệt deploy production |
| CD (Deployment) | + Deploy production tự động | Không |

---

## 5. CI/CD Pipeline tổng thể

CI/CD là **một pipeline tự động liên tục** kết hợp 2 nửa, thường được vẽ thành biểu tượng vô cực ∞:

- **CI (vòng trái)**: plan → code → build → test
- **CD (vòng phải)**: release → deploy → operate → monitor

**Tool phổ biến theo từng giai đoạn:**

| Giai đoạn | Tool |
|---|---|
| Plan | Jira, Confluence |
| Code | GitHub, GitLab |
| Build | Gradle, webpack, Docker |
| Test | Jest, Playwright, JUnit |
| Release | Jenkins, GitHub Actions |
| Deploy | Argo CD, Spinnaker |
| Operate | Kubernetes, Terraform |
| Monitor | Datadog, Prometheus, Grafana |

**Lợi ích**: cải thiện collaboration giữa Dev và Ops, giảm lỗi thủ công, release nhanh và tin cậy hơn.

---

## 6. CI/CD trong Machine Learning

Khác biệt cốt lõi: **ML pipeline có 3 thành phần biến động** — code, model, data — không chỉ code như software thông thường.

**No ML (truyền thống):**

```
Test (code) → Build → Deploy API
```

**With ML:**

```
Test (code, model, data) → Build → Deploy API
                                 ↘ Deploy pipelines (data/ML)
```

**Khác biệt:**

- Phải test thêm **model** (accuracy, fairness, drift) và **data** (schema, distribution, chất lượng).
- Phải deploy **2 thứ song song**:
  - **Inference API** (serving model)
  - **Pipelines** xử lý data và retrain model
- Cần thêm các bước: data validation, model validation, model registry, automated retraining trigger.

→ Đây là lý do **MLOps** ra đời như một nhánh chuyên biệt của DevOps.

---

## 7. Liên quan

- [[Model Serving Patterns]] — pattern deploy model trong CD stage
- [[K8s]] — orchestration platform thường dùng làm target deploy
- [[Helm]] — package & deploy ứng dụng lên K8s trong pipeline
