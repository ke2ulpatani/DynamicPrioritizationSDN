
from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.util import dpid_to_str
from pox.lib.util import str_to_bool
import time

from pox.lib.addresses import EthAddr

log = core.getLogger()

_flood_delay = 0


#Code to have mac address blocking as well as for service prioritization
y = ""
class LearningSwitch (object):
  
  def __init__ (self, connection, transparent):
    with open("/home/mininet/pox/pox/forwarding/mac_to_be_blocked.txt") as file:
      x=file.read()
    log.debug("mac added to firewall is %s",x)
    with open("/home/mininet/pox/pox/forwarding/qos.txt") as file:
      y=file.read()
    log.debug("port added to queue is %s and type of y is %s",y,type(y))
    y=y.strip()
    y=int(y)
    log.debug("port added to queue is %s and type of y is %s",y,type(y))
    self.connection = connection
    self.transparent = transparent
    self.macToPort = {}
    self.firewall = {}
    self.mac_to_be_blocked('00-00-00-00-00-01',EthAddr(x))
    self.mac_to_be_blocked('00-00-00-00-00-02',EthAddr(x))
    connection.addListeners(self)
    self.hold_down_expired = _flood_delay == 0

  def CheckBlockList (self, dpidstr, src=0):
    try:
      entry = self.firewall[(dpidstr, src)]
      
      if (entry == True):
        log.debug("Rule (%s) found in %s: FORWARD",
                  src, dpidstr)
      else:
        log.debug("Rule (%s) found in blocked mac list %s",
                  src, dpidstr)
      return entry
    except KeyError:
      log.debug("Rule (%s) NOT found in blocked mac list%s: FORWARD",
                src, dpidstr)
      return True

  def mac_to_be_blocked (self, dpidstr, src=0):
    self.firewall[(dpidstr,src)]=False
  
  def _handle_PacketIn (self, event):
    packet = event.parsed

    def flood (message = None):
      msg = of.ofp_packet_out()
      if time.time() - self.connection.connect_time >= _flood_delay:

        if self.hold_down_expired is False:
          self.hold_down_expired = True
          log.info("%s: Flood hold-down expired -- flooding",
              dpid_to_str(event.dpid))

        if message is not None: log.debug(message)
        msg.actions.append(of.ofp_action_output(port = of.OFPP_FLOOD))
      else:
        pass
      msg.data = event.ofp
      msg.in_port = event.port
      self.connection.send(msg)

    def drop (duration = None):
      if duration is not None:
        if not isinstance(duration, tuple):
          duration = (duration,duration)
        msg = of.ofp_flow_mod()
        msg.match = of.ofp_match.from_packet(packet)
        msg.idle_timeout = duration[0]
        msg.hard_timeout = duration[1]
        msg.buffer_id = event.ofp.buffer_id
        self.connection.send(msg)
      elif event.ofp.buffer_id is not None:
        msg = of.ofp_packet_out()
        msg.buffer_id = event.ofp.buffer_id
        msg.in_port = event.port
        self.connection.send(msg)

    self.macToPort[packet.src] = event.port # 1


    dpidstr = dpid_to_str(event.connection.dpid)

    if self.CheckBlockList(dpidstr, packet.src) == False:
      drop()
      return

    if not self.transparent:
      if packet.type == packet.LLDP_TYPE or packet.dst.isBridgeFiltered():
        drop()
        return

    if packet.dst.is_multicast:
      flood()
    else:
      if packet.dst not in self.macToPort: # 4
        flood("Port for %s unknown -- flooding" % (packet.dst,)) # 4a
      else:
        port = self.macToPort[packet.dst]
        if port == event.port:
          log.warning("Same port for packet from %s -> %s on %s.%s.  Drop."
              % (packet.src, packet.dst, dpid_to_str(event.dpid), port))
          drop(10)
          return
        log.debug("installing flow for %s.%i -> %s.%i" %
                  (packet.src, event.port, packet.dst, port))
        msg = of.ofp_flow_mod()
        msg.match = of.ofp_match.from_packet(packet, event.port)
        msg.idle_timeout = 10
        msg.hard_timeout = 30
	log.debug("type of msg.match.tp_src is %s and value is %s",type(msg.match.tp_src),msg.match.tp_src)
	#log.debug("port added to queue is %s and type of y is %s",y,type(y))
	with open("/home/mininet/pox/pox/forwarding/qos.txt") as file:
	  y=file.read()
	log.debug("port added to queue is %s and type of y is %s",y,type(y))
	y=y.strip()
	y=int(y)
	log.debug("port added to queue is %s and type of y is %s",y,type(y))
	if msg.match.tp_src == y or msg.match.tp_dst == y:
	  log.debug("msg sent to special queue")
          msg.actions.append(of.ofp_action_enqueue(port = port,queue_id=1))
        #elif msg.match.tp_src == 5003 or msg.match.tp_dst == 5003:
          #msg.actions.append(of.ofp_action_enqueue(port = port,queue_id=2))
        else:
          msg.actions.append(of.ofp_action_output(port = port))
        msg.data = event.ofp # 6a
        self.connection.send(msg)

class l2_learning (object):
  def __init__ (self, transparent):
    core.openflow.addListeners(self)
    self.transparent = transparent

  def _handle_ConnectionUp (self, event):
    log.debug("Connection %s" % (event.connection,))
    LearningSwitch(event.connection, self.transparent)

def launch (transparent=False, hold_down=_flood_delay):
  try:
    global _flood_delay
    _flood_delay = int(str(hold_down), 10)
    assert _flood_delay >= 0
  except:
    raise RuntimeError("Expected hold-down to be a number")

  core.registerNew(l2_learning, str_to_bool(transparent))
