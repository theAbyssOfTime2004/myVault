Ok, lùi lại một bước. Vấn đề không phải là công thức, mà là **hình dung ra hiện tượng vật lý** trước khi tính. Đây là bài kinh điển "vận động viên trượt băng xoay tròn" — chỉ đổi thành "người đứng trên bàn quay".

## Hình dung tình huống

Tưởng tượng bạn ngồi trên ghế văn phòng loại xoay được, ai đó đẩy cho bạn quay. Ban đầu bạn dang hai tay ra (như chữ T). Sau đó bạn thu tay lại ôm sát người. Bạn sẽ **tự thấy mình quay nhanh hẳn lên** — không cần ai đẩy thêm. Đó chính xác là hiện tượng bài này mô tả. "Bàn quay" + "người" chỉ là 1 hệ vật rắn đang quay quanh 1 trục thẳng đứng.

## Vì sao mômen quán tính $I$ thay đổi?

$I$ đo "khối lượng nằm xa trục quay bao nhiêu" — không phải khối lượng người thay đổi, mà là **cách khối lượng đó phân bố quanh trục** thay đổi:

- Tay dang rộng → khối lượng tay/bàn tay ở xa trục → $I$ lớn ($I_i = 6{,}0$)
- Tay khép lại sát người → khối lượng đó dồn về gần trục → $I$ nhỏ ($I_f = 2{,}0$)

## Vì sao dùng bảo toàn **mômen động lượng** chứ không phải năng lượng?

Đây là chỗ hay nhầm nhất. Câu hỏi cần tự đặt ra: _"có lực/mômen nào từ bên ngoài hệ tác động lên hệ 'người + bàn' không?"_

- Bỏ qua ma sát ở trục quay → không có mômen cản từ bên ngoài.
- Lực người dùng để **kéo tay vào** là lực cơ bắp — lực này là **nội lực** (một phần cơ thể tác dụng lên phần khác của chính cơ thể), giống hệt lý do tại sao 2 người đẩy nhau trên sân băng thì tổng động lượng vẫn bảo toàn dù mỗi người tự tạo lực.

→ Không có mômen ngoại lực ⇒ $L = I\omega$ giữ nguyên trong suốt quá trình, kể cả khi $I$ và $\omega$ đều đang biến đổi liên tục. Đó là lý do được phép viết $I_i\omega_i = I_f\omega_f$ dù $I$ thay đổi ở giữa.

## Vì sao động năng lại KHÔNG bảo toàn, dù $L$ bảo toàn?

Vì $K=\frac12 I\omega^2$ không phải là cùng một đại lượng với $L=I\omega$ — chúng biến thiên khác nhau khi $I,\omega$ thay đổi. Việc $K$ tăng lên không vi phạm gì cả, vì **năng lượng KHÔNG bị bắt buộc bảo toàn** ở đây — chỉ có $L$ mới bị bắt buộc (do không có mômen ngoại lực). Năng lượng bổ sung đến từ nơi khác: chính là công cơ bắp người bỏ ra để kéo tay vào (giống việc bạn nhảy lên thì động năng "từ đâu ra" — từ năng lượng hóa học trong cơ, không phải từ hư không).

## Cách tiếp cận chung cho dạng bài này

1. Đọc đề, tìm dấu hiệu: "mômen quán tính", "tốc độ góc", "bỏ qua ma sát" → đây là bài quay, không phải tịnh tiến.
2. Tự hỏi: có mômen ngoại lực nào tác động không? Nếu không → $L=I\omega$ = const, viết được phương trình bảo toàn ngay.
3. Việc gì thay đổi ($I$) và việc gì hỏi ($\omega_f$) → đại số đơn giản từ bước 2.
4. Nếu đề hỏi thêm về năng lượng → tính riêng $K=\frac12I\omega^2$ ở 2 thời điểm, **không giả định nó bảo toàn**.