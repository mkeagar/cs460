import optparse
import sys

import matplotlib
from pylab import *

# Parse a file of rates and plot a smoothed graph. The rate is smoothed
# by summing all the bytes sent over a 1 second interval, and sliding
# the window every 0.1 seconds.
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
			# append data to a list of tuples
			flow = int(flow)
			t = float(t)
			sequence = int(sequence)
			if size == "x":
				continue
			size = int(size)
			if not size == 0:
				if flow == 1:
					self.data1.append((t,sequence,size))
				elif flow == 2:
					self.data2.append((t,sequence,size))
				elif flow == 3:
					self.data3.append((t, sequence, size))
				elif flow == 4:
					self.data4.append((t, sequence, size))
				elif flow == 5:
					self.data5.append((t, sequence, size))
				else:
					print "Erroneous data: ",flow, t, sequence, size
			# Keep track of the minimum and maximum time seen
			if not self.min_time or t < self.min_time:
				self.min_time = t
			if not self.max_time or t > self.max_time:
				self.max_time = t

			# print len(self.data1),len(self.data2),len(self.data3),len(self.data4),len(self.data5)

	def plot(self):
		""" Create a line graph of the rate over time for flow 1 and 2. """
		clf()

		# Plot rate for flow 1
		x = []
		y = []
		i = 0
		maxY = None
		while i < self.max_time:
			bytes = 0
			# loop through array of data and find relevant data
			for (t,sequence,size) in self.data1:
				if (t >= i - 1) and (t <= i):
					bytes += size
			# compute interval
			left = i - 1
			if i - 1 < 0:
				left = 0
			right = i
			# add data point
			if (right - left) != 0:
				rate = (bytes*8.0/1000000)/(right-left)
				x.append(i)
				y.append(rate)
				if not maxY or rate > maxY:
					maxY = int(rate) + 1
			i += 0.1
		
		plot(x,y)

		# Plot rate for flow 2
		x = []
		y = []
		i = 0
		while i < self.max_time:
			bytes = 0
			# loop through array of data and find relevant data
			for (t,sequence,size) in self.data2:
				if (t >= i - 1) and (t <= i):
					bytes += size
			# compute interval
			left = i - 1
			if i - 1 < 0:
				left = 0
			right = i
			# add data point
			if (right - left) != 0:
				rate = (bytes*8.0/1000000)/(right-left)
				x.append(i)
				y.append(rate)
				if not maxY or rate > maxY:
					maxY = int(rate) + 1
			i += 0.1
		
		plot(x,y)

		# Plot rate for flow 3
		x = []
		y = []
		i = 0
		while i < self.max_time:
			bytes = 0
			# loop through array of data and find relevant data
			for (t,sequence,size) in self.data3:
				if (t >= i - 1) and (t <= i):
					bytes += size
			# compute interval
			left = i - 1
			if i - 1 < 0:
				left = 0
			right = i
			# add data point
			if (right - left) != 0:
				rate = (bytes*8.0/1000000)/(right-left)
				x.append(i)
				y.append(rate)
				if not maxY or rate > maxY:
					maxY = int(rate) + 1
			i += 0.1
		
		plot(x,y)

		# Plot rate for flow 4
		x = []
		y = []
		i = 0
		while i < self.max_time:
			bytes = 0
			# loop through array of data and find relevant data
			for (t,sequence,size) in self.data4:
				if (t >= i - 1) and (t <= i):
					bytes += size
			# compute interval
			left = i - 1
			if i - 1 < 0:
				left = 0
			right = i
			# add data point
			if (right - left) != 0:
				rate = (bytes*8.0/1000000)/(right-left)
				x.append(i)
				y.append(rate)
				if not maxY or rate > maxY:
					maxY = int(rate) + 1
			i += 0.1
		
		plot(x,y)

		# Plot rate for flow 1
		x = []
		y = []
		i = 0
		while i < self.max_time:
			bytes = 0
			# loop through array of data and find relevant data
			for (t,sequence,size) in self.data5:
				if (t >= i - 1) and (t <= i):
					bytes += size
			# compute interval
			left = i - 1
			if i - 1 < 0:
				left = 0
			right = i
			# add data point
			if (right - left) != 0:
				rate = (bytes*8.0/1000000)/(right-left)
				x.append(i)
				y.append(rate)
				if not maxY or rate > maxY:
					maxY = int(rate) + 1
			i += 0.1
		
		plot(x,y)

		xlabel('Time (seconds)')
		ylabel('Rate (Mbps)')
		ylim([0,maxY])
		savefig(self.output_file + '.png')

def parse_options():
		# parse options
		parser = optparse.OptionParser(usage = "%prog [options]",
									   version = "%prog 0.1")

		parser.add_option("-f","--input_file",type="string",dest="input_file",
						  default=None,
						  help="input_file")

		parser.add_option("-o","--output_file",type="string",dest="output_file",
						default="rate",
						help="output_file_name")

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
