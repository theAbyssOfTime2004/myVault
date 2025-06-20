2025-01-03 17:47


Tags: [[computer networking]], [[P2P applications]]

# BitTorrent

- filed divided into 256kb chunks
- peers in torrent send/receive file chunks
![[Pasted image 20250103174828.png]]
- peer joining torrent:
	- has no chunks, but will accumulate them over time from other peers
	- registers with tracker to get list of peers, connect to subset of peers ("neighbour")
- while downloading, peer uploads chunks to other peers
- peer may change peers with whom it exchanges chunks
- *churn*: peers may come and go
- once peer has entire file, it may (selfishly) leave or (altruistically) remain in torrent
### Requesting, sending file chunks
- **Requesting chunks:**
	- at any given time, different peers have different subsets of file chunks
	- periodically, Aice asks each peer for list of chunks that they have
	- Alice requests missing chunks from peers, rarest first
- **Sending chunks: tit-for-tat**
	- Alice sends chunks to those four peers currently sending her chunks at highest rate
		- other peers are choked by Alice (do not receive chunks from her)
		- re-evaluate top 4 every 10sec
	- every 30 secs: randomly select another peer, starts sending chunks
		- "optimistically unchoke" this peer
		- newly chosen peer may join top 4
	![[Pasted image 20250103175648.png]]
	
# References
