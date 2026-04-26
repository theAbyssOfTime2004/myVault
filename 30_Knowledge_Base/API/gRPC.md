2026-04-26


Tags: [[api]], [[grpc]], [[backend]], [[networking]], [[protobuf]]

# gRPC

> [!info] gRPC (Google Remote Procedure Call) là một framework RPC hiệu năng cao, chạy trên HTTP/2, dùng Protocol Buffers để serialize dữ liệu. Thay vì gọi URL và truyền JSON, client gọi function trực tiếp trên server như thể nó là local function — phần mạng được framework xử lý hoàn toàn.

---

## 1. Hai thành phần nền tảng

### Protocol Buffers (protobuf)

Là format serialize nhị phân do Google phát triển. Thay vì JSON:

```json
{"user_id": 1, "name": "Mai Dang", "age": 25}
```

protobuf encode thành binary compact hơn nhiều (~3-10x nhỏ hơn, parse nhanh hơn ~5-10x).

Schema được định nghĩa trong file `.proto`:

```protobuf
syntax = "proto3";

message User {
  int32 user_id = 1;
  string name = 2;
  int32 age = 3;
}
```

Từ file `.proto`, protobuf compiler (`protoc`) generate ra code client và server stub cho ngôn ngữ bạn chọn (Python, Go, Java, ...).

### HTTP/2

gRPC chạy trên HTTP/2, tận dụng các tính năng:

- **Multiplexing**: Nhiều request/response chạy song song trên một TCP connection, không bị head-of-line blocking như HTTP/1.1.
- **Header compression (HPACK)**: Headers được compress, giảm overhead.
- **Binary framing**: Dữ liệu truyền dưới dạng binary frame thay vì text.
- **Server push** và **bidirectional streaming**: Native support.

---

## 2. Định nghĩa Service

Mọi thứ bắt đầu từ file `.proto`:

```protobuf
syntax = "proto3";

service OrderService {
  // Unary: client gửi 1 request, server trả 1 response
  rpc GetOrder (GetOrderRequest) returns (Order);

  // Server streaming: client gửi 1 request, server stream nhiều response
  rpc WatchOrderStatus (GetOrderRequest) returns (stream OrderStatusUpdate);

  // Client streaming: client stream nhiều request, server trả 1 response
  rpc UploadOrderItems (stream OrderItem) returns (UploadResult);

  // Bidirectional streaming: cả hai bên stream đồng thời
  rpc Chat (stream ChatMessage) returns (stream ChatMessage);
}

message GetOrderRequest { int32 order_id = 1; }
message Order { int32 id = 1; string status = 2; float total = 3; }
message OrderStatusUpdate { string status = 1; string timestamp = 2; }
```

---

## 3. Bốn loại RPC

| Loại | Client | Server | Use case |
|---|---|---|---|
| Unary | 1 request | 1 response | Phần lớn CRUD operations |
| Server streaming | 1 request | nhiều response | Real-time update, large dataset |
| Client streaming | nhiều request | 1 response | Upload file lớn theo chunk |
| Bidirectional streaming | nhiều request | nhiều response | Chat, collaborative editing |

---

## 4. Workflow thực tế

```
1. Viết file .proto (định nghĩa service + message)
        │
        ▼
2. Chạy protoc → generate server stub + client stub
        │
        ▼
3. Server implement logic vào server stub
        │
        ▼
4. Client dùng generated client stub để gọi như local function
```

**Phía Python server:**
```python
class OrderServiceServicer(order_pb2_grpc.OrderServiceServicer):
    def GetOrder(self, request, context):
        order = db.get(request.order_id)
        return order_pb2.Order(id=order.id, status=order.status)
```

**Phía Go client:**
```go
conn, _ := grpc.Dial("order-service:50051", grpc.WithTransportCredentials(...))
client := order_pb2.NewOrderServiceClient(conn)
resp, _ := client.GetOrder(ctx, &order_pb2.GetOrderRequest{OrderId: 42})
```

Client gọi `GetOrder` như local function — framework serialize request thành binary, gửi qua HTTP/2, nhận binary response, deserialize thành struct.

---

## 5. gRPC vs REST

| | REST | gRPC |
|---|---|---|
| Protocol | HTTP/1.1 (thường) | HTTP/2 |
| Serialization | JSON (text) | Protobuf (binary) |
| Schema | Không bắt buộc (OpenAPI optional) | Bắt buộc (`.proto` file) |
| Code generation | Không | Có (client + server stub) |
| Streaming | Không native | Native (4 loại) |
| Browser support | Tốt | Hạn chế (cần gRPC-Web proxy) |
| Debug | Dễ (curl, Postman) | Khó hơn (cần grpcurl, Postman gRPC) |
| Latency | Cao hơn | Thấp hơn |

---

## 6. Ví dụ thực tế

**Hệ thống microservices e-commerce:**

- `api-gateway` nhận REST request từ mobile app (vì browser/mobile không hỗ trợ tốt gRPC)
- `api-gateway` gọi nội bộ `order-service`, `inventory-service`, `payment-service` qua gRPC
- `order-service` dùng server streaming để push trạng thái đơn hàng real-time cho `notification-service`

Lý do dùng gRPC cho internal: Các service gọi nhau hàng nghìn lần/giây, latency thấp và throughput cao quan trọng hơn debuggability. Schema `.proto` đóng vai trò contract giữa các team.

**Inference serving:**

KServe và Triton Inference Server dùng gRPC với V2 Open Inference Protocol vì:
- Model input/output thường là tensor (float array lớn) — binary protobuf hiệu quả hơn JSON nhiều
- Client streaming cho phép gửi nhiều inference request trong một connection

---

## 7. Khi nào không nên dùng gRPC

- API public expose ra browser: Browser không hỗ trợ gRPC trực tiếp, phải dùng gRPC-Web + proxy (Envoy) — phức tạp không cần thiết.
- Team nhỏ, tốc độ iteration quan trọng: Phải maintain `.proto` file, chạy codegen, đồng bộ giữa các service — overhead đáng kể so với REST.
- Khi cần human-readable payload để debug dễ dàng.
