from scapy.all import *

packet=IP(dst='192.168.56.102')/ICMP()/Raw(load=RandString(56))

answer=sr1(packet, timeout=1)

answer.show
