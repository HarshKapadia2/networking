# Homa

([Back to Home](README.md))

## Table of Contents

-   [Introduction](#introduction)
-   [The Data Center Environment](#the-data-center-environment)
    -   [Topology](#topology)
    -   [Traffic Properties](#traffic-properties)
    -   [Traffic Control Challenges](#traffic-control-challenges)
    -   [Network Requirements](#network-requirements)
    -   [Protocol Requirements](#protocol-requirements)
-   [Message vs Packet](#message-vs-packet)
-   [Problems with TCP](#problems-with-tcp)
-   [Sender vs Receiver](#sender-vs-receiver)
-   [Homa Features](#homa-features)
-   [Homa Design Principles](#homa-design-principles)
-   [Homa Packet Types](#homa-packet-types)
-   [Streaming vs Messages](#streaming-vs-messages)
    -   [The Problem with TCP Streaming](#the-problem-with-tcp-streaming)
    -   [How Messages Help](#how-messages-help)
-   [Resources](#resources)

## Introduction

-   The [Transmission Control Protocol (TCP)](tcp.md) is the most widely used transport protocol on the internet. It is well-designed, but just like any other protocol, it has its own issues. It is not suitable for every environment and faces [problems in a Data Center environment](#problems-with-tcp).
-   **Homa** is transport protocol designed for the Data Centers. It aims to replace TCP as the transport protocol in Data Centers and claims to fix all of TCP's problems for the Data Center. It is not API-compatible with TCP.
-   Homa reduces the 'Data Center tax' that TCP introduces with its connection maintenance and processing overheads.
-   The primary goal of Homa is to provide the lowest possible latency for short messages at high network load.
    -   The focus is on reducing **tail message latency** (P99 [99th percentile] latency) for short messages, i.e., the latency of short messages at high network load, as it is the most important performance metric for Data Center applications.

## The Data Center Environment

### Topology

<p align="center">
    <img src="./files/img/homa/typical-data-center-cluster.png" alt="A typical Data Center cluster" loading="lazy" />
</p>

-   Data Center -> Clusters -> Racks (with a Top of Rack [ToR] switch) -> Machines
-   There are multiple structures in which connections can be made between each of the components above, but the usual structure is as he above point.
-   Common topologies
    -   Fat-Tree
    -   Leaf-Spine (or Spine-and-Leaf)
    -   VL2
    -   JellyFish
    -   DCell
    -   BCube
    -   Xpander

### Traffic Properties

-   It is difficult to generalise all Data Center traffic into one certain type, because it is highly dependent on how applications are designed and built.
-   Depending on the application, there can be thousands of flow arrivals per second.
-   Flows are unpredictable in types, sizes and burst periods.
    -   Burstiness can be in terms of traffic in a flow or the number of flows.
-   Connections can be long-lived as well and need not always be transmitting.
-   Rough types
    -   Interactive flows/latency-sensitive flows
    -   Throughput-sensitive flows
    -   Deadline-bound flows

### Traffic Control Challenges

-   Unpredictable traffic matrix
    -   Application dependent
    -   Most flows are short with just a few packets, but most bytes are delivered by long flows.
    -   High flow arrival rates with majority being short flows.
-   Mix of various flow types/sizes
    -   Application dependent
    -   Interactive flows (User-initiated queries like web searches) are time-sensitive, latency-sensitive and high priority flows.
    -   Throughput-sensitive flows (like MapReduce parallel data computing jobs) are not delay-sensitive, but need consistent bandwidth.\
    -   Deadline-bound flows with soft or hard deadlines can be both Interactive or Throughput-sensitive flows.
-   Traffic burstiness
    -   Traffic burstiness causes increased packet losses, increased buffer occupancy, increased queuing delay, decreased throughput, increased flow completion times
    -   [TCP Slow Start](tcp.md#slow-start-ss) with large window sizes can cause bursty traffic as well.
-   Packer re-ordering
    -   At the receiver: Increases latency, Increases CPU utlization and reduces the server's link utilization
    -   Features such as [Fast Retransmit](tcp.md#fast-retransmit) might mistake re-ordering for loss.
-   Performance Isolation
    -   Control has to be developed on multiple layers and on multiple hardware components to prevent misuse and privacy, while keeping Service Level Agreements (SLAs) in mind.
-   The Incast problem
    -   Multiple senders sending to one machine causes bottleneck issues.
-   The Outcast problem
    -   TCP Outcast is when a port that has many flows and a few flows coming in from different ports, gives priority to the port with many flows, causing Port Blackout for the port with fewer flows. Port Blackout is essentially packets of the fewer flows being dropped, which affects them due to the TCP timeouts it causes.

### Network Requirements

A Data Center environment should have:

-   Very high bandwidth/capacity/link utilization
    -   Depends on topology and traffic control measures.
    -   Aids in having more tenants on the same infrastructure.
-   Very low latency
-   Very small flow completion times
    -   Mainly affected by queuing and packet losses.
-   Very low deadline miss rate/lateness
-   High fairness
    -   Applies to shared resources like link bandwidth and buffer space. (Maybe even to CPU cycles and memory.)
    -   SLAs should always be met.
    -   Prevents misuse and starvation.
-   High energy efficiency

### Protocol Requirements

Some of the important features a **Data Center transport protocol** should have:

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
    -   Trying to load balance Data Center workloads causes additional overheads to manage cache and the connections, and also causes hot spots where workload is not properly distributed.
    -   Load Balancing overheads are a major reason for tail latency.
-   Network Interface Card (NIC) offload
    -   The protocol cannot be a pure software implementation, because that's too slow. It should make use of inherent NIC features, for which better NICs are needed as well.

## Message vs Packet

-   Message
    -   A logically sensible data unit that makes sense in its entirety and can be processed.
-   Packet
    -   A split of a message (a chunk) that obviously doesn't make logical sense individually, but can be combined with other packets to form a message.
    -   They usually have offsets, sequence numbers, or some other mechanism to help order packets in a logical sequence.

## Problems with TCP

The following features of TCP cause it problems **in the Data Center**:

-   Stream orientation
    -   Please refer to [the 'Streaming vs Messages' section](#streaming-vs-messages).
-   Connection orientation
    -   Connections are not the best inside the Data Center, because each application might have hundreds or thousands of them and that causes overheads in space and time.
    -   Keeping aside packet buffer space and application level state, 2000 bytes of state data has to be maintained for every TCP socket.
    -   Connection setup takes up one Round Trip Time (RTT).
-   Bandwidth sharing (Fair scheduling)
    -   Under high loads, short messages have a very bad RTT as compared to long messages, due to [TCP Head of Line Blocking (HoLB)](https://stackoverflow.com/questions/45583861/how-does-http2-solve-head-of-line-blocking-hol-issue).
    -   Under high load, all streams share bandwidth, which collectively slows down everyone.
-   Sender-driven congestion control
    -   Congestion is usually detected when there is buffer occupancy, which implies that there will be some packet queuing, which further implies increased latency and HoLB.
    -   TCP does not make use of priority queues in modern switches, which implies that all messages are treated equally, which causes problems for short messages behind long message queues. (HoLB)
    -   It causes a latency vs throughput dilemma, where less latency implies buffers being under-utilized, which in-turn reduces the throughput for long messages, and high throughput implies always having data in buffers ready to go, but the queuing causes delays for short messages, increasing the latency.
    -   Please refer to [the 'Streaming vs Messages' section](#streaming-vs-messages).
-   In-order packet delivery
    -   Asymmetries in packet delivery in a Data Center environment due to Packet Spraying (sending packets across multiple connections) can cause packet reordering beyond TCP's tolerance threshold and cause unnecessary retransmissions.
    -   If Packet Spraying is not used and Flow-consistent Routing is used, which fixes links for particular TCP flows, it can cause hot spots for the duration of the connection on particular links if multiple flows get hashed through the same links.
    -   Linux performs Load Balancing at the software level by routing packets through multiple cores for processing and to maintain the order or delivery, all packets have to pass through the same sequence of cores, which can lead to core hot spots as well, if multiple flows get hashed to the same cores. This also increases the tail latency of TCP.

## Sender vs Receiver

-   Client to server communication:
    -   Sender: Client
    -   Receiver: Server
-   Server to client communication:
    -   Sender: Server
    -   Receiver: Client

## Homa Packet Types

> NOTE:
>
> -   [Message vs Packet](#message-vs-packet)
> -   [Sender vs Receiver](#sender-vs-receiver)

-   `DATA`
    -   Sent from sender to receiver.
    -   Contains a range of bytes within a message, defined by an offset and a length.
    -   Also indicates the total message length.
-   `GRANT`
    -   Sent from receiver to sender.
    -   Indicates that the sender may now transmit all bytes in the message up to a given offset.
    -   Also specifies the priority level to use.
-   `RESEND`
    -   Sent from receiver to sender.
    -   Indicates that the sender should re-transmit a given range of bytes within a message.
-   `BUSY`
    -   Sent from sender to receiver.
    -   Indicates that a response to `RESEND` will be delayed.
        -   The sender might be busy transmitting higher priority messages or an RPC operation is still being executed.
    -   Used to prevent timeouts.

## Homa Features

<p align="center">
    <img src="./files/img/homa/homa-overview.png" alt="Overview of the Homa protocol" loading="lazy" />
</p>

-   Message-oriented protocol, that implements [Remote Procedure Calls (RPCs)](http.md#rest-vs-rpc) rather than streams.
    -   Please refer to the [Message vs Packet](#message-vs-packet) and the [Streaming vs Messages](#streaming-vs-messages) sections.
    -   Homa exposes discrete messages to transport, letting multiple threads read from a single socket without worrying about getting a message from a different connection (as in the TCP world).
    -   This is disadvantageous in the sense that longer messages will have a higher latency, because every message will have to be delivered in its entirety, as these are not streams.
        -   This can be overcome by sending multiple messages in parallel, so essentially the data is being broken into multiple messages. (This is so much like TCP though and won't this need re-ordering and state maintenance, which is what Homa wanted to avoid?)
-   Connectionless protocol
    -   Homa uses RPCs and so it doesn't require explicit connection establishment between the sender and receiver, and vice versa. This reduces connection setup overhead.
    -   An application can use a single socket to manage any number of concurrent RPCs with any number of peers.
    -   Each RPC is handled independently and there are no message ordering guarantees between concurrent RPCs.
    -   Homa ensures reliable connections (errors are sent after unrecoverable network or host failures).
    -   It is a connectionless protocol, but not a stateless protocol.
    -   State maintained by Homa
        -   State for sockets, RPCs and peers are kept (200 bytes per host vs TCP's 2000 bytes per connection [not including data buffer space]).
        -   One way to think of Homa is that it maintains short-lived and lightweight connections for each RPC.
        -   Each RPC is handled independently and Flow Control, Retry and Congestion Control are implemented per RPC state.
-   Shortest Remaining Processing Time (SRPT) Scheduling
    -   Homa uses SRPT Scheduling (a type of Run-to-Completion Scheduling) to queue messages to send and receive. It is best if both, the receiver and the sender, use SRPT, as it prevents short messages from starving behind long messages in queues on both ends.
    -   Homa makes use of priority queues in modern switches and queues shorter messages through the priority queues, so that they don't get starved by long messages. This helps reduce the 'latency vs bandwidth' optimization problem.
        -   Reducing queuing is the key to reducing latency.
        -   Homa intentionally does 'controlled overcommitment', i.e., it allows a little buffering (for longer messages), to keep link utilization high (thus optimizing for throughput, while keeping latency low through SRPT and priority queues).
            -   The controlled overcommitment helps in keeping up capacity utilization in cases where senders aren't sending messages in a timely fashion.
    -   Homa also allocates 5-10% of the bandwidth to the oldest message (which will be the longest one), so that the longest message also doesn't completely starve.
-   Receiver-driven Congestion Control
    -   A receiver is usually in a better position to signal and drive congestion rather than the sender, because the receiver knows how much buffer capacity it has left and the number of RPCs that it has. So, it is better to let the receiver signal whether messages can be sent or not.
    -   A sender can send a few unscheduled packets to receive some replies from the receiver to test the waters, but packets after that will be scheduled and can be sent only if the receiver sends a _grant_ for those messages.
        -   The message size is mentioned in the initial unscheduled blindly sent (to reduce latency) packets, which further helps the receiver to make a decision on scheduling those messages and also allows it to give priority to shorter messages.
            -   Yes, this might cause some buffering if there are too many senders that send unscheduled packets, but that minimum buffering is unavoidable. The scheduling of further messages through the _grant_ mechanism ensures reduced buffer occupancy.
        -   A `GRANT` packet is sent for every `DATA` packet (if the receiver decides that it can accept more data) and it contains an offset for the number of outstanding bytes of the message size that it wants from the sender and also the priority that the sender should send the packet with. So Homa can vary priorities dynamically based on the load it has on the receiver.
        -   The sender should transmit 'RTT bytes' (including software delays on both ends) and by the time RTT bytes are sent, it should receive an indication from the receiver whether to keep sending or not, thus reducing transmission latency in case an immediate grant is received.
    -   As the receiver knows the load it has and expects from the received messages, it can prioritise messages (using a small number of priority queues) and the bandwidth they can have.
        -   Knowing the message sizes, they can predict the bandwidth required and take the decision of granting and priority on those basis.
        -   This helps the receiver implement SRPT Scheduling, as they have the priority in their control.
-   Out-of-Order packets
    -   Homa can tolerate Out-of-Order packets, so Packet Spraying works, which aids load balancing over multiple links, avoiding network traffic hot spot creation.

## Homa Design Principles

-   Transmitting short messages blindly
-   Using in-network priorities
-   Allocating priorities dynamically at receivers in conjunction with receiver-driven rate control
-   Controlled over-commitment of receiver downlinks

## Streaming vs Messages

> NOTE: [Message vs Packet](#message-vs-packet)

### The Problem with TCP Streaming

-   TCP is not aware of the message size. It is only aware of the length of the current packet.
-   TCP will break up (segment) whatever it receives from the application above it in the OSI stack into packets of 'Maximum Segment Size (MSS) bytes' and send it across. (Streaming)
    -   It might also wait for MSS to be fulfilled before sending, but that is a setting that can be toggled.
-   This streaming behaviour obviously adds buffering and packet ordering at the receiver, but more importantly the receiver has no knowledge of when it can start processing something or how much data it is going to receive. The sender is thus responsible to not overwhelm the receiver (Flow Control) and the network (Congestion Control).
-   TCP streaming causes Load Balancing difficulties, because the path of sending data is usually consistent (Flow-consistent routing) and multiple flows on the same paths can cause congestion (hot spots) and HoLB.
-   Causes an increase in tail latency due to HoLB, where short messages get delayed behind long messages on the same stream.
    -   Using multiple TCP connections to the same host to counter HoLB causes a connection explosion, with too much state to be maintained per connection and too much work to send, receive and manage all the connections on the receiver and sender.

### How Messages Help

-   The sender transmits the **message size** to the receiver during the initial unscheduled transmission, so the receiver can calculate the exact bandwidth required for the entire communication and decide grants and priorities.
-   Buffering and packet ordering at the receiver will still exist here, but now the receiver is cognizant of how much data it can expect to receive and can make decisions based on bandwidth requirements, its current load, its buffer occupancy, observed RTT, etc.
    -   This helps `GRANT` packets from the receiver to the sender to specify an offset of outstanding 'RTT bytes' of the message to transmit to the receiver to ensure as far as possible, no interruptions in transmitting, which improves bandwidth utilization.
        -   Specifying this also helps with buffer occupancy predictions and checks, because the receiver knows how much a particular RPC was allowed to send in a particular packet.
    -   This puts the power of Congestion and Flow Control in the hands of the receiver, which makes more sense, because it is the entity that has the best knowledge of its state, rather than the sender having to make guesses based on parameters like 'packet loss' and 'duplicate acknowledgements', that are not the most accurate indicators of congestion.
-   Removing streaming also gets rid of the [TCP Head of Line Blocking (HoLB)](https://stackoverflow.com/questions/45583861/how-does-http2-solve-head-of-line-blocking-hol-issue) problem.
    -   In the HTTP world, QUIC (the transport protocol for HTTP/3) solves this by having multiple independent streams, unlike TCP in HTTP/2, which was multiplexing multiple streams over a single TCP stream/connection (thus causing HoLB).
        -   The point here can be that Homa is doing away with streaming altogether and just using messages, so not only is HoLB solved, but so are [the other issues with TCP streaming](#the-problem-with-tcp-streaming).

## Resources

-   [Directed Study application](files/homa/directed-study-application.pdf)
-   Research papers
    -   [It's Time to Replace TCP in the Datacenter (v2)](files/homa/research-papers/its-time-to-replace-tcp-in-the-datacenter-v2.pdf) ([arXiv](https://arxiv.org/abs/2210.00714v2))
    -   [Homa: A Receiver-Driven Low-Latency Transport Protocol Using Network Priorities (Complete Version)](files/homa/research-papers/homa-a-receiver-driven-low-latency-transport-protocol-using-network-priorities-complete-version.pdf) ([arXiv](https://arxiv.org/abs/1803.09615))
    -   [Datacenter Traffic Control: Understanding Techniques and Tradeoffs](files/homa/research-papers/data-center-traffic-control-understanding-techniques-and-tradeoffs.pdf) ([IEEE Xplore](https://ieeexplore.ieee.org/abstract/document/8207422))
-   Presentations
    -   Homa 1 ([PDF](files/homa/presentations/homa-1.pdf), [Google Slides](https://docs.google.com/presentation/d/1uryO-L3TkBjBTeEFQAh6cAy9x4VJwpEGIUIOZRuAf5E/edit?usp=sharing))
-   Videos
    -   [Discussing the Homa paper - Replacing TCP for the Datacenter](https://www.youtube.com/watch?v=nEFOni_87Yw)
    -   [USENIX ATC '21 - A Linux Kernel Implementation of the Homa Transport Protocol](https://www.youtube.com/watch?v=qu5WDcZRveo)
    -   [Netdev 0x16 - Keynote: It's Time to Replace TCP in the Datacenter](https://www.youtube.com/watch?v=o2HBHckrdQc)
-   [Transmission Control Protocol (TCP)](tcp.md)
-   [Remote Procedure Calls (RPCs)](http.md#rest-vs-rpc)
-   [Incast](https://www2.eecs.berkeley.edu/Pubs/TechRpts/2012/EECS-2012-40.pdf)
-   Data Plane Development Kit (DPDK)
    -   [What is DPDK?](https://www.packetcoders.io/what-is-dpdk)
    -   [dpdk.org](https://www.dpdk.org)
