from concurrent.futures import ThreadPoolExecutor
import queue,  time, threading

def customer(e):
	time.sleep(1)
	print(e)

def deamon_thread_target(qu):
	with ThreadPoolExecutor(3) as executor:
		while True:
			e = qu.get()
			if e == 'EOF':
				break
			executor.submit(customer, e)

q = queue.Queue()

# t = threading.Thread(target=deamon_thread_target, args=[q])
# t.start()

time.sleep(5)

q.put('1')
q.put('2')
q.put('3')
q.put('4')
q.put('5')
q.put('6')
q.put('7')
q.put('8')
q.put('9')
q.put('10')
q.put('11')
q.put('12')
q.put('EOF')
