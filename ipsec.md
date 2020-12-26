# IPSec

- The IP Security (IPSec) Protocol is a Network Layer encryption protocol most commonly used in VPNs (either to securely browse the internet or to securely connect to a remote network) that is used to create P2P (point to point) associations between tunnel endpoints.
- It encrypts and authenticates IP packets.
- It is used to make a secure tunnel between the client and the server (or target machine).
- It is supported by both IPv4 and IPv6.


## Features

- Anti-replay protection
- Perfect forward safety
- Data origin authenticity
- Data integrity
- Transparency
- Dynamic re-keying (Keys expire relatively frequently to improve security and they are automatically re-negotiated by the pprotocol)
- Confidentiality


## IKE

- The Internet Key Exchange (IKE) Protocol helps with policy and key management to encrypt data and form security associations (SAs).
- It is the first step before using either AH or ESP for securing the payload.
- Security Associations (SAs) are an agreement of IKE and IPSec params.
- This protocol runs on port 500 and uses UDP.
- IKEv1 has 2 phases while IKEv2 has a 1 step negotiation process.

### IKEv1

#### Negotiation modes

The origin machine proposes a connection to the target machine and that proposal can occur in two modes.

- Main mode
  - Uses six messages.
  - Takes a longer time than agressive mode.
  - More secure than agressive mode as it hides the ISAKMP IDs (IP, domain name, certificate, etc).
- Agressive mode
  - Uses three messages.
  - Allows flexible authentication.
  - Less secure than main mode as it does not hide the ISAKMP IDs (IP, domain name, certificate, etc).

#### Negotiation

- Phase 1 (Control/Management plane)
  - Main goal: To authenticate the endpoints and form a temporary secure tunnel to facilitate the exchange of cryptographic properties, keys, etc.
  - Create an ISAKMP SA. (ISAKMP = Internet Security Association and Key Management Protocol)
  - Used for management for exchange of info and diagnostics.
  - Bi-directional SA, as both need to come to an agrement on how to communicate.
  - Negotiate Policy Set with target machine
    - Hashing (Eg: MD5, SHA1, etc.) (To check data integrity.)
    - Authentication (Eg: pre-shared key, RSA signatures using PKI, certificates, etc.)
    - [Diffie-Hellman Group](https://www.omnisecu.com/tcpip/what-is-diffie-hellman-group.php) (Larger the group number, more is the range of the random prime number generation, but more is the processing power used to generate the number.)
    - Encryption (Eg: AES, AES 256, DES, triple DES, etc.)
  - Uses UDP on port 500 if NAT is not being used. (If the packet is not originating from a local network, but from a public IP, NAT is not needed.)
  - If no public IP, the UDP is used on port 4500 for NAT.
- Phase 1.5
  - Optional negotiations for Extended Authentication (XAUTH), Mode Configuration (mode-config), etc.
- Phase 2 (Data plane)
  - Main goal: Estabish encrypted tunnel to send user data securely, by negotiating data protection params.
  - Uses the Quick mode and does its work in two messages as a authentication has already been done.
  - Negotiate Policy Set with target machine
    - Encapsulation protocol, encryption and authentication methods
      - [IPSec security protocol (ESP or AH)](#security-protocols)
      - Hashing algo (MD5, SHA1, SHA256, etc.)
      - Encryption cipher (DES, 3DES, AES, AES256, etc.)
      - IPSec mode (Transport or Tunnel)
    - Proxy identities
      - Defines what traffic will be protected using ACLs (Access Control Lists).
      - Defines where the data has to be sent.
    - SA Lifetime
      - How long should the keys live for?
      - Value can be in time or bits.
      - Shorter the lifetime, more the security, as there will be frequent re-keying.
      - This value does not need to match at both ends.
    - Perfect Forward Secrecy (PFS)
      - Optional param.
      - Causes new Diffie-Hellman Key Exchange prior to when the IPSec SA is to be re-keyed.
      - With DH happening again, the new keys are not based off the previous shared secret, so they are not related and cannot be guessed.
      - More secure, but increases CPU overhead.
  - Each side creates a Transform Set, which decides how each one is going to encrypt the actual data (payload).
  - One SA is created by each side, so IPSec SAs are uni-directional.
  - So, two SAs are created in this phase. (Inbound and outbound.)
  - Each SA will have a SPI (Security Parameter Index - a random 32 bit number) attached to it, so later on while communicating, they can be compared with all the SPIs that the machine has received and on matching with one, the machine can use that SA to know the steps to decrypt the payload.
  - Uses ESP or AH protocols for transport if NAT is not required.
  - With NAT, ESP over UDP and port 4500 is used.
  - AH is not NAT friendly as it authenticates the outer IP Header as well. (The hash will not match after NAT, so the integrity check will not pass.)

### IKEv2

- Still uses UDP over port 500 or 4500.
- Runs in one phase as compared to IKEv1 which runs in two phases.
- Has the same goal as IKEv1.
- Not backward compatible with IKEv1.
- Everything that was additionally added to IKEv1 is a part of the [IKEv2 standard](https://tools.ietf.org/html/rfc5996). Some of the IKEv1 additions that are now part of the IKEv2 standard:
  - ISAKMP
  - AH/ESP
  - IPSec DOI
  - DPD
  - NAT-T
  - mode-config
  - XAUTH

#### Negotiation

 > NOTE: There is only one phase in IKEv2.

- IKE_SA_INIT messages
  - IKEv2 Security Association (SA) is established.
  - Proposal selection
  - Key exchange
- IKE_AUTH messages
  - Minimum four message exchanges and can go up to 12-16 depending upon the type of auth being used.
  - Mutual auth and identity exchange.
  - Initial IPSec SAs are established.
  - IKEv2 supports asymmetric peer authentication
    - Different pre-shared keys (PSKs) on both machines
    - One side using PSK auth and the other PKI auth (involves a digital certificate).
  - Optional
    - Certificate exchange
    - Configuration exchange
- Optional messages
  - CREATE_CHILD_SA
  - INFORMATIONAL


## Security protocols

> NOTE:
> - The contents of the 'Payload' depends on the [IPSec operation mode](#operation-modes).
> - AH and ESP can be used together as well, but it is quite uncommon to do so.

### AH

- IPSec AH (Authentication Header) Protocol.
- IP protocol ID 51.
- Provides origin authenticity.
- AH does not encrypt the payload, so this method is mostly obsolete.
- Provides an integrity check for both the payload and the outer IP header.
- If NAT occurs on the outer IP header, AH will complain due to the resulting mismatch in the integrity check.

### ESP

- IPSec ESP (Encapsulating Security Payload) Header Protocol.
- IP protocol ID 50.
- It encrypts the payload.
- Provides an integrity check for the payload, but not for the outer IP header.
- It does not complain if NAT occurs on the outer IP header, because it does not check the integrity of the outer IP header.
- It provides anti-replay attack protection.


## Operation modes

- AH and ESP protocols both support two types of encapsulations.
- The main difference in the two modes is the original IP header.

### Transport mode

- Cryptographic operations are performed by both source and destination hosts and encrypted data is sent using L2TP.
- Original IP header is retained. (There are no separate 'outer' and 'inner' IP headers as in AH.)
- If ESP is used, the client's data and the layer 4 header is encrypted using ESP.
- If AH is used, the complete packet is authenticated.
- It is usuallly used in host to host IPSec, for eg, if a server in the same LAN uses IPSec, then this mode would be used.

<p align="center">
  IPSec Transport mode :point_down:
  <br />
  <img src="https://user-images.githubusercontent.com/50140864/103147453-5eaede00-477b-11eb-919c-87926b6bcf44.png" />
  <br />
  <br />
  Encapsulation with AH in Transport mode :point_down:
  <br />
  <img src="https://user-images.githubusercontent.com/50140864/103147400-9c5f3700-477a-11eb-9654-9d4ee5726977.png" />
  <br />
  NOTE: There is only one IP header, ie, the original IP header.
  <br />
  <br />
  Encapsulation with ESP in Transport mode :point_down:
  <br />
  <img src="https://user-images.githubusercontent.com/50140864/103147395-8cdfee00-477a-11eb-9116-f3161217fd67.png" />
  <br />
  NOTE: There is only one IP header, ie, the original IP header.
</p>

### Tunnel mode

- Cryptographic operations are performed by special gateways as well as source and destination hosts.
- This adds a new IP header (the outer IP header), so the original (inner) IP header is hidden to the public.
- The inner IP header usually has internal IP addressing (the internal IPs in the remote network) and the outer IP header has the public IP addressing (required to send packets to the remote network's gateway).
- If ESP is used, then the client data and all original headers are encrypted using ESP.
- If AH is used, the complete packet is authenticated.
- This is used a lot as most traffic is sent over a public network.
- it is usually used between IPSec gateways or a remote VPN type of scenario where a host connects to an IPSec gateway.

<p align="center">
  IPSec Tunnel mode :point_down:
  <br />
  <img src="https://user-images.githubusercontent.com/50140864/103147440-23acaa80-477b-11eb-9a4e-d341a4e78f31.png" />
  <br />
  <br />
  Encapsulation with AH in Tunnel mode :point_down:
  <br />
  <img src="https://user-images.githubusercontent.com/50140864/103147385-70dc4c80-477a-11eb-9c6e-85c6fee2f82c.png" />
  <br />
  <br />
  Encapsulation with ESP in Tunnel mode :point_down:
  <br />
  <img src="https://user-images.githubusercontent.com/50140864/103147380-5c984f80-477a-11eb-89bf-b60e7cd44dd1.png" />
  <br />
  <br />
  Overview of IPSec operation modes :point_down:
  <br />
  <img src="https://user-images.githubusercontent.com/50140864/103147149-3e315480-4778-11eb-9696-4fead37110ea.png" width="50%" />
</p>


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
  - [What is IKEv2?](https://www.youtube.com/watch?v=eO__0SfhU4g)
- [IPsec VPN Overview](https://www.youtube.com/watch?v=ikSybz2e2RU) (Covers almost everything about IPSec.)
- [Ports used in IPSec](https://www.speedguide.net/port.php?port=4500)
- Sources for pictures
  - [Understanding VPN IPSec Tunnel Mode and IPSec Transport Mode](http://www.firewall.cx/networking-topics/protocols/870-ipsec-modes.html)
  - [An answer in the Cisco Community](https://community.cisco.com/t5/vpn/how-nat-t-works-with-ipsec/m-p/1528921/highlight/true#M41422)
