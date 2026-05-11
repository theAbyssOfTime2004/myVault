2025-03-14 20:47


Tags: [[Machine Learning]], [[Deep Learning]], [[data scientist]], [[beginner]], [[Mathematics]]

# Linear Algebra Review

### Vector, Scaling, Span và tổ hợp tuyến tính

- Các Số (thường sẽ đóng vai trò) là các Scalars cho các vector, có nhiệm vụ scaling (mở rộng, kéo giãn, co lại) các vectors
- Các vector $\vec{i}$ và $\vec{j}$ là các basis vectors (hay còn gọi là cơ sở), theo trục Ox, Oy, và có thể có vô số các cơ sở theo các hướng khác nhau ($\vec{v}$, $\vec{w}$,...)
- ![[Pasted image 20250314205346.png]]
khi ta scaling các basis vector này bằng các scalars (ví dụ ở đây là a và b) thì ta gọi tổng a$\vec{v}$ + b$\vec{w}$ là một tổ hợp tuyến tính![[Pasted image 20250314205747.png]]

- độ dãn (hay the span) của 2 vectors là tập chứa toàn bộ các tổ hợp tuyến tính giữa 2 vectors đó
- khi nói về 1 vector duy nhất: think of them as an arrow
- khi nói về 1 tập các vectors: think of sets of vectors as points 
- Xét trong không gian 3 chiều với tổ hợp tuyến tính giữa 2 basis vectors a$\vec{v}$ + b$\vec{w}$ thì ta có thể nói rằng span của 2 vectors này là 1 mặt phẳng cắt qua gốc tọa độ không gian 3 chiều của ta hay chính xác hơn tập tất cả các vectors có tips nằm trên mặt phẳng này chính là span của 2 basis vectors của ta 
![[Pasted image 20250314210517.png]]
- Với tổ hợp tuyến tính giữa 3 vectors thì cũng tương tự, chọn 3 scalars a, b, c, scale từng vector và sau đó cộng chúng lại và span của 3 vectors này cũng vẫn sẽ là tập toàn bộ các tổ hợp tuyến tính có thể có được
![[Pasted image 20250314210906.png]]
- Nếu vector thứ 3 của ta nằm trong span của vector thứ 1 và 2 thì span sẽ không thay đổi và cũng vẫn chỉ là mặt phẳng như trường hợp 2 vector 
- Nếu vector thứ 3 đó không nằm trong span của 2 vector 1 và 2 nghĩa là ta có thể tự do di chuyển span của 2 vector thứ 1 và 2 trên phương của vector thứ 3, quét nó qua toàn bộ không gian
- Khi ta nói rằng 2 vector thẳng hàng (đầu và đuôi chúng cùng điểm vs nhau) hay vector thứ 3 nằm trong span của vector 1 và 2 thì nghĩa là các vector này dư thừa và chúng không thêm gì vào span của chúng ta cả (nghĩa là không có thông tin gì mới được sinh ra từ các vectors này)  ta gọi chúng là phụ thuộc tuyến tính
### Các phép biến đổi tuyến tính và phép nhân ma trận
- Phép nhân ma trận là thực hiện cùng lúc nhiều các phép biến đổi tuyến tính - linear transformations (dilations, shears, rotations, reflections and projections) và ta có thể hình dung chúng 1 cách dễ dàng thông qua gridlines 
- các phép biến đổi tuyến tính có thể hiểu như các function biến đổi 1 vector thành 1 vector khác
- ![[Pasted image 20250315000850.png]]
- Ở đây các vector [1,2] và [3,1] ban đầu đã được biến đổi thông qua phép biến đổi tuyến tính và ta có thể tìm được vector output thông qua phép nhân ma trận trong hình
- Các phép nhân ma trận phải được thực hiện theo đúng thứ tự ví dụ $M_{1}M_{2}$ != $M_{2}M_{1}$ bởi vì thay đổi trật tự của phép biến đổi tuyến tính sẽ dẫn đến kết quả có thể khác nhau
### Định Thức (determinant)
- Ta thấy rằng các phép biến đổi tuyến tính sẽ làm tăng hoặc giảm đi diện tích của 1 ô vuông đơn vị (có thể bẳng cách co lại hoặc kéo dãn các basis vector)
- Vấn đề là làm sao để có thể đo lường được sự kéo dãn hay co lại đó, ta có một đại lượng gọi là định thức, định thức của 1 phép biến đổi cho ta biết mức độ tương quan giữa phần diện tích của vùng nằm trong cặp (hoặc các ma trận với số chiều cao hơn) sau khi biến đổi tuyến tính là bao nhiêu
- ![[Pasted image 20250315001939.png]]
- ![[Pasted image 20250315002611.png]]
- ![[Pasted image 20250315002628.png]]
- ![[Pasted image 20250315002737.png]]
- khi định thức là số âm, ta có thể nói về dấu của định thức như là một định nghĩa mang tính định hướng (orientation) hơn là giá trị của 1 vùng diện tích như khi ta nhắc đến số
- ![[Pasted image 20250315003015.png]]
- ![[Pasted image 20250315003030.png]]
- ![[Pasted image 20250315003140.png]]
- Do đó theo hình trên ma trận 2x2 tạo bởi 2 basis vector có tọa độ (1,1) và (2,-1) có định thức là -3.0 nghĩa là sau khi thực hiện phép biến đổi tuyến tính, vùng diện tích được tạo bởi 2 basis vector bị đảo ngược và giá trị scale theo hệ số 3
- Việc định thức bằng âm biểu thị một sự thay đổi về hướng (orientation) là hiển nhiên khi ta xét mối quan hệ tuyến tính giữa định thức và phần diện tích tạo bởi 2 basis vector trong một phép biến đổi tuyến tính thì khi 2 vector càng gần nhau nghĩa là phần diện tích hay định thức đang tiến về 0 và khi $\vec{i}$ thẳng hàng với $\vec{j}$ thì định thức = 0 và nếu ta cứ tiếp tục thì $\vec{i}$ và $\vec{j}$ sẽ đổi vị trí cho nhau do đó dấu sẽ thay đổi
- Trong không gian 3 chiều thì tương tự, thay vì xét phần diện tích của 1 hình chữ nhật, ta xét thể tích của một khối lập phương bị biến dạng theo các phép biến đổi (*parallelpiped*) 1x1x1
### Ma trận nghịch đảo
![[Pasted image 20250315004901.png]]
![[Pasted image 20250315005105.png]]
- ta
- ![[Pasted image 20250315005659.png]]
- ![[Pasted image 20250315005714.png]]
- ma trận nghịch đảo (inverse matrix) có thể được tìm ra bởi việc sử dụng các phép biến đổi nghịch đảo (inverse transformations) và về cơ bản, khi ta giải một hệ phương trình tuyến tính như hình trên thì có nghĩa là ta đang thực hiện các phép biến đổi nghịch đảo để tìm $\vec{x}$ từ $\vec{v}$
- ![[Pasted image 20250315010500.png]]
- ta có thể hiểu rằng việc cần làm ở đây là tìm một $\vec{x}$ that will land on $\vec{v}$ và miễn sao phép biến đổi A không ép không gian thành 1 chiều thấp hơn nghĩa là det(A) != 0 thì sẽ có tồn tại 1 phép biến đổi nghịch đảo $A^{-1}$ và nhân $A^{-1}$ với $\vec{v}$ ta sẽ tìm được $\vec{x}$ 
 - bởi vì khi ép không gian thành 1 chiều thấp hơn (<=> det(A) = 0) nghĩa là phép biến đổi tuyến tính nén không gian của vector trong hệ phương trình tuyến tính thành không gian có số chiều nhỏ hơn do đó ta không thể tìm được biến đổi nghịch đảo của nó, bởi vì ta không thể unsquish a line into a plane
 - Khi định thức của ma trận là 0, ma trận này không thể có nghịch đảo vì phép biến đổi tuyến tính của nó không phải là một phép biến đổi "đảo ngược" được. Phép biến đổi này đã làm mất thông tin (hay "nén" không gian), khiến chúng ta không thể phục hồi lại không gian ban đầu.
 - ![[Pasted image 20250315011401.png]]
 - Rank hay hạng của ma trận là là số chiều đầu ra của phép biến đổi tuyến tính
 - column space của ma trận A là tập hợp tất cả các vector có thể được tạo ra qua các tổ hợp tuyến tính của các vector cột của ma trận A
 - Rank is the number of dimension in the column space
 - Null space hay Kernel của ma trận là tất cả những vector mà khi nhân với ma trận, kết quả sẽ là vector 0
 ![[Pasted image 20250315013105.png]]
 $\vec{x}$ ở đây là null space của A
 - **Ma trận không vuông** có thể là kết quả của các phép biến đổi tuyến tính mà làm **giảm chiều** hoặc **tăng chiều** của không gian đầu vào.
- Khi có **nhiều cột hơn hàng** (ma trận $m \times n$ với $m<n$), phép biến đổi này có thể làm tăng chiều của không gian đầu ra nhưng lại có khả năng tạo ra sự phụ thuộc tuyến tính.
- Khi có **ít cột hơn hàng** (ma trận $m \times n$ với $m>n$), phép biến đổi này có thể làm giảm số chiều của không gian đầu ra.
### Tích vô hướng (dot product)
- ![[Pasted image 20250315014622.png]]
-  ![[Pasted image 20250315014638.png]]
- Tích vô hướng được dùng để đo độ "tương đồng" giữa các vector, nếu 2 vector có hướng gần giống nhau, tích vô hướng sẽ có giá trị lớn, nếu chúng vuông góc với nhau (không có sự tương đồng về hướng), tích vô hướng sẽ bằng **0**.
- **Tích vô hướng** giữa hai vector trong không gian 2 chiều có thể được xem là một phép biến đổi tuyến tính từ không gian 2 chiều (với vector đầu vào) sang không gian 1 chiều (với giá trị đầu ra là một số thực).
# References
