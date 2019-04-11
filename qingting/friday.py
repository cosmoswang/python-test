from selenium import webdriver
from selenium.webdriver.common.by import By
import json, time, sys, requests
import downloader, proxy_finder

def main1(start):
    try:
        driver = webdriver.Edge()
        driver.get('http://www.audio69.com/book/415.html')

        plist = driver.find_elements(By.XPATH, '//*[@id="wrapper"]/div/div/div/div[4]/div/ul/li')

        # dl = downloader.Downloader('friday')
        # dl.start()
        array = []
        for li in plist:
            # print(li.text)
            a = li.find_element(By.TAG_NAME, 'a')
            # href = a.get_attribute('href')
            epsode = li.text
            a.click()
            open_page(driver, epsode)
            driver.back()
        
    finally:
        # dl.end()
        driver.quit()

def main2(start):
    try:
        driver = webdriver.Edge()
        url_patten = 'http://www.audio69.com/book/415/{}.html'

        with open('./urls.txt', 'w') as f:
            for i in range(661):
                driver.get(url_patten.format(i))
                source = driver.find_element(By.XPATH, '//*[@id="wrapper"]/div/div/div/div[2]/div[1]/audio/source')
                src = source.get_attribute('src')
                # print('{:0>3} - {}'.format(i, src))
                f.write('{:0>3} - {}\n'.format(i, src))
    finally:
        driver.quit()

def open_page(driver, epsode):
    # driver.implicitly_wait(30)
    print('-------------------------')
    time.sleep(2)
    print('2222222222222222222222222')
    source = driver.find_element(By.XPATH, '//*[@id="wrapper"]/div/div/div/div[2]/div[1]/audio/source')
    src = source.get_attribute('src')
    # dl.download({
	# 		'title': epsode,
	# 		'url': src
	# 	})
    print('{} - {}'.format(epsode, src))

def main():
    urls = []
    with open('./qingting/friday_urls.txt', 'r') as fd:
        urls = fd.readlines()

    pf = proxy_finder.Proxy_finder()
    print('--- 获取代理列表')
    ip_list = pf.get_next_proxy_list()
    ip_list.reverse()

    for url in urls:
        url = url.rstrip()
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134'
        proxy = ''

        while True:
            if len(ip_list) == 0:
                print('--- 获取代理列表')
                ip_list = pf.get_next_proxy_list()
                ip_list.reverse()
            proxy = ip_list.pop()
            if proxy['https'] == 'HTTP' or proxy['connection'] < 1:
                break

        # print('使用代理 http://{}:{}下载文件{}'.format(proxy['ip'], proxy['port'], url))
        print('开始下载{}'.format(url))

        while True:
            while True:
                if len(ip_list) == 0:
                    print('--- 获取代理列表')
                    ip_list = pf.get_next_proxy_list()
                    ip_list.reverse()
                proxy = ip_list.pop()
                if proxy['https'] == 'HTTP' or proxy['connection'] < 1:
                    break

            print('\t正在使用代理 http://{}:{}下载'.format(proxy['ip'], proxy['port']))
            r = download(url, user_agent, 'http://{}:{}'.format(proxy['ip'], proxy['port']), 6)
            if r != None:
                print('\t下载成功')
                filename = url[url.rfind('/') + 1:]
                with open('./qingting/.res/friday/{}'.format(filename), 'wb') as w:
                    w.write(r.content)

                break
            else:
                print('\t下载失败，正在重试')

def download(url, user_agent, proxy_str, timeout):
    try:
        return requests.get(url=url, headers={'User-Agent': user_agent}, proxies={'http': proxy_str}, timeout=timeout)
    except (requests.ConnectionError, requests.HTTPError, requests.Timeout):
        return None
if __name__ == "__main__":
    main()