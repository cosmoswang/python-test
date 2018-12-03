# -*- coding: utf-8 -*-
import urllib3

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

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134'

manager = urllib3.PoolManager(headers={'User-Agent': user_agent})

for url in urls:
	r = manager.request('get', url['url'])
	if r.status == 200:
		print(type(r.data))
		with open('./qingting/.res/m4a/{}.m4a'.format(url['title']), 'wb') as f:
			f.write(r.data)
