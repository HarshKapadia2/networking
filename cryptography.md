# Cryptography

([Back to Home](README.md))

## Table of Contents

-   [Introduction](#introduction)
-   [Types of Cryptography](#types-of-cryptography)
-   [Ciphers](#ciphers)
    -   [Feistel](#feistel)
    -   [AES](#aes)
    -   [DES, 2DES, 3DES](#des-2des-3des)
    -   [Blowfish](#blowfish)
    -   [RC5](#rc5)
-   [Key Exchange](#key-exchange)
    -   [Diffie-Hellman](#diffie-hellman)
-   [Hashing](#hashing)
    -   [SHA](#sha)
-   [Digital Signatures](#digital-signatures)
-   [Digital Certificates and Certificate Revocation (OCSP and CRL)](#digital-certificates-and-certificate-revocation-ocsp-and-crl)
-   [PGP](#pgp)
-   [Perfect Forward Secrecy](#perfect-forward-secrecy)
-   [Resources](#resources)

## Introduction

-   Cryptology is the scientific study of Cryptography and Cryptanalysis.
-   Cryptography is the practice and study of techniques for secure communication in the presence of third parties called adversaries.
-   Cryptanalysis is used to breach cryptographic security systems and gain access to the contents of encrypted messages, even if the cryptographic key is unknown.
-   [7 Cryptography Concepts EVERY Developer Should Know](https://www.youtube.com/watch?v=NuyzuNBFWxQ)
-   [Security Pitfalls in Cryptography](https://www.schneier.com/essays/archives/1998/01/security_pitfalls_in.html)
-   [Why Cryptography Is Harder Than It Looks](https://www.schneier.com/essays/archives/1997/01/why_cryptography_is.html)

## Types of Cryptography

<p align="center">
  <img src="https://user-images.githubusercontent.com/50140864/103271702-f19c8200-49e0-11eb-9605-4d75c41f1c7c.png" />
</p>

## Ciphers

### Feistel

-   [Feistel Cipher](https://www.youtube.com/watch?v=FGhj3CGxl8I)
-   [Modes of Operation](https://www.youtube.com/watch?v=Rk0NIQfEXBA)
-   [EXTRA BITS: Feistel Modes of Operation Code](https://www.youtube.com/watch?v=0abs6qfuLpg)
-   [Securing Stream Ciphers (HMAC)](https://www.youtube.com/watch?v=wlSG3pEiQdc)

### AES

-   AES: Advanced Encryption Standard
-   Block size: 128 bits
-   Key size: 128, 192 or 256 bits
-   No. of rounds: 10, 12 and 14 rounds for 128, 192 and 256 bits key size respectively)
-   [SP Networks](https://www.youtube.com/watch?v=DLjzI5dX8jc)
-   [Rinjdael algorithm](https://www.youtube.com/watch?v=VYech-c5Dic) (the base of AES)
-   [AES Explained](https://www.youtube.com/watch?v=O4xNJsjtN6E)
-   [128 Bit or 256 Bit Encryption?](https://www.youtube.com/watch?v=pgzWxOtk1zg)
-   [In depth working of AES](https://www.youtube.com/watch?v=YVT4fcW7sI8&list=PL9FuOtXibFjV77w2eyil4Xzp8eooqsPp8&index=26) (Hindi)

### DES, 2DES, 3DES

-   DES: Data Encryption Standard
-   Block size: 64 bits
-   Key size: 56 bits (64 bits in reality)
    -   The 64 bit key is made of eight chunks of eight bits each. The eighth bit in each chunk is a parity bit (and is thus discarded). **So, the actual key length is 64 - 8 = 56.**
-   No. of rounds: 16
-   Prerequisite
    -   [Feistel Cipher](#feistel)
-   Hindi
    -   [DES](https://www.youtube.com/watch?v=eMHcQByhR-g&list=PL9FuOtXibFjV77w2eyil4Xzp8eooqsPp8&index=20)
    -   [DES Key Generation](https://www.youtube.com/watch?v=vj7HJ56mdiw&list=PL9FuOtXibFjV77w2eyil4Xzp8eooqsPp8&index=21)
    -   [DES Avalanche and Completeness Effect](https://www.youtube.com/watch?v=lg1GyrUtOrM&list=PL9FuOtXibFjV77w2eyil4Xzp8eooqsPp8&index=22)
    -   [2DES and Meet in the Middle attack](https://www.youtube.com/watch?v=rGSsEdx0dcU&list=PL9FuOtXibFjV77w2eyil4Xzp8eooqsPp8&index=24)
    -   [3DES](https://www.youtube.com/watch?v=_zldFlu7tCM&list=PL9FuOtXibFjV77w2eyil4Xzp8eooqsPp8&index=25)
    -   [DES Weaknesses](https://www.youtube.com/watch?v=4Uo7kivJ0EQ&list=PL9FuOtXibFjV77w2eyil4Xzp8eooqsPp8&index=23)
-   English
    -   http://wesecure.net/learn/index.html

### Blowfish

-   Block size: 64 bits (Twofish has a block size of 128 bits.)
-   Key size: 32 to 448 bits (The default is 128 bits.)
-   No. of rounds: 16
-   [Blowfish Explained](https://www.youtube.com/watch?v=gz8AV0bPaOU)

### RC5

-   RC: Rivest/Ron's Cipher
-   Block size: 32, 64 or 128 bits
-   Key size: 0 to 2040 bits
-   No. of rounds: 0 to 255

## Key Exchange

### Diffie-Hellman

-   Key exchange algorithm
-   [End to End Encryption (E2EE)](https://www.youtube.com/watch?v=jkV1KEJGKRA)
    -   Side note: [End-to-End Encryption in the Browser Impossible?](https://www.youtube.com/watch?v=DM1tPmxGY7Y)
-   [Secret Key Exchange (Diffie-Hellman)](https://www.youtube.com/watch?v=NmM9HA2MQGI)
-   [Diffie-Hellman - the Mathematics bit](https://www.youtube.com/watch?v=Yjrfm_oRO0w)
-   [Key Exchange Problems](https://www.youtube.com/watch?v=vsXMMT2CqqE) (includes explanation on RSA)
-   [Elliptic Curves](https://www.youtube.com/watch?v=NF1pwjL9-DE)
-   [Elliptic Curve Back Door](https://www.youtube.com/watch?v=nybVFJVXbww)
-   'Ephemeral' means 'something that is short lasting'.
-   ECDH = Elliptic Curve Diffie-Hellman
-   [ECDH in SSH](https://youtu.be/0Sffl7YO0aY?t=361)
-   [Perfect Forward Secrecy (FS or PFS)](#perfect-forward-secrecy)

## Hashing

-   [Hashing Algorithms and Security](https://www.youtube.com/watch?v=b4b8ktEV4Bg)

### SHA

-   Secure Hashing Algorithm
-   [SHA](https://www.youtube.com/watch?v=DMtFhACPnTY)
-   [SHA1 Problems](https://www.youtube.com/watch?v=f8ZP_1K2Y-U)

## Digital Signatures

-   Help in establishing message integrity, i.e., proving that a particular person/origin sent the data.
-   Message Authentication Codes (MACs) are symmetric key protocols, while Digital Signatures are asymmetric/public key protocols.
-   [What are Digital Signatures?](https://www.youtube.com/watch?v=s22eJ1eVLTU)
-   [Digital Signatures: What They Are & How They Work](https://sectigo.com/resource-library/how-digital-signatures-work)
-   [Digital Signatures](https://cryptobook.nakov.com/digital-signatures)

## Digital Certificates and Certificate Revocation (OCSP and CRL)

-   [SSL/TLS Certificates](https://www.youtube.com/watch?v=r1nJT63BFQ0)
-   [Compressing Certificates in TLS](https://www.youtube.com/watch?v=Ael488F_peM)
-   [Certificate Revocation Techniques (CRL, OCSP, OCSP Stapling)](https://www.youtube.com/watch?v=g08Omc1wi0s)
-   [Shared vs Private SSL/TLS Certificates](https://www.ssldragon.com/blog/difference-between-shared-and-private-ssl-certificates)
-   [The SSL Certificate Issuer Field is a Lie](https://www.agwa.name/blog/post/the_certificate_issuer_field_is_a_lie) ([Credits](https://twitter.com/hnasr/status/1615758928398389248))
-   [No More Extended Validation Certificate Overhead from Chrome 106](https://blog.webpagetest.org/posts/eliminating-ev-certificate-performance-overhead)
-   [Revocation checking and Google Chrome CRLSet](https://www.imperialviolet.org/2012/02/05/crlsets.html)
-   [Revocation Doesn't Work](https://www.imperialviolet.org/2011/03/18/revocation.html)
-   [The Impact of SSL Certificate Revocation on Web Performance](https://nooshu.com/blog/2020/01/26/the-impact-of-ssl-certificate-revocation-on-web-performance)
-   [A no-bull technical guide to EV HTTPS](https://expeditedsecurity.com/blog/are-ev-ssl-certificates-worth-it)
-   [PKI information and X.509 certificate extensions](http://www.pkiglobe.org)

## PGP

-   PGP: [Pretty Good Privacy](https://en.wikipedia.org/wiki/Pretty_Good_Privacy)
-   [OpenPGP](https://www.openpgp.org)
    -   Standard for PGP software
-   GPG/GnuPG: [GNU Privacy Guard](https://gnupg.org)
    -   Tool to use PGP
    -   GNU: GNU's Not Unix
-   Provides
    -   Authentication (using the Web of Trust - importing the receiver's public key into the sender's key ring)
    -   Confidentiality (using a combo of symmetric/conventional and asymmetric key cryptography)
-   Used for signing, encrypting and decrypting e-mails, files, directories, disks, etc.
-   It uses the decentralized 'Web of Trust' to verify the identity of users. (Key rings and graphs)
-   [Intro to PGP](https://www.youtube.com/watch?v=WTwQd7ovAqY&list=PL9FuOtXibFjV77w2eyil4Xzp8eooqsPp8&index=63)
-   [PGP and GPG difference](https://askubuntu.com/questions/186805/difference-between-pgp-and-gpg)
-   [PGP and the Web of Trust](https://www.youtube.com/watch?v=H5-lipH1KwQ)
-   [A Pretty Good Introduction to Pretty Good Privacy](https://www.youtube.com/watch?v=Lq-yKJFHJpk)
-   [End-to-End Encryption in the Browser Impossible?](https://www.youtube.com/watch?v=DM1tPmxGY7Y)
-   [OpenPGP, PGP, and GPG: What is the Difference?](https://www.goanywhere.com/blog/openpgp-pgp-gpg-whats-the-difference)
-   [Security basics with GPG, OpenSSH, OpenSSL and Keybase](https://www.integralist.co.uk/posts/security-basics)
-   [Creating the Perfect GPG Keypair](https://alexcabal.com/creating-the-perfect-gpg-keypair)
-   [Does OpenPGP key expiration add to security?](https://security.stackexchange.com/a/79386)
    -   Very good answer for understanding expiry date shenanigans of subkeys and the secret (private) key, and about the revocation certificate.
-   [How To Use GPG to Encrypt and Sign Messages](https://www.digitalocean.com/community/tutorials/how-to-use-gpg-to-encrypt-and-sign-messages)
-   [Digitally Signing and Encrypting Messages](https://support.mozilla.org/en-US/kb/digitally-signing-and-encrypting-messages)
-   [Guidelines for strong passwords](https://en.wikipedia.org/wiki/Password_strength#Guidelines_for_strong_passwords)
-   [Why should one not use the same asymmetric key for encryption as they do for signing?](https://security.stackexchange.com/questions/1806/why-should-one-not-use-the-same-asymmetric-key-for-encryption-as-they-do-for-sig)
-   Exercise: [Sending an Encrypted and Signed e-mail](e-mail.md#sending-an-encrypted-and-signed-e-mail)

## Perfect Forward Secrecy

-   PFS or FS: Perfect Forward Secrecy
-   [Wikipedia: Perfect Forward Secrecy](https://en.wikipedia.org/wiki/Forward_secrecy)
-   [Perfect Forward Secrecy (PFS) in TLS](https://www.youtube.com/watch?v=zSQtyW_ywZc)
    -   [Heartbleed problem](https://www.youtube.com/watch?v=1dOCHwf8zVQ)
    -   The Logjam TLS attack: [Imperfect Forward Secrecy: How Diffie-Hellman Fails in Practice](https://weakdh.org/imperfect-forward-secrecy-ccs15.pdf) ([weakdh.org](https://weakdh.org))
    -   [More about TLS](tls.md)

## Resources

-   [Computerphile](https://www.youtube.com/user/Computerphile)
-   [Christof Paar](https://www.youtube.com/channel/UC1usFRN4LCMcfIV7UjHNuQg/videos)
-   [Eddie Woo](https://www.youtube.com/watch?v=6xDGSalpPXk&list=PL5KkMZvBpo5CdoOxa3dqll2n6KsXqerYO)
-   [Abhishek Sharma](https://www.youtube.com/watch?v=9X1rSWLFhLY&list=PL9FuOtXibFjV77w2eyil4Xzp8eooqsPp8) (Hindi)
-   [Gideon Samid](https://www.youtube.com/user/GideonTheTeacher/videos) (http://wesecure.net)
-   [Crypto 101](https://www.crypto101.io)
-   [Cryptology, Cryptography, and Cryptanalysis – Get your Vocabulary Straight!](https://qvault.io/2019/12/16/cryptology-cryptography-and-cryptanalysis-get-your-vocabulary-straight)
-   [Why Johnny Can’t Encrypt](https://people.eecs.berkeley.edu/~tygar/papers/Why_Johnny_Cant_Encrypt/OReilly.pdf)
