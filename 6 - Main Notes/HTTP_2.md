2025-01-02 16:00


Tags: [[computer networking]]

# HTTP_2
**goal**: decreased delay in *multi-object HTTP request*.
### HTTP 1.1:
- introduced *multiple, pipeline GETS* over single TCP connection.
	- server responds in-order (FCFS: *first come first serve* scheduling) to GET requests.
	- With FCFS, small object may have to wait for transmission behind large objects (so called *head of line* or *HOL* blocking).
	- loss recovery (retransmitting lost TCP segments) stalls object transmission.
### HTTP_2:
- increased flexibility at server in sending objects to client:
	- methods, status code,  most header fields are unchanged from HTTP 1.1.
	- transmission order of requested objects based on *client-specified object priority* (not necessarily FCFS).
	- *push* unrequested objects to client.
	- divide objects into frames, schedule frames to mitigates *HOL* blocking. 
### Mitigating HOL blocking:
- **HTTP 1.1**: client requests 1 large object (e.g., video files and 3 smaller objects)
 ![[Pasted image 20250102160836.png]]
 - **HTTP_2**: objects divided into frames, frame transmission interleaved.
 ![[Pasted image 20250102160928.png]]

### HTTP_2 to HTTP_3:
- HTTP_2 over single TCP connection means:
	- recovery from packet loss still stalls all object transmissions.
		- as in HTTP 1.1, browsers have incentive to open multiple parallel TCP connections to reduce stalling, increase overall throughput.
	- no security over vanilla TCP connection.
- **HTTP 3**: add security, per object error-and congestion-control (more pipelining) over UDP 
	- more on HTTP 3 transport layer.
![[Pasted image 20250102161320.png]]

# References
