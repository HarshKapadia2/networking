# IPSec

- The IP Security Protocol (IPSec) is a Network Layer encryption protocol most commonly used in VPNs (either to securely browse the internet or to securely connect to a remote network).
- It is supported by both IPv4 and IPv6.


## Features

- Anti-replay protection
- Perfect forward safety
- Data origin authenticity
- Transparency
- Dynamic re-keying
- Confidentiality


## Operation modes

- Transport
  - Cryptographic operations are performed by both source and destination hosts and encrypted data is sent using L2TP.
- Tunnel
  - Cryptographic operations are performed by special gateways as well as source and destination hosts.


## Security protocols

- IPSec AH (Authentication Header)
- IPSec ESP (Encapsulating Security Payload) header


## Advantages

- It is supported by all major devices.
- It is stable while switching networks or re-connecting.
- Offers high grade encryption.
- Operates at the network level.


## Disadvantages

- It can be blocked using firewalls.
- Slow due to data being encapsulated twice.
- Takes a significant amount of bandwidth and time.
- Relatively difficukt to configure than [SSL (TLS)](tls.md).


## Resources

- [What is IPSec VPN and How Does it Work?](https://www.youtube.com/watch?v=pphB1pONPPU)
