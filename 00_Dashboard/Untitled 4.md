Ok, lùi lại một bước. Vấn đề không phải là công thức, mà là **hình dung ra hiện tượng vật lý** trước khi tính. Đây là bài kinh điển "vận động viên trượt băng xoay tròn" — chỉ đổi thành "người đứng trên bàn quay".

# câu 1
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

# câu 2
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

# câu 3
## Hình dung tình huống

Nhìn hình 2: đây là mặt phẳng nghiêng có ròng rọc đặt ở đỉnh dốc. $m_1$ nằm trên mặt dốc (có ma sát), dây vắt qua ròng rọc ở đỉnh, đầu kia treo $m_2$ lơ lửng thẳng đứng ngoài mép dốc. Khi buông ra, $m_2$ có xu hướng rơi xuống do trọng lực, kéo dây làm $m_1$ trượt lên dốc — nhưng vì ròng rọc **có khối lượng** ($M=1{,}0$ kg, không phải ròng rọc lý tưởng), nó không chỉ đổi hướng dây mà còn "ăn" một phần lực căng để tự quay, khiến $T_1 \neq T_2$ (khác với ròng rọc không khối lượng học ở Chương 2, nơi $T$ hai bên bằng nhau).

## Bước 1 — Xác định chiều chuyển động trước khi đặt dấu ma sát

So sánh "lực kéo" của $m_2$ (là $m_2g$) với "lực cản" của $m_1$ dọc theo dốc (là $m_1g\sin\theta$). Bên nào lớn hơn sẽ thắng, hệ chuyển động theo chiều đó. Việc này **phải làm trước** vì lực ma sát luôn ngược chiều chuyển động thực tế — nếu đoán sai chiều, dấu của lực ma sát trong phương trình sẽ sai theo.

## Bước 2 — Vẽ lực riêng cho từng vật (3 vật: $m_1$, $m_2$, ròng rọc)

- **$m_1$ trên dốc:** trọng lực phân tích thành 2 thành phần (dọc dốc $m_1g\sin\theta$, vuông góc dốc $m_1g\cos\theta$ → cho phản lực $N$ và từ đó ra lực ma sát $f=kN$), lực căng $T_1$ kéo dọc dốc hướng lên.
- **$m_2$ treo thẳng đứng:** trọng lực $m_2g$ hướng xuống, lực căng $T_2$ hướng lên.
- **Ròng rọc (trụ đặc, $I=\frac12MR^2$):** hai lực căng $T_1$ và $T_2$ tác dụng ở mép ròng rọc theo hai phía, gây ra mômen lực làm nó quay.

## Bước 3 — Viết 3 phương trình

1. Newton II cho $m_2$ (phương thẳng đứng): liên hệ $m_2g$, $T_2$, gia tốc $a$.
2. Newton II cho $m_1$ (dọc theo dốc): liên hệ $T_1$, $m_1g\sin\theta$, lực ma sát, gia tốc $a$.
3. Phương trình quay cho ròng rọc: $(T_2-T_1)R = I\beta$, với $\beta$ là gia tốc góc.

## Bước 4 — Ràng buộc để giải hệ

Vì dây không trượt trên ròng rọc: $a = R\beta$. Thế vào phương trình (3) để đổi $\beta$ thành $a$, lúc này cả 3 phương trình đều chỉ còn ẩn $a, T_1, T_2$ — cộng/khử qua lại để rút ra $a$ trước, rồi thế ngược lại tìm $T_1$, $T_2$.

**Điểm khác biệt quan trọng so với bài ròng rọc nhẹ ở Chương 2:** ở đây bạn có **3 phương trình cho 3 ẩn** ($a, T_1, T_2$) thay vì 2 phương trình cho 2 ẩn — vì $T_1\neq T_2$.


# Câu 4

## Hình dung tình huống

Đây là **máy lạnh** (không phải động cơ nhiệt sinh công) — nghĩa là chu trình đi **ngược chiều kim đồng hồ** trên đồ thị P-V (khác với động cơ nhiệt thường đi thuận chiều kim đồng hồ). Máy lạnh cần **nhận công từ bên ngoài** (W đưa vào) để "bơm" nhiệt từ nơi lạnh sang nơi nóng — ngược tự nhiên. Khí lưỡng nguyên tử → nhớ $i=5$, $\gamma = \frac{i+2}{i} = \frac75$.

## Bước 1 (câu a) — Vẽ chu trình

Xác định 4 điểm trên P-V theo thứ tự $V$ giảm dần: $V_1=18 > V_2=8 > V_3=4$ (nên đoạn 1→2→3 là nén khí). Mỗi đoạn có hình dạng đường cong khác nhau:

- $(1\to2)$ đoạn nhiệt: đường dốc hơn (do $PV^\gamma$)
- $(2\to3)$ đẳng áp: đường nằm ngang ($P=const$)
- $(3\to4)$ đẳng nhiệt: đường cong thoải hơn ($PV=const$)
- $(4\to1)$ đẳng áp: đường nằm ngang khép về điểm 1

## Bước 2 (câu b) — Tìm $T_4, V_4$: đi tuần tự qua từng trạng thái, đừng nhảy cóc

Đây là chỗ hay rối nhất — phải tính **lần lượt từng trạng thái theo đúng thứ tự chu trình**, không nhảy thẳng đến trạng thái 4:

1. $(1\to2)$ đoạn nhiệt: dùng $P_1V_1^\gamma = P_2V_2^\gamma$ tìm $P_2$, rồi từ $P_1V_1/T_1=P_2V_2/T_2$ tìm $T_2$.
2. $(2\to3)$ đẳng áp nên $P_3=P_2$; đã biết $V_3$ → dùng $V_2/T_2=V_3/T_3$ tìm $T_3$.
3. $(3\to4)$ đẳng nhiệt → $T_4=T_3$ **ngay lập tức**, không cần tính gì thêm — đây là nửa đáp số câu b.
4. $(4\to1)$ đẳng áp, khép kín về trạng thái 1 → nghĩa là $P_4=P_1$ (vì cùng 1 đoạn đẳng áp nối thẳng đến điểm 1). Dùng $V_4/T_4 = V_1/T_1$ (đã có $T_4$ ở bước 3) để tìm $V_4$.

**Bẫy:** nhiều bạn quên rằng đẳng áp $(4\to1)$ nghĩa là $P_4$ phải **bằng đúng $P_1$**, không phải một áp suất mới nào khác.

## Bước 3 (câu c) — Tính W từng đoạn

Tra đúng công thức theo loại quá trình (bảng ở note Chương 6) cho từng đoạn — đoạn nhiệt dùng $W=\Delta U = nC_V\Delta T$, đẳng áp dùng $W=-P\Delta V$, đẳng nhiệt dùng $W=-nRT\ln(V_f/V_i)$. Cộng đại số (chú ý dấu!) cả 4 đoạn ra tổng công chu trình.

## Bước 4 (câu d) — Hệ số làm lạnh $\varepsilon$

1. Với mỗi đoạn đã có $W$ ở bước 3, tính $Q = \Delta U - W$ (từ $\Delta U=Q+W$) — chú ý $\Delta U$ mỗi đoạn tính từ $nC_V\Delta T$ của chính đoạn đó (riêng đoạn đoạn nhiệt thì $Q=0$ sẵn, không cần tính).
2. Xem dấu $Q$ từng đoạn: đoạn nào $Q>0$ là khí **nhận nhiệt** (ứng với $Q_c$ hút từ nguồn lạnh), đoạn nào $Q<0$ là khí **thải nhiệt** (ứng với $Q_h$ ra nguồn nóng).
3. Áp công thức $\varepsilon = \dfrac{|Q_c|}{W_{tổng}}$ ở note Chương 7 (mục Máy làm lạnh), với $W_{tổng}$ là công **hệ nhận vào** trong cả chu trình (từ bước 3, chú ý dấu cho đúng chiều "nhận công" của máy lạnh).

## Công thức chung — đúng cho MỌI quá trình (không phụ thuộc loại)

$$PV=nRT \qquad \Delta U = nC_V\Delta T \qquad \Delta U = Q+W$$

với $C_V=\dfrac{i}{2}R$, $C_P=C_V+R$, $\gamma=\dfrac{C_P}{C_V}=\dfrac{i+2}{i}$.

## Bảng công thức riêng từng quá trình

|                        | **Đẳng tích** ($V$=const)           | **Đẳng áp** ($P$=const)             | **Đẳng nhiệt** (T = const)      | **Đoạn nhiệt** (Q=0)                                                     |
| ---------------------- | ----------------------------------- | ----------------------------------- | ------------------------------- | ------------------------------------------------------------------------ |
| **Hệ thức trạng thái** | $\dfrac{P_1}{T_1}=\dfrac{P_2}{T_2}$ | $\dfrac{V_1}{T_1}=\dfrac{V_2}{T_2}$ | $P_1V_1=P_2V_2$                 | $P_1V_1^\gamma=P_2V_2^\gamma$  <br>$T_1V_1^{\gamma-1}=T_2V_2^{\gamma-1}$ |
| **Công $W$             | $W=0$                               | $W=-P\Delta V=-nR\Delta T$          | $W=-nRT\ln\dfrac{V_f}{V_i}$     | $W=nC_V\Delta T=\dfrac{P_2V_2-P_1V_1}{\gamma-1}$                         |
| **Nhiệt $Q$** (hệ nhận | $Q=nC_V\Delta T$                    | $Q=nC_P\Delta T$                    | $Q=-W=A=nRT\ln\dfrac{V_f}{V_i}$ | $Q=0$                                                                    |
| **$\Delta U$**         | $\Delta U=Q$                        | $\Delta U=nC_V\Delta T$             | $\Delta U=0$                    | $\Delta U=W=-A=nC_V\Delta T$                                             |

## Mẹo nhớ nhanh — "cái gì bằng 0"

- **Đẳng tích:** $W=0$ (không có $\Delta V$ thì không có công)
- **Đoạn nhiệt:** $Q=0$ (theo định nghĩa — cách nhiệt với môi trường)
- **Đẳng nhiệt:** $\Delta U=0$ (nội năng khí lý tưởng chỉ phụ thuộc $T$, mà $T$ không đổi)
- **Đẳng áp:** không có gì bằng 0 cả — đây là quá trình "đầy đủ nhất", cả $W, Q, \Delta U$ đều khác 0.

Bảng này đã có sẵn trong [Chương 6](https://claude.ai/epitaxy/10_Projects/13_Uni_Retake/Ch%C6%B0%C6%A1ng%206%20-%20Nguy%C3%AAn%20l%C3%BD%20I%20Nhi%E1%BB%87t%20%C4%91%E1%BB%99ng%20l%E1%BB%B1c%20h%E1%BB%8Dc.md) mục 6 — nên học thuộc bảng này trước, vì **mọi bài chu trình đều chỉ là ráp 3-4 quá trình này lại với nhau**.


Đúng là công thức trong slide **$W=nRT\ln(V_i/V_f)$** — nhưng đây là **công mà khí NHẬN**, còn công thức tôi dùng ở Câu 2 (**$A=nRT\ln(V_f/V_i)$**) là **công mà khí THỰC HIỆN/SINH RA**. Hai đại lượng này **ngược dấu nhau**: $A = -W$.

Tóm gọn thành quy trình quyết định thực dụng, không cần nhớ máy móc:

## Bước 1 — Nhìn loại chu trình đang xét

|Loại máy|Quy ước tự nhiên|Vì sao|
|---|---|---|
|**Động cơ nhiệt** (sinh công để chạy máy khác)|Dùng **A** (công khí **sinh ra**)|Vì công thức hiệu suất $\eta = A/Q_{nhận}$ cần $A$ dương|
|**Máy lạnh / bơm nhiệt** (cần điện để chạy)|Dùng **W** (công khí **nhận**)|Vì công thức $\varepsilon =|

Đây là dấu hiệu **đáng tin nhất** — cứ xác định trước "đây là loại máy gì" rồi chọn quy ước theo đúng công thức hiệu suất/hệ số sẽ dùng ở câu sau.

## Bước 2 — Nếu đề dùng chữ rõ ràng, ưu tiên chữ đó

- "công khí **sinh** ra", "công **do** khí thực hiện" → chắc chắn là $A$
- "công khí **nhận**", "công **cấp cho** khí" → chắc chắn là $W$
- "công thực hiện" (chung chung, không rõ) → quay lại Bước 1

## Bước 3 — Mẹo an toàn nhất: đừng nhớ tên, nhớ **hướng vật lý**

Với **từng quá trình riêng lẻ**, không cần nhớ "$A$ hay $W$" — chỉ cần hỏi:

- **Khí giãn nở** ($V$ tăng) → khí **sinh công dương** một cách trực quan (khí đẩy pít-tông ra)
- **Khí bị nén** ($V$ giảm) → khí **nhận công dương** một cách trực quan (bị đẩy vào)

Tính độ lớn $|P\Delta V|$ trước, rồi gán dấu theo hướng vật lý này — **không phụ thuộc** đề gọi nó là $A$ hay $W$, vì $|A|=|W|$ luôn bằng nhau, chỉ khác dấu.

## Bước 4 — Chốt bằng kiểm tra ngược

Sau khi ra đáp số cuối (hiệu suất $\eta$ hoặc hệ số $\varepsilon$), nếu **ra âm hoặc vô lý** (>100% hay <0) → tức là bạn đã lỡ trộn lẫn quy ước $A$/$W$ giữa các quá trình trong cùng bài → quay lại đổi dấu tất cả cho nhất quán.

**Chốt 1 câu:** cứ xác định máy là _động cơ_ (dùng $A$=sinh) hay _máy lạnh_ (dùng $W$=nhận) ngay từ đầu bài, rồi giữ nguyên quy ước đó xuyên suốt — không đổi giữa chừng.



Đề cho: $R = 8{,}31\times10^3$ J/(kmol.K).

**Lưu ý quan trọng:** đề cho số mol trực tiếp là $n=0{,}6$ **mol**, nhưng $R$ lại cho theo đơn vị **kmol**. Nhớ lại quy tắc đã chốt trước đó — phải **đồng bộ đơn vị** giữa $n$ và $R$: $$n = 0{,}6\ \text{mol} = 0{,}6\times10^{-3}\ \text{kmol} = 6\times10^{-4}\ \text{kmol}$$

rồi dùng cùng với $R=8{,}31\times10^3$ J/(kmol.K) trong các công thức như $PV=nRT$, $\Delta U = n\dfrac{i}{2}R\Delta T$, v.v.

(Bạn cũng có thể chọn cách khác: giữ $n=0{,}6$ mol và tự đổi sang $R=8{,}31$ J/(mol.K) — hai cách cho cùng kết quả, miễn nhất quán.)


## Định nghĩa

**Quá trình thuận nghịch (reversible)** là quá trình xảy ra **vô cùng chậm**, sao cho tại **mọi thời điểm**, hệ luôn ở trạng thái **cân bằng nhiệt động** (áp suất, nhiệt độ đồng đều trong toàn hệ). Vì luôn cân bằng, quá trình có thể **đảo ngược hoàn toàn** mà không để lại thay đổi nào ở hệ hay môi trường xung quanh.

## Ý nghĩa thực dụng khi làm bài (quan trọng nhất)

**"Thuận nghịch" là điều kiện để các công thức bạn đang dùng có hiệu lực:**

- $W = -\int P,dV$, $A=\int P,dV$ — các công thức này dùng $P$ **của chính khí đang xét**. Nếu quá trình **không** thuận nghịch (VD khí giãn nở đột ngột vào chân không), áp suất bên trong hệ không đồng nhất tại từng thời điểm → không thể xác định $P$ để tích phân, công thức này **không áp dụng được trực tiếp**.
- $PV^\gamma=const$ (phương trình đoạn nhiệt), $\dfrac{P_1V_1}{T_1}=\dfrac{P_2V_2}{T_2}$ — cũng chỉ đúng khi hệ đi qua **một chuỗi liên tục các trạng thái cân bằng**, tức là quá trình thuận nghịch.
- Vì luôn cân bằng, mỗi quá trình có thể vẽ thành **một đường xác định, liên tục** trên đồ thị P–V (đúng như hình vẽ đề cho) — nếu bất thuận nghịch thì không vẽ được đường rõ ràng như vậy.

→ Nói ngắn gọn: cụm từ "**chu trình thuận nghịch**" chính là lời **xác nhận của đề** rằng bạn được phép dùng thẳng mọi công thức khí lý tưởng chuẩn ($W$, $A$, $Q$, phương trình đoạn nhiệt...) cho từng quá trình con mà không cần lo về mất mát hay hiệu ứng bất thuận nghịch nào khác.

## Ý nghĩa phụ (không cần cho bài tập numeric, chỉ để hiểu sâu hơn)

- Chu trình thuận nghịch có **hiệu suất cao nhất có thể** so với chu trình bất thuận nghịch hoạt động giữa cùng 2 nguồn nhiệt (liên quan định lý Carnot).
- Sau 1 chu trình thuận nghịch, **độ biến thiên entropy tổng** (hệ + môi trường) $=0$; còn bất thuận nghịch thì $>0$ — đây là nội dung Nguyên lý II bạn đã ôn ở [Chương 7](https://claude.ai/epitaxy/10_Projects/13_Uni_Retake/Ch%C6%B0%C6%A1ng%207%20-%20Nguy%C3%AAn%20l%C3%BD%20II%20Nhi%E1%BB%87t%20%C4%91%E1%BB%99ng%20l%E1%BB%B1c%20h%E1%BB%8Dc.md).