# e-mail

## Protocols

### e-mail transfer protocols

- Send e-mail: SMTP
- Receive e-mail: POP3, IMAP

#### SMTP

- SMTP: Simple Mail Transfer Protocol
- OSI Layer: Application Layer
- Port: 25 (default, insecure), 2525 (insecure), 587 (secure with [TLS](tls.md)) & 465 (deprecated, secure with TLS)
- TCP/UDP: TCP
- Only used to send e-mails
  - from sender to sender's mail server
  - from sender's mail server to receiver's mail server
- It is a 'Push Protocol' as it is used to send data.
- Uses TCP, so it is a connection oriented protocol.

#### POP3

- POP3: Post Office Protocol 3
- OSI Layer: Application Layer
- Port: 110 (insecure) & 995 (secure with TLS)
- TCP/UDP: TCP
- Only used to receive e-mails from receivers's mail server to receiver.
- It is a 'Pull Protocol' as it is used to receive data.
- Uses TCP, so it is a connection oriented protocol.
- Does not provide synchronization of e-mails and folders.
- One e-mail delivered to one of receiver's devices, the e-mail is deleted from the server. (It can be configured to prevent this though.)

#### IMAP

- IMAP: Internet Message Access Protocol
- OSI Layer: Application Layer
- Port: 143 (insecure) & 993 (secure with TLS)
- TCP/UDP: TCP
- Only used to receive e-mails from receivers's mail server to receiver.
- It is a 'Pull Protocol' as it is used to receive data.
- Uses TCP, so it is a connection oriented protocol.
- Provides synchronization of e-mails and folders.
- The e-mail is kept on the server and local copies are cached on devices as well.


### e-mail security protocols

#### PGP

- PGP: Pretty Good Privacy
- Provides
  - Authentication (using digital signature)
  - Confidentiality (using a combo of symmetric/conventional and asymmetric key cryptography)
- It uses the decentralized 'Web of Trust' to verify the identity of users.


## Resources

- Working of e-mail infrastructure
  - [How Email Works](https://www.youtube.com/watch?v=x28ciavQ4mI&list=PLzQX06Oo2BXS4JsXtPuy6tmKyApQlAuS1&index=13)
  - [Mail terminology (infrastructure and authentication): MTA, MUA, MSA, MDA, SMTP, DKIM, SPF and DMARC](https://afreshcloud.com/sysadmin/mail-terminology-mta-mua-msa-mda-smtp-dkim-spf-dmarc)
  - [See a full e-mail header (Gmail)](https://support.google.com/mail/answer/29436?hl=en)
- SMTP
  - [How SMTP Works](https://www.youtube.com/watch?v=RdNErie6dKU) (Hindi)
  - [What is SMTP](https://www.youtube.com/watch?v=PJo5yOtu7o8)
  - [What SMTP Port Should I Use?](https://www.sparkpost.com/blog/what-smtp-port/)
- POP3 and IMAP
  - [POP3 vs IMAP](https://www.youtube.com/watch?v=SBaARws0hy4)
  - [Email Protocols - POP3, SMTP and IMAP Tutorial](https://www.siteground.com/tutorials/email/protocols-pop3-smtp-imap/)
- e-mail security
  - [Basic e-mail security](https://www.youtube.com/watch?v=6ezYWDUON6o&list=PLzQX06Oo2BXS4JsXtPuy6tmKyApQlAuS1&index=14)
  - PGP
     - [Intro to PGP](https://www.youtube.com/watch?v=WTwQd7ovAqY&list=PL9FuOtXibFjV77w2eyil4Xzp8eooqsPp8&index=63)
     - [PGP and the Web of Trust](https://www.youtube.com/watch?v=H5-lipH1KwQ)
     - [A Pretty Good Introduction to Pretty Good Privacy](https://www.youtube.com/watch?v=Lq-yKJFHJpk)
  - [Mail terminology (infrastructure and authentication): MTA, MUA, MSA, MDA, SMTP, DKIM, SPF and DMARC](https://afreshcloud.com/sysadmin/mail-terminology-mta-mua-msa-mda-smtp-dkim-spf-dmarc)
