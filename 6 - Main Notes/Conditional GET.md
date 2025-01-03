2025-01-02 15:51


Tags: [[computer networking]] [[Web and HTTP]]

# Conditional GET
**Goal**: don't send object if cache has up-to-date cached version.
	- no object transmission delay.
	- lower link utilization.
- *cache*: specify date of cached copy in HTTP request 
	`if-modified-since:<date>`
- *server*: response contains no  object if cached copy is up-to-date:
	`HTTP/1.0 304 not Modified`
![[Pasted image 20250102155721.png]]

# References
