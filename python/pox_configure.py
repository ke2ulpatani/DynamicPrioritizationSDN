
#!/usr/bin/env python
#Code to configure pox controller

import sys
import subprocess

tos=sys.argv[1]
mac_to_be_blocked=sys.argv[2]
bandwidth=sys.argv[3]

with open("pox/pox/forwarding/mac_to_be_blocked.txt","w") as file:
        file.write(mac_to_be_blocked)
with open("pox/pox/forwarding/qos.txt","w") as file:
        file.write(tos)
temp1="ovs-vsctl -- set Port s1-eth3 qos=@newqos -- --id=@newqos create QoS type=linux-htb other-config:max-rate=1000000000 queues=0=@q0,1=@q1 -- --id=@q0 create Queue other-config:min-rate=1000000000 other-config:max-rate=1000000000 -- --id=@q1 create Queue other-config:min-rate="+str(bandwidth)+"000000 other-config:max-rate="+str(bandwidth)+"000000"
temp2=tem1.split()
subprocess.call(temp2)

temp1="./pox/pox.py log.level --DEBUG forwarding.custom_firewall"
temp2=temp1.split()
subprocess.call(temp2)








