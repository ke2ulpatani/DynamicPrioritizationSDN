#!/usr/bin/env python
#Code to parse ip addr output
import re

def parse_ip_addr_output(input_string):
	ip_address=""
	#Type your code here

	ip = r'(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})'
	found_ip = re.findall( ip,text )	
	ip_address = found_ip[1]

	return (ip_address)




