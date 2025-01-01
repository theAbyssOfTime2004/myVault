2025-01-01 21:58
[[computer networking]]
Tags:

# Cookies
### HTTP GET/response interaction is stateless
- Mỗi request từ http được gửi từ client đến server là độc lập với nhau.
- Server không lưu trữ bất kỳ thông tin nào về trạng thái của các giao thức trước đó với client.
Điều này dẫn đến:
- Không cần máy chủ hoặc trình duyệt duy trì "trạng thái" của một chuỗi giao tiếp nhiều bước.
- Không cần khôi phục từ các giao dịch không hoàn chỉnh.
**cookies**: Cookies giúp giải quyết vấn đề **stateless** của HTTP bằng cách lưu thông tin trạng thái (như phiên đăng nhập) ở phía trình duyệt và gửi nó cùng mỗi yêu cầu, cho phép duy trì trạng thái trong các giao dịch nhiều bước mà không cần biến HTTP thành stateful.
- 4 thành phần của cookies: 
	**1.** Dòng header của cookie trong HTTP response message: 
	-  Khi server muốn lưu cookie, server gửi 1 dòng set-cookie trong http response đến client.
	**2.** Dòng header của cookie trong HTTP request message tiếp theo: 
	- Ở các yêu cầu tiếp theo, trình duyệt gửi giá trị cookie trở lại server qua header của HTTP request.
	**3.** File lưu code trên máy tính người dùng:
	- Cookie được trình duyệt lưu trữ trong 1 file ở máy người dùng và trình duyệt tự động giúp cookie đó khi gửi yêu cầu đến đúng website.
	**4.** Cơ sở dữ liệu bên phía server.
	- Server lưu thông tin tương ứng với giá trị cookie.
### State maintaining:
- Protocol endpoints: trạng thái được duy trì tại các đầu cuối của giao thức, và còn đảm bảo dữ liệu lưu trữ qua nhiều giao dịch.
- cookies: Dữ liệu trạng thái được truyền qua các thông điệp HTTP, làm cầu nối giữa client và server.
### Aside: 
- cookies: tiết lộ thông tin, các web dùng cookies thu thập hành vi và sở thích của người dùng.
- tracking cookies: được bên 3 sử dụng để theo dõi danh tính người dùng trên web.
- Điều này dẫn đến việc xây dựng hồ sơ người dùng dựa trên hành vi (thường gây ra lo ngại về quyền riêng tư).
# References
