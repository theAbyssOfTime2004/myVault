2025-04-04 15:25


Tags: [[data mining]], [[data scientist]]

# ISOMAP

## 1. Tiếp Cận Vấn Đề

### Vấn đề với khoảng cách Euclidean truyền thống
- Trong phân phối dữ liệu phi tuyến, khoảng cách Euclidean truyền thống có thể gây hiểu nhầm. Ví dụ trong hình 3.4, nếu chỉ dựa vào khoảng cách Euclidean, điểm A và B có vẻ gần nhau, nhưng xét theo cấu trúc toàn cục của dữ liệu, chúng thực sự rất xa nhau.
![[Pasted image 20250404153334.png]]
- Khoảng cách Euclidean giữa hai điểm x và y được định nghĩa như sau:
### Khái niệm Geodesic
- Khoảng cách được hiểu là độ dài ngắn nhất của đường đi từ một điểm dữ liệu đến điểm khác, khi chỉ sử dụng các bước nhảy ngắn từ điểm này sang điểm lân cận gần nhất (k-nearest neighbors). Trong Hình 3.4, để đi từ A đến B phải đi dọc theo toàn bộ hình elip của phân phối dữ liệu và đi qua C, nên A và B thực sự là cặp điểm xa nhau nhất.

## 2. Phương pháp ISOMAP

- ISOMAP (Isometric Mapping) là phương pháp giảm chiều phi tuyến giúp ước tính khoảng cách Geodesic trên manifold. Quy trình ISOMAP bao gồm:
	1. Xây dựng đồ thị k-hàng xóm gần nhất (k-NN Graph)
	- Cho tập dữ liệu $(X = \{ x_1, x_2, \dots, x_n \})$ trong không gian $( \mathbb{R}^d )$.
	- Xác định **k hàng xóm gần nhất** của mỗi điểm $( x_i )$ dựa trên khoảng cách Euclidean hoặc metric phù hợp.
	- Tạo một đồ thị có trọng số $(G = (V, E))$, trong đó:
		- **Tập đỉnh** $( V )$ là các điểm dữ liệu.
		-  **Tập cạnh** $( E )$ kết nối mỗi điểm $( x_i )$ với $( k )$ hàng xóm gần nhất của nó.
		- **Trọng số cạnh** $( w(x_i, x_j) )$ là khoảng cách Euclidean giữa $( x_i )$ và $( x_j )$.
	2. Tính toán khoảng cách geodesic trên đồ thị
		- Với hai điểm bất kỳ $(\bar{X} )$ và $( \bar{Y} )$, xác định khoảng cách geodesic $( \text{Dist}(\bar{X}, \bar{Y}) )$.
		- Khoảng cách này được tính bằng **đường đi ngắn nhất (shortest path)** trên đồ thị $( G )$, sử dụng thuật toán như:
			-  **Dijkstra** (cho đồ thị thưa).
			- **Floyd-Warshall** (cho đồ thị nhỏ và đầy đủ).

# Phân tích ưu điểm và nhược điểm của ISOMAP

## 1. Ưu điểm

-  **Bảo toàn khoảng cách geodesic:**  
	ISOMAP duy trì tốt cấu trúc phi tuyến của dữ liệu bằng cách sử dụng khoảng cách geodesic trên manifold thay vì khoảng cách Euclidean thuần túy. Điều này giúp phương pháp thể hiện chính xác hơn mối quan hệ xa gần giữa các điểm dữ liệu trong không gian nhúng.  

 - **Giảm chiều dữ liệu hiệu quả:**  
	Phương pháp ISOMAP có thể ánh xạ dữ liệu từ không gian nhiều chiều về không gian thấp chiều một cách mượt mà mà vẫn bảo toàn được cấu trúc nội tại. Đây là lợi thế so với các phương pháp tuyến tính như PCA, vốn không thể xử lý tốt dữ liệu nằm trên manifold phi tuyến.  

 - **Không yêu cầu lựa chọn hàm kernel thủ công:**  
	Không giống như một số phương pháp khác như t-SNE hay kernel PCA, ISOMAP không cần thiết lập thủ công một hàm kernel để xác định quan hệ giữa các điểm. Điều này giúp giảm bớt sự phụ thuộc vào các siêu tham số và tránh việc chọn kernel không phù hợp.  

 - **Có cơ sở toán học vững chắc:**  
	ISOMAP được xây dựng trên nền tảng của **đa tạp Riemann (Riemannian manifold)** và **đồ thị ngắn nhất**, cho phép nó duy trì tính chặt chẽ về mặt toán học trong quá trình giảm chiều dữ liệu.  

 - **Ứng dụng rộng rãi trong phân tích dữ liệu phi tuyến:**  
	ISOMAP đặc biệt hữu ích trong các bài toán liên quan đến **thị giác máy tính, nhận dạng mẫu, sinh học phân tử**, và **xử lý ngôn ngữ tự nhiên**, nơi mà dữ liệu thường có cấu trúc phi tuyến phức tạp.  

---

## 2. Nhược điểm

-  **Nhạy cảm với nhiễu và lỗi trong dữ liệu:**  
	Khoảng cách geodesic trong ISOMAP phụ thuộc vào đồ thị k-NN, do đó nếu dữ liệu chứa nhiễu hoặc có các điểm nằm ngoài manifold thực tế, đồ thị có thể bị sai lệch, dẫn đến kết quả giảm chiều không chính xác.  

 - **Chi phí tính toán cao khi xử lý tập dữ liệu lớn:**  
	ISOMAP yêu cầu tính toán đường đi ngắn nhất giữa tất cả các cặp điểm trong đồ thị, thường sử dụng **thuật toán Dijkstra** hoặc **Floyd-Warshall**, dẫn đến độ phức tạp $O(n^3)$ đối với Floyd-Warshall hoặc $O(n^2 \log n)$ đối với Dijkstra (với đồ thị thưa). Điều này làm cho ISOMAP kém hiệu quả khi số lượng điểm dữ liệu lớn.  

 - **Không xử lý tốt manifold có lỗ hổng hoặc không liên thông:**  
	Nếu manifold của dữ liệu không liên thông hoặc chứa các khoảng trống, các đường đi ngắn nhất trên đồ thị có thể không phản ánh đúng khoảng cách thực sự giữa các điểm. Điều này khiến ISOMAP bị sai lệch hoặc không thể hoạt động chính xác.  

 - **Phụ thuộc vào tham số k trong k-NN Graph:**  
	Việc lựa chọn số lượng hàng xóm $( k )$ ảnh hưởng lớn đến chất lượng của đồ thị và kết quả của ISOMAP. Nếu $( k )$ quá nhỏ, đồ thị có thể bị rời rạc; nếu $( k )$ quá lớn, đồ thị có thể chứa cạnh không mong muốn, làm mất đi tính cục bộ của manifold.  

---

## Kết luận

- ISOMAP là một phương pháp mạnh mẽ trong giảm chiều dữ liệu phi tuyến, giúp bảo toàn cấu trúc manifold tốt hơn so với các phương pháp tuyến tính. Tuy nhiên, nhược điểm về **độ phức tạp tính toán, nhạy cảm với nhiễu, và yêu cầu liên thông của manifold** khiến nó không phải lúc nào cũng là lựa chọn tối ưu, đặc biệt khi làm việc với tập dữ liệu lớn hoặc dữ liệu không đồng nhất.  

# References
