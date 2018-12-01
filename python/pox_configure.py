
#!/usr/bin/env python
#Code to configure pox controller

import sys
import subprocess

tos_to_prioritize=sys.argv[1]
mac_to_be_blocked=sys.argv[2]

with open("pox/pox/forwarding/mac_to_be_blocked.txt","w") as file:
        file.write(mac_to_be_blocked)

temp1="./pox/pox.py log.level --DEBUG forwarding.custom_firewall"
temp2=temp1.split()
subprocess.call(temp2)








