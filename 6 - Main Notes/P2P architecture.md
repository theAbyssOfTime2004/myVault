2025-01-03 17:29


Tags: [[computer networking]]

# P2P architecture

- No always-on server
- arbitrary end systems directly communicate
- peers request service from other peers, provide service in return to other peers
	- *self scalability - new peers bring new service capacity, and new service demands*
- peers are intermittenly connected and change IP addresses
	- complex management 
- examples: P2P file sharing (BitTorrent), streaming (KanKan), VoIP (Skype)
### File distribution: client-server vs P2P
*Q*: how much time to distribute file (size F) from one server to N peers?
	- Peer upload/download capacity is limited resource
![[Pasted image 20250103173503.png]]
**CLIENT-SERVER**:
![[Pasted image 20250103173546.png]]
**P2P**:
![[Pasted image 20250103173606.png]]
**Client - server vs P2P**: example
![[Pasted image 20250103173709.png]]
# References
