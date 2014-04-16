import optparse
import sys

import matplotlib
from pylab import *

# Parses a file of rates and plot a sequence number graph. Black
# squares indicate a sequence number being sent and dots indicate a
# sequence number being ACKed.
class Plotter:
	def __init__(self,input_file, output_file):
		""" Initialize plotter with a file name. """
		self.input_file = input_file
		self.output_file = output_file
		self.data1 = []
		self.data2 = []
		self.data3 = []
		self.data4 = []
		self.data5 = []
		self.ack1 = []
		self.ack2 = []
		self.ack3 = []
		self.ack4 = []
		self.ack5 = []
		self.min_time = None
		self.max_time = None

	def parse(self):
		""" Parse the data file """
		first = None
		f = open(self.input_file)
		for line in f.readlines():
			if line.startswith("#"):
				continue
			try:
				flow,t,sequence,size = line.split()
			except:
				continue
			flow = int(flow)
			t = float(t)
			sequence = int(sequence)
			if size != "x":
				size = int(size)
			if size == 0:
				if flow == 1:
					self.ack1.append((t, sequence))
				elif flow == 2:
					self.ack2.append((t, sequence))
				elif flow == 3:
					self.ack3.append((t, sequence))
				elif flow == 4:
					self.ack4.append((t, sequence))
				elif flow == 5:
					self.ack5.append((t, sequence))
				else:
					print "Erroneous data:", flow, t, sequence, size
			else:
				if flow == 1:
					self.data1.append((t,sequence,size))
				elif flow == 2:
					self.data2.append((t,sequence,size))
				elif flow == 3:
					self.data3.append((t,sequence,size))
				elif flow == 4:
					self.data4.append((t, sequence, size))
				elif flow == 5:
					self.data5.append((t, sequence, size))
				else:
					print "Erroneous data:", flow, t, sequence, size

			if not self.min_time or t < self.min_time:
				self.min_time = t
			if not self.max_time or t > self.max_time:
				self.max_time = t

	def plot(self):
		""" Create a sequence graph of the packets. """
		clf()
		figure(figsize=(15,5))

		# Plot graph for flow 1
		x = []
		y = []
		dropX = []
		dropY = []
		ackX = []
		ackY = []
		for (t,sequence,size) in self.data1:
			if size == "x":
				dropX.append(t)
				dropY.append(sequence % (1000 * 50))
			else:
				x.append(t)
				y.append(sequence % (1000*50))

		# Collect actual ack data
		for (t, sequence) in self.ack1:
			ackX.append(t)
			ackY.append(sequence % (1000 * 50))

		scatter(x,y,marker='s',s=3, color='blue')
		scatter(dropX,dropY,marker='x', color='blue')
		scatter(ackX,ackY,marker='s',s=0.2, color='blue')

		# Plot graph for flow 2
		x = []
		y = []
		dropX = []
		dropY = []
		ackX = []
		ackY = []
		for (t,sequence,size) in self.data2:
			if size == "x":
				dropX.append(t)
				dropY.append(sequence % (1000 * 50))
			else:
				x.append(t)
				y.append(sequence % (1000*50))

		# Collect actual ack data
		for (t, sequence) in self.ack2:
			ackX.append(t)
			ackY.append(sequence % (1000 * 50))
		
		scatter(x,y,marker='s',s=3, color='red')
		scatter(dropX,dropY,marker='x', color='red')
		scatter(ackX,ackY,marker='s',s=0.2, color='red')

		# Plot graph for flow 3
		x = []
		y = []
		dropX = []
		dropY = []
		ackX = []
		ackY = []
		for (t,sequence,size) in self.data3:
			if size == "x":
				dropX.append(t)
				dropY.append(sequence % (1000 * 50))
			else:
				x.append(t)
				y.append(sequence % (1000*50))

		# Collect actual ack data
		for (t, sequence) in self.ack3:
			ackX.append(t)
			ackY.append(sequence % (1000 * 50))

		scatter(x,y,marker='s',s=3, color='green')
		scatter(dropX,dropY,marker='x', color='green')
		scatter(ackX,ackY,marker='s',s=0.2, color='green')

		# Plot graph for flow 4
		x = []
		y = []
		dropX = []
		dropY = []
		ackX = []
		ackY = []
		for (t,sequence,size) in self.data4:
			if size == "x":
				dropX.append(t)
				dropY.append(sequence % (1000 * 50))
			else:
				x.append(t)
				y.append(sequence % (1000*50))

		# Collect actual ack data
		for (t, sequence) in self.ack4:
			ackX.append(t)
			ackY.append(sequence % (1000 * 50))

		scatter(x,y,marker='s',s=3, color='orange')
		scatter(dropX,dropY,marker='x', color='orange')
		scatter(ackX,ackY,marker='s',s=0.2, color='orange')

		# Plot graph for flow 5
		x = []
		y = []
		dropX = []
		dropY = []
		ackX = []
		ackY = []
		for (t,sequence,size) in self.data5:
			if size == "x":
				dropX.append(t)
				dropY.append(sequence % (1000 * 50))
			else:
				x.append(t)
				y.append(sequence % (1000*50))

		# Collect actual ack data
		for (t, sequence) in self.ack5:
			ackX.append(t)
			ackY.append(sequence % (1000 * 50))

		scatter(x,y,marker='s',s=3, color='purple')
		scatter(dropX,dropY,marker='x', color='purple')
		scatter(ackX,ackY,marker='s',s=0.2, color='purple')

		xlabel('Time (seconds)')
		ylabel('Sequence Number Mod 1500')
		xlim([-0.001,self.max_time + 0.01])
		# xlim([-0.001,2])
		ylim([-1000, 60000])
		savefig(self.output_file + '.png')

def parse_options():
		# parse options
		parser = optparse.OptionParser(usage = "%prog [options]",
									   version = "%prog 0.1")

		parser.add_option("-f","--input_file",type="string",dest="input_file",
						  default=None,
						  help="input_file")

		parser.add_option("-o","--output_file",type="string",dest="output_file",
						default="sequence",
						help="output_file")

		(options,args) = parser.parse_args()
		return (options,args)


if __name__ == '__main__':
	(options,args) = parse_options()
	if options.input_file == None:
		print "plot.py -f input_file [-o output_file_name]"
		sys.exit()
	p = Plotter(options.input_file, options.output_file)
	p.parse()
	p.plot()
