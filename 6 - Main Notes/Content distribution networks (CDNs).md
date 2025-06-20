2025-01-03 18:28


Tags: [[computer networking]], [[video streaming and content distribution networks]]

# Content distribution networks (CDNs)

- challenge: how to stream content (selected from millions of videos) to hundreds of thousands of *simultaneous* users?
- *option 1*: single, large "mega-server"
	-  single point of failure 
	- point of network congestion 
	- long path to distant clients 
	-  multiple copies of video sent over outgoing link
=> ***doesn't scale***
- *option 2*: store/serve multiple copies of videos at multiple geographically distributed sites *(CDN)*
	- *enter deep*: push CDN servers deep into many access networks
		- close to users
		- Akamai: 240.000 servers deployed in more than 120 countries (2015)
	- *bring home*: smaller number (10's) of larger cluster in POPs near (but not within) access networks
		- used by Limelight
### CDNs
- CDN: stores copies of content at CDN nodes
	- e.g. Netflix stores copies of MadMen
- subcriber requests content from CDN
	- directed to nearby copy, retrieves content
	- may choose different copy if network path congested
![[Pasted image 20250103183426.png]]
![[Pasted image 20250103183438.png]]
### CDN content access: a closer look
- Bob (client) requests video `http://netcinema.com/6Y7B23V`
	- video stored in CDN at  `http://KingCDN.com/NetC6y&B23V` 
	![[Pasted image 20250103183545.png]]
### Case study: Netflix
![[Pasted image 20250103183608.png]]
# References
