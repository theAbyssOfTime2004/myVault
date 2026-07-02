Cùng cách làm như bài trước — đặt tổ hợp của cơ sở $U$ **bằng** tổ hợp của cơ sở $W$, rồi cân bằng từng tọa độ. Làm đầy đủ cho bài này:

## Bước 0 — Cơ sở $U$, $W$ (đã có từ câu a, b)

$W=\langle w_1=(-1,0,1,0),\ w_2=(0,-1,0,1)\rangle$ (giải hệ, $\dim W=2$).

$U=\langle u_1,u_2,u_3\rangle$: vì $u_3=u_1+u_2=(1,1,1,1)$ (thừa) nên $\dim U=2$, cơ sở ${u_1=(1,0,0,1),,u_2=(0,1,1,0)}$.

Gộp 4 vectơ (dòng) $\to$ hạng 3 $\Rightarrow \dim(U+W)=3$. Grassmann: $\dim(U\cap W)=2+2-3=1$.

## Bước 1 — Lập phương trình

$$\alpha u_1+\beta u_2 = s, w_1+t, w_2$$

## Bước 2 — Khai triển từng vế theo tọa độ

**Vế trái:** $$\alpha(1,0,0,1)+\beta(0,1,1,0)=(\alpha,\ \beta,\ \beta,\ \alpha)$$

**Vế phải:** $$s(-1,0,1,0)+t(0,-1,0,1)=(-s,\ -t,\ s,\ t)$$

## Bước 3 — Cân bằng từng tọa độ

|Tọa độ|Vế trái|Vế phải|Phương trình|
|---|---|---|---|
|1|$\alpha$|$-s$|$\alpha=-s$|
|2|$\beta$|$-t$|$\beta=-t$|
|3|$\beta$|$s$|$\beta=s$|
|4|$\alpha$|$t$|$\alpha=t$|

## Bước 4 — Giải hệ

Từ (1): $s=-\alpha$. Từ (4): $t=\alpha$. Thế vào (2): $\beta=-t=-\alpha$. Thế vào (3): $\beta=s=-\alpha$ — **hai phương trình (2),(3) cho cùng kết quả** $\beta=-\alpha$ (không mâu thuẫn) ⇒ hệ có nghiệm với **1 tham số tự do**.

Đặt $\alpha=r$: $\beta=-r,\ s=-r,\ t=r$.

## Bước 5 — Thế vào một vế (chọn vế $U$)

$$v=\alpha u_1+\beta u_2=r,u_1-r,u_2=r(u_1-u_2)=r\big[(1,0,0,1)-(0,1,1,0)\big]=r(1,-1,-1,1)$$

**Kiểm vế $W$:** $s w_1+t w_2=-r,w_1+r,w_2=r(w_2-w_1)=r\big[(0,-1,0,1)-(-1,0,1,0)\big]=r(1,-1,-1,1)$ — **trùng** ✓

$$\boxed{U\cap W=\langle(1,-1,-1,1)\rangle,\qquad \dim(U\cap W)=1\ (\text{khớp Grassmann}).}$$

---

**Điểm mấu chốt của bài này** (khác bài trước): ở đây **2 phương trình (2) và (3) cho cùng một kết quả** $\beta=-\alpha$ thay vì mỗi cái ràng buộc riêng $\alpha,\beta$ — đó chính là lý do có **1 tham số tự do** dư ra (thay vì 0, tức $U\cap W={0}$). Luôn nhớ: nếu số ẩn ($\alpha,\beta,s,t$ = 4 ẩn) trừ số phương trình **độc lập thực sự** (không phải cứ đếm 4 dòng là 4 ràng buộc — có thể trùng nhau như ở đây) ra đúng $\dim(U\cap W)$ theo Grassmann thì bạn làm đúng. 


Có — thay vì suy luận thế biến ngược qua lại (dễ rối khi hệ phức tạp hơn), cứ coi 4 phương trình đó là **một hệ thuần nhất bình thường với 4 ẩn $\alpha,\beta,s,t$**, rồi **khử Gauss y như mọi bài Chương 3** — đúng kỹ năng bạn đã quen.

## Chuyển 4 phương trình thành ma trận hệ số

Viết lại mỗi phương trình về dạng $=0$ (chuyển vế), theo thứ tự ẩn $(\alpha,\beta,s,t)$:

$$\begin{cases}\alpha+s=0\ \beta+t=0\ \beta-s=0\ \alpha-t=0\end{cases}\quad\Rightarrow\quad\begin{pmatrix}1&0&1&0\0&1&0&1\0&1&-1&0\1&0&0&-1\end{pmatrix}$$

## Khử Gauss như bình thường

$$\xrightarrow{R_4-R_1}\begin{pmatrix}1&0&1&0\0&1&0&1\0&1&-1&0\0&0&-1&-1\end{pmatrix}\xrightarrow{R_3-R_2}\begin{pmatrix}1&0&1&0\0&1&0&1\0&0&-1&-1\0&0&-1&-1\end{pmatrix}\xrightarrow{R_4-R_3}\begin{pmatrix}1&0&1&0\0&1&0&1\0&0&-1&-1\0&0&0&0\end{pmatrix}$$

## Đọc kết quả — y hệt cách đọc nghiệm ở Câu 1a

Hạng $=3$, số ẩn $=4$ ⇒ **1 ẩn tự do** — con số này **tự động khớp** $\dim(U\cap W)=1$ (Grassmann), khỏi cần đối chiếu riêng.

Cột không pivot là cột $t$ ⇒ $t$ tự do. Đặt $t=r$:

- Dòng 3: $-s-t=0\Rightarrow s=-r$
- Dòng 2: $\beta+t=0\Rightarrow \beta=-r$
- Dòng 1: $\alpha+s=0\Rightarrow \alpha=-s=r$

$$(\alpha,\beta,s,t)=r(1,-1,-1,1)$$

## Thế vào vế $U$ như cũ

$$v=\alpha u_1+\beta u_2=r,u_1-r,u_2=r(1,-1,-1,1)$$

Khớp kết quả trước.

## Vì sao cách này nhanh & an toàn hơn

- **Không phải đoán xem thế biến nào trước** — cứ máy móc khử Gauss, luôn ra đúng.
- **Số ẩn tự do tự động $=\dim(U\cap W)$** — khỏi phải "kiểm lại có khớp Grassmann không", nó tự khớp vì đây chính là bản chất của Grassmann.
- Khi hệ **phức tạp hơn** (nhiều ẩn hơn, hệ số lẻ hơn) thì thế biến tay dễ sai, còn khử Gauss thì quy trình cố định, luôn theo được.

**Tóm gọn quy trình TH1 hoàn chỉnh:**

1. Đặt $\sum\alpha_iu_i=\sum\beta_jv_j$.
2. Cân bằng tọa độ → hệ phương trình theo ẩn $\alpha_i,\beta_j$.
3. **Chuyển hệ đó thành ma trận, khử Gauss như bình thường** (bước mới bạn vừa học) → đọc ẩn tự do.
4. Thế vào 1 vế → cơ sở $U\cap W$.