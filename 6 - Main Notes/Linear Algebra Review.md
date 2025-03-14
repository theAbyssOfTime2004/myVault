2025-03-14 20:47


Tags: [[Machine Learning]], [[DeepLearning]], [[data scientist]], [[beginner]], [[Mathematics]]

# Linear Algebra Review

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
- Khi ta nói rằng 2 vector thẳng hàng (đầu và đuôi chúng cùng điểm vs nhau) hay vector thứ 3 nằm trong span của vector 1 và 2 thì nghĩa là các vector này dư thừa và chúng không thêm gì vào span của chúng ta cả (nghĩa là không có thông tin gì mới được sinh ra từ các vectors này) 
# References
