2025-04-04 15:25


Tags: [[data mining]], [[data scientist]]

# ISOMAP

## 1. Tiếp Cận Vấn Đề
### Vấn đề với khoảng cách Euclidean truyền thống
- Trong phân phối dữ liệu phi tuyến, khoảng cách Euclidean truyền thống có thể gây hiểu nhầm. Ví dụ trong hình 3.4, nếu chỉ dựa vào khoảng cách Euclidean, điểm A và B có vẻ gần nhau, nhưng xét theo cấu trúc toàn cục của dữ liệu, chúng thực sự rất xa nhau.
![[Pasted image 20250404153334.png]]
- Khoảng cách Euclidean giữa hai điểm x và y được định nghĩa như sau:
### Khái niệm Geodesic
- Khoảng cách được hiểu là độ dài ngắn nhất của đường đi từ một điểm dữ liệu đến điểm khác, khi chỉ sử dụng các bước nhảy ngắn từ điểm này sang điểm lân cận gần nhất (k-nearest neighbors). Trong Hình 3.4, để đi từ A đến B phải đi dọc theo toàn bộ hình elip của phân phối dữ liệu và đi qua C, nên A và B thực sự là cặp điểm xa nhau nhất!
# References
