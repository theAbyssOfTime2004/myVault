2024-12-07 02:50


Tags: [[computer networking]], [[The Domain Name System DNS]]


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

**Root Name Server**: official, contact-of-last-resort by name servers that can not resolve name
- is an *increadibly important* internet function.
	- internet couldn't function without it.
	- DNSSEC - provide security (authentication and message integrity)
- ICANN (Internet Corporation for Assigned Names and Numbers) manages root DNS domain.
![[Pasted image 20250103162249.png]]

### TLD: authoritative servers
**Top-level domain (TLD) servers**: 
- responsible for .com, .org, .net, .edu, .aero, .jobs, .museum, and all top-level country domains , e.g.: .cn, .uk, .fr, .ca, .jp
- Network Solutions: authoritative registry for .com, .net TLD
- Educause: .edu TLD
**Authoritative DNS servers:**
- Organization's own DNS server(s), providing authoritative hostname to IP mappings for organization's named hosts.
- Can be maintained by organizations or service provider.
### Local DNS name servers
- does not strictly belong to hierarchy
- each ISP (residential ISP, company, university) has one.
	- also called "default name server"
- when host makes DNS query, query is sent to its local DNS server.
	- has local cache of recent name-to-address translation pairs (but may be outdated)
	- acts as a proxy, forward query into hierarchy

![[Pasted image 20241207033802.png]] 
# References
