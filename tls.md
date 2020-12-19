# TLS

- The Transport Layer Security (TLS) Protocol helps in encrypting and authenticating the communication between two services.
- TLS came after the release of SSL 3.0, which did some similar things (TLS 1.0 was also called SSL 3.1) and the current version of TLS is 1.3.
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

- Ciphers to be used
- Key exchange (Secret Key)
- Authentication (public/asymmetric key cryptography and digital signature with certificates)
- Robustness (prevent Man in the Middle attacks, Replay attacks, Downgrade attacks, etc)

### RSA

### AES

### Diffie-Hellman

- Type of Public/Asymmetric/Secret Key Cryptography.
- (Secret) Key exchange protocol for a shared secret between two devices who want to start communication.
- The established shared secret is then used to derive symmetric keys with Private/Symmetric/Secret Key Encryption algorithms like AES (because Private Key Cryptography is faster than Public Key Cryptography).
- Some types
  - ECDHE (Elliptic Curve Diffie-Hellman Ephemeral) (Ephemeral implies generating a key every time a conversation takes place)
  - X255i9 (A type of Elliptic Curve Diffie-Hellman that uses Curve25519)
  - P-256
- Vulnerable to 'Man in the Middle' attack and here is were Public Key Cryptography ciphers like RSA, DSA, etc help out by providing authentication.
  - Just RSA can be used in place of Diffie-Hellman, but is not, as it is slow and its keys are established for over years, which if broken, pose a big risk. So, Diffie-Hellman is used as a quicker method (if used a few times) and safety blanket for key exchange, with RSA providing authenticity.

### SHA256


## Resources

- [TLS Intro](https://www.youtube.com/watch?v=0TLDTodL7Lc)
- [TLS Handshake](https://www.youtube.com/watch?v=86cQJ0MMses)
- Diffie-Hellman
  - [End to End Excryption (E2EE)](https://www.youtube.com/watch?v=jkV1KEJGKRA)
  - [Secret Key Exchange (Diffie-Hellman)](https://www.youtube.com/watch?v=NmM9HA2MQGI)
  - [Diffie-Hellman - the Mathematics bit](https://www.youtube.com/watch?v=Yjrfm_oRO0w)
  - [Key Exchange Problems](https://www.youtube.com/watch?v=vsXMMT2CqqE)
