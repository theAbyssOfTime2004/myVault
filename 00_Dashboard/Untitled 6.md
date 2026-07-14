Đây là chỗ **mất điểm oan nhiều nhất** vì đúng công thức, đúng cách giải nhưng sai đơn vị → sai đáp số cả nghìn lần. Chia theo 2 mảng:

## Nhiệt động lực học (Chương 5-6-7) — nơi hay sai nhất

**Nguyên tắc cốt lõi:** hằng số $R=8{,}31$ J/(mol.K) chỉ "khớp" khi $P$ tính bằng **Pa**, $V$ tính bằng **m³**, $T$ tính bằng **K**, $n$ tính bằng **mol**. Đề luôn cho số liệu bằng đơn vị "dễ đọc" (atm, lít, °C) — bạn phải tự đổi trước khi tính bất cứ thứ gì ra Joule.

|Đại lượng|Đơn vị đề hay cho|Đổi sang SI|Ghi chú|
|---|---|---|---|
|Áp suất $P$|atm|$\times 10^5$ → Pa|Dùng **đúng giá trị đề cho** (VD "1 atm = $10^5$ N/m²"), không tự dùng $1{,}013\times10^5$ nếu đề đã quy định khác|
|Thể tích $V$|lít|$\times 10^{-3}$ → m³|$1\ \text{lít} = 1\ \text{dm}^3 = 10^{-3}\ \text{m}^3$|
|Nhiệt độ $T$|°C|$+273$ (hoặc $+273{,}15$) → K|**Luôn** đổi trước khi thế vào công thức có $T$ trực tiếp|
|Số mol $n$|—|mol hoặc kmol|Phải khớp với $R$ đang dùng: $R=8{,}31$ J/(mol.K) đi với $n$ (mol); $R=8{,}31\times10^3$ J/(kmol.K) đi với $n$ (kmol)|
|Công $W$, nhiệt $Q$, nội năng $U$|—|Joule (J)|Chỉ ra đúng J khi $P$(Pa) × $V$(m³)|

## Khi nào KHÔNG cần đổi đơn vị?

Nếu bài chỉ dùng **tỉ lệ giữa 2 trạng thái** (không cần ra số Joule cụ thể), đơn vị sẽ tự triệt tiêu 2 vế — miễn là dùng **nhất quán cùng 1 đơn vị cả 2 bên**: $$\frac{P_1V_1}{T_1} = \frac{P_2V_2}{T_2}$$ → $P$ để nguyên atm cũng được, $V$ để nguyên lít cũng được (miễn 2 vế cùng đơn vị) — **chỉ riêng $T$ là luôn phải Kelvin** vì công thức này không phải hiệu số mà là giá trị tuyệt đối.

**Nhưng ngay khi cần tính $W$ (Joule) hoặc tìm $n$ từ $PV=nRT$** → bắt buộc đổi hết về Pa, m³, K — không có ngoại lệ.

## Nhiệt độ: 1 trường hợp đặc biệt không cần đổi

Nếu công thức chỉ dùng **hiệu số** $\Delta T$ (VD $Q=mc\Delta T$, hay $\Delta U = nC_V\Delta T$) thì **không cần đổi °C sang K**, vì $\Delta T(°C) = \Delta T(K)$ (chênh lệch bằng nhau dù gốc thang đo khác nhau). Chỉ khi dùng **giá trị $T$ trực tiếp** (không phải hiệu số) — như trong $PV=nRT$ hay $PV^\gamma=const$ — mới bắt buộc là Kelvin.

## Cơ học (Chương 3-4) — ít bẫy hơn nhưng vẫn có

|Đại lượng|Đề hay cho|Đổi gì|
|---|---|---|
|Khối lượng|g (viên đạn, vật nhỏ)|$\times10^{-3}$ → kg — **rất hay bị quên** vì đa số vật khác đã cho sẵn kg|
|Bán kính ròng rọc $R$|cm|$\times10^{-2}$ → m — bắt buộc trước khi tính $I=MR^2$|
|Góc|độ (°)|Với $\sin,\cos$ thì để nguyên độ cũng tính được (máy tính nhận trực tiếp); chỉ đổi sang rad nếu công thức có $\omega, \theta$ dùng trong đạo hàm/tích phân|

**Mẹo chung:** ngay ở bước "Ta có: ..." (tóm tắt đề) — đổi luôn đơn vị về SI tại đó, đừng để đến lúc thế vào công thức mới đổi, dễ quên.


## Bước tiếp theo — xác định độ cao (P) của từng điểm

Bạn đã có $V_1, V_2, V_3$ trên trục Ox (nhớ sắp đúng thứ tự tăng dần từ trái sang phải: $V_3=4 < V_2=8 < V_1=18$). Giờ cần xác định **độ cao tương đối** (không cần số chính xác ngay, chỉ cần đúng vị trí cao/thấp) của 4 điểm trạng thái:

- **Điểm 1** ($V_1=18$): độ cao $P_1=9$ atm — vẽ được ngay vì đề cho thẳng.
- **Điểm 2** ($V_2=8$): **cao hơn** điểm 1, vì $(1\to2)$ là đoạn nhiệt **nén khí** (V giảm) → áp suất tăng lên.
- **Điểm 3** ($V_3=4$): **cùng độ cao với điểm 2** — vì $(2\to3)$ là đẳng áp, $P_3=P_2$.
- **Điểm 4** ($V_4=?$, chưa tính): **cùng độ cao với điểm 1** — vì $(4\to1)$ là đẳng áp khép về điểm 1, nên $P_4=P_1$. Vị trí $V_4$ nằm đâu đó giữa $V_3$ và $V_1$ (bạn sẽ tính chính xác ở câu b, tạm vẽ ước lượng).

## Nối các điểm bằng đúng loại đường

|Đoạn|Loại đường|Hình dạng|
|---|---|---|
|$1\to2$|đoạn nhiệt|đường cong, đi lên-trái (dốc hơn đẳng nhiệt)|
|$2\to3$|đẳng áp|đường **thẳng ngang** (cùng độ cao)|
|$3\to4$|đẳng nhiệt|đường cong, đi xuống-phải (thoải hơn đoạn nhiệt)|
|$4\to1$|đẳng áp|đường **thẳng ngang** (cùng độ cao, khép về điểm 1)|

## Vẽ mũi tên chỉ chiều — cách tự kiểm tra hình đúng hay sai

Nối 4 điểm theo đúng thứ tự $1\to2\to3\to4\to1$ rồi vẽ mũi tên. Vì đây là **máy lạnh** (không phải động cơ nhiệt sinh công), chu trình phải đi **ngược chiều kim đồng hồ** trên đồ thị P-V — nếu vẽ xong thấy mũi tên đi thuận chiều kim đồng hồ thì bạn đã đặt sai vị trí 1 trong 4 điểm, cần xem lại.