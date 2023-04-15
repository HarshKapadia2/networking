# Homa

([Back to Home](README.md))

## Table of Contents

-   [Introduction](#introduction)
-   [Data Center Environment](#data-center-environment)
    -   [Topology](#topology)
    -   [Traffic Properties](#traffic-properties)
    -   [Traffic Control Challenges](#traffic-control-challenges)
    -   [Network Requirements](#network-requirements)
    -   [Protocol Requirements](#protocol-requirements)
-   [Message vs Packet](#message-vs-packet)
-   [Problems with TCP](#problems-with-tcp)
-   [Sender vs Receiver](#sender-vs-receiver)
-   [Packet Types](#packet-types)
-   [Features](#features)
    -   [Message Orientation](#message-orientation)
    -   [Connectionless Protocol](#connectionless-protocol)
    -   [Shortest Remaining Processing Time (SRPT)](#srpt)
    -   [Receiver-Driven Congestion Control](#receiver-driven-congestion-control)
    -   [Out-of-Order Packet Tolerance](#out-of-order-packet-tolerance)
    -   [No Per-Packet Acknowledgements](#no-per-packet-acknowledgements)
    -   [At-Least-Once Semantics](#at-least-once-semantics)
-   [Design Principles](#design-principles)
-   [Linux Internals](#linux-internals)
-   [Streaming vs Messages](#streaming-vs-messages)
    -   [The Problem with TCP Streaming](#the-problem-with-tcp-streaming)
    -   [How Messages Help](#how-messages-help)
-   [API](#api)
-   [Message Sequence Scenarios](#message-sequence-scenarios)
-   [Resources](#resources)

## Introduction

-   The [Transmission Control Protocol (TCP)](tcp.md) is the most widely used transport protocol on the internet. It is well-designed, but just like any other protocol, it has its own issues. It is not suitable for every environment and faces [problems in a Data Center environment](#problems-with-tcp).
-   **Homa** is transport protocol designed for the Data Centers. It aims to replace TCP as the transport protocol in Data Centers and claims to fix all of TCP's problems for the Data Center. It is not API-compatible with TCP.
-   Homa reduces the 'Data Center tax' that TCP introduces with its connection maintenance and processing overheads.
-   The primary goal of Homa is to provide the lowest possible latency for short messages at high network load.
    -   The focus is on reducing **tail message latency** (P99 [99th percentile] latency) for short messages, i.e., the latency of short messages at high network load, as it is the most important performance metric for Data Center applications.

## Data Center Environment

### Topology

<p align="center">
    <img src="files/img/homa/typical-data-center-cluster.png" alt="A typical Data Center cluster" loading="lazy" />
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
-   Usually, short flows require low latencies and long flows require high throughput.

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
-   Network Interface Card/Controller (NIC) offload
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
        -   Techniques such as [Delayed ACKs](https://medium.com/@gonzalo.cloud/what-is-delayed-ack-and-how-can-it-be-a-bottleneck-in-your-network-77a7ecf7bb0b) have to be used to reduce packet overheads.
    -   Keeping aside packet buffer space and application level state, 2000 bytes of state data has to be maintained for every TCP socket.
    -   Connection setup takes up one Round Trip Time (RTT).
-   Bandwidth sharing (Fair scheduling)
    -   Under high loads, short messages have a very bad RTT as compared to long messages, due to [TCP Head of Line Blocking (HoLB)](tcp.md#tcp-head-of-line-blocking).
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

> A peer can be a sender or a receiver and can have multiple RPCs.

## Packet Types

> NOTE:
>
> -   [Message vs Packet](#message-vs-packet)
> -   [Sender vs Receiver](#sender-vs-receiver)
> -   Source: [`protocol.md` file](https://github.com/PlatformLab/HomaModule/blob/master/protocol.md#packet-types) and [`homa_impl.h` file](https://github.com/PlatformLab/HomaModule/blob/master/homa_impl.h)

-   `DATA`
    -   `DATA(rpc_id, data, offset, self_prio, m_len)`
    -   Sent by the sender or receiver.
    -   Contains a contiguous range of bytes within a message, defined by an offset.
    -   Also indicates the total message length.
    -   It has the ability to acknowledge (`ACK`) one RPC, so future RPCs can be used to acknowledge one RPC, thus not requiring an explicit `ACK` packet to be sent.
-   `GRANT`
    -   `GRANT(rpc_id, offset, exp_prio)`
    -   Sent by the receiver.
    -   Indicates that the sender may now transmit all bytes in the message up to a given offset.
    -   Also specifies the priority level to use for the `DATA` packets.
-   `RESEND`
    -   `RESEND(rpc_id, offset, len, exp_prio)`
    -   Sent by the sender or receiver.
    -   Indicates that the sender should re-transmit a given range of bytes within a message.
    -   Includes priority that should be used for the retransmitted packets.
    -   To prevent unnecessary bandwidth usage, Homa only issues one outstanding `RESEND` packet to a given peer at a time. (One peer can have multiple RPCs.) Homa rotates the `RESEND`s among the RPCs to that peer.
    -   If enough timeouts occur (i.e., enough `RESEND` packets are sent), Homa concludes that a peer has crashed, aborts all RPCs for that peer and discards all the state associated with those RPCs.
-   `UNKNOWN`
    -   `UNKNOWN(rpc_id)`
    -   Sent by the sender or receiver.
    -   Indicates that the RPC for which a packet was received is unknown to it.
-   `BUSY`
    -   `BUSY(rpc_id)`
    -   Sent from sender to receiver.
    -   Indicates that a response to `RESEND` will be delayed.
        -   The sender might be busy transmitting higher priority messages or another RPC operation is still being executed.
    -   Used to prevent timeouts.
        -   It can be thought of as a 'keep-alive' indicator, as it keeps the communication alive and prevents the RPC from being aborted due to lack of data receipt.
-   `CUTOFFS`
    -   `CUTOFFS(rpc_id, exp_unsched_prio)`
    -   Sent by the receiver.
    -   Indicates priority cutoff values that the sender should use for unscheduled packets.
-   `ACK`
    -   `ACK(rpc_id)`
    -   Sent by the sender.
    -   Explicitly acknowledges that receipt of a response message to **one or more RPCs**.
        -   Aids the receiver to discard state for completed RPCs.
-   `NEED_ACK`
    -   `NEED_ACK(rpc_id)`
    -   Sent by the receiver.
    -   Indicates an explicit requirement for an acknowledgement (`ACK` packet) for the response of a particular RPC.

> -   `FREEZE`
>     -   Only for performance measurements, testing and debugging.
> -   `BOGUS`
>     -   Only for unit testing.

## Features

<p align="center">
    <img src="files/img/homa/homa-overview.png" alt="Overview of the Homa protocol" loading="lazy" />
</p>

Homa's features:

### Message Orientation

-   Homa is a Message-oriented protocol, that implements [Remote Procedure Calls (RPCs)](http.md#rest-vs-rpc) rather than streams.
-   Please refer to the [Message vs Packet](#message-vs-packet) and the [Streaming vs Messages](#streaming-vs-messages) sections.
-   Homa exposes discrete messages to transport, letting multiple threads read from a single socket without worrying about getting a message from a different connection (as in the TCP world, especially with HTTP/2 multiplexing multiple streams on one TCP connection, causing HoLB).

### Connectionless Protocol

-   Homa uses RPCs and so it doesn't require explicit connection establishment between the sender and receiver, and vice versa. This reduces connection setup overhead.
-   An application can use a single socket to manage any number of concurrent RPCs with any number of peers.
-   Each RPC is handled independently and there are no message ordering guarantees between concurrent RPCs.
-   Homa ensures reliable connections (errors are sent after unrecoverable network or host failures).
-   It is a connectionless protocol, but not a stateless protocol.
-   State maintained by Homa
    -   State for sockets, RPCs and peers are kept (200 bytes per host vs TCP's 2000 bytes per connection [not including data buffer space]).
    -   One way to think of Homa is that it maintains short-lived and lightweight connections for each RPC.
    -   Each RPC is handled independently and Flow Control, Retry and Congestion Control are implemented per RPC state.

### SRPT

-   Homa uses Shortest Remaining Processing Time (SRPT) Scheduling rather than Fair Scheduling.
-   Homa uses SRPT Scheduling (a type of Run-to-Completion Scheduling) to queue messages to send and receive. It is best if both, the receiver and the sender, use SRPT, as it prevents short messages from starving behind long messages in queues on both ends.
-   Homa makes use of priority queues in modern switches and queues shorter messages through the priority queues, so that they don't get starved by long messages. This helps reduce the 'latency vs bandwidth' optimization problem.
    -   Priority is divided into two groups, the highest levels are for unscheduled packets and the lower levels are for scheduled packets. In each group, the highest priorities are for the shorter messages.
        -   All packet types other than `DATA` packets have the highest priorities.
    -   The receiver assigns priorities dynamically (depending on the flows that it has) and can change them at any time it wishes. It communicates them through `GRANT` packets for scheduled packets and through `CUTOFFS` packets for unscheduled packets.
    -   The receiver assigning priorities makes sense because it knows all the flows that want to send data to it and its current network load and buffer occupancy.
    -   Reducing queuing is the key to reducing latency.
        -   Homa not only limits queue buildup in switches, but also in the Network Interface Controller (NIC), so that HoLB does not take place.
            -   To prevent queue build up in the NIC, it uses a queue and a 'Pacer Thread' that essentially keeps an approximate of the time in which the NIC queue will be empty and sends packets to the NIC from its queue based on that estimate while maintaining the original SRPT order.
    -   Homa intentionally does 'controlled overcommitment', i.e., it allows a little buffering (for longer messages), to keep link utilization high (thus optimizing for throughput, while keeping latency low through SRPT and priority queues).
        -   The controlled overcommitment helps in keeping up capacity utilization in cases where senders aren't sending messages in a timely fashion.
-   Homa also allocates 5-10% of the bandwidth to the oldest message (which will be the longest one), so that the longest message also doesn't completely starve. Both, the granting mechanism and the Pacer Thread take this into consideration.

### Receiver-Driven Congestion Control

-   A receiver is usually in a better position to signal and drive congestion rather than the sender, because the receiver knows how much buffer capacity it has left and the number of RPCs that it has. So, it is better to let the receiver signal whether messages can be sent or not.
-   A sender can send a few unscheduled packets to receive some replies from the receiver to test the waters, but packets after that will be scheduled and can be sent only if the receiver sends a _grant_ for those messages.
    -   The message size is mentioned in the initial unscheduled blindly sent (to reduce latency) packets, which further helps the receiver to make a decision on scheduling those messages and also allows it to give priority to shorter messages.
        -   Yes, this might cause some buffering if there are too many senders that send unscheduled packets, but that minimum buffering is unavoidable. The scheduling of further messages through the _grant_ mechanism ensures reduced buffer occupancy.
    -   A `GRANT` packet is sent after a decided amount of data (defaulted at 10,000 bytes), if the receiver decides that it can accept more data and it contains an offset for the number of outstanding bytes of the message size that it wants from the sender and also the priority that the sender should send the packet with. So Homa can vary priorities dynamically based on the load it has on the receiver.
        -   Homa does not send a `GRANT` packet for every `DATA` packet, as that causes a lot of overheads and Homa uses [TCP Segmentation Offload (TSO)](tcp.md#tcp-segmentation-offload), which implies that the sender transmits packets in groups, so every packet does not need to have a `GRANT` packet.
            -   The 'RTT bytes' that the `GRANT` packet sends might be split into multiple packets depending on the Maximum Transmission Unit (MTU) value.
    -   The sender should transmit 'RTT bytes' (including software delays on both ends) and by the time RTT bytes are sent, it should receive an indication from the receiver whether to keep sending or not, thus reducing transmission latency in case an immediate grant is received.
-   As the receiver knows the load it has and expects from the received messages, it can prioritise messages (using a small number of priority queues) and the bandwidth they can have.
    -   Knowing the message sizes, they can predict the bandwidth required and take the decision of granting and priority on those basis.
    -   This helps the receiver implement SRPT Scheduling, as they have the priority in their control.

### Out-of-Order Packet Tolerance

-   Homa has a high tolerate for out-of-order packets.
-   Homa can tolerate Out-of-Order packets, so Packet Spraying works, which aids load balancing over multiple links, avoiding network traffic hot spot creation.
    -   Homa does not follow TCP's Flow Consistent Routing.

### No Per-Packet Acknowledgements

-   Homa does not send out explicit acknowledgements for every packet, thus reducing almost half the packets that have to be sent per message. This reduces transmission overheads and conserves bandwidth.
-   As mentioned in the 'Homa Features' sub-point 'Receiver-driven Congestion Control' above, a `GRANT` packet is not sent for every `DATA` packet, but for a bunch of packets, so `GRANT` packets are not acknowledgement packets for every packet that was sent.
    -   Although not explicitly mentioned anywhere, they can be considered as SACK (Selective Acknowledgement) packets in my opinion.
-   If any packet is missing, the receiver will send a `RESEND` packet requesting for the information.
-   The sender has to send an explicit `ACK` packet on completely receiving a RPC response message from the receiver for a RPC request message, so that the receiver can discard the RPC state.
    -   If an `ACK` packet is not sent by the sender, the receiver can explicitly ask for one using the `NEED_ACK` packet.
    -   If the sender has not received the entire response message, it can send a `RESEND` packet to the receiver.

### At-Least-Once Semantics

-   [At-least-once semantics](https://www.lightbend.com/blog/how-akka-works-at-least-once-message-delivery#:~:text=Message%20Delivery%20Semantics)
-   In case of failures or losses, Homa does have mechanisms to ensure retransmission (Eg: The `RESEND` packet or fresh retries after deadlines), so packets are sent at least once, but can be sent more times to ensure delivery.

## Design Principles

Homa's Design Principles:

-   Transmitting short messages blindly
-   Using in-network priorities
-   Allocating priorities dynamically at receivers in conjunction with receiver-driven rate control
-   Controlled over-commitment of receiver downlinks

## Linux Internals

How Homa works in Linux:

<p align="center">
    <img src="files/img/homa/homa-linux-working.png" alt="Working of Homa in the Linux kernel" loading="lazy" />
</p>

-   Transmit (top): [`homa_send()`](#homa-api) -> copy packets -> [TSO](tcp.md#tcp-segmentation-offload)/GSO -> Homa, IP layer -> NIC (and its driver)
-   Receive (bottom): NIC ([RSS](<https://networking.harshkapadia.me/linux#:~:text=Scaling%20in%20the%20Linux%20Networking%20Stack%20(RSS%2C%20RPS%2C%20RFS%2C%20etc.)>)) -> Interrupt -> [NAPI](linux.md#napi) (GRO, SoftIRQ core choosing) -> SoftIRQ (network stack traversal) -> copy packets -> `homa_recv()`
-   Research paper explanation: [Packet flow and batching (4.1)](https://networking.harshkapadia.me/files/homa/research-papers/a-linux-kernel-implementation-of-the-homa-transport-protocol.pdf#page=5) from [A Linux Kernel Implementation of the Homa Transport Protocol](files/homa/research-papers/a-linux-kernel-implementation-of-the-homa-transport-protocol.pdf) ([USENIX](https://www.usenix.org/conference/atc21/presentation/ousterhout))
-   Review article: [A Linux Kernel Implementation of the Homa Transport Protocol, Part II](https://www.micahlerner.com/2021/08/29/a-linux-kernel-implementation-of-the-homa-transport-protocol.html)

## Streaming vs Messages

> NOTE: [Message vs Packet](#message-vs-packet)

### The Problem with TCP Streaming

-   TCP is not aware of the message size. It is only aware of the length of the current packet.
-   TCP will break up (segment) whatever it receives from the application above it in the OSI stack into packets of 'Maximum Segment Size (MSS) bytes' and send it across. (Streaming)
    -   It might also wait for MSS to be fulfilled before sending (like in [Nagle's Algorithm](https://en.wikipedia.org/wiki/Nagle's_algorithm)), but that is a setting that can be toggled.
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
-   Removing streaming also gets rid of the [TCP Head of Line Blocking (HoLB)](tcp.md#tcp-head-of-line-blocking) problem.
    -   In the HTTP world, QUIC (the transport protocol for HTTP/3) solves this by having multiple independent streams, unlike TCP in HTTP/2, which was multiplexing multiple streams over a single TCP stream/connection (thus causing HoLB).
        -   HoLB: Multiple messages multiplexed over a single TCP connection (as in HTTP/2) implies that even if only one packet at the start of the [Congestion Window (CWND)](tcp.md#important-terms) needs to be retransmitted, all the packets after it will be buffered at the receiver and not be handed to their respective streams up the networking stack even if the individual packets that might be belonging to different streams are complete.
            -   This is also where the scare of reading packets from a different stream from one connection pops up in TCP.
        -   The point here can be that Homa is doing away with streaming altogether and just using messages, so not only is HoLB solved, but so are [the other issues with streaming](#the-problem-with-tcp-streaming).

## API

> NOTE:
>
> -   These are the functions that implement the Homa API visible to applications. They are intended to be a part of the user-level run-time library.
> -   Source: [`homa_api.c` file](https://github.com/PlatformLab/HomaModule/blob/master/homa_api.c)

Homa's API:

-   `homa_send()`
    -   Send a request message to initiate a RPC.
    -   `homa_sendv()`
        -   Same as `homa_send()`, except that the request message can be divided among multiple disjoint chunks of memory.
-   `homa_reply()`
    -   Send a response message for a RPC previously received.
    -   `homa_replyv()`
        -   Similar to `homa_reply()`, except the response message can be divided among several chunks of memory.
-   `homa_abort()`
    -   Terminate the execution of a RPC.
    -   `homa_abortp()`
        -   Same as `homa_abort()`, but just receives all parameters in one `struct` instead of separately/individually.

## Message Sequence Scenarios

> NOTE: [Sender vs Receiver](#sender-vs-receiver)

Homa's Message Sequence Scenarios:

<p align="center">
    <img src="files/img/homa/homa-message-sequence-diagram-1.png" alt="Homa message sequence diagram" loading="lazy" />
</p>

-   The image above showcases a normal Homa RPC communication.
-   Both, a RPC Request and a RPC Response are shown.
-   Priority levels: `P0` (lowest) to `P7` (highest)
-   It is important to note that `GRANT` packets are for 'RTT bytes' to keep link utilization at 100%, but `DATA` packets are of the size of the [Maximum Transmission Unit (MTU)](tcp.md#important-terms). So each `GRANT` packet might generate multiple `DATA` packets.

<p align="center">
	<br />
	<br />
    <img src="files/img/homa/homa-message-sequence-diagram-2.png" alt="Homa message sequence diagram" loading="lazy" />
</p>

-   A RPC Request is shown in the image above.
-   The sender crashes after sending two of its three granted `DATA` packets. The first granted (scheduled) `DATA` packet is lost as well, which causes a timeout on the receiver, causing it to send a `RESEND` packet for the missing data.
-   After multiple `RESEND` packets not receiving responses, the receiver determines that the sender is non-responsive and discards all of the state related to that RPC ID.
-   On coming back online, the sender looks at its previous state and tries to resume by sending the last granted `DATA` packet that it had not sent, but the receiver sends an `UNKNOWN` packet, as it has already discarded all information related to that RPC ID.
-   The sender has to re-start the communication with the receiver.

<p align="center">
	<br />
	<br />
    <img src="files/img/homa/homa-message-sequence-diagram-3.png" alt="Homa message sequence diagram" loading="lazy" />
</p>

-   A RPC Request is shown in the image above.
-   Here, a `DATA` packet is lost and the `RESEND` packet for that missing data is lost as well, but the next `RESEND` packet makes it to the sender.
-   The sender can either immediately respond with the missing data in a `DATA` packet or if it is busy transmitting other higher priority packets, then it can send a `BUSY` packet to the receiver to prevent a timeout (like a 'keep-alive' indicator) and can send the `DATA` packet once it is free.

<p align="center">
	<br />
	<br />
    <img src="files/img/homa/homa-message-sequence-diagram-4.png" alt="Homa message sequence diagram" loading="lazy" />
</p>

-   A RPC Request is shown in the image above.
-   This scenario needs to be confirmed properly, but this is most likely how it happens.
-   If the blindly sent unscheduled `DATA` packets don't reach the receiver due to loss, overload, congestion or other reasons, then the sender times out waiting for a response from the receiver.
-   On timing out, the sender sends a `RESEND` packet to the receiver, asking for a response.
-   If the `RESEND` packet reaches the receiver, then it will respond with an `UNKNOWN` packet, because it never got the initial packets and was never aware of the RPC.
-   The sender has to re-start the communication with the receiver.

## Resources

-   [Directed Study application](files/homa/directed-study-application.pdf)
-   Presentations
    -   Homa 1 ([PDF](files/homa/presentations/homa-1.pdf), [Google Slides](https://docs.google.com/presentation/d/1uryO-L3TkBjBTeEFQAh6cAy9x4VJwpEGIUIOZRuAf5E/edit?usp=sharing))
    -   Homa 2 ([PDF](files/homa/presentations/homa-2.pdf), [Google Slides](https://docs.google.com/presentation/d/1NLEzvXmMS3w5n46XY8d2teHnPXZjphkSq9ZwmYnbkj8/edit?usp=sharing))
-   Research papers
    -   [It's Time to Replace TCP in the Datacenter (v2)](files/homa/research-papers/its-time-to-replace-tcp-in-the-datacenter-v2.pdf) ([arXiv](https://arxiv.org/abs/2210.00714v2))
    -   [Homa: A Receiver-Driven Low-Latency Transport Protocol Using Network Priorities (Complete Version)](files/homa/research-papers/homa-a-receiver-driven-low-latency-transport-protocol-using-network-priorities-complete-version.pdf) ([arXiv](https://arxiv.org/abs/1803.09615))
    -   [A Linux Kernel Implementation of the Homa Transport Protocol](files/homa/research-papers/a-linux-kernel-implementation-of-the-homa-transport-protocol.pdf) ([USENIX](https://www.usenix.org/conference/atc21/presentation/ousterhout))
    -   [Datacenter Traffic Control: Understanding Techniques and Tradeoffs](files/homa/research-papers/data-center-traffic-control-understanding-techniques-and-tradeoffs.pdf) ([IEEE Xplore](https://ieeexplore.ieee.org/abstract/document/8207422))
-   [The Homa Linux kernel module source](https://github.com/PlatformLab/HomaModule)
    -   [Homa Protocol Synopsis](https://github.com/PlatformLab/HomaModule/blob/master/protocol.md)
-   Videos
    -   [Discussing the Homa paper - Replacing TCP for the Datacenter](https://www.youtube.com/watch?v=nEFOni_87Yw)
    -   [USENIX ATC '21 - A Linux Kernel Implementation of the Homa Transport Protocol](https://www.youtube.com/watch?v=qu5WDcZRveo)
    -   [Netdev 0x16 - Keynote: It's Time to Replace TCP in the Datacenter](https://www.youtube.com/watch?v=o2HBHckrdQc)
-   Articles
    -   [Homa: A Receiver-Driven Low-Latency Transport Protocol Using Network Priorities, Part I](https://www.micahlerner.com/2021/08/15/a-linux-kernel-implementation-of-the-homa-transport-protocol.html)
    -   [A Linux Kernel Implementation of the Homa Transport Protocol, Part II](https://www.micahlerner.com/2021/08/29/a-linux-kernel-implementation-of-the-homa-transport-protocol.html)
-   [Transmission Control Protocol (TCP)](tcp.md)
-   [Remote Procedure Calls (RPCs)](http.md#rest-vs-rpc)
-   [Incast](https://www2.eecs.berkeley.edu/Pubs/TechRpts/2012/EECS-2012-40.pdf)
-   Data Plane Development Kit (DPDK)
    -   [What is DPDK?](https://www.packetcoders.io/what-is-dpdk)
    -   [dpdk.org](https://www.dpdk.org)
-   [Linux networking specifics](linux.md)
