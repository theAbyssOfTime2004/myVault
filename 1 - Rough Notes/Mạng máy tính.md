[[computer networking]], [[Web and HTTP]]

- every computer must include
	- cookies (for maintaining user/server state between transactions) 
	- Recall: HTTP GET/ response interaction is stateless
	- cookies contain:
		- basic
		- application
		- combination
		- optimization
	- cookies have 4 components:
		- cookie header line of HTTP *response* msg
		- cookie header line in next HTTP *request* msg
		- cookie file kept on users host 
		- back end database at website
	- cache 
		- web caches (proxy server): satisfy client request without involving origin server
		- web cache acts as both client and server 
			- server for original requesting client
			- client to origin server
		- caching example: install a web cache
			- (calculating access link utilization, end to end delay with cache) which will result in much lower end to end delay than to without installing cache, and pretty cheap when comparing to update access link data rate.
	- HTTP (key goal: decreased delay in multi-object HTTP requests)
		- HTTP 1.1
		- HTTP 2: over single TCP connection
			- mitigating HOL blocking: objects devided into frames, frame transmission interleaved
		- HTTP 3: adds security, per object error and congestion-control (more pipelining) over UDP
- ![[Pasted image 20250103190446.png]]
- payload = tải trọng = app + data 
- ![[Pasted image 20250104145124.png]]
- 4861 = tổng tất cả các payload $!=$ tổng tất cả các gói tin
- redirection = status code 301
-  Can you tell whether your browser downloaded the two images serially, or whether they were downloaded from the two web sites in parallel? - *Parallel* 
- nslookup : The _nslookup_ command is a network administration tool used to query the Domain Name System (DNS) to obtain domain name or IP address mapping information
- The **`nslookup -type=NS`** command is used to query the **Name Server (NS) records** of a domain. NS records specify the authoritative DNS servers for a domain, meaning the servers that are responsible for handling DNS queries for that domain.
- ![[Pasted image 20250104153222.png]]
- ![[Pasted image 20241207033802.png]]
	- client (192.168.1.113) gửi dns query đến dns server (local - 192.168.1.1) hỏi rằng địa chỉ ip của server hvthao2.ddns.net là gì 
	- sau đấy dns server (local - 192.168.1.1) trả lời (response) địa chỉ ip của server hvthao2.ddns.net là 14.161.12.235 
	- sau đấy client gửi http request qua server hvthao2.ddns.net


| Layers    |          |
| --------- | -------- |
| APP       | http dns |
| TRANSPORT | tcp udp  |
| NETWORK   | ip icmp  |
| LINK      | ethernet |
| PHYSIC    |          |

- max size of udp payload = $2^{16} - 1 -8$ = $2^{16} - 9$ (B) which is nearly 64KB
- 