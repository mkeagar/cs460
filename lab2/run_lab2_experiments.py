import subprocess

banner = "********************************************\n" \
		"*                                          *\n" \
		"*  Lab 2: Reliable Transport - Experiments *\n" \
		"*                                          *\n" \
		"********************************************\n"
print banner

print "\n[ 1: 0% loss, Bandwidth: 10 Mbps, d_prop: 10 ms, Window size: 1 packets (1000 bytes) ]\n"
args = ['python', 'transfer.py', '--loss', '0.0','--filename', 'internet-architecture.pdf', '--window_size', '1']
result = subprocess.Popen(args,stdout = subprocess.PIPE).communicate()[0]
print result
print "\n[ End 1 ]\n"

print "\n[ 2: 0% loss, Bandwidth: 10 Mbps, d_prop: 10 ms, Window size: 2 packets (2000 bytes) ]\n"
args = ['python', 'transfer.py', '--loss', '0.0','--filename', 'internet-architecture.pdf', '--window_size', '2']
result = subprocess.Popen(args,stdout = subprocess.PIPE).communicate()[0]
print result
print "\n[ End 2 ]\n"

print "\n[ 3: 0% loss, Bandwidth: 10 Mbps, d_prop: 10 ms, Window size: 5 packets (5000 bytes) ]\n"
args = ['python', 'transfer.py', '--loss', '0.0','--filename', 'internet-architecture.pdf', '--window_size', '5']
result = subprocess.Popen(args,stdout = subprocess.PIPE).communicate()[0]
print result
print "\n[ End 3 ]\n"

print "\n[ 4: 0% loss, Bandwidth: 10 Mbps, d_prop: 10 ms, Window size: 10 packets (10000 bytes) ]\n"
args = ['python', 'transfer.py', '--loss', '0.0','--filename', 'internet-architecture.pdf', '--window_size', '10']
result = subprocess.Popen(args,stdout = subprocess.PIPE).communicate()[0]
print result
print "\n[ End 4 ]\n"

print "\n[ 5: 0% loss, Bandwidth: 10 Mbps, d_prop: 10 ms, Window size: 15 packets (15000 bytes) ]\n"
args = ['python', 'transfer.py', '--loss', '0.0','--filename', 'internet-architecture.pdf', '--window_size', '15']
result = subprocess.Popen(args,stdout = subprocess.PIPE).communicate()[0]
print result
print "\n[ End 5 ]\n"

print "\n[ 6: 0% loss, Bandwidth: 10 Mbps, d_prop: 10 ms, Window size: 20 packets (20000 bytes) ]\n"
args = ['python', 'transfer.py', '--loss', '0.0','--filename', 'internet-architecture.pdf', '--window_size', '20']
result = subprocess.Popen(args,stdout = subprocess.PIPE).communicate()[0]
print result
print "\n[ End 6 ]\n"

banner = "********************************************\n" \
		"*                                          *\n" \
		"*             End Experiments              *\n" \
		"*                                          *\n" \
		"********************************************\n"

print banner