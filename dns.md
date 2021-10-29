# DNS

## Table of Contents

-   [What is DNS and Why is DNS Needed?](#what-is-dns-and-why-is-dns-needed)
-   [Common DNS Records](#common-dns-records)
    -   [A Record](#a-record)
    -   [AAAA Record](#aaaa-record)
    -   [CNAME Record](#cname-record)
    -   [ALIAS/ANAME Record](#aliasaname-record)
    -   [NS Record](#ns-record)
    -   [MX Record](#mx-record)
    -   [TXT Record](#txt-record)
    -   [PTR Record](#ptr-record)
    -   [CAA Record](#caa-record)
    -   [SRV Record](#srv-record)
    -   [CERT Record](#cert-record)
    -   [SOA Record](#soa-record)
-   [Resources](#resources)

## What is DNS and Why is DNS Needed?

-   DNS stands for 'Domain Name System' or 'Domain Name Server.'
-   All web sites, web apps and other resources on the internet are uniquely identified through IP addresses. For example, `8.8.8.8` is `google.com`'s IP address.
-   Computers work well with numbers, but humans cannot remember the IP addresses of all the resources that they want to visit on the internet and words are easier to remember than a string of numbers (in case of IPv4) or an alphanumeric string (in case of IPv6), so every resource has a unique URL (Eg: `github.com`) that makes it easy to remember the name to get to the intended resource.
-   Now resources can only be contacted by knowing their IP addresses, so there has to be some mapping for domain names to their IP addresses.
-   Here is where the Domain Name System Protocol steps in, wherein the device from which a request is made for a resource first hits a Domain Name Server to get the IP address of the requested resource and uses that IP address to then contact the requested resource to fetch it.
-   The DNS protocol is an [Application Layer](osi_layers.md) protocol that uses port 53 and [mainly uses UDP](https://stackoverflow.com/a/40063445/11958552) as its Transport Layer protocol.

## Common DNS Records

-   DNS records are used to provide important information about a domain.
-   They are also called 'Resource Records' (RRs) and are stored in DNS Zone Files, which are stored on the domain's Name Server.
-   Almost every record follows the format `Name TTL Class Type Data`.
    Eg: `www 86400 IN A 192.168.1.1`
    -   Name/Host
        -   The host name of the record.
        -   Also called 'hostname.'
        -   Eg values: `@` (blank), a subdomain (`www`, `blog`, `links`, etc.), `*` (wildcard), etc.
        -   Eg usage
            -   If the host value is `www` for the domain `harshkapadia.me`, then the record is pertaining to `www.harshkapadia.me`.
            -   Similarly, if the host value is `@` (blank) for the domain `harshkapadia.me`, then the record is pertaining to `harshkapadia.me`, ie, the base domain itself, so the output will have `@` replaced by `harshkapadia.me.`.
    -   TTL
        -   Time To Live in seconds, unless otherwise mentioned.
        -   Lists the time for which DNS servers should cache the record. An update to the record will thus take time to reflect, as the previous value might be cached.
    -   Class
        -   It defines the protocol family.
        -   `IN` stands for 'Internet' and is used the most.
        -   [More on classes](https://www.agiledns.net/KB/DNS-Resource-Record-Classes)
    -   Type
        -   Type of DNS record.
        -   There are [more than 260 RR types](https://www.iana.org/assignments/dns-parameters/dns-parameters.xhtml#dns-parameters-4) defined by IANA! The most common ones are discussed below.
        -   Eg: [A record](#a-record), [CNAME record](#cname-record), etc.
    -   Data/Value
        -   An IP address to which the record points or any other data that should be contained in the record.

**NOTE**: For the following record sections, the base/apex/root domain is `harshkapadia.me`.

### A Record

-   This is the 'Address Record.'
-   It is used to map a domain name to an IPv4 address.
-   Eg
    -   `www 1800 IN A 185.199.108.153` will point `www.harshkapadia.me` to GitHub Pages' IP address.
    -   Similarly, a value of `@` for the host will have the output as `harshkapadia.me. 1800 IN A 185.199.108.153` and will point the base domain (`harshkapadia.me`) to GitHub Pages' IP address.
        -   NOTE: `@` is a blank host value that implies the record is pertaining to `harshkapadia.me`, the base domain.

### AAAA Record

-   This is an address record as well and behaves like an [A Record](#a-record), but pertains to IPv6 addresses.
-   Eg: `www 86400 IN AAAA 2a01:8840:6::1` points `www.harshkapadia.me` to the IPv6 address.

### CNAME Record

-   'CNAME' stands for 'Canonical Name.'
-   It is used to redirect one domain name to another domain name.
-   One limitation to is that they can only be placed on subdomains (Eg: `blog.harshkapadia.me`), but not the root domain (Eg: `harshkapadia.me`).
-   Eg: `www 1800 IN CNAME harshkapadia.me.` will redirect `www.harshkapadia.me` to `harshkapadia.me`, but `harshkapadia.me. 1800 IN CNAME www.harshkapadia.me.` will **not** redirect `harshkapadia.me` to `www.harshkapadia.me`, as a CNAME Record cannot be placed on a base domain.

### ALIAS/ANAME Record

-   An ALIAS or ANAME Record behaves like a [CNAME Record](#cname-record), but allows redirecting apex (root/base) domains (Eg: `harshkapadia.me`) as well.
-   Eg: `harshkapadia.me. 1800 IN ALIAS www.harshkapadia.me.` will redirect `harshkapadia.me` to `www.harshkapadia.me`.

### NS Record

-   'NS' stands for 'Name Server.'
-   It points the domain or subdomain to a Name Server, which allows the discovering of the IP address of the domain.
-   Eg: `harshkapadia.me. 86400 IN NS ns1.provider.com.`

### MX Record

-   'MX' stands for 'Mail eXchange.'
-   This record points to a Mail Server which should be used for a domain using SMTP (Simple Mail Transfer Protocol).
-   It always points to a domain and not an IP address.
-   If a domain doesn’t have an MX Record, a sending server will attempt to deliver mail to the domain’s A Record instead.
-   An extra number that sets the priority of this record if multiple mail servers are defined is added to the record. Lower numbers have higher priority.
-   Eg: `harshkapadia.me. 86400 IN MX 10 site2.smtp.mx.exch580.serverdata.net.` points the domain `harshkapadia.me` to the Mail Server. This implies that an e-mail to `contact@harshkapadia.me` will hit the Mail Server.

### TXT Record

-   Allows the addition of textual data up to 255 characters to a domain or subdomain.
-   A common usage is for the verification of ownership of domain, e-mail spam prevention or to check running services.
-   Eg: `harshkapadia.me. 86400 IN TXT random_string`

### PTR Record

-   'PTR' stands for 'Pointer.'
-   It is also called a 'Reverse DNS Record.'
-   Its functionality is exactly opposite to that of an [A Record](#a-record), wherein it resolves an IP address to a domain name.
-   The IP address has to be defined by the owner of the server hosting the resource.
-   It is used to check whether a server name is associated with the IP address from where a connection was initiated. One application is in e-mail spam verification.
-   Eg: `34.216.184.93.in-addr.arpa. 2100 IN PTR harshkapadia.me.`

### CAA Record

-   'CAA' stands for 'Certificate Authority Authorization.'
-   It is used to specify which Certificate Authorities (CAs) are allowed to issue certificates for a domain.
-   If no CAA Record is present, any CA is allowed to issue a certificate for the domain but if a CAA Record is present, only the CAs listed in the record(s) are allowed to issue certificates for that host.
-   It is also inherited by subdomains, unless overridden.
-   It also provides a means of indicating notification rules in case someone requests a certificate from an unauthorized CA.

### SRV Record

-   'SRV' stands for 'Service.'
-   It is a service location record like the [MX Record](#mx-record), but for other communication protocols like SIP and XMPP.
-   Format: `_Service._Protocol.Name. TTL Class Type Priority Weight Port Target.`
-   'Priority' works just like in the [MX Record](#mx-record) and the 'Weight' is similar to the 'Priority' field and is taken into consideration if the priority of the records is the same.
-   Eg: `_xmpp._tcp.harshkapadia.me. 86400 IN SRV 10 5 5223 server.harshkapadia.me.`

### CERT Record

-   'CERT' stands for 'Certificate.'
-   It is used to store encryption certificates (like PKIX, SPKI, PGP, etc.) and Certificate Revocation Lists (CRLs contain lists of certificates that are no longer valid.) in DNS.
-   It helps in verifying the authenticity of sending and receiving parties in a communication.

### SOA Record

-   'SOA' stands for 'Start Of Authority.'
-   It appears at the beginning of a DNS Zone File and indicates the Authoritative Name Server for the current DNS zone, contact details for the Domain Administrator, Domain Serial Number and information on how frequently DNS information for the zone should be refreshed.

## Resources

-   [What is DNS? How DNS Works.](https://www.cloudflare.com/learning/dns/what-is-dns)
-   [DNS Records Explained.](https://ns1.com/resources/dns-records-explained)
-   [DNS Records: A Beginner’s Guide.](https://www.godaddy.com/garage/dns-records-a-beginners-guide)
-   [DNS: Types of DNS Records, DNS Servers and DNS Query Types](https://ns1.com/resources/dns-types-records-servers-and-queries)
-   [ALIAS Records](https://support.dnsimple.com/articles/alias-record)
-   [How ALIAS Records Work.](https://support.dnsimple.com/articles/alias-record/#how-alias-records-work)
-   [What is an MX Record? What is the Correct Syntax for MX Records? What is Priority?](https://kb.intermedia.net/Article/903)
-   [What is a DNS TXT Record?](https://www.cloudflare.com/learning/dns/dns-records/dns-txt-record)
-   [CAA Records](https://support.dnsimple.com/articles/caa-record)
-   [What is a DNS SRV Record?](https://www.cloudflare.com/learning/dns/dns-records/dns-srv-record)
-   Why is there a period (`.`) after the domain name?
    -   [Why Does Putting a Dot After the URL Remove Login Information?](https://superuser.com/questions/1467958/why-does-putting-a-dot-after-the-url-remove-login-information)
    -   [Should I Append a Dot (.) at the End of my DNS URLs?](https://serverfault.com/questions/803033/should-i-append-a-dot-at-the-end-of-my-dns-urls)
