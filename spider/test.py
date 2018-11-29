import time, os, uuid

ts = 154293788076 / 100
dt = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ts))
print(dt)

list = os.listdir('./spider/output')
list.sort(reverse=True)
	
filenames = ['test.log', '.log', 'ad.dfsdf.exe', 'C:/dsf/root/.log', 'C:/dsf/root/ad.log']
for filename in filenames:
	print(os.path.splitext(filename))

a = 10
i = 1
while i < 5:
	i += 1
	a = 1

print(a) 

print(str(uuid.uuid1()))