import sys
sys.path.append('..')

from src.sim import Sim
from src.node import Node
from src.link import Link
from src.transport import Transport
from lab3.my_rtp import My_RTP

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

		parser.add_option("-q","--queue_size",type="int",dest="queue_size",
						  default=None,
						  help="the size of the queue for the network link")

		(options,args) = parser.parse_args()
		self.filename = options.filename
		self.loss = options.loss
		self.queue_size = options.queue_size

	def diff(self):
		args = ['diff','-u',self.filename,self.directory+'/5_1-'+self.filename]
		result = subprocess.Popen(args,stdout = subprocess.PIPE).communicate()[0]
		print
		if not result:
			print "File transfer 1 correct!"
		else:
			print "File transfer 1 failed. Here is the diff:"
			print
			print result

		args = ['diff','-u',self.filename,self.directory+'/5_2-'+self.filename]
		result = subprocess.Popen(args,stdout = subprocess.PIPE).communicate()[0]
		print
		if not result:
			print "File transfer 2 correct!"
		else:
			print "File transfer 2 failed. Here is the diff:"
			print
			print result

		args = ['diff','-u',self.filename,self.directory+'/5_3-'+self.filename]
		result = subprocess.Popen(args,stdout = subprocess.PIPE).communicate()[0]
		print
		if not result:
			print "File transfer 3 correct!"
		else:
			print "File transfer 3 failed. Here is the diff:"
			print
			print result

		args = ['diff','-u',self.filename,self.directory+'/5_4-'+self.filename]
		result = subprocess.Popen(args,stdout = subprocess.PIPE).communicate()[0]
		print
		if not result:
			print "File transfer 4 correct!"
		else:
			print "File transfer 4 failed. Here is the diff:"
			print
			print result

		args = ['diff','-u',self.filename,self.directory+'/5_5-'+self.filename]
		result = subprocess.Popen(args,stdout = subprocess.PIPE).communicate()[0]
		print
		if not result:
			print "File transfer 5 correct!"
		else:
			print "File transfer 5 failed. Here is the diff:"
			print
			print result

	def run(self):
		# parameters
		Sim.scheduler.reset()
		Sim.set_debug(True)

		# setup network
		n1 = Node()
		n2 = Node()
		l = Link(address=1,startpoint=n1,endpoint=n2,queue_size=self.queue_size,bandwidth=10000000,propagation=0.01,loss=self.loss, printOut=True)
		n1.add_link(l)
		n1.add_forwarding_entry(address=2,link=l)
		l = Link(address=2,startpoint=n2,endpoint=n1,queue_size=self.queue_size,bandwidth=10000000,propagation=0.01,loss=self.loss)
		n2.add_link(l)
		n2.add_forwarding_entry(address=1,link=l)

		# setup transport
		t1 = Transport(n1)
		t2 = Transport(n2)

		# setup application 1
		a = AppHandler("5_1-" + self.filename)

		# setup connection
		c1 = My_RTP(t1,1,1,2,1,a)
		c2 = My_RTP(t2,2,1,1,1,a)

		# setup application 2
		a = AppHandler("5_2-" + self.filename)

		# setup connection
		c3 = My_RTP(t1,1,2,2,2,a)
		c4 = My_RTP(t2,2,2,1,2,a)

		# setup application 3
		a = AppHandler("5_3-" + self.filename)

		# setup connection
		c5 = My_RTP(t1,1,3,2,3,a)
		c6 = My_RTP(t2,2,3,1,3,a)

		# setup application 4
		a = AppHandler("5_4-" + self.filename)

		# setup connection
		c7 = My_RTP(t1,1,4,2,4,a)
		c8 = My_RTP(t2,2,4,1,4,a)

		# setup application 5
		a = AppHandler("5_5-" + self.filename)

		# setup connection
		c9 = My_RTP(t1,1,5,2,5,a)
		c10 = My_RTP(t2,2,5,1,5,a)

		# send a file
		with open(self.filename,'r') as f:
			while True:
				data = f.read(1000)
				if not data:
					break
				c1.load_buffer(data)
				c3.load_buffer(data)
				c5.load_buffer(data)
				c7.load_buffer(data)
				c9.load_buffer(data)

		c1.set_file_prefix("5_1")
		c2.set_file_prefix("5_1")
		c3.set_file_prefix("5_2")
		c4.set_file_prefix("5_2")
		c5.set_file_prefix("5_3")
		c6.set_file_prefix("5_3")
		c7.set_file_prefix("5_4")
		c8.set_file_prefix("5_4")
		c9.set_file_prefix("5_5")
		c10.set_file_prefix("5_5")


		c1.open_window_file()
		c3.open_window_file()
		c5.open_window_file()
		c7.open_window_file()
		c9.open_window_file()

		Sim.scheduler.add(delay=0, event="window_init", handler=c1.window_init)
		Sim.scheduler.add(delay=0.1, event="window_init", handler=c3.window_init)
		Sim.scheduler.add(delay=0.2, event="window_init", handler=c5.window_init)
		Sim.scheduler.add(delay=0.3, event="window_init", handler=c7.window_init)
		Sim.scheduler.add(delay=0.4, event="window_init", handler=c9.window_init)

		# run the simulation
		Sim.scheduler.run()
		n1.links[0].myfile.close()
		c1.close_window_file()
		c3.close_window_file()
		c5.close_window_file()
		c7.close_window_file()
		c9.close_window_file()

		Sim.close_rate_file()

if __name__ == '__main__':
	m = Main()
