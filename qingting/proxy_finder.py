from bs4 import BeautifulSoup
import queue,  time, threading, os, random, requests

class Proxy_finder:

    def __init__(self):
        self.baseUrl = 'https://www.xicidaili.com/nn/{}'
        self.page = 1

    def get_next_proxy_list(self):
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134'
        html = requests.get(url=self.baseUrl.format(self.page), headers={'User-Agent': user_agent}).text
        self.page = self.page + 1
        soup = BeautifulSoup(html, 'html.parser')
        ips = soup.find(id='ip_list').find_all('tr')
        ip_list = []
        for i in range(1, len(ips)):
            ip_info = ips[i]
            tds = ip_info.find_all('td')
            # ip_list.append(tds[1].text + ':' + tds[2].text)
            ip = tds[1].text
            port = tds[2].text
            https = tds[5].text
            speed = float(tds[6].find('div').attrs['title'][:-1])
            connection = float(tds[7].find('div').attrs['title'][:-1])

            a_proxy = {'ip': ip, 'port': port, 'https': https,
                       'speed': speed, 'connection': connection}
            ip_list.append(a_proxy)

        return ip_list

if __name__ == "__main__":
    pf = Proxy_finder()
    ip_list = pf.get_next_proxy_list()
    print(ip_list)

    ip_list = pf.get_next_proxy_list()
    print(ip_list)

    ip_list = pf.get_next_proxy_list()
    print(ip_list)
