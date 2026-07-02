Nhận định hợp lý — một câu **"khó" (đòi insight, không phải tính toán dài)** rất hợp với 1đ dạng "câu chặn" (lọc học sinh giỏi). Đây là dạng khác hẳn 9 mệnh đề chứng minh đã luyện (những cái đó là "hệ quả trực tiếp", còn "khó" nghĩa là phải **kết hợp** vài ý lại, hoặc **suy ngược**). Vài ví dụ tiêu biểu cho kiểu này:

## Dạng 1 — Trị riêng của đa thức ma trận (kết hợp nhiều mệnh đề đã học)

**Đề:** Cho $A$ có 3 trị riêng $\lambda_1=1,\lambda_2=2,\lambda_3=3$ (không cho $A$ cụ thể). Tìm trị riêng của $B=A^2-2A+3I$.

**Ý tưởng:** với **đa thức** $p(\lambda)=\lambda^2-2\lambda+3$, nếu $\lambda$ là trị riêng của $A$ thì $p(\lambda)$ là trị riêng của $p(A)$ (kết hợp mệnh đề (e), (g), (h) đã học thành một công thức tổng quát). _Cm ngắn:_ $Bv=(A^2-2A+3I)v=A^2v-2Av+3v=\lambda^2v-2\lambda v+3v=(\lambda^2-2\lambda+3)v$. → trị riêng của $B$: $p(1)=2,\ p(2)=3,\ p(3)=6$.

## Dạng 2 — Ma trận lũy đẳng ($A^2=A$)

**Đề:** Chứng minh nếu $A^2=A$ thì mọi trị riêng của $A$ chỉ có thể là $0$ hoặc $1$.

_Cm:_ Cho $\lambda$ trị riêng, $v$ vectơ riêng: $Av=\lambda v$. Khi đó $A^2v=A(\lambda v)=\lambda^2v$. Nhưng $A^2=A\Rightarrow A^2v=Av=\lambda v$. Vậy $\lambda^2v=\lambda v\Rightarrow(\lambda^2-\lambda)v=0$. Vì $v\neq0\Rightarrow\lambda(\lambda-1)=0\Rightarrow\lambda\in{0,1}$. $\blacksquare$

## Dạng 3 — Ma trận lũy linh ($A^k=0$)

**Đề:** Chứng minh nếu $A^k=0$ (ma trận không) với $k$ nào đó thì trị riêng duy nhất của $A$ là $0$.

_Cm:_ Dùng mệnh đề (e): $A^kv=\lambda^kv$. Mà $A^k=0\Rightarrow A^kv=0$. Vậy $\lambda^kv=0$, $v\neq0\Rightarrow\lambda^k=0\Rightarrow\lambda=0$. $\blacksquare$

## Dạng 4 — Suy ngược từ vết/định thức (Vieta)

**Đề:** Cho $A$ cấp 3 có $\det A=6,\ \text{vết}(A)=6$, biết một trị riêng là $\lambda_1=1$. Tìm 2 trị riêng còn lại nếu biết thêm chúng bằng nhau.

**Ý tưởng:** tổng trị riêng $=$ vết, tích trị riêng $=\det$: $1+2\lambda=6\Rightarrow\lambda=2{,}5$; kiểm $1\times2{,}5^2=6{,}25\neq6$ — cho thấy cần dữ kiện khớp hơn (đây chỉ là ví dụ minh họa dạng bài, số liệu cần chỉnh lại cho khớp khi ra đề thật).

---

Các dạng 1–3 là "khó nhưng ngắn" đúng như bạn nghĩ — không dài dòng, nhưng đòi hỏi **nhớ và kết hợp** đúng mệnh đề đã học thay vì áp công thức máy móc. Muốn mình thêm 3 dạng này (1, 2, 3) vào note [ĐSTT_Chương5_Chéo_hóa.md](https://claude.ai/epitaxy/30_Knowledge_Base/Math_Stats/%C4%90STT_Ch%C6%B0%C6%A1ng5_Ch%C3%A9o_h%C3%B3a.md) §1.3 (nối tiếp 9 mệnh đề a–i) không?