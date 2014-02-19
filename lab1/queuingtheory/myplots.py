import optparse
import sys
import os

import matplotlib
matplotlib.use('Agg')
from pylab import *

# Class that parses a file and plots several graphs
class Plotter:
	def __init__(self):
		self.x = [ 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95, 0.98]
		self.xPercent = []
		for num in self.x:
			self.xPercent.append(str(num) + "%")
		
		self.loads = [10, 20, 30, 40, 50, 60, 70, 80, 90, 95, 98]
		self.queuing = []
		self.averages = []
		self.prefixes = ["queuing"]
		self.ext = ".out"
		
		for prefix in self.prefixes:
			vals = []
			for load in self.loads:
				lines = open(prefix + str(load) +self.ext)
				things = []
				totalDelay = 0.0
				for line in lines:
					thing = float(line.split()[-1])
					things.append(thing)
					totalDelay = totalDelay + thing
				vals.append(things)
				average= totalDelay / len(things)
				self.averages.append(average)
			if prefix == "queuing":
				self.queuing = vals

	def combinedQueuingBoxPlot(self):
		""" Boxplot for queuing delay """
		R = 1000000.0
		L = 8000.0
		mu = R / L
		clf()
		x = np.arange(0,1.0,0.01)
		plot(x, 1/(2*mu)*(x/(1-x)), label="theory", color="Orange")	# Queuing delay theoretical values
		boxplot(self.queuing, positions=self.x, widths=0.05)
		xticks(self.x, rotation=35)
		xlim(0, 1.0)
		xlabel('Utilization')
		ylabel('Queuing Delay')
		legend(loc=0)
		savefig('QueuingDelayBoxplot.png')
		
	def averagesPlot(self):
		""" Line plot of Average for queuing delay """
		R = 1000000.0
		L = 8000.0
		mu = R / L
		clf()
		x = np.arange(0,1.0,0.01)
		plot(x, 1/(2*mu)*(x/(1-x)), label="theory", color="Orange") # Queuing delay theoretical values
		plot(self.x, self.averages, label="simulation", color="Green")
		xticks(self.x, rotation=35)
		xlim(0, 1.0)
		xlabel('Utilization')
		ylabel('Queuing Delay')
		legend(loc=0)
		savefig('QueuingDelayAverages.png')

if __name__ == '__main__':
	p = Plotter()
	p.combinedQueuingBoxPlot()
	p.averagesPlot()
