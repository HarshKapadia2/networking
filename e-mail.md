# e-mail

([Back to Home](README.md))

## Protocols

### Transfer protocols

-   Send e-mail: SMTP
-   Receive e-mail: POP3, IMAP

#### SMTP

-   SMTP: Simple Mail Transfer Protocol
-   OSI Layer: Application Layer
-   Port: 25 (default, insecure), 2525 (insecure), 587 (secure with [TLS](tls.md)) & 465 (deprecated, secure with TLS)
-   TCP/UDP: TCP
-   Only used to send e-mails
    -   from sender to sender's mail server
    -   from sender's mail server to receiver's mail server
-   It is a 'Push Protocol' as it is used to send data.
-   Uses TCP, so it is a connection oriented protocol.

#### POP3

-   POP3: Post Office Protocol 3
-   OSI Layer: Application Layer
-   Port: 110 (insecure) & 995 (secure with TLS)
-   TCP/UDP: TCP
-   Only used to receive e-mails from receivers's mail server to receiver.
-   It is a 'Pull Protocol' as it is used to receive data.
-   Uses TCP, so it is a connection oriented protocol.
-   Does not provide synchronization of e-mails and folders.
-   One e-mail delivered to one of receiver's devices, the e-mail is deleted from the server. (It can be configured to prevent this though.)

#### IMAP

-   IMAP: Internet Message Access Protocol
-   OSI Layer: Application Layer
-   Port: 143 (insecure) & 993 (secure with TLS)
-   TCP/UDP: TCP
-   Only used to receive e-mails from receivers's mail server to receiver.
-   It is a 'Pull Protocol' as it is used to receive data.
-   Uses TCP, so it is a connection oriented protocol.
-   Provides synchronization of e-mails and folders.
-   The e-mail is kept on the server and local copies are cached on devices as well.

### Utility protocols

#### MIME

-   MIME: Multipurpose Internet Mail Extensions
-   Supplementary/add-on protocol to the e-mail transfer protocols.
-   e-mail transfer protocols can inherently only transfer normal text (NVT 7-bit ASCII) data, but it uses the MIME to extend its capabilities.
-   MIME allows the user to send audio, video, image and other types of files via e-mail. It also helps support different languages like German, French, etc. that don't follow the 7-bit ASCII format.
-   Converts files to the NVT 7-bit format for sending them and parses them back to their original format on the other end.
-   Although MIME was created for [SMTP](#smtp), it can be used with [POP3](#pop3), [IMAP](#imap) and [HTTP](http.md) as well.
-   MIME headers
    -   `Mime-Version: 1.1`
    -   `Content-Type: media-type/media-subtype` (Eg: `text/html`, `multipart/form-data`, `image/png`, `video/mp4`, `text/css`, `audio/mp3`, etc.)
    -   `Content-Transfer-Encoding` (Values: `7bit`, `8bit`, `base64`, etc.)
    -   `Content-Id`
    -   `Content-Description`

<p align="center">
  An e-mail MIME header :point_down:
  <br />
  <img src="https://user-images.githubusercontent.com/50140864/103176023-9eb5b400-4894-11eb-83c3-422024f8b8e1.png" />
</p>

### Security protocols

#### PGP

-   PGP: Pretty Good Privacy
-   Provides
    -   Authentication (using the Web of Trust - importing the receiver's public key into the sender's key ring)
    -   Confidentiality (using a combo of symmetric/conventional and asymmetric key cryptography)
-   Used for signing, encrypting and decrypting e-mails, files, directories, disks, etc.
-   It uses the decentralized 'Web of Trust' to verify the identity of users. (Key rings and graphs)

#### S/MIME

-   S/MIME: Secure/Multipurpose Internet Mail Extensions
-   Provides security (authentication and encryption) for e-mails.
-   Main functions
    -   Digital signature (authentication and non-repudiation)
    -   Encryption (integrity and confidentiality)

## Resources

-   Working of e-mail infrastructure
    -   [How Email Works](https://www.youtube.com/watch?v=x28ciavQ4mI&list=PLzQX06Oo2BXS4JsXtPuy6tmKyApQlAuS1&index=13)
    -   [Mail terminology (infrastructure and authentication): MTA, MUA, MSA, MDA, SMTP, DKIM, SPF and DMARC](https://afreshcloud.com/sysadmin/mail-terminology-mta-mua-msa-mda-smtp-dkim-spf-dmarc)
    -   [See a full e-mail header (Gmail)](https://support.google.com/mail/answer/29436?hl=en)
-   SMTP
    -   [How SMTP Works](https://www.youtube.com/watch?v=RdNErie6dKU) (Hindi)
    -   [What is SMTP](https://www.youtube.com/watch?v=PJo5yOtu7o8)
    -   [What SMTP Port Should I Use?](https://www.sparkpost.com/blog/what-smtp-port/)
    -   [MIME](https://www.youtube.com/watch?v=Ta8r_I7-wrw&list=PL9FuOtXibFjV77w2eyil4Xzp8eooqsPp8&index=65) (Hindi)
-   POP3 and IMAP
    -   [POP3 vs IMAP](https://www.youtube.com/watch?v=SBaARws0hy4)
    -   [Email Protocols - POP3, SMTP and IMAP Tutorial](https://www.siteground.com/tutorials/email/protocols-pop3-smtp-imap/)
-   e-mail security
    -   [Basic e-mail security](https://www.youtube.com/watch?v=6ezYWDUON6o&list=PLzQX06Oo2BXS4JsXtPuy6tmKyApQlAuS1&index=14)
    -   PGP
        -   [Intro to PGP](https://www.youtube.com/watch?v=WTwQd7ovAqY&list=PL9FuOtXibFjV77w2eyil4Xzp8eooqsPp8&index=63)
        -   [PGP and the Web of Trust](https://www.youtube.com/watch?v=H5-lipH1KwQ)
        -   [A Pretty Good Introduction to Pretty Good Privacy](https://www.youtube.com/watch?v=Lq-yKJFHJpk)
        -   [End-to-End Encryption in the Browser Impossible?](https://www.youtube.com/watch?v=DM1tPmxGY7Y)
    -   S/MIME
        -   [MIME](https://www.youtube.com/watch?v=Ta8r_I7-wrw&list=PL9FuOtXibFjV77w2eyil4Xzp8eooqsPp8&index=65) (Hindi)
        -   [S/MIME](https://www.youtube.com/watch?v=Ta8r_I7-wrw&list=PL9FuOtXibFjV77w2eyil4Xzp8eooqsPp8&index=66) (Hindi)
    -   [Mail terminology (infrastructure and authentication): MTA, MUA, MSA, MDA, SMTP, DKIM, SPF and DMARC](https://afreshcloud.com/sysadmin/mail-terminology-mta-mua-msa-mda-smtp-dkim-spf-dmarc)
