import optparse
import sys
import os

import matplotlib
matplotlib.use('Agg')
from pylab import *

# Class that parses a file and plots several graphs
class Plotter:
	def __init__(self):
		self.window_size = []
		self.loads = ["_data"]
		self.throughput = []
		self.avg_queuing = []
		self.prefixes = ["experiment"]
		self.ext = ".txt"
		
		for prefix in self.prefixes:
			for load in self.loads:
				lines = open(prefix + load + self.ext)
				for line in lines:
					line_array = line.split()
					self.window_size.append(int(line_array[0]))
					self.avg_queuing.append(float(line_array[1]))
					self.throughput.append((float(line_array[-1]) * 8) / float(line_array[-2]) / 1000000)

	def throughputLinePlot(self):
		""" Line plot for throughput """
		plot(self.window_size, self.throughput, label = "Throughput vs Window Size")
		xticks(self.window_size)
		xlim(0, 21)
		xlabel('Window Size (No. of Packets)')
		ylabel('Throughput in Mbps')
		legend(loc=0)
		savefig('ThroughputLinePlot.png')
		
	def averageQueuingDelay(self):
		""" Line plot for throughput """
		plot(self.window_size, self.avg_queuing, label = "Average Queuing Delay vs Window Size")
		xticks(self.window_size)
		xlim(0, 21)
		xlabel('Window Size (No. of Packets)')
		ylabel('Avg. Queuing Delay (seconds)')
		legend(loc=0)
		savefig('AvgQueuingDelayLinePlot.png')

if __name__ == '__main__':
	p = Plotter()
	# p.throughputLinePlot()
	p.averageQueuingDelay()
