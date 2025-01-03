2025-01-03 17:57


Tags: [[computer networking]]

# video streaming and CDNs
**context**: 
- stream video traffic: major consumer of internet bandwith
	- Netflix, Youtube, Amazon Prime: 80% of residential ISP traffic (2020)
- challenge: scale - how to reach ~1B users? 
	- single mega-video server won't work because:
		- - **High Latency:** Users located far from the server would experience delays.
		- **Bandwidth Limitations:** A single server cannot handle the immense amount of traffic simultaneously.
		- **Single Point of Failure:** If the server goes down, all users lose access.
		- **Overload Risks:** The server would be overwhelmed by billions of requests.
- challenge: heterogeneity
	- different users have different capabilities (e.g., wired versus mobile; bandwith rich versus bandwith poor)
- ***solution: distributed, application - level infrastructure***
### Multimedia: video 
- video: sequence of images display at constant rate (e.g., 24 fps)
- digital image: array of pixels 
	- each pixel represented by bits
- coding: use redundancy *within* and *between* images to decrease # bits used to encode image
	- spatial (within image)
	- temporal (from one image to next)
	![[Pasted image 20250103180428.png]]
	
- **CBR: (constant bit rate)**: video encoding rate fixed
- **VBR: (variable bit rate)**: video encoding rate changes as amount of spatial, temporal coding changes
- example:
	- MPEG (CD-ROM) 1.5 MBPS
	- MPEG2 (DVD) 3-6 MBPS
	- MPEG4 (often used in Internet, 64Kbps - 12Mbps)
![[Pasted image 20250103180606.png]]

### Streaming stored video
![[Pasted image 20250103180840.png]]
- **Main challenges**:
	- server-to-client bandwidth will *vary* orver time, with changing network congestion levels (in house, in access network, in network core, at video server)
	- packet loss and delay due to congestion will delay playout, or result in poor video quality
![[Pasted image 20250103181051.png]]

# References
