import sys
sys.path.append('..')

from src.sim import Sim
from src import node
from src import link
from src import packet
from src.packet import Packet

from networks.network import Network

import random

class RoutingApp(object):
	def __init__(self,node,net):
		self.node = node
		self.distanceVectorTable = {}
		self.addDVToTable(node.hostname, {self.node.hostname : 0})
		self.net = net
		self.sendDVTable()

	def receive_packet(self,packet):
		print Sim.scheduler.current_time(),self.node.hostname,packet.ident
		self.updateDVTable(packet)

	def updateDVTable(self, packet):
		print "Node %s is updating its DVT, packet from: %s, packet.body: %s" % (self.node.hostname, packet.orig_host, packet.body)
		newRow = dict(packet.body)

		if packet.orig_host in self.distanceVectorTable:
			oldRow = self.distanceVectorTable[packet.orig_host]
			for key in newRow.keys():
				if key in oldRow:
					if (oldRow[key]) > (newRow[key] + 1):
						oldRow[key] = newRow[key]
						self.sendDVTable()
				else:
					oldRow[key] = newRow[key]
					self.sendDVTable()

		else:
			self.addDVToTable(packet.orig_host, newRow)
			linkToMe = self.net.get_node(packet.orig_host).get_address(self.node.hostname)
			linkToHim = self.node.get_link(packet.orig_host)
			self.node.add_forwarding_entry(linkToMe, linkToHim)
			self.sendDVTable()


	def addDVToTable(self, nodeName, distanceVector):
		print "nodeName:",nodeName
		self.distanceVectorTable[nodeName] = distanceVector
		for key in distanceVector.keys():
			if nodeName == self.node.hostname:
				self.distanceVectorTable[self.node.hostname][key] = distanceVector[key]
			else:
				self.distanceVectorTable[self.node.hostname][key] = distanceVector[key] + 1

	def sendDVTable(self):
		p = Packet(source_address=0, destination_address=0, ttl=1, protocol='dvrouting', body=self.distanceVectorTable[self.node.hostname], orig_host=self.node.hostname)
		Sim.scheduler.add(delay=0, event=p, handler=self.node.send_packet)

	def printDVTable(self):
		print "Node %s DVT: %s" % (self.node.hostname, self.distanceVectorTable)

class TestHandler(object):
	def __init__(self, node):
		self.node = node

	def receive_packet(self, packet):
		print Sim.scheduler.current_time(),packet.ident,packet.created,Sim.scheduler.current_time() - packet.created,packet.transmission_delay,packet.propagation_delay,packet.queueing_delay


if __name__ == '__main__':
	# parameters
	Sim.scheduler.reset()
	Sim.set_debug(True)

	# setup network
	net = Network('../networks/five-nodes-mesh.txt')

	# get nodes
	n1 = net.get_node('n1')
	n2 = net.get_node('n2')
	n3 = net.get_node('n3')
	n4 = net.get_node('n4')
	n5 = net.get_node('n5')

	# setup dvrouting application
	r1 = RoutingApp(n1,net)
	t1 = TestHandler(n1)
	n1.add_protocol(protocol="dvrouting",handler=r1)
	n1.add_protocol(protocol="testrouting",handler=t1)

	r2 = RoutingApp(n2,net)
	t2 = TestHandler(n2)
	n2.add_protocol(protocol="dvrouting",handler=r2)
	n2.add_protocol(protocol="testrouting",handler=t2)

	r3 = RoutingApp(n3,net)
	t3 = TestHandler(n3)
	n3.add_protocol(protocol="dvrouting",handler=r3)
	n3.add_protocol(protocol="testrouting",handler=t3)

	r4 = RoutingApp(n4,net)
	t4 = TestHandler(n4)
	n4.add_protocol(protocol="dvrouting",handler=r4)
	n4.add_protocol(protocol="testrouting",handler=t4)

	r5 = RoutingApp(n5,net)
	t5 = TestHandler(n5)
	n5.add_protocol(protocol="dvrouting",handler=r5)
	n5.add_protocol(protocol="testrouting",handler=t5)


	# Now we will send a packet from each node to each other node to test the basic routing functionality that is in place.

	# Node n1 packets
	p = packet.Packet(source_address=n1.get_address('n2'), destination_address=n2.get_address('n1'), ident=12, ttl=1, protocol='testrouting', body="n1 to n2 test packet")
	Sim.scheduler.add(delay=10, event=p, handler=n1.send_packet)
	p = packet.Packet(source_address=n1.get_address('n3'), destination_address=n3.get_address('n1'), ident=13, ttl=1, protocol='testrouting', body="n1 to n3 test packet")
	Sim.scheduler.add(delay=11, event=p, handler=n1.send_packet)
	p = packet.Packet(source_address=n1.get_address('n4'), destination_address=n4.get_address('n1'), ident=14, ttl=1, protocol='testrouting', body="n1 to n4 test packet")
	Sim.scheduler.add(delay=12, event=p, handler=n1.send_packet)
	p = packet.Packet(source_address=n1.get_address('n5'), destination_address=n5.get_address('n1'), ident=15, ttl=1, protocol='testrouting', body="n1 to n5 test packet")
	Sim.scheduler.add(delay=13, event=p, handler=n1.send_packet)

	# Node n2 packets
	p = packet.Packet(source_address=n2.get_address('n1'), destination_address=n1.get_address('n2'), ident=21, ttl=1, protocol='testrouting', body="n1 to n2 test packet")
	Sim.scheduler.add(delay=20, event=p, handler=n2.send_packet)
	p = packet.Packet(source_address=n2.get_address('n3'), destination_address=n3.get_address('n2'), ident=23, ttl=1, protocol='testrouting', body="n1 to n3 test packet")
	Sim.scheduler.add(delay=21, event=p, handler=n2.send_packet)
	p = packet.Packet(source_address=n2.get_address('n4'), destination_address=n4.get_address('n2'), ident=24, ttl=1, protocol='testrouting', body="n1 to n4 test packet")
	Sim.scheduler.add(delay=22, event=p, handler=n2.send_packet)
	p = packet.Packet(source_address=n2.get_address('n5'), destination_address=n5.get_address('n2'), ident=25, ttl=1, protocol='testrouting', body="n1 to n5 test packet")
	Sim.scheduler.add(delay=23, event=p, handler=n2.send_packet)

	# Node n3 packets
	p = packet.Packet(source_address=n3.get_address('n1'), destination_address=n1.get_address('n3'), ident=31, ttl=1, protocol='testrouting', body="n1 to n2 test packet")
	Sim.scheduler.add(delay=30, event=p, handler=n3.send_packet)
	p = packet.Packet(source_address=n3.get_address('n2'), destination_address=n2.get_address('n3'), ident=32, ttl=1, protocol='testrouting', body="n1 to n3 test packet")
	Sim.scheduler.add(delay=31, event=p, handler=n3.send_packet)
	p = packet.Packet(source_address=n3.get_address('n4'), destination_address=n4.get_address('n3'), ident=34, ttl=1, protocol='testrouting', body="n1 to n4 test packet")
	Sim.scheduler.add(delay=32, event=p, handler=n3.send_packet)
	p = packet.Packet(source_address=n3.get_address('n5'), destination_address=n5.get_address('n3'), ident=35, ttl=1, protocol='testrouting', body="n1 to n5 test packet")
	Sim.scheduler.add(delay=33, event=p, handler=n3.send_packet)

	# Node n4 packets
	p = packet.Packet(source_address=n4.get_address('n1'), destination_address=n1.get_address('n4'), ident=41, ttl=1, protocol='testrouting', body="n1 to n2 test packet")
	Sim.scheduler.add(delay=40, event=p, handler=n4.send_packet)
	p = packet.Packet(source_address=n4.get_address('n2'), destination_address=n2.get_address('n4'), ident=42, ttl=1, protocol='testrouting', body="n1 to n3 test packet")
	Sim.scheduler.add(delay=41, event=p, handler=n4.send_packet)
	p = packet.Packet(source_address=n4.get_address('n3'), destination_address=n3.get_address('n4'), ident=43, ttl=1, protocol='testrouting', body="n1 to n4 test packet")
	Sim.scheduler.add(delay=42, event=p, handler=n4.send_packet)
	p = packet.Packet(source_address=n4.get_address('n5'), destination_address=n5.get_address('n4'), ident=45, ttl=1, protocol='testrouting', body="n1 to n5 test packet")
	Sim.scheduler.add(delay=43, event=p, handler=n4.send_packet)	

	# Node n5 packets
	p = packet.Packet(source_address=n5.get_address('n1'), destination_address=n1.get_address('n5'), ident=51, ttl=1, protocol='testrouting', body="n1 to n2 test packet")
	Sim.scheduler.add(delay=50, event=p, handler=n5.send_packet)
	p = packet.Packet(source_address=n5.get_address('n2'), destination_address=n2.get_address('n5'), ident=52, ttl=1, protocol='testrouting', body="n1 to n3 test packet")
	Sim.scheduler.add(delay=51, event=p, handler=n5.send_packet)
	p = packet.Packet(source_address=n5.get_address('n3'), destination_address=n3.get_address('n5'), ident=53, ttl=1, protocol='testrouting', body="n1 to n4 test packet")
	Sim.scheduler.add(delay=52, event=p, handler=n5.send_packet)
	p = packet.Packet(source_address=n5.get_address('n4'), destination_address=n4.get_address('n5'), ident=54, ttl=1, protocol='testrouting', body="n1 to n5 test packet")
	Sim.scheduler.add(delay=53, event=p, handler=n5.send_packet)


	# run the simulation
	Sim.scheduler.run()
	r1.printDVTable()
	r2.printDVTable()
	r3.printDVTable()
	r4.printDVTable()
	r5.printDVTable()
