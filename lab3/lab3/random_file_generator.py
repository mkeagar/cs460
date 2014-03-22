import random

characters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', \
			'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X' ,'Y', 'Z', \
			'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')']

print "\nPlease enter a file size in bytes:"
filesize = int(raw_input())

print "\nPlease enter a filename:"
filename = raw_input()

myfile = open(filename, 'w')

for i in xrange(filesize-1):
	c = random.choice(characters)
	myfile.write(c)
	myfile.flush()

myfile.write("\n")
myfile.flush()
myfile.close()