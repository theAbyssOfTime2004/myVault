Không sai — **giống hệt tình huống Câu C** trước đây: bạn chỉ **đổi thứ tự** trị riêng trên đường chéo, miễn ma trận $P$ đi kèm cũng đổi cột theo đúng thứ tự đó.

## Điều kiện để không sai

Nếu $D=\begin{pmatrix}5&0\0&1\end{pmatrix}$ thì $P$ phải có:

- **cột 1** = vectơ riêng ứng $\lambda=5$: $(1,1)$
- **cột 2** = vectơ riêng ứng $\lambda=1$: $(3,-1)$

$$P=\begin{pmatrix}1&3\1&-1\end{pmatrix}\quad(\text{không phải }P=\begin{pmatrix}3&1\-1&1\end{pmatrix}\text{ trong đáp án mẫu}).$$

## Kiểm nhanh

$\det P=-1-3=-4$, $P^{-1}=\tfrac{1}{-4}\begin{pmatrix}-1&-3\-1&1\end{pmatrix}=\tfrac14\begin{pmatrix}1&3\1&-1\end{pmatrix}$.

$$P^{-1}AP\overset{?}{=}\begin{pmatrix}5&0\0&1\end{pmatrix}$$

Bạn tự bấm Casio kiểm — nếu ra đúng $\begin{psmallmatrix}5&0\0&1\end{psmallmatrix}$ thì cặp $(P,D)$ của bạn hoàn toàn hợp lệ.

## Câu hỏi ngược lại

Bạn dùng $P$ nào để ra $D=\text{diag}(5,1)$? Nếu $P$ bạn ghi **cột 1 vẫn là $(3,-1)$** (vectơ ứng $\lambda=1$) mà $D$ lại để $5$ trước — đó mới là **sai thật sự** (lệch thứ tự giữa cột $P$ và đường chéo $D$). Gửi $P$ bạn dùng để mình xác nhận chính xác.

## Lưu ý cho phần b (tính $A^n$)

Nếu dùng $D=\text{diag}(5,1)$ với $P$ đúng ($=\begin{psmallmatrix}1&3\1&-1\end{psmallmatrix}$) thì $D^n=\text{diag}(5^n,1)$ — kết quả cuối $A^n$ (ma trận số) vẫn phải **giống hệt** đáp án mẫu, vì $A^n$ là bất biến không phụ thuộc cách bạn xếp thứ tự trị riêng.
$-1\cdot1^n = -1^n$ (vì $1^n=1$ với mọi $n$, nhân $-1$ chỉ đổi dấu, không đổi số mũ thành $n+1$).

Đúng — $1^n \cdot 1 = 1^n$ (nhân với $1$ giữ nguyên, không cộng thêm số mũ; $1^{n+1}$ chỉ đúng khi nhân với **$1^1$** một cách hình thức theo quy tắc $1^n\cdot1^1=1^{n+1}$, nhưng về **giá trị số** thì $1^{n+1}=1^n=1$ — cả hai đều bằng $1$, không có gì khác biệt vì $1$ lũy thừa bao nhiêu cũng ra $1$).