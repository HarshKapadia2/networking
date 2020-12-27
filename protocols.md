# Protocols

Abbr. | Name | Port | TCP/UDP | OSI Layer | Remarks
----- | ---- | ---- | ------- | --------- | -------
AH | Authentication Header | | | Network Layer | [Learn more.](ipsec.md#ah)
ARP | Address Resolution Protocol | | | Data Link Layer
DHCP | Dynamic Host Configuration Protocol | | | Data Link Layer
DNS | Domain Name Server | 53
ESP | Encapsulating Security Payload | | | Network Layer | [Learn more.](ipsec.md#esp)
HTTP | Hyper Text Transfer Protocol | 80 | | Application Layer | [Learn more.](http.md)
HTTPS | Hyper Text Transfer Protocol Secure | 443 | | Application Layer | [Learn more.](http.md) Also called 'HTTP over TLS (or SSL)'
ICMP | Internet Control Message Protocol | | | Network Layer
IKE | Internet Key Exchange | 500 (w/o NAT) & 4500 (with NAT) | UDP | Network Layer | [Learn more.](ipsec.md#ike)
IMAP | Internet Message Access Protocol | 143 (insecure) & 993 (secure with TLS) | TCP | Application Layer | [Learn more.](e-mail.md#imap)
IP | Internet Protocol | | | Network Layer
IPSec | Internet Protocol Security | | | Network Layer | [Learn more.](ipsec.md)
ISAKMP | Internet Security Association and Key Management Protocol | 500 (w/o NAT) & 4500 (with NAT) | UDP | Network Layer | [Learn more.](ipsec.md#ikev1)
OCSP | Online Certificate Status Protocol | | | Transport Layer | TLS extension
POP3 | Post Office Protocol 3 | 110 (insecure) & 995 (secure with TLS) | TCP | Application Layer | [Learn more.](e-mail.md#pop3)
RIP | Routing Information Protocol | | | Network Layer
SMTP | Simple Mail Transfer Protocol | 25 (default, insecure), 2525 (insecure) & 465 (secure with TLS) | TCP | Application Layer | [Learn more.](e-mail.md#smtp)
SNI | Server Name Indication | | | Transport Layer | TLS extension
SSL | Secure Sockets Layer | | | Transport Layer | Almost replaced by TLS.
TCP | Transmission Control Protocol | | - | Transport Layer
TLS | Transport Layer Security | | | Transport Layer | [Learn more.](tls.md)
UDP | User Datagram Protocol | | - | Transport Layer

## Resources

- [Well known port numbers](https://www.meridianoutpost.com/resources/articles/well-known-tcpip-ports.php)
