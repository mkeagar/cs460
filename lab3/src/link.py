from sim import Sim

import random

class Link(object):
    def __init__(self,address=0,startpoint=None,endpoint=None,queue_size=None,
                 bandwidth=1000000.0,propagation=0.001,loss=0.0, printOut=False):
        self.address = address
        self.startpoint = startpoint
        self.endpoint = endpoint
        self.queue_size = queue_size
        self.bandwidth = bandwidth
        self.propagation = propagation
        self.loss = loss
        self.busy = False
        self.queue = []
        self.printOut = printOut
        if self.printOut:
            self.myfile = open("queue_data.txt", 'w')

    ## Handling packets ##

    def handle_packet(self,packet):
        # drop packet due to queue overflow
        if self.queue_size and len(self.queue) == self.queue_size:
            Sim.trace("%d dropped packet due to queue overflow" % (self.address))
            if self.printOut:
                self.myfile.write(str(Sim.scheduler.current_time()) + " x\n")
                Sim.print_packet_loss(packet)
            return
        # drop packet due to random loss
        if self.loss > 0 and random.random() < self.loss:
            Sim.trace("%d dropped packet due to random loss" % (self.address))
            if self.printOut:
                self.myfile.write(str(Sim.scheduler.current_time()) + " x\n")
            return
        packet.enter_queue = Sim.scheduler.current_time()
        if len(self.queue) == 0 and not self.busy:
            # packet can be sent immediately
            self.busy = True
            self.transmit(packet)
        else:
            # add packet to queue
            self.queue.append(packet)
        
    def transmit(self,packet):
        if self.printOut:
            self.myfile.write(str(Sim.scheduler.current_time()) + " " + str(len(self.queue)) + "\n")
        packet.queueing_delay += Sim.scheduler.current_time() - packet.enter_queue
        delay = (8.0*packet.length)/self.bandwidth
        packet.transmission_delay += delay
        packet.propagation_delay += self.propagation
        # schedule packet arrival at end of link
        Sim.scheduler.add(delay=delay+self.propagation,event=packet,handler=self.endpoint.handle_packet)
        # schedule next transmission
        Sim.scheduler.add(delay=delay,event='finish',handler=self.next)

    def next(self,event):
        if len(self.queue) > 0:
            packet = self.queue.pop(0)
            self.transmit(packet)
        else:
            self.busy = False
