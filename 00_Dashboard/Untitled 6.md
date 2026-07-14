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