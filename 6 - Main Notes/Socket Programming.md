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
	- ==UDP provides unreliable transfer of groups of byte ("datagram") giải between client and server==
![[Pasted image 20250104135600.png]]
- **Server**: Creates a socket → Receives data from the client → Sends a reply.
- **Client**: Creates a socket → Sends data to the server → Receives a reply → Closes the socket.
- UDP is a simple, connectionless protocol that prioritizes speed and efficiency but does not guarantee data delivery or order.
### Socket programming with TCP
- *Client must contact server*
	- server process must first be running
	- server must have created socket (door) tht welcomes client's contact
- *Client contacts server by*:
	- creating TCP socket, specifying IP address, port number of server process.
	- *when client creates socket*: client TCP establishes connection to server TCP
- when contacted by client, *server TCP creates new socket* for server process to communicate with that particular client
	- allows server to talk with multiple clients
	- source port numbers used to distinguish clients 
- Application viewpoint
	- ==TCP provides reliable in-order byte-stream transfer ("pipe") between client and== 
![[Pasted image 20250104140245.png]]
- **Server**:
    - Creates a listening socket → Waits for client connection → Accepts connection → Reads/writes data → Closes the connection socket.
- **Client**:
    - Creates a socket → Connects to the server → Sends data → Receives data → Closes the socket.
### Comparison to UDP:
- **TCP**:
    - Reliable, ordered delivery of data.
    - Connection-oriented (requires setup and teardown of connections).
    - Suitable for applications like file transfers, web browsing, or email.
- **UDP**:
    - Faster, but unreliable.
    - Connectionless (no setup required).
    - Suitable for real-time applications like video streaming or online gaming.

# References
