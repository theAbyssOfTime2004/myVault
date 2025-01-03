2025-01-03 16:55


Tags: [[computer networking]]

# Caching, Updating DNS Records

- once (any) name server learns mapping (address - IP), it caches mapping
	- cache entries will be timeout (disappear) after some time (time to live TTL)
	- TLD servers are typically cached in local name servers
		- since they are not usally queried to by root name server
- cached entries maybe out-of-date (*best-effort name to address translation!*)
	- if name host changes IP address, may not be known Internet_wide until all TTLs expire!
- update, notify mechanisms proposed IETF standard 
	- RFC 2136
### DNS Records
**DNS**: distributed database storing resource records `(RR)`
- RR format: (`name, value, type, ttl`)
- *Type=A* 
	- `name` is hostname
	- `value` is IP address
- *Type=NS* 
	- `name` is domain (e.g., foo.com)
	- `value` is hostname of authoritative nameserver for this domain
- *Type=CNAME* 
	- `name` is allias name for some "canonical" (the real) name
	- www.ibm.com  is really servereast.backup2.ibm.com
	- `value` is canonical name
- *Type=MX* 
	- `value` is name of mailserver associated with `name`

### DNS protocol messages
- DNS *query* and *reply* msgs, both have the same *format*:
![[Pasted image 20250103171040.png]]
![[Pasted image 20250103171057.png]]

### Inserting Records into DNS
**Example**: new startup "Network Utopia"
- register name `networkutopia.com` at *DNS registrar* (e.g., Network Solutions)
	- provide names, IP addresses of authoritative name server (primary and secondary).
	- registrar inserts NS, A RRs into .com TLD server:
		- `(networkutopia.com, dns1.networkutopia.com, NS)`
		- `(dns1.networkutopia.com, 212.212.212.1, A)`
	- create authoritative server locally with IP address `212.212.212.1` 
		- type A record for `www.networkuptopia.com`
		- type MX record for `networkutopia.com`

### DNS security 
- **DDOS attack**: 
	- bombard root servers with traffic
		- not successful to date
		- traffic filtering 
		- local DNS servers cache IPs of TLD servers, allowing root server to bypass.
	- bombard TLD servers
		- potentailly more dangerous 
- **Redirect attack**: 
	- man-in-middle:
		- intercept DNS queries
	- DNS poisoning:
		- send bogus replies to DNS server, which caches
- **Exploit DNS for DDOS**:
	- send queries with spoofed source address: target IP
	- requires amplification
- **DNSSEC (RFC 4033):**
- Is a proposed security solution to prevent various types of attacks on DNS.
- Provides mechanisms for authentication and data integrity for DNS.
# References
