2025-01-02 16:50


Tags: [[computer networking]], [[Email, SMTP, IMAP]]

# The RFC (5321)
- uses TCP to reliably transfer email msg from client (mail server initiating connection) to server, port 25.
- direct transfer: sending server (acting like client) to receiving server.
- 3 phases of transfer:
	- handshaking (greeting)
	- transfer of msgs
	- closure
- command/response interaction (like HTTP) 
	- *command*: ASCII text
	- *response*: status code and phrase
- msg must be in 7-bit ASCII
![[Pasted image 20250102165340.png]]



| Đặc điểm                   | smtp                               | http                              |     |
| -------------------------- | ---------------------------------- | --------------------------------- | --- |
| cơ chế hoạt động           | Push                               | Pull                              |     |
| tương tác                  | ASCII command/response             | ASCII command/response            |     |
| phương thức giữa đối tượng | nhiều đối tượng trong 1 thông điệp | Mỗi đối tượng là 1 phản hồi riêng |     |
| Kết nối                    | liên tục                           | thường đóng sau khi mở phản hồi   |     |
| Mã hóa nội dung            | 7 bit ASCII                        | không yêu cầu                     |     |
| ký tự kết thúc             | CRLF.CRLF                          | không yêu cầu                     |     |
- *SMTP*: delivery/storage of e-mail msgs to receiver's server
- mail access protocol: retrieval from server
- IMAP: INTERNET MAIL ACCESS PROTOCOL (*RFC3501*): msgs stored on server, IMAP provides retrieval, deletion, folders of stored msgs on server.
- *HTTP*: gmail, Hotmail,etc,... provides web-based interface on top of  SMTP (to send), IMAP (or POP) to retrieve email msgs.

# References
