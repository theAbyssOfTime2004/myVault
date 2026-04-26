2026-04-26


Tags: [[api]], [[websocket]], [[backend]], [[networking]], [[realtime]]

# WebSocket

> [!info] WebSocket là một giao thức cho phép duy trì một kết nối TCP liên tục (persistent) giữa client và server. Sau khi kết nối được thiết lập, cả hai bên có thể gửi dữ liệu cho nhau bất cứ lúc nào mà không cần mở lại kết nối mới — đây là full-duplex communication.

---

## 1. Vấn đề HTTP giải quyết không tốt

HTTP được thiết kế theo mô hình request-response: client gửi request, server phản hồi, kết nối đóng (hoặc reuse cho request tiếp theo với keep-alive, nhưng server không thể chủ động gửi dữ liệu).

Với ứng dụng cần real-time (chat, live dashboard, collaborative editor), có các workaround trên HTTP:

**Short polling:** Client gọi `GET /messages` mỗi N giây. Đơn giản nhưng độ trễ cao, request thừa nhiều.

**Long polling:** Client gửi request, server giữ request đó mở cho đến khi có dữ liệu mới (hoặc timeout). Giảm request thừa nhưng:
- Mỗi "push" vẫn cần một HTTP request mới
- Server phải quản lý nhiều request đang treo
- Không efficient ở scale lớn

**Server-Sent Events (SSE):** Server stream dữ liệu một chiều về client qua HTTP. Phù hợp khi chỉ cần server → client (VD: live feed). Không hỗ trợ client → server trên cùng connection.

WebSocket giải quyết cả hai chiều trên một kết nối duy nhất.

---

## 2. WebSocket Handshake

WebSocket bắt đầu bằng HTTP Upgrade request:

**Client gửi:**
```http
GET /chat HTTP/1.1
Host: yourapp.com
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==
Sec-WebSocket-Version: 13
```

**Server phản hồi:**
```http
HTTP/1.1 101 Switching Protocols
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Accept: s3pPLMBiTxaQ9kYGzzhZRbK+xOo=
```

Sau `101 Switching Protocols`, kết nối được nâng cấp từ HTTP lên WebSocket protocol. TCP connection vẫn giữ nguyên, nhưng từ đây dữ liệu truyền theo WebSocket frame format, không phải HTTP.

---

## 3. WebSocket Frame

Dữ liệu truyền qua WebSocket được đóng gói trong **frame**:

```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-------+-+-------------+-------------------------------+
|F|R|R|R| opcode|M| Payload len |    Extended payload length    |
|I|S|S|S|  (4)  |A|     (7)     |             (16/64)           |
|N|V|V|V|       |S|             |                               |
| |1|2|3|       |K|             |                               |
+-+-+-+-+-------+-+-------------+-------------------------------+
```

**Opcodes quan trọng:**
- `0x1`: Text frame (UTF-8)
- `0x2`: Binary frame
- `0x8`: Close
- `0x9`: Ping
- `0xA`: Pong

Ping/Pong là heartbeat mechanism built-in: server gửi Ping, client phải trả Pong để xác nhận kết nối vẫn sống.

---

## 4. Quản lý kết nối ở server

Mỗi WebSocket connection là một kết nối TCP tồn tại lâu dài. Server cần quản lý nhiều connection đồng thời:

**Vấn đề với thread-per-connection model:**
- 10,000 user đồng thời = 10,000 thread đang chờ → tốn bộ nhớ, context switch overhead lớn

**Giải pháp — event-driven / async I/O:**
- Node.js (event loop), Python asyncio, Go goroutine xử lý nhiều connection trên ít thread
- Mỗi connection được track bằng một object trong memory

```python
# FastAPI + WebSocket
connected_clients: dict[str, WebSocket] = {}

@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    await websocket.accept()
    connected_clients[user_id] = websocket
    try:
        while True:
            data = await websocket.receive_text()
            await handle_message(user_id, data)
    except WebSocketDisconnect:
        del connected_clients[user_id]
```

---

## 5. Scale ngang với WebSocket

**Vấn đề:**

User A kết nối vào Server 1. User B kết nối vào Server 2. User A gửi tin nhắn cho User B — Server 1 không có connection của User B.

**Giải pháp — Pub/Sub broker:**

```
User A → Server 1 → publish "to:UserB" → Redis Pub/Sub ← subscribe ← Server 2 → User B
```

Mỗi server subscribe vào channel trên Redis (hoặc Kafka, NATS). Khi nhận message, publish lên broker, broker fan-out đến server nào đang giữ connection của recipient.

---

## 6. Ví dụ thực tế

**Chat app:**

1. User A mở app, client tạo WebSocket connection: `wss://chat.yourapp.com/ws`
2. User A gõ tin nhắn, client gửi frame: `{"to": "userB", "text": "hello"}`
3. Server nhận, lookup User B đang ở server nào, route qua Redis Pub/Sub
4. Server giữ connection của User B push frame về client của User B
5. Client B nhận, render tin nhắn — không có HTTP request nào trong bước 2-5

**Live dashboard (chỉ cần server → client):**

1. Admin mở dashboard monitoring, client tạo WebSocket connection
2. Server mỗi giây query metrics và push frame: `{"cpu": 72, "mem": 85, "rps": 1240}`
3. Client nhận, update chart

> [!note] Trường hợp chỉ cần server → client, SSE (Server-Sent Events) đơn giản hơn và đủ dùng. WebSocket chỉ cần thiết khi client cũng cần gửi dữ liệu realtime về server trên cùng connection.

---

## 7. Reconnection

WebSocket connection có thể bị ngắt do network instability, server restart, proxy timeout. Client cần tự implement reconnection logic:

```javascript
function createConnection() {
  const ws = new WebSocket("wss://yourapp.com/ws");

  ws.onclose = (event) => {
    if (!event.wasClean) {
      // Unexpected disconnect — reconnect sau delay
      setTimeout(createConnection, 3000);
    }
  };

  ws.onmessage = (event) => { /* xử lý */ };
  return ws;
}
```

Exponential backoff thường được dùng thay vì fixed delay để tránh thundering herd khi server restart.

---

## 8. So sánh tổng quan

| | REST | WebSocket | Webhook | SSE |
|---|---|---|---|---|
| Hướng dữ liệu | Client → Server → Client | Bidirectional | Server → Server | Server → Client |
| Kết nối | Stateless | Persistent | Stateless | Persistent (HTTP) |
| Protocol | HTTP | WebSocket (trên TCP) | HTTP | HTTP |
| Real-time | Không (cần polling) | Có | Không (event-driven) | Có (1 chiều) |
| Browser support | Tốt | Tốt | N/A | Tốt |
| Use case | CRUD, request-response | Chat, live collab, gaming | Payment callback, CI trigger | Live feed, notification |
