#!/usr/bin/env python3
# coding=utf-8

import os, socket, sys, threading, getopt
from concurrent.futures import ThreadPoolExecutor, as_completed

def main(ip, from_port=1, to_port=65535, threads_count=100):
	ports_opened = []
	
	with open('./result_{}'.format(ip), 'w') as f:
		print('checking ports on {}, in range({}, {}), with {} threads'.format(ip, from_port, to_port, threads_count))
		f.write('checking ports on {}, in range({}, {}, with {} threads)'.format(ip, from_port, to_port, threads_count))
		with ThreadPoolExecutor(threads_count) as exe:
			# exe.daemon = True
			for port in range(from_port, to_port):
				exe.submit(testport, ip, port, ports_opened, f)


		print(2)
		f.write(str(ports_opened) + "\n")



def testport(ip, port, ports_opened, f):
	# print('[THREAD:{}]  -  port {} opening'.format(threading.currentThread().name, port))
	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
	try: 
		s.connect((ip, port)) 
		s.shutdown(2) 
		ports_opened.append(port)
		f.write('[THREAD : {}]\t-\tport {} opened\n'.format(threading.currentThread().name, port))
	except:
		f.write('[THREAD : {}]\t-\tport {} not opened\n'.format(threading.currentThread().name, port))

def usage():
	print("""usage : {} [-f | --fromport <fromport>] [-t | --toport <toport>] [-c | --threadscount <thread_count>] address
    """.format(os.path.basename(sys.argv[0])))

if __name__ == "__main__":
	try:
		opts, args = getopt.getopt(sys.argv[1:], "hf:t:c:", ["fromport=", "toport=", "threadscount=", "help"])
	except getopt.GetoptError as err:
		print(err)
		usage()
		sys.exit(2)
	
	if len(opts) == 0 and len(args) == 0:
		usage()
		sys.exit(0)
	
	ip = 'localhost'
	from_port = 1
	to_port = 65535
	threads_count = 20

	if len(args) > 0:
		ip = args[0]
	for o, a in opts:
		if o in ("-h", "--help"):
			usage()
			sys.exit()
		elif o in ("-f", "--fromport"):
			from_port = int(a)
		elif o in ("-t", "--toport"):
			to_port = int(a)
		elif o in ("-c", "--threadscount"):
			threads_count = int(a)
		else:
			assert False, "unhandled option"

	main(ip, from_port, to_port, threads_count)

