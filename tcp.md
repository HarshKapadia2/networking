# Transmission Control Protocol (TCP)

([Back to Home](README.md))

## Table of Contents

-   [Introduction](#introduction)
-   [Reliable Communication Mechanisms](#reliable-communication-mechanisms)
-   [Important Terms](#important-terms)
-   [Congestion Control Algorithms of TCP](#congestion-control-algorithms-of-tcp)
    -   [Slow Start](#slow-start-ss)
    -   [Congestion Avoidance](#congestion-avoidance)
    -   [Fast Retransmit](#fast-retransmit)
    -   [Fast Recovery](#fast-recovery)
-   [Versions of TCP](#versions-of-tcp)
    -   [TCP Tahoe](#tcp-tahoe)
    -   [TCP Reno](#tcp-reno)
    -   [TCP CUBIC](#tcp-cubic)
    -   [TCP Vegas](#tcp-vegas)
    -   [TCP BBR](#tcp-bbr)
-   [Resources](#resources)

## Introduction

-   [Building Blocks of TCP](https://hpbn.co/building-blocks-of-tcp)
-   [SYN packet handling in the wild](https://blog.cloudflare.com/syn-packet-handling-in-the-wild)
-   [Threads and Connections](https://www.youtube.com/watch?v=CZw57SIwgiE)
-   [Socket Programming: Echo Server, and RTT and Throughput Measurement](./files/tcp/socket-echo-rtt-tput-instructions.pdf)
    -   Exercise and good resources to get introduced to socket programming.
    -   [github.com/HarshKapadia2/socket-programming](https://github.com/HarshKapadia2/socket-programming) (Private repo)
-   [Slow Start vs Congestion Avoidance in TCP](https://www.youtube.com/watch?v=r9kbjAN2788)
-   [Implementing Reliable Transport Protocols](files/tcp/reliable-transport-protocols-instructions.pdf)
    -   Implementing Stop-and-Wait (Alternating-Bit) Protocol, Selective-Repeat Protocol (with Cumulative Acknowledgements) and Go-Back-N Protocol (with Selective Acknowledgements).
    -   [Sample Output Trace](files/tcp/reliable-transport-protocols-sample-output-trace.pdf)
    -   [github.com/HarshKapadia2/reliable-transport-protocol](https://github.com/HarshKapadia2/reliable-transport-protocol) (Private repo)
-   Comparing the performance of various versions of TCP
    -   [github.com/HarshKapadia2/tcp-version-performance-comparison](https://github.com/HarshKapadia2/tcp-version-performance-comparison)

## Reliable Communication Mechanisms

-   Confirm delivery
    -   Sender gets Acknowledgement (ACK) Packets from the receiver
-   No loss at receiver
    -   Flow Control
    -   Sliding Window
-   Detect corrupted packets
    -   Checksum
-   Detect lost packets
    -   Set up a timer on the sender.
    -   Retransmission Timeout (RTO)
-   Recover from lost packets
    -   Re-transmit packets
    -   Automatic Repeat Request (ARQ)
-   Detect duplicates
    -   Add a Sequence Number to each packet.
-   In-order delivery
    -   Add a Sequence Number to each packet.
-   Multiplexing and De-multiplexing

## Important Terms

-   CWND
    -   Congestion Window
-   RAWND
    -   Receiver Advertised Window
    -   Available buffer space on receiver sent to client.
-   SWS
    -   Sender Window Size
    -   `SWS = min(CWND, RAWND)`
-   ACK
    -   Acknowledgement Packet/Datagram
    -   Packet that acknowledges the receipt of another packet.
-   MSS
    -   Maximum Segment Size
    -   Maximum **payload (data) size** per segment/datagram (Transport Layer).
-   MTU
    -   Maximum Transmission Unit
    -   Maximum **payload (data) size** per frame (Data Link Layer).
-   RTT
    -   Round Trip Time
    -   Time from the start of the first packet sent from the CWND to the receipt of the ACK of the last packet sent from e current CWND.
-   Capacity/Bandwidth > Throughput > Goodput
    -   Capacity/Bandwidth
        -   The total transmission/sending rate of the link.
        -   Measured in bps (Bits per Second)
    -   Throughput
        -   Actual transmission/sending rate available after losses.
        -   Includes new data and retransmitted data.
        -   Measured in bps (Bits per Second)
    -   Goodput
        -   The transmission/sending rate of new data.
        -   Measured in bps (Bits per Second)

## Congestion Control Algorithms of TCP

-   Slow Start (SS)
-   Congestion Avoidance
-   Fast Retransmit
-   Fast Recovery

> Read from [Section 3.6](https://networking.harshkapadia.me/files/books/computer-networking-a-top-down-approach-8th-edition.pdf#page=266) and [Section 3.7](https://networking.harshkapadia.me/files/books/computer-networking-a-top-down-approach-8th-edition.pdf#page=274) of the 'Computer Networking - A Top-Down Approach' book.

### Slow Start (SS)

-   Exponential growth (Doubling) to rapidly increase sending rate
-   'SS Threshold's
    -   CWND size at which SS stops.
-   CWND
    -   Initial
        -   CWND = 1 MSS
        -   SS threshold = Large value
    -   Incrementing CWND
        -   `CWND size = CWND size + 1 MSS` **per ACK**, which implies doubling the CWND size **every RTT**.
        -   Incrementing CWND stops when `CWND = min(SS Threshold, RAWND)`.
            -   New SS Threshold value?
        -   SS phase stop (**Whichever of the following occurs first.**)
            -   Packet loss occurs
                -   Implies congestion
                -   `SS Threshold = CWND size / 2`
                -   Packet loss indicators
                    -   RTO expiring (Timeout)
                        -   Heavy congestion
                    -   Duplicate ACKs
                        -   Low to moderate congestion
            -   SS Threshold is reached
            -   RAWND is reached
                -   Rate of sending becomes constant
-   Ramps up sending rate faster than [AIMD](#congestion-avoidance).

### Congestion Avoidance

-   Linear increase of sending rate rather than exponential increase (as in [Slow Start](#slow-start-ss)), as Congestion Avoidance is slowly probing for congestion point.
    -   Need to probe for congestion point to be able to operate at optimal throughput (just below link capacity).
-   Congestion Avoidance practices **AIMD** (Additive Increase, Multiplicative Decrease).
-   Starts after 'SS Threshold' is hit in Slow Start.
-   AIMD
    -   Additive Increase (AI)
        -   `CWND size = CWND size + (1 / MSS)` **per ACK**, which implies increasing the CWND size by one MSS **every RTT**.
        -   Linear increase
    -   Multiplicative Decrease (MD)
        -   `CWND size = CWND size / 2`
        -   This is a multiplicative decrease, as CWND decreases by a factor of `1 / 2`.

### Fast Retransmit

-   On receiving three consecutive duplicate ACKs, the sender immediately re-transmits the assumingly lost packet.
-   This is done to utilize the channel appropriately and not have wait times with no packet sending till the RTO expires to trigger a re-transmission.
-   There is a chance that the packet was not lost and will just reach late, but to hasten the transfer to use the link capacity optimally, Fast Retransmit is used.
    -   This is fair to do, as loss detection by duplicate ACKs implies that the network is not as congested as when a loss is detected by a RTO expiring (which implies that no packets can be sent or received), so it is okay to retransmit without maybe requiring to, to hasten up communication and increase communication efficiency.

### Fast Recovery

-   Fast Recovery works with [Fast Retransmit](#fast-retransmit).
    -   [If we have Fast Retransmit does it mean we have Fast Recovery?](https://networkengineering.stackexchange.com/a/35448)
-   It starts on the detection of three consecutive duplicate ACKs.
    -   Duplicate ACKs indicate low to moderate congestion.
-   On the detection of three consecutive duplicate ACKs
    -   [Fast Retransmit](#fast-retransmit) kicks in here and sends the missing packet.
    -   `SS Threshold = CWND size / 2`
    -   Now `CWND size = SS Threshold + 3 MSS` (1 MSS per duplicate ACK and there are three duplicate ACKs here), which implies that the CWND is artificially inflated.
    -   For every duplicate ACK received after the three duplicate ACKs, `CWND size = CWND size + 1 MSS`
    -   Once the ACK for the retransmitted packet is received, `CWND size = SS Threshold`, which implies that the CWND is deflated and returned back to its usual condition.
    -   Fast Recovery now goes to the [Congestion Avoidance](#congestion-avoidance) algorithm, but if a timeout (RTO expiry) occurs, then it goes to the [Slow Start](#slow-start-ss) algorithm.
-   [More info (RFC 5681, Section 3.2)](https://www.rfc-editor.org/rfc/rfc5681#section-3.2)
-   [Where is the Slow Start Threshold value set by TCP Reno Fast Recovery used?](https://stackoverflow.com/questions/48689788/where-is-the-slow-start-threshhold-value-set-by-tcp-reno-fast-recovery-used)

## Versions of TCP

-   TCP Tahoe
-   TCP Reno
-   TCP NewReno
-   TCP CUBIC
-   TCP Vegas
-   TCP BBR
-   CTCP (Compound TCP)
-   FAST TCP (FAST Active Queue Management Scalable TCP)
-   TCP Veno
-   TCP Westwood
-   TCP Bic
-   H-TCP (TCP Hamilton)
-   HS-TCP (Highspeed TCP)
-   TCP Hybla
-   TCP Illinois
-   TCP SACK

and more...

### TCP Tahoe

-   A Loss-based Congestion Control Algorithm.
-   Congestion Control algorithms used
    -   [Slow Start (SS)](#slow-start-ss)
    -   [Congestion Avoidance](#congestion-avoidance)
        -   Only Additive Increase (AI)
-   Only timeouts were used to detect packet loss, so `CWND size = 1 MSS` after every RTO expiry.

<p align="center">
    <img src="./files/img/tcp/tcp-tahoe.png" alt="TCP Tahoe Time vs CWND size graph" loading="lazy" />
</p>

### TCP Reno

-   A Loss-based Congestion Control Algorithm.
-   Congestion Control algorithms used
    -   [Slow Start (SS)](#slow-start-ss)
    -   [Congestion Avoidance (AIMD)](#congestion-avoidance)
    -   [Fast Recovery](#fast-recovery) with [Fast Retransmit](#fast-retransmit)
-   Packet loss detection
    -   Timeout (RTO expiry)
        -   `CWND size = 1 MSS`
    -   Three consecutive duplicate ACKs
        -   `CWND size = CWND size / 2` (MD)

<p align="center">
    <img src="./files/img/tcp/tcp-reno.png" alt="TCP Reno Time vs CWND size graph" loading="lazy" />
</p>

### TCP CUBIC

-   A Loss-based Congestion Control Algorithm.
-   Similar to TCP Reno, but has changes in the Congestion Avoidance phase.
-   [More info](http://intronetworks.cs.luc.edu/1/html/newtcps.html#tcp-cubic)

### TCP Vegas

-   A Delay-based Congestion Control Algorithm.
-   It compares the current Throughput with Throughput when the link was uncongested, and decides the current sending rate based on that.
-   [More info](http://intronetworks.cs.luc.edu/1/html/newtcps.html#tcp-vegas)

### TCP BBR

-   [BBR: Congestion-Based Congestion Control](https://queue.acm.org/detail.cfm?id=3022184) (Research paper)
-   [TCP BBR - Exploring TCP congestion control](https://toonk.io/tcp-bbr-exploring-tcp-congestion-control)

## Resources

-   [github.com/HarshKapadia2/tcp-version-performance-comparison](https://github.com/HarshKapadia2/tcp-version-performance-comparison)
-   [TCP Congestion Control](https://en.wikipedia.org/wiki/TCP_congestion_control)
-   [Newer TCP Implementations](http://intronetworks.cs.luc.edu/1/html/newtcps.html)
-   [github.com/AlimuddinKhan/TCP_Protocol_Comparison](https://github.com/AlimuddinKhan/TCP_Protocol_Comparison)
