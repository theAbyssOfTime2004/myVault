2025-01-03 18:20


Tags: [[computer networking]], [[video streaming and content distribution networks]]

# Streaming Multimedia - DASH
- **DASH**: Dynamic, Adaptive Streaming over HTTP
- *server*:
	- divides video file into multiple chunks
	- each chunk stored, encoded at different rates
	- *manifest file*: provides URLs for different chunks
- *client*:
	- periodically measures server-to-client bandwidth
	- consulting manifest, requests one chunk at a time
		- chooses maximum coding rate sustainable given current bandwidth
		- can choose different coding rates at different points in time (depending on available bandwidth at time)
- *"intelligence" at client*: client determines
	- *when* to request chunk (so that buffer starvation, or overflow does not occur)
	- *what encoding rate* to request (higher quality when more bandwidth available)
	- *where* to request chunk (can request from URLs server that is "close" to client or has highest available bandwidth)
- *Streaming video* = encoding + DASH + playout buffering

# References
