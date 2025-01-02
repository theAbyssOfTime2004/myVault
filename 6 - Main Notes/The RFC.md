2025-01-02 16:50


Tags: [[computer networking]]

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


# References
