2024-12-07 02:50


Tags: [[computer networking]]


# DOMAIN NAME SYSTEM (DNS)

- *people*: have many identifiers:
	- SSN, name, pasport #,..
- *internet hosts, router*:
	- IP address (32 bit) - used for addressing datagrams
	- "name", e.g., cs.umass.edu - used by humans.
**DOMAN NAME SYSTEM (DNS)**: 
- *distributed database* implemented in hierachy of many *name servers*
- *application-layer protocol*: hosts, name servers communicate to resolve names (address/name translation)
		- note: core internet function, **implemented as application-layer protocol**
		- complexity at network's "edge"
### DNS Service and structure:
**Service**:
- hostname to IP address translation
- host aliasing
	- canonical, alias names
- mail server aliasing
	- load distribution 
	![[Pasted image 20250102172450.png]]
**Structure**:
- Is a distributed and hierarchical database.
![[Pasted image 20250102172716.png]]


![[Pasted image 20241207033802.png]] 
# References
