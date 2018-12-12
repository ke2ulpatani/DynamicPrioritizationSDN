#!/usr/bin/python
#usage: sudo python test_new.py <linear> or <tree>
import os

from mininet.topo import Topo

from mininet.net import Mininet

from mininet.util import dumpNodeConnections

from mininet.node import *

from mininet.log import setLogLevel

import sys

topology=sys.argv[1]

class FirstTopo( Topo ):
	"Simple topology example."
 	def __init__( self ):
 		"Create custom topo."
 # Initialize topology
 		Topo.__init__( self )
 # Add hosts and switches
		h1 = self.addHost( 'h1', mac = '00:00:00:00:00:01' )
 		h2 = self.addHost( 'h2', mac = '00:00:00:00:00:02' )
 		h3 = self.addHost( 'h3', mac = '00:00:00:00:00:03' )
 		h4 = self.addHost( 'h4', mac = '00:00:00:00:00:04' )
 		h5 = self.addHost( 'h5', mac = '00:00:00:00:00:05' )
		h6 = self.addHost( 'h6', mac = '00:00:00:00:00:06' )
		
		leftSwitch = self.addSwitch( 's1' )
 		rightSwitch = self.addSwitch( 's2' )
 # Add links
 		self.addLink( h1, leftSwitch )
 		self.addLink( h2, leftSwitch )
 		self.addLink( leftSwitch, rightSwitch )
 		self.addLink( leftSwitch, h3 )
 		self.addLink( rightSwitch, h4 )
 		self.addLink( rightSwitch, h5 )
 		self.addLink( rightSwitch, h6 )

class SecondTopo( Topo ):
        "Simple topology example."
        def __init__( self ):
                "Create custom topo."
 # Initialize topology
                Topo.__init__( self )
 # Add hosts and switches
                h1 = self.addHost( 'h1', mac = '00:00:00:00:00:01' )
                h2 = self.addHost( 'h2', mac = '00:00:00:00:00:02' )
                h3 = self.addHost( 'h3', mac = '00:00:00:00:00:03' )
                h4 = self.addHost( 'h4', mac = '00:00:00:00:00:04' )
                h5 = self.addHost( 'h5', mac = '00:00:00:00:00:05' )
                h6 = self.addHost( 'h6', mac = '00:00:00:00:00:06' )
		
                topSwitch = self.addSwitch( 't1' )
                lowSwitch1 = self.addSwitch( 'l1' )
		lowSwitch2 = self.addSwitch( 'l2' )
		lowSwitch3 = self.addSwitch( 'l3' )
 # Add links
                self.addLink( topSwitch, lowSwitch1 )
 		self.addLink( topSwitch, lowSwitch2 )
 		self.addLink( topSwitch, lowSwitch3 )
		self.addLink( lowSwitch1, h1 )
                self.addLink( lowSwitch1, h2 )
		self.addLink( lowSwitch2, h3 )
		self.addLink( lowSwitch2, h4 )
 		self.addLink( lowSwitch3, h5 )
 		self.addLink( lowSwitch3, h6 )

class POXBridge( Controller ):
	def start( self ):
		"Start POX learning switch"
		self.pox = '%s/pox/pox.py' %os.environ[ 'HOME' ]
		self.cmd( self.pox, 'forwarding.l2_learning &' )
	def stop( self ):
		"Stop POX"
		self.cmd( 'kill%' + self.pox )

controllers = { 'poxbridge': POXBridge }


def runExperiment():
	if topology == 'linear':
		topo = FirstTopo()
	elif topology == 'tree':
		topo = SecondTopo()
	
	"Create and test a simple experiment"

	net = Mininet(topo = topo, controller = lambda a: RemoteController(a,ip = "127.0.0.1", port = 6633), autoStaticArp = True)
	net.start()
	print "Dumping host connections"
	dumpNodeConnections(net.hosts)
	print "Testing network connectivity"
	net.pingAll()
	net.stop()

if __name__ == '__main__':
 # Tell mininet to print useful information
 	setLogLevel('info')
 	runExperiment()
