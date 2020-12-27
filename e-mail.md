# e-mail

## Protocols

- Send e-mail: SMTP
- Receive e-mail: POP3, IMAP

### SMTP

- SMTP: Simple Mail Transfer Protocol
- OSI Layer: Application Layer
- Port: 25 (default, insecure), 2525 (insecure) & 465 (secure with TLS)
- TCP/UDP: TCP
- Only used to send e-mails
  - from sender to sender's mail server
  - from sender's mail server to receiver's mail server
- It is a 'Push Protocol' as it is used to send data.
- Uses TCP, so it is a connection oriented protocol.

### POP3

- POP3: Post Office Protocol 3
- OSI Layer: Application Layer
- Port: 110 (insecure) & 995 (secure with TLS)
- TCP/UDP: TCP
- Only used to receive e-mails from receivers's mail server to receiver.
- It is a 'Pull Protocol' as it is used to receive data.
- Uses TCP, so it is a connection oriented protocol.
- Does not provide synchronization of e-mails and folders.
- One e-mail delivered to one of receiver's devices, the e-mail is deleted from the server. (It can be configured to prevent this though.)

### IMAP

- IMAP: Internet Message Access Protocol
- OSI Layer: Application Layer
- Port: 143 (insecure) & 993 (secure with TLS)
- TCP/UDP: TCP
- Only used to receive e-mails from receivers's mail server to receiver.
- It is a 'Pull Protocol' as it is used to receive data.
- Uses TCP, so it is a connection oriented protocol.
- Provides synchronization of e-mails and folders.
- The e-mail is kept on the server and local copies are cached on devices as well.


## Resources

- [How SMTP Works](https://www.youtube.com/watch?v=RdNErie6dKU) (Hindi)
- [What is SMTP](https://www.youtube.com/watch?v=PJo5yOtu7o8)
- [POP3 vs IMAP](https://www.youtube.com/watch?v=SBaARws0hy4)
- [Email Protocols - POP3, SMTP and IMAP Tutorial](https://www.siteground.com/tutorials/email/protocols-pop3-smtp-imap/)
- [Mail terminology](https://afreshcloud.com/sysadmin/mail-terminology-mta-mua-msa-mda-smtp-dkim-spf-dmarc) (MTA MUA MSA MDA SMTP DKIM SPF DMARC)
