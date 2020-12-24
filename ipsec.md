# IPSec

- The IP Security (IPSec) Protocol is a Network Layer encryption protocol most commonly used in VPNs (either to securely browse the internet or to securely connect to a remote network).
- It is used to make a secure tunnel between the client and the server (or target machine).
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


## Encapsulation

- IPSec encapsulates the usual TCP/IP packets and adds headers to the target remote network IP and other values of the remote network.
- The inner IP header usually has internal IP addressing (the internal IPs in the remote network) and the outer IP header has the public IP addressing (required to send packets to the remote network).
- IPSec security protocols help encrypt the data being transported over the network.

<p align="center">
  Usual TCP/IP packet :point_down:
  <br />
  <img src="https://user-images.githubusercontent.com/50140864/103090432-fe9f2700-4616-11eb-8aff-2ea1efb0ca93.png" />
  <br />
  <br />
  Encapsulated TCP/IP packet :point_down:
  <br />
  <img src="https://user-images.githubusercontent.com/50140864/103090471-15de1480-4617-11eb-9522-c100a054fcd7.png" width="20%" />
</p>


## IKE

- The Internet Key Exchange (IKE) Protocol helps with policy and key management to encrypt data and form security associations (SAs).
- This protocol runs on port 500 and uses UDP.
- It is the first step before using either AH or ESP for securing the encapsulation.
- IKEv1 has 2 phases while IKEv2 has a 1 step negotiation process.

### IKEv1

> NOTE: 'Payload' refers to all the data inside the encapsulation (including the TCP and inner IP info).

- Phase 1
  - Create an ISAKMP SA. (ISAKMP = Internet Security Association and Key Management Protocol)
  - Used for management for exchange of info and diagnostics.
  - Bi-directional SA, as both need to come to an agrement on how to communicate.
  - Negotiate Policy Set with target machine
    - Hashing (data integrity)
    - Authentication (Certificates, etc)
    - [Diffie-Hellman Group](https://www.omnisecu.com/tcpip/what-is-diffie-hellman-group.php)
    - Lifetime (How long should the IKE tunnel live for. Shorter the lifetime, more the security, as there will frequently be new keys.)
    - Encryption (AES, triple DES, etc)
- Phase 2
  - Create an IPSec SA.
  - Each side creates a Transform Set, which decides how each one is going to encrypt the actual data (payload).
  - One SA is created by each side, so IPSec SAs are uni-directional.
  - So, two SAs are created in this phase. (Inbound and outbound.)
  - Each SA will have a SPI (Security Parameter Index - a random 32 bit number) attached to it, so later on while communicating, they can be compared with all the SPIs that the machine has received and on matching with one, the machine can take the steps to decrypt the payload.


## Security protocols

> NOTE: 'Payload' refers to all the data inside the encapsulation (including the TCP and inner IP info).

### AH

- IPSec AH (Authentication Header) Protocol
- Provides origin authenticity.
- AH provides an integrity check for both the payload and the outer IP header.
- If NAT occurs on the outer IP header, AH will complain due to the resulting mismatch in the integrity check.
- AH does not encrypt the payload, so this method is mostly obsolete.

### ESP

- IPSec ESP (Encapsulating Security Payload) Header Protocol
- ESP provides an integrity check for the payload, but not for the outer IP header.
- ESP does not complain if NAT occurs on the outer IP header, because it does not check the integrity of the outer IP header.
- ESP encrypts the payload.


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

- [VPN & Remote Working](https://www.youtube.com/watch?v=1mtSNVdC7tM)
- [What is IPSec VPN and How Does it Work?](https://www.youtube.com/watch?v=pphB1pONPPU)
- [Understanding AH vs ESP and ISAKMP vs IPSec in VPN tunnels](https://www.youtube.com/watch?v=rwu8__GG_rw)
- IKE
  - [IKE phase 1 negotiation](https://www.youtube.com/watch?v=_oTcicLqyyY)
  - [Principle of IKEv1 and IKEv2](https://www.youtube.com/watch?v=wM3aIbF1IVs&list=PLzAnmgsb6R14VW6LET39B-pedj6dp5wQw&index=22)
