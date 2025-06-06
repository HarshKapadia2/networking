# Border Gateway Protocol

([Back to Home](README.md))

-   BGP: Border Gateway Protocol
-   Advertises the discoverability and reachability of a network between Autonomous Systems (ASs).
    -   [Autonomous Systems (ASs)](https://www.cloudflare.com/learning/network-layer/what-is-an-autonomous-system)
    -   [Internet Exchange Points (IXPs)](https://www.linkedin.com/pulse/focus-subsea-network-architecture-ixps-maxie-reynolds)
    -   [How ASs peer with each other at IXPs](https://www.cloudflare.com/learning/network-layer/what-is-an-autonomous-system/#:~:text=How%20do%20autonomous%20systems%20connect%20with%20each%20other%3F)
-   Outages caused by BGP misconfigurations/issues
    -   The 2021 Facebook outage
        -   [Understanding how Facebook disappeared from the Internet](https://blog.cloudflare.com/october-2021-facebook-outage)
        -   [Detailed analysis on the facebook outage](https://www.youtube.com/watch?v=JODWEal5vko)
    -   [Why Google Went Offline Today and a Bit about How the Internet Works](https://blog.cloudflare.com/why-google-went-offline-today-and-a-bit-about)
    -   Virgin Media outage (4th April 2023)
        -   [The Virgin Media ISP outage - What happened? - YouTube](https://www.youtube.com/watch?v=6GWMJ42aY0w)
        -   [Cloudflare’s view of the Virgin Media outage in the UK](https://blog.cloudflare.com/virgin-media-outage-april-4-2023/)
-   Resource Public Key Infrastructure (RPKI)
    -   RPKI provides origin IP and IP prefix verification (protection against Sub-Prefix Hijacking Attack), while BGPSec provides AS path verification (protection against Shortest AS Path/One-Hop Attack). For full protection, both RPKI and BGPSec have to be implemented by all ASes along the path from the source to the destination.
    -   [RPKI - The required cryptographic upgrade to BGP routing](https://blog.cloudflare.com/rpki)
    -   [RPKI and BGP: our [Cloudflare's] path to securing Internet Routing](https://blog.cloudflare.com/rpki-details)
    -   [BGP leaks and cryptocurrencies](https://blog.cloudflare.com/bgp-leaks-and-crypto-currencies)
    -   [Murphy's Law Strikes Again: AS7007](https://lists.ucc.gu.uwa.edu.au/pipermail/lore/2006-August/000040.html)
        -   [Murphy's Law](https://en.wikipedia.org/wiki/Murphy's_law)
    -   [One year of BGP (in)security](https://blog.apnic.net/2020/07/03/one-year-of-bgp-insecurity)
        -   [MITM and Routing Security](https://labs.apnic.net/index.php/2013/12/11/mitm-and-routing-security)
-   [Is BGP safe yet?](https://isbgpsafeyet.com)
