# Homa

([Back to Home](README.md))

## Table of Contents

-   [Introduction](#introduction)
-   [The Data Center Environment](#the-data-center-environment)
    <!-- -   [Workload Types](#workload-types)
    -   [Topology](#topology)
    -   [Network Requirements](#network-requirements) -->
    -   [Protocol Requirements](#protocol-requirements)
-   [Problems with TCP](#problems-with-tcp)
-   [Homa's Features](#homas-features)
-   [Resources](#resources)

## Introduction

-   The [Transmission Control Protocol (TCP)](tcp.md) is the most widely used transport protocol on the internet. It is well-designed, but just like any other protocol, it has its own issues. It is not suitable for every environment.
-   [TCP faces some problems in a Data Center environment.](#problems-with-tcp) **Homa**, a new (as in 2023) transport protocol designed for the Data Centers, aims to replace TCP as the transport protocol in Data Centers and claims to fix all of TCP's problems for the Data Center. It is not API-compatible with TCP.
-   Homa reduces the 'Data Center tax' that TCP introduces with its connection maintenance and processing overheads.

## The Data Center Environment

<!-- ### Workload Types

### Topology

### Network Requirements -->

### Protocol Requirements

Some of the important features a Data Center transport protocol should have:

-   Reliable delivery
    -   Data should be delivered regardless of failures.
-   Low latency
    -   Data should be delivered as fast as possible.
    -   Tail latency should be good.
    -   Packet processing overheads should be low.
-   High throughput
    -   Both data throughput (amount of data sent) and message throughput (no. of messages sent) should be high.
-   Congestion control
    -   Refers to packet buildup in core and edge buffers.
    -   Congestion needs to be kept at a minimum to ensure low latency.
-   Efficient Load Balancing
    -   Trying to load balance Data Center workloads causes additional overheads to manage cache and the connections, and also causes host spots where workload is not properly distributed.
    -   Load Balancing overheads are a major reason for tail latency.
-   Network Interface Card (NIC) offload
    -   The protocol cannot be a pure software implementation, because that's too slow. It should make use of inherent NIC features, for which better NICs are needed as well.

## Problems with TCP

The following features of TCP cause it problems in the Data Center:

-   Stream orientation
    -   TCP streams messages in chunks and the receiver has no guarantee of whether it will receive the entire message in one go or not, and has to maintain state for partially received communication. This introduces complexity and overheads. Threads have to wait to construct an entire message before being able to process the request.
    -   Causes Load Balancing difficulties.
    -   Causes an increase in tail latency due to head-of-line blocking, where short messages get delayed behind long messages on the same stream.
-   Connection orientation
    -   Connections are not the best inside the Data Center, because each application might have hundreds or thousands of them and that causes overheads in space and time.
    -   Connection setup takes up one Round Trip Time (RTT).
-   Bandwidth sharing (Fair scheduling)
    -   Under high loads, short messages have a very bad RTT as compared to long messages.
    -   Under high load, all streams share bandwidth, which collectively slows down everyone.
-   Sender-driven congestion control
    -   Congestion is usually detected when there is buffer occupancy, which implies that there will be some packet queuing.
    -   TCP does not make use of priority queues in modern switches, which implies that all messages are treated equally, which causes problems for short messages behind long message queues.
    -   It causes a latency vs throughput dilemma, where less latency implies buffers being under-utilized, which in-turn reduces the throughput for long messages, and high throughput implies always having data in buffers ready to go, but the queuing causes delays for short messages.
-   In-order packet delivery
    -   Asymmetries in packet delivery in a Data Center environment due to Packet Spraying (sending packets across multiple connections) can cause packet reordering beyond TCP's tolerance threshold and cause unnecessary retransmissions.
    -   If Packet Spraying is not used and Flow-consistent Routing is used, which fixes links for particular TCP flows, it can cause hot spots for the duration of the connection on particular links if multiple flows get hashed through the same links.
    -   Linux performs Load Balancing at the software level by routing packets through multiple cores for processing and to maintain the order or delivery, all packets have to pass through the same sequence of cores, which can lead to core hot spots as well, if multiple flows get hashed to the same cores. This also increases the tail latency of TCP.

## Homa's Features

-   Message-oriented protocol, that implements Remote Procedure Calls (RPCs) rather than streams.
    -   Homa exposes discrete messages to transport, letting multiple threads read from a single socket without worrying about getting a message from a different connection (as in the TCP world).
    -   This is disadvantageous in the sense that longer messages will have a higher latency, because every message will have to be delivered in its entirety, as these are not streams.
        -   This can be overcome by sending multiple messages in parallel, so essentially the data is being broken into multiple messages. (This is so much like TCP though and won't this need re-ordering and state maintenance, which is what Homa wanted to avoid?)
-   Connectionless protocol
    -   It reduces connection setup overhead.
    -   An application can use a single socket to manage any number of concurrent RPCs with any number of peers.
    -   Each RPC is handled independently and there are no message ordering guarantees between concurrent RPCs.
    -   Homa ensures reliable connections (errors are sent after unrecoverable network or host failures).
    -   State maintained by Homa
        -   State for sockets, RPCs and peers (200 bytes per host vs TCP's 2000 bytes per connection) are kept.
        -   One way to think of Homa is that it maintains short-lived and lightweight connections for each RPC.
        -   Each RPC is handled independently and Flow Control, Retry and Congestion Control are implemented per RPC state.
-   Shortest Remaining Processing Time (SRPT) Scheduling
    -   Homa uses SRPT Scheduling (a type of Run-to-Completion Scheduling) to queue messages to send.
    -   Homa makes use of priority queues in modern switches and queues shorter messages through the priority queues, so that they don't get starved by long messages. This helps reduce the 'latency vs bandwidth' optimization problem.
        -   Homa intentionally allows a little buffering for longer messages to keep link utilization high (thus optimizing for throughput, while keeping latency low through SRPT and priority queues).
    -   Homa also allocates 5-10% of the bandwidth to the oldest message (which will be the longest one), so that the longest message also doesn't completely starve.
-   Receiver-driven Congestion Control
    -   A receiver is usually in a better position to signal and drive congestion rather than the client, because the receiver knows how much buffer it has left and the number of connections that it has. So, it is better to let the receiver signal whether messages can be sent or not.
    -   A sender can send a few unscheduled packets to receiver some replies from the receiver to test the waters, but packets after that will be scheduled and can be sent only if the receiver sends a _grant_ for those messages.
    -   As the receiver knows the load it has and expects from the received messages, it can prioritise messages and the bandwidth they can have.
-   Out-of-Order packets
    -   Homa can tolerate Out-of-Order packets, so Packet Spraying works, which aids load balancing over multiple links, avoiding network traffic hot spot creation.

## Resources

-   [Directed Study application](files/homa/directed-study-application.pdf)
-   Research papers
    -   [It's Time to Replace TCP in the Datacenter (v2)](files/homa/research-papers/its-time-to-replace-tcp-in-the-datacenter-v2.pdf) ([arXiv](https://arxiv.org/abs/2210.00714v2))
-   [Transmission Control Protocol (TCP)](tcp.md)
