2025-01-02 15:35


Tags: [[computer networking]]

# Web caches (Proxy server)
**Goal**: Satisfy client request without involving origin server. 
- user configures browser to point to a *Web cache*.
- browsers send all HTTP requests to cache.
	- *if* object in cache: cache returns object to client.
	- *else* (object not in cache): cache request object from origin server, caches received object, then returns object to client.
	![[Pasted image 20250102154142.png]]
- Web cache acts as both client and server:
	- server for original requesting client.
	- client to origin server.
- typically cache is installed by ISP (university, company, residential ISP).
*Why is web caching?* :
- reduce response time for client request (since cache is closer to client).
- reduce traffic on an institution's access link 
- internet is densed with caches.
	- enable "poor" content providers to more efficiently deliver their contents.

# References
