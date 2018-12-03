#!/usr/bin/python

from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.util import dpidToStr
log = core.getLogger()

def _handle_ConnectionUp (event):
	msg = of.ofp_flow_mod()
	packet = event.parsed

	tos = packet.nw_tos

	




	ipv4_packet = packet.find("ipv4")

	#Message to the switch
	msg_out = of.ofp_packet_out()
	if packet.type == ethernet.IP_TYPE: 
		msg_out = packet_in.in_port
		msg_out.match = of.ofp_match.from_packet(packet)
		if ipv4_packet.tos == 1:
			action = of.ofp_action_output(port = )
		else:
			action = of.of


	msg.action.append(action)
	self.connection.send(msg)

def launch ():
  core.openflow.addListenerByName("PriorityModule", _handle_ConnectionUp)
  log.info("Priority Module is running")
