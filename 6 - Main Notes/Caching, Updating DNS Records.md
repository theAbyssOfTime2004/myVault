2025-01-03 16:55


Tags: [[computer networking]]

# Caching, Updating DNS Records

- once (any) name server learns mapping, it caches mapping
	- cache entries timeout (disappear) after some time (time to live TTL)
	- TLD servers typically cached in local name servers
		- thus root name servers not often visited
- cached entries maybe out-of-date (*best-effort name to address translation!*)
	- if name host changes IP address, may not be known Internet_wide until all TTLs expire!
- update, notify mechanisms proposed IETF standard 
	- RFC 2136

# References
