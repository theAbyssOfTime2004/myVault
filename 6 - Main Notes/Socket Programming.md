2025-01-04 13:40


Tags: [[computer networking]], [[socket programming with UDP and TCP]]

# Socket Programming

- **goal**: learn how to build client/server applications that communicate using sockets
- **socket**: door between application process and end-end-transport protocol 
![[Pasted image 20250104134112.png]]
- two socket types for two transport services:
	- *UDP*: unreliable datagram
	- *TCP*: reliable, byte stream-oriented
- Application Example:
	- client reads a line of characters (data) from its keyboard and sends data to server
	- server receives the data and converts characters to uppercase
	- server sends modified data to client
	- client receives modified data and display line on its screen
### Socket programming with UDP
- UDP: *no "connection" between client & server
	- no handshaking before sending data
	- sender explicitly attaches IP destination address and port # to each packet
	- receiver extracts sender IP address and port# from received packet
- UDP: *transmitted data may be lost or received out - of - order*
- Application viewpoint:
	- UDP provides unreliable transfer of groups of byte ("datagram") between client and server

# References
