import optparse
import sys

import matplotlib
from pylab import *

# Parses a file of rates and plot a sequence number graph. Black
# squares indicate a sequence number being sent and dots indicate a
# sequence number being ACKed.
class Plotter:
    def __init__(self,file):
        """ Initialize plotter with a file name. """
        self.file = file
        self.data1 = []
        self.data2 = []
        self.ack1 = []
        self.ack2 = []
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
            flow = int(flow)
            t = float(t)
            sequence = int(sequence)
            if size != "x":
                size = int(size)
            if size == 0:
                if flow == 1:
                    self.ack1.append((t, sequence))
                else:
                    self.ack2.append((t, sequence))
            else:
                if flow == 1:
                    self.data1.append((t,sequence,size))
                else:
                    self.data2.append((t,sequence,size))

            if not self.min_time or t < self.min_time:
                self.min_time = t
            if not self.max_time or t > self.max_time:
                self.max_time = t

    def plot(self):
        """ Create a sequence graph of the packets. """
        clf()
        figure(figsize=(15,5))
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
        scatter(dropX,dropY,marker='x', color='orange')
        scatter(ackX,ackY,marker='s',s=0.2, color='blue')

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
        scatter(dropX,dropY,marker='x', color='green')
        scatter(ackX,ackY,marker='s',s=0.2, color='red')

        xlabel('Time (seconds)')
        ylabel('Sequence Number Mod 1500')
        xlim([-0.001,self.max_time + 0.01])
        ylim([-1000, 60000])
        savefig('2-sequence.png')

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
