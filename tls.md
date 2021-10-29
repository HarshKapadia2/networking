# TLS

([Back to Home](README.md))

-   The Transport Layer Security (TLS) protocol helps in encrypting and authenticating the communication between two services.
-   It is a Transport Layer protocol as per the [OSI Model](osi_layers.md).
-   It is the better version of the Secure Sockets Layer (SSL) protocol. (The last SSL version was 3.0.)
    -   TLS 1.0 was also called SSL 3.1.
-   The latest version of TLS is 1.3.
-   It is placed between TCP and [HTTP](http.md).
    -   Usually TCP -> HTTP, but with HTTPS, TCP -> TLS -> HTTP.
    -   Thus, HTTPS is also called 'HTTP over TLS (or SSL)'.
-   It is not just used in web sites. It is used for other communication as well, for eg, DB communication, browsing on TOR browser, etc.

## Examples

> NOTE:
>
> -   This information can be found in the Security tab in the browser DevTools or on clicking the 'lock' (or 'unlock') symbol to the left of the URL in the browser search bar.
> -   The string of cipher information seen in the pictures below is called a 'cipher suite'. There are several of them for each protocol and they tell us which ciphers are being used by a particular protocol after both machines have agreed on the ciphers to be used.

*https://github.com* :point_down:

<img src="https://user-images.githubusercontent.com/50140864/102624600-3c5d0500-416a-11eb-9893-0b7ea946c2ba.png" width="80%" />

*https://otc.zulipchat.com* :point_down:

<img src="https://user-images.githubusercontent.com/50140864/102624926-bc836a80-416a-11eb-9a12-237e2af7a694.png" width="80%" />

[_Source_](https://youtu.be/86cQJ0MMses?t=65) :point_down:

<img src="https://user-images.githubusercontent.com/50140864/102624503-1cc5dc80-416a-11eb-8240-0a5219c2bc2b.png" width="90%" />

> **NOTE: Resources for everything written below can be found in the '[Resources](#resources)' section at the end of this file.**

## Cryptography in TLS

Some common terms seen in the pictures above

-   Diffie-Hellman (EDCHE, X25519, P-256, etc)
-   RSA
-   AES
-   SHA256

### Diffie-Hellman (DH)

-   It is a part of Public/Asymmetric Key Cryptography.
-   It is a Key Exchange Protocol for a shared secret between two devices who want to start communication.
-   The established shared secret is then used to derive symmetric keys with Private/Symmetric/Secret Key Cryptography ciphers like AES (because Private Key Cryptography is faster than Public Key Cryptography).
-   Some types of DH
    -   ECDHE (Elliptic Curve Diffie-Hellman Ephemeral)
        -   Ephemeral means 'something that lasts for a short time' and here it implies that a new key is generated every time a conversation takes place, ie, very frequently.
    -   X25519
        -   A type of Elliptic Curve Diffie-Hellman that uses Curve25519.
    -   P-256
        -   A type of curve used in Elliptic Curve Cryptography.
-   Vulnerable to 'Man in the Middle' attacks and here is were Public Key Cryptography ciphers like RSA, DSA, etc help out by providing authentication.
    -   Perfect Forward Secrecy (PFS)
        -   Just RSA can be used in place of Diffie-Hellman, but is not, as it is slow and its keys are established for over years, which if leaked, pose a big risk.
        -   So, Diffie-Hellman (DH) is used as a quicker method and safety blanket for key exchange, with RSA only providing initial authenticity. It acts as a safety blanket, as it generates keys independently of RSA and after every session (if the ephemeral version of DH is used) and the communication will not be compromised even if the RSA private key is leaked.

### RSA

-   Type of Public/Asymmetric Key Cryptography cipher.
-   The name 'RSA' is an acronym of the scientists involved in making the cipher.
    -   The scientists in order: Ron Rivest, Adi Shamir and Leonard Adleman.
-   Ensures authenticity of sender.
-   Prevents 'Man in the Middle' attacks, as it authenticates the sender.

### AES

-   Advanced Encryption Standard (AES) is a type of a Private/Symmetric/Secret Key Cryptography cipher.
-   The shared secret from Diffie-Hellman is used to derive a key.
-   Provides encryption for the data being shared between the two communicating machines.

### SHA256

-   Hashing algorithm which is a part of the Secure Hashing Algorithm (SHA) family. (SHA2 to be specific.)
-   Generates a unique\* 256 bit hexadecimal string output called a 'hash', for any length of input.
    -   unique\*: Hash collisions are extremely rare.
-   Used wherever needed, for eg, to derive a key from the shared secret, in digital signatures, etc.

## Conditions to be fulfilled by a TLS handshake

-   What ciphers to be used for normal communication.
    -   Eg: AES
-   Key exchange cipher to generate a symmetric key.
    -   Eg: Diffie-Hellman
-   Authentication
    -   Public/Asymmetric Key Cryptography like RSA and verifying with digital signature with certificates.
-   Robustness
    -   Prevent Man in the Middle Attacks, Replay Attacks, Downgrade Attacks, etc during the handshake.

## TLS 1.2 handshake

> NOTE:
>
> -   `C` = Client and `S` = Server.
> -   TLS 1.2 takes two roundtrips (`C -> S`, `S -> C`, `C -> S` and `S -> C`) to complete the handshake. (TLS 1.3 takes just one roundtip.)

<p align="center">
  The TLS 1.2 handshake as seen in Wireshark :point_down:
  <br />
  <img src="https://user-images.githubusercontent.com/50140864/102719477-68b48500-4314-11eb-9631-e2806662900d.png" width="100%" />
</p>

-   TLS works on top of TCP, so a [TCP handshake](https://www.youtube.com/watch?v=bW_BILl7n0Y) is done first.
-   `C -> S` Client Hello
    -   States max version of TLS supported.
    -   Send a random number to prevent Replay attacks.
    -   Sends a list of cipher suites that the client supports.

<p align="center">
  Client Hello :point_down:
  <br />
  <img src="https://user-images.githubusercontent.com/50140864/102721208-71f71f00-431f-11eb-9be9-2d3304b925ee.png" width="80%" />
  <br />
  <br />
  Contents of 'Random' :point_down:
  <br />
  <img src="https://user-images.githubusercontent.com/50140864/102721273-c8645d80-431f-11eb-9a74-09c849a63c36.png" width="80%" />
</p>

-   `S -> C` Server Hello
    -   Choose TLS version and cipher suite.
    -   Send random number.
    -   Send a certificate (with the public key of the server attached to it.)
    -   Server Key Exchange message (DH)
        -   It sends params for the Diffie-Hellman (DH) key exchange. (The generator and the huge prime number.)
        -   It sends it's generated public part of the key exchange process.
        -   Digital signature (a hashed value of some of the previous messages signed by the private key of the server). RSA is used here.
        -   Send 'Server Hello Done'.

<p align="center">
  Server Hello :point_down:
  <br />
  <img src="https://user-images.githubusercontent.com/50140864/102721373-66582800-4320-11eb-93c7-42dcff85e0c1.png" width="80%" />
  <br />
  <br />
  Server Key Exchange :point_down:
  <br />
  <img src="https://user-images.githubusercontent.com/50140864/102721626-ef239380-4321-11eb-91b7-b0b8da838157.png" width="80%" />
  <br />
  <br />
  Server Key Exchange (contd) :point_down:
  <br />
  <img src="https://user-images.githubusercontent.com/50140864/102721653-24c87c80-4322-11eb-8147-3795b2b13d9f.png" width="80%" />
  <br />
  Server Hello Done :point_up:
</p>

-   `C -> S` Client Key Exchange message (DH)
    -   It sends it's generated public part of the key exchange process.
    -   Side note: Both the server and client can now form the pre-master secret by completing the Diffie-Hellman process and then combine them with the random numbers sent in the above messages to make the master secret.
    -   Change Cipher Spec message. (Says that it is ready to begin encryption.)
    -   Finished message (Contains an encrypted summary of all the messages so far.)

<p align="center">
  Client Key Exchange :point_down:
  <br />
  <img src="https://user-images.githubusercontent.com/50140864/102721728-aa4c2c80-4322-11eb-9ea3-21b975a40ad4.png" width="80%" />
  <br />
  <br />
  Change Cipher Spec :point_down:
  <br />
  <img src="https://user-images.githubusercontent.com/50140864/102721900-9b19ae80-4323-11eb-92d7-bcc0801cd64d.png" width="80%" />
  <br />
  <br />
  Finished :point_down:
  <br />
  <img src="https://user-images.githubusercontent.com/50140864/102721928-c9978980-4323-11eb-8990-d2e714f83f5b.png" width="80%" />
</p>

-   `S -> C` Change Cipher Spec message
    -   Finished message (Contains an encrypted summary of all the messages so far.)
    -   Side note: Only if the two finished messages match, will the handshake succeed. This prevents any Man in the Middle attacks.

<p align="center">
  Change Cipher Spec :point_down:
  <br />
  <img src="https://user-images.githubusercontent.com/50140864/102721900-9b19ae80-4323-11eb-92d7-bcc0801cd64d.png" width="80%" />
  <br />
  <br />
  Finished :point_down:
  <br />
  <img src="https://user-images.githubusercontent.com/50140864/102721928-c9978980-4323-11eb-8990-d2e714f83f5b.png" width="80%" />
</p>

-   The handshake is complete. The application data is encrypted using the Private/Symmetric/Secret Key Cryptography cipher mentioned in the **chosen** cipher suite (Eg: AES) and both machines can now communicate with encryption and authenticity.

 <p align="center">
  An overview of the TLS 1.2 handshake :point_down:
  <br />
  <img src="https://user-images.githubusercontent.com/50140864/102719277-30607700-4313-11eb-874f-70523df03e0f.png" width="80%" />
</p>

## TLS 1.3 handshake

> NOTE:
>
> -   `C` = Client and `S` = Server.
> -   TLS 1.3 takes one roundtrip (`C -> S` and `S -> C`) to complete the handshake. (TLS 1.2 takes two roundtips.)

-   TLS works on top of TCP, so a [TCP handshake](https://www.youtube.com/watch?v=bW_BILl7n0Y) is done first.
-   `C -> S` Client Hello
    -   Send list of supported TLS versions.
    -   Send random number.
    -   Send list of supported Cipher Suites.
    -   Send Client Key Exchange.
    -   Send TLS Extensions
        -   [SNI or ESNI](https://www.youtube.com/watch?v=t0zlO5-NWFU)
        -   [ALPN](https://www.youtube.com/watch?v=lR1uHVS7I-8)

<p align="center">
  Client Hello :point_down:
  <br />
  <img src="https://user-images.githubusercontent.com/50140864/102996572-5b341080-4549-11eb-91d1-d2e68f64592b.png" width="80%" />
</p>

-   `S -> C` Server Hello
    -   Agree on a cipher suite.
    -   Agree on TLS protocol version.
    -   Send random number.
    -   Send Server Key Exchange.
    -   Send Certificate.
    -   Send TLS Extensions.
        -   OCSP Stapling (Certificate Verify)
    -   Send Finished message.

<p align="center">
  Server Hello :point_down:
  <br />
  <img src="https://user-images.githubusercontent.com/50140864/102997188-7bb09a80-454a-11eb-9399-0f6c7e5a2dfd.png" width="80%" />
</p>

-   `C -> S` Client sends a Finished message and then encrypted and authenticated communication starts.

<p align="center">
  An overview of the TLS 1.3 handshake (as a cURL request) :point_down:
  <br />
  <img src="https://user-images.githubusercontent.com/50140864/105168866-bbb26f80-5b40-11eb-94f9-1f87c3c8fbde.png" width="80%" />
  <br />
  <img src="https://user-images.githubusercontent.com/50140864/105169280-527f2c00-5b41-11eb-9b65-c75b2e1dc765.png" width="80%" />
  <br />
  <img src="https://user-images.githubusercontent.com/50140864/105169404-81959d80-5b41-11eb-82af-3df69445ab26.png" width="80%" />
</p>

## Resources

-   TLS
    -   [TLS Intro](https://www.youtube.com/watch?v=0TLDTodL7Lc)
    -   [TLS Handshake](https://www.youtube.com/watch?v=86cQJ0MMses)
    -   [Illustrated TLS 1.2 Handshake](https://tls.ulfheim.net/)
    -   [Illustrated TLS 1.3 Handshake](https://tls13.ulfheim.net/)
    -   [Wiresharking TLS](https://www.youtube.com/watch?v=06Kq50P01sI)
    -   [cURL Verbose Mode Explained](https://www.youtube.com/watch?v=PVm0YEEuS8s)
    -   [TLS playlist by Hussein Nasser](https://www.youtube.com/playlist?list=PLQnljOFTspQW4yHuqp_Opv853-G_wAiH-)
-   [Application Layer Protocol Negotiation (ALPN)](https://www.youtube.com/watch?v=lR1uHVS7I-8)
-   [Server Name Indication (SNI and ESNI)](https://www.youtube.com/watch?v=t0zlO5-NWFU)
-   [`cryptography.md`](cryptography.md) (for Diffie-Hellman, RSA, AES, Hashing, Digital signatures and Digital certificates resources)
-   [Perfect Forward Secrecy (PFS) in TLS](https://www.youtube.com/watch?v=zSQtyW_ywZc)
    -   [Heartbleed problem](https://www.youtube.com/watch?v=1dOCHwf8zVQ)
-   [Automatic Cipher Suite Ordering in `crypto/tls`](https://go.dev/blog/tls-cipher-suites) (The Go Blog)
-   Picture sources
    -   [RFC 5246: The Transport Layer Security (TLS) Protocol Version 1.2](https://tools.ietf.org/html/rfc5246)
    -   [Dissecting TLS Using Wireshark](https://blog.catchpoint.com/2017/05/12/dissecting-tls-using-wireshark/)
    -   [SSL/TLS Handshake Explained With Wireshark Screenshot](https://www.linuxbabe.com/security/ssltls-handshake-process-explained-with-wireshark-screenshot)
