2025-01-03 16:36


Tags: [[computer networking]]

# DNS name resolution
**example**: host at *engineering.nyu.edu* wants IP address for *gaia.cs.umass.edu*
### Iterated query:
- contacted server replies with name of server to contact
- "I dont know this name, but ask this server".
![[Pasted image 20250103163911.png]]
In an iterated query, the contacted DNS server replies either with the answer or with the name of another server to contact. The steps are as follows:

1. **Step 1**:
    - The requesting host at `engineering.nyu.edu` sends a query to its **local DNS server** (`dns.nyu.edu`), asking:  
        _"What is the IP address of `gaia.cs.umass.edu`?"_
2. **Step 2**:
    - The **local DNS server** doesn’t know the IP address, so it forwards the query to the **root DNS server**.
3. **Step 3**:
    - The **root DNS server** responds, saying:  
        _"I don’t know the IP address, but you should ask the Top-Level Domain (TLD) DNS server for `.edu`."_  
        It provides the address of the **TLD DNS server**.
4. **Step 4**:
    - The local DNS server forwards the query to the **TLD DNS server** responsible for `.edu`.
5. **Step 5**:
    - The **TLD DNS server** responds:  
        _"I don’t know the IP address, but you should ask the authoritative DNS server for `cs.umass.edu`."_  
        It provides the address of the **authoritative DNS server**.
6. **Step 6**:
    - The local DNS server sends the query to the **authoritative DNS server** for `cs.umass.edu`.
7. **Step 7**:
    - The **authoritative DNS server** responds with the exact IP address of `gaia.cs.umass.edu`
8. **Step 8**:
    - The local DNS server receives the IP address and sends it back to the requesting host at `engineering.nyu.edu`.

### Recursive query: 
- puts burden of name resolution on contacted name server.
- heavy load at upper levels of hierarchy.
![[Pasted image 20250103164516.png]]
In a recursive query, the contacted DNS server performs the entire resolution process and provides the final answer to the requester. The steps are as follows:

1. **Step 1**:
    - The requesting host at `engineering.nyu.edu` sends a query to its **local DNS server** (`dns.nyu.edu`), asking:  
        _"What is the IP address of `gaia.cs.umass.edu`?"_
2. **Step 2**:
    - The **local DNS server** does not know the IP address, so it takes on the responsibility of finding it.
    - It forwards the query to the **root DNS server**.
3. **Step 3**:
    - The **root DNS server** responds to the local DNS server, saying:  
        _"I don’t know the IP address, but you should ask the TLD DNS server for `.edu`."_  
        It provides the address of the **TLD DNS server**.
4. **Step 4**:
    - The local DNS server sends the query to the **TLD DNS server** for `.edu`.
5. **Step 5**:
    - The **TLD DNS server** responds, saying:  
        _"I don’t know the IP address, but you should ask the authoritative DNS server for `cs.umass.edu`."_  
        It provides the address of the **authoritative DNS server**.
6. **Step 6**:
    - The local DNS server sends the query to the **authoritative DNS server** for `cs.umass.edu`.
7. **Step 7**:
    - The **authoritative DNS server** responds with the exact IP address of `gaia.cs.umass.edu`.
8. **Step 8**:
    - The **local DNS server** sends the resolved IP address back to the requesting host at `engineering.nyu.edu`.

![[Pasted image 20250103165407.png]]


# References
