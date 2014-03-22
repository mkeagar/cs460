import subprocess

banner = "********************************************\n" \
		"*                                          *\n" \
		"*   Lab 2: Reliable Transport - Testing    *\n" \
		"*                                          *\n" \
		"********************************************\n"

print banner

print "**************** Test Set 1 ****************"

print "\n[ 1: 0% loss, Bandwidth: 10 Mbps, d_prop: 10 ms, Window size: 3 packets (3000 bytes) ]\n"
args = ['python', 'transfer.py', '--loss', '0.0','--filename', 'test.txt', '--window_size', '3']
result = subprocess.Popen(args,stdout = subprocess.PIPE).communicate()[0]
print result
print "\n[ End 1 ]\n"

print "[ 2: 10% loss, Bandwidth: 10 Mbps, d_prop: 10 ms, Window size: 3 packets (3000 bytes) ]\n"
args = ['python', 'transfer.py', '--loss', '0.1','--filename', 'test.txt', '--window_size', '3']
result = subprocess.Popen(args,stdout = subprocess.PIPE).communicate()[0]
print result
print "\n[ End 2 ]\n"

print "[ 2: 20% loss, Bandwidth: 10 Mbps, d_prop: 10 ms, Window size: 3 packets (3000 bytes) ]\n"
args = ['python', 'transfer.py', '--loss', '0.2','--filename', 'test.txt', '--window_size', '3']
result = subprocess.Popen(args,stdout = subprocess.PIPE).communicate()[0]
print result
print "\n[ End 3 ]\n"

print "[ 2: 50% loss, Bandwidth: 10 Mbps, d_prop: 10 ms, Window size: 3 packets (3000 bytes) ]\n"
args = ['python', 'transfer.py', '--loss', '0.5','--filename', 'test.txt', '--window_size', '3']
result = subprocess.Popen(args,stdout = subprocess.PIPE).communicate()[0]
print result
print "\n[ End 4 ]\n"


print "**************** Test Set 2 ****************"

print "\n[ 1: 0% loss, Bandwidth: 10 Mbps, d_prop: 10 ms, Window size: 10 packets (10000 bytes) ]\n"
args = ['python', 'transfer.py', '--loss', '0.0','--filename', 'internet-architecture.pdf', '--window_size', '10']
result = subprocess.Popen(args,stdout = subprocess.PIPE).communicate()[0]
print result
print "\n[ End 1 ]\n"

print "[ 2: 10% loss, Bandwidth: 10 Mbps, d_prop: 10 ms, Window size: 10 packets (10000 bytes) ]\n"
args = ['python', 'transfer.py', '--loss', '0.1','--filename', 'internet-architecture.pdf', '--window_size', '10']
result = subprocess.Popen(args,stdout = subprocess.PIPE).communicate()[0]
print result
print "\n[ End 2 ]\n"

print "[ 2: 20% loss, Bandwidth: 10 Mbps, d_prop: 10 ms, Window size: 10 packets (10000 bytes) ]\n"
args = ['python', 'transfer.py', '--loss', '0.2','--filename', 'internet-architecture.pdf', '--window_size', '10']
result = subprocess.Popen(args,stdout = subprocess.PIPE).communicate()[0]
print result
print "\n[ End 3 ]\n"

print "[ 2: 50% loss, Bandwidth: 10 Mbps, d_prop: 10 ms, Window size: 10 packets (10000 bytes) ]\n"
args = ['python', 'transfer.py', '--loss', '0.5','--filename', 'internet-architecture.pdf', '--window_size', '10']
result = subprocess.Popen(args,stdout = subprocess.PIPE).communicate()[0]
print result
print "\n[ End 4 ]\n"

banner = "********************************************\n" \
		"*                                          *\n" \
		"*               End Testing                *\n" \
		"*                                          *\n" \
		"********************************************\n"

print banner