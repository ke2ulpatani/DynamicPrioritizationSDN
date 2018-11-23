#!/usr/bin/env python
#Code to create mininet topology and run iperf commands

from parse_ip_addr import *
from parse_iperf import *
import sys

topology=sys.argv[1]
tos=sys.argv[2]


commands=["mn --topo linear,2,2","to be filled","h1s1 ip a","h2s1 ip a","h1s1 iperf -s &","h2s1 iperf -s &"]

#command to create topology
temp1=commands[0]
temp2=temp1.split()
subprocess.call(temp2)

#command to call POX controller


#command to read ip address of first server
temp1=commands[2]
temp2=temp1.split()
subprocess_output=subprocess.Popen(temp2,stdout=subprocess.PIPE)
ip_first_server=subprocess.communicate()
ip_first_server=str(ip_first_server)
ip_first_server=parse_ip_addr_output(ip_first_server)

#command to read ip address of second server
temp1=commands[3]
temp2=temp1.split()
subprocess_output=subprocess.Popen(temp2,stdout=subprocess.PIPE)
ip_second_server=subprocess.communicate()
ip_second_server=str(ip_second_server)
ip_second_server=parse_ip_addr_output(ip_second_server)

#command to run first server
temp1=commands[4]
temp2=temp1.split()
subprocess.call(temp2)

#command to run second server
temp1=commands[5]
temp2=temp1.split()
subprocess.call(temp2)

print ("output is")
print (ip_first_server)
print (ip_second_server)

#running first client
temp1="python first_client "+str(ip_first_server)+" &"
temp2=temp1.split()
subprocess.call(temp2)

#running second client
temp1="python second_client "+str(ip_second_server)+str(tos)+" &"
temp2=temp1.split()
subprocess.call(temp2)







