## Hình dung tình huống

Bạn có 1 ấm nhôm chứa nước, đặt trên bếp điện đang cấp nhiệt liên tục và đều đặn (công suất không đổi). Nhiệt đi vào hệ "ấm + nước" nhưng làm **2 việc khác nhau, theo trình tự trước-sau**:

1. **Giai đoạn 1 — làm nóng lên:** nhiệt làm nhiệt độ của cả ấm lẫn nước tăng dần từ 27°C lên tới 100°C (nhiệt độ sôi). Trong giai đoạn này, nhiệt độ còn đang thay đổi.
2. **Giai đoạn 2 — hóa hơi:** khi nước đã đạt 100°C, nó bắt đầu sôi. Nhiệt tiếp tục đổ vào nhưng **không làm nhiệt độ tăng thêm nữa** — toàn bộ nhiệt lúc này dùng để "bứt" các phân tử nước khỏi thể lỏng thành thể hơi. Chỉ có 400g trong 2,0kg nước làm được việc này sau 30 phút, phần còn lại vẫn ở dạng lỏng tại 100°C.

Đây là lý do vì sao bạn không thể dùng 1 công thức duy nhất — phải tách 2 giai đoạn, dùng đúng công cụ cho từng giai đoạn:

- Giai đoạn có $\Delta T$ (nhiệt độ đổi) → $Q=mc\Delta T$
- Giai đoạn nhiệt độ đứng yên nhưng đổi thể (lỏng→hơi) → $Q=mL$

## Vì sao cộng cả ấm nhôm vào?

Ấm không phải "vật chứa vô hình" — bản thân khối kim loại 700g cũng hấp thụ nhiệt và nóng lên cùng lúc với nước (từ 27°C lên 100°C, cùng $\Delta T$). Vì nước và nhôm có nhiệt dung riêng khác nhau, phải tính $Q$ cho từng vật riêng ($m_{nước}c_{nước}\Delta T$ và $m_{ấm}c_{nhôm}\Delta T$) rồi mới cộng lại — không được gộp chung khối lượng vào 1 công thức vì $c$ khác nhau.

**Bẫy cần tránh:** ở bước hóa hơi, khối lượng dùng trong $Q=mL$ chỉ là phần **đã hóa hơi (400g)**, không phải toàn bộ 2,0kg nước.

## Vì sao có con số 80%?

Đây là bài toán "hiệu suất sử dụng năng lượng" — bếp tỏa ra tổng cộng một lượng nhiệt nào đó trong 30 phút, nhưng không phải tất cả đều đi vào ấm nước (một phần thất thoát ra không khí xung quanh). Chỉ 80% lượng bếp tỏa ra là "có ích" (đi vào đun nước+ấm+hóa hơi). Vậy:

$\text{nhiệt có ích (}=Q_1+Q_2\text{)} = 80 \% \times \text{tổng nhiệt bếp tỏa ra}$

Từ đó suy ngược ra tổng nhiệt bếp tỏa ra, rồi vì bếp có **công suất không đổi**, công suất = tổng nhiệt / thời gian (nhớ đổi 30 phút → giây).

## Tóm tắt các bước tự làm

1. Tính $Q_1$: nhiệt làm nóng nước + ấm từ 27°C → 100°C (2 số hạng, cộng lại).
2. Tính $Q_2$: nhiệt hóa hơi đúng 400g nước tại 100°C.
3. $Q = Q_1+Q_2$ — đây là đáp số câu a.
4. Suy ra tổng nhiệt bếp thực tỏa ra từ tỉ lệ 80%, rồi chia cho thời gian (giây) ra công suất — đáp số câu b.
Đúng, đây là thói quen rất tốt — giúp tránh sót dữ kiện và tránh nhầm đơn vị. Ví dụ áp dụng cho Câu 2:

**Ta có:**

- $m_{ấm} = 0{,}7$ kg (nhôm), $c_{nhôm} = 880$ J/(kg.K)
- $m_{nước} = 2{,}0$ kg, $c_{nước} = 4200$ J/(kg.K)
- $t_1 = 27°C$, $t_2 = 100°C$ (nhiệt độ sôi)
- Hiệu suất sử dụng nhiệt của bếp: $H = 80\%$
- Thời gian đun: $\Delta t = 30$ phút $= 1800$ s
- Khối lượng nước đã hóa hơi: $m_{hơi} = 0{,}4$ kg
- $L = 2{,}3\times10^6$ J/kg

**Tìm:**
a) $Q$ (tổng nhiệt đun nóng + hóa hơi)
b) $P$ (công suất bếp)

Vài lưu ý khi tóm tắt kiểu này:

- Liệt kê **cả đơn vị gốc** đề cho, để không quên đổi (30 phút → giây, hay nếu đề cho nhiệt độ °C mà công thức cần K thì phải đổi ngay ở bước này).
- Tách rõ **dữ kiện nào thuộc vật nào** (nước vs ấm) — nhất là khi có 2 chất khác nhau dùng chung 1 bài, dễ gán nhầm $c$ cho sai vật.
- Ghi rõ **đại lượng nào là "một phần"** (như $m_{hơi}=0,4$ khác với $m_{nước}=2,0$) ngay từ bước tóm tắt để không lẫn lộn lúc thế vào công thức.

Cách này áp dụng được cho mọi câu, kể cả các bài chu trình khí (Câu 4) — tóm tắt hết $V_1, V_2, V_3, P_1, T_1$... và loại quá trình từng đoạn trước khi tính, sẽ đỡ rối hơn nhiều.