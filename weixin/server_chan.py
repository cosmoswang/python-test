import requests, weinxin_token

def send_shortmsg(msg):
	data = {'text' : msg}
	resp = requests.post('https://sc.ftqq.com/{}.send'.format(weinxin_token.token), data=data)
	print(resp)

def send_longmsg(msg, desc):
	data = {'text' : msg, 'desp' : desc}
	resp = requests.post('https://sc.ftqq.com/{}.send'.format(weinxin_token.token), data=data)
	print(resp)

if __name__ == "__main__":
	send_longmsg('长文本，带mark down', """This paragraph contains a list of items.
 
* Item 1
 
* Item 2
 
* Item three
	""")