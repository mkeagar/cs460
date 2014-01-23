import sys
sys.path.append('../../../bene/')

from src.sim import Sim
from src import node
from src import link
from src import packet

import random

class DelayHandler(object):
    def handle_packet(self,packet):
        print Sim.scheduler.current_time(),packet.ident,packet.created,Sim.scheduler.current_time() - packet.created,packet.transmission_delay,packet.propagation_delay,packet.queueing_delay



if __name__ == '__main__':
    # parameters
    Sim.scheduler.reset()

    # setup network
    n1 = node.Node()
    n2 = node.Node()
    n3 = node.Node()
    # create link from 1 to 2
    l = link.Link(address=1,startpoint=n1,endpoint=n2,bandwidth=1000000000.0,propagation=0.1)
    n1.add_link(l)
    n1.add_forwarding_entry(address=2,link=l)
    n1.add_forwarding_entry(address=3,link=l)
    # create link from 2 to 1
    l = link.Link(address=2,startpoint=n2,endpoint=n1,bandwidth=1000000000.0,propagation=0.1)
    n2.add_link(l)
    n2.add_forwarding_entry(address=1,link=l)
    # create link from 2 to 3
    l = link.Link(address=2,startpoint=n2,endpoint=n3,bandwidth=1000000000.0,propagation=0.1)
    n2.add_link(l)
    n2.add_forwarding_entry(address=3,link=l)
    # create link from 3 to 2
    l = link.Link(address=3,startpoint=n3,endpoint=n2,bandwidth=1000000000.0,propagation=0.1)
    n3.add_link(l)
    n3.add_forwarding_entry(address=2,link=l)
    n3.add_forwarding_entry(address=1,link=l)
    
    d = DelayHandler()
    n3.add_protocol(protocol="delay",handler=d)

    # send stream of packets - 1MB file as one thousand packets of 1KB
    delay = 0.000008
    for i in range(1000):
        p = packet.Packet(destination_address=3,ident=i,protocol='delay',length=1000)
        Sim.scheduler.add(delay=delay*i, event=p, handler=n1.handle_packet)

    # run the simulation
    Sim.scheduler.run()
