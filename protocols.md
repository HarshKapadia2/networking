# Protocols

([Back to Home](README.md))

Abbr. | Name | Default Port(s) | TCP/UDP (Default) | OSI Layer | Remarks
----- | ---- | ---- | ------- | --------- | -------
AH | Authentication Header | | | Network Layer | [Learn more](ipsec.md#ah)
ALPN | Application Layer Protocol Negotiation | | | Transport Layer | TLS extention.
ARP | Address Resolution Protocol | | | Data Link Layer | [Learn more](https://www.varonis.com/blog/arp-poisoning)
BGP | Border Gateway Protocol | 179 | TCP | Network Layer | [Learn more](bgp.md)
DHCP | Dynamic Host Configuration Protocol | | | Data Link Layer
DNS | Domain Name System | 53 | [Mainly UDP, but can be TCP](https://stackoverflow.com/a/40063445/11958552) | Application Layer | [Learn more.](dns.md) DNSSEC and [DOH](https://www.youtube.com/watch?v=SudCPE1Cn6U) are enhancements.
EIGRP | Enhanced Interior Gateway Routing Protocol | | | Network Layer
ESP | Encapsulating Security Payload | | | Network Layer | [Learn more](ipsec.md#esp)
HTTP | Hyper Text Transfer Protocol | 80 | | Application Layer | [Learn more](http.md)
HTTPS | Hyper Text Transfer Protocol Secure | 443 | | Application Layer | [Learn more.](http.md) Also called 'HTTP over TLS (or SSL)'
ICMP | Internet Control Message Protocol | | | Network Layer
IGRP | Interior Gateway Routing Protocol | | | Network Layer
IKE | Internet Key Exchange | 500 (w/o NAT) & 4500 (with NAT) | UDP | Network Layer | [Learn more](ipsec.md#ike)
IMAP | Internet Message Access Protocol | 143 (insecure) & 993 (secure with TLS) | TCP | Application Layer | [Learn more](e-mail.md#imap)
IP | Internet Protocol | | | Network Layer | [Learn more](./ip.md)
IPSec | Internet Protocol Security | | | Network Layer | [Learn more](ipsec.md)
ISAKMP | Internet Security Association and Key Management Protocol | 500 (w/o NAT) & 4500 (with NAT) | UDP | Network Layer | [Learn more](ipsec.md#ikev1)
IS-IS | Intermediate System To Intermediate System | | | Network Layer
NAT | Network Address Translation | | | Network Layer
OCSP | Online Certificate Status Protocol | | | Transport Layer | TLS extension.
OSPF | Open Shortest Path First | | | Network Layer
POP3 | Post Office Protocol 3 | 110 (insecure) & 995 (secure with TLS) | TCP | Application Layer | [Learn more](e-mail.md#pop3)
RIP | Routing Information Protocol | | | Network Layer
SCP | Secure Copy | 22
SFTP | Secure/SSH File Transfer Protocol | 22
SMTP | Simple Mail Transfer Protocol | 25 (default, insecure), 2525 (insecure), 587 (secure with TLS) & 465 (deprecated, secure with TLS) | TCP | Application Layer | [Learn more](e-mail.md#smtp)
SNI | Server Name Indication | | | Transport Layer | TLS extension.
SSH | Secure Shell | 22 | TCP | Application Layer | [Learn more](./ssh.md)
SSL | Secure Sockets Layer | | | Transport Layer | Almost replaced by [TLS](tls.md).
TCP | Transmission Control Protocol | | - | Transport Layer | [Learn more](./tcp.md)
TLS | Transport Layer Security | | | Transport Layer | [Learn more](tls.md)
UDP | User Datagram Protocol | | - | Transport Layer | [Learn more](https://hpbn.co/building-blocks-of-udp)

## Resources

-   [Well known port numbers](https://www.meridianoutpost.com/resources/articles/well-known-tcpip-ports.php)
-   [List of network protocols (OSI model)](https://en.wikipedia.org/wiki/List_of_network_protocols_(OSI_model))
