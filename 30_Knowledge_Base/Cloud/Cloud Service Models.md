# Cloud Service Models

tags: #cloud #gcp #kubernetes #infrastructure

## Mô hình Cloud service

Phân biệt nhau ở chỗ **nhà cung cấp quản lý đến layer nào** trong stack.

| | On-Premises | IaaS | PaaS | SaaS |
|---|---|---|---|---|
| Phần cứng | Bạn | Nhà CC | Nhà CC | Nhà CC |
| OS | Bạn | Bạn | Nhà CC | Nhà CC |
| Runtime / Middleware | Bạn | Bạn | Nhà CC | Nhà CC |
| Ứng dụng | Bạn | Bạn | Bạn | Nhà CC |
| Dữ liệu | Bạn | Bạn | Bạn | Nhà CC |

Thứ tự kiểm soát từ cao xuống thấp:
```
On-Premises > IaaS > PaaS > SaaS
```

### On-Premises
Tự sở hữu và vận hành toàn bộ: mua phần cứng, đặt trong data center hoặc server room, tự quản lý từ tầng vật lý lên đến ứng dụng.

### IaaS — Infrastructure as a Service
Thuê tài nguyên phần cứng ảo hóa: CPU, RAM, ổ đĩa, băng thông. Tự quản lý OS trở lên.
- Ví dụ: AWS EC2, Google Compute Engine, Azure VM

### PaaS — Platform as a Service
Nhà cung cấp quản lý OS, runtime, middleware. Chỉ cần đẩy code lên.
- Ví dụ: Heroku, Render, Google App Engine

### SaaS — Software as a Service
Nhà cung cấp quản lý toàn bộ stack. Người dùng chỉ truy cập qua trình duyệt hoặc API.
- Ví dụ: Gmail, Notion, Figma, Slack

---

## GCP — Tổng quan dịch vụ

### Compute
| Dịch vụ | Mô tả |
|---|---|
| Compute Engine | Máy ảo (IaaS) |
| GKE | Chạy container với Kubernetes |
| Cloud Run | Container serverless, tự scale |
| Cloud Functions | Serverless function, trigger theo event |

### Data Store
| Dịch vụ | Mô tả |
|---|---|
| Cloud Storage | Lưu trữ file/object |
| BigQuery | Data warehouse, truy vấn SQL trên dữ liệu lớn |
| Cloud Bigtable | NoSQL hiệu năng cao, dùng cho time-series, IoT |

### Data Processing
| Dịch vụ | Mô tả |
|---|---|
| Dataproc | Chạy Hadoop/Spark cluster |
| Pub/Sub | Message queue, event-driven architecture |
| Dataflow | Pipeline xử lý streaming và batch (Apache Beam) |

### AI Platform
| Dịch vụ | Mô tả |
|---|---|
| Vertex AI | Train, deploy và quản lý ML model |

---

## Kiến trúc ML trên GCP

Luồng điển hình cho Serverless Prediction at Scale:

```
Client → Internet → Apigee (API Proxy) → Cloud Function → Model Container (CAIP) → response
```

- **Apigee**: API gateway, xử lý auth, rate limiting, routing
- **Cloud Function**: serverless, triggered on call, tiền xử lý input
- **Model Container**: đóng gói ML model, chạy inference
- Cả hai đều chạy **multiple instances**, tự scale theo request

Có thể mở rộng thêm: preprocessing, routing theo model version, logging.

---

## Network: Inbound vs Outbound

Định nghĩa từ góc nhìn của server/hệ thống:

- **Inbound**: traffic từ bên ngoài gửi **vào** server
- **Outbound**: traffic từ server gửi **ra** ngoài

Quan trọng khi cấu hình firewall / security group — phải set rule riêng cho từng chiều.

---

## Quy trình kết nối GKE cluster

```bash
gcloud auth login
gcloud config set project <PROJECT_ID>
gcloud container clusters get-credentials <CLUSTER_NAME> --region <REGION> --project <PROJECT_ID>
kubectx         # xem và switch context
k9s             # TUI quản lý cluster
```
