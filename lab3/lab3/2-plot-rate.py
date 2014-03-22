import optparse
import sys

import matplotlib
from pylab import *

# Parse a file of rates and plot a smoothed graph. The rate is smoothed
# by summing all the bytes sent over a 1 second interval, and sliding
# the window every 0.1 seconds.
class Plotter:
    def __init__(self,file):
        """ Initialize plotter with a file name. """
        self.file = file
        self.data1 = []
        self.data2 = []
        self.min_time = None
        self.max_time = None

    def parse(self):
        """ Parse the data file """
        first = None
        f = open(self.file)
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
                else:
                    self.data2.append((t,sequence,size))
            # Keep track of the minimum and maximum time seen
            if not self.min_time or t < self.min_time:
                self.min_time = t
            if not self.max_time or t > self.max_time:
                self.max_time = t

    def plot(self):
        """ Create a line graph of the rate over time for flow 1 and 2. """
        clf()
        x = []
        y = []
        i = 0
        max = None
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
                if not max or rate > max:
                    max = int(rate) + 1
            i += 0.1
        
        plot(x,y)

        x = []
        y = []
        i = 0
        max = None
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
                if not max or rate > max:
                    max = int(rate) + 1
            i += 0.1
        
        plot(x,y)

        xlabel('Time (seconds)')
        ylabel('Rate (Mbps)')
        ylim([0,max])
        savefig('2-rate.png')

def parse_options():
        # parse options
        parser = optparse.OptionParser(usage = "%prog [options]",
                                       version = "%prog 0.1")

        parser.add_option("-f","--file",type="string",dest="file",
                          default=None,
                          help="file")

        (options,args) = parser.parse_args()
        return (options,args)


if __name__ == '__main__':
    (options,args) = parse_options()
    if options.file == None:
        print "plot.py -f file"
        sys.exit()
    p = Plotter(options.file)
    p.parse()
    p.plot()
