# -*- coding: utf-8 -*-
import urllib3
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import queue,  time, threading, os, random, requests

class Downloader:

	def __init__(self, name):
		self.name = name
		self.queue = queue.Queue()
		self.use_agent = True

	def check_exists(self, title):
		files = os.listdir(self.path)
		for f in files:
			if f.count(title) > 0:
				return True

		return False
		
	def start(self):
		self.t = threading.Thread(target=self.__deamon_thread_target, args=[self.queue])
		self.t.start()
		user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134'
		self.manager = urllib3.PoolManager(headers={'User-Agent': user_agent})
		self.path = './qingting/.res/{}'.format(self.name)
		if not os.path.exists(self.path):
			os.makedirs(self.path)

	def end(self):
		self.queue.put('EOF')
	
	def download(self, url):
		self.queue.put(url)

	def __download(self, url):
		if self.use_agent:
			proxy = self.get_random_ip(self.get_ip_list())
			print('使用代理{}下载{}'.format(proxy['http'], url['title']))
			user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134'
			p_manager = urllib3.ProxyManager(proxy['http'], headers={'connection': 'keep-alive', 'User-Agent': user_agent})
			r = p_manager.request('get', url['url'])
		else:
			r = self.manager.request('get', url['url'])
		if r.status == 200:
			file = os.path.join(self.path, '{}-{}.m4a'.format(url['title'], url['timelong']))
			with open(file, 'wb') as f:
				f.write(r.data)
		else:
			print('--------download {} failed'.format(r.status))
		
	def __deamon_thread_target(self, qu):
		with ThreadPoolExecutor(3) as executor:
			while True:
				e = qu.get()
				if e == 'EOF':
					break
				executor.submit(self.__download, e)
	
	def get_ip_list(self):
		url = 'http://www.xicidaili.com/wt/'
		user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134'
		html = requests.get(url=url, headers={'User-Agent': user_agent}).text
		soup = BeautifulSoup(html, 'html.parser')
		ips = soup.find(id='ip_list').find_all('tr')
		ip_list = []
		for i in range(1, len(ips)):
			ip_info = ips[i]
			tds = ip_info.find_all('td')
			ip_list.append(tds[1].text + ':' + tds[2].text)
		return ip_list

	def get_random_ip(self,ip_list):
		proxy_list = []
		for ip in ip_list:
			proxy_list.append('http://' + ip)
		proxy_ip = random.choice(proxy_list)
		proxies = {'http': proxy_ip}
		return proxies


def main():
	urls = [
		{
			'title':
			'97 罗斯福：欲戴王冠，必承其重！',
			'url':
			'https://od.sign.qingting.fm/m4a/5be426047cb8910340086a20_11079962_24.m4a?sign=63c95e6dd590c332aab9c844a99a51ac&t=5c02c877'
		},
		{
			'title':
			'96 罗斯福：连任四届总统，没人比我更优秀了吧？',
			'url':
			'https://od.sign.qingting.fm/m4a/5be01abe7cb891034158cd7a_11056225_24.m4a?sign=f426b42c46f896665706872164886ae1&t=5c02c8f1'
		},
		{
			'title':
			'95 马汉：一生悬命海军带美国出人头地，身后却受冷待',
			'url':
			'https://od.sign.qingting.fm/m4a/5bdadbf97cb891034158af65_11033945_24.m4a?sign=a570f9892dcb8db027f7418941700c5a&t=5c02c929'
		}
	]

	downloader = Downloader('test')
	downloader.start()
	
	for url in urls:
		downloader.download(url)

	downloader.end()

if __name__ == "__main__":
	main()