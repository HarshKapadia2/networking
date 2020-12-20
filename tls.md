# TLS

- The Transport Layer Security (TLS) Protocol helps in encrypting and authenticating the communication between two services.
- TLS came after the release of SSL 3.0, which did some similar things (TLS 1.0 was also called SSL 3.1) and the current version of TLS is 1.3.
  - SSL is the older version of TLS.
- Usually TCP -> HTTP, but with HTTPS, TCP -> TLS -> HTTP. So the encryption is put in between TCP and HTTP.
- TLS is not used just in web sites only. It is used for other communication as well.
- HTTPS is also called 'HTTP over TLS (or SSL)'.


## Examples

> NOTE:
> - This information can be found in the Security tab in the browser DevTools or on clicking the 'lock' (or 'unlock') symbol to the left of the URL in the browser search bar.
> - The string of cipher information seen in the pictures below is called a 'cipher suite'. There are several of them for each protocol and they tell us which ciphers are being used by a particular protocol after both machines have agreed on the ciphers to be used.

*https://github.com* :point_down:

![](https://user-images.githubusercontent.com/50140864/102624600-3c5d0500-416a-11eb-9893-0b7ea946c2ba.png)

*https://otc.zulipchat.com* :point_down:

![](https://user-images.githubusercontent.com/50140864/102624926-bc836a80-416a-11eb-9a12-237e2af7a694.png)

[*Source*](https://youtu.be/86cQJ0MMses?t=65) :point_down:

![](https://user-images.githubusercontent.com/50140864/102624503-1cc5dc80-416a-11eb-8240-0a5219c2bc2b.png)


## Cryptography in TLS

### Diffie-Hellman (DH)

- Type of Public/Asymmetric Key Cryptography.
- (Secret) Key exchange protocol for a shared secret between two devices who want to start communication.
- The established shared secret is then used to derive symmetric keys with Private/Symmetric/Secret Key Encryption algorithms like AES (because Private Key Cryptography is faster than Public Key Cryptography).
- Some types
  - ECDHE (Elliptic Curve Diffie-Hellman Ephemeral) (Ephemeral implies generating a key every time a conversation takes place, ie, very frequently.)
  - X255i9 (A type of Elliptic Curve Diffie-Hellman that uses Curve25519.)
  - P-256 (A type of curve used in Elliptic Curve Cryptography.)
- Vulnerable to 'Man in the Middle' attacks and here is were Public Key Cryptography ciphers like RSA, DSA, etc help out by providing authentication.
  - Perfect forward secrecy: Just RSA can be used in place of Diffie-Hellman, but is not, as it is slow and its keys are established for over years, which if broken, pose a big risk. So, Diffie-Hellman is used as a quicker method (if used a few times) and safety blanket for key exchange, with RSA providing authenticity.

### RSA

- RSA is the name of the scientists involved.
- Type of Public/Asymmetric Key Cryptography.
- Ensures authenticity of sender.
- Prevents 'Man in the Middle' attacks (as it authenticates the sender).

### AES

- Advanced Encryption Standard (AES) is a type of a Private/Symmetric/Secret Key Cryptography.
- The shared secret from Diffie-Hellman is used to derive a key.
- Provides encryption for the data being shared between the two communicating machines.

### SHA256

- Hashing algo which is a part of the Secure Hashing Algorithm family. (SHA2 to be specific.)
- Used wherever needed, for eg, to derive a key from the shared secret, in digital signatures, etc.


## Conditions to be fulfilled by a TLS handshake

- What ciphers to be used for normal communication. (Eg: AES)
- Key exchange algorithm to generate a symmetric key. (Eg: Diffie-Hellman)
- Authentication (public/asymmetric key cryptography like RSA and verifying with digital signature with certificates)
- Robustness (prevent Man in the Middle attacks, Replay attacks, Downgrade attacks, etc during the handshake)


## TLS 1.2 Handshake

> NOTE:
> - `C` = Client and `S` = Server.
> - TLS 1.2 takes two roundtrips (`C -> S`, `S -> C`, `C -> S` and `S -> C`) to complete the handshake. (TLS 1.3 takes just one roundtip.)

- TLS works on top of TCP, so a [TCP handshake](https://www.youtube.com/watch?v=bW_BILl7n0Y) is done first.
- `C -> S` Client hello
  - States max version of TLS supported.
  - Send a random number to prevent Replay attacks.
  - Sends a list of cipher suites that the client supports.
- `S -> C` Server hello
  - Choose TLS version and cipher suite.
  - Send random number again.
  - Send a certificate (with the public key of the server attached to it.)
  - Server key exchange message (DH)
    - It sends params for the Diffie-Hellman (DH) key exchange. (The generator and the huge prime number.)
    - It sends it's generated public part of the key exchange process.
    - Digital signature (a hashed value of some of the previous messages signed by the private key of the server). RSA is used here.
    - Send 'Server hello done'.
- `C -> S` Client key exchange message (DH)
  - It sends it's generated public part of the key exchange process.
  - Side note: Both the server and client can now form the pre-master secret by completing the Diffie-Hellman process and then combine them with the random numbers sent in the above messages to make the master secret.
  - Change cipher spec message. (Says that it is ready to begin encryption.)
  - Finished message (Contains an encrypted summary of all the messages so far.)
- `S -> C` Change cipher spec message
  - Finished message (Contains an encrypted summary of all the messages so far.)
  - Side note: Only if the two finished messages match, will the handshake succeed. This prevents any Man in the Middle attacks.
- The handshake is complete and the encrypted data is now communicated using the pre-decided cipher as mentioned in the decided cipher suite (eg: AES).


## Resources

- [TLS Intro](https://www.youtube.com/watch?v=0TLDTodL7Lc)
- [TLS Handshake](https://www.youtube.com/watch?v=86cQJ0MMses)
- Diffie-Hellman
  - [End to End Excryption (E2EE)](https://www.youtube.com/watch?v=jkV1KEJGKRA)
  - [Secret Key Exchange (Diffie-Hellman)](https://www.youtube.com/watch?v=NmM9HA2MQGI)
  - [Diffie-Hellman - the Mathematics bit](https://www.youtube.com/watch?v=Yjrfm_oRO0w)
  - [Key Exchange Problems](https://www.youtube.com/watch?v=vsXMMT2CqqE) (includes explanation on RSA)
  - [Elliptic Curves](https://www.youtube.com/watch?v=NF1pwjL9-DE)
  - [Elliptic Curve Back Door](https://www.youtube.com/watch?v=nybVFJVXbww)
- AES
  - [SP Networks](https://www.youtube.com/watch?v=DLjzI5dX8jc)
  - [Rinjdael algorithm](https://www.youtube.com/watch?v=VYech-c5Dic) (the base of AES)
  - [AES Explained](https://www.youtube.com/watch?v=O4xNJsjtN6E)
  - [128 Bit or 256 Bit Encryption?](https://www.youtube.com/watch?v=pgzWxOtk1zg)
- Hashing
  - [Hashing Algorithms and Security](https://www.youtube.com/watch?v=b4b8ktEV4Bg)
  - [SHA](https://www.youtube.com/watch?v=DMtFhACPnTY)
  - [SHA1 Problems](https://www.youtube.com/watch?v=f8ZP_1K2Y-U)
- Digital signatures and certificates
  - [What are Digital Signatures?](https://www.youtube.com/watch?v=s22eJ1eVLTU)
  - [SSL/TLS Certificates](https://www.youtube.com/watch?v=r1nJT63BFQ0)
  - [TLS playlist by Hussein Nasser](https://www.youtube.com/playlist?list=PLQnljOFTspQW4yHuqp_Opv853-G_wAiH-)
