# OSI Layers

No. | Name | Protocol(s) | Remarks
--- | ---- | --------- | -------
7 | Application Layer | DNS, HTTP, HTTPS, IMAP, POP3, SMTP | Concerned with headers, cookies, content, etc.
6 | Presentation Layer |  | Concerned with encryption.
5 | Session Layer | | Attach session tag.
4 | Transport Layer | ALPN, OCSP, SNI, SSL, TCP, TLS, UDP | Attach ports and sequence nos. Each individual part is called a segment.
3 | Network Layer | AH, BGP, EIGRP, ESP, ICMP, IGRP, IKE, IP, IPSEC, ISAKMP, IS-IS, OSPF, RIP | Attach IP add. Each individual part is called a packet.
2 | Data Link Layer | ARP, DHCP | Attach MAC add. Each individual part is called a frame.
1 | Physical Layer | | Data transfer in 1s and 0s.

<p align="center">
  <br />
  <br />
  <img src="https://user-images.githubusercontent.com/50140864/101920490-e3352480-3bf1-11eb-8a76-18fc51052498.png" />
</p>


## Resources

- [The OSI Model](https://www.youtube.com/watch?v=7IS7gigunyI)
- [Encapsulation explained and why Ping (part of ICMP) doesn't work at layer three](https://www.youtube.com/watch?v=2shvrp0-yHw) and even then [ICMP is considered as a layer three protocol](https://serverfault.com/questions/511965/why-is-icmp-categorized-as-a-layer-3-protocol).
- [Protocols](protocols.md)
