# Linux

## Table of Contents

-   [Introduction](#introduction)
-   [Packet Processing](#packet-processing)
-   [Packet Handling](#packet-handling)
-   [Traffic Control](#traffic-control)
-   [NAPI](#napi)
-   [Miscellaneous](#miscellaneous)

## Introduction

A collection of Linux internals, mostly geared towards Computer Networking.

> [C programming resources](https://dev.harshkapadia.me/resources#c)

## Packet Processing

-   [Queueing in the Linux Network Stack](https://www.coverfire.com/articles/queueing-in-the-linux-network-stack)
-   [Kernel-bypass techniques for high-speed network packet processing](https://www.youtube.com/watch?v=MpjlWt7fvrw)
-   [Illustrated Guide to Monitoring and Tuning the Linux Networking Stack: Receiving Data](https://blog.packagecloud.io/illustrated-guide-monitoring-tuning-linux-networking-stack-receiving-data)
-   [How Linux processes your network packet](https://www.youtube.com/watch?v=3Ij0aZRsw9w)
-   [SYN packet handling in the wild](https://blog.cloudflare.com/syn-packet-handling-in-the-wild)
-   [Listening to Networks](https://www.youtube.com/watch?v=NGOD8VdyevM)
-   [The Network Packet's Diary: A Kernel Journey](https://www.youtube.com/watch?v=T5TvPRQFNoM)
-   [Path of a Packet in the Linux Kernel Stack](https://www.cs.dartmouth.edu/~sergey/netreads/path-of-packet/Network_stack.pdf)
-   [New API (NAPI)](#napi)

## Packet Handling

-   Socket
    -   [socket(7)](https://man7.org/linux/man-pages/man7/socket.7.html) describes the Linux networking socket layer user interface and [socket(2)](https://man7.org/linux/man-pages/man2/socket.2.html) creates an endpoint for communication and returns a file descriptor that refers to that endpoint.
        -   What the numbers `2` and `7` mean: [The Linux man-pages project (check 'intro' pages)](https://man7.org/linux/man-pages/index.html)
    -   [Socket/Address family (`AF_INET`, `AF_INET6`, etc.)](https://man7.org/linux/man-pages/man7/address_families.7.html)
    -   [Socket type (`SOCK_STREAM`, `SOCK_DGRAM`, etc.)](https://man7.org/linux/man-pages/man2/socket.2.html#:~:text=Currently%20defined%20types%20are%3A)
-   [bind(2)](https://man7.org/linux/man-pages/man2/bind.2.html)
-   [recvmsg(2)](https://www.man7.org/linux/man-pages/man2/recvmsg.2.html)
    -   System calls: [syscalls(2)](https://man7.org/linux/man-pages/man2/syscalls.2.html)
-   [sysctl(8)](https://www.man7.org/linux/man-pages/man8/sysctl.8.html) system administration command to configure kernel parameters at runtime.
    -   [Linux `sysctl` command](https://linuxize.com/post/sysctl-command-in-linux)

## Traffic Control

-   [tc(8)](https://man7.org/linux/man-pages/man8/tc.8.html) stands for 'Traffic Control' and it shows and manipulates traffic control settings.
    -   [Traffic Control HOWTO](https://tldp.org/HOWTO/html_single/Traffic-Control-HOWTO)

## NAPI

-   NAPI: New Application Programming Interface
-   NAPI is a part of the packet processing framework of Linux and provides interrupt mitigation and packet throttling to improve the performance of high-speed networking.
-   [New API (NAPI)](https://wiki.linuxfoundation.org/networking/napi)
-   [What are the advantages NAPI before the IRQ Coalesce?](https://stackoverflow.com/questions/28090086/what-are-the-advantages-napi-before-the-irq-coalesce)

## Miscellaneous

-   [Linux networking references](https://linux-kernel-labs.github.io/refs/heads/master/labs/networking.html#further-reading)
-   [Scaling in the Linux Networking Stack](https://docs.kernel.org/networking/scaling.html) (RSS, RPS, RFS, etc.)
-   [Networking in a Linux Container in Docker](https://harshkapadia2.github.io/docker/linux-networking)
