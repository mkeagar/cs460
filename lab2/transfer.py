import sys
sys.path.append('..')

from src.sim import Sim
from src.node import Node
from src.link import Link
from src.transport import Transport
from lab2.my_rtp import My_RTP

import optparse
import os
import subprocess

class AppHandler(object):
    def __init__(self,filename):
        self.filename = filename
        self.directory = 'received'
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)
        self.f = open("%s/%s" % (self.directory,self.filename),'w')

    def handle_packet(self,packet):
        Sim.trace("application got packet with %d bytes" % (packet.length))
        self.f.write(packet.body)
        self.f.flush()

class Main(object):
    def __init__(self):
        self.directory = 'received'
        self.parse_options()
        self.run()
        self.diff()

    def parse_options(self):
        parser = optparse.OptionParser(usage = "%prog [options]",
                                       version = "%prog 0.1")

        parser.add_option("-f","--filename",type="str",dest="filename",
                          default='test.txt',
                          help="filename to send")

        parser.add_option("-l","--loss",type="float",dest="loss",
                          default=0.0,
                          help="random loss rate")

        (options,args) = parser.parse_args()
        self.filename = options.filename
        self.loss = options.loss

    def diff(self):
        args = ['diff','-u',self.filename,self.directory+'/'+self.filename]
        result = subprocess.Popen(args,stdout = subprocess.PIPE).communicate()[0]
        print
        if not result:
            print "File transfer correct!"
        else:
            print "File transfer failed. Here is the diff:"
            print
            print result

    def run(self):
        # parameters
        Sim.scheduler.reset()
        Sim.set_debug(True)

        # setup network
        n1 = Node()
        n2 = Node()
        l = Link(address=1,startpoint=n1,endpoint=n2,bandwidth=10000000,propagation=0.01,loss=self.loss)
        n1.add_link(l)
        n1.add_forwarding_entry(address=2,link=l)
        l = Link(address=2,startpoint=n2,endpoint=n1,bandwidth=10000000,propagation=0.01,loss=self.loss)
        n2.add_link(l)
        n2.add_forwarding_entry(address=1,link=l)

        # setup transport
        t1 = Transport(n1)
        t2 = Transport(n2)

        # setup application
        a = AppHandler(self.filename)

        # setup connection
        c1 = My_RTP(t1,1,1,2,1,a)
        c2 = My_RTP(t2,2,1,1,1,a)

        # send a file
        with open(self.filename,'r') as f:
            while True:
                data = f.read(1000)
                if not data:
                    break
                c1.load_buffer(data)
                # Sim.scheduler.add(delay=0, event=data, handler=c1.send)

        c1.window_init()

        # run the simulation
        Sim.scheduler.run()

if __name__ == '__main__':
    m = Main()