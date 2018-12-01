#!/usr/bin/env python
#Code to configure pox controller

from parse_ip_addr import *
from parse_iperf import *
import sys

tos_to_prioritize=sys.argv[1]
mac_to_be_blocked=sys.argv[2]

with open("/home/mininet/pox/pox/misc/mac_to_be_blocked.txt","w") as file:
	file.write(mac_to_be_blocked)

temp1="./home/mininet/pox/pox.py log.level --DEBUG misc.custom_firewall"
temp2=temp1.split()
subprocess.call(temp2))






