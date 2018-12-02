#!/usr/bin/env python
#Code to ssh into mininet VM and execute bash script

#USAGE - sudo python ssh_to_mininet.py <type of service tag> <topology type>

import sys
import paramiko
import time

topology=sys.argv[1]

tos = sys.argv[2]
mac_to_be_blocked=sys.argv[3]
bandwidth=sys.argv[4]

def to_mininet(ip_address,topology,tos,mac_to_be_blocked):
	
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh.connect(ip_address,username='mininet', password='mininet', port=22)
	command1="python /home/mininet/pox_configure.py "+str(tos)+" "+str(mac_to_be_blocked)+" "+str(bandwidth)
	#command1="ip addr"
	stdin, stdout, stderr = ssh.exec_command(command1)
	stdout.channel.recv_exit_status()
	ssh.close()
	command_1_output = stdout.read().replace('\n',' ')
	command_1_output=command_1_output.replace('\r','')
	command_1_output=command_1_output.lower()
	print command_1_output
	print ("\n\n\n")
	time.sleep(8)
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh.connect(ip_address,username='mininet', password='mininet', port=22)
	#command2="cat iperf_results"
	command2="ip route"
	stdin, stdout, stderr = ssh.exec_command(command2)
	stdout.channel.recv_exit_status()
	ssh.close()
	command_2_output = stdout.read().replace('\n',' ')
	command_2_output=command_2_output.replace('\r','')
	command_2_output=command_2_output.lower()
	print command_2_output

#----------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------


#THIS IS THE MAIN FUNCTION
#THE NEXT LINE NEEDS TO BE UPDATED WITH THE IP ADDRESS OF MININET
mininet_ip = "10.152.44.102"

to_mininet(mininet_ip,topology,tos,mac_to_be_blocked)
